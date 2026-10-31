---
tags: [style, color, lighting, toon, theory]
updated: 2026-10-31
sources: 14
status: draft
---
# Anime Color and Lighting Theory for Games

## TL;DR
- Anime colour is **flat fills + hard shadow + hue-shifted shadows**: shadows go cooler (towards blue/purple) and lit areas warmer. Darkening with black looks muddy.
- **Value hierarchy beats hue**: characters and VFX get the highest contrast. The world stays mid-value and lower saturation so the fight reads.
- Anime games light **characters separately from the world**. Guilty Gear Xrd gives every character its own lights that affect nothing else, and Genshin-style shaders use authored face-shadow maps (SDF) instead of real lighting on faces.
- Roblox can't do per-character lights or custom shaders, so you **bake the anime lighting into textures**, keep scene lighting simple (ShadowMap, neutral sun), and use small ColorCorrection values (contrast 0–0.1, saturation 0.1–0.3).
- Use **temporary lighting states** for drama: ultimates and domains tween `Lighting` and ColorCorrection (tint, inversion, darkening) for 0.5–5 s, then return.
- Pick a **limited master palette** (about 8–12 world colours + 1 energy colour per character) and test it in greyscale.

## Why it matters for anime battlegrounds
Fights happen in chaos: 15+ players, particles and debris. Colour and value organise that chaos. If your map is as saturated as your Gojo-blue blast, nobody sees the blast. And because most Roblox players are on phones with small screens and auto-exposure-free rendering, the value structure has to be obvious.

## How to do it

### Step 1: Value structure first
1. Paint or screenshot the scene in **greyscale** (Photoshop/Krita: a Black & White adjustment layer; PureRef has a desaturate toggle).
2. Assign value bands:

| Layer | Value range (0 = black, 100 = white) | Saturation |
|---|---|---|
| Sky / far background | 60–85 | Low |
| Ground / big environment surfaces | 35–60 | Low–mid |
| Props / landmarks | 25–70 | Mid |
| Characters | Full range, darkest darks + brightest lights | Mid–high accent |
| VFX | 85–100 core with saturated edges | Highest |

> [!tip]
> The rule of thumb "the brightest, most saturated thing on screen should be the thing that hurts you" comes straight from Riot's VFX guide principle that visual impact should match gameplay impact.

### Step 2: Hue-shifted cel shadows
- **Shadow = base hue shifted 10–30° towards blue/purple, saturation slightly up, value down 15–30%.** Light side = base shifted slightly warm (towards yellow/orange).
- Skin is the classic test: lit `#F7D8C4` → shadow around `#D9A3A0` (pinker and cooler), not grey-brown. *(Example values for illustration, not from a source.)*
- Add a **2nd darker crease shadow** only in deep occlusion (under the chin, between fingers, inner hair).
- Blender toon-shader users note that shadow and mid-tone colours often *multiply* with base colour, so the displayed shadow differs from the swatch. Check the final render, not the picker.

### Step 3: Rim and highlight
- **Rim light** separates character from background: 1–3 px painted edge on hair/shoulders, light-coloured or tinted with the environment's sky colour.
- **Specular highlights** on hair are a painted band (the "angel ring"), not real specular. On Roblox keep `EnvironmentSpecularScale` low so it doesn't fight painted highlights.

### Step 4: How the pros light anime characters
| Technique | Who | What it does | Roblox equivalent |
|---|---|---|---|
| Per-character lights | Guilty Gear Xrd (Arc System Works, GDC 2015) | Each character has its own light sources affecting only that character | Not possible; bake lighting into texture, or use `Highlight` fill for special states |
| Custom cel shader editor | Guilty Gear Xrd | Iterated shading late in production | Not possible; iterate in Blender, then bake |
| Face shadow texture / SDF | Genshin Impact (per community recreations) | A greyscale map stores at which light angle each face pixel turns shadowed, giving clean anime nose and cheek shadows | Bake one or two fixed face shadow states into the texture, or swap decals by light side (advanced) |
| Ramp textures | Many toon shaders | N·L samples a 1D ramp for colour bands | Fake with painted bands |

> [!warning] Unverified
> The Genshin face-shadow description comes from community shader recreations (GitHub, Godot Shaders, UE forums), not from miHoYo's own talk, which I couldn't locate.

### Step 5: Roblox scene lighting for anime
Baseline (adapt per map):

| Property | Starting point | Source / reason |
|---|---|---|
| `Lighting.Technology` | ShadowMap (Future only for small, controlled scenes) | Future is per-pixel and each light adds cost; devices without support fall back ShadowMap → Voxel |
| ColorCorrection Contrast | 0.0–0.1 | DevForum cartoon consensus |
| ColorCorrection Saturation | 0.1–0.3 | DevForum consensus; ~1.0 is an outlier and looks garish |
| ColorCorrection Brightness | 0–0.2 | Adopt Me creator values relayed on DevForum: 0.2 / 0.1 / 0.12 with tint (255, 243, 235) |
| Tint | Neutral or slightly warm (255, 243, 235) | Avoid heavy tints on the baseline |
| Bloom | Default 0.4 / 24 / 0.95 or disabled | Community advice: avoid heavy bloom for cartoon looks |
| Ambient (example) | (163, 163, 163) with Brightness ~2.67 | One builder's cartoon preset on DevForum |
| Materials | SmoothPlastic for most surfaces | DevForum style advice |

