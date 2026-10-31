---
tags: [commissions, hiring, pricing, contracts, ip, briefs, production]
updated: 2026-10-31
sources: 25
status: draft
---
# Commissioning and Briefing Artists

## TL;DR
- **Rates vary 10x+**. Public Roblox price lists run from **500–800 R$ per accessory** at the cheap end to **5K–25K R$ (~$17–87) per single model**, **15K–75K R$ per sculpted character**, and **9K–70K R$ (€49–150) per advanced PBR model**. VFX: **1K–3K R$ per character aura, 1K–4K R$ per weapon aura, 5K–50K R$ for complex large-scale VFX**. US job-board averages for "Roblox modeling" sit around **$40/hr** (ZipRecruiter, June 2026).
- **Know the Robux maths**: DevEx pays **$0.0038/R$** for Robux earned since 2025-09-05 (legacy balances $0.0035; 30,000 R$ minimum), so 100K R$ ≈ $380 to the artist. Game-pass or shirt payments lose **30%** to Roblox; **group payouts are untaxed** (community consensus). Pay via group payouts or USD.
- **Write a brief** with: purpose, references (PureRef export), style sheet, technical spec (tris, texture size, maps, rig, file format), deliverables, deadline, revisions (typically **2 rounds of minor revisions included**), payment schedule (commonly **30% up front / 70% on delivery**), and rights.
- **Get IP in writing**. Freelancer terms differ: some transfer full ownership on 100% payment; others keep authorship and grant only a **non-exclusive licence for a single experience**. Roblox's upload terms require you to have the rights to what you upload.
- **Assets live in your group**: the artist sends source files (.blend/.spp/.fbx/.png), and *you* upload to the group. Use Asset Privacy and sharing (Restricted by default when enabled) to control access.
- **Anime IP**: commissioning fan art of licensed characters for a monetised game is a legal risk. Fan-game removals and DMCA disputes are common in the genre, and the 2026 Anime Vanguards lawsuit shows how revenue-share deals blow up without clear contracts.

## Why it matters for anime battlegrounds
Most battlegrounds games are built by small cores that commission VFX, animation and models move by move. Bad briefs waste revision rounds; unclear rights can cost you the game. Pricing literacy stops you from overpaying or (more often) underpaying and losing good artists mid-update.

## How to do it

### Step 1: Know the market (2024–2026 data points)
| Item | Price seen | Source type | Notes |
|---|---|---|---|
| Accessory, unrigged / rigged | 500 / 800 R$ | Team price sheet (carrd) | Low end |
| Large decoration | 1,000 R$ | Same | |
| Modelled asset (simple) | 500–700 R$; large object 600–1,000 R$ | DevForum price guide (older) | Beginner rates |
| Simple mesh + UVs (studio team offer) | 500–2K R$; larger (cars) 5K–10K R$ | Featherfly Studios hiring post (older) | |
| Small asset / small build | 200–9K R$ / 10K–20K R$ | `Aeksus` DevForum post (older) | Negotiable base prices |
| Asset models / vehicles | 1K–15K R$ / 10K–40K R$ | `Dr Radium` carrd | |
| Basic model, no textures | 1K–5K R$ (€5–20); basic PBR tier 1.5K–7K R$ | Modeller price list (DevForum) | |
| Advanced model, PBR/normal | 9K–70K R$ (€49–150) | Modeller price list | |
| Single asset | 5K–25K R$ (~$17–87) | Modeller (now closed) | |
| Sculpted character (high poly only) | 15K–75K R$ | Same | |
| Large map | up to ~$437 | Same | |
| Per-triangle pricing | ~$1.75 per 500-tri model | One modeller | Unusual model |
| Character aura VFX | 1K–3K R$ | VFX carrd (`assetstring`) | |
| Weapon aura VFX | 1K–4K R$ | Same | |
| Complex large-scale VFX | 5K–50K R$ | Same | Ultimates, domains |
| Simple / advanced aura | 100–500 / 500–10K R$ | Another VFX artist | |
| Hourly "Roblox modeling" (US) | avg $40.33; most $31.25–43.51 | ZipRecruiter (Jun 2026) | US job-board data |
| Salaried builder and modeller | $35K USD/yr | DevForum hiring post | Full-time |
| Monthly modeller retainer | 20K R$/month | DevForum hiring post (older) | |

