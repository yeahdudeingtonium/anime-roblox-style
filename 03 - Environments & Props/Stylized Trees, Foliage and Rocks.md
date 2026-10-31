---
tags: [environments, foliage, trees, rocks, nature, stylized]
updated: 2026-10-31
sources: 14
status: draft
---
# Stylized Trees, Foliage and Rocks

## TL;DR
- Stylized (Ghibli or anime) trees = **simple trunk + clumped leaf-card canopy + edited normals** that point outward from the canopy volume, so the tree shades like a soft blob and not like hundreds of noisy planes.
- On Roblox, use **`MeshPart.DoubleSided = true`** for leaf cards instead of duplicating faces. The older normal-edit-with-duplicated-faces trick doubles polygons and is no longer recommended.
- Keep leaves **`Transparency = 0`** with alpha from the texture (`SurfaceAppearance.AlphaMode = Transparency`, or the mesh texture alpha). Overlapping semi-transparent foliage causes **transparency overdraw**, one of the explicitly named performance problems.
- Rocks: low-poly faceted forms (200–1,500 tris), **flat 2–3-tone painted textures**, chunky silhouettes. Reuse 4–6 rock meshes rotated and scaled, so they instance.
- Terrain grass (`Terrain.Decoration = true`, `GrassLength` default 0.7) moves with `Workspace.GlobalWind`. It is cheap ground cover but looks realistic, so tint terrain grass toward your palette or use painted MaterialVariants.

## Why it matters for anime battlegrounds
Nature maps (training forests, mountain arenas, the Naruto-style "valley" fight, GPO and Blox Fruits islands) are mostly trees and rocks. In fights they act as **landmarks and silhouette frames**, and they must not block reads or tank mobile frame rate when 15 players spam VFX. Rocks double as **destruction debris**: the same rock meshes become crater chunks (see [[Destructible Environments and Craters]]).

## How to do it
### Step 1: Trunk
- 300–1,200 tris. Taper, exaggerated S-curve, 3–5 primary branches leading into canopy clumps (see [[Shonen Anime Shape Language]]: big–medium–small rhythm).
- Paint a 2-tone bark texture with a vertical stroke direction, or use a bark tileable on a trim strip.
- `CollisionFidelity = Box` or `Hull`. Players don't need branch collisions. Box has the lowest physics memory per the performance docs.

### Step 2: Canopy cards
The workflow from the DevForum "Ultimate Guide to Stylized Trees" and related threads:
1. Model **3–7 clump volumes** (low-poly spheres or blobs) where the canopy masses go.
2. Scatter leaf cards over them, using Blender's particle system with **vertex groups / weight paint** controlling density. One feedback thread suggests about **60–100 hair particles** per clump.
3. Use a **leaf-cluster alpha texture**, not single leaves. Run it through an edge-padding tool like PixelFix so there is **no black halo** at alpha edges.
4. **Transfer normals**: add a *Normal Edit* modifier (radial, targeting the clump sphere) or *Data Transfer* from the clump volume, so every card's normal points outward like the sphere's. One thread reports Data Transfer not working for them, and Normal Edit is the more commonly cited route. This is the single biggest "stylized" step. 80.lv stylized-foliage breakdowns describe the same principle: change leaf normals "so that they react to lights as a unit".
5. Decimate or clean up. Target canopy tris **2,000–6,000** for a hero tree and **800–2,000** for a filler tree.

> [!warning] Unverified
> The tri targets above are my own budgets for mobile-friendly battlegrounds maps. Roblox only documents the 20,000-tri-per-mesh hard limit.

### Step 3: Roblox import settings for foliage
| Property | Value | Why |
|---|---|---|
| `DoubleSided` | `true` on leaf cards | Renders both faces without duplicated geometry (official property) |
| `Transparency` | `0` | Alpha cutout through the texture. Avoid partial part transparency, which causes overdraw |
| `SurfaceAppearance.AlphaMode` | `Transparency` (with part Transparency 0) | Opaque pixels render fully opaque and "works better with depth-based effects and occlusion" |
| `Material` | `Plastic`/`SmoothPlastic` | No unwanted base-material texture |
| `CastShadow` | `true` on hero trees, `false` on small bushes | Shadows are expensive. Disable them on small or far objects |
| `CanCollide` / `CanQuery` / `CanTouch` | `false` on canopy | Physics and raycasts skip foliage |
| `RenderFidelity` | `Automatic` | LOD by distance (<250 / 250–500 / >500 studs) |

A community feedback thread suggests turning double-sided **off** and cast shadow off on dense small foliage for performance. Profile both, because double-sided doubles the rasterized faces.

### Step 4: Toon color on foliage
- Paint the canopy texture in **3 tones**: shadow (cool, darker), mid, and a sun-catch rim on top.
- With radial normals plus `LightingStyle = Soft`, the lit and shadow split follows the clump shape, which gives a cel-like look. See [[Toon Shading on Roblox]].
- Vary hue between tree instances with **separate small texture variants** (2–3 per species). Each variant is its own instancing group, so keep the variant count low.

### Step 5: Wind
- Terrain grass and `Clouds` follow `Workspace.GlobalWind`. **Mesh trees don't** sway automatically.
- Mesh sway options: (a) skinned tree mesh plus a looped Animation (costly on many trees; the performance docs warn about skinned meshes moving), or (b) no sway, with motion coming from **falling-leaf `ParticleEmitter`s** that have `WindAffectsDrag = true` and `Drag > 0`, so particles follow global wind.
- Recommendation for battlegrounds: **static trees plus leaf particles near hero trees only.**

