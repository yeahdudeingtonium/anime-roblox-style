---
tags: [camera, cutscene, shake, fov, ultimates, game-feel]
updated: 2026-10-31
sources: 9
status: draft
---
# Camera Work for Abilities

## TL;DR
- Four camera tools, from cheap to expensive: **shake** (every hit), **FOV punch** (skills/dashes), **offset/zoom nudge** (skills), and a **Scriptable cutscene camera** (ultimates, grabs, awakenings).
- `Camera.FieldOfView` is vertical, **clamped 1–120°, default 70°**. Anime "punch-in": 70 → 85–95 over 0.05–0.1 s, back over 0.25–0.4 s.
- Shake with Sleitnick's **RbxCameraShaker** (an EZ Camera Shake port, MIT). Presets: `Bump` = (magnitude 2.5, roughness 4, fadeIn 0.1, fadeOut 0.75), `Explosion` = (5, 10, 0, 1.5). Apply it as a CFrame *offset after* the base camera.
- Cutscene cameras: set `CameraType = Scriptable`, drive CFrame from **baked frames relative to the attacker's root CFrame**, then restore the old type and subject. The camera is **local only**, so every client runs its own copy.
- Keep ultimate cutscenes **short (≈1.5–4 s)** and let *non-targeted* players keep their gameplay camera (see [[Ultimate and Awakening Sequences]]).

## Why it matters for anime battlegrounds
Anime action is half camera: whip pans, push-ins, Dutch angles, impact zooms. Battlegrounds ultimates lean hardest on cinematic cameras. Cheap per-hit shake and FOV punches make the M1 loop feel strong without taking control away.

## How to do it
### Step 1: Shake (per hit)
RbxCameraShaker usage (README/source):
```lua
local CameraShaker = require(ReplicatedStorage.CameraShaker)
local camera = workspace.CurrentCamera
local shaker = CameraShaker.new(Enum.RenderPriority.Camera.Value + 1, function(shakeCf)
    camera.CFrame = camera.CFrame * shakeCf
end)
shaker:Start()
shaker:Shake(CameraShaker.Presets.Bump)        -- one-shot
-- custom: CameraShakeInstance.new(magnitude, roughness, fadeInTime, fadeOutTime)
shaker:ShakeOnce(1.2, 8, 0, 0.25)              -- light M1 hit (my values)
```

Preset values from the module source:
| Preset | Magnitude | Roughness | FadeIn | FadeOut | PosInfluence | RotInfluence | Type |
|---|---|---|---|---|---|---|---|
| Bump | 2.5 | 4 | 0.1 | 0.75 | 0.15 all | 1,1,1 | one-shot |
| Explosion | 5 | 10 | 0 | 1.5 | 0.25 all | 4,1,1 | one-shot |
| Earthquake | 0.6 | 3.5 | 2 | 10 | 0.25 all | 1,1,4 | sustained |
| BadTrip | 10 | 0.15 | 5 | 10 | 0,0,0.15 | 2,1,4 | sustained |
| HandheldCamera | 1 | 0.25 | 5 | 10 | 0 | 1,0.5,0.5 | sustained |
| Vibration | 0.4 | 20 | 2 | 2 | 0,0.15,0 | 1.25,0,4 | sustained |
| RoughDriving | 1 | 2 | 1 | 1 | 0 | 1,1,1 | sustained |

Battlegrounds mapping (my starting points):
| Event | Shake | Notes |
|---|---|---|
| M1 1–3 (attacker & victim only) | ShakeOnce(0.8–1.5, 8–12, 0, 0.15–0.25) | Very short; high roughness = crisp |
| M1 4 / finisher | ShakeOnce(2–3, 8, 0, 0.4) | Near `Bump` |
| Downslam / wall slam | `Bump` or ShakeOnce(3, 10, 0, 0.6) | |
| Ultimate final hit | `Explosion` | Pair with an impact frame |
| Awakening transformation | `Earthquake` sustained → StartFadeOut(1) | |
| Bystanders within 30–60 studs | Scale magnitude by distance falloff | Don't shake the whole server |

> [!warning] Forum reports
> Users report `Bump` ranging "from light shaking to rocking the whole screen", and some call the module outdated. Tune the values. Never ship presets blind.

### Step 2: FOV punch
```lua
local TweenService = game:GetService("TweenService")
local function fovPunch(peak: number, inTime: number, outTime: number)
    local base = 70
    local camera = workspace.CurrentCamera
    TweenService:Create(camera, TweenInfo.new(inTime, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {FieldOfView = peak}):Play()
    task.delay(inTime, function()
        TweenService:Create(camera, TweenInfo.new(outTime, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut), {FieldOfView = base}):Play()
    end)
end
-- dash: fovPunch(82, 0.06, 0.3)   finisher: fovPunch(88, 0.05, 0.35)
```
- **Wider FOV = speed and impact.** **Narrower (50–60°) = weight and drama** (ultimate pose holds).
- Docs warn that very low or high FOVs disorient players. Stay within roughly 50–100° in gameplay.

