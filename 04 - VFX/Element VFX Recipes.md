---
tags: [vfx, recipes, fire, lightning, wind, water, cursed-energy, explosions, ground-cracks, dust]
updated: 2026-10-31
sources: 11
status: draft
---
# Element VFX Recipes

## TL;DR
- Each element is a **stack of 3–5 layers**: core (bright, additive), body (main hue), detail (sparks, strands), and residue (smoke, dust, embers; normal blend). [1][2]
- **Additive (`LightEmission 1`)** for fire, lightning, energy and holy. **Normal blend (`LightEmission 0`)** for smoke, dust, water body, rocks and dark/cursed energy, because additive can't darken [3].
- Structure every recipe as anticipation → impact → dissipation (see [[Anime VFX Fundamentals]]). The values below are for the impact and dissipation layers. The charge-up is usually the same textures with `ShapeInOut = Inward`.
- Ground effects (cracks, craters, dust rings) come from **raycast-placed meshes/rocks + Disc-shaped dust emitters**. Several DevForum crater/rock modules exist (TSB-inspired). [4]
- All numbers are **starting points**. Tune them against reference clips and the [[VFX Performance Budget]].

> [!warning] Unverified
> Every property value in the recipe tables below is an untested starting point written for this vault, not copied from TSB, JJS, Heroes Battlegrounds or Type Soul. The property semantics and ranges are verified against the official API [3][5][6]; the specific numbers are not. Set status to `verified-in-studio` only after testing.

## Why it matters for anime battlegrounds
Movesets are built from elements: fire fists, lightning dashes, wind slashes, water whips, cursed energy blasts, ground slams. Having a tested base recipe per element means each new move is a variation (scale, color, timing), not a blank page. It also keeps the game's look consistent.

## How to do it

### Conventions used in the tables
- `Size` / `Transparency` written as keypoints `t:value` (t = 0–1 lifetime).
- Colors as RGB. `Color` written as `t:RGB` keypoints.
- "Emit N" = burst with `Rate 0` + `Emit(N)`. "Rate N" = continuous.
- All emitters: `LightInfluence 0` unless noted (set it explicitly; see [[ParticleEmitter Deep Dive]]).

```lua
-- helpers for building sequences in code
local function NS(...) local k = {} for _, p in {...} do table.insert(k, NumberSequenceKeypoint.new(p[1], p[2], p[3] or 0)) end return NumberSequence.new(k) end
local function CS(...) local k = {} for _, p in {...} do table.insert(k, ColorSequenceKeypoint.new(p[1], p[2])) end return ColorSequence.new(k) end
-- e.g. emitter.Size = NS({0, 0}, {0.1, 4}, {1, 0})
```

---

### 1. Fire (anime flame burst / fire fist)
| Layer | Texture | Key settings |
|---|---|---|
| Core flash | Soft round glow | Emit 1, `Lifetime 0.12`, `Size 0:0, 0.2:6, 1:8`, `Transparency 0:0, 1:1`, `Color` white-yellow (255,250,220), `LightEmission 1`, `Brightness 3`, `ZOffset 1` |
| Flame tongues | 4×4 flame flipbook, hard-edged | Emit 12–20, `Lifetime 0.3–0.5`, `Speed 10–25`, `SpreadAngle (40,40)`, `Drag 4`, `Acceleration (0,15,0)`, `Size 0:1, 0.3:3, 1:0.5`, `Color 0:(255,240,180) 0.3:(255,140,30) 1:(180,30,10)`, `FlipbookMode OneShot`, `FlipbookBlendFrames false`, `LightEmission 1`, `Rotation (0,360)` |
| Embers | Small spark | Emit 15, `Lifetime 0.6–1.2`, `Speed 15–40`, `SpreadAngle (180,180)`, `Drag 3`, `Acceleration (0,8,0)`, `Size 0:0.2, 1:0`, `Color` (255,170,60), `LightEmission 1` |
| Smoke residue | 4×4 smoke puff flipbook | Emit 6, `Lifetime 0.8–1.2`, `Speed 3–6`, `Size 0:2, 1:5`, `Transparency 0:0.6, 0.3:0.4, 1:1`, `Color` (60,50,50), `LightEmission 0`, `LightInfluence 0.5`, `ZOffset -0.5` |
| Light | `PointLight` | `Color (255,150,60)`, `Range 12`, `Brightness` tween 4 → 0 over 0.3 s |

