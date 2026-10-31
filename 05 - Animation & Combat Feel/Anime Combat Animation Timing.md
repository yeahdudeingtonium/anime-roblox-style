---
tags: [animation, timing, combat, frame-data, anime, limited-animation]
updated: 2026-10-31
sources: 12
status: draft
---
# Anime Combat Animation Timing

## TL;DR
- Think of every attack as **startup → active → recovery** in frames at 60 fps (1 frame = 16.7 ms). Fighting games list jabs at about 4f startup and heavies at about 10f. Battlegrounds games need slower, more readable numbers because of network latency.
- The Roblox Animation Editor's timeline runs at **30 fps by default** (`seconds:frames`, so `0:15` = 0.5 s). The frame rate is an *editing* setting only. Playback always interpolates at render rate, so you must **author the stepping yourself**.
- The anime look comes from **limited animation**: strong key poses, **holds**, and stepped timing ("on 2s/3s"). On Roblox, the **`Constant` easing style** removes interpolation between keyframes, so the rig snaps from key to key.
- Mix rates. Use smooth (`Linear`/`CubicV2`) for anticipation and follow-through, stepped (`Constant`) on the 2–4 frames around the hit, and a **long hold on the impact pose** that hitstop extends further.
- Starting budgets at 60 fps (design recommendations, not measured from any game): **M1 jab ~6–9f startup**, **heavy/finisher ~14–20f**, **ultimate wind-up ~0.6–1.5 s** before the first damaging frame.

## Why it matters for anime battlegrounds
TSB, Jujutsu Shenanigans and Heroes Battlegrounds sell "anime" mostly through **timing**, not model detail. They use snappy anticipation, a snap to a held impact pose, then a slow settle. Arc System Works deliberately **cut frames** out of Guilty Gear Xrd's 3D animation so it read like hand-drawn sprites. A full-frame-rate version of the same move looked worse ("Limited Animation"; GDC 2015, Junya C. Motomura). The same idea transfers directly to a Roblox R6 rig.

## Core vocabulary
| Term | Meaning | Roblox mapping |
|---|---|---|
| Startup | Frames from input to first hitbox frame | Time from `track:Play()` to the `Hit` KeyframeMarker |
| Active | Frames the hitbox can connect | Between `HitStart` / `HitEnd` markers (or one-shot query at `Hit`) |
| Recovery | Frames after active until you can act again | Marker `Recover`/`CanCancel` → end of track |
| Hold | A pose kept unchanged for N frames | Duplicate the keyframe N frames later (or `Constant` easing) |
| On 1s / 2s / 3s | New drawing every 1 / 2 / 3 frames of 24 fps film | Key spacing in the timeline (see table) |
| Hitstop | Both fighters freeze on contact | `track:AdjustSpeed(0)` for N ms, see [[Hitstop, Hit Reactions and Knockback]] |
| Anticipation | Wind-up pose opposite to the action | First 30–50% of startup |
| Smear / multiples | Stretched or duplicated in-between | See [[Anime Posing and Smears on Roblox]] |

## Frame math cheat sheet
At a 60 fps render rate, 1 frame = 16.67 ms. In the Roblox editor at its default 30 fps, one *timeline* frame = 33.3 ms = 2 render frames.

| Anime timing (24 fps film) | Drawings / s | Hold per drawing | 60 fps render frames | Key spacing at 30 fps timeline | Key spacing at 60 fps timeline | Key spacing at 24 fps timeline |
|---|---|---|---|---|---|---|
| On 1s | 24 | 41.7 ms | 2.5 | every 1 frame (≈) | every 2–3 frames | every 1 frame |
| On 2s | 12 | 83.3 ms | 5 | every 2–3 frames | every 5 frames | every 2 frames |
| On 3s | 8 | 125 ms | 7.5 | every 4 frames (133 ms) | every 7–8 frames | every 3 frames |
| On 4s (hold-heavy TV) | 6 | 166.7 ms | 10 | every 5 frames | every 10 frames | every 4 frames |

> [!tip] Use a 24 fps timeline for anime 2s/3s
> The editor's frame rate setting lets you edit at a different rate. A 2019 DevForum announcement describes a custom-framerate setting and import detection that tries 30, then 24, then 60 fps. At 24 fps, "on 2s" and "on 3s" land exactly on whole timeline frames. The setting does **not** change playback. It only changes where keys snap.

> [!warning] Unverified
> The exact list of frame rate choices in the current (2026) Animation Editor settings menu could not be confirmed from the official docs. The docs only say the timeline menu has a **Frame Rate** option and that the default is 30 fps.

