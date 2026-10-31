---
tags: [vfx, textures, flipbook, photoshop, krita, blender, embergen, workflow]
updated: 2026-10-31
sources: 14
status: draft
---
# Creating VFX Textures

## TL;DR
- Paint VFX textures **white/greyscale with the shape in alpha**, then tint in Roblox with `Color`. One texture serves every character's palette. [1][2]
- Size: power-of-two, **≤ 1024×1024** for particle and flipbook sheets in practice (larger uploads are reported to be downscaled to 1024). The general texture spec says up to 4096² for textures, so test. Frames: 2×2 → 512 px, 4×4 → 256 px, 8×8 → 128 px on a 1K sheet. [3][4][5]
- Leave **transparent padding** around every flipbook frame, and fade alpha to 0 before frame edges. Mipmaps bleed between frames otherwise. [5][6]
- **Edge padding:** transparent pixels must carry the shape's RGB (white), not black. Renderers write black into alpha = 0 pixels, and Roblox's bilinear filtering and mips bleed it into a grey halo. [2]
- Tools: Photoshop/Krita (hand-painted anime shapes), Blender (mesh + shader renders → sheets), EmberGen (real-time fluid sims → flipbooks, PNG/TGA/EXR export). [7][8][9]

## Why it matters for anime battlegrounds
Free toolbox textures (soft glows, sparkles) give every battlegrounds game the same mushy look. Custom crisp textures (hard-edged smoke puffs, jagged impact stars, brush-stroke slashes, stepped flame flipbooks) are where a game gets its identity. They're also where memory gets wasted: an 8×8 1024² flipbook used once is a poor deal on phones. Clients low on memory **disable flipbooks automatically** [3].

## How to do it

### Step 1 — Decide the texture type
| Type | Typical size | Use | Notes |
|---|---|---|---|
| Single particle sprite | 128–512² | Sparks, stars, glows, debris | Power of two, centered, alpha fades before edges |
| Flipbook sheet | 512² or 1024² | Smoke puffs, explosions, slash reveals, flames | 2×2, 4×4, 8×8 or Custom grid [3] |
| Beam/trail strip | e.g. 1024×64 or 512×128 | Slash trails, energy beams, lightning | Detail only across the width; filtering along the length is invisible [2] |
| Tiling noise | 256–512² | Scrolling beam bodies, mesh surfaces | Seamless in the scroll direction |
| Mesh texture (UV-mapped) | 512–1024² | Slash crescents, rings, domes | Gradient along U for tail → head |
| Screen overlay | 1024² | Speed lines, impact burst art | Used on ImageLabels |

Official general texture guidance: 256² for ~5×5 stud objects, 512² for ~10×10, 1024² for ~20×20, with a max of 4096² supported for textures [4]. That guidance targets surfaces. VFX sprites usually need far less.

> [!warning] Unverified
> Image upload resolution for decals/particle textures: DevForum posts state uploads above 1024×1024 are downscaled to 1024 [5], while the texture-spec page says 4096² is supported for textures [4]. Which applies to `ParticleEmitter.Texture` today is not confirmed. Author at 1024 max for VFX until tested.

### Step 2 — Paint anime shapes (Photoshop / Krita)
1. Canvas 512² (single) or 1024² (sheet), transparent background, 8-bit RGBA.
2. Paint in **pure white** on a transparent layer. Shape and opacity live entirely in alpha. Put a dark background layer underneath for viewing only, and hide it on export.
3. Anime language: **hard edges with a 1–2 px anti-aliased rim** (the community HD pack uses ~2 px AA edges) [10]. Stepped opacity (2–3 flat tones) instead of airbrushed gradients.
4. Shapes to stock: 4/6/8-point impact stars, crescent slash, radial burst lines, hard ring, round smoke puff (2–3 variants), flame tongue, spark streak (a thin vertical capsule), dust clump, rock chip, brush stroke (wind).
5. Export PNG (official formats: .png, .jpg, .tga, .bmp; PNG for alpha) [4].
6. **Krita** animation: draw frames on the timeline, export as an image sequence on a transparent background, then pack into a grid. A community "Spritesheet Exporter" Python plugin exports directly to a sheet with a set rows × columns [8].

