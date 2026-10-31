---
tags: [characters, faces, eyes, dynamic-heads, facs, normals, anime]
updated: 2026-10-31
sources: 18
status: draft
---
# Anime Faces and Eyes on Roblox

> [!info] How this was researched
> Roblox rules were read from the official Roblox creator-docs source repo (github.com/Roblox/creator-docs, `main`, 2026-10-31), because create.roblox.com was unreachable from the research session. DevForum threads were seen only through search-result summaries, so treat forum-derived claims as weaker.

## TL;DR
- There are three ways to build an anime face on Roblox: **(A) painted texture or decal on a simple head** (cheapest, most "anime", easy expression swaps), **(B) separate mesh eyes/brows/mouth planes** (swappable and animatable with bones), **(C) a full Dynamic Head with FACS** (needed for the Marketplace, works with avatar chat, hardest to keep looking 2D).
- In-game characters (your own fighters, NPCs, bosses) **do not need to pass dynamic-head validation**, so A or B is fine. Anything sold as an avatar body must have a dynamic head with **≥ 17 FACS poses** that passes **5 landmark tests**. [1][2]
- **Roblox replaced Classic Heads/Faces with Dynamic Heads in Feb–Mar 2026** (the "Dynamic Head Migration"). After pushback it added a way to switch off face animation. Player avatars in your game will arrive with dynamic heads. [3][4]
- Custom normals for anime-style face shading: Blender's **Data Transfer from a sphere/ellipsoid proxy** is the standard trick. Evidence suggests Roblox keeps imported vertex normals (with FBX-triangulation and layered-clothing caveats), but Roblox has **no custom shaders**, so the gain is subtle. Paint the shadow into the texture instead (see [[Toon Shading on Roblox]]). [5][6][7]
- Swap expressions by changing **`MeshPart.TextureID`** (script-writable) or swapping whole pre-made **SurfaceAppearance instances** (their map properties are not script-writable), or toggle **visibility of separate face meshes**. For dynamic heads, drive **FaceControls** properties or play face animations.

## Why it matters for anime battlegrounds
Anime faces are mostly 2D: big flat irises, one-line mouths, brows that carry all the emotion. In a battlegrounds game the face is seen at most 2–4 seconds at a time, in **ultimate cutscenes / awakening zooms**, and the rest of the time it is about 20 pixels tall. So the face has to (1) read as a clean 2D design up close and (2) swap to rage/shock/smirk in a single frame on cue. Hard frame-timed expression pops fit [[Anime Combat Animation Timing]] better than blended FACS sliders.

## How to do it

### Option A: Painted face on a simple head (recommended for in-game fighters)
1. Model a smooth head of about **600–1,200 tris**, and UV the face area as one flat, front-projected island (UV → Project from View in front ortho). A front projection keeps eye shapes undistorted.
2. Give the face island a **large share of the texture**: about 25–35% of a 1024² atlas, i.e. roughly a 512×512 equivalent for the face. (My recommendation. Roblox caps humanoid character maps at **1024×1024** under its PBR budget guidance.) [8]
3. Paint eyes, brows and mouth flat. Use an outline color, not black, for the anime look (dark red-brown for skin lines).
4. For expressions, make an **expression atlas**: duplicate the face region per expression (neutral, angry, shocked, pained, smirk, eyes-closed), each as a separate texture asset, then swap **`MeshPart.TextureID`** from a script. Scripts can write it.
   > [!warning] SurfaceAppearance maps are not script-writable
   > The API reference lists `SurfaceAppearance.ColorMap` (and the Normal, Roughness and Metalness maps) as **PluginSecurity** for write, and notes that "most SurfaceAppearance properties cannot be modified by scripts". `ColorMapContent` (which can point at an EditableImage) is also PluginSecurity for write. Scripts *can* change `SurfaceAppearance.Color`, `AlphaMode`, `EmissiveStrength` and `EmissiveTint`. So with a SurfaceAppearance face, swap expressions by **parenting a different pre-made SurfaceAppearance instance** (pre-made in ReplicatedStorage) under the head, or keep the face on a separate TextureID-driven mesh. [18]
5. Alternative: a **Decal** on the head. Decals project onto a face of the part's bounding box, so they only work cleanly on near-box heads such as the classic R6 head. [9]

