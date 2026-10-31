---
tags: [market-research, autopsy, live-data, title-grammar, core-loop]
updated: 2026-10-31
sources: 4 live sweeps (Roblox omni-search + games API), 20 game descriptions
sample: 1336 unique games created ≤120 days ago, from 150 search phrases
status: draft
---
# Live Pattern Report: 2026-10-31

> [!info] Data
> - **Sweeps** (all in `08 - Market Research/Data/`):
>   - `sweep-verbs` (30 phrases, 395 games)
>   - `sweep-verbs2` (40 phrases, 524 games)
>   - `sweep-themes` (40 phrases, 402 games)
>   - `sweep-grammar` (40 phrases, 478 games)
> - **Combined sample:** 1336 unique games, each created ≤120 days ago.
> - **Baseline:** **23% ≥1K CCU** (313 games) and **4% ≥10K** (48 games). Median CCU is 139.
> - **Success markers:** ≥1K live CCU = it worked. ≥10K = a hit.

## TL;DR
1. **Keep the game alive, then worry about the title.** Updates and likes predict success far better than any title pattern. Games updated today hit 1K **38%** of the time. Games last updated 15 or more days ago hit **4%**. Games at ≥93% likes hit **37%**, against **9%** below 70%.
2. **Change the verb, not the noun.** In the egg wave, "[Verb] For Eggs" and "[Verb] to Steal" twists hit 1K **45%** of the time. Reskins that swap the noun ("Steal a [Adj] Egg") hit **33%** and produced zero 10K games. Putting a new verb on the egg itself ("Ride/Throw/Roll an Egg") hit only **17%**.
3. **The title verb is only a skin.** 14 of the 20 top movers we read share one backend: train (treadmill or pull-ups) → speed or strength → collect an egg or pet → the pet earns cash on your base (offline too) → rebirth.
4. **"+1" is saturated.** 221 games hit at **19%**, below the 23% baseline. "+1 X Per/Every Y" hits **11%**. Only "+1 X Evolution" (30%) and "+1 [body part]" still work.
5. **Anime is a style, not a hook.** 68 anime games hit at **24%**, the baseline. Anime wins only when it's bolted onto a roll, mine, steal or +1 loop: Anime Dice 60.8K, +1 Anime Eyes 31.3K, My Anime Mine 14K. Merge, guess, draw and card anime games went **0 for 16**.
6. **Winners show up in weeks 2–4.** No game 0–7 days old had reached 1K (0/12). The 22–30 day bucket peaks at **32%**. Games that haven't broken through by day 90 fade: the 91–120 day bucket is at **14%**.

---

## 1. Title grammar
| Structure | n | ≥1K | 1K% | ≥10K | 10K% | median CCU |
|---|---|---|---|---|---|---|
| **Build a/an …** | 16 | 9 | **56%** | 1 | 6% | 1266 |
| … to Escape | 6 | 3 | 50% | 0 | 0% | 748 |
| **… For Egg(s)** | 28 | 12 | **43%** | 1 | 4% | 947 |
| **Steal a/an …** | 53 | 19 | **36%** | 2 | 4% | 356 |
| … Tycoon | 15 | 5 | 33% | 0 | 0% | 425 |
| Don't … | 16 | 5 | 31% | 1 | 6% | 470 |
| [Verb] to [Verb] | 33 | 10 | 30% | 2 | 6% | 109 |
| [Verb] [Noun] For [Noun] | 20 | 6 | 30% | 1 | 5% | 236 |
| +1 X Evolution | 33 | 10 | 30% | 1 | 3% | 303 |
| … RNG | 14 | 4 | 29% | 0 | 0% | 108 |
| [Verb] and [Verb] … | 57 | 14 | 25% | 2 | 4% | 127 |
| [Verb] a/an [Noun] (2–4 words) | 260 | 60 | 23% | 6 | 2% | 146 |
| … Simulator | 18 | 4 | 22% | 1 | 6% | 106 |
| *Baseline* | *1336* | *313* | *23%* | *48* | *4%* | *139* |
| +1 … (any) | 221 | 41 | 19% | 7 | 3% | 145 |
| … Tower / TD | 62 | 12 | 19% | 3 | 5% | 206 |
| Ride a/an … | 12 | 2 | 17% | 1 | 8% | 139 |
| Be/Become a … | 20 | 3 | 15% | 0 | 0% | 139 |
| … Obby | 14 | 2 | 14% | 0 | 0% | 64 |
| Grow a … | 14 | 2 | 14% | 0 | 0% | 49 |
| **+1 X Every/Per Y** | 45 | 5 | **11%** | 2 | 4% | 38 |
| Escape … (as the first word) | 10 | 1 | 10% | 0 | 0% | 256 |

