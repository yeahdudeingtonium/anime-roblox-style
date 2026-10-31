---
tags: [combat, m1, combo, hitbox, block, dash, ragdoll, keyframemarker]
updated: 2026-10-31
sources: 11
status: draft
---
# M1 Combo System Design

## TL;DR
- The battlegrounds pattern: **4 M1s** with short stun between hits, where **M1 #4 is a finisher** (knockback), plus variants: hold **Space/jump on #4 → uppercut**, **in the air → downslam**. DevForum devs describe it as "4–5 M1s, a down slam and an uptilt" or "4 M1s with a little stunlock… that ends with a throw".
- **Animation drives the hitbox**: each M1 has KeyframeMarkers `Hit` (spawn the hitbox query), `CanCancel` (accept the next input or dash), and `End`. The server validates.
- **Block** holds an Action-priority pose, reduces or negates damage, and has its own short hitstop. Guard break or a heavy punishes it. **Dash** (front/side/back) is the movement and escape tool. TSB lets you dash to recover from a knockdown when it isn't on cooldown, and a side dash cancelled into a move becomes a "micro dash".
- Combo-step state: `step = (step % 4) + 1`. **Reset to 1 after ~0.8–1.2 s** without input. Lock out M1s for ~0.6–1.0 s after #4.
- Hit detection: the client detects quickly (`GetPartBoundsInBox`/`GetPartsInPart` or raycast hitboxes), the server checks distance/angle/cooldown. Many devs report desync with naive client hitboxes, so design for it.

## Why it matters for anime battlegrounds
The M1 string is 70%+ of moment-to-moment play in TSB-likes. Combo strings in TSB guides are built from M1s → downslam → uptilt → skills, e.g. "3 M1s, Down Slam, Uppercut, consecutive punches…" (Sportskeeda). If the M1 loop feels bad, no ultimate saves the game.

## State machine
```
Idle ──M1──▶ M1_1 ──CanCancel+M1──▶ M1_2 ──▶ M1_3 ──▶ M1_4 (finisher)
  ▲            │                                     │  ├─ +Space held → Uppercut (launch)
  │            └──── 1.0 s no input ── reset ◀────────┤  └─ airborne → Downslam (ragdoll)
  │                                                  ▼
  └──────────────────── M1 lockout 0.6–1.0 s ◀────────┘
Any state ──hit by enemy──▶ Stunned (Action3) ──▶ Idle
Any state ──F held──▶ Blocking (Action) ──heavy/guardbreak──▶ GuardBroken
Any cancel window ──Q──▶ Dash (front/side/back)
```

## Animation drives it: marker contract
Agree on a marker vocabulary with animators. Every attack asset must contain:

| Marker | Parameter (string) | Purpose |
|---|---|---|
| `Hit` | `"1"` (hit index) or `"dmg=4,kb=0"` | Run the hitbox query on this frame |
| `HitEnd` (optional) | — | For multi-frame active windows (sweep until here) |
| `CanCancel` | — | Accept buffered M1 / dash / skill from here |
| `Smear`, `VFX`, `Sound` | e.g. `"RightArm"` | Cosmetic, client only |
| `End` | — | Return to neutral (or use `Ended`) |

```lua
-- Client: CombatController (simplified)
local M1_TRACKS = {} -- preloaded per character, priority Action2
local step, lastM1, busy, buffered = 0, 0, false, false
local COMBO_RESET, LOCKOUT = 1.0, 0.8

local function doM1()
    if busy then buffered = true return end
    if os.clock() - lastM1 > COMBO_RESET then step = 0 end
    step = step % 4 + 1
    lastM1 = os.clock()
    busy, buffered = true, false
    local track = M1_TRACKS[step]
    track:Play(0.03, 1, 1)
    local c1, c2
    c1 = track:GetMarkerReachedSignal("Hit"):Connect(function(param)
        local targets = queryHitbox(character, step)      -- local, fast
        HitRequest:FireServer(step, targets, workspace:GetServerTimeNow())
    end)
    c2 = track:GetMarkerReachedSignal("CanCancel"):Connect(function()
        busy = false
        if buffered and step < 4 then doM1() end
    end)
    track.Stopped:Once(function()
        c1:Disconnect(); c2:Disconnect()
        if step == 4 then task.delay(LOCKOUT, function() busy = false end) else busy = false end
    end)
end
```
> [!warning] Connect once, not per swing
> In production, connect marker signals **once per track** at load time and route by `step`. The per-play connect above is for readability. Leaking connections is a common bug.

## Hitbox approaches
| Method | How | Pros | Cons |
|---|---|---|---|
| Spatial query box | `workspace:GetPartBoundsInBox(root.CFrame * CFrame.new(0,0,-3), Vector3.new(5,5,5), params)` on `Hit` | Simple, one frame | Can miss on lag |
| Swept query | Repeat the query each frame between `Hit` and `HitEnd` | Covers fast moves | More cost |
| Raycast hitbox (community "Raycast Hitbox 4.0") | Rays from limb attachments each frame | Accurate to the animation | Setup per weapon/limb |
| Server-only | Server runs the query at an estimated time | Exploit-resistant | Feels laggy for the attacker |

Typical sizes (recommendation): M1 box **4–6 studs wide × 5 tall × 4–6 deep**, centred **2.5–3.5 studs** in front of the root. Finisher +1–2 studs depth.

Server validation (minimum):
- Distance attacker→target ≤ hitbox reach + ping allowance (e.g. +3–6 studs).
- Target roughly in front (dot product > 0).
- Step and cooldown consistent with server-side timing.
- Target not in i-frames (dash) and not blocking (or apply block rules).

