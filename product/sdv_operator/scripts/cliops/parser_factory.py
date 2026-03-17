from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Callable, Mapping

from cliops.common import default_campaign_id


HandlerMap = Mapping[str, Callable]


VISIBLE_TOPLEVEL_COMMANDS = [
    "start",
    "doctor",
    "capl",
    "canoe",
    "tui",
    "shell",
    "scenario",
    "verify",
    "evidence",
    "gate",
    "artifact",
    "package",
    "release",
    "contract",
]

COMPAT_TOPLEVEL_COMMANDS = [
    "wizard",
    "scenario-run",
    "interactive",
    "verify-prepare",
    "verify-batch",
    "verify-smoke",
    "verify-post-run",
    "verify-fill-score",
    "verify-insight",
    "verify-bind-doc",
    "verify-fill-template",
    "verify-status",
    "verify-surface-bundle",
    "verify-finalize",
    "gate-doc-sync",
    "gate-cfg-hygiene",
    "gate-capl-sync",
    "gate-multibus-dbc",
    "gate-cli-readiness",
    "package-build-exe",
    "package-bundle-portable",
    "go",
    "demo",
    "precheck",
    "mstart",
    "mstop",
    "mstatus",
]

TOPLEVEL_COMMANDS = [*VISIBLE_TOPLEVEL_COMMANDS, *COMPAT_TOPLEVEL_COMMANDS]


def _add_hidden_parser(subparsers: argparse._SubParsersAction, name: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=argparse.SUPPRESS)
    subparsers._choices_actions = [
        action for action in subparsers._choices_actions if getattr(action, "dest", None) != name
    ]
    return parser


def add_verify_prepare_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.set_defaults(func=handlers["cmd_verify_prepare"], operator_command_id="verify.prepare")


def add_verify_batch_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--campaign-id", default=default_campaign_id(), help="Campaign ID, e.g. CMP_20260310")
    p.add_argument("--profile-id", default="", help="Campaign profile ID, e.g. ut_active_baseline")
    p.add_argument("--pack-id", default="", help="Verification pack ID, e.g. ts_canoe_it_active_baseline")
    p.add_argument("--suite-id", default="", help="Active suite ID, e.g. TS_CANOE_IT_ACTIVE_BASELINE")
    p.add_argument("--assign-folder", default="", help="GUI import wrapper folder, e.g. canoe/tests/modules/test_units/assign/IT_ACTIVE_BASELINE")
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--phase", choices=["pre", "post", "full"], default="pre")
    p.add_argument("--surface-scope", default="ALL", help="Surface ECU scope label, e.g. ALL / BCM / ADAS")
    p.add_argument("--repeat-count", type=int, default=1, help="Planned repeat count for this campaign")
    p.add_argument("--duration-minutes", type=int, default=0, help="Planned campaign duration in minutes (0 means not fixed)")
    p.add_argument("--interval-seconds", type=int, default=0, help="Planned interval between repeats in seconds")
    p.add_argument("--skip-gates", action="store_true", help="Skip all gate steps in pre/full phase")
    p.add_argument("--stop-on-fail", action="store_true", help="Stop immediately at first failed step")
    p.add_argument(
        "--execute-native-tier",
        default="",
        choices=["", "UT", "IT", "ST", "FULL"],
        help="Optionally execute one native CANoe test configuration during pre/full phase",
    )
    p.add_argument(
        "--native-timeout-seconds",
        type=int,
        default=1800,
        help="Timeout for native test configuration execution",
    )
    p.add_argument(
        "--native-poll-ms",
        type=int,
        default=500,
        help="Polling interval for native test configuration execution",
    )
    p.add_argument(
        "--native-restart-if-running",
        action="store_true",
        help="Stop and restart the target native configuration if it is already running",
    )
    p.add_argument(
        "--native-fail-on-verdict",
        action="store_true",
        help="Return non-zero when native execution completes with failed verdict",
    )
    p.add_argument(
        "--report-formats",
        default="json,md",
        help="Comma-separated report formats: json,md,csv,junit (default: json,md)",
    )
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
        help="Batch summary JSON output path",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.md"),
        help="Batch summary markdown output path",
    )
    p.add_argument(
        "--output-csv",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
        help="Batch summary CSV output path (optional format)",
    )
    p.add_argument(
        "--output-junit",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.junit.xml"),
        help="Batch summary JUnit XML output path (optional format)",
    )
    p.set_defaults(func=handlers["cmd_verify_batch"], operator_command_id="verify.batch")


