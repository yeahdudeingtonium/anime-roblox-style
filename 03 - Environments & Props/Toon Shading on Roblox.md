---
tags: [environments, toon-shading, cel-shading, outlines, rendering, lighting]
updated: 2026-10-31
sources: 16
status: draft
---
# Toon Shading on Roblox

## TL;DR
- Roblox has **no custom shaders** and no unlit material. Every cel or toon look is put together from the engine's own features: outlines from `Highlight` or inverted hulls, shading painted into textures, and lighting that flattens what the renderer would otherwise shade.
- **`Highlight` is the cheapest outline.** The current docs allow **255** on screen at once (older docs and search caches say 31). The first visible Highlight costs up to about **1 ms of GPU on mobile**. You cannot set line thickness: `LineThickness` exists but is hidden and locked to Roblox's own scripts.
- **Inverted-hull outlines** (a duplicate mesh scaled out and turned inside out) give the classic anime ink line with thickness you control. The cost is double the triangles and draw calls for every outlined object.
- **Bake the shading into the albedo**: two- or three-tone hand-painted ramps, plus `SurfaceAppearance` with a strong emissive mask. This holds up better than any lighting trick, but emissive still multiplies with albedo, so the surface is never truly unlit.
- **Flatten the lighting**: `LightingStyle = Soft`, high `Ambient`/`OutdoorAmbient`, `EnvironmentDiffuseScale` 0, low `Brightness`, `GlobalShadows` on for hard cast shadows. This is the base layer every other trick sits on.
- Avoid the old hacks (fog-color banding, Neon layering, ForceField overlays) in production. They break on mobile, on low quality levels or across engine updates.

## Why it matters for anime battlegrounds
Shonen battlegrounds games (TSB, Jujutsu Shenanigans, Heroes Battlegrounds) sell **readability at speed**. Characters must pop off the map while VFX fill the screen. Real PBR shading with soft gradients works against the flat, graphic look of anime key frames (see [[Shonen Anime Shape Language]]). Toon tricks give silhouette separation and flat color blocks, and they leave room in value and saturation for [[Anime VFX Fundamentals]] to stand out. Because no shader route exists, every choice below is a trade between performance, how many devices it works on, and how authentic the look is.

> [!warning] Unverified
> I could not confirm in a primary source exactly which techniques TSB, Jujutsu Shenanigans or Heroes Battlegrounds use. From gameplay footage, most use **flat-colored, low-detail maps without outlines**, and outlines appear mainly on highlighted or targeted characters. Treat that as an observation, not a documented fact.

## Technique catalogue

### 1. `Highlight` outlines (engine-native)
A `Highlight` draws a silhouette **outline** plus an **interior fill** over a `Model` or `BasePart`. Parent it to the target, or set `Adornee`.

| Property | Default (`Instance.new`) | Toon use |
|---|---|---|
| `OutlineColor` | `[255,255,255]` | Set to near-black or a dark hue of the object, e.g. `[20,15,30]` |
| `OutlineTransparency` | `0` | `0` for ink lines; `0.3–0.5` for softer environment lines |
| `FillColor` | `[255,0,0]` | Irrelevant if fill is hidden |
| `FillTransparency` | `0.5` | **Set to `1`** for outline-only |
| `DepthMode` | `AlwaysOnTop` | **`Occluded`** for toon outlines (otherwise lines draw through walls) |
| `Enabled` | `true` | A disabled Highlight **still takes a slot** |
| `LineThickness` | `1` | Hidden, `RobloxScriptSecurity`. **You cannot change it** |

**Limits and costs (current docs):**
- **255** simultaneous Highlights per client. Any beyond that are silently ignored, and disabled ones still count. Older docs said 31, and search engines still show that number.
- The **first** visible Highlight costs the most, up to **1 ms of GPU on mobile**. Extra Highlights add little.
- On mobile, the cost grows with **screen coverage**. On other platforms it does not.
- Adding or removing a Highlight can trigger a **geometry rebuild**, which causes spikes and extra draw calls. Create Highlights once and change their properties, which is cheap.
- Do not nest Highlighted objects inside other Highlighted objects, because draw order is back-to-front and the result breaks.
- One Highlight on a parent `Model` outlines the **whole model's silhouette** and draws no internal lines. You get an outer contour only, with no crease or inner lines.
- Low-end devices render Highlights "more pixelated".
- Community reports say Highlights misbehave on **transparent parts without a Humanoid**, and that `Occluded` looks odd on some iOS devices.

**Pros:** no extra geometry, a single instance per model, works on any mesh or part, toggles at runtime.
**Cons:** fixed thin line width that scales with screen resolution, no inner lines, the 255 cap, a mobile GPU cost, and no per-face control. You cannot outline a whole city with it.