> [!warning] Unverified
> These are individual price lists and job posts, many undated or pre-2024. There is no official Talent Hub rate survey. Use them as **ranges**, and ask artists for their current rate card.

**Robux to real money:**
| Robux | Artist cash via DevEx ($0.0038) | Notes |
|---|---|---|
| 10,000 | ~$38 | |
| 30,000 | ~$114 | DevEx minimum |
| 100,000 | ~$380 | |
| 100,000 via game pass | the artist receives 70,000 → ~$266 | 30% marketplace fee; 60% if bought through another experience |

Since 2026-06-08 Roblox also pays about **42% more** (≈$0.0054/R$) on qualifying spend by US players aged 18+ in eligible games. It's a blended effect, not a flat rate.

### Step 2: Choose where to hire
| Channel | Pros | Cons |
|---|---|---|
| Roblox **Talent Hub** | Built-in; compensation can be set as Robux, currency or revenue %; filter by pay | Users report UX gaps and unclear payment docs |
| DevForum "Find and Hire Talent" | Big pool; portfolios linked | Lots of noise |
| Discord (community servers, artists' own) | Fast; where most anime-game freelancers live | No escrow; scams |
| Fiverr / Twine / carrd portfolios | Escrow on Fiverr; USD invoicing | Fees; quality varies widely |
| X (Twitter) portfolios | See recent work, e.g. VFX test clips | DMs only |

Portfolio filter, a minimum bar for anime battlegrounds work:
- In-engine **Roblox Studio clips** (not only Blender renders) at game camera distance.
- For VFX: at least 3 complete moves with startup, impact and dissipation, ideally from shipped games (see [[Public Roblox Artist Portfolios]]).
- For models: wireframes + tri counts + texture sizes shown.
- Clear terms page: payment, revisions, rights.

### Step 3: Write the brief (template)
```
PROJECT: <game name> — <asset name>            DEADLINE: <date>
PURPOSE: What it is and where it's seen (e.g. "Ultimate for Character X, seen
         mid-combat at 20–60 studs, phone + PC").
REFERENCES: PureRef board export (link), 3 "do" refs, 2 "don't" refs.
STYLE: Link to style sheet (palette hexes, outline rule, shading rule).
TECH SPEC:
  Models:  <= N tris, 1 material, texture 1024² (512² accessories),
           maps: Color only | Color+Normal | full SurfaceAppearance,
           FBX (rigged, R15-compatible) / OBJ (static), origin at feet, studs scale.
  VFX:     <= 300 live particles, lifetime <= 1 s, textures <= 512²,
           works on ShadowMap, no reliance on Highlight, delivered as Attachment
           + ParticleEmitters/Beams + a test script / Moon or Blender anim sync notes.
  Anim:    R15, 60 fps timing, events/markers named for hit frames.
DELIVERABLES: Source (.blend/.spp/.psd), exported files, textures,
              a Studio place file with the asset set up, preview video.
MILESTONES: 30% on start → WIP check (blockout) → 70% on delivery.
REVISIONS: 2 rounds of minor revisions included; major changes quoted separately.
RIGHTS: Full ownership/exclusive transfer to <group> on final payment;
        artist may show in portfolio after <date/launch>.
PAYMENT: USD (PayPal/Wise) or Robux via group payout.
```

Write the spec using the numbers in [[Mobile-Aware Stylization]], [[Anime Character Modeling in Blender]] and [[Anime VFX Fundamentals]].

### Step 4: Milestones and revisions
1. **Blockout or concept check** (10–20% of the timeline): silhouette, scale and timing. Most changes should happen here.
2. **WIP in Studio** (50%): in-engine, with the game's lighting.
3. **Final** with deliverables.
- 2 minor revision rounds is a common included amount; a major redesign is billed extra (VFX carrd terms).
- Some artists require requests through an intake form (Google Form). Respect their process.

### Step 5: Payment mechanics
- **Group payouts** (one-time or recurring) are the efficient way to pay in Robux: no tax on the payout itself, though money *entering* a group from sales has already had the 30% fee taken.
- Game passes and shirts cost the payer **30% more** (the artist receives 70%). Many artists say the client must cover that tax.
- USD: PayPal or Wise invoices; agree who covers the fees.
- **Deposits**: 30% up front is a common ask (verify with each artist).
- Never pay 100% up front to an unknown artist; never demand 100% of the work before any payment.

### Step 6: Rights, IP and ownership
| Model | What you get | When to use |
|---|---|---|
| **Full transfer / work-for-hire on payment** | Ownership after 100% payment; artist waives rights (some templates) | Core game assets, characters, moves |
| **Exclusive licence** | Sole use, artist keeps authorship | When the artist insists on authorship |
| **Non-exclusive single-experience licence** | Use in one named experience only (e.g. `Checcerr`'s published T&C: perpetual, non-exclusive, single experience, after full payment; partial payment grants nothing) | Cheap generic assets only |

Key points:
- A written work-for-hire agreement matters. Without one, the freelancer may keep copyright (general legal explainers; Roblox DevForum "Developer Contracts on Roblox – Legal Lesson").
- Roblox's terms grant Roblox a licence to what you upload. A DevForum argument holds that if you don't own the rights, you can't grant that licence, which makes rights transfer before upload important.
- **Minors**: many Roblox artists are under 18. A DevForum legal lesson covers the enforceability of contracts with minors; involve guardians for big deals.
- **Revenue share**: if you offer a % of revenue, define the base (gross or net Robux? before or after ads and fees?), the duration, the audit rights, and what happens when the person leaves. The 2026 Anime Vanguards lawsuit (allegations include a revenue share pressured down from 20% to 10% and claims over copyrighted work used in the game) is a cautionary example.

> [!warning] Not legal advice
> This is a summary of public community practice. For anything above a few thousand dollars, or for revenue-share deals, use a real contract reviewed by a lawyer in your jurisdiction.

### Step 7: Anime IP specifically
- Fan games of licensed anime operate under "informal publisher tolerance" (RoWatcher). Removals and alleged DMCA actions happen: fan MHA games were reported removed around the official Gamefam/Crunchyroll launch, and an Anime Adventures remake was taken down by the original developers' DMCA.
- **Brief original designs**: "a cursed-energy sorcerer with a blindfold" is still too close if it copies a specific character's design, name and moves 1:1. Ask artists for original silhouettes and palettes that *evoke* an archetype.
- Don't ask artists to rip or trace official models. It's an IP issue and a reputational one for them.

### Step 8: Asset handover and access
- Artist delivers source files; **your group uploads**. If the artist must upload, have them upload to the group with granted permissions.
- **Asset Privacy**: when enabled for an account or group, newly created images, decals and meshes are **Restricted** by default; grant access through Creator Dashboard or bulk-grant in the Asset Manager. Only the group owner can toggle it, and it isn't retroactive.
- Since May 2025 creators can share images, decals, meshes, mesh parts and models with friends and groups.

## Numbers & Settings
| Setting | Value | Why |
|---|---|---|
| DevEx rate | $0.0038/R$ (legacy $0.0035) | Since 2025-09-05 |
| DevEx minimum | 30,000 R$ | Cash-out threshold |
| Marketplace fee (game pass) | 30% (artist gets 70%) | Pay with group payouts instead |
| Deposit | 30% (common ask) | Shares the risk |
| Included revisions | 2 minor rounds | Common term |
| VFX aura | 1K–3K R$ | Market sample |
| Single model | 5K–25K R$ | Market sample |
| US hourly (Roblox modeling) | ~$31–44 | ZipRecruiter Jun 2026 |

## Checklist
- [ ] Rate card requested and compared with the ranges above
- [ ] Portfolio shows in-Studio clips at game camera distance
- [ ] Brief sent with tech spec, refs, deliverables, milestones, revisions, rights
- [ ] Written agreement: ownership transfer on final payment, portfolio permission, confidentiality
- [ ] Payment route chosen (group payout or USD) and fees agreed
- [ ] Source files received; assets uploaded to the group; privacy and permissions set
- [ ] Original designs, no 1:1 copies of licensed characters

## Common Mistakes
- Paying through game passes and surprising the artist with a 30% cut.
- "Make it like Gojo's Hollow Purple" with no spec, so 5 revision rounds follow.
- No rights clause, then the artist later claims the asset or resells it.
- Accepting final assets only as uploaded IDs on the artist's account.
- Open-ended revenue-share promises with no definitions.
- Judging VFX from a black-background render instead of in-game.

## Related
- [[Top Roblox Modeler Workflow Patterns]]
- [[Public Roblox Artist Portfolios]]
- [[Case Study - Studio-Scale and Licensed Anime Games]]
- [[Reference Gathering and Screenshot Breakdown]]
- [[Anime Character Modeling in Blender]]
- [[Anime VFX Fundamentals]]
- [[Anime Combat Animation Timing]]
- [[Mobile-Aware Stylization]]

## Sources
1. littledragonopenings carrd (accessory 500/800 R$, decoration 1,000 R$): https://littledragonopenings.carrd.co
2. DevForum – Commission Price Guide For New Developers: https://devforum.roblox.com/t/commission-price-guide-for-new-developers/1356888
3. DevForum – [OPEN] 3d Modelling / Texturing Portfolio (1K–5K / 9K–70K R$ tiers): https://devforum.roblox.com/t/open-3d-modelling-texturing-portfolio/1417715
4. DevForum – [PERM CLOSED] crazymanchetosssss | 3D Modeler (5K–25K R$, 15K–75K R$): https://devforum.roblox.com/t/perm-closed-crazymanchetosssss-3d-modeler/904781
5. assetstring – VFX pricing (carrd): https://assetstring.carrd.co/
6. ZipRecruiter – Roblox Modeling pay (June 2026): https://www.ziprecruiter.com/Jobs/Roblox-Modeling
7. DevForum – [CLOSED] [$35K USD/yr] Professional Roblox Builder & 3D Modeler: https://devforum.roblox.com/t/closed-35k-usdyr-professional-roblox-builder-3d-modeler/4700225
8. DevForum – [Closed] Looking for 3D Modeller/Designer [20K Robux per month]: https://devforum.roblox.com/t/closed-looking-for-3d-modellerdesigner-20k-robux-per-month-or-gbp-equivalent/1135137
9. Business Wire – Roblox DevEx increase (2025-09-05): https://www.businesswire.com/news/home/20250905587466/en
10. AxeeTech – Roblox DevEx Rates 2026 (three rates incl. 18+ US): https://axeetech.com/roblox-devex-rates/
11. DevForum – How do I pay my devs (group payouts vs game pass): https://devforum.roblox.com/t/how-do-i-pay-my-devs/1303153
12. DevForum – Does group payouts have 30% tax: https://devforum.roblox.com/t/question-does-group-payouts-have-30-tax-to-the-user-paid-not-revenue/2857804
13. DevForum – Team Pages, Compensation Filtering… on Talent Hub: https://devforum.roblox.com/t/team-pages-compensation-filtering-and-moderation-improvements-on-talent-hub/2068704
14. DevForum – Checcerr's Freelance & Commission Terms: https://devforum.roblox.com/t/checcerrs-freelance-commission-terms-of-service-tos/4070249
15. DevForum – Freelance hourly contract template: https://devforum.roblox.com/t/freelance-hourly-contract-template/3309402
16. DevForum – Developer Contracts on Roblox – Legal Lesson: https://devforum.roblox.com/t/developer-contracts-on-roblox-legal-lesson/1580826
17. DevForum – How to Enforce Contracts with Minors – Legal Lesson: https://devforum.roblox.com/t/how-to-enforce-contracts-with-minors-legal-lesson/1992759
18. DevForum – Question about Intellectual Property (upload licence argument): https://devforum.roblox.com/t/question-about-intellectual-property/241063
19. Dexerto – Roblox dev sues Anime Vanguards owners: https://www.dexerto.com/roblox/roblox-dev-sues-anime-vanguards-owners-after-claiming-he-was-cut-out-of-millions-3368438/
20. All Things How – Anime Adventures return, Re:Adventures DMCA: https://allthings.how/anime-adventures-roblox-return-tensura-reveal-and-the-re-adventures-dmca/
21. Roblox Creator Hub – Asset privacy: https://create.roblox.com/docs/projects/assets/privacy
22. DevForum – Expanded Sharing for Assets: https://devforum.roblox.com/t/expanded-sharing-for-assets/3641687
23. DevForum – [RE-OPEN] 3D Modeler to join Featherfly Studios team: https://devforum.roblox.com/t/re-open-3d-modeler-to-join-featherfly-studios-team/240366
24. DevForum – [CLOSED] Aeksus // Low Poly & Semi Realistic Builder & Modeler: https://devforum.roblox.com/t/closed-aeksus-low-poly-semi-realistic-builder-modeler/316934
25. Dr Radium (carrd): https://dr-radium.carrd.co/
