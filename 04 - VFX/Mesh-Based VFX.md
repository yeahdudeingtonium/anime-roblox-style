---
tags: [vfx, meshes, slashes, shockwave, tweenservice, blender]
updated: 2026-10-31
sources: 13
status: draft
---
# Mesh-Based VFX

## TL;DR
- Mesh VFX = a MeshPart (or a Part with a `SpecialMesh`) with a textured or Neon/ForceField surface, **tweened** in `Size` (or `SpecialMesh.Scale`), `CFrame` and `Transparency`. Use it for slashes, shockwave rings, spheres, pillars, tornadoes and craters. [1][2]
- Meshes give **crisp silhouettes** at any size. Particles give volume and chaos. Top effects combine them: mesh for the shape, particles for sparks and smoke. [3][4]
- Slash meshes are crescent ribbons UV-mapped so a gradient texture runs from the leading edge to the tail. Animate the reveal with a **flipbook on a particle** or by **swapping or offsetting textures**. True UV scrolling on MeshParts has no built-in property (EditableMesh is the workaround). [5][6]
- `SpecialMesh.Scale` and `VertexColor` change look **without changing the part's physics size** [7]. MeshPart `Size` tweens are simpler and work with `TextureContent`.
- Always pair expanding meshes with `Circ`/`Exponential` `Out` easing and a transparency tween that finishes **with or before** the scale tween. Destroy or return them to a pool after use. [8][9]

## Why it matters for anime battlegrounds
The big readable shapes in TSB, JJS and Heroes Battlegrounds (crescent slashes, expanding shockwave rings, domain spheres, pillars of energy, ground craters) are almost always geometry. Particles alone can't hold a clean, screen-sized crescent. A stretched 256 px texture goes blurry, while geometry rasterizes at screen resolution [3]. DevForum users note anime effects "pair Blender meshes with particle emitters", though one commenter argues particles alone suffice and are cheaper [4]. Use meshes where the **shape** is the message.

## How to do it

### Step 1 — Build the base meshes in Blender
Core kit (one each, reuse everywhere):

| Mesh | Construction | Tri budget (starting point) | UV layout |
|---|---|---|---|
| **Slash crescent** | Plane strip bent along a 120–200° arc, thicker in the middle, pinched to points at both ends | 40–200 | U along the arc (0 tail → 1 head), V across width |
| **Shockwave ring** | Flat annulus (circle, inset faces, delete center) or a short open cylinder | 64–256 | U around, V inner → outer |
| **Sphere / dome** | UV sphere, 16–24 segments, normals optionally flipped for "inside" domes | 200–800 | Standard sphere UV for scrolling noise |
| **Pillar / beam column** | Open cylinder, 16 sides, no caps | 32–64 | U around, V bottom → top |
| **Tornado / spiral** | Cone or twisted cylinder (Simple Deform: Twist) | 100–400 | V up the spiral |
| **Crater rocks** | 3–6 low-poly chunks (8–40 tris each) | 8–40 each | Box projection, tiled rock texture |

A DevForum tutorial walks through a mesh effect built from a subdivided cylinder with a Mask modifier, exported as .obj and imported as a MeshPart [5]. A commenter notes some Blender steps moved after Blender 4.2 [5]. Another DevForum tutorial makes animated slashes entirely in Blender: a deformed mesh with Voronoi and gradient shaders, rendered to PNG frames, packed into a sprite sheet and used as a **particle flipbook** [5].

> [!warning] Unverified
> The tri budgets are reasonable starting points for single-use VFX meshes, not measured from shipped battlegrounds games. See [[Top Roblox Modeler Workflow Patterns]] for import specifics.

Import notes:
- MeshParts can take one texture via `TextureContent` (`TextureID`) [2]. A mesh must be **UV-mapped** externally to show a texture [6].
- Export the texture as **RGBA PNG** so alpha cuts the shape [6].
- Set `Anchored = true`, `CanCollide = false`, `CanQuery = false`, `CanTouch = false`, `CastShadow = false`, and `Material = SmoothPlastic` (textured), `Neon` (glow core) or `ForceField` (shimmering shell).

