#!/usr/bin/env python3
"""Score UT/IT/ST evidence logs against timing rules.

Input format is compatible with:
  canoe/logging/evidence/templates/verification_log_template.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from collections import Counter, defaultdict
from pathlib import Path


def parse_float(value: str) -> float | None:
    s = (value or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def normalize_verdict(value: str) -> str:
    text = (value or "").strip().upper()
    if text in {"PASS", "FAIL"}:
        return text
    return ""


def valid_iso_date(value: str) -> bool:
    text = (value or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return False
    try:
        dt.datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def score_row(rule_type: str, rule_ms: str, latency: float) -> tuple[bool, str]:
    rt = (rule_type or "").strip().upper()
    rs = (rule_ms or "").strip()

    if rt == "LE":
        limit = float(rs)
        return latency <= limit, f"latency <= {limit}"
    if rt == "GE":
        limit = float(rs)
        return latency >= limit, f"latency >= {limit}"
    if rt == "EQ":
        target = float(rs)
        return latency == target, f"latency == {target}"
    if rt == "BETWEEN":
        left, right = rs.split(":")
        lo, hi = float(left), float(right)
        return lo <= latency <= hi, f"{lo} <= latency <= {hi}"
    raise ValueError(f"Unsupported rule_type '{rule_type}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score verification evidence CSV")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to verification_log.csv",
    )
    parser.add_argument(
        "--output-csv",
        default="canoe/logging/evidence/scored_verification_log.csv",
        help="Scored CSV output path",
    )
    parser.add_argument(
        "--output-md",
        default="canoe/logging/evidence/scored_verification_report.md",
        help="Markdown summary report output path",
    )
    parser.add_argument(
        "--no-strict-metadata",
        action="store_true",
        help="Do not fail rows when owner/date/evidence paths are blank",
    )
    parser.add_argument(
        "--no-strict-axis",
        action="store_true",
        help="Do not fail rows when logic_verdict/comm_verdict are blank",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_csv = Path(args.output_csv)
    output_md = Path(args.output_md)

    if not input_path.exists():
        print(f"[FAIL] input not found: {input_path}")
        return 2

    rows: list[dict[str, str]] = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("[FAIL] no rows in input csv")
        return 2

    tier_counter = Counter()
    verdict_counter = Counter()
    fail_details: list[str] = []
    parse_errors: list[str] = []
    metadata_errors: list[str] = []
    axis_errors: list[str] = []
    tier_pass = defaultdict(int)
    tier_fail = defaultdict(int)

    scored_rows: list[dict[str, str]] = []

    for i, row in enumerate(rows, start=2):
        tier = (row.get("tier") or "").strip().upper()
        test_id = (row.get("test_id") or "").strip()
        rule_type = row.get("rule_type") or ""
        rule_ms = row.get("rule_ms") or ""
        owner = (row.get("owner") or "").strip()
        run_date = (row.get("run_date") or "").strip()
        evidence_log_path = (row.get("evidence_log_path") or "").strip()
        evidence_capture_path = (row.get("evidence_capture_path") or "").strip()
        logic_verdict = normalize_verdict(row.get("logic_verdict", ""))
        comm_verdict = normalize_verdict(row.get("comm_verdict", ""))

        input_ts = parse_float(row.get("input_ts_ms", ""))
        output_ts = parse_float(row.get("output_ts_ms", ""))
        latency = parse_float(row.get("latency_ms", ""))

        if latency is None and input_ts is not None and output_ts is not None:
            latency = output_ts - input_ts

        tier_counter[tier or "UNKNOWN"] += 1

        if latency is None:
            computed_verdict = "FAIL"
            rule_expr = "latency missing"
            parse_errors.append(f"L{i} {test_id}: latency/input/output missing")
            period_verdict = "FAIL"
        else:
            try:
                passed, rule_expr = score_row(rule_type, rule_ms, latency)
                period_verdict = "PASS" if passed else "FAIL"
                computed_verdict = period_verdict
            except Exception as ex:
                computed_verdict = "FAIL"
                rule_expr = f"rule parse error: {ex}"
                parse_errors.append(f"L{i} {test_id}: {ex}")
                period_verdict = "FAIL"

        if not args.no_strict_metadata:
            if not owner:
                metadata_errors.append(f"L{i} {test_id}: owner missing")
                computed_verdict = "FAIL"
            if not run_date or not valid_iso_date(run_date):
                metadata_errors.append(f"L{i} {test_id}: run_date invalid or missing")
                computed_verdict = "FAIL"
            if not evidence_log_path:
                metadata_errors.append(f"L{i} {test_id}: evidence_log_path missing")
                computed_verdict = "FAIL"
            if not evidence_capture_path:
                metadata_errors.append(f"L{i} {test_id}: evidence_capture_path missing")
                computed_verdict = "FAIL"

        if not args.no_strict_axis:
            if logic_verdict not in {"PASS", "FAIL"}:
                axis_errors.append(f"L{i} {test_id}: logic_verdict missing")
                computed_verdict = "FAIL"
                logic_verdict = ""
            if comm_verdict not in {"PASS", "FAIL"}:
                axis_errors.append(f"L{i} {test_id}: comm_verdict missing")
                computed_verdict = "FAIL"
                comm_verdict = ""
            if logic_verdict == "FAIL" or comm_verdict == "FAIL":
                computed_verdict = "FAIL"
        else:
            if logic_verdict == "FAIL" or comm_verdict == "FAIL":
                computed_verdict = "FAIL"

        verdict_counter[computed_verdict] += 1
        if computed_verdict == "PASS":
            tier_pass[tier] += 1
        else:
            tier_fail[tier] += 1
            fail_details.append(
                f"- {test_id or 'UNKNOWN'} ({tier or 'UNKNOWN'}): "
                f"latency={latency} rule={rule_type}:{rule_ms} ({rule_expr})"
            )

        out = dict(row)
        out["computed_latency_ms"] = "" if latency is None else f"{latency:.3f}"
        out["computed_rule_expr"] = rule_expr
        out["computed_period_verdict"] = period_verdict
        out["computed_logic_verdict"] = logic_verdict
        out["computed_comm_verdict"] = comm_verdict
        out["computed_verdict"] = computed_verdict
        scored_rows.append(out)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    out_fields = list(scored_rows[0].keys())
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(scored_rows)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Verification Evidence Score Report",
        "",
        f"- Generated: {now}",
        f"- Input: `{input_path}`",
        f"- Output CSV: `{output_csv}`",
        "",
        "## Summary",
        f"- Total: {sum(tier_counter.values())}",
        f"- PASS: {verdict_counter['PASS']}",
        f"- FAIL: {verdict_counter['FAIL']}",
        "",
        "## Tier Breakdown",
        "| Tier | Total | PASS | FAIL |",
        "| --- | ---: | ---: | ---: |",
    ]
    for tier in sorted(tier_counter.keys()):
        lines.append(
            f"| {tier} | {tier_counter[tier]} | {tier_pass[tier]} | {tier_fail[tier]} |"
        )

    if parse_errors:
        lines += ["", "## Parse Errors"]
        lines += [f"- {e}" for e in parse_errors]

    if metadata_errors:
        lines += ["", "## Metadata Errors"]
        lines += [f"- {e}" for e in metadata_errors]

    if axis_errors:
        lines += ["", "## Axis Errors"]
        lines += [f"- {e}" for e in axis_errors]

    if fail_details:
        lines += ["", "## Failed Rows"]
        lines += fail_details

    verdict = "PASS" if verdict_counter["FAIL"] == 0 else "FAIL"
    lines += ["", f"## Gate Result", f"- `{verdict}`"]

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[EVIDENCE_SCORE] total={sum(tier_counter.values())} pass={verdict_counter['PASS']} fail={verdict_counter['FAIL']} result={verdict}")
    print(f"[OUT] {output_csv}")
    print(f"[OUT] {output_md}")

    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
