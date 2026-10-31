---
tags: [vfx, particles, particleemitter, flipbook, roblox-api]
updated: 2026-10-31
sources: 9
status: draft
---
# ParticleEmitter Deep Dive

## TL;DR
- `ParticleEmitter` emits 2D camera-facing (by default) quads. Parent it to an **Attachment** to emit from a point, or to a **BasePart** to emit from the part's volume or shape. [1]
- Hard limits from the official docs: **Rate up to 400/s per emitter (100/s on mobile)**, **Lifetime capped at 20 s**, **FlipbookFramerate max 30 fps**. `Emit(n)` defaults to **16** particles. [1][2]
- Anime essentials: `LightEmission = 1` (additive) for energy, `LightInfluence = 0` (self-lit), `ZOffset` for layering, `Squash` + `VelocityParallel` for streak sparks, `Rate = 0` + `Emit()` for bursts. [1][2]
- Flipbooks: `Grid2x2` / `Grid4x4` / `Grid8x8` / `Custom` (`FlipbookSizeX`/`Y`, 1–64 each). The texture size must be an exact multiple of the layout. **OneShot** mode ignores `FlipbookFramerate` and spreads frames over `Lifetime`. [1][3]
- `LightInfluence` defaults to **1 when inserted in Studio** and **0 when created with `Instance.new()`**. Code-made and Studio-made emitters look different unless you set it explicitly. [1]

## Why it matters for anime battlegrounds
Particles carry most of the genre: hit sparks, impact stars, dust kicks, charge-up motes, aura, embers, smoke. They're cheaper and easier to author than tweened meshes, and they replicate their *state* (not individual particles) so you can drive them from a single `Emit()` call on each client. A DevForum commenter argues scripters should learn particle VFX because it's more efficient than tweened or animated meshes [4]. In practice, top games mix both (see [[Mesh-Based VFX]]).

## How to do it

### Step 1 — Parent and orient
- **Attachment parent** = point source. Rotate the attachment (`Attachment.Orientation`) instead of using `EmissionDirection` [1].
- **Part parent** = particles spawn in the part's bounding box or `Shape` [1]. Use an invisible, anchored, `CanCollide = false`, `CanQuery = false` part.
- **Sphere and Cylinder shapes don't display correctly when parented to an Attachment.** Use a BasePart for those [5].

### Step 2 — Set the property groups
Every property listed in the current API reference (retrieved 2026-10-31), grouped the way you'll use them [1]:

**Appearance**
| Property | Type | What it does | Anime use |
|---|---|---|---|
| `Texture` / `TextureContent` | ContentId / Content | Image on each particle. PNG with transparent background works best [5] | White or greyscale art, tinted by `Color` |
| `Color` | ColorSequence | Tint over each particle's lifetime (lerped by age / lifetime) | White → main hue → dark accent |
| `Transparency` | NumberSequence (0 opaque, 1 invisible) | Fade over lifetime. Keypoint envelopes randomize per particle | Always fade in and out to avoid popping [5] |
| `Size` | NumberSequence (studs) | World size of the square quad over lifetime | Impact pop: 0 → max in the first 10%, then shrink |
| `Squash` | NumberSequence | >0 = thinner and taller, <0 = wider and shorter, over lifetime | Streak sparks, speed lines, rain [5] |
| `LightEmission` | float 0–1 | 0 = normal blend, 1 = additive. Doesn't light the world | 1 for energy, 0 for smoke/dark |
| `LightInfluence` | float 0–1 | How much world light tints particles. Studio default 1, `Instance.new` default 0 | 0 for glowing VFX |
| `Brightness` | float | Scales emitted light when `LightInfluence` is 0 | 1–5 with Bloom for hot cores |
| `Orientation` | enum | `FacingCamera` (default), `FacingCameraWorldUp`, `VelocityParallel`, `VelocityPerpendicular` | `VelocityParallel` for sparks, `VelocityPerpendicular` for flat ground rings |
| `ZOffset` | float (studs, fractional) | Moves render position toward (+) or away (−) from camera without changing screen size | Core in front of rim, sparks in front of the character |
| `LocalTransparencyModifier` | float | Client-only extra transparency, doesn't replicate | Hide own aura in first person |

