---
tags: [style, shape-language, characters, toon, foundations]
updated: 2026-10-31
sources: 12
status: draft
---
# Shonen Anime Shape Language

## TL;DR
- Shonen reads come from **silhouette first, surface detail last**: spiky/angular hair, oversized hands, fists and weapons, a clear V-shaped torso for heroes, and one or two signature shapes (scarf, coat tail, hair spike) that survive at 30 px tall.
- Anime surfaces are **flat colour + one hard shadow step + optional rim**. Every bump in the normals shows up as a blotch, so cel-shaded models need *cleaner*, smoother normals than PBR models, not more detail (Guilty Gear Xrd GDC 2015).
- On Roblox you don't have custom shaders. You fake the look with **SmoothPlastic or unlit-looking textures, painted-in shadows, the `Highlight` instance (max 31 rendered at once), inverted-hull outlines and ColorCorrection**.
- Proportions: R15 avatar scales all default to `1`. A shonen look on custom rigs comes from **long legs, small heads (7–8 heads tall for "cool" fighters) or chunky heads (4–5 heads tall for chibi/comedic), and big extremities**. Battlegrounds games that keep the player's avatar push the shonen read into **VFX, animation and silhouette-adding accessories** instead.
- Design the shape language at **three distances**: thumbnail (about 30 px), mid-combat (about 120 px), and close-up (domain/ultimate cutscene). If it doesn't read at 30 px, more texture won't save it.

## Why it matters for anime battlegrounds
Battlegrounds fights are fast third-person brawls in which 6–20 players spam abilities. Players identify a character (and the threat it poses) in a fraction of a second, usually through particle clutter. That identification is almost entirely **silhouette + colour block + motion**. Riot's League VFX style guide puts the same idea as "visual impact should represent gameplay impact", with readability ranked above theme. Shonen anime solved this decades ago with exaggerated, high-contrast shapes, and the Roblox engine (no custom shaders, 1 material per mesh, a mobile-heavy audience) rewards the same approach.

## How to do it

### Step 1: Pick the base shape per archetype
Classic shape psychology, as used throughout anime character design:

| Archetype | Dominant shape | Shonen examples of the read | Roblox translation |
|---|---|---|---|
| Hero / protagonist | Triangle pointing **up** + circle (approachable) | Spiky hair, V-torso, open stance | 3–5 big hair spikes (not 20 thin ones); broad shoulder accessory |
| Rival / cool type | Sharp **inverted** triangles, long verticals | Long coat, narrow eyes, sword | Long coat tail mesh + katana; dark value block |
| Powerhouse / tank | Squares / rectangles | Huge forearms, square jaw | Scale arms and hands 1.2–1.4x; blocky gauntlets |
| Trickster / support | Circles, curves | Round hair, flowing cloth | Rounded hair cards, scarf with sway bones |
| Villain / curse | Jagged, asymmetric, negative space | Horns, tattoos, uneven wings | Asymmetric shoulder piece, emissive markings |

> [!tip] One signature silhouette element per character
> Pick one thing that is still visible as a black blob: a scarf tail, a giant sword, a hair spike, a halo. In a 12-player server that one element is how people spot each other.

### Step 2: Proportions
- **Heads tall**: 7–8 heads for "cool" shonen fighters (long legs, small head), 5–6 for younger protagonists, 2–4 for chibi/comedy. These are general illustration conventions, not a Roblox rule.
- **Exaggerate the extremities**: hands, feet/boots and weapons 10–30% larger than realistic. They carry the poses and hit reads in combat animation (see [[Anime Combat Animation Timing]]).
- **Roblox reality**: R15 Humanoid scale values (`BodyHeightScale`, `BodyWidthScale`, `BodyDepthScale`, `HeadScale`) all default to `1`. `BodyProportionScale`/`BodyTypeScale` move joints between standard R15 and taller, thinner positions (0 = standard R15). Community reports say pushing scales towards about 5 causes turning glitches. Keep custom fighters inside the normal R15 joint layout so the stock animation tools and hitboxes work.