def add_verify_smoke_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.set_defaults(func=handlers["cmd_verify_smoke"], operator_command_id="verify.smoke")


def add_verify_collect_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--tier", required=True, choices=["UT", "IT", "ST", "FULL"])
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument("--raw-log-source", default="", help="Optional raw log source override")
    p.add_argument("--allow-missing-raw-log", action="store_true")
    p.set_defaults(func=handlers["cmd_verify_collect"], operator_command_id="verify.collect_native")


def add_verify_post_run_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument("--raw-log-source", default="", help="Optional raw log source override")
    p.add_argument("--allow-missing-raw-log", action="store_true")
    p.add_argument("--baseline-csv", default="", help="Optional baseline scored CSV for regression comparison")
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.set_defaults(func=handlers["cmd_verify_post_run"], operator_command_id="verify.post_run")


def add_verify_report_tools_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--json", action="store_true", help="Print tooling payload as JSON")
    p.set_defaults(func=handlers["cmd_verify_report_tools"], operator_command_id="verify.report_tools")


def add_verify_report_bundle_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--tier", default="", choices=["", "UT", "IT", "ST", "FULL"], help="Tier contract to resolve native summary report")
    p.add_argument("--report", default="", help="Explicit .vtestreport path override")
    p.add_argument("--include-pdf", action="store_true", help="Also export official PDF via ReportViewerCli")
    p.add_argument("--json", action="store_true", help="Print merged bundle JSON")
    p.set_defaults(func=handlers["cmd_verify_report_bundle"], operator_command_id="verify.report_bundle")


def add_verify_quick_args(
    p: argparse.ArgumentParser,
    handlers: HandlerMap,
    default_run_id: Callable[[], str],
) -> None:
    p.add_argument("--run-id", default=default_run_id(), help="Run ID, e.g. 20260306_1930")
    p.add_argument("--owner", default="DEV2")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.set_defaults(func=handlers["cmd_verify_quick"], operator_command_id="verify.quick_verify")


def add_verify_fill_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--baseline-csv", default="", help="Optional baseline scored CSV for regression comparison")
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.set_defaults(func=handlers["cmd_verify_fill_score"], operator_command_id="verify.fill_score")


def add_verify_insight_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for trend comparison")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/run_insight_report.md",
        help="Run-level insight markdown output path",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/run_insight_report.json",
        help="Run-level insight JSON output path",
    )
    p.set_defaults(func=handlers["cmd_verify_insight"], operator_command_id="verify.insight")


def add_verify_bind_doc_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-alert-workproducts)",
    )
    p.add_argument(
        "--output-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="05/06/07 doc binding CSV output path",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="05/06/07 doc binding JSON output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="05/06/07 doc binding markdown output path",
    )
    p.set_defaults(func=handlers["cmd_verify_bind_doc"], operator_command_id="verify.bind_doc")


def add_verify_fill_template_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-alert-workproducts)",
    )
    p.add_argument("--owner-fallback", default="TBD", help="Fallback owner for READY rows")
    p.add_argument("--date-fallback", default=dt.date.today().isoformat(), help="Fallback date for READY rows")
    p.add_argument(
        "--binding-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="Binding CSV output path",
    )
    p.add_argument(
        "--binding-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="Binding JSON output path",
    )
    p.add_argument(
        "--binding-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="Binding markdown output path",
    )
    p.add_argument(
        "--output-csv",
        default="canoe/tmp/reports/verification/doc_fill_template.csv",
        help="Doc fill template CSV output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/doc_fill_template.md",
        help="Doc fill template markdown output path",
    )
    p.set_defaults(func=handlers["cmd_verify_fill_template"], operator_command_id="verify.fill_template")