Shape rule: fire is sharp, tapering tongues [7]. A continuous flame aura uses the same flame layer at `Rate 20–30`, `LockedToPart true`.

### 2. Lightning (strike / electric dash)
| Layer | Tool | Key settings |
|---|---|---|
| Bolt core | Beams between 6–10 jittered attachments (see [[Beams and Trails for Anime VFX]]) | `Width0/1 0.3–0.5`, `Color` white, `LightEmission 1`, `Brightness 4`, reshape every ~0.05 s [1], lifetime 0.15–0.3 s with flicker |
| Bolt glow | Second beam on the same attachments | `Width 1–1.5`, `Color (120,200,255)`, `Transparency 0.4`, `ZOffset -0.1` |
| Impact sparks | Square or streak texture | Emit 20, `Lifetime 0.15–0.3`, `Speed 40–90`, `SpreadAngle (180,180)`, `Drag 8`, `Orientation VelocityParallel`, `Squash` negative (≈ −2), `Size 0:0.4, 1:0`, `LightEmission 1` (VelocityParallel + Squash streak sparks [1][8]) |
| Ground arcs | Short beams along the floor | 3–5 arcs, `TextureSpeed 4`, random re-target every 0.08 s |
| Flash | ColorCorrection on client | `Brightness +0.3`, 2 frames ([[Impact Frames and Screen Effects]]) |

Community lightning module: "Lightning Beams" v1.1 (client-only, Perlin noise, sparks and explosion sub-modules) [9].

### 3. Wind (slash / gust / tornado)
| Layer | Tool | Key settings |
|---|---|---|
| Wind crescents | Slash mesh or curved beam with a dry-brush stroke texture | White, `Transparency 0.3 → 1`, scale 0.6 → 1.2 over 0.25 s, Circ Out ([[Mesh-Based VFX]]) |
| Streak lines | Thin streak texture | Emit 10, `Lifetime 0.2–0.35`, `Speed 50–80`, `Orientation VelocityParallel`, `Squash` −3, `Size 0:0.3, 1:0.1`, `Transparency 0:0.3, 1:1`, `Color (230,250,255)`, `LightEmission 0.3` |
| Swirl (tornado) | Twisted cone mesh + scrolling texture, or curved beams around the axis | Spin via CFrame tween 720°/s, `Transparency 0.5` |
| Dust pickup | Dust puff | Disc shape at ground, `ShapePartial 1` (rim only), Emit 15, `Speed 10–20`, `ShapeInOut Outward`, normal blend |

Wind is mostly **white at low opacity**. Readability comes from motion and streak direction, not color. A community scrolling-texture rule: a still beam with `TextureSpeed` reads as moving wind with nothing to update per frame [1].

### 4. Water (whip / wave / splash)
| Layer | Tool | Key settings |
|---|---|---|
| Body | Tube or wave mesh, textured with flowing stripes; or beams with `TextureSpeed 2–3` | `Color (60,150,255)` body + white highlight stripe beam on top (`ZOffset 0.1`), body `LightEmission 0.2` |
| Splash droplets | Droplet texture | Emit 25, `Lifetime 0.5–0.9`, `Speed 20–40`, `SpreadAngle (60,60)`, `Acceleration (0,-60,0)`, `Orientation VelocityParallel`, `Squash` −1, `Size 0:0.4, 1:0.2`, `Color (200,235,255)`, `LightEmission 0` |
| Foam ring | Ring mesh (white) or Disc emitter rim-only | Expand 2 → 12 studs over 0.4 s, `Transparency 0 → 1` |
| Mist | Soft puff | Emit 6, `Lifetime 1`, `Transparency 0:0.7, 1:1`, `Size 0:3, 1:6`, normal blend, `LightInfluence 1` |

Effects-animation theory for liquids covers density, force, gravity, viscosity and after-splash behavior [10]: droplets arc and fall (use `Acceleration`), and splashes have a secondary, smaller after-splash (add a second Emit 0.15 s later at 40% count).

### 5. Dark energy / cursed energy (black body, colored rim)
| Layer | Tool | Key settings |
|---|---|---|
| Black body | Hard-edged flame or wisp flipbook | Rate 25 (aura) or Emit 15, `Lifetime 0.4–0.7`, `Speed 2–6`, `Acceleration (0,6,0)`, `Size 0:1, 0.5:2.5, 1:0`, `Color (15,0,25)`, **`LightEmission 0`**, `LightInfluence 0`, `FlipbookBlendFrames false` |
| Colored rim | Same texture, slightly larger | `Color 0:(160,60,255) 1:(80,0,160)`, `LightEmission 1`, `Size` ×1.2 of body, `ZOffset -0.2` (behind the body so it peeks out as a rim) |
| Crackle | Short electric arcs | Red/purple beams, 2–3 at a time, reshape every 0.05 s |
| Hit | Black-and-white impact frame + black lightning | Mono ColorCorrection 2–3 frames ([[Impact Frames and Screen Effects]]) |

