---
tags: [combat-feel, hitstop, hit-reaction, knockback, ragdoll, game-feel]
updated: 2026-10-31
sources: 12
status: draft
---
# Hitstop, Hit Reactions and Knockback

## TL;DR
- **Hitstop** (hit freeze, hitlag) briefly freezes attacker *and* victim on contact. Fighting-game references at 60 fps: KOF XIII **7f light / 11f heavy**, GG Strive **11f at attack level 0**. Smash's fan-derived formula scales with damage, roughly `damage/3 + 4–5` frames before multipliers.
- On Roblox: `track:AdjustSpeed(0)` on both characters' current tracks, then restore after N ms. **Run it locally on every client** from a RemoteEvent, because `AdjustSpeed` replication is unreliable and must come from the network owner.
- **Shake the victim during hitstop** (Sakurai: grounded characters vibrate side-to-side, airborne up-and-down), not the attacker. Add a short camera shake and a flash. See [[Camera Work for Abilities]].
- Hit reactions: a **directional flinch** (2–3 variants) at priority **Action3** for normal hits, a **knockback launch** for finishers, and a **ragdoll** for big finishers via `HumanoidStateType.Physics` + BallSocketConstraints.
- Knockback: `LinearVelocity` or `ApplyImpulse` on the HumanoidRootPart, `impulse = AssemblyMass × Δv`. Apply it on the **victim's network owner**, or the server when the victim is an NPC.

## Why it matters for anime battlegrounds
Hitstop is the single biggest "impact" lever. It turns a lerp into a *punch*. Anime adds the held impact pose and the impact frame (see [[Anime VFX Fundamentals]]). Battlegrounds games then chain M1s → knockback or downslam → ragdoll, so reaction animation and physics must hand off cleanly. See [[M1 Combo System Design]].

## Reference values
| Source | Light | Medium | Heavy | Notes |
|---|---|---|---|---|
| KOF XIII (wiki) | 7f hitstop | — | 11f hitstop | 60 fps |
| GG Strive (Dustloop) | Lv0: 11f hitstop, 12f stand hitstun, 9f block | | | Higher levels add more |
| GG Strive counter hits | regular hitstop + **12f slowdown** after it (v1.18 note) | | | Slowdown instead of a longer freeze |
| Smash (SmashWiki, fan-derived) | `⌊⌊⌊d/3 + 4⌋·e⌋·c⌋` (JP) / `+5` (intl.) | | | d = damage %, e/c = move multipliers |

> [!warning] Unverified
> The full GG Strive per-level hitstop table and current Street Fighter 6 hitstop values could not be retrieved (sites blocked from this session). Only the rows above are sourced.

### Recommended starting values for a Roblox battlegrounds game
Network latency means remote players see your hit ~50–150 ms late anyway. Keep hitstop short on M1s so combos don't feel sticky, and long on finishers.

| Hit type | Hitstop (60 fps frames) | ms | Victim shake | Camera shake |
|---|---|---|---|---|
| M1 1–3 | 3–5f | 50–85 ms | 0.05–0.1 stud, side-to-side | none or tiny |
| M1 4 / finisher | 6–9f | 100–150 ms | 0.15 stud | `Bump`-style, short |
| Heavy skill | 8–12f | 133–200 ms | 0.2 stud | medium |
| Ultimate final hit | 15–30f | 250–500 ms | 0.3 stud + impact frame | `Explosion`-style |
| Blocked hit | 2–4f | 33–67 ms | block-pose shake | none |

> [!warning] Unverified
> These are recommendations derived from the fighting-game values above. They are not measured from TSB, JJS or Heroes Battlegrounds.

## How to do it
### Step 1: Mark the contact frame
Add an Animation Event `Hit` on the impact keyframe. Hold the impact pose 3–6 timeline frames after it so a freeze lands on a good pose (see [[Anime Combat Animation Timing]]). DevForum users found that **duplicating the frame right after the marker** keeps the frozen pose stable despite replication delay.

### Step 2: Freeze locally on every client
```lua
-- Client: HitstopController (runs on every client)
local function hitstop(characters: {Model}, duration: number)
    local paused = {}
    for _, char in characters do
        local animator = char:FindFirstChildWhichIsA("Humanoid")
            and char.Humanoid:FindFirstChildOfClass("Animator")
        if animator then
            for _, t in animator:GetPlayingAnimationTracks() do
                paused[t] = t.Speed
                t:AdjustSpeed(0)
            end
        end
    end
    task.delay(duration, function()
        for t, speed in paused do
            if t.IsPlaying then t:AdjustSpeed(speed) end
        end
    end)
end
HitstopRemote.OnClientEvent:Connect(hitstop) -- server fires to all clients on confirmed hit
```
- The attacker's client can freeze **immediately** (prediction) and ignore the server echo.
- Freeze VFX too: set `ParticleEmitter.TimeScale` to 0 (or low) on the hit sparks for the same duration if you want a full freeze-frame.

### Step 3: Shake the victim, not the world
Sakurai (Famitsu column via Source Gaming translation): during hitstop, **grounded** characters vibrate **left-right** and **airborne** characters **up-down**. On Roblox, offset the victim's visual root (e.g. the `RootJoint` C0 or a client-only Motor6D offset) by ±0.05–0.3 studs, alternating every 1–2 frames. Don't move the HumanoidRootPart physically during hitstop.

### Step 4: Play the hit reaction
| Reaction | Priority | Length | Trigger |
|---|---|---|---|
| Flinch (front/back/left/right) | Action3 | 0.25–0.4 s | M1 1–3 |
| Stagger (heavier) | Action3 | 0.5–0.7 s | M1 4 if not launching |
| Launch / knockback pose | Action3 / Action4 | Loops until landing | Finisher, uppercut |
| Downslam bounce | Action4 | 0.3–0.5 s, then ragdoll | Downslam |
| Get-up | Action4 | 0.4–0.8 s | End of ragdoll |
| Block impact | Action (block layer) | 0.15–0.25 s | Blocked hit |