### Step 3: Cutscene camera (ultimates, grabs)
1. Author in Moon Animator 2 with the attacker at a known origin, then export the camera (`FOV`, `Frames`, `Settings` folders). See [[Moon Animator 2 vs Blender vs Animation Editor]].
2. Convert to a baked table: `{ {t=0, cf=CFrame, fov=70}, ... }` stored **relative to the attacker's HumanoidRootPart**.
3. Playback (client):
```lua
local prevType, prevSubject = camera.CameraType, camera.CameraSubject
camera.CameraType = Enum.CameraType.Scriptable
local root = attacker.HumanoidRootPart
local t0 = os.clock()
local conn
conn = RunService.RenderStepped:Connect(function()
    local t = (os.clock() - t0) * timeScale            -- timeScale lets hitstop/slow-mo work
    local f = sampleFrames(frames, t)                  -- lerp between baked samples (or step for anime cuts)
    if not f then
        conn:Disconnect()
        camera.CameraType, camera.CameraSubject = prevType, prevSubject
        return
    end
    camera.CFrame = root.CFrame * f.cf
    camera.FieldOfView = f.fov
end)
```
4. **Hard cuts are anime.** Don't interpolate between shots. Step to the next shot's CFrame (a cut), then ease *within* the shot.
5. Lock the root CFrame at cutscene start (cache it) if the attacker moves during the ultimate, unless you want the camera to follow.
6. `Camera:Interpolate()` exists but tweens linearly. Use your own baked sampler or TweenService for eased moves.

### Step 4: Shot grammar for a 3-second ultimate
| Shot | Duration | Camera | FOV |
|---|---|---|---|
| 1. Wind-up close-up (face/eyes) | 0.4–0.6 s | 3 studs from face, slight low angle | 40–55 |
| 2. Charge wide | 0.5–0.8 s | Orbit 90° around attacker | 70 |
| 3. Strike (foreshortened fist) | 0.2–0.4 s | Behind victim looking at attacker, or fist-toward-lens | 85–100 |
| 4. Impact frame | 0.05–0.15 s | Freeze; invert colours/black frame | same |
| 5. Aftermath wide | 0.6–1.0 s | Pull back + `Explosion` shake | 70→60 |
| 6. Return | 0.2–0.3 s | Blend back to gameplay camera | 70 |

> [!warning] Unverified
> These shot lengths are my recommendations based on anime cut pacing. They are not frame-counted from a specific battlegrounds ultimate.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| FOV default / clamp | 70° / 1–120° | Camera docs |
| Dash FOV punch | 70→80–84, in 0.06 s, out 0.3 s | Speed (recommendation) |
| Finisher FOV punch | 70→86–90, in 0.05 s, out 0.35 s | Impact (recommendation) |
| Shake bind priority | `RenderPriority.Camera + 1` | Apply after the default camera |
| `Bump` | 2.5, 4, 0.1, 0.75 | Module source |
| `Explosion` | 5, 10, 0, 1.5 | Module source |
| Cutscene length | 1.5–4 s | Keeps the match flowing |

## Checklist
- [ ] Shake applied as an offset after the camera update (bind priority > Camera)
- [ ] Shake magnitude falls off with distance from the impact
- [ ] FOV always returns to base, even if the move is interrupted (reset on stun/death)
- [ ] Cutscene camera restores CameraType + CameraSubject on end **and** on cancel
- [ ] Cutscene frames are relative to the attacker's root CFrame
- [ ] Settings toggle for "reduce camera shake" (accessibility)

## Common Mistakes
- Setting `camera.CFrame` without `Scriptable`, so the default camera fights it (flicker).
- Absolute world-space camera keys from Moon, so the camera flies to the sky.
- Tween-based cutscenes that drift with frame rate.
- Shaking every player in the server for every M1.
- FOV tween stacking (spamming dashes ratchets FOV upward). Always tween to an absolute base.

## Related
- [[Ultimate and Awakening Sequences]]
- [[Hitstop, Hit Reactions and Knockback]]
- [[Moon Animator 2 vs Blender vs Animation Editor]]
- [[Anime Posing and Smears on Roblox]]
- [[Anime VFX Fundamentals]]

## Sources
1. Roblox Creator Docs: Camera class (FieldOfView 1–120 default 70; Scriptable; Interpolate linear). https://create.roblox.com/docs/reference/engine/classes/Camera
2. Sleitnick/RbxCameraShaker: CameraShakePresets.lua (preset values). https://github.com/Sleitnick/RbxCameraShaker/blob/master/src/CameraShaker/CameraShakePresets.lua
3. Sleitnick/RbxCameraShaker: CameraShakeInstance.lua (constructor signature). https://github.com/Sleitnick/RbxCameraShaker/blob/master/src/CameraShaker/CameraShakeInstance.lua
4. DevForum: "EZ Camera Shake ported to Roblox". https://devforum.roblox.com/t/ez-camera-shake-ported-to-roblox/98482
5. DevForum: "Moon Animator: How do I export and import the camera?". https://devforum.roblox.com/t/moon-animator-how-do-i-export-and-import-the-camera/1717989
6. DevForum: "Moon Animator 2 Camera Animation Scripting" (relative-to-character fix). https://devforum.roblox.com/t/moon-animator-2-camera-animation-scripting/2427795
7. DevForum: "Frame animation function built around Moon Animator 2" (Scriptable, restore type). https://devforum.roblox.com/t/frame-animation-function-built-around-moon-animator-2/4214289
8. Game Developer: Vlambeer co-founder (Jan Willem Nijman) on action-game feel / "The Art of Screenshake". https://gamedeveloper.com/design/vlambeer-co-founder-shares-advice-on-building-better-action-games
9. Source Gaming: Sakurai on hitstop (camera distance and vibration relate to hitstop). https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/
