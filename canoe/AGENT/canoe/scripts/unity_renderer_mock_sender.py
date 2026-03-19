#!/usr/bin/env python3
"""
Mock sender for Unity renderer integration testing.

Use this when CANoe is not running yet.
It emits the same UDP packet schema as unity_renderer_bridge.py.
"""

from __future__ import annotations

import argparse
import json
import socket
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mock UiRender UDP packet sender")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7400)
    parser.add_argument("--period-ms", type=int, default=50)
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = (args.host, args.port)
    period_s = max(0.01, args.period_ms / 1000.0)
    seq = 0

    print(
        f"[MOCK] start host={args.host} port={args.port} period={args.period_ms}ms"
    )

    while True:
        packet = {
            "schema": "sdv.ui_render.v1",
            "seq": seq,
            "tsMs": int(time.time() * 1000),
            "uiRender": {
                "renderMode": seq % 4,
                "renderColor": seq % 4,
                "renderPattern": seq % 8,
                "renderTextCode": 100 + (seq % 8),
                "renderDirection": seq % 4,
                "roadZoneColorCode": seq % 4,
                "roadFlowDirection": seq % 3,
                "vehicleObjectPos": seq % 101,
                "emsBlinkPhase": seq % 2,
                "ambientPulsePhase": seq % 4,
                "icFlowPhase": seq % 8,
                "activeAlertType": seq % 3,
            },
        }
        data = json.dumps(packet, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        sock.sendto(data, target)

        if seq % 20 == 0:
            print(
                f"[MOCK] seq={seq} zone={packet['uiRender']['roadZoneColorCode']} "
                f"pos={packet['uiRender']['vehicleObjectPos']}"
            )

        seq += 1
        time.sleep(period_s)


if __name__ == "__main__":
    run()
