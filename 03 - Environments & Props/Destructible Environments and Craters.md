---
tags: [environments, destruction, craters, debris, decals, geometryservice]
updated: 2026-10-31
sources: 14
status: draft
---
# Destructible Environments and Craters

## TL;DR
- The battlegrounds "crater" look is almost always **fake geometry**: a ring of rock Parts or MeshParts raycast-placed around the impact, colored and textured to match the hit surface, plus flying debris, plus a crack **decal**. These are then tweened away after a few seconds. This is the pattern in community TSB-style crater and rock modules.
- Real mesh destruction now exists: **`GeometryService:FragmentAsync()`** (voronoi shatter) and **`GenerateFragmentSites()`** (including localized `{Origin, Radius}`), plus `SubtractAsync`/`UnionAsync`/`IntersectAsync`/`SweepPartAsync`. CSG on meshes plus sweep and fragment are behind a **beta flag** per the solid-modeling docs.
- Solid-modeling results are capped at **20,000 triangles**, operations are **async** and should not be spammed, and client-side calls only work on **client-created** parts with no replication.
- Do VFX-level destruction (craters, debris, dust) **on each client**. Only replicate the event (position, radius, surface). Do authoritative "building broken" state on the server with **pre-fractured** models swapped in.
- Decals now support **`EmissiveMaskContent` and PBR maps** (normal maps are plugin-set), useful for glowing magma cracks. Every decal still adds draw calls.

## Why it matters for anime battlegrounds
Destruction **is** the shonen fantasy: being punched through a wall, ground splitting under an ultimate, a crater after a dive kick. TSB-inspired modules are among the most-shared DevForum resources for this genre. Done wrong, destruction is the top cause of **server lag, network spikes and mobile frame drops**. See [[Anime VFX Fundamentals]] for the impact-frame side and [[Environment Performance Budgets]] for costs.

## How to do it
### Step 1: Choose a destruction tier
| Tier | What | Where computed | Cost | Use |
|---|---|---|---|---|
| T0: Decal | Crack or scorch decal on the floor | Client | Very low (1 draw call each) | Every hit |
| T1: Fake crater | Ring of 8–20 rocks + debris + dust | Client | Low–medium | Heavy hits, slams |
| T2: Prop swap | Intact prop replaced by a pre-fractured version, pieces unanchored | Server state, client visuals | Medium | Walls, cars, poles |
| T3: Runtime CSG | `SubtractAsync` hole, `FragmentAsync` shatter | Server or client | High, async | Rare showcase moments |

### Step 2: Fake crater recipe (T1)
The recipe the community modules converge on (Rock Module, Battlegrounds crater module, Crater System by Frodev, Bezier Debris):
1. **Raycast down** from the impact point to get the surface `Position`, `Normal`, `Material`, `Color` (and MaterialVariant).
2. Spawn **N rocks in a ring** (radius R; N = 8–20) with random size (e.g. 1.5–4 studs), tilted outward 20–45° and half-buried. **Copy the surface's Material, MaterialVariant and Color**, so they read as torn-up floor.
3. Spawn **debris**: 4–12 small chunks, unanchored or tweened along Bezier arcs, raycasting their landing spot.
4. Add a **crack decal** on a thin invisible Part aligned to the normal, with a random rotation.
5. Add **dust**: a short `ParticleEmitter:Emit(n)` burst. See [[Anime VFX Fundamentals]].
6. After **3–8 s**, tween the rocks down into the ground and the decals' transparency to 1, then return the objects to a **pool** (PartCache) instead of `Destroy()`.

> [!example] Module APIs seen in community resources
> Rock Module V1.0 exposes a `Crater(centerCFrame, radius, minRocks, maxRocks, playerCollision)`-style function. Frodev's system copies the hit surface's material and color. The Battlegrounds crater module uses a raycast plus PartCache.

