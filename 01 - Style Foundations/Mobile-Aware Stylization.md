---
tags: [style, performance, mobile, optimization, budgets]
updated: 2026-10-31
sources: 15
status: draft
---
# Mobile-Aware Stylization

## TL;DR
- Stylization is a **performance strategy**: flat colour, simple shapes and painted lighting are cheaper than PBR realism *and* read better on a 6-inch screen.
- Budget everything at the **scene** level. A DevForum checklist (which says it mirrors Roblox's docs) suggests staying under **~600 draw calls and ~650K triangles** in cluttered areas; a community guide uses **500 / 500K**; one vendor suggests **<100 draw calls** for mid-range phones (treat as aggressive).
- At 60 FPS each frame has **16.67 ms**. Lower-end phones crash from out-of-memory long before the GPU struggles, so **memory is the real mobile wall** (community target: <1.3 GB client memory).
- Use **built-in materials and reused meshes and textures** first. They cost far less memory than unique custom textures, and reuse keeps draw calls down (Roblox docs).
- Roblox now **streams textures** and (since 2026) renders up to 4K, serving weaker devices lower mips. Don't lean on this: flat-colour anime art at 512–1024 looks the same and costs less.
- **ShadowMap over Future** for big PvP maps; Future is per-pixel and each light adds cost.

## Why it matters for anime battlegrounds
A battlegrounds server is a worst case: 15–30 animated characters, each firing particles, meshes, beams and lights, often at the same moment. The map and characters must leave headroom for the VFX spikes, or the game hitches exactly when it should feel best (on the hit).

## How to do it

### Step 1: Pick a baseline device and profile from day one
- Roblox docs recommend choosing at least one **baseline device** and testing on it throughout development, watching frame rate and memory.
- Studio memory readings run server and client together and so overstate memory. Test in a live client on a real phone.
- Tools: MicroProfiler (Ctrl+F6), Developer Console (F9), the render stats overlay (Shift+F2) for draw calls and triangles.

### Step 2: Scene budgets
| Budget | Target | Source type |
|---|---|---|
| Frame time | 16.67 ms (60 FPS) | Roblox docs |
| Draw calls (scene), cluttered area | <600 | DevForum checklist (says it mirrors docs) |
| Triangles (scene), cluttered area | <650K | DevForum checklist |
| Draw calls (scene), conservative | <500 | Community optimisation guide |
| Triangles (scene), conservative | <500K | Community optimisation guide |
| Draw calls (UI) | Concern above ~150 | Community optimisation guide |
| Draw calls, mid-range mobile | <100 | Third-party vendor (aggressive) |
| Client memory | <1.3 GB | Community post |

> [!warning] Unverified
> Only the frame budget and the general advice are confirmed in Roblox's own docs. The numeric draw-call, triangle and memory targets are community or vendor rules of thumb. Profile on your own baseline device.

### Step 3: Asset-level budgets for anime battlegrounds
| Asset | Tris | Texture | Notes |
|---|---|---|---|
| Custom fighter body | 5K–15K | 1× 1024² | Under the ~20K per-mesh import cap |
| Hair / accessory | 1K–4K | 512² | Few big spikes |
| Weapon | 500–3K | 512² or shared atlas | Shonen weapons are big; use silhouette, not tris |
| Modular building piece | 200–2K | Shared trim/atlas | See [[Stylized Environment Kits]] |
| Tree | 300–1.5K + cards | Shared atlas | Instance the same mesh |
| VFX mesh (slash, ring) | 50–500 | 256–512² flipbook/gradient | Reuse across moves |

*(Asset ranges are working targets derived from the scene budgets above, not official Roblox figures.)*

Mesh LOD: Roblox's render-fidelity docs tier meshes by camera distance, highest under **250 studs**, medium **250–500**, lowest **500+**. Make sure your silhouette still holds at the lowest tier, especially on big landmark meshes.

### Step 4: Stylization choices that save performance
| Choice | Saves | Why |
|---|---|---|
| SmoothPlastic + vertex/part colours | Texture memory | Built-in materials use much less memory than custom textures (Roblox docs) |
| Texture atlases / trim sheets | Draw calls + memory | One texture shared by many meshes |
| Painted lighting in albedo instead of SurfaceAppearance PBR | 3 extra maps per asset | PBR needs colour + normal + roughness + metalness |
| Reused meshes, rotated and scaled | Draw calls | Roblox docs: reuse instead of importing duplicates |
| Flat colours tolerate low mips | Bandwidth | Texture streaming downgrades gracefully |
| "Hull" collision / simplified geometry | Physics + memory | Creatures of Sonaria team reduced size by switching meshes to hull (Roblox newsroom) |

Community claim to verify: images larger than 512×512 are stored uncompressed in memory unless used through SurfaceAppearance or MaterialVariant. If true, it's another reason to keep anime textures at 512 where they hold up.

### Step 5: Lighting and post-processing on mobile
- **ShadowMap** is the safer default for large maps. Future is per-pixel, so DPI scaling affects its cost, and each light adds significant cost. Roblox staff conceded not every Android device hits interactive frame rates on Future.
- Devices that lack per-pixel support **fall back ShadowMap → Voxel**, so design the baseline look to survive Voxel.
- **Ability lights**: cap at about 2–4 dynamic `PointLight`s per ability, short-lived, `Shadows = false`. *(Working rule, not an official number.)*
- Post: one ColorCorrection, light or no Bloom, avoid DepthOfField and SunRays on the baseline.

### Step 6: VFX headroom
- Each player's move should fit a **particle budget** (for example ≤300 live particles per ability, ≤1 s lifetime). See [[Anime VFX Fundamentals]].
- Pre-create VFX templates and clone/reuse them. Destroy them after their lifetime.
- `Highlight` is capped at **31 rendered**. Low-end devices fall back to a checker fill with no outline. Don't rely on Highlight for essential gameplay info on mobile.

### Step 7: Memory and streaming
- **Instance streaming** improves join time, reduces memory and raises frame rate (Roblox docs). Twin Atlas credits streaming for making Creatures of Sonaria load by what players see.
- **Texture streaming** loads high mips only when needed; you **cannot** globally disable it or pin a SurfaceAppearance at full resolution (community reply). Mobile players may see blurrier SurfaceAppearances, another reason to favour flat anime colour.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Frame budget | 16.67 ms | 60 FPS |
| Scene draw calls | 500–600 max | Community/doc-mirrored |
| Scene tris | 500K–650K max | Community/doc-mirrored |
| Per-mesh tri cap | ~20K (21K quoted by vendors) | Importer |
| Mesh LOD tiers | <250 / 250–500 / 500+ studs | Render fidelity docs |
| Highlight cap | 31 | Engine |
| Lighting tech | ShadowMap | Cost vs Future |

## Checklist
- [ ] Baseline phone chosen (for example a 3–4 year-old Android with 4 GB RAM)
- [ ] Shift+F2 stats recorded at the busiest spot of the map with 20 players spamming
- [ ] Atlas/trim plan for the environment kit
- [ ] Character textures ≤1024², accessories ≤512²
- [ ] Lighting set to ShadowMap; look tested on Voxel fallback
- [ ] StreamingEnabled tested; important arena geometry set to persist if needed
- [ ] VFX particle budget per move documented

## Common Mistakes
- Testing only in Studio on a gaming PC.
- Unique 1024² textures for every rock and crate.
- SurfaceAppearance PBR on stylized assets that are flat-coloured anyway.
- Future lighting + many PointLights per ability.
- Relying on Highlight outlines for team colours (31 cap + mobile fallback).
- Building to the per-mesh 20K cap on every asset ("it imported, so it's fine").

## Related
- [[Stylized Environment Kits]]
- [[Lighting for Anime Maps]]
- [[Anime VFX Fundamentals]]
- [[Toon Shading on Roblox]]
- [[Anime Character Modeling in Blender]]
- [[Shonen Anime Shape Language]]
- [[Battlegrounds Visual Language Analysis]]

## Sources
1. Roblox Creator Hub – Design for performance (baseline device, memory, materials, reuse, 16.67 ms): https://create.roblox.com/docs/performance-optimization/design
2. DevForum – Checklist for building optimization (600 draw calls / 650K tris, 512 px claim): https://devforum.roblox.com/t/checklist-for-building-optimization/3232350
3. DevForum – Real world building and scripting optimization for Roblox (500/500K, UI 150): https://devforum.roblox.com/t/real-world-building-and-scripting-optimization-for-roblox/3127146
4. Nilo – Optimize model for Roblox export (vendor; <100 draw calls, power-of-two textures, 21K cap): https://nilo.io/articles/optimize-model-for-roblox-export
5. GitHub – polywright "How Checks Decide" (20K tri cap cited from docs): https://github.com/m4bwav/polywright/wiki/How-Checks-Decide
6. Roblox Creator Hub – Meshes (render fidelity distance tiers): https://create.roblox.com/docs/parts/meshes
7. DevForum – Future vs ShadowMap performance: https://devforum.roblox.com/t/future-vs-shadowmap-performance/3246937
8. DevForum – Future is Bright on Android fully rolled out (per-pixel, DPI): https://devforum.roblox.com/t/future-is-bright-on-android-is-fully-rolled-out-client-beta/3235808
9. DevForum – Future Is Bright Phase 3 Studio Beta (fallback): https://devforum.roblox.com/t/future-is-bright-phase-3-studio-beta/639903
10. DevForum – 4k Texture Rendering: https://devforum.roblox.com/t/4k-texture-rendering/4316229
11. DevForum – SurfaceAppearance loads inconsistently on mobile: https://devforum.roblox.com/t/surface-appearance-loads-inconsistently-on-mobile-and-often-displays-at-very-low-quality-even-if-the-phone-allows-it/4530853
12. Roblox Creator Hub – Highlight: https://create.roblox.com/docs/reference/engine/classes/Highlight
13. Roblox Newsroom – Inside Roblox Studio: Creators Discuss Working in Unique Art Styles (July 2026): https://about.roblox.com/newsroom/2026/07/roblox-studio-fidelity-creator-interviews-twin-atlas-fluorlite-maximillian-ecos
14. GamesBeat – Twin Atlas is among the studios changing what Roblox games look like: https://gamesbeat.com/twin-atlas-is-among-the-studios-changing-what-roblox-games-look-like-exclusive-interview/
15. DevForum – PBR materials vs. Textures: https://devforum.roblox.com/t/pbr-materials-vs-textures/1943694
