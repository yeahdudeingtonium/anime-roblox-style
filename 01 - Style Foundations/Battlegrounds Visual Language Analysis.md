---
tags: [style, analysis, battlegrounds, reference-games, ui, vfx, lighting]
updated: 2026-10-31
sources: 16
status: draft
---
# Battlegrounds Visual Language Analysis

## TL;DR
- The top battlegrounds games (The Strongest Battlegrounds, Jujutsu Shenanigans, Heroes Battlegrounds) win on **combat feel and VFX, not environment fidelity**. Their maps are simple, open and readable, and the "anime" lives in the moves.
- Shared formula: **simple, low-detail arena + Roblox avatars or simple characters + very dense, short-lived, high-contrast VFX + snappy animation + minimal HUD**. Short sessions ("20 minutes of pure combat") and frequent move-drop updates drive the genre.
- **VFX density is the art budget**: white/black flash frames, screen shake, slash meshes, debris and craters carry each hit. The environment stays low-contrast so effects read on top.
- **Lighting is plain on purpose**: bright neutral daylight with mild saturation, so VFX colours (blue, purple, red, gold) separate from the world.
- **UI is thin**: a health bar, a 4-slot move hotbar with cooldown sweep, an ultimate/awakening meter, and kill-feed or combo text. Phone-first layouts with big touch targets.
- Treat everything under "Observed patterns" as **visual analysis to verify in-game**. Public written breakdowns by these studios don't exist.

## Why it matters for anime battlegrounds
If you copy the wrong layer (for example, building a 4K photoreal Tokyo map), you spend months on what players don't value and lose frame rate on the phones most of them use. The genre leaders show where the art budget should go: **moves first, map second**.

## The games and what is publicly known
| Game | Developer (public) | Source-backed facts | Scale (tracker snapshots, conflicting) |
|---|---|---|---|
| The Strongest Battlegrounds (TSB) | Yielding Arts group; verified account `22freshfrenchfries` | One Punch Man-inspired; released 2023; credited with popularising the battlegrounds sub-genre; nominated twice at Roblox Innovation Awards 2024 | ~17–19 B visits; all-time peak CCU reported as 613.6K, 1M and 1.4M by different trackers |
| Jujutsu Shenanigans (JJS) | Tze (public handle) | JJK-inspired; temporarily removed 2025-07-21 over an external link, restored about 4 h later; ~338K CCU peak after a 2026-03-20 update | 6.4–7.7 B visits |
| Heroes Battlegrounds | "more awesome games yo" group (most sources) | MHA-inspired; released 2023-04-11 | — |
| My Hero Academia Battlegrounds / Ultimate | Gamefam + Crunchyroll (licensed) | Launched Dec 2023 as the first officially licensed AAA anime on Roblox | — |

Details and further studios: [[Case Study - The Strongest Battlegrounds and Jujutsu Shenanigans]] and [[Case Study - Studio-Scale and Licensed Anime Games]].

## Observed patterns (verify in-game)
> [!warning] Unverified
> The tables below are visual analysis of how these games commonly look in gameplay videos, not statements from the developers. Before relying on any row, record your own clips and check it frame by frame (see [[Reference Gathering and Screenshot Breakdown]]).

### Map style
| Trait | Typical pattern | Why it works |
|---|---|---|
| Layout | One mid-size open arena: flat grass/city ground, a few buildings, trees, hills/rocks at the edges | Fights travel fast and far (knockback, dashes); obstacles are for ragdoll impacts |
| Detail level | Low-to-mid poly, mostly default Roblox materials or simple textures | Keeps draw calls low with 15–30 players plus VFX |
| Destruction | Craters, debris parts and temporary terrain damage on big hits | Gives "anime impact" without a detailed map |
| Palette | Desaturated greens/greys/concrete | Lets saturated VFX dominate |
| Landmarks | 2–4 big recognisable shapes (tower, mountain, building cluster) | Orientation in chaotic fights |

A Portuguese JJS map guide describes the ranked arena as **a square grass field with invisible borders and four spawn points**, an example of how minimal these spaces are.

### Character style
- Character identity is carried by **moveset, VFX colour and animation**, not by unique high-poly anime bodies (see the warning about avatars in [[Shonen Anime Shape Language]]).
- Where custom meshes appear (weapons, hair, transformations, summons), they are **simple, chunky shapes** with flat or lightly textured colour, often `Neon` for energy parts.

### Lighting
- Bright daytime sun, moderate ambient, little fog: a "readable" default.
- Mild ColorCorrection (community cartoon values: contrast about 0.1, saturation 0.1–0.3), with no heavy bloom on the world.
- Drama is added **temporarily** by abilities: screen darkening, colour inversion, tinted ColorCorrection during ultimates and domains, then a return to baseline. Full guide: [[Lighting for Anime Maps]].

### VFX density
| Layer | Typical duration | Role |
|---|---|---|
| Hit spark / flash | 1–3 frames (about 0.03–0.1 s) | Contact confirmation |
| Impact frame (white/black inversion) | 2–6 frames | Anime "sakuga" punch, used on heavies and finishers |
| Slash/crescent mesh | 0.1–0.3 s | Shape of the attack |
| Shockwave rings, dust, debris | 0.3–1.0 s | Weight and ground contact |
| Aura / awakening | Persistent while active | State readability |
| Camera shake + FOV punch | 0.1–0.4 s | Felt impact |

