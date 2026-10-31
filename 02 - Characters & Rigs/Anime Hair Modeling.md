---
tags: [characters, hair, blender, accessories, anime]
updated: 2026-10-31
sources: 13
status: draft
---
# Anime Hair Modeling

> [!info] How this was researched
> Roblox limits come from the Roblox creator-docs source repo (`main`, 2026-10-31). Hair-technique sources are Blender Artists, Polycount and BlenderNation threads seen through search results.

## TL;DR
- Shonen hair on Roblox is almost always a **solid, closed mesh made of big spike clumps**, not hair cards. Cards need alpha transparency, which sorts badly, costs more, and fights cel-shading's hard edges.
- Budget: a **Rigid Hair accessory is ≤ 4,000 tris**, and the Hair box (Normal scale) is **1.87 W × 3.12 H × 2.18 D studs**, offset 1.25 up / 1.875 down, 0.9375 front / 1.25 behind. Spiky Goku-style hair often breaks that box, which only matters if you sell it on the Marketplace. In-game hair can be any size up to the **20k-tris-per-mesh** engine cap. [1][2]
- Best workflow: **curve or flat-plane blockout → convert → hand-clean low poly**. Don't decimate converted curves, because it wrecks the topology. [3][4][5]
- Shading: give each clump **its own smoothing island** (hard edges between clumps), then optionally transfer normals from a smooth hair-volume proxy so the whole head of hair shades as one shape. Paint a single **anime highlight band** ("angel ring") into the texture.
- Attach as an **Accessory on `HairAttachment`** for player-swappable hair, or **weld/skin into the head mesh** for fixed-design NPCs and bosses. Moving locks (ponytails, long bangs) get **bones**. See [[Clothing and Accessories for Anime Characters]].

## Why it matters for anime battlegrounds
Hair *is* the character's silhouette in shonen design (Gojo's upswept white hair, Goku's Super Saiyan spikes, Tanjiro's short tufts). Battlegrounds games sell transformations (awakening, "Super" forms) mostly through **hair shape and color swaps**, so the hair must be swappable and readable from about 40 studs away. See [[Shonen Anime Shape Language]].

## How to do it

### Step 1: Design the clump map
- Draw the hair in front, side, back and top views as **5–15 major clumps** (bangs 3–5, sides 2 each, back 3–6, crown 1–3). Anime hair reads from *few, big* shapes.
- Mark each clump's **root** (on the scalp) and **tip direction**. Spikes should point along a consistent "flow" (radiating from the crown or swept by wind).

### Step 2: Scalp base
- Duplicate the head's top half, scale it out about 0.02–0.05 studs, and delete the face area. This "skull cap" hides gaps between clumps and is the scalp color under the hair. About 100–250 tris.

### Step 3: Clumps. Pick a method
| Method | How | Pros | Cons |
|---|---|---|---|
| **Box-model spikes** | Cube → extrude 3–5 segments → scale tip to a point → bend | Cleanest topology, lowest tris (about 40–120 per spike) | Slow for many clumps |
| **Curve with bevel/taper** | Bezier curve, Geometry → Bevel (Profile: custom or a 3–4-point circle), Taper curve for the point; Object → Convert to Mesh | Fast to iterate on flow | Too many tris after conversion; clean by hand [3] |
| **Flat modeling** | Model the whole hairstyle as a flat plane, then wrap it onto the head with Curve / Simple Deform / Lattice modifiers [4] | Very fast for bangs | Messy for complex styles [5] |
| **Icosphere-strand low poly** | Start from an icosphere whose faces follow the skull; pull spikes from faces [6] | Very low poly, N64 look | Chunky |
| **Sculpt + retopo** | Sculpt in Dyntopo, retopo by hand [7] | Best for big organic hairstyles | Slowest |

Practical recommendation: **curve blockout → Convert to Mesh → delete every second edge loop along the length → merge the tip to one vertex**.

### Step 4: Tri budget per clump
- Spike cross-section: **3–4 sides** (triangular or diamond). Anime spikes read as faceted blades. 6+ sides only for large rounded locks.
- Length segments: **3–5** (more only where the clump curves hard).
- A 4-sided spike with 4 segments and a pointed tip ≈ 4×4×2 = **32 tris**. 40 such clumps ≈ 1,300 tris. A full hairstyle at **1,200–2,500 tris** is realistic and leaves room under the 4k accessory cap. (These are my arithmetic and recommendations.)

### Step 5: Normals and smoothing
- Mark **sharp edges** between clumps (select a clump boundary → Edge → Mark Sharp) and apply the **Smooth by Angle** modifier (Blender 4.1+) at about 30–40°. [8]
- Optional "one big shape" shading: build a low-poly **smooth hair volume** proxy around all clumps and **Data Transfer custom normals** from it. The whole hairstyle then shades like one soft blob with spikes. This is a common anime-NPR trick. Whether Roblox keeps the result is the same open question as in [[Anime Faces and Eyes on Roblox]] (pre-triangulate before FBX). [9]
> [!warning] Unverified
> Custom-normal preservation on Roblox import isn't officially documented. Test in Studio.

### Step 6: UVs and texture
- Lay every clump's UV strip **root-to-tip in the same direction** (e.g. root at the bottom of the UV space, tip at the top). Then *one* vertical gradient in the texture colors all clumps at once (dark root → base → light tip).
- Paint a **highlight band** ("angel ring", a jagged light band) across the strips at about 30–40% from the root. With aligned UVs it lines up across clumps automatically.
- Texture size: **256×256** is Roblox's recommended map size for hair-sized assets (2×2×2 stud space). 512 is plenty for a hero character's hair. [10]
- Transformation recolors: author the hair texture in **near-white grayscale** and tint via `SurfaceAppearance.Color` (multiplies the color map at no performance cost), or use `AlphaMode = TintMask` so only the hair region tints. Super Saiyan-style gold is then a property change, not a new texture. [11]

