---
tags: [characters, pipeline, export, fbx, gltf, importer, avatar-setup, validation]
updated: 2026-10-31
sources: 16
status: draft
---
# Blender to Roblox Studio Export Pipeline

> [!info] How this was researched
> All Roblox settings come from the Roblox creator-docs source repo (`main`, 2026-10-31), which create.roblox.com is built from. The site itself was unreachable from the research session. Blender UI names match current docs (Roblox's tutorials reference **Blender 5.2**).

## TL;DR
- Blender scene: **Units → Unit System None** (1 BU = 1 stud). FBX export: **Path Mode Copy + Embed Textures**, **Apply Scalings: FBX Unit Scale**, Forward **Z**, Up **Y** (per Roblox's Blender page), **Add Leaf Bones OFF**, **Bake Animation OFF** (ON only for FACS/animation), **Custom Properties ON** for dynamic heads. [1][2][3]
- **glTF avoids the FBX 100× scale problem**, and a Roblox engineer suggested glTF (or pre-triangulating) when FBX triangulation breaks custom normals. Note glTF imports with an extra Model level per mesh. [1][4][5]
- Studio: **File → Import** (3D Importer). Pick **Rig Type** (R15 / Custom / No Rig), **Rig Scale** (Default=Classic, Rthro=Normal, Rthro Narrow=Slender), and **Constraint Type → Joint Upgrade** for avatar bodies. Untick **Upload to Roblox** while iterating. [4][6]
- Limits to check *before* export: **≤ 20,000 tris per mesh**, **≤ 4 influences per vertex**, **one material per mesh**, **one UV set, UVs inside 0–1**, textures **≤ 1024² recommended for characters** (engine supports up to 4096², Marketplace avatar items ≤ 2048²). [7][8][9]
- **Avatar Setup** (Avatar tab) turns a single mesh into a full R15 avatar (partition, rig, skin, FACS, cages, attachments). Use the **Development Avatar** preset for in-game characters, which allows skipping auto-decimation. [10]

## Why it matters for anime battlegrounds
You'll re-export each fighter dozens of times (moveset tweaks, transformation variants, VFX sockets). A repeatable pipeline that preserves scale, bone orientation and hard-edge shading means animators never redo work because "the import broke". This note is the canonical place for settings. Other notes link here.

## How to do it

### Step 1: Pre-flight in Blender
| Check | Rule | Source |
|---|---|---|
| Triangles | ≤ 20,000 per mesh; body parts per R15 budgets | [7][8] |
| Geometry | Watertight, quads where possible, no zero-thickness faces | [7] |
| Transforms | Applied (frozen); pivots at 0,0,0 | [7][8] |
| Bones | Rot 0 / scale 1 at rest, root at origin, no root weights | [7] |
| Influences | ≤ 4 per vertex (Weights → Limit Total 4) | [7] |
| Materials | 1 per mesh (Roblox meshes take one material) | [9] |
| UVs | Single UV map, inside 0–1; overlaps allowed | [9] |
| Names | `_Geo` body parts, `_Att` attachments, `_InnerCage`/`_OuterCage` cages | [8][11] |
| Modifiers | Applied or deleted (export settings don't run them reliably) | [3] |
| Pose | I/A/T-pose; A/T preferred by Avatar Setup | [8][10] |

### Step 2: Choose the format
| | FBX | glTF (.gltf/.glb) |
|---|---|---|
| Scale | Needs FBX Unit Scale (or 0.01) [1] | No scaling configuration needed [1] |
| Rig, skin, animation, cages, vertex colors, PBR | Yes [4] | Yes [4] |
| Hierarchy in Studio | MeshPart directly in Model [4] | Extra Model per mesh; extra Models for cage nodes (deletable) [4] |
| Hard edges | Kept (per bug report) | A bug report said glTF smoothed hard edges; staff attributed it to the exporter [12] |
| Normals | FBX triangulation can corrupt custom normals; pre-triangulate [5] | Suggested by staff as an alternative [5] |
| Dynamic head data | Custom Properties carry pose mapping [3] | Avatar Setup can export `.gltf` for FACS/cage edits [13] |

### Step 3: Blender FBX export settings (Roblox's documented set)
File → Export → FBX:
- **Include:** Limit to Selected Objects (if exporting a subset). **Custom Properties ON** (needed for dynamic-head pose mapping). [1][3]
- **Path Mode: Copy**, then click the **Embed Textures** toggle next to it. [2]
- **Transform:** Apply Scalings = **FBX Unit Scale** (keep every other scale at 1.0). Forward / Up as in Roblox's Blender page: **Z Forward, Y Up**. [1]
  - If size is still wrong: Transform → Scale **0.01**, *or* Scene Units → Unit Scale **0.01** (Roblox warns the latter causes camera and modifier issues). [1]
- **Armature:** **Add Leaf Bones OFF**. [2]
- **Bake Animation:** OFF for static meshes. For bodies with FACS: **ON**, with **NLA Strips / All Actions / Force Start/End Keyframes OFF**, **Simplify 0.0**, and the timeline Start/End covering all poses. [2][3]
> [!warning] Unverified
> Bone axes (Primary/Secondary) and "Only Deform Bones" aren't specified by Roblox. Defaults work for Roblox's templates. If a custom rig imports with bones rolled 90°, check that **Primary Bone Axis Y / Secondary X** (defaults) were kept.

### Step 4: Roblox Blender plugin (optional fast path)
- Roblox's open-source **"Upload to Roblox"** add-on (Blender ≥ 3.2) uploads selected objects or collections via Open Cloud as **Packages**. Re-uploading updates the package (with `PackageLink.AutoUpdate`). [14]
- Good for **props and static meshes**. For rigged characters, use the Importer, which shows rig, skin and cage previews and errors. Roblox calls the plugin a "reference implementation" (bug-fix PRs only). [14]

### Step 5: Import into Studio
Home/File → **Import** → choose file → **Import Preview**:
| Group | Setting | Recommended for an anime fighter | Source |
|---|---|---|---|
| File General | Upload to Roblox | OFF while iterating, ON for final | [4][10] |
| File General | Import Only As Model | ON | [4] |
| File General | Keep Zero Influence Bones | ON if you have socket/VFX bones | [4] |
| File General | Set Pivot to Scene Origin | ON (default) | [4] |
| File General | Uses Cage | ON if cages are present (auto-detected) | [4] |
| Rig General | Rig Type | **R15** (spec rig) / **Custom** (extra bones, bosses) / Custom Humanoid (advanced R15) | [4][6] |
| Rig General | Rig Scale | Default=Classic, Rthro=Normal, Rthro Narrow=Slender | [4][8] |
| Rig General | Constraint Type | Joint Upgrade (avatar bodies) | [6] |
| Rig General | Validate UGC Body | Opens Avatar Setup after import | [4] |
| File Transform | World Forward / Up | Front / Top | [1] |
| File Geometry | Scale Unit | Stud | [1] |
| File Geometry | Merge Meshes | OFF for rigs | [4] |
| Object Geometry | Make Double Sided | OFF (costs more); ON only for thin capes or cards | [4] |
| Object Geometry | Ignore Vertex Colors | OFF if you use vertex colors | [4] |

- Hover warning icons in the hierarchy for details. Errors block import. [4]
- Each new import goes into the **moderation queue**. Appeals take up to about 10 minutes. [10]
- Test as a player: rename the Model **`StarterCharacter`** and put it in **StarterPlayer**. [6]

### Step 6: Avatar Setup (optional)
- Avatar tab → **Avatar Setup** → Preset **Platform Avatar** (Marketplace, strict) or **Development Avatar** (NPCs and starter characters, looser). [10]
- Type each mesh: **Body / Layered / Rigid / Eye Layered**. Gear options: **Handle face as 2D decal**, **Create R15 with optional joints**, **Manually Align Front**, **Improve facial caging**, **Reduce triangle count** (untick to skip decimation for dev avatars). [10]
- Input requirements: total ≤ 10,742 tris, 2 eyes + 3 mouthparts as separate geometry, A/T-pose, front facing −Z, watertight, no accessories, distinct neck, with textures (multiple textures get baked to one per PBR channel). [13]

### Step 7: Post-import fixes
- Textures missing → upload via the Asset Manager, then set `TextureID` or add a SurfaceAppearance (`_ALB`, `_NOR`, `_RGH`, `_MTL`). [6]
- MeshPart props for Marketplace avatars: Material **Plastic**, Transparency **0**, VertexColor **1,1,1**, no Scripts or extra Parts. [8]
- `RenderFidelity` stays **Automatic** (full detail < 250 studs, medium 250–500, lowest > 500). [15]

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Blender Unit System | None | 1 BU = 1 stud [1] |
| FBX Apply Scalings | FBX Unit Scale | Correct size [1][2] |
| Fallback scale | 0.01 | [1] |
| Add Leaf Bones | OFF | [2] |
| Max tris per mesh | 20,000 | [7] |
| Max influences | 4 | [7] |
| UV sets | 1, inside 0–1 | [9] |
| Texture: engine max | 4096² | [9] |
| Texture: humanoid character recommended max | 1024² | PBR budget table [9] |
| Texture: Marketplace avatar items | ≤ 2048² | [8] |
| Normal maps | OpenGL, tangent space | [9] |
| Body triangle total (Marketplace) | 10,742 | [8] |
| Moderation appeal | up to about 10 min | [10] |

> [!warning] Unverified
> Roblox's texture page says both "up to 4096×4096" (general) and "Maximum Texture Resolution... 1024×1024" (UV-mapping section). Engine support vs per-asset guidance is the likely reading. Test whether a 2048² character map displays at full resolution on your target devices.

## Checklist
- [ ] Pre-flight table passes (tris, transforms, influences, names, UVs)
- [ ] FBX: Copy + Embed, FBX Unit Scale, Leaf Bones off, Custom Properties on
- [ ] Bake Animation only for FACS/animated exports, timeline range correct
- [ ] Import preset saved (`⋯ → Save as New`), e.g. "Anime Fighter R15" and "Anime Boss Custom"
- [ ] Upload to Roblox OFF while iterating
- [ ] StarterCharacter playtest done
- [ ] Final upload with Upload ON; asset IDs recorded in the character sheet

## Common Mistakes
- **100× size on import** because of Blender metric defaults with FBX. Use FBX Unit Scale or glTF. [1]
- **Leaf bones exported** leaves `_end` bones cluttering the rig and breaking name matching. [2]
- **Multiple materials per mesh** cause the mesh to split or the texture to be lost. Atlas into one. [9]
- **Two UV maps** (e.g. a lightmap UV left over): Studio only allows one. [9]
- **Forgetting Custom Properties** on dynamic heads so the FACS mapping is lost. [3]
- **Re-importing with Upload ON every time** fills the inventory with duplicates. [10]
- **Imported quads after normal editing** get FBX re-triangulation, breaking the face shading. [5]

## Related
- [[Anime Character Modeling in Blender]]
- [[Skinning and Weight Painting for Roblox]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Texturing Anime Characters]]
- [[Anime Faces and Eyes on Roblox]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs, *Blender* (units, import/export axes, FBX scale options, glTF note): https://create.roblox.com/docs/art/blender
2. Roblox Creator Docs, *Export settings* (Path Mode Copy, Embed Textures, Leaf Bones, Bake Animation): https://create.roblox.com/docs/art/modeling/export-requirements
3. Roblox Creator Docs, *Export character bodies* (Custom Properties, animation options): https://create.roblox.com/docs/avatar/character-bodies/export
4. Roblox Creator Docs, *Importer*: https://create.roblox.com/docs/studio/importer
5. DevForum, staff reply on FBX triangulation breaking custom normals: https://devforum.roblox.com/t/roblox-converts-incorrectly-some-normals-from-3d-models-when-im-making-my-own-shadings-for-avatars/2711054
6. Roblox Creator Docs, *Import character bodies* (Custom Humanoid, Joint Upgrade, StarterCharacter): https://create.roblox.com/docs/avatar/character-bodies/import
7. Roblox Creator Docs, *General specifications*: https://create.roblox.com/docs/art/modeling/specifications
8. Roblox Creator Docs, *Character body specifications*: https://create.roblox.com/docs/avatar/character-bodies/specifications
9. Roblox Creator Docs, *Texture specifications*: https://create.roblox.com/docs/art/modeling/texture-specifications
10. Roblox Creator Docs, *Avatar Setup*: https://create.roblox.com/docs/avatar-setup
11. Roblox Creator Docs, *Meshes* (importer name conversions): https://create.roblox.com/docs/parts/meshes
12. DevForum, *glTF importer invalid normals*: https://devforum.roblox.com/t/gltf-importer-invalid-normals/2612421
13. Roblox Creator Docs, *Avatar Setup specifications* and *Dynamic head specifications*: https://create.roblox.com/docs/avatar-setup/auto-setup-requirements · https://create.roblox.com/docs/avatar/dynamic-heads/specifications
14. GitHub, *Roblox Blender plugin* README: https://github.com/Roblox/roblox-blender-plugin
15. Roblox Creator Docs, *Meshes → Level of detail*: https://create.roblox.com/docs/parts/meshes
16. Roblox creator-docs source repo (mirror used): https://github.com/Roblox/creator-docs
