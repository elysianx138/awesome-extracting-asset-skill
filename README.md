# Awesome Extracting Asset Skill

[中文说明](./README.zh.md)

**Stop letting AI coding agents blindly scan your old repos and blow up the context window.**

`extracting-asset-skill` is an open-source **Meta-Skill** for AI coding agents (Claude Code, Antigravity, Cursor, Codex, etc.) that extracts reusable technical and creative assets from any finished project—procedural 3D/2D models, shaders, UI primitives, audio engines, or effect libraries—into a clean, searchable, style-decoupled **Agent Skill**.

---

## Why This Exists

When you build multiple games or creative projects with AI, reusing code from previous projects usually fails in three ways:

1. **Context Window Explosion**: Pointing an AI agent to an old repo makes it scan dozens of files before writing a single line of new code.
2. **Style & Business-Glue Lock-In**: Colors, proportions, i18n, and old game state are tangled inside components—reusing them either breaks builds or makes your new project look identical to the old one.
3. **Thumbnail Bloat**: Humans forget what 40 procedural models or UI components look like, yet stuffing dozens of `.png` screenshots inside a Skill bloats the package and wastes tokens.

## Core Design (4 Pillars)

1. **Silent Scan & Alignment Gate (`Step 0`)**
   - Scans the source project first, separates **High-Value Reusable Assets** from **Project-Specific Glue**, and asks 4 short questions before writing a single file: *Scope, Mode (new domain Skill vs. incremental merge), Maintenance Path (Central Asset Vault), and Deliverables*.
2. **Universal Base + Pluggable Style Pack**
   - Strips project-specific imports into options/callbacks (`templates/`, tagged `"style": "universal"`).
   - Moves palettes, proportions, lighting, and CSS tokens into swappable `styles/<style-id>/` packs so one domain Skill can serve many distinct games.
3. **Line-Exact CLI Search (`assets-catalog.json` + `search_assets.py`)**
   - Instead of scanning whole folders, AI runs `search_assets.py` to get exact `file#Lline` pointers and reads only the matched block.
   - Supports `--sync-lines` verification across JS/TS exports, CSS selectors, and Python definitions with 0 warnings.
4. **Zero-PNG Live Interactive Showroom (`showroom/gallery.html`)**
   - Zero `.png` thumbnails inside the Skill. Humans open a live local HTML showroom importing the real `templates/` and `styles/` (with live theme switching or 3D orbit controls), while AI queries JSON only.

---

## Installation

### Option 1: Ask your AI Agent directly
Send this prompt to any Agent that supports `SKILL.md`:

```text
Install the skill from this repository: https://github.com/elysianx138/awesome-extracting-asset-skill
```

### Option 2: Manual install
Copy `skills/extracting-asset-skill/` into your agent's skills directory:
- **Workspace (Antigravity / Codex / Universal)**: `.agents/skills/extracting-asset-skill/`
- **Claude Code (Global)**: `~/.claude/skills/extracting-asset-skill/`

### Option 3: Sync to a Central Asset Vault
```bash
python skills/extracting-asset-skill/scripts/pack_and_sync_skill.py \
  skills/extracting-asset-skill \
  --target "~/game-asset-vault"
```

---

## Quick Usage

Once installed, simply prompt your coding agent:

```text
Use extracting-asset-skill to extract reusable UI primitives and theme tokens from ./my-previous-game
```

Or merge a second game's visual style into an existing domain Skill:

```text
Use extracting-asset-skill to extract the frosted-glass theme and drawer toolbar from ./game-2 and merge them into my existing building-web-game-ui skill
```

---

## Repository Structure

```text
skills/extracting-asset-skill/
├── SKILL.md                           # Main workflow & Step 0 alignment gate
├── references/
│   ├── style-pack-pattern.md          # Universal Base + Style Pack & Zero-PNG Showroom architecture
│   └── skill-spec-checklist.md        # Token economy & SKILL.md spec checklist
├── scripts/
│   └── pack_and_sync_skill.py         # Multi-target sync (--target) & POSIX ZIP packager
└── templates/
    ├── search_assets.py               # Domain-agnostic catalog search & --sync-lines CLI
    └── style.json                     # Starter Style Pack metadata template
```

## License

MIT License — see [LICENSE](./LICENSE).
