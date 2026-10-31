---
tags: [animation, posing, smears, foreshortening, line-of-action, anime]
updated: 2026-10-31
sources: 11
status: draft
---
# Anime Posing and Smears on Roblox

## TL;DR
- Pose for **silhouette first**. One clear **line of action** (a single C or S curve head→heel) per key pose, readable as a black shape at the gameplay camera distance.
- **Foreshortening sells power.** Push the striking limb *toward the camera* and widen the FOV for the shot (80–100° vs the default 70°). This is the "Kanada perspective" look that anime action is known for.
- R6/R15 rigs are rigid parts, so you can't squash a mesh. **Cheat with Motor6D translation** (pull the arm out of its socket 0.2–0.6 studs on the strike frame), **swap-in smear meshes**, **afterimage clones (multiples)**, and **VFX streaks**.
- A smear lives for **1–2 render frames (17–33 ms)** or one stepped key. Longer and the trick shows.
- "Kill everything 3D": Arc System Works' guiding rule for Guilty Gear Xrd. If a pose reads as a 3D model rotating, re-pose it to read as a drawing from *this* camera.

## Why it matters for anime battlegrounds
Battlegrounds players watch fights from a third-person orbit camera, plus cinematic cameras during ultimates. Readable, exaggerated key poses are what make an R6 block-body look like a shonen fighter. The model barely matters if the poses and the frames between them are strong. Pair with [[Shonen Anime Shape Language]] (shapes) and [[Anime Combat Animation Timing]] (when to hold each pose).

## Principles that matter most here
From Disney's 12 principles (Ollie Johnston & Frank Thomas, *The Illusion of Life*, 1981), the anime-critical subset:
| Principle | Anime application on Roblox |
|---|---|
| Anticipation | Wind-up opposite to the strike, held 2–5 frames longer than feels natural |
| Staging | One idea per pose; clear silhouette against the camera |
| Pose to pose | Block key poses first; anime is pose-to-pose with holds |
| Exaggeration | Push torso twist and stride 30–50% past "realistic" |
| Arcs | Fists and feet travel on arcs, never straight lerps (add a mid key) |
| Solid drawing → "solid posing" | Weight over the support foot, no twinning (left and right mirrored) |
| Timing | See [[Anime Combat Animation Timing]] |

## Step 1: Line of action and silhouette
1. Draw (mentally or on a screenshot) one curve from head through spine to the planted foot.
2. Every key pose should have **one dominant curve**. A **C curve** reads as power or compression (wind-up). A **straight line** reads as full extension (impact).
3. **Twist the torso** (R6 `Torso` via `RootJoint`; R15 `LowerTorso`/`UpperTorso` waist) 20–40° away for anticipation, then 30–60° into the hit.
4. Silhouette test: in Studio set the rig to a flat black material or check the pose against the sky. Can you tell it is a punch?

> [!tip] R6 limitation
> R6 has no elbows or knees (6 parts). A DevForum thread notes R6 poses "always look weird" when you try realistic bends. Lean into it with bigger **whole-limb rotations**, **torso lean**, and **root translation** (lunges) instead of joint bends. See [[Roblox Character Rigs R6 vs R15 vs Custom]].

## Step 2: Foreshortening toward the camera
Anime exaggerates perspective: the fist toward the lens becomes huge. Kanada Yoshinori's boldly exaggerated perspective was nicknamed "Kanada Pers".
- **In gameplay** (orbit camera) you can't control the angle, so make the pose read from the side **and** the front.
- **In cutscene shots** (ultimates, finishers) you control the camera:
  - Put the lens 2–4 studs from the striking fist, with the attacker's body behind it.
  - Raise `Camera.FieldOfView` to 80–100° for the strike frames (default 70°, clamp 1–120°). Wider FOV = stronger perspective distortion = bigger fist.
  - Drop back to 50–60° for the held "power pose" after impact. That compresses perspective and reads as a heroic still.
- **Cheat the pose per camera.** Guilty Gear Xrd's team found some poses "could not be achieved through perspective alone" and adjusted models per shot. On Roblox, author a *cutscene-only* variant of the pose (arm translated toward the camera and rotated so it faces the lens). Don't reuse the gameplay animation.

> [!warning] Unverified
> The specific per-camera mesh-deformation technique Arc System Works used in Xrd isn't documented in sources I could reach. Only the general statement (poses needing more than perspective) and the "kill everything 3D" quote attributed to the GDC 2015 talk are sourced.

## Step 3: Smears on rigid rigs
A smear frame is a single distorted in-between that conveys speed. 3D productions (e.g. *Spider-Verse*) use squash/stretch and overlaid 2D effects. Blender add-ons generate "extra long smears" and **multiples** by duplicating mesh along the motion arc. Roblox options:

