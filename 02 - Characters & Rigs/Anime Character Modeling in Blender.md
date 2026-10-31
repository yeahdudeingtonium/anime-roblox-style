---
tags: [characters, blender, modeling, topology, anime]
updated: 2026-10-31
sources: 12
status: draft
---
# Anime Character Modeling in Blender

> [!info] How this was researched
> Roblox numbers come from the Roblox Creator Docs (2026-10-31). create.roblox.com could not be reached from the research session, so the pages were read from Roblox's official docs source repo (`github.com/Roblox/creator-docs`, `main` branch), which is what create.roblox.com is built from. Links below point at the live create.roblox.com URLs.

## TL;DR
- Roblox's hard limit is **20,000 triangles per mesh**. A **Marketplace-valid R15 body totals 10,742 tris** (head 4,000 / torso 1,750 / each limb 1,248). For an in-game anime fighter, aim at about **6–9k tris for the body plus 1–3k for hair** so a server of 12–16 players stays cheap. [1][2]
- Model in **quads, watertight, no n-gons, nothing zero-thickness**. Face **+Z, up +Y** for the body spec. Avatar Setup expects the front on **−Z**, so check which tool you are feeding. [1][2][3]
- Shonen proportions run about **7–8 heads tall** for a realistic-ish adult (Jujutsu Kaisen, Demon Slayer). Roblox "battlegrounds" bodies usually stay **close to Roblox's blocky R6/R15 silhouette** because players' own avatars must fit the same animations. [4][9]
- Put polygons where things **bend or show in silhouette**: 3 loops per elbow and knee, a shoulder loop ring, hair spikes, and the jaw line. Flat planes (back, thighs) get almost nothing, because cel shading has no specular to reveal faceting.
- Keep it **15 parts with `_Geo` names** if you might ever want R15 animations, layered clothing or Avatar Setup. Use a **single mesh** for custom NPCs and bosses. [1][5]

## Why it matters for anime battlegrounds
Battlegrounds games (The Strongest Battlegrounds, Jujutsu Shenanigans, Heroes Battlegrounds) put many characters on screen at once, spam VFX, and run on phones. A character that reads well at 30 studs and still bends cleanly in a 0.15 s punch matters more than sculpted detail. Anime style helps here: it is **silhouette + flat color + a few hard shadow shapes**, which needs far fewer polygons than PBR realism. For scale: Arc System Works' *Guilty Gear Xrd* used about **40,000 polygons per character** with **no normal maps**, with shading controlled by hand. That is a 1v1 console game with two characters on screen. A Roblox battlegrounds server needs roughly a quarter of that per character. [11] See [[Shonen Anime Shape Language]] for the silhouette side and [[Toon Shading on Roblox]] for how this geometry is lit.

## How to do it