### Option B: Separate face meshes (eyes, brows, mouth)
- Model the eyes as **slightly domed planes or lens shapes** floating about 0.005–0.01 studs in front of the face surface (avoids z-fighting). Brows and mouth are separate thin planes. Each one is its own MeshPart or part of a face accessory mesh.
- Swap expressions by **switching Transparency** of pre-made variants, by changing their textures, or by rigging the planes to face bones (eyelid bones, brow bones) and animating them in the Animation Editor.
- Pupils: a separate disc mesh, bone-driven for gaze, or a texture with **UV offset** (a SurfaceAppearance can't scroll, but a `Texture` instance on a part can via OffsetStudsU/V).
- Cost: each extra MeshPart is another draw call unless instanced. Keep it to ≤ 4–6 face pieces per character. [10]

### Option C: Dynamic Head (FACS) for Marketplace or avatar compatibility
Requirements (Roblox, 2026):
- **Head mesh ≤ 4,000 tris**, with an outer cage named `Head_OuterCage` from Roblox's template (don't add or delete cage vertices). [1][11]
- **Facial landmarks:** the cage must project 3 landmarks (left eye, right eye, mouth). The mouth landmark vertices sit on the **second loop** out from the mouth opening. [1]
- A face rig under a **`RootFaceJoint`** (usually named `DynamicHead`) parented to the R15 `Head` bone. Roblox advises **fewer than 50 face joints**. Its Cubie reference uses **30+**, and typical heads have **50 base poses**. [12]
- **17 required FACS poses**: LeftEyeClosed, RightEyeClosed, EyesLookDown, JawDrop, Pucker, Left/RightLipCornerPuller, ChinRaiser, ChinRaiserUpperLip, Left/RightCheekRaiser, Left/RightInnerBrowRaiser, Left/RightLipCornerDown, Left/RightLowerLipDepressor. [1]
- **Validation tests** (all must visibly move the landmarks): left blink, right blink, mouth open (`JawDrop`=1), happy (`Pucker` + both `LipCornerPuller`=1), sad (10 controls including `CheekRaiser`=0.85). [1][2]
- **Neutral pose on frame 0**; FBX export with **Bake Animation on** and **Custom Properties on**, because pose-to-frame mapping lives in custom properties. [13][12]

**Anime problem:** validation checks that the *cage-projected landmarks on the head mesh* move. Painted 2D eyes don't move geometry, and eyes on a separate mesh also fail ("ensure that your landmarks are applied to the head mesh, not the eyeballs"). [2] Workarounds:
- Use **Avatar Setup → "Handle face as 2D decal"**. It infers eye and mouth regions from your texture, generates cages and FACS, and maps the result onto a dynamic-head template. You must run it with **body + head together**, delete any existing `FaceControls` first, and use SurfaceAppearance rather than TextureID. [14]
- Or model real eyelid and lip geometry (anime "almond" lids) that closes over flat painted irises.

### Face normals for cel-shaded faces
Problem: a standard N·L terminator crawls across an anime face in ugly blotches (nose, cheek and eye-socket shadows). Approaches:
1. **Normal transfer from a proxy** (Blender): duplicate a sphere or ellipsoid shaped to the face, add a **Data Transfer** modifier on the head (Face Corner Data → Custom Normals, from the proxy, mix mode Replace, masked with a vertex group so only the face is affected). In Blender 4.1+ Auto Smooth became a modifier and custom normals no longer need the old Auto Smooth toggle. [5][7][17]
2. **Paint shadow shapes** into the albedo and set the face to receive almost no dynamic shading (bright skin, low-contrast lighting). This is the most robust approach on Roblox.
3. Genshin-style **SDF face shadow maps** (a texture that stores shadow thresholds for 0–180° light angles) need a custom shader, which **Roblox cannot do**. [6]

Does the normal edit survive Roblox import?
- A Roblox staff reply on a DevForum thread about creators' "own shadings for avatars" blamed broken normals on **FBX's built-in triangulation** and suggested **pre-triangulating** (Triangulate modifier, applied, *after* the normal transfer, with "Keep Normals") or **exporting glTF**. That implies authored normals are imported. [15]
- Another thread reports **layered clothing deformation messing up custom vertex normals on a skinned mesh**. Expect custom normals to be recomputed when a WrapLayer deforms the mesh. [16]
> [!warning] Unverified
> No official Roblox page states that custom split normals are preserved. Verify in Studio: import two copies (with and without the transfer) under the same Lighting and compare.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Head tris (DynamicHead asset) | ≤ 4,000 | Spec [1] |
| Required FACS poses | 17 | Avatar chat and validation [1] |
| Typical FACS base poses | 50 | Roblox tutorial [12] |
| Face joints | < 50 recommended | Perf and organisation [12] |
| Mouth landmark | 2nd vertex loop from the lip opening | Validation [1] |
| Sad test cheek raiser | 0.85 | Validation table [1] |
| Max texture for humanoid characters | 1024×1024 (PBR budget) | [8] |
| Marketplace texture cap | 2048×2048 | Body spec [11] |
| Face island share of atlas | 25–35% | My recommendation for close-up cutscenes |
| Face plane offset (Option B) | 0.005–0.01 studs | Avoid z-fighting (practice) |

