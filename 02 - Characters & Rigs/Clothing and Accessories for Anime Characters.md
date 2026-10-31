---
tags: [characters, clothing, accessories, layered-clothing, capes, physics]
updated: 2026-10-31
sources: 14
status: draft
---
# Clothing and Accessories for Anime Characters

> [!info] How this was researched
> Roblox numbers come from the Roblox creator-docs source repo (`main`, 2026-10-31). create.roblox.com was unreachable from the research session. DevForum module info comes from search-result summaries.

## TL;DR
- There are four ways to dress a character: **(1) model the outfit into the body mesh** (best for fixed-design fighters, NPCs and bosses), **(2) Classic 2D Shirt/Pants textures** (R6/R15, near zero cost, the "battlegrounds default"), **(3) Rigid accessories** (armour, swords on back, haori collars), **(4) Layered clothing** (WrapLayer; stretches over any body, but the most expensive).
- **Rigid and layered accessories: ≤ 4,000 tris each, single mesh, ≤ 2048² textures for the Marketplace.** Layered tops and bottoms fit in an **8 × 8 × 8 stud** box. A rigid Back accessory (cape) fits **9.86 × 8.59 × 4.87 studs** (Normal scale). [1][2]
- Layered clothing needs **`_InnerCage` + `_OuterCage`** meshes with **UVs that match the body cage**. Roblox pairs cage vertices *by UV*. It works on non-R15 rigs too, if the target has a WrapTarget and you add a Weld when there's no Humanoid. [2][3][4]
- **Capes, scarves, haori tails:** use **3–6 bones per strip** and either *hand-animate* them (most reliable for hitstop and VFX timing) or *simulate* them client-side (SmartBone-style modules). Don't use chains of physics parts on player characters. [5][6]
- Performance: avatar instantiation with **layered clothing is expensive**. Roblox flags **`updateInvalidatedFastClusters` > 4 ms** as the symptom. Battlegrounds games respawn constantly, so prefer baked outfits. [7]

## Why it matters for anime battlegrounds
Shonen outfits are iconic and simple: school uniforms (Jujutsu Kaisen), haori with checker or flame patterns (Demon Slayer), gi with belts (Dragon Ball), long coats (Bleach). Players pick a *character moveset*, not an outfit, so most battlegrounds games either **keep the player's own avatar** and just add VFX (the The Strongest Battlegrounds approach, where players fight as their Roblox avatars) or **force a character model** per moveset. Either way, clothing must survive fast, extreme poses and get swapped on respawn hundreds of times per server hour.

> [!warning] Unverified
> Which battlegrounds titles force custom outfits and which keep player avatars changes with updates. Check the current game before citing it as a reference.

## How to do it

### Option 1: Outfit modelled into the body (recommended for custom fighters/NPCs)
- Model clothes as **part of the body surface**. Delete hidden skin underneath (no torso under a coat) to save tris and avoid poke-through.
- Coat tails, haori sleeves and skirts get **extra bones** (see below) or stay rigid and short.
- One texture atlas for body plus outfit (see [[Texturing Anime Characters]]).

### Option 2: Classic Shirt / Pants (2D)
- Template part sizes: **128×128** (front/back), **64×128** (sides), **128×64** (up/down), **64×64** (limb tops/bottoms). T-shirts are a square image (e.g. **512×512**). [8]
- Pros: free performance, works on R6 and R15, players can recolor. Cons: flat, with no silhouette change. Fine for school uniforms, *not* for flowing coats.

### Option 3: Rigid accessories
Rules (Roblox 2026): single mesh, **≤ 4k tris**, watertight, quads preferred, ≤ 2048² textures (Marketplace), non-albedo maps ≤ 256². Box sizes, Normal scale, in studs: [1][9]
| Type | W × H × D |
|---|---|
| Hat | 1.87 × 2.5 × 1.87 |
| Hair | 1.87 × 3.12 × 2.18 |
| Face | 1.87 × 1.25 × 1.25 |
| Neck | 2.95 × 3.68 × 2.16 |
| Shoulder (on NeckAttachment) | 6.90 × 3.68 × 3.24 |
| Front | 2.95 × 3.68 × 3.24 |
| Back | 9.86 × 8.59 × 4.87 |
| Waist | 3.94 × 4.29 × 7.57 |

