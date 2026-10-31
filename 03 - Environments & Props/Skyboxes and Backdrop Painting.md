---
tags: [environments, skybox, backdrop, matte-painting, sky]
updated: 2026-10-31
sources: 11
status: draft
---
# Skyboxes and Backdrop Painting

## TL;DR
- A Roblox `Sky` is a **6-face cube map** (`SkyboxBk`, `SkyboxDn`, `SkyboxFt`, `SkyboxLf`, `SkyboxRt`, `SkyboxUp`). Faces must be **seamless along all edges** when folded. The built-in default faces are 512² (`sky512_*.tex`).
- For anime skies, **paint** an equirectangular (2:1) panorama with flat cel clouds and a soft gradient, convert it to 6 cube faces at **1024²** (community guides use 1024–2048), and upload them. Roblox textures support up to **4096²**.
- Turn off the default sun or moon (`CelestialBodiesShown = false`, or `SunAngularSize = 0` while keeping stars) and **paint the sun into the sky**, or use a custom `SunTextureId` with `SunAngularSize` (0–60, default 21).
- Get cheap animated clouds by rotating `SkyboxOrientation` on Y (for example 0.5–5°/s). The docs describe it as low-cost on all platforms. It does not rotate celestial bodies or reflections.
- Fill the gap between the playable map and the sky with a **backdrop ring**: low-poly silhouettes (mountains, skyline) in 2–3 value layers that fade toward the sky color, plus `Atmosphere` haze.

## Why it matters for anime battlegrounds
Anime battle scenes are framed by **painted skies**: towering cumulus, dramatic sunsets, a giant moon. On Roblox the sky covers half the screen during jumps and launches, so it carries much of the style. Using Roblox's default sky, or a photo HDRI sky, is the fastest way to look "un-anime". The backdrop also hides map edges and sets the scale of super-speed fights (see [[Battleground Arena Map Design]]).

## How to do it
### Step 1: Paint or render the panorama
Options, roughly in order of anime authenticity:
1. **Hand-paint** a 2:1 equirectangular image (for example 4096×2048) in Krita or Photoshop with a panorama grid. Keep the horizon at the vertical middle.
2. **Render in Blender**: model stylized cloud meshes, toon-shade them, and render with an equirectangular panoramic camera. A DevForum tutorial covers making Roblox skyboxes in Blender at 1024 or 2048 px per face.
3. **Render inside Studio**: square viewport, **90° FOV**, six captures in the order front, left, back, right, up, down. Suggested capture size is 512 or 1024 square.

Paint rules for an anime sky:
- **Gradient**: saturated zenith (for example `#3A7BD5`) fading to a pale, slightly warm horizon (`#CFE6F5`). Anime skies get *lighter* toward the horizon.
- **Clouds**: flat cel shapes with 2–3 tones (white lit tops, lavender or grey-blue undersides), crisp edges, big–medium–small grouping. See [[Shonen Anime Shape Language]].
- Keep the **bottom face (Dn)** simple, a solid horizon-colored or ground color. Players rarely see it, and Atmosphere covers it.
- Keep high-contrast detail **away from the cube edges and corners**, where seams and distortion show.

### Step 2: Convert to 6 faces
- Use a panorama-to-cubemap converter (the DevForum guide recommends the "Panorama to Cubemap" tool by Jaxry). An *incomplete* panorama causes seams.
- Output 6 square faces at **1024²** (or 2048² for hero maps). 4096² is the documented texture maximum, but 6 faces at 4K is a lot of texture memory on mobile.

> [!warning] Unverified
> Some older community posts call 1024 the skybox maximum. Current Roblox docs state textures in general go up to 4096², but I found no doc that confirms the sky faces render above 1024 without downscaling on every device. Test on a phone.

### Step 3: Apply in Studio
1. Insert `Sky` under `Lighting`.
2. Upload the 6 images and paste the IDs into `SkyboxBk`, `SkyboxDn`, `SkyboxFt`, `SkyboxLf`, `SkyboxRt`, `SkyboxUp` (the `*Content` versions also accept Content).
3. Check every seam by flying the camera around. If a face is rotated, rotate the image 90° and re-upload. Up and Down faces are the usual offenders.

### Step 4: Celestial bodies
| Property | Default | Anime use |
|---|---|---|
| `CelestialBodiesShown` | true | false when the sun is painted in |
| `SunAngularSize` | 21 (0–60) | 0 hides only the sun. 10–15 for a smaller, stylized sun |
| `SunTextureId` | `rbxasset://sky/sun.jpg` | A custom flat cel sun disk with a glow ring |
| `MoonAngularSize` | 11 | 14–25 for a dramatic "big anime moon" |
| `MoonTextureId` | `rbxasset://sky/moon.jpg` | A custom painted moon |
| `StarCount` | 3000 | 300–800 for cleaner night skies |

The sun position follows `ClockTime` and `GeographicLatitude`. Line the painted light direction up with the actual sun direction, so shadows match the painting (see [[Lighting for Anime Maps]]).

