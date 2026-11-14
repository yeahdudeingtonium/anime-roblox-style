---
tags: [market-research, ideas, verdict]
updated: 2026-11-14
sources: 3
status: draft
---
# Market Check: Hatch Animals That Fish

**The idea (the owner's):** hatch animals from eggs, and the animals fish for you.
**The question:** is there a market, is the lane open, and can it succeed? (Market research only; no design.)

All data is live from `tools/roblox_intel.py` and the RoWatcher history API on 2026-11-14 (Saturday). Raw data: `Data/sweep-fishing-2026-11-14.json` (325 games).

## Verdict
**Yes, it can succeed. It's one of the stronger lanes found so far,** because three things line up that rarely do:
1. **The genre is huge and evergreen**, not a wave that will close.
2. **The exact concept is unclaimed.**
3. **The core mechanic, "your crew does the verb", is proven** by a durable hit in another genre.

**Realistic outcome range** (judgement, based on the comparables below):

| Case | CCU | Looks like |
|---|---|---|
| Bad | < 500 | Plays like the generic fishing launches (85% of new fishing games sit under 1K) |
| Base | 1–5K | Ro-BassFishing 2.9K, Shoot That Fish 2.2K, BRO FISHING 1.3K |
| Good | 10–20K, durable | My Anime Mine's curve (slow build to 10K around day 50, then a 14–20K plateau) |

It's not a quick-spike idea. If it works, it should build slowly and *hold*, which is the better kind of success.

## Evidence for

### 1. The genre is big and doesn't expire
- **140 fishing games hold about 248K live CCU between them.**

  | Game | Live CCU | Age |
  |---|---|---|
  | Fisch | 70K | 975 d |
  | Fish It! | 65K | 754 d |
  | Net a Fish! | 32K | 29 d |
  | Harpoon a Fish | 14.8K | 77 d |
  | Heavyweight Fishing | 11.5K | 467 d |
  | Ice Fishing Simulator | 8.8K | 1,194 d |
  | Sell a Million Sushi | 8.3K | 32 d |

- **The trends are stable, not a dying wave.**
  - **Fisch** holds about 75K and spikes to about 430K on its monthly update days (Sep 5, Oct 3, Oct 31).
  - **Fish It** is easing (125K → 66K since August) but is still huge.
  - **Heavyweight** holds 11–18K.
  - **Net a Fish!** is still climbing: 3.2K (Nov 1) → 41K (Nov 13).
- In the [[Mutation Playbook]], **evergreen genres have no deadline**. Harpoon a Fish launched when Fish It was 676 days old and still hit 14.8K.

### 2. The exact concept is open
- About 15 phrasings were searched ("hatch pets that fish", "pets fish for you", "fishing pets", "pet fishing", "hatch a fisher", "fishing crew", "my pet fishery"…). **No game has hatched animals doing the fishing.**
- **The two lookalikes are the opposite idea, and they flopped:**
  - *[🐟] My Fishing Animals*: 0 CCU, 0 peak ever, 95 days old.
  - *[🐟] Fish Animals!*: 15 CCU, 12 days old.

  In both, *you* fish and *animals are the catch*. That's a noun swap on the Throw Food For Animals template, which this data shows is a graveyard. Their failure says nothing against animals fishing *for* you.
- *Net a Fish!* lists "helpers" as one upgrade line and pet crates as boosts. The player still does the fishing. It's the closest neighbour, and the biggest competitive risk (see below).

### 3. "Your crew does the verb" is proven and durable
| Game | Verb the helpers do | Live CCU | Curve |
|---|---|---|---|
| **My Anime Mine** | anime crew breaks rocks | 16–17K, 99% likes, 86 d | 109 → 24K peak; **14–20K plateau for 6 weeks** |
| **Bee Swarm Simulator** | bees collect pollen | 36.5K at **8.6 years old** | the original helper loop |
| Train Pets for Eggs | pets train on a treadmill | 5.1K, 46 d | — |

- In [[Mutation Playbook]] terms this is a **SOURCE/helper change** on the fishing genre, plus a **REWARD graft** (egg hatching, the most proven reward on Roblox, from Steal An Egg at about 960K). As supporting changes, SOURCE changes reached 10K 83% of the time and RISK changes 86% (rates inflated by search bias, so read them as rankings).
- Hatching plus the rarity roll gives every action a **reveal**, which is the playbook's fun principle 2.

## Evidence against (the real risks)

| # | Risk | Evidence | How serious |
|---|---|---|---|
| 1 | **The genre is crowded at the bottom.** | 58 fishing games launched in the last 90 days; only 9 (15%) are at 1K+ and 2 at 10K+. The winners each had a distinct verb or tool (net, harpoon, shoot) or a graft (selling sushi). | High: being "another fishing game" fails |
| 2 | **Net a Fish! could add this.** | It already has helpers and pet crates, it's still rising (41K), and its dev updates constantly. If it makes helpers the core, this lane closes. | High: speed matters even though the genre is evergreen |
| 3 | **Passive core vs. the algorithm.** | Roblox's Recommended for You weighs **first-play bounce under 60 s** heavily ([[Roblox Discovery Algorithm]]). If the player just watches pets fish, early bounce rises. My Anime Mine passes this, so it's solvable, but it's the #1 execution risk. | Medium-high |
| 4 | **Title confusion with a flop.** | "My Fishing Pets" reads almost exactly like the dead *My Fishing Animals* (0 CCU) and *My Fishing Brainrots* (127). | Low, if the title says the hatch-and-helper part explicitly |
| 5 | **16+ launch gate.** | New games reach only age-checked 16+ players until 250 highly engaged players. Cute pets plus fishing needs to look fun to teens, not babyish. | Medium |

## What it must get right to succeed (requirements, not design)
1. **Pets fishing must be visibly different from "player fishing with a pet buff"**, or it reads as one more fishing game (risk 1).
2. **Something to do in the first 60 seconds** besides watching, to keep bounce down (risk 3).
3. **Ship fast**, before Net a Fish or another studio makes helper fishing the core (risk 2). There's no seasonal deadline, but there is a competitor clock.
4. **A title that names both halves** (hatching or pets + fishing for you), and isn't a "My Fishing ___" title.

## Bottom line
- **Market:** yes. It's an evergreen, top-5-sized genre with about 248K live CCU.
- **Lane:** open. Nobody does it; the lookalikes are the inverse idea and failed for unrelated reasons.
- **Proven mechanics:** yes. Helper-does-the-verb (My Anime Mine, Bee Swarm) plus hatching (Steal An Egg).
- **Can it succeed:** yes. Base case 1–5K, good case a durable 10–20K. The main risks are execution (passive first minute, standing out in a crowded genre) and speed versus Net a Fish!. They are not risks of demand.

## Related
[[Mutation Playbook]] · [[Idea Judgement Rules]] · [[Roblox Discovery Algorithm]] · [[Growth Curves and Timing]] · [[Mutation Shortlist 2026-11-14]]
