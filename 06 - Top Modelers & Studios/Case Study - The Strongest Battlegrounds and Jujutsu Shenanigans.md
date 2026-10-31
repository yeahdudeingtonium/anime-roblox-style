---
tags: [case-study, battlegrounds, tsb, jjs, heroes-battlegrounds, studios]
updated: 2026-10-31
sources: 16
status: draft
---
# Case Study - The Strongest Battlegrounds and Jujutsu Shenanigans

## TL;DR
- **The Strongest Battlegrounds (TSB)**, by the **Yielding Arts** group (verified account `22freshfrenchfries`), released 2023 and One Punch Man-inspired, is widely credited with **creating the "battlegrounds" sub-genre**: short-match, arena-style anime PvP. It sits at ~17–19 B visits, and was nominated twice at the 2024 Roblox Innovation Awards.
- **Jujutsu Shenanigans (JJS)**, by **Tze** (public handle) and JJK-inspired, is the main challenger: ~6.4–7.7 B visits, a ~338K CCU peak days after a 2026-03-20 update, and a scare when Roblox briefly removed it on 2025-07-21 (Tze attributed it to an external link; restored about 4 h later).
- **Heroes Battlegrounds**, by the "more awesome games yo" group and MHA-inspired, released 2023-04-11 and follows the same template.
- The template: **simple arena + moveset-driven characters + dense VFX + frequent "new character / new move" updates + skill-based (not pay-to-win) combat**, built for **~20-minute sessions**.
- **Public art-pipeline information is essentially nil.** No interviews, credits pages or GDC/RDC talks from these teams turned up. Everything about *how* their art is made is inferred; see the warnings.
- Lesson for you: these games prove **VFX + animation + update cadence beat environment fidelity**. Build the combat-feel pipeline first.

## Why it matters for anime battlegrounds
These are the reference games every player compares you to. Knowing what's documented (and what's just community lore) stops you from chasing myths and focuses you on the observable success factors.

## What's documented

### The Strongest Battlegrounds
| Fact | Detail | Source quality |
|---|---|---|
| Owner | Yielding Arts group; verified account `22freshfrenchfries` | Fan wiki |
| Lead developer | Fan wiki says the account holder formerly went by "Cronigod" | Fan wiki; **unverified** |
| Release / theme | 2023; One Punch Man-inspired (Saitama-like "Strongest Hero" moveset) | Multiple guides |
| Genre role | Credited with popularising the battlegrounds sub-genre | RoWatcher analysis |
| Awards | Nominated twice at the Roblox Innovation Awards 2024; Bloxy News reported an award for "Best Strategy Experience" with 1.6M votes | Fan wiki + Bloxy News (X) |
| Visits | ~17.2–19.1 B (tracker snapshots, 2026) | Trackers |
| CCU | All-time peak reported as 613.6K / 1M (2026-05-16) / 1.4M by different trackers; 2026 day-to-day ~33K–83K | Trackers, conflicting |
| Studio portfolio | Yielding Arts has published 14 games; TSB accounts for virtually all its players | RoWatcher |
| In-game tooling | A private-server "Skill Builder V2" lets players combine existing skills, animations and effects into custom moves | Guide site |

> [!warning] Unverified
> The fan wiki also claims the developer said updates slowed because of a broken hand and college. Treat this as community lore. The "Best Strategy Experience" award wording comes from a Bloxy News post; I couldn't confirm it on Roblox's own Innovation Awards page.

### Jujutsu Shenanigans
| Fact | Detail | Source quality |
|---|---|---|
| Developer | Tze (public handle) | Multiple guides |
| Theme | Jujutsu Kaisen-inspired | Multiple |
| 2025-07-21 removal | Temporarily removed; Tze attributed it to an external link in the game; restored about 4 h after devs started communicating | Deltia's Gaming |
| 2026 peak | ~338,296 CCU two days after a 2026-03-20 update ("Disaster Plants") | RoWatcher |
| Visits | 6.4 B (Profitable, 2026-07-21) to 7.7 B (Rotrends variant) | Trackers |
| Peak CCU (trackers) | 628.2K–694.5K reported | Rotrends, conflicting |
| Ranked arena | Square grass field, invisible borders, 4 spawn points | Map guide (PT) |

> [!warning] Unverified
> Profiles describing Tze as a teenage solo dev who does "scripting, VFX and animation", and who is building a Demon Slayer game called "Rogue Demon", come from shapes.inc pages that look like AI-generated personas. Don't cite them.

### Heroes Battlegrounds
- Developer: the "more awesome games yo" group in most sources (outliers name others). Release 2023-04-11 per Rotrends.
- A VFX artist's portfolio (Khan VFX carrd) lists "Heroes Battlegrounds" among the games worked for. That suggests the team uses **freelance or contract VFX artists**, a common genre pattern. *(Portfolio self-claim; verify with the artist.)*

## What can be inferred about how they're built
> [!warning] Unverified
> The following comes from gameplay observation and from the general patterns in [[Top Roblox Modeler Workflow Patterns]], **not** from statements by these teams. Use it as a hypothesis to check against your own captures.

