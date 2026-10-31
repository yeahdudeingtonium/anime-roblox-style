---
tags: [characters, limits, reference, cheat-sheet, validation]
updated: 2026-10-31
sources: 15
status: draft
---
# Roblox Character Limits Cheat Sheet

> [!info] How this was researched
> Every number was read on 2026-10-31 from Roblox's official docs source (`github.com/Roblox/creator-docs`, `main`), which builds create.roblox.com. The site itself was unreachable from the research session. Re-check before shipping, because Roblox changes avatar specs often (2026 alone brought the Dynamic Head Migration and the Avatar Joint Upgrade).

## TL;DR
- **Engine:** ≤ 20,000 tris per mesh · ≤ 4 bone influences per vertex · 1 material and 1 UV set per mesh · textures up to 4096². [1][2]
- **Avatar body (Marketplace):** 15 parts, **10,742 tris total**, head 4,000. Dynamic head with **≥ 17 FACS poses**. Textures ≤ 2048². [3][4]
- **Accessories:** rigid or layered **≤ 4,000 tris**, single mesh. Layered needs inner and outer cages. [5][6]
- **In-game-only characters** (your fighters, NPCs, bosses) only have to meet the *engine* limits. Avatar-validation rules apply to things you sell or that must work as player avatars.
- **2026 changes:** player avatars now always have **dynamic heads** (classic faces converted), and new experiences default to **AnimationConstraint** joints instead of Motor6D on R15 player characters. [7][8]

## Why it matters for anime battlegrounds
This is the one-page lookup for modelers and riggers. Details and reasoning live in the linked notes: [[Anime Character Modeling in Blender]], [[Blender to Roblox Studio Export Pipeline]], [[Skinning and Weight Painting for Roblox]].

## Numbers & Settings

### Geometry
| Item | Limit | Source |
|---|---|---|
| Any MeshPart | 20,000 tris | [1] |
| Avatar body total | 10,742 tris (≈ 5,495 quads) | [3][9] |
| DynamicHead | 4,000 tris | [3] |
| Torso (Upper + Lower) | 1,750 tris | [3] |
| Each arm / each leg (3 parts) | 1,248 tris | [3] |
| Rigid accessory | 4,000 tris, single mesh | [5] |
| Layered accessory | 4,000 tris, single mesh | [6] |
| Topology | Watertight, quads preferred, no n-gons, no zero thickness | [1][3] |
| Orientation (body spec) | Face +Z, up +Y; transforms frozen, pivots 0,0,0 | [3] |
| Orientation (Avatar Setup) | Front −Z | [9] |
| Pose | I / A / T (Avatar Setup prefers A/T) | [3][9] |

### Body size (validation)
| Item | Min (W × L × D studs) | Max | Source |
|---|---|---|---|
| Whole body | 1.0 × 4.0 × 0.5 | 8.0 × 10.0 × 4.0 | [3] |
| Head | 0.05 × 0.5 × 0.05 | 4.0 × 2.0 × 4.0 | [3] |
| Arm / Leg | 0.05 × 0.5 × 0.05 | 4.0 × 4.5 × 4.0 | [3] |
| Torso | 0.05 × 0.65 × 0.05 | 4.0 × 4.0 × 4.0 | [3] |
| Fill rule | Parts ≥ 50% of their bounding box (front/side/back) | | [3] |
| Mannequin heights | Normal about 5.75–6.5, Slender about 5.25–6.25 studs | | [5] |

### Rig and skinning
| Item | Value | Source |
|---|---|---|
| Standard R15 joints | 15 (Root → HumanoidRootNode → LowerTorso → …) | [3] |
| Advanced R15 optional joints | up to 37 (Spine, Chest, Clavicles, HeadBase, 30 fingers, 2 toes) | [3] |
| Influences per vertex | ≤ 4 | [1] |
| Root influences | none (dropped on import) | [1][10] |
| Rest bones | rot 0,0,0; scale 1,1,1; root at 0,0,0 | [1] |
| Face rig | `RootFaceJoint` (e.g. `DynamicHead`) under `Head`; < 50 joints advised | [11] |
| Required FACS poses | 17 | [4] |
| Dynamic-head validation tests | L blink, R blink, jaw open, happy, sad | [4] |
| Mouth landmark | 2nd vertex loop from the lip opening | [4] |
| Attachments on a body | 19 (`*_Att` in Blender) | [3][12] |
| Joint type for R15 players (new experiences) | AnimationConstraint (AvatarJointUpgrade default) | [8] |

### Naming
| Thing | Pattern | Source |
|---|---|---|
| Body parts | `Head_Geo`, `UpperTorso_Geo`, `LeftUpperArm_Geo`, … (15) | [3] |
| Attachments | `Hat_Att`, `Hair_Att`, `Neck_Att`, `Root_Att` (0,0,0), `LeftGrip_Att`, … | [3] |
| Cages | `<Mesh>_OuterCage` (bodies), plus `<Mesh>_InnerCage` (layered) | [1][6] |
| Bundled face accessories | `EyebrowAccessory`, `EyelashAccessory`, `HairAccessory` | [6] |
| Special skin joints | `RBX_Leader`, `RBX_Follower` (weight 1.0 only) | [13] |