> [!tip] Where Highlights fit in battlegrounds
> Use them on **characters, interactables and the current lock-on target**, not on the environment. With 12–20 players per server you stay far under 255. Use one outline color for allies and another for enemies.

### 2. Inverted-hull outlines (mesh technique)
This is the classic anime-game method (the Guilty Gear and Genshin family). Duplicate the mesh, push its vertices out along their normals by a small distance, **flip the normals**, and color it flat black. Only the inner back faces of the shell render, so they show as a rim around the silhouette.

How to build it:
1. In Blender, duplicate the mesh, use **Solidify** with a negative thickness or Alt+S *Shrink/Fatten*, then *Mesh ▸ Normals ▸ Flip*. Export as a separate mesh or a second object in the same FBX.
2. Import it to Roblox as a `MeshPart`. Set `Material = SmoothPlastic`, `Color` near-black, `CastShadow = false`, `CanCollide = false`, `CanQuery = false`, `CanTouch = false`, and `DoubleSided = false`.
3. Weld it to the base part. One community report says welding a CFrame-inverted outline can "un-invert" it. Flipping the normals in Blender avoids that.
4. Shell thickness for props of 2–10 studs is about **0.02–0.06 studs**. Scale it with object size, because the line gets thinner on screen as distance grows.

Alternatives people use: a `SpecialMesh` with one or three negative scale axes, or a CFrame with inverted handedness. These are hacky, and their behavior after engine updates is unverified.

**Pros:** real thickness control, can be colored per object, shows inner silhouette lines on concave shapes, no slot cap.
**Cons:** **doubles triangle count** and adds a draw call for each unique outline mesh. Shell intersections show up on thin parts. The line thins at distance, so a far city loses its lines. Skinned characters need the shell skinned too. Watch the 20,000-triangle limit per mesh.

> [!example] Budget math
> A 3,000-tri prop with a hull becomes about 6,000 tris. Fifty identical copies still **instance into one draw call per mesh** if `MeshContent` and texture/SurfaceAppearance match, so a hulled **kit** is affordable while hulled **unique props** are not.

### 3. Baked gradient / hand-painted shading (texture technique)
Paint the light into the albedo: a light side, a shadow side in a **hue-shifted** darker tone (shift shadows toward blue or purple, not plain black), and an optional rim or highlight band. This is the most reliable cel look, because the renderer only adds a small amount of shading on top.

- Use a **2-step or 3-step ramp** per material: base, shadow at about 70–80% value with the hue shifted 10–20° toward cool, and an optional highlight.
- For kits, put the ramps on a **trim sheet / atlas** so many props share one texture. See [[Stylized Environment Kits]].
- Combine with the flattened lighting setup (technique 6) so the runtime shading does not fight the painted shading.
- For characters, see [[Texturing Anime Characters]].

**Pros:** works on every device and quality level, costs nothing at runtime, gives full art direction.
**Cons:** the light direction is fixed in the texture, so the sun cannot move freely. It takes more texture authoring time, and it looks wrong if a strong dynamic light hits it from the "painted shadow" side.

### 4. `SurfaceAppearance` tricks
`SurfaceAppearance` (on `MeshPart`s) supports `ColorMap`, `NormalMap`, `RoughnessMap`, `MetalnessMap`, **`EmissiveMaskContent`**, `EmissiveStrength`, `EmissiveTint`, `Color` (tint) and `AlphaMode` (`Overlay`, `Transparency`, `TintMask`, `Opaque`).

- **Emissive "pseudo-unlit"**: a white emissive mask with tuned `EmissiveStrength` adds a constant light term. The docs state that emissive is **added to the lighting, and the sum is multiplied by the albedo**. Shadows therefore get lifted toward flat color but never become fully unlit, and large values **clamp to white**. Start at `EmissiveStrength` 0.3–0.6 and tune per lighting preset.
- **Flat normals**: leave out the normal map, or bake **spherical or "bent" normals** into it, so shading wraps smoothly over a whole form instead of per facet. This matters a lot for foliage (see [[Stylized Trees, Foliage and Rocks]]).
- **Roughness 1 / Metalness 0**: a white roughness map and a black metalness map kill specular highlights, which is key to a matte anime look. Also keep `Lighting.EnvironmentSpecularScale` at 0. Its default is 0.
- **`TintMask` AlphaMode**: one shared grayscale texture, recolored per instance through `SurfaceAppearance.Color`. This is useful for palette variants of the same prop. Check instancing: per the performance docs, different SurfaceAppearances break instancing.
- **`ResampleMode = Pixelated`**: nearest-neighbor filtering gives crisp graphic edges on low-res toon textures.
- Most SurfaceAppearance properties **cannot be changed by scripts at runtime**.

