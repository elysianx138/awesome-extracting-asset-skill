---
name: extracting-asset-skill
description: Extracts reusable technical and creative assets (3D/2D procedural models, shaders, UI design systems, audio engines, or effect libraries) from any project into a standard, AI-searchable Agent Skill with a decoupled Universal Base + Style Pack architecture, catalog search script, and zero-PNG live showroom. Use this skill when the user asks to package, abstract, or merge a project's assets, art style, or reusable modules into a portable Skill or central asset vault.
---

# Extracting Asset Skill

Follow this standardized workflow to transform any project's reusable assets into a clean, portable, domain-grouped Agent Skill.

## Step 0: Silent Scan & Alignment Gate (MANDATORY — Ask Before Writing!)

**NEVER dump an entire repository blindly into a Skill.** Before creating or modifying any files:

1. **Quickly scan the workspace** to classify candidate modules into:
   - **High-Value Reusable Assets** (e.g., procedural 3D/2D geometry, shaders, post-processing, UI primitives, CSS themes, audio synths, particle FX).
   - **Project-Specific Glue (Recommend Skipping)** (e.g., save/load state, story text, analytics, platform SDK wrappers, one-off business logic).
2. **Present a concise inventory & ask the user 4 short questions** (with recommended defaults):
   - **Scope**: Which asset groups should be extracted? (List candidates clearly + recommend skipping tightly coupled glue.)
   - **Mode**: Create a **new domain Skill**, OR **merge/append** new primitives & a **Style Pack (`styles/<id>/`)** into an existing domain Skill? *(Prefer grouping by domain — e.g., one UI Skill for all games — instead of one Skill per game.)*
   - **Maintenance Path (Asset Vault)**: Where should core assets be stored and maintained long-term? (e.g., a central asset vault such as `~/game-asset-vault`, the current workspace `.agents/skills/`, or synced to both.)
   - **Deliverables**: Include a **zero-PNG live interactive Showroom (`showroom/gallery.html`)**? Only pack a `.zip` or install globally if the user explicitly requests it.
3. **Wait for explicit user confirmation** before writing any files.

## Step 1: Decouple Universal Base vs. Style Pack (or Incremental Merge)

Read [Style Pack Pattern](references/style-pack-pattern.md). Always separate:
- **Universal Base (`templates/`)**: Style-agnostic engines, geometry builders, shader skeletons, UI interaction primitives. Tag `"style": "universal"` in `assets-catalog.json`.
  - **Strip Business Glue**: Replace internal project imports (`i18n`, `game`, `battle`, `audio`) with clean options, callbacks, or CSS custom properties so every module runs standalone.
- **Style Pack (`styles/<style-id>/`)**: Project-specific palette, proportions, typography, surface grain, or post presets (`style.json` + theme/palette file). Keep `styles/_template/` ready for future games.
- **When Merging into an Existing Skill**:
  1. Run `python scripts/search_assets.py --list-cats` and `--list-styles` first to avoid duplicating existing primitives.
  2. Add only net-new primitives to `templates/` and add the new game's look as `styles/<new-id>/`.

## Step 2: Author Progressive-Disclosure Docs

Read [Skill Spec Checklist](references/skill-spec-checklist.md) and write/update:
- `SKILL.md` (**under 150 lines**): Valid YAML frontmatter (`name` lowercase-hyphen gerund, third-person `description` with trigger conditions), core rules, Step 0 search rule, and relative links to `references/`.
- `references/*.md` (2–4 focused files, **each under 160 lines**): Split by domain so future AI sessions load only what they need.

## Step 3: Build Structured Catalog, Search CLI & Standalone Verification

1. Copy `templates/search_assets.py` into `<target-skill>/scripts/search_assets.py` (supports JS/TS exports and CSS selectors/tokens).
2. Register or append exported symbols in `<target-skill>/assets-catalog.json` with `id`, `name`, `en`, `cat`, `style`, `tags`, `file`, `fn`, `line`, `summary`.
3. **Verify standalone integrity**:
   - Run syntax/type checks on extracted code (`node --check` / `tsc --noEmit`).
   - Run `python <target-skill>/scripts/search_assets.py --sync-lines` and confirm **0 warnings**.

## Step 4: Optional Zero-PNG Live Interactive Showroom

- **NEVER store `.png` thumbnails inside a Skill directory** (they bloat packages and waste context).
- Build or update `showroom/gallery.html` directly importing real `templates/` and `styles/` so humans can inspect 3D/2D/UI assets and switch Style Packs live in the browser.
- Document an **Auto-Launch Trigger** in the generated `SKILL.md`, while AI asset lookup always uses `scripts/search_assets.py`.

## Step 5: Sync to Maintenance Path (and Optional Pack)

Sync to the user's confirmed vault / workspace path(s) (and pack `.zip` or `--install-global` **only if requested**):
```bash
python scripts/pack_and_sync_skill.py <skill_dir> --target "<vault_dir>" [--target "<workspace>/.agents/skills"] [--zip <output.zip>] [--install-global]
```
Report the verified file count, synced maintenance path(s), and example search commands.
