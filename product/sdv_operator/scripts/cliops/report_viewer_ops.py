from __future__ import annotations

import argparse
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from .common import ROOT
from .native_contract import NativeContractError, resolve_tier_contract


class ReportViewerError(RuntimeError):
    """Raised when official Vector report tooling is unavailable or fails."""


REPORT_STAGING_ROOT = ROOT / "canoe" / "tmp" / "reports" / "verification"
OFFICIAL_REPORTS_ROOT = REPORT_STAGING_ROOT / "official_reports"
OFFICIAL_TOOLING_JSON = REPORT_STAGING_ROOT / "official_report_tooling.json"
OFFICIAL_MANIFEST_JSON = REPORT_STAGING_ROOT / "official_report_manifest.json"
OFFICIAL_MANIFEST_MD = REPORT_STAGING_ROOT / "official_report_manifest.md"
DATA_API_DUMP_PS1 = ROOT / "product" / "sdv_operator" / "scripts" / "official_tools" / "report_viewer_dataapi_dump.ps1"
POWERSHELL_EXE = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"


@dataclass(frozen=True)
class ReportViewerTooling:
    viewer_install_dir: str
    cli_path: str
    selector_install_dir: str
    selector_exe: str
    help_usage: str
    help_data_api: str
    help_api_reference: str
    api_packages_dir: str
    data_api_assembly_dir: str
    data_api_dll: str
    data_api_diva_dll: str
    data_api_dump_script: str
    supported_cli_exports: list[str]