> [!warning] Unverified
> The big battlegrounds games appear to **keep the player's own avatar** and layer the "anime character" on through movesets, VFX and accessories rather than swapping in a custom anime body. I couldn't confirm this from a written source; check it in-game before basing your design on it. If true, your shonen shape language has to live in **VFX shapes, weapon meshes, auras and animation poses**, not the body.

### Step 3: Surface (flat colour, hard shadow, rim, outline)
1. **Base colour blocks**: 3–5 large flat colour areas per character (hair, top, bottom, skin, accent). Keep one **accent** at high saturation (scarf, eyes, energy colour) and the rest calmer.
2. **One shadow step**: anime colouring uses a single hard-edged shadow tone, sometimes plus a darker "2nd shadow" in creases. Shift the shadow's hue cool (blue/purple) instead of just darkening. Pure-black darkening looks muddy. See [[Anime Color and Lighting Theory for Games]].
3. **Normals matter more than detail**: Arc System Works' Junya Motomura (GDC 2015) explained that cel shading is binary (lit or unlit), so "every little noise on the surface will become extremely distracting" and "the slightest difference in the surface normal may end up as a huge blotch". The team built shaders around models made *specifically* for them and gave every character its own light sources that touch nothing else.
4. **Rim light**: a thin bright edge on the side facing away from the camera. Roblox has no Fresnel node, so you **paint it into the texture** (lit side of hair or shoulders) or fake it with `Highlight` fill or outline (see Step 4).
5. **Outlines**: 1–3 px dark lines, darker in the inner creases than on the silhouette.

### Step 4: Translate to Roblox (no custom shaders)
| Anime element | Roblox technique | Limits / numbers |
|---|---|---|
| Flat colour | `SmoothPlastic` material, or a texture painted with baked flat shading; low `EnvironmentDiffuseScale`/`EnvironmentSpecularScale` | One material per mesh |
| Cel shadow | Paint shadows into the albedo (lighting-independent), and/or a toon-ish lighting setup with ShadowMap | Painted shadows don't move with light; fine for a fixed sun |
| Outline (silhouette) | `Highlight` with `FillTransparency = 1`, `OutlineColor` dark | **Max 31 Highlights rendered at once**; disabled ones still take a slot; low-end devices fall back to a checker fill with no outline |
| Outline (inverted hull) | Duplicate mesh, flip normals in Blender, scale up about 1.02–1.05, black colour | Works best on convex shapes. A community Studio trick uses negative scale (about −1.05) on MeshParts only; may break with engine updates, so prefer baking the hull in Blender |
| Rim light | Paint it into the texture; or `Highlight` outline in a light colour for "power-up" states | Same 31 cap |
| Inner lines | Paint into the texture at 1024 px | Texture-res dependent; see below |
| Glow / energy | `Neon` material + Bloom, emissive maps in SurfaceAppearance | Bloom defaults: Intensity 0.4, Size 24, Threshold 0.95 |

Full shader workflows live in [[Toon Shading on Roblox]].

### Step 5: Texture density
- Roblox's English texture spec has long stated **1024×1024** as the max. In early 2026 Roblox shipped **4K texture rendering** (Studio Beta on 2026-01-30, later live in published experiences) on top of texture streaming, and the current localized spec page lists **4096×4096**. Weak devices get lower mips automatically.
- For anime characters, **1024² for the body + 512² for hair/accessories** is still the sensible target. Flat colour and hard lines don't gain much from 4K, and streaming may serve mobile players a low mip anyway (DevForum reports of blurry SurfaceAppearances on mobile).

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Heads tall (cool fighter) | 7–8 | Long-legged shonen look |
| Heads tall (chibi) | 2–4 | Comedy / simulator tone |
| Big shapes per character | 3–5 colour blocks | Reads at 30 px |
| Shadow tones | 1 (+1 crease) | Anime cel convention |
| Hair spikes | 3–7 large | Thin spikes vanish at distance and cost tris |
| Highlight cap | 31 on screen | Engine limit |
| Inverted hull scale | 1.02–1.05 | Thicker looks like a balloon |
| Character texture | 1024² body / 512² parts | Flat colour gains little from 4K |
| Mesh tri cap | ~20,000 per mesh (some sources say 21,000) | Importer limit; test edge cases |

