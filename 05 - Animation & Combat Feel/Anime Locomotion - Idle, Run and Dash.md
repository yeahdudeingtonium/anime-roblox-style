---
tags: [animation, locomotion, idle, run, dash, animate-script]
updated: 2026-10-31
sources: 8
status: draft
---
# Anime Locomotion - Idle, Run and Dash

## TL;DR
- Replace the default `Animate` script's IDs (`idle.Animation1/2`, `walk.WalkAnim`, `run.RunAnim`, `jump`, `fall`, `climb`…). For default-anim replacements, name the final keyframe **`End`**. Defaults and catalog bundles run at **Core** priority, so author yours at **Idle/Movement**.
- **Combat idle** is the most-seen animation in the game. Give it a fighting stance with a strong silhouette, a 1.5–3 s loop, a small breathing motion, and first/last keys identical (loops don't interpolate last→first).
- **Anime run**: lean 15–30° forward, exaggerated stride, optional "ninja run" arms-back variant. The cycle should match ground speed so feet don't slide. Default `WalkSpeed` is **16 studs/s**.
- **Dash** = a 0.15–0.3 s velocity burst + a 2–3-pose stepped animation (crouch → stretched blur pose → recover) + an FOV punch + an afterimage/dust VFX.
- The new **Animation Graph Editor** can replace the Animate script with a Blend1D (speed) or StateMachine graph driven by `SetParameter("humanoidSpeed", v)`.

## Why it matters for anime battlegrounds
Players spend most of their time idling between exchanges and running toward the next fight. A stiff default R6 run undercuts every flashy ultimate. TSB-style games also switch stances (awakened idle/run), which locomotion must support.

## Step 1: Replace the default Animate IDs
From the official "Use animations" doc (Script in ServerScriptService, on `CharacterAppearanceLoaded`):
```lua
local animateScript = character:WaitForChild("Animate")
animateScript.idle.Animation1.AnimationId = "rbxassetid://<combat idle>"
animateScript.idle.Animation2.AnimationId = "rbxassetid://<idle variant>"
animateScript.idle.Animation1.Weight.Value = 9   -- 90% of idles
animateScript.idle.Animation2.Weight.Value = 1   -- 10% fidget
animateScript.run.RunAnim.AnimationId  = "rbxassetid://<anime run>"
animateScript.walk.WalkAnim.AnimationId = "rbxassetid://<walk>"
animateScript.jump.JumpAnim.AnimationId = "rbxassetid://<jump>"
animateScript.fall.FallAnim.AnimationId = "rbxassetid://<fall>"
```
- Weighted idle selection follows `animation weight / total weight` (official).
- Stop playing tracks first (`for _, t in animator:GetPlayingAnimationTracks() do t:Stop(0) end`), as the doc sample does.
- For stance changes (awakening), swap these IDs at runtime and restart the current state, or move locomotion into a graph `SelectNode` keyed by a `"stance"` parameter.

## Step 2: Combat idle
| Element | Target (recommendation) |
|---|---|
| Loop length | 1.5–3.0 s (45–90 frames at 30 fps) |
| Stance | Feet ~1.2× shoulder width, lead foot forward, guard hands up |
| Breathing | Torso ±1–3° rotation, root ±0.05–0.1 stud vertical |
| Hold quality | Stepped or near-stepped for a "drawn" feel; smooth breathing is fine |
| Priority | Idle |
| First = last key | Required (no last→first interpolation) |

- Anime idles often **hold** the stance and animate only secondary elements (hair, cloth, aura VFX). On R6, do the breathing on the torso and let VFX do the rest. See [[Anime VFX Fundamentals]].
- Each character gets its own idle, because it is their silhouette identity. See [[Shonen Anime Shape Language]].

## Step 3: Run cycle
| Element | Target (recommendation) |
|---|---|
| Cycle length | 0.5–0.67 s per two steps (15–20 frames at 30 fps) at WalkSpeed 16 |
| Forward lean | 15–30° (more = faster read) |
| Contact / passing / up poses | 4 key poses per step, 8 per cycle; try them stepped (on 2s) for an anime feel |
| Arm style | Pumping fists, or "ninja run" (arms swept back, torso low) |
| Priority | Movement |
| Footstep markers | `FootStep` event on each contact (docs example uses exactly this) |

Speed matching:
- Measure stride: studs the foot travels per cycle ÷ cycle length should be about ground speed. If the game sprints at a higher WalkSpeed, scale playback with `track:AdjustSpeed(currentSpeed / authoredSpeed)` (the default Animate script does similar speed scaling for walk/run).
- In the Graph Editor: `Blend1DNode` between walk (≈8 studs/s) and run (≈16+) on a `humanoidSpeed` parameter, which avoids foot sliding.

> [!warning] Unverified
> TSB/JJS sprint speeds and whether they use a custom WalkSpeed are not documented in reachable sources.

## Step 4: Dash
Anime dash = **anticipation crouch → smear/blur pose (held) → brake**.

| Phase | Duration | Animation | Physics | FX |
|---|---|---|---|---|
| Crouch | 2–3 frames (≈0.05 s) | Low, knees bent, `Constant` | none | dust puff |
| Travel | 0.15–0.3 s | **One held stretched pose** (body low, limbs trailing) | `LinearVelocity` 50–90 studs/s (recommendation) | afterimages every 0.03–0.05 s, FOV 70→80–84 |
| Brake | 0.1–0.2 s | Skid pose, hand on ground optional | velocity off | dust, small shake |

- Side dashes have mirrored left/right assets. Back dash is a separate hop.
- Use **Movement** priority if the upper body may attack mid-dash (dash-cancel M1s), or **Action** if the dash should own the whole body.
- `Humanoid.AutoRotate = false` during side/back dashes so the character keeps facing the target (AutoRotate otherwise turns the model toward the movement direction).
- Afterimage technique: see [[Anime Posing and Smears on Roblox]]. FOV punch: see [[Camera Work for Abilities]].

## Step 5: Jump, fall and landing
- Anime jumps hold an **apex pose** (tuck or "superhero" pose) longer than physics would suggest. Author a looping fall pose.
- Landing: a 0.15–0.25 s squash pose (crouch) at Action priority, triggered by `Humanoid.StateChanged` → `Landed`.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Default WalkSpeed | 16 studs/s | Humanoid docs |
| Idle weight formula | weight / total | Use animations doc |
| Default-anim final keyframe | `End` | Animation Editor doc |
| Idle / run priority | Idle / Movement | Enum recommendations |
| Combat idle loop | 1.5–3 s | Recommendation |
| Run cycle | 0.5–0.67 s | Recommendation |
| Dash travel | 0.15–0.3 s at 50–90 studs/s | Recommendation |

## Checklist
- [ ] Idle/run/walk/jump/fall IDs replaced and published under the group
- [ ] Loops have identical first and last keys
- [ ] Final keyframe named `End` on default replacements
- [ ] Run playback scaled to actual speed (no foot sliding)
- [ ] `FootStep` markers drive dust and sound
- [ ] Dash: crouch → held stretch → brake, plus FOV punch + afterimages
- [ ] Stance swap (awakening) changes locomotion IDs or a graph parameter

## Common Mistakes
- Leaving locomotion at Core priority so it fights with the defaults. Author at Idle/Movement.
- Smooth, floaty run cycles with no lean.
- A dash animation longer than the velocity burst, so the character slides in a pose after stopping.
- Animating legs in upper-body attacks, which freezes the run during M1s (see [[Roblox Animation System Reference]]).

## Related
- [[Roblox Animation System Reference]]
- [[Anime Combat Animation Timing]]
- [[M1 Combo System Design]]
- [[Camera Work for Abilities]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]

## Sources
1. Roblox Creator Docs: Use animations (replace defaults, idle weights, Animate script references). https://create.roblox.com/docs/animation/using
2. Roblox Creator Docs: Animation Editor (looping caveat, `End` keyframe, priorities). https://create.roblox.com/docs/animation/editor
3. Roblox Creator Docs: AnimationPriority (Core for defaults; Idle/Movement recommendations). https://create.roblox.com/docs/reference/engine/enums/AnimationPriority
4. Roblox Creator Docs: Animation events (`FootStep` example). https://create.roblox.com/docs/animation/events
5. Roblox Creator Docs: Humanoid (WalkSpeed 16, AutoRotate). https://create.roblox.com/docs/reference/engine/classes/Humanoid
6. Roblox Creator Docs: Animation Graph Editor (Blend1D, SetParameter humanoidSpeed sample). https://create.roblox.com/docs/animation/graph-editor
7. Roblox Creator Docs: AnimationTrack (AdjustSpeed). https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
8. NoPing blog: TSB guide (front dash vulnerable; side/back shorter cooldowns). https://noping.com/blog/the-strongest-battlegrounds-tsb-in-roblox