Pick direction from `(attackerPos − victimPos)` in the victim's local space. Stop or override the victim's own attack track when stunned (**priority Action3 > attacks at Action2**).

### Step 5: Knockback
- **Impulse**: `victimRoot:ApplyImpulse(dir * victimRoot.AssemblyMass * speed)`. The impulse acts at the centre of mass (linear only). Higher mass needs more impulse, so read `AssemblyMass` at runtime instead of hard-coding.
- **LinearVelocity** (controlled slide): attach to the root attachment, set `VectorVelocity`, enable force limits (`MaxForce` applies when `ForceLimitsEnabled` and `ForceLimitMode = Magnitude`), and destroy it after 0.15–0.35 s. This gives repeatable distances, which combos need.
- Set `Humanoid.AutoRotate = false` during knockback so the victim doesn't spin to face their input.
- **Network owner matters**: a player's character physics is owned by that player's client. Apply knockback there (RemoteEvent to the victim's client, or server-side with validation), or it gets overwritten.

### Step 6: Ragdoll
- `Humanoid:ChangeState(Enum.HumanoidStateType.Physics)`: "doesn't apply any force on its own and will not automatically transition", so you must set and unset it manually. The old `Ragdoll` state is **deprecated**.
- Replace Motor6Ds with `BallSocketConstraint`s (disable the Motor6D and enable a pre-built constraint between the same attachments), then reverse on get-up.
- Stop all tracks with `animator:GetPlayingAnimationTracks()` before ragdolling, and play the get-up at Action4 after re-enabling the motors.
- `Humanoid.BreakJointsOnDeath` defaults to true. Set it false if you want death ragdolls built on the same system.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| M1 hitstop | 50–85 ms | Snappy chains (recommendation) |
| Finisher hitstop | 100–150 ms | Weight (recommendation) |
| Ultimate final hitstop | 250–500 ms | Climax (recommendation) |
| Victim shake amplitude | 0.05–0.3 studs | Sakurai-style vibration |
| Knockback slide duration | 0.15–0.35 s | Repeatable distance |
| Launch knockback speed | 40–80 studs/s | Reference: default WalkSpeed is 16 studs/s (recommendation) |
| Stun priority | Action3 | Beats Action2 attacks |
| Ragdoll state | `HumanoidStateType.Physics` | Manual control |

## Checklist
- [ ] `Hit` marker + held impact pose on every attack
- [ ] Hitstop runs locally per client, triggered by the server-confirmed hit
- [ ] Victim vibrates during hitstop; attacker holds still
- [ ] Directional flinch set (at least front/back)
- [ ] Knockback applied by the victim's network owner, with AutoRotate off
- [ ] Ragdoll uses the Physics state + BallSockets and cleans up on get-up
- [ ] Blocked hits get shorter hitstop + a block-shake animation

## Common Mistakes
- Freezing only the attacker. Both must freeze.
- Long hitstop on every M1, which makes combos feel like dragging through mud.
- Calling `AdjustSpeed(0)` from the server on a player character and expecting everyone to see it.
- Applying knockback from the attacker's client to the victim (not network owner), so it rubber-bands.
- Using the deprecated `Ragdoll` humanoid state.

## Related
- [[M1 Combo System Design]]
- [[Camera Work for Abilities]]
- [[Anime Combat Animation Timing]]
- [[Anime VFX Fundamentals]]
- [[Roblox Animation System Reference]]

## Sources
1. KOF XIII wiki (SuperCombo mirror): Hitstun/Blockstun state (hitstop 7 light / 11 heavy). https://srk.shib.live/w/The_King_of_Fighters_XIII/Character_States/Hitstun_Blockstun_state
2. Dustloop: GGST AdditionalDataHeader template (Lv0 row). https://www.dustloop.com/w/Template:AdditionalDataHeader-GGST
3. Dustloop: GGST Version 1.18 (counter-hit 12f slowdown). https://www.dustloop.com/w/GGST/Version/1.18
4. SmashWiki: Hitlag (fan-derived formula). https://ssbwiki.com/Hitlag
5. Source Gaming: "Thoughts on Hitstop" (Sakurai Famitsu Vol. 490–491 translation; vibration directions). https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/
6. GoNintendo: Sakurai's game-dev video on 8 hit stop techniques. https://www.gonintendo.com/contents/13581-sakurai-s-latest-game-dev-video-features-8-hit-stop-techniques
7. Roblox Creator Docs: AnimationTrack (AdjustSpeed, Speed). https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
8. DevForum: "How to stop animation at certain time" / "AdjustSpeed working inconsistently" (freeze technique, buffer frame, network owner). https://devforum.roblox.com/t/how-to-stop-animation-at-certain-time/1530098 , https://devforum.roblox.com/t/adjustspeed-working-inconsistently/2643111
9. Roblox Creator Docs: BasePart:ApplyImpulse. https://create.roblox.com/docs/reference/engine/classes/BasePart
10. Roblox Creator Docs: LinearVelocity (MaxForce, ForceLimitMode). https://create.roblox.com/docs/reference/engine/classes/LinearVelocity
11. Roblox Creator Docs: HumanoidStateType (Physics; Ragdoll deprecated). https://create.roblox.com/docs/reference/engine/enums/HumanoidStateType
12. Roblox Creator Docs: Humanoid (AutoRotate, BreakJointsOnDeath, WalkSpeed default 16). https://create.roblox.com/docs/reference/engine/classes/Humanoid