### Step 6: Rocks
- Shape: blocky, faceted, flat planes with bevel-like color bands (the "anime rock" look of GPO and Blox Fruits islands). 200–600 tris for small, 800–1,500 for cliff chunks.
- Texture: a top-down gradient (lighter top faces, cooler bottoms) painted into the albedo, plus an optional moss or grass cap as a separate mesh or a second trim row.
- Reuse **4–6 meshes** rotated and scaled for all rocks, so they instance.
- **Cliffs:** stack large rock meshes, or use **terrain** with a painted Rock MaterialVariant override for the bulk and mesh rocks as silhouette "teeth" on top.
- `CollisionFidelity = Hull` for walkable rocks, `Box` for decorative ones.

### Step 7: Ground cover and terrain
- Terrain voxels are **4×4×4 studs**. Terrain Grass shows **512×512 per 8×8 studs** (texel note in the texture specs).
- `Terrain.Decoration = true` gives animated grass on the `Grass` material only. Grass animation slows when the player has **Reduce Motion** on.
- Custom painted terrain materials: use **Expanded Terrain** plus custom terrain materials, or a MaterialVariant **override** on `Grass`/`Ground`. See [[Materials and MaterialVariants for Stylized Worlds]].
- Flower and bush scatter: 1–3 cheap meshes (≤200 tris), instanced. Avoid hundreds of unique decals.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Mesh tri limit | 20,000 | Mesh specs |
| Hero tree | 3k–7k tris total | Starting budget (unverified) |
| Filler tree | 1k–2.5k tris | Starting budget (unverified) |
| Rock | 200–1,500 tris | Starting budget (unverified) |
| Leaf particles per clump | 60–100 (Blender scatter) | DevForum feedback |
| RenderFidelity Automatic bands | <250 / 250–500 / >500 studs | MeshPart docs |
| Terrain voxel | 4×4×4 studs | Terrain docs |
| GrassLength | 0.7 default | API dump |

## Checklist
- [ ] Clump volumes, then cards, then normals transferred from the volumes.
- [ ] Leaf alpha edge-padded (no halo).
- [ ] `DoubleSided` on, `Transparency` 0, AlphaMode Transparency.
- [ ] Collisions and queries off on canopies, Box/Hull on trunks.
- [ ] 4–6 rock meshes reused everywhere.
- [ ] Shadows off on bushes and small rocks.
- [ ] Look at the densest forest view on a phone: watch Draw (scene) and overdraw.

## Common Mistakes
- Default flat-plane normals, which give noisy, "sparkly", realistic-looking canopies.
- Semi-transparent (`Transparency` 0.1–0.9) leaf parts layered deeply, which causes overdraw spikes.
- A unique mesh per tree from a big FBX import, so nothing instances.
- Precise collision on foliage, which costs physics memory.
- Tall dense forests in the arena center, where they hide fights and block camera sightlines.

## Related
- [[Toon Shading on Roblox]]
- [[Stylized Environment Kits]]
- [[Materials and MaterialVariants for Stylized Worlds]]
- [[Environment Performance Budgets]]
- [[Destructible Environments and Craters]]
- [[Battleground Arena Map Design]]
- [[Shonen Anime Shape Language]]

## Sources
1. DevForum: Ultimate Guide to Stylized Trees on Roblox: https://devforum.roblox.com/t/ultimate-guide-to-stylized-trees-on-roblox/1124673
2. DevForum: Trying to make "Stylized trees" correctly (Normal Edit, DoubleSided note): https://devforum.roblox.com/t/trying-to-make-stylized-trees-correctly/1359589
3. DevForum: Stylized foliage feedback (60–100 particles, PixelFix, settings): https://devforum.roblox.com/t/stylized-foliage-feedback/2894617
4. DevForum: Feedback on stylized trees: https://devforum.roblox.com/t/feedback-on-stylized-trees/2137703
5. MeshPart class (DoubleSided, RenderFidelity table): https://create.roblox.com/docs/reference/engine/classes/MeshPart
6. SurfaceAppearance class (AlphaMode behavior): https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance
7. Improve performance (overdraw, shadows, collision fidelity, skinned movement): https://create.roblox.com/docs/performance-optimization/improve
8. Terrain (voxels, grass decoration, Reduce Motion): https://create.roblox.com/docs/parts/terrain
9. Global wind (grass, clouds, particles WindAffectsDrag): https://create.roblox.com/docs/environment/global-wind
10. Texture specifications (terrain texel density): https://create.roblox.com/docs/art/modeling/texture-specifications
11. 80.lv: Forest Waypoint in UE4 (leaf normals react as a unit): https://80.lv/articles/forest-waypoint-in-ue4-creating-stylized-landscape-and-materials
12. 80.lv: Turning a 2D illustration into a 3D environment with a hand-painted look (spherical normals): https://80.lv/articles/turning-a-2d-illustration-into-a-3d-environment-with-a-hand-painted-look
13. 80.lv: Creating stylized 3D environment of Edo Japan featuring Mount Fuji (hand-placed leaf cards, test normals): https://80.lv/articles/creating-stylized-3d-environment-of-edo-japan-featuring-mount-fuji
14. Roblox API dump (GrassLength, Terrain.Decoration defaults): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
