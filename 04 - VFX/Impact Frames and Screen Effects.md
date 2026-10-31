---
tags: [vfx, impact-frames, screen-shake, colorcorrection, camera, fov, speed-lines]
updated: 2026-10-31
sources: 14
status: draft
---
# Impact Frames and Screen Effects

## TL;DR
- An **impact frame** is one to a few highly stylized frames at the moment of a big hit: stark black and white, inverted colors, or abstract shapes. It comes from sakuga (Kanada-style light flares and impact frames). [1][2]
- On Roblox, build them with a `ColorCorrectionEffect` on the **client** (Saturation **−1** = full greyscale, Brightness **−1 … 1** = black … white, Contrast, multiplicative TintColor) held for **2–4 frames**, then restored. [3][4]
- Screen shake: use a **kick** (full strength on frame 1, fast decay), not a long wobble. The EZ Camera Shake port (`RbxCameraShaker`) is the common module. [5][6]
- **FOV punch:** `Camera.FieldOfView` is clamped **1–120**, default **70**. Drop or raise it by a few degrees for 0.05 s, then ease back over ~0.2 s. [7][5]
- Put screen effects under **`Camera`** (only that player sees them) or create them in a LocalScript. Effects under `Lighting` show to **everyone** in the server. [4]

## Why it matters for anime battlegrounds
The black-and-white flash on a Black Flash-style crit, the white-out on an ultimate, the camera jolt on a wall slam: these are what players clip and share. They also make up for Roblox's limits. A 2–3 frame flash hides missing in-between animation, and a camera kick adds weight a 60-tri rock can't. They're also the easiest effects to overdo. Only the attacker and victim (or nearby players) should get the strongest version.

## How to do it

### Step 1 — Know the building blocks (official API)
| Instance | Property | Range / behavior | Impact use |
|---|---|---|---|
| `ColorCorrectionEffect` | `Brightness` | −1 = all black … 1 = all white [3] | White-out (+0.6 to +1), black-out (−1) |
| | `Contrast` | <0 reduced, >0 increased [3] | +1 to +3 for harsh manga look |
| | `Saturation` | >1 vivid, **−1 = full desaturation** [3] | −1 for black-and-white frames |
| | `TintColor` | Multiplicative per channel; (255,0,0) zeroes G and B [3] | Red tint for rage or crit |
| `BloomEffect` | `Intensity`, `Size` (px), `Threshold` (1 = only white blooms, 0 = everything) [8] | Spike Intensity for a glow pop |
| `BlurEffect` | `Size` | Radial-free Gaussian blur of the whole view [4] | 1-frame blur on dash |
| `Camera` | `FieldOfView` | **1–120, default 70** (vertical degrees) [7] | FOV punch |
| `Highlight` | `FillColor`, `FillTransparency`, `OutlineColor`, `DepthMode` | **Max 255 simultaneous Highlights on a client.** Disabled ones still take a slot [9] | Silhouette characters during the frame |

Post-processing effects parented to `Lighting` display to all players. Parented to `Camera`, they display only to that player [4].

### Step 2 — Black-and-white impact frame
1. LocalScript creates (once) a `ColorCorrectionEffect` named `ImpactCC` under `workspace.CurrentCamera`.
2. On hit confirm (server → client remote), run a 3-step sequence:

```lua
local RunService = game:GetService("RunService")
local cam = workspace.CurrentCamera
local cc = cam:FindFirstChild("ImpactCC") or Instance.new("ColorCorrectionEffect")
cc.Name = "ImpactCC"; cc.Parent = cam

local function waitFrames(n)
	for _ = 1, n do RunService.RenderStepped:Wait() end
end

local function impactFrame(style: "mono" | "white" | "invertish")
	if style == "mono" then
		cc.Saturation, cc.Contrast, cc.Brightness = -1, 2, 0
	elseif style == "white" then
		cc.Saturation, cc.Contrast, cc.Brightness = -1, 0, 0.8
	else -- harsh high-contrast tinted frame
		cc.Saturation, cc.Contrast, cc.Brightness = -1, 3, -0.2
		cc.TintColor = Color3.fromRGB(255, 80, 80)
	end
	waitFrames(3)                  -- hold ~0.05 s at 60 fps
	cc.Saturation, cc.Contrast, cc.Brightness = 0, 0, 0
	cc.TintColor = Color3.new(1, 1, 1)
end
```

Counting `RenderStepped` frames keeps the hold the same *number of frames* on any FPS. Count seconds instead if you want a fixed duration.

Pair it with:
- **Characters as solid silhouettes:** add `Highlight` instances (FillColor black or white, `FillTransparency 0`, `OutlineTransparency 1`) to the attacker and victim for the same frames. Destroy them after, because of the 255 limit [9].
- **Hide the map:** briefly set `Lighting.Ambient`/`OutdoorAmbient` to black and `Brightness` to 0 (map goes dark, Highlights stay). A 2023 DevForum thread on "advanced impact frames" describes boosting saturation via color correction and switching lighting to black or white [10].

