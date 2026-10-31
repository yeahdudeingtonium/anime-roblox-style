---
tags: [environments, lighting, atmosphere, post-processing, skybox, presets]
updated: 2026-10-31
sources: 14
status: draft
---
# Lighting for Anime Maps

## TL;DR
- **`Lighting.Technology` is deprecated.** It was replaced by **`LightingStyle`** (`Realistic` | `Soft`) plus **`PrioritizeLightingQuality`** (bool), through the Unified Lighting rollout announced on 2025-07-23. The old modes map over: Future → Realistic + true, ShadowMap → Soft + true, Voxel → Soft + false.
- For anime battlegrounds, start from **`Soft` + `PrioritizeLightingQuality = true`**: flat, soft lighting with shadow maps. Switch to `Realistic` only for night-city maps that need many local lights.
- Get the anime "airbrushed sky" look from **`Atmosphere`** (Density about 0.25–0.35, Haze 0–1.5, a tinted `Color`) and a **painted `Sky`** with `CelestialBodiesShown` usually off.
- Post-processing should be light: Bloom (Intensity 0.3–1, Threshold 0.9–1.5), ColorCorrection (Saturation +0.1 to +0.3), a subtle SunRays. **Avoid world DepthOfField in combat.** Keep DoF for cutscenes and menus.
- `ColorGradingEffect.TonemapperPreset = Retro` flattens contrast for an older or retro anime look. Only the most recently parented one applies.
- The presets below are **starting points, not verified in Studio** (marked). Tune them on a phone.

## Why it matters for anime battlegrounds
Lighting sets the **value structure** that characters and VFX are read against. Anime backgrounds use high-key skies, cool shadows, warm light and saturated but not neon local color. Battlegrounds also need **bright, even lighting across the whole arena**, so a fight in the "shadow corner" is as readable as one in the sun, and enough headroom that bloom-heavy ultimates (see [[Anime VFX Fundamentals]]) still pop. Pair this note with [[Toon Shading on Roblox]] for the flattening tricks.

## How to do it
### Step 1: Pick the lighting style
| Property | Values | Anime recommendation |
|---|---|---|
| `LightingStyle` | `Realistic` (most advanced lights and shadows) / `Soft` ("flat, retro-Roblox look with softer lights and shadows") | **Soft** for day maps. Realistic for night cities with many neon lights |
| `PrioritizeLightingQuality` | `true` keeps advanced shadows and shaders close up as quality drops; `false` keeps view distance | **true** on arena maps (small, so view distance matters less); **false** on huge open-world maps (Blox Fruits / GPO-style seas) |
| `GlobalShadows` | bool | **true**: cast shadows give characters grounding contact |
| `ShadowSoftness` | 0 (hard) – 1 (soft) | 0–0.15 for crisp anime shadows. The guide says it is only valid with `Realistic` |

> [!warning] Unverified
> According to the `LightingStyle` property docs, "Soft with PrioritizeLightingQuality enabled uses shadow maps rather than voxel lighting". I have not confirmed in Studio how much `Soft` differs visually from the old ShadowMap mode on mobile.

Notes:
- The old `Technology` enum values `Legacy`, `Compatibility` and `Unified` cannot be selected in Studio. Roblox suggests recreating the Compatibility look with **Voxel lighting plus `ColorGradingEffect` set to `Retro`**.
- The light `Range` for `PointLight`, `SpotLight` and `SurfaceLight` is **always clamped to 120 studs**.
- Shadows degrade automatically at lower quality levels and are **off entirely below quality level 4**.