def add_verify_finalize_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--tiers", nargs="+", default=["UT", "IT", "ST"], choices=["UT", "IT", "ST"])
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--owner-fallback", default="")
    p.add_argument("--date-fallback", default="")
    p.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for insight comparison")
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-alert-workproducts)",
    )
    p.add_argument(
        "--insight-md",
        default="canoe/tmp/reports/verification/run_insight_report.md",
        help="Run-level insight markdown output path",
    )
    p.add_argument(
        "--insight-json",
        default="canoe/tmp/reports/verification/run_insight_report.json",
        help="Run-level insight JSON output path",
    )
    p.add_argument(
        "--binding-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="Doc binding CSV output path",
    )
    p.add_argument(
        "--binding-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="Doc binding JSON output path",
    )
    p.add_argument(
        "--binding-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="Doc binding markdown output path",
    )
    p.add_argument(
        "--fill-csv",
        default="canoe/tmp/reports/verification/doc_fill_template.csv",
        help="Doc fill template CSV output path",
    )
    p.add_argument(
        "--fill-md",
        default="canoe/tmp/reports/verification/doc_fill_template.md",
        help="Doc fill template markdown output path",
    )
    p.set_defaults(func=handlers["cmd_verify_finalize"], operator_command_id="verify.finalize")


def add_package_clean_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--scope", choices=["staging", "archive", "build", "all"], default="staging")
    p.add_argument("--run-id", default="", help="Archive run ID to delete")
    p.add_argument("--phase", choices=["pre", "post", "full"], default="", help="Optional archive phase")
    p.add_argument("--all-runs", action="store_true", help="Delete the entire archive root")
    p.add_argument("--yes", action="store_true", help="Apply deletion. Without this flag, preview only.")
    p.set_defaults(func=handlers["cmd_package_clean"], operator_command_id="package.clean")


def add_artifact_list_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--scope", choices=["staging", "archive", "source", "build"], default="staging")
    p.add_argument("--run-id", default="", help="Archive run ID or evidence run ID")
    p.add_argument("--phase", choices=["pre", "post", "full"], default="", help="Optional archive phase")
    p.add_argument("--latest", action="store_true", help="Resolve the most recent archive run automatically")
    p.add_argument("--json", action="store_true", help="Print JSON instead of plain text")
    p.set_defaults(func=handlers["cmd_artifact_list"], operator_command_id="artifact.list")


def add_artifact_open_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument(
        "--target",
        choices=[
            "staging-root",
            "batch-report",
            "run-insight",
            "doc-binding-bundle",
            "doc-fill-template",
            "surface-bundle",
            "readiness",
            "doctor",
            "surface-inventory",
            "unit-test-doc",
            "integration-test-doc",
            "system-test-doc",
            "test-asset-mapping",
            "active-test-units-guide",
            "active-test-suites-guide",
            "execution-guide",
            "closeout-standard",
            "evidence-policy",
            "native-test-portfolio",
            "native-testcase-blueprints",
            "network-gateway-pack",
            "verification-pack-matrix",
            "campaign-profiles",
            "capability-matrix-json",
            "traceability-profile",
            "artifact-layout",
            "phase-policy",
            "manifest",
            "commands-doc",
            "maintenance-doc",
            "results-doc",
            "packaging-doc",
            "ci-bridge-doc",
            "role-boundary-doc",
            "capability-matrix-doc",
            "incoming-root",
            "incoming-trace-root",
            "incoming-logging-root",
            "jenkinsfile-sample",
            "build-root",
            "archive-run",
            "reports-dir",
            "surface-dir",
            "native-reports",
            "evidence-dir",
            "supplementary-trace",
            "supplementary-logging",
            "execution-manifest",
        ],
        required=True,
        help="Artifact target to resolve and open",
    )
    p.add_argument("--run-id", default="", help="Archive run ID")
    p.add_argument("--phase", choices=["pre", "post", "full"], default="", help="Optional archive phase")
    p.add_argument("--latest", action="store_true", help="Resolve the most recent archive run automatically")
    p.add_argument("--print-only", action="store_true", help="Print resolved path only")
    p.set_defaults(func=handlers["cmd_artifact_open"], operator_command_id="artifact.open")


def add_verify_status_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/run_readiness.json",
        help="Run readiness JSON output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/run_readiness.md",
        help="Run readiness markdown output path",
    )
    p.set_defaults(func=handlers["cmd_verify_status"], operator_command_id="verify.run_readiness_status")


