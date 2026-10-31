---
tags: [vfx, performance, mobile, optimization, budget, overdraw]
updated: 2026-10-31
sources: 13
status: draft
---
# VFX Performance Budget

## TL;DR
- The two GPU killers are **fill rate** (big particles covering many pixels) and **overdraw** (many overlapping transparent layers). Both are called out in the official particle docs. [1]
- Hard engine limits: **Rate ≤ 400/s per emitter (100/s on mobile)**, **Lifetime ≤ 20 s**, **Highlights ≤ 255 per client**, **Debris ≤ 1,000 items**. [1][2][3]
- Flipbooks cost memory, and **clients low on memory turn them off automatically**, which is likely on older phones. Reuse textures and keep resolutions small. [1]
- Roblox gives **no official particle-count budget**. A community heuristic is **~500–800 active particles on desktop, ~150–300 on mobile**. Treat it as a starting point and profile. [4]
- Profile with the **MicroProfiler** (`Perform/Scene/UpdateView` covers particle updates) and test at **Editor Quality Level** lowest and highest. Property changes on ParticleEmitters can hit performance hard. [5][1]

## Why it matters for anime battlegrounds
A large share of battlegrounds players are on phones, and fights happen in clusters. Ten players ulting in one corner is the worst case the budget must survive. The climax frame is exactly when every effect stacks, so a frame drop lands on the moment that should feel best. A VFX artist portfolio for anime-style titles describes profiling every delivery against the game's particle budget as the step most artists skip [6].

## How to do it

### Step 1 — Understand the costs
| Cost | What drives it | Mitigation |
|---|---|---|
| **Fill rate** | Particle `Size` on screen. "The more pixels particles occupy on a player's screen, the more costly it is on the GPU" [1] | Smaller particles, fewer screen-filling layers, shorter big-flash lifetimes |
| **Overdraw** | Overlapping transparent particles, beams and meshes. "The more layers of transparent effects on screen, the more costly" [1]. The engine re-renders overlapping pixels [7] | Fewer layers, more opaque/cut-out shapes, avoid stacked semi-transparent spheres |
| **Draw calls** | Particles, decals and textures don't batch well and add draw calls [5] | Fewer unique emitters and textures per effect |
| **Property churn** | "Property changes to ParticleEmitters can have a dramatic impact on performance" [5] | Set properties once on templates. Don't animate emitter properties every frame |
| **Texture memory** | Unique textures, flipbooks | Shared atlases, ≤ 512–1024² sheets, reuse [1] |
| **Instance churn** | `Instance.new`/`Destroy` per hit | Clone templates, pool high-frequency parts [8] |
| **Script time** | Per-frame tweens, RenderStepped loops | TweenService over manual loops, disconnect on end |
| **Network** | Server-created VFX replicating | Client-side VFX ([[Scripting and Emitting VFX]]) |

Official design guidance also says to avoid partial transparency (values other than 0 and 1) where you can, because of overdraw [9]. VFX can't avoid it entirely, but you can keep large surfaces opaque or short-lived.

### Step 2 — Set per-effect budgets
> [!warning] Unverified
> No official per-effect numbers exist. These tiers are starting points derived from the community 150–300 mobile / 500–800 desktop heuristic [4], assuming up to ~4 simultaneous fights on screen.

| Tier | Peak live particles (desktop / mobile) | Emitters | Beams/Trails | Meshes | Screen FX |
|---|---|---|---|---|---|
| M1 hit | 20 / 8 | 1–2 | 1 trail | 0–1 | Shake (attacker/victim) |
| Dash | 30 / 12 | 1–2 | 1–2 trails | 0 | Speed lines (self only) |
| Skill | 80 / 30 | 3–5 | 0–3 | 1–3 | Shake |
| Ultimate | 200 / 70 | 5–8 | 0–6 | 2–6 | Impact frame + shake + FOV |
| Ambient map VFX | 100 / 30 (whole map) | few | few | 0 | none |

Estimate live particles for a burst: `EmitCount`. For a continuous emitter: `Rate × average Lifetime` (e.g. 40/s × 0.5 s = 20 alive).

### Step 3 — Mobile-specific rules
1. Rate cap is **100/s per emitter on mobile** [1]. Don't design auras that need 300/s.
2. Flipbooks may be disabled under memory pressure [1]. **Make sure the effect still reads with frame 0 only** (a static texture fallback).
3. Halve `EmitCount` and drop smoke and secondary layers when `SavedQualityLevel` is low ([[Scripting and Emitting VFX]]).
4. Avoid full-screen additive flashes stacking with Bloom. They're cheap, but tens of overlapping quads are not.
5. Test on a real low-end phone. Studio's emulator doesn't reproduce GPU fill-rate limits.

> [!warning] Unverified
> Graphics-quality behavior: DevForum users report `Rate` emission is throttled at lower quality (older rule of thumb: Rate × level/10) while `Emit()` is not. A 2026 bug report says quality no longer changes `Rate` after an update. One creator observed no `Rate` emission at the lowest quality. Behavior may change; re-test [10][11].

