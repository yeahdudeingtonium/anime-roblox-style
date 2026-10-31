---
tags: [vfx, fundamentals, anime, shape-language, timing, color, readability]
updated: 2026-10-31
sources: 12
status: draft
---
# Anime VFX Fundamentals

## TL;DR
- Every effect has three phases: **anticipation** (build-up), **climax/impact** (most elements, highest contrast, highest saturation) and **dissipation** (short, low contrast, low opacity). Dissipation should end fast so it doesn't steal focus. [1]
- Anime effects use **hard-edged, graphic shapes** (tapering flame tongues, jagged impact stars, crisp rings) rather than soft, realistic volumes. Soft edges are kept for motion blending only. [2][3]
- **Value beats hue.** A white or near-white core with a saturated colored rim reads instantly. Additive blending (`LightEmission = 1`) plus Bloom gives the anime glow on Roblox. [4][5]
- Timing is **fast in, long glide out**: the impact frame or flash holds for 2–3 frames, then shapes break up and fade. Anime deliberately breaks physics for rhythm (squash before, stretch at release, hang for emphasis). [3][6]
- Readability first: in a 10–20 player battlegrounds server, the effect must say *who hit whom and how hard* in under ~0.3 s, and secondary layers must end before the main hit. [3][7]

## Why it matters for anime battlegrounds
The Strongest Battlegrounds, Jujutsu Shenanigans, Heroes Battlegrounds and Type Soul all sell the same fantasy: you *are* a shonen fighter. Players judge a move by its effects as much as its damage numbers, and these games are often recorded as clips for TikTok and YouTube Shorts. In the genre, VFX also carries gameplay information: the start-up (telegraph), the hit confirm, and the size of the area of effect. A gorgeous effect that hides the telegraph or the hitbox is a design bug, not just an art problem.

This note covers the theory. The property-level how-to lives in [[ParticleEmitter Deep Dive]], [[Beams and Trails for Anime VFX]], [[Mesh-Based VFX]], [[Impact Frames and Screen Effects]] and [[Element VFX Recipes]]. Animation timing that VFX must sync to is in [[Anime Combat Animation Timing]].

## How to do it

### Step 1 — Structure every effect as Anticipation → Impact → Dissipation
The 80.lv "VFX Staples" talk (made for a mobile PVP game) describes the three stages [1]:

| Phase | What happens | Visual rules | Typical battlegrounds duration (starting point) |
|---|---|---|---|
| **Anticipation / fade-in** | Energy gathers, the telegraph | Inward motion (particles converging, `ShapeInOut = Inward`), rising brightness, small and tight shapes. Length set by game design (the move's start-up) [1] | 0.15–0.6 s (matches the move's wind-up animation) |
| **Climax / impact** | The hit or release | **Maximum number of elements, biggest contrast, high saturation** [1]. White flash, impact star, shockwave ring, camera shake, impact frame | 0.03–0.1 s for the flash itself (2–6 frames at 60 fps) |
| **Dissipation / fade-out** | Smoke, embers, decaying rings | **Short, low contrast, low opacity** so it does not distract [1]. Shapes break up (erode) instead of only fading | 0.2–0.8 s |

> [!warning] Unverified
> The duration column is a starting point from genre observation, not a measured value from TSB or JJS. Measure your reference clips frame by frame (see [[Anime Combat Animation Timing]]) before you lock numbers.

The same talk notes that climax and dissipation can be animated together, but dissipation should live on its **own layer** so a move's duration can change without breaking the effect [1]. On Roblox, that means a separate ParticleEmitter (or a separate mesh) for the lingering smoke, emitted from the same attachment.