## Stepped vs smooth interpolation on Roblox
The Animation Editor's per-keyframe **Easing Style** options (official docs):
- **Linear**: constant speed.
- **Constant**: "Removes interpolation between the selected keyframe and next keyframe. The animation will 'snap' from keyframe to keyframe." This is your **stepped / limited-animation** tool.
- **CubicV2**: eases in or out with cubic interpolation.
- **Elastic**, **Bounce**.

Easing **Direction** options: In (slow start), Out (fast start, slow end), InOut.

How to use them for anime:
1. **Block in stepped.** Set every key to `Constant` while blocking, the way 3D animators work in "stepped" mode. You see only the poses and their timing. If it reads as a flipbook, the poses are good.
2. **Selectively un-step.** Switch to smooth only where motion should *flow*: the anticipation wind-up (CubicV2 In) and the settle back to guard (CubicV2 Out).
3. **Keep the strike stepped.** From the last anticipation frame to the impact pose, use 1–2 `Constant` keys (optionally one smear key between them). Anime strikes often "teleport" into the contact pose.
4. **Hold the impact pose.** Duplicate the impact keyframe 3–6 timeline frames later (at 30 fps) so the pose is readable even before hitstop is added.

> [!warning] Unverified
> A DevForum user reported that the `Constant` easing style (called "None" in Moon Animator) caused an animation to break in game. This is one report, not a confirmed bug. Test stepped animations in a live server, not only in the editor.

## Anticipation → strike → hold → settle (the anime beat)
A typical anime punch broken into beats. These are design targets, in 60 fps frames:

| Beat | M1 jab | Heavy / M1 #4 finisher | Ultimate strike |
|---|---|---|---|
| Anticipation (wind-up, opposite direction) | 3–5f | 8–12f | 30–60f+ (often with camera cut) |
| Strike (stepped, 0–1 smear key) | 2–3f | 2–4f | 2–4f |
| Active (hitbox live) | 2–4f | 3–6f | 1 frame per hit, or a multi-hit window |
| Impact hold (before hitstop) | 4–6f | 6–10f | 10–30f + impact frame |
| Recovery / settle | 8–14f | 18–30f | 30–90f (pose, aura, camera return) |
| **Total** | **~19–32f (0.32–0.53 s)** | **~37–62f (0.6–1.0 s)** | **multi-second, see [[Ultimate and Awakening Sequences]]** |

> [!warning] Unverified
> These are **starting values I derived** from fighting-game frame data and anime holds. They are not measured from TSB, JJS or Heroes Battlegrounds frame-by-frame. Capture your reference game at 60 fps and count frames before you lock numbers.

### Reference frame data from fighting games (60 fps)
| Game / move | Startup | Active | Notes |
|---|---|---|---|
| SF6 Ryu standing LP (jab) | 4f | 3f | +4 on hit, −1 on block (GameSkinny) |
| SF6 Ryu standing MP | 6f | 4f | +7 on hit (GameSkinny) |
| SF6 Ryu standing HP | 10f | 5f | single source; verify in training mode |
| KOF XIII hitstop | light 7f / heavy 11f | | wiki table |
| GG Strive attack Lv0 | hitstop 11f | | stand hitstun 12f (Dustloop template) |

Battlegrounds games run over the network. The attacker's input reaches the server about one round trip later, so they generally use **slower startups than SF6**. 6–9f for a jab gives the hit time to land visually on other clients.

## Building a jab on a 30 fps timeline (worked example)
Target: an M1 jab, total ≈ 0.43 s = 13 timeline frames at 30 fps (26 render frames).

| Timeline frame (30 fps) | Time | Key | Easing |
|---|---|---|---|
| 0:00 | 0.000 s | Guard pose (copy of idle frame 0) | CubicV2 In |
| 0:02 | 0.067 s | Anticipation: shoulder back, torso twisted 25° away | Constant |
| 0:04 | 0.133 s | Smear key (arm stretched, see posing note) | Constant |
| 0:05 | 0.167 s | **Impact pose** + marker `Hit` | Constant |
| 0:08 | 0.267 s | Impact pose duplicate (hold) + marker `CanCancel` | CubicV2 Out |
| 0:13 | 0.433 s | Back to guard + marker `End` | — |

Startup = 0.167 s ≈ 10 render frames. Hold = 0.1 s, before hitstop adds another 0.05–0.1 s.

