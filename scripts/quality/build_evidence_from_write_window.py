#!/usr/bin/env python3
"""Fill verification_log.csv from Write Window evidence markers.

Expected CAPL log markers:
  [EVIDENCE_IN] scenario=<id> inputTsMs=<ms>
  [EVIDENCE_OUT] scenario=<id> outputTsMs=<ms> result=<0|1> ...
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from pathlib import Path
from typing import Dict, List


IN_RE = re.compile(r"\[EVIDENCE_IN\]\s+scenario=(\d+)\s+inputTsMs=(\d+)")
OUT_RE = re.compile(
    r"\[EVIDENCE_OUT\]\s+scenario=(\d+)\s+outputTsMs=(\d+)\s+result=(\d+)\s+"
    r"level=(\d+)\s+type=(\d+)\s+code=(\d+)\s+timeout=(\d+)\s+risk=(\d+)\s+"
    r"decel=(\d+)\s+failSafe=(\d+)\s+renderType=(\d+)\s+renderCode=(\d+)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fill verification CSV from Write Window logs")
    parser.add_argument("--template-csv", required=True, help="Path to verification_log.csv")
    parser.add_argument("--raw-log", required=True, help="Path to raw_write_window.txt")
    parser.add_argument("--output-csv", default="", help="Output CSV path (default: <template>_filled.csv)")
    parser.add_argument("--owner", default="", help="Owner value to fill when blank")
    parser.add_argument("--run-date", default=dt.date.today().isoformat(), help="Run date YYYY-MM-DD")
    return parser.parse_args()


def parse_events(raw_text: str) -> tuple[Dict[int, List[int]], Dict[int, List[Dict[str, int]]]]:
    in_events: Dict[int, List[int]] = {}
    out_events: Dict[int, List[Dict[str, int]]] = {}

    for line in raw_text.splitlines():
        m_in = IN_RE.search(line)
        if m_in:
            scn = int(m_in.group(1))
            ts = int(m_in.group(2))
            in_events.setdefault(scn, []).append(ts)
            continue

        m_out = OUT_RE.search(line)
        if m_out:
            scn = int(m_out.group(1))
            out_events.setdefault(scn, []).append(
                {
                    "outputTsMs": int(m_out.group(2)),
                    "result": int(m_out.group(3)),
                    "level": int(m_out.group(4)),
                    "type": int(m_out.group(5)),
                    "code": int(m_out.group(6)),
                    "timeout": int(m_out.group(7)),
                    "risk": int(m_out.group(8)),
                    "decel": int(m_out.group(9)),
                    "failSafe": int(m_out.group(10)),
                    "renderType": int(m_out.group(11)),
                    "renderCode": int(m_out.group(12)),
                }
            )

    return in_events, out_events


def pick_event_pair(scenario_id: int, in_events: Dict[int, List[int]], out_events: Dict[int, List[Dict[str, int]]]):
    inputs = in_events.get(scenario_id, [])
    outputs = out_events.get(scenario_id, [])
    if not inputs or not outputs:
        return None, None

    input_ts = max(inputs)
    output_event = None
    for cand in outputs:
        if cand["outputTsMs"] >= input_ts:
            output_event = cand
            break
    if output_event is None:
        output_event = outputs[-1]
    return input_ts, output_event


def build_observed(event: Dict[str, int]) -> str:
    return (
        f"level={event['level']},type={event['type']},code={event['code']},"
        f"timeout={event['timeout']},risk={event['risk']},decel={event['decel']},"
        f"failSafe={event['failSafe']},renderType={event['renderType']},renderCode={event['renderCode']}"
    )


def derive_comm_verdict(event: Dict[str, int]) -> str:
    if event["type"] == 0 and event["renderType"] == 0:
        return "PASS"
    if event["type"] == event["renderType"]:
        return "PASS"
    return "FAIL"


def main() -> int:
    args = parse_args()
    template_csv = Path(args.template_csv)
    raw_log = Path(args.raw_log)
    if not template_csv.exists():
        print(f"[FAIL] template csv not found: {template_csv}")
        return 2
    if not raw_log.exists():
        print(f"[FAIL] raw log not found: {raw_log}")
        return 2

    output_csv = Path(args.output_csv) if args.output_csv else template_csv.with_name(template_csv.stem + "_filled.csv")

    rows: List[Dict[str, str]] = []
    with template_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    raw_text = raw_log.read_text(encoding="utf-8", errors="ignore")
    in_events, out_events = parse_events(raw_text)

    updated = 0
    for row in rows:
        scenario_id = int((row.get("scenario_id") or "0").strip() or "0")
        in_ts, out_ev = pick_event_pair(scenario_id, in_events, out_events)
        if in_ts is None or out_ev is None:
            continue

        row["input_ts_ms"] = str(in_ts)
        row["output_ts_ms"] = str(out_ev["outputTsMs"])
        row["latency_ms"] = str(out_ev["outputTsMs"] - in_ts)
        row["observed"] = build_observed(out_ev)
        row["logic_verdict"] = "PASS" if out_ev["result"] == 1 else "FAIL"
        row["comm_verdict"] = derive_comm_verdict(out_ev)
        if args.owner and not (row.get("owner") or "").strip():
            row["owner"] = args.owner
        if args.run_date and not (row.get("run_date") or "").strip():
            row["run_date"] = args.run_date
        updated += 1

    fields = list(rows[0].keys()) if rows else []
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[EVIDENCE_FILL] rows={len(rows)} updated={updated} output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
