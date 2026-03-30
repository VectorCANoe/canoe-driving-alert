#!/usr/bin/env python3
"""Capture runtime coupling probes from an active CANoe session.

Purpose:
- move from static code suspicion to reproducible runtime evidence
- trigger known scenario paths when requested
- sample key sysvars for alert/body/access/brake coupling clusters
- write local evidence under ``canoe/tmp/runtime_probes/``

Safety:
- requires an already running CANoe instance with the intended cfg open
- does not open/save cfg files
- only writes one-shot scenario/sysvar inputs when explicitly requested
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple

import pythoncom  # type: ignore
import win32com.client  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "canoe" / "tmp" / "runtime_probes"

PROFILE_VARS: Dict[str, List[str]] = {
    "alert": [
        "Test::scenarioActiveId",
        "Test::scenarioCommandAck",
        "CoreState::selectedAlertDecisionLevel",
        "CoreState::selectedAlertDecisionType",
        "CoreState::selectedAlertEffectiveLevel",
        "CoreState::selectedAlertEffectiveType",
        "CoreState::selectedAlertGateReason",
        "CoreState::duplicatePopupGuard",
        "Cluster::warningTextCode",
        "Body::ambientMode",
    ],
    "body": [
        "Test::scenarioActiveId",
        "Cmd::ambientModeCmd",
        "Cmd::doorLockCmd",
        "Cmd::doorOpenCmd",
        "CoreState::selectedAlertEffectiveLevel",
        "CoreState::selectedAlertEffectiveType",
        "CoreState::turnLampState",
        "Body::ambientMode",
        "Test::driverBeltOff",
        "Test::passengerBeltOff",
        "Test::seatBeltOverride",
    ],
    "access": [
        "Test::scenarioActiveId",
        "Cmd::doorLockCmd",
        "Cmd::doorOpenCmd",
        "CoreState::turnLampState",
        "CoreState::selectedAlertEffectiveLevel",
        "CoreState::selectedAlertEffectiveType",
        "CoreState::selectedAlertGateReason",
        "Body::ambientMode",
        "Test::driverBeltOff",
        "Test::passengerBeltOff",
        "Test::seatBeltOverride",
    ],
    "brake": [
        "Test::scenarioActiveId",
        "Chassis::vehicleSpeed",
        "Chassis::brakePressure",
        "Chassis::throttlePosition",
        "CoreState::selectedAlertEffectiveLevel",
        "CoreState::selectedAlertEffectiveType",
        "CoreState::selectedAlertGateReason",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture runtime coupling evidence from an active CANoe session."
    )
    parser.add_argument(
        "--profile",
        choices=["alert", "body", "access", "brake", "all"],
        default="all",
        help="Named variable set to capture. Default: all.",
    )
    parser.add_argument(
        "--scenario-id",
        type=int,
        default=None,
        help="Optional scenarioCommand id to trigger before sampling.",
    )
    parser.add_argument(
        "--await-ms",
        type=int,
        default=4000,
        help="Max wait for scenario ack/active after trigger. Default: 4000.",
    )
    parser.add_argument(
        "--settle-ms",
        type=int,
        default=300,
        help="Extra wait after trigger settles. Default: 300.",
    )
    parser.add_argument(
        "--duration-ms",
        type=int,
        default=5000,
        help="Sampling duration after settle. Default: 5000.",
    )
    parser.add_argument(
        "--interval-ms",
        type=int,
        default=200,
        help="Sampling interval. Default: 200.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help=f"Output directory root. Default: {DEFAULT_OUTPUT_ROOT}",
    )
    parser.add_argument(
        "--label",
        default="",
        help="Optional label suffix for the output directory.",
    )
    parser.add_argument(
        "--custom-var",
        action="append",
        default=[],
        help="Extra Namespace::Variable to include. Repeatable.",
    )
    parser.add_argument(
        "--stop-scenario-after",
        action="store_true",
        help="Pulse Test::scenarioStopReq after capture when scenario-id was used.",
    )
    parser.add_argument(
        "--print-vars",
        action="store_true",
        help="Print the final capture variable list and exit.",
    )
    return parser.parse_args()


class CanoeSysVarClient:
    def __init__(self) -> None:
        self._app = None
        self._cache: Dict[Tuple[str, str], Any] = {}

    def connect_active(self) -> None:
        pythoncom.CoInitialize()
        try:
            self._app = pythoncom.GetActiveObject("CANoe.Application")
            return
        except Exception:
            pass

        try:
            self._app = win32com.client.Dispatch("CANoe.Application")
        except Exception as exc:  # pragma: no cover - runtime environment dependent
            raise RuntimeError(
                "CANoe automation session not found. Open the intended cfg in CANoe first."
            ) from exc

        try:
            config_path = str(self._app.Configuration.FullName)
        except Exception as exc:  # pragma: no cover - runtime environment dependent
            raise RuntimeError("CANoe automation session has no readable configuration.") from exc

        if not config_path:
            raise RuntimeError(
                "CANoe opened through automation has no cfg loaded. Open the intended cfg in CANoe first."
            )

    @property
    def version(self) -> str:
        return str(self._app.Version)

    @property
    def config_path(self) -> str:
        return str(self._app.Configuration.FullName)

    @property
    def measurement_running(self) -> bool:
        return bool(self._app.Measurement.Running)

    def _resolve_var(self, namespace: str, variable: str):
        key = (namespace, variable)
        if key in self._cache:
            return self._cache[key]

        attempts: List[Callable[[], Any]] = [
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

    def get_value(self, fq_name: str) -> Any:
        namespace, variable = parse_fq_var(fq_name)
        var_obj = self._resolve_var(namespace, variable)
        value = var_obj.Value
        try:
            return int(value)
        except Exception:
            try:
                return float(value)
            except Exception:
                return str(value)

    def set_int(self, fq_name: str, value: int) -> None:
        namespace, variable = parse_fq_var(fq_name)
        var_obj = self._resolve_var(namespace, variable)
        var_obj.Value = int(value)


def parse_fq_var(fq_name: str) -> Tuple[str, str]:
    if "::" not in fq_name:
        raise ValueError(f"Expected Namespace::Variable form, got: {fq_name}")
    namespace, variable = fq_name.split("::", 1)
    return namespace, variable


def dedupe(items: Iterable[str]) -> List[str]:
    seen: set[str] = set()
    ordered: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def build_var_list(profile: str, extra_vars: Sequence[str]) -> List[str]:
    if profile == "all":
        vars_list: List[str] = []
        for key in ("alert", "body", "access", "brake"):
            vars_list.extend(PROFILE_VARS[key])
    else:
        vars_list = list(PROFILE_VARS[profile])
    vars_list.extend(extra_vars)
    return dedupe(vars_list)


def wait_for_scenario(
    client: CanoeSysVarClient,
    scenario_id: int,
    await_ms: int,
) -> Dict[str, Any]:
    deadline = time.time() + (await_ms / 1000.0)
    state: Dict[str, Any] = {
        "requested": scenario_id,
        "ack": None,
        "active": None,
        "accepted": False,
    }
    while time.time() < deadline:
        ack = client.get_value("Test::scenarioCommandAck")
        active = client.get_value("Test::scenarioActiveId")
        state["ack"] = ack
        state["active"] = active
        if int(ack) == scenario_id or int(active) == scenario_id:
            state["accepted"] = True
            return state
        time.sleep(0.05)
    return state


def wait_for_exact_value(
    client: CanoeSysVarClient,
    fq_name: str,
    expected: int,
    await_ms: int,
) -> bool:
    deadline = time.time() + (await_ms / 1000.0)
    while time.time() < deadline:
        if int(client.get_value(fq_name)) == expected:
            return True
        time.sleep(0.05)
    return False


def sample_vars(
    client: CanoeSysVarClient,
    vars_list: Sequence[str],
    duration_ms: int,
    interval_ms: int,
) -> List[Dict[str, Any]]:
    start = time.time()
    end = start + (duration_ms / 1000.0)
    samples: List[Dict[str, Any]] = []

    while True:
        now = time.time()
        row: Dict[str, Any] = {
            "utc_iso": dt.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "relative_ms": int((now - start) * 1000.0),
        }
        for fq_name in vars_list:
            row[fq_name] = client.get_value(fq_name)
        samples.append(row)
        if now >= end:
            break
        time.sleep(max(interval_ms, 20) / 1000.0)

    return samples


def write_csv(path: Path, rows: Sequence[Dict[str, Any]], vars_list: Sequence[str]) -> None:
    fieldnames = ["utc_iso", "relative_ms", *vars_list]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    vars_list = build_var_list(args.profile, args.custom_var)

    if args.print_vars:
        print("\n".join(vars_list))
        return 0

    client = CanoeSysVarClient()
    client.connect_active()

    if not client.measurement_running:
        raise RuntimeError("CANoe measurement is not running. Start measurement first.")

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    label = f"_{args.label}" if args.label else ""
    scenario_slug = f"_scn{args.scenario_id}" if args.scenario_id is not None else ""
    run_slug = f"{timestamp}_{args.profile}{scenario_slug}{label}"

    output_root = Path(args.output_root)
    output_dir = output_root / run_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = {fq_name: client.get_value(fq_name) for fq_name in vars_list}
    scenario_state: Dict[str, Any] | None = None

    if args.scenario_id is not None:
        if int(client.get_value("Test::scenarioActiveId")) != 0:
            client.set_int("Test::scenarioStopReq", 1)
            wait_for_exact_value(client, "Test::scenarioActiveId", 0, args.await_ms)
            time.sleep(0.2)

        client.set_int("Test::scenarioCommand", args.scenario_id)
        scenario_state = wait_for_scenario(client, args.scenario_id, args.await_ms)
        time.sleep(max(args.settle_ms, 0) / 1000.0)

    samples = sample_vars(client, vars_list, args.duration_ms, args.interval_ms)

    if args.stop_scenario_after and args.scenario_id is not None:
        client.set_int("Test::scenarioStopReq", 1)

    summary: Dict[str, Any] = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "profile": args.profile,
        "config_path": client.config_path,
        "canoe_version": client.version,
        "measurement_running": client.measurement_running,
        "scenario_id": args.scenario_id,
        "scenario_state": scenario_state,
        "duration_ms": args.duration_ms,
        "interval_ms": args.interval_ms,
        "variables": vars_list,
        "baseline": baseline,
        "sample_count": len(samples),
        "samples": samples,
    }

    json_path = output_dir / "probe.json"
    csv_path = output_dir / "probe.csv"
    meta_path = output_dir / "README.txt"

    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv(csv_path, samples, vars_list)
    meta_path.write_text(
        "\n".join(
            [
                f"profile={args.profile}",
                f"scenario_id={args.scenario_id}",
                f"config_path={client.config_path}",
                f"json={json_path}",
                f"csv={csv_path}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"[probe] output_dir={output_dir}")
    print(f"[probe] sample_count={len(samples)}")
    if scenario_state is not None:
        print(
            "[probe] scenario accepted="
            f"{scenario_state['accepted']} ack={scenario_state['ack']} active={scenario_state['active']}"
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover - runtime environment dependent
        print(f"[probe] error: {exc}")
        sys.exit(1)
