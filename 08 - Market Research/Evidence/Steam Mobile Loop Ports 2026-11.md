---
tags: [market-research, evidence, tier-d, steam, mobile, roblox-port, core-loops]
updated: 2026-11-14
sources: 34
status: draft
---
# Steam Mobile Loop Ports 2026-11

**Question:** Which *proven* Steam and mobile loops can be turned into a Roblox one-action game (the "Throw Food For Animals" format) by changing exactly ONE part, and which of those titles are still open on Roblox today?

**Method (2026-11-14):** About 30 WebSearch queries. WebFetch failed with ENOTFOUND on every host tried (sensortower.com, foxdata.com, steamcharts.com, store.steampowered.com, mobilegamer.biz, vgchartz.com), so **all outside-platform numbers come from search snippets** that quote SteamDB, GameDiscoverCo, AppMagic and similar trackers. I also ran 120+ live Roblox searches with `tools/roblox_intel.py search` (live CCU, age in days, like%), all on 2026-11-14 between about 10:00 and 11:00 UTC. A CCU figure in this note means *live playing now* unless it says otherwise. Builds on [[Tier D - Steam Mobile Cross-Platform]] and is judged against [[Idea Judgement Rules]].

## TL;DR
- **Direct-name ports of Steam hits flop; verb-first renames win.** This happened on three separate waves. How to Fish: the "How To Fish" copy has 12 CCU, while Net a Fish! has 33K and Harpoon a Fish 14K. Moon Sweepers: the "Moon Sweepers" copies have 1–10, while Sweep The Moon has 22K. Worst Class Ever: the "Worst class ever" copy has 85, while Class Clowns has 4.3K. Never reuse the Steam name. Keep the fantasy and put a verb first.
- **The parts that survive the port are the fantasy and the verb. The parts that never survive are the Steam depth** (haggling, horde builds, puzzle grids, extraction PvP). Each one gets replaced by the Roblox engine: one verb, then rarity roll, then base income, then rebirth.
- **A rarity roll beats a plain egg noun.** Golf a Lucky Egg has 3.8K at 10 days, while Golf For Eggs (2), Golf An Egg (4) and Golf for Animals (0) sit on the same verb. The "Lucky" roll is the part that made the difference.
- **The freshest open waves are Worst Class Ever** (full release Nov 9–10, 44K Steam peak on Nov 13, 100K+ copies day one) **and Probably Stolen** (186K peak Nov 8, about 750K copies in 5 days). Neither has a verb-first Roblox port yet. **Top bets: "Prank the Teacher" and "Sell Stolen Loot".**
- **Mobile spatial puzzles still don't port** (Block Blast, Arrows, Bus jam, Meowdoku). Their Roblox copies sit at 0–234 CCU. Pixel Flow is the only one with a shooter verb, and it is a long shot.
- **ROB RUN (365K peak, Nov 13) is the biggest Steam spike right now, but Roblox already owns the loop** (Jailbreak, Criminal Simulator 24.5K, ROB IT 2.5K). Skip it.

---

## 1. Outside-platform evidence summary (Sep–Nov 2026 plus evergreen)

