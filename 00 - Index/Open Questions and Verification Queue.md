---
tags: [meta, verification, todo]
updated: 2026-10-31
status: solid
---
# Open Questions and Verification Queue

Everything the 2026-10-31 research pass could **not** confirm. Work through this list in Studio or in-game, then flip the relevant note's `status` to `verified-in-studio`.

> [!warning] Research access gap
> The session that wrote this vault could not open create.roblox.com, devforum.roblox.com, YouTube, GDC Vault, Wikipedia, 80.lv, ArtStation, Polycount or the player-count trackers.
> - **Roblox docs facts** were read from the official source repo, github.com/Roblox/creator-docs, so treat them as reliable.
> - **DevForum, GDC and tracker claims** come from search summaries and are marked `Unverified` in their notes.
> - **Fix:** allow those domains in the cloud environment's network settings, then re-run a verification pass.

## Conflicts in Roblox's own docs
- [ ] **Texture max resolution**: 1024² vs 4096² (4K rendering shipped 2026). Character PBR guidance says 1024², the Marketplace says 2048². See [[Roblox Character Limits Cheat Sheet]], [[Texturing Anime Characters]] and [[Creating VFX Textures]].
- [ ] **Triangle cap per mesh**: 20,000 (docs) vs 21,000 (vendors). See [[Anime Character Modeling in Blender]].
- [ ] **Character facing**: +Z (body spec) vs −Z (Avatar Setup requirements). See [[Blender to Roblox Studio Export Pipeline]].
- [ ] **ShadowSoftness default**: 0.2 (docs) vs 0.5 (API dump), so set it explicitly. See [[Lighting for Anime Maps]].
- [ ] **ParticleEmitter Rate**: documented cap of 400/s, but Roblox's own tutorial uses 50,000. See [[ParticleEmitter Deep Dive]].
- [ ] **Import menu naming**: "From File" vs "From FBX Animation". See [[Importing, Uploading and Replicating Animations]].

## Engine behaviour to test in Studio
- [ ] **Avatar Joint Upgrade**: R15 now uses `AnimationConstraint` instead of Motor6D. Does it touch R6? Does combat code that looks for Motor6D break? See [[Roblox Character Rigs R6 vs R15 vs Custom]].
- [ ] **Custom split normals**: are they kept on FBX/glTF import? This decides whether Guilty Gear-style face shading works. See [[Anime Faces and Eyes on Roblox]].
- [ ] **Bone limits**: what is the maximum bone count per skinned mesh?
- [ ] **Bone scale keys**: do they enable true squash and stretch? See [[Anime Posing and Smears on Roblox]].
- [ ] **NPC instancing**: do NPCs with different `SurfaceAppearance.Color` tints still batch together? See [[NPC and Boss Characters]].
- [ ] **Soft lighting on phones**: how do `LightingStyle = Soft` and `PrioritizeLightingQuality` look on real devices?
- [ ] **Low graphics quality**: does it still suppress ParticleEmitter `Rate`? See [[VFX Performance Budget]].
- [ ] **Custom flipbook layouts**: are they fully live, and do they now allow non-power-of-two sheets?
- [ ] **FragmentAsync on meshes**: out of beta yet? See [[Destructible Environments and Craters]].
- [ ] **Animation Graph Editor**: still beta? See [[Roblox Animation System Reference]].
- [ ] **Inverted-colour impact-frame hacks**: do they still work? See [[Impact Frames and Screen Effects]].
- [ ] **Lighting presets and triangle budgets**: tune all of them on a mid-range phone.

## Reference-game facts to measure in-game
Nobody has published these, so they have to be captured and counted ourselves (60 fps recording, frame-step).
- [ ] **Rigs**: do TSB, JJS and Heroes BG use R6, R15 or custom? Do they keep the player's own avatar?
- [ ] **Animation timing**: M1 startup, active and recovery frames; hitstop length; dash distance and cooldown; ultimate length. See [[Anime Combat Animation Timing]] and [[Hitstop, Hit Reactions and Knockback]].
- [ ] **Map sizes** in studs. See [[Battleground Arena Map Design]].
- [ ] **VFX density**: particle counts during an ultimate. See [[Anime VFX Fundamentals]].
- [ ] **Peak CCU**: trackers disagree (TSB is reported as 613.6K, 1M and 1.4M). See [[Case Study - The Strongest Battlegrounds and Jujutsu Shenanigans]].

## Design questions for the owner
- [ ] **Rigs**: R6 blocky-anime or custom skinned characters?
- [ ] **Core loop**: which one? The research shortlist is battlegrounds + cosmetics, then a survivors-like PvE mode, then anime TD with ethical gacha. See [[Core Loop Comparison Matrix]] and [[Hybrid Loops for Anime Games]].
- [ ] **Look targets**: the 2–3 games whose look to match most closely.
- [ ] **Competition count**: count the clones above 1K CCU for the chosen loop before committing.
