#!/usr/bin/env python3
"""
Sync SDV Unity integration assets into one or more Unity projects.

What it copies:
- Unity bridge scripts -> Assets/Scripts/SdvBridge
- Generated skin pack -> Assets/Resources/Skins/unity_skin_pack_v1
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List


REQUIRED_SCRIPT_NAMES = [
    "UdpUiRenderReceiver.cs",
    "UiRenderVisualMap.cs",
    "ExternalRoadViewController.cs",
    "CabinPanoramaViewController.cs",
    "SdvSceneAutoBinder.cs",
    "UiRenderStatusOverlay.cs",
    "QuickPrototypeSceneBuilder.cs",
    "SdvSkinRuntimeLoader.cs",
]


def is_unity_project_root(path: Path) -> bool:
    return (path / "Assets").is_dir() and (path / "ProjectSettings" / "ProjectVersion.txt").is_file()


def discover_unity_projects(repo_root: Path) -> List[Path]:
    results: List[Path] = []
    for project_settings in repo_root.rglob("ProjectSettings"):
        root = project_settings.parent
        if is_unity_project_root(root):
            results.append(root)
    # unique + stable order
    return sorted({p.resolve() for p in results}, key=lambda p: str(p))


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_scripts(sample_dir: Path, target_project: Path) -> int:
    dst_dir = target_project / "Assets" / "Scripts" / "SdvBridge"
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for name in REQUIRED_SCRIPT_NAMES:
        src = sample_dir / name
        if not src.exists():
            raise FileNotFoundError(f"Missing required script: {src}")
        shutil.copy2(src, dst_dir / name)
        copied += 1
    return copied


def copy_skin_pack(skin_pack_dir: Path, target_project: Path, clean: bool) -> int:
    dst_dir = target_project / "Assets" / "Resources" / "Skins" / "unity_skin_pack_v1"
    if clean:
        ensure_clean_dir(dst_dir)
    else:
        dst_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for src in skin_pack_dir.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(skin_pack_dir)
        dst = dst_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    return copied


def write_sync_note(target_project: Path) -> None:
    note = target_project / "Assets" / "Scripts" / "SdvBridge" / "README_SYNCED_FROM_CANOE.md"
    note.write_text(
        "\n".join(
            [
                "# Synced SDV Bridge Files",
                "",
                "This folder was synced from CANoe-IVI-OTA repository.",
                "Source scripts: canoe/reference/unity_bridge_samples/",
                "Source skin pack: canoe/reference/oss_panels/_exports/unity_skin_pack_v1/",
                "",
                "Do not place arbitration logic here. Renderer-only mapping is allowed.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync SDV Unity integration assets")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Repository root path",
    )
    parser.add_argument(
        "--target-project",
        action="append",
        default=[],
        help="Unity project root path (can be used multiple times)",
    )
    parser.add_argument(
        "--auto-detect",
        action="store_true",
        help="Auto detect Unity projects under repo root",
    )
    parser.add_argument(
        "--clean-skin-dir",
        action="store_true",
        help="Clean skin destination directory before copy",
    )
    return parser.parse_args()


def normalize_targets(repo_root: Path, args: argparse.Namespace) -> List[Path]:
    targets: List[Path] = []
    if args.auto_detect:
        targets.extend(discover_unity_projects(repo_root))
    for raw in args.target_project:
        p = Path(raw).resolve()
        if p not in targets:
            targets.append(p)
    return targets


def run() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    sample_dir = repo_root / "canoe" / "reference" / "unity_bridge_samples"
    skin_pack_dir = repo_root / "canoe" / "reference" / "oss_panels" / "_exports" / "unity_skin_pack_v1"

    if not sample_dir.exists():
        raise FileNotFoundError(f"Sample script directory not found: {sample_dir}")
    if not skin_pack_dir.exists():
        raise FileNotFoundError(
            f"Skin pack not found: {skin_pack_dir} (run build_unity_skin_pack.py first)"
        )

    targets = normalize_targets(repo_root, args)
    if not targets:
        raise RuntimeError("No target Unity project. Use --auto-detect or --target-project.")

    ok_count = 0
    for project in targets:
        if not is_unity_project_root(project):
            print(f"[SYNC] skip (not unity root): {project}")
            continue

        script_count = copy_scripts(sample_dir, project)
        skin_count = copy_skin_pack(skin_pack_dir, project, clean=args.clean_skin_dir)
        write_sync_note(project)
        ok_count += 1

        print(
            f"[SYNC] done project={project} scripts={script_count} "
            f"skin_files={skin_count} clean={args.clean_skin_dir}"
        )

    if ok_count == 0:
        raise RuntimeError("No Unity project synced.")

    print(f"[SYNC] completed synced_projects={ok_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