def add_verify_surface_bundle_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument(
        "--inventory-json",
        type=Path,
        default=Path("product/sdv_operator/config/surface_ecu_inventory.json"),
        help="Surface ECU inventory JSON path",
    )
    p.add_argument(
        "--traceability-json",
        type=Path,
        default=Path("product/sdv_operator/config/surface_traceability_profile.json"),
        help="Surface ECU traceability profile JSON path",
    )
    p.add_argument(
        "--doctor-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doctor_report.json"),
        help="Doctor report JSON path",
    )
    p.add_argument(
        "--readiness-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/run_readiness.json"),
        help="Run readiness JSON path",
    )
    p.add_argument(
        "--batch-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
        help="Batch report JSON path",
    )
    p.add_argument(
        "--smoke-csv",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev_completeness_smoke.csv"),
        help="Smoke CSV path used to collect executed scenario IDs",
    )
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/surface_evidence_bundle.json"),
        help="Surface evidence bundle JSON output path",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/surface_evidence_bundle.md"),
        help="Surface evidence bundle Markdown output path",
    )
    p.add_argument(
        "--surface-dir",
        type=Path,
        default=Path("canoe/tmp/reports/verification/surface"),
        help="Per-surface bundle output root",
    )
    p.set_defaults(func=handlers["cmd_verify_surface_bundle"], operator_command_id="verify.surface_bundle")


def add_scenario_run_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--id", type=int, required=True, help="Scenario ID (0..255)")
    p.add_argument("--namespace", default="Test", help="System variable namespace")
    p.add_argument(
        "--var",
        default="scenarioCommand",
        choices=["scenarioCommand", "testScenario"],
        help="Target sysvar name",
    )
    p.add_argument("--ack-var", default="scenarioCommandAck", help="Ack sysvar name")
    p.add_argument("--wait-ack-ms", type=int, default=1200, help="Ack wait timeout in ms")
    p.add_argument("--poll-ms", type=int, default=20, help="Ack poll interval in ms")
    p.add_argument("--no-ensure-running", action="store_true", help="Do not auto-start measurement")
    p.set_defaults(func=handlers["cmd_scenario_run"], operator_command_id="operate.scenario_trigger")


def add_start_demo_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--id", type=int, default=4, help="Scenario ID (0..255), default=4")
    p.add_argument(
        "--var",
        default="scenarioCommand",
        choices=["scenarioCommand", "testScenario"],
        help="Target sysvar name",
    )
    p.add_argument("--wait-ack-ms", type=int, default=1200, help="Ack wait timeout in ms")
    p.add_argument("--poll-ms", type=int, default=20, help="Ack poll interval in ms")
    p.add_argument("--no-ensure-running", action="store_true", help="Do not auto-start measurement")
    p.set_defaults(func=handlers["cmd_start_demo"], operator_command_id="operate.scenario_trigger")


def add_start_precheck_args(
    p: argparse.ArgumentParser,
    handlers: HandlerMap,
    default_run_id: Callable[[], str],
) -> None:
    p.add_argument("--run-id", default=default_run_id(), help="Run ID, e.g. 20260308_1900")
    p.add_argument("--campaign-id", default=default_campaign_id(), help="Campaign ID, e.g. CMP_20260310")
    p.add_argument("--owner", default="DEV2")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--surface-scope", default="ALL", help="Surface ECU scope label, e.g. ALL / BCM / ADAS")
    p.add_argument("--repeat-count", type=int, default=1, help="Planned repeat count for this precheck")
    p.add_argument("--duration-minutes", type=int, default=0, help="Planned campaign duration in minutes (0 means not fixed)")
    p.add_argument("--interval-seconds", type=int, default=0, help="Planned interval between repeats in seconds")
    p.add_argument("--skip-gates", action="store_true", help="Skip all gates in precheck")
    p.add_argument("--stop-on-fail", action="store_true", help="Stop at first failed step")
    p.add_argument(
        "--report-formats",
        default="json,md",
        help="Comma-separated formats: json,md,csv,junit (default: json,md)",
    )
    p.set_defaults(func=handlers["cmd_start_precheck"], operator_command_id="verify.precheck_batch")


def add_start_preset_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument(
        "name",
        choices=["quickstart", "verify-pack", "portable-release"],
        help="Preset workflow name",
    )
    p.set_defaults(func=handlers["cmd_start_preset"])


def add_doctor_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--ensure-running", action="store_true", help="Auto-start measurement if stopped")
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doctor_report.json"),
        help="Doctor report JSON output path",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doctor_report.md"),
        help="Doctor report markdown output path",
    )
    p.set_defaults(func=handlers["cmd_doctor"], operator_command_id="inspect.environment_doctor")


def add_capl_sysvar_get_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--namespace", required=True, help="System variable namespace")
    p.add_argument("--var", required=True, help="System variable name")
    p.set_defaults(func=handlers["cmd_capl_sysvar_get"], operator_command_id="inspect.read_system_variable")