### Step 3 — Inverted-color frames
There's no official "invert" property. Community tricks:

> [!warning] Unverified
> - Stacking two `ColorCorrectionEffect`s with values of −1 is reported to invert workspace colors (pure black and white unchanged); setting both `Contrast = -1` reportedly inverts all colors; `Saturation = -2` reportedly gives inverted hue without inverting brightness [10].
> - A `Highlight` with **negative** `FillTransparency` (e.g. −1, FillColor (127,127,127)) on a Glass part with Transparency 1 reportedly inverts what is behind it. This relies on out-of-range behavior described as a glitch and may break at any engine update [10].
> Test both in a current Studio build before shipping.

Safer alternative: a **pre-drawn impact image** (inverted silhouette art, manga burst) on a full-screen `ImageLabel` in a `ScreenGui` (`IgnoreGuiInset = true`). Show it for 2–3 frames. A DevForum resource plays an After Effects–rendered PNG sequence as an impact frame [11].

### Step 4 — Screen shake that reads as impact
- **Kick:** offset is max on frame 1 and decays exponentially within 0.15–0.3 s. "Camera kick, not wobble: full strength on the first frame, decaying fast, says impact. Long, even noise says earthquake." [5]
- `RbxCameraShaker` (EZ Camera Shake port) API: `CameraShaker.new(Enum.RenderPriority.Camera.Value + 1, function(shakeCf) camera.CFrame *= shakeCf end)`, then `:Shake(CameraShaker.Presets.Explosion)` for one-shots (Explosion = "intense and rough") or `:ShakeOnce(magnitude, roughness, fadeIn, fadeOut)` [6].
- **Don't tween `Camera.CFrame` for shake.** A DevForum thread notes TweenService locks the camera position during the tween and fights other camera code [12]. Apply the offset after the default camera in `BindToRenderStep`.
- **Distance falloff:** scale the magnitude by `1 - math.clamp(dist / radius, 0, 1)`, so only nearby players feel it [5].

| Hit tier | Magnitude (CameraShaker units) | Roughness | Fade out |
|---|---|---|---|
| M1 hit (attacker/victim only) | 0.5–1 | 8–12 | 0.15 s |
| Heavy / finisher | 2–3 | 10–15 | 0.3 s |
| Ultimate / ground slam (radius) | 4–6 | 15–20 | 0.6 s |

> [!warning] Unverified
> Magnitude and roughness numbers are starting points; check the exact `Presets` values in the module source before copying.

### Step 5 — FOV punch
```lua
local TweenService = game:GetService("TweenService")
local cam = workspace.CurrentCamera
local function fovPunch(delta: number)
	local base = 70 -- store your game's base FOV instead of reading the current one mid-tween
	cam.FieldOfView = math.clamp(base + delta, 1, 120)
	TweenService:Create(cam, TweenInfo.new(0.25, Enum.EasingStyle.Quint, Enum.EasingDirection.Out),
		{ FieldOfView = base }):Play()
end
-- fovPunch(-6)  -- zoom-in "punch" on contact; fovPunch(+10) for dash or launch
```
Very low or very high FOV is disorienting [7]. Keep punches within about ±10°. A community impact doc describes "a few degrees, easing back" [5].

### Step 6 — Speed lines
Three DevForum-documented approaches [13]:
1. **Sprite sheet on an ImageLabel:** a full-screen manga speed-line sheet. Cycle frames with `ImageRectOffset`/`ImageRectSize`.
2. **Procedural UI wedges:** one wedge image with a `UIGradient`, cloned and randomly rotated around screen center, offset so the lines don't form a perfect circle.
3. **Camera-attached ParticleEmitter:** emitter on a part CFramed to the camera each frame, disc-like emission so lines fly past the player. Tie `Rate`/`Speed` to the character's velocity magnitude.

For focus lines on a hit, use approach 1 or 2 for 3–6 frames, centered on the victim's screen position (`Camera:WorldToViewportPoint`).

### Step 7 — Hit-stop (freeze)
- Pause the attacker's and victim's AnimationTracks with `track:AdjustSpeed(0)` for 0.05–0.1 s, then restore. The cited range is ~50–100 ms [5].
- Freeze active particle emitters with `TimeScale = 0`, then restore to 1 [14].
- Keep hitboxes and server logic unfrozen. Hit-stop is a client presentation effect.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Impact frame hold | 2–4 frames | 1–few frames definition [1]; 2–3 frame flash [5] |
| Mono frame | `Saturation -1`, `Contrast 2` | Saturation −1 = full desaturation [3] |
| White-out | `Brightness 0.6–1` | 1 = all white [3] |
| FOV range | 1–120 (default 70) | Official [7] |
| FOV punch | −4 to −8° in, return 0.2–0.3 s | Community [5] (starting point) |
| Hit-stop | 0.05–0.1 s | [5] |
| Highlight cap | 255 per client | Official [9] |

