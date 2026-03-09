"""Shared product command catalog for shell palette and Textual TUI."""

from __future__ import annotations

import datetime as dt
import shlex
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CommandParam:
    key: str
    flag: str
    label: str
    default: str = ""
    help: str = ""
    placeholder: str = ""
    kind: str = "text"
    choices: tuple[str, ...] = ()
    required: bool = False


@dataclass(frozen=True)
class PaletteCommand:
    command_id: str
    title: str
    command: str
    summary: str
    windows_only: bool = False
    notes: str = ""
    use_when: tuple[str, ...] = field(default_factory=tuple)
    success_signals: tuple[str, ...] = field(default_factory=tuple)
    expected_outputs: tuple[str, ...] = field(default_factory=tuple)
    failure_focus: tuple[str, ...] = field(default_factory=tuple)
    next_step: str = ""
    base_command: str = ""
    params: tuple[CommandParam, ...] = field(default_factory=tuple)

    def executable_base(self) -> str:
        return self.base_command or self.command


def build_command_tokens(command: PaletteCommand, values: dict[str, str] | None = None) -> list[str]:
    """Build CLI tokens from a palette command and optional form values."""
    tokens = shlex.split(command.executable_base())
    for param in command.params:
        raw = (values or {}).get(param.key, param.default)
        raw = raw.strip()
        if not raw:
            if param.required:
                raise ValueError(f"{param.label} is required.")
            continue
        if param.kind == "int":
            try:
                int(raw)
            except ValueError as ex:  # pragma: no cover - UI validation surfaces the message
                raise ValueError(f"{param.label} must be an integer.") from ex
        if param.choices and raw not in param.choices:
            allowed = ", ".join(param.choices)
            raise ValueError(f"{param.label} must be one of: {allowed}")
        tokens.extend([param.flag, raw])
    return tokens


def resolve_default_value(raw: str) -> str:
    if raw == "{run_id}":
        return dt.datetime.now().strftime("%Y%m%d_%H%M")
    if raw == "{today}":
        return dt.date.today().isoformat()
    return raw


def resolve_command_defaults(command: PaletteCommand) -> dict[str, str]:
    return {param.key: resolve_default_value(param.default) for param in command.params}


def build_command_index() -> dict[str, PaletteCommand]:
    return {
        command.command_id: command
        for commands in PRODUCT_COMMAND_GROUPS.values()
        for command in commands
    }


