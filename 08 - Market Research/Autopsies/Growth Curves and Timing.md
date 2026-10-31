---
tags: [market-research, roblox, autopsy, growth-curves, timing, ccu]
updated: 2026-10-31
sources: 22
status: draft
---

# Growth Curves and Timing

How fast simple one-action Roblox games rise, how long they last, and what a flop looks like. Measured against the owner's bar: **1K+ CCU means it worked, 10K+ means it hit.**

**Method:** I pulled full CCU histories from the RoWatcher public API (`/api/v1/games/<id>/history`, samples every 2–30 min) for 35 named games, 63 weekly gainers and about 250 more sweep games created since July 2026 (345 games in all). I reduced each day to a **daily peak** (the 2nd-highest sample of the UTC day, which removes single-sample glitches) and a **sustained level** (the trailing 7-day median of the daily peaks, which removes weekend event spikes). Live CCU comes from `tools/roblox_intel.py` (Roblox API, 2026-10-31 ~09:00 UTC). The processed data is in `08 - Market Research/Data/growth-curves-2026-10-31.json`. Related notes: [[Tier A - Roblox Velocity]], [[Simple Action Loops Scorecard]].

## TL;DR
- **Traction shows up in weeks 2–5, not in days.** Among games where we saw the crossing, the median day to **10K is day 25** (n=39, range 4–86). Once a game reaches 1K, **10K follows in a median of 5 days** (n=15; 9 of 15 within 6 days). A game that sits at 1–3K for more than 2 weeks almost always tops out under 10K.
- **The decision window is day 14 to day 35.** Winners seen from launch were at a median of **360 CCU on day 7 and 2,660 on day 14 (×4.2)**, and 7 of 8 had at least one day where CCU doubled. Games that capped at 1–10K were at **111, then 187 (×1.5)**. True flops sit flat under 150 and fall in week 2.
- **Half-life is about 12 days.** After the sustained peak, the 7-day level halves in a median of **12 days** (10K–100K peaks: n=47, middle half 10–17 days, 46 of 47 halved) and falls to 25% by about **day 19**. Peaks come at a median of **day ~32** after creation.
- **New gainers fade, old games keep their gains.** New 2026 games in the W37–W39 gainer lists are now at a median of **22% of their digest-week level** (only 3 of 20 kept ≥50%, and 8 of 20 are below 10%). Returning established games (AR2, Lumber Tycoon 2, PHIGHTING, Dandy's World, Anime Adventures) are at **0.76–2.8×**.
- **Updates and events give spikes, not a step up.** 74% of spike days fall on **Fri–Sun** (Sat alone is 37%). The median spike is **×2.3** (p90 ×4.5). Two to four days later, CCU sits at a median of **1.35× the pre-spike level**, but 35% of the time it is back below where it started.
- **A clone can still win about 70 days into a wave, but only with a new verb.** The egg wave (Steal An Egg, created Jul 25) still produced 100K+ games created on day 42 (Break and Steal an Egg), day 43 (Climb For Animals Eggs) and day 71 (Fake an Egg). Skin-swap clones (Soccer, Dino, Hello Kitty, Claw egg) peaked at 42–1.7K.

## Per-game table

Column notes. **First seen** is when RoWatcher started tracking: when the game was already at 1K or 10K by then, the days-to value is written as "≤d". **Spike peak** is the highest single day, usually a weekend event. **Sustained** is the peak of the 7-day median. **Retained** is live CCU divided by sustained peak. **½-life** counts days from the sustained peak until the 7-day level fell below 50%.

### 15 hits

| Game | Universe ID | Created | First seen (day @ CCU) | Day 1K | Day 10K | Spike peak (date) | Sustained peak (day) | Live 10-31 | Retained | ½-life | Early trajectory and update pattern |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Steal An Egg | 10563114921 | 2026-07-25 | d12 @ 14.1K | ≤12 | ≤12 | 9.9M–14.3M (Sep 5–12; RoWatcher figure, single-day admin events) | 2.49M (d55) | 1.21M | 49% | not yet (98 days) | Day 12: 14K, day 13: 23K. Taken down Aug 8–11 ("Content Deleted"), then 78K → 517K by day 27 → 2.2M by day 28. 8 of 12 spikes on Saturdays at **×5–5.6** (weekly admin events). Weekday base drifting down since mid-Sept |
| Break and Steal an Egg | 10765288803 | 2026-09-05 | d23 @ 17.8K | ≤23 | ≤23 | 648K (Oct 25; RoTrends/RoWatcher list 1.3M Oct 18) | 228K (d43) | 95.5K | 40% | not yet | Days 23–28: 17K → 77K, then a Sunday spike of 392K on day 29 and a 240K plateau. Spikes ×2–7 |
| Anime Dice | 10708913337 | 2026-08-15 | d11 @ 247 | 17 | 22 | 103K (Oct 25) | 79.8K (d69) | 60.8K | 76% | not yet | Days 11–14: 247 → 529. Day 17: 1.4K, day 22: 12K, day 28: 34K. Slow, steady climber with "UPD n" title tags. Spikes ×2–2.7 on any weekday |
| Throw Food For Animals | 10766972131 | 2026-09-18 | d21 @ 153 | **33** | 36 | 134K (Oct 31) | 54.1K (d43) | 129K | rising | not yet | **Late bloomer.** Days 21–30: 40–150 CCU and flat to falling, then day 32: 336, day 34: 1.9K, day 36: 19K, day 42: 133K. Rode the Halloween algorithm push |
| DONT SPLASH | 10771421858 | 2026-10-17 | d3 @ 7.3K | ≤3 | **4** | 133K (Oct 30) | 109K (d14) | 83.5K | 76% | not yet | Fastest in the set: 7K → 20K → 32K → 54K → 89K → 116K on days 3–8. "NEW STAGES" update on Oct 23 (day 6). W43 top gainer (+1,032%) |
| My Anime Mine | 10740316645 | 2026-08-19 | d12 @ 104 | **25** | **50** | 24.3K (Oct 24) | 19.2K (d69) | 14.2K | 73% | not yet | **Slow burner.** Days 12–21: 100–300. Day 28: 1.8K, day 38: 5.3K, day 50: 10K. The Tier A log called it a "745-peak flop" on Sep 12, which turned out wrong |
| +1 Anime Eyes | 10770933473 | 2026-10-14 | d13 @ 14.2K | ≤13 | ≤13 | 50.2K (Oct 30) | 35.6K (d17) | 30.9K | 88% | not yet | 14K → 13K → 36K → 50K on days 13–16. Two weeks old, still near its peak |
| Fake an Egg | 10769384180 | 2026-10-04 | d13 @ 20.7K | ≤13 | ≤13 | 142K (Oct 25) | 52.9K (d26) | 43.1K | 82% | not yet | Days 13–20: 20–30K, day 22: 51K, then a Sunday spike of 142K. Renamed "[30 MIN]" on Oct 22 for a timed event: **×5.5 within 3 days** |
| Steal A Pet And Ride It! | 10769315427 | 2026-10-04 | d19 @ 21.9K | ≤21 | ≤21 | 46.3K (Oct 31) | 36.8K (d27) | 44.2K | at peak | not yet | 22K → 17K → 19K → 37K → 44K → 46K on days 19–27 |
| Ride a Dino | 10758824872 | 2026-08-24 | d52 @ 4.0K | ≤52 | 54 | 110K (Oct 25) | 43.4K (d62) | 22.2K | 51% | 1 day (spike-driven) | Discovered at day 52 with 4K. One Sunday spike of **×8.3**. Weekend/weekday ratio 2.7 (very weekend-heavy) |
| Feed A Mosquito | 10747719434 | 2026-08-21 | d51 @ 3.9K | ≤51 | 52 | 42.2K (Oct 24) | 31.3K (d68) | 24.5K | 79% | not yet | Under 1K for most of its first 7 weeks (W42 shows 8.1K after **+432%**), then grew through V3/V4 updates |
| Grow a Garden (2025) | 7436755782 | 2025-03-25 | (tracked from 2026-06) | — | — | 21.3M (Jun 21 2025); all-time high 22.3–22.4M (Aug 23 2025) per press | 2026: 53K | 23.2K | ~0.1% of ATH | — | Press timeline: launched Mar 26 2025. About 5M at the May 18 "Blood Moon" update (about **day 53**), 11.7M on May 31, 16.4M on Jun 14, 21.3M on Jun 21 (**about day 87**). In 2026 it still runs **12 of 12 Saturday events at ×4.1–4.8** |
| Steal a Brainrot (2025) | 7709344486 | 2025-05-16 | (tracked from 2026-06) | — | — | 25.4M (Aug 23 or Oct 2025, sources disagree) | 2026: 341K | 342K | ~1.3% of ATH | — | Press: about 5M in Jul 2025 and 20M on Aug 23 2025 (about **day 99**). Still 342K at 17 months, with Sat/Sun/Tue events at ×1.7–2.6 |
| 99 Nights in the Forest (2025) | 7326934954 | 2025-03-04 | (tracked from 2026-06) | — | — | 14.2M (2025, press) | 2026: 344K | 215K | ~1.5% of ATH | 46 days (2026 plateau) | Weekend events at ×1.6–2.9. Peak date is not confirmed in the sources fetched |
| Dead Rails (2025) | 7018190066 | 2025-01-01 | (tracked from 2026-06) | — | — | 2025 claims of 200K+ (600K weekends, unverified); RoWatcher ATH 79K (Nov 2025) | 2026: 34.1K | 22.9K | 67% of 2026 level | 25 days | Took off around **day 55** after Roblox's official accounts promoted it in late Feb 2025. In 2026 it gets Saturday events at ×1.6–3.1 |

Reference collapse (not one of the 15): **Ride A Pet** (10035204815, created Apr 14 2026). It sat **151 days at under 5K**, then grew 4.9K → 71K → 170K on days 151–157, with spikes of 808K (Sep 19) and 1.42M (Sep 26). Sustained peak 270K on day 168. **½-life 10 days.** Live 21.6K, which is **8% of sustained peak and 1.5% of spike peak**. It is the clearest example of an old game being revived by one update and then decaying fast.

### 15 flops and collapses (peaks of 100–3K, or a big peak followed by a crash)

| Game | Universe ID | Created | First seen | Day 1K | Day 10K | Spike peak | Sustained (day) | Live | Retained | ½-life | Early trajectory: what went wrong |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kaiju Zero | 10768540520 | 2026-09-29 | d0 @ 23 | never | never | 786 (Oct 30) | 384 (d32) | 452 | — | — | 23–25 CCU on days 0–1, about 400 by day 32. Never had a doubling day. **Flop by the 1K bar**, though it is creeping up |
| Raise a Kaiju | 10767871547 | 2026-09-24 | d34 @ 0 | never | never | 0 | 0 | 3 | — | — | 25.9K lifetime visits. Dead on arrival |
| Raise a KAIJU and destroy a CITY | 10770428190 | 2026-10-11 | not on RoWatcher | never | never | 33 (RoTrends ATH) | — | 0 | 0% | — | 22K visits. Last updated day 2, then abandoned |
| Tap to Grow a Kaiju! | 10769680228 | 2026-10-06 | d9 @ 73 | never | never | 132 (d13) | 79 (d13) | 39 | 49% | — | 73 → 57 → 95 → 79 → 132 → 44 on days 9–14. **Lower in week 2 than in week 1** |
| Steal An Soccer Egg | 10765753780 | 2026-09-09 | d26 @ 25 | never | never | 42 | 25 | 18 | — | — | 13–42 CCU. Skin-swap clone, last updated 48 days ago |
| Survive the Garden | 10765982039 | 2026-09-11 | d37 @ 177 | never | never | 1.2K one day (otherwise 239) | 177 (d37) | 86 | ~40% | 3 days | Flat at 100–180, with one event day |
| Steal a Dino Egg | 10760645243 | 2026-08-25 | d11 @ 393 | 52 | never | 1.06K (Oct 16) | 877 (d63) | 349 | 40% | — | Took 7 weeks to touch 1K, then slid back. Skin-swap clone |
| Steal an Egg With a Claw | 10770630360 | 2026-10-13 | d6 @ 125 | 16 | never | 1.7K (Oct 30) | 831 (d18) | 1.09K | ~130% | — | 125 → 628 → 217 → 87 → 1.7K on days 6–10. **Choppy, with no compounding.** "Worked" by the 1K bar but plateaued |
| Steal an Hello Kitty! | 10766884294 | 2026-09-18 | d20 @ 1.1K | ≤20 | never | 1.3K | 1.15K (d20) | 489 | 43% | 15 days | Peaked the week it was found, then drifted down. IP-skin clone |
| +1 Garden Evolution | 10765972921 | 2026-09-11 | d11 @ 5 | 45 | never | 1.6K (Oct 29) | 1.17K (d50) | 628 | 54% | — | 5 → 54 → 244 → 1K by day 45. Grow-a clone with a slow crawl |
| Grow a Plant | 10768292556 | 2026-09-27 | d9 @ 1.6K | ≤9 | 20 | 37.7K (spike) | 9.2K (d25) | 2.8K | 30% | **8 days** | 1.6K on day 9, a ×9.4 Saturday spike to 22.6K on day 20, then down to 2.8K. Grow-a clone with a spike-led collapse |
| Steal Brainrot Eggs | 10765158636 | 2026-09-04 | d4 @ 123 | 12 | never | 5.3K | 3.7K (d21) | 918 | 25% | **6 days** | 123 → 214 → 1.2K → 3.3K on days 4–14, peaked day 18, halved by day 27 |
| Steal A Brainrot Egg | 10757504146 | 2026-08-23 | d7 @ 257 | 10 | 20 | 13.6K | 8.5K (d22) | 1.1K | 13% | 14 days | 257 → 1.1K → 8.1K on days 7–14, peaked day 21, about 13% left by day 69 |
| Steal Animal Egg | 10766056678 | 2026-09-11 | d21 @ 15.6K | ≤21 | ≤21 | 107K (Oct 10) | 30.9K (d29) | 1.9K | **6%** | **11 days** | Reached 30K within days of discovery, with Saturday spikes at ×3.3, then fell 30K → 5.7K between days 30 and 40 |
| Steal Fish Eggs | 10718240577 | 2026-08-16 | d19 @ 814 | 21 | 25 | 45.7K (Sep 13) | 15.6K (d29) | 497 | **3%** | 17 days | W37 top gainer (+447%). 814 → 3.2K → 15.5K on days 19–25, peaked day 28, at 3% by day 76 |
| Grow a Garden 2 | 10200395747 | 2026-05-21 | d40 @ 512K | ≤40 | ≤40 | 532K (Aug 3) | 522K (d74) | 1.45K | **0.3%** | 18 days | Sequel with a big start (a different GAG2 listing, 10004943774, reportedly hit 976K in June). Went from 500K to near zero within about 2 months of its peak |
| Ride An Egg | 10767808614 | 2026-09-24 | not on RoWatcher | ? | — | 9.38K = **today** (RoTrends ATH) | 7-day average 1.31K | 9.16K | at peak | — | Low for 5 weeks (1.05M lifetime visits), and on **day 37** it is breaking out. Not a flop: an example of a late riser |

> [!warning] Unverified
> The single-day peaks of Steal An Egg (9.9M–14.3M) and Ride A Pet (1.42M) come from RoWatcher. Intraday samples show a smooth multi-hour ramp (for example, Steal An Egg went 2.5M → 3.0M+ over two hours on Sep 5), which looks like a real admin-abuse event rather than a glitch. But no second tracker confirms the size. Sustained (7-day median) figures are the safer numbers to quote.

## Weekly gainers log (RoWatcher "Week in Numbers", W37–W43)

The "now" column is the 7-day median of daily peaks for Oct 25–31, divided by the median for the digest week. RoWatcher published only 7 numbered digests in Sept–Oct (no W36 or W44 exists). The 8th source is the set of 4 RoWatcher weekly narrative posts (Oct 5, 12, 19 and 26).

| Week | Platform | Top gainers (CCU, WoW) | New & notable | Where they are now |
|---|---|---|---|---|
| W37 Sep 7–13 | avg +2%; 286,963 new games; 545 breakouts | Steal Fish Eggs 6.5K +447%; How to Fisch! 11.4K +426%; Anime Dice 34.9K +322%; +1 Tongue Escape 32.4K +302%; MM2 of The Locust 11.3K +280% | Jump To Steal An Egg 45K; +1 Speed Snow Keyboard Escape 38K; Lift a Cube 29K; +1 Mog Evolution 23K; SAEM admin panel 22K | **Anime Dice ×2.68 (only survivor)**. Steal Fish Eggs ×0.04, Fisch ×0.23, Tongue ×0.22, Jump To Steal ×0.22, Snow Keyboard ×0.05, Lift a Cube ×0.01, Mog ×0.12 |
| W38 Sep 14–20 | avg 11.7M (−2.3%), peak 16.1M | Ride A Pet 92.6K +1,753%; Flip a House 27.7K +762%; Apocalypse Rising 2 +700%; Lumber Tycoon 2 +444%; Locust MM2 +371% | The Hunt: Roblox 20 381K; +1 Loot To Forge 34K; Verity's Game 25K; Swing For Eggs 24K; Survive The Slope 22K | Ride A Pet ×0.23; Flip a House ×0.05; AR2 ×0.89, LT2 ×0.76 (old games hold); The Hunt ×0.00 (one-off event); Loot To Forge ×0.31; Swing For Eggs ×0.27; Slope ×0.01 |
| W39 Sep 21–27 | avg −3%; 465,915 new; 1,515 breakouts | Grapple Cart Obby +1,164%; PHIGHTING! +735%; Dream Car Collection +549%; Build An Ant Empire +397%; Mine Antarctica +344% | Rauls Rivals Modded 61K; AMR Test Lab 35K; Steal From The Rich 32K; Steal all Cars 23K | Grapple ×0.27; PHIGHTING ×1.44; Dream Car ×0.59; Ant Empire ×1.70; Mine Antarctica ×0.27; Steal From The Rich ×0.36; Steal all Cars ×0.05 |
| W40 Sep 28–Oct 4 | avg 11.2M (−5.5%); 975,230 new; Survival +45% | 7 Days Cat-Sitting 34K +825%; Dandy's World 192K +408%; Renovate A House +344%; Melt All The Ice +343%; +1 Stone Skipping 23K +341% | **Break and Steal an Egg 392K**; Huss Valley 120K; Sarab 51K; Paint to Get Rich 47K; Steal an Clown Egg 36K | Cat-Sitting ×0.67; Dandy's ×2.61; Renovate ×1.51; Melt ×0.52; Stone Skipping ×0.70; Break & Steal ×4.07; Huss ×1.19; Sarab ×0.27; Paint ×0.29; Clown Egg ×0.41 |
| W41 Oct 5–11 | avg +3%; 911,650 new; 5,632 breakouts | Cameraman TD +543%; Anime Zero 37.9K +430%; Shoot For Eggs +373%; Build and Conquer +323%; Run Or Be Rich +317% | Makeup Mania 65K; Climb For Animals Eggs 41K; +1 Speed Controller Escape 41K; Sari-Sari Store 30K; Call A Pet 29K | Cameraman ×11.7; Anime Zero ×0.16; Shoot For Eggs ×0.06; Run Or Be Rich ×0.00; Makeup Mania ×0.02; **Climb For Animals Eggs ×2.71**; Controller Escape ×0.02; Call A Pet ×0.02 |
| W42 Oct 12–18 | avg +3.9%; 1,040,184 new; narrative post: platform 15.4M (+29.8%) | Tribes 3v3 +1,101%; Tap Simulator REBORN +627%; Cat Battles 45.6K +584%; Feed A Mosquito +432%; Facecard +427% | Bike For Egg 60.5K; Ride a Dino 39K; Lucky Scoop Order 28K; Backseat Rally 27K; Fake an Egg 23.9K | Too early: median ×1.08. Cat Battles ×4.38, Fake an Egg ×2.37, Mosquito ×2.53, Ride a Dino ×1.56 |
| W43 Oct 19–25 | avg 12.5M (+4.1%); 1,342,320 new; narrative post: platform 16.6M (+38%, Halloween) | Anime Adventures +2,888%; Ragdoll Reality +2,525%; **DONT SPLASH 82.9K +1,032%**; Steel Fighters +651%; Bike Universe +639% | The Hollow 449K; DONT SPLASH 116K; Train Pets for Eggs 41K; Rivals Modded Admin 28K; PINKIE PROMISE 26K | Too early. The Hollow already ×0.90 off a 449K debut-day peak |

**What the log says**
- **New games fade by week 5–7.** W37–39 new entries: median ×0.22 now, 3 of 20 ≥×0.5, 8 of 20 below ×0.1, and a median of **3.5% of their raw peak**. W40–41 (3–4 weeks on): median ×0.52, 10 of 19 ≥×0.5. W42–43: median ×1.08, still in their rise.
- **Old games revived by an update keep the gain** (AR2, LT2, PHIGHTING, Dandy's World, Anime Adventures: ×0.76–2.84). A new game's gainer week is usually its peak week; an established game's gain is a step up.
- **New games first appear on the list at a median age of day 29** (n=57, range 6–159). That matches the day-25 median for reaching 10K.
- **Kinds of games that gain:** (1) egg-loop variants (Swing / Shoot / Climb / Bike / Train-for / Fake / Break-and-Steal), 10 of 57 new entries; (2) "+1 X" incrementals; (3) seasonal horror/anomaly games (Cat-Sitting, PINKIE PROMISE, The Hollow, DONT SPLASH); (4) one-off events (The Hunt, admin-panel copies) that drop to zero within 2 weeks. Among egg games, the ones with a **new verb** (Break, Climb, Bike, Fake) are still at ×0.88–4.07; the ones with an object swap or thin twist (Fish, Shoot, Jump-to, Clown) are at ×0.04–0.41.
- **October is seasonally inflated.** Platform CCU rose +29.8% in the week of Oct 17 and +38% in the week of Oct 24 (Halloween). Late-October retention figures look better than they will in November.

## Timing laws (with numbers)

1. **Traction law.** Reaching 10K takes a median of **25 days** (n=39, middle half about 16–45 days). Reaching 1K, where we saw the crossing, takes a median of **day 33** (n=21, range 3–83). That figure skews late, because games already over 1K when discovered drop out of the count. Fast hits (DONT SPLASH 10K on day 4, Cat Battles day 9, Ragdoll Reality day 9) are the minority.
2. **Breakout law.** **1K → 10K takes a median of 5 days** (n=15; 60% within 6 days; maximum 25). If a game has held 1–3K for 14+ days without a doubling day, expect a cap at 1–10K (Hello Kitty, Dino Egg, Claw Egg, +1 Garden Evolution, Steal Brainrot Eggs).
3. **"Dead by day X" law (with an honest caveat).** In the RoWatcher-tracked sample, games still under 1K reached it later at these rates: **day 14: 79%** (n=28), **day 30: 60%** (n=35), **day 45: 30%** (n=23). Reached 10K later: 39%, 26% and 22%. That sample is **survivor-biased**, because RoWatcher only tracks games that showed some signal. The unbiased cross-section from the sweep (395 games) has **48% of games aged 14–30 days at 1K+, and 31–32% of games aged 30–120 days**. The share does not grow after day 30, so late arrivals are matched by decay. Working rule: **under 100 CCU at day 30, with no week-on-week growth and no recent update, means it is not recovering.** The tracked flops never got past 150 (Tap to Grow a Kaiju, Soccer Egg, Raise a Kaiju, Survive the Garden). **Under 1K but growing ×1.5+ per week while updating is still alive.** My Anime Mine went 300 → 1K → 10K on days 21 → 25 → 50; Throw Food went 150 → 1.9K → 19K on days 30 → 34 → 36; Steal and Fish an Egg went 30 → 1K → 10K on days 34 → 35 → 45. Ride An Egg is breaking out on day 37.
4. **Peak timing.** The sustained peak arrives at a median of **day 32** from creation, the same across every bucket from under 1K to 100K+ (n=345). Hits typically climb **2–5 weeks past the 10K crossing** (Anime Dice: day 22 → day 69; Break & Steal: day ≤23 → day 43).
5. **Half-life law.** Measured on the 7-day median: **½ in 12 days** for 10K–100K peaks (n=47, 46 of 47 halved, middle half 10–17 days) and also **12 days** for 3K–10K peaks (n=32). It reaches **25% by about day 19** after the peak. Fast clone collapses: Steal Brainrot Eggs 6 days, Grow a Plant 8, Ride A Pet 10, Steal Animal Egg 11, Steal Fish Eggs 17, Grow a Garden 2 18. Platform-scale games run on a different clock: Steal An Egg is only now near ½ after about 6 weeks, 99 Nights 46 days, Grow a Garden 64 days.
6. **Wave law.** A noun wave (eggs, Jul 25 → now) can still create 100K+ entrants up to **about day 70** after the first hit: Break & Steal on day 42, Climb For Animals Eggs day 43, Bike For Egg day 52, Fake an Egg and Steal A Pet And Ride It day 71. Each needed a **new verb**. Pure reskins created any time in the wave peaked at 42–1.7K. The parent's own ½-life (about 6+ weeks for a platform #1) sets roughly how long the wave lasts. The brainrot wave's parent is still at 342K after 17 months, but its 2026 clones collapse (Steal A Brainrot Egg is at 13%).
7. **Revival law.** Old, quiet games can explode from one update (Ride A Pet: 151 days under 5K, then 270K sustained) but then decay with the same ~10–12 day ½-life. Revived **established** IPs keep their gains (AR2, LT2, Dandy's World).

## Flop signatures (days 0–14)

| Signal | Winner (peak ≥10K, n=8 seen from ≤day 7) | Capped at 1–10K (n=7) | Flop (peak <1K; Kaiju Zero, Tap to Grow, Soccer Egg, Raise a Kaiju) |
|---|---|---|---|
| CCU day 7 | median **360** | 111 | 0–75 |
| CCU day 14 | median **2,660** | 187 | 25–130 |
| Day 14 ÷ day 7 | **×4.2** | ×1.5 | ≤×1, often falling (Tap to Grow: 132 → 44) |
| A day that doubles the day before | 7 of 8 | 4 of 7 | 0 |
| Weekend lift | ×1.5–3 on Sat/Sun | choppy | none |
| After the first spike | the trough between spikes rises week on week | the trough stays flat | — |

**Collapse signature (fast clones that do hit 10K):** the climb is driven by the title plus one weekend spike that is **×3–9 the weekday level** (Grow a Plant ×9.4, Steal Animal Egg 107K spike vs 31K sustained, Ride A Pet 1.42M vs 270K). Then the weekday trough starts falling **within 7 days of the sustained peak**, and the 7-day level halves in 6–17 days. Spike size alone does not predict a collapse: Steal An Egg runs ×5 Saturdays and holds. **The best tell is whether the weekday trough after each spike is higher or lower than the one before.**

## Update and event effect

- **When spikes happen:** of 733 spike days (≥1.6× the prior 3-day median, base ≥1K) across tracked games with peaks of 5K+: **Sat 37%, Sun 23%, Fri 14%**, Thu 8%, Wed 7%, Mon 6%, Tue 5%. Weekend events and update drops are the norm.
- **Size:** median **×2.3** (Sat median ×2.65), p90 ×4.5. Mature weekly-event games: Grow a Garden ×4.1–4.8 every Saturday (12 of 12 weeks), Steal An Egg ×5–5.6 on event Saturdays, 99 Nights / Dead Rails / Steal a Brainrot ×1.6–3.
- **What remains afterwards:** 2–4 days after a spike, CCU is at a median of **1.35×** the pre-spike level. 55% of spikes left CCU more than 1.2× higher; **35% left it below where it started** (n=714). This is taken during mostly-growing periods, so the true lasting lift is lower.
- **Typical weekend lift** (Sat/Sun ÷ Mon–Thu, weeks at ≥1K): median **×1.54** (n=574 weeks).
- **Timed events:** Fake an Egg's "[30 MIN]" rename gave **×5.5 within 3 days**. Steal Fish Eggs' title-tag renames gave ×2.8–7.1 for one day each, while its trend kept falling. Events lift a game's day; they do not stop the decay.
- **Season:** a Halloween update plus the October platform tide (+30–38% WoW) is why nearly every W41–W43 gainer has 🎃 in its title.

## Checklist
- [ ] Ship by a Friday so the first weekend falls on days 1–3. Plan a weekend event or update for every Saturday of the first 6 weeks (74% of lifts land Fri–Sun).
- [ ] Track the daily peak and the 7-day median from day 1. **Day 7 target: 300+. Day 14 target: 2K+, or ×4 over day 7.**
- [ ] On day 14, if CCU is under 150 and flat or falling with no doubling day, change the hook (title, thumbnail, verb) instead of adding content.
- [ ] On day 30, if CCU is under 100 with no week-on-week growth, kill it or pivot. If it is under 1K but growing ×1.5 a week, keep updating weekly, as the late bloomers did.
- [ ] Once past 1K, expect 10K within about a week. If 1–3K holds for 2+ weeks, treat ~3K as the ceiling and put effort into retention, not acquisition.
- [ ] After the peak, budget for about a 12-day half-life. Prepare the next big update before day 10 after the peak.
- [ ] When cloning a wave, change the **verb** (Break / Fake / Ride / Climb), not the noun, and launch within about 70 days of the wave parent.

## Common Mistakes
- Reading a single-day peak (a weekend admin event) as the game's level. Quote 7-day medians.
- Calling a game dead at day 14 when it is at 100–300 and rising. My Anime Mine and Throw Food would have been written off.
- Trusting RoWatcher "days to 1K/10K" for games it discovered late. Use the "≤" values as upper bounds.
- Comparing late-October retention to other months: Halloween inflated platform CCU by +30–38%.
- Expecting a gainer-list appearance to last. For new games it is usually the peak week.

## Caveats
- **Survivor bias.** RoWatcher only tracks games once they show a signal (discoverySource: chart / clone_search), and my sweep sample was filtered to 100K+ visits. Flops are therefore under-represented, and the late-recovery rates in law 3 are upper bounds.
- **Late discovery.** 11 of the 15 hits were first tracked when already at 4K–21K (first seen on days 3–52), so their day-0–7 curves are missing. The winner vs flop comparison rests on only 8 + 7 games seen from day 7 or earlier.
- **The 2025 mega-hits have no launch data.** RoWatcher's history for them starts in mid-2026. Their launch timelines come from press reports, which disagree (Steal a Brainrot's 25.4M is dated Aug 23 or Oct 2025 depending on the source). Dead Rails' 2025 peak could not be verified, because gameanalytics.com and gameranx.com are blocked by the session's network settings.
- **Daily peak definition:** the 2nd-highest sample per UTC day. Days with sparse samples can understate or overstate the level. One filter removes days more than 4× both neighbours in the per-game table.
- **Tracker disagreement:** Break and Steal's peak reads 648K (this API, daily) vs 1.3M (RoWatcher/RoTrends page). Steal An Egg's reads 9.9M vs 14.3M. Ride An Egg and Raise a KAIJU…CITY are not on RoWatcher at all, so RoTrends was used for those two.
- **Update attribution is indirect.** RoWatcher's name-change log is sparse (0–5 entries per game), so "update effect" is inferred from spike days and title tags, not from actual publish times.
- Live CCU is a single snapshot (2026-10-31 ~09:00 UTC, Saturday morning in Europe and Friday night in the US), so weekend-sensitive games read high.

## Sources
- RoWatcher public API v1 (documented on the site's API docs page; base https://rowatcher.com/api/v1) · history: `https://rowatcher.com/api/v1/games/<universeId>/history?from=2025-01-01` · details: `https://rowatcher.com/api/v1/games/<universeId>` · changes: `https://rowatcher.com/api/v1/games/<universeId>/changes`
- RoWatcher game pages, e.g. https://rowatcher.com/games/10563114921/steal-an-egg · https://rowatcher.com/games/10765288803 · https://rowatcher.com/games/10771421858/dont-splash · https://rowatcher.com/games/10766972131 · https://rowatcher.com/games/10035204815
- RoWatcher Week in Numbers: https://rowatcher.com/news/roblox-week-in-numbers-2026-w37 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w38 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w39 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w40 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w41 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w42 · https://rowatcher.com/news/roblox-week-in-numbers-2026-w43
- RoWatcher weekly narratives: https://rowatcher.com/news/ccu-surges-39-as-egg-games-and-k-pop-demons-rule-the-week · https://rowatcher.com/news/roblox-hits-15-1m-ccu-as-halloween-surge-rewrites-the-charts · https://rowatcher.com/news/roblox-week-of-oct-17-ccu-surges-cats-battle-dinos-ride · https://rowatcher.com/news/halloween-surge-pushes-roblox-to-16-6m-ccu-week-of-oct-24
- RoTrends (Ride An Egg, Raise a KAIJU, Ride a Dino cross-check): https://www.rotrends.com/game/10767808614 · https://www.rotrends.com/game/10770428190 · https://www.rotrends.com/game/10758824872/Ride-a-Dino
- Roblox live stats via `tools/roblox_intel.py` (games.roblox.com APIs), 2026-10-31
- Grow a Garden timeline: https://en.wikipedia.org/wiki/Grow_a_Garden · https://www.gamesradar.com/games/mmo/with-21-million-concurrent-players-roblox-hit-grow-a-garden-is-bigger-than-half-of-steam-combined-but-players-are-already-flooding-another-far-weirder-competitor · https://allthings.how/grow-a-garden-player-count-server-limit-and-record-highs/
- Steal a Brainrot: https://www.wikiwand.com/en/articles/Steal_a_Brainrot · https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players · https://www.pocketgamer.biz/robloxs-peak-concurrent-user-count-hits-record-474m-as-steal-a-brainrot-and-grow-a-garden-compete
- 99 Nights in the Forest: https://www.pcgamer.com/games/survival-crafting/with-a-peak-player-count-of-14-2-million-99-nights-in-the-forest-has-an-audience-other-multiplayer-games-would-kill-for-to-find-these-behemoth-playerbases-you-need-to-be-on-a-platform-like-roblox/
- Dead Rails (search snippet only; page blocked): https://www.gameanalytics.com/blog/dead-rails-and-the-hit-makers-formula · https://rowatcher.com/games/7018190066/dead-rails
- Processed data: `08 - Market Research/Data/growth-curves-2026-10-31.json`; sweep base: `08 - Market Research/Data/sweep-verbs-2026-10-31.json`
