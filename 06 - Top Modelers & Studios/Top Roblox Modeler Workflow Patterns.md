---
tags: [workflow, modeling, pipeline, blender, substance, synthesis, studios]
updated: 2026-10-31
sources: 19
status: draft
---
# Top Roblox Modeler Workflow Patterns

## TL;DR
- The dominant Roblox pipeline is **Blender (modelling, UVs, rigging) → Substance 3D Painter or hand-painting (Photoshop/Krita/Blender texture paint) → FBX/OBJ → Studio Asset Manager/3D Importer → SurfaceAppearance or TextureID**. ZBrush shows up only for high-poly sculpts that get baked down.
- **Two texturing camps**: *PBR via SurfaceAppearance* (Substance's built-in "Roblox (SurfaceAppearance)" export template, up to 4 maps) vs *hand-painted/flat colour* on a single texture or plain SmoothPlastic. Anime battlegrounds lean heavily toward the second for characters and environments, with PBR used sparingly.
- Roblox-native showcase artists (for example `Fluorlite`, now an environment artist at Twin Atlas) build **directly in Studio** with parts, Creator Store assets and, since 2026, procedural models. Top results don't require heavy DCC use for every asset.
- Hard engine constraints shape every workflow: **~20K tris per mesh**, **one material per mesh**, **1024² textures historically (4K rendering added in 2026 with streaming)**, **31 Highlights**, and mobile memory.
- Pros **reuse aggressively**: trim sheets/atlases, shared VFX textures, modular kits, instanced meshes. Draw calls and memory matter more than polycount.
- Anime battlegrounds teams are tiny (often 1–5 core people plus commissioned freelancers). The "studio" is frequently an owner + scripter + freelance VFX, animator and modeller network on Discord and the DevForum.

## Why it matters for anime battlegrounds
Knowing the common pipeline tells you what to hire for, which file formats and deliverables to ask for, and where the quality comes from (VFX + animation + reuse, not hero-asset fidelity).

## How to do it: the synthesized pipeline

### Step 1: Concept and reference (0.5–2 days per character or kit)
- Style sheet + PureRef board (see [[Reference Gathering and Screenshot Breakdown]]).
- Turnaround (front, side, back) or at minimum front + 3/4 for characters; top-down plus elevation for map kits.
- Studios with budget hire 2D concept artists. Twin Atlas job listings describe concept art for "characters, creatures, environments, props and items".

### Step 2: Block-out in Studio first (environments)
- Grey-box with Parts at real scale to test **combat distances** (dash length, knockback) before any modelling.
- Native Studio builders keep many pieces as Parts/Unions; `Fluorlite` describes building showcase work natively in Studio and leaning on the Creator Store.
- New in 2026: `/generate_procedural_model` in Studio creates configurable procedural models (parameters change geometry, colour, material). Useful for kit variations.

### Step 3: Model in Blender
| Asset | Typical approach |
|---|---|
| Character / hair | Low-poly box modelling + hair cards or chunky hair shells; see [[Anime Character Modeling in Blender]] |
| Weapons | Hard-surface low poly; exaggerated silhouette; bevel only on the silhouette edges |
| Environment kit | Modular pieces on a stud grid with shared trims; see [[Stylized Environment Kits]] |
| VFX meshes | Crescents, rings, spikes, shockwave cones with gradient UVs; see [[Anime VFX Fundamentals]] |

Roblox-specific rules:
- One material per MeshPart, so split by material or atlas.
- Keep each mesh under ~20K tris (vendors quote 21K; test borderline cases).
- Apply transforms, sensible origin, scale so Studio import is 1:1 in studs.
- Export FBX (rigged or skinned) or OBJ (static).

### Step 4: Texture
| Path | Tools | Output | When |
|---|---|---|---|
| Flat / hand-painted | Blender texture paint, Photoshop, Krita, Substance (hand-paint layers) | 1 colour map (TextureID or SurfaceAppearance ColorMap) | Anime characters, toon environments, most battlegrounds assets |
| Baked stylized | Sculpt in ZBrush/Blender → bake normal/AO → paint over | Colour (+ normal) | Chunky stylized props with readable bevels |
| PBR | Substance 3D Painter → "Roblox (SurfaceAppearance)" preset | Colour, Normal, Roughness, Metalness (plus opacity in ColorMap alpha) | Weapons with metal, showcase-quality props |

Substance gotchas reported by users:
- Pick the template named **Roblox (SurfaceAppearance)**, not the MTL one; it only exists in recent Painter versions.
- Set the shader to the Roblox shader; with "pbr metallic roughness" one user got blank exports. Enable the **Opacity** and **Emissive** channels in Texture Set settings if export errors mention them.
- The 2020 DevForum tutorial notes the 1K cap and drops AO in favour of Opacity in the template.

### Step 5: Import and set up in Studio
- Import via the 3D Importer / Asset Manager; check scale, pivot, and that skinned meshes keep their bones.
- Add a SurfaceAppearance (or set TextureID) and keep `EnvironmentSpecularScale` low for toon assets.
- Set CollisionFidelity (Box/Hull where possible), `CastShadow` off on small detail meshes, `Anchored` for static kit pieces.
- Check LOD: Roblox tiers meshes by distance (<250 / 250–500 / 500+ studs).

### Step 6: Optimise and share
- Use packages for kit pieces so changes propagate.
- Asset Privacy (full release for new Image/Mesh/Decal assets in 2026): when a creator or group enables it, newly uploaded images, decals and meshes default to **Restricted**, so you share them explicitly with collaborators or experiences. Only the group owner can toggle it; it isn't retroactive.

## Patterns observed across top artists and studios
| Pattern | Evidence |
|---|---|
| Blender + Substance Painter is the standard toolkit | Freelance portfolios such as `RosariaDev` (Blender + Substance Painter, weapons section), `Ticoelephant` (about 5 years Blender + Substance, stylized and realistic weapons), `Rxgnar` (textures "mostly using Substance Painter", PBR + emission) |
| VFX artists specialise and credit shipped games | `Plebarae` credits effects in Combat Warriors, Kaizen, Anime Champions X, Mythfall; a carrd VFX portfolio lists Jujutsu Infinite, Shonen Unleashed, Heroes Battlegrounds, Project Baki |
| Studio-native fidelity work | `Fluorlite` (showcases built in Studio; now environment artist at Twin Atlas) |
| Streaming and simplification over raw detail | Twin Atlas: instance streaming for Creatures of Sonaria; meshes changed to "hull" to shrink the game |
| Intake forms + fixed revision rounds | VFX carrds route requests through a Google Form and include 2 rounds of minor revisions |
| Self-made VFX, no packs | `assetstring` VFX page: "fully self-made", textures custom or open source, no free models or pre-made packs |
| Deposits + client pays the Robux tax | DevForum modeller listings commonly ask for 30% up front / 70% on completion, with the client covering the 30% Robux marketplace fee |

> [!warning] Unverified
> I found **no public, sourced pipeline write-up** from the art teams of The Strongest Battlegrounds, Jujutsu Shenanigans, Heroes Battlegrounds, Type Soul, Blox Fruits, GPO, Project Mugetsu or Sakura Stand. The patterns above come from freelance artists who work in the genre and from adjacent studios (Twin Atlas). Don't attribute specific tools to those games' teams without a source.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Per-mesh tri cap | ~20K | Importer limit |
| Materials per mesh | 1 | Engine |
| SurfaceAppearance maps | Colour, Normal, Roughness, Metalness | Engine |
| Texture size (anime char) | 1024² body / 512² parts | Flat art + mobile |
| Max texture rendering | 4096² (since 2026, streamed) | Docs + DevForum |
| LOD tiers | <250 / 250–500 / 500+ studs | Render fidelity |
| Highlight cap | 31 | Engine |

## Checklist
- [ ] Studio grey-box approved before modelling begins
- [ ] Blender export preset saved (FBX, scale, apply transforms)
- [ ] Texture path chosen per asset class (flat vs baked vs PBR)
- [ ] Substance "Roblox (SurfaceAppearance)" template tested once end to end
- [ ] Collision fidelity and CastShadow set on import
- [ ] Assets uploaded to the **group** (not a freelancer's personal account); Asset Privacy settings checked
- [ ] Packages used for modular kit pieces

## Common Mistakes
- PBR-texturing every asset in a toon game (memory, mixed style).
- Importing duplicates of the same mesh instead of reusing one asset ID.
- Building hero props to 20K tris "because it fits".
- Letting freelancers upload final assets to their personal accounts.
- Sculpting high-frequency detail that turns into noise under toon lighting.

## Related
- [[Commissioning and Briefing Artists]]
- [[Public Roblox Artist Portfolios]]
- [[Case Study - The Strongest Battlegrounds and Jujutsu Shenanigans]]
- [[Case Study - Studio-Scale and Licensed Anime Games]]
- [[Anime Character Modeling in Blender]]
- [[Stylized Environment Kits]]
- [[Toon Shading on Roblox]]
- [[Anime VFX Fundamentals]]
- [[Mobile-Aware Stylization]]

## Sources
1. DevForum – Substance Painter to Studio Tutorial | SurfaceAppearance PBR: https://devforum.roblox.com/t/substance-painter-to-studio-surfaceappearance/866962
2. Adobe Community – Issue exporting textures for Roblox (SurfaceAppearance preset, shader fix): https://community.adobe.com/t5/substance-3d-painter-bugs/issue-when-exporting-textures-theyre-for-roblox-so-ive-used-the-surface-appearance-preset/idi-p/13968719
3. Roblox creator-docs – Texture specifications: https://github.com/Roblox/creator-docs/blob/main/content/en-us/art/modeling/texture-specifications.md
4. DevForum – 4k Texture Rendering: https://devforum.roblox.com/t/4k-texture-rendering/4316229
5. Roblox Creator Hub – Meshes (one texture or 4 PBR maps; LOD tiers): https://create.roblox.com/docs/parts/meshes
6. GitHub polywright – tri cap check: https://github.com/m4bwav/polywright/wiki/How-Checks-Decide
7. DevForum – Creator Roadmap 2026: Spring Update (procedural models, asset privacy): https://devforum.roblox.com/t/creator-roadmap-2026-spring-update/4625473
8. Roblox Creator Hub – Asset privacy: https://create.roblox.com/docs/projects/assets/privacy
9. DevForum – [Full Release] Privacy for Newly-Created Image, Mesh, and Decal Assets: https://devforum.roblox.com/t/full-release-privacy-for-newly-created-image-mesh-and-decal-assets/4620416
10. Roblox Newsroom – Creators Discuss Working in Unique Art Styles (Fluorlite, Twin Atlas): https://about.roblox.com/newsroom/2026/07/roblox-studio-fidelity-creator-interviews-twin-atlas-fluorlite-maximillian-ecos
11. GamesBeat – Twin Atlas exclusive interview: https://gamesbeat.com/twin-atlas-is-among-the-studios-changing-what-roblox-games-look-like-exclusive-interview/
12. Twine – Twin Atlas 2D Artist listing: https://www.twine.net/projects/b9sx90-twin-atlas-2d-artist-2d-animator-in-las-vegas-united-states-job
13. Rosaria's Portfolio (carrd): https://rosaria-leah.carrd.co/
14. DevForum – [OPEN] Ticoelephant 3D modeler portfolio: https://devforum.roblox.com/t/open-ticoelephant-3d-modeler-portfolio/1485449
15. DevForum – [3D modeler] Rxgnar's Portfolio: https://devforum.roblox.com/t/3d-modeler-rxgnars-portfolio/4683143
16. Plebarae – Roblox VFX Artist: https://plebarae.com/
17. Khan VFX portfolio (carrd): https://khanvfx.carrd.co/
18. assetstring VFX pricing page (carrd): https://assetstring.carrd.co/
19. DevForum – Commission Price Guide For New Developers (general commission norms): https://devforum.roblox.com/t/commission-price-guide-for-new-developers/1356888 *(the 30%/70% deposit pattern came from search snippets of several DevForum listings whose individual threads I couldn't open; treat as unverified)*