PRODUCT_COMMAND_GROUPS: dict[str, list[PaletteCommand]] = {
    "Primary Workflow": [
        PaletteCommand(
            command_id="verify.all_gates",
            title="1) Gate all",
            command="gate all",
            summary="런타임 조작 전에 전체 preflight gate 묶음을 실행합니다.",
            notes="일일 운영의 첫 단계입니다. 여기서 실패하면 먼저 정합성 문제를 수정하십시오.",
            use_when=(
                "측정을 올리기 전에 DBC/CAPL/문서 정합을 한 번에 확인할 때",
                "작업 시작 직후 현재 저장소가 검증 가능한 상태인지 판단할 때",
            ),
            success_signals=(
                "gate summary가 PASS로 끝남",
                "cli_readiness_gate.json/md가 생성됨",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/cli_readiness_gate.json",
                "canoe/tmp/reports/verification/cli_readiness_gate.md",
            ),
            failure_focus=(
                "text-integrity / cfg-hygiene / doc-sync 중 어떤 gate가 깨졌는지 먼저 확인",
                "FAIL이면 runtime 조작 전에 정합성부터 복구",
            ),
            next_step="PASS면 Scenario run으로 넘어가십시오.",
        ),
        PaletteCommand(
            command_id="operate.scenario_trigger",
            title="2) Scenario run",
            command="scenario run --id 4",
            base_command="scenario run",
            summary="SIL 시나리오를 CANoe에 주입하고 ack 경로를 확인합니다.",
            windows_only=True,
            notes="Gate all이 끝났고 measurement가 올라와 있을 때 실행하십시오.",
            use_when=(
                "CANoe measurement가 running이고 Test::scenarioCommand 경로를 검증할 때",
                "패널/로그/증빙을 실제 시나리오 기준으로 시작할 때",
            ),
            success_signals=(
                "scenarioCommandAck가 동일한 ID로 돌아옴",
                "후속 Verify quick에서 해당 run의 증빙이 쌓이기 시작함",
            ),
            expected_outputs=(
                "ACK log line in TUI/CLI output",
                "후속 Verify quick을 위한 run context",
            ),
            failure_focus=(
                "Measurement stopped 여부",
                "Test::scenarioCommandAck / active CAPL path / COM attach 상태",
            ),
            next_step="ack가 확인되면 Verify quick으로 넘어가십시오.",
            params=(
                CommandParam(
                    key="scenario_id",
                    flag="--id",
                    label="시나리오 ID",
                    default="4",
                    help="0은 정지, 1~25는 시나리오 실행, 100은 auto-demo, 200~255는 baseline diagnostic입니다.",
                    placeholder="4",
                    kind="int",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.quick_verify",
            title="3) Verify quick",
            command="verify quick",
            summary="증빙 폴더 생성, smoke, readiness scoring을 한 번에 수행합니다.",
            windows_only=True,
            notes="Scenario run 직후 첫 번째 검증 증빙을 수집할 때 사용합니다.",
            use_when=(
                "시나리오 주입 후 UT/IT/ST 증빙 준비 상태를 한 번에 확인할 때",
                "05/06/07 문서에 붙일 evidence readiness를 빠르게 점검할 때",
            ),
            success_signals=(
                "run_readiness overall_status가 PASS 또는 준비 가능한 상태로 생성됨",
                "evidence 폴더와 readiness json/md가 생성됨",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/run_readiness.json",
                "canoe/tmp/reports/verification/run_readiness.md",
                "canoe/logging/evidence/UT/<run_id>",
                "canoe/logging/evidence/IT/<run_id>",
                "canoe/logging/evidence/ST/<run_id>",
            ),
            failure_focus=(
                "[EVIDENCE_OUT] marker 누락 tier",
                "filled/scored 파일 미생성 tier",
            ),
            next_step="결과와 증빙을 확인한 뒤 05/06/07 문서에 반영하십시오.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="증빙 실행 식별자입니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="담당자",
                    default="DEV2",
                    help="smoke/status 보고서에 기록되는 owner 태그입니다.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
    ],
    "Runtime Support": [
        PaletteCommand(
            command_id="inspect.environment_doctor",
            title="환경 점검",
            command="doctor",
            summary="CANoe COM 연결, measurement 상태, 핵심 sysvar 접근성을 확인합니다.",
            windows_only=True,
            notes="Scenario run이나 Verify quick 전에 먼저 확인하십시오.",
            use_when=(
                "TUI/CLI가 현재 CANoe 세션을 제대로 잡고 있는지 먼저 확인할 때",
                "시나리오 ack timeout이나 sysvar missing이 발생했을 때 원인 분리용으로",
            ),
            success_signals=(
                "COM attach PASS",
                "Measurement running = running",
                "필수 sysvar check PASS",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/doctor_report.json",
                "canoe/tmp/reports/verification/doctor_report.md",
            ),
            failure_focus=(
                "COM attach 불가인지, measurement stop인지, sysvar 누락인지 구분",
                "실패 종류별로 바로 다음 조치가 달라짐",
            ),
            next_step="정상이면 Scenario run 또는 Verify quick으로 이동하십시오.",
        ),
        PaletteCommand(
            command_id="operate.measure_status",
            title="측정 상태",
            command="canoe measure-status",
            summary="현재 CANoe measurement 상태를 읽습니다.",
            windows_only=True,
            use_when=("Scenario run 전에 measurement 상태를 확인할 때",),
            success_signals=("running 또는 stopped 상태가 명확히 출력됨",),
            failure_focus=("COM attach/session 문제인지 단순 stopped인지 구분",),
            next_step="stopped면 먼저 측정을 시작하십시오.",
        ),
        PaletteCommand(
            command_id="operate.measure_start",
            title="측정 시작",
            command="canoe measure-start",
            summary="COM 경유로 CANoe measurement를 시작합니다.",
            windows_only=True,
            use_when=("Scenario run 전에 CANoe measurement를 올려야 할 때",),
            success_signals=("measurement start 결과가 PASS",),
            failure_focus=("권한/session mismatch 또는 CANoe attach 문제",),
            next_step="running이 확인되면 Scenario run으로 이동하십시오.",
        ),
        PaletteCommand(
            command_id="operate.measure_stop",
            title="측정 중지",
            command="canoe measure-stop",
            summary="COM 경유로 CANoe measurement를 중지합니다.",
            windows_only=True,
            use_when=("실행 정리 또는 상태 초기화가 필요할 때",),
            success_signals=("measurement stop 결과가 PASS",),
            next_step="필요 시 reset 또는 다음 measurement start를 준비하십시오.",
        ),
        PaletteCommand(
            command_id="verify.precheck_batch",
            title="사전 점검 배치",
            command="start precheck",
            summary="gate, prepare, smoke, readiness status를 한 번에 수행합니다.",
            windows_only=True,
            notes="개발 상태를 빠르게 훑고 검증 진입 가능 여부를 판단할 때 사용합니다.",
            use_when=(
                "개발 종료 전 현재 상태를 한 번에 스냅샷하고 싶을 때",
                "오늘 작업이 검증 진입 가능한 수준인지 빠르게 판단할 때",
            ),
            success_signals=(
                "dev2_batch_report status가 PASS",
                "step별 rc가 모두 0",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/dev2_batch_report.json",
                "canoe/tmp/reports/verification/dev2_batch_report.md",
            ),
            failure_focus=(
                "첫 fail step 이름과 rc",
                "precheck에서 막히면 runtime 조작 전에 먼저 해결",
            ),
            next_step="PASS면 본 시나리오 실행이나 증빙 수집으로 넘어가십시오.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="증빙 실행 식별자입니다. 일반적으로 YYYYMMDD_HHMM 형식을 사용합니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="담당자",
                    default="DEV2",
                    help="보고서에 기록되는 운영자 태그입니다.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.batch",
            title="검증 배치 (CI/Jenkins)",
            command="verify batch",
            base_command="verify batch",
            summary="pre/post/full 검증 배치를 실행하고 Jenkins용 JUnit XML까지 생성합니다.",
            windows_only=True,
            notes="Dev2의 대표 CI bridge 경로입니다. native CANoe 결과는 archive하고, Dev2는 정규화된 배치 산출물을 생성합니다.",
            use_when=(
                "Jenkins 또는 야간 회귀에서 machine-readable 결과를 남겨야 할 때",
                "pre/post/full 검증 단계를 하나의 운영 명령으로 고정할 때",
            ),
            success_signals=(
                "dev2_batch_report status가 PASS",
                "dev2_batch_report.junit.xml 이 생성됨",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/dev2_batch_report.json",
                "canoe/tmp/reports/verification/dev2_batch_report.md",
                "canoe/tmp/reports/verification/dev2_batch_report.junit.xml",
            ),
            failure_focus=(
                "실패한 step rc",
                "run_readiness missing_items",
                "native .vtestreport는 별도 archive 대상으로 취급",
            ),
            next_step="Jenkins에서는 junit + archiveArtifacts로 산출물을 수집하십시오.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    placeholder="20260309_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="담당자",
                    default="DEV2",
                    placeholder="DEV2",
                    required=True,
                ),
                CommandParam(
                    key="phase",
                    flag="--phase",
                    label="배치 단계",
                    default="pre",
                    choices=("pre", "post", "full"),
                    required=True,
                ),
                CommandParam(
                    key="report_formats",
                    flag="--report-formats",
                    label="출력 포맷",
                    default="json,md,junit",
                    placeholder="json,md,junit",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.run_readiness_status",
            title="증빙 준비 상태",
            command="verify status --run-id 20260308_0900",
            base_command="verify status",
            summary="raw evidence, marker, score 준비 상태를 점검합니다.",
            use_when=(
                "특정 run_id의 증빙 누락 tier를 확인할 때",
                "05/06/07 채우기 전에 현재 증빙 품질을 재점검할 때",
            ),
            success_signals=(
                "target run_id에 대해 marker_count / filled / scored 상태가 채워짐",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/run_readiness.json",
                "canoe/tmp/reports/verification/run_readiness.md",
            ),
            failure_focus=(
                "UT/IT/ST 중 어떤 tier가 marker 또는 scored 파일이 없는지",
            ),
            next_step="누락 tier를 보강한 뒤 Verify quick 또는 status를 다시 실행하십시오.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="canoe/logging/evidence 아래에서 확인할 실행 폴더입니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.surface_bundle",
            title="표면 ECU 묶음",
            command="verify surface-bundle",
            base_command="verify surface-bundle",
            summary="배치/doctor/readiness 결과를 BCM·IVI·CLUSTER·ADAS·V2X 같은 surface ECU 기준으로 다시 묶습니다.",
            notes="reviewer-facing 결과와 Jenkins archive 구조를 runtime module이 아니라 surface ECU 기준으로 고정할 때 사용합니다.",
            use_when=(
                "배치 결과를 OEM reviewer가 읽는 표면 ECU 기준으로 재정렬해야 할 때",
                "Jenkins archive를 surface ECU 번들 단위로 나눠야 할 때",
            ),
            success_signals=(
                "surface_evidence_bundle.json/md 생성",
                "surface/<bundle_key>/bundle.json|md 생성",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/surface_evidence_bundle.json",
                "canoe/tmp/reports/verification/surface_evidence_bundle.md",
                "canoe/tmp/reports/verification/surface/**/*",
            ),
            failure_focus=(
                "surface inventory 누락 또는 drift",
                "doctor/readiness/batch 산출물 미생성",
            ),
            next_step="Jenkins archive와 reviewer package를 surface ECU 기준으로 묶으십시오.",
        ),
        PaletteCommand(
            command_id="operate.guided",
            title="가이드 모드",
            command="start guided",
            summary="Textual TUI를 쓰기 어려울 때 사용하는 순차형 fallback입니다.",
            notes="터미널 호환성 문제가 있을 때만 사용하십시오.",
        ),
    ],
    "System Access": [
        PaletteCommand(
            command_id="inspect.read_system_variable",
            title="시스템 변수 조회",
            command="capl sysvar-get --namespace Core --var failSafeMode",
            base_command="capl sysvar-get",
            summary="CAPL/COM 경유로 system variable 값을 읽습니다.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="네임스페이스",
                    default="Core",
                    help="조회할 system variable namespace입니다.",
                    placeholder="Core",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="변수",
                    default="failSafeMode",
                    help="조회할 system variable 이름입니다.",
                    placeholder="failSafeMode",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.write_system_variable",
            title="시스템 변수 쓰기",
            command="capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int",
            base_command="capl sysvar-set",
            summary="CAPL/COM 경유로 system variable 값을 설정합니다.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="네임스페이스",
                    default="Test",
                    help="설정할 system variable namespace입니다.",
                    placeholder="Test",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="변수",
                    default="scenarioCommand",
                    help="설정할 system variable 이름입니다.",
                    placeholder="scenarioCommand",
                    required=True,
                ),
                CommandParam(
                    key="value",
                    flag="--value",
                    label="값",
                    default="4",
                    help="설정할 값입니다.",
                    placeholder="4",
                    required=True,
                ),
                CommandParam(
                    key="value_type",
                    flag="--value-type",
                    label="값 형식",
                    default="int",
                    help="int, float, bool, string 중 하나를 사용합니다.",
                    placeholder="int",
                    choices=("int", "float", "bool", "string"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.command_contract",
            title="명령 계약 보기",
            command="contract",
            summary="지원하는 공개 명령과 compatibility alias를 확인합니다.",
        ),
    ],
    "Packaging": [
        PaletteCommand(
            command_id="artifact.list_staging",
            title="staging 산출물 목록",
            command="artifact list --scope staging",
            summary="현재 staging 산출물 경로를 한 번에 확인합니다.",
            notes="도구가 방금 생성한 JSON/MD/JUnit/surface bundle/readiness 위치를 점검할 때 사용합니다.",
            use_when=(
                "최근 실행이 어떤 파일을 만들었는지 빠르게 확인할 때",
                "결과 화면만으로 부족해서 staging 원본 파일 경로를 직접 열어야 할 때",
            ),
            success_signals=("staging root와 핵심 report 경로가 OK로 표시됨",),
            expected_outputs=("canoe/tmp/reports/verification/*",),
            failure_focus=("MISSING로 표시되는 핵심 산출물이 있는지 확인",),
            next_step="필요한 산출물은 artifact open으로 바로 여십시오.",
        ),
        PaletteCommand(
            command_id="artifact.list_archive_latest",
            title="최근 아카이브 목록",
            command="artifact list --scope archive --latest",
            base_command="artifact list --scope archive --latest",
            summary="가장 최근 verification archive run 구조를 확인합니다.",
            use_when=(
                "reviewer/Jenkins 기준 최종 보관 구조를 빠르게 점검할 때",
            ),
            success_signals=("reports/surface/manifests/native_reports 경로가 OK로 표시됨",),
            expected_outputs=("artifacts/verification_runs/<latest>/<phase>/*",),
            failure_focus=("archive materialization이 실제로 끝났는지 확인",),
            next_step="필요한 하위 경로는 artifact open으로 바로 여십시오.",
        ),
        PaletteCommand(
            command_id="artifact.list_source_contracts",
            title="원본 계약 파일 목록",
            command="artifact list --scope source",
            summary="산출물 생성에 쓰이는 원본 계약/설정 파일을 확인합니다.",
            notes="surface inventory, traceability profile, artifact layout, 결과 문서 원본까지 같이 보여줍니다.",
            use_when=(
                "산출물 기준이 어떤 원본 파일에서 왔는지 바로 확인할 때",
            ),
            success_signals=("source contract 목록이 모두 표시됨",),
            expected_outputs=(
                "product/sdv_operator/config/*.json",
                "product/sdv_operator/docs-src/*.md",
            ),
            next_step="원본 파일 검토가 필요하면 artifact open으로 바로 여십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_surface_bundle",
            title="표면 ECU 결과 열기",
            command="artifact open --target surface-bundle",
            summary="surface ECU 기준 reviewer-facing 결과 문서를 바로 엽니다.",
            use_when=(
                "BCM/IVI/CLUSTER/ADAS/V2X 기준 결과를 바로 확인할 때",
            ),
            success_signals=("surface_evidence_bundle.md가 열림",),
            expected_outputs=("canoe/tmp/reports/verification/surface_evidence_bundle.md",),
            next_step="필요하면 Results 화면과 대조하거나 archive bundle로 이어서 이동하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_batch_report",
            title="배치 리포트 열기",
            command="artifact open --target batch-report",
            summary="가장 최근 batch markdown 리포트를 바로 엽니다.",
            use_when=("staging 결과의 전체 흐름과 phase verdict를 바로 문서로 보고 싶을 때",),
            success_signals=("dev2_batch_report.md가 열림",),
            expected_outputs=("canoe/tmp/reports/verification/dev2_batch_report.md",),
            next_step="surface bundle이나 execution manifest까지 이어서 확인하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_execution_manifest",
            title="실행 매니페스트 열기",
            command="artifact open --target execution-manifest --latest",
            base_command="artifact open --target execution-manifest --latest",
            summary="가장 최근 archive run의 execution manifest를 엽니다.",
            use_when=(
                "run_id/phase/owner/scenario/surface key를 한 파일에서 확인할 때",
            ),
            success_signals=("execution_manifest.json이 열림",),
            expected_outputs=("artifacts/verification_runs/<latest>/<phase>/manifests/execution_manifest.json",),
            failure_focus=("latest archive run이 없는지 먼저 확인",),
            next_step="reviewer bundle 또는 Jenkins archive 구조와 같이 검토하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_native_reports",
            title="native report 열기",
            command="artifact open --target native-reports --latest",
            base_command="artifact open --target native-reports --latest",
            summary="가장 최근 archive run의 native CANoe report 폴더를 엽니다.",
            use_when=(
                "Dev1 native .vtestreport를 reviewer 기준 archive 안에서 바로 확인할 때",
            ),
            success_signals=("native_reports 폴더가 열림",),
            expected_outputs=("artifacts/verification_runs/<latest>/<phase>/native_reports/**/*",),
            failure_focus=("latest archive run 또는 native report 복사본이 없는지 확인",),
            next_step="execution manifest와 함께 실행 키와 stable key를 대조하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_source_inventory",
            title="원본 surface inventory 열기",
            command="artifact open --target surface-inventory",
            summary="surface ECU inventory 원본 JSON을 바로 엽니다.",
            use_when=(
                "결과 묶음이 어떤 surface 정의를 기준으로 만들어졌는지 원본을 보고 확인할 때",
            ),
            success_signals=("surface_ecu_inventory.json이 열림",),
            expected_outputs=("product/sdv_operator/config/surface_ecu_inventory.json",),
            next_step="traceability/profile 문서도 필요하면 source target으로 이어서 여십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_traceability_profile",
            title="원본 traceability profile 열기",
            command="artifact open --target traceability-profile",
            summary="surface bundle이 어떤 Req/TestCase/Scenario 매핑 기준을 쓰는지 원본 JSON을 엽니다.",
            use_when=("surface inventory만으로 부족하고 traceability 기준까지 바로 보고 싶을 때",),
            success_signals=("surface_traceability_profile.json이 열림",),
            expected_outputs=("product/sdv_operator/config/surface_traceability_profile.json",),
            next_step="필요하면 execution manifest와 함께 대조하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_artifact_layout",
            title="원본 artifact layout 열기",
            command="artifact open --target artifact-layout",
            summary="staging과 final archive 구조를 정의하는 layout contract를 엽니다.",
            use_when=("산출물 경로가 어디로 materialize되는지 원본 계약을 보고 확인할 때",),
            success_signals=("verification_artifact_layout.json이 열림",),
            expected_outputs=("product/sdv_operator/config/verification_artifact_layout.json",),
            next_step="archive list 또는 packaging 문서와 함께 구조를 검토하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_ci_bridge_doc",
            title="CI bridge 문서 열기",
            command="artifact open --target ci-bridge-doc",
            summary="Jenkins와 Verification Console 사이의 연결 규약 문서를 엽니다.",
            use_when=(
                "Jenkins가 담당하는 역할과 Verification Console이 담당하는 역할을 다시 확인할 때",
            ),
            success_signals=("ci-bridge.md가 열림",),
            expected_outputs=("product/sdv_operator/docs-src/ci-bridge.md",),
            next_step="batch/JUnit/archive 설정은 Jenkinsfile.verify와 함께 확인하십시오.",
        ),
        PaletteCommand(
            command_id="artifact.open_jenkinsfile_sample",
            title="Jenkins 샘플 열기",
            command="artifact open --target jenkinsfile-sample",
            summary="Jenkins pipeline 샘플을 바로 엽니다.",
            use_when=(
                "Jenkins stage, junit, archiveArtifacts 흐름을 실제 예제로 확인할 때",
            ),
            success_signals=("Jenkinsfile.verify가 열림",),
            expected_outputs=("product/sdv_operator/examples/Jenkinsfile.verify",),
            next_step="CI bridge 문서와 함께 역할 경계를 확인하십시오.",
        ),
        PaletteCommand(
            command_id="package.validate_contract",
            title="패키징 계약 점검",
            command="package validate-contract",
            summary="manifest와 release layout 상수가 일치하는지 점검합니다.",
            use_when=(
                "배포 전에 현재 제품 경계와 산출물 계약이 깨지지 않았는지 확인할 때",
            ),
            success_signals=(
                "release_contract_report status가 PASS",
                "manifest public surface와 release_artifacts가 모두 일치함",
            ),
            expected_outputs=(
                "canoe/tmp/reports/verification/release_contract_report.json",
                "canoe/tmp/reports/verification/release_contract_report.md",
            ),
            failure_focus=(
                "manifest public_surface 누락",
                "release_artifacts 경로 drift",
            ),
            next_step="PASS면 build-exe 또는 bundle-portable로 넘어가십시오.",
        ),
        PaletteCommand(
            command_id="package.clean",
            title="생성물 정리",
            command="package clean --scope staging",
            base_command="package clean",
            summary="staging/build/archive generated output만 정리합니다.",
            notes="archive는 run_id 또는 all-runs 지정 없이는 지워지지 않습니다. 기본은 preview이며, 실제 삭제는 --yes가 필요합니다.",
            use_when=(
                "검증 산출물이 누적되어 작업면이 복잡해졌을 때",
                "배포 전 build/dist/site 캐시를 비우고 다시 만들고 싶을 때",
            ),
            success_signals=(
                "preview 목록이 기대한 생성물만 가리킴",
                "staging clean 후 run 결과가 다시 생성됨",
            ),
            expected_outputs=(
                "verification staging cleaned",
                "optional archive/build cleanup",
            ),
            failure_focus=(
                "archive는 run_id 없이 지우지 않음",
                "README.md 같은 설명 파일은 유지됨",
            ),
            next_step="preview가 맞으면 shell에서 동일 명령 뒤에 --yes를 붙여 적용하십시오.",
            params=(
                CommandParam(
                    key="scope",
                    flag="--scope",
                    label="정리 범위",
                    default="staging",
                    choices=("staging", "archive", "build", "all"),
                    required=True,
                ),
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="",
                    placeholder="20260310_0010",
                ),
                CommandParam(
                    key="phase",
                    flag="--phase",
                    label="Phase",
                    default="",
                    choices=("pre", "post", "full"),
                ),
            ),
        ),
        PaletteCommand(
            command_id="package.portable_bundle",
            title="포터블 번들",
            command="package bundle-portable --mode onefolder",
            base_command="package bundle-portable",
            summary="배포용 portable ZIP 산출물을 생성합니다.",
            use_when=("검증 팀이나 발표용으로 전달 가능한 산출물을 만들 때",),
            success_signals=("dist/portable/sdv_portable.zip 생성",),
            expected_outputs=("dist/portable/sdv_portable.zip",),
            failure_focus=("manifest 범위 밖 파일 누락 또는 build 경로 문제",),
            next_step="ZIP을 풀어서 run.py/TUI 진입이 되는지 smoke 하십시오.",
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="패키징 모드",
                    default="onefolder",
                    help="기본 배포는 onefolder, 단일 실행파일 테스트는 onefile을 사용합니다.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="package.windows_exe",
            title="윈도우 실행파일",
            command="package build-exe --mode onefolder",
            base_command="package build-exe",
            summary="Windows executable 산출물을 생성합니다.",
            windows_only=True,
            use_when=("Windows 운영자용 standalone 실행 산출물이 필요할 때",),
            success_signals=("dist/sdv_cli/sdv.exe 또는 onefolder bundle 생성",),
            expected_outputs=("dist/sdv_cli/sdv.exe", "dist/sdv_cli/sdv/"),
            failure_focus=("PyInstaller spec/build cache 문제",),
            next_step="실행파일로 doctor와 TUI 기동 smoke를 확인하십시오.",
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="빌드 모드",
                    default="onefolder",
                    help="운영 handoff는 onefolder, 단일 exe 검증은 onefile을 사용합니다.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
        ),
    ],
}


def build_shell_palette_groups() -> dict[str, list[tuple[str, str]]]:
    """Render the shared product catalog as shell palette tuples."""
    groups: dict[str, list[tuple[str, str]]] = {}
    for group_name, items in PRODUCT_COMMAND_GROUPS.items():
        groups[group_name] = [(f"/{item.command}", item.summary) for item in items]
    groups["Session"] = [
        ("/history", "최근 shell 명령 이력을 표시합니다."),
        ("/repeat 1", "가장 최근 shell 명령을 다시 실행합니다."),
        ("/exit", "shell을 종료합니다."),
    ]
    return groups