### Step 2 — Choose a surface strategy
| Strategy | How | Pros | Cons |
|---|---|---|---|
| **Neon part** | `Material = Neon`, Color = hue, tween Transparency | Glows with Bloom, no texture needed | Flat, no internal detail |
| **ForceField material** | `Material = ForceField` on a sphere or ring | Animated shimmer for free, good for shields and domains | Look varies by `Color`; less controllable |
| **Textured MeshPart** | `TextureContent` = gradient/noise PNG, tween Transparency | Hand-drawn anime look | No built-in UV scroll |
| **SpecialMesh FileMesh** | Part + SpecialMesh with `MeshId`, `TextureId`, `VertexColor` | `Scale` tween doesn't touch part size; `VertexColor` tints [7] | Legacy-ish workflow |
| **Texture instance on faces** | `Texture` object with `OffsetStudsU/V` tweened | Real scrolling on box faces [10] | Projects per face, ugly on curved meshes |
| **EditableMesh UV shift** | Shift UVs each frame by script | True UV scrolling on curves [6] | Must enable Mesh/Image APIs; strict client memory budget [11] |

A DevForum feature request confirms scrolling textures on curved MeshParts is hard today and proposes a UV offset property. The workaround is EditableMesh UV edits [6].

### Step 3 — Animate with TweenService
Pattern for a shockwave ring (client-side):

```lua
local TweenService = game:GetService("TweenService")

local function shockwave(template: MeshPart, cf: CFrame, startSize: Vector3, endSize: Vector3, life: number)
	local ring = template:Clone()
	ring.CFrame = cf
	ring.Size = startSize
	ring.Transparency = 0
	ring.Parent = workspace.Terrain -- or a client VFX folder
	local info = TweenInfo.new(life, Enum.EasingStyle.Circ, Enum.EasingDirection.Out)
	TweenService:Create(ring, info, { Size = endSize }):Play()
	-- fade a bit faster than it grows so it never "stops" visibly
	TweenService:Create(ring, TweenInfo.new(life * 0.85, Enum.EasingStyle.Quad, Enum.EasingDirection.In),
		{ Transparency = 1 }):Play()
	task.delay(life, function() ring:Destroy() end)
end
```

Starting values for common shapes:

| Effect | Start size | End size | Life | Easing | Notes |
|---|---|---|---|---|---|
| Ground shockwave ring | (2, 0.2, 2) | (30, 0.2, 30) | 0.35 s | Circ Out | Transparency 0 → 1 Quad In |
| Air shockwave (vertical ring facing the attacker) | (1, 1, 0.1) | (18, 18, 0.1) | 0.25 s | Exponential Out | Second ring delayed 0.05 s, 70% size |
| Hit sphere flash (Neon) | 0.5 | 6 | 0.12 s | Quad Out | Transparency 0 → 1 |
| Slash crescent | 0.6× final | 1.1× final | 0.2 s | Circ Out | Also rotate +20° around the slash axis |
| Domain dome (ForceField) | 1 | 60 | 0.8 s | Back Out | Hold, then fade 0.5 s |
| Energy pillar | (4, 0, 4) | (4, 40, 4) | 0.15 s up | Exponential Out | Then shrink X/Z to 0 over 0.3 s |

> [!warning] Unverified
> These are untested design starting points, not values from TSB, JJS or any other game.

### Step 4 — Slash reveal techniques
1. **Scale + rotate + fade** the crescent (cheapest, most common).
2. **Flipbook on a particle:** render the slash animation to a 4×4 sheet and emit one particle with `Orientation = VelocityPerpendicular` or `FacingCamera`, `FlipbookMode = OneShot`, lifetime 0.2–0.3 s [5][12].
3. **Two-mesh trick:** a bright thin "edge" crescent (Neon, white) plus a wider textured body crescent, offset 0.05 s.
4. **Texture swap:** cycle `TextureContent` across 3–4 pre-uploaded frames on the crescent (stepped "on twos" look). Preload the images with `ContentProvider:PreloadAsync` to avoid blank frames.

### Step 5 — Layer with particles
Every mesh hit should get particles for chaos: sparks along the slash arc, a dust ring at the ground ring, embers off the sphere. See [[ParticleEmitter Deep Dive]] and [[Element VFX Recipes]]. The community HD comparison notes that reference anime slashes have many thin strands, a frayed dissolving tail, a hot edge, white → color → gone timing, and sparkles along the arc. A flat single-color ribbon lacks all five [13].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Physics flags | `Anchored`, no Collide/Query/Touch, no CastShadow | VFX must never affect gameplay or shadows |
| Easing (expand) | `Circ`/`Exponential` `Out` | Fast start, long glide [8] |
| Fade timing | 80–90% of scale time | Avoids a visible "stop" |
| Debris cap | `Debris:AddItem` max **1,000** objects (oldest destroyed early) | Official [9] |
| SpecialMesh `Scale` | doesn't change part size | Official [7] |