## Block
| Rule | Value (recommendation) |
|---|---|
| Block anim priority | Action (looping hold) |
| M1 damage while blocking | 0–20% |
| Block hitstop | 2–4f |
| Pushback on block | 1–2 studs |
| Guard break | Finisher or dedicated skill breaks block → 1.0–1.5 s stun |
| Block from behind | Doesn't count (dot product check) |
| Move speed while blocking | ~50% WalkSpeed (default 16 → 8) |

> [!warning] Unverified
> Block damage reduction, guard-break counts and stun lengths in TSB/JJS were not available from sources I could reach. The values above are design starting points.

## Dash
- Directions: front (offensive, long cooldown, leaves you vulnerable per guides), side and back (shorter cooldowns per a TSB guide).
- Implementation: `LinearVelocity` on the root for 0.15–0.3 s, with the dash animation at **Movement or Action** priority (upper body can still attack if it's Movement).
- **Cancel window**: accept a dash from `CanCancel` onward to allow M1 → dash → M1 extensions (TSB combos use shove → dash → M1s).
- **Micro dash**: a side dash cancelled by a skill input stops the velocity early.
- **Knockdown escape**: dash input during a ragdoll ends the ragdoll early if the dash is off cooldown (TSB behaviour per guides).

> [!warning] Unverified
> Exact TSB dash cooldown seconds aren't documented in reachable sources.

## Ragdoll and finishers
- M1 #4 on the ground → knockback launch (see [[Hitstop, Hit Reactions and Knockback]]).
- **Uppercut** (Space on #4) → victim launched up 15–25 studs/s, attacker can follow with an air combo.
- **Downslam** (air #4) → victim slammed down → ragdoll 1.0–2.0 s, then get-up with brief i-frames (0.3–0.5 s) to prevent infinite loops.
- Wall combos: TSB players use walls/trees/trash cans at the end of an M1 string for follow-ups. Detect a wall behind the victim with a raycast along the knockback direction and convert to a "wall splat" stun.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| M1 count | 4 (#4 finisher) | Genre standard (DevForum, TSB guides) |
| Combo reset timeout | 0.8–1.2 s | Forgiving, still rhythmic |
| M1 lockout after #4 | 0.6–1.0 s | Stops infinite strings |
| Stun per M1 | ≥ time to next M1's `Hit` + 0.1 s | Guarantees chain on hit |
| M1 anim priority | Action2 | Over block/move |
| Stun priority | Action3 | Over M1 |
| M1 `Play` fadeTime | 0.02–0.05 s | Snappy |
| Dash duration | 0.15–0.3 s | Burst |
| Get-up i-frames | 0.3–0.5 s | Anti-loop |

## Checklist
- [ ] Marker contract documented and present in every attack asset
- [ ] Tracks preloaded per character; marker signals connected once
- [ ] Input buffer from `CanCancel` (one buffered input)
- [ ] Server validates distance, facing, timing, i-frames, block
- [ ] Stun duration guarantees the next M1 connects (true combo) only while the string is intact
- [ ] Downslam/ragdoll has an escape (dash) and get-up i-frames
- [ ] Combo resets on stun, death and character respawn

## Common Mistakes
- Hitbox spawned on `Play()` instead of the `Hit` marker, so animation and damage desync.
- Using `task.wait(0.2)` timers instead of markers, which breaks when animators retime.
- Stun shorter than the next M1's startup, so the opponent escapes mid-string, or longer than the lockout, so infinites appear.
- No server validation (exploiters hit across the map).
- All tracks at the same priority, so stun and attack blend 50/50.

## Related
- [[Hitstop, Hit Reactions and Knockback]]
- [[Anime Combat Animation Timing]]
- [[Roblox Animation System Reference]]
- [[Anime Locomotion - Idle, Run and Dash]]
- [[Ultimate and Awakening Sequences]]

## Sources
1. DevForum: "What's the best way to approach a battleground combat system?" (hitbox sync, ping). https://devforum.roblox.com/t/hitbox-system-battlegrounds/3194134
2. DevForum: "Combat system - hitboxes" (client GetPartsInPart desync). https://devforum.roblox.com/t/combat-system-hitboxes/3312821
3. DevForum: "Creating basic M1s in a battle ground game". https://devforum.roblox.com/t/creating-basic-m1s-in-a-battle-ground-game/1446335
4. DevForum: "How do you Battlegrounds scripter make Battlegrounds games?" / "Battlegrounds game help" (4–5 M1s, downslam, uptilt). https://devforum.roblox.com/t/how-do-you-battlegrounds-scripter-make-battlegrounds-games/3468609 , https://devforum.roblox.com/t/battlegrounds-game-help/2534505
5. DevForum: "Types of Hitboxes". https://devforum.roblox.com/t/types-of-hitboxes/1897975
6. Sportskeeda: Best TSB one-shot combos (M1 → Down Slam → Uppercut strings). https://hindi3.sportskeeda.com/roblox-news/best-the-strongest-battlegrounds-one-shot-combos
7. ProGameGuides: All character combos for TSB. https://progameguides.com/roblox/all-character-combos-for-the-strongest-battlegrounds-roblox/
8. Bloxodes wiki: TSB techniques (micro dash; punching doesn't cancel dash). https://bloxodes.com/wiki/the-strongest-battlegrounds/techniques
9. NoPing blog: TSB guide (dash to recover from knockdown; side/back dashes have shorter cooldowns). https://noping.com/blog/the-strongest-battlegrounds-tsb-in-roblox
10. Roblox Creator Docs: AnimationTrack:GetMarkerReachedSignal; Animation events. https://create.roblox.com/docs/reference/engine/classes/AnimationTrack , https://create.roblox.com/docs/animation/events
11. NoLeep: How to do wall combo in TSB. https://noleep.com/en/?p=5392
