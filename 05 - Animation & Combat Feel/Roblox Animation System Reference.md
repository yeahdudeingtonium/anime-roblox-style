---
tags: [animation, roblox-api, animator, animation-graph, priorities, keyframemarker]
updated: 2026-10-31
sources: 9
status: draft
---
# Roblox Animation System Reference

## TL;DR
- **Animator** (under `Humanoid` or `AnimationController`) plays and **replicates** every `AnimationTrack`. `Animator:LoadAnimation()` always makes a **new** track, so cache tracks or use `Animator:GetTrackByAnimationId()`.
- There are **7 priorities**, high to low: **Action4 > Action3 > Action2 > Action > Movement > Idle > Core**. Evaluation goes **per joint**, high to low, until the summed weight reaches 1.0. Same-priority tracks **blend by weight**. Enum *values* are not ranks (Action4 = 5, Core = 1000).
- `Play(fadeTime=0.1, weight=1, speed=1)`, `Stop(fadeTime=0.1)` and `AdjustWeight(weight=1, fadeTime=0.1)` are the official defaults.
- Use **`GetMarkerReachedSignal(name)`** with Animation Events (KeyframeMarkers) for hitboxes, VFX and sounds. `KeyframeReached` is **deprecated**.
- **New in 2026 docs: the Animation Graph Editor.** It builds node-based graphs (Clip, Add, Over, Blend1D/2D, Mask, Select, PrioritySelect, Sequence, OneShot, StateMachine…) published as an `AnimationGraphDefinition` asset. You drive them with `AnimationTrack:SetParameter()`, and graph state replicates automatically.
- Remote characters can be **LOD-throttled**. `Animator.PreferLodEnabled = false` forces full-rate evaluation, and `Animator.EvaluationThrottled` tells procedural code to skip a frame.

## Why it matters for anime battlegrounds
Battlegrounds characters layer many tracks at once: idle, run, an M1 swing on the arms, a stun on the torso, and an ultimate. Wrong priorities cause the classic bugs. Examples: the run animation leaks into a punch, a stun gets overridden by an M1, and an ultimate gets broken by a jump. The graph editor is the first official tool for state machines and blend trees without hand-written Animate scripts.

## Priorities and blending (exact rules)
From the `AnimationPriority` enum docs:
> When multiple AnimationTracks are played concurrently by the same Animator and affect the same animated joints, the tracks are evaluated in order from high to low priority, per joint, while the total track weight sum remains less than 1.0. When the track weight sum reaches or exceeds 1.0 for a joint, evaluation stops and no lower-priority tracks will be evaluated for that joint. AnimationTracks with the same priority that are playing concurrently will blend proportional to their track weights (normalized if the sum exceeds 1).

| Rank | Priority | Enum value | Docs' recommended use | Battlegrounds use |
|---|---|---|---|---|
| 1 (highest) | Action4 | 5 | Overrides all | Ultimates/cutscene grabs, ragdoll get-up |
| 2 | Action3 | 4 | Overrides Action2 | Stun / hit reactions (must beat M1s) |
| 3 | Action2 | 3 | Overrides Action | M1s, skills |
| 4 | Action | 2 | Actions over idle/locomotion | Block hold, emotes |
| 5 | Movement | 1 | Walk/run/swim/climb | Run, dash loops |
| 6 | Idle | 0 | Idles | Combat idle |
| 7 (lowest) | Core | 1000 | Roblox defaults and catalog bundles | Leave for default Animate |

> [!tip] Partial-body layering is free
> Evaluation is **per joint**. An M1 that keys only the arms and torso lets the run animation keep driving the legs. Delete leg tracks from upper-body attacks so you can move while you punch. Key them to make the attack root the character in place.

> [!warning] Weight < 1 leaks lower priorities
> Because evaluation continues "while the total track weight sum remains less than 1.0", a stun played at weight 0.6 lets 40% of the run animation through on those joints. Play combat tracks at weight 1.

