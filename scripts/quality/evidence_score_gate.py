#!/usr/bin/env python3
"""Score UT/IT/ST evidence logs against timing rules and generate insights.

Input format is compatible with:
  canoe/logging/evidence/templates/verification_log_template.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
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


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    rank = (len(ordered) - 1) * (pct / 100.0)
    lower = int(math.floor(rank))
    upper = int(math.ceil(rank))
    if lower == upper:
        return ordered[lower]
    ratio = rank - lower
    return ordered[lower] * (1.0 - ratio) + ordered[upper] * ratio


def make_latency_stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {
            "count": 0,
            "min": None,
            "p50": None,
            "p90": None,
            "p95": None,
            "avg": None,
            "max": None,
        }
    return {
        "count": len(values),
        "min": min(values),
        "p50": percentile(values, 50),
        "p90": percentile(values, 90),
        "p95": percentile(values, 95),
        "avg": sum(values) / len(values),
        "max": max(values),
    }


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def load_baseline_latencies(path: Path) -> dict[str, float]:
    baseline: dict[str, float] = {}
    if not path.exists():
        return baseline
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tier = (row.get("tier") or "").strip().upper()
            test_id = (row.get("test_id") or "").strip()
            if not test_id:
                continue
            latency = parse_float(row.get("computed_latency_ms", ""))
            if latency is None:
                latency = parse_float(row.get("latency_ms", ""))
            if latency is None:
                continue
            key = f"{tier}:{test_id}"
            baseline[key] = latency
    return baseline


def score_row(rule_type: str, rule_ms: str, latency: float) -> tuple[bool, str, float | None, float | None]:
    """Return (pass, rule_expr, margin_ms, target_ms).

    margin_ms:
      - Positive or zero when row is inside rule boundary.
      - Negative when row is outside boundary.
      - For EQ, margin is zero only if exact match, otherwise negative distance.
    """
    rt = (rule_type or "").strip().upper()
    rs = (rule_ms or "").strip()

    if rt == "LE":
        limit = float(rs)
        margin = limit - latency
        return latency <= limit, f"latency <= {limit}", margin, limit

    if rt == "GE":
        limit = float(rs)
        margin = latency - limit
        return latency >= limit, f"latency >= {limit}", margin, limit

    if rt == "EQ":
        target = float(rs)
        delta = abs(latency - target)
        margin = 0.0 if delta == 0 else -delta
        return latency == target, f"latency == {target}", margin, target

    if rt == "BETWEEN":
        left, right = rs.split(":")
        lo, hi = float(left), float(right)
        passed = lo <= latency <= hi
        if passed:
            margin = min(latency - lo, hi - latency)
        else:
            margin = -min(abs(latency - lo), abs(latency - hi))
        return passed, f"{lo} <= latency <= {hi}", margin, (lo + hi) / 2.0

    raise ValueError(f"Unsupported rule_type '{rule_type}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score verification evidence CSV")
    parser.add_argument("--input", required=True, help="Path to verification_log.csv")
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
        "--output-json",
        default="",
        help="JSON summary output path (default: <output-md>.json)",
    )
    parser.add_argument(
        "--baseline-csv",
        default="",
        help="Optional baseline scored CSV for latency regression comparison",
    )
    parser.add_argument(
        "--regression-threshold-ms",
        type=float,
        default=5.0,
        help="Delta threshold for improved/regressed classification against baseline",
    )
    parser.add_argument(
        "--near-limit-ms",
        type=float,
        default=15.0,
        help="PASS rows with margin <= this value are reported as near-limit",
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

    input_path = _repo_path(Path(args.input))
    output_csv = _repo_path(Path(args.output_csv))
    output_md = _repo_path(Path(args.output_md))
    output_json = _repo_path(Path(args.output_json)) if args.output_json else output_md.with_suffix(".json")
    baseline_csv = _repo_path(Path(args.baseline_csv)) if args.baseline_csv else None

    if not input_path.exists():
        print(f"[FAIL] input not found: {_rel(input_path)}")
        return 2

    rows: list[dict[str, str]] = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("[FAIL] no rows in input csv")
        return 2

    tier_counter: Counter[str] = Counter()
    verdict_counter: Counter[str] = Counter()
    fail_reason_counter: Counter[str] = Counter()
    parse_errors: list[str] = []
    metadata_errors: list[str] = []
    axis_errors: list[str] = []
    fail_details: list[str] = []
    tier_pass: dict[str, int] = defaultdict(int)
    tier_fail: dict[str, int] = defaultdict(int)
    tier_latencies: dict[str, list[float]] = defaultdict(list)
    all_latencies: list[float] = []
    near_limit_rows: list[tuple[str, str, float, str, str]] = []
    baseline_deltas: list[tuple[str, str, float, float, float]] = []
    baseline_cmp_counter: Counter[str] = Counter()
    scored_rows: list[dict[str, str]] = []

    baseline_map = load_baseline_latencies(baseline_csv) if baseline_csv else {}

    for i, row in enumerate(rows, start=2):
        tier = (row.get("tier") or "").strip().upper() or "UNKNOWN"
        test_id = (row.get("test_id") or "").strip() or "UNKNOWN"
        scenario_id = (row.get("scenario_id") or "").strip() or "-"
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

        tier_counter[tier] += 1
        failure_reasons: list[str] = []
        margin_ms: float | None = None
        target_ms: float | None = None

        if latency is None:
            computed_verdict = "FAIL"
            period_verdict = "FAIL"
            rule_expr = "latency missing"
            parse_errors.append(f"L{i} {test_id}: latency/input/output missing")
            failure_reasons.append("PERIOD_DATA_MISSING")
        else:
            try:
                passed, rule_expr, margin_ms, target_ms = score_row(rule_type, rule_ms, latency)
                period_verdict = "PASS" if passed else "FAIL"
                computed_verdict = period_verdict
                if not passed:
                    failure_reasons.append("PERIOD_RULE_FAIL")
            except Exception as ex:
                computed_verdict = "FAIL"
                period_verdict = "FAIL"
                rule_expr = f"rule parse error: {ex}"
                parse_errors.append(f"L{i} {test_id}: {ex}")
                failure_reasons.append("PERIOD_RULE_PARSE_ERROR")

        if not args.no_strict_metadata:
            if not owner:
                metadata_errors.append(f"L{i} {test_id}: owner missing")
                computed_verdict = "FAIL"
                failure_reasons.append("META_OWNER_MISSING")
            if not run_date or not valid_iso_date(run_date):
                metadata_errors.append(f"L{i} {test_id}: run_date invalid or missing")
                computed_verdict = "FAIL"
                failure_reasons.append("META_RUN_DATE_INVALID")
            if not evidence_log_path:
                metadata_errors.append(f"L{i} {test_id}: evidence_log_path missing")
                computed_verdict = "FAIL"
                failure_reasons.append("META_LOG_PATH_MISSING")
            if not evidence_capture_path:
                metadata_errors.append(f"L{i} {test_id}: evidence_capture_path missing")
                computed_verdict = "FAIL"
                failure_reasons.append("META_CAPTURE_PATH_MISSING")

        if not args.no_strict_axis:
            if logic_verdict not in {"PASS", "FAIL"}:
                axis_errors.append(f"L{i} {test_id}: logic_verdict missing")
                computed_verdict = "FAIL"
                logic_verdict = ""
                failure_reasons.append("AXIS_LOGIC_MISSING")
            if comm_verdict not in {"PASS", "FAIL"}:
                axis_errors.append(f"L{i} {test_id}: comm_verdict missing")
                computed_verdict = "FAIL"
                comm_verdict = ""
                failure_reasons.append("AXIS_COMM_MISSING")
            if logic_verdict == "FAIL":
                computed_verdict = "FAIL"
                failure_reasons.append("AXIS_LOGIC_FAIL")
            if comm_verdict == "FAIL":
                computed_verdict = "FAIL"
                failure_reasons.append("AXIS_COMM_FAIL")
        else:
            if logic_verdict == "FAIL":
                computed_verdict = "FAIL"
                failure_reasons.append("AXIS_LOGIC_FAIL")
            if comm_verdict == "FAIL":
                computed_verdict = "FAIL"
                failure_reasons.append("AXIS_COMM_FAIL")

        if latency is not None:
            tier_latencies[tier].append(latency)
            all_latencies.append(latency)

        if (
            computed_verdict == "PASS"
            and margin_ms is not None
            and margin_ms >= 0
            and margin_ms <= args.near_limit_ms
        ):
            near_limit_rows.append((tier, test_id, margin_ms, rule_type, rule_ms))

        baseline_key = f"{tier}:{test_id}"
        if latency is not None and baseline_key in baseline_map:
            base = baseline_map[baseline_key]
            delta = latency - base
            baseline_deltas.append((tier, test_id, base, latency, delta))
            if delta > args.regression_threshold_ms:
                baseline_cmp_counter["REGRESSED"] += 1
            elif delta < -args.regression_threshold_ms:
                baseline_cmp_counter["IMPROVED"] += 1
            else:
                baseline_cmp_counter["STABLE"] += 1

        verdict_counter[computed_verdict] += 1
        if computed_verdict == "PASS":
            tier_pass[tier] += 1
        else:
            tier_fail[tier] += 1
            fail_details.append(
                f"- {test_id} ({tier}, scenario={scenario_id}): "
                f"latency={fmt_num(latency)}ms rule={rule_type}:{rule_ms} ({rule_expr}) "
                f"reasons={';'.join(sorted(set(failure_reasons)))}"
            )

        for reason in set(failure_reasons):
            fail_reason_counter[reason] += 1

        out = dict(row)
        out["computed_latency_ms"] = "" if latency is None else f"{latency:.3f}"
        out["computed_rule_expr"] = rule_expr
        out["computed_period_verdict"] = period_verdict
        out["computed_logic_verdict"] = logic_verdict
        out["computed_comm_verdict"] = comm_verdict
        out["computed_margin_ms"] = "" if margin_ms is None else f"{margin_ms:.3f}"
        out["computed_target_ms"] = "" if target_ms is None else f"{target_ms:.3f}"
        out["computed_fail_reasons"] = ";".join(sorted(set(failure_reasons)))
        out["computed_verdict"] = computed_verdict
        scored_rows.append(out)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    out_fields = list(scored_rows[0].keys())
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(scored_rows)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gate_result = "PASS" if verdict_counter["FAIL"] == 0 else "FAIL"
    total_rows = sum(tier_counter.values())
    overall_stats = make_latency_stats(all_latencies)
    tier_stats = {tier: make_latency_stats(vals) for tier, vals in tier_latencies.items()}

    near_limit_rows_sorted = sorted(near_limit_rows, key=lambda x: x[2])[:10]
    top_regressions = sorted([x for x in baseline_deltas if x[4] > 0], key=lambda x: x[4], reverse=True)[:10]
    top_improvements = sorted([x for x in baseline_deltas if x[4] < 0], key=lambda x: x[4])[:10]

    summary_payload = {
        "generated_at": now,
        "input_csv": _rel(input_path),
        "output_csv": _rel(output_csv),
        "total": total_rows,
        "pass": verdict_counter["PASS"],
        "fail": verdict_counter["FAIL"],
        "gate_result": gate_result,
        "latency_stats_overall": overall_stats,
        "latency_stats_by_tier": tier_stats,
        "fail_reasons": dict(fail_reason_counter),
        "near_limit_ms": args.near_limit_ms,
        "near_limit_cases": [
            {
                "tier": tier,
                "test_id": test_id,
                "margin_ms": margin,
                "rule_type": rt,
                "rule_ms": rms,
            }
            for tier, test_id, margin, rt, rms in near_limit_rows_sorted
        ],
        "baseline": {
            "enabled": baseline_csv is not None,
            "baseline_csv": _rel(baseline_csv) if baseline_csv else "",
            "regression_threshold_ms": args.regression_threshold_ms,
            "comparison_counts": dict(baseline_cmp_counter),
            "top_regressions": [
                {
                    "tier": tier,
                    "test_id": test_id,
                    "baseline_latency_ms": base,
                    "current_latency_ms": cur,
                    "delta_ms": delta,
                }
                for tier, test_id, base, cur, delta in top_regressions
            ],
            "top_improvements": [
                {
                    "tier": tier,
                    "test_id": test_id,
                    "baseline_latency_ms": base,
                    "current_latency_ms": cur,
                    "delta_ms": delta,
                }
                for tier, test_id, base, cur, delta in top_improvements
            ],
        },
        "strict_metadata": not args.no_strict_metadata,
        "strict_axis": not args.no_strict_axis,
    }

    output_json.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    lines = [
        "# Verification Evidence Score Report",
        "",
        f"- Generated: {now}",
        f"- Input: `{_rel(input_path)}`",
        f"- Output CSV: `{_rel(output_csv)}`",
        f"- Output JSON: `{_rel(output_json)}`",
        "",
        "## Summary",
        f"- Total: {total_rows}",
        f"- PASS: {verdict_counter['PASS']}",
        f"- FAIL: {verdict_counter['FAIL']}",
        f"- Gate Result: `{gate_result}`",
        "",
        "## Latency KPI (Overall)",
        f"- count: {overall_stats['count']}",
        f"- min/p50/p90/p95/avg/max (ms): {fmt_num(overall_stats['min'])} / {fmt_num(overall_stats['p50'])} / {fmt_num(overall_stats['p90'])} / {fmt_num(overall_stats['p95'])} / {fmt_num(overall_stats['avg'])} / {fmt_num(overall_stats['max'])}",
        "",
        "## Tier Breakdown",
        "| Tier | Total | PASS | FAIL | p95(ms) | avg(ms) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for tier in sorted(tier_counter.keys()):
        stats = tier_stats.get(tier, make_latency_stats([]))
        lines.append(
            f"| {tier} | {tier_counter[tier]} | {tier_pass[tier]} | {tier_fail[tier]} | {fmt_num(stats['p95'])} | {fmt_num(stats['avg'])} |"
        )

    if near_limit_rows_sorted:
        lines += ["", f"## Near-Limit PASS Cases (margin <= {args.near_limit_ms}ms)"]
        lines += [
            f"- {tier}:{test_id} margin={margin:.3f}ms rule={rt}:{rms}"
            for tier, test_id, margin, rt, rms in near_limit_rows_sorted
        ]

    if fail_reason_counter:
        lines += ["", "## Failure Reason Distribution"]
        for key, count in sorted(fail_reason_counter.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {key}: {count}")

    if parse_errors:
        lines += ["", "## Parse Errors"]
        lines += [f"- {item}" for item in parse_errors]

    if metadata_errors:
        lines += ["", "## Metadata Errors"]
        lines += [f"- {item}" for item in metadata_errors]

    if axis_errors:
        lines += ["", "## Axis Errors"]
        lines += [f"- {item}" for item in axis_errors]

    if fail_details:
        lines += ["", "## Failed Rows"]
        lines += fail_details

    if baseline_csv:
        lines += ["", "## Baseline Comparison"]
        lines += [f"- baseline csv: `{_rel(baseline_csv)}`"]
        lines += [f"- threshold: {args.regression_threshold_ms}ms"]
        lines += [
            f"- compared: {len(baseline_deltas)} / regressed: {baseline_cmp_counter['REGRESSED']} / improved: {baseline_cmp_counter['IMPROVED']} / stable: {baseline_cmp_counter['STABLE']}"
        ]
        if top_regressions:
            lines += ["", "### Top Regressions"]
            lines += [
                f"- {tier}:{test_id} baseline={base:.3f}ms current={cur:.3f}ms delta=+{delta:.3f}ms"
                for tier, test_id, base, cur, delta in top_regressions
            ]
        if top_improvements:
            lines += ["", "### Top Improvements"]
            lines += [
                f"- {tier}:{test_id} baseline={base:.3f}ms current={cur:.3f}ms delta={delta:.3f}ms"
                for tier, test_id, base, cur, delta in top_improvements
            ]

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        "[EVIDENCE_SCORE] "
        f"total={total_rows} pass={verdict_counter['PASS']} fail={verdict_counter['FAIL']} result={gate_result}"
    )
    print(f"[OUT] {_rel(output_csv)}")
    print(f"[OUT] {_rel(output_md)}")
    print(f"[OUT] {_rel(output_json)}")

    return 0 if gate_result == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
