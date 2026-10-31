---
tags: [environments, performance, optimization, mobile, streaming, draw-calls, lod]
updated: 2026-10-31
sources: 14
status: draft
---
# Environment Performance Budgets

## TL;DR
- **Measure, don't guess**: Render stats (Shift+F2) give **Draw (scene)** calls and triangles. Roblox's own example budget for a baseline device is **under 1,000 draw calls and 1,000,000 triangles** in the worst view. A popular community guide aims lower, at **about 500 draw calls / 500k tris** in-scene and **≤150 UI draws**. Pick a baseline phone and test on it.
- **Instancing** collapses identical meshes into one draw call when the **`MeshContent` is the same** and the **SurfaceAppearance (or `TextureContent`) is identical**, or, with neither, the **Material** is identical. Upload each mesh once and duplicate it.
- **Decals, Textures and particles don't batch well.** Transparency overdraw and many shadow-casting lights are the other named killers.
- **StreamingEnabled** is on by default for new places. Recommended: `StreamingMinRadius` 64, `StreamingTargetRadius` 1024, `StreamOutBehavior = Opportunistic`, `ModelStreamingBehavior = Improved`.
- **LOD**: `MeshPart.RenderFidelity = Automatic` (High <250 studs, Medium 250–500, Low >500), plus **`Model.LevelOfDetail = SLIM`** for static models (cloud-generated composite LODs that also reduce draw calls). `Workspace.MeshStreamingAndImprovedLods` turns on mesh streaming with the "Wild Mesh Simplifier".
- Shadows **turn off below quality level 4**. Set `CastShadow = false` on small or distant parts and `Light.Shadows = false` on most lights.

## Why it matters for anime battlegrounds
Battlegrounds games are VFX-heavy: 15+ players spamming particles, beams, craters and screen effects. **The environment must leave GPU headroom for combat.** A map that runs at 60 fps empty can drop to 20 fps on a phone in a 6-player ultimate brawl. A large share of Roblox players are on mobile, so the environment budget is the part you control most tightly. See [[Anime VFX Fundamentals]] for the VFX side.

## How to do it
### Step 1: Pick a baseline device and budgets
Roblox recommends choosing at least one **baseline device**, testing on it throughout development, and deriving limits from the frame drops you see there. The Studio device emulator is **not** accurate for memory, because Studio runs server and client together.

| Budget (worst on-screen view) | Roblox example | Community target (low-end mobile) | My battlegrounds proposal* |
|---|---|---|---|
| Draw (scene) calls | < 1,000 | ~500 | **≤ 400 environment** (leave ~200+ for VFX/characters) |
| Scene triangles | < 1,000,000 | ~500k | **≤ 400k environment** |
| Draw (UI) | — | ≤ 150 | ≤ 100 |
| Shadow-casting local lights | "use fewer" | — | ≤ 4 visible |

\*My split between environment and VFX is a proposal (unverified). Profile your own combat.

> [!warning] Unverified
> An older DevForum post reported an iPhone 8 holding 60 fps at about 250k triangles and dropping to 30 fps above 500k. That hardware is dated, so use it only as a sanity check.

### Step 2: Instancing rules (draw calls)
From the performance docs, multiple meshes with the same `MeshContent` share **one draw call** when:
- SurfaceAppearances are **identical** (if present), otherwise `TextureContent`s are identical;
- Materials are identical when there is **neither** SurfaceAppearance nor TextureID.

Practical rules:
1. **Upload each mesh once**, then duplicate in Studio. Big-FBX imports create duplicate IDs. The docs include a command-bar script that prints `Name, MeshId` to find duplicates.
2. Use **Packages** so re-imports keep a single ID.
3. **Merge** static clusters that are always seen together. The curriculum example cut 8 draw calls to 1 for a tower, and the trade-off is coarser culling.
4. Don't vary a SurfaceAppearance per copy for "variety", because each variant is its own batch.
5. Note: **`Highlight`** add/remove can rebuild geometry and add draw calls (see [[Toon Shading on Roblox]]).

