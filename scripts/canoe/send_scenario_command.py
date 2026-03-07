#!/usr/bin/env python3
"""Send scenario command sysvar to running CANoe via COM.

Primary use:
- trigger validation scenarios without panel UI.
"""

from __future__ import annotations

import argparse
import time


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send Test sysvar scenario command to CANoe")
    parser.add_argument("--id", type=int, required=True, help="Scenario ID (0..255)")
    parser.add_argument("--namespace", default="Test", help="System variable namespace")
    parser.add_argument(
        "--var",
        default="scenarioCommand",
        choices=["scenarioCommand", "testScenario"],
        help="Target sysvar name",
    )
    parser.add_argument("--ack-var", default="scenarioCommandAck", help="Ack sysvar name")
    parser.add_argument(
        "--wait-ack-ms",
        type=int,
        default=1200,
        help="Wait timeout for ack observation in ms (scenarioCommand mode)",
    )
    parser.add_argument("--poll-ms", type=int, default=20, help="Ack polling interval in ms")
    parser.add_argument(
        "--no-ensure-running",
        action="store_true",
        help="Do not auto-start measurement when stopped",
    )
    return parser


def _resolve_var(app, namespace: str, variable: str):
    attempts = [
        lambda: app.System.Namespaces(namespace).Variables(variable),
        lambda: app.System.Namespaces(namespace).Variables.Item(variable),
        lambda: app.System.Namespaces.Item(namespace).Variables(variable),
        lambda: app.System.Namespaces.Item(namespace).Variables.Item(variable),
        lambda: app.Configuration.SystemVariables.Namespaces(namespace).Variables(variable),
        lambda: app.Configuration.SystemVariables.Namespaces(namespace).Variables.Item(variable),
    ]
    for attempt in attempts:
        try:
            return attempt()
        except Exception:
            continue
    raise RuntimeError(f"System variable not found: {namespace}::{variable}")


def main() -> int:
    args = build_parser().parse_args()

    if not (0 <= args.id <= 255):
        print("[SCENARIO] FAIL: --id must be in range 0..255")
        return 2

    try:
        import win32com.client  # type: ignore
    except Exception:
        print("[SCENARIO] FAIL: pywin32 (win32com.client) is required")
        return 2

    try:
        app = win32com.client.Dispatch("CANoe.Application")
    except Exception as ex:
        print(f"[SCENARIO] FAIL: cannot attach CANoe COM: {ex}")
        print("[SCENARIO] hint: run terminal with same privilege/session as CANoe")
        return 2

    try:
        if not args.no_ensure_running and not app.Measurement.Running:
            app.Measurement.Start()
            time.sleep(0.4)

        target = _resolve_var(app, args.namespace, args.var)

        ack_obj = None
        if args.var == "scenarioCommand":
            try:
                ack_obj = _resolve_var(app, args.namespace, args.ack_var)
            except Exception:
                ack_obj = None

        target.Value = int(args.id)
        print(f"[SCENARIO] sent {args.namespace}::{args.var}={args.id}")

        if ack_obj is None:
            return 0

        deadline = time.perf_counter() + max(0, args.wait_ack_ms) / 1000.0
        poll_s = max(0.005, args.poll_ms / 1000.0)

        while time.perf_counter() <= deadline:
            try:
                ack_value = int(ack_obj.Value)
            except Exception:
                ack_value = -1
            if ack_value == args.id:
                print(f"[SCENARIO] ack {args.namespace}::{args.ack_var}={ack_value} (PASS)")
                return 0
            time.sleep(poll_s)

        try:
            final_ack = int(ack_obj.Value)
        except Exception:
            final_ack = -1
        print(
            f"[SCENARIO] WARN: ack timeout ({args.wait_ack_ms}ms), "
            f"last {args.namespace}::{args.ack_var}={final_ack}"
        )
        return 3

    except Exception as ex:
        print(f"[SCENARIO] FAIL: {ex}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
