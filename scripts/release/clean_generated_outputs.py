#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "product" / "sdv_operator" / "config" / "cleanup_policy.json"


def load_policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def clean_children(root: Path, preserve_names: set[str], dry_run: bool) -> list[str]:
    removed: list[str] = []
    if not root.exists():
        return removed
    for child in root.iterdir():
        if child.name in preserve_names:
            continue
        removed.append(rel(child))
        if not dry_run:
            remove_path(child)
    return removed


def clean_root(path: Path, dry_run: bool) -> list[str]:
    removed: list[str] = []
    if not path.exists():
        return removed
    removed.append(rel(path))
    if not dry_run:
        remove_path(path)
    return removed


def build_targets(policy: dict, scope: str, run_id: str, phase: str, all_runs: bool) -> list[tuple[str, Path, str]]:
    targets: list[tuple[str, Path, str]] = []
    if scope in {"staging", "all"}:
        for item in policy["staging_roots"]:
            targets.append(("children", ROOT / item, item))
    if scope in {"build", "all"}:
        for item in policy["build_roots"]:
            targets.append(("root", ROOT / item, item))
    if scope in {"archive", "all"}:
        archive_root = ROOT / policy["archive_root"]
        if run_id:
            target = archive_root / run_id
            if phase:
                target = target / phase
            targets.append(("root", target, rel(target)))
        elif all_runs:
            targets.append(("root", archive_root, rel(archive_root)))
        elif scope == "archive":
            raise SystemExit("[CLEANUP] archive cleanup requires --run-id or --all-runs")
    return targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean generated operator outputs without touching source assets")
    parser.add_argument("--scope", choices=["staging", "archive", "build", "all"], default="staging")
    parser.add_argument("--run-id", default="", help="Archive run ID to delete (required for archive scope unless --all-runs)")
    parser.add_argument("--phase", choices=["pre", "post", "full"], default="", help="Optional archive phase under a run ID")
    parser.add_argument("--all-runs", action="store_true", help="Allow deleting the entire archive root")
    parser.add_argument("--yes", action="store_true", help="Apply deletion. Omit for dry-run preview.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    policy = load_policy()
    preserve_names = set(policy.get("preserve_names", []))
    dry_run = not args.yes

    targets = build_targets(policy, args.scope, args.run_id, args.phase, args.all_runs)
    removed: list[str] = []

    for mode, path, _label in targets:
        if mode == "children":
            removed.extend(clean_children(path, preserve_names, dry_run))
        else:
            removed.extend(clean_root(path, dry_run))

    action = "preview" if dry_run else "removed"
    print(f"[CLEANUP] mode={action} scope={args.scope}")
    if not removed:
        print("[CLEANUP] no targets matched")
        return 0
    for item in removed:
        print(f"- {item}")
    if dry_run:
        print("[CLEANUP] re-run with --yes to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