## Checklist
- [ ] Silhouette sheet: fill every character solid black. Can you tell them apart at 30 px?
- [ ] One signature silhouette element per character
- [ ] Max 5 colour blocks + 1 saturated accent
- [ ] Shadow colour hue-shifted (not just darker)
- [ ] Normals smoothed / custom-split so cel shadows don't blotch (Guilty Gear lesson)
- [ ] Outline strategy chosen: Highlight (counted against 31) vs inverted hull vs painted
- [ ] Weapons and hands scaled up 10–30%
- [ ] Texture 1024² or less unless there's a proven need

## Common Mistakes
- **Detail instead of shape**: noisy sculpted folds on a cel-shaded character create shadow blotches and read as mush at combat distance.
- **20 thin hair spikes**: they vanish at distance, cost triangles, and flicker in outlines.
- **Putting a `Highlight` on every player**: past 31 the rest silently don't render, and disabled Highlights still count.
- **Black shadows**: darkening with black instead of a cool hue makes the palette look dirty.
- **Using realistic proportions with anime faces**: neither style reads.
- **Ignoring the avatar question**: designing a beautiful custom body for a game that actually keeps player avatars.

## Related
- [[Anime Character Modeling in Blender]]
- [[Toon Shading on Roblox]]
- [[Anime Color and Lighting Theory for Games]]
- [[Battlegrounds Visual Language Analysis]]
- [[Mobile-Aware Stylization]]
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]

## Sources
1. GDC Vault – Junya Motomura, "GuiltyGearXrd's Art Style: The X Factor Between 2D and 3D" (GDC 2015): https://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
2. Arc System Works handout PDF (Motomura): https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf
3. Game Developer – "Guilty Gear Xrd's striking 2D/3D art deconstructed at GDC 2015": https://gamedeveloper.com/art/see-i-guilty-gear-xrd-i-s-striking-2d-3d-art-deconstructed-at-gdc-2015
4. Roblox Creator Hub – Highlight class (31 cap, disabled still counts, low-end fallback): https://create.roblox.com/docs/reference/engine/classes/Highlight
5. DevForum – Highlights now support Outlines on Mobile [Client Beta]: https://devforum.roblox.com/t/highlights-now-support-outlines-on-mobile-client-beta/3059061
6. DevForum – How to make a black outline (inverted hull, −1.05 scale trick): https://devforum.roblox.com/t/how-to-make-a-black-outline/482739
7. DevForum – How To Outline Objects [New Method]: https://devforum.roblox.com/t/how-to-outline-objects-new-method-outlines-through-walls/1347775
8. Roblox creator-docs (GitHub) – texture specifications (1024 max, SurfaceAppearance maps): https://github.com/Roblox/creator-docs/blob/main/content/en-us/art/modeling/texture-specifications.md
9. DevForum – [Studio Beta] 4k Texture rendering (2026-01-30): https://devforum.roblox.com/t/studio-beta-4k-texture-rendering/4144950 and 4k Texture Rendering (live): https://devforum.roblox.com/t/4k-texture-rendering/4316229
10. DevForum – R15 Character Scaling / New Body Type & Proportion Sliders: https://devforum.roblox.com/t/r15-character-scaling/30642 , https://devforum.roblox.com/t/new-body-type-proportion-sliders-for-humanoid/85863
11. Riot Games – League VFX style guide ("visual impact should represent gameplay impact"): https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/
12. Roblox API mirror – BloomEffect defaults: https://robloxapi.github.io/ref/class/BloomEffect.html
