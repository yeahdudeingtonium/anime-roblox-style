---
tags: [characters, npc, boss, performance, silhouette, scale]
updated: 2026-10-31
sources: 13
status: draft
---
# NPC and Boss Characters

> [!info] How this was researched
> Performance and engine facts come from the Roblox creator-docs source repo and API reference (`main`, 2026-10-31). create.roblox.com was unreachable from the research session. Budgets marked "recommendation" are mine, derived from those rules, not Roblox numbers.

## TL;DR
- **Humanoids are expensive.** Roblox recommends **AnimationController** (no Humanoid) for static NPCs, custom movement + AnimationController for simple mobs, **disabling unused HumanoidStateTypes**, **playing NPC animations on the client**, **pooling** NPCs and **spawning only near players**. [1]
- **Instancing** collapses identical meshes into one draw call when they share the same **MeshContent** and identical **SurfaceAppearance** (or identical TextureContent). Build mob crowds from **one shared mesh + texture**, with variety through `SurfaceAppearance.Color` tint. [1][2]
- **SLIM** (Roblox's 2026 auto-LOD) **does not help Humanoid NPCs**: model SLIM excludes models containing a Humanoid, and SLIM avatars only cover R15 player characters. NPCs and custom proportions fall back to normal rendering. [3]
- Bosses aren't bound by avatar limits: any rig, any size (scale with `Model:ScaleTo`), up to **20k tris per mesh** across several meshes. Readability comes from **silhouette at 60–100 studs**, glowing weak points (EmissiveMask), and big, slow anticipation. [4][5][2]
- Avoid **frequent respawns of skinned/Humanoid models**, and especially layered clothing. Roblox flags `updateInvalidatedFastClusters` **> 4 ms** in the MicroProfiler. [1]

## Why it matters for anime battlegrounds
Battlegrounds games are mostly PvP but lean on NPCs for **training dummies**, **story/raid bosses** (curse-user bosses, Titan-style giants), **summons** (shikigami, stands, clones) and **lobby characters**. Summons and clone techniques (e.g. shadow clones) can spawn 5–20 extra characters in one move, on a server already running 16 players' VFX. NPC cost is a gameplay-design constraint, not just an art one.

## How to do it

### Step 1: Classify every NPC
| Class | Examples | Rig & components | Tri budget (recommendation) | Texture |
|---|---|---|---|---|
| **Lobby / static** | Shopkeeper, quest giver, statue of a past champion | Model + **AnimationController** + Animator, anchored, no Humanoid [1][6] | 3–6k | 512² shared |
| **Training dummy** | Combo practice target | Humanoid needed for health/damage, most states disabled [1] | 1–3k | 256² |
| **Mob / summon** | Cursed spirits, clones, shikigami | AnimationController + custom movement, or a stripped Humanoid; client-side animation [1] | 1.5–4k | Shared atlas, tinted |
| **Boss** | Raid boss, story antagonist | Custom skinned rig, Humanoid or custom controller | 10–20k per mesh, up to about 40k total | 1–2 × 1024² |
| **Cutscene-only** | Ultimate cinematic stand-ins | Client-only Model, AnimationController, destroyed after | Hero quality | Hero quality |

### Step 2: Silhouette and scale (art)
- **Player-scale NPCs:** keep them within about ±15% of player height so hitboxes and animations (grabs, throws) line up. Roblox avatar bodies run **4–10 studs tall** by spec, so check your extremes. [7]
- **Bosses:** 2×–6× player height (roughly 10–30 studs). Above that, the camera can't frame both the boss and the player without custom camera work.
- Read test: render the boss as **pure black at 60–100 studs** (Studio camera, fog off). The pose, the head and the weapon must read from shape alone. See [[Shonen Anime Shape Language]].
- **Telegraph surfaces:** put attack-telegraph glow on dedicated EmissiveMask regions (eyes, mouth, weapon edge) and ramp `EmissiveStrength` from a script before big attacks. Emissive properties are script-writable. [2][8]
- Scale an imported boss with **`Model:ScaleTo(factor)`** (scales parts and positions around the pivot relative to the original scale 1). Easier than re-exporting from Blender. [5]

### Step 3: Geometry and LOD
- `RenderFidelity = Automatic`: full detail < 250 studs, medium 250–500, lowest > 500. Bosses are often seen at 100–300 studs, so check the medium LOD looks acceptable. [9]
- Avoid `RenderFidelity.Precise` on many meshes. Roblox calls this out as a common cost. [1]
- Collision: NPC visual MeshParts → **`CollisionFidelity = Box`** (or `CanCollide` off) with simple invisible hitbox parts. Box has the lowest memory overhead. [1]
- Bosses over 20k tris: split by body region (head, torso, each arm, legs, weapon), each its own skinned MeshPart sharing **one armature**. [4]
> [!warning] Unverified
> Splitting a skinned character into multiple MeshParts that share one bone hierarchy (vs one Bone set per MeshPart) behaves differently depending on how bones are parented on import. Test with a 2-part split first.

### Step 4: Runtime performance patterns
1. **Client-side animation:** create the Animator on the client and play NPC animations locally. This cuts server load and replication, and you can skip animating far-away NPCs. [1]
2. **Disable Humanoid states** you don't need: `Humanoid:SetStateEnabled(Enum.HumanoidStateType.Climbing, false)`, likewise Swimming, Seated, etc. [1]
3. **Pool**: send defeated NPCs to an inactive pool and reactivate them instead of `Destroy()` + clone. Fewer avatar instantiations means fewer FastCluster rebuilds. [1]
4. **Proximity spawning**: spawn mobs when players are near, cull when they leave. [1]
5. **Don't touch the avatar hierarchy after spawn**: attach VFX parts *outside* the character Model, and for procedural motion write **`Motor6D.Transform`** (or `AnimationConstraint.Transform`) instead of C0/C1. [1][10]
6. **Avoid size/scale changes during gameplay**: they rebuild FastClusters. Do boss "growth" phases with a pre-scaled second model or with VFX, not a live `ScaleTo` mid-fight. [1]
7. Bones' transforms are **not replicated**, so procedural bone motion (tails, capes) must run on each client anyway. [11]

### Step 5: Draw-call budget for crowds
- Same mesh + identical SurfaceAppearance → **one instanced draw call**. Different textures per clone → separate calls. [1]
- Prefer **SurfaceAppearance.Color tint** for variety (it doesn't change the map, so it should keep instancing).
> [!warning] Unverified
> Whether differing `SurfaceAppearance.Color` tints still count as "identical SurfaceAppearances" for instancing. Verify with Render Stats (Shift+F2) draw-call counts. [1]
- Check **Render Stats → Timing** (Shift+F2) for draw calls with 20 summons on screen. [1]

### Step 6: Bosses as characters (design notes)
- **Weak points and phases:** model phase-2 damage (cracked armour, exposed core) as **separate meshes toggled by Transparency**, not as live mesh edits.
- **Readable wind-ups:** boss attacks need longer anticipation than player attacks (see [[Anime Combat Animation Timing]]). Make the rig able to *exaggerate*: extra spine bones and a long neck/tail chain.
- **Rig choice:** Custom rig plus Adaptive Animation mapping if you want to reuse R15 locomotion for humanoid bosses; a pure custom rig for monsters. See [[Roblox Character Rigs R6 vs R15 vs Custom]]. [12]

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Max tris per mesh | 20,000 | [4] |
| RenderFidelity Automatic bands | < 250 / 250–500 / > 500 studs | [9] |
| FastCluster red flag | `updateInvalidatedFastClusters` > 4 ms | [1] |
| Avatar body height range (spec) | 4–10 studs | [7] |
| Boss height | 10–30 studs | Recommendation |
| Mob tris | 1.5–4k | Recommendation |
| Boss tris | 10–20k per mesh | Recommendation within the [4] cap |
| Mob textures | Shared 256–512² atlas | Instancing [1] |
| SLIM coverage | R15 *player* avatars and static Models only | [3] |
| Collision fidelity for NPC visuals | Box | Lowest memory [1] |

## Checklist
- [ ] Every NPC classified (static / dummy / mob / boss / cutscene)
- [ ] Static NPCs use AnimationController, no Humanoid
- [ ] Unused Humanoid states disabled on dummies and mobs
- [ ] NPC animations played on clients; far NPCs not animated
- [ ] Pooling and proximity spawning in place
- [ ] Mobs share one mesh + one SurfaceAppearance; tint for variety
- [ ] Boss silhouette test at 60–100 studs passed
- [ ] Boss medium-LOD (250–500 studs) checked
- [ ] MicroProfiler: no `updateInvalidatedFastClusters` spikes > 4 ms during summon moves

## Common Mistakes
- **Full Humanoid on every summon or clone**: stepHumanoid cost scales with count. [1]
- **Server-side animation for 30 mobs**: replication overhead. [1]
- **Cloning a fresh model per spawn** instead of pooling. [1]
- **Expecting SLIM to fix NPC crowds**: it excludes Humanoid models. [3]
- **Unique textures per mob variant** break instancing. [1]
- **Boss growth via live ScaleTo** causes FastCluster rebuild hitches. [1]
- **Precise collision on big boss meshes**: memory and physics cost. Use simple hitboxes. [1]

## Related
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Texturing Anime Characters]]
- [[Clothing and Accessories for Anime Characters]]
- [[Anime Combat Animation Timing]]
- [[Shonen Anime Shape Language]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs, *Improve performance* (Humanoids, draw calls, collision, MicroProfiler scopes): https://create.roblox.com/docs/performance-optimization/improve
2. Roblox Creator Docs, *PBR textures / SurfaceAppearance* (Color tint, emissive): https://create.roblox.com/docs/art/modeling/surface-appearance
3. Roblox Creator Docs, *SLIM* (limitations: Humanoid models excluded; avatars R15 players only): https://create.roblox.com/docs/workspace/streaming/slim
4. Roblox Creator Docs, *General specifications* (20k tris per mesh): https://create.roblox.com/docs/art/modeling/specifications
5. Roblox API reference, *Model:ScaleTo*: https://create.roblox.com/docs/reference/engine/classes/Model
6. Roblox API reference, *AnimationController*: https://create.roblox.com/docs/reference/engine/classes/AnimationController
7. Roblox Creator Docs, *Character body specifications* (total body bounding box 4–10 studs tall): https://create.roblox.com/docs/avatar/character-bodies/specifications
8. Roblox API reference, *SurfaceAppearance* (EmissiveStrength/EmissiveTint/Color script-writable): https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance
9. Roblox Creator Docs, *Meshes → Level of detail*: https://create.roblox.com/docs/parts/meshes
10. Roblox API reference, *AnimationConstraint* (Transform usage): https://create.roblox.com/docs/reference/engine/classes/AnimationConstraint
11. Roblox API reference, *Bone* (not replicated or serialized): https://create.roblox.com/docs/reference/engine/classes/Bone
12. Roblox Creator Docs, *Adaptive Animation*: https://create.roblox.com/docs/characters/adaptive-animation
13. Roblox Creator Docs, *Characters → Non-player characters*: https://create.roblox.com/docs/characters