| # | Game | Platform | Evidence (date) | Fresh? |
|---|---|---|---|---|
| 1 | Worst Class Ever | Steam | Launched Nov 9–10 2026; **44,164 peak on Nov 13** (SteamDB via search); 100K+ copies day one (developer); about 86% positive from 323 reviews; demo peaked at 27.8K on Oct 24 with 1M+ demo downloads | **Yes, 4 days** |
| 2 | Probably Stolen | Steam ($20) | Launched Oct 28; 350K copies in 24h, 500K by Oct 30, **750K by Nov 3** (GameDiscoverCo); **peak 186,095 on Nov 8**; 96% positive from 7K+ reviews | **Yes, 17 days** |
| 3 | Moon Sweepers | Steam (16-player co-op) | Launched Oct 23; **83,138 peak on Nov 1**, about 41K live in early November | **Yes, 22 days** |
| 4 | ROB RUN | Steam (F2P, Early Access) | Launched Nov 4; **365,092 peak on Nov 13**; Mixed reviews (about 43% negative) | Yes, 10 days |
| 5 | How to Fish | Steam | Launched Aug 20; **373,971 peak on Aug 26**; 6.3M units and $26M in August (GameDiscoverCo via Cinevva); player count is fading | No, 86 days |
| 6 | Megabonk (Survivors-like) | Steam | 1M sold in 2 weeks (Oct 2025); 117K peak | Evergreen |
| 7 | BALL x PIT | Steam/console | **2M+ units (Aug 2026, VGChartz)**; 300K in its first 5 days | Evergreen |
| 8 | Super Battle Golf | Steam | 20.4K all-time peak; about 563K copies (Jul 2026). From [[Tier D - Steam Mobile Cross-Platform]] | Stale |
| 9 | PEAK | Steam | 171K peak; Alinea expected 10M+ sold (2025) | Evergreen |
| 10 | R.E.P.O. | Steam | 271,571 peak (Mar 2025); 15–16.8M sold | Evergreen |
| 11 | Schedule I | Steam | 455–459K peak (Apr 2025), a record for a solo developer; about 6.5M sold (estimate) | Evergreen |
| 12 | Supermarket Simulator | Steam | 38K peak (Mar 2024); 1.5–1.8M copies (estimate) | Evergreen |
| 13 | Bongo Cat | Steam (F2P idle) | 194.5K all-time peak; **June 2026 average 150K** (Steambase) | Evergreen |
| 14 | Pixel Flow! | Mobile | **$198.4M in year 1** (Aug 2025–Aug 2026, PocketGamer.biz/AppMagic); PG Awards Game of the Year 2026 | Proven, current |
| 15 | Block Blast! | Mobile + Poki | **#3 global downloads in Oct 2026** (Sensor Tower), or #1 at 25.1M per FoxData | **Yes, Oct** |
| 16 | Bus Fever Party! | Mobile | **#5 global downloads in Sep 2026** (Sensor Tower); listed as a breakout in FoxData's October ranking | **Yes, Sep–Oct** |
| 17 | Arrows (directional puzzles) | Mobile | Led downloads in May–Jun 2026; top 10 for H1 2026 | Stale |
| 18 | Meowdoku! | Mobile | **#4–5 global downloads in Oct 2026** (Sensor Tower); 10M in June | **Yes, Oct** |
| 19 | Smash Fest! (cannon at stacks) | Mobile | Reached #1 on US iOS free with no paid ads (Jun–Jul 2026); about 6M downloads/month in Jul and Aug | Proven, Jul–Aug |
| 20 | Hole.io | Mobile | **119M downloads in 2025**, more than at its 2018 launch; 195.5M from Jan 2025 to Jul 2026 | Evergreen, reviving |
| 21 | Katamari-style roll-and-grow | Console/mobile | Evergreen; no fresh data found | Evergreen |
| 22 | Idle miners (Idle Miner Tycoon) | Mobile | Evergreen; no fresh data found | Evergreen |
| 23 | Colony Flow (ants carry pixels) | Mobile | 1M+ Google Play installs; Mobidictum Sep 2026 headline cites 2.1M downloads | Yes, Sep |

---

## 2. Loop tables (one per loop)

Loop line format: `verb -> reward -> spend -> stronger verb -> rebirth`. The parts are VERB / REWARD / SOURCE / STAT / RISK / META / SOCIAL. Under "Roblox ports", each entry reads *live CCU / age in days*.

