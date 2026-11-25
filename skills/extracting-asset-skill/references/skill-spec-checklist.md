# Anthropic Agent Skills Spec Checklist

Verify every generated Skill against these rules before packaging:

## 1. YAML Frontmatter
- `name`: lowercase ASCII letters, digits, and hyphens only; prefer gerund form (e.g., `modeling-drift-diary-3d`, `styling-cozy-glass-ui`).
- `description`: written in third person; states **what** the skill does AND **when** an AI should trigger it.

## 2. Progressive Disclosure & Token Economy
- Keep `SKILL.md` concise (**< 150 lines**). Assume the AI already knows standard programming; document ONLY project-specific rules, palettes, proportions, and workflows.
- Keep each `references/*.md` file focused and **< 160 lines**, linked via relative markdown paths from `SKILL.md`.
- Never embed raw source dumps or base64/PNG thumbnails inside `SKILL.md` or `references/`.

## 3. Deterministic Tooling (`scripts/`)
- Always offload asset discovery and line-number validation to `scripts/search_assets.py` so the AI reads only the exact matched line ranges instead of scanning entire directories.
- Run `--sync-lines` before shipping to guarantee **0 broken file paths or missing exports**.