### Step 2: Ambient and color
| Property | Default | What it does |
|---|---|---|
| `Ambient` | `[0,0,0]` per guide | Hue for areas occluded from the sky (interiors). If `GlobalShadows` is off, it applies everywhere |
| `OutdoorAmbient` | `[127,127,127]` | Hue for outdoor areas. Clamped to be ≥ `Ambient` per channel |
| `ColorShift_Top` | `[0,0,0]` | Tint on sun-facing surfaces, giving warm key light |
| `ColorShift_Bottom` | `[0,0,0]` | Tint on surfaces facing away from the sun. Hard to see with `GlobalShadows` on |
| `Brightness` | 1 (API) | Sun or moon intensity |
| `ExposureCompensation` | 0, range −5 to 5 | +1 doubles exposure, −1 halves it |
| `EnvironmentDiffuseScale` | 0 | Sky-derived ambient. **Keep it 0–0.3 for toon** |
| `EnvironmentSpecularScale` | 0 | Sky reflections. **Keep it 0 for matte anime** |
| `ClockTime` / `TimeOfDay` | 14 / "14:00:00" | Sun position |
| `GeographicLatitude` | 41.73 | Sun arc. Lower it (about 20–30) for higher noon suns |

**Anime ambient rule:** shadows should be **lighter and cooler** than realistic ones. Push `OutdoorAmbient` toward blue-violet (for example `[150,155,185]`) and `ColorShift_Top` toward warm (for example `[255,230,200]`).

### Step 3: Atmosphere
| Property | Instance default | Range / notes |
|---|---|---|
| `Density` | 0.395 | 0 = clear, 1 = opaque. Affects objects and terrain only, and the sky only through them |
| `Offset` | 0 | Higher gives a horizon silhouette; lower blends distant objects into the sky. A low offset can make the skybox **ghost through geometry** |
| `Color` | `[200,170,108]` | Needs Haze > 0 to show |
| `Decay` | `[92,60,14]` | Hue away from the sun. Needs Haze and Glare > 0 |
| `Glare` | 0 | Glow around the sun. Needs Haze > 0 |
| `Haze` | 0 | Haziness at the horizon and in the distance |

The official examples show Density 0 vs 0.35, Offset 0 vs 1, Haze 1 vs 2.8, and Color `[255,255,255]` vs `[255,200,255]`. Note that **Fog properties are hidden while an Atmosphere exists**. Choose one or the other.

### Step 4: Post-processing stack
Parent effects to `Lighting` (everyone sees them) or `Camera` (that player only, for example for a hit-flash).

| Effect | Instance defaults | Anime use | Stacking |
|---|---|---|---|
| `BloomEffect` | Intensity 0.4, Size 24, Threshold 0.95 | Glow on bright VFX and Neon. Threshold ~1+ blooms only true highlights | Multiple compose |
| `ColorCorrectionEffect` | Brightness 0, Contrast 0, Saturation 0, Tint white | +Saturation, slight +Contrast, a warm or cool tint per map | Multiple compose |
| `SunRaysEffect` | Intensity 0.25, Spread 1 (0–1) | God rays in "dramatic" moments. May not render on low-end devices | n/a |
| `DepthOfFieldEffect` | FarIntensity 0.75, FocusDistance 0.05, InFocusRadius 10, NearIntensity 0.75 | Cutscenes and ultimate cameras only | n/a |
| `BlurEffect` | Size 24 | Menus and stun flashes, through Camera | Only the largest `Size` applies |
| `ColorGradingEffect` | TonemapperPreset Default | `Retro` = less saturation and contrast | Only the most recently parented one applies |

> [!tip] Effects as gameplay feedback
> Tween a `ColorCorrectionEffect` under `Camera` for impact frames: `TintColor` to red, `Contrast` +0.5 for 0.05 s on a heavy hit. See [[Anime VFX Fundamentals]].

### Step 5: Sky and clouds
- `Sky` has six faces (`SkyboxBk/Dn/Ft/Lf/Rt/Up`), `SunAngularSize` (default 21, clamped 0–60), `MoonAngularSize` (11), `StarCount` (3000), `CelestialBodiesShown`, and `SkyboxOrientation`, which you can rotate cheaply for drifting painted clouds. Full workflow in [[Skyboxes and Backdrop Painting]].
- `Clouds` **only render when parented to `Terrain`**. Properties are Cover (0–1, default 0.5), Density (0.7) and Color. Global wind drives them. Dynamic clouds are realistic volumetrics, so for a painted anime sky, consider skipping them and painting clouds into the skybox.