**Breakdown of "+1" titles:**

| "+1" sub-type | n | 1K% | ≥10K |
|---|---|---|---|
| Evolution | 33 | 30% | 1 |
| Forge/Loot | 21 | 24% | 0 |
| Body part (eyes, arm, tongue, tail, wings) | 14 | 21% | 2 |
| Escape | 57 | 14% | 0 |
| Per/Every | 49 | 12% | 2 |
| Speed/Strength/Jump | 48 | 10% | 0 |

**First word of the title** (only words with n ≥ 10):

| Verdict | First words (1K rate, games) |
|---|---|
| Strong | **build 48%** (25), **steal 38%** (79), troll 36%, don't 36%, my 31% |
| Dead | **merge 0/24**, stack 1/11, hatch 1/10, catch 1/14, kick 1/11, pull 1/11, idle 1/11, draw 1/15, grow 2/17, become 2/15 |

### Word count and decoration
| Feature | n | 1K% | 10K% | median CCU |
|---|---|---|---|---|
| 1 word | 17 | 29% | 6% | 608 |
| 2 words | 192 | 22% | **7%** | 108 |
| 3 words | 604 | 24% | 4% | 124 |
| 4 words | 341 | 25% | 2% | 167 |
| 5–6 words | 172 | 22% | 2% | 162 |
| 7+ words | 9 | **0%** | 0% | 69 |
| [bracket tag] | 582 | 29% | 4% | 187 |
| no tag | 754 | 19% | 3% | 107 |
| 🎃 in title | 278 | 31% | 6% | 234 |
| any emoji | 651 | 26% | 5% | 165 |
| no emoji | 685 | 21% | 2% | 115 |
| ends with "!" | 296 | 21% | 2% | 84 |
| "UPD" tag | 105 | 23% | 2% | 77 |

> [!warning] Confound
> Tags look like a +10 point lift, but most of that comes from the fact that active developers both tag and update. Among games updated ≤3 days ago, the gap shrinks:
> - bracket tag: 37% vs 32% without
> - 🎃: 38% vs 34% without (9% vs 5% at ≥10K)
>
> A seasonal tag is a small real bump at most. It is not a strategy.

## 2. Theme and noun waves (matched on the title)
| Theme | n | ≥1K | 1K% | ≥10K | median CCU |
|---|---|---|---|---|---|
| brainrot | 6 | 3 | 50% | 0 | 1032 |
| **egg** | 129 | 44 | **34%** | 6 | 369 |
| **animals** (cat, dog, horse, fish, bug) | 82 | 28 | **34%** | 6 | 233 |
| vehicle (car, bike, drive) | 49 | 16 | 33% | 4 | 127 |
| army/military | 14 | 4 | 29% | 0 | 105 |
| pet | 31 | 8 | 26% | 1 | 226 |
| venom/spider | 8 | 2 | 25% | 2 | 108 |
| **anime** | 68 | 16 | **24%** | 3 | 109 |
| prison/school/teacher | 14 | 3 | 21% | 0 | 154 |
| phone/keyboard | 48 | 9 | 19% | 1 | 162 |
| ninja/sword/assassin | 16 | 3 | 19% | 1 | 146 |
| food (fries, pizza, candy, chicken, eat, cook) | 80 | 14 | 18% | 3 | **38** |
| slime/squishy | 29 | 5 | 17% | 0 | 232 |
| aura | 13 | 2 | 15% | 0 | 133 |
| **dino/dragon/kaiju/titan** | 42 | 6 | **14%** | 1 | 170 |
| **halloween/pumpkin/ghost/zombie** | 93 | 13 | **14%** | **0** | **31** |

