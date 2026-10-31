---
tags: [characters, skinning, weight-painting, blender, bones]
updated: 2026-10-31
sources: 13
status: draft
---
# Skinning and Weight Painting for Roblox

> [!info] How this was researched
> Roblox rules come from the Roblox creator-docs source repo (`main`, 2026-10-31). create.roblox.com was unreachable from the research session. Blender behaviour comes from Blender manual pages found in search, community threads, and the Blender release notes.

## TL;DR
- **Hard rules:** a vertex can be influenced by **at most 4 bones**. **No weights on `Root`** (or `HumanoidRootNode`), because they are dropped on import. Rest-pose bones need **rot 0 / scale 1**, root at the origin. [1][2][3]
- In Blender: paint with **Auto Normalize on**, then before export run **Weights → Limit Total (limit 4)**, **Normalize All** (Lock Active off), and **Clean** (threshold ≈ 0.01) on every skinned mesh.
- **Preserve Volume (dual quaternion) is not exported in FBX**, so elbows and shoulders collapse in Roblox unless the *topology and weights* hold volume. Add the joint loops from [[Anime Character Modeling in Blender]] and use **corrective weight smoothing**, not the DQ checkbox. [4]
- Skinning is a **visual-only** deformation: hitboxes and collision don't follow. Anime "smear" stretching via scaled bones is possible in-engine but must stay readable. See [[Anime Combat Animation Timing]]. [5]
- For layered clothing you can skip manual weights with **WrapLayer.AutoSkin** (EnabledOverride / EnabledPreserve). Eyebrows and eyelashes must use the special `RBX_Leader` / `RBX_Follower` joints. [6]

## Why it matters for anime battlegrounds
Anime fight animation pushes joints far past T-pose: arms fully overhead for a charge-up, 150° knee bends in landing poses, extreme twists in spinning kicks. Bad weights show up exactly in the frames players screenshot (ultimate poses). Roblox doesn't run your Blender modifiers or corrective shape keys on body joints, so **what you weight is what you get**.

## How to do it

### Step 1: Prepare the mesh and armature
- Apply all transforms on the mesh and armature (Ctrl+A → All Transforms). Bones at rest: rotation 0, scale 1. [1]
- Joint loops in place (3 per elbow/knee). See [[Anime Character Modeling in Blender]].
- Bone display → **Stick** for visibility while painting (Roblox's humanoid skinning tutorial recommends this). [3]
- Parent with **Ctrl+P → With Automatic Weights** as a starting point. Roblox's dynamic-head tutorial notes auto-weights may pre-assign influences you need to check. [7]

### Step 2: Paint with the right settings
- Weight Paint mode → Options → **Auto Normalize ON** (forces each vertex's weights to sum to 1). Roblox calls this out because >4 influences "may occur... with Auto Normalize disabled". [3]
- Turn on **X-Mirror** (Options → Mirror X) for symmetric characters. Roblox asks for symmetrical influences where possible. [1]
- Paint in **pose mode tests**: select the bone (Ctrl+click), press **R** to rotate it, and check the extreme pose. Roblox's own tutorial uses exactly this loop. [3]

### Step 3: Joint-by-joint targets (anime extremes)
| Joint | Weight blend region | Test pose |
|---|---|---|
| Neck | Head ↔ UpperTorso across the bottom 2 neck loops | 45° turn + 30° look-up (lock-on) |
| Shoulder | UpperArm ↔ UpperTorso over the deltoid ring; armpit loop about 50/50 | Arm straight up (180°), arm crossed in front |
| Elbow | LowerArm ↔ UpperArm, centre loop 50/50, outer loops about 80/20 | 140° bend (fist to shoulder) |
| Wrist | Hand ↔ LowerArm on 1–2 loops | 70° flex |
| Waist | UpperTorso ↔ LowerTorso over 2–3 loops | 45° twist (punch wind-up) |
| Hip | UpperLeg ↔ LowerTorso along the "pants line" | High kick (leg at 110°) |
| Knee | LowerLeg ↔ UpperLeg like the elbow | 150° crouch |
| Cape / hair chain | Each vertex shared by ≤ 2 adjacent chain bones | Full swing ±60° |
(Region sizes are my recommended starting points, not Roblox rules.)

### Step 4: Clean before export (every skinned mesh)
1. **Weights → Limit Total**, Limit = **4**, Subset = Deform Pose Bones. Enforces Roblox's 4-influence rule. [1][8]
   > [!warning] Unverified
   > Limit Total's default value. Set it to 4 explicitly rather than trusting the default.
2. **Weights → Clean**, Limit ≈ 0.01, removes tiny stray influences (common after Auto Weights).
3. **Weights → Normalize All**, Lock Active **off**.
4. Check that no vertex is weighted to `Root` (select the Root vertex group → Select, and it should select nothing). [2]
5. Optional: **Quantize** (steps 10–20) for cleaner, more predictable deformation on low-poly bodies.

### Step 5: Volume loss without dual quaternions
- FBX can't carry Blender's Preserve Volume (DQ) setting. Community reports confirm it is dropped on export, and most real-time engines use linear blend skinning. [4]
- Fixes that survive export:
  - **Add a loop** on the outside of the elbow/knee and weight it 60/40 toward the parent bone to keep the "elbow point".
  - **Shoulder helper bone** (e.g. a `ShoulderTwist` child of UpperTorso), driven in animation. Only on Custom rigs, because spec R15 doesn't allow extra body bones in Platform Avatars. [9]
  - **Wrist twist distribution**: split forearm twist across 2–3 loops so a 90° wrist twist doesn't candy-wrap.
> [!warning] Unverified
> Roblox doesn't document its skinning algorithm. Linear blend skinning is assumed from the lack of any DQ option and from general engine practice.

### Step 6: Verify in Studio
- Import (see [[Blender to Roblox Studio Export Pipeline]]), open the **Animation Editor**, and pose each joint to extremes. Bones are visible with **Show Constraint Details**. [5]
- DevForum reports show meshes with vertices on **up to 12 bones** looking broken in Roblox while fine in Blender. That is the classic >4 influences symptom. [10]

### Special cases
- **Layered clothing:** enable `StarterPlayer.LoadCharacterLayeredClothing` and set `WrapLayer.AutoSkin = EnabledOverride` to have the engine compute skinning from the body's cages. `EnabledPreserve` keeps existing weights. [6]
- **Eyebrows/eyelashes:** skin to `RBX_Leader` (vertices on the brow/lid line) and `RBX_Follower` (the rest) at weight **1.0 only**, children of `Root`. Required for those accessory types. Body meshes containing these joints are rejected. [6]
- **Dynamic head:** face joints under `RootFaceJoint`, < 50 joints recommended, Auto Normalize on. [7]
- **Bone-driven smears:** scale or translate bones for 1–2 frames to stretch a fist or leg. Bones only change visuals, so collision is unaffected. [5]

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Max influences per vertex | 4 | Roblox spec [1] |
| Root / HumanoidRootNode weights | 0 (dropped on import) | [2][3] |
| Limit Total | 4 | Enforce the spec |
| Clean threshold | ≈ 0.01 | Remove stray weights (recommendation) |
| Quantize steps | 10–20 | Optional tidiness (recommendation) |
| Cape/hair chain sharing | ≤ 2 bones per vertex | Avoid rubbery stretch (recommendation) |
| RBX_Leader/Follower weight | exactly 1.0 | Validation rule [6] |
| Face joints | < 50 | [7] |

## Checklist
- [ ] Transforms applied; rest-pose bones rot 0 / scale 1
- [ ] Auto Normalize + X-Mirror on while painting
- [ ] Every joint tested at anime-extreme poses
- [ ] Limit Total (4) → Clean (0.01) → Normalize All on every skinned mesh
- [ ] Root vertex group empty
- [ ] No reliance on Preserve Volume; elbows and shoulders hold volume without it
- [ ] Imported and posed in the Studio Animation Editor
- [ ] Layered clothing: AutoSkin mode decided

## Common Mistakes
- **Trusting Automatic Weights as final**: it bleeds torso weights into arms and hair into shoulders. [7]
- **Painting with Auto Normalize off** pushes vertices to more than 4 influences and breaks deformation in Roblox. [3][10]
- **Weights on Root**: silently dropped, so the vertex snaps. [2]
- **Previewing with Preserve Volume on** in Blender hides problems that appear in Roblox. [4]
- **Hitboxes following skinned limbs**: impossible, because bones are visual only. [5]
- **Asymmetric weights** on a symmetric character show up as one elbow collapsing in mirrored animations. [1]

## Related
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Anime Character Modeling in Blender]]
- [[Blender to Roblox Studio Export Pipeline]]
- [[Clothing and Accessories for Anime Characters]]
- [[Anime Combat Animation Timing]]

