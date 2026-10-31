---
tags: [characters, texturing, surfaceappearance, cel-shading, atlas, anime]
updated: 2026-10-31
sources: 14
status: draft
---
# Texturing Anime Characters

> [!info] How this was researched
> Roblox facts come from the Roblox creator-docs source repo and API reference (`main`, 2026-10-31). create.roblox.com was unreachable from the research session. Anime-industry references (Guilty Gear Xrd, Genshin) come from secondary write-ups found in search, because the GGXrd GDC PDF host was blocked.

## TL;DR
- Roblox has **no custom shaders**, so the "anime look" on a character is mostly **in the texture**: flat base colors + **painted (baked) hard shadow shapes** + **painted line work**, lit by low-contrast scene lighting. See [[Toon Shading on Roblox]].
- One **atlas per character**, **one material per mesh**, **one UV set in 0–1**. Roblox's PBR budget table puts **humanoid characters at 1024×1024 max**. Hair and shoes are 256², jackets and pants 512². [1]
- **TextureID** = 1 color map, script-swappable, cheapest. **SurfaceAppearance** = color + normal + roughness + metalness + emissive mask, alpha modes and **free color tinting**, but its maps **can't be changed by scripts**. A SurfaceAppearance overrides TextureID. [2][3][4]
- For a matte cel look with SurfaceAppearance: **Roughness ≈ 1 (white), Metalness 0 (black), no normal map** (or a flat one), with an **EmissiveMask** for glowing eyes, cursed markings and auras. [2]
- Variants for free: author colors in **light/grayscale** and use `SurfaceAppearance.Color` (a multiplier) or `AlphaMode = TintMask` for team colors, transformation hair, and awakened clothing. [2]

## Why it matters for anime battlegrounds
A dozen characters, each with 2–3 forms, plus constant VFX. Texture memory and draw calls add up fast on phones. Anime style is the cheapest style to texture *well*: big flat color areas compress well and survive Roblox's automatic downsampling ("When rendering many textures at the same time, Roblox may downsample textures"). [1]

Industry reference points: Guilty Gear Xrd skipped normal maps entirely and controlled cel shading by hand [14]. Genshin-style characters typically don't self-shadow, so shading comes from light direction plus authored masks [13]. Both studios use custom shaders. On Roblox the equivalent control has to come from **painted textures**.

## How to do it

### Step 1: UV layout for an anime atlas
- **One UV map**, all islands inside 0–1, **overlaps allowed**. Mirror left/right limbs onto the same UVs to double texel density (unless the design is asymmetric, like a single sleeve or one-sided markings). [1]
- Texel priority (my recommendation for battlegrounds):
  | Region | Share of a 1024² atlas |
  |---|---|
  | Face (front-projected) | 20–30% |
  | Torso + outfit front | 25% |
  | Arms + hands | 15% |
  | Legs + shoes | 15% |
  | Back, under-arms, soles | 5–10% |
  | Emblems/details strip | 5% |
- Straighten islands along clothing seams and stripes (*Follow Active Quads* on quad strips). Straight UV lines make painted stripes and line art crisp. This is the same idea behind Guilty Gear Xrd's UV-aligned "inner lines" (secondhand sources). [5]