### Step 3: Triangles and LOD
- Per-mesh hard limit: **20,000 tris**.
- `RenderFidelity`: `Automatic` (distance LOD) is the default. **`Precise` on many meshes is a named common problem.** `Performance` trades looks for speed.
- **SLIM** (`Model.LevelOfDetail = SLIM`):
  - Generates **cloud-transcoded composite meshes with multiple LODs**, renders them when the original is streamed out *or* "when SLIM is more efficient", and **dramatically reduces draw calls, tris and memory**.
  - Requires StreamingEnabled, a place **saved to Roblox** (not a local file), and **Team Create** enabled.
  - Static models only: adding or removing parts, changing materials or animating breaks it. **Don't use it on destructibles.**
  - Keep each model's extent under about 64 cubic studs ("~64 cubic studs" per the docs) so it streams as a unit. Split big buildings into modules.
  - Generation can take 1–2 minutes. The legacy `StreamingMesh` imposter (untextured) can be batch-converted to SLIM.
- `Workspace.EnableSLIMAvatars` gives lightweight animated stand-ins for R15 avatars, which helps 20-player servers. R6 and custom-proportion avatars are excluded.
- `Workspace.MeshStreamingAndImprovedLods` (RolloutState, not scriptable): when enabled, meshes load **lowest LOD first** and stream in detail.

### Step 4: StreamingEnabled settings
| Property | Recommended | Notes |
|---|---|---|
| `StreamingEnabled` | true (default for new places) | Cannot be set by script |
| `StreamingMinRadius` | **64** (default) | Highest-priority radius. Raising it costs memory and bandwidth |
| `StreamingTargetRadius` | **1024** (default) | Max distance streamed |
| `StreamOutBehavior` | **Opportunistic** | Aggressively GC distant content, avoiding OOM. The docs call `LowMemory` the default |
| `ModelStreamingBehavior` | **Improved** | Most efficient for Nonatomic models |
| `ModelStreamingMode` | Atomic for scripted or destructible models; **minimize Persistent** | Persistent never streams out |
| `EnableSLIMAvatars` | Enabled | — |

- Arena maps (≤500 studs) sit fully inside the target radius, so streaming mostly helps join time and memory.
- Open-world maps (GPO / Blox Fruits style) rely on streaming plus SLIM for the islands. **Frustum streaming** (`Player.FrustumStreaming`) can stream long-range content inside the camera view, for example for scoped or long sightlines, at extra memory cost.
- Test with `StreamingTargetRadius = 64` to catch scripts that assume parts exist.

### Step 5: Transparency, decals, particles
- **Overdraw**: layered semi-transparent surfaces (foliage, glass, fog cards) render pixels repeatedly. Delete hidden layers and prefer alpha-cutout leaves with `Transparency = 0`.
- **Decals and Textures** each add draw calls. Cap crater decals (see [[Destructible Environments and Craters]]).
- **Particles**: property changes on `ParticleEmitter`s "can have a dramatic impact on performance". Prefer `:Emit(n)` bursts over toggling properties every frame.

### Step 6: Shadows and lights
- The engine degrades shadows with quality and **disables them below level 4**.
- `BasePart.CastShadow = false` on small and distant parts (shadow artifacts are possible), and on moving objects where you can.
- `Light.Shadows = false` unless it matters. Limit range and angle, use fewer lights, and disable lights by room or distance.
- Light range is **clamped to 120 studs**.

### Step 7: Memory and physics
- **Built-in materials** use far less memory than custom textures. Spend texture memory on what matters (see [[Materials and MaterialVariants for Stylized Worlds]]).
- Texture sizing: 256² for about 5-stud objects, 512² for 10, 1024² for 20 (max 4096²). The engine streams lower mips first.
- `CollisionFidelity`: `Box` has the lowest memory, and `PreciseConvexDecomposition` is the most expensive. Build complex collision from Box parts.
- Moving **skinned meshes** without a Humanoid force FastCluster rebuilds. Embed a Humanoid only for meshes that really move.

