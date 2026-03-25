#!/usr/bin/env python3
"""
Navigation Simulator (Option B)

- Grid map (N x M) based road context generation
- Vehicle (x, y) movement simulation
- CANoe COM API system-variable injection

Renderer/logic split policy:
- CAPL keeps warning/arbitration decisions.
- This script provides navigation/chassis input stimuli only.
"""

from __future__ import annotations

import argparse
import random
import signal
import sys
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import win32com.client  # type: ignore


ZONE_NORMAL = 0
ZONE_SCHOOL = 1
ZONE_HIGHWAY = 2
ZONE_GUIDE = 3

DIR_NONE = 0
DIR_LEFT = 1
DIR_RIGHT = 2


@dataclass(frozen=True)
class NavCell:
    x: int
    y: int
    road_zone: int
    nav_direction: int
    speed_limit: int


class StopRequested(Exception):
    pass


class CanoeSysVarClient:
    def __init__(self, visible_log: bool = True) -> None:
        self._app = None
        self._cache: Dict[Tuple[str, str], object] = {}
        self._visible_log = visible_log

    def connect(self) -> None:
        self._app = win32com.client.Dispatch("CANoe.Application")
        if self._visible_log:
            print(f"[CANoe] Connected: {self._app.Version}")

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
        var_obj = self._resolve_var(namespace, variable)
        var_obj.Value = int(value)


def road_context_from_grid(x: int, y: int, width: int, height: int) -> Tuple[int, int, int]:
    """
    Returns (road_zone, nav_direction, speed_limit).

    Zoning policy (deterministic):
    - School zone: upper-left block
    - Highway: middle horizontal belt
    - Guide(IC): right-side corridor, direction split by half
    - Else: normal
    """
    x_school_end = max(2, int(width * 0.30))
    y_school_end = max(2, int(height * 0.35))

    y_hwy_start = max(1, int(height * 0.42))
    y_hwy_end = max(y_hwy_start + 1, int(height * 0.62))

    x_ic_start = max(1, int(width * 0.72))

    if x <= x_school_end and y <= y_school_end:
        return (ZONE_SCHOOL, DIR_NONE, 30)

    if y_hwy_start <= y <= y_hwy_end and x < x_ic_start:
        return (ZONE_HIGHWAY, DIR_NONE, 100)

    if x >= x_ic_start:
        if y < (height // 2):
            return (ZONE_GUIDE, DIR_LEFT, 60)
        return (ZONE_GUIDE, DIR_RIGHT, 60)

    return (ZONE_NORMAL, DIR_NONE, 50)


def serpentine_path(width: int, height: int) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    for y in range(height):
        if y % 2 == 0:
            xs = range(width)
        else:
            xs = range(width - 1, -1, -1)
        for x in xs:
            path.append((x, y))
    return path


def zone_speed_target(road_zone: int, speed_limit: int) -> int:
    if road_zone == ZONE_SCHOOL:
        return speed_limit + 12
    if road_zone == ZONE_HIGHWAY:
        return max(speed_limit - 15, 70)
    if road_zone == ZONE_GUIDE:
        return 45
    return 35


def inject_step(
    canoe: CanoeSysVarClient,
    cell: NavCell,
    apply_speed: bool,
) -> None:
    canoe.set_int("Infotainment", "roadZone", cell.road_zone)
    canoe.set_int("Infotainment", "navDirection", cell.nav_direction)
    canoe.set_int("Infotainment", "zoneDistance", 10)
    canoe.set_int("Infotainment", "speedLimit", cell.speed_limit)

    if apply_speed:
        speed = zone_speed_target(cell.road_zone, cell.speed_limit)
        canoe.set_int("Chassis", "vehicleSpeed", speed)
        canoe.set_int("Chassis", "driveState", 3)
        canoe.set_int("Chassis", "steeringInput", 0 if cell.road_zone == ZONE_HIGHWAY else 1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CANoe navigation grid simulator")
    parser.add_argument("--width", type=int, default=14, help="Grid width")
    parser.add_argument("--height", type=int, default=8, help="Grid height")
    parser.add_argument("--interval-ms", type=int, default=250, help="Step period in ms")
    parser.add_argument("--steps", type=int, default=0, help="Step count (0=infinite)")
    parser.add_argument("--loop", action="store_true", help="Loop path repeatedly")
    parser.add_argument("--random-walk", action="store_true", help="Use random walk instead of serpentine")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for random walk")
    parser.add_argument("--dry-run", action="store_true", help="Print only, no CANoe injection")
    parser.add_argument("--no-speed-update", action="store_true", help="Do not inject chassis speed/steering")
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    width = max(2, args.width)
    height = max(2, args.height)
    interval_s = max(0.05, args.interval_ms / 1000.0)
    infinite = args.steps == 0
    max_steps = args.steps

    stop_flag = {"stop": False}

    def _on_sigint(_sig, _frame):
        stop_flag["stop"] = True

    signal.signal(signal.SIGINT, _on_sigint)

    canoe: Optional[CanoeSysVarClient] = None
    if not args.dry_run:
        canoe = CanoeSysVarClient()
        canoe.connect()
        canoe.set_int("Test", "testScenario", 0)

    path = serpentine_path(width, height)
    rng = random.Random(args.seed)
    cur_x, cur_y = 0, 0
    path_idx = 0
    step = 0

    print(
        "[NAV_SIM] start "
        f"(grid={width}x{height}, interval={args.interval_ms}ms, mode={'random' if args.random_walk else 'path'})"
    )

    while True:
        if stop_flag["stop"]:
            raise StopRequested()

        if not infinite and step >= max_steps:
            break

        if args.random_walk:
            moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            dx, dy = rng.choice(moves)
            cur_x = min(width - 1, max(0, cur_x + dx))
            cur_y = min(height - 1, max(0, cur_y + dy))
            x, y = cur_x, cur_y
        else:
            x, y = path[path_idx]
            path_idx += 1
            if path_idx >= len(path):
                if args.loop or infinite:
                    path_idx = 0
                else:
                    break

        road_zone, nav_dir, speed_limit = road_context_from_grid(x, y, width, height)
        cell = NavCell(
            x=x,
            y=y,
            road_zone=road_zone,
            nav_direction=nav_dir,
            speed_limit=speed_limit,
        )

        if canoe is not None:
            inject_step(canoe, cell, apply_speed=not args.no_speed_update)

        print(
            f"[NAV_SIM] step={step:04d} pos=({cell.x:02d},{cell.y:02d}) "
            f"zone={cell.road_zone} dir={cell.nav_direction} limit={cell.speed_limit}"
        )

        step += 1
        time.sleep(interval_s)

    print("[NAV_SIM] completed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except StopRequested:
        print("[NAV_SIM] stopped by user")
        sys.exit(0)
    except Exception as exc:
        print(f"[NAV_SIM] error: {exc}")
        sys.exit(1)
