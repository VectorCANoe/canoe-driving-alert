#!/usr/bin/env python3
"""Development completeness smoke check for CANoe SIL.

Checks key runtime path updates before formal UT/IT/ST evidence runs:
Core -> Body -> Cluster -> UiRender
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import win32com.client  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[2]


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


@dataclass(frozen=True)
class SmokeCase:
    tier: str
    test_id: str
    scenario_id: int
    rule_type: str
    rule_ms: str
    timeout_ms: int
    expected: str


CASES: List[SmokeCase] = [
    SmokeCase(
        tier="IT",
        test_id="SMOKE_CORE_PATH_004",
        scenario_id=4,
        rule_type="LE",
        rule_ms="150",
        timeout_ms=2000,
        expected="Emergency scenario propagates Core->Body/Cluster->UiRender",
    ),
    SmokeCase(
        tier="ST",
        test_id="SMOKE_TIMEOUT_006",
        scenario_id=6,
        rule_type="BETWEEN",
        rule_ms="1000:1300",
        timeout_ms=2200,
        expected="Timeout clear asserted after no emergency update",
    ),
    SmokeCase(
        tier="ST",
        test_id="SMOKE_FAILSAFE_018",
        scenario_id=18,
        rule_type="LE",
        rule_ms="150",
        timeout_ms=1200,
        expected="Fail-safe mode blocks decel assist",
    ),
]


class CanoeSysVarClient:
    def __init__(self) -> None:
        self._app = None
        self._cache: Dict[Tuple[str, str], object] = {}

    def connect(self) -> None:
        try:
            self._app = win32com.client.Dispatch("CANoe.Application")
        except Exception as ex:
            raise RuntimeError(
                "Failed to attach CANoe COM. "
                "Run this script in the same Windows user session/privilege as CANoe "
                "(both normal user or both administrator)."
            ) from ex

    def ensure_measurement_running(self) -> None:
        if not self._app.Measurement.Running:
            self._app.Measurement.Start()
            time.sleep(0.6)

    def _resolve_var(self, namespace: str, variable: str):
        key = (namespace, variable)
        if key in self._cache:
            return self._cache[key]

        attempts: List[Callable[[], object]] = [
            lambda: self._app.System.Namespaces(namespace).Variables(variable),
            lambda: self._app.System.Namespaces(namespace).Variables.Item(variable),
            lambda: self._app.System.Namespaces.Item(namespace).Variables(variable),
            lambda: self._app.System.Namespaces.Item(namespace).Variables.Item(variable),
            lambda: self._app.Configuration.SystemVariables.Namespaces(namespace).Variables(variable),
            lambda: self._app.Configuration.SystemVariables.Namespaces(namespace).Variables.Item(variable),
        ]

        for attempt in attempts:
            try:
                var_obj = attempt()
                self._cache[key] = var_obj
                return var_obj
            except Exception:
                continue

        raise RuntimeError(f"System variable not found: {namespace}::{variable}")

    def set_int(self, namespace: str, variable: str, value: int) -> None:
        self._resolve_var(namespace, variable).Value = int(value)

    def get_int(self, namespace: str, variable: str) -> int:
        return int(self._resolve_var(namespace, variable).Value)

    def has_var(self, namespace: str, variable: str) -> bool:
        try:
            self._resolve_var(namespace, variable)
            return True
        except Exception:
            return False

    def trigger_scenario(self, scenario_id: int, *, ack_wait_ms: int = 1200, poll_s: float = 0.02) -> str:
        candidates = [
            ("scenarioCommand", "scenarioCommandAck"),
            ("testScenario", None),
        ]

        for var_name, ack_name in candidates:
            if not self.has_var("Test", var_name):
                continue

            self.set_int("Test", var_name, 0)
            time.sleep(0.15)
            self.set_int("Test", var_name, scenario_id)

            if not ack_name or not self.has_var("Test", ack_name):
                return var_name

            deadline = time.perf_counter() + max(0, ack_wait_ms) / 1000.0
            while time.perf_counter() <= deadline:
                if self.get_int("Test", ack_name) == scenario_id:
                    return f"{var_name}/{ack_name}"
                time.sleep(poll_s)

            return f"{var_name} (ack-timeout)"

        raise RuntimeError("No usable scenario trigger sysvar found in Test namespace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run development completeness smoke checks")
    parser.add_argument(
        "--owner",
        default="TBD",
        help="Owner name recorded in output CSV",
    )
    parser.add_argument(
        "--run-date",
        default=dt.date.today().isoformat(),
        help="Run date in YYYY-MM-DD",
    )
    parser.add_argument(
        "--output-csv",
        default="canoe/tmp/reports/verification/dev_completeness_smoke.csv",
        help="CSV output path",
    )
    parser.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/dev_completeness_smoke.md",
        help="Markdown output path",
    )
    parser.add_argument(
        "--poll-ms",
        type=int,
        default=20,
        help="Polling interval in ms",
    )
    parser.add_argument(
        "--raw-log-path",
        default="canoe/logging/evidence/ST/<run_id>/raw_write_window.txt",
        help="Reference raw log path stored in CSV rows",
    )
    parser.add_argument(
        "--capture-path",
        default="canoe/logging/evidence/ST/<run_id>/captures/",
        help="Reference capture path stored in CSV rows",
    )
    return parser.parse_args()


def snapshot(client: CanoeSysVarClient) -> Dict[str, int]:
    return {
        "core_level": client.get_int("Core", "selectedAlertLevel"),
        "core_type": client.get_int("Core", "selectedAlertType"),
        "timeout_clear": client.get_int("Core", "timeoutClear"),
        "risk": client.get_int("Core", "proximityRiskLevel"),
        "decel": client.get_int("Core", "decelAssistReq"),
        "failsafe": client.get_int("Core", "failSafeMode"),
        "body_color": client.get_int("Body", "ambientColor"),
        "body_pattern": client.get_int("Body", "ambientPattern"),
        "cluster_code": client.get_int("Cluster", "warningTextCode"),
        "ui_color": client.get_int("UiRender", "renderColor"),
        "ui_text": client.get_int("UiRender", "renderTextCode"),
        "ui_alert_type": client.get_int("UiRender", "activeAlertType"),
    }


def evaluate_core(case: SmokeCase, data: Dict[str, int]) -> bool:
    if case.scenario_id == 4:
        return data["core_level"] >= 6 and data["core_type"] in {1, 2}
    if case.scenario_id == 6:
        return data["timeout_clear"] == 1 and data["core_level"] == 0
    if case.scenario_id == 18:
        return data["failsafe"] >= 1 and data["decel"] == 0
    return False


def evaluate_comm(case: SmokeCase, data: Dict[str, int]) -> bool:
    if case.scenario_id == 4:
        return (
            data["body_color"] in {6, 7}
            and data["cluster_code"] >= 100
            and data["ui_alert_type"] == data["core_type"]
            and data["ui_color"] == data["body_color"]
        )
    if case.scenario_id == 6:
        return data["cluster_code"] == 0 and data["ui_text"] == 0
    if case.scenario_id == 18:
        return data["cluster_code"] >= 100 and data["ui_text"] >= 100
    return False


def observed_text(data: Dict[str, int]) -> str:
    return (
        f"level={data['core_level']},type={data['core_type']},timeout={data['timeout_clear']},"
        f"risk={data['risk']},decel={data['decel']},failsafe={data['failsafe']},"
        f"bodyColor={data['body_color']},clusterCode={data['cluster_code']},"
        f"uiColor={data['ui_color']},uiText={data['ui_text']},uiType={data['ui_alert_type']}"
    )


def run_case(client: CanoeSysVarClient, case: SmokeCase, poll_s: float) -> Dict[str, str]:
    trigger_mode = client.trigger_scenario(case.scenario_id, poll_s=poll_s)

    start = time.perf_counter()
    timeout_s = case.timeout_ms / 1000.0
    last = snapshot(client)
    logic_pass = evaluate_core(case, last)
    comm_pass = evaluate_comm(case, last)
    matched = logic_pass and comm_pass
    output_ms = ""

    while (time.perf_counter() - start) <= timeout_s:
        last = snapshot(client)
        logic_pass = evaluate_core(case, last)
        comm_pass = evaluate_comm(case, last)
        matched = logic_pass and comm_pass
        if matched:
            output_ms = str(int((time.perf_counter() - start) * 1000))
            break
        time.sleep(poll_s)

    return {
        "tier": case.tier,
        "test_id": case.test_id,
        "scenario_id": str(case.scenario_id),
        "input_ts_ms": "0",
        "output_ts_ms": output_ms,
        "latency_ms": "",
        "rule_type": case.rule_type,
        "rule_ms": case.rule_ms,
        "expected": case.expected,
        "observed": f"trigger={trigger_mode}; {observed_text(last)}",
        "logic_verdict": "PASS" if logic_pass else "FAIL",
        "comm_verdict": "PASS" if comm_pass else "FAIL",
        "verdict": "PASS" if matched else "FAIL",
    }


def write_outputs(rows: List[Dict[str, str]], args: argparse.Namespace) -> None:
    output_csv = _repo_path(Path(args.output_csv))
    output_md = _repo_path(Path(args.output_md))
    raw_log_path = _rel(_repo_path(Path(args.raw_log_path))) if args.raw_log_path else ""
    capture_path = _rel(_repo_path(Path(args.capture_path))) if args.capture_path else ""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    fields = [
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
        "note",
    ]

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["owner"] = args.owner
            out["run_date"] = args.run_date
            out["evidence_log_path"] = raw_log_path
            out["evidence_capture_path"] = capture_path
            out["note"] = "dev completeness smoke check"
            writer.writerow(out)

    total = len(rows)
    logic_pass = sum(1 for r in rows if r["logic_verdict"] == "PASS")
    comm_pass = sum(1 for r in rows if r["comm_verdict"] == "PASS")
    overall_pass = sum(1 for r in rows if r["verdict"] == "PASS")

    lines = [
        "# Dev Completeness Smoke Report",
        "",
        f"- Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Rows: {total}",
        f"- Logic PASS: {logic_pass}/{total}",
        f"- Comm PASS: {comm_pass}/{total}",
        f"- Overall PASS: {overall_pass}/{total}",
        "",
        "| test_id | scenario_id | logic | comm | overall | output_ts_ms |",
        "| --- | ---: | --- | --- | --- | ---: |",
    ]

    for row in rows:
        lines.append(
            f"| {row['test_id']} | {row['scenario_id']} | {row['logic_verdict']} | "
            f"{row['comm_verdict']} | {row['verdict']} | {row['output_ts_ms'] or '-'} |"
        )

    lines += [
        "",
        "## Output",
        f"- CSV: `{_rel(output_csv)}`",
        f"- MD: `{_rel(output_md)}`",
    ]
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    poll_s = max(0.01, args.poll_ms / 1000.0)

    client = CanoeSysVarClient()
    try:
        client.connect()
        client.ensure_measurement_running()
    except Exception as ex:
        print(f"[SMOKE][FAIL] {ex}")
        return 2

    rows: List[Dict[str, str]] = []
    for case in CASES:
        rows.append(run_case(client, case, poll_s=poll_s))

    write_outputs(rows, args)
    print(f"[SMOKE] rows={len(rows)} output_csv={_rel(_repo_path(Path(args.output_csv)))} output_md={_rel(_repo_path(Path(args.output_md)))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