**Pros:** official, PBR-compatible, the emissive path is the closest thing to unlit.
**Cons:** emissive is not truly unlit and is clamped by dynamic range. It only works on MeshParts. Its look changes with device quality level.

### 5. Decals with emissive masks
`Decal` now has `EmissiveMaskContent`, `EmissiveStrength` (default 1), `EmissiveTint`, PBR maps (normal, roughness and metalness are plugin-writable), `UVOffset`/`UVScale` and `ZIndex`. Use them for glowing kanji signs, painted shadow overlays and ink-line decals on primitive parts. Decals **do not batch well** and each one adds draw calls.

### 6. Lighting that flattens shading
This is the global base layer. See [[Lighting for Anime Maps]] for full presets.

| Setting | Toon value | Why |
|---|---|---|
| `Lighting.LightingStyle` | `Soft` | Officially described as "a flat, retro-Roblox look with softer lights and shadows" |
| `PrioritizeLightingQuality` | `true` to keep shadow maps, `false` to save view distance | With `Soft` + `true` you get shadow maps, which give crisp anime cast shadows |
| `Ambient` / `OutdoorAmbient` | High, e.g. `[140,140,150]` / `[170,170,180]` | Lifts the shadow side so the value range compresses toward two tones |
| `Brightness` | `1.5–2.5` | A moderate key light, so the lit side does not blow out |
| `EnvironmentDiffuseScale` | `0` | Dynamic sky ambient adds soft gradients, so turn it off |
| `EnvironmentSpecularScale` | `0` | No reflections |
| `ShadowSoftness` | `0–0.1` (only valid with `Realistic`) | Hard-edged shadows read as cel |
| `ColorGradingEffect.TonemapperPreset` | `Default` (vivid) or `Retro` (flatter, less contrast) | `Retro` imitates pre-2019 lighting |
| `ColorCorrectionEffect` | `Saturation` 0.1–0.3, `Contrast` 0.05–0.15 | Anime color pop |

> [!warning] Unverified
> The ambient and brightness numbers above are my own starting points, not values from Roblox documentation. Tune them in Studio at quality levels 1, 5 and 10.

### 7. Neon and ForceField abuse (legacy hacks)
- **Neon layering**: one community method makes parts glow with a bright Neon color and stacks slightly larger transparent Neon shells to tint them. The author warns that decals and textures go white in sunlight. Neon glow depends on color brightness and bloom, and quality levels change it. **Not recommended**, because it causes transparency overdraw and glow behaves differently on each device.
- **ForceField material outline**: overlay duplicate meshes using ForceField's rim "outline" property. Its own author says it is "not as good as inverse-sizing a mesh". ForceField needs a MeshPart with UVs covering most of 0–1 and a `TextureID` with a wide value range. It also animates, which you rarely want for outlines.
- **Fog-color banding**: setting `FogColor` to extreme values pushes the renderer past its color precision and produces banded, cel-like steps. It **needs no `Atmosphere`**, works best with SmoothPlastic, and per the community post "**completely breaks on devices without a dedicated GPU**", which means mobile. **Do not ship this.**

### 8. ViewportFrame cel shaders
Some creators render the world into GUI `ViewportFrame`s for post-processing. Workspace objects and terrain always sit behind ViewportFrame content, and the performance cost is high. This is only practical for menus or character showcases, not gameplay.

### 9. EditableImage / EditableMesh (runtime tools)
- `EditableMesh` exposes `SetNormal`, `SetFaceNormals`, `AddColor` and similar, so in theory you could **rewrite normals at runtime** (for example spherical normals on foliage) or generate hull shells procedurally. Limits are **60,000 vertices and 20,000 triangles**, there are strict client memory budgets, and it must be enabled per experience (*Allow Mesh / Image APIs*).
- `EditableImage` has a **max size of 1024×1024**, defaults to 512×512, and only **one displayed EditableImage updates per frame**. It could recolor a toon ramp at runtime, for example a time-of-day palette swap.
- **Verdict:** bake normals and ramps offline in Blender. Editables are for user-generated content and dynamic cases, not a shading pipeline.

