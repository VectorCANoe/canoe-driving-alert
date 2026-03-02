import re
from pathlib import Path

ROOT = Path("canoe/project/panel")
OUT = Path("canoe/docs/operations/PANEL_BINDING_AUDIT.md")

OBJ_RE = re.compile(
    r'<Object Type="Vector\.CANalyzer\.Panels\.Design\.[^"]+" Name="([^"]+)" ControlName="([^"]+)">'
)
VAR_RE = re.compile(r"<Property Name=\"SymbolConfiguration\">[^<]*UiRender;;;([^;]+);")
IMG_RE = re.compile(
    r"<Property Name=\"ImageFile\">([^<]+)</Property>|<Property Name=\"ImageFileName\">([^<]+)</Property>"
)

EXPECTED = {
    "SDV_External_Road_View.xvp": {
        "roadZoneColorCode",
        "roadFlowDirection",
        "vehicleObjectPos",
        "activeAlertType",
        "emsBlinkPhase",
        "renderDirection",
    },
    "SDV_Cabin_Panorama_View.xvp": {
        "renderMode",
        "renderColor",
        "renderPattern",
        "ambientPulsePhase",
        "renderDirection",
        "activeAlertType",
        "emsBlinkPhase",
    },
    "SDV_Navigation_View.xvp": {
        "roadZoneColorCode",
        "roadFlowDirection",
        "vehicleObjectPos",
        "icFlowPhase",
    },
    "SDV_Ambient_View.xvp": {
        "renderMode",
        "renderColor",
        "renderPattern",
        "ambientPulsePhase",
        "activeAlertType",
        "emsBlinkPhase",
    },
    "SDV_Cluster_View.xvp": {
        "renderTextCode",
        "renderDirection",
        "roadZoneColorCode",
        "vehicleObjectPos",
        "activeAlertType",
        "emsBlinkPhase",
    },
}


def collect_rows(text: str):
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
        im = IMG_RE.search(chunk)
        image = ""
        if im:
            image = (im.group(1) or im.group(2) or "").strip()
        rows.append((m.group(1), m.group(2), vm.group(1), image))
    return rows


def main():
    panels = sorted(ROOT.glob("SDV_*.xvp"))
    lines = [
        "# PANEL BINDING AUDIT",
        "",
        "Auto-generated from `canoe/project/panel/SDV_*.xvp`.",
        "",
    ]

    for panel in panels:
        text = panel.read_text(encoding="utf-8", errors="replace")
        rows = collect_rows(text)
        used_vars = sorted({r[2] for r in rows})

        lines.append(f"## {panel.name}")
        if used_vars:
            lines.append(f"- UiRender vars: `{', '.join(used_vars)}`")
        else:
            lines.append("- UiRender vars: `(none)`")

        if panel.name in EXPECTED:
            extra = sorted(set(used_vars) - EXPECTED[panel.name])
            missing = sorted(EXPECTED[panel.name] - set(used_vars))
            if extra:
                lines.append(f"- Unexpected vars vs target: `{', '.join(extra)}`")
            else:
                lines.append("- Unexpected vars vs target: `(none)`")
            if missing:
                lines.append(f"- Missing vars vs target: `{', '.join(missing)}`")
            else:
                lines.append("- Missing vars vs target: `(none)`")

        lines.append("")
        lines.append("| Object Name | Control Name | UiRender Var | Image |")
        lines.append("|---|---|---|---|")
        for name, ctrl, var, img in rows:
            lines.append(f"| `{name}` | `{ctrl}` | `{var}` | `{img}` |")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"generated:{OUT}")


if __name__ == "__main__":
    main()