## Checklist
- [ ] All screen effects are created on the client, under `Camera` or in `PlayerGui`.
- [ ] Impact frames are reserved for heavy hits or ultimates (not every M1).
- [ ] Only the attacker, victim and players within a radius get shake and flash. Bystanders get a reduced version.
- [ ] Every effect restores its exact previous values (store them first).
- [ ] Temporary Highlights are destroyed, not just disabled.
- [ ] Add a settings toggle: "Reduce screen flashes / shake" (photosensitivity and motion comfort).
- [ ] Test at 30 fps and 144 fps (frame-count vs. time-based holds).

## Common Mistakes
- **Putting ColorCorrection in Lighting from the server.** Every player in the server gets flashbanged by every fight.
- **Long shakes.** A 1 s wobble feels like an earthquake, not a punch.
- **Impact frame on every hit.** It loses meaning and becomes a seizure risk. Rapid full-screen flashing is a known photosensitivity concern, so cap flashes per second and offer a toggle.
- **Tweening Camera.CFrame for shake.** It fights the camera scripts [12].
- **Forgetting to restore FOV** when a punch is interrupted by another punch. Always tween back to a stored base, never to the "current" value.

## Related
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]
- [[Scripting and Emitting VFX]]
- [[Lighting for Anime Maps]]
- [[Toon Shading on Roblox]]

## Sources
1. Yelzkizi, "10 Mind-Blowing Anime FX Tips" (impact frame definition). https://yelzkizi.org/anime-fx-blender-after-effects-tutorial/ (practitioner blog)
2. fullfrontal.moe, "Sakuga Espresso" (Kanada: light flares, impact frames). https://fullfrontal.moe/sakuga-espresso/
3. Roblox Creator Docs, ColorCorrectionEffect reference. https://create.roblox.com/docs/reference/engine/classes/ColorCorrectionEffect (source yaml read 2026-10-31)
4. Roblox Creator Docs, "Post-processing effects" (Lighting = all players, Camera = specific player). https://create.roblox.com/docs/environment/post-processing-effects
5. EasyVFX `docs/impact.md` (hit-stop 50–100 ms, 2–3 frame flash, camera kick vs. wobble, FOV punch, distance falloff). https://github.com/VuxSussy/EasyVFX/blob/main/docs/impact.md
6. Sleitnick, RbxCameraShaker README (EZ Camera Shake port; presets; Shake/ShakeOnce/StartShake API). https://github.com/Sleitnick/RbxCameraShaker ; DevForum thread https://devforum.roblox.com/t/ez-camera-shake-ported-to-roblox/98482
7. Roblox Creator Docs, Camera.FieldOfView (clamped 1–120, default 70). https://create.roblox.com/docs/reference/engine/classes/Camera
8. Roblox Creator Docs, BloomEffect reference. https://create.roblox.com/docs/reference/engine/classes/BloomEffect
9. Roblox Creator Docs, Highlight reference (255 simultaneous limit). https://create.roblox.com/docs/reference/engine/classes/Highlight
10. DevForum: "Advanced impact frames" https://devforum.roblox.com/t/advanced-impact-frames/2468478 ; "How do i invert screen colors?" https://devforum.roblox.com/t/how-do-i-invert-screen-colors/1603778 ; "A short guide in inverting the color of specific areas in your game" https://devforum.roblox.com/t/a-short-guide-in-inverting-the-color-of-specific-areas-in-your-game/3652191 ; "Attempting to invert player colors and textures" https://devforum.roblox.com/t/attempting-to-invert-player-colors-and-textures/3093605
11. DevForum, "Feedback on impact-frame player and/or frameplayer" (After Effects PNG sequence). https://devforum.roblox.com/t/feedback-on-impact-frame-player-andor-frameplayer/3537568 ; "[Open Source] Impactframe Module" https://devforum.roblox.com/t/open-source-impactframe-module/2963136
12. DevForum, "Camera shake for combat" (TweenService locks camera position). https://devforum.roblox.com/t/camera-shake-for-combat/2317381
13. DevForum: "How would I go about making a dash/speed screen effect" https://devforum.roblox.com/t/how-would-i-go-about-making-a-dashspeed-screen-effect/1669992 ; "How to make this type of speed/wind lines based on player velocity" https://devforum.roblox.com/t/how-to-make-this-type-of-speedwind-lines-based-on-player-velocity/3560980 ; "How would I create a speed/wind effect?" https://devforum.roblox.com/t/how-would-i-create-a-speedwind-effect/959829
14. Roblox Creator Docs, ParticleEmitter.TimeScale. https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