## Presets
> [!warning] Unverified
> These preset values are my own starting points, built from the documented property ranges. They have **not** been checked in Studio or taken from a published game. Use them as a base, then adjust them against a reference screenshot on a mid-range phone.

### Preset A: Bright Anime Day (default arena)
| Object.Property | Value |
|---|---|
| Lighting.LightingStyle | Soft |
| Lighting.PrioritizeLightingQuality | true |
| Lighting.ClockTime | 13.5 |
| Lighting.GeographicLatitude | 25 |
| Lighting.Brightness | 2.2 |
| Lighting.Ambient | [120,125,140] |
| Lighting.OutdoorAmbient | [165,170,190] |
| Lighting.ColorShift_Top | [255,240,215] |
| Lighting.EnvironmentDiffuseScale | 0.15 |
| Lighting.EnvironmentSpecularScale | 0 |
| Lighting.ExposureCompensation | 0.1 |
| Atmosphere.Density | 0.28 |
| Atmosphere.Offset | 0.2 |
| Atmosphere.Color | [200,225,255] |
| Atmosphere.Decay | [140,175,230] |
| Atmosphere.Glare | 0.2 |
| Atmosphere.Haze | 1.2 |
| Bloom | Intensity 0.5, Size 24, Threshold 1.1 |
| ColorCorrection | Saturation 0.2, Contrast 0.08, Brightness 0.02, Tint [255,252,245] |
| SunRays | Intensity 0.06, Spread 0.6 |
| Sky | Painted blue gradient with cumulus; CelestialBodiesShown false *or* SunAngularSize 12 |

### Preset B: Dramatic Sunset (finale / boss arena)
| Object.Property | Value |
|---|---|
| Lighting.LightingStyle | Soft (or Realistic for longer, softer shadows) |
| Lighting.ClockTime | 17.6 |
| Lighting.Brightness | 2.8 |
| Lighting.Ambient | [90,70,110] |
| Lighting.OutdoorAmbient | [150,110,150] |
| Lighting.ColorShift_Top | [255,170,110] |
| Lighting.ColorShift_Bottom | [80,60,140] |
| Lighting.ShadowSoftness | 0.1 |
| Atmosphere.Density | 0.33 |
| Atmosphere.Offset | 0.1 |
| Atmosphere.Color | [255,190,150] |
| Atmosphere.Decay | [120,70,140] |
| Atmosphere.Glare | 1.5 |
| Atmosphere.Haze | 2.2 |
| Bloom | Intensity 0.8, Size 32, Threshold 0.95 |
| ColorCorrection | Saturation 0.25, Contrast 0.15, Tint [255,235,220] |
| SunRays | Intensity 0.15, Spread 0.8 |
| Sky | Painted orange-magenta gradient, long streaky clouds, sun low on the horizon face |

### Preset C: Night City (neon district, Jujutsu-style urban)
| Object.Property | Value |
|---|---|
| Lighting.LightingStyle | Realistic |
| Lighting.PrioritizeLightingQuality | true |
| Lighting.ClockTime | 0 |
| Lighting.Brightness | 0.6 |
| Lighting.Ambient | [45,45,75] |
| Lighting.OutdoorAmbient | [70,75,120] |
| Lighting.EnvironmentDiffuseScale | 0.2 |
| Lighting.EnvironmentSpecularScale | 0.3 (wet streets only) |
| Lighting.ExposureCompensation | 0.3 |
| Atmosphere.Density | 0.35 |
| Atmosphere.Color | [120,110,170] |
| Atmosphere.Decay | [60,40,90] |
| Atmosphere.Haze | 1.8 |
| Atmosphere.Glare | 0 |
| Bloom | Intensity 1.0, Size 28, Threshold 0.9 |
| ColorCorrection | Saturation 0.15, Contrast 0.12, Tint [235,235,255] |
| Sky | Dark indigo gradient, CelestialBodiesShown true, StarCount 500, MoonAngularSize 14 |
| Local lights | PointLights in signs, Range ≤ 30, **Shadows = false** on most |