## Sources
1. Roblox Creator Docs, *General specifications* (4 influences, transforms, symmetry, no root influence): https://create.roblox.com/docs/art/modeling/specifications
2. Roblox Creator Docs, *Character body specifications → Skinning*: https://create.roblox.com/docs/avatar/character-bodies/specifications
3. Roblox Creator Docs, *Skin a humanoid model* (Auto Normalize, stick bones, Root influences dropped): https://create.roblox.com/docs/art/modeling/skin-a-humanoid-model
4. Diffeomorphic import_daz issue tracker / Daz forums (FBX drops dual-quaternion Preserve Volume): https://bitbucket.org/Diffeomorphic/import_daz/issues/763/bones-need-preserve-volume-dual-quaternion · https://www.daz3d.com/forums/discussion/comment/8744401
5. Roblox Creator Docs, *Rigging and skinning* (Bones visual only; Show Constraint Details): https://create.roblox.com/docs/art/modeling/rigging
6. Roblox Creator Docs, *Automatic Skinning Transfer*: https://create.roblox.com/docs/avatar/automatic-skinning-transfer
7. Roblox Creator Docs, *Create basic dynamic heads*: https://create.roblox.com/docs/art/characters/facial-animation/create-basic-heads
8. Blender Manual, *Editing Weight Paint* (Limit Total, Clean, Normalize All, Quantize): https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
9. Roblox Creator Docs, *Avatar Setup specifications* (no bones beyond the standard/advanced spec): https://create.roblox.com/docs/avatar-setup/auto-setup-requirements
10. DevForum, *Meshes work improperly when they have vertices attached to too many bones*: https://devforum.roblox.com/t/meshes-work-improperly-when-they-have-vertices-attached-to-too-many-bones/2483885
11. Roblox Creator Docs, *Skin a simple mesh*: https://create.roblox.com/docs/art/modeling/skin-a-simple-mesh
12. Roblox Creator Docs, *Animation Editor*: https://create.roblox.com/docs/animation/editor
13. Roblox creator-docs source repo (mirror used): https://github.com/Roblox/creator-docs