### Step 2 — Use anime shape language
- **Fire** = sharp, tapering tongues. **Smoke** = overlapping billowing circles. [8]
- **Impacts** = jagged star shapes that burst outward on flat planes at the moment of the hit, like shonen manga impact stars. [2]
- **Hard shapes read as strong, soft blobs read as weak.** Spikes and crisp rims read instantly. [3]
- Japanese effects animation (sakuga) is the root of this look. Yoshinori Kanada's work is described as using asymmetrical, subliminal shapes, and his style is tied to light flares and impact frames [9]. A whole generation of "Kanada followers" copied his effects scenes in the late 1970s [10]. Takashi Hashimoto is described as one of Japan's greatest effects animators, whose explosions are each unique rather than repeated [9].
- Gilland's *Elemental Magic* (Vol. I and II) is the standard book on hand-drawn effects: fire, smoke, explosions, liquids, magic. Its water chapters cover density, force, gravity, viscosity and after-splash behavior. Vol. II covers timing and frame rates [11].

**Practical rule for Roblox:** get the silhouette from **geometry** (Beams, Neon parts, meshes), because geometry rasterizes at screen resolution and stays crisp. Use textures for interior detail and soft glow. A 256 px particle stretched to half the screen goes blocky or blurry [5].

| Shape | Reads as | Roblox tool |
|---|---|---|
| Thin crescent, sharp at both ends | Blade, slash | Curved Beam, slash MeshPart, Trail |
| Radial spikes / star | Impact, crit | Particle with star texture, `Size` pop 0 → big in 0.05 s |
| Expanding thin ring | Shockwave, force | Ring mesh or Beam ring, tween Size up and Transparency to 1 |
| Converging lines | Charge, anticipation | Particles with `ShapeInOut = Inward`, or Beams scaling inward |
| Tapered zig-zag | Lightning | Beams between jittered attachments |
| Round puffs | Smoke, dust | Flipbook smoke particle, `Drag` high |

### Step 3 — Color: value structure first, hue second
- Use a **white (or near-white) core + colored rim**, not one flat color. The bright core reads as "hot" and keeps the edge defined [5].
- **Color over life: white → main color → secondary color**, fast (about 0.35 s for a slash in one community tool) [4].
- Use additive blending for energy: `LightEmission = 1`, `LightInfluence = 0` gives self-lit glow that ignores map lighting [5][12]. Use **normal blending** (`LightEmission = 0`) for smoke, dust, rocks and dark energy, because additive blending can't darken a scene.
- With `LightEmission > 0`, darker particle colors look more transparent [12]. That's why black "cursed energy" needs `LightEmission = 0`.
- Bloom in Lighting makes light colors glow ([[Lighting for Anime Maps]]). Keep `BloomEffect.Threshold` high enough that only VFX bloom, not the whole map.
- **Per-character palette = identity.** Assign each character or move set one main hue and one accent so players can tell whose attack is whose in a crowded fight. Avoid giving two characters the same main hue.

| Element | Core | Main | Accent / falloff | Blend |
|---|---|---|---|---|
| Fire | (255, 255, 220) | (255, 140, 30) | (200, 40, 10) → smoke grey | Additive core, normal smoke |
| Lightning | (255, 255, 255) | (120, 200, 255) | (60, 80, 255) | Additive |
| Wind | (255, 255, 255) at low opacity | (200, 240, 255) | none | Normal or low additive |
| Cursed / dark energy | (20, 0, 30) body | (120, 0, 200) rim | (255, 60, 200) sparks | Normal body + additive rim |
| Holy / light | (255, 255, 255) | (255, 230, 150) | (255, 200, 80) | Additive |

> [!warning] Unverified
> The palette table is a design starting point, not taken from any specific game. "Black Flash"-style dark hits are commonly described as black lightning, sometimes with red or purple tints, but low-quality sources disagree on the exact palette [13].