> [!tip] Night maps must stay readable
> Never let ambient drop below about `[40,40,60]` in a combat map. Players must read silhouettes. Signs with **emissive SurfaceAppearance/Decals** give "light" without the cost of real lights.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Light Range clamp | 120 studs | Lighting docs |
| Shadows disabled | below quality 4 | Performance docs |
| ExposureCompensation range | −5…5 | Lighting class |
| SunAngularSize | 0–60, default 21 | Sky class |
| SunRays Spread | 0–1 | Outside that range is undefined |
| Blur stacking | Only the largest Size | BlurEffect |
| ColorGrading stacking | Only the most recent | ColorGradingEffect |

## Checklist
- [ ] Set `LightingStyle`, `PrioritizeLightingQuality` and `GlobalShadows`. Ignore the old `Technology`.
- [ ] Add one `Atmosphere`, one `Sky`, and Bloom + ColorCorrection under Lighting.
- [ ] Keep `EnvironmentSpecularScale` at 0 unless a map needs wet or metal reflections.
- [ ] Put gameplay screen effects under `Camera`, not Lighting.
- [ ] Check readability at quality 1 (no shadows, reduced effects).
- [ ] Save each preset as a ModuleScript table so lighting can switch per arena or round.

## Common Mistakes
- Copying "Future lighting" tutorials from before 2025. `Technology` no longer shows in Studio.
- Fog and Atmosphere together (fog properties are hidden and ignored).
- A high `Atmosphere.Density` on small arenas, which washes out characters 100 studs away.
- World DepthOfField during combat, which blurs enemies at range.
- Multiple ColorGradingEffects, of which only the last one applies.
- Night maps lit with dozens of shadow-casting PointLights, which tanks mobile.

## Related
- [[Toon Shading on Roblox]]
- [[Skyboxes and Backdrop Painting]]
- [[Environment Performance Budgets]]
- [[Battleground Arena Map Design]]
- [[Anime VFX Fundamentals]]
- [[Shonen Anime Shape Language]]

## Sources
Roblox docs were checked 2026-10-31 against `github.com/Roblox/creator-docs` (commit 2026-10-29), because create.roblox.com was unreachable from the research sandbox. Instance defaults come from the Roblox-Client-Tracker API dump.
1. Global lighting: https://create.roblox.com/docs/environment/lighting
2. Lighting class: https://create.roblox.com/docs/reference/engine/classes/Lighting
3. LightingStyle enum: https://create.roblox.com/docs/reference/engine/enums/LightingStyle
4. Technology enum (deprecations, Retro suggestion): https://create.roblox.com/docs/reference/engine/enums/Technology
5. DevForum: Let There Be (Unified) Light! Unified Lighting is Fully Live (2025-07-23, mapping table): https://devforum.roblox.com/t/let-there-be-unified-light-unified-lighting-is-fully-live/3401512
6. Atmospheric effects: https://create.roblox.com/docs/environment/atmosphere
7. Atmosphere class: https://create.roblox.com/docs/reference/engine/classes/Atmosphere
8. Post-processing effects: https://create.roblox.com/docs/environment/post-processing-effects
9. BloomEffect / BlurEffect / ColorCorrectionEffect / SunRaysEffect / DepthOfFieldEffect / ColorGradingEffect classes: https://create.roblox.com/docs/reference/engine/classes/BloomEffect (and sibling class pages)
10. Sky class and Skybox guide: https://create.roblox.com/docs/reference/engine/classes/Sky , https://create.roblox.com/docs/environment/skybox
11. Dynamic clouds: https://create.roblox.com/docs/environment/clouds
12. Improve performance (shadows off below quality 4): https://create.roblox.com/docs/performance-optimization/improve
13. Roblox API dump (instance defaults): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
14. DevForum bug report: ShadowSoftness hidden under Soft: https://devforum.roblox.com/t/unified-lighting-beta-shadowsoftness-lighting-property-does-not-appear-when-lightingstyle-is-set-to-soft/3509181
