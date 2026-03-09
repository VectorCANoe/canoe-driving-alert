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
CHANNEL_ASSIGN_ROOT = ROOT / "canoe" / "cfg" / "channel_assign"


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
    alias_to_canonical = {
        # Validation aliases
        "SIL_TEST_CTRL": "VAL_SCENARIO_CTRL",
        "VEHICLE_BASE_TEST_CTRL": "VAL_BASELINE_CTRL",
        # Canonical migration aliases
        "NAV_CONTEXT_MGR": "NAV_CTX_MGR",
        "CHASSIS_GW": "CHS_GW",
        "ETH_SWITCH": "ETH_SW",
        "DOMAIN_GW_ROUTER": "DOMAIN_ROUTER",
        "BRAKE_CTRL": "BRK_CTRL",
        "STEERING_CTRL": "STEER_CTRL",
        "BCM_AMBIENT_CTRL": "AMBIENT_CTRL",
        "DRIVER_STATE_CTRL": "DRV_STATE_MGR",
        "CLUSTER_BASE_CTRL": "CLU_BASE_CTRL",
        "ENGINE_CTRL": "ENG_CTRL",
        "TRANSMISSION_CTRL": "TCM",
        "ACCL_CTRL": "ACCEL_CTRL",
        "STRG_CTRL": "STEER_CTRL",
    }

    capl_nodes_raw = {
        p.stem
        for p in (ROOT / "canoe" / "src" / "capl").glob("**/*.can")
        if "v1_legacy" not in p.parts and "retired_placeholders" not in p.parts
    }
    capl_nodes = {alias_to_canonical.get(n, n) for n in capl_nodes_raw}
    assign_nodes_raw = {
        p.stem
        for p in CHANNEL_ASSIGN_ROOT.glob("**/*.can")
    }
    assign_nodes = {alias_to_canonical.get(n, n) for n in assign_nodes_raw}
    cfg_nodes_raw: set[str] = set()
    cfg_candidates = [
        ROOT / "canoe" / "cfg" / "CAN_500kBaud_1ch_split.cfg",
        ROOT / "canoe" / "cfg" / "CAN_v2_topology_wip.cfg",
        ROOT / "canoe" / "cfg" / "CAN_500kBaud_1ch.cfg",
        ROOT / "canoe" / "cfg" / "v1_cfg" / "CAN_500kBaud_1ch.cfg",
    ]
    cfg_path = next((p for p in cfg_candidates if p.exists()), cfg_candidates[0])
    if not cfg_path.exists():
        fail = True
        fail_issues.append(
            "Missing CFG file for gate: expected one of "
            + ", ".join([p.name for p in cfg_candidates])
        )
        cfg_text = ""
        cfg_nodes = set()
    else:
        cfg_text = read_text(cfg_path)
        cfg_can_paths = re.findall(r"\"([^\"]+\.can)\"", cfg_text)
        cfg_nodes_raw = {
            Path(x.replace("\\", "/")).stem
            for x in cfg_can_paths
        }
        cfg_nodes = {alias_to_canonical.get(n, n) for n in cfg_nodes_raw}

    # Dynamic expected node set: source + channel_assign are the primary sync surface.
    expected_nodes = capl_nodes | assign_nodes

    dbc_paths = [
        ROOT / "canoe" / "databases" / "chassis_can.dbc",
        ROOT / "canoe" / "databases" / "powertrain_can.dbc",
        ROOT / "canoe" / "databases" / "body_can.dbc",
        ROOT / "canoe" / "databases" / "infotainment_can.dbc",
        ROOT / "canoe" / "databases" / "adas_can.dbc",
        ROOT / "canoe" / "databases" / "eth_backbone_can_stub.dbc",
    ]
    missing_dbc_files = [p.name for p in dbc_paths if not p.exists()]

    missing_capl = sorted(expected_nodes - capl_nodes)
    missing_assign = sorted(expected_nodes - assign_nodes)
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
    if missing_assign:
        fail = True
        fail_issues.append(f"channel_assign missing nodes: {', '.join(missing_assign)}")
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
    legacy_name_hits = sorted((set(alias_to_canonical.keys()) & capl_nodes_raw) | (set(alias_to_canonical.keys()) & cfg_nodes_raw))
    if legacy_name_hits:
        warn_issues.append(
            "Legacy validation labels detected (allowed by alias policy, GUI rename pending): "
            + ", ".join(legacy_name_hits)
        )
    cfg_runtime_only = sorted(cfg_nodes - expected_nodes)
    cfg_runtime_missing = sorted(expected_nodes - cfg_nodes)
    if cfg_runtime_only:
        warn_issues.append(
            "CFG runtime has legacy-only node links (GUI migration pending): "
            + ", ".join(cfg_runtime_only[:12])
        )
    if cfg_runtime_missing:
        warn_issues.append(
            f"CFG runtime links are partial vs channel_assign/source ({len(cfg_nodes)}/{len(expected_nodes)}): "
            + ", ".join(cfg_runtime_missing[:12])
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
        ["channel_assign links", f"{len(expected_nodes)-len(missing_assign)}/{len(expected_nodes)}", "PASS" if not missing_assign else "FAIL"],
        ["CFG runtime links", f"{len(cfg_nodes)}/{len(expected_nodes)}", "PASS" if len(cfg_nodes) == len(expected_nodes) else "WARN"],
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
        issue_lines.append("- 없음")
    issues = "\n".join(issue_lines)

    if TEMPLATE_PATH.exists():
        template = read_text(TEMPLATE_PATH)
    else:
        template = """# Doc-Code Sync Report

- Generated At: {{generated_at}}
- Branch: {{branch}}
- Commit: {{commit_sha}}
- Gate Result: {{gate_result}}

## Req Coverage
{{req_coverage_table}}

## Func Coverage
{{func_coverage_table}}

## Implementation Summary
{{impl_summary}}

## Issues
{{issues}}
"""
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
