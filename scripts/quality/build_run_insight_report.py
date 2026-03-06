#!/usr/bin/env python3
"""Build run-level verification insight report from scored UT/IT/ST logs."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


TIERS = ("UT", "IT", "ST")


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


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


def latency_stats(values: list[float]) -> dict[str, float | int | None]:
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


def fmt_num(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def parse_rule_upper(rule_type: str, rule_ms: str) -> float | None:
    rt = (rule_type or "").strip().upper()
    rs = (rule_ms or "").strip()
    if not rs:
        return None
    try:
        if rt == "LE":
            return float(rs)
        if rt == "BETWEEN":
            _lo, hi = rs.split(":")
            return float(hi)
    except ValueError:
        return None
    return None


def load_scored_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not path.exists():
        return rows
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
    parser = argparse.ArgumentParser(description="Build run-level insight report")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--baseline-run-id", default="")
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument("--near-limit-ms", type=float, default=15.0)
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/run_insight_report.md"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/run_insight_report.json"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    run_rows: list[dict[str, str]] = []
    missing_tiers: list[str] = []
    source_map: dict[str, str] = {}

    for tier in TIERS:
        path = find_scored_csv(args.evidence_root, tier, args.run_id)
        rows = load_scored_rows(path)
        if not rows:
            missing_tiers.append(tier)
            continue
        source_map[tier] = str(path)
        run_rows.extend(rows)

    if not run_rows:
        print(f"[FAIL] no scored data found for run-id={args.run_id}")
        return 2

    overall_verdict = Counter()
    tier_counter = Counter()
    tier_pass = Counter()
    tier_fail = Counter()
    fail_reason_counter = Counter()
    all_latencies: list[float] = []
    tier_latencies: dict[str, list[float]] = defaultdict(list)
    near_limit_rows: list[tuple[str, str, float, str, str]] = []
    utilization_rows: list[tuple[str, str, float]] = []
    scenario_latencies: dict[str, list[float]] = defaultdict(list)

    baseline_delta_rows: list[tuple[str, str, float, float, float]] = []
    baseline_counter = Counter()
    baseline_map: dict[str, float] = {}

    if args.baseline_run_id:
        for tier in TIERS:
            bpath = find_scored_csv(args.evidence_root, tier, args.baseline_run_id)
            for row in load_scored_rows(bpath):
                test_id = (row.get("test_id") or "").strip()
                if not test_id:
                    continue
                latency = parse_float(row.get("computed_latency_ms", "")) or parse_float(row.get("latency_ms", ""))
                if latency is None:
                    continue
                baseline_map[f"{tier}:{test_id}"] = latency

    for row in run_rows:
        tier = (row.get("tier") or "").strip().upper() or "UNKNOWN"
        test_id = (row.get("test_id") or "").strip() or "UNKNOWN"
        scenario = (row.get("scenario_id") or "").strip() or "-"
        verdict = (row.get("computed_verdict") or row.get("verdict") or "").strip().upper()
        if verdict not in {"PASS", "FAIL"}:
            verdict = "FAIL"
        overall_verdict[verdict] += 1
        tier_counter[tier] += 1
        if verdict == "PASS":
            tier_pass[tier] += 1
        else:
            tier_fail[tier] += 1

        latency = parse_float(row.get("computed_latency_ms", "")) or parse_float(row.get("latency_ms", ""))
        margin = parse_float(row.get("computed_margin_ms", ""))
        rule_type = (row.get("rule_type") or "").strip()
        rule_ms = (row.get("rule_ms") or "").strip()
        if latency is not None:
            all_latencies.append(latency)
            tier_latencies[tier].append(latency)
            scenario_latencies[scenario].append(latency)

            upper = parse_rule_upper(rule_type, rule_ms)
            if upper and upper > 0:
                utilization_rows.append((tier, test_id, latency / upper))

        if (
            verdict == "PASS"
            and margin is not None
            and margin >= 0
            and margin <= args.near_limit_ms
        ):
            near_limit_rows.append((tier, test_id, margin, rule_type, rule_ms))

        reasons = (row.get("computed_fail_reasons") or "").strip()
        for reason in [r for r in reasons.split(";") if r]:
            fail_reason_counter[reason] += 1

        if baseline_map and latency is not None:
            key = f"{tier}:{test_id}"
            if key in baseline_map:
                base = baseline_map[key]
                delta = latency - base
                baseline_delta_rows.append((tier, test_id, base, latency, delta))
                if delta > 5.0:
                    baseline_counter["REGRESSED"] += 1
                elif delta < -5.0:
                    baseline_counter["IMPROVED"] += 1
                else:
                    baseline_counter["STABLE"] += 1

    overall_stats = latency_stats(all_latencies)
    tier_stats = {tier: latency_stats(vals) for tier, vals in tier_latencies.items()}
    near_limit_top = sorted(near_limit_rows, key=lambda x: x[2])[:10]
    utilization_top = sorted(utilization_rows, key=lambda x: x[2], reverse=True)[:10]
    scenario_hotspots = sorted(
        [(sid, latency_stats(vals)) for sid, vals in scenario_latencies.items()],
        key=lambda x: (x[1]["p95"] or -1),
        reverse=True,
    )[:10]
    top_regressions = sorted([r for r in baseline_delta_rows if r[4] > 0], key=lambda x: x[4], reverse=True)[:10]

    gate_result = "PASS" if overall_verdict["FAIL"] == 0 else "FAIL"
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    recommendations: list[str] = []
    if overall_verdict["FAIL"] > 0:
        recommendations.append(
            "FAIL row exists: close failed rows in verification_log_scored.csv first, then re-run score and insight."
        )
    if near_limit_top:
        recommendations.append(
            "Near-limit PASS detected: review scheduler/period jitter for listed tests before release freeze."
        )
    if baseline_counter["REGRESSED"] > 0:
        recommendations.append(
            "Regression against baseline detected: prioritize top regression cases and verify CAPL change impact."
        )
    if gate_result == "PASS" and not near_limit_top and baseline_counter["REGRESSED"] == 0:
        recommendations.append(
            "Stable run: proceed to evidence binding in 05/06/07 and prepare G4 audit packet."
        )
    if missing_tiers:
        recommendations.append(
            "Missing tier data found: complete scored outputs for missing tiers to ensure UT/IT/ST coverage."
        )

    payload = {
        "generated_at": now,
        "run_id": args.run_id,
        "baseline_run_id": args.baseline_run_id,
        "gate_result": gate_result,
        "missing_tiers": missing_tiers,
        "source_map": source_map,
        "summary": {
            "total": sum(tier_counter.values()),
            "pass": overall_verdict["PASS"],
            "fail": overall_verdict["FAIL"],
        },
        "latency_stats_overall": overall_stats,
        "latency_stats_by_tier": tier_stats,
        "near_limit_ms": args.near_limit_ms,
        "near_limit_cases": [
            {"tier": t, "test_id": tid, "margin_ms": m, "rule_type": rt, "rule_ms": rms}
            for t, tid, m, rt, rms in near_limit_top
        ],
        "top_budget_utilization": [
            {"tier": t, "test_id": tid, "utilization": util} for t, tid, util in utilization_top
        ],
        "scenario_hotspots": [
            {"scenario_id": sid, "stats": stats} for sid, stats in scenario_hotspots
        ],
        "fail_reason_distribution": dict(fail_reason_counter),
        "baseline_comparison": {
            "compared_count": len(baseline_delta_rows),
            "status_counts": dict(baseline_counter),
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
        },
        "recommendations": recommendations,
    }

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Run Insight Report",
        "",
        f"- Generated: {now}",
        f"- Run ID: `{args.run_id}`",
        f"- Baseline Run ID: `{args.baseline_run_id or '-'}`",
        f"- Gate Result: `{gate_result}`",
        "",
        "## Summary",
        f"- Total: {sum(tier_counter.values())}",
        f"- PASS: {overall_verdict['PASS']}",
        f"- FAIL: {overall_verdict['FAIL']}",
        "",
        "## Tier Coverage",
        "| Tier | Total | PASS | FAIL | p95(ms) | avg(ms) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for tier in TIERS:
        stats = tier_stats.get(tier, latency_stats([]))
        lines.append(
            f"| {tier} | {tier_counter[tier]} | {tier_pass[tier]} | {tier_fail[tier]} | {fmt_num(stats['p95'])} | {fmt_num(stats['avg'])} |"
        )
    if missing_tiers:
        lines += ["", f"- Missing tier data: {', '.join(missing_tiers)}"]

    lines += [
        "",
        "## Overall Latency KPI",
        f"- min/p50/p90/p95/avg/max (ms): {fmt_num(overall_stats['min'])} / {fmt_num(overall_stats['p50'])} / {fmt_num(overall_stats['p90'])} / {fmt_num(overall_stats['p95'])} / {fmt_num(overall_stats['avg'])} / {fmt_num(overall_stats['max'])}",
    ]

    if utilization_top:
        lines += ["", "## Timing Budget Utilization (Top 10, higher = riskier)"]
        lines += [f"- {t}:{tid} utilization={util*100:.1f}%" for t, tid, util in utilization_top]

    if near_limit_top:
        lines += ["", f"## Near-Limit PASS (margin <= {args.near_limit_ms}ms)"]
        lines += [f"- {t}:{tid} margin={m:.3f}ms rule={rt}:{rms}" for t, tid, m, rt, rms in near_limit_top]

    if scenario_hotspots:
        lines += ["", "## Scenario Hotspots (Top p95)"]
        lines += [
            f"- scenario={sid} p95={fmt_num(stats['p95'])}ms avg={fmt_num(stats['avg'])}ms count={stats['count']}"
            for sid, stats in scenario_hotspots
        ]

    if fail_reason_counter:
        lines += ["", "## Failure Reason Distribution"]
        for reason, count in sorted(fail_reason_counter.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {reason}: {count}")

    if args.baseline_run_id:
        lines += [
            "",
            "## Baseline Comparison",
            f"- compared rows: {len(baseline_delta_rows)}",
            f"- regressed/improved/stable: {baseline_counter['REGRESSED']} / {baseline_counter['IMPROVED']} / {baseline_counter['STABLE']}",
        ]
        if top_regressions:
            lines += ["", "### Top Regressions"]
            lines += [
                f"- {tier}:{test_id} baseline={base:.3f}ms current={cur:.3f}ms delta=+{delta:.3f}ms"
                for tier, test_id, base, cur, delta in top_regressions
            ]

    if recommendations:
        lines += ["", "## Recommended Actions"]
        lines += [f"- {item}" for item in recommendations]

    lines += ["", "## Output", f"- JSON: `{args.output_json}`"]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"[RUN_INSIGHT] run_id={args.run_id} total={sum(tier_counter.values())} "
        f"pass={overall_verdict['PASS']} fail={overall_verdict['FAIL']} result={gate_result}"
    )
    print(f"[OUT] {args.output_md}")
    print(f"[OUT] {args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
