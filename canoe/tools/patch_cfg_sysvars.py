"""
Patch CAN_500kBaud_1ch_split.cfg: inject 4 missing sysvar variables
into the embedded <systemvariables> XML block.

Run from repo root:
    python canoe/tools/patch_cfg_sysvars.py
"""
import re
import shutil
from pathlib import Path

CFG = Path(__file__).resolve().parents[2] / "canoe" / "cfg" / "CAN_500kBaud_1ch_split.cfg"

INSERTS = {
    # namespace_name -> list of variable XML lines to append before </namespace>
    "Core": [
        '      <variable anlyzLocal="2" readOnly="false" valueSequence="false" unit="km/h" '
        'name="speedLimitNorm" comment="Normalized speed limit from NAV_CTX_MGR" '
        'bitcount="32" isSigned="false" encoding="65001" type="int" '
        'minValue="0" minValuePhys="0" maxValue="255" maxValuePhys="255" />',
    ],
    "CoreState": [
        '      <variable anlyzLocal="2" readOnly="false" valueSequence="false" unit="" '
        'name="domainBoundaryStatus" comment="Domain boundary health: 1=all Chassis/Body/Info domains alive within 300ms" '
        'bitcount="32" isSigned="false" encoding="65001" type="int" '
        'minValue="0" minValuePhys="0" maxValue="1" maxValuePhys="1" />',
        '      <variable anlyzLocal="2" readOnly="false" valueSequence="false" unit="" '
        'name="routingPolicy" comment="GW routing policy: 0=timeout 1=normal 2=emergency" '
        'bitcount="32" isSigned="false" encoding="65001" type="int" '
        'minValue="0" minValuePhys="0" maxValue="2" maxValuePhys="2" />',
    ],
    "Infotainment": [
        '      <variable anlyzLocal="2" readOnly="false" valueSequence="false" unit="km/h" '
        'name="speedLimit" comment="Zone speed limit from CAN input" '
        'bitcount="32" isSigned="false" encoding="65001" type="int" '
        'minValue="0" minValuePhys="0" maxValue="255" maxValuePhys="255" />',
    ],
}

ALREADY_PRESENT = {"speedLimitNorm", "domainBoundaryStatus", "routingPolicy", "speedLimit"}


def main() -> None:
    raw = CFG.read_bytes()

    # detect line ending
    crlf = b"\r\n" in raw
    le = b"\r\n" if crlf else b"\n"

    text = raw.decode("utf-8-sig")   # strips BOM if present, keeps rest

    # quick check: skip if already patched
    missing = [v for v in ALREADY_PRESENT if f'name="{v}"' not in text]
    if not missing:
        print("All variables already present in cfg — nothing to do.")
        return

    print(f"Missing in cfg internal XML: {missing}")

    for ns, lines_to_add in INSERTS.items():
        # only insert variables that are actually missing
        lines_needed = [l for l in lines_to_add
                        if re.search(r'name="(\w+)"', l).group(1) in missing]
        if not lines_needed:
            continue

        # match the closing tag of this specific namespace
        # pattern: one or more <variable .../> lines followed by </namespace>
        # we insert before the </namespace> that closes namespace name="NS"
        pattern = (
            r'(<namespace name="' + re.escape(ns) + r'"[^>]*>)'
            r'((?:\s*<variable [^/]*/>\s*)+)'
            r'(\s*</namespace>)'
        )

        def make_replacer(ns_lines):
            def replacer(m):
                insert_block = le.decode() + (le.decode()).join(ns_lines)
                return m.group(1) + m.group(2).rstrip() + insert_block + m.group(3)
            return replacer

        new_text, n = re.subn(pattern, make_replacer(lines_needed), text, count=1)
        if n == 0:
            print(f"  WARNING: namespace '{ns}' not found or pattern mismatch — skipped")
        else:
            print(f"  Patched namespace '{ns}'")
            text = new_text

    # backup original
    shutil.copy2(CFG, CFG.with_suffix(".cfg.bak"))
    print(f"Backup saved: {CFG.with_suffix('.cfg.bak')}")

    out_bytes = text.encode("utf-8")
    CFG.write_bytes(out_bytes)
    print(f"Done: {CFG}")


if __name__ == "__main__":
    main()