## Mixing rates inside one move
Anime cuts switch rates freely. One article describes a sequence that moves between 1s, 2s and 3s in the same cut, and high-action shots go to 2s or 1s. A practical split:
- **Wind-up on 2s** (snappy but legible)
- **Strike on 1s or a single snap** (reads as instant)
- **Impact hold on "∞"** (hitstop + duplicate key)
- **Recovery on 3s or smooth** (relaxes the eye)

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Editor default frame rate | 30 fps | Official default. `0:15` = 0.5 s |
| Anime 2s at 60 fps render | 5 render frames per pose | 83 ms holds |
| Anime 3s at 60 fps render | 7–8 render frames per pose | 125 ms holds |
| Easing for stepped keys | `Constant` | Snaps key to key |
| Easing for wind-up | `CubicV2` + `In` | Slow start, fast end |
| Easing for settle | `CubicV2` + `Out` | Fast start, slow end |
| `AnimationTrack:Play()` default fadeTime | 0.1 s | API default. Set **0–0.05** for snappy M1s |
| Jab startup target | 6–9 render frames | Readable over network (recommendation) |
| Heavy startup target | 14–20 render frames | Telegraphs block/dodge window (recommendation) |
| Impact hold (authored) | 4–10 render frames | Before hitstop is added |

## Checklist
- [ ] Set the timeline to 24 fps (for exact 2s/3s) or stay at 30 and key every 2/4 frames
- [ ] Block every move with all keys `Constant` first
- [ ] Mark `Hit`, `CanCancel` and `End` with KeyframeMarkers (see [[M1 Combo System Design]])
- [ ] Give the impact pose a duplicated hold key of 3–6 timeline frames
- [ ] Play with `fadeTime` 0–0.05 instead of the default 0.1 s, or the snap gets mushy
- [ ] Count frames in a 60 fps capture of your reference game before finalising
- [ ] Test stepped keys in a live server, not just in the editor

## Common Mistakes
- **Smooth-interpolating everything.** Linear or Cubic everywhere gives "Roblox floaty" motion. The anime look needs holds and snaps.
- **Leaving the default 0.1 s fade on `Play()`.** A 6-frame jab startup becomes mush because the previous pose blends for 6 frames.
- **Equal timing per key.** Anime timing is uneven: long hold, fast snap, long hold.
- **Ignoring network delay.** Jabs at 3–4f startup look great locally but appear to hit before they animate on other clients.
- **Animating at 60 fps on 1s** and expecting it to look like anime. Motomura's GGXrd comparison showed the full-frame version looked *worse*.

## Related
- [[Anime Posing and Smears on Roblox]]
- [[Hitstop, Hit Reactions and Knockback]]
- [[M1 Combo System Design]]
- [[Moon Animator 2 vs Blender vs Animation Editor]]
- [[Roblox Animation System Reference]]
- [[Ultimate and Awakening Sequences]]
- [[Anime VFX Fundamentals]]
- [[Shonen Anime Shape Language]]

## Sources
1. Roblox Creator Docs: Animation Editor (default 30 fps, easing styles incl. Constant, priorities). https://create.roblox.com/docs/animation/editor (read via mirror https://github.com/Roblox/creator-docs/blob/main/content/en-us/animation/editor.md)
2. Roblox Creator Docs: AnimationTrack (Play/Stop default fadeTime 0.1, weight 1, speed 1). https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
3. DevForum: "[New] Set custom framerate in Animation Editor [Beta]" (frame rate is editing-only; import detection 30→24→60). https://devforum.roblox.com/t/new-set-custom-framerate-in-animation-editor-beta/392218
4. GDC Vault: "GuiltyGearXrd's Art Style: The X Factor Between 2D and 3D", Junya C. Motomura, GDC 2015. https://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
5. Arc System Works: GDC 2015 talk and handout PDF announcement. https://www.arcsystemworks.com/guilty-gear-xrd-art-talk-at-game-developers-conference-2015/
6. Wikipedia: Guilty Gear Xrd (artists deliberately cut frames to keep a sprite-like feel). https://en.wikipedia.org/wiki/Guilty_Gear_Xrd
7. Anime News Network Lexicon: "Shot on threes (ones, twos, etc.)". https://www.animenewsnetwork.com/encyclopedia/lexicon.php?id=61
8. iD Tech: What does animating on ones, twos, and threes mean? https://www.idtech.com/blog/what-does-animating-on-ones-twos-and-threes-mean
9. GameSkinny: Street Fighter 6 Ryu frame data guide (5LP 4f/3f, 5MP 6f/4f, 5HP 10f/5f). https://www.gameskinny.com/tips/street-fighter-6-ryu-frame-data-analysis-guide/
10. SuperCombo/KOF XIII wiki: Hitstun/Blockstun state (hitstop 7 light / 11 heavy). https://srk.shib.live/w/The_King_of_Fighters_XIII/Character_States/Hitstun_Blockstun_state
11. Dustloop: GGST data header template (Lv0 hitstop 11f, stand hitstun 12f). https://www.dustloop.com/w/Template:AdditionalDataHeader-GGST
12. DevForum: "Animation broken when played" (Constant / Moon "None" easing report). https://devforum.roblox.com/t/animation-broken-when-played/2278086