> [!warning] Unverified
> Rock counts, sizes and lifetimes above are typical values I inferred from module descriptions and gameplay. Each module's exact defaults weren't readable (DevForum was unreachable). Check the module before relying on numbers.

### Step 3: Prop and wall destruction (T2)
- **Pre-fracture in Blender** (Cell Fracture add-on) into 6–20 chunks. Each chunk is a MeshPart sharing **one texture or atlas**. Keep both the intact and fractured models in `ReplicatedStorage`.
- On hit (server-validated), set the intact model invisible or remove it, clone the fractured version on clients, unanchor the pieces, apply `AssemblyLinearVelocity` away from the hit, and fade them after 5–10 s.
- `CollisionFidelity = Box` on chunks keeps physics memory low. Consider a collision group so debris doesn't collide with players. Several modules expose a `PlayerCollision` flag.
- Respawn the intact prop after 30–120 s or at round end.
- Use **Atomic** streaming mode for destructible models, so client scripts see all parts at once. Note that runtime-modified models **cannot use SLIM**.

### Step 4: Runtime CSG and fragmentation (T3)
```lua
-- Localized shatter (from Roblox solid-modeling docs pattern)
local GeometryService = game:GetService("GeometryService")
local sites = GeometryService:GenerateFragmentSites(part, {Origin = hitPos, Radius = 6})
local ok, fragments = pcall(function()
	return GeometryService:FragmentAsync(part, sites)
end)
-- fragments[i].Instance; fragments[i].Index == 1 is the unshattered remainder
```
Rules from the docs:
- Inputs: Parts, PartOperations and MeshParts (meshes must be **watertight**). **Terrain is not supported.**
- Results have **no Parent**. Parent them, then `Destroy()` the original.
- Results over 20,000 tris get simplified, or the call errors.
- Fragmentation "can be massive". Clean up with `Debris` or timers. Hand-writing well-behaved sites takes 50+ lines of Luau.
- Copy `Decal`/`SurfaceAppearance` children onto the fragments yourself (the doc example does this).
- MeshPart results get white `Color` with face colors showing, and faces cut from other parts get UV `(0,0)`. Make **pixel (0,0) of your texture a sensible interior color** (for example the concrete-core grey).
- `PartOperation` results are box-mapped, which can stretch textures. Use `SmoothingAngle` 30–70°, because 90–180° causes shading artifacts.
- `MeshPart:ApplyMesh()` / `PartOperation:SubstituteGeometry()` swap geometry in place, so children (lights, emitters, decals) are kept and there is no flicker.
- Async. Don't chain many calls in quick succession.

> [!warning] Beta
> Per the solid-modeling page, "Performing CSG on meshes and using the sweep and fragment operations are only available by enabling the beta feature". Confirm the beta has graduated before shipping T3 in a live game.

### Step 5: Terrain craters
- `Terrain:FillBall(center, radius, Enum.Material.Air)` digs a real hole. Terrain is voxel-based at **4×4×4 studs**, so small craters look blobby. Use it for radius ≥ 8 studs.
- Restore it later by re-filling with the original material (store it first, for example with `ReadVoxels`).
- GeometryService does not work on Terrain.

> [!warning] Unverified
> `Terrain:FillBall`, `ReadVoxels` and `WriteVoxels` exist in the current API dump. I have not tested the save-and-restore pattern or its cost on mobile.

### Step 6: Crater and crack decals
| Property | Value | Notes |
|---|---|---|
| Texture | 512² or 1024² crack/scorch with alpha | 3–5 variants on one atlas, picked with `UVOffset`/`UVScale` |
| `Decal.Color3` | Darker multiply tint | Match the floor |
| `EmissiveMaskContent` | Mask of the crack lines | Magma or energy cracks (Gojo/Sukuna-style) |
| `EmissiveStrength` | 1 → tween to 0 over 2 s | Cooling glow. Large values clamp to white |
| `ZIndex` | Higher than the floor decals | Draw order on the same face |
| `Transparency` | Tween 0 → 1 at the end of life | Fade out |

