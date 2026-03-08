#!/usr/bin/env python3
"""Validate the SDV Operator packaging contract against manifest + layout constants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.release.layout import (
    EXE_ONEFILE_PATH,
    EXE_ONEFOLDER_DIR,
    PORTABLE_FOLDER_PATH,
    PORTABLE_ZIP_PATH,
    PYINSTALLER_SPEC_ROOT,
    PYINSTALLER_WORK_ROOT,
    ROOT,
)

REPORT_ROOT = ROOT / "canoe" / "tmp" / "reports" / "verification"
JSON_REPORT = REPORT_ROOT / "release_contract_report.json"
MD_REPORT = REPORT_ROOT / "release_contract_report.md"
MANIFEST_PATH = ROOT / "product" / "sdv_operator" / "manifest.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


EXPECTED_ARTIFACTS = {
    "exe_onefolder": rel(EXE_ONEFOLDER_DIR),
    "exe_onefile": rel(EXE_ONEFILE_PATH),
    "portable_folder": rel(PORTABLE_FOLDER_PATH),
    "portable_zip": rel(PORTABLE_ZIP_PATH),
    "pyinstaller_work": rel(PYINSTALLER_WORK_ROOT),
    "pyinstaller_spec": rel(PYINSTALLER_SPEC_ROOT),
}


def main() -> int:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    checks: list[dict[str, str]] = []

    if not MANIFEST_PATH.exists():
        failures.append(f"manifest missing: {MANIFEST_PATH}")
        manifest = {}
    else:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )
        if not ok:
            failures.append(f"{name}: {detail}")

    public_surface = manifest.get("public_surface", [])
    if isinstance(public_surface, list):
        missing = [item for item in public_surface if not (ROOT / str(item)).exists()]
        record(
            "public_surface",
            not missing,
            "all public surface files exist" if not missing else f"missing: {', '.join(missing[:5])}",
        )
    else:
        record("public_surface", False, "manifest.public_surface must be a list")

    for key in ("runtime_modules", "backend_modules"):
        value = manifest.get(key, [])
        if isinstance(value, list):
            missing = [item for item in value if not (ROOT / str(item)).exists()]
            record(
                key,
                not missing,
                "all module paths exist" if not missing else f"missing: {', '.join(missing[:5])}",
            )
        else:
            record(key, False, f"manifest.{key} must be a list")

    scope_doc = manifest.get("packaging_scope_doc", "")
    record(
        "packaging_scope_doc",
        isinstance(scope_doc, str) and bool(scope_doc) and (ROOT / scope_doc).exists(),
        f"found: {scope_doc}" if isinstance(scope_doc, str) and bool(scope_doc) and (ROOT / scope_doc).exists() else "missing packaging scope doc",
    )

    release_artifacts = manifest.get("release_artifacts", {})
    if not isinstance(release_artifacts, dict):
        record("release_artifacts", False, "manifest.release_artifacts must be an object")
    else:
        mismatch: list[str] = []
        for key, expected in EXPECTED_ARTIFACTS.items():
            actual = str(release_artifacts.get(key, ""))
            if actual != expected:
                mismatch.append(f"{key}={actual or '<missing>'} (expected {expected})")
        record(
            "release_artifacts",
            not mismatch,
            "layout contract matches manifest" if not mismatch else "; ".join(mismatch),
        )

    generated_outputs = manifest.get("generated_outputs", [])
    if isinstance(generated_outputs, list):
        bad = [item for item in generated_outputs if not isinstance(item, str) or not item.strip()]
        record(
            "generated_outputs",
            not bad,
            "generated output paths are declared" if not bad else "generated_outputs contains empty or non-string entries",
        )
    else:
        record("generated_outputs", False, "manifest.generated_outputs must be a list")

    status = "PASS" if not failures else "FAIL"
    detail = "release contract is aligned with manifest/layout" if status == "PASS" else failures[0]
    payload = {
        "status": status,
        "detail": detail,
        "checks": checks,
        "artifacts": [rel(JSON_REPORT), rel(MD_REPORT)],
        "manifest": rel(MANIFEST_PATH),
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        "# Release Contract Report",
        "",
        f"- Status: {status}",
        f"- Detail: {detail}",
        f"- Manifest: `{rel(MANIFEST_PATH)}`",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        md_lines.append(f"| {check['name']} | {check['status']} | {check['detail']} |")
    MD_REPORT.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"[RELEASE_CONTRACT] status={status}")
    print(f"[RELEASE_CONTRACT] detail={detail}")
    print(f"[OUT] {rel(JSON_REPORT)}")
    print(f"[OUT] {rel(MD_REPORT)}")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
