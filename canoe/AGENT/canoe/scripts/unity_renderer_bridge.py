#!/usr/bin/env python3
"""
CANoe -> Unity UI Render Bridge (UDP JSON)

Policy alignment:
- Logic/arbitration stays in CAPL nodes.
- Renderer receives derived outputs only (UiRender namespace).
"""

from __future__ import annotations

import argparse
import json
import signal
import socket
import sys
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import win32com.client  # type: ignore


UI_RENDER_FIELDS: List[str] = [
    "renderMode",
    "renderColor",
    "renderPattern",
    "renderTextCode",
    "renderDirection",
    "roadZoneColorCode",
    "roadFlowDirection",
    "vehicleObjectPos",
    "emsBlinkPhase",
    "ambientPulsePhase",
    "icFlowPhase",
    "activeAlertType",
]


@dataclass
class BridgeConfig:
    host: str
    port: int
    period_ms: int
    print_every: int


class CanoeSysVarReader:
    def __init__(self) -> None:
        self._app = None
        self._cache: Dict[Tuple[str, str], object] = {}

    def connect(self) -> None:
        self._app = win32com.client.Dispatch("CANoe.Application")
        print(f"[Bridge] Connected to CANoe: {self._app.Version}")

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

    def get_int(self, namespace: str, variable: str) -> int:
        var_obj = self._resolve_var(namespace, variable)
        return int(var_obj.Value)


def parse_args() -> BridgeConfig:
    parser = argparse.ArgumentParser(description="CANoe UiRender UDP bridge for Unity")
    parser.add_argument("--host", default="127.0.0.1", help="UDP target host")
    parser.add_argument("--port", type=int, default=7400, help="UDP target port")
    parser.add_argument(
        "--period-ms",
        type=int,
        default=50,
        help="Send period in milliseconds (recommended: 50/100)",
    )
    parser.add_argument(
        "--print-every",
        type=int,
        default=20,
        help="Print one status line every N packets",
    )
    args = parser.parse_args()
    return BridgeConfig(
        host=args.host,
        port=max(1, args.port),
        period_ms=max(10, args.period_ms),
        print_every=max(1, args.print_every),
    )


def build_payload(reader: CanoeSysVarReader, seq: int) -> Dict[str, object]:
    ui_render = {name: reader.get_int("UiRender", name) for name in UI_RENDER_FIELDS}
    return {
        "schema": "sdv.ui_render.v1",
        "seq": seq,
        "tsMs": int(time.time() * 1000),
        "uiRender": ui_render,
    }


def run(config: BridgeConfig) -> int:
    reader = CanoeSysVarReader()
    reader.connect()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = (config.host, config.port)
    period_s = config.period_ms / 1000.0
    seq = 0
    stop = {"value": False}

    def _on_sigint(_sig, _frame):
        stop["value"] = True

    signal.signal(signal.SIGINT, _on_sigint)
    print(
        f"[Bridge] start host={config.host} port={config.port} "
        f"period={config.period_ms}ms fields={len(UI_RENDER_FIELDS)}"
    )

    while not stop["value"]:
        payload = build_payload(reader, seq)
        data = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        sock.sendto(data, target)

        if seq % config.print_every == 0:
            print(
                f"[Bridge] seq={seq} mode={payload['uiRender']['renderMode']} "
                f"color={payload['uiRender']['renderColor']} "
                f"zone={payload['uiRender']['roadZoneColorCode']}"
            )

        seq += 1
        time.sleep(period_s)

    print("[Bridge] stopped")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run(parse_args()))
    except Exception as exc:
        print(f"[Bridge] error: {exc}")
        sys.exit(1)
