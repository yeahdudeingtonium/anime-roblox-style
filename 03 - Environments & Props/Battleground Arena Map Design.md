---
tags: [environments, level-design, arena, battlegrounds, readability, scale]
updated: 2026-10-31
sources: 12
status: draft
---
# Battleground Arena Map Design

## TL;DR
- Battlegrounds maps are **open combat bowls**, not corridors. They have a large flat-ish central floor, a ring of landmark structures, and a hard boundary. Combat is free-roam melee with dashes and knockbacks, so the map is mostly **runway and landing space**.
- **Scale for super-speed**: knockbacks and dashes travel tens of studs, so the central floor should be **several hundred studs across**. Default Roblox walking (16 studs/s, 7.2-stud jump) is the wrong scale reference.
- **Readability first**: low-detail, mid-value floors, strong silhouette landmarks for orientation, and **no clutter** waist-high in the main floor that snags knockback or hides characters.
- **Camera sightlines**: the default camera sits behind the player (`CameraMaxZoomDistance` 400 default, vertical FOV 70°). Tall props near the action occlude the camera, so keep tall geometry on the **perimeter**.
- Put **destructibles and breakables** (cars, poles, walls) at the **edge of the floor**, where knockback sends players, so hits produce payoff without blocking the center.

## Why it matters for anime battlegrounds
In TSB, Jujutsu Shenanigans and Heroes Battlegrounds, the map is a **stage for anime moments**: someone gets punched through a building, a crater forms, a player is launched off a cliff. Unlike a shooter, there is no cover gameplay. The design goals are **visibility**, **space to perform combos**, **spectacle surfaces** to smash, and **orientation** (where am I, where is the enemy). Lighting and toon values support this (see [[Lighting for Anime Maps]]).

> [!warning] Unverified
> I could not find published dimensions for the TSB, JJS or Heroes Battlegrounds maps. The community wiki pages were unreachable. The layout descriptions below are general observations from gameplay footage and secondary sites, not measured facts. Measure the real maps in-game (for example by walking time × WalkSpeed) before copying any proportions.

## How to do it
### Step 1: Define the movement envelope
Collect your own combat numbers first. Every map dimension follows from them.

| Metric | Measure in your game | Map consequence |
|---|---|---|
| Base run speed | e.g. 16–28 studs/s | Time to cross the arena |
| Dash distance | e.g. 20–40 studs | Minimum clear floor around hotspots |
| Max knockback travel | e.g. 60–150 studs (ultimates) | Floor radius plus wall distance |
| Air time / max height | e.g. 30–80 studs | Building heights for wall-slams; ceiling for boundary |
| Players per server | e.g. 12–20 | Total floor area per player |

> [!example] Rule-of-thumb sizing (my proposal, unverified)
> - Central floor radius ≥ 2× max standard knockback. With 60-stud knockbacks, that is a ~250–300-stud-wide central floor.
> - Total playable area: about 6,000–10,000 sq studs per player. For 16 players that is roughly a 350×350 to 400×400-stud play zone, plus a perimeter skyline.
> - Perimeter buildings 40–120 studs tall, so a wall-slam lands visibly mid-facade.

### Step 2: Layout archetypes
| Archetype | Description | Examples (style) |
|---|---|---|
| **City block bowl** | Wide intersection or plaza center, buildings ring the edge, a few alleys | Shibuya-style crossing; Jujutsu urban fights |
| **Training ground** | Flat dirt or grass field, wooden posts, low walls, mountains backdrop | Naruto-style training field |
| **Mountain / crater valley** | Flat valley floor, cliff walls as natural boundary, rock pillars | DBZ-style wasteland |
| **Shrine / temple court** | Stone-paved court, torii gate as landmark, stairs to an upper tier | Jujutsu Kaisen shrine fights |
| **Island (open world)** | Large terrain islands separated by sea, for GPO / Blox Fruits-style traversal | Different design: streaming and travel matter more than arena readability |

See [[Japanese Anime Set Dressing]] for prop lists per archetype.

### Step 3: Readability rules
1. **Value hierarchy**: floor = mid value and low saturation. Characters and VFX = highest contrast. Buildings = slightly darker or cooler than the floor. Sky = lightest (see [[Shonen Anime Shape Language]]).
2. **No detail noise on the floor**: large tileables (MaterialVariant `StudsPerTile` 10–20+), sparse decals (crosswalks, cracks). Busy textures camouflage characters.
3. **Clutter belt**: keep the central floor at least 80% empty. Put props (vending machines, cars, benches) in a **ring 20–40 studs from the walls**.
4. **Landmarks** for orientation: one unique silhouette per compass direction (tower, torii, giant statue, mountain notch). Players recover from knockback by recognizing where they are.
5. **Height variation**: 1–2 tiers maximum in the main floor (for example a 6–10-stud raised plaza). More tiers fragment fights.

### Step 4: Camera and sightlines
- The default camera FOV is **70° vertical**, and `CameraMaxZoomDistance` defaults to **400** studs. Third-person cameras collide with geometry, so tall props near fights cause camera pops.
- Keep **overhangs, bridges and tree canopies** out of the central floor, or make them non-occluding.
- Leave line-of-sight across the arena for targeting and lock-on. Low walls should be 4–6 studs tall: they give grounding without hiding a 5-stud character.
- Test with the **lowest graphics quality**, where view distance shrinks with `PrioritizeLightingQuality`.