Notes:
- **Dragons and kaiju aren't pulling:** dragon 0/9, kaiju 1/14.
- **Slime is dead:** "slime" 0/12.
- **Pumpkin titles are dead:** 1/33. A seasonal word works as a tag, never as the theme.
- **Food is bimodal.** It has a few big hits (Sell Fries 46.7K, Cook the Chicken 15.7K, Sell a Million Sushi 9.2K), but its median CCU is only 38.
- **The spider, venom and bug cluster is small but hot.** +1 Venom Evolution has 40.8K, +1 Spider Arm 28.2K (11 days old) and Bug Evolution 23.9K (22 days old).

## 3. Age curve: when do winners appear?
| Age (days) | n | 1K% | 10K% | median CCU |
|---|---|---|---|---|
| 0–7 | 12 | **0%** | 0% | 134 |
| 8–14 | 50 | 20% | 6% | 84 |
| 15–21 | 116 | 22% | 3% | 71 |
| **22–30** | 188 | **32%** | 5% | 151 |
| 31–45 | 258 | 24% | 4% | 126 |
| 46–60 | 210 | 23% | 4% | 162 |
| 61–90 | 265 | 28% | 4% | 209 |
| **91–120** | 237 | **14%** | 1% | 91 |

- The median age is **40 days** for ≥10K games and 45 days for ≥1K games.
- Breakouts happen fast. DONT SPLASH reached 82.7K at 14 days, +1 Spider Arm 28.2K at 11 days, My Small Business 26.2K at 13 days and +1 Anime Eyes 31.3K at 16 days. A game is usually decided within about 30 days.
- **Late entrants to a wave suffer.** Egg games 0–14 days old hit 1K only 11% of the time (1/9). Egg games 15–60 days old hit 34–36%. Steal An Egg launched on 2026-07-25, so the egg wave's clone window was roughly mid-August to late September.

## 4. Update recency and like %
| Last update | n | 1K% | 10K% | median CCU |
|---|---|---|---|---|
| today | 445 | **38%** | 6% | 425 |
| 1–3 days ago | 276 | 29% | 5% | 165 |
| 4–14 days ago | 356 | 14% | 1% | 92 |
| 15+ days ago | 257 | **4%** | 0% | 19 |

| Like % | n | 1K% | 10K% | median CCU |
|---|---|---|---|---|
| <70 | 267 | **9%** | 1% | 39 |
| 70–84 | 410 | 18% | 3% | 71 |
| 85–92 | 347 | 29% | 4% | 241 |
| ≥93 | 312 | **37%** | 7% | 517 |

- **Combined:** games at ≥93% likes that were updated ≤1 day ago hit 1K **49%** of the time and 10K **10%** of the time (163 games).
- **The opposite:** games under 85% likes with no update for 4+ days hit 1K **4%** of the time (351 games).
- Causation runs both ways: a game that is winning gets updated. Still, a game that goes **two weeks without an update is effectively dead**.

## 5. Repeat creators (clone studios)
| Creator | ≥1K / games | What they make |
|---|---|---|
| **Crazay family** (Future, Junior, Houses, ASMR, Art) | **8/13** | Crazay Future is **5/5**, all "[Verb] for/to Eggs": Hide to Steal Eggs 10.3K, Lift Rock For Eggs 6.2K, Jump For Eggs 3.7K, Pull An Egg 2.0K, Drill for Eggs 1.8K. They also made Break a Brainrot Lucky Block 5.2K. |
| **xFrozen** (x Dudes, x Cube) | **5/7** | Don't Steal My Eggs! 6.3K, Egg Skipping 1.8K, Clone to Steal Eggs 1.5K, Climb and Drop an Egg 1.4K, Open Sea For Animals! 1.1K |
| HELP ME PLEASE studios | 2/2 | Cook the Chicken (by slapping it) 15.7K, 7 Days Cat-Sitting 12.4K. Both are short story games. |
| My Little Eggs | 1/3 | Bike For Animals Eggs 1.5K, Surf For Eggs 949, Kick an Egg 33 |
| Groups branded "+1" (all of them) | **2/28** | Locked In +1 Games 0/5, No Stop Games 0/3 |
| Habit Games! | 0/3 | Merge an Anime, Merge a Factory, Merge Your Car |
| CRAZY ANIMAL GAMES | 0/3 | "Kick for ADMIN PANEL X999999M" |

Takeaways:
- Creators with 2 or more games hit 1K at 24%, the same as the baseline. Volume alone doesn't win.
- **The studios that win stay on the live wave (eggs) and change the verb each time.** The ones that lose re-skin a saturated grammar ("+1", merge, admin-panel bait).