## Decision matrix
| Technique | Mobile-safe | Perf cost | Authenticity | Use for |
|---|---|---|---|---|
| Highlight outline | Yes (≈1 ms first) | Low | Medium (silhouette only) | Characters, targets |
| Inverted hull | Yes | 2× tris | High | Hero props, characters |
| Baked ramp textures | Yes | None | High | Everything static |
| SA emissive lift | Mostly | Low | Medium | Flattening shadow side |
| Soft lighting setup | Yes | Saves | Medium | Global base |
| Neon / ForceField / fog hacks | **No** | Overdraw | Low | Don't |
| ViewportFrame | No | High | Medium | Menus only |

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Highlight cap | 255 / client | Current docs; disabled ones count |
| First Highlight GPU | ≤1 ms mobile | Docs |
| Hull shell offset | 0.02–0.06 studs | Starting point (unverified) |
| Mesh triangle limit | 20,000 per mesh | Docs; hull counts too |
| EditableMesh | 60k verts / 20k tris | Docs |
| EditableImage max | 1024×1024 | Docs |
| `ShadowSoftness` default | 0.2 (docs) / 0.5 (API dump instance default) | The two sources disagree. Set it explicitly |

## Checklist
- [ ] Set up the flattened lighting base (`Soft`, high ambient, `EnvironmentDiffuseScale` 0) first.
- [ ] Paint 2–3-tone ramps into the albedo for all static kit pieces.
- [ ] Kill specular: roughness 1, metalness 0, `EnvironmentSpecularScale` 0.
- [ ] Highlights only on characters and interactables, `FillTransparency` 1, `DepthMode` Occluded.
- [ ] Create Highlights once and change their properties. Never spam Add/Destroy each frame.
- [ ] Inverted hulls only on hero props with shared mesh IDs, so they instance.
- [ ] Test at graphics quality 1, 4 and 10 and on a real phone.

## Common Mistakes
- Leaving `DepthMode = AlwaysOnTop`, which makes outlines show through walls like a wallhack.
- Disabling Highlights instead of destroying them, which uses up the 255 slots.
- Shipping the fog-banding trick, which leaves mobile players with broken visuals.
- Painted shadows on one side combined with a moving sun, so the lighting contradicts the texture.
- An inverted hull with `CastShadow = true`, which produces a doubled, fat shadow.
- Pure-black shadow colors instead of hue-shifted ones, which look muddy and not anime.

## Related
- [[Lighting for Anime Maps]]
- [[Stylized Environment Kits]]
- [[Stylized Trees, Foliage and Rocks]]
- [[Materials and MaterialVariants for Stylized Worlds]]
- [[Shonen Anime Shape Language]]
- [[Texturing Anime Characters]]
- [[Anime VFX Fundamentals]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
Roblox docs were checked on 2026-10-31 against the official source repo `github.com/Roblox/creator-docs` (latest commit 2026-10-29), because create.roblox.com could not be reached from the research environment. Instance defaults come from the `Full-API-Dump.json` in Roblox-Client-Tracker.
1. Highlighting objects (255 limit, perf tips): https://create.roblox.com/docs/effects/highlighting
2. Highlight class reference: https://create.roblox.com/docs/reference/engine/classes/Highlight
3. Lighting class (LightingStyle, ShadowSoftness, Technology deprecation): https://create.roblox.com/docs/reference/engine/classes/Lighting
4. Global lighting guide: https://create.roblox.com/docs/environment/lighting
5. Post-processing / ColorGradingEffect: https://create.roblox.com/docs/environment/post-processing-effects
6. SurfaceAppearance class (emissive formula, AlphaMode, ResampleMode): https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance
7. Decal class (emissive/PBR decals): https://create.roblox.com/docs/reference/engine/classes/Decal
8. Material enum (ForceField requirements, Glass): https://create.roblox.com/docs/reference/engine/enums/Material
9. EditableMesh / EditableImage: https://create.roblox.com/docs/reference/engine/classes/EditableMesh , https://create.roblox.com/docs/reference/engine/classes/EditableImage
10. Improve performance (instancing rules): https://create.roblox.com/docs/performance-optimization/improve
11. Roblox API dump (instance defaults, LineThickness security): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
12. DevForum: Cel/toon-shading effect using ForceField: https://devforum.roblox.com/t/celtoon-shading-effect-using-forcefield/524315
13. DevForum: How To: Cel Shading Effect (fog banding, GPU caveat): https://devforum.roblox.com/t/how-to-cel-shading-effect/1472627
14. DevForum: Adding a Toon Shader (Highlight / Neon / Viewport approaches): https://devforum.roblox.com/t/adding-a-toon-shader/1851704
15. DevForum: How to add outlines into meshes / inverted mesh threads: https://devforum.roblox.com/t/how-to-add-outlines-into-meshes/1136992 , https://devforum.roblox.com/t/welding-a-mesh-with-an-inverted-cframe-gives-strange-behavior/1944337
16. DevForum: Highlight does not work with transparency on non-humanoid models: https://devforum.roblox.com/t/highlight-does-not-work-with-transparency-on-non-humanoid-models/2731329