Why `LightEmission 0`: with additive blending, darker colors become more transparent, so black additive particles vanish [3]. "Black Flash"-style hits are widely described as black lightning, with red or purple tints in some depictions [11].

### 6. Explosion (anime blast)
Timing: flash (0.05 s) → fireball (0.3 s) → shockwave ring (0.3 s, ends first among secondaries) → smoke column (1–1.5 s) → debris (physics-like arcs).

| Layer | Key settings |
|---|---|
| White flash sphere | Neon part, size 1 → 12 in 0.08 s, Transparency 0 → 1 in 0.12 s |
| Fireball | 4×4 explosion flipbook, Emit 8, `Lifetime 0.35–0.5`, `FlipbookMode OneShot`, `Size 0:4, 1:10`, fire color ramp, `LightEmission 1` |
| Shockwave ring | Ring mesh, (2,0.2,2) → (40,0.2,40) in 0.3 s Circ Out, fade Quad In |
| Smoke | Smoke flipbook, Emit 10, `Lifetime 1–1.5`, `Speed 5–15`, `Drag 2`, `Acceleration (0,4,0)`, `Size 0:4, 1:12`, `Transparency 0:0.3, 1:1`, `Color (50,45,45)`, normal blend, `ZOffset -1` |
| Debris | Rock-chip flipbook with `FlipbookStartRandom true`, `FlipbookFramerate 0` (static random frame [5]), Emit 12, `Speed 30–60`, `Acceleration (0,-80,0)`, `RotSpeed (-360,360)`, normal blend |
| Camera | Shake (magnitude by distance) + FOV punch +6 |

### 7. Ground cracks and craters (slam / landing)
1. **Raycast down** from the impact point to get the surface position, normal, `Material` and `Color`.
2. **Crater rocks:** spawn 8–14 low-poly rock meshes in a ring (radius 4–10 studs), angled outward 20–40°, colored to match the surface. Rise in 0.08 s (Back Out), hold 1.5–3 s, then sink and fade over 0.5 s. Community modules do this with raycast placement and PartCache/ObjectCache pooling [4].
3. **Cracks decal:** a flat MeshPart or `Decal` on a thin part aligned to the surface normal, with a crack texture (white alpha, tinted dark), scaling from 0.5 → 1 in 0.1 s. Fade after 2 s.
4. **Flying debris:** 4–8 small rock parts with initial velocity (unanchored, `CanCollide false`, destroyed after 1.5 s), or the debris particle layer above.
5. **Dust ring:** Disc-shaped emitter at ground level (`Shape Disc`, `ShapeStyle Surface`, `ShapePartial 1` for rim-only emission [5]), Emit 25, `Speed 15–30`, `ShapeInOut Outward`, `Drag 3`, `Size 0:2, 1:5`, `Transparency 0:0.4, 1:1`, color sampled from the surface, normal blend.

The community modules are years old. Check they still use current APIs before adopting them. No dedicated open-source "ground crack" module was found [4].

### 8. Dust (footsteps, dash kick, landing)
| Use | Key settings |
|---|---|
| Dash kick | Attachment at the feet, Emit 6–10 on dash start, `EmissionDirection` back, `Speed 8–15`, `SpreadAngle (30,30)`, `Drag 4`, `Lifetime 0.4–0.7`, `Size 0:1, 1:3`, `Transparency 0:0.5, 1:1`, `Color` sampled from the floor material, normal blend, `LightInfluence 1` |
| Landing ring | Disc rim emitter (see cracks above) at 40% count |
| Running puffs | Emit 2 on each footstep marker |

`LightInfluence 1` here so dust darkens in shadowed areas of the map ([[Lighting for Anime Maps]]).

