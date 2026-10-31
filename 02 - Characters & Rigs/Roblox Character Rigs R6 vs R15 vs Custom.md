---
tags: [characters, rigs, r6, r15, motor6d, bones, animation]
updated: 2026-10-31
sources: 22
status: draft
---
# Roblox Character Rigs R6 vs R15 vs Custom

> [!info] How this was researched
> Engine facts come from the Roblox creator-docs source repo and API reference YAML (`main`, 2026-10-31). create.roblox.com was unreachable from the research session. Claims about what specific games use come from DevForum and marketplace search results and are flagged.

## TL;DR
- **R6** = 6 parts (`Head`, `Torso`, `Left/Right Arm`, `Left/Right Leg`) joined by Motor6Ds. **R15** = 15 MeshParts with a standard bone and joint hierarchy, plus up to **37 optional joints** in an advanced R15 rig. **Custom** = any Model, rigged with Motor6Ds between parts and/or **Bones inside a skinned MeshPart**. [1][2][3]
- Battlegrounds games lean **R6** for player characters. The large market of "battlegrounds-style" animation packs is overwhelmingly R6, R6 gives simpler and more predictable hitboxes, and the blocky silhouette reads like a classic fighting-game sprite. R15 or skinned "R6-looking" rigs are used when the game wants layered clothing, dynamic heads or smoother bends. [4][5][6]
- **Big 2026 change:** with `StarterPlayer.AvatarJointUpgrade` (the **default for new experiences**), **R15 player characters spawn with `AnimationConstraint` joints instead of Motor6D**. Code that looks for `Motor6D` breaks. Write procedural offsets into `.Transform` during `PreSimulation`. [7][8]
- Bones vs Motor6D: **Motor6D moves whole parts** (rigid, cheap, hitbox-friendly). **Bones deform a skinned mesh** (smooth elbows and capes, **visual only**: no collision change, and bone transforms aren't replicated). [3][9]
- For custom NPCs and bosses: import as **Rig Type: Custom**, then run **Adaptive Animation** (HumanoidRigDescription) to map ≥ 15 joints so standard R15 animations retarget. [10][11]

## Why it matters for anime battlegrounds
The rig decides **(1)** which animation library you can use (R6 packs vs R15 packs), **(2)** how hitboxes are built (usually boxes welded to `HumanoidRootPart` or `Torso`), **(3)** whether players keep their own avatars, and **(4)** what anime-style deformation you get (R6 can't bend an elbow; skinned rigs can). Choose it **before** modelling (see [[Anime Character Modeling in Blender]]) and before animating (see [[Anime Combat Animation Timing]]).

## How to do it

### The options compared
| | R6 (classic) | R15 (avatar standard) | Skinned "R6-look" on R15 | Custom (Bones / Motor6D) |
|---|---|---|---|---|
| Parts | 6 visible + HumanoidRootPart [1] | 15 MeshParts [2] | 15 MeshParts shaped blocky [5] | Any |
| Joints | Motor6D (`Neck`, `Left/Right Shoulder`, `Left/Right Hip`, `RootJoint`) [12] | Motor6D or AnimationConstraint (AJU) [7][8] | as R15 | Motor6D and/or Bones |
| Elbows/knees | None | Yes | Yes (skinned) | Your choice |
| Player avatars | Yes, as R6 body | Yes, full avatar support | Avatars replaced | Usually replaced |
| Layered clothing / dynamic heads | No (except via R6-to-R15 adapter) [13] | Yes | Yes | Only with your own WrapTarget [14] |
| Animation packs on the market | Very common ("battlegrounds" packs) [6] | Common | R15 or retargeted R6 | Adaptive Animation retargets R15 [11] |
| SLIM avatar LOD | No (falls back) [15] | Yes | Custom proportions fall back [15] | No |
| Humanoid rule | `Head` must connect to `Torso` or it dies [1] | `Head` must connect to `UpperTorso` [1] | as R15 | Optional Humanoid |

> [!warning] Unverified
> I could not confirm from first-party sources which rig each title (The Strongest Battlegrounds, Jujutsu Shenanigans, Heroes Battlegrounds) currently forces. Community material strongly associates the genre with R6: R6 "battlegrounds" animation packs, and a DevForum thread asking how to make "an R6 game with R15 quality like Ultimate Battlegrounds". Check in-game (`Humanoid.RigType`) before copying a choice. [4][5][6]

### Why battlegrounds devs pick R6 (community reasoning)
- Simpler, more readable **hitbox and limb collision** behaviour. [4]
- A huge pool of ready **R6 combat animations** and animators who work in it. [6]
- The "classic Roblox" look that anime-battlegrounds players expect, and fewer bends to clean up in fast 2–4 frame anticipation poses.
- Downsides: no layered clothing and no dynamic heads on players (Roblox's R6-to-R15 Adapter, toggled via `Workspace.AvatarUnificationMode`, was built to emulate R6 on R15 bodies). [13]

### Setting the game's avatar type
- **File → Avatar Settings**: avatar type **R6 / R15 / R15 & R6**, collision mode (Default OuterBox, **Single Collider** = consistent box for all players, Legacy InnerBox), animation set **Standard R15 / Standard R6**, body scale limits, and accessory scale limits (Scale or Remove). [16]
- **Single Collider** matters for fighting games: every player gets the same collision box regardless of avatar. [16]

### Building a custom skinned rig (fighter or boss)
1. Blender armature: root bone at **0,0,0**, all bones with **scale 1,1,1 and rotation 0,0,0** in rest pose (applied), **no weights on the root bone**. [3]
2. For R15 compatibility use the exact hierarchy: `Root → HumanoidRootNode → LowerTorso → UpperTorso → Head`, arms and legs as in the spec. Optional advanced joints: `Spine`, `Chest`, `LeftClavicle`/`RightClavicle`, `HeadBase`, 15 finger joints per hand (`LeftHandIndex1-3`…), `LeftToeBase`/`RightToeBase`. [2]
3. Extra bones for anime secondary motion (capes, ponytails, coat tails, sleeves): make them **children of the nearest R15 bone**, but note that Avatar Setup's own-rig path says body rigs "should not include additional bones beyond" the standard/advanced spec. Keep extra-bone characters on the **Custom** import path. [17]
4. Import with **Rig Type: R15** (spec-compliant) or **Custom** (anything else). The importer **drops zero-influence bones** unless you tick **Keep Zero Influence Bones**, which you want for helper/attachment bones (weapon sockets, VFX points). [18]
5. Custom rig → Avatar tab → **Adaptive Animation → Create**, assign at least the **15 standard joints**, and set a **T-pose** baseline, so any R15 animation can play on it. [11]
6. Animating: the Animation Editor animates both Motor6D rigs and Bones. For Motor6D rigs, make sure `AssemblyRootPart` is the part that should stay still. [19]

### Motor6D vs Bones vs AnimationConstraint
| Joint | Moves | Use for | Notes |
|---|---|---|---|
| **Motor6D** | Whole BaseParts | R6, mechanical rigs, weapons welded to hands | Roblox: "remains appropriate for non-avatar mechanical rigs"; procedural edits go in `.Transform`, not C0/C1, for performance [7][20] |
| **AnimationConstraint** | Whole BaseParts | R15 player avatars under AJU | C0/C1/Part0/Part1 are **read-only aliases**; `IsKinematic = false` enables ragdoll and force-based motion; `IsA("Motor6D")` returns false [8] |
| **Bone** | Vertices of a skinned MeshPart | Smooth deformation, capes, hair, faces | **Visual only, no collision**; `Bone.Transform` works like `Motor6D.Transform`; bones "are not replicated or serialized" [3][9] |

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| R15 required joints | 15 | Spec [2] |
| Advanced R15 optional joints | up to 37 | Spec [2] |
| Finger joints per hand | 15 (5 × 3) | [2] |
| Max bone influences per vertex | 4 | [3] |
| Face joints (dynamic head) | < 50 recommended | [21] |
| Adaptive Animation minimum mapped joints | 15 | [11] |
| Avatar Joint Upgrade | default ON for new experiences | [7][8] |
| Collision for fighters | Avatar Settings → Single Collider | Consistent hitbox base [16] |
| Rest-pose bone transforms | rot 0,0,0 / scale 1,1,1 / root at origin | [3] |

## Checklist
- [ ] Pick the rig per character type: players (R6 or R15), fighters (R15 or skinned), bosses (custom)
- [ ] Avatar Settings set: type, collision (Single Collider?), animation set
- [ ] Combat scripts find joints via AnimationConstraint **or** Motor6D (AJU-safe)
- [ ] Procedural aim/look offsets written to `.Transform` in `PreSimulation`
- [ ] Hitboxes built from parts welded to the root, never from bones
- [ ] Custom rigs: Keep Zero Influence Bones on if you need socket bones
- [ ] Adaptive Animation mapping done; R15 test animation plays correctly
- [ ] Test R6 animation packs on your exact rig proportions (arm length changes reach)

## Common Mistakes
- **`FindFirstChildOfClass("Motor6D")` on R15 characters** in a new experience returns nil under AJU. [8]
- **Writing C0 every frame** for aim/look offsets: expensive, and read-only on AnimationConstraint. Use `.Transform`. [8][20]
- **Weighting vertices to the Root bone**: the influence is dropped on import. [3][22]
- **Hitboxes on bones** don't work, because bones don't change collision. [9]
- **Setting `RigType` wrong**: an R15 humanoid set to R6 dies instantly (no `Torso` connected to `Head`). [1]
- **Extra cape/hair bones in a "Platform Avatar" body** get rejected or ignored. Keep them for in-game custom rigs. [17]

## Related
- [[Skinning and Weight Painting for Roblox]]
- [[Blender to Roblox Studio Export Pipeline]]
- [[Anime Combat Animation Timing]]
- [[NPC and Boss Characters]]
- [[Clothing and Accessories for Anime Characters]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox API reference, *Humanoid* (R6/R15 rules, RigType): https://create.roblox.com/docs/reference/engine/classes/Humanoid
2. Roblox Creator Docs, *Character body specifications* (R15 hierarchy, 37 optional joints): https://create.roblox.com/docs/avatar/character-bodies/specifications
3. Roblox Creator Docs, *General specifications* and *Rigging and skinning*: https://create.roblox.com/docs/art/modeling/specifications · https://create.roblox.com/docs/art/modeling/rigging
4. DevForum, *Should I use R6 or R15?* / *What are the main upsides and drawbacks to R15 and R6?*: https://devforum.roblox.com/t/should-i-use-r6-or-r15/2796617 · https://devforum.roblox.com/t/what-are-the-main-upsides-and-drawbacks-to-r15-and-r6/3086520
5. DevForum, *How do I make an R6 game with R15 quality like Ultimate Battlegrounds?*: https://devforum.roblox.com/t/how-do-i-make-an-r6-game-with-r15-quality-like-ultimate-battlegrounds/3034990
6. BuiltByBit / Kitsblox battlegrounds R6 animation pack listings (market evidence): https://builtbybit.com/resources/battleground-combat-animations-pack.95957/ · https://kitsblox.com/pack/soul-sword-combat-pack-r6
7. Roblox API reference, *Motor6D* (superseded for avatar rigs by AnimationConstraint): https://create.roblox.com/docs/reference/engine/classes/Motor6D
8. Roblox API reference, *AnimationConstraint* (AJU migration notes): https://create.roblox.com/docs/reference/engine/classes/AnimationConstraint · DevForum announcement: https://devforum.roblox.com/t/avatar-joint-upgrade-for-physically-simulated-character-movement-is-now-live/4298561
9. Roblox API reference, *Bone* (Transform; not replicated or serialized): https://create.roblox.com/docs/reference/engine/classes/Bone
10. Roblox Creator Docs, *Characters* overview: https://create.roblox.com/docs/characters
11. Roblox Creator Docs, *Adaptive Animation*: https://create.roblox.com/docs/characters/adaptive-animation
12. DevForum, *R6 legs are floating on idle animation (on custom Rig)* and related threads (R6 Motor6D names, RootJoint in HumanoidRootPart): https://devforum.roblox.com/t/r6-legs-are-floating-on-idle-animation-on-custom-rig/4194848
13. DevForum, *R6 to R15 Adapter [Beta]: Enable R15 Tech in R6 Experiences*: https://devforum.roblox.com/t/r6-to-r15-adapter-beta-enable-r15-tech-in-r6-experiences/2557840
14. Roblox Creator Docs, *Character appearance → Layered accessories on non-R15*: https://create.roblox.com/docs/characters/appearance
15. Roblox Creator Docs, *SLIM* (avatar restrictions): https://create.roblox.com/docs/workspace/streaming/slim
16. Roblox Creator Docs, *Avatar Settings*: https://create.roblox.com/docs/studio/avatar-settings
17. Roblox Creator Docs, *Avatar Setup specifications* (rig requirements): https://create.roblox.com/docs/avatar-setup/auto-setup-requirements
18. Roblox Creator Docs, *Importer* (Rig Type, Keep Zero Influence Bones): https://create.roblox.com/docs/studio/importer
19. Roblox Creator Docs, *Animation Editor*: https://create.roblox.com/docs/animation/editor
20. Roblox Creator Docs, *Improve performance → Humanoids*: https://create.roblox.com/docs/performance-optimization/improve
21. Roblox Creator Docs, *Create basic dynamic heads*: https://create.roblox.com/docs/art/characters/facial-animation/create-basic-heads
22. Roblox Creator Docs, *Skin a humanoid model*: https://create.roblox.com/docs/art/modeling/skin-a-humanoid-model
