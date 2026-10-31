---
tags: [environments, materials, materialvariant, terrain, textures, stylized]
updated: 2026-10-31
sources: 10
status: draft
---
# Materials and MaterialVariants for Stylized Worlds

## TL;DR
- Roblox's built-in materials (2022 set) look semi-realistic. For an anime look, **override them** with painted **`MaterialVariant`s** in `MaterialService` (global "Set as Override"), or assign variants per part through `BasePart.MaterialVariant`.
- MaterialVariant maps: `ColorMap` (alpha **not** used), `NormalMap`, `RoughnessMap`, `MetalnessMap`, `EmissiveMaskContent` + `EmissiveStrength`/`EmissiveTint`. Tiling uses `StudsPerTile` (default **10**) and `MaterialPattern` (`Regular` = ordered like bricks or planks; `Organic` = less repetition, like stone or dirt).
- **Expanded Terrain** (per-place, off by default) lets you paint **up to 62 custom terrain materials**, each with a color and an optional MaterialVariant. Multiple grass shades are possible without global overrides.
- `MaterialService.Use2022Materials`: mixing **legacy (pre-2022) terrain materials with MaterialVariants has a performance penalty**. Migrate to the 2022 set.
- Built-in materials use **far less memory** than custom textures. Use painted variants for the 3–6 biggest surfaces and plain `SmoothPlastic` + `Color` for everything else.
- `SmoothPlastic` (no texture) + flat colors is the purest "toon" base, and it instances by Material when there are no textures.

## Why it matters for anime battlegrounds
Most of the screen in a battlegrounds map is **floor, walls and terrain**. Painted tileables on those surfaces decide whether the map reads as anime or as "Roblox realistic". MaterialVariants are the cheapest way to restyle huge areas: no UV unwrapping, physics comes with them, and they apply to Parts *and* terrain. Pair them with [[Stylized Environment Kits]] for meshes and [[Toon Shading on Roblox]] for lighting.

## How to do it
### Step 1: Decide the base strategy
| Surface | Approach | Why |
|---|---|---|
| Large floors (asphalt, gravel, grass, concrete) | MaterialVariant override (painted tileable) | No UVs, huge coverage, physics kept |
| Terrain | Expanded Terrain custom materials (+ variants) | Several colors of the same base, up to 62 |
| Buildings and kit pieces | Trim sheet via SurfaceAppearance (see [[Stylized Environment Kits]]) | Detail with UV control |
| Small props | `SmoothPlastic` + color, or a shared atlas | Lowest memory |
| Glowing elements | Neon, or an emissive mask on the variant or SA | Neon is all-or-nothing, the emissive mask gives control |