> [!warning] Unverified
> Whether the Spritesheet Exporter is bundled with current Krita versions or needs installing from GitHub was not confirmed [8].

### Step 3 — Render from Blender
Good for slash reveals, shockwave flipbooks and toon smoke:
1. Model the shape (e.g. a crescent strip) and animate the reveal with a gradient/Voronoi shader driving alpha. A DevForum tutorial does slashes entirely this way, renders PNG frames, and assembles a sprite sheet for a particle flipbook [11].
2. Camera **orthographic**, framed square. **Film → Transparent** on. A Factorio guide documents the same transparent-background, orthographic-camera setup for sprite sheets [12].
3. Use **Emission** shaders (unlit) so lighting doesn't bake in. Color ramp in "Constant" interpolation gives stepped toon bands.
4. Render 16 frames (4×4) or 4 frames (2×2) at the frame size (256² for 4×4 on a 1K sheet).
5. **Fix edge colour:** fill transparent RGB with white (or push-pull the edge color outward). One community pack went from a grey rim to clean edges this way, and file size dropped from 3.5 MB to 1.4 MB [2].

### Step 4 — Simulate with EmberGen
- EmberGen exports image sequences and flipbooks as **EXR, PNG, TGA** [9].
- Pick a grid whose rows and columns **divide the resolution evenly**. Mismatches produce black frames at the end of the sheet [9].
- One user found 256² frames too pixelated when scaled up, and 512² frames pushed the sheet to 8K×4K (unusable on Roblox) [9]. For Roblox, the 1024² sheet ceiling means **4×4 at 256² or 2×2 at 512²**.
- Keep frame counts modest: about 64 frames is a production ceiling, and frame stride (render every other frame) plus blending fills the gaps [9]. On Roblox, 16 frames with `FlipbookBlendFrames` on is usually enough.
- Export **straight (unpremultiplied) alpha**. One developer had to switch EmberGen to straight alpha to match the viewport in-engine [9].
- For an anime look, post-process sim frames: posterize to 2–3 alpha levels, then threshold for hard edges. Realtime VFX threads suggest hand-painting as the best route for a stylized look, or toon-shaded polygonized sims [7].

### Step 5 — Pack the sheet
- Layout: left → right, top → bottom (frame 0 top-left). Equal cell sizes. The total size must be an exact multiple of the grid or Roblox shows `FlipbookIncompatible` [3].
- **Padding:** keep the art inside ~90% of each cell. Fade alpha to 0 before the cell edge, because semi-opaque pixels touching the edge get cut off [6]. A Roblox engineer noted that a UV-atlas margin is what prevents lower mips from bleeding between frames, and that older mobile GPUs limit how much the engine can compensate [6].
- ImageMagick one-liner (16 frames of 256² → 1024² 4×4 sheet):
  `magick montage frame_*.png -tile 4x4 -geometry 256x256+0+0 -background none sheet.png`
- Name assets clearly: `vfx_smoke_puff_4x4_1024.png`, `vfx_slash_arc_strip_1024x64.png`.

### Step 6 — Upload and test
1. Import via the Asset Manager (Bulk Import for many files) [13].
2. Set the emitter's `FlipbookLayout` to match, and check the frame order with `FlipbookMode = Loop`, `FlipbookFramerate = 4` (slow).
3. Check at Editor Quality Level lowest and highest [3], and on a phone (flipbooks may switch off under memory pressure [3]).

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Flipbook sheet sizes | 8² … 1024², power of two | Release thread [5] |
| Frame size on 1K sheet | 2×2 = 512, 4×4 = 256, 8×8 = 128 px | [5] |
| Custom grid | 1–64 columns/rows | [14] |
| Texture formats | png, jpg, tga, bmp | Official [4] |
| Max texture res (general) | 4096² | Official [4] |
| Edge AA | ~2 px | Community pack [10] |
| Alpha | Straight, transparent RGB = white | [2][9] |
| Strip textures | e.g. 1024×64 | [2] |