## AnimationTrack API you will actually use
| Member | Default / notes |
|---|---|
| `Play(fadeTime, weight, speed)` | 0.1 / 1 / 1. Weight fades 0→target over fadeTime |
| `Stop(fadeTime)` | 0.1. Don't use 0 if Motor6D `MaxVelocity` is 0 (joints freeze) |
| `AdjustSpeed(speed)` | 1 = authored speed, negative = backwards, **0 = freeze** (hitstop) |
| `AdjustWeight(weight, fadeTime)` | 1 / 0.1 |
| `Priority`, `Looped` | Settable at runtime. Defaults come from the asset |
| `TimePosition`, `Length` | Seconds. Length is 0 until the asset loads |
| `WeightCurrent`, `WeightTarget` | Floats. Compare with tolerance, not `==` |
| `GetMarkerReachedSignal(name)` | Fires `(paramString)` for every marker with that name |
| `GetTimeOfKeyframe(name)` | Seconds of a named keyframe |
| `Stopped` vs `Ended` | Stopped fires at stop. **Ended** fires after the fade-out, when the rig is neutral |
| `DidLoop` | Fires each completed loop |
| `KeyframeReached` | **Deprecated**, superseded by `GetMarkerReachedSignal` |
| `SetParameter(key, value)` / `GetParameter` / `GetParameterDefaults()` | Animation-graph inputs (NaN/Inf sanitized to 0) |

## Animator API
| Member | Notes |
|---|---|
| `LoadAnimation(anim)` | Always creates a **new** track. Animator must be in Workspace |
| `GetTrackByAnimationId(id)` | Returns an existing track or nil, without making a new one |
| `GetPlayingAnimationTracks()` | Use to stop everything on stun/ragdoll |
| `StepAnimations(dt)` | Manual stepping (used for previews and tools) |
| `ApplyJointVelocities` | Physics hand-off (ragdoll from animation) |
| `PreferLodEnabled` | Default true. Engine may reduce evaluation frequency on remote characters by distance, screen coverage and budget |
| `EvaluationThrottled` | Read-only. True when the pose was reused this frame |
| `AnimationPlayed(track)` event | Hook for VFX on any played track |

> [!example] Caching tracks per character
> ```lua
> local tracks = {}
> local function getTrack(animator: Animator, anim: Animation)
>     local t = tracks[anim]
>     if not t then
>         t = animator:LoadAnimation(anim)
>         tracks[anim] = t
>     end
>     return t
> end
> ```
> Clear the cache on `CharacterAdded`. A new character means a new Animator.

## Animation Events / KeyframeMarkers
- Create them in the Animation Editor: timeline settings → **Show Animation Events** → **Edit Animation Events** → **+ Add Event**, with a name and an optional **Parameter** string.
- At runtime: `track:GetMarkerReachedSignal("Hit"):Connect(function(param) ... end)`. The parameter is a string, so encode things like `"dmg=8,kb=20"` and parse it.
- Names need not be unique. Each marker with the same name fires the signal, so one `Hit` event can mark all 3 hits of a multi-hit.
- Under the hood, a `KeyframeMarker` is parented to a `Keyframe` with a `Value` string.

## Animation Graph Editor (new)
Opened from **Avatar tab → Graph Editor**. The Animation Editor stays the clip-authoring tool. The graph combines clips into logic.

| Node (`Enum.AnimationNodeType`) | What it does | Battlegrounds use |
|---|---|---|
| ClipNode | Plays a clip asset | Every animation |
| AddNode | Additive layer on a base | Breathing / hit-flinch additive |
| OverNode | Overlay with per-joint mask | Upper-body attacks over legs |
| MaskNode | Per-joint weight mask | Arms-only block |
| Blend1DNode / Blend2DNode | Blend along 1D / 2D parameter | Walk→run by speed, strafe |
| SelectNode | Picks input by string parameter | Stance: `"neutral"`, `"awakened"` |
| PrioritySelectNode | Highest-priority input whose trigger is true | Stun > attack > move |
| SequenceNode / RandomSequenceNode | Plays inputs in order / weighted random | Idle variations |
| OneShotNode | One-shot over a looping base on trigger, blends in and out | M1 swing over run |
| SpeedNode, SubtractNode | Speed scale, difference pose | Hitstop via speed param |
| StateMachineNode | Full state machine | Locomotion |
| GraphOutput | Final pose | — |