## 6. Twist lineage: the egg cluster (129 games)
The original is **Steal An Egg**: 1,228,197 CCU, 98 days old. These are its offspring:

| Twist type | n | ≥1K | 1K% | ≥10K | median CCU | Best examples (CCU) |
|---|---|---|---|---|---|---|
| **[Verb] For Eggs** (a new movement verb, with the egg as the reward) | 31 | 14 | **45%** | 2 | **949** | Bike For Egg! 46.1K, Climb For Animals Eggs 45.3K, Train Pets for Eggs 8.0K, Lift Rock For Eggs 6.2K, Dig For Eggs 6.0K, Jump For Eggs 3.7K, Swim For Eggs 3.4K |
| **[Verb] to Steal / Fake** (a new verb gates the steal) | 11 | 5 | **45%** | 2 | 816 | **Fake an Egg 43.0K** (disguise as an egg and ambush), Hide to Steal Eggs 10.3K, Mog to Steal 2.8K, Jump To Steal 1.9K, Clone to Steal 1.5K |
| Break and Steal (adds a second verb) | 7 | 2 | 29% | 1 | 70 | **Break and Steal an Egg 92.4K** (the first mover). Its 6 clones peak at 1.2K, and 3 sit below 5 CCU. |
| Don't Steal (flips to defense) | 2 | 1 | 50% | 0 | 3538 | Don't Steal My Eggs! 6.3K |
| Steal a [Adj] Egg (noun reskin) | 36 | 12 | 33% | **0** | 398 | strange egg 6.4K, Squishy Dumplings 4.9K, Anime 2.3K, Monkey 1.5K. Flops: Kitten 4, Candy 2, Soccer 22, Car 250, Genshin 275 |
| [Verb] an Egg (a new verb on the egg) | 29 | 5 | **17%** | 0 | **52** | Ride An Egg 9.3K. Flops: Roll an Egg 3, Stack an Egg 52, Kick an Egg 33/20, Paint Eggs 642, Drive An Egg 617 |

**Rule:** a new **movement or training verb** with "egg" as the reward works. A new **deception verb** that gates stealing works. A noun swap gets you to roughly 1K at best and never to 10K. Copying a two-verb title after its first mover fails: the Break-and-Steal clones are 1 for 6.

## 7. Anime specifically (68 games, 24% ≥1K, the baseline)
| Game | CCU | Age (days) | Like % | Loop (from its description) |
|---|---|---|---|---|
| **Anime Dice** | **60,759** | 77 | 99 | Roll dice → reveal an anime unit → upgrade dice luck → team → mutations. Earns money offline. |
| **+1 Anime Eyes** | **31,316** | **16** | 96 | Click for +1 Chakra → unlock 14 eyes (Sharingan and so on) → 15 stages of enemies and bosses → pets, auras, rebirth. Gains offline. |
| **My Anime Mine** | 13,976 | 72 | 99 | Anime crew breaks rocks for ore → level up, mutate, enchant → research tree → next zone. Incremental. |
| Steal an Anime Pack | 9,088 | 78 | 95 | Steal and open packs → units earn cash (offline too) → train speed → steal from other players. "Inspired by Anime Dice." |
| Anime Galaxies | 7,677 | 17 | 95 | Gacha banners → tower defense (TD), with challenges every 15 minutes and a season pass. Not a simple game. |
| Anime Legacy Simulator | 7,260 | 50 | 96 | Train and fight simulator |
| Anime Breaker | 6,188 | 81 | 95 | Break things → anime units |
| Defeat Anime RNG | 5,596 | 99 | 96 | RNG plus boss fights |
| Anime Zero | 3,941 | 106 | 97 | — |
| +1 Anime Evolve | 3,554 | 53 | 94 | "+1 Evolution" grammar |
| Anime Nexus RNG | 3,282 | 41 | 96 | RNG |
| Build An Anime Character | 3,273 | 27 | **63** | Spin for parts → combine stats → 1v1 battles. Low like %. |
| Anime Realms X | 2,473 | 27 | 96 | — |
| Steal An Anime Egg | 2,281 | 68 | 97 | Steal-egg reskin |
| Choose the Stronger Anime! | 2,180 | 67 | 80 | Party / quiz |
| Break and Steal an Anime Egg | 1,192 | 30 | 85 | Reskin. Three other copies sit at 70, 0 and 0 CCU. |
| *Flops* | <1K | | | Wish For Anime 927, +1 Anime Fight Evolution 783, Anime Girl Card Farm 713, Guess the Anime Color 612, +1 Forge For Anime 499, Build An Anime Army 450, Paint the Anime 401, **Anime Dice 2: 249**, **Anime Dice Fighter: 298**, Merge an Anime 42 / Merge a Anime Army 22 / Merge a Anime! 10, Draw the Anime! 59, +1 Anime per Step 100 |