### Step 2: Paint toon tileables
- **Size**: 512² or 1024² (the Roblox curriculum's practical max for tileables is 1024², and higher costs more). Parts display about 1024² over 8×8 studs by default, and terrain about 512² over 8×8 studs.
- **Content**: big, flat color shapes, 2–3 tones, **low-frequency** detail. No photo noise. Avoid single distinctive elements (one big rock) that make repetition obvious.
- **Normal map**: optional and subtle. Strong normals give realistic lighting breakup, which fights the toon look.
- **Roughness**: white (fully rough) for a matte anime surface. **Metalness**: black.
- **Seamless** on both axes. Check with a 3×3 tile preview.

> [!tip] Hide repetition
> Use `MaterialPattern = Organic` for stone, dirt and grass, so tiling is less regular. Add a few large decals (cracks, puddles, painted shadow blobs) to break up big floors, keeping the decal count capped (see [[Environment Performance Budgets]]).

### Step 3: Create a MaterialVariant (Material Manager)
1. Open **Material Manager**. Pick the closest **base material** (for example `Asphalt` for roads), so physics are inherited.
2. Create a variant, name it (for example `Anime_Asphalt`), and assign the Color, Normal, Roughness and Metalness maps.
3. Set `StudsPerTile`: for example **12–20** for roads (bigger paint strokes read as anime), **6–8** for tiles or bricks.
4. Set `MaterialPattern` (`Regular` for bricks or planks, `Organic` for natural surfaces).
5. To restyle the base material everywhere, enable **Set as Override** under Overrides. It shows up as `MaterialService.AsphaltName = "Anime_Asphalt"`. From scripts, use `MaterialService:SetBaseMaterialOverride()`.
6. `CustomPhysicalProperties` on the variant can override friction and density (inherited when not set explicitly).

Rules:
- Variants only work as **descendants of `MaterialService`**.
- Name + BaseMaterial is the identifier. Duplicates with the same pair mean only one is used.
- An override applies to **all** parts **and terrain** using that base material.

### Step 4: Terrain with Expanded Terrain
1. Workspace → **Expanded Terrain = Enabled**. The place restarts, and the terrain backend swaps (smaller file size, better terrain streaming and load times).
2. In the Terrain Editor material picker, click **+**, pick a name and base material, then a MaterialVariant and/or a **Color** tint.
3. Paint up to **62** custom materials, for example 3 grass shades (sunlit, shade, dry), path dirt and cliff rock.
4. Manage them in the **Terrain Materials Manager** (Window ▸ 3D). Deleted-but-used materials show **bright purple**.
5. Limitation: **custom physical properties on a variant aren't yet respected** by custom terrain material slots.
6. `TerrainDetail` instances can set different top, side and bottom faces for a terrain material, for example a grass top with dirt sides on cliffs.

### Step 5: Special materials for toon effects
| Material | Toon use | Caveats |
|---|---|---|
| `SmoothPlastic` | Default toon surface | No texture; instancing by Material |
| `Neon` | Glowing signs, energy pillars | Glow depends on color brightness, bloom and quality level. All-or-nothing |
| `ForceField` | Barrier or domain-expansion shells (animated) | Needs a MeshPart with UVs covering 0–1 and a TextureID with a wide value range |
| `Glass` | Windows | **Refraction not supported on mobile.** Transparency causes overdraw |

### Step 6: Memory discipline
- Roblox design-for-performance guidance: built-in materials use **far less memory** than custom textures, so save texture budget for textures that are central to the look.
- Proposal: **one biome = at most 6 custom variants** (2 floor, 1 wall, 3 terrain) at 1024², plus one trim sheet and one prop atlas.

> [!warning] Unverified
> The "≤6 variants per biome" figure is my own budget proposal, not a Roblox recommendation.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| `StudsPerTile` default | 10 | API dump |
| `MaterialPattern` | Regular / Organic | Enum docs |
| Custom terrain materials | up to 62 | Custom terrain docs |
| Tileable size | ≤1024² recommended | Env-art curriculum |
| Part default texel | 1024² per 8×8 studs | Texture specs |
| Terrain default texel | 512² per 8×8 studs | Texture specs |
| MaterialVariant `AlphaMode` default | Opaque | API dump |

## Checklist
- [ ] `Use2022Materials` on. No legacy terrain materials mixed with variants.
- [ ] Painted, seamless, low-frequency tileables, roughness white, metalness black.
- [ ] Overrides set only for base materials you want restyled globally.
- [ ] Expanded Terrain enabled for multi-shade terrain.
- [ ] StudsPerTile tuned against character scale (stroke size readable at 30–60 studs).
- [ ] Memory checked (F9) after adding variants.

## Common Mistakes
- Photo-scanned textures on an anime map.
- Overriding `Plastic` globally, which accidentally restyles every default part, including UI-ish props.
- Expecting `ColorMap` alpha to cut holes in a MaterialVariant. Its alpha is not used.
- Tiny `StudsPerTile` values, which produce noisy, buzzing textures at distance.
- Relying on custom physical properties in Expanded Terrain slots (not yet respected).

## Related
- [[Stylized Environment Kits]]
- [[Toon Shading on Roblox]]
- [[Stylized Trees, Foliage and Rocks]]
- [[Environment Performance Budgets]]
- [[Texturing Anime Characters]]

## Sources
Roblox docs were checked 2026-10-31 against `github.com/Roblox/creator-docs` (commit 2026-10-29). create.roblox.com was unreachable from the sandbox.
1. Materials (overrides, Material Manager, base materials, footnotes): https://create.roblox.com/docs/parts/materials
2. MaterialVariant class: https://create.roblox.com/docs/reference/engine/classes/MaterialVariant
3. MaterialService class (Use2022Materials penalty, override API): https://create.roblox.com/docs/reference/engine/classes/MaterialService
4. MaterialPattern enum: https://create.roblox.com/docs/reference/engine/enums/MaterialPattern
5. Custom terrain materials (Expanded Terrain, 62 materials, limitations): https://create.roblox.com/docs/parts/custom-terrain-materials
6. Material enum (ForceField, Glass mobile refraction): https://create.roblox.com/docs/reference/engine/enums/Material
7. Texture specifications (texel defaults): https://create.roblox.com/docs/art/modeling/texture-specifications
8. Env-art curriculum, Develop polished assets (tileables ≤1024): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/develop-polished-assets
9. Design for performance (materials use less memory): https://create.roblox.com/docs/performance-optimization/design
10. Roblox API dump (StudsPerTile, AlphaMode defaults): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