Fundamentals and budgets are in [[Anime VFX Fundamentals]]. Timing (hitstop, anticipation) is in [[Anime Combat Animation Timing]].

### UI
- Health bar (often top-centre or bottom-centre), a **4-ish move hotbar** with cooldown radial or fill, an ultimate/awakening bar, and kill feed.
- Big, high-contrast move names with Japanese-poster-like typography for ultimates.
- Mobile layout: hotbar near the right thumb, jump/dash buttons big.

## What to copy vs what to avoid
| Copy | Avoid |
|---|---|
| Simple readable arena, strong landmarks | Over-detailed photoreal map |
| Saturated VFX on a muted world | Saturated world that competes with VFX |
| Short, punchy effects (<1 s) with flash frames | Long-lived particle soup that hides the hit |
| Temporary lighting shifts for ultimates | Permanent bloom/sun-rays/DOF |
| Clear 4-slot UI | Busy HUD with many currencies on screen |
| Original names and designs (see IP note) | Direct copies of trademarked characters and names |

> [!warning] IP risk
> RoWatcher notes that most of these games run as fan projects "under informal publisher tolerance", which creates licensing risk. When Gamefam's official MHA game launched, several fan-made MHA games were reported (allegedly) removed by DMCA. Design original characters that *evoke* shonen archetypes. See [[Commissioning and Briefing Artists]].

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| Players per server | 15–30 typical (observed) | Plan your VFX budget per player |
| Baseline ColorCorrection | Contrast 0–0.1, Saturation 0.1–0.3 | Forum cartoon consensus |
| Bloom | Default (0.4 / 24 / 0.95) or off for the world | Save glow for VFX |
| Hit flash | 1–3 frames | Readable without blinding |
| Big VFX lifetime | ≤1 s | Clears the screen for the next exchange |
| Scene draw-call budget | <600 draw calls, <650K tris in busy areas | DevForum optimisation checklist (it says the figure mirrors Roblox docs; see [[Mobile-Aware Stylization]]) |

## Checklist
- [ ] Record 5 min of gameplay from TSB, JJS and Heroes BG; screenshot 20 frames each
- [ ] Measure: how many on-screen colours does the map use vs the VFX?
- [ ] Build a grey-box arena with 2–4 landmarks before any detailing
- [ ] Define a baseline lighting preset and 2–3 "ultimate" lighting overrides
- [ ] Draft a 4-slot HUD and test it on a phone at 100% scale
- [ ] Make a list of original character concepts that avoid trademarked names and designs

## Common Mistakes
- Thinking the map is the product. In this genre it's a stage.
- Matching the world's saturation to the VFX, so nothing pops.
- Copying names and character designs 1:1 from a licensed anime.
- Adding Future lighting plus many dynamic lights to every move on a 30-player server (see [[Mobile-Aware Stylization]]).
- Forgetting that the effects have to read from 30+ studs away on a phone screen.

## Related
- [[Shonen Anime Shape Language]]
- [[Anime Color and Lighting Theory for Games]]
- [[Lighting for Anime Maps]]
- [[Stylized Environment Kits]]
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]
- [[Case Study - The Strongest Battlegrounds and Jujutsu Shenanigans]]
- [[Reference Gathering and Screenshot Breakdown]]

## Sources
1. Roblox Fandom – Yielding Arts: https://roblox.fandom.com/wiki/Yielding_Arts
2. Bloxy News on X – TSB Innovation Awards post: https://x.com/Bloxy_News/status/1810357961807769996
3. RoWatcher – "The Strongest Battlegrounds: How One Punch Man Sparked Roblox's Anime Fighter Revolution": https://rowatcher.com/news/the-strongest-battlegrounds-how-one-punch-man-sparked-roblox-s-anime-fighter-revolution
4. RoWatcher – "Why Anime Battlegrounds Are Taking Over Roblox in 2026": https://rowatcher.com/news/why-anime-battlegrounds-are-taking-over-roblox-in-2026
5. RoWatcher – TSB game stats: https://rowatcher.com/games/3808081382
6. Bloxodes – TSB stats: https://bloxodes.com/stats/games/the-strongest-battlegrounds-3808081382
7. Rotrends – Jujutsu Shenanigans: https://rotrends.com/game/3508322461
8. RoWatcher – "Jujutsu Shenanigans Surges Past 338K Peak Players": https://rowatcher.com/news/jujutsu-shenanigans-surges-past-338k-peak-players-after-disaster-plants-update
9. Deltia's Gaming – What happened to Jujutsu Shenanigans (2025 removal): https://deltiasgaming.com/?p=291826
10. Critical Hits – Jujutsu Shenanigans map locations (arena description): https://criticalhits.com.br/dicas/jujutsu-shenanigans-todos-os-locais-do-mapa/
11. Rotrends – Heroes Battlegrounds: https://rotrends.com/game/4568630521
12. Gamefam – anime page (first official AAA anime license): https://gamefam.com/anime
13. Pocket Tactics – Three giant Roblox games disappear in potential DMCA battle: https://www.pockettactics.com/anime-adventures/private
14. DevForum – Cartoon lighting settings (contrast 0.1 / saturation 0.3): https://devforum.roblox.com/t/cartoon-lighting-settings/333686
15. Roblox Creator Hub – Design for performance: https://create.roblox.com/docs/performance-optimization/design ; DevForum – Checklist for building optimization: https://devforum.roblox.com/t/checklist-for-building-optimization/3232350
16. Riot – League VFX style guide: https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/