- Attachment names must match the body: `HatAttachment`, `HairAttachment`, `FaceFrontAttachment`, `NeckAttachment`, `BodyBackAttachment`, `WaistBackAttachment`, etc. [2]
- Battlegrounds uses: sheathed katana on `WaistBackAttachment` or `BodyBackAttachment`, cursed-energy aura shells, masks on `FaceFrontAttachment`, scarves on `NeckAttachment` (rigid if short).
- In-game-only accessories can ignore the Marketplace box and tri limits (engine cap: 20k tris per mesh). [10]

### Option 4: Layered clothing (WrapLayer)
1. Start from Roblox's **layered-accessory project files** (template inner and outer cages). The outer cage starts identical to the inner, and you only push the outer out over your garment. **Never delete cage vertices or edit cage UVs.** [2]
2. Skin the garment to the R15 armature (≤ 4 influences per vertex), or skip skinning and set `WrapLayer.AutoSkin = EnabledOverride` / `EnabledPreserve` with `StarterPlayer.LoadCharacterLayeredClothing` on. Roblox says auto-skinned accessories "work well... even if those characters have a different number of joints". [2][11]
3. Names: `Jacket`, `Jacket_InnerCage`, `Jacket_OuterCage`. The importer turns them into a MeshPart with a `WrapLayer`. [3][10]
4. Convert to an Accessory with the **Accessory Fitting Tool**. Tops attach via `BodyFrontAttachment`, bottoms via `WaistCenterAttachment`. [2]
5. **On custom (non-R15) rigs:** the body needs a `WrapTarget` (an `_OuterCage` mesh), all cages must share UVs, and if there's **no Humanoid** add a `Weld` (Part0 = accessory, Part1 = body part). [4]

> [!tip] Anime-specific
> Layered clothing smooths and inflates shapes. Sharp anime folds (zig-zag hem lines, crisp collars) soften when wrapped over a different body. For a signature outfit, Option 1 keeps the design exact.

### Capes, scarves, haori tails, long sleeves
| Approach | How | Use when |
|---|---|---|
| **Hand-animated bones** | 3–6 bone chain per strip, keyed in every attack animation (overlap follows the body by 1–3 frames) | Hero characters; you want the cape to "pose" on impact frames, see [[Anime Combat Animation Timing]] |
| **Procedural bones (client)** | Spring/verlet module drives Bone CFrames each frame (e.g. SmartBone 2) | Many characters, idle and run; runs per client so may differ between players [5][6] |
| **Physics part chain** | Parts plus Rope/Hinge constraints welded to the torso | Bosses or props only. Network ownership and physics cost on player characters |
| **Rigid with a pose swap** | Two or three rigid cape meshes swapped by state (idle / dash / ult) | Mobile-heavy games, cheapest |

- Bones for skinned capes are created in Blender (a child chain of `UpperTorso`, e.g. `Cape1…Cape5`), weight-painted with smooth falloff (each vertex shared by ≤ 2 adjacent cape bones), and imported. Bones then appear as `Bone` instances you can animate or script. Bones change visuals only, not collision. [12]
- SmartBone setup (per its DevForum thread): tag the MeshPart and list root bones in a `Roots` attribute. The original module is retired in favour of **SmartBone 2**. [5][6]
> [!warning] Unverified
> SmartBone 2's current API and collision support. Read its DevForum page before integrating.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Rigid accessory | ≤ 4,000 tris, single mesh | [1] |
| Layered accessory | ≤ 4,000 tris, single mesh | [2] |
| Layered clothing box | 8 × 8 × 8 studs | [2] |
| Eyebrow/eyelash box | 1.5 × 0.5 × 0.5 studs | [2] |
| Max influences per vertex | 4 | [2][10] |
| Marketplace accessory texture | ≤ 2048² | [1][2] |
| Rigid non-albedo maps | ≤ 256² | [9] |
| Cape bones per strip | 3–6 | Recommendation |
| Overlap lag on cape keys | 1–3 frames at 30 fps | Recommendation (animation practice) |
| Perf red flag | `updateInvalidatedFastClusters` > 4 ms | [7] |
| Accessory MeshPart props (Marketplace) | Material Plastic, Transparency 0, VertexColor 1,1,1 | [2] |

