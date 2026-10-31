---
tags: [environments, modular-kits, trim-sheets, atlases, grid, workflow]
updated: 2026-10-31
sources: 13
status: draft
---
# Stylized Environment Kits

## TL;DR
- Build maps from a **small modular kit** on a **fixed stud grid**. Roblox's own projects use **5 studs** (laser-tag curriculum) and **16 studs** (Beyond the Dark). Pick one grid and lock it before modeling.
- **Units import 1:1 as studs.** Blender "2 m" becomes 2 studs. Model in Blender with 1 unit = 1 stud.
- Texture with **trim sheets** (tile on one axis) plus **tileables** (tile on both axes) and a few **decals**. Beyond the Dark textured about 90% of its architecture with a handful of trim sets.
- Upload each mesh **once** and duplicate it in Studio. Identical `MeshContent` plus identical SurfaceAppearance or texture **instance into one draw call**. Use **Packages** to keep IDs stable across iterations.
- Pivot every piece at a **consistent corner** (forward-most lower corner) so it snaps with grid snapping, for example 5 studs and 90°.
- For the anime look, the trim sheet carries **painted 2–3-tone ramps and ink-line edges**, not PBR grunge. See [[Toon Shading on Roblox]].

## Why it matters for anime battlegrounds
Battlegrounds maps get **rebuilt constantly**: new arenas, seasonal reskins, destruction (see [[Destructible Environments and Craters]]). A kit lets one modeler fill a 1,000×1,000-stud map in days, keeps the art style consistent, and keeps draw calls low because every wall piece is the same mesh. Swappable trim sheets let you reskin, say, "Shibuya day" into "Shibuya ruined" without remodeling. See also [[Top Roblox Modeler Workflow Patterns]].

## How to do it
### Step 1: Lock the grid and the scale
| Decision | Roblox reference value | Notes |
|---|---|---|
| Character height | Default avatar roughly 5–6 studs (unverified, measure your rig) | Jump height 7.2 studs, WalkSpeed 16 (API defaults) |
| Grid | **5 studs** (Roblox env-art curriculum) or **16 studs** (Beyond the Dark) | The grid size is arbitrary but must be consistent across the project and every artist |
| Min wall height | 10 studs (curriculum) | Taller than the default 7.2-stud jump |
| Min doorway/hallway | 10 studs wide (curriculum) | Two players pass at once |
| Studio snap | 5 studs move, 90° rotate | Curriculum setting |

> [!tip] Battlegrounds scale
> Super-speed combat needs **bigger** modules than an RPG town. A 16-stud or 20-stud grid with buildings 40–120 studs tall reads better when players dash 50+ studs per move. See [[Battleground Arena Map Design]].

> [!warning] Unverified
> The 16/20-stud recommendation for battlegrounds is my own inference from gameplay speed, not a documented TSB or JJS spec.

### Step 2: Design the minimal piece list
Beyond the Dark's rule is **"Keep pieces simple"**: a few versatile pieces, not many one-offs. Each extra piece costs authoring time plus memory and performance.

**Starter anime-city kit (about 25 meshes):**
| Category | Pieces |
|---|---|
| Walls | Wall_1x1, Wall_2x1, Wall_Window_1x1, Wall_Door_1x1, Wall_Shutter_1x1 (convenience store), Corner_Out, Corner_In |
| Floors/roofs | Floor_1x1, Floor_2x2, RoofEdge_1x1, RoofCorner, Parapet_1x1 |
| Trim | Trim_Base, Trim_Mid (floor divider), Trim_Top (cornice) |
| Street | Sidewalk_1x1, Curb_1x1, Crosswalk_Decal, Road_2x2 |
| Props (instanced) | Vending machine, AC unit, utility pole, power-line Beam, bin, traffic cone, sign blank |

For shrine, dojo and city dressing lists, see [[Japanese Anime Set Dressing]].

### Step 3: Pivots and snapping
- Put the pivot at the **forward-most lower corner** or another logical snap point, as the Roblox curriculum kit does, so pieces "snap to a logical position… in 5 stud increments".
- Make every piece at least one grid unit tall and wide.
- In Studio, set the model's `PivotOffset`, or bake the pivot in Blender by placing the origin at the corner before export.
- Keep piece bounds on the grid exactly, for example 16.000 studs and not 15.98, or gaps flicker.

### Step 4: Trim sheets
A **trim sheet** tiles on **one** axis, and each row has a distinct treatment. A **tileable** tiles on **both** axes. Rules from the Roblox curriculum and Beyond the Dark:
- Avoid **contextual details** that only fit one object, because repeats become obvious.
- Make the sheet **square** (equal X and Y).
- You can go up to 1024×1024 for curriculum trim sheets, and higher resolution costs more. Roblox textures in general support up to **4096×4096**, and the engine streams lower mips first.
- Start with an **inventory** of needed materials, then build a **trim template** so map sets can be swapped (clean ↔ damaged).
- For alpha trims, set `SurfaceAppearance.AlphaMode` from `Overlay` to `Transparency`.
- Name SurfaceAppearances with an `_SA` suffix (for example `Metal_Trim_A_SA`) and turn them into **Packages** with `AutoUpdate`.

**Anime trim-sheet layout (1024×1024, 8 rows of 128 px):**
| Row | Content |
|---|---|
| 1 | Cornice with painted top light and ink line |
| 2 | Floor-divider band |
| 3 | Window-frame strip (white or grey aluminium) |
| 4 | Concrete wall, flat with 2-tone AO baked into the edges |
| 5 | Tile wall (bathroom-tile facade, a classic Japanese apartment look) |
| 6 | Wood plank (dojo or shrine) |
| 7 | Roof tile (kawara) strip |
| 8 | Neutral ink-line / edge strip for silhouette trims |

