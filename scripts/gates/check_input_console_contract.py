#!/usr/bin/env python3
"""Validate local Input_Console.xvp against output-first command rules.

Rules:
- input panels must write only command/injection lifecycle seams
- owner/readback seams must not be written from the input console
- root and Desktop_ASSIGN mirror must stay byte-identical
- simulator-style local console must not regress back to trackbar-heavy UI
"""

from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT_XVP = REPO_ROOT / "canoe" / "project" / "panel" / "Input_Console.xvp"
MIRROR_XVP = (
    REPO_ROOT
    / "canoe"
    / "project"
    / "panel"
    / "Desktop_ASSIGN"
    / "Module"
    / "Input_Console.xvp"
)
SYSVARS_PATH = REPO_ROOT / "canoe" / "project" / "sysvars" / "project.sysvars"

SYMBOL_RE = re.compile(r'<Property Name="SymbolConfiguration">([^<]+)</Property>')
TRACKBAR_RE = re.compile(r"TrackBarControl")
RADIO_RE = re.compile(r"RadioButtonControl")
IMAGE_RE = re.compile(r'<Property Name="ImageFile">([^<]+)</Property>')

ALLOWED_WRITE_SEAMS = {
    "Test::scenarioCommand",
    "Test::scenarioStopReq",
    "Test::testScenario",
    "Test::driverBeltOff",
    "Test::passengerBeltOff",
    "V2X::AnimationTrigger",
    "V2X::policePos",
    "V2X::ambulancePos",
}
ALLOWED_WRITE_PREFIXES = (
    "Cmd::",
    "Inject::",
)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_symbol(symbol_cfg: str) -> tuple[str, str] | None:
    parts = symbol_cfg.split(";")
    if len(parts) < 7:
        return None

    domain = parts[2]
    msg = parts[4]
    sig = parts[5]
    rw = parts[6]

    if not domain:
        return None

    symbol = f"{domain}::{msg + '.' if msg else ''}{sig}"
    return rw, symbol


def extract_symbols(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    parsed: list[tuple[str, str]] = []
    for match in SYMBOL_RE.finditer(text):
        result = parse_symbol(match.group(1))
        if result is not None:
            parsed.append(result)
    return parsed


def extract_image_paths(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return sorted(set(IMAGE_RE.findall(text)))


def extract_sysvars(path: Path) -> set[str]:
    tree = ET.parse(path)
    symbols: set[str] = set()
    for ns in tree.findall(".//namespace"):
        ns_name = ns.get("name")
        if not ns_name:
            continue
        for var in ns.findall("./variable"):
            var_name = var.get("name")
            if var_name:
                symbols.add(f"{ns_name}::{var_name}")
    return symbols


def is_allowed_write(symbol: str) -> bool:
    if symbol in ALLOWED_WRITE_SEAMS:
        return True
    return symbol.startswith(ALLOWED_WRITE_PREFIXES)


def main() -> int:
    missing = [str(path) for path in (ROOT_XVP, MIRROR_XVP, SYSVARS_PATH) if not path.exists()]
    if missing:
        print("[FAIL] Input console file missing:")
        for path in missing:
            print(f"  - {path}")
        return 2

    root_hash = file_hash(ROOT_XVP)
    mirror_hash = file_hash(MIRROR_XVP)
    root_text = ROOT_XVP.read_text(encoding="utf-8")
    root_syms = extract_symbols(ROOT_XVP)
    image_paths = extract_image_paths(ROOT_XVP)
    sysvars = extract_sysvars(SYSVARS_PATH)

    writes = sorted({symbol for rw, symbol in root_syms if rw == "1"})
    reads = sorted({symbol for rw, symbol in root_syms if rw == "2"})
    all_symbols = sorted(set(writes) | set(reads))
    bad_writes = sorted(symbol for symbol in writes if not is_allowed_write(symbol))
    missing_symbols = sorted(symbol for symbol in all_symbols if "." not in symbol and symbol not in sysvars)
    has_trackbar = bool(TRACKBAR_RE.search(root_text))
    has_radio = bool(RADIO_RE.search(root_text))
    missing_root_images = sorted(
        rel for rel in image_paths if not (ROOT_XVP.parent / rel).exists()
    )
    missing_mirror_images = sorted(
        rel for rel in image_paths if not (MIRROR_XVP.parent / rel).exists()
    )

    print(f"[INPUT_CONSOLE] root={ROOT_XVP}")
    print(f"[INPUT_CONSOLE] mirror={MIRROR_XVP}")
    print(f"[INPUT_CONSOLE] writes={len(writes)} reads={len(reads)}")
    print(f"[INPUT_CONSOLE] mirror_match={'yes' if root_hash == mirror_hash else 'no'}")
    print(f"[INPUT_CONSOLE] trackbar_present={'yes' if has_trackbar else 'no'}")
    print(f"[INPUT_CONSOLE] radio_present={'yes' if has_radio else 'no'}")
    print(f"[INPUT_CONSOLE] image_refs={len(image_paths)}")

    if bad_writes:
        print("[FAIL] Forbidden write seams detected:")
        for symbol in bad_writes:
            print(f"  - {symbol}")

    if missing_symbols:
        print("[FAIL] Symbols missing from project.sysvars:")
        for symbol in missing_symbols:
            print(f"  - {symbol}")

    if has_trackbar:
        print("[FAIL] TrackBarControl detected. Input_Console must stay click-first.")

    if has_radio:
        print("[FAIL] RadioButtonControl detected. Input_Console must stay designer-safe and button-driven.")

    if root_hash != mirror_hash:
        print("[FAIL] Root and Desktop_ASSIGN mirror differ.")

    if missing_root_images:
        print("[FAIL] Root Input_Console image files missing:")
        for rel in missing_root_images:
            print(f"  - {rel}")

    if missing_mirror_images:
        print("[FAIL] Desktop_ASSIGN Input_Console image files missing:")
        for rel in missing_mirror_images:
            print(f"  - {rel}")

    if (
        bad_writes
        or missing_symbols
        or root_hash != mirror_hash
        or has_trackbar
        or has_radio
        or missing_root_images
        or missing_mirror_images
    ):
        return 2

    print("[PASS] Input_Console uses command/injection seams only, all sysvars exist, remains click-first, is designer-safe, and mirror matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