### Step 7: Body part or accessory?
| Choice | When | How |
|---|---|---|
| **Rigid Accessory** (`AccessoryType = Hair`) | Player-equippable hair; transformations swapped at runtime | Single mesh, `HairAttachment` in the Handle; matching `HairAttachment` on the head [2] |
| **Welded to head** | NPC or boss with a fixed design | Merge into the head mesh, or weld a MeshPart to Head |
| **Skinned to face/head bones** | Long bangs or ponytail that must swing | Add bones (e.g. 3–5 per ponytail), weight-paint; animate or simulate (SmartBone-style modules) [see [[Clothing and Accessories for Anime Characters]]] |
| **Layered (WrapLayer) hair** | Hair that must deform with a dynamic head's expressions | Needs inner and outer cages; `HairAccessory` naming when bundled with a body [12] |

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Rigid accessory max | 4,000 tris | Spec [2] |
| Engine max per mesh | 20,000 tris | Spec [1] |
| Hair box (Normal) | 1.87 × 3.12 × 2.18 studs | Marketplace fit [2] |
| Hair box (Slender) | 1.78 wide (height/depth as Normal) | [2] |
| Hair texture | 256² recommended, 512² hero | PBR budget table [10] |
| Rigid accessory non-albedo maps | ≤ 256² | Spec [10] |
| Marketplace texture cap | 2048² | [2] |
| Spike cross-section | 3–4 sides | Anime facets, low tris (recommendation) |
| Segments per spike | 3–5 | Recommendation |
| Smooth by Angle | 30–40° | Keeps clump edges crisp (recommendation) |
| Whole hairstyle | 1,200–2,500 tris | Recommendation |

## Checklist
- [ ] Clump map drawn in 4 views (5–15 major clumps)
- [ ] Scalp cap under the hair
- [ ] Spikes 3–4 sided, 3–5 segments, merged tips
- [ ] Sharp edges between clumps, Smooth by Angle applied
- [ ] UV strips aligned root→tip; one gradient plus highlight band
- [ ] Hair texture authored light/grayscale for tinting transformations
- [ ] Under 4k tris if it's an accessory; within the box if selling it
- [ ] Moving locks have bones and are weight-painted
- [ ] Imported and checked in Studio from 40 studs and in close-up

## Common Mistakes
- **Alpha hair cards** in a cel-shaded game: sorting artifacts, double cost, and they look Western-realistic.
- **Decimating a converted curve** gives shredded triangles and broken shading. Remove loops by hand. [3][5]
- **Random UV directions** so the root-to-tip gradient breaks per clump.
- **Dark baked texture** that can't be tinted. Multiplying tint can only darken, so author light. [11]
- **Hair as part of the head mesh** for an avatar body pushes the head under the 50%-fill rule and blocks hair swaps. [13]
- **Forgetting a scalp** so you can see through the gaps between spikes from above (top-down camera in many fights).

## Related
- [[Clothing and Accessories for Anime Characters]]
- [[Anime Character Modeling in Blender]]
- [[Texturing Anime Characters]]
- [[Toon Shading on Roblox]]
- [[Shonen Anime Shape Language]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs, *General specifications* (20k tris per mesh): https://create.roblox.com/docs/art/modeling/specifications
2. Roblox Creator Docs, *Rigid accessory specifications* (4k tris, Hair box, 2048 cap): https://create.roblox.com/docs/avatar/rigid-accessories/specifications
3. Blender Artists, *Tips for converting curves to low poly meshes to use in a game engine?*: https://blenderartists.org/t/tips-for-converting-curves-to-low-poly-meshes-to-use-in-a-game-engine/681160
4. BlenderNation, *Flat Modeling Anime Hair* (aVersionOfReality): https://www.blendernation.com/2020/02/01/flat-modeling-anime-hair/
5. Blender Artists, *Poly-modeling stylized hair*: https://blenderartists.org/t/poly-modeling-stylized-hair/1336729
6. Blender Artists, *How would you model spikey anime hair in an N64 style*: https://blenderartists.org/t/how-would-you-model-spikey-anime-hair-in-an-n64-style/1387855
7. Polycount, low-poly spiky + smooth hair discussion: https://polycount.com/discussion/comment/2646273
8. Blender 4.1 release notes, Modeling (Smooth by Angle modifier): https://developer.blender.org/docs/release_notes/4.1/modeling/
9. Blender Artists, *Customizing Normals tutorial series*: https://blenderartists.org/t/customizing-normals-tutorial-series/1369038
10. Roblox Creator Docs, *Texture specifications* (PBR budget table): https://create.roblox.com/docs/art/modeling/texture-specifications
11. Roblox Creator Docs, *PBR textures / SurfaceAppearance* (Color tint multiplier, TintMask): https://create.roblox.com/docs/art/modeling/surface-appearance
12. Roblox Creator Docs, *Layered accessory specifications* (HairAccessory naming): https://create.roblox.com/docs/avatar/layered-accessories/specifications
13. Roblox Creator Docs, *Character body specifications* (50% bounding-box rule): https://create.roblox.com/docs/avatar/character-bodies/specifications
