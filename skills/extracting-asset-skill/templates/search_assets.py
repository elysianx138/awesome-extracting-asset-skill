#!/usr/bin/env python3
"""
Fast Asset Catalog Search & Maintenance CLI template.
Supports JS/TS exports and CSS selectors/tokens during `--sync-lines`.

Usage:
  python scripts/search_assets.py --list-cats
  python scripts/search_assets.py --list-styles
  python scripts/search_assets.py --q <keyword>
  python scripts/search_assets.py --cat <category>
  python scripts/search_assets.py --sync-lines
"""
import argparse
import json
import os
import re

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(SKILL_ROOT, "assets-catalog.json")


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_symbol_pattern(fpath, symbol):
    ext = os.path.splitext(fpath)[1].lower()
    if ext == ".css":
        return re.compile(rf"(?:^|[\s,])({re.escape(symbol)})(?:\b|[\s:{{,\[])")
    if ext == ".py":
        return re.compile(rf"^\s*(?:def|class)\s+{re.escape(symbol)}\b")
    return re.compile(
        rf"^\s*export\s+(?:default\s+)?(?:async\s+)?(?:function|const|let|class|interface|type)\s+{re.escape(symbol)}\b"
    )


def sync_lines(data):
    updated = 0
    missing = []
    for item in data["assets"]:
        fpath = os.path.join(SKILL_ROOT, item["file"].replace("/", os.sep))
        if not os.path.isfile(fpath):
            missing.append(f"{item['id']} -> missing file {item['file']}")
            continue
        fn = item["fn"]
        pattern = build_symbol_pattern(fpath, fn)
        found_line = None
        with open(fpath, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                if pattern.search(line):
                    found_line = idx
                    break
        if found_line is None:
            missing.append(f"{item['id']} -> symbol '{fn}' not found in {item['file']}")
        elif item.get("line") != found_line:
            item["line"] = found_line
            updated += 1
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Synced {len(data['assets'])} assets ({updated} line numbers updated, {len(missing)} warnings).")
    for m in missing:
        print("  WARN:", m)


def main():
    ap = argparse.ArgumentParser(description="Search Skill asset catalog")
    ap.add_argument("--q", default="", help="Keyword (Chinese/English name, tag, symbol, or file)")
    ap.add_argument("--cat", default="", help="Filter by category")
    ap.add_argument("--style", default="", help="Filter by style pack (e.g. universal, <style-id>)")
    ap.add_argument("--list-cats", action="store_true", help="List categories and asset counts")
    ap.add_argument("--list-styles", action="store_true", help="List available Style Packs in styles/")
    ap.add_argument("--sync-lines", action="store_true", help="Verify and refresh line numbers against files")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    data = load_catalog()
    assets = data["assets"]

    if args.sync_lines:
        sync_lines(data)
        return

    if args.list_styles:
        styles_dir = os.path.join(SKILL_ROOT, "styles")
        found = []
        if os.path.isdir(styles_dir):
            for name in sorted(os.listdir(styles_dir)):
                sp = os.path.join(styles_dir, name, "style.json")
                if name.startswith("_") or not os.path.isfile(sp):
                    continue
                with open(sp, "r", encoding="utf-8") as sf:
                    found.append(json.load(sf))
        if args.json:
            print(json.dumps(found, ensure_ascii=False, indent=2))
        else:
            print(f"Installed Style Packs ({len(found)}):")
            for s in found:
                print(f"  - {s['id']}: {s['name']} ({s['en']})")
        return

    if args.list_cats:
        counts = {}
        for a in assets:
            counts[a["cat"]] = counts.get(a["cat"], 0) + 1
        if args.json:
            print(json.dumps(counts, ensure_ascii=False, indent=2))
        else:
            print(f"Total catalog entries: {len(assets)}")
            for k, v in sorted(counts.items()):
                print(f"  {k:<12} : {v}")
        return

    q = args.q.strip().lower()
    cat = args.cat.strip().lower()
    style = args.style.strip().lower()
    hits = []
    for a in assets:
        if cat and a["cat"].lower() != cat:
            continue
        if style and a.get("style", "universal").lower() not in (style, "universal"):
            continue
        if q:
            hay = " ".join(
                [
                    a["id"],
                    a["name"],
                    a["en"],
                    a["cat"],
                    a.get("style", ""),
                    a["fn"],
                    a["file"],
                    a["summary"],
                    " ".join(a.get("tags", [])),
                ]
            ).lower()
            if q not in hay:
                continue
        hits.append(a)

    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return

    if not hits:
        print(f"No assets matched (q='{args.q}', cat='{args.cat}'). Try --list-cats.")
        return

    print(f"Matched {len(hits)} asset(s):")
    for a in hits:
        print(f"- [{a['cat']} | {a.get('style', 'universal')}] {a['name']} ({a['en']}) -> {a['file']}#L{a['line']} `{a['fn']}`")
        print(f"    {a['summary']}")


if __name__ == "__main__":
    main()
