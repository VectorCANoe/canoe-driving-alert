#!/usr/bin/env python3
"""Check verification run readiness for finalize workflow."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path


TIERS = ("UT", "IT", "ST")
EVIDENCE_MARKER = "[EVIDENCE_OUT]"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check run readiness for verify finalize")
    parser.add_argument("--run-id", required=True, help="Run ID, e.g. 20260307_1030")
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/run_readiness.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/run_readiness.md"),
    )
    return parser


def marker_count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text.count(EVIDENCE_MARKER)


def scored_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def status_from_rows(rows: dict[str, dict[str, object]]) -> str:
    # Order matters: most concrete status wins.
    if all(bool(item["scored_exists"]) for item in rows.values()):
        return "SCORED_READY"
    if all(bool(item["template_exists"]) and bool(item["raw_exists"]) and int(item["marker_count"]) > 0 for item in rows.values()):
        return "READY_FOR_FINALIZE"
    if any(bool(item["template_exists"]) for item in rows.values()):
        return "PREPARED_PARTIAL"
    return "NOT_PREPARED"


def main() -> int:
    args = build_parser().parse_args()
    now = dt.datetime.now().isoformat(timespec="seconds")

    tier_rows: dict[str, dict[str, object]] = {}
    for tier in TIERS:
        run_dir = args.evidence_root / tier / args.run_id
        template_csv = run_dir / "verification_log.csv"
        raw_log = run_dir / "raw_write_window.txt"
        filled_csv = run_dir / "verification_log_filled.csv"
        scored_csv = run_dir / "verification_log_scored.csv"
        report_md = run_dir / "verification_report.md"
        report_json = run_dir / "verification_report.json"
        tier_rows[tier] = {
            "run_dir": str(run_dir),
            "template_exists": template_csv.exists(),
            "raw_exists": raw_log.exists(),
            "marker_count": marker_count(raw_log),
            "filled_exists": filled_csv.exists(),
            "scored_exists": scored_csv.exists(),
            "report_md_exists": report_md.exists(),
            "report_json_exists": report_json.exists(),
            "scored_rows": scored_row_count(scored_csv),
        }

    overall = status_from_rows(tier_rows)
    missing_items: list[str] = []
    for tier, item in tier_rows.items():
        if not item["template_exists"]:
            missing_items.append(f"{tier}: verification_log.csv")
        if not item["raw_exists"]:
            missing_items.append(f"{tier}: raw_write_window.txt")
        if item["raw_exists"] and int(item["marker_count"]) == 0:
            missing_items.append(f"{tier}: no [EVIDENCE_OUT] marker in raw_write_window.txt")

    payload = {
        "generated_at": now,
        "run_id": args.run_id,
        "overall_status": overall,
        "tiers": tier_rows,
        "missing_items": missing_items,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Verification Run Readiness",
        "",
        f"- Generated: {now}",
        f"- Run ID: `{args.run_id}`",
        f"- Overall: `{overall}`",
        "",
        "## Tier Status",
        "| Tier | Template | Raw Log | Marker Count | Filled | Scored | Scored Rows |",
        "|---|---|---|---:|---|---|---:|",
    ]
    for tier in TIERS:
        item = tier_rows[tier]
        lines.append(
            "| {tier} | {template_exists} | {raw_exists} | {marker_count} | {filled_exists} | {scored_exists} | {scored_rows} |".format(
                tier=tier,
                **item,
            )
        )

    if missing_items:
        lines += ["", "## Missing / Action Needed"]
        lines.extend([f"- {item}" for item in missing_items])

    lines += [
        "",
        "## Output",
        f"- JSON: `{args.output_json}`",
        f"- MD: `{args.output_md}`",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[RUN_STATUS] run_id={args.run_id} overall={overall} missing={len(missing_items)}")
    print(f"[OUT] {args.output_json}")
    print(f"[OUT] {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
