#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC_ROOT = ROOT / "driving-situation-alert"
TMP_ROOT = DOC_ROOT / "tmp"
REPORT_PATH = TMP_ROOT / "reports" / "Doc_Code_Sync_Report.md"
TEMPLATE_PATH = TMP_ROOT / "templates" / "Doc_Code_Sync_Report_Template.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ids(text: str, prefix: str) -> set[str]:
    return set(re.findall(rf"{prefix}_\d{{3}}", text))


def git(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(["git", *cmd], cwd=ROOT)
        return out.decode("utf-8", errors="ignore").strip()
    except Exception:
        return "unknown"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def main() -> int:
    doc_files = {
        "01": DOC_ROOT / "01_Requirements.md",
        "03": DOC_ROOT / "03_Function_definition.md",
        "0301": DOC_ROOT / "0301_SysFuncAnalysis.md",
        "0302": DOC_ROOT / "0302_NWflowDef.md",
        "0303": DOC_ROOT / "0303_Communication_Specification.md",
        "0304": DOC_ROOT / "0304_System_Variables.md",
        "05": DOC_ROOT / "05_Unit_Test.md",
        "06": DOC_ROOT / "06_Integration_Test.md",
        "07": DOC_ROOT / "07_System_Test.md",
    }

    texts = {k: read_text(p) for k, p in doc_files.items()}

    req_ref = ids(texts["01"], "Req")
    func_ref = ids(texts["03"], "Func")

    req_rows: list[list[str]] = []
    fail = False
    warn_issues: list[str] = []
    fail_issues: list[str] = []

    # Required full coverage docs
    strict_req_docs = ["03", "0301", "0302", "0303", "0304", "05", "07"]
    advisory_req_docs = ["06"]

    for key in strict_req_docs + advisory_req_docs:
        present = ids(texts[key], "Req")
        miss = sorted(req_ref - present)
        status = "PASS"
        if miss:
            if key in strict_req_docs:
                status = "FAIL"
                fail = True
                fail_issues.append(f"{key}: missing Req {', '.join(miss[:6])}")
            else:
                status = "WARN"
                warn_issues.append(f"{key}: missing Req {', '.join(miss[:6])} (Lean IT advisory)")
        req_rows.append([key, str(len(req_ref) - len(miss)), str(len(req_ref)), status])

    req_table = markdown_table(["Doc", "Covered", "Total", "Status"], req_rows)

    # Func coverage: architecture chain docs should be complete
    strict_func_docs = ["0301", "0302", "0303", "0304"]
    func_rows: list[list[str]] = []
    for key in strict_func_docs:
        present = ids(texts[key], "Func")
        miss = sorted(func_ref - present)
        status = "PASS"
        if miss:
            status = "FAIL"
            fail = True
            fail_issues.append(f"{key}: missing Func {', '.join(miss[:6])}")
        func_rows.append([key, str(len(func_ref) - len(miss)), str(len(func_ref)), status])
    func_table = markdown_table(["Doc", "Covered", "Total", "Status"], func_rows)

    # Implementation checks
    expected_nodes = {
        "ADAS_WARN_CTRL",
        "NAV_CONTEXT_MGR",
        "WARN_ARB_MGR",
        "EMS_POLICE_TX",
        "EMS_AMB_TX",
        "EMS_ALERT_RX",
        "BCM_AMBIENT_CTRL",
        "CLU_HMI_CTRL",
        "SIL_TEST_CTRL",
        "VEHICLE_BASE_TEST_CTRL",
        "CHASSIS_GW",
        "INFOTAINMENT_GW",
        "BODY_GW",
        "IVI_GW",
        "ETH_SWITCH",
        "DOMAIN_GW_ROUTER",
        "DOMAIN_BOUNDARY_MGR",
        "ENGINE_CTRL",
        "TRANSMISSION_CTRL",
        "ACCEL_CTRL",
        "BRAKE_CTRL",
        "STEERING_CTRL",
        "HAZARD_CTRL",
        "WINDOW_CTRL",
        "DRIVER_STATE_CTRL",
        "CLUSTER_BASE_CTRL",
    }

    capl_nodes = {p.stem for p in (ROOT / "canoe" / "src" / "capl").glob("**/*.can")}
    cfg_text = read_text(ROOT / "canoe" / "cfg" / "CAN_500kBaud_1ch_split.cfg")
    cfg_nodes = {
        Path(x.replace("..\\src\\capl\\", "").replace("\\", "/")).stem
        for x in re.findall(r"\.\.\\src\\capl\\[^\s\"<>]+\.can", cfg_text)
    }

    dbc_paths = [
        ROOT / "canoe" / "databases" / "chassis_can.dbc",
        ROOT / "canoe" / "databases" / "powertrain_can.dbc",
        ROOT / "canoe" / "databases" / "body_can.dbc",
        ROOT / "canoe" / "databases" / "infotainment_can.dbc",
        ROOT / "canoe" / "databases" / "test_can.dbc",
    ]
    missing_dbc_files = [p.name for p in dbc_paths if not p.exists()]

    missing_capl = sorted(expected_nodes - capl_nodes)
    missing_cfg = sorted(expected_nodes - cfg_nodes)

    if missing_capl:
        fail = True
        fail_issues.append(f"CAPL missing: {', '.join(missing_capl)}")
    if missing_cfg:
        fail = True
        fail_issues.append(f"CFG unlinked nodes: {', '.join(missing_cfg)}")
    if missing_dbc_files:
        fail = True
        fail_issues.append(f"Missing DBC files: {', '.join(missing_dbc_files)}")

    # boundary manager policy advisory
    dbcs = [p for p in (ROOT / "canoe" / "databases").glob("*_can.dbc")]
    bu_tokens: set[str] = set()
    for p in dbcs:
        t = read_text(p)
        for line in re.findall(r"^BU_:\s+(.+)$", t, flags=re.M):
            bu_tokens.update(line.split())
    if "DOMAIN_BOUNDARY_MGR" not in bu_tokens:
        warn_issues.append("DOMAIN_BOUNDARY_MGR not in DBC BU_: keep as rx-only internal policy or add Rx participant explicitly.")

    impl_rows = [
        ["CAPL node files", f"{len(expected_nodes)-len(missing_capl)}/{len(expected_nodes)}", "PASS" if not missing_capl else "FAIL"],
        ["CFG node links", f"{len(expected_nodes)-len(missing_cfg)}/{len(expected_nodes)}", "PASS" if not missing_cfg else "FAIL"],
        ["Split DBC files", f"{len(dbc_paths)-len(missing_dbc_files)}/{len(dbc_paths)}", "PASS" if not missing_dbc_files else "FAIL"],
    ]
    impl_summary = markdown_table(["Item", "Coverage", "Status"], impl_rows)

    gate_result = "FAIL" if fail else ("WARN" if warn_issues else "PASS")
    issue_lines = []
    if fail_issues:
        issue_lines.append("### FAIL")
        for i in fail_issues:
            issue_lines.append(f"- {i}")
    if warn_issues:
        issue_lines.append("### WARN")
        for i in warn_issues:
            issue_lines.append(f"- {i}")
    if not issue_lines:
        issue_lines.append("- 없음")
    issues = "\n".join(issue_lines)

    template = read_text(TEMPLATE_PATH)
    rendered = (
        template.replace("{{generated_at}}", dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        .replace("{{commit_sha}}", git(["rev-parse", "--short", "HEAD"]))
        .replace("{{branch}}", git(["rev-parse", "--abbrev-ref", "HEAD"]))
        .replace("{{gate_result}}", gate_result)
        .replace("{{req_coverage_table}}", req_table)
        .replace("{{func_coverage_table}}", func_table)
        .replace("{{impl_summary}}", impl_summary)
        .replace("{{issues}}", issues)
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(rendered, encoding="utf-8")
    print(f"[doc-code-sync-gate] report written: {REPORT_PATH}")
    print(f"[doc-code-sync-gate] result: {gate_result}")

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
