#!/usr/bin/env python3
"""Check critical runtime seam ownership in src/capl.

Purpose:
- keep observer/readback seams single-writer
- prevent TEST_SCN or peer ECUs from re-becoming pseudo-owners
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "canoe" / "src" / "capl"

EXPECTED_WRITERS = {
    "Display::animFrame": {"EMS.can"},
    "Display::steeringFrame": {"CLU.can"},
    "Body::frontWiperAnimFrame": {"WIP.can"},
    "Body::blinkLeft": {"BCM.can"},
    "Body::blinkRight": {"BCM.can"},
    "Chassis::brakeLamp": {"ESC.can"},
    "Chassis::vehicleSpeed": {"VCU.can"},
    "Chassis::driveState": {"VCU.can"},
    "V2X::v2xFrame": {"V2X.can"},
    "V2X::MyCarFrame": {"V2X.can"},
    "V2X::AmbFrame": {"V2X.can"},
    "Infotainment::emergencySound": {"V2X.can"},
    "UiRender::navLaneFrame": {"NAV.can"},
    "UiRender::renderVolumLevel": {"AMP.can"},
    "CoreState::baseVolume": {"AMP.can"},
    "Core::selectedAlertType": {"ADAS.can"},
    "Cluster::warningTextCode": {"CLU.can"},
}

BANNED_TEST_SCN_WRITES = {
    "Infotainment::roadZone",
    "Infotainment::navDirection",
    "Infotainment::zoneDistance",
    "Infotainment::speedLimit",
}

BANNED_OWNER_REFERENCES = {
    "@Test::manualAlertOverride",
    "@Test::alertVolumeSetting",
}

WRITE_RE_TEMPLATE = r"@{seam}\s*=(?!=)"


def collect_writers() -> dict[str, list[tuple[str, int, str]]]:
    writers: dict[str, list[tuple[str, int, str]]] = {seam: [] for seam in EXPECTED_WRITERS}
    for path in SRC_ROOT.rglob("*.can"):
        text = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, line in enumerate(text, start=1):
            for seam in EXPECTED_WRITERS:
                if re.search(WRITE_RE_TEMPLATE.format(seam=re.escape(seam)), line):
                    writers[seam].append((path.name, idx, line.strip()))
    return writers


def collect_banned_test_scn_writes() -> list[tuple[str, int, str]]:
    path = SRC_ROOT / "input" / "TEST_SCN.can"
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits: list[tuple[str, int, str]] = []
    for idx, line in enumerate(text, start=1):
        for seam in BANNED_TEST_SCN_WRITES:
            if re.search(WRITE_RE_TEMPLATE.format(seam=re.escape(seam)), line):
                hits.append((path.name, idx, line.strip()))
    return hits


def collect_banned_owner_references() -> list[tuple[str, int, str]]:
    hits: list[tuple[str, int, str]] = []
    for path in SRC_ROOT.rglob("*.can"):
        if path.name == "TEST_SCN.can":
            continue
        text = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, line in enumerate(text, start=1):
            for pattern in BANNED_OWNER_REFERENCES:
                if pattern in line:
                    hits.append((path.name, idx, line.strip()))
    return hits


def main() -> int:
    writers = collect_writers()
    failures: list[str] = []
    banned_test_scn_writes = collect_banned_test_scn_writes()
    banned_owner_references = collect_banned_owner_references()

    print(f"[SEAM_OWNERSHIP] scanned src/capl under {SRC_ROOT}")
    for seam, expected in EXPECTED_WRITERS.items():
        seam_writers = writers[seam]
        writer_names = {name for name, _, _ in seam_writers}
        print(
            f"[SEAM] {seam} expected={','.join(sorted(expected))} "
            f"actual={','.join(sorted(writer_names)) if writer_names else '(none)'}"
        )

        if writer_names != expected:
            failures.append(seam)
            for name, idx, line in seam_writers:
                print(f"  -> {name}:{idx}: {line}")

    if failures:
        print("[FAIL] Critical seam ownership mismatch:")
        for seam in failures:
            print(f"  - {seam}")
        return 2

    if banned_test_scn_writes:
        print("[FAIL] TEST_SCN writes banned legacy context seams directly:")
        for name, idx, line in banned_test_scn_writes:
            print(f"  -> {name}:{idx}: {line}")
        return 2

    if banned_owner_references:
        print("[FAIL] Owner CAPL still references banned legacy test fallback seams:")
        for name, idx, line in banned_owner_references:
            print(f"  -> {name}:{idx}: {line}")
        return 2

    print("[PASS] Critical output seams have the expected single writer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
