---
tags: [meta, handoff]
updated: 2026-10-31
status: solid
---
# Handoff: where we left off (2026-10-31)

Read this first in any new session. Then read [[Owner Decisions]] and [[Idea Judgement Rules]].

## What exists
- **Art-bible vault** (sections 01–07): anime style, characters, environments, VFX, animation, top modelers, core loops.
- **Market research** (08): [[Idea Judgement Rules]] (the living rulebook), [[Roblox Discovery Algorithm]], [[Live Pattern Report 2026-10-31]], [[Growth Curves and Timing]], [[Idea Ledger Round 1]], [[Idea Ledger Round 2 - Young Waves]].
- **Tool:** `tools/roblox_intel.py` gives live Roblox search, charts, sweeps and game stats. It needs only Python 3.
  - Windows: `python tools\roblox_intel.py search "roll a snowball"`
  - The RoWatcher history API also works: `https://rowatcher.com/api/v1/games/<universeId>/history?from=2025-12-01`
- **The owner has their own scraper and data** (location unknown). Merge it into `08 - Market Research/Data/` when found.

## Current decision in progress
The owner likes **Roll a Snowball** (December timing) and is open to **Kick to Escape**. They asked **how each would be played**. Next step: write a full game-design spec for both into `09 - Game Designs/`. Cover the core loop, controls, the first 60 s, the minute-3 goal, progression, the risk lever, monetization and the MVP scope, and score each on the 10-point test.

### Evidence gathered for Roll a Snowball (2026-10-31)
- **Reference loop:** *roll the world* (6.1K CCU, 25 days old) is a roll-up game. Anything smaller sticks to your ball; grow bigger to roll up bigger things; "stars" act as rebirth; there's a PvP storm mode at size 50; and rarity finds (golden, diamond, rainbow).
- **Last winter's analogue:** *[PETS] Roll a Snowball* (universe 9410341657) launched **Dec 23, 2025**, late, and still **peaked at 3.1K CCU**, 2.5M visits, 97.2% rating (RoTrends). It's dead now; an October revival test peaked at 111.
- **Current snowball titles are near 0 in October:** +1 Roll a Snowball! 0, +1 Snowball Rolling 4, Be a Snowball! 0. That's expected off-season. A December launch is a timing bet.
- **Risk:** it's a theme swap of *roll the world* (rule 6). The hedge is the season, a fresh verb mix (roll + build a snowman / snowball fight) and an early-December launch (live by Dec 12–15).

### Evidence for Kick to Escape
- **Reference:** *Punch to Escape!* (7.1K CCU, 14 days old). Punch through prison walls → vacuum up rubble → sell it to your cellmate → buy upgrades and robots. The risk lever is guards searching.
- **Also:** *Escape The Walls* (8.5K, 19 days), a 1–4 player co-op wall-smash incremental, room after room.
- **Open title:** the only near match is Kick Door To Escape (303 CCU, 336 days old). Needs a build of 3 weeks or less to land in the clone window.

## Rules of thumb (short version)
Success markers: 1K CCU = worked, 10K = hit. Change the verb, keep the reward; noun-swap copies die (Fake a Pet 12, Sell Popcorn 186). Waves peak around day 32 with a ~12-day half-life. New games reach only 16+ players until 250 highly engaged players. Ship on Fridays.
