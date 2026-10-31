---
tags: [vfx, beams, trails, attachments, slashes, lightning, roblox-api]
updated: 2026-10-31
sources: 8
status: draft
---
# Beams and Trails for Anime VFX

## TL;DR
- **Beam** = a textured ribbon between two Attachments along a **cubic Bézier** (`CurveSize0/1` + attachment orientation). Use it for energy beams, lasers, lightning segments, arcs and rings. [1][2]
- **Trail** = a ribbon recorded behind two moving Attachments, every frame. Use it for sword slashes, dash streaks and projectile tails. **Lifetime 0.01–20 s (default 2)**. [3][4]
- Both share `LightEmission` (0 normal → 1 additive), `LightInfluence` (0–1), `Brightness` (**0–10000, default 1**), `FaceCamera`, `TextureMode` (Stretch / Wrap / Static) and `TextureLength`. [1][3]
- Beams have `Segments` (**default 10**). A Color/Transparency sequence with *n* keypoints needs **at least n−1 segments**. `TextureSpeed` (**default 1**) scrolls the texture for flowing energy for free. [1]
- Chained beams with `FaceCamera = true` show notches at joints. For one continuous stroke, use **one curved beam** (arc up to ~200°). For chains, orient shared attachments to face the camera yourself. [5]

## Why it matters for anime battlegrounds
Slashes, kamehameha-style beams, lightning and dash streaks are signature moves of the genre. Beams and Trails are **geometry**, so their edges rasterize at screen resolution and stay sharp at any distance, unlike a stretched particle texture [5]. They're cheap: one instance draws a whole ribbon.

## How to do it

### Step 1 — Attachments (the anchor for everything)
Attachments define the start and end of beams and the edges of trails. Key properties (current API) [6]:

| Property | Notes |
|---|---|
| `Position` / `CFrame` | Offset in the parent's local space (parent: BasePart, Bone or Attachment) |
| `Orientation` | Local rotation, Z-X-Y order. **Beam curves bend along the attachment's X axis** [1] |
| `Axis` / `SecondaryAxis` | Unit X and Y axes (defaults (1,0,0) and (0,1,0)). Kept orthogonal automatically |
| `WorldPosition` / `WorldCFrame` / `WorldAxis` | World-space equivalents. Settable, converted to local |
| `Visible` | Renders a small green sphere in-game (debugging). Default false |

Tips:
- Attach VFX attachments to **Bones or Motor6D-driven parts** (the weapon or hand) so they follow animations.
- Turn on **Show Constraint Details** in Studio's View menu to see attachments while authoring [2][4].

### Step 2 — Beams: properties that matter
From the API reference [1]:

| Property | Type / range | Use |
|---|---|---|
| `Attachment0` / `Attachment1` | Attachment | Both must descend from Workspace for the beam to render |
| `Width0` / `Width1` | studs (negatives clamp to 0) | Taper: 0 at the tip → wide at the source |
| `CurveSize0` / `CurveSize1` | studs | Bézier handles: P1 = A0 + CurveSize0 × A0's +X; P2 = A1 − CurveSize1 × A1's X |
| `Segments` | int, default 10 | More = smoother curve. Need ≥ n−1 for n sequence keypoints |
| `Texture`, `TextureMode`, `TextureLength` | | Wrap/Static: repeats = length ÷ TextureLength. Stretch: repeats TextureLength times [2] |
| `TextureSpeed` | float, default 1 (cycles/s, + = A0→A1, − reverses) | Flowing energy, scrolling lightning |
| `SetTextureOffset(offset)` | 0–1 | Reset or sync the scroll |
| `Color` | ColorSequence along the length | White core at the source → hue at the tip |
| `Transparency` | NumberSequence along the length | Fade both ends to hide hard cutoffs |
| `LightEmission` | 0–1 | 1 for energy |
| `LightInfluence` | 0–1 | 0 for self-lit |
| `Brightness` | 0–10000, default 1 | Active when LightInfluence < 1. 2–5 with Bloom |
| `FaceCamera` | bool | Always faces camera (good for single straight beams) |
| `ZOffset` | studs | Separates stacked beams between the same attachments (avoids z-fighting) |
| `Enabled` | bool | Show/hide |

**Circle-arc trick:** a cubic Bézier approximates a circular arc of angle θ and radius r when each handle length is `4/3 · tan(θ/4) · r` along the tangent. That gives about 0.5523·r for a 90° arc, and one beam stays within ~2% of a circle up to a semicircle [5]. Four beams make a full ring (shockwave), with each attachment's X axis along the tangent.

### Step 3 — Trails: properties that matter
From the API reference [3]:

| Property | Range / default | Use |
|---|---|---|
| `Attachment0` / `Attachment1` | | Width of the trail = distance between them |
| `Lifetime` | 0.01–20 s, default 2 | **Slashes: 0.1–0.25 s.** Shorter = snappier, shorter trail [4] |
| `WidthScale` | NumberSequence 0–1 over lifetime | Taper the tail: 1 → 0 |
| `MinLength` | studs | No new segment until attachments move this far |
| `MaxLength` | studs, default 0 (unlimited) | Cap trail length on fast dashes |
| `Color` / `Transparency` | sequences over segment lifetime | White → hue, 0 → 1 |
| `TextureMode` | Stretch / Wrap / Static | **Stretch**: texture stretches with lifetime, shrinks when stopped (slashes). **Wrap**: tiles, stationary relative to attachments. **Static**: "stamped" in world (footprints, tire tracks) [4] |
| `TextureLength` | | Per mode, as above |
| `FaceCamera` | bool | Usually **false** for blade slashes (keep the blade plane) |
| `LightEmission` / `LightInfluence` / `Brightness` | 0–1 / 0–1 / 0–10000 | Same as beams |
| `Enabled` + `Clear()` | | Disable stops new segments; `Clear()` wipes existing ones immediately |

Changing a trail's attachments while it's drawing removes all drawn segments [3].

### Step 4 — Recipe: sword slash trail
1. Two attachments on the blade: `Base` at the guard, `Tip` at the point (distance = trail width).
2. Trail (a short-lifetime trail on the blade is the standard community approach [8]): `Lifetime 0.15`, `FaceCamera false`, `LightEmission 1`, `LightInfluence 0`, `Brightness 2`.
3. `Transparency`: (0, 0) → (0.6, 0.4) → (1, 1). `WidthScale`: (0, 1) → (1, 0.2).
4. `Color`: (0, white) → (0.3, main hue) → (1, dark hue).
5. Texture: a horizontal gradient strip with a bright leading edge, `TextureMode = Stretch`, `TextureLength = 1`.
6. Script: `trail.Enabled = true` on the animation's swing start marker, `false` on the swing end marker (see [[Scripting and Emitting VFX]]).
7. Layer a slash **mesh** or curved Beam on the impact frame for the crisp crescent (see [[Mesh-Based VFX]]). The trail alone looks soft at low frame rates, because segments are recorded per frame [3].

### Step 5 — Recipe: energy beam (kamehameha-style)
Layer three beams between the same two attachments (hand → target), each with a different `ZOffset` [1]:

| Layer | Width0/1 | Texture / speed | Color | Notes |
|---|---|---|---|---|
| Core | 1.5 / 1.5 | Soft horizontal gradient, `TextureSpeed 0` | White | `ZOffset 0.2`, `Brightness 3` |
| Body | 4 / 4 | Noise streaks, `TextureSpeed 2–4` | Main hue | `ZOffset 0` |
| Outer swirl | 6 / 5 | Spiral streaks, `TextureSpeed −1.5` | Hue, transparency 0.5 | `ZOffset −0.2` |

Add a charge sphere at the source and an impact burst at the end ([[Mesh-Based VFX]], [[ParticleEmitter Deep Dive]]). Tween `Width0/1` from 0 → full in 0.08 s on fire, and back to 0 over 0.2 s on end. Raycast each frame to move the end attachment to the hit point.

### Step 6 — Recipe: lightning with beams
Two proven approaches:
- **Procedural:** create N attachments along the path, offset each randomly perpendicular to the path, and connect them with beams. Re-randomize every ~0.05 s (about 3 frames at 60 fps) and flicker transparency. A community tool uses exactly this "zig-zag that reshapes every ~0.05 s and flickers" [5]. Use miter joints (average tangent at corners) to avoid overlaps [5].
- **Module:** the DevForum "Lightning Beams" module (v1.1) does Perlin-noise lightning along a Bézier, with sparks and explosion sub-modules. It's **client-sided only**, so fire a RemoteEvent to clients [7].

Beam settings for each bolt segment (starting point): `Width0 0.4`, `Width1 0.4`, `LightEmission 1`, `LightInfluence 0`, `Brightness 4`, `Color` white core, plus a second wider beam (`Width 1.2`, hue (120, 200, 255), transparency 0.4) on the same attachments with `ZOffset −0.1`.

