---
tags: [meta, conventions]
updated: 2026-10-31
---
# Vault Conventions

This repo is an **Obsidian vault**: Claude's working notes on how to build anime (shonen battlegrounds) style games on Roblox. Clone it and open the folder in Obsidian.

## Rules for every note
- **Frontmatter**: `tags`, `updated` (YYYY-MM-DD), `sources` (count), `status` (`draft` | `solid` | `verified-in-studio`).
- **Title = H1**, one topic per note, filename matches the title.
- Link related notes with `[[Note Name]]` (no folder path, no `.md`).
- Every factual or numeric claim (limits, property values, budgets) gets a source in the note's `## Sources` section with a URL. Mark unconfirmed things `> [!warning] Unverified`.
- Write a `## TL;DR` with 3–6 bullets near the top, then the deep content, then `## Checklist` (actionable), `## Common Mistakes`, `## Sources`.
- Use concrete numbers: tri counts, texture resolutions, property values, frame timings.
- Use Obsidian callouts: `> [!tip]`, `> [!warning]`, `> [!example]`.

## Folders
| Folder | Holds |
|---|---|
| 00 - Index | MOCs (maps of content), conventions, roadmap |
| 01 - Style Foundations | What "shonen anime on Roblox" looks like, shape language, color |
| 02 - Characters & Rigs | Blender modeling, topology, faces, hair, rigs, import |
| 03 - Environments & Props | Modular kits, stylized nature, lighting, toon tricks, perf |
| 04 - VFX | Particles, beams, trails, slashes, impact frames, textures |
| 05 - Animation & Combat Feel | Timing, smears, hitstop, camera, Moon Animator/Blender |
| 06 - Top Modelers & Studios | Case studies of games, artists, and their workflows |
| 90 - References | Link library, reference-game breakdowns, tools list |
| 99 - Templates | Note templates |
