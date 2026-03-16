#!/usr/bin/env python3
"""Build 05/06/07 document binding bundle from scored verification logs.

Outputs:
- CSV: row-level binding matrix (doc IDs vs scored evidence rows)
- JSON: machine-readable summary
- MD: human-readable status report
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_SPECS = {
    # Accept canonical test IDs only:
    # - *_NNN   (e.g. UT_ADAS_001, ST_BASE_PT_001)
    # - *_A/B/C (boundary suffix, e.g. UT_BND_024_A)
    # This intentionally excludes prose-level shorthand tokens like UT_BASE_PT.
    "UT": ("05_Unit_Test.md", re.compile(r"\bUT_[A-Z0-9_]+_(?:\d{3}|[A-Z])\b")),
    "IT": ("06_Integration_Test.md", re.compile(r"\bIT_[A-Z0-9_]+_(?:\d{3}|[A-Z])\b")),
    "ST": ("07_System_Test.md", re.compile(r"\bST_[A-Z0-9_]+_(?:\d{3}|[A-Z])\b")),
}


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def load_doc_ids(doc_path: Path, pattern: re.Pattern[str]) -> list[str]:
    doc_path = _repo_path(doc_path)
    if not doc_path.exists():
        return []
    text = doc_path.read_text(encoding="utf-8", errors="ignore")
    ids: list[str] = []
    seen: set[str] = set()
    for match in pattern.finditer(text):
        value = match.group(0)
        if value not in seen:
            seen.add(value)
            ids.append(value)
    return ids


def load_scored_rows(path: Path) -> list[dict[str, str]]:
    path = _repo_path(path)
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def find_scored_csv(evidence_root: Path, tier: str, run_id: str) -> Path:
    run_dir = evidence_root / tier / run_id
    preferred = run_dir / "verification_log_scored.csv"
    fallback = run_dir / "verification_log_filled.csv"
    if preferred.exists():
        return preferred
    return fallback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build 05/06/07 doc binding bundle")
    parser.add_argument("--run-id", required=True, help="Run ID, e.g. 20260307_1030")
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument("--docs-root", type=Path, default=Path("driving-alert-workproducts"))
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doc_binding_bundle.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doc_binding_bundle.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doc_binding_bundle.md"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.evidence_root = _repo_path(args.evidence_root)
    args.docs_root = _repo_path(args.docs_root)
    args.output_csv = _repo_path(args.output_csv)
    args.output_json = _repo_path(args.output_json)
    args.output_md = _repo_path(args.output_md)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    output_rows: list[dict[str, str]] = []
    status_counter = Counter()
    tier_counter = Counter()
    missing_docs: list[str] = []
    scored_sources: dict[str, str] = {}

    for tier, (doc_name, pattern) in DOC_SPECS.items():
        doc_path = args.docs_root / doc_name
        doc_ids = load_doc_ids(doc_path, pattern)
        if not doc_path.exists():
            missing_docs.append(_rel(doc_path))

        scored_path = find_scored_csv(args.evidence_root, tier, args.run_id)
        scored_sources[tier] = _rel(scored_path)
        scored_rows = load_scored_rows(scored_path)
        scored_map = {
            (row.get("test_id") or "").strip(): row
            for row in scored_rows
            if (row.get("test_id") or "").strip()
        }

        # Doc IDs -> evidence mapping
        for test_id in doc_ids:
            row = scored_map.get(test_id)
            if row:
                status = "READY"
            else:
                status = "DOC_ONLY"
            status_counter[status] += 1
            tier_counter[tier] += 1
            out = {
                "tier": tier,
                "test_id": test_id,
                "doc_id": test_id,
                "doc_file": doc_name,
                "doc_present": "Y",
                "evidence_present": "Y" if row else "N",
                "binding_status": status,
                "computed_verdict": (row.get("computed_verdict") or "") if row else "",
                "computed_latency_ms": (row.get("computed_latency_ms") or "") if row else "",
                "rule_type": (row.get("rule_type") or "") if row else "",
                "rule_ms": (row.get("rule_ms") or "") if row else "",
                "owner": (row.get("owner") or "") if row else "",
                "run_date": (row.get("run_date") or "") if row else "",
                "evidence_log_path": (row.get("evidence_log_path") or "") if row else "",
                "evidence_capture_path": (row.get("evidence_capture_path") or "") if row else "",
                "computed_fail_reasons": (row.get("computed_fail_reasons") or "") if row else "",
                "note": "",
            }
            output_rows.append(out)

        # Evidence IDs not present in doc
        doc_set = set(doc_ids)
        for test_id, row in sorted(scored_map.items()):
            if test_id in doc_set:
                continue
            status_counter["EVIDENCE_ONLY"] += 1
            tier_counter[tier] += 1
            output_rows.append(
                {
                    "tier": tier,
                    "test_id": test_id,
                    "doc_id": "",
                    "doc_file": doc_name,
                    "doc_present": "N",
                    "evidence_present": "Y",
                    "binding_status": "EVIDENCE_ONLY",
                    "computed_verdict": row.get("computed_verdict", ""),
                    "computed_latency_ms": row.get("computed_latency_ms", ""),
                    "rule_type": row.get("rule_type", ""),
                    "rule_ms": row.get("rule_ms", ""),
                    "owner": row.get("owner", ""),
                    "run_date": row.get("run_date", ""),
                    "evidence_log_path": row.get("evidence_log_path", ""),
                    "evidence_capture_path": row.get("evidence_capture_path", ""),
                    "computed_fail_reasons": row.get("computed_fail_reasons", ""),
                    "note": "Scored evidence exists but no matching ID in 05/06/07",
                }
            )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)

    # Deterministic row order
    output_rows.sort(key=lambda r: (r["tier"], r["binding_status"], r["test_id"]))

    fields = [
        "tier",
        "test_id",
        "doc_id",
        "doc_file",
        "doc_present",
        "evidence_present",
        "binding_status",
        "computed_verdict",
        "computed_latency_ms",
        "rule_type",
        "rule_ms",
        "owner",
        "run_date",
        "evidence_log_path",
        "evidence_capture_path",
        "computed_fail_reasons",
        "note",
    ]
    with args.output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    payload = {
        "generated_at": now,
        "run_id": args.run_id,
        "docs_root": _rel(args.docs_root),
        "evidence_root": _rel(args.evidence_root),
        "scored_sources": scored_sources,
        "missing_docs": missing_docs,
        "summary": {
            "total_rows": len(output_rows),
            "ready": status_counter["READY"],
            "doc_only": status_counter["DOC_ONLY"],
            "evidence_only": status_counter["EVIDENCE_ONLY"],
        },
        "tier_rows": dict(tier_counter),
    }
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Doc Binding Bundle Report (05/06/07)",
        "",
        f"- Generated: {now}",
        f"- Run ID: `{args.run_id}`",
        f"- Docs Root: `{_rel(args.docs_root)}`",
        f"- Evidence Root: `{_rel(args.evidence_root)}`",
        "",
        "## Summary",
        f"- Total Rows: {len(output_rows)}",
        f"- READY: {status_counter['READY']}",
        f"- DOC_ONLY: {status_counter['DOC_ONLY']}",
        f"- EVIDENCE_ONLY: {status_counter['EVIDENCE_ONLY']}",
        "",
        "## Tier Rows",
    ]
    for tier in ("UT", "IT", "ST"):
        lines.append(f"- {tier}: {tier_counter[tier]}")

    if missing_docs:
        lines += ["", "## Missing Documents"]
        lines += [f"- {item}" for item in missing_docs]

    lines += [
        "",
        "## Output",
        f"- CSV: `{_rel(args.output_csv)}`",
        f"- JSON: `{_rel(args.output_json)}`",
        f"- MD: `{_rel(args.output_md)}`",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"[DOC_BIND] run_id={args.run_id} total={len(output_rows)} "
        f"ready={status_counter['READY']} doc_only={status_counter['DOC_ONLY']} "
        f"evidence_only={status_counter['EVIDENCE_ONLY']}"
    )
    print(f"[OUT] {_rel(args.output_csv)}")
    print(f"[OUT] {_rel(args.output_json)}")
    print(f"[OUT] {_rel(args.output_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