## Numbers & Settings
| Element | Blend | Lifetime (impact layers) | Main colors |
|---|---|---|---|
| Fire | Additive + normal smoke | 0.3–0.5 s | (255,240,180) → (255,140,30) → (180,30,10) |
| Lightning | Additive | 0.15–0.3 s | white + (120,200,255) |
| Wind | Low additive / normal | 0.2–0.35 s | white, (230,250,255) |
| Water | Mostly normal | 0.5–0.9 s | (60,150,255), white highlights |
| Cursed/dark | Normal body + additive rim | 0.4–0.7 s | (15,0,25) + (160,60,255) |
| Explosion | Mixed | 0.05 s flash … 1.5 s smoke | Fire ramp + grey smoke |
| Dust | Normal, lit | 0.4–1 s | Sampled from the floor |

## Checklist
- [ ] Each element has a template in `ReplicatedStorage/VFX/Assets/<Element>` with 3–5 layers.
- [ ] Additive vs. normal blend is chosen per layer, as in the tables.
- [ ] Charge-up variants exist (Inward emission) for each element.
- [ ] Ground effects sample floor material and color via raycast.
- [ ] Each recipe has been checked against the [[VFX Performance Budget]] tier.
- [ ] After testing, record the final values here and set `status: verified-in-studio`.

## Common Mistakes
- **Additive black energy.** It turns invisible [3].
- **Smoke brighter than the fire.** Residue layers must be low contrast and low opacity [2].
- **Dust in a fixed brown.** It looks pasted on snow or concrete maps. Sample the surface.
- **Same texture, same timing for every element.** Wind needs streak motion, water needs gravity arcs, and fire needs upward acceleration.
- **Shockwave ring outliving the explosion core.** Secondary layers should end first [1].

## Related
- [[Anime VFX Fundamentals]]
- [[ParticleEmitter Deep Dive]]
- [[Beams and Trails for Anime VFX]]
- [[Mesh-Based VFX]]
- [[Impact Frames and Screen Effects]]
- [[Creating VFX Textures]]
- [[VFX Performance Budget]]
- [[Lighting for Anime Maps]]
- [[Anime Combat Animation Timing]]

## Sources
1. EasyVFX README and `docs/sharp-vfx.md` / `docs/impact.md` (layer structure, bolt reshape ~0.05 s, VelocityParallel + Squash sparks, TextureSpeed wind, secondary layers end first). https://github.com/VuxSussy/EasyVFX
2. 80.lv, "VFX Staples: Shape, Color, and Motion" (dissipation low contrast/opacity). https://80.lv/articles/vfx-staples-shape-color-and-motion/
3. Roblox Creator Docs, ParticleEmitter.Color / LightEmission (darker colors look more transparent when LightEmission > 0). https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
4. DevForum crater/rock modules: "Battlegrounds crater module" https://devforum.roblox.com/t/battlegrounds-crater-module/3370194 ; "Rock Module V.1.0 - Craters, Explosions, and more!" https://devforum.roblox.com/t/rock-module-v10-craters-explosions-and-more-effects/3041562 ; "'Punch' Rock Module inspired by TSB" https://devforum.roblox.com/t/punch-rock-module-inspired-by-tsb/3171422 ; "Rocks Module - Useful for Anime Games Skill Effects" https://devforum.roblox.com/t/rocks-module-useful-for-anime-games-skill-effects/1687374
5. Roblox Creator Docs, "Particle emitters" guide (ShapePartial disc rim, FlipbookStartRandom + framerate 0, shapes). https://create.roblox.com/docs/effects/particle-emitters
6. Roblox Creator Docs, Beam reference. https://create.roblox.com/docs/reference/engine/classes/Beam
7. Yelzkizi, "10 Mind-Blowing Anime FX Tips" (fire = sharp tapering tongues; smoke = overlapping circles). https://yelzkizi.org/anime-fx-blender-after-effects-tutorial/
8. Roblox Creator Docs, "Particle emitters" → Simulate rain (VelocityParallel → negative Squash). https://create.roblox.com/docs/effects/particle-emitters#simulate-rain
9. DevForum, "[Effect] v1.1 Lightning Beams". https://devforum.roblox.com/t/effect-v11-lightning-beams-seamless-smooth-and-procedurally-animated-with-beam-like-properties/843534
10. Parka Blogs, review of Joseph Gilland's *Elemental Magic* (liquids: density, force, gravity, viscosity, after-splash). https://www.parkablogs.com/index.php/content/book-review-elemental-magic-art-of-special-effects-animation
11. Search summary on Black Flash depiction (black lightning; red/purple tints; low-quality sources). https://dexerto.com/anime/jujutsu-kaisen-gege-akutami-black-flash-inspired-video-game-2823239
