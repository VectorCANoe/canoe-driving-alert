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
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


ROOT = Path(__file__).resolve().parents[2]
RUN_PY = ROOT / "scripts" / "run.py"
PYPROJECT = ROOT / "pyproject.toml"
OUT_DIR = ROOT / "canoe" / "tmp" / "reports" / "verification"
OUT_JSON = OUT_DIR / "cli_readiness_gate.json"
OUT_MD = OUT_DIR / "cli_readiness_gate.md"


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


def main() -> int:
    checks: list[tuple[bool, str]] = []
    py = sys.executable

    checks.append(run_check([py, str(RUN_PY), "--help"], "run.py help"))
    checks.append(run_check([py, str(RUN_PY), "verify", "--help"], "verify group help"))
    checks.append(run_check([py, str(RUN_PY), "gate", "--help"], "gate group help"))
    checks.append(run_check([py, str(RUN_PY), "package", "--help"], "package group help"))
    checks.append(run_check([py, str(RUN_PY), "contract", "--json"], "contract json"))
    checks.append(check_pyproject_entrypoint())

    # Validate canonical contract includes required commands.
    proc = subprocess.run([py, str(RUN_PY), "contract", "--json"], cwd=ROOT, capture_output=True, text=True)
    contract_ok = False
    contract_detail = "contract contents: FAIL (invalid json)"
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            canonical = data.get("canonical", [])
            required = [
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
    print(f"[OUT] {OUT_JSON}")
    print(f"[OUT] {OUT_MD}")
    return 0 if result == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