**Emission**
| Property | Type | What it does | Anime use |
|---|---|---|---|
| `Enabled` | bool | Stops new spawns. Existing particles live out their lifetime | Toggle auras |
| `Rate` | float (per s) | Continuous emission. **Max 400/s per emitter, 100/s on mobile** [5] | 0 for bursts, 10–60 for auras |
| `Lifetime` | NumberRange (s) | Random life per particle. **Capped at 20 s** [5]. 0 = no emission | 0.15–0.6 s for hits |
| `Speed` | NumberRange (studs/s) | Initial velocity along `EmissionDirection`. Negative = reverse | 30–120 for sparks |
| `SpreadAngle` | Vector2 (deg) | Random cone. One axis 360 = circle, both 360 = sphere | (180,180) radial burst, (0,360) flat ring |
| `EmissionDirection` | NormalId | Face to emit from (part parent) | Top for dust kicks |
| `Shape` | enum | Box, Sphere, Cylinder, Disc | Disc for ground shockwave dust |
| `ShapeStyle` | enum | Volume or Surface | Surface for rings |
| `ShapeInOut` | enum | Outward, Inward, InAndOut | Inward for charge-up |
| `ShapePartial` | float | Cylinder: top radius ratio (0 = cone). Disc: inner radius (1 = rim only). Sphere: hemisphere angle (0.5 = dome) | Disc 1.0 = perfect ring of dust |
| `Rotation` | NumberRange (deg) | Initial rotation, clockwise positive | (0, 360) to hide repetition |
| `RotSpeed` | NumberRange (deg/s) | Spin. Very high values can alias and look still | ±90–360 for debris |
| `VelocitySpread` | float (deg) | Random offset from emitter direction | |

**Motion**
| Property | Type | What it does | Anime use |
|---|---|---|---|
| `Acceleration` | Vector3 (studs/s², world axes) | Constant acceleration on all particles | (0, −50, 0) gravity for rocks and sparks |
| `Drag` | float | Seconds to lose half the speed (exponential). Negative = speeds up | 4–10 for snappy "burst then stop" sparks |
| `LockedToPart` | bool | Particles move rigidly with the parent | Auras, charge orbs |
| `VelocityInheritance` | float 0–1 | Fraction of parent part velocity added at spawn | 0.3–1 for dash trails "shedding" |
| `TimeScale` | float 0–1 | 1 = normal, 0.5 = half speed, 0 = frozen | Hit-stop freeze |
| `WindAffectsDrag` | bool | Follows `Workspace.GlobalWind` if `Drag > 0` | Ambient leaves only |

**Flipbook** — see Step 4.

**Methods:** `Emit(particleCount: int = 16)` instantly emits; `Clear()` removes all live particles [1].

### Step 3 — Layer with ZOffset
`ZOffset` is in studs and accepts fractions. It isn't an integer ZIndex [1]. A typical hit stack:

| Layer | ZOffset | Blend |
|---|---|---|
| Smoke / dust (back) | −1 to −0.5 | Normal |
| Colored rim / outer glow | 0 | Additive |
| White core flash | 0.5 | Additive |
| Sparks / impact star (front) | 1–2 | Additive |

A DevForum reply suggests `ZOffset ≈ 2` keeps particles on top of a character [6]. The same thread reports that a ParticleEmitter couldn't render in front of a `Highlight` at the time [6]. Sufficiently negative values push particles inside or behind the parent part [1].

### Step 4 — Flipbooks
Official rules [1][5]:
- `FlipbookLayout`: `None`, `Grid2x2` (4 frames), `Grid4x4` (16), `Grid8x8` (64), `Custom` (`FlipbookSizeX` columns × `FlipbookSizeY` rows).
- `FlipbookIncompatible` is the error string shown when the texture size isn't an exact multiple of the layout.
- `FlipbookMode`:
  - `Loop`: repeats.
  - `OneShot`: plays once across the particle's `Lifetime`. **`FlipbookFramerate` doesn't apply.** Frame rate = frames ÷ lifetime. Best for explosions and smoke puffs.
  - `PingPong`: forward then backward.
  - `Random`: random frames with crossfade.
- `FlipbookFramerate`: NumberRange, **max 30 fps**.
- `FlipbookStartRandom`: random start frame. With framerate 0, each particle shows one random static frame (great for rock or debris variety from one sheet).
- `FlipbookBlendFrames`: linear crossfade between frames vs. a hard swap. **Turn it off for crisp anime "on twos" stepped animation.** Turn it on for smooth smoke.
- **Include transparent spacing between frames.** Mip filtering may need more [5].
- **Memory warning:** flipbooks cost memory. Low-memory clients (often older phones) **automatically deactivate flipbooks**. Reuse textures and keep resolutions small [5].
- Custom layouts: `FlipbookSizeX` and `FlipbookSizeY` accept integers **1–64**, and are ignored unless the layout is `Custom` [3].
- The original release thread listed supported flipbook texture sizes as powers of two from **8×8 up to 1024×1024** [7].

Frame-size math on a 1024² sheet: 2×2 → 512 px frames, 4×4 → 256 px, 8×8 → 128 px [7].

> [!warning] Unverified
> Whether non-power-of-two or non-square textures now work with `Custom` layouts in live games (the custom-layout post was a Client Beta announcement) is not confirmed. Test before relying on it [3].

### Step 5 — Bursts vs. continuous
- **Burst (hits, impacts):** `Enabled = false` or `Rate = 0`, then `emitter:Emit(n)`. Script patterns are in [[Scripting and Emitting VFX]].
- **Continuous (auras, fire):** `Rate` > 0, toggle `Enabled`.
- DevForum users report `Emit()` ignores the graphics-quality rate throttle, while `Rate` emission is throttled at low quality [8]. A recent bug report says quality no longer changes `Rate` after an update [8]. Test current behavior yourself.