| Technique | How | Cost | Best for |
|---|---|---|---|
| **Motor6D stretch** | On the smear key, translate the arm joint 0.2–0.6 studs along the motion (arm "detaches"), with `Constant` easing | Free | M1 jabs, kicks |
| **Smear mesh swap** | A pre-made stretched/blurred arm MeshPart welded to the limb. Make it visible for 1–2 frames on a `Smear` marker, hide the real limb with `LocalTransparencyModifier` or Transparency | 1 extra mesh per limb | Heavies, finishers |
| **Multiples / afterimages** | On marker, clone the limb or character (`Archivable` clone, anchored, no collisions), tween Transparency 0.3→1 over 0.1–0.2 s | 1–6 clones per hit; clean up | Rapid punches (barrage) |
| **VFX streak** | Beam/Trail or a flipbook "speed arc" texture on the limb path | Particles budget | Everything; pairs with the above |
| **Speed-line overlay** | Screen-space ImageLabel or a part in front of the camera | Cheap | Ultimates |

Details on trails, beams and impact frames: [[Anime VFX Fundamentals]].

> [!example] Smear marker script (client)
> ```lua
> track:GetMarkerReachedSignal("Smear"):Connect(function(limbName)
>     local smear = character:FindFirstChild(limbName .. "Smear") -- prewelded, Transparency = 1
>     if not smear then return end
>     smear.Transparency = 0
>     task.delay(1/30, function() smear.Transparency = 1 end) -- ~2 render frames
> end)
> ```

> [!warning] Unverified
> Whether Roblox `Bone` animation supports per-bone **scale** keys (which would allow true squash and stretch on skinned rigs) wasn't confirmed. Treat scale as unsupported and fake it.

## Step 4: Holds and "living holds"
Anime holds are dead-still drawings. In 3D a perfectly frozen rig can look broken. Options:
- **True hold** (anime style): duplicate the key and add hitstop. Best during impact (≤ 0.3 s).
- **Moving hold**: a 1–3° drift over the hold, for longer power poses (≥ 0.5 s). Add VFX motion (aura, hair, cloth) so the frame still feels alive while the body stays still.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Torso twist, anticipation | 20–40° away | Readable wind-up (recommendation) |
| Torso twist, impact | 30–60° into the hit | Commitment (recommendation) |
| Motor6D smear stretch | 0.2–0.6 studs | Visible but not broken (recommendation) |
| Smear lifetime | 1–2 render frames (17–33 ms) | Reads as speed, not as a glitch |
| Afterimage fade | 0.1–0.2 s, Transparency 0.3→1 | Multiples without clutter |
| Cutscene strike FOV | 80–100° | Perspective exaggeration |
| Cutscene power-pose FOV | 50–60° | Compressed heroic still |
| Default FOV | 70° (range 1–120) | Camera docs |

## Checklist
- [ ] Every key pose has one line of action and passes a silhouette test
- [ ] Anticipation pose is opposite in direction to the strike
- [ ] Strike limb travels on an arc (mid key added)
- [ ] Smear frames ≤ 2 render frames
- [ ] Cutscene versions of poses made separately from gameplay versions
- [ ] Afterimage clones are destroyed (Debris or a manual timer) and never collide

## Common Mistakes
- **Twinning**: both arms and legs mirrored. It kills the dynamism.
- Posing for the Studio viewport angle only. Check from the gameplay camera height and distance.
- Leaving a smear mesh visible for 5+ frames.
- Realistic joint limits on an anime character. Exaggerate.
- Trying to scale limbs in Blender and losing it on import.

## Related
- [[Anime Combat Animation Timing]]
- [[Camera Work for Abilities]]
- [[Anime VFX Fundamentals]]
- [[Shonen Anime Shape Language]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]

## Sources
1. Wikipedia: Twelve basic principles of animation (Johnston & Thomas, 1981). https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
2. Wikipedia: Smear frame. https://en.wikipedia.org/wiki/Smear_frame
3. Superhive (Blender Market): Auto Smear Frames add-on ("extra long smears", multiples). https://superhivemarket.com/products/auto-smear-frames
4. SIGGRAPH 2024: "SMEAR: Stylized Motion Exaggeration with ARt-direction". https://hal-iogs.archives-ouvertes.fr/hal-04576817v1
5. Animétudes: "The Kanada style now" and "Yoshinori Kanada and the nature of animation". https://animetudes.com/2021/07/09/the-kanada-style-now/
6. Our Star Blazers: "Yoshinori 'Iko' Kanada, 1952-2009" ("Kanada Pers" exaggerated perspective). https://ourstarblazers.com/vault/399/
7. Wikipedia: Guilty Gear Xrd (poses not achievable by perspective alone; deliberate frame cuts). https://en.wikipedia.org/wiki/Guilty_Gear_Xrd
8. Game Watch Impress: GDC 2015 GGXrd art talk report (~40,000 polys per character, keyframe sprite-like animation). https://game.watch.impress.co.jp/docs/news/20150307_691725.html
9. Noggi3D Notion: "guilty gear style summary" ("Kill everything 3D" quote attribution). https://noggi3d.notion.site/guilty-gear-style-summary
10. DevForum: "Advice for positioning R6 limbs while animating?". https://devforum.roblox.com/t/advice-for-positoning-r6-limbs-while-animating/1533251
11. Roblox Creator Docs: Camera.FieldOfView (1–120, default 70). https://create.roblox.com/docs/reference/engine/classes/Camera
