import re
import sys
from pathlib import Path

ROOT = Path("canoe/project/panel")

OBJ_RE = re.compile(
    r'<Object Type="Vector\.CANalyzer\.Panels\.Design\.[^"]+" Name="([^"]+)" ControlName="([^"]+)">'
)
VAR_RE = re.compile(r"<Property Name=\"SymbolConfiguration\">[^<]*UiRender;;;([^;]+);")

DISALLOWED_BY_PANEL = {
    "SDV_External_Road_View.xvp": {"renderPattern", "renderColor", "renderTextCode"},
    "SDV_Cabin_Panorama_View.xvp": {"renderTextCode"},
}


def extract_vars(panel_path: Path):
    text = panel_path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for m in OBJ_RE.finditer(text):
        start = m.start()
        end = text.find("</Object>", start)
        if end == -1:
            end = min(len(text), start + 1800)
        chunk = text[start:end]
        vm = VAR_RE.search(chunk)
        if not vm:
            continue
        rows.append((m.group(1), m.group(2), vm.group(1)))
    return rows


def main():
    failed = False

    for panel_name, disallowed in DISALLOWED_BY_PANEL.items():
        panel_path = ROOT / panel_name
        if not panel_path.exists():
            print(f"FAIL: missing panel file: {panel_path}")
            failed = True
            continue

        rows = extract_vars(panel_path)
        violations = [r for r in rows if r[2] in disallowed]

        print(f"[{panel_name}]")
        if not violations:
            print("PASS: no disallowed UiRender bindings")
        else:
            failed = True
            print("FAIL: disallowed UiRender bindings found")
            for obj_name, ctrl_name, var in violations:
                print(f"  - object={obj_name}, control={ctrl_name}, var=UiRender::{var}")

    demo_stage = ROOT / "SDV_Demo_Stage.xvp"
    if demo_stage.exists():
        print("[SDV_Demo_Stage.xvp]")
        print("INFO: legacy panel present (freeze mode expected)")

    if failed:
        print("RESULT: FAIL")
        return 1

    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