### Step 8: Profiling loop
1. Shift+F2: Draw (scene), tris, Draw (shadow), Draw (UI).
2. F9 Developer Console: memory (PhysicsParts, GraphicsTexture, and so on).
3. MicroProfiler (**Ctrl+F6** / ⌘F6 in Studio and the desktop client) for frame spikes. Pause the capture with Ctrl+P.
4. Repeat at quality 1, 4, 7 and 10 **on a real phone**, in the busiest arena view, with 6+ players using ultimates.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Roblox example budget | <1,000 draws, <1M tris | Design-for-performance doc |
| Community low-end target | ~500 draws, ~500k tris, UI ≤150 | DevForum guide |
| RenderFidelity bands | <250 / 250–500 / >500 studs | MeshPart docs |
| StreamingMinRadius / Target | 64 / 1024 | Streaming techniques |
| Shadows off | quality < 4 | Improve-performance doc |
| SLIM model extent | ~64 cubic studs | Streaming techniques |
| Light range clamp | 120 studs | Lighting class |
| EditableMesh limit | 60k verts / 20k tris | EditableMesh class |

## Checklist
- [ ] Baseline phone chosen. Budgets written down.
- [ ] Mesh ID duplicate scan run. Everything reused via Packages.
- [ ] `RenderFidelity` Automatic everywhere (no Precise unless justified).
- [ ] Static props and buildings `LevelOfDetail = SLIM`. Destructibles excluded.
- [ ] Streaming: Min 64, Target 1024, Opportunistic, Improved.
- [ ] CastShadow off on small or far parts. Lights shadowless by default.
- [ ] Overdraw check in dense foliage and glass views.
- [ ] Profiling pass with combat VFX running.

## Common Mistakes
- Testing performance only in Studio or on a gaming PC.
- Importing the whole map as one FBX, so nothing instances.
- `RenderFidelity = Precise` on everything "for quality".
- SLIM on models that change at runtime.
- Persistent models used to dodge streaming bugs, so memory never frees.
- Dozens of shadow-casting neon PointLights in night maps.

## Related
- [[Stylized Environment Kits]]
- [[Materials and MaterialVariants for Stylized Worlds]]
- [[Stylized Trees, Foliage and Rocks]]
- [[Destructible Environments and Craters]]
- [[Toon Shading on Roblox]]
- [[Lighting for Anime Maps]]
- [[Anime VFX Fundamentals]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
Roblox docs were checked 2026-10-31 against `github.com/Roblox/creator-docs` (commit 2026-10-29). create.roblox.com was unreachable from the sandbox.
1. Improve performance (draw calls, instancing, overdraw, shadows, collision): https://create.roblox.com/docs/performance-optimization/improve
2. Design for performance (baseline device, 1,000 / 1,000,000 example): https://create.roblox.com/docs/performance-optimization/design
3. Instance streaming: https://create.roblox.com/docs/workspace/streaming
4. Streaming techniques (recommended settings, SLIM extents): https://create.roblox.com/docs/workspace/streaming/techniques
5. SLIM: https://create.roblox.com/docs/workspace/streaming/slim
6. Frustum streaming: https://create.roblox.com/docs/workspace/streaming/frustum
7. MeshPart class (RenderFidelity table): https://create.roblox.com/docs/reference/engine/classes/MeshPart
8. Workspace class (MeshStreamingAndImprovedLods): https://create.roblox.com/docs/reference/engine/classes/Workspace
9. Texture specifications: https://create.roblox.com/docs/art/modeling/texture-specifications
10. Env-art curriculum, Optimize your experience: https://create.roblox.com/docs/tutorials/curriculums/environmental-art/optimize-your-experience
11. DevForum: Real world building and scripting optimization for Roblox (500/500k, UI 150): https://devforum.roblox.com/t/real-world-building-and-scripting-optimization-for-roblox/3127146
12. DevForum: Question about triangle count in Roblox avatars (iPhone 8 anecdote): https://devforum.roblox.com/t/question-about-triangle-count-in-roblox-avatars/249548
13. DevForum: Optimization For Roblox Environments: https://devforum.roblox.com/t/optimization-for-roblox-environments/3844846
14. MicroProfiler (Ctrl+F6): https://create.roblox.com/docs/performance-optimization/microprofiler