| Anime sub-loop | n | 1K% |
|---|---|---|
| dice / roll / RNG / wish | 10 | 30% (1 game at 10K) |
| +1 | 10 | 20% (1 game at 10K) |
| egg reskin | 6 | 33% (2 games, both near 1K) |
| merge | 3 | **0%** |
| guess / draw / paint / color / clean | 7 | **0%** |
| cards | 6 | **0%** |

Two lessons:
- **Direct copies of the anime hit fail.** Anime Dice 2 has 249 CCU and Anime Dice Fighter has 298.
- **The winning anime twist ports a proven non-anime loop into the anime skin:** +1 Eyes, a mine, pack-stealing.

## 8. Loops of the top movers (from their descriptions)
| Game | CCU | Loop |
|---|---|---|
| Throw Food For Animals | 129.5K | Throw food far → attract animals → animals earn money → better food → train on pull-up bars for Throw Power → new areas |
| DONT SPLASH | 82.7K | Poolrooms horror. Don't touch the water. (Outlier, not a simulator.) |
| Sell Fries! [Anomaly] | 46.7K | Collect potatoes → make fries → serve customers → upgrade the kitchen → something happens "when night falls" (anomaly twist) |
| Bike For Egg! | 46.1K | Steal eggs from pets → hatch → pets earn money → upgrade the treadmill and base → train speed → steal from players → index |
| Climb For Animals Eggs | 45.3K | Climb → new biomes → hatch → animals earn cash (offline) → treadmill speed → rebirth |
| Steal A Pet And Ride It! | 44.1K | Steal a cage from a sleeping boss → run home before it catches you → open the cage → **ride the pet to get faster** → barn earns cash → treadmill → rebirth |
| Fake an Egg | 43.0K | Disguise as an egg → wait → steal the victim's best pet. A pure social-deception twist on the egg loop. |
| +1 Venom Evolution | 40.9K | Train → fight stages → wins unlock evolutions → max transformation |
| +1 Anime Eyes | 31.3K | Click for +1 Chakra → eyes → stages and bosses → pets, auras, rebirth, offline gains |
| +1 Spider Arm | 28.3K | Hold SPACE to climb with a spider rig → train for +1 arm (more speed and grip) → a grip meter drains → 13 escape stages → wins unlock rigs |
| My Small Business | 26.2K | Design → print → pack orders → hire → offline coins, co-op with friends (cozy tycoon) |
| Cook the Chicken (by slapping it) | 15.7K | Absurd premise. A 20–30 minute story game. |
| Hide to Steal Eggs | 10.3K | Hide inside eggs to sneak onto other players' plots → train strength to carry heavier eggs → hatch |
| Ride An Egg | 9.3K | Roll an egg out → run back alive while animals chase you → go further for more luck → treadmill speed → offline cash |
| Don't Steal My Eggs! | 6.3K | A defense flip: catch thieves to protect your eggs → pets earn cash → speed |

**Shared backend:** **14 of these 20 games** use train (treadmill or pull-ups) → stat → collect pet, egg or unit → passive base income → rebirth. **7 of 20** say "offline earnings" outright. The exceptions are DONT SPLASH, Cook the Chicken, Sell Fries and Fake an Egg: three short story or horror games and one deception game.

---