### 2.1 Worst Class Ever: TOP PICK
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Worst Class Ever | Steam | 44,164 peak Nov 13 2026; 100K+ copies day one. [SteamDB](https://steamdb.info/app/5175310/charts/), [Steam news](https://store.steampowered.com/news/app/5175310/view/719047432802926646), [GameSpark](https://gamespark.jp/article/2026/11/10/174723.html) | prank while teacher's back is turned -> prank points -> buy bigger pranks/disguises -> bolder pranks unseen -> new grade | **Direct-name copies flopped:** "Worst class ever" 85/21d, "The WORST Class Experience" 98/17d. **Renames worked:** 🤡 Class Clowns 4.3K/17d, Be a Teacher! 3.9K/15d (the teacher side). Make the Teacher QUIT! 95/34d | **Prank the Teacher.** Change the VERB only: collapse the menu of prank actions into one throw-a-prank tap at the teacher's back. Keep the getting-caught risk. Add a desk that earns prank points offline. Alternative: **Throw Spitballs** | **Open.** No exact title. Nearest are Make the Teacher QUIT! (95) and Class Clowns (4.3K). The Steam wave is 4 days old, which is ideal for rule 2. "Throw Spitballs" is also open; the throw-verb family is live (Throw a Seed 16.4K/6d) |

Parts: VERB = prank. REWARD = prank points. SOURCE = the teacher's gaze. STAT = sneak level and prank tier. RISK = getting caught, which costs your streak. META = grade levels. SOCIAL = class versus teacher. **Port fit:** the stealth/deception fantasy over-indexes on Roblox (rule 7: Fake an Egg, Paint and Hide). The asymmetric teacher role needs 2+ players, so keep an NPC teacher for solo servers.

### 2.2 Probably Stolen
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Probably Stolen | Steam | 750K copies by Nov 3; peak 186,095 on Nov 8; 96% positive. [TheGamer](https://www.thegamer.com/probably-stolen-indie-game-100000-players-on-steam/), [Notebookcheck](https://notebookcheck.net/500K-sales-in-2-days-This-indie-game-with-96-positive-reviews-is-blowing-up.1440296.0.html), [games.gg](https://games.gg/news/probably-stolen-cyberpunk-shopkeeper-sim-steam-surge/) | inspect dodgy item -> buy low/sell high -> upgrade shop and scanner -> rarer goods -> new district | Own a Pawn Shop 647/27d; Thrift&Flip: Resell Tycoon 4.9K/71d; Storage Hunters 9.7K/164d; Bid For It 66/51d; Pawn Tycoon 17. Sell-X [Anomaly] family: Sell Pearls 2.3K/25d, Sell Gas 876/19d | **Sell Stolen Loot.** Change the SOURCE only: haggling and inspection become a loot crate with a rarity roll (common to secret). Keep buy-low/sell-high and add shop shelves that earn offline. Alternative: **Spot the Fake** | **Open.** No exact title. "Spot the Fake" is a **graveyard** (15 CCU/27d, a quiz). Keep "Steal/Stolen" in the title, since rule 8 makes it the best first word |

**Port fit:** the haggling mini-game is too deep for an audience aged 8–14. The crate roll keeps the "is it a jackpot?" moment. Avoid any real-crime framing: the loot is cartoon "stolen" stuff, just as in Steal An Egg.

### 2.3 Moon Sweepers
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Moon Sweepers | Steam | 83,138 peak Nov 1; launched Oct 23. [SteamDB mirror](https://steamdb.com/en/tools/steam-charts/5335510-moon-sweepers), [mein-mmo](https://mein-mmo.de/steam-moon-sweepers-hit/) | sweep moon dust -> credits -> better brooms/vacuums -> clean faster -> bigger area | **Already ported and won:** Sweep The Moon 22K/21d (98% liked); [MARS] Clean the Moon! 4.9K/33d. **Direct names flopped:** 🌑Moon Sweepers 10, MOON SWEEPERS! 1. Noun-swap Clean the Sun 33/19d | **Vacuum the Moon.** Change the VERB only | **Open, but late.** No exact title; Vacuum Everything has 360. It would be the 3rd verb-swap on the wave, so per rule 3 expect 3–7K at best. Low priority |

**Lesson:** this is the cleanest proof that a Steam co-op hit becomes a Roblox one-verb hit (Sweep The Moon), and that **noun swaps on it are already dead** (Clean the Sun).

### 2.4 ROB RUN
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| ROB RUN | Steam F2P | 365,092 peak Nov 13, 9 days after launch; Mixed reviews. [SteamDB news](https://store.steampowered.com/news/group/4777282/view/712291505861034339), [GameRant](https://gamerant.com/games-like-gta-6-rob-run-reviews/) | rob store -> loot -> launder/buy gear -> bigger heists -> server wipe (rebirth) | Roblox-native genre: Jailbreak 4.5K; Criminal Simulator 24.5K/36d (it predates ROB RUN); ROB IT 2.5K; Steal and Escape Police 480; Steal a Vault 152/37d; 🥚 ROB AN EGG 23/5d | *(none recommended)*. A "Rob a Vault" mutation would land in a graveyard | **Saturated.** The Rob/Steal + vault titles sit under 200 CCU. "Steal and Run" is a chained-verb title (rule 4) |

### 2.5 How to Fish
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| How to Fish | Steam | 373,971 peak Aug 26; 6.3M units in August. [GamesRadar](https://www.gamesradar.com/games/co-op/latest-steam-lottery-winner-how-to-fish-sells-1-million-copies-in-2-days-yes-well-be-adding-more-content/), [Cinevva](https://app.cinevva.com/news/2026-09-04-how-to-fish-august-indie-sales) | cast and bonk flopping fish -> coins -> better rod/bonker -> bigger fish -> new lake | **Verb renames won:** Net a Fish! 33K/29d, Harpoon a Fish 14K/77d, Shoot That Fish 2.3K/58d, Shoot To Fish 498. **Direct names flopped:** How To Fish 12, How to Really Fish 75 (from a 14K peak). Slap A Fish 45, +1 Slap A Fish 55/9d | **Bonk a Fish.** Change the VERB only: bonk instead of net/harpoon | **Open, but late.** No exact title. Wave age is 86 days, so rule 2 predicts about 1–3K, and the fresh slap copies are already at 55 |

### 2.6 Megabonk / Vampire Survivors-likes
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Megabonk | Steam | 1M sold in 2 weeks (Oct 2025); 117K peak. [PC Gamer](https://www.pcgamer.com/games/roguelike/vampire-survivors-like-megabonk-makes-megabucks-selling-a-million-copies-in-2-weeks-and-currently-has-more-daily-players-than-borderlands-4-on-steam-ill-be-eating-spaghetti-with-extra-sauce-tonight) | auto-attack horde -> XP gems -> pick upgrade -> screen-clearing build -> prestige | Zombie Rush Survival 8.9K/189d; Survive a Million Monkeys 4.9K/95d; [🎃] Survive Zombie Arena 6.8K; Survive the Swarm 382; Robong Survivors (the faithful port) **10**/367d | **Bonk the Horde.** Change the PROGRESSION only: drop the run-based upgrade draft and use a permanent "+1 bonk power" stat that persists, plus a pet that auto-bonks for base income | **Open.** No exact title. Nearest are BONK! Ragdoll Boxing 3.2K/27d and Survive the Horde 137. The faithful Survivors port has 10 CCU, which shows the draft-pick roguelite does not survive the port |

### 2.7 BALL x PIT
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| BALL x PIT | Steam/console | 2M+ units (Aug 2026). [VGChartz via search](https://www.vgchartz.com/article/468682/ball-x-pit-sales-top-2-million-units-free-update-out-now/), [PC Gamer](https://www.pcgamer.com/games/roguelike/ball-bouncing-city-building-off-the-wall-roguelike-ball-x-pit-is-a-huge-hit-selling-300-000-copies-in-just-its-first-five-days-on-sale/) | fire balls -> break bricks -> fuse balls -> bigger volleys -> new pit | No faithful port. +1 Bouncy Ball 1.3K/37d; Block Breakout 21; Idle Brick Breaker 3; Bounce an Egg 428; Bounce For Eggs! 23/23d | **Bounce Lucky Balls.** Change the META only: ball fusion becomes a rarity roll ("Lucky" balls), and the balls bounce on your plot for offline income | **Open.** No exact title. Weak neighbours, so this is a moderate bet: the brick-breaker verb is unproven on Roblox |

### 2.8 Super Battle Golf (golf chaos)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Super Battle Golf | Steam | 20.4K peak; about 563K copies (Jul 2026). [Tier D](https://steamcharts.com/app/4069520) | whack ball -> coins -> clubs/items -> wilder shots -> new course | **[⛳] Golf a Lucky Egg 3.8K/10d (rising first mover).** Hit a Golf Ball 512; Golf For Eggs 2; Golf An Egg 4; Golf for Animals **0**/50d; Golf a Lucky Block 6 | *(Be a fast follower only)*: **Putt a Lucky Pet** | **Open**, but rule 3 says the first mover takes most of the wave, and the plain golf-egg titles are graveyards. Use it as rule evidence, not a build |

### 2.9 Pixel Flow! / Colony Flow
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Pixel Flow! | Mobile | $198.4M year 1 (to Aug 2026). [PocketGamer.biz](https://www.pocketgamer.biz/loom-games-pixel-flow-makes-almost-200m-in-player-spending-during-first-year/) | send colour shooters at pixel art -> clear pixels -> coins -> more shooters -> next artwork | Ants Pixel March 345/88d (Colony-Flow-like); Break 1,000,000 Pixels 0; PixelShoot 95; Hide In Pixels 586 (a different loop) | **Shoot the Pixels.** Change the SOCIAL part only: one giant shared pixel wall per server, where everyone's shots clear it together, and your shooter turret earns on your base | **Open.** No exact title. All neighbours are under 600, so this is a long shot |

### 2.10 Smash Fest! (cannon at stacks)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Smash Fest! | Mobile | #1 US iOS free (Jun–Jul 2026); about 6M downloads/month. [FoxData](https://foxdata.com/en/blogs/how-smash-fest-hit-1-on-the-us-app-store-with-zero-paid-uaand-what-it-means-for-hybrid-casual/), [Gamigion](https://www.gamigion.com/smash-fest-casual-liveops-turned-into-genre-wide-trend/) | fire limited cannonballs -> topple stack -> coins -> more/bigger shots -> next level | Knock the Blocks 1.1K/858d; Chaos Jenga 3.7K (old); Cannon For Eggs 18/15d; Fire A Cannon! 0; +1 Cannon Shooting 28; SMASH a Tower 0 | **Cannon the Castle.** Change the RISK only: remove the limited ammo, so shots become a free "+1 cannon power" grind | **Open, but warning.** Every cannon title is under 30 CCU. Not recommended |

### 2.11 PEAK (co-op climb)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| PEAK | Steam | 171K peak; 10M+ expected. [Alinea](https://alineaanalytics.substack.com/p/peak-sold-18-million-copies-last) | climb with stamina -> reach camp -> items -> higher biome -> summit | CLIMB 54 (13.9M visits all-time); Cliffbound 247. **Collapsed versions won:** Climb For Animals Eggs 19.4K/68d, Climb and Steal an Egg 7.2K | *(already collapsed by others)* | **Saturated** on the egg engine. Proof that the port works only once it is collapsed |

### 2.12 R.E.P.O. (haul loot co-op)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| R.E.P.O. | Steam | 271,571 peak; 15–16.8M sold. [SteamDB](https://steamdb.info/app/3241660/charts) | grab valuables -> haul to cart without breaking -> cash -> upgrades -> deeper level | [UPD] Lethal Ape Experience 23.5K; Lethal Ape (The Mines) 12K; REPO SANDBOX 1.3K; REPO Game 9 | **Carry Loot Home** | **Warning:** "Carry It Home" has 0 at 49d (a graveyard). Carry Food For Animals has 2.2K/14d, but it uses the animal reward. Skip |

### 2.13 Schedule I (grow and sell)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Schedule I | Steam | 459K peak (Apr 2025). [TweakTown](https://www.tweaktown.com/news/104474/schedule-hits-459k-peak-players-the-most-by-solo-developer-in-steam-history/index.html) | grow product -> sell to customers -> hire workers/expand -> bigger empire | Schedule 🥔 27; Schedule X 2. A kid-safe version already exists: Sell Lemons 6.4K/606d; Sell Lemonade! [Anomaly] 295/10d; Sell Pearls 2.3K | *(fold into the Sell-X family)* | **Saturated.** Its kid-safe form *is* the Roblox "Sell X" family |

### 2.14 Supermarket Simulator
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Supermarket Simulator | Steam | 38K peak; 1.5–1.8M copies. [GWO](https://wnhub.io/news/stores-and-publishing/item-43033) | stock shelves -> sell -> expand store -> more products -> bigger store | Supermarket Simulator 1.2K/764d; Own a Grocery Store 2.9K/113d; Survive Overnight in a Mega Store 6K; Checkout Chaos 108 | — | **Saturated** |

### 2.15 Idle miners
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Idle Miner Tycoon / mining idles | Mobile | Evergreen (no fresh figure found) | mine -> ore -> upgrade shaft/managers -> deeper -> prestige | +1 Mine Per Click 1K/181d; Mine a Mountain 789; Mining Simulator 125; Idle Miner Tycoon 0 | — | **Saturated.** The Roblox engine already *is* an idle miner |

### 2.16 Bongo Cat
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Bongo Cat | Steam F2P | 194.5K all-time peak; 150K average in Jun 2026. [Steambase](https://steambase.io/games/bongo-cat) | type/tap anywhere -> points -> hats/cosmetic drops -> rarer drops | No port. Spin a Bongo 7; rhythm titles are old (Funky Friday 2.3K) | **Drum For Eggs.** Change the SOURCE only: a tap-drum generates the eggs | **Open.** No exact title. Weak: Roblox has no background-play mode, which is the whole Bongo Cat hook |

### 2.17 Hole.io
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Hole.io | Mobile | 119M downloads in 2025. [Appfigures](https://appfigures.com/resources/insights/20250314/amp?f=4) | swallow objects -> grow -> swallow bigger -> top the leaderboard | 🕳️ Be a Hole 479/873d (264M visits); Eat the World 1.9K; Eat Everything In A Grocery Store 1.5K/41d; Eat The City! 29 | — | **Graveyard** for city-eating titles (29) |

### 2.18 Katamari (roll and grow)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Katamari | Console | Evergreen | roll -> pick up objects -> grow -> roll bigger things -> next stage | [🦖] roll the world 792/38d; +1 Money Roll 247; Grow a Snowman 451/28d; Roll a Snowball 0; +1 Roll a Snowball! 4 | **Roll a Snowman** (a Christmas tag, rule 13) | **Mostly a graveyard.** Snowball titles are at 0–30 |

### 2.19 Mobile spatial puzzles (Block Blast, Arrows, Bus Fever, Meowdoku)
| Game | Platform | Evidence + date + link | Loop line | Roblox ports (live CCU) | Proposed mutated port | Live-check result |
|---|---|---|---|---|---|---|
| Block Blast! | Mobile | #3 downloads Oct 2026 (Sensor Tower) | place block -> clear line -> score -> streak | Blast a Block! 53/288d; Block Clear Race 234; Block Puzzle 100; Drop a Block 0 | — | **Reject.** Ports are 0–234 |
| Arrows | Mobile | Download leader May–Jun 2026. [mobilegamer.biz](https://mobilegamer.biz/junes-top-mobile-game-downloads-arrows-amaze-go-free-fire-max-roblox-more/) | tap arrow out in order -> clear grid -> coins | ARROWS: Puzzle Game 1/122d; Arrow Out Puzzle 0 | *Pull the Arrows* | Open but **reject**. The faithful ports are at 0–1 |
| Bus Fever Party! | Mobile | #5 downloads Sep 2026 (Sensor Tower) | route colour buses -> clear jam -> coins -> bigger lots | Bus Station: Traffic Jam 16/47d | **Pack the Bus** | Open. Weak: a puzzle verb with a 16-CCU faithful port |
| Meowdoku! | Mobile | #4–5 downloads Oct 2026; 10M in June. [PocketGamer.biz](https://www.pocketgamer.biz/june-2026-mobile-game-charts/) | sudoku with cats | No port | — | **Reject.** Logic puzzle for ages 8–14 on Roblox |

### 2.20 Reference: Meccha Chameleon (Jun 2026), the saturated case
Paint-hide: 15M+ sold on Steam. Roblox clones beat it within 3 weeks ([Kotaku](https://kotaku.com/more-people-are-playing-meccha-chameleon-knock-offs-than-the-original-hit-steam-game-as-the-roblox-clone-machine-goes-into-overdrive-2000715371)). Today the late copies sit at Hide In Pixels 586/49d and Hide In Drawings 1.9K/36d. This shows how far a Steam wave falls by around day 150.

---

## 3. Which outside loops survive the port

**Ranked mutated ports** (each keeps the proven core and changes one part):

| Rank | Title | Source loop | ONE part changed | Live-check (2026-11-14) | Why |
|---|---|---|---|---|---|
| 1 | **Prank the Teacher** | Worst Class Ever | VERB → one throw-prank tap | Open; nearest Class Clowns 4.3K/17d | Wave 4 days old; stealth over-indexes (rule 7) |
| 2 | **Sell Stolen Loot** | Probably Stolen | SOURCE → rarity crate | Open; Own a Pawn Shop 647, Sell Pearls 2.3K | Wave 17 days old; Steal/Sell words win |
| 3 | **Throw Spitballs** | Worst Class Ever (alternative) | VERB → throw | Open; throw family live (Throw a Seed 16.4K/6d) | Rides two waves at once (throw verb plus class prank) |
| 4 | **Bonk the Horde** | Megabonk / Survivors-likes | PROGRESSION → persistent +1 stat | Open; faithful port has 10 | Horde verb proven (Zombie Rush 8.9K) |
| 5 | **Vacuum the Moon** | Moon Sweepers | VERB | Open, 3rd mover | Leader has 22K; expect 3–7K |
| 6 | **Bounce Lucky Balls** | BALL x PIT | META → rarity roll | Open; +1 Bouncy Ball 1.3K | The Lucky roll fixes the golf-egg failure |
| 7 | **Bonk a Fish** | How to Fish | VERB | Open, late (86d) | Net a Fish 33K proves the wave; expect 1–3K |
| 8 | **Shoot the Pixels** | Pixel Flow! | SOCIAL → shared server wall | Open; neighbours under 600 | $198M loop, unproven on Roblox |
| 9 | **Putt a Lucky Pet** | Super Battle Golf | REWARD → pet roll | Open; Golf a Lucky Egg 3.8K/10d leads | Fast follower only |
| 10 | **Pack the Bus** | Bus Fever Party! | VERB → physical packing | Open; faithful port 16 | Long shot |

**Port-survival rules (from this scan):**
1. **Never reuse the Steam title.** Direct-name copies sat at 1–98 CCU on all three waves (How To Fish 12, Moon Sweepers 10, Worst class ever 85), while verb-first renames reached 4–33K.
2. **What survives is the fantasy plus one verb.** Pranking, sweeping, netting fish and climbing all survived. Drafts, haggling, ammo limits, puzzle grids and extraction PvP never did: the faithful Survivors port has 10 CCU, Arrows 1, Block Blast 53, cannon titles 0–28.
3. **Replace Steam depth with the Roblox engine:** one verb, then a rarity roll ("Lucky"), then base or offline income, then rebirth. The roll is what separated Golf a Lucky Egg (3.8K) from Golf For Eggs (2).
4. **Speed beats fidelity.** Sweep The Moon shipped on Steam launch day (Oct 23) and took 22K. Clean the Moon shipped earlier, off the demo, but on a weaker verb, and has 4.9K. Steam demos (Next Fest) give a 1–3 week head start, so watch the Next Fest top 50.
5. **Co-op Steam hits port best; single-player mobile puzzles port worst.** Roblox is a social platform. Mobile puzzles have no "better with a friend" hook (rule 14).
6. **Skip loops Roblox already owns natively** (cops and robbers, supermarket, mining, Sell-X). A Steam spike there (ROB RUN, 365K) adds no opening.
7. **Noun swaps after the leader are dead on arrival:** Clean the Sun 33, Slap A Fish 45, Eat The City 29. This confirms rule 6.

## Checklist
- [ ] Shortlist "Prank the Teacher" and "Sell Stolen Loot" and score both on the 10-point test (rule 14).
- [ ] Re-run `roblox_intel.py search` on both titles plus "prank", "spitball" and "stolen" the day before shipping.
- [ ] Check Class Clowns and Be a Teacher! again on Nov 21. If either passes 15K, the teacher wave is being claimed.
- [ ] Ship on a Friday (rule 16), ideally within 7–10 days on the existing engine.
- [ ] Add the next Steam Next Fest top-50 list to the weekly watch, as a 1–3 week head start.

## Common Mistakes
- Porting the Steam game faithfully (Robong Survivors: 10 CCU).
- Using the Steam game's name (How To Fish: 12; Moon Sweepers: 10).
- Adding a noun swap after the leader (Clean the Sun: 33).
- Porting a mobile puzzle grid without a social or physical hook (Blast a Block: 53).
- Taking a Steam CCU spike as an opening on Roblox when Roblox already owns the genre (ROB RUN).

## Caveats
> [!warning] Unverified
> Every Steam and mobile figure comes from a WebSearch snippet, because WebFetch was blocked on all hosts (ENOTFOUND). Sales figures for Worst Class Ever and Probably Stolen are developer or publisher claims. Peaks differ across trackers, and the latest snapshot is used.

- Roblox CCU is a single live snapshot taken on 2026-11-14, a Saturday, when weekend inflation applies (rule 16). Weekday numbers will be lower.
- The Roblox searches are keyword-based and return the top 5–8 results each, so a port with an unusual title could be missed. Search "worst class" and "prank" again before building.
- Moon Sweepers' Roblox copies (Clean the Moon, Oct 11–12) predate the Steam launch (Oct 23). They were probably made from the trailer or demo, so the original's influence there is inferred.
- I could not confirm Smash Fest!'s exact mechanic beyond "aim a cannon at stacked objects" (FoxData and Gamigion snippets).
- I found no fresh 2026 data for Katamari, idle miners or Megabonk; those are listed as evergreen.

## Sources
1. Worst Class Ever SteamDB charts: https://steamdb.info/app/5175310/charts/
2. Worst Class Ever 100K copies day one (Steam news): https://store.steampowered.com/news/app/5175310/view/719047432802926646
3. GameSpark launch report: https://gamespark.jp/article/2026/11/10/174723.html
4. Probably Stolen 100K players (TheGamer): https://www.thegamer.com/probably-stolen-indie-game-100000-players-on-steam/
5. Probably Stolen 500K in 2 days (Notebookcheck): https://notebookcheck.net/500K-sales-in-2-days-This-indie-game-with-96-positive-reviews-is-blowing-up.1440296.0.html
6. Probably Stolen 186K peak (games.gg): https://games.gg/news/probably-stolen-cyberpunk-shopkeeper-sim-steam-surge/
7. Probably Stolen 750K in 5 days: https://tech-insider.org/probably-stolen-750k-copies-5-days-gamediscoverco-2026/
8. Moon Sweepers player count: https://steamdb.com/en/tools/steam-charts/5335510-moon-sweepers
9. Moon Sweepers (mein-mmo): https://mein-mmo.de/steam-moon-sweepers-hit/
10. ROB RUN 365K peak (SteamDB news): https://store.steampowered.com/news/group/4777282/view/712291505861034339
11. ROB RUN reviews (GameRant): https://gamerant.com/games-like-gta-6-rob-run-reviews/
12. How to Fish 1M in 2 days (GamesRadar): https://www.gamesradar.com/games/co-op/latest-steam-lottery-winner-how-to-fish-sells-1-million-copies-in-2-days-yes-well-be-adding-more-content/
13. How to Fish August sales (Cinevva): https://app.cinevva.com/news/2026-09-04-how-to-fish-august-indie-sales
14. Megabonk 1M (PC Gamer): https://www.pcgamer.com/games/roguelike/vampire-survivors-like-megabonk-makes-megabucks-selling-a-million-copies-in-2-weeks-and-currently-has-more-daily-players-than-borderlands-4-on-steam-ill-be-eating-spaghetti-with-extra-sauce-tonight
15. Ball x Pit 2M (VGChartz): https://www.vgchartz.com/article/468682/ball-x-pit-sales-top-2-million-units-free-update-out-now/
16. Ball x Pit 300K in 5 days (PC Gamer): https://www.pcgamer.com/games/roguelike/ball-bouncing-city-building-off-the-wall-roguelike-ball-x-pit-is-a-huge-hit-selling-300-000-copies-in-just-its-first-five-days-on-sale/
17. Super Battle Golf: https://steamcharts.com/app/4069520
18. PEAK (Alinea): https://alineaanalytics.substack.com/p/peak-sold-18-million-copies-last
19. R.E.P.O. SteamDB: https://steamdb.info/app/3241660/charts
20. Schedule I 459K (TweakTown): https://www.tweaktown.com/news/104474/schedule-hits-459k-peak-players-the-most-by-solo-developer-in-steam-history/index.html
21. Supermarket Simulator (GWO via WN Hub): https://wnhub.io/news/stores-and-publishing/item-43033
22. Bongo Cat (Steambase): https://steambase.io/games/bongo-cat
23. Pixel Flow $198M (PocketGamer.biz): https://www.pocketgamer.biz/loom-games-pixel-flow-makes-almost-200m-in-player-spending-during-first-year/
24. Sensor Tower Oct 2026 top 10: https://sensortower.com/blog/top-10-worldwide-mobile-games-by-revenue-and-downloads-in-october-2026
25. Sensor Tower Sep 2026 top 10: https://sensortower.com/blog/top-10-worldwide-mobile-games-by-revenue-and-downloads-in-september-2026
26. FoxData Oct 2026 rankings: https://foxdata.com/en/blogs/global-mobile-game-rankings-october-2026-top-15-downloads-revenue/
27. Arrows June downloads (mobilegamer.biz): https://mobilegamer.biz/junes-top-mobile-game-downloads-arrows-amaze-go-free-fire-max-roblox-more/
28. Meowdoku June (PocketGamer.biz): https://www.pocketgamer.biz/june-2026-mobile-game-charts/
29. Smash Fest! (FoxData): https://foxdata.com/en/blogs/how-smash-fest-hit-1-on-the-us-app-store-with-zero-paid-uaand-what-it-means-for-hybrid-casual/
30. Smash Fest! (Gamigion): https://www.gamigion.com/smash-fest-casual-liveops-turned-into-genre-wide-trend/
31. Hole.io 2025 (Appfigures): https://appfigures.com/resources/insights/20250314/amp?f=4
32. Colony Flow (Mobidictum): https://mobidictum.com/?p=410270
33. Meccha Chameleon Roblox clones (Kotaku): https://kotaku.com/more-people-are-playing-meccha-chameleon-knock-offs-than-the-original-hit-steam-game-as-the-roblox-clone-machine-goes-into-overdrive-2000715371
34. Roblox live data: `python3 tools/roblox_intel.py search` run on 2026-11-14; raw output in session scratchpad