### Step 4 — Authoring rules that save frames
- **Shorter lifetimes.** Anime VFX wants this anyway (see [[Anime VFX Fundamentals]]).
- **Fewer, sharper particles** beat many soft ones. Use geometry (Beams, meshes) for big crisp shapes.
- **Fade size to 0** at end of life rather than holding big transparent quads.
- **Cap Trails** with `MaxLength`, and keep `Lifetime` short.
- **Beams:** keep `Segments` as low as the curve allows (default 10) [12].
- **Highlights:** destroy temporary ones. 255 is the per-client display cap [2].
- **Disable off-screen ambient emitters** by distance (`Enabled = false` beyond ~200 studs).
- **LOD for others' effects:** spawn a reduced version for fights far from the local player.

### Step 5 — Profile
1. **MicroProfiler** (Ctrl+F6 in client): watch `Perform/Scene/UpdateView` (rendering prep and particle updates) and `Perform/Scene/RenderView` [5].
2. **Render stats** (Shift+F2) for draw calls and triangles during a scripted 10-player ult stress test.
3. Studio Settings → **Editor Quality Level**: check effects at the lowest and highest level [1].
4. **Developer Console → Memory** → `GraphicsTexture` and `GraphicsParticles` while effects play.
5. Write a **stress-test script** that fires every ultimate at once on dummies and logs frame time.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Max emitter Rate | 400/s desktop, 100/s mobile | Official [1] |
| Max particle Lifetime | 20 s | Official [1] |
| Highlight cap | 255 per client | Official [2] |
| Debris cap | 1,000 | Official [3] |
| Active particles (heuristic) | 500–800 desktop, 150–300 mobile | Community [4] |
| Flipbook sheet | ≤ 1024², prefer 512² | Memory [1][13] |
| Ambient emitter cull distance | ~200 studs | Starting point |

## Checklist
- [ ] Each move has a documented tier and particle budget.
- [ ] Stress test: 10 dummies ulting at once ≥ 30 fps on a low-end phone.
- [ ] Effects read correctly with flipbooks disabled (frame 0 only).
- [ ] Low-quality path halves particles and drops secondary layers.
- [ ] No per-frame property animation on ParticleEmitters.
- [ ] Temporary Highlights destroyed. Trails capped.
- [ ] MicroProfiler capture saved for the worst-case scene.

## Common Mistakes
- **One giant soft glow particle covering the screen.** Huge fill-rate cost for a blurry result.
- **Stacked transparent spheres** (domain + shield + aura). Overdraw multiplies.
- **Tweening emitter `Rate`/`Size` every frame** instead of using NumberSequences [5].
- **Designing on a high-end PC at max quality only.**
- **Unique flipbook per move.** Memory pressure disables them all on phones [1].
- **Ignoring other players' effects.** Your 200-particle ult × 6 players = 1,200.

## Related
- [[ParticleEmitter Deep Dive]]
- [[Scripting and Emitting VFX]]
- [[Creating VFX Textures]]
- [[Element VFX Recipes]]
- [[Lighting for Anime Maps]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs, "Particle emitters" (fill rate and overdraw warnings, Rate 400/100, Lifetime 20 s, flipbook memory deactivation, Editor Quality Level). https://create.roblox.com/docs/effects/particle-emitters
2. Roblox Creator Docs, Highlight (255 simultaneous). https://create.roblox.com/docs/reference/engine/classes/Highlight
3. Roblox Creator Docs, Debris:AddItem (1,000 cap). https://create.roblox.com/docs/reference/engine/classes/Debris
4. Kitsblox, "Roblox Particle System Deep Dive" (500–800 desktop / 150–300 mobile heuristic). https://kitsblox.com/blog/roblox-particle-system-deep-dive
5. Roblox Creator Docs, "Improve performance" (particles/decals don't batch; ParticleEmitter property changes; UpdateView = particle updates; transparency overdraw). https://create.roblox.com/docs/performance-optimization/improve
6. Plebarae, Roblox VFX artist portfolio (profiling against particle budget). https://plebarae.com/
7. Roblox Creator Docs, "Optimize your experience" → Delete layered transparencies. https://create.roblox.com/docs/tutorials/curriculums/environmental-art/optimize-your-experience
8. DevForum, "PartCache, for all your quick part-creation needs". https://devforum.roblox.com/t/partcache-for-all-your-quick-part-creation-needs/246641
9. Roblox Creator Docs, "Design for performance" (avoid partial transparency). https://create.roblox.com/docs/performance-optimization/design
10. DevForum: "Particle emitter limit on low graphics is impacting my game" https://devforum.roblox.com/t/particle-emitter-limit-on-low-graphics-is-impacting-my-game/2159584 ; "Particle Emitters no longer change Rate with graphics quality" https://devforum.roblox.com/t/particle-emitters-no-longer-change-rate-with-graphics-quality/4834736 ; "Bypassing Particle LOD Rate Throttle" https://devforum.roblox.com/t/bypassing-particle-lod-rate-throttle/2446042
11. EasyVFX `docs/sharp-vfx.md` (lowest-quality Rate observation). https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
12. Roblox Creator Docs, Beam.Segments. https://create.roblox.com/docs/reference/engine/classes/Beam
13. DevForum, "Particles' Flipbook Release". https://devforum.roblox.com/t/particles%E2%80%99-flipbook-release/2029388