## Checklist
- [ ] Every VFX mesh is UV-mapped, has an RGBA texture or a Neon/ForceField material.
- [ ] Physics, query, touch and shadow flags are off.
- [ ] Transparency tween ends at or before the scale tween ends.
- [ ] Meshes are cloned from a template in ReplicatedStorage, client-side, and destroyed or pooled.
- [ ] Particle layers are added for sparks, dust and embers.
- [ ] Preloaded textures for any texture-swap animation.
- [ ] Tested at gameplay camera distance and on a phone.

## Common Mistakes
- **Tweening on the server.** It replicates every property change, looks choppy for others, and costs bandwidth. Tween on clients ([[Scripting and Emitting VFX]]).
- **Leaving CanQuery or CanTouch on.** VFX meshes then block raycast hitboxes or trigger Touched events.
- **CastShadow on.** Giant black shadow discs under shockwaves.
- **Linear easing.** It looks robotic and not anime.
- **One-mesh-does-all.** A single flat ribbon reads as cheap. Add an edge, a body and sparks.
- **Huge transparent spheres** filling the screen cause overdraw (see [[VFX Performance Budget]]).

## Related
- [[Beams and Trails for Anime VFX]]
- [[ParticleEmitter Deep Dive]]
- [[Creating VFX Textures]]
- [[Element VFX Recipes]]
- [[Top Roblox Modeler Workflow Patterns]]
- [[Toon Shading on Roblox]]

## Sources
1. Roblox Creator Docs, TweenService reference. https://create.roblox.com/docs/reference/engine/classes/TweenService (source yaml in Roblox/creator-docs, read 2026-10-31)
2. Roblox Creator Docs, MeshPart reference (TextureContent). https://create.roblox.com/docs/reference/engine/classes/MeshPart
3. EasyVFX `docs/sharp-vfx.md` ("Get the hard edges from geometry, not from textures"). https://github.com/VuxSussy/EasyVFX/blob/main/docs/sharp-vfx.md
4. DevForum, "how do they do these kinds of VFX? ... moon animator" (Blender meshes + particles vs. particles-only opinion). https://devforum.roblox.com/t/question-how-do-they-do-these-kinds-of-vfx-is-it-by-coding-or-animating-with-moon-animator-or-smthng/1588766
5. DevForum, "VFX Tutorial" (cylinder + Mask modifier, .obj export; Blender 4.2 note) https://devforum.roblox.com/t/vfx-tutorial-roblox/872437 ; "How to make Animated Slash Effects with only Blender!" (Voronoi/gradient shader → PNG frames → sprite sheet → particle flipbook) https://devforum.roblox.com/t/how-to-make-animated-slash-effects-with-only-blender/1794034
6. DevForum, "Scrollable textures for MeshParts" (feature request; EditableMesh UV workaround) https://devforum.roblox.com/t/scrollable-textures-for-meshparts/2820890 ; "How do I make UVs transparent in Blender?" (RGBA PNG) https://devforum.roblox.com/t/how-do-i-make-uvs-transparent-in-blender/691869
7. Roblox Creator Docs, DataModelMesh reference (Scale, Offset, VertexColor don't change part physics). https://create.roblox.com/docs/reference/engine/classes/DataModelMesh
8. EasyVFX `docs/impact.md` ("Fast in, long glide": Circ easing for slashes and shockwaves). https://github.com/VuxSussy/EasyVFX/blob/main/docs/impact.md
9. Roblox Creator Docs, Debris:AddItem (default 10 s, hardcoded max 1,000 items). https://create.roblox.com/docs/reference/engine/classes/Debris
10. Roblox Creator Docs, Texture class (OffsetStudsU/V, StudsPerTileU/V). https://create.roblox.com/docs/reference/engine/classes/Texture
11. Roblox Creator Docs, EditableMesh (must enable "Allow Mesh / Image APIs"; strict client memory budgets). https://create.roblox.com/docs/reference/engine/classes/EditableMesh
12. Roblox Creator Docs, ParticleEmitter (FlipbookMode OneShot). https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
13. EasyVFX README, "HD quality with Blender (v2)" comparison table. https://github.com/VuxSussy/EasyVFX