def _display_path(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return str(path.resolve())
    except OSError:
        return str(path)


def _pick_latest(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return sorted(paths, key=lambda item: str(item).lower())[-1]


def _discover_report_viewer_cli() -> Path | None:
    candidates = list(Path(r"C:\Program Files").glob(r"Vector CANoe Test Report Viewer*\ReportViewerCli.exe"))
    return _pick_latest(candidates)


def _discover_data_api_dir() -> Path | None:
    base = Path(r"C:\Program Files\Common Files\Vector CANoe Test Report Viewer DiVa API Assemblies")
    if not base.exists():
        return None
    candidates = [item for item in base.iterdir() if item.is_dir()]
    return _pick_latest(candidates)


def _discover_selector_exe() -> Path | None:
    candidates = list(Path(r"C:\Program Files").glob(r"Vector CANoe Test Report Viewer Selector\ReportViewerSelector.exe"))
    return _pick_latest(candidates)


def _tooling_payload(tooling: ReportViewerTooling) -> dict:
    return {
        "schema": "vector.reportviewer.tooling.snapshot.v2",
        "generated_at": datetime.now().isoformat(),
        "tooling": asdict(tooling),
        "component_policy": [
            {
                "component": "CANoe Test Report Viewer",
                "role": "native report GUI fallback",
                "priority": "recommended",
                "required_for_product": False,
                "installed": bool(tooling.viewer_install_dir),
            },
            {
                "component": "ReportViewerCli.exe",
                "role": "official XML/XUnit/PDF export",
                "priority": "mandatory",
                "required_for_product": True,
                "installed": bool(tooling.cli_path),
            },
            {
                "component": "Vector.ReportViewer.DataApi",
                "role": "official .vtestreport structural parse",
                "priority": "mandatory",
                "required_for_product": True,
                "installed": bool(tooling.data_api_dll and tooling.data_api_diva_dll),
            },
            {
                "component": "ReportViewerSelector.exe",
                "role": "viewer launch helper",
                "priority": "optional",
                "required_for_product": False,
                "installed": bool(tooling.selector_exe),
            },
        ],
    }


def discover_report_viewer_tooling() -> ReportViewerTooling:
    cli = _discover_report_viewer_cli()
    api_dir = _discover_data_api_dir()
    selector = _discover_selector_exe()
    if cli is None:
        raise ReportViewerError("Vector ReportViewerCli.exe not found.")
    if api_dir is None:
        raise ReportViewerError("Vector Data API assembly directory not found.")
    install_dir = cli.parent
    usage_help = install_dir / "Help01" / "content" / "topics" / "canoetestreportviewer" / "ctrvusage.htm"
    data_api_help = install_dir / "Help01" / "content" / "topics" / "canoetestreportviewer" / "ctrvdataapi.htm"
    api_reference = install_dir / "Help01" / "Subsystems" / "VectorCANoeTestReportViewerDataAPI" / "VectorCANoeTestReportViewerDataAPI.htm"
    api_packages = install_dir / "API Packages"
    data_api_dll = api_dir / "Vector.ReportViewer.DataApi.dll"
    data_api_diva_dll = api_dir / "Vector.ReportViewer.DataApi.DiVa.dll"
    if not data_api_dll.exists():
        raise ReportViewerError(f"Vector.ReportViewer.DataApi.dll not found: {data_api_dll}")
    if not data_api_diva_dll.exists():
        raise ReportViewerError(f"Vector.ReportViewer.DataApi.DiVa.dll not found: {data_api_diva_dll}")
    if not DATA_API_DUMP_PS1.exists():
        raise ReportViewerError(f"Data API dump script missing: {DATA_API_DUMP_PS1}")
    return ReportViewerTooling(
        viewer_install_dir=_display_path(install_dir),
        cli_path=_display_path(cli),
        selector_install_dir=_display_path(selector.parent if selector else None),
        selector_exe=_display_path(selector),
        help_usage=_display_path(usage_help),
        help_data_api=_display_path(data_api_help),
        help_api_reference=_display_path(api_reference),
        api_packages_dir=_display_path(api_packages),
        data_api_assembly_dir=_display_path(api_dir),
        data_api_dll=_display_path(data_api_dll),
        data_api_diva_dll=_display_path(data_api_diva_dll),
        data_api_dump_script=_display_path(DATA_API_DUMP_PS1),
        supported_cli_exports=["xml", "xunit", "pdf"],
    )


def _write_tooling_snapshot(tooling: ReportViewerTooling) -> None:
    OFFICIAL_TOOLING_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = _tooling_payload(tooling)
    OFFICIAL_TOOLING_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _resolve_report_path(*, tier: str | None, explicit_report: str | None) -> tuple[str, Path, str]:
    if explicit_report:
        report_path = Path(explicit_report).expanduser()
        tier_name = (tier or report_path.stem).strip().upper()
        return tier_name, report_path, report_path.stem
    if not tier:
        raise ReportViewerError("either --tier or --report is required")
    try:
        contract = resolve_tier_contract(tier)
    except NativeContractError as ex:
        raise ReportViewerError(str(ex)) from ex
    return contract.tier, contract.summary_report_path, contract.summary_report_path.stem


def _official_tier_dir(tier: str) -> Path:
    return OFFICIAL_REPORTS_ROOT / tier.upper()


def _run_subprocess(args: list[str], *, label: str) -> None:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        detail = (proc.stdout or proc.stderr or "").strip()
        raise ReportViewerError(f"{label} failed (rc={proc.returncode}): {detail}")


def _export_with_cli(*, tooling: ReportViewerTooling, report_path: Path, output_dir: Path, base_name: str, include_pdf: bool) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    xml_path = output_dir / f"{base_name}.xml"
    xunit_path = output_dir / f"{base_name}.xunit.xml"
    _run_subprocess(
        [tooling.cli_path, f"--report={report_path}", f"--export={xml_path}"],
        label="official XML export",
    )
    _run_subprocess(
        [tooling.cli_path, f"--report={report_path}", f"--xunit={xunit_path}"],
        label="official XUnit export",
    )
    out = {
        "xml": _display_path(xml_path),
        "xunit": _display_path(xunit_path),
    }
    if include_pdf:
        pdf_path = output_dir / f"{base_name}.pdf"
        _run_subprocess(
            [tooling.cli_path, f"--report={report_path}", f"--pdf={pdf_path}"],
            label="official PDF export",
        )
        out["pdf"] = _display_path(pdf_path)
    return out


def _run_data_api_dump(*, tooling: ReportViewerTooling, report_path: Path, output_dir: Path, base_name: str) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / f"{base_name}.dataapi.json"
    _run_subprocess(
        [
            str(POWERSHELL_EXE),
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            tooling.data_api_dump_script,
            "-ReportPath",
            str(report_path),
            "-OutputJson",
            str(output_json),
            "-AssemblyDir",
            tooling.data_api_assembly_dir,
        ],
        label="official Data API dump",
    )
    return _display_path(output_json)


def _parse_xunit_summary(xunit_path: Path) -> dict:
    root = ET.parse(xunit_path).getroot()
    suites = root.findall("testsuite")
    failed_cases: list[dict[str, object]] = []
    total = 0
    failures = 0
    errors = 0
    skipped = 0
    for suite in suites:
        total += int(suite.attrib.get("tests", "0") or 0)
        failures += int(suite.attrib.get("failures", "0") or 0)
        errors += int(suite.attrib.get("errors", "0") or 0)
        skipped += int(suite.attrib.get("skipped", "0") or 0)
        testcase = suite.find("testcase")
        if testcase is None:
            continue
        failure = testcase.find("failure")
        if failure is None:
            continue
        failed_cases.append(
            {
                "name": testcase.attrib.get("name", suite.attrib.get("name", "")),
                "classname": testcase.attrib.get("classname", ""),
                "time_seconds": testcase.attrib.get("time", ""),
                "failure_type": failure.attrib.get("type", ""),
                "failure_message": failure.attrib.get("message", ""),
            }
        )
    passed = max(total - failures - errors - skipped, 0)
    return {
        "tests": total,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "passed": passed,
        "failed_cases": failed_cases,
    }


def _parse_xml_causes(xml_path: Path) -> dict[str, str]:
    root = ET.parse(xml_path).getroot()
    causes: dict[str, str] = {}
    for testcase in root.findall("./testunit/testfixture/testcase"):
        title = testcase.findtext("title", default="").strip()
        verdict = testcase.find("verdict")
        if verdict is None:
            continue
        cause = verdict.findtext("cause", default="").strip()
        if title and cause:
            causes[title] = cause
    return causes


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_bundle_summary_md(path: Path, bundle: dict) -> None:
    lines = [
        "# Official Report Bundle",
        "",
        f"- tier: `{bundle.get('tier', '-')}`",
        f"- report_path: `{bundle.get('report_path', '-')}`",
        f"- report_title: `{bundle.get('report_title', '-')}`",
        f"- report_verdict: `{bundle.get('report_verdict', '-')}`",
        f"- tests/failures/errors/skipped: `{bundle['xunit_summary'].get('tests', 0)}` / `{bundle['xunit_summary'].get('failures', 0)}` / `{bundle['xunit_summary'].get('errors', 0)}` / `{bundle['xunit_summary'].get('skipped', 0)}`",
        "",
        "## Exports",
        "",
    ]
    for key, value in bundle.get("exports", {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Failed Cases", ""])
    failed_cases = bundle.get("failed_cases", [])
    if not failed_cases:
        lines.append("- none")
    else:
        for item in failed_cases:
            lines.append(f"- `{item.get('name', '-')}`: `{item.get('message', '-')}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _update_manifest(*, tooling: ReportViewerTooling, bundle: dict) -> None:
    manifest = {
        "schema": "vector.reportviewer.official.manifest.v1",
        "generated_at": datetime.now().isoformat(),
        "tooling": asdict(tooling),
        "tiers": {},
    }
    if OFFICIAL_MANIFEST_JSON.exists():
        try:
            manifest = json.loads(OFFICIAL_MANIFEST_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
        manifest["generated_at"] = datetime.now().isoformat()
        manifest["tooling"] = asdict(tooling)
        if not isinstance(manifest.get("tiers"), dict):
            manifest["tiers"] = {}
    tier_key = str(bundle.get("tier", "")).upper()
    manifest["tiers"][tier_key] = {
        "report_path": bundle.get("report_path", ""),
        "report_title": bundle.get("report_title", ""),
        "report_verdict": bundle.get("report_verdict", ""),
        "tests": bundle.get("xunit_summary", {}).get("tests", 0),
        "failures": bundle.get("xunit_summary", {}).get("failures", 0),
        "errors": bundle.get("xunit_summary", {}).get("errors", 0),
        "skipped": bundle.get("xunit_summary", {}).get("skipped", 0),
        "exports": bundle.get("exports", {}),
        "bundle_json": bundle.get("bundle_json", ""),
        "bundle_md": bundle.get("bundle_md", ""),
        "failed_cases": bundle.get("failed_cases", []),
    }
    OFFICIAL_MANIFEST_JSON.parent.mkdir(parents=True, exist_ok=True)
    OFFICIAL_MANIFEST_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Official Report Manifest",
        "",
        f"- generated_at: `{manifest['generated_at']}`",
        "",
        "| tier | verdict | tests | failures | bundle |",
        "|---|---|---:|---:|---|",
    ]
    for tier, row in sorted(manifest["tiers"].items()):
        lines.append(
            f"| `{tier}` | `{row.get('report_verdict', '-')}` | `{row.get('tests', 0)}` | `{row.get('failures', 0)}` | `{row.get('bundle_json', '-')}` |"
        )
    OFFICIAL_MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_official_report_bundle(*, tier: str | None, explicit_report: str | None, include_pdf: bool) -> dict:
    tooling = discover_report_viewer_tooling()
    _write_tooling_snapshot(tooling)
    resolved_tier, report_path, base_name = _resolve_report_path(tier=tier, explicit_report=explicit_report)
    if not report_path.exists():
        raise ReportViewerError(f"native report not found: {report_path}")
    output_dir = _official_tier_dir(resolved_tier)
    exports = _export_with_cli(
        tooling=tooling,
        report_path=report_path,
        output_dir=output_dir,
        base_name=base_name,
        include_pdf=include_pdf,
    )
    data_api_json = _run_data_api_dump(
        tooling=tooling,
        report_path=report_path,
        output_dir=output_dir,
        base_name=base_name,
    )
    exports["data_api_json"] = data_api_json
    xunit_summary = _parse_xunit_summary(Path(exports["xunit"]))
    xml_causes = _parse_xml_causes(Path(exports["xml"]))
    data_api_payload = _load_json(Path(data_api_json))
    failed_cases = []
    for row in xunit_summary.get("failed_cases", []):
        name = str(row.get("name", ""))
        failed_cases.append(
            {
                "name": name,
                "classname": row.get("classname", ""),
                "time_seconds": row.get("time_seconds", ""),
                "message": xml_causes.get(name, row.get("failure_message", "")),
                "failure_type": row.get("failure_type", ""),
            }
        )
    bundle = {
        "schema": "vector.reportviewer.official.bundle.v1",
        "generated_at": datetime.now().isoformat(),
        "tier": resolved_tier,
        "report_path": _display_path(report_path),
        "report_title": data_api_payload.get("report", {}).get("title", base_name),
        "report_verdict": data_api_payload.get("report", {}).get("verdict", ""),
        "exports": exports,
        "xunit_summary": xunit_summary,
        "xml_causes": xml_causes,
        "data_api": data_api_payload,
        "failed_cases": failed_cases,
    }
    bundle_json = output_dir / f"{base_name}.bundle.json"
    bundle_md = output_dir / f"{base_name}.bundle.md"
    bundle["bundle_json"] = _display_path(bundle_json)
    bundle["bundle_md"] = _display_path(bundle_md)
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_json.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_bundle_summary_md(bundle_md, bundle)
    _update_manifest(tooling=tooling, bundle=bundle)
    return bundle


def cmd_verify_report_tools(args: argparse.Namespace) -> int:
    try:
        tooling = discover_report_viewer_tooling()
        _write_tooling_snapshot(tooling)
    except ReportViewerError as ex:
        print(f"[REPORT_TOOLS] FAIL: {ex}")
        return 2
    payload = _tooling_payload(tooling)
    payload["snapshot_path"] = _display_path(OFFICIAL_TOOLING_JSON)
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"[REPORT_TOOLS] viewer={tooling.viewer_install_dir}")
        print(f"[REPORT_TOOLS] cli={tooling.cli_path}")
        print(f"[REPORT_TOOLS] selector={tooling.selector_exe or '-'}")
        print(f"[REPORT_TOOLS] data_api={tooling.data_api_dll}")
        print(f"[REPORT_TOOLS] data_api_diva={tooling.data_api_diva_dll}")
        print(f"[REPORT_TOOLS] help_usage={tooling.help_usage}")
        print(f"[REPORT_TOOLS] help_data_api={tooling.help_data_api}")
        print(f"[REPORT_TOOLS] help_api_reference={tooling.help_api_reference}")
        print(f"[REPORT_TOOLS] api_packages={tooling.api_packages_dir}")
        print(f"[REPORT_TOOLS] snapshot={_display_path(OFFICIAL_TOOLING_JSON)}")
    return 0


def cmd_verify_report_bundle(args: argparse.Namespace) -> int:
    try:
        bundle = build_official_report_bundle(
            tier=(getattr(args, "tier", "") or "").strip().upper() or None,
            explicit_report=(getattr(args, "report", "") or "").strip() or None,
            include_pdf=bool(getattr(args, "include_pdf", False)),
        )
    except ReportViewerError as ex:
        print(f"[REPORT_BUNDLE] FAIL: {ex}")
        return 2
    if getattr(args, "json", False):
        print(json.dumps(bundle, indent=2, ensure_ascii=False))
    else:
        print(
            f"[REPORT_BUNDLE] tier={bundle['tier']} verdict={bundle['report_verdict']} "
            f"tests={bundle['xunit_summary'].get('tests', 0)} failures={bundle['xunit_summary'].get('failures', 0)}"
        )
        print(f"[OUT] {bundle['bundle_json']}")
        print(f"[OUT] {bundle['bundle_md']}")
        print(f"[OUT] {_display_path(OFFICIAL_MANIFEST_JSON)}")
        print(f"[OUT] {_display_path(OFFICIAL_MANIFEST_MD)}")
    return 0
