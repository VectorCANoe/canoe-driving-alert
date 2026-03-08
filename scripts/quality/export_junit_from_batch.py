#!/usr/bin/env python3
"""Export Jenkins-friendly JUnit XML from the Dev2 batch report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree as ET


def _load_json(path: Path) -> dict | None:
    if not path or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact_summary(artifacts: list[dict]) -> tuple[int, int]:
    present = sum(1 for item in artifacts if item.get("exists"))
    missing = len(artifacts) - present
    return present, missing


def build_junit_xml(batch: dict, readiness: dict | None, doctor: dict | None) -> ET.Element:
    steps = batch.get("steps", [])
    artifacts = batch.get("artifacts", [])
    fail_count = sum(1 for step in steps if int(step.get("rc", 1)) != 0)
    present, missing = _artifact_summary(artifacts)

    root = ET.Element(
        "testsuites",
        tests=str(len(steps)),
        failures=str(fail_count),
        errors="0",
        skipped="0",
        time="0",
    )
    suite = ET.SubElement(
        root,
        "testsuite",
        name=f"sdv_operator.verify_batch.{batch.get('phase', 'unknown')}",
        tests=str(len(steps)),
        failures=str(fail_count),
        errors="0",
        skipped="0",
        time="0",
        timestamp=str(batch.get("generated_at", "")),
    )

    props = ET.SubElement(suite, "properties")
    for key in ("run_id", "owner", "run_date", "phase", "status", "pass_count", "fail_count"):
        ET.SubElement(props, "property", name=key, value=str(batch.get(key, "")))
    ET.SubElement(props, "property", name="artifact_present", value=str(present))
    ET.SubElement(props, "property", name="artifact_missing", value=str(missing))
    if readiness:
        ET.SubElement(props, "property", name="readiness_status", value=str(readiness.get("overall_status", "")))
    if doctor:
        ET.SubElement(props, "property", name="doctor_status", value=str(doctor.get("status", "")))

    for step in steps:
        name = str(step.get("name", "unknown-step"))
        rc = int(step.get("rc", 1))
        case = ET.SubElement(
            suite,
            "testcase",
            classname=f"sdv_operator.batch.{batch.get('phase', 'unknown')}",
            name=name,
            time="0",
        )
        if rc != 0:
            failure = ET.SubElement(case, "failure", message=f"{name} failed with rc={rc}", type="StepFailure")
            failure.text = f"step={name}\nrc={rc}\nphase={batch.get('phase', '')}\nrun_id={batch.get('run_id', '')}"

    system_out_lines = [
        f"batch_status={batch.get('status', '')}",
        f"artifacts_present={present}",
        f"artifacts_missing={missing}",
    ]
    if readiness:
        system_out_lines.append(f"readiness_overall={readiness.get('overall_status', '')}")
        for item in readiness.get("missing_items", []):
            system_out_lines.append(f"readiness_missing={item}")
    if doctor:
        system_out_lines.append(f"doctor_status={doctor.get('status', '')}")
        for check in doctor.get("checks", []):
            check_pass = check.get("status", "") == "PASS"
            system_out_lines.append(
                "doctor_check="
                f"{check.get('name', '')}|pass={check_pass}|detail={check.get('detail', '')}"
            )
    for artifact in artifacts:
        system_out_lines.append(
            "artifact="
            f"{artifact.get('path', '')}|exists={artifact.get('exists', False)}|size={artifact.get('size_bytes', 0)}"
        )
    ET.SubElement(suite, "system-out").text = "\n".join(system_out_lines)
    return root


def main() -> int:
    parser = argparse.ArgumentParser(description="Export JUnit XML from Dev2 batch report JSON")
    parser.add_argument("--batch-json", type=Path, required=True)
    parser.add_argument("--run-readiness", type=Path, default=Path("canoe/tmp/reports/verification/run_readiness.json"))
    parser.add_argument("--doctor-report", type=Path, default=Path("canoe/tmp/reports/verification/doctor_report.json"))
    parser.add_argument("--output-xml", type=Path, required=True)
    args = parser.parse_args()

    batch = _load_json(args.batch_json)
    if not batch:
        print(f"[JUNIT] FAIL: batch json not found: {args.batch_json}")
        return 2

    root = build_junit_xml(batch, _load_json(args.run_readiness), _load_json(args.doctor_report))
    args.output_xml.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(args.output_xml, encoding="utf-8", xml_declaration=True)
    print(f"[JUNIT] PASS: {args.output_xml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
