---
tags: [style, reference, workflow, pureref, analysis]
updated: 2026-10-31
sources: 9
status: draft
---
# Reference Gathering and Screenshot Breakdown

## TL;DR
- Collect reference **with a question in mind** ("how do TSB heavies sell impact?"), not as mood wallpaper. Every board gets a written goal.
- Use **PureRef** (free and pay-what-you-want for personal use; commercial licences since 2024; Windows/macOS/Linux) as the board: drag in images, group, annotate, toggle desaturate, keep it always on top over Blender or Studio.
- For motion, grab **frame-by-frame** sources: your own 60 FPS gameplay captures and **Sakugabooru** (240K+ tagged anime clips, player speeds down to 0.2× with frame stepping).
- Break each screenshot down into **5 passes**: silhouette, value, palette, lighting direction, and detail density. Write the numbers down (colour hex, frames, sizes).
- Split boards by **purpose**: Style (anime source), Genre (Roblox competitors), Tech (how it's built in Roblox), Production (your own WIP vs ref).
- Never ship traced or copied assets. References are for *understanding*. See IP notes in [[Commissioning and Briefing Artists]].

## Why it matters for anime battlegrounds
The genre is crowded and players compare instantly. Reference work tells you what "feels like anime" in measurable terms (2-frame flash, 3 colour blocks, 0.25 s slash) so you can brief artists precisely and judge their output against something concrete.

## How to do it

### Step 1: Set up the board structure
```
PureRef boards/
  00_Goal.pur          <- one-sentence goals per board
  10_Style_Anime.pur   <- key frames from the anime you're evoking
  20_Genre_Roblox.pur  <- TSB / JJS / Heroes BG / Type Soul screenshots
  30_Tech_Roblox.pur   <- DevForum images, Studio screenshots, property panels
  40_Characters/<name>.pur
  50_VFX/<move>.pur
  60_Maps/<map>.pur
  90_WIP_vs_Ref.pur    <- your screenshots side by side with the target
```
PureRef features to use: canvas drag-and-drop, alignment and grouping, text notes, desaturate toggle for value checks, export the board as an image to share in a brief, always-on-top over your 3D app.

### Step 2: Capture sources
| Source | What for | Tip |
|---|---|---|
| Your own gameplay capture (OBS, 60 FPS) | Roblox-specific timing, VFX lifetimes, UI | Step frame by frame in a video player; 1 frame = 16.7 ms |
| Sakugabooru | Anime effects animation, smears, impact frames | Use 0.2× speed and frame step; note the animator tag |
| Official anime screenshots / key visuals | Colour scripts, lighting moods | Collect 3–5 per mood, not 50 |
| ArtStation / X portfolios | Stylized modelling, hand-painted texture, VFX breakdowns | Save the artist handle and URL on the board |
| DevForum showcases | How it's done *inside Roblox* | Record the thread URL next to the image |
| Roblox Creator Store / Talent Hub portfolios | Market quality bar | See [[Public Roblox Artist Portfolios]] |

> [!tip] Always record the source URL next to the image
> When you later write a brief or a vault note, you'll need it, and it keeps you honest about what's inspiration and what's someone else's asset.

### Step 3: The 5-pass screenshot breakdown
Do this on a duplicate of the screenshot, as layers in Photoshop or Krita (or annotations in PureRef):

1. **Silhouette pass**: fill characters and key props black on white. Count the recognisable shapes. Can you name each?
2. **Value pass**: desaturate. Where are the darkest darks and lightest lights? Is the focal point (the hit) the highest contrast?
3. **Palette pass**: colour-pick 5–12 swatches: world vs character vs VFX. Note the hex values and roughly how much of the screen each covers.
4. **Lighting pass**: draw arrows for key light, rim and bounce. Is the shading painted or real-time? Hard or soft shadow edge?
5. **Density pass**: circle the high-detail areas. Detail should cluster at the focal point and fall off elsewhere.

Write a 3-line summary per screenshot:
```
TSB heavy punch, frame 4: white flash 2f, crater debris 0.6s, map saturation low;
VFX core value 95, world 40-60; only 3 colours on screen besides UI.
Takeaway: our flash is 6f, cut to 2-3f.
```

### Step 4: Motion breakdown (VFX and animation)
For every reference move, record:

| Field | Example |
|---|---|
| Anticipation frames | 6f (0.1 s) |
| Active / contact frame | f7 |
| Hitstop | 3–5f freeze |
| Flash / impact frame | 2f white, 1f black |
| Main shape lifetime | Slash mesh 0.2 s |
| Secondary FX | Dust ring 0.5 s, debris 1 s |
| Camera | Shake 0.2 s, FOV +5° |

These feed directly into [[Anime Combat Animation Timing]] and [[Anime VFX Fundamentals]].

### Step 5: Turn references into a style guide
A one-page style sheet per project:
- 3 "north star" frames (anime) + 3 genre frames (Roblox)
- Master palette (8–12 world, energy colours separate)
- Shape rules ("3–7 hair spikes", "weapons 1.2× scale")
- Lighting preset values (see [[Anime Color and Lighting Theory for Games]])
- Do / Don't pairs from the WIP vs Ref board

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Capture FPS | 60 | 1 frame = 16.7 ms timing precision |
| Refs per mood | 3–5 | Focus beats volume |
| Palette swatches per breakdown | 5–12 | Enough to see the structure |
| Sakugabooru min speed | 0.2× + frame step | Smear and impact frame study |

## Checklist
- [ ] PureRef installed; board folder structure created
- [ ] Each board has a written one-sentence goal
- [ ] Source URL and artist handle attached to every image
- [ ] 5-pass breakdown done on at least 10 genre screenshots
- [ ] Motion table filled for the 5 most important moves
- [ ] One-page style sheet exported and shared with the team or artists

## Common Mistakes
- Hoarding 500 images with no question attached.
- Only collecting anime stills, never Roblox competitor frames (you need both: target and constraints).
- Breaking down colour without value.
- Losing source links, then being unable to credit or check them.
- Treating references as assets to trace or rip (IP and ToS risk).

## Related
- [[Shonen Anime Shape Language]]
- [[Battlegrounds Visual Language Analysis]]
- [[Anime Color and Lighting Theory for Games]]
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]
- [[Commissioning and Briefing Artists]]
- [[Public Roblox Artist Portfolios]]

## Sources
1. PureRef – Support/download page (pay what you want): https://pureref.com/support_us.php
2. CG Channel – PureRef 2.0 / commercial licensing (May 2024): https://www.cgchannel.com/tag/pureref-2-0
3. AlternativeTo – PureRef overview (platforms, offline): https://alternativeto.net/software/pureref/
4. DevForum – PureRef: Amazing Canvas Tool: https://devforum.roblox.com/t/pureref-amazing-canvas-tool/1096817
5. Gwern mirror – 2024 paper on anime study referencing Sakugabooru: https://gwern.net/doc/anime/2024-tai.pdf
6. Hugging Face – sakugabooru2025 dataset (site description and scale): https://huggingface.co/datasets/trojblue/sakugabooru2025
7. Sakuga-42M dataset page: https://zhenglinpan.github.io/sakuga_dataset_webpage
8. Sakuga Mobile (App Store; player features): https://apps.apple.com/us/app/sakuga-mobile/id1530701238
9. Riot – League VFX style guide (readability first): https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/