def add_capl_sysvar_set_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--namespace", required=True, help="System variable namespace")
    p.add_argument("--var", required=True, help="System variable name")
    p.add_argument("--value", required=True, help="Target value")
    p.add_argument(
        "--value-type",
        default="int",
        choices=["int", "float", "bool", "string"],
        help="Input value type",
    )
    p.set_defaults(func=handlers["cmd_capl_sysvar_set"], operator_command_id="inspect.write_system_variable")


def add_canoe_capl_call_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    p.add_argument("--function-name", required=True, help="CAPL function name")
    p.add_argument("--args", nargs="*", default=[], help="CAPL call args")
    p.add_argument(
        "--arg-type",
        default="string",
        choices=["int", "float", "bool", "string"],
        help="Single coercion type for all --args values",
    )
    p.set_defaults(func=handlers["cmd_canoe_capl_call"], operator_command_id="inspect.capl_function_call")


def add_canoe_test_config_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--config-name", default="", help="Native CANoe test configuration name")
    p.add_argument("--tier", default="", choices=["", "UT", "IT", "ST", "FULL"], help="Tier alias resolved via native execution contract")


def add_canoe_test_config_status_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    add_canoe_test_config_common_args(p)
    p.add_argument("--json", action="store_true", help="Print JSON payload")
    p.set_defaults(func=handlers["cmd_canoe_test_config_status"], operator_command_id="operate.native_test_config_status")


def add_canoe_test_config_run_args(p: argparse.ArgumentParser, handlers: HandlerMap) -> None:
    add_canoe_test_config_common_args(p)
    p.add_argument("--timeout-seconds", type=int, default=1800, help="Execution timeout in seconds")
    p.add_argument("--poll-ms", type=int, default=500, help="Polling interval in milliseconds")
    p.add_argument("--no-ensure-running", action="store_true", help="Do not auto-start measurement before execution")
    p.add_argument("--restart-if-running", action="store_true", help="Stop and restart if the configuration is already running")
    p.add_argument("--fail-on-verdict", action="store_true", help="Return non-zero when execution verdict is failed")
    p.add_argument("--json", action="store_true", help="Print JSON payload")
    p.set_defaults(func=handlers["cmd_canoe_test_config_run"], operator_command_id="operate.native_test_config_run")