Decals "don't batch well" and add draw calls. **Cap concurrent crater decals** (e.g. 30) and recycle the oldest.

### Step 7: Networking pattern
- Server: validate the hit, then fire **one** `RemoteEvent` to all clients: `{pos, normal, radius, surfaceMaterial, surfaceColor, seed}`.
- Clients: spawn rocks, debris and decals locally using the **seed**, so every client sees the same pattern.
- Never create hundreds of server Parts per hit. Replication and physics ownership of debris are the classic lag source.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Solid-model result cap | 20,000 tris | Solid-modeling docs |
| SmoothingAngle | 30–70° good; 90–180° not recommended | Docs |
| Terrain voxel | 4 studs | Terrain docs |
| Rocks per crater | 8–20 | Typical (unverified) |
| Crater lifetime | 3–8 s | Typical (unverified) |
| Concurrent crater decals | ≤30 | Proposal (unverified) |

## Checklist
- [ ] All crater visuals client-side, seeded, pooled.
- [ ] Rocks copy the surface material, variant and color via raycast.
- [ ] A decal cap with recycling.
- [ ] Pre-fractured props share one texture. Chunks use Box collision.
- [ ] Destructibles placed where knockback lands (see [[Battleground Arena Map Design]]).
- [ ] Respawn timers for broken props.
- [ ] Runtime CSG gated behind a feature flag until the beta status is confirmed.

## Common Mistakes
- Server-spawned debris for every punch, causing replication storms and server FPS drops.
- `Destroy()`/`Instance.new` every hit instead of pooling, which churns the GC.
- Crater rocks in default grey on a red brick floor, which reads as fake.
- Unbounded FragmentAsync pieces that never get cleaned up.
- Using SLIM on destructible models. Runtime changes break SLIM rendering.

## Related
- [[Anime VFX Fundamentals]]
- [[Battleground Arena Map Design]]
- [[Stylized Trees, Foliage and Rocks]]
- [[Environment Performance Budgets]]
- [[Stylized Environment Kits]]

## Sources
1. Solid modeling (in-game ops, fragment, beta, results rules): https://create.roblox.com/docs/parts/solid-modeling
2. GeometryService class: https://create.roblox.com/docs/reference/engine/classes/GeometryService
3. Decal class (emissive, UV, ZIndex): https://create.roblox.com/docs/reference/engine/classes/Decal
4. Improve performance (decals don't batch, collision fidelity): https://create.roblox.com/docs/performance-optimization/improve
5. Streaming techniques (SLIM static-only, atomic models): https://create.roblox.com/docs/workspace/streaming/techniques
6. Terrain (4-stud voxels): https://create.roblox.com/docs/parts/terrain
7. DevForum: Battlegrounds crater module (raycast + PartCache): https://devforum.roblox.com/t/battlegrounds-crater-module/3370194
8. DevForum: Rock Module V.1.0 – Craters, Explosions: https://devforum.roblox.com/t/rock-module-v10-craters-explosions-and-more-effects/3041562
9. DevForum: 'Punch' Rock Module inspired by TSB: https://devforum.roblox.com/t/punch-rock-module-inspired-by-tsb/3171422
10. DevForum: Bezier Debris 1.0: https://devforum.roblox.com/t/bezier-debris-10/4755754
11. DevForum: Crater system by Frodev (copies surface material/color): https://devforum.roblox.com/t/crater-system-by-frodev/2628508
12. DevForum: Rocks Module – Useful for Anime Games Skill Effects: https://devforum.roblox.com/t/rocks-module-useful-for-anime-games-skill-effects/1687374
13. DevForum: How to make cool rocks stuff like GPO: https://devforum.roblox.com/t/how-to-make-cool-rocks-stuff-like-gpo/1457410
14. DevForum: How do I create this Crater/Rock effect?: https://devforum.roblox.com/t/how-do-i-create-this-craterrock-effect/2796810