### Textures
| Item | Value | Source |
|---|---|---|
| Engine max | 4096² | [2] |
| Humanoid character (PBR budget) | 1024² max | [2] |
| Hair / shoes / t-shirt class | 256² | [2] |
| Jackets / pants class | 512² | [2] |
| Rigid accessory non-albedo maps | ≤ 256² | [2] |
| Marketplace avatar items | ≤ 2048² | [3][5][6] |
| Normal maps | OpenGL tangent space | [2] |
| Upload formats | .png .jpg .tga .bmp | [2] |
| Classic shirt template pieces | 128×128, 64×128, 128×64, 64×64 | [14] |

### Accessory boxes (Normal scale, studs, W × H × D)
| Type | Size | Source |
|---|---|---|
| Hat | 1.87 × 2.5 × 1.87 | [5] |
| Hair | 1.87 × 3.12 × 2.18 | [5] |
| Face | 1.87 × 1.25 × 1.25 | [5] |
| Back | 9.86 × 8.59 × 4.87 | [5] |
| Layered tops/bottoms | 8 × 8 × 8 | [6] |
| Eyebrows/eyelashes | 1.5 × 0.5 × 0.5 | [6] |

### Marketplace MeshPart properties
Material **Plastic** · Transparency **0** · VertexColor **1,1,1** · no Scripts or extra Parts in the Model. [3][6]

> [!warning] Unverified
> - **Max bone count per mesh**: no official number found. DevForum anecdotes range from "no real limit" to import hangs on huge rigs.
> - **Texture page conflict**: "up to 4096×4096" vs "Maximum Texture Resolution 1024×1024" in the UV section of the same page. [2]
> - **Facing direction conflict**: +Z (body spec) vs −Z (Avatar Setup). [3][9]
> - **Custom split normals**: preservation on import is undocumented (see [[Anime Faces and Eyes on Roblox]]).

## Checklist
- [ ] Check this sheet against the live create.roblox.com pages each quarter
- [ ] Add a line here whenever a Studio import or validation error teaches us a new limit

## Common Mistakes
- Treating Marketplace limits (10,742 tris, 2048² textures) as **in-game** limits. In-game fighters only have to meet the engine limits.
- Treating old tutorials' numbers as current. The 10k-tris-per-MeshPart limit from the 2020 skinned-mesh beta is now 20k. [1][15]

## Related
- [[Anime Character Modeling in Blender]]
- [[Blender to Roblox Studio Export Pipeline]]
- [[Skinning and Weight Painting for Roblox]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Anime Faces and Eyes on Roblox]]
- [[Clothing and Accessories for Anime Characters]]
- [[Texturing Anime Characters]]
- [[NPC and Boss Characters]]

## Sources
1. Roblox Creator Docs, *General specifications*: https://create.roblox.com/docs/art/modeling/specifications
2. Roblox Creator Docs, *Texture specifications*: https://create.roblox.com/docs/art/modeling/texture-specifications
3. Roblox Creator Docs, *Character body specifications*: https://create.roblox.com/docs/avatar/character-bodies/specifications
4. Roblox Creator Docs, *Dynamic head specifications*: https://create.roblox.com/docs/avatar/dynamic-heads/specifications
5. Roblox Creator Docs, *Rigid accessory specifications*: https://create.roblox.com/docs/avatar/rigid-accessories/specifications
6. Roblox Creator Docs, *Layered accessory specifications*: https://create.roblox.com/docs/avatar/layered-accessories/specifications
7. DevForum (Roblox), *Completing the Dynamic Head Migration*: https://devforum.roblox.com/t/completing-the-dynamic-head-migration/4301387
8. Roblox API reference, *AnimationConstraint* / *Motor6D*: https://create.roblox.com/docs/reference/engine/classes/AnimationConstraint
9. Roblox Creator Docs, *Avatar Setup specifications*: https://create.roblox.com/docs/avatar-setup/auto-setup-requirements
10. Roblox Creator Docs, *Skin a humanoid model*: https://create.roblox.com/docs/art/modeling/skin-a-humanoid-model
11. Roblox Creator Docs, *Create basic dynamic heads*: https://create.roblox.com/docs/art/characters/facial-animation/create-basic-heads
12. Roblox Creator Docs, *Export character bodies* (15 meshes + 19 attachments): https://create.roblox.com/docs/avatar/character-bodies/export
13. Roblox Creator Docs, *Automatic Skinning Transfer*: https://create.roblox.com/docs/avatar/automatic-skinning-transfer
14. Roblox Creator Docs, *Classic clothing*: https://create.roblox.com/docs/avatar/classic-clothing
15. DevForum, *Skinned MeshPart Studio Beta* (2020 beta: 10k tris per MeshPart): https://devforum.roblox.com/t/skinned-meshpart-studio-beta/705528