def build_parser(handlers: HandlerMap, default_run_id: Callable[[], str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="{" + ",".join(VISIBLE_TOPLEVEL_COMMANDS) + "}",
    )

    start = sub.add_parser("start", help="Operator-first quick entrypoints")
    start_sub = start.add_subparsers(dest="start_command")
    add_start_demo_args(start_sub.add_parser("demo", help="Trigger default demo scenario (no panel)"), handlers)
    add_start_precheck_args(start_sub.add_parser("precheck", help="Run precheck batch (gates+prepare+smoke+status)"), handlers, default_run_id)
    add_start_preset_args(start_sub.add_parser("preset", help="Run named preset workflow"), handlers)
    start_sub.add_parser("shell", help="Open interactive slash shell").set_defaults(func=handlers["cmd_start_shell"])
    start_sub.add_parser("guided", help="Open menu-style guided operator flow").set_defaults(func=handlers["cmd_start_guided"])
    start.set_defaults(func=handlers["cmd_start_guided"])

    add_doctor_args(sub.add_parser("doctor", help="Check CANoe COM + measurement + required sysvars"), handlers)

    capl = sub.add_parser("capl", help="CAPL-linked sysvar access via CANoe COM")
    capl_sub = capl.add_subparsers(dest="capl_command", required=True)
    add_capl_sysvar_get_args(capl_sub.add_parser("sysvar-get", help="Read one system variable value"), handlers)
    add_capl_sysvar_set_args(capl_sub.add_parser("sysvar-set", help="Write one system variable value"), handlers)

    canoe_cmd = sub.add_parser("canoe", help="CANoe COM control plane")
    canoe_sub = canoe_cmd.add_subparsers(dest="canoe_command", required=True)
    canoe_sub.add_parser("measure-status", help="Read measurement status").set_defaults(func=handlers["cmd_canoe_measure_status"], operator_command_id="operate.measure_status")
    canoe_sub.add_parser("measure-start", help="Start measurement").set_defaults(func=handlers["cmd_canoe_measure_start"], operator_command_id="operate.measure_start")
    canoe_sub.add_parser("measure-stop", help="Stop measurement").set_defaults(func=handlers["cmd_canoe_measure_stop"], operator_command_id="operate.measure_stop")
    canoe_sub.add_parser("measure-reset", help="Reset measurement (stop/start)").set_defaults(func=handlers["cmd_canoe_measure_reset"], operator_command_id="operate.measure_reset")
    add_canoe_capl_call_args(canoe_sub.add_parser("capl-call", help="Call CAPL function"), handlers)
    canoe_sub.add_parser("test-config-list", help="List native CANoe test configurations").set_defaults(func=handlers["cmd_canoe_test_config_list"], operator_command_id="operate.native_test_config_list")
    add_canoe_test_config_status_args(canoe_sub.add_parser("test-config-status", help="Read one native CANoe test configuration status"), handlers)
    add_canoe_test_config_run_args(canoe_sub.add_parser("test-config-run", help="Execute one native CANoe test configuration"), handlers)

    sub.add_parser("tui", help="Product-style Textual operator console").set_defaults(func=handlers["cmd_tui"])
    sub.add_parser("shell", help="Interactive slash-command shell").set_defaults(func=handlers["cmd_shell"])
    _add_hidden_parser(sub, "wizard").set_defaults(func=handlers["cmd_wizard"])

    scenario = sub.add_parser("scenario", help="Manual scenario trigger commands (no panel)")
    scenario_sub = scenario.add_subparsers(dest="scenario_command", required=True)
    add_scenario_run_args(scenario_sub.add_parser("run", help="Send scenario command via CANoe COM"), handlers)

    verify = sub.add_parser("verify", help="Verification pipeline commands")
    verify_sub = verify.add_subparsers(dest="verify_command", required=True)
    add_verify_prepare_args(verify_sub.add_parser("prepare", help="Create UT/IT/ST evidence run folders"), handlers)
    add_verify_batch_args(verify_sub.add_parser("batch", help="Run Dev2 pre/post/full batch workflow"), handlers)
    add_verify_smoke_args(verify_sub.add_parser("smoke", help="Run CANoe COM smoke checks"), handlers)
    add_verify_collect_args(verify_sub.add_parser("collect", help="Collect native reports and raw evidence for one tier"), handlers)
    add_verify_post_run_args(verify_sub.add_parser("post-run", help="Collect + fill-score one tier in one step"), handlers)
    add_verify_report_tools_args(verify_sub.add_parser("report-tools", help="Inspect official Vector report tooling install"), handlers)
    add_verify_report_bundle_args(verify_sub.add_parser("report-bundle", help="Export and parse native report via official Vector tooling"), handlers)
    add_verify_quick_args(verify_sub.add_parser("quick", help="Run prepare + smoke + status in one flow"), handlers, default_run_id)
    add_verify_fill_args(verify_sub.add_parser("fill-score", help="Fill and score one tier"), handlers)
    add_verify_insight_args(verify_sub.add_parser("insight", help="Build run-level insight report"), handlers)
    add_verify_bind_doc_args(verify_sub.add_parser("bind-doc", help="Build 05/06/07 doc binding bundle"), handlers)
    add_verify_fill_template_args(verify_sub.add_parser("fill-template", help="Build 05/06/07 doc fill template"), handlers)
    add_verify_status_args(verify_sub.add_parser("status", help="Check run readiness before finalize"), handlers)
    add_verify_surface_bundle_args(verify_sub.add_parser("surface-bundle", help="Build reviewer-facing surface ECU evidence bundle"), handlers)
    add_verify_finalize_args(verify_sub.add_parser("finalize", help="Run full post-run verification bundle"), handlers)

    evidence = sub.add_parser("evidence", help="Evidence/readout focused commands")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    ev_status = evidence_sub.add_parser("status", help="Alias of verify status")
    add_verify_status_args(ev_status, handlers)
    ev_status.set_defaults(func=handlers["cmd_evidence_status"], operator_command_id="verify.run_readiness_status")
    ev_insight = evidence_sub.add_parser("insight", help="Alias of verify insight")
    add_verify_insight_args(ev_insight, handlers)
    ev_insight.set_defaults(func=handlers["cmd_evidence_insight"], operator_command_id="verify.insight")
    ev_finalize = evidence_sub.add_parser("finalize", help="Alias of verify finalize")
    add_verify_finalize_args(ev_finalize, handlers)
    ev_finalize.set_defaults(func=handlers["cmd_evidence_finalize"], operator_command_id="verify.finalize")

    gate = sub.add_parser("gate", help="Quality gate commands")
    gate_sub = gate.add_subparsers(dest="gate_command", required=True)
    gate_sub.add_parser("all", help="Run the full gate bundle").set_defaults(func=handlers["cmd_gate_all"], operator_command_id="verify.all_gates")
    gate_sub.add_parser("doc-sync", help="Run Req-Doc-Code sync gate").set_defaults(func=handlers["cmd_gate_doc_sync"])
    gate_sub.add_parser("text-integrity", help="Run mojibake/question-run text integrity gate").set_defaults(func=handlers["cmd_gate_text_integrity"])
    gate_sub.add_parser("cfg-hygiene", help="Run cfg text hygiene gate").set_defaults(func=handlers["cmd_gate_cfg_hygiene"])
    gate_sub.add_parser("capl-sync", help="Run src/capl vs cfg/channel_assign sync gate").set_defaults(func=handlers["cmd_gate_capl_sync"])
    gate_sub.add_parser("multibus-dbc", help="Run multi-bus cfg + DBC domain policy gate").set_defaults(func=handlers["cmd_gate_multibus_dbc"])
    gate_sub.add_parser("cli-readiness", help="Run CLI readiness gate before GUI phase").set_defaults(func=handlers["cmd_gate_cli_readiness"])

    artifact = sub.add_parser("artifact", help="Artifact inspection/open/cleanup commands")
    artifact_sub = artifact.add_subparsers(dest="artifact_command", required=True)
    add_artifact_list_args(artifact_sub.add_parser("list", help="List staging or archive artifact paths"), handlers)
    add_artifact_open_args(artifact_sub.add_parser("open", help="Open one artifact target"), handlers)
    add_package_clean_args(artifact_sub.add_parser("clean", help="Clean staging/archive/build outputs"), handlers)

    package = sub.add_parser("package", help="Build/distribution commands")
    package_sub = package.add_subparsers(dest="package_command", required=True)
    pkg_build = package_sub.add_parser("build-exe", help="Build Windows exe bundle via PyInstaller")
    pkg_build.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build.add_argument("--clean", action="store_true")
    pkg_build.set_defaults(func=handlers["cmd_package_build_exe"], operator_command_id="package.windows_exe")

    pkg_portable = package_sub.add_parser(
        "bundle-portable",
        help="Create portable ZIP (exe + required runtime files)",
    )
    pkg_portable.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_portable.add_argument("--clean", action="store_true")
    pkg_portable.add_argument("--rebuild-exe", action="store_true")
    pkg_portable.add_argument("--output-dir", default="")
    pkg_portable.add_argument("--bundle-name", default="")
    pkg_portable.add_argument("--zip-name", default="")
    pkg_portable.set_defaults(func=handlers["cmd_package_bundle_portable"], operator_command_id="package.portable_bundle")

    pkg_validate = package_sub.add_parser("validate-contract", help="Validate manifest/layout packaging contract")
    pkg_validate.set_defaults(func=handlers["cmd_package_validate_contract"], operator_command_id="package.validate_contract")
    add_package_clean_args(package_sub.add_parser("clean", help="Clean generated staging/archive/build outputs"), handlers)

    release = sub.add_parser("release", help="Distribution-focused wrappers")
    release_sub = release.add_subparsers(dest="release_command", required=True)
    rel_exe = release_sub.add_parser("exe", help="Alias of package build-exe")
    rel_exe.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    rel_exe.add_argument("--clean", action="store_true")
    rel_exe.set_defaults(func=handlers["cmd_release_exe"], operator_command_id="package.windows_exe")

    rel_portable = release_sub.add_parser("portable", help="Alias of package bundle-portable")
    rel_portable.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    rel_portable.add_argument("--clean", action="store_true")
    rel_portable.add_argument("--rebuild-exe", action="store_true")
    rel_portable.add_argument("--output-dir", default="")
    rel_portable.add_argument("--bundle-name", default="")
    rel_portable.add_argument("--zip-name", default="")
    rel_portable.set_defaults(func=handlers["cmd_release_portable"], operator_command_id="package.portable_bundle")

    contract = sub.add_parser("contract", help="Show canonical command contract")
    contract.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    contract.set_defaults(func=handlers["cmd_contract"], operator_command_id="inspect.command_contract")

    add_scenario_run_args(_add_hidden_parser(sub, "scenario-run"), handlers)
    _add_hidden_parser(sub, "interactive").set_defaults(func=handlers["cmd_shell"])

    add_verify_prepare_args(_add_hidden_parser(sub, "verify-prepare"), handlers)
    add_verify_batch_args(_add_hidden_parser(sub, "verify-batch"), handlers)
    add_verify_smoke_args(_add_hidden_parser(sub, "verify-smoke"), handlers)
    add_verify_collect_args(_add_hidden_parser(sub, "verify-collect"), handlers)
    add_verify_post_run_args(_add_hidden_parser(sub, "verify-post-run"), handlers)
    add_verify_report_tools_args(_add_hidden_parser(sub, "verify-report-tools"), handlers)
    add_verify_report_bundle_args(_add_hidden_parser(sub, "verify-report-bundle"), handlers)
    add_verify_fill_args(_add_hidden_parser(sub, "verify-fill-score"), handlers)
    add_verify_insight_args(_add_hidden_parser(sub, "verify-insight"), handlers)
    add_verify_bind_doc_args(_add_hidden_parser(sub, "verify-bind-doc"), handlers)
    add_verify_fill_template_args(_add_hidden_parser(sub, "verify-fill-template"), handlers)
    add_verify_status_args(_add_hidden_parser(sub, "verify-status"), handlers)
    add_verify_surface_bundle_args(_add_hidden_parser(sub, "verify-surface-bundle"), handlers)
    add_verify_finalize_args(_add_hidden_parser(sub, "verify-finalize"), handlers)
    _add_hidden_parser(sub, "gate-doc-sync").set_defaults(func=handlers["cmd_gate_doc_sync"])
    _add_hidden_parser(sub, "gate-cfg-hygiene").set_defaults(func=handlers["cmd_gate_cfg_hygiene"])
    _add_hidden_parser(sub, "gate-capl-sync").set_defaults(func=handlers["cmd_gate_capl_sync"])
    _add_hidden_parser(sub, "gate-multibus-dbc").set_defaults(func=handlers["cmd_gate_multibus_dbc"])
    _add_hidden_parser(sub, "gate-cli-readiness").set_defaults(func=handlers["cmd_gate_cli_readiness"])
    pkg_build_legacy = _add_hidden_parser(sub, "package-build-exe")
    pkg_build_legacy.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build_legacy.add_argument("--clean", action="store_true")
    pkg_build_legacy.set_defaults(func=handlers["cmd_package_build_exe"], operator_command_id="package.windows_exe")
    pkg_portable_legacy = _add_hidden_parser(sub, "package-bundle-portable")
    pkg_portable_legacy.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_portable_legacy.add_argument("--clean", action="store_true")
    pkg_portable_legacy.add_argument("--rebuild-exe", action="store_true")
    pkg_portable_legacy.add_argument("--output-dir", default="")
    pkg_portable_legacy.add_argument("--bundle-name", default="")
    pkg_portable_legacy.add_argument("--zip-name", default="")
    pkg_portable_legacy.set_defaults(func=handlers["cmd_package_bundle_portable"], operator_command_id="package.portable_bundle")
    _add_hidden_parser(sub, "package-validate-contract").set_defaults(
        func=handlers["cmd_package_validate_contract"],
        operator_command_id="package.validate_contract",
    )
    add_package_clean_args(_add_hidden_parser(sub, "package-clean"), handlers)

    _add_hidden_parser(sub, "go").set_defaults(func=handlers["cmd_start_guided"])
    add_start_demo_args(_add_hidden_parser(sub, "demo"), handlers)
    add_start_precheck_args(_add_hidden_parser(sub, "precheck"), handlers, default_run_id)
    _add_hidden_parser(sub, "mstart").set_defaults(func=handlers["cmd_canoe_measure_start"], operator_command_id="operate.measure_start")
    _add_hidden_parser(sub, "mstop").set_defaults(func=handlers["cmd_canoe_measure_stop"], operator_command_id="operate.measure_stop")
    _add_hidden_parser(sub, "mstatus").set_defaults(func=handlers["cmd_canoe_measure_status"], operator_command_id="operate.measure_status")

    return parser