Deeper map lighting: [[Lighting for Anime Maps]]. Shader tricks: [[Toon Shading on Roblox]].

### Step 6: Temporary lighting states (the anime "moment")
| State | Duration | Changes |
|---|---|---|
| Impact frame | 2–6 frames | ColorCorrection Saturation −1 + Contrast up, or a full-screen white/black frame (UI) |
| Ultimate start | 0.3–1.0 s | Darken world (Brightness −0.3), tint towards move colour |
| Domain / field | 3–10 s | Swap sky, fog colour and ColorCorrection tint; restore after |
| Awakening | Persistent per player | Only on that player: aura VFX + Highlight (watch the 31 cap) |

Use `TweenService` on Lighting properties and always restore the baseline (see [[Anime VFX Fundamentals]]).

### Step 7: Palette building
1. Pick **1 key hue** for the map's mood (dusk orange, Shibuya night blue, training-ground green).
2. Build **8–12 world swatches**: 3 ground, 3 structure, 2 foliage, 2 accent, 1–2 sky.
3. Reserve **energy colours** (bright blue, purple, red, gold) for VFX. Keep them out of the world palette.
4. Test: put each character's energy colour against the map in greyscale. It should be the brightest value.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Shadow hue shift | 10–30° cool | Anime colour convention |
| Shadow value drop | 15–30% | Visible but not black |
| World swatches | 8–12 | Cohesion |
| Saturation (CC) | 0.1–0.3 | Pop without garishness |
| Contrast (CC) | 0–0.1 | Avoid crushed blacks |
| Ultimate darken | 0.3–1 s tween | Drama without disorientation |

## Checklist
- [ ] Greyscale test of map + characters + VFX
- [ ] World palette of 8–12 swatches; energy colours excluded
- [ ] Shadow swatches hue-shifted, not black-multiplied
- [ ] Baseline Lighting + ColorCorrection preset saved as a model or script
- [ ] 2–3 tweened "moment" lighting states with guaranteed restore
- [ ] Phone test: is the VFX still the brightest thing outdoors at noon?

## Common Mistakes
- Saturation 0.8–1.0 on ColorCorrection: garish and tiring.
- Heavy bloom on the whole world so every white wall glows.
- Black shadows painted into character textures.
- Using the same blue for the sky and for the main character's energy.
- Lighting states that don't restore when a player dies mid-ultimate.
- Future lighting with dozens of `PointLight`s from abilities on mobile.

## Related
- [[Shonen Anime Shape Language]]
- [[Toon Shading on Roblox]]
- [[Lighting for Anime Maps]]
- [[Anime VFX Fundamentals]]
- [[Battlegrounds Visual Language Analysis]]
- [[Mobile-Aware Stylization]]

## Sources
1. GDC Vault – GuiltyGearXrd's Art Style (per-character lights, shader editor): https://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
2. Arc System Works – Guilty Gear Xrd Art Talk at GDC 2015: https://www.arcsystemworks.com/guilty-gear-xrd-art-talk-at-game-developers-conference-2015/
3. GitHub – NoiRC256/URPSimpleGenshinShaders (face shadow texture explanation): https://github.com/NoiRC256/URPSimpleGenshinShaders
4. GitHub – xcupsilon/unreal-genshin-character-shader (SDF shadow, artist light/shadow colours): https://www.github.com/xcupsilon/unreal-genshin-character-shader
5. Godot Shaders – Toon Shader inspired by Genshin Impact (ramp): https://godotshaders.com/shader/toon-shader-inspired-of-genshin-impact/
6. StraySpark – How to get anime toon look in Blender (hue-shifted shadows): https://www.strayspark.studio/blog/how-to-get-anime-toon-look-blender
7. Pixivision – 15 Cel Shading Tutorials: https://www.pixivision.net/en/a/2363
8. DevForum – Cartoon lighting settings: https://devforum.roblox.com/t/cartoon-lighting-settings/333686
9. DevForum – Which lighting style is best for cartoon style maps (Adopt Me values): https://devforum.roblox.com/t/which-lighting-style-is-best-for-cartoon-style-maps/643528
10. DevForum – Lighting Settings For Cartoony Style: https://devforum.roblox.com/t/lighting-settings-for-cartoony-style/2167959
11. DevForum – How can I make my game look more anime-ish or cartoonish?: https://devforum.roblox.com/t/how-can-i-make-my-game-look-more-anime-ish-or-cartoonish/2825602
12. DevForum – Future is Bright on Android fully rolled out (per-pixel cost): https://devforum.roblox.com/t/future-is-bright-on-android-is-fully-rolled-out-client-beta/3235808
13. DevForum – Future Is Bright Phase 3 Studio Beta (fallback order): https://devforum.roblox.com/t/future-is-bright-phase-3-studio-beta/639903
14. Riot – League VFX style guide: https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/
