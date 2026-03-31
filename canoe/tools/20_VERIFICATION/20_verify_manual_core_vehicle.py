#!/usr/bin/env python3
"""Verify the manual core vehicle baseline from an active CANoe session.

Purpose:
- prove that the manual input panel still drives the owner ECU baseline car
- capture a reproducible PASS/FAIL snapshot for the core manual vehicle
- keep the check focused on vehicle fundamentals, not scenario harness logic

Scope:
- P/N/D/R selector behavior
- throttle / brake
- steering extremes
- cruise set / engage
- ambient body command

Safety:
- requires an already running CANoe instance with the intended cfg open
- writes only manual command sysvars
- stores local evidence under ``canoe/tmp/manual_core_vehicle_smoke/``
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import pythoncom  # type: ignore
import win32com.client  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "canoe" / "tmp" / "manual_core_vehicle_smoke"

CMD_DEFAULTS: Dict[str, int] = {
    "Cmd::ignitionOn": 0,
    "Cmd::driveStateCmd": 0,
    "Cmd::vehicleSpeedCmd": 0,
    "Cmd::throttlePedalPct": 0,
    "Cmd::brakePedalPct": 0,
    "Cmd::steeringAngleCmd": 0,
    "Cmd::cruiseStateCmd": 0,
    "Cmd::cruiseSetSpeedCmd": 0,
    "Body::ambientMode": 0,
    "Cmd::doorLockCmd": 0,
    "Cmd::doorOpenCmd": 0,
    "Cmd::windowCmd": 0,
    "Cmd::wiperCmd": 0,
    "Cmd::turnSignalCmd": 0,
}

CORE_READ_VARS: List[str] = [
    "Chassis::driveState",
    "Chassis::vehicleSpeed",
    "Chassis::throttlePosition",
    "Chassis::brakePressure",
    "Chassis::steeringAngle",
    "Display::steeringFrame",
    "Display::animFrame",
    "Powertrain::cruiseSetSpeed",
    "Body::ambientMode",
    "Body::windowPos",
    "Body::frontWiperAnimFrame",
    "CoreState::turnLampState",
    "CoreState::driveMode",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the manual core vehicle baseline from an active CANoe session."
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

        self._app = win32com.client.Dispatch("CANoe.Application")

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

    def get_int(self, fq_name: str) -> int:
        namespace, variable = fq_name.split("::", 1)
        var_obj = self._resolve_var(namespace, variable)
        return int(var_obj.Value)

    def set_int(self, fq_name: str, value: int) -> None:
        namespace, variable = fq_name.split("::", 1)
        var_obj = self._resolve_var(namespace, variable)
        var_obj.Value = int(value)


def apply_cmds(client: CanoeSysVarClient, overrides: Dict[str, int], wait_ms: int = 400) -> None:
    merged = dict(CMD_DEFAULTS)
    merged.update(overrides)
    for fq_name, value in merged.items():
        client.set_int(fq_name, value)
    time.sleep(wait_ms / 1000.0)


def sample_core(client: CanoeSysVarClient) -> Dict[str, int]:
    return {fq_name: client.get_int(fq_name) for fq_name in CORE_READ_VARS}


def hard_stop(client: CanoeSysVarClient, timeout_s: float = 4.0) -> None:
    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 0, "Cmd::brakePedalPct": 100}, 100)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if client.get_int("Chassis::vehicleSpeed") == 0:
            break
        time.sleep(0.1)
    apply_cmds(client, {}, 300)


def build_step(name: str, data: Dict[str, int], passed: bool, expectation: str) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "expectation": expectation,
        "values": data,
    }


def main() -> int:
    args = parse_args()

    client = CanoeSysVarClient()
    client.connect_active()

    if not client.config_path:
        raise RuntimeError("CANoe cfg is not loaded.")
    if not client.measurement_running:
        raise RuntimeError("CANoe measurement is not running. Start measurement first.")

    steps: List[Dict[str, Any]] = []

    hard_stop(client)
    baseline = sample_core(client)
    steps.append(
        build_step(
            "baseline_idle",
            baseline,
            baseline["Chassis::driveState"] == 0
            and baseline["Chassis::vehicleSpeed"] == 0
            and baseline["Display::steeringFrame"] == 35,
            "P idle must remain driveState=0, vehicleSpeed=0, and steeringFrame centered",
        )
    )

    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 3, "Cmd::throttlePedalPct": 100}, 3600)
    d_full = sample_core(client)
    steps.append(
        build_step(
            "drive_full_throttle",
            d_full,
            d_full["Chassis::driveState"] == 3
            and d_full["Chassis::throttlePosition"] == 100
            and d_full["Chassis::vehicleSpeed"] >= 100
            and d_full["Display::animFrame"] > 0,
            "D + throttle100 should reach driveState=3, throttlePosition=100, vehicleSpeed>=100, and animFrame>0 within the baseline acceleration window",
        )
    )

    apply_cmds(
        client,
        {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 3, "Cmd::throttlePedalPct": 0, "Cmd::brakePedalPct": 100},
        2400,
    )
    d_brake = sample_core(client)
    steps.append(
        build_step(
            "drive_full_brake",
            d_brake,
            d_brake["Chassis::driveState"] == 3
            and d_brake["Chassis::vehicleSpeed"] == 0
            and d_brake["Chassis::brakePressure"] == 100,
            "D + brake100 should stop the car within the baseline brake ramp window and drive brakePressure=100",
        )
    )

    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 2, "Cmd::throttlePedalPct": 40}, 1500)
    neutral = sample_core(client)
    steps.append(
        build_step(
            "neutral_blocks_propulsion",
            neutral,
            neutral["Chassis::driveState"] == 2 and neutral["Chassis::vehicleSpeed"] == 0,
            "N + throttle must keep vehicleSpeed=0",
        )
    )

    hard_stop(client)
    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 1, "Cmd::throttlePedalPct": 100}, 2000)
    reverse = sample_core(client)
    steps.append(
        build_step(
            "reverse_low_speed_motion",
            reverse,
            reverse["Chassis::driveState"] == 1 and 10 <= reverse["Chassis::vehicleSpeed"] <= 40,
            "R + throttle100 should move in the reverse speed band",
        )
    )

    hard_stop(client)
    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 3, "Cmd::steeringAngleCmd": -540}, 500)
    steer_left = sample_core(client)
    steps.append(
        build_step(
            "steering_left_extreme",
            steer_left,
            steer_left["Chassis::steeringAngle"] == 0 and steer_left["Display::steeringFrame"] == 0,
            "Steering -540 should map to the left legacy extreme and steeringFrame=0",
        )
    )

    apply_cmds(client, {"Cmd::ignitionOn": 1, "Cmd::driveStateCmd": 3, "Cmd::steeringAngleCmd": 540}, 500)
    steer_right = sample_core(client)
    steps.append(
        build_step(
            "steering_right_extreme",
            steer_right,
            steer_right["Chassis::steeringAngle"] == 138 and steer_right["Display::steeringFrame"] == 69,
            "Steering +540 should map to the right legacy extreme and steeringFrame=69",
        )
    )

    hard_stop(client)
    apply_cmds(
        client,
        {
            "Cmd::ignitionOn": 1,
            "Cmd::driveStateCmd": 3,
            "Cmd::cruiseStateCmd": 1,
            "Cmd::cruiseSetSpeedCmd": 50,
        },
        3400,
    )
    cruise = sample_core(client)
    steps.append(
        build_step(
            "manual_cruise_enable",
            cruise,
            cruise["Powertrain::cruiseSetSpeed"] == 50 and cruise["Chassis::vehicleSpeed"] >= 20,
            "Cruise ON + set 50 should latch cruiseSetSpeed=50 and move speed upward within the baseline cruise ramp window",
        )
    )

    hard_stop(client)
    apply_cmds(client, {"Body::ambientMode": 3}, 500)
    ambient = sample_core(client)
    steps.append(
        build_step(
            "ambient_manual_apply",
            ambient,
            ambient["Body::ambientMode"] == 3,
            "Body::ambientMode=3 should remain reflected at owner output",
        )
    )

    hard_stop(client)
    apply_cmds(
        client,
        {
            "Cmd::ignitionOn": 1,
            "Cmd::driveStateCmd": 0,
            "Cmd::doorLockCmd": 1,
            "Cmd::doorOpenCmd": 1,
        },
        600,
    )
    door_open = sample_core(client)
    steps.append(
        build_step(
            "door_unlock_open_standstill",
            door_open,
            door_open["Chassis::driveState"] == 0 and door_open["Body::windowPos"] >= 20,
            "Door unlock/open at standstill should trigger the manual open path and lift windowPos to the open threshold",
        )
    )

    apply_cmds(
        client,
        {
            "Cmd::ignitionOn": 1,
            "Cmd::driveStateCmd": 0,
            "Cmd::windowCmd": 2,
        },
        600,
    )
    window_down = sample_core(client)
    steps.append(
        build_step(
            "window_down_manual",
            window_down,
            window_down["Body::windowPos"] >= 10,
            "Window down command should increase the manual window position",
        )
    )

    hard_stop(client)
    apply_cmds(
        client,
        {
            "Cmd::ignitionOn": 1,
            "Cmd::turnSignalCmd": 2,
        },
        500,
    )
    turn_right = sample_core(client)
    steps.append(
        build_step(
            "turn_right_manual",
            turn_right,
            turn_right["CoreState::turnLampState"] == 2,
            "Right turn command should reflect to turnLampState=2",
        )
    )

    apply_cmds(
        client,
        {
            "Cmd::ignitionOn": 1,
            "Cmd::wiperCmd": 1,
        },
        800,
    )
    wiper_int = sample_core(client)
    steps.append(
        build_step(
            "wiper_int_manual",
            wiper_int,
            wiper_int["Body::frontWiperAnimFrame"] > 0,
            "Intermittent wiper command should advance the front wiper animation frame",
        )
    )

    overall_pass = all(step["passed"] for step in steps)

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    label = f"_{args.label}" if args.label else ""
    output_dir = Path(args.output_root) / f"{timestamp}_manual_core_vehicle{label}"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "config_path": client.config_path,
        "measurement_running": client.measurement_running,
        "overall_pass": overall_pass,
        "step_count": len(steps),
        "steps": steps,
    }

    (output_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "README.txt").write_text(
        "\n".join(
            [
                "Manual core vehicle smoke result",
                f"overall_pass={overall_pass}",
                f"steps={len(steps)}",
                f"config={client.config_path}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if overall_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
