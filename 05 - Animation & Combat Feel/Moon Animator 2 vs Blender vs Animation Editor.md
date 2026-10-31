---
tags: [animation, tools, moon-animator, blender, animation-editor, workflow]
updated: 2026-10-31
sources: 11
status: draft
---
# Moon Animator 2 vs Blender vs Animation Editor

## TL;DR
- **Roblox Animation Editor** (built-in): free and official. It has the dope sheet + **Curve Editor**, IK, **Animation Events**, priority/loop settings, FBX import, keyframe optimization, and now pairs with the **Animation Graph Editor**. It is best for clean publishing and for anyone new.
- **Moon Animator 2** (xSIXx plugin): the de-facto tool for **battlegrounds cutscenes**. In one timeline it animates rigs **plus cameras, parts, lights and properties** (e.g. `FieldOfView`). Rig animation exports as a `KeyframeSequence`. Camera and property tracks need a script or player module to play in game.
- **Blender**: the strongest posing tools (IK/FK rigs, graph editor, NLA, onion-skinning add-ons, smear add-ons). It needs a bridge: an FBX import through the Animation Editor, or community plugins (Den_S exporter/importer, Cautioned's Blender Animations plugin used by R6 IK+FK rigs).
- Typical pro split: **Blender or Moon for authoring → Animation Editor for markers, priority and publishing → Moon (or a script) for ultimate camera work**.

## Why it matters for anime battlegrounds
Ultimates need **character + victim + camera + VFX parts** on one timeline, which is Moon's strength. M1s and locomotion need clean, small, well-marked assets, which the built-in editor handles best. Stylised anime posing (strong arcs, IK, smears) is easiest in Blender.

## Comparison
| Feature | Animation Editor | Moon Animator 2 | Blender |
|---|---|---|---|
| Cost | Free, built-in | Plugin (pricing conflicting in sources; check Creator Store) | Free |
| Frame rate | 30 fps default, custom rates (editing only) | Its own timeline | Any |
| Stepped keys | `Constant` easing | "None" easing (DevForum) | Constant interpolation |
| Curve editor | Yes (converts KeyframeSequence → CurveAnimation; Euler vs Quaternion choice) | Easing presets; extra styles baked as extra keys (DevForum) | Full graph editor |
| IK | Yes (Manage IK) | Yes (community docs) | Best (custom IK/FK rigs) |
| Animation events / markers | Yes (name + parameter string) | Unverified | Through bridge plugins only (unverified) |
| Camera animation | No | **Yes** (CFrame + FOV tracks) | Yes, but needs custom export |
| Multi-rig scenes (attacker + victim) | One rig at a time | **Yes** | Yes |
| Output | KeyframeSequence / CurveAnimation → publish | KeyframeSequence in `AnimSaves` per rig; camera as value folders | FBX or plugin data → Studio |
| Publish to group | Built-in (Creator field) | Uses Roblox publish flow | Via Studio |

> [!warning] Unverified
> Moon Animator 2 has no official public feature documentation that I could reach (an "official tutorial" video exists, but only scraped copies came up). Features listed here come from DevForum community threads. Confirm current pricing and features on the plugin's Creator Store listing.

## Workflow A: Built-in Animation Editor only (solo dev, M1s)
1. Insert a rig (Avatar → Character / Rig Builder). For custom Motor6D rigs, make sure `AssemblyRootPart` is the part that should stay stationary. `PrimaryPart` does **not** set it.
2. Block poses with `Constant` easing (see [[Anime Combat Animation Timing]]). Press `R` to toggle Move/Rotate, which uses Studio snap increments.
3. Add Animation Events (`Hit`, `CanCancel`, `End`).
4. Set priority, then ⋯ → Publish to Roblox → Creator = group.
5. Optional: the Curve Editor for polish. **Choose the rotation type first.** Converting quaternions to Euler is one-way, and Euler curves can gimbal-lock.

## Workflow B: Moon Animator 2 for cutscenes and ultimates
1. File → New Animation. Add the attacker rig, victim rig, camera, and any VFX parts.
2. Animate the camera by locking the Studio view as keys. You can also key `FieldOfView`.
3. Export:
   - Rigs → `KeyframeSequence` under each rig's `AnimSaves`. Publish each as an asset.
   - Camera → a folder with **`FOV`, `Frames`, `Settings`**. One guide renames them to `FieldOfView` and `CFrame` for its player module.
4. Play in game: set `Camera.CameraType = Scriptable` and step the CFrame frames each render step. **Multiply by the attacker's `HumanoidRootPart.CFrame`** if you animated relative to the character, otherwise the camera flies to a random world spot. Restore the camera type afterwards.
5. Community players: MoonLite (free, MaximumADHD), Moon2Cutscene, and the paid Moon2Module (converts projects to ModuleScripts, ~$4.99 listing). Moon2Module reportedly uses tweens + `task.wait()`.

> [!tip] Bake the camera, don't tween it
> Tween/`task.wait()` playback drifts with frame time. Bake the camera CFrames at a fixed rate (e.g. 60 per second) into a table and index by elapsed time in `RenderStepped`. Then hitstop and slow-mo can scale time cleanly. See [[Camera Work for Abilities]].

## Workflow C: Blender for posing
1. Get the Roblox rig into Blender:
   - **Den_S plugin + add-on**: exports a rigged Roblox model as a matching armature and imports animation back. Known pitfalls: face decals cause errors (remove them), the rig sits far from the origin (centre the rig at about `0, 3, 0`), and Mixamo bone names need fixing (uncheck "Add Leaf Bones").
   - **R6 IK+FK Blender Rig (DevForum, v2.2x)**: requires **Cautioned's Blender Animations plugin**, updated for Blender 5.0 per the thread.
2. Animate with Blender's Constant interpolation for stepped blocking. Use smear add-ons for multiples (see [[Anime Posing and Smears on Roblox]]).
3. Export:
   - **Plugin route**: `.rbxanim` file or clipboard → Roblox plugin → KeyframeSequence.
   - **FBX route**: export armature + mesh with **Bake Animation** on, then Animation Editor → ⋯ → Import → From File.
4. Add markers and priority in the Animation Editor, then publish.

> [!warning] Scale and per-vertex deformation do not transfer
> Roblox Motor6D animation is per-part rigid transforms (R6/R15). Bone-based skinned meshes support bone transforms. Blender shape keys, per-vertex smears and non-uniform bone scale generally do **not** come across through these pipelines. Den_S's thread notes that animation works "per whole body part, not per vertex". Fake scale and smears with swapped meshes or VFX instead.

## Choosing
| You are… | Use |
|---|---|
| A solo scripter-animator making M1s | Animation Editor |
| Making ultimates with camera + 2 characters | Moon Animator 2 (+ camera player) |
| An experienced 3D animator, heavy posing | Blender → bridge → Animation Editor for markers |
| A team of 3+ animators | Blender/Moon authoring + one "publisher" who owns group upload and the ID registry |

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Editor default fps | 30 | Official |
| FBX export | Bake Animation ON | Roblox export requirements |
| Rig placement for Den_S export | about (0, 3, 0) | Avoids the off-origin armature |
| Moon camera export folders | FOV / Frames / Settings | Community guide |
| Camera FOV range | 1–120°, default 70 | Camera docs |

## Checklist
- [ ] Pick one authoring tool per asset type and document it
- [ ] Decide rotation type (Quaternion vs Euler) before opening the Curve Editor
- [ ] Moon camera playback multiplies by the root CFrame and uses a Scriptable camera
- [ ] Blender exports checked for missing bones and leaf bones
- [ ] All final assets get markers + priority + group publish in Studio

## Common Mistakes
- Exporting a Moon camera and expecting `Animator` to play it. Cameras need a script.
- Using Moon's extra easing styles everywhere. They are **baked as extra keyframes** and inflate asset size (DevForum feature request).
- Animating Blender scale or shape keys that silently vanish in Roblox.
- Converting to curves without choosing quaternions, then fighting gimbal flips.

## Related
- [[Importing, Uploading and Replicating Animations]]
- [[Camera Work for Abilities]]
- [[Anime Combat Animation Timing]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs: Animation Editor. https://create.roblox.com/docs/animation/editor
2. Roblox Creator Docs: Curve Editor (quaternion→Euler one-way conversion). https://create.roblox.com/docs/animation/curve-editor
3. Roblox Creator Docs: Animation Graph Editor. https://create.roblox.com/docs/animation/graph-editor
4. DevForum: "Getting Started with Moon Animator 2 - [Unofficial]". https://devforum.roblox.com/t/getting-started-with-moon-animator-2-unofficial/476330
5. DevForum: "Moon Animator: How do I export and import the camera?". https://devforum.roblox.com/t/moon-animator-how-do-i-export-and-import-the-camera/1717989
6. DevForum: "Frame animation function built around Moon Animator 2". https://devforum.roblox.com/t/frame-animation-function-built-around-moon-animator-2/4214289
7. DevForum: "Moon2Module – plugin that converts your Moon Animator projects into ModuleScripts". https://devforum.roblox.com/t/moon2module-plugin-that-converts-your-moon-animator-projects-into-modulescripts/2975574
8. DevForum: "Add the missing Easing Styles for animations" (Moon bakes extra keys). https://devforum.roblox.com/t/add-the-missing-easing-styles-for-animations/2397709
9. DevForum: "Blender rig exporter/animation importer" (Den_S). https://devforum.roblox.com/t/blender-rig-exporteranimation-importer/34729
10. DevForum: "R6 IK + FK Blender Rig | V2.22" (requires Cautioned's Blender Animations plugin). https://devforum.roblox.com/t/r6-ik-fk-blender-rig-v222/3586405
11. Roblox Creator Docs: Camera class (FieldOfView 1–120, default 70). https://create.roblox.com/docs/reference/engine/classes/Camera
