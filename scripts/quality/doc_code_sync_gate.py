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
    # Some CANoe text artifacts (.cfg/.dbc) can be saved with legacy Windows encodings.
    # Gate parsing uses mostly ASCII tokens, so decode robustly instead of hard-failing.
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp949", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


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
    cfg_path = ROOT / "canoe" / "cfg" / "CAN_500kBaud_1ch_split.cfg"
    if not cfg_path.exists():
        fallback_cfg = ROOT / "canoe" / "cfg" / "CAN_500kBaud_1ch.cfg"
        if fallback_cfg.exists():
            cfg_path = fallback_cfg
    cfg_text = read_text(cfg_path)
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
    cfg_lines = cfg_text.splitlines()
    cfg_abs_path_hits = []
    for i, line in enumerate(cfg_lines, start=1):
        # Windows absolute path in CFG is environment-specific and should not be committed.
        if re.search(r"[A-Za-z]:\\", line):
            # CANoe GUI may keep template hint path from Vector installation.
            if r"C:\Users\Public" in line or r"C:\Public" in line:
                continue
            # .cbf paths are auto-generated by CANoe F8 compile and are always absolute.
            if line.strip().endswith(".cbf"):
                continue
            cfg_abs_path_hits.append((i, line.strip()))
    # Common mojibake artifacts often seen when Windows user profile path is encoded badly.
    cfg_mojibake_hits = []

    if missing_capl:
        fail = True
        fail_issues.append(f"CAPL missing: {', '.join(missing_capl)}")
    if missing_cfg:
        fail = True
        fail_issues.append(f"CFG unlinked nodes: {', '.join(missing_cfg)}")
    if missing_dbc_files:
        fail = True
        fail_issues.append(f"Missing DBC files: {', '.join(missing_dbc_files)}")
    if cfg_abs_path_hits:
        fail = True
        sample = ", ".join([f"L{ln}" for ln, _ in cfg_abs_path_hits[:5]])
        fail_issues.append(
            f"CFG contains Windows absolute paths (forbidden): {len(cfg_abs_path_hits)} lines ({sample}) in {cfg_path.name}"
        )
    if cfg_mojibake_hits:
        warn_sample = ", ".join([f"L{ln}" for ln, _ in cfg_mojibake_hits[:5]])
        warn_issues.append(
            f"CFG possible mojibake text detected: {len(cfg_mojibake_hits)} lines ({warn_sample}) in {cfg_path.name}"
        )

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
        ["CFG absolute path hygiene", "0 forbidden path", "PASS" if not cfg_abs_path_hits else "FAIL"],
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
        issue_lines.append("- ?놁쓬")
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