## Laws (data-backed; read them as relative rankings, not absolute odds)
1. **Update or die.** Updated today: 38% hit 1K. Updated 4–14 days ago: 14%. Updated 15+ days ago: 4%. That's a 9.5× gap between today and 15+ days.
2. **Likes gate everything.** At ≥93% likes, 37% hit 1K (7% hit 10K). Below 70%, 9% hit 1K. A game at ≥93% likes that was updated within the last day hits 1K 49% of the time.
3. **Ride the live wave in its days 20–60.** Egg games 15–60 days old hit 34–36%. Egg games 0–14 days old hit 11%. The egg wave (34%, 129 games) and the animal wave (34%, 82 games) are the only big themes above baseline.
4. **Change the verb, keep the reward.** "[Verb] For Eggs" hits 45% with a median of 949 CCU. Noun reskins hit 33% and produced 0 games at 10K. "[Verb] an Egg" hits 17% with a median of 52.
5. **Deception and stealth verbs over-index.** Fake an Egg has 43.0K, Hide to Steal 10.3K, Don't Steal My Eggs 6.3K, Paint and Hide 17.3K. The "[Verb] to Steal" group hits 45% of the time.
6. **Copying a two-verb title after its first mover fails.** Break and Steal an Egg has 92.4K. Its 6 clones are 1 for 6, with a median of 70 CCU.
7. **Steal and Build are the best first words** (38% of 79 games and 48% of 25). Merge is the worst (0 of 24). Hatch, catch, stack, pull, idle and draw each hit about 10% or less.
8. **"+1" is saturated.** 221 games hit at 19%, below baseline. "+1 Per/Every" hits 11%, "+1 speed/jump" 10%, "+1 Escape" 14%. Only "+1 Evolution" (30%) and "+1 [body part]" (2 of 14 at 10K) still hold up, and they need a fresh fantasy (venom, spider, anime eyes).
9. **Keep the title to 2–4 words.** The 1K rate is flat from 2 to 6 words (22–25%), but the 10K rate drops from 7% at 2 words to 2% at 4+ words. Titles of 7+ words went 0 for 9.
10. **A seasonal tag is decoration; a seasonal theme is poison.** Among games updated in the last 3 days, 🎃 gives about +4 points. Halloween, pumpkin, ghost and zombie as the theme hit 14% with zero 10K games (pumpkin alone is 1 of 33).
11. **Anime is a skin.** Anime as a whole is at baseline (24% of 68). Anime on a roll, mine, steal-pack or +1 loop gives 60.8K, 31.3K, 14K and 9.1K. Anime merge, guess, draw and card games went 0 for 16. Direct sequels or clones of Anime Dice sit at 249 and 298.
12. **Dragon, kaiju, slime and food themes underperform.** Dragon/dino/kaiju/titan hit 14% (dragon 0 of 9, kaiju 1 of 14). Slime is 0 of 12. Food has a median of 38 CCU despite three hits.
13. **Winners show up in weeks 2–4.** Games 0–7 days old: 0 of 12 at 1K. Days 22–30: 32%. Days 91–120: 14%. The median ≥10K game is 40 days old. If you haven't reached 1K by day 30, iterate or reship.
14. **Clone studios win by changing the verb on the live wave, not by changing the grammar.** The Crazay family is 8 of 13 at 1K (Crazay Future 5 of 5, all egg-verb twists) and xFrozen is 5 of 7. Groups branded "+1" are 2 of 28.
15. **The verb in the title sits on top of one shared backend.** 14 of the 20 top movers run train → stat → collect egg or pet → passive income (offline) → rebirth. The title verb is the shop window, and that loop is the game behind it.

## Caveats
- **Search-rank bias.** Roblox search ranks popular games higher, so every phrase over-samples winners. The real ≥1K rate across all new games is far below 23%. Use these numbers only to compare one group against another.
- **This is a single snapshot.** CCU was taken on Saturday 2026-10-31, Halloween, during an event week. Weekend and holiday peaks inflate CCU, and 🎃-tagged games may be getting a temporary event bump.
- **Survivorship.** Games that died are under-represented in search, so dead patterns (merge, pumpkin) are probably even worse than shown.
- **Small groups.** Many grammar and theme cells have fewer than 20 games: brainrot (6), venom/spider (8), Don't Steal (2), to Escape (6). Treat them as directional only.
- **Causation runs both ways** for updates and likes, because successful games attract updates and votes.
- **Theme matching is by title** and depends on regex choices. Word counts drop bracket tags, parentheses and anything after a "|".
- **The creator field is the group name.** Families like "Crazay ___" were matched by name token, so separate owners who happen to share a token could be merged by mistake.

Related: [[Simple Action Loops Scorecard]] · [[Idea Ledger Round 1]] · [[Growth Curves and Timing]]