### Step 1: Set up Blender for studs
- Scene Properties → Units → **Unit System: None**, **Rotation: Degrees** (Roblox's own Blender guide). Then 1 Blender unit = 1 stud. [3]
- Import a Roblox mannequin (Classic, Rthro Normal or Rthro Slender) from the Avatar resources page so you model at platform scale. Normal is roughly **5.75–6.5 studs tall**, Slender roughly **5.25–6.25 studs**. [6]
- Use Blender **5.x**. Roblox's current dynamic-head tutorial is written against **Blender 5.2**. [7]

### Step 2: Turnaround and proportion sheet
- Front and side orthographic sketches at the **same head height**. Shonen males: about 7–7.5 heads, wide shoulders (about 2 to 2.3 head-widths), narrow hips. Chibi/SD: **2–3 heads**. [4]
- Exclude hair from head-height counts. Spiky hair can add 0.5–1 head of height and must still fit the Hair accessory box if it is an accessory (Normal scale: **1.87 × 3.12 × 2.18 studs**). [4][6]
- Decide now: **R6-looking** (blocky, 6 parts), **R15-compatible** (15 parts), or **custom single mesh** (NPCs, bosses). See [[Roblox Character Rigs R6 vs R15 vs Custom]].

### Step 3: Blockout (about 300–800 tris)
- One cube per body part, Mirror modifier on X with Clipping on. Get the silhouette right from 3/4 and from straight on at small size. Squint at it at about 120 px tall, the size a player sees in a fight.
- Lock the **pivots/joint positions** of the R15 skeleton now (neck, shoulders, elbows, wrists, hips, knees, ankles). Every later loop will be placed relative to these.

### Step 4: Base mesh (target 5–8k tris for the body)
Topology rules for deformation (standard practice, and the reason Roblox asks for quads):
| Area | Recommended loops | Why |
|---|---|---|
| Elbow, knee | 3 loops across the joint (one at the pivot, one each side about 0.1 stud away) | Keeps volume when bent 120°+ |
| Shoulder | Loop ring that follows the deltoid, plus 1 extra loop at the armpit | Arms go overhead in nearly every ultimate pose |
| Wrist, ankle | 2 loops | Low bend angle |
| Hips / groin | Diagonal loop "pants line" from crotch to hip bone | Leg raise for kicks |
| Neck | 2–3 loops | Head turn in lock-on |
| Fingers | Mitten hand (thumb + paddle) unless you plan advanced R15 finger bones | Saves about 400–800 tris; fists are animated as one shape |
| Torso | 8–12 radial edges around the waist is enough | Cel shading hides faceting |

- **Edge flow follows the shadow shapes you want.** In anime, a hard shadow under the pecs or along the jaw should land on an edge loop, so the shading terminator (or your painted shadow) has a clean line to follow.
- Avoid poles (5+ edge vertices) on joints. Put them on flat areas (mid-chest, back).
- **Caps:** for R15 parts, every limb must be capped so it is watertight when split. Caps count toward the budget. [1]

### Step 5: Split into the 15 R15 parts (if R15/avatar compatible)
- Names: `Head_Geo`, `UpperTorso_Geo`, `LowerTorso_Geo`, `LeftUpperArm_Geo`, `LeftLowerArm_Geo`, `LeftHand_Geo`, the matching `Right*`, `LeftUpperLeg_Geo`, `LeftLowerLeg_Geo`, `LeftFoot_Geo`, and the matching `Right*`. [1]
- Alternative: give **one mesh** to Avatar Setup and let it partition, cap, rig and cage for you (it decimates if over budget, unless you untick **Reduce triangle count** in the Development Avatar preset). [5][8]

### Step 6: Head and face geometry
- Plain in-game anime face: a smooth "egg" head of about 600–1,200 tris with the face **painted** (see [[Anime Faces and Eyes on Roblox]]).
- Dynamic-head compatible: Avatar Setup requires **2 separate eyes** (half-sphere eyes in eyebags) and **3 separate mouth parts** (upper teeth, lower teeth, tongue) in a mouthbag, none sharing vertices with the head. [8]

### Step 7: Clean-up before export
- Apply all modifiers (Mirror, Subdivision) and **Apply All Transforms** (Ctrl+A). Roblox wants frozen transforms and pivots at 0,0,0. [1]
- Mesh → Clean Up → Merge by Distance (0.0001), Delete Loose, Fill Holes for watertightness.
- Statistics overlay on, so the triangle count is always visible (quads × 2 ≈ tris, per Roblox's own guidance). [1]
- Continue at [[Blender to Roblox Studio Export Pipeline]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Max tris per mesh (any MeshPart) | 20,000 | Engine import limit [2] |
| Marketplace body total | 10,742 tris | Body spec [1] |
| DynamicHead asset | 4,000 tris | [1] |
| Torso (Upper + Lower) | 1,750 tris | [1] |
| Each arm / each leg (3 parts) | 1,248 tris | [1] |
| Rigid or layered accessory | 4,000 tris | [6][10] |
| Body total bounding box | min 1 × 4 × 0.5, max 8 × 10 × 4 studs (W × H × D) | Validation [1] |
| Head bounding box max | 4 × 2 × 4 studs | [1] |
| Body parts must fill | ≥ 50% of their bounding box (front/side/back) | Visibility rule [1] |
| Recommended in-game anime player body | 6,000–9,000 tris | My budget for 16-player servers (not a Roblox rule) |
| Recommended boss | 10,000–20,000 tris, split across meshes if needed | 20k per-mesh cap [2] |
| Export pose | I-, A- or T-pose (body spec); A or T preferred by Avatar Setup | [1][8] |
| Orientation | Face +Z, up +Y (body spec) / front −Z (Avatar Setup) | Conflicting docs, test both [1][8] |

> [!warning] Unverified
> The two Roblox pages disagree on facing direction (+Z in the body spec, −Z in Avatar Setup requirements). Avatar Setup also has a **Manually Align Front** option. Test-import once before modelling a whole roster.

## Checklist
- [ ] Units: None, 1 BU = 1 stud; mannequin imported for scale
- [ ] Turnaround sheet with head-height grid
- [ ] Blockout reads from 3/4 and at about 120 px tall
- [ ] 3 loops on elbows/knees, shoulder ring, hip "pants line"
- [ ] Body ≤ 10,742 tris (or your own lower in-game budget)
- [ ] No n-gons, watertight, no zero-thickness faces
- [ ] 15 `_Geo` parts named exactly (if R15) with capped limbs
- [ ] All transforms applied, pivots at origin
- [ ] Test import into Studio before UV/texture work

## Common Mistakes
- **Modelling at Blender metric scale** and getting a 100× giant on FBX import (see the export note for the fix). [3]
- **Sculpting first and retopologising later** for a cel-shaded character. Anime models are better hand-poly-modelled, because the edge layout *is* the shading.
- **Too many torso loops, too few joint loops.** Those tris do nothing in cel shading.
- **Merged fingers plus a finger rig.** Pick one. Advanced R15 finger bones need finger geometry. [1]
- **Forgetting caps** on split limbs, which then fail validation as non-watertight. [1]
- **Heads that don't fill 50% of their box** (e.g. a tiny head inside giant hair geometry modelled as part of the head). Put the hair on an accessory instead. [1]

## Related
- [[Shonen Anime Shape Language]]
- [[Anime Faces and Eyes on Roblox]]
- [[Anime Hair Modeling]]
- [[Skinning and Weight Painting for Roblox]]
- [[Blender to Roblox Studio Export Pipeline]]
- [[Top Roblox Modeler Workflow Patterns]]
- [[Toon Shading on Roblox]]

## Sources
1. Roblox Creator Docs, *Character body specifications*: https://create.roblox.com/docs/avatar/character-bodies/specifications
2. Roblox Creator Docs, *General (modeling) specifications*: https://create.roblox.com/docs/art/modeling/specifications
3. Roblox Creator Docs, *Blender* (units, import/export, FBX scale): https://create.roblox.com/docs/art/blender
4. Wikipedia, *Chibi (style)* (head-to-body ratios), plus Clip Studio Tips article 4953 on SD head counts: https://en.wikipedia.org/wiki/Chibi_(style) · https://tips.clip-studio.com/en-us/articles/4953
5. Roblox Creator Docs, *Avatar Setup*: https://create.roblox.com/docs/avatar-setup
6. Roblox Creator Docs, *Rigid accessory specifications* (mannequin heights, Hair box): https://create.roblox.com/docs/avatar/rigid-accessories/specifications
7. Roblox Creator Docs, *Create basic dynamic heads* (Blender 5.2): https://create.roblox.com/docs/art/characters/facial-animation/create-basic-heads
8. Roblox Creator Docs, *Avatar Setup specifications*: https://create.roblox.com/docs/avatar-setup/auto-setup-requirements
9. DevForum, *How do I make an R6 game with R15 quality like Ultimate Battlegrounds?*: https://devforum.roblox.com/t/how-do-i-make-an-r6-game-with-r15-quality-like-ultimate-battlegrounds/3034990
10. Roblox Creator Docs, *Layered accessory specifications*: https://create.roblox.com/docs/avatar/layered-accessories/specifications
11. Game Watch Impress (GDC 2015 GGXrd report: about 40,000 polygons per character, no normal maps): https://game.watch.impress.co.jp/docs/news/20150307_691725.html
12. Roblox creator-docs source repo (mirror used for reading): https://github.com/Roblox/creator-docs
