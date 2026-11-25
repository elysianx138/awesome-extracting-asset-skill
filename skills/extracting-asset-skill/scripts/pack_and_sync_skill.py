#!/usr/bin/env python3
"""
Pack any standard Agent Skill directory into a portable POSIX-slash ZIP
and/or sync it to custom maintenance paths (e.g. Obsidian Asset Vault,
workspace `.agents/skills/`) and global Skills directories.

Usage:
  python scripts/pack_and_sync_skill.py <skill_dir> --target "~/game-asset-vault"
  python scripts/pack_and_sync_skill.py <skill_dir> --target ".agents/skills" --zip <out.zip>
  python scripts/pack_and_sync_skill.py <skill_dir> --install-global
"""
import argparse
import os
import shutil
import zipfile


def sync_to_root(skill_dir, skill_name, root_dir):
    os.makedirs(root_dir, exist_ok=True)
    dest = os.path.join(os.path.abspath(root_dir), skill_name)
    if os.path.abspath(dest) == os.path.abspath(skill_dir):
        return None
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(skill_dir, dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description="Pack and sync an Agent Skill")
    ap.add_argument("skill_dir", help="Path to the skill folder containing SKILL.md")
    ap.add_argument("--target", action="append", default=[], help="Target parent directory to sync into (repeatable)")
    ap.add_argument("--zip", dest="zip_path", default="", help="Output .zip file path")
    ap.add_argument("--install-global", action="store_true", help="Copy into global Antigravity & Claude Code skills dirs")
    args = ap.parse_args()

    skill_dir = os.path.abspath(args.skill_dir)
    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        raise SystemExit(f"Error: SKILL.md not found in {skill_dir}")

    skill_name = os.path.basename(skill_dir)

    if args.zip_path:
        zpath = os.path.abspath(args.zip_path)
        os.makedirs(os.path.dirname(zpath), exist_ok=True)
        count = 0
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for r, _, fns in os.walk(skill_dir):
                for fn in sorted(fns):
                    full = os.path.join(r, fn)
                    rel = os.path.relpath(full, skill_dir)
                    arc = os.path.join(skill_name, rel).replace(os.sep, "/")
                    z.write(full, arc)
                    count += 1
        print(f"Packed ZIP: {zpath} ({count} files, {os.path.getsize(zpath)} bytes)")

    synced = []
    for t in args.target:
        dest = sync_to_root(skill_dir, skill_name, t)
        if dest:
            synced.append(dest)
    if synced:
        print("Synced to target(s):", synced)

    if args.install_global:
        home = os.path.expanduser("~")
        targets = [
            os.path.join(home, ".gemini", "config", "skills"),
            os.path.join(home, ".gemini", "antigravity", "skills"),
            os.path.join(home, ".claude", "skills"),
        ]
        installed = []
        for root in targets:
            if os.path.isdir(os.path.dirname(root)):
                dest = sync_to_root(skill_dir, skill_name, root)
                if dest:
                    installed.append(dest)
        print("Installed globally to:", installed)


if __name__ == "__main__":
    main()