> [!warning] Unverified
> EasyVFX's author reports that at the lowest graphics quality Roblox drew no `Rate` emission at all while `Emit` bursts still drew (single observation, 2026-10-26) [9]. Design must-see loops as repeated bursts if this matters.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Max Rate | 400/s per emitter (100/s mobile) | Official [5] |
| Max Lifetime | 20 s (internally capped) | Official [5] |
| Max FlipbookFramerate | 30 fps | Official [1] |
| `Emit()` default | 16 | Official [1] |
| FlipbookSizeX/Y | 1–64 | Custom layout [3] |
| Hit spark lifetime | 0.15–0.35 s | Short = snappy (starting point) |
| Hit spark speed / drag | 40–100 / 6–10 | Burst then stop (starting point) |
| Streak spark | `Orientation = VelocityParallel`, `Squash` negative (e.g. −2) | Docs: with VelocityParallel, use negative squash to stretch along travel [5] |
| Additive glow | `LightEmission 1`, `LightInfluence 0`, `Brightness 1–3` | [1] |

> [!warning] Unverified
> The "starting point" values are untested defaults for anime hit sparks, not taken from any shipped game. Tune in Studio.

## Checklist
- [ ] `LightInfluence` set explicitly on every emitter (don't trust defaults).
- [ ] Every Transparency sequence starts and ends near 1 (no popping).
- [ ] Burst emitters have `Rate = 0` / `Enabled = false` and are fired with `Emit()`.
- [ ] ZOffset stack defined: smoke < rim < core < sparks.
- [ ] Flipbook sheets have frame padding and power-of-two sizes ≤ 1024.
- [ ] `FlipbookBlendFrames` off for stepped anime look, on for smooth smoke.
- [ ] Sphere/Cylinder shapes are only on part-parented emitters.
- [ ] Checked at Editor Quality Level lowest and highest [5].

## Common Mistakes
- **Using Rate for one-off hits.** You get inconsistent counts, a frame-rate-dependent look, and throttling on low settings.
- **Giant soft particles.** They fill the screen with overdraw and look blurry. Make them smaller and sharper (see [[VFX Performance Budget]]).
- **Forgetting OneShot ignores FlipbookFramerate.** People tweak framerate and nothing changes.
- **Black-background textures without additive blending.** If the texture has no alpha, use `LightEmission = 1` to hide dark regions [5].
- **Code-created emitters looking "too bright".** `LightInfluence` defaults to 0 for `Instance.new` [1].
- **Extremely high RotSpeed.** Spin aliases to the frame rate and appears frozen [1].

## Related
- [[Anime VFX Fundamentals]]
- [[Creating VFX Textures]]
- [[Scripting and Emitting VFX]]
- [[VFX Performance Budget]]
- [[Element VFX Recipes]]
- [[Lighting for Anime Maps]]

## Sources
1. Roblox Creator Docs, ParticleEmitter class reference (all properties, LightInfluence defaults, Emit default 16, FlipbookFramerate max 30, ZOffset, OneShot). https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter — read from source https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/ParticleEmitter.yaml on 2026-10-31
2. Roblox Creator Docs, "Create basic visual effects" (flare: LightEmission 1, ZOffset 1, Rate 0.45; dust: ZOffset −5). https://create.roblox.com/docs/tutorials/curriculums/core/building/create-basic-visual-effects
3. DevForum, "[Client Beta] Optimize your particle animations with custom flipbook layouts" (FlipbookSizeX/Y 1–64; ignored unless Custom). https://devforum.roblox.com/t/client-beta-optimize-your-particle-animations-with-custom-flipbook-layouts/4005128 (via search summary)
4. DevForum, "how do they do these kinds of VFX? ... moon animator" (particles more efficient than tweened meshes, opinion). https://devforum.roblox.com/t/question-how-do-they-do-these-kinds-of-vfx-is-it-by-coding-or-animating-with-moon-animator-or-smthng/1588766
5. Roblox Creator Docs, "Particle emitters" guide (Rate 400/100 mobile, Lifetime 20 s cap, flipbook spacing and memory, Sphere/Cylinder + Attachment warning, rain Squash tip). https://create.roblox.com/docs/effects/particle-emitters — source https://github.com/Roblox/creator-docs/blob/main/content/en-us/effects/particle-emitters.md
6. DevForum, "How do I get a particle effect in front of a highlight effect?" https://devforum.roblox.com/t/how-do-i-get-a-particle-effect-in-front-of-a-highlight-effect/2707313
7. DevForum, "Particles' Flipbook Release" (supported sizes 8–1024 px, frame size math). https://devforum.roblox.com/t/particles%E2%80%99-flipbook-release/2029388
8. DevForum, "Particle emitter limit on low graphics is impacting my game" https://devforum.roblox.com/t/particle-emitter-limit-on-low-graphics-is-impacting-my-game/2159584 and "Particle Emitters no longer change Rate with graphics quality" https://devforum.roblox.com/t/particle-emitters-no-longer-change-rate-with-graphics-quality/4834736
9. EasyVFX `docs/sharp-vfx.md`. https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
