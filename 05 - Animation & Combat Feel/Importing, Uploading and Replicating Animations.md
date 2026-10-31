---
tags: [animation, upload, replication, permissions, group-games, pipeline]
updated: 2026-10-31
sources: 10
status: draft
---
# Importing, Uploading and Replicating Animations

## TL;DR
- **Save ≠ publish.** *Save* stores a `KeyframeSequence` in `ServerStorage` (it doesn't replicate). *Publish to Roblox* creates an asset ID you reference via `Animation.AnimationId = "rbxassetid://…"`.
- For a **group-owned game, publish animations with the group as Creator** (official step). Animations owned by a user often fail to load in a group game for other players (many DevForum reports).
- **Play character animations from the owning client.** Tracks started by a player's client on an Animator in their `Player.Character` replicate to the server and other clients. NPC animations must be loaded and played **on the server**. The Animator must be **created on the server**.
- Asset sharing: the Creator Dashboard **Permissions** page for **Animations** lets you grant collaborators (friends or groups) and experiences (by universe ID). **Game grants cannot be revoked.**
- Import external animation via **Animation Editor → ⋯ → Import → From File (.fbx)**. Emotes must be converted to `CurveAnimation` and be < 10 s.

## Why it matters for anime battlegrounds
A battlegrounds game ships hundreds of animations: 4+ M1s, skills and ultimates per character, across 10+ characters. Ownership mistakes are the #1 reason "animations work in Studio but not in game". Replication choices decide whether other players see your M1 on time.

## Pipeline overview
```
Author (Animation Editor / Moon Animator 2 / Blender)
   → KeyframeSequence or CurveAnimation in the place
   → Publish to Roblox (Creator = the GROUP that owns the game)
   → Asset ID → Animation instance in ReplicatedStorage
   → Client: Animator:LoadAnimation() on own character → Play()
   → Replicates via Animator to server + other clients
```

## Step 1: Import (if not authored in Studio)
1. Put a matching rig in the workspace. The official emote guide uses a standard R15 rig from **Avatar → Character**. Use your own R6 or custom rig for battlegrounds.
2. Open the Animation Editor (the emote guide calls the Avatar-tab button **Clip Editor**) and select the rig.
3. **⋯ → Import → From File**, then pick the `.fbx`. One English doc version labels it **From FBX Animation**, so the menu label varies.
4. FBX export from DCC tools must have **Bake Animation** enabled when you export animation (Roblox export requirements).
5. Community route for Blender: Den_S's "Blender rig exporter/animation importer" (Roblox plugin + Blender add-on). Newer R6 IK/FK Blender rigs require **Cautioned's Blender Animations plugin** (exports `.rbxanim` / clipboard → Roblox plugin). Details in [[Moon Animator 2 vs Blender vs Animation Editor]].

## Step 2: Set metadata before publishing
- **Priority**: ⋯ → **Set Animation Priority**. Set this per asset, though you can override at runtime with `track.Priority`. See [[Roblox Animation System Reference]].
- **Looping**: the Looping button. A looped animation does **not** interpolate last→first, so duplicate the first keys as the last keys.
- **Events**: add KeyframeMarkers (`Hit`, `CanCancel`, `VFX`, `Sound`).
- If you replace a default Animate-script animation (run/jump/etc.), rename the final keyframe **`End`** (case-sensitive) before export.
- Use **⋯ → Optimize Keyframes** to strip redundant keys. The editor also auto-removes intermediate keys when 3+ consecutive keys share a value (for facial and curve conversions).

## Step 3: Publish
1. **⋯ → Publish to Roblox.**
2. Title + description.
3. **Creator field → select the group** if the game is group-owned (official "IMPORTANT" step).
4. Submit, then copy the asset ID.

> [!warning] Group game ownership
> DevForum threads consistently report that a group game only loads animations owned by that group, or by the place's owner in specific cases. The fix is to **re-publish under the group and swap the IDs**. In a 2024–25 thread, staff acknowledged a bug where some group members couldn't publish under the group even with access. The interim workaround was granting the legacy "Create and edit community experiences" permission, which is broad. Check the current status before relying on it.

> [!warning] Unverified
> The exact rule for whether a **user-owned** animation plays in a **user-owned** game made by a different user (e.g. a commissioned animator) was not confirmed from official docs. The safe rule is that the game owner (user or group) owns or is granted every animation.

## Step 4: Share across creators (commissions, teams)
From the Asset privacy doc (Creator Dashboard → Development Items → **Animations** → asset → **Permissions**):
- **Collaborators tab**: grant to a **friend** or to a **group** in which you have the experience-edit permission.
- **Experiences tab**: grant to universe IDs (comma-separated for several).
- **Game grants are permanent and cannot be revoked.**
- The account-level "Asset Privacy" toggle affects only Images, Decals and Meshes. Animations keep their own defaults.
- The DevForum "Revamped Asset Manager" beta supports bulk grants.

## Step 5: Replicate correctly
Official `Animator:LoadAnimation` rules:
- An Animator under a `Humanoid`/`AnimationController` **in a player's Character**: animations started **on that client** replicate to the server and others.
- An Animator **not** in a player character (NPCs, dummies, boss rigs): **load and play on the server**.
- The **Animator must be created on the server**. A client-created Animator's tracks do not replicate.
- `LoadAnimation` on a client-owned model also loads it for the server.

| Who plays it | Where to call Play | Why |
|---|---|---|
| Player's own M1/skills | Owning client (LocalScript) | Zero local latency, auto-replicates |
| Victim's stun on a **player** | Victim's client (via RemoteEvent) *or* server | Server-played tracks on player characters also replicate but override client control. Pick one authority |
| NPC / training dummy | Server | Required |
| Cutscene camera | Each client locally | Camera is never replicated |
| Graph-based Animate | Per `Workspace.AuthorityMode` | See graph docs |

> [!warning] AdjustSpeed and network owner
> DevForum reports: `AdjustSpeed(0)` (hitstop/freeze) only works reliably when called by the character's **network owner**, and its replication to other clients can be late or inconsistent. Run hitstop **locally on every client** from a RemoteEvent rather than trusting replication. See [[Hitstop, Hit Reactions and Knockback]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Final keyframe name for default-anim replacement | `End` | Required by Animate script |
| Emote max length | < 10 s | Emote specs |
| Emote data type | `CurveAnimation` | Required for emotes |
| Marketplace emote upload fee | 80 Robux | Emote import doc |
| Animation storage for runtime | `ReplicatedStorage` Animation instances | Clients need access |
| Save location of drafts | `ServerStorage` (`AnimSaves` ObjectValue on rig) | Not replicated |

## Checklist
- [ ] Every animation published with Creator = the group that owns the game
- [ ] Keep a spreadsheet or ModuleScript of `name → assetId → priority → owner`
- [ ] Animation instances live in ReplicatedStorage, not ServerStorage
- [ ] Animator exists on the server-spawned character (default Humanoid does this)
- [ ] Player moves played from the owning client. NPC moves from the server
- [ ] Hitstop/freeze triggered per client by RemoteEvent
- [ ] Commissioned animators: they publish to *your group* or grant your universe ID

## Common Mistakes
- Shipping the `ServerStorage` KeyframeSequence instead of a published asset.
- Publishing under a personal account, then transferring the game to a group, so every animation breaks for players.
- Creating `Animator` with `Instance.new` on the client.
- Re-uploading the same move 5 times with no ID registry. Nobody knows which ID is live.
- Assuming the account Asset Privacy toggle covers animations (it doesn't).

## Related
- [[Roblox Animation System Reference]]
- [[Moon Animator 2 vs Blender vs Animation Editor]]
- [[M1 Combo System Design]]
- [[Roblox Character Rigs R6 vs R15 vs Custom]]
- [[Top Roblox Modeler Workflow Patterns]]

## Sources
1. Roblox Creator Docs: Animation Editor (save vs export, group Creator field, `End` keyframe, looping, priority). https://create.roblox.com/docs/animation/editor
2. Roblox Creator Docs: Use animations (Animator, LoadAnimation pattern, replacing defaults, weights). https://create.roblox.com/docs/animation/using
3. Roblox Creator Docs: Animator class (client/server replication rules). https://create.roblox.com/docs/reference/engine/classes/Animator
4. Roblox Creator Docs: Asset privacy (Animations permissions tab, irrevocable game grants). https://create.roblox.com/docs/projects/assets/privacy
5. Roblox Creator Docs: Import emotes (⋯ → Import → From File; CurveAnimation; 80 Robux). https://create.roblox.com/docs/avatar/emotes/import
6. Roblox Creator Docs: Emote specifications (< 10 s). https://create.roblox.com/docs/avatar/emotes/specifications
7. Roblox Creator Docs: Export requirements (Bake Animation). https://create.roblox.com/docs/art/modeling/export-requirements
8. DevForum: "Animations under a group don't work for group members". https://devforum.roblox.com/t/animations-under-a-group-dont-work-for-group-members/3073070
9. DevForum: "Failed to load animation with sanitized ID, Group Animations". https://devforum.roblox.com/t/failed-to-load-animation-with-sanitized-id-group-animations/3827277
10. DevForum: "AdjustSpeed() not correctly replicating to other clients" and "AnimationTrack:AdjustSpeed(0) not working?". https://devforum.roblox.com/t/adjustspeed-not-correctly-replicating-to-other-clients/2907655 , https://devforum.roblox.com/t/animationtrackadjustspeed0-not-working/3390106