## Checklist
- [ ] Decide A (painted), B (face meshes) or C (dynamic head) per character type
- [ ] Face UV island front-projected and large
- [ ] Expression set painted: neutral, angry, shocked, pained, smirk, closed
- [ ] Swap system tested (TextureID or instance swap) at the frame the animation needs it
- [ ] If C: 17 FACS poses, neutral at frame 0, Bake Animation on, Custom Properties on
- [ ] If C: test with Avatar Setup validation before the final texture pass
- [ ] Normal-transfer test: compare edited vs unedited in Studio under game Lighting
- [ ] Pre-triangulate before FBX export if the face has edited normals

## Common Mistakes
- **Building a full FACS rig for an NPC** that never talks. Option A costs about 1/10th of the effort.
- **Eyes on a separate mesh with a dynamic head** cause validation failure because the landmarks can't detect motion. [2]
- **Cage pushed inside the head mesh** makes landmark projection fail. [2]
- **Exporting quads after a normal edit** lets FBX re-triangulate and break the shading. [15]
- **Assuming players' faces are classic decals**: since the 2026 migration they are dynamic heads, and decal-swapping scripts written for classic faces may break. [3][4]
- **Face texture with too few pixels.** The ultimate close-up is when people take screenshots.

## Related
- [[Toon Shading on Roblox]]
- [[Texturing Anime Characters]]
- [[Anime Character Modeling in Blender]]
- [[Skinning and Weight Painting for Roblox]]
- [[Anime Combat Animation Timing]]
- [[Shonen Anime Shape Language]]

## Sources
1. Roblox Creator Docs, *Dynamic head specifications*: https://create.roblox.com/docs/avatar/dynamic-heads/specifications
2. Roblox Creator Docs, *Dynamic head validation*: https://create.roblox.com/docs/avatar/dynamic-heads/validate
3. DevForum (Roblox), *Completing the Dynamic Head Migration* (Jan–Mar 2026): https://devforum.roblox.com/t/completing-the-dynamic-head-migration/4301387
4. PC Gamer, *Roblox walks back some of its dramatic changes to avatar faces*: https://www.pcgamer.com/games/roblox-walks-back-some-of-its-dramatic-changes-to-avatar-faces-but-not-enough-to-make-everyone-happy · PCGamesN: https://www.pcgamesn.com/roblox/classic-heads-converted-removed
5. Blender Artists, *Customizing Normals tutorial series* (Data Transfer normal setups): https://blenderartists.org/t/customizing-normals-tutorial-series/1369038
6. GitHub, NoiRC256 *URPSimpleGenshinShaders* (face shadow map stores 0–180° light coverage): https://github.com/NoiRC256/URPSimpleGenshinShaders
7. Blender Manual, *Data Transfer Modifier*: https://docs.blender.org/manual/en/4.2/modeling/modifiers/modify/data_transfer.html
8. Roblox Creator Docs, *Texture specifications*: https://create.roblox.com/docs/art/modeling/texture-specifications
9. Roblox Creator Docs, *Textures and decals*: https://create.roblox.com/docs/parts/textures-decals
10. Roblox Creator Docs, *Improve performance* (draw calls and instancing): https://create.roblox.com/docs/performance-optimization/improve
11. Roblox Creator Docs, *Character body specifications*: https://create.roblox.com/docs/avatar/character-bodies/specifications
12. Roblox Creator Docs, *Create basic dynamic heads*: https://create.roblox.com/docs/art/characters/facial-animation/create-basic-heads
13. Roblox Creator Docs, *Export character bodies*: https://create.roblox.com/docs/avatar/character-bodies/export
14. Roblox Creator Docs, *Avatar Setup* ("Handle face as 2D decal"): https://create.roblox.com/docs/avatar-setup
15. DevForum, *Roblox converts incorrectly some normals… when I'm making my own shadings for avatars* (staff reply: FBX triangulation; pre-triangulate or use glTF): https://devforum.roblox.com/t/roblox-converts-incorrectly-some-normals-from-3d-models-when-im-making-my-own-shadings-for-avatars/2711054
16. DevForum, *Layered clothing is messing up custom vertex normals in a skinned UGC mesh*: https://devforum.roblox.com/t/layered-clothing-is-messing-up-custom-vertex-normals-in-a-skinned-ugc-mesh/3035624
17. Blender 4.1 release notes, Modeling (Auto Smooth replaced by a modifier/node group; custom normals always used): https://developer.blender.org/docs/release_notes/4.1/modeling/
18. Roblox Engine API reference, *SurfaceAppearance* and *MeshPart* (property security; TextureID writable, ColorMap PluginSecurity): https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance · https://create.roblox.com/docs/reference/engine/classes/MeshPart