> [!warning] Unverified
> This 8-row layout is my own proposal, not taken from a published Roblox game.

### Step 5: Texture atlases for props
Small props (signs, bins, vending machines) share **one atlas texture**, for example 1024² holding 8–16 props. Benefits:
- Fewer texture uploads and less memory.
- Note: instancing in Roblox depends on **identical MeshContent plus identical texture or SurfaceAppearance**. An atlas alone does **not** merge different meshes into one draw call. It saves memory and texture binds, and every copy of the *same* prop still instances.
- Texel density guide from Roblox: about 256² for 5×5-stud objects, 512² for 10×10, and 1024² for 20×20. Default Parts show 1024² over an 8×8-stud face.

### Step 6: Tileables and MaterialVariants
For large flat surfaces (roads, plazas, terrain), use **MaterialVariants** in `MaterialService` instead of unique meshes. They cost no UV work and come with physics. See [[Materials and MaterialVariants for Stylized Worlds]] for `StudsPerTile` (default 10), `MaterialPattern` (`Regular` vs `Organic`) and overrides.

### Step 7: Import and reuse
- Studio imports an FBX as a `Model` with child `MeshPart`s per component (for example Top_Trim, Bottom_Trim, Wall).
- **Upload each mesh once, then duplicate.** Importing a whole map as one FBX gives identical meshes separate content IDs, which breaks instancing.
- Re-imported iterations get **new IDs** unless you update the Package. Re-import into the Package so you never ship two IDs of the same wall.
- Merge **static clusters** that are always seen together (a tower made of 8 parts) into one mesh. The curriculum cut 8 draw calls to 1. Don't merge things that destruction needs to break apart.

### Step 8: Greybox first
Greybox the arena with primitive Parts on the same grid (curriculum flow: greybox, then playtest, then swap in kit pieces). Only replace with art once the sightlines and traversal feel right. See [[Battleground Arena Map Design]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Grid | 5 or 16 studs | Roblox curriculum / Beyond the Dark |
| Unit import | 1 DCC unit = 1 stud | Beyond the Dark |
| Mesh tri limit | 20,000 per mesh | Mesh specs |
| Max texture | 4096² | Texture specs |
| Trim sheet (curriculum) | ≤1024², square | Env-art curriculum |
| Texel guide | 256²/5 studs, 512²/10, 1024²/20 | Texture specs |
| Snap | 5 studs / 90° | Curriculum |
| Min wall / door | 10 studs tall / 10 wide | Curriculum |

## Checklist
- [ ] Choose a grid and write it on the map's README.
- [ ] Blender scene unit scale = 1 and 1 unit = 1 stud. Origin at the snap corner.
- [ ] Piece list of 25 or fewer for v1, all on the grid.
- [ ] One trim sheet plus 2–4 tileables plus 1 prop atlas per biome.
- [ ] SurfaceAppearances turned into Packages, `_SA` suffix.
- [ ] Meshes uploaded once, duplicated in Studio. Verify IDs with a command-bar script.
- [ ] Greybox playtested before final art.

## Common Mistakes
- Importing the whole level as one FBX, which gives duplicate mesh IDs, no instancing, and a draw-call explosion.
- Off-grid pieces (15.9 studs), which cause z-fighting seams and gaps.
- Trim sheets with one-off details (a unique sign baked in) that repeat obviously.
- A different SurfaceAppearance per copy for color variety, which kills instancing. Use a shared texture plus vertex color or `TintMask` sparingly.
- Pivots in the mesh center, so nothing snaps.

## Related
- [[Materials and MaterialVariants for Stylized Worlds]]
- [[Japanese Anime Set Dressing]]
- [[Battleground Arena Map Design]]
- [[Environment Performance Budgets]]
- [[Toon Shading on Roblox]]
- [[Top Roblox Modeler Workflow Patterns]]
- [[Texturing Anime Characters]]

## Sources
Roblox docs were checked 2026-10-31 against `github.com/Roblox/creator-docs` (commit 2026-10-29). create.roblox.com was unreachable from the sandbox.
1. Env-art curriculum, Develop polished assets (trim sheets, tileables, kit pivots, 5-stud snapping): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/develop-polished-assets
2. Env-art curriculum, Greybox your environment (5-stud snap, 10-stud walls and halls): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/greybox-your-environment
3. Env-art curriculum, Assemble an asset library (SurfaceAppearance packages, import structure): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/assemble-an-asset-library
4. Env-art curriculum, Optimize your experience (duplicate IDs, 8→1 draw calls): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/optimize-your-experience
5. Beyond the Dark, Building architecture (16-stud grid, units as studs, trim sheets, 90%): https://create.roblox.com/docs/resources/beyond-the-dark/building-architecture
6. Texture specifications (4096 max, texel guide): https://create.roblox.com/docs/art/modeling/texture-specifications
7. Mesh specifications (20,000 tris): https://create.roblox.com/docs/art/modeling/specifications
8. Improve performance (instancing rules, packages): https://create.roblox.com/docs/performance-optimization/improve
9. MaterialVariant class: https://create.roblox.com/docs/reference/engine/classes/MaterialVariant
10. Roblox API dump (Humanoid defaults WalkSpeed 16, JumpHeight 7.2): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
11. Polycount trim-sheet / modular discussions: https://polycount.com/discussions/tagged/trim-sheet , https://polycount.com/discussion/238299/building-modular-interiors-question
12. Polycount wiki, Modular environments (referenced from forum): http://wiki.polycount.com/wiki/Modular_environments
13. Shermanwaffle Urban Japanese Street (modular, trim sheets, edge decals) via Polycount: https://polycount.com/discussion/comment/2749193/
