---
tags: [ultimate, awakening, cutscene, vfx, sound, camera, combat]
updated: 2026-10-31
sources: 10
status: draft
---
# Ultimate and Awakening Sequences

## TL;DR
- Two kinds: an **ultimate/cutscene move** (a single cinematic attack, 2–6 s, usually a grab or lock-on) and an **awakening** (a transformation into a buffed mode, with a short activation cinematic followed by a timed state).
- Structure everything as a **5-beat timeline**: *trigger (lock) → wind-up/charge → strike (impact frame + hitstop) → aftermath → release*. Budget **≤ 1 s of lost control before damage** in PvP.
- One **server-authoritative timeline** (who is locked, damage at time T), with **client-side presentation** (animation, camera, VFX, sound) cued by KeyframeMarkers on the attacker's Action4 track.
- Real-game references: in Jujutsu Shenanigans, everyone inside a domain is **immobile during the domain cutscene** while a popup explains it. In Heroes Battlegrounds, **cutscene moves pause the user's ultimate bar drain** (not the enemy's), and Symbol of Fear does 46% base, rising to 100% if on-screen prompts are hit (a QTE).
- Non-participants must **keep playing**. Cinematic camera only for the attacker + victim(s), or for players inside the domain radius.

## Why it matters for anime battlegrounds
Ultimates and awakenings are the shareable moment: clips, thumbnails, the "anime" promise of the genre. They are also where most desync, softlock and "cutscene abuse" bugs live, so you need a disciplined timeline.

## Anatomy and time budget
| Beat | Ultimate (grab cutscene) | Awakening activation | What happens |
|---|---|---|---|
| 0. Trigger | 0 s | 0 s | Input → server validates meter, range, grab hit |
| 1. Lock / grab | 0.1–0.3 s | 0.1–0.2 s | Anchor or weld victim, i-frames on both, Action4 tracks start |
| 2. Wind-up / charge | 0.5–1.5 s | 0.8–2.0 s | Close-up camera, aura VFX, voice line, music sting |
| 3. Strike | 0.2–0.6 s per hit | 0.2–0.4 s (power-up burst) | Stepped strike, smear, **impact frame** |
| 4. Impact hold | 0.25–0.5 s | 0.2–0.4 s | Hitstop 15–30f, Explosion shake, flash |
| 5. Aftermath / release | 0.5–1.2 s | 0.4–0.8 s | Wide shot, victim launched or ragdolled, camera returns |
| **Total** | **≈2–4.5 s** | **≈1.7–3.8 s** | |

> [!warning] Unverified
> These budgets are design recommendations. TSB/JJS/HBG ultimate lengths weren't frame-counted from reachable sources. A techwiser table lists JJS domain *durations* (Infinite Void 14 s, Malevolent Shrine 18 s), but its labelling is unclear and the game updates often.

## Step 1: Server timeline (authority)
```lua
-- Server: UltimateRunner (sketch)
local function runUltimate(attacker, victim, def)
    setInvulnerable(attacker, true); setInvulnerable(victim, true)
    lockCharacter(attacker); lockCharacter(victim)           -- anchor root or weld to attacker
    UltCue:FireAllClients(attacker, victim, def.id, workspace:GetServerTimeNow())
    for _, hit in def.hits do                                 -- { t = 1.35, dmg = 12 }, ...
        task.wait(hit.t - elapsed())                          -- same times as the animation markers
        applyDamage(victim, hit.dmg)
    end
    task.wait(def.length - elapsed())
    unlockCharacter(attacker); unlockCharacter(victim)
    setInvulnerable(attacker, false); setInvulnerable(victim, false)
    applyKnockback(victim, def.finalKnockback)
end
```
- **Damage times = marker times.** Export marker times from the animation (`track:GetTimeOfKeyframe` or a marker table) into `def.hits` so animators retiming doesn't desync damage.
- Always have a **failsafe unlock** (`task.delay(def.length + 1, unlockAll)`) in case of errors, deaths or leaving players.
- Decide the interruption policy: full i-frames for participants is the norm. Bystanders can't interrupt.

## Step 2: Client presentation (every client)
On `UltCue`:
1. Compute the offset `elapsed = GetServerTimeNow() - serverStart`, then start the attacker and victim tracks at `TimePosition = elapsed` (late joiners catch up).
2. **Participants and nearby players**: start the cutscene camera (see [[Camera Work for Abilities]]). Others: optional distance-based shake only.
3. Drive VFX and sound from **markers** on the attacker track (`VFX`, `Sound`, `ImpactFrame`, `Hit`).
4. Set `Animator.PreferLodEnabled = false` on both rigs for the duration, so remote characters aren't LOD-throttled mid-cinematic. Restore it after.
5. Preload: animation, sound and texture assets for each character's ultimate when the character is selected, not on cast.

| Layer | Driven by | Notes |
|---|---|---|
| Attacker anim | Action4 track | One long asset, or several chained via markers |
| Victim anim | Action4 track (paired asset) | Authored together in Moon Animator 2 |
| Camera | Baked CFrame table, relative to attacker root | Hard cuts between shots |
| VFX | Markers → emit/enable | See [[Anime VFX Fundamentals]] |
| Sound | Markers → `Sound:Play()` | Voice + whoosh + impact + music sting |
| Screen FX | Markers → impact frame (black/white invert 2–6 frames), speed lines, letterbox | |
| Hitstop | `Hit` marker → local freeze | See [[Hitstop, Hit Reactions and Knockback]] |