### Step 4 — Timing and spacing like an animator
- **Hold the hard white flash for 2–3 frames.** A white flash, then dark, then the color fading gives the hit depth [3].
- **Hit-stop:** a short freeze on a heavy hit, cited at about 50–100 ms in game-feel writing [3]. On Roblox you can freeze particles with `ParticleEmitter.TimeScale = 0` and restore it to 1 (`TimeScale` runs from 0 to 1) [12].
- **Fast in, long glide:** circular or exponential easing (fastest start, long slow-down) for slashes and shockwaves [3]. In TweenService: `Enum.EasingStyle.Circ` or `Exponential`, `EasingDirection.Out`.
- **Anticipation carries weight:** much of a hit's weight comes from the moment *before* contact [3]. Anime squashes in before a move, stretches explosively and hangs mid-air for emphasis [6].
- **Camera kick, not wobble:** full strength on the first frame, decaying fast, says "impact". Long, even noise says "earthquake" [3]. See [[Impact Frames and Screen Effects]].
- **Shorten everything.** A practitioner tip for making combat VFX read as anime: roughly halve particle lifespans and add a two-frame high-contrast screen flash [2].

### Step 5 — Readability rules for multiplayer
1. **Secondary layers end first.** A shockwave brighter or longer than the strike steals focus [3].
2. **Don't cover the target.** Use `ZOffset` and size so the hit spark sits in front of the victim but doesn't hide their animation.
3. **Telegraph vs. payoff contrast.** Anticipation is dimmer and tighter. The payoff is the brightest and biggest moment.
4. **Silhouette test:** screenshot the climax frame, desaturate it (or set `ColorCorrectionEffect.Saturation = -1`). If you can't read the action in greyscale, fix values before hues.
5. **Scale to importance.** M1 (basic attack) hits: 1–2 layers. Skills: 3–5 layers. Ultimates: full layered effect + impact frame + camera. One community guide says pro artists layer 3–5 emitters per effect (core glow, outer particles, sparks, smoke) [7].
6. **Performance is readability.** A frame drop during the climax kills the hit. See [[VFX Performance Budget]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Hit flash hold | 2–3 frames (~0.033–0.05 s) | White flash → dark → color gives depth [3] |
| Hit-stop | ~0.05–0.1 s | Shorter goes unnoticed, longer reads as lag [3] |
| Energy blend | `LightEmission = 1`, `LightInfluence = 0` | Additive, self-lit [5][12] |
| Smoke/dust/dark blend | `LightEmission = 0`, `LightInfluence` 0.3–1 | Lets particles darken and react to map light [12] |
| Layers per M1 hit | 1–2 | Spam-safe, readable |
| Layers per skill | 3–5 | Core, outer, sparks, smoke [7] |
| Dissipation opacity | start ≥ 0.5 transparency | Low contrast, low opacity [1] |
| Easing for expanding shapes | `Circ` / `Exponential` `Out` | Fast start, long glide [3] |

## Checklist
- [ ] Every effect is split into anticipation / impact / dissipation layers (separate emitters or meshes).
- [ ] The climax frame passes the greyscale silhouette test.
- [ ] Energy layers are additive. Smoke, dust and dark layers use normal blending.
- [ ] A white core and colored rim exist on every energy effect.
- [ ] The flash holds 2–3 frames, and secondary rings die before the main effect.
- [ ] Each character has a distinct main hue.
- [ ] The telegraph is visible at gameplay camera distance (10–20 studs).
- [ ] The effect is tested on the lowest graphics quality and on a phone (see [[VFX Performance Budget]]).

## Common Mistakes
- **Realistic soft smoke everywhere.** It reads mushy and Western. Use hard-edged flipbooks or stepped alpha.
- **Effects that linger.** A 2 s dissipation on an M1 floods the screen in a 4-player brawl.
- **All additive.** Stacked additive layers blow out to pure white and lose the color story. Mix in normal-blended dark layers for contrast.
- **No anticipation.** The hit lands with no build-up, so it feels weak no matter how big it is.
- **One flat color.** No core/rim value contrast, so the effect looks like a sticker.
- **Rings brighter than the hit.** The shockwave steals focus from the strike.

## Related
- [[ParticleEmitter Deep Dive]]
- [[Beams and Trails for Anime VFX]]
- [[Mesh-Based VFX]]
- [[Impact Frames and Screen Effects]]
- [[Creating VFX Textures]]
- [[Element VFX Recipes]]
- [[Anime Combat Animation Timing]]
- [[Toon Shading on Roblox]]
- [[Lighting for Anime Maps]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. 80.lv, "VFX Staples: Shape, Color, and Motion" (three phases; climax = max elements, biggest contrast, high saturation; dissipation = low contrast, low opacity; dissipation on separate layer). Author attributed secondhand to Stefan Jevremović. https://80.lv/articles/vfx-staples-shape-color-and-motion/ (read via search excerpt, 2026-10-31)
2. VFX Apprentice, "Genshin Impact VFX Breakdown: Stylized Technical Art Guide" (hard-edged jagged shapes, manga impact stars on flat planes; soft edges for motion). https://www.vfxapprentice.com/blog/genshin-impact-stylized-vfx-breakdown ; impact frame definition and "halve lifespans + two-frame flash" tip from https://yelzkizi.org/anime-fx-blender-after-effects-tutorial/ (practitioner blog, lower confidence)
3. EasyVFX (MIT, open source Roblox VFX plugin), `docs/impact.md`: hit-stop 50–100 ms, 2–3 frame white flash, hard shapes, secondary layers end first, camera kick, anticipation, Circ easing; cites RealtimeVFX threads https://realtimevfx.com/t/stylised-explosive-and-fiery-hit-spark-looking-for-feedback/11286 and https://realtimevfx.com/t/lightning-strike-stylized-what-do-you-guys-think-update/1972 . https://github.com/VuxSussy/EasyVFX/blob/main/docs/impact.md
4. EasyVFX README, "HD quality" table (white flash → color → gone in ~0.35 s; hot rim + glow). https://github.com/VuxSussy/EasyVFX
5. EasyVFX `docs/sharp-vfx.md` (geometry for hard edges, white core + colored rim, LightEmission 1 / LightInfluence 0, Bloom). https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
6. "AniMatrix: An Anime Video Generation Model that Thinks in Art, Not Physics" (anime breaks physics for anticipation, timing, impact). https://arxiv.org/html/2605.03652v1
7. Kitsblox, "Roblox Particle System Deep Dive" (3–5 emitters per effect; community heuristic). https://kitsblox.com/blog/roblox-particle-system-deep-dive
8. Yelzkizi, "10 Mind-Blowing Anime FX Tips" (smoke = overlapping circles, fire = sharp tapering tongues). https://yelzkizi.org/anime-fx-blender-after-effects-tutorial/
9. fullfrontal.moe, "Sakuga Espresso" (Kanada shapes, light flares, impact frames; Hashimoto's explosions). https://fullfrontal.moe/sakuga-espresso/
10. Wikipedia, "Ichirō Itano" (Kanada followers, late 1970s). https://en.wikipedia.org/wiki/Ichir%C5%8D_Itano ; Animetudes, "Exploring sakuga part 1". https://animetudes.com/2020/08/22/exploring-sakuga-part-1-birth-of-otaku-birth-of-sakuga/
11. Joseph Gilland, *Elemental Magic* Vol. I (ISBN 9780240811635) and Vol. II (ISBN 9780240814797), Focal Press/Routledge. https://www.routledge.com/products/9781138403109 ; review https://www.parkablogs.com/index.php/content/book-review-elemental-magic-art-of-special-effects-animation
12. Roblox Creator Docs, ParticleEmitter class reference (LightEmission, LightInfluence, Color, TimeScale). https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter (source: https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/ParticleEmitter.yaml , read 2026-10-31)
13. Web search summary on Black Flash depiction (black lightning; red/purple tints in some sources; low-quality sources). E.g. https://dexerto.com/anime/jujutsu-kaisen-gege-akutami-black-flash-inspired-video-game-2823239
