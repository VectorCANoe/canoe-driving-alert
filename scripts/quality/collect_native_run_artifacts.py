#!/usr/bin/env python3
"""Collect native CANoe run artifacts for one verification tier."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CFG_PATH = REPO_ROOT / "canoe" / "cfg" / "CAN_v2_topology.cfg"
CONTEXT_FILE_NAME = "native_execute_context.json"
SUPPLEMENTARY_EXTENSIONS = {
    "trace": {".asc", ".pcap", ".pcapng"},
    "logging": {".blf", ".mf4", ".mdf", ".log", ".txt", ".csv"},
}
ASSIGN_DIR_BY_TIER = {
    "UT": "UT_ACTIVE_BASELINE",
    "IT": "IT_ACTIVE_BASELINE",
    "ST": "ST_ACTIVE_BASELINE",
    "FULL": "FULL_ACTIVE_BASELINE",
}


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _copy_if_exists(src: Path, dst: Path) -> str | None:
    src = _repo_path(src)
    dst = _repo_path(dst)
    if not src.exists() or not src.is_file():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return _rel(dst)


def _copy_matching(src_root: Path, pattern: str, dst_root: Path) -> list[str]:
    src_root = _repo_path(src_root)
    dst_root = _repo_path(dst_root)
    copied: list[str] = []
    if not src_root.exists():
        return copied
    for src in sorted(src_root.glob(pattern)):
        if not src.is_file():
            continue
        dst = dst_root / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(_rel(dst))
    return copied


def _copy_tree(src_root: Path, dst_root: Path) -> list[str]:
    src_root = _repo_path(src_root)
    dst_root = _repo_path(dst_root)
    copied: list[str] = []
    if not src_root.exists():
        return copied
    for src in sorted(src_root.rglob("*")):
        if not src.is_file():
            continue
        dst = dst_root / src.relative_to(src_root)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(_rel(dst))
    return copied


def _dir_has_files(path: Path) -> bool:
    path = _repo_path(path)
    if not path.exists() or not path.is_dir():
        return False
    return any(item.is_file() for item in path.rglob("*"))


def _parse_iso_timestamp(raw: str) -> dt.datetime | None:
    value = raw.strip()
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError:
        return None


def native_execute_context_path(tier: str) -> Path:
    return REPO_ROOT / "canoe" / "logging" / "evidence" / "incoming" / tier / CONTEXT_FILE_NAME


def load_native_execute_context(tier: str) -> dict[str, object]:
    path = native_execute_context_path(tier)
    if not path.exists() or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    payload["_path"] = _rel(path)
    return payload


def _resolve_cfg_output_dir(raw_path: str) -> Path:
    cfg_dir = CFG_PATH.parent
    path = Path(raw_path)
    if path.is_absolute():
        return path.parent
    return (cfg_dir / path).resolve().parent


def _discover_cfg_logging_output_dirs() -> list[Path]:
    if not CFG_PATH.exists():
        return []
    try:
        text = CFG_PATH.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    pattern = re.compile(r'<VFileName[^>]*>\s+\d+\s+"([^"]+)"')
    discovered: list[Path] = []
    seen: set[str] = set()
    for raw_path in pattern.findall(text):
        lower = raw_path.lower()
        if not any(ext in lower for ext in (".blf", ".mf4", ".mdf", ".asc", ".log", ".pcap")):
            continue
        directory = _resolve_cfg_output_dir(raw_path)
        key = str(directory).lower()
        if key in seen:
            continue
        seen.add(key)
        discovered.append(directory)
    return discovered


def _default_auto_discovery_roots() -> list[Path]:
    roots = _discover_cfg_logging_output_dirs()
    deduped: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root).lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(root)
    return deduped


def _recent_time_window(
    tier: str,
    *,
    lookback_minutes: int,
    summary_report: Path,
    raw_log_source: Path | None,
) -> tuple[dt.datetime | None, dt.datetime | None, dict[str, object]]:
    context = load_native_execute_context(tier)
    started_at = _parse_iso_timestamp(str(context.get("started_at", "")))
    completed_at = _parse_iso_timestamp(str(context.get("completed_at", "")))
    if started_at is not None:
        earliest = started_at - dt.timedelta(seconds=5)
        latest = (completed_at + dt.timedelta(minutes=10)) if completed_at is not None else None
        return earliest, latest, context

    anchors: list[dt.datetime] = []
    if summary_report.exists() and summary_report.is_file():
        anchors.append(dt.datetime.fromtimestamp(summary_report.stat().st_mtime))
    if raw_log_source is not None and raw_log_source.exists() and raw_log_source.is_file():
        anchors.append(dt.datetime.fromtimestamp(raw_log_source.stat().st_mtime))
    if not anchors:
        return None, None, context
    anchor = max(anchors)
    return anchor - dt.timedelta(minutes=lookback_minutes), anchor + dt.timedelta(minutes=10), context


def _copy_recent_supplementary(
    *,
    kind: str,
    src_roots: list[Path],
    dst_root: Path,
    earliest: dt.datetime | None,
    latest: dt.datetime | None,
    exclude_roots: list[Path],
) -> tuple[list[str], list[str]]:
    copied: list[str] = []
    used_roots: list[str] = []
    seen_files: set[str] = set()
    lowered_exclude = [str(_repo_path(root).resolve()).lower() for root in exclude_roots]
    extensions = SUPPLEMENTARY_EXTENSIONS[kind]
    for src_root in src_roots:
        root = _repo_path(src_root)
        try:
            resolved_root = root.resolve()
        except OSError:
            continue
        root_key = str(resolved_root).lower()
        if any(root_key.startswith(prefix) for prefix in lowered_exclude):
            continue
        if not root.exists() or not root.is_dir():
            continue
        root_used = False
        for src in sorted(root.glob("*")):
            if not src.is_file() or src.suffix.lower() not in extensions:
                continue
            try:
                resolved_src = src.resolve()
            except OSError:
                continue
            src_key = str(resolved_src).lower()
            if any(src_key.startswith(prefix) for prefix in lowered_exclude):
                continue
            modified = dt.datetime.fromtimestamp(src.stat().st_mtime)
            if earliest is not None and modified < earliest:
                continue
            if latest is not None and modified > latest:
                continue
            if src_key in seen_files:
                continue
            dst = dst_root / src.name
            if dst.exists():
                prefix = root.name or "supplementary"
                dst = dst_root / f"{prefix}__{src.name}"
            counter = 2
            while dst.exists():
                dst = dst_root / f"{dst.stem}_{counter}{dst.suffix}"
                counter += 1
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(_rel(dst))
            seen_files.add(src_key)
            root_used = True
        if root_used:
            used_roots.append(_rel(root))
    return copied, used_roots


def default_raw_log_candidates(tier: str) -> list[Path]:
    canonical_base = REPO_ROOT / "canoe" / "logging" / "evidence" / "incoming"
    legacy_base = REPO_ROOT / "canoe" / "tmp" / "write_window"
    return [
        canonical_base / tier / "raw_write_window.txt",
        canonical_base / f"{tier}_ACTIVE_BASELINE_raw_write_window.txt",
        canonical_base / f"{tier}_raw_write_window.txt",
        canonical_base / "raw_write_window.txt",
        legacy_base / tier / "raw_write_window.txt",
        legacy_base / f"{tier}_ACTIVE_BASELINE_raw_write_window.txt",
        legacy_base / f"{tier}_raw_write_window.txt",
        legacy_base / "raw_write_window.txt",
    ]


def default_trace_source_dirs(tier: str) -> list[Path]:
    canonical_base = REPO_ROOT / "canoe" / "logging" / "evidence" / "incoming"
    return [
        canonical_base / tier / "trace",
    ]


def default_logging_source_dirs(tier: str) -> list[Path]:
    canonical_base = REPO_ROOT / "canoe" / "logging" / "evidence" / "incoming"
    return [
        canonical_base / tier / "logging",
    ]


def resolve_source_dir(explicit: str, candidates: list[Path]) -> Path | None:
    if explicit:
        path = _repo_path(Path(explicit))
        return path if path.exists() and path.is_dir() else None
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir() and _dir_has_files(candidate):
            return candidate
    return None


def resolve_raw_log_source(tier: str, explicit: str) -> Path | None:
    if explicit:
        path = _repo_path(Path(explicit))
        return path if path.exists() and path.is_file() else None
    for candidate in default_raw_log_candidates(tier):
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect native CANoe reports and raw log for one run")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--tier", required=True, choices=["UT", "IT", "ST", "FULL"])
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument("--cfg-root", type=Path, default=Path("canoe/cfg"))
    parser.add_argument("--assign-root", type=Path, default=Path("canoe/tests/modules/test_units/assign"))
    parser.add_argument(
        "--raw-log-source",
        default="",
        help="Optional raw Write Window source file. If omitted, standard drop paths are probed.",
    )
    parser.add_argument(
        "--allow-missing-raw-log",
        action="store_true",
        help="Do not fail when raw_write_window source is missing.",
    )
    parser.add_argument(
        "--trace-source-dir",
        default="",
        help="Optional canonical trace export directory. Defaults to canoe/logging/evidence/incoming/<TIER>/trace",
    )
    parser.add_argument(
        "--logging-source-dir",
        default="",
        help="Optional canonical logging export directory. Defaults to canoe/logging/evidence/incoming/<TIER>/logging",
    )
    parser.add_argument(
        "--supplementary-lookback-minutes",
        type=int,
        default=90,
        help="Fallback recent-file window when native execute context is unavailable",
    )
    parser.add_argument(
        "--disable-supplementary-auto-discovery",
        action="store_true",
        help="Do not probe cfg-derived or local logging roots when incoming trace/logging dirs are empty",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    evidence_root = _repo_path(args.evidence_root)
    cfg_root = _repo_path(args.cfg_root)
    assign_root = _repo_path(args.assign_root)
    assign_name = ASSIGN_DIR_BY_TIER[args.tier]

    run_dir = evidence_root / args.tier / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    native_dir = run_dir / "native_reports"
    native_dir.mkdir(parents=True, exist_ok=True)
    supplementary_dir = run_dir / "supplementary"
    supplementary_trace_dir = supplementary_dir / "trace"
    supplementary_logging_dir = supplementary_dir / "logging"

    copied_summary: list[str] = []
    copied_assign_reports: list[str] = []
    copied_settings: list[str] = []
    copied_trace_files: list[str] = []
    copied_logging_files: list[str] = []

    summary_report = cfg_root / f"Report_{assign_name}.vtestreport"
    copied = _copy_if_exists(summary_report, native_dir / summary_report.name)
    if copied:
        copied_summary.append(copied)

    copied_settings.extend(
        _copy_matching(cfg_root, f"Report_{assign_name}*.settings", native_dir / "settings")
    )

    assign_dir = assign_root / assign_name
    if assign_dir.exists():
        copied_assign_reports.extend(
            _copy_matching(assign_dir, "Report_*.vtestreport", native_dir / assign_name)
        )

    raw_log_source = resolve_raw_log_source(args.tier, args.raw_log_source)
    raw_log_dest = run_dir / "raw_write_window.txt"
    raw_log_copied = None
    if raw_log_source is not None:
        raw_log_copied = _copy_if_exists(raw_log_source, raw_log_dest)
    elif not args.allow_missing_raw_log:
        print(
            "[COLLECT] FAIL: raw write window source not found. "
            "Pass --raw-log-source or configure one of the standard drop paths."
        )
        return 2

    discovery_earliest, discovery_latest, native_context = _recent_time_window(
        args.tier,
        lookback_minutes=args.supplementary_lookback_minutes,
        summary_report=summary_report,
        raw_log_source=raw_log_source,
    )
    auto_discovery_roots = _default_auto_discovery_roots()
    excluded_roots = [run_dir, evidence_root / args.tier]

    trace_source_dir = resolve_source_dir(args.trace_source_dir, default_trace_source_dirs(args.tier))
    logging_source_dir = resolve_source_dir(args.logging_source_dir, default_logging_source_dirs(args.tier))
    trace_collection_mode = "none"
    logging_collection_mode = "none"
    trace_auto_roots: list[str] = []
    logging_auto_roots: list[str] = []
    if trace_source_dir is not None:
        copied_trace_files.extend(_copy_tree(trace_source_dir, supplementary_trace_dir))
        trace_collection_mode = "explicit" if args.trace_source_dir else "incoming"
    elif not args.disable_supplementary_auto_discovery:
        copied_trace_files, trace_auto_roots = _copy_recent_supplementary(
            kind="trace",
            src_roots=auto_discovery_roots,
            dst_root=supplementary_trace_dir,
            earliest=discovery_earliest,
            latest=discovery_latest,
            exclude_roots=excluded_roots,
        )
        if copied_trace_files:
            trace_collection_mode = "auto-discovered"
    if logging_source_dir is not None:
        copied_logging_files.extend(_copy_tree(logging_source_dir, supplementary_logging_dir))
        logging_collection_mode = "explicit" if args.logging_source_dir else "incoming"
    elif not args.disable_supplementary_auto_discovery:
        copied_logging_files, logging_auto_roots = _copy_recent_supplementary(
            kind="logging",
            src_roots=auto_discovery_roots,
            dst_root=supplementary_logging_dir,
            earliest=discovery_earliest,
            latest=discovery_latest,
            exclude_roots=excluded_roots,
        )
        if copied_logging_files:
            logging_collection_mode = "auto-discovered"

    manifest = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "run_id": args.run_id,
        "tier": args.tier,
        "assign_name": assign_name,
        "native_execute_context": native_context,
        "summary_reports": copied_summary,
        "assign_reports": copied_assign_reports,
        "settings_files": copied_settings,
        "raw_log_source": "" if raw_log_source is None else _rel(raw_log_source),
        "raw_log_copied": raw_log_copied or "",
        "trace_source_dir": "" if trace_source_dir is None else _rel(trace_source_dir),
        "trace_collection_mode": trace_collection_mode,
        "trace_auto_discovery_roots": trace_auto_roots,
        "trace_files": copied_trace_files,
        "logging_source_dir": "" if logging_source_dir is None else _rel(logging_source_dir),
        "logging_collection_mode": logging_collection_mode,
        "logging_auto_discovery_roots": logging_auto_roots,
        "logging_files": copied_logging_files,
    }
    manifest_path = run_dir / "native_report_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"[COLLECT] tier={args.tier} run_id={args.run_id} "
        f"summary={len(copied_summary)} assign_reports={len(copied_assign_reports)} "
        f"settings={len(copied_settings)} raw_log={'Y' if raw_log_copied else 'N'} "
        f"trace_files={len(copied_trace_files)}({trace_collection_mode}) "
        f"logging_files={len(copied_logging_files)}({logging_collection_mode})"
    )
    print(f"[OUT] {_rel(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