### Step 5: Animate with SkyboxOrientation
```lua
-- From the Roblox skybox guide: spin on Y with a fixed tilt
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")
local sky = Lighting:FindFirstChildOfClass("Sky")
local ROTATION_SPEED = 1 -- degrees per second (docs example uses 5)
RunService.Heartbeat:Connect(function(dt)
	sky.SkyboxOrientation = Vector3.new(0, (sky.SkyboxOrientation.Y + ROTATION_SPEED * dt) % 360, 0)
end)
```
Limits from the docs: celestial bodies don't rotate, indoor or mirror reflections of the sky don't rotate, ViewportFrame skies follow the global orientation, and dynamic `Clouds` aren't affected. Run it on the **client** (a LocalScript), because it is purely cosmetic.

### Step 6: Backdrop ring (between map and sky)
Layer 2–3 rings of silhouettes beyond the playable boundary:
| Layer | Distance from arena edge | Content | Value |
|---|---|---|---|
| Near | 50–150 studs | Low-poly buildings or trees, simple texture | Mid, slightly cooler than the arena |
| Mid | 200–600 studs | Flat silhouette meshes (single color), mountains or skyline | Lighter, desaturated toward the sky |
| Far | in the skybox | Painted mountains or city in the panorama | Lightest, nearly sky color |

- Make backdrop meshes **single flat colors** (`SmoothPlastic`, no texture, `CastShadow = false`, `CanCollide = false`, `CanQuery = false`). They instance cheaply.
- Tune `Atmosphere.Offset` higher for a crisp horizon silhouette, or lower to blend the far layers into the sky. A low offset can ghost the skybox through geometry, and a high one reveals LOD popping.
- Use `Model.LevelOfDetail = SLIM` on big static backdrop models (see [[Environment Performance Budgets]]).
- Beyond the streaming radius, unstreamed geometry disappears unless SLIM stand-ins exist. **Painting distant elements into the skybox** is the cheapest guarantee that they're always visible.

> [!warning] Unverified
> The layer distances are my own proposal for arena maps of about 300–500 studs.

### Step 7: Per-preset skies
Make one skybox per lighting preset (day, sunset, night) and swap the six IDs, or the whole `Sky` instance, when the arena's preset changes. Preload the images with `ContentProvider:PreloadAsync` to avoid a gray flash.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Faces | 6, seamless | Skybox docs |
| Face resolution | 1024² standard, 2048² hero | Community guidance (verify on mobile) |
| Texture max | 4096² | Texture specs |
| Default faces | 512² (`sky512_*`) | Sky class defaults |
| SunAngularSize | 0–60, default 21 | Sky class |
| MoonAngularSize | default 11 | API dump |
| StarCount | default 3000 | API dump |
| Capture FOV (Studio render) | 90° | DevForum |

## Checklist
- [ ] Panorama painted with an anime gradient and cel clouds. Horizon centered.
- [ ] Converted to 6 faces, seams checked on all 12 cube edges.
- [ ] Sun painted in (bodies off) or a custom sun texture aligned to ClockTime.
- [ ] Slow client-side Y rotation (optional).
- [ ] Backdrop ring of flat silhouettes, Atmosphere tuned.
- [ ] One sky per lighting preset, preloaded.

## Common Mistakes
- Photo or HDRI skies on a toon map, a style clash.
- A painted sun in one direction and the real sun casting shadows from another.
- High-contrast clouds across cube seams, so the seams are visible.
- 6×4K faces on a mobile-first game, which wastes memory.
- Rotating the sky on the server every Heartbeat, which causes needless replication.

## Related
- [[Lighting for Anime Maps]]
- [[Battleground Arena Map Design]]
- [[Environment Performance Budgets]]
- [[Shonen Anime Shape Language]]
- [[Toon Shading on Roblox]]

## Sources
1. Skyboxes guide (construction, celestial bodies, orientation script and limits): https://create.roblox.com/docs/environment/skybox
2. Sky class (properties, defaults, SunAngularSize clamp): https://create.roblox.com/docs/reference/engine/classes/Sky
3. Atmosphere class (Offset ghosting/LOD popping): https://create.roblox.com/docs/reference/engine/classes/Atmosphere
4. Texture specifications (4096²): https://create.roblox.com/docs/art/modeling/texture-specifications
5. SLIM: https://create.roblox.com/docs/workspace/streaming/slim
6. Roblox API dump (MoonAngularSize, StarCount defaults): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
7. DevForum: Custom Skyboxes 101 (2:1 panorama, Jaxry converter): https://devforum.roblox.com/t/custom-skyboxes-101/2849003
8. DevForum: Rendering skyboxes in Studio (90° FOV, face order, 512/1024): https://devforum.roblox.com/t/rendering-skyboxes-in-studio/939151
9. DevForum: Creating custom skyboxes using Blender & crafting stunning atmospheres (1024/2048): https://devforum.roblox.com/t/creating-custom-skyboxes-using-blender-crafting-stunning-atmospheres/3134324
10. DevForum: Is there any way to transform a Roblox map into an HDRI (old 1024 claim): https://devforum.roblox.com/t/is-there-anyway-to-transform-a-roblox-map-into-a-hdri-image/253080/2
11. 80.lv: Creating a painterly-like stylized environment inspired by Howl's Moving Castle (painterly sky reference): https://80.lv/articles/creating-a-painterly-like-and-stylized-environment-inspired-by-howl-s-moving-castle