## Checklist
- [ ] White/greyscale texture, shape in alpha, tinted in Roblox.
- [ ] Power-of-two size, ≤ 1024² for particle use.
- [ ] Flipbook cells padded, alpha 0 at cell borders.
- [ ] Transparent pixels have white RGB (no dark halo).
- [ ] Straight alpha export.
- [ ] Grid divides the resolution exactly.
- [ ] One texture reused across many effects where possible (memory).
- [ ] Tested at the lowest quality level and on mobile.

## Common Mistakes
- **Baking color into the texture.** You then need a new upload per character palette.
- **Black matte halos.** Rendered PNGs with black RGB in transparent pixels give dirty edges at a distance [2].
- **8×8 sheets for big slow effects.** 128 px frames look blurry when large. Use 2×2 or a single texture [2].
- **Airbrushed soft gradients.** They read as realistic and mushy. Anime wants flat steps and crisp edges.
- **Art touching cell edges.** The next frame bleeds in at lower mips [6].
- **Too many unique flipbooks.** Memory pressure disables them on phones [3].

## Related
- [[ParticleEmitter Deep Dive]]
- [[Mesh-Based VFX]]
- [[Beams and Trails for Anime VFX]]
- [[VFX Performance Budget]]
- [[Toon Shading on Roblox]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs, "Particle emitters" guide (PNG with transparent background; greyscale + LightEmission 1). https://create.roblox.com/docs/effects/particle-emitters
2. EasyVFX `docs/sharp-vfx.md` §6–7 (edge padding, black RGB bleed, strip textures, 4×4 = 256 px frames). https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
3. Roblox Creator Docs, "Particle emitters" → Flipbooks (layouts, spacing, memory deactivation, FlipbookIncompatible) and ParticleEmitter reference. https://create.roblox.com/docs/effects/particle-emitters ; https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
4. Roblox Creator Docs, "Texture specifications" (formats; up to 4096²; 256/512/1024 guidance). https://create.roblox.com/docs/art/modeling/texture-specifications
5. DevForum, "Particles' Flipbook Release" (supported 8–1024 px sizes; frame math) https://devforum.roblox.com/t/particles%E2%80%99-flipbook-release/2029388 ; "Dramatically increase the maximum image / decal / texture upload size" (1024 downscale) https://devforum.roblox.com/t/dramatically-increase-the-maximum-image-decal-texture-upload-size/649052
6. DevForum, "Animated Particles with the Particle Flipbooks Beta" (margins, alpha to zero at edges, mip bleeding, textureQueryLod on old mobile). https://devforum.roblox.com/t/animated-particles-with-the-particle-flipbooks-beta/1718023
7. Real Time VFX, "Smoke spirte sheet" (hand-painting for stylized) https://realtimevfx.com/t/smoke-spirte-sheet/10838 ; "How do I achieve this 3d procedural stylized smoke effect?" https://realtimevfx.com/t/how-do-i-achieve-this-3d-procedural-stylized-smoke-effect/27363
8. imikado, kritaSpritesheetManager (Krita spritesheet export plugin) https://github.com/imikado/kritaSpritesheetManager ; Krita manual, Import Animation https://docs.krita.org/reference_manual/import_animation.html
9. JangaFX EmberGen product page (EXR/PNG/TGA) https://jangafx.com/embergen/ ; Real Time VFX "Embergen resolution issue" https://realtimevfx.com/t/embergen-resolution-issue/14270 ; JangaFX forum "Black border after render" https://forums.jangafx.com/t/black-border-after-render/1578 ; itch.io devlog (straight alpha) https://itch.io/post/7671987
10. EasyVFX `docs/impact.md` (v3 textures with ~2 px anti-aliased edges). https://github.com/VuxSussy/EasyVFX/blob/main/docs/impact.md
11. DevForum, "How to make Animated Slash Effects with only Blender!" https://devforum.roblox.com/t/how-to-make-animated-slash-effects-with-only-blender/1794034
12. Factorio forums, "[Guide] Making spritesheets with Blender" (transparent film, orthographic camera). https://forums.factorio.com/viewtopic.php?p=84796
13. Roblox Creator Docs, Asset Manager. https://create.roblox.com/docs/projects/assets/manager
14. DevForum, "[Client Beta] Optimize your particle animations with custom flipbook layouts". https://devforum.roblox.com/t/client-beta-optimize-your-particle-animations-with-custom-flipbook-layouts/4005128
