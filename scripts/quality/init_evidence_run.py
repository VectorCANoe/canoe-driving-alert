#!/usr/bin/env python3
"""Initialize UT/IT/ST evidence run folders with templates."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_SPECS = {
    "UT": ("05_Unit_Test.md", re.compile(r"\bUT_(?:\d{3}|[A-Z0-9_]+_(?:\d{3}|[A-Z]))\b")),
    "IT": ("06_Integration_Test.md", re.compile(r"\bIT_(?:\d{3}|[A-Z0-9_]+_(?:\d{3}|[A-Z]))\b")),
    "ST": ("07_System_Test.md", re.compile(r"\bST_(?:\d{3}|[A-Z0-9_]+_(?:\d{3}|[A-Z]))\b")),
}
EXACT_ID_RE = re.compile(r"^(UT|IT|ST)_(\d{3})$")
RANGE_RE = re.compile(r"^(UT|IT|ST)_(\d{3})-(?:UT|IT|ST)_(\d{3})$")
SCENARIO_CALL_RE = re.compile(r"launchScenarioAndWait\((\d+)\s*,")
VERIFICATION_FIELDS = [
    "tier",
    "test_id",
    "scenario_id",
    "input_ts_ms",
    "output_ts_ms",
    "latency_ms",
    "rule_type",
    "rule_ms",
    "expected",
    "observed",
    "logic_verdict",
    "comm_verdict",
    "verdict",
    "owner",
    "run_date",
    "evidence_log_path",
    "evidence_capture_path",
    "native_asset",
    "note",
]
CAPTURE_FIELDS = [
    "tier",
    "test_id",
    "capture_slot",
    "file_name",
    "file_path",
    "description",
    "note",
]


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def load_doc_ids(doc_path: Path, pattern: re.Pattern[str]) -> list[str]:
    if not doc_path.exists():
        return []
    text = doc_path.read_text(encoding="utf-8", errors="ignore")
    seen: set[str] = set()
    ids: list[str] = []
    for match in pattern.finditer(text):
        test_id = match.group(0)
        if test_id not in seen:
            seen.add(test_id)
            ids.append(test_id)
    return sorted(ids, key=_sort_key)


def load_doc_meta(tier: str, doc_path: Path, pattern: re.Pattern[str]) -> dict[str, dict[str, str]]:
    if not doc_path.exists():
        return {}
    meta: dict[str, dict[str, str]] = {}
    for line in doc_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if not parts or all(not part for part in parts):
            continue
        joined = " | ".join(parts)
        match = pattern.search(joined)
        if not match:
            continue
        test_id = match.group(0)
        if tier == "UT":
            title = parts[2] if len(parts) > 2 else ""
            expected = parts[3] if len(parts) > 3 else title
        elif tier == "IT":
            title = parts[2] if len(parts) > 2 else ""
            expected = parts[3] if len(parts) > 3 else title
        else:
            title = parts[1] if len(parts) > 1 else ""
            expected = title
        meta[test_id] = {
            "title": title,
            "expected": expected,
        }
    return meta


def _sort_key(test_id: str) -> tuple[str, int, str]:
    m = EXACT_ID_RE.match(test_id)
    if m:
        return (m.group(1), int(m.group(2)), "")
    return (test_id[:2], 999999, test_id)


def _expand_id_expr(text: str) -> list[str]:
    value = text.strip().strip("`")
    m_exact = EXACT_ID_RE.match(value)
    if m_exact:
        return [value]
    m_range = RANGE_RE.match(value)
    if not m_range:
        return []
    prefix = m_range.group(1)
    start = int(m_range.group(2))
    end = int(m_range.group(3))
    if end < start:
        start, end = end, start
    return [f"{prefix}_{index:03d}" for index in range(start, end + 1)]


def load_asset_map(mapping_path: Path) -> dict[str, str]:
    if not mapping_path.exists():
        return {}
    rows = mapping_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    asset_map: dict[str, str] = {}
    for line in rows:
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        if parts[0] in {"ID", "---"} or not parts[0]:
            continue
        expanded = _expand_id_expr(parts[0])
        if not expanded:
            continue
        asset = parts[1].strip().strip("`")
        for test_id in expanded:
            asset_map.setdefault(test_id, asset)
    return asset_map


def load_asset_scenarios(asset: str) -> list[str]:
    if not asset:
        return []
    asset_path = REPO_ROOT / "canoe" / "tests" / "modules" / "test_units" / asset / f"{asset}.can"
    if not asset_path.exists():
        return []
    text = asset_path.read_text(encoding="utf-8", errors="ignore")
    scenarios: list[str] = []
    seen: set[str] = set()
    for match in SCENARIO_CALL_RE.finditer(text):
        value = match.group(1)
        if value not in seen:
            seen.add(value)
            scenarios.append(value)
    return scenarios


def derive_rule_seed(text: str) -> tuple[str, str]:
    normalized = text.replace("`", "")
    matches = re.findall(r"(\d+)\s*ms", normalized, flags=re.IGNORECASE)
    if not matches:
        return "", ""

    ms = int(matches[0])
    lower = normalized.lower()

    if "timeout" in lower or "타임아웃" in normalized or "동안 갱신이 없으면" in normalized:
        if ms == 1000:
            return "BETWEEN", "1000:1300"
        return "BETWEEN", f"{ms}:{ms + 300}"
    if "주기" in normalized:
        return "EQ", str(ms)
    if "이내" in normalized or "상한" in normalized:
        return "LE", str(ms)
    if "이상" in normalized:
        return "GE", str(ms)
    return "", ""


def build_verification_rows(
    tier: str,
    test_ids: list[str],
    asset_map: dict[str, str],
    doc_meta: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for test_id in test_ids:
        native_asset = asset_map.get(test_id, "")
        scenarios = load_asset_scenarios(native_asset)
        if not scenarios:
            scenarios = [""]
        meta = doc_meta.get(test_id, {})
        expected = meta.get("expected", "")
        rule_type, rule_ms = derive_rule_seed(expected)
        for index, scenario_id in enumerate(scenarios, start=1):
            note = "Fill rule_* and evidence paths for executed rows before score"
            if native_asset and scenario_id:
                suffix = f" scenario {index}/{len(scenarios)}" if len(scenarios) > 1 else ""
                note = f"Auto-seeded from {native_asset}{suffix}"
            if not rule_type or not rule_ms:
                note += "; rule seed requires manual confirmation"
            rows.append(
                {
                    "tier": tier,
                    "test_id": test_id,
                    "scenario_id": scenario_id,
                    "input_ts_ms": "",
                    "output_ts_ms": "",
                    "latency_ms": "",
                    "rule_type": rule_type,
                    "rule_ms": rule_ms,
                    "expected": expected,
                    "observed": "",
                    "logic_verdict": "",
                    "comm_verdict": "",
                    "verdict": "",
                    "owner": "",
                    "run_date": "",
                    "evidence_log_path": "",
                    "evidence_capture_path": "",
                    "native_asset": native_asset,
                    "note": note,
                }
            )
    return rows


def build_capture_rows(tier: str, test_ids: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for test_id in test_ids:
        for slot, description in (
            ("vehicle", "vehicle screen capture"),
            ("control", "control panel capture"),
            ("monitor", "state monitor capture"),
        ):
            rows.append(
                {
                    "tier": tier,
                    "test_id": test_id,
                    "capture_slot": slot,
                    "file_name": "",
                    "file_path": "",
                    "description": description,
                    "note": "",
                }
            )
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def ensure_standard_roots(evidence_root: Path, write_window_root: Path) -> None:
    for tier in ("UT", "IT", "ST", "FULL"):
        (evidence_root / tier).mkdir(parents=True, exist_ok=True)
        (write_window_root / tier).mkdir(parents=True, exist_ok=True)
        (write_window_root / tier / "trace").mkdir(parents=True, exist_ok=True)
        (write_window_root / tier / "logging").mkdir(parents=True, exist_ok=True)
    (evidence_root / "templates").mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create evidence run folder skeleton")
    parser.add_argument(
        "--run-id",
        default=dt.datetime.now().strftime("%Y%m%d_%H%M"),
        help="Run folder suffix (default: current timestamp)",
    )
    parser.add_argument(
        "--root",
        default="canoe/logging/evidence",
        help="Evidence root path",
    )
    parser.add_argument(
        "--docs-root",
        default="driving-alert-workproducts",
        help="Official docs root path",
    )
    parser.add_argument(
        "--mapping-md",
        default="canoe/docs/verification/test-asset-mapping.md",
        help="Test asset mapping markdown path",
    )
    parser.add_argument(
        "--write-window-root",
        default="canoe/logging/evidence/incoming",
        help="Standard Write Window drop root path",
    )
    args = parser.parse_args()

    root = _repo_path(Path(args.root))
    docs_root = _repo_path(Path(args.docs_root))
    mapping_path = _repo_path(Path(args.mapping_md))
    write_window_root = _repo_path(Path(args.write_window_root))
    asset_map = load_asset_map(mapping_path)
    ensure_standard_roots(root, write_window_root)

    tiers = ["UT", "IT", "ST"]
    created = []
    for tier in tiers:
        doc_name, pattern = DOC_SPECS[tier]
        doc_path = docs_root / doc_name
        test_ids = load_doc_ids(doc_path, pattern)
        doc_meta = load_doc_meta(tier, doc_path, pattern)
        run_dir = root / tier / args.run_id
        cap_dir = run_dir / "captures"
        run_dir.mkdir(parents=True, exist_ok=True)
        cap_dir.mkdir(parents=True, exist_ok=True)

        write_csv(
            run_dir / "verification_log.csv",
            VERIFICATION_FIELDS,
            build_verification_rows(tier, test_ids, asset_map, doc_meta),
        )
        write_csv(run_dir / "capture_index.csv", CAPTURE_FIELDS, build_capture_rows(tier, test_ids))
        (run_dir / "raw_write_window.txt").write_text("", encoding="utf-8")
        created.append(run_dir)

    print("[EVIDENCE_INIT] created run folders:")
    for p in created:
        print(f"- {_rel(p)}")
    print("[EVIDENCE_INIT] standard write-window drop roots:")
    for tier in ("UT", "IT", "ST", "FULL"):
        print(f"- {_rel(write_window_root / tier / 'raw_write_window.txt')}")
    print("[EVIDENCE_INIT] standard supplementary drop roots:")
    for tier in ("UT", "IT", "ST", "FULL"):
        print(f"- {_rel(write_window_root / tier / 'trace')}")
        print(f"- {_rel(write_window_root / tier / 'logging')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