## Checklist
- [ ] Decide per character: baked outfit, classic 2D, rigid or layered
- [ ] Hidden body under clothes deleted (baked outfits)
- [ ] Accessory attachments named to match the body's attachments
- [ ] Layered: template cages used, no cage vertex or UV edits, ≤ 4 influences
- [ ] Custom rig + layered: WrapTarget on body, Weld if no Humanoid
- [ ] Cape/scarf bones placed and weighted; plan for hand-animated vs procedural
- [ ] Respawn test in a 16-player server: watch `updateInvalidatedFastClusters` in the MicroProfiler

## Common Mistakes
- **Deleting cage vertices** "to clean up", which breaks UV pairing so the clothing explodes or fails import. [2][3]
- **Physics capes on every player**: replication and simulation cost, plus jitter during dashes.
- **Layered clothing on frequently respawning characters** gives respawn hitches. [7]
- **Accessory attachment name mismatch** (`BodyBackAttachment` vs `BackAttachment`), so the accessory spawns at the feet or the origin.
- **Cape weights shared by 3–4 cape bones** make the cape stretch like rubber. Keep it to 2.
- **Forgetting that Bones don't move collision**: hitboxes must not depend on cape or sleeve bones. [12]

## Related
- [[Anime Hair Modeling]]
- [[Skinning and Weight Painting for Roblox]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Texturing Anime Characters]]
- [[Anime Combat Animation Timing]]
- [[NPC and Boss Characters]]

## Sources
1. Roblox Creator Docs, *Rigid accessory specifications*: https://create.roblox.com/docs/avatar/rigid-accessories/specifications
2. Roblox Creator Docs, *Layered accessory specifications*: https://create.roblox.com/docs/avatar/layered-accessories/specifications
3. Roblox Creator Docs, *Cage meshes*: https://create.roblox.com/docs/art/modeling/cage-meshes
4. Roblox Creator Docs, *Character appearance → Layered accessories on non-R15*: https://create.roblox.com/docs/characters/appearance
5. DevForum, *[OLD] SmartBone – optimized module for dynamically simulated bones*: https://devforum.roblox.com/t/old-smartbone-an-optimized-module-for-dynamically-simulated-bones/2087131
6. DevForum, *SmartBone 2 – Simulated physics and collision solution for Bones*: https://devforum.roblox.com/t/smartbone-2-simulated-physics-and-collision-solution-for-bones/2728928
7. Roblox Creator Docs, *Improve performance → Humanoids*: https://create.roblox.com/docs/performance-optimization/improve
8. Roblox Creator Docs, *Classic clothing*: https://create.roblox.com/docs/avatar/classic-clothing
9. Roblox Creator Docs, *Texture specifications*: https://create.roblox.com/docs/art/modeling/texture-specifications
10. Roblox Creator Docs, *General specifications* and *Meshes* (importer naming → WrapLayer/WrapTarget): https://create.roblox.com/docs/art/modeling/specifications · https://create.roblox.com/docs/parts/meshes
11. Roblox Creator Docs, *Automatic Skinning Transfer*: https://create.roblox.com/docs/avatar/automatic-skinning-transfer
12. Roblox Creator Docs, *Rigging and skinning* (Bones don't affect collision): https://create.roblox.com/docs/art/modeling/rigging
13. Roblox Creator Docs, *Accessory Fitting Tool*: https://create.roblox.com/docs/avatar/accessory-fitting-tool
14. Roblox creator-docs source repo (mirror used): https://github.com/Roblox/creator-docs