### Step 2: Base colors (flat)
- Fill each material zone with **one flat color** from the character palette (see [[Shonen Anime Shape Language]]). No gradients or noise at this stage.
- Skin: if players should keep their own skin tone, leave skin areas **transparent** and use `AlphaMode = Overlay`, which reveals `MeshPart.Color` underneath (Roblox's custom-skin-tone method). For fixed-design fighters, paint the skin. [2][6]

### Step 3: Painted shadows (the "baked cel" pass)
Pick one light direction for the whole roster (e.g. key light from upper front-left) and paint **one hard shadow tone** per color (2-tone cel). Optionally add a third darker "occlusion" tone in creases.
1. **Bake-assisted:** in Blender, set up a sun lamp, a material with a **Shader to RGB → Color Ramp (Constant interpolation)** at threshold about 0.5, and bake (Cycles → Bake → Diffuse/Emit) to get a hard-edged shadow mask. Then hand-clean it in Krita or Photoshop.
2. **Hand-painted:** paint the shadow shapes directly in Texture Paint mode. Anime shadows are *designed* shapes (under the chin, under the bangs, below the pecs, inner thighs), not physically correct.
3. Multiply the mask over the base colors with a **cool, saturated shadow tint** (e.g. skin shadow = base hue shifted 10–20° toward red/purple, not gray).
> [!tip] Why bake instead of relying on Roblox lighting
> Roblox's dynamic shading is soft (PBR), and the terminator moves with the sun. A painted 2-tone shadow stays anime under any map lighting. Keep the scene's dynamic shading weak (low contrast and ambient balance; see [[Toon Shading on Roblox]]) so the two don't fight.

### Step 4: Line art and details
- Paint **inner lines** (muscle lines, clothing folds, nose/lip lines) at 2–4 px on a 1024² map. Use dark versions of the local color, not pure black.
- Silhouette outlines are *not* textured. Use inverted-hull meshes or Highlight-based outlines (see [[Toon Shading on Roblox]]).
- Hair: gradient + "angel ring" highlight band on UV-aligned strips (see [[Anime Hair Modeling]]).

### Step 5: TextureID vs SurfaceAppearance
| | `MeshPart.TextureID` | `SurfaceAppearance` |
|---|---|---|
| Maps | 1 color | Color, Normal, Roughness, Metalness, EmissiveMask [2][4] |
| Transparency | Via texture alpha | AlphaMode: Overlay (default), Transparency, TintMask, Opaque (beta) [2] |
| Tinting | No | `Color` multiplier, no performance cost [2] |
| Emissive | No | `EmissiveMaskContent` + `EmissiveStrength` + `EmissiveTint` [2] |
| Script swapping | **Yes** (writable) [3] | **Maps no** (PluginSecurity); `Color`, `AlphaMode`, `Emissive*` yes [4] |
| Priority | Overridden if a SurfaceAppearance exists [7] | Wins |
| Avatar Setup | Recommends replacing with SurfaceAppearance for quality [8] | Preferred |

Recommended setup:
- **Player fighters/NPCs that swap face expressions:** body on SurfaceAppearance, face expressions on a separate small mesh using TextureID (see [[Anime Faces and Eyes on Roblox]]).
- **Mass NPCs:** TextureID only (one map, shared). Identical TextureContent lets identical meshes instance into one draw call. [9]

### Step 6: SurfaceAppearance values for a cel look
| Map | Value | Why |
|---|---|---|
| ColorMap | Painted albedo with shadows and lines | The look lives here |
| RoughnessMap | White (1.0), 64² or omit | Kills specular highlights, which read "plastic" [2] |
| MetalnessMap | Black (0), 64² or omit | No metal reflection on skin or cloth [2] |
| NormalMap | Omit (or a flat 128,128,255) | Normal-map lighting adds realism you don't want. OpenGL tangent space if used [1] |
| EmissiveMask | White where it glows (eyes in awakened mode, tattoos, energy lines) | Pulse `EmissiveStrength` from script for power-up [2] |
| Color (tint) | White default; tint per form/team | Multiplies the ColorMap [2] |
> [!warning] Unverified
> Whether omitting the Roughness map gives the same result as a pure-white map on all quality levels. Test both. Also, `AlphaMode.Opaque` is currently in beta. [2]

### Step 7: Vertex colors (texture-free option)
- The importer brings in **vertex colors** from FBX and glTF (toggle: *Ignore Vertex Colors*). For very low-poly NPC crowds you can paint flat colors and shadow zones as vertex colors and skip textures entirely. [10][11]
- Marketplace avatar items require the MeshPart's `VertexColor` *property* at 1,1,1. That is a different thing from imported per-vertex colors. [6]
> [!warning] Unverified
> How imported vertex colors combine with TextureID/SurfaceAppearance (multiply vs replace). Test before committing.

### Step 8: Resolution budget
| Asset | Roblox guidance | Anime battlegrounds suggestion |
|---|---|---|
| Humanoid character | 1024² max (8×8×8 stud size class) [1] | 1024² hero, 512² standard NPC |
| Hair, shoes, t-shirt-size | 256² [1] | 256–512² |
| Jackets, pants, long items | 512² [1] | 512² |
| Jewelry, brows | 64–128² [1] | 128² |
| Rigid accessory non-albedo maps | 256² max [1] | 64² flat roughness/metal |
| Marketplace avatar textures | ≤ 2048² [6] | n/a for in-game |
| By world size | 256² for 5×5 studs, 512² for 10×10, 1024² for 20×20 [1] | Bosses 15+ studs tall: 1024² atlas or 2 × 1024² |

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Materials per mesh | 1 | [1] |
| UV sets | 1, inside 0–1 | [1] |
| Engine texture max | 4096² | [1] |
| Character map | 1024² | PBR budget [1] |
| Normal map format | OpenGL tangent space, RGB 24-bit | [1] |
| Roughness / metal / emissive maps | 8-bit grayscale | [1] |
| SurfaceAppearance texture slots | 5 map types | [2] |
| Shadow tones | 1 (2-tone) or 2 (3-tone) | Anime convention (recommendation) |
| Inner line width | 2–4 px at 1024² | Recommendation |
| Draw-call instancing | Same mesh + identical SurfaceAppearance (or TextureContent) | [9] |

## Checklist
- [ ] One atlas, one material, one UV set per mesh
- [ ] Face island large and front-projected
- [ ] Flat base colors from the palette
- [ ] 2-tone (or 3-tone) shadow pass painted from one roster-wide light direction
- [ ] Inner lines painted; outlines handled by geometry/Highlight
- [ ] SurfaceAppearance: roughness white, metal black, no normal map
- [ ] Emissive mask for power-up glow; tested pulsing EmissiveStrength
- [ ] Transformation colors via `Color` tint or TintMask, not new textures
- [ ] Checked at 30+ studs on a low graphics level

## Common Mistakes
- **Realistic PBR maps** (normal, AO, specular) on an anime character make it look like a figurine, not a cel frame.
- **Gray shadows**: anime shadows are hue-shifted and saturated.
- **Expecting runtime ColorMap swaps.** Not script-writable. Swap instances or use TextureID. [4]
- **Dark-authored textures + tint**: tint multiplies, so a dark map can't turn gold. Author light. [2]
- **Multiple materials** (skin, cloth, metal) per mesh in Blender: Roblox meshes take one. Bake to one atlas. [1]
- **Unique texture per NPC clone** breaks instancing. Share textures across clones. [9]

## Related
- [[Toon Shading on Roblox]]
- [[Anime Faces and Eyes on Roblox]]
- [[Anime Hair Modeling]]
- [[Shonen Anime Shape Language]]
- [[Blender to Roblox Studio Export Pipeline]]
- [[NPC and Boss Characters]]

## Sources
1. Roblox Creator Docs, *Texture specifications* (resolutions, PBR budget, UV rules, formats): https://create.roblox.com/docs/art/modeling/texture-specifications
2. Roblox Creator Docs, *PBR textures / SurfaceAppearance* (alpha modes, tint, emissive): https://create.roblox.com/docs/art/modeling/surface-appearance
3. Roblox API reference, *MeshPart* (TextureID writable by scripts): https://create.roblox.com/docs/reference/engine/classes/MeshPart
4. Roblox API reference, *SurfaceAppearance* (map properties PluginSecurity; "most properties cannot be modified by scripts"): https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance
5. Polycount discussion of the Motomura/Guilty Gear Xrd line technique (secondhand): https://polycount.com/discussion/comment/2187341 · GDC Vault session: https://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
6. Roblox Creator Docs, *Character body specifications* (custom skin tone, 2048 cap, VertexColor property): https://create.roblox.com/docs/avatar/character-bodies/specifications
7. Roblox Creator Docs, *Meshes → Texture* (PBR overrides TextureID): https://create.roblox.com/docs/parts/meshes
8. Roblox Creator Docs, *Avatar Setup* (use SurfaceAppearance instead of TextureID): https://create.roblox.com/docs/avatar-setup
9. Roblox Creator Docs, *Improve performance → Draw calls*: https://create.roblox.com/docs/performance-optimization/improve
10. Roblox Creator Docs, *Importer* (vertex colors, Ignore Vertex Colors): https://create.roblox.com/docs/studio/importer
11. Roblox Creator Docs, *Blender → Vertex painting*: https://create.roblox.com/docs/art/blender
12. Roblox Creator Docs, *Blender and Maya texture settings* (Principled BSDF hookup for import): https://create.roblox.com/docs/art/modeling/assign-textures
13. ArtStation blog, B. J. Ayers, *Blender NPR: Recreating the Genshin Impact Shader* (characters don't self-shadow; face shading isn't custom normals): https://bjayers.artstation.com/blog/category/5
14. Game Watch Impress (GGXrd GDC 2015: about 40k polys, no normal maps, manual cel shading control): https://game.watch.impress.co.jp/docs/news/20150307_691725.html