## Step 3: Authoring the paired animation
1. In Moon Animator 2, put the attacker at the origin facing −Z and the victim at a fixed offset (e.g. 4 studs in front), plus a camera track.
2. Animate both rigs and the camera together. Export each rig's KeyframeSequence and the camera frames.
3. At runtime, **snap the victim to `attackerRoot.CFrame * offset`** at lock time so the paired animation lines up.
4. Use stepped timing for strikes and smooth for camera moves *within* a shot. See [[Anime Combat Animation Timing]].

## Step 4: Awakening specifics
- **Activation cinematic** (1.5–4 s, recommendation) → **stance swap**: new idle/run IDs, new M1 set, aura VFX loop, UI meter.
- Duration is driven by a draining bar. In HBG, cutscene moves pause the user's own bar drain until the cutscene ends.
- TSB-style games tie the awakening bar to damage dealt/taken (genre convention).

> [!warning] Unverified
> TSB awakening duration/meter rules weren't found in reachable sources.

- On awakening end: crossfade back to the base stance (`fadeTime` 0.2–0.3 s), stop the aura loops, restore locomotion IDs.

## Step 5: Domain-style (area) ultimates
JJS pattern: the area cutscene **freezes everyone inside** and shows a popup explaining the domain, then everyone is free inside the domain arena.
- Capture the set of players inside the radius on the server at cast time. Only they get the cinematic camera and immobilisation.
- Keep the shared cutscene **≤ 3–4 s** (recommendation). Locking out up to 10+ players for longer feels bad.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Track priority | Action4 | Overrides everything |
| Lost control before damage | ≤ 1 s | PvP fairness (recommendation) |
| Total ultimate length | 2–4.5 s | Recommendation |
| Impact-frame flash | 2–6 render frames | Anime impact frame (recommendation) |
| Final-hit hitstop | 15–30f | See hitstop note |
| Failsafe unlock | length + 1 s | Softlock prevention |
| `PreferLodEnabled` on participants | false during cinematic | Animator docs |

## Checklist
- [ ] Server owns lock, i-frames, damage times, failsafe unlock
- [ ] Damage times generated from animation marker times
- [ ] Clients sync start via `GetServerTimeNow()` offset
- [ ] Cinematic camera only for participants/inside radius; restore on end and cancel
- [ ] Paired victim snapped to the attacker's offset at lock
- [ ] Assets preloaded at character select
- [ ] Awakening swaps locomotion + M1 IDs and restores them cleanly

## Common Mistakes
- Hard-coding `task.wait(1.35)` in scripts while animators retime the animation.
- Locking the whole server's cameras for one player's ultimate.
- No failsafe, so a victim stays anchored forever when the attacker leaves mid-ultimate.
- Victim tracks at Action3 being overridden by their own buffered M1 input. Disable their input too.
- 8-second cutscenes in a 1v1-focused game.

## Related
- [[Camera Work for Abilities]]
- [[Hitstop, Hit Reactions and Knockback]]
- [[Anime Combat Animation Timing]]
- [[Moon Animator 2 vs Blender vs Animation Editor]]
- [[Anime VFX Fundamentals]]
- [[M1 Combo System Design]]

## Sources
1. Sportskeeda: Jujutsu Shenanigans 0.2 domain guide (domain cutscene freezes those inside; popup explanation). https://www.sportskeeda.com/roblox-news/jujutsu-shenanigans-0-2-domain-guide
2. Sportskeeda: JJS beginner's guide to Restless Gambler (domain cutscene explains rules). https://sportskeeda.com/roblox-news/jujutsu-shenanigans-a-beginner-s-guide-restless-gambler
3. TechWiser: All characters in Jujutsu Shenanigans (domain durations, unclear labelling). https://techwiser.com/all-characters-in-jujutsu-shenanigans/
4. Sportskeeda: Heroes Battlegrounds Symbol of Fear guide (46% → 100% with prompts). https://sportskeeda.com/roblox-news/heroes-battleground-symbol-fear-guide
5. Sportskeeda: Heroes Battlegrounds patch notes (cutscene moves pause your ultimate bar). https://www.sportskeeda.com/roblox-news/heroes-battlegrounds-update-17-november-patch-notes
6. Roblox Creator Docs: Animator (PreferLodEnabled, EvaluationThrottled). https://create.roblox.com/docs/reference/engine/classes/Animator
7. Roblox Creator Docs: AnimationTrack (TimePosition, GetTimeOfKeyframe, GetMarkerReachedSignal). https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
8. Roblox Creator Docs: AnimationPriority (Action4 overrides all). https://create.roblox.com/docs/reference/engine/enums/AnimationPriority
9. DevForum: "Moon Animator 2 Camera Animation Scripting" (camera relative to character). https://devforum.roblox.com/t/moon-animator-2-camera-animation-scripting/2427795
10. Animétudes: "The Kanada style now" (impact frames and snappy timing as anime signatures). https://animetudes.com/2021/07/09/the-kanada-style-now/
