#!/usr/bin/env python3
"""CLI readiness gate.

Purpose:
- verify canonical command contract is stable and machine-readable
- verify core command groups are executable/help-ready
- verify packaging entrypoint exists (`sdv = sdv_cli:main`)
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


ROOT = Path(__file__).resolve().parents[2]
RUN_PY = ROOT / "scripts" / "run.py"
BUILD_EXE_PY = ROOT / "scripts" / "release" / "build_sdv_exe.py"
BUILD_PORTABLE_PY = ROOT / "scripts" / "release" / "build_portable_bundle.py"
PYPROJECT = ROOT / "pyproject.toml"
CAMPAIGN_PROFILES = ROOT / "product" / "sdv_operator" / "config" / "campaign_profiles.json"
VERIFICATION_PACK_MATRIX = ROOT / "product" / "sdv_operator" / "config" / "verification_pack_matrix.json"
TEST_SUITES_README = ROOT / "canoe" / "tests" / "modules" / "test_suites" / "README.md"
TEST_ASSET_MAPPING = ROOT / "canoe" / "docs" / "verification" / "test-asset-mapping.md"
OUT_DIR = ROOT / "canoe" / "tmp" / "reports" / "verification"
OUT_JSON = OUT_DIR / "cli_readiness_gate.json"
OUT_MD = OUT_DIR / "cli_readiness_gate.md"
READINESS_RUN_ID = "CLI_READINESS_REL"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def run_check(cmd: list[str], name: str) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    ok = proc.returncode == 0
    details = (proc.stdout or proc.stderr or "").strip()
    return ok, f"{name}: {'PASS' if ok else 'FAIL'} (rc={proc.returncode})" + (f"\n{details}" if details else "")


def check_pyproject_entrypoint() -> tuple[bool, str]:
    if tomllib is None:
        return False, "pyproject check: FAIL (tomllib unavailable)"
    if not PYPROJECT.exists():
        return False, "pyproject check: FAIL (pyproject.toml missing)"

    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    entry = scripts.get("sdv")
    if entry == "sdv_cli:main":
        return True, "pyproject check: PASS (sdv = sdv_cli:main)"
    return False, f"pyproject check: FAIL (sdv entry is '{entry}')"


def check_no_repo_root_leak(path: Path, name: str) -> tuple[bool, str]:
    if not path.exists():
        return False, f"{name}: FAIL ({rel(path)} missing)"
    text = path.read_text(encoding="utf-8", errors="ignore")
    root_token = str(ROOT).replace("\\", "/")
    ok = root_token not in text
    detail = f"{name}: {'PASS' if ok else 'FAIL'} ({rel(path)})"
    if not ok:
        detail += f"\ncontains absolute repo root: {root_token}"
    return ok, detail


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _count_assign_assets(assign_folder: str) -> int:
    folder = ROOT / assign_folder
    if not folder.exists():
        return -1
    return len([item for item in folder.iterdir() if item.is_file()])


def _count_mapping_rows(prefix: str) -> int:
    text = TEST_ASSET_MAPPING.read_text(encoding="utf-8")
    return len(re.findall(rf"^\| `{prefix}_\d+` \|", text, flags=re.MULTILINE))


def _count_official_rows(path: Path, prefix: str) -> int:
    text = path.read_text(encoding="utf-8")
    if prefix == "UT":
        return len(re.findall(r"^\|[^|]*\|[^|]*\|\s*UT_\d+\b", text, flags=re.MULTILINE))
    return len(re.findall(rf"^\| {prefix}_\d+ \|", text, flags=re.MULTILINE))


def _parse_suite_readme_counts() -> dict[str, int]:
    text = TEST_SUITES_README.read_text(encoding="utf-8")
    out: dict[str, int] = {}
    for suite_id, count in re.findall(r"-\s+(TS_CANOE_[A-Z_]+)\s+:\s+(\d+)\s+assets", text):
        out[suite_id.strip()] = int(count)
    return out


def check_active_suite_sync() -> tuple[bool, str]:
    if not CAMPAIGN_PROFILES.exists() or not VERIFICATION_PACK_MATRIX.exists():
        return False, "active suite sync: FAIL (campaign_profiles.json or verification_pack_matrix.json missing)"

    packs_raw = _load_json(VERIFICATION_PACK_MATRIX)
    profiles_raw = _load_json(CAMPAIGN_PROFILES)
    packs = {
        str(item.get("pack_id", "")).strip(): item
        for item in packs_raw.get("packs", [])
        if isinstance(item, dict) and str(item.get("pack_id", "")).strip()
    }
    profiles = {
        str(item.get("profile_id", "")).strip(): item
        for item in profiles_raw.get("profiles", [])
        if isinstance(item, dict) and str(item.get("profile_id", "")).strip()
    }
    suite_readme_counts = _parse_suite_readme_counts()

    expected = {
        "UT": {
            "profile_id": "ut_active_baseline",
            "pack_id": "ts_canoe_ut_active_baseline",
            "title": "UT Active Baseline",
            "official_doc": ROOT / "driving-alert-workproducts" / "05_Unit_Test.md",
        },
        "IT": {
            "profile_id": "it_active_baseline",
            "pack_id": "ts_canoe_it_active_baseline",
            "title": "IT Active Baseline",
            "official_doc": ROOT / "driving-alert-workproducts" / "06_Integration_Test.md",
        },
        "ST": {
            "profile_id": "st_active_baseline",
            "pack_id": "ts_canoe_st_active_baseline",
            "title": "ST Active Baseline",
            "official_doc": ROOT / "driving-alert-workproducts" / "07_System_Test.md",
        },
        "FULL": {
            "profile_id": "full_active_baseline",
            "pack_id": "ts_canoe_full_active_baseline",
            "title": "FULL Active Baseline",
        },
    }

    failures: list[str] = []
    per_tier_counts: dict[str, int] = {}

    for tier, rule in expected.items():
        pack = packs.get(rule["pack_id"])
        profile = profiles.get(rule["profile_id"])
        if not isinstance(pack, dict):
            failures.append(f"{tier}: missing pack {rule['pack_id']}")
            continue
        if not isinstance(profile, dict):
            failures.append(f"{tier}: missing profile {rule['profile_id']}")
            continue

        pack_title = str(pack.get("title", "")).strip()
        profile_title = str(profile.get("title", "")).strip()
        if pack_title != rule["title"]:
            failures.append(f"{tier}: pack title mismatch ({pack_title})")
        if profile_title != rule["title"]:
            failures.append(f"{tier}: profile title mismatch ({profile_title})")

        pack_asset_count = int(pack.get("asset_count", 0) or 0)
        assign_count = _count_assign_assets(str(pack.get("assign_folder", "")))
        if assign_count < 0:
            failures.append(f"{tier}: assign folder missing ({pack.get('assign_folder', '')})")
        elif assign_count != pack_asset_count:
            failures.append(f"{tier}: asset_count {pack_asset_count} != assign folder count {assign_count}")

        if str(profile.get("pack_id", "")).strip() != rule["pack_id"]:
            failures.append(f"{tier}: profile pack_id mismatch ({profile.get('pack_id')})")

        if tier in {"UT", "IT", "ST"}:
            suite_id = str(pack.get("suite_id", "")).strip()
            readme_count = suite_readme_counts.get(suite_id)
            if readme_count is None:
                failures.append(f"{tier}: suite README count missing ({suite_id})")
            elif readme_count != pack_asset_count:
                failures.append(f"{tier}: suite README count {readme_count} != asset_count {pack_asset_count}")

            mapping_count = _count_mapping_rows(tier)
            if mapping_count != pack_asset_count:
                failures.append(f"{tier}: test-asset-mapping rows {mapping_count} != asset_count {pack_asset_count}")

            official_doc = rule["official_doc"]
            official_doc_ref = str(pack.get("official_doc_ref", "")).strip()
            if rel(official_doc) != official_doc_ref:
                failures.append(f"{tier}: official_doc_ref mismatch ({official_doc_ref})")
            if str(profile.get("contract_ref", "")).strip() != rel(official_doc):
                failures.append(f"{tier}: profile contract_ref mismatch ({profile.get('contract_ref')})")

            official_rows = _count_official_rows(official_doc, tier)
            if official_rows != pack_asset_count:
                failures.append(f"{tier}: official doc rows {official_rows} != asset_count {pack_asset_count}")

            if str(pack.get("closeout_role", "")).strip() != "official":
                failures.append(f"{tier}: pack closeout_role must be official")
            if str(profile.get("closeout_role", "")).strip() != "official":
                failures.append(f"{tier}: profile closeout_role must be official")

            per_tier_counts[tier] = pack_asset_count
        else:
            expected_full = sum(per_tier_counts.get(key, 0) for key in ("UT", "IT", "ST"))
            if expected_full and pack_asset_count != expected_full:
                failures.append(f"FULL: asset_count {pack_asset_count} != UT+IT+ST total {expected_full}")
            if str(pack.get("closeout_role", "")).strip() != "regression_only":
                failures.append("FULL: pack closeout_role must be regression_only")
            if str(profile.get("closeout_role", "")).strip() != "regression_only":
                failures.append("FULL: profile closeout_role must be regression_only")
            contract_ref = str(profile.get("contract_ref", "")).strip()
            if contract_ref != "canoe/docs/verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md":
                failures.append(f"FULL: contract_ref mismatch ({contract_ref})")

    if failures:
        return False, "active suite sync: FAIL\n" + "\n".join(f"- {item}" for item in failures)
    return True, "active suite sync: PASS (assign folders, suite README, test-asset-mapping, 05/06/07, product config aligned)"


def main() -> int:
    checks: list[tuple[bool, str]] = []
    py = sys.executable

    checks.append(run_check([py, str(RUN_PY), "--help"], "run.py help"))
    checks.append(run_check([py, str(RUN_PY), "scenario", "--help"], "scenario group help"))
    checks.append(run_check([py, str(RUN_PY), "verify", "--help"], "verify group help"))
    checks.append(run_check([py, str(RUN_PY), "gate", "--help"], "gate group help"))
    checks.append(run_check([py, str(RUN_PY), "package", "--help"], "package group help"))
    checks.append(run_check([py, str(RUN_PY), "contract", "--json"], "contract json"))
    checks.append(run_check([py, str(RUN_PY), "artifact", "list", "--scope", "source", "--json"], "artifact source json"))
    checks.append(run_check([py, str(RUN_PY), "verify", "status", "--run-id", READINESS_RUN_ID], "run readiness smoke"))
    checks.append(check_no_repo_root_leak(OUT_DIR / "run_readiness.json", "run readiness json path hygiene"))
    checks.append(check_no_repo_root_leak(OUT_DIR / "run_readiness.md", "run readiness md path hygiene"))
    checks.append(run_check([py, str(RUN_PY), "verify", "bind-doc", "--run-id", READINESS_RUN_ID], "doc binding smoke"))
    checks.append(check_no_repo_root_leak(OUT_DIR / "doc_binding_bundle.json", "doc binding json path hygiene"))
    checks.append(check_no_repo_root_leak(OUT_DIR / "doc_binding_bundle.md", "doc binding md path hygiene"))
    checks.append(run_check([py, str(RUN_PY), "verify", "fill-template", "--run-id", READINESS_RUN_ID], "doc fill smoke"))
    checks.append(check_no_repo_root_leak(OUT_DIR / "doc_fill_template.md", "doc fill md path hygiene"))
    checks.append(run_check([py, str(RUN_PY), "verify", "surface-bundle"], "surface bundle smoke"))
    checks.append(run_check([py, str(BUILD_EXE_PY), "--help"], "build_sdv_exe backend import"))
    checks.append(run_check([py, str(BUILD_PORTABLE_PY), "--help"], "build_portable_bundle backend import"))
    checks.append(check_pyproject_entrypoint())
    checks.append(check_active_suite_sync())

    # Validate canonical contract includes required commands.
    proc = subprocess.run([py, str(RUN_PY), "contract", "--json"], cwd=ROOT, capture_output=True, text=True)
    contract_ok = False
    contract_detail = "contract contents: FAIL (invalid json)"
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            canonical = data.get("canonical", [])
            required = [
                "python scripts/run.py scenario run --id <0..255>",
                "python scripts/run.py verify prepare --run-id <YYYYMMDD_HHMM>",
                "python scripts/run.py verify insight --run-id <YYYYMMDD_HHMM>",
                "python scripts/run.py verify bind-doc --run-id <YYYYMMDD_HHMM>",
                "python scripts/run.py verify fill-template --run-id <YYYYMMDD_HHMM>",
                "python scripts/run.py verify status --run-id <YYYYMMDD_HHMM>",
                "python scripts/run.py verify finalize --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
                "python scripts/run.py gate doc-sync",
                "python scripts/run.py gate cli-readiness",
                "python scripts/run.py package build-exe --mode onefolder",
            ]
            missing = [item for item in required if item not in canonical]
            if not missing:
                contract_ok = True
                contract_detail = "contract contents: PASS"
            else:
                contract_detail = f"contract contents: FAIL (missing: {missing})"
        except json.JSONDecodeError as ex:
            contract_detail = f"contract contents: FAIL (json error: {ex})"
    checks.append((contract_ok, contract_detail))

    passed = sum(1 for ok, _ in checks if ok)
    failed = len(checks) - passed
    result = "PASS" if failed == 0 else "FAIL"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "result": result,
        "passed": passed,
        "failed": failed,
        "checks": [{"ok": ok, "detail": detail} for ok, detail in checks],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# CLI Readiness Gate Report",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Result: `{result}`",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        "",
        "## Checks",
    ]
    for ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        lines.append(f"- [{status}] {detail.splitlines()[0]}")

    if failed:
        lines += ["", "## Failure Details"]
        for ok, detail in checks:
            if not ok:
                lines.append("```text")
                lines.append(detail)
                lines.append("```")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[CLI_GATE] result={result} passed={passed} failed={failed}")
    print(f"[OUT] {rel(OUT_JSON)}")
    print(f"[OUT] {rel(OUT_MD)}")
    return 0 if result == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
