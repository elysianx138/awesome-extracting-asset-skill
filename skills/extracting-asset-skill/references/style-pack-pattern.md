# Universal Base + Style Pack & Zero-PNG Showroom Pattern

## 1. Why Split Base vs. Style Pack?
Hardcoding one project's colors, proportions, or lighting into engine files locks the entire asset library to a single look.
- **Universal Base (`templates/`)**: Pure geometry builders, math/noise utilities, shader skeletons, layout primitives (`"style": "universal"`).
- **Style Pack (`styles/<id>/`)**: Palette tokens, scale/proportion constants, surface grain parameters, lighting & post-processing LUTs (`style.json` + token files).
- **Incremental Reuse**: When a new project uses the same engine with a new art direction, add ONLY a new `styles/<new-id>/` folder rather than duplicating the whole Skill.

## 2. Zero-PNG Live Showroom (`showroom/gallery.html`)
- **For Humans**: Live interactive 3D/2D/UI preview directly importing the real `templates/` code. Editing any `.ts`/`.css` file updates the showroom on refresh with zero stale screenshots.
- **For AI**: AI agents never read `gallery.html` to search assets; they query `scripts/search_assets.py` against `assets-catalog.json`.
- **Auto-Launch**: Document a 3-step launch rule in the generated `SKILL.md` (ensure `gallery.html` exists in workspace → start dev server in background → open `http://localhost:5173/gallery.html`).