### Step 5: Boundaries
- **Natural**: cliffs, a sea, a highway wall, fog through the Atmosphere density ramp.
- **Invisible walls**: `CanCollide` Parts at 150+ studs high. Show them with a VFX shimmer when hit, so players understand them.
- **Kill planes**: Workspace `FallenPartsDestroyHeight` for voids. Use a water or void plane under islands.
- Skyline backdrop beyond the boundary: low-poly building silhouettes or a painted skybox (see [[Skyboxes and Backdrop Painting]]).

### Step 6: Spectacle surfaces
- **Breakable walls** on perimeter buildings at knockback height (5–30 studs).
- **Physics props**: cars, poles and crates that fly when hit, placed in the clutter belt.
- **Crater-friendly floor**: the floor should be simple Parts or flat MeshParts that crater and debris modules can raycast and sample color from. See [[Destructible Environments and Craters]].
- Reset rules: destroyed props respawn on a timer (30–120 s) or per round.

### Step 7: Spawns and flow
- 6–12 spawn points around the clutter belt, facing the center.
- Spawn protection zones with low visual noise.
- Avoid one obvious "king of the hill" position. Battlegrounds want fights everywhere.

### Step 8: Streaming and size
- Arena maps of 300–500 studs fit inside the default **`StreamingTargetRadius` of 1024**. You can keep streaming on with mostly persistent-free models, and the whole arena stays loaded.
- Open-world maps (GPO, Blox Fruits style) need streaming tuning and SLIM LOD. See [[Environment Performance Budgets]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Default WalkSpeed / JumpHeight | 16 / 7.2 studs | API defaults: a baseline, not anime scale |
| Camera FOV | 70° vertical | API default |
| CameraMaxZoomDistance | 400 | API default |
| StreamingTargetRadius | 1024 default | Streaming docs |
| StreamingMinRadius | 64 default | Streaming docs |
| Central floor clear | ≥80% | Proposal (unverified) |
| Low wall height | 4–6 studs | Proposal (unverified) |

## Checklist
- [ ] Measure the dash, knockback and air-time envelope before greyboxing.
- [ ] Greybox on a grid (see [[Stylized Environment Kits]]). Playtest 1v1 and with 12+ players.
- [ ] Central floor at least 80% clear. Props in the perimeter clutter belt.
- [ ] 4 landmarks, one per direction.
- [ ] No overhangs above the main floor. Camera tested at max zoom.
- [ ] Boundaries readable, invisible walls give feedback.
- [ ] Breakables at the floor edge with a respawn timer.

## Common Mistakes
- RPG-town scale (narrow streets 10–20 studs), where knockbacks slam into walls constantly and the camera clips.
- Detailed, saturated floor textures that hide characters.
- Clutter in the center that snags knockback trajectories and breaks combos.
- One giant map with nowhere to recognize: players get lost after knockbacks.
- Arena gameplay under huge open-world streaming settings, causing pop-in mid-fight.

## Related
- [[Japanese Anime Set Dressing]]
- [[Destructible Environments and Craters]]
- [[Stylized Environment Kits]]
- [[Lighting for Anime Maps]]
- [[Skyboxes and Backdrop Painting]]
- [[Environment Performance Budgets]]
- [[Shonen Anime Shape Language]]
- [[Anime VFX Fundamentals]]

## Sources
1. Roblox API dump (WalkSpeed, JumpHeight, Camera FOV, CameraMaxZoomDistance defaults): https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/Full-API-Dump.json
2. Instance streaming (radii, LOD): https://create.roblox.com/docs/workspace/streaming
3. Streaming techniques (64 / 1024 defaults): https://create.roblox.com/docs/workspace/streaming/techniques
4. Env-art curriculum, greybox (grid, wall/hall minimums): https://create.roblox.com/docs/tutorials/curriculums/environmental-art/greybox-your-environment
5. Lighting class (PrioritizeLightingQuality view distance): https://create.roblox.com/docs/reference/engine/classes/Lighting
6. Moldy Skull Games: Fighting game readability and you (background vs secondary action): https://moldy-skull-games.itch.io/zeitgeist/devlog/577786/3-fighting-game-readability-and-you
7. Source Gaming: Sakurai on Melee stage design (character identifiability): https://sourcegaming.info/2017/07/22/melee_stage_design/
8. GameCraft Studios: Improving the arena art while not distracting the player: https://gamecraftstudios.itch.io/for-sparta/devlog/229602/game-design-improving-the-arena-art-while-not-distracting-the-player
9. ExitLag: The Strongest Battlegrounds overview (secondary source; map role): https://www.exitlag.com/blog/the-strongest-battlegrounds-overview/
10. BuiltByBit: Anime-Stylized Japanese City Map / Cell Games Arena Map listings (market examples of battleground map archetypes): https://builtbybit.com/resources/anime-stylized-japanese-city-map.112455/ , https://builtbybit.com/resources/cell-games-arena-map.114445/
11. DevForum: Punch Rock Module inspired by TSB (destruction on floors): https://devforum.roblox.com/t/punch-rock-module-inspired-by-tsb/3171422
12. Game Design Forum, Half-Life arena vs cover analysis: https://www.quaddicted.com/webarchive/thegamedesignforum.com_20160521/features/rd_hl_5.html