```lua
-- Minimal jittered bolt (client). a0..aN are Attachments in a folder under workspace.Terrain
local function reshape(points, startPos, endPos, jitter)
	local dir = endPos - startPos
	local n = #points
	local side = dir:Cross(Vector3.yAxis).Unit
	if side ~= side then side = Vector3.xAxis end -- NaN guard when dir is vertical
	local up = side:Cross(dir).Unit
	for i, att in ipairs(points) do
		local t = (i - 1) / (n - 1)
		local offset = (i == 1 or i == n) and Vector3.zero
			or side * (math.random() - 0.5) * jitter + up * (math.random() - 0.5) * jitter
		att.WorldPosition = startPos + dir * t + offset
	end
end
```

### Step 7 — Avoid joint notches on chained beams
With `FaceCamera = true`, each beam turns toward the camera on its own, so neighbors disagree at the shared attachment and show a notch [5]. Fix it this way: set `FaceCamera = false`, and each frame orient every shared attachment with X = path tangent and Y = tangent × (camera − point) [5]. Give each segment its slice of one overall gradient instead of restarting `ColorSequence` per segment [5].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Trail Lifetime range | 0.01–20 s (default 2) | Official [3] |
| Beam/Trail Brightness | 0–10000 (default 1) | Official [1][3] |
| Beam Segments | default 10; ≥ n−1 for n keypoints | Official [1] |
| Beam TextureSpeed | default 1 cycle/s | Official [1] |
| Slash trail lifetime | 0.1–0.25 s | Snappy (starting point) |
| Bolt reshape interval | ~0.05 s | Community practice [5] |
| Bézier arc handle | 4/3·tan(θ/4)·r | Circle approximation [5] |

> [!warning] Unverified
> Slash lifetime and the energy-beam widths are starting points, not measured from a specific game.

## Checklist
- [ ] Attachments are parented to animated bones or parts, not to the root.
- [ ] Slash trails: `FaceCamera false`, `Lifetime ≤ 0.25`, taper with `WidthScale`.
- [ ] Beams with multi-keypoint sequences have enough `Segments`.
- [ ] Stacked beams on the same attachments use different `ZOffset`.
- [ ] Energy beams use `TextureSpeed` instead of script-driven offset updates.
- [ ] Lightning re-randomizes every 2–4 frames and is created client-side.
- [ ] `trail:Clear()` is called when teleporting or dashing to stop long smears across the map.

## Common Mistakes
- **Trail smears after a teleport or dash.** Call `Clear()`, or disable the trail before the CFrame jump.
- **Trails on low-FPS clients look polygonal.** Segments are per frame. Back up big slashes with a mesh or curved beam.
- **Beam invisible.** One attachment isn't a descendant of Workspace [1], or the texture hasn't loaded (then it renders as a solid line [1]).
- **Gradient banding on chained beams.** Each segment restarts its gradient [5].
- **Using Wrap mode for slashes.** The texture stays stationary relative to the attachments and doesn't stretch with the swing [4].

## Related
- [[ParticleEmitter Deep Dive]]
- [[Mesh-Based VFX]]
- [[Element VFX Recipes]]
- [[Scripting and Emitting VFX]]
- [[Anime Combat Animation Timing]]
- [[Anime VFX Fundamentals]]

## Sources
1. Roblox Creator Docs, Beam class reference (Brightness 0–10000 default 1, Segments default 10 / n−1 rule, TextureSpeed default 1, CurveSize, ZOffset, SetTextureOffset). https://create.roblox.com/docs/reference/engine/classes/Beam — source https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/Beam.yaml (read 2026-10-31)
2. Roblox Creator Docs, "Beams" guide (TextureMode math, Bézier P0–P3, Show Constraint Details). https://create.roblox.com/docs/effects/beams
3. Roblox Creator Docs, Trail class reference (Lifetime 0.01–20 default 2, WidthScale, Min/MaxLength, Clear). https://create.roblox.com/docs/reference/engine/classes/Trail — source https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/Trail.yaml
4. Roblox Creator Docs, "Trails" guide (TextureMode movement behavior, lifetime shortening). https://create.roblox.com/docs/effects/trails
5. EasyVFX `docs/sharp-vfx.md` (one curved beam per stroke, 4/3·tan(θ/4)·r, FaceCamera notches, camera-facing shared attachments, miter joints, gradient slices, ~0.05 s bolt reshape). https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
6. Roblox Creator Docs, Attachment class reference. https://create.roblox.com/docs/reference/engine/classes/Attachment — source https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/Attachment.yaml
7. DevForum, "[Effect] v1.1 Lightning Beams: Seamless, smooth and procedurally animated with beam-like properties". https://devforum.roblox.com/t/effect-v11-lightning-beams-seamless-smooth-and-procedurally-animated-with-beam-like-properties/843534
8. Kitsblox, "How to Add Visual Effects to Your Roblox Game" (trail slash with short lifetime; Width0/Width1). https://kitsblox.com/blog/how-to-add-visual-effects-roblox