| Area | Likely approach | What you should do |
|---|---|---|
| Characters | Player avatars or simple rigs, with identity carried by moveset and VFX | Decide early: avatar-based or custom bodies (see [[Shonen Anime Shape Language]]) |
| Maps | One open, low-detail arena; destructible debris on heavy hits | Grey-box for combat distances; see [[Stylized Environment Kits]] |
| VFX | Dense, short-lived ParticleEmitters, mesh slashes, flash/impact frames, camera shake | Budget per move; see [[Anime VFX Fundamentals]] |
| Animation | Snappy anticipation → contact → hitstop; heavy use of ragdoll knockback | See [[Anime Combat Animation Timing]] |
| Lighting | Neutral daylight baseline; temporary darkening and tints during ultimates | See [[Lighting for Anime Maps]] |
| Team | Small core + commissioned VFX, animation and modelling | See [[Commissioning and Briefing Artists]] |
| Cadence | New character or moveset drops, seasonal events, limited cosmetics | Plan a content pipeline, not a one-shot launch |

## Why they won (documented analysis)
RoWatcher's genre analysis credits:
1. **Skill over spending**: "the skill ceiling is skill — not currency", unlike grind RPGs (Blox Fruits).
2. **Short sessions**: "20 minutes of pure combat" alongside longer RPGs.
3. **Update cadence**: frequent new characters, seasonal events, time-limited cosmetics.
4. **Risk**: most run as fan projects under "informal publisher tolerance" (IP risk), and genre fatigue is concentrating discovery on a few leaders.

## Lessons for your project
- Spend the art budget on **moves** (VFX + animation + SFX); keep the arena simple.
- Ship with a **pipeline for new movesets every few weeks**: briefs, freelancers, a reusable VFX library.
- **Avoid external links and policy risks** in-game. JJS's removal shows a single violation can take a mega-game offline.
- Use **original** characters, or be prepared for IP risk.

## Numbers & Settings
| Metric | TSB | JJS |
|---|---|---|
| Release | 2023 | not confirmed by a source |
| Visits (2026) | ~17–19 B | ~6.4–7.7 B |
| Peak CCU (reported) | 613.6K–1.4M (conflicting) | ~338K (2026, news) to 694.5K (tracker) |
| Studio | Yielding Arts | Tze |

## Checklist
- [ ] Capture 10 min of TSB + JJS gameplay at 60 FPS and break down 5 moves each ([[Reference Gathering and Screenshot Breakdown]])
- [ ] Write down the avatar-vs-custom-character decision
- [ ] Draft a 6-week moveset release cadence
- [ ] List policy risks (external links, IP names) and remove them
- [ ] Recruit VFX and animation freelancers before launch, not after

## Common Mistakes
- Citing fan-wiki or AI-persona pages as fact about these developers.
- Copying the One Punch Man or JJK names and assets 1:1.
- Building a detailed map before the combat feels good.
- Assuming the leaders have big art teams. Their edge is focus and cadence.

## Related
- [[Battlegrounds Visual Language Analysis]]
- [[Case Study - Studio-Scale and Licensed Anime Games]]
- [[Top Roblox Modeler Workflow Patterns]]
- [[Public Roblox Artist Portfolios]]
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]
- [[Lighting for Anime Maps]]

## Sources
1. Roblox Fandom – Yielding Arts: https://roblox.fandom.com/wiki/Yielding_Arts
2. Roblox Fandom – 22freshfrenchfries: https://roblox.fandom.com/wiki/Player:22freshfrenchfries
3. Bloxy News on X – TSB Innovation Award post: https://x.com/Bloxy_News/status/1810357961807769996
4. RoWatcher – TSB and the anime fighter revolution: https://rowatcher.com/news/the-strongest-battlegrounds-how-one-punch-man-sparked-roblox-s-anime-fighter-revolution
5. RoWatcher – Why Anime Battlegrounds Are Taking Over Roblox in 2026: https://rowatcher.com/news/why-anime-battlegrounds-are-taking-over-roblox-in-2026
6. RoWatcher – TSB stats: https://rowatcher.com/games/3808081382
7. Rotrends – TSB: https://rotrends.com/game/3808081382
8. Bloxodes – TSB stats: https://bloxodes.com/stats/games/the-strongest-battlegrounds-3808081382
9. All Things How – Skill Builder V2 in TSB: https://allthings.how/skill-builder-v2-in-the-strongest-battlegrounds-how-it-works/
10. Deltia's Gaming – What Happened to Jujutsu Shenanigans? Developer Gives Update: https://deltiasgaming.com/?p=291826
11. RoWatcher – JJS surges past 338K peak players: https://rowatcher.com/news/jujutsu-shenanigans-surges-past-338k-peak-players-after-disaster-plants-update
12. Rotrends – Jujutsu Shenanigans: https://rotrends.com/game/3508322461
13. Profitable – Jujutsu Shenanigans: https://profitable.app/roblox/games/jujutsu-shenanigans
14. Critical Hits – JJS map locations: https://criticalhits.com.br/dicas/jujutsu-shenanigans-todos-os-locais-do-mapa/
15. Rotrends – Heroes Battlegrounds: https://rotrends.com/game/4568630521
16. Khan VFX portfolio (lists Heroes Battlegrounds): https://khanvfx.carrd.co/