Transitions use `DefaultTransitionDuration` (seconds) and `DefaultTransitionCurve`, which currently supports only `Linear` and `CubicV2`. Sequence advance uses `WaitFor` = `Finished` | `Trigger`. `BeforeFinished` starts the blend one transition duration early.

Scripting: publish the graph to get an asset ID, then load it like any animation and call `track:SetParameter("humanoidSpeed", v)`. Marker events that reach the top of the graph still fire `GetMarkerReachedSignal`.

Replication depends on `Workspace.AuthorityMode` when the Animate script is created:
- **Automatic**: the owning client drives player graphs and the server drives NPC graphs. `SetParameter` values replicate automatically, last writer wins per frame, with a small delay.
- **Server**: the server simulates every graph and replicates params plus internal node state. The owning client uses `PredictionMode`.

**Graph → Create Animate script** generates `Animate (ModuleScript)` + `RunClient` + `RunServer`.

> [!warning] Unverified
> I could not confirm whether the Animation Graph Editor is still labelled Beta in Studio on 2026-10-31. The doc page has no beta banner. Treat it as new and test before you migrate a live combat game.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Priority levels | 7 | Action4 highest, Core lowest |
| Play/Stop/AdjustWeight fadeTime default | 0.1 s | API default |
| Combat track weight | 1.0 | Prevents lower-priority leak |
| M1 fadeTime | 0–0.05 s | Snappy start |
| Stun fadeTime | 0.03–0.08 s | Instant read without popping |
| Graph transition curves | Linear, CubicV2 | Only ones supported |
| `PreferLodEnabled` for bosses/cutscene actors | false | Full-rate evaluation |

## Checklist
- [ ] Assign priorities: Idle / Movement / Action (block) / Action2 (M1, skills) / Action3 (stun) / Action4 (ult, grabs)
- [ ] Remove leg tracks from upper-body attacks that should allow movement
- [ ] Cache tracks. Never call `LoadAnimation` per input
- [ ] Use `GetMarkerReachedSignal`, never `KeyframeReached`
- [ ] Use `Ended` (not `Stopped`) when you need the rig back to neutral
- [ ] Set `PreferLodEnabled = false` on cutscene participants during ultimates
- [ ] Prototype locomotion in the Graph Editor and keep combat tracks scripted until it is proven

## Common Mistakes
- Thinking `Action4`'s enum value 5 means "fifth priority". **Values are indices, not ranks.**
- Same-priority M1 and stun tracks blending 50/50. Put stuns one priority above attacks.
- Calling `LoadAnimation` every click, which leaks tracks and costs performance (official warning).
- `Stop(0)` on rigs whose Motor6D `MaxVelocity` is 0, which freezes the joints.
- Testing replication with an Animator created on the client. Its tracks never replicate.

## Related
- [[Importing, Uploading and Replicating Animations]]
- [[M1 Combo System Design]]
- [[Anime Combat Animation Timing]]
- [[Anime Locomotion - Idle, Run and Dash]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]

## Sources
1. Roblox Creator Docs: AnimationPriority enum. https://create.roblox.com/docs/reference/engine/enums/AnimationPriority
2. Roblox Creator Docs: AnimationTrack class. https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
3. Roblox Creator Docs: Animator class (LoadAnimation, GetTrackByAnimationId, PreferLodEnabled, EvaluationThrottled). https://create.roblox.com/docs/reference/engine/classes/Animator
4. Roblox Creator Docs: KeyframeMarker class. https://create.roblox.com/docs/reference/engine/classes/KeyframeMarker
5. Roblox Creator Docs: Animation events. https://create.roblox.com/docs/animation/events
6. Roblox Creator Docs: Animation Graph Editor. https://create.roblox.com/docs/animation/graph-editor
7. Roblox Creator Docs: AnimationNodeType enum. https://create.roblox.com/docs/reference/engine/enums/AnimationNodeType
8. Roblox Creator Docs: AnimationNodeDefinition class. https://create.roblox.com/docs/reference/engine/classes/AnimationNodeDefinition
9. Roblox creator-docs GitHub mirror (source used to read all of the above on 2026-10-31). https://github.com/Roblox/creator-docs
