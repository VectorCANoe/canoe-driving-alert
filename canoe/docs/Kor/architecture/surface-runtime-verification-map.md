# Surface, Runtime, and Verification Map 한글판

원문:
- [../../architecture/surface-runtime-verification-map.md](../../architecture/surface-runtime-verification-map.md)

## 1. 목적

이 문서는 현재 CANoe SIL 시스템이 아래 네 계층으로 어떻게 나뉘는지 설명합니다.

- user-facing surface
- runtime processing
- transport seams
- verification seams

핵심 목적은 agent와 개발자가 무엇을 어디서 수정해야 하는지 빠르게 찾게 하는 것입니다.

## 2. 상위 구조

| 계층 | 주 소스 | 대표 내용 |
|---|---|---|
| Surface | `project/panel/*`, `project/sysvars/project.sysvars` | panel 입력, output monitor, render mirror |
| Runtime | `src/capl/**` | normalization, arbitration, output control, fail-safe |
| Transport | `databases/*.dbc`, UDP backbone contract, `docs/contracts/*` | CAN frame, Ethernet seam, ownership policy |
| Verification | `tests/**`, `Test::*`, `Diag::*`, `docs/verification/*` | scenario orchestration, verdict, evidence, diagnostic mirror |

## 3. Surface 계층

surface 계층은 사람이나 harness가 가장 먼저 접하는 계층입니다.

### 3.1 Input surface

현재 panel/system-variable input surface는 아래 namespace를 기준으로 읽습니다.

- `Chassis`
- `Infotainment`
- `V2X`
- `Test`

대표 입력:
- `Chassis::vehicleSpeed`
- `Chassis::driveState`
- `Chassis::steeringInput`
- `Infotainment::roadZone`
- `Infotainment::navDirection`
- `Infotainment::zoneDistance`
- `V2X::emergencyType`
- `V2X::emergencyDirection`
- `V2X::eta`
- `V2X::alertState`
- `Test::scenarioCommand`

### 3.2 Output / monitor surface

현재 monitored output surface는 아래 namespace를 기준으로 읽습니다.

- `Body`
- `Cluster`
- `Core`
- `CoreState`
- `UiRender`
- `Diag`
- `Test`

대표 출력:
- `Body::ambientMode`
- `Body::ambientColor`
- `Body::ambientPattern`
- `Cluster::warningTextCode`
- `Core::selectedAlertLevel`
- `Core::selectedAlertType`
- `Core::timeoutClear`
- `CoreState::warningPathStatus`
- `CoreState::e2eHealthState`
- `UiRender::renderTextCode`
- `Test::scenarioResult`

## 4. Runtime 계층

runtime 계층은 실제 시스템 동작을 소유합니다.

### 4.1 Input capture / normalization

domain input을 CAN 또는 UDP seam에서 받아 `Core::*`로 정규화합니다.

예:
- vehicle state / steering context
- navigation context / speed limit
- emergency context / timing
- ADAS pre-activation용 object-risk context

### 4.2 Arbitration / fail-safe

runtime arbitration이 만드는 결과:
- selected alert meaning
- risk output
- fail-safe state
- degraded / blocked path decision

이 부분은 panel concern이 아니라 runtime behavior입니다.

### 4.3 Output generation

runtime output은 아래를 구동합니다.
- ambient/body alert
- cluster/HMI warning code
- render-friendly mirror
- verification / trace anchor

## 5. Transport 계층

transport 계층은 runtime을 domain CAN과 Ethernet seam으로 외부에 노출합니다.

### 5.1 Domain CAN

domain-local ECU contract는 domain CAN으로 읽습니다.

주요 DBC:
- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `adas_can.dbc`

### 5.2 Ethernet backbone

inter-domain seam은 active baseline에서 UDP multicast Ethernet으로 읽습니다.

baseline:
- `239.0.2.1:5000`

대표 Ethernet seam:
- `ethVehicleStateMsg`
- `ethSteeringMsg`
- `ethNavContextMsg`
- `ETH_EmergencyAlert`
- `ethSelectedAlertMsg`
- `ethFailSafeStateMsg`
- `ethObjectRiskInputMsg`
- `ethObjectRiskStateMsg`

### 5.3 Transport rule source

transport-level 진실은 아래 문서에서 읽습니다.
- [../../contracts/ethernet-backbone.md](../../contracts/ethernet-backbone.md)
- [../../contracts/communication-matrix.md](../../contracts/communication-matrix.md)
- [../../contracts/multibus-policy.md](../../contracts/multibus-policy.md)
- [../../contracts/ethernet-interface.md](../../contracts/ethernet-interface.md)

## 6. Verification 계층

verification은 의도적으로 explicit하게 분리되어 있습니다.

### 6.1 Scenario / scoring seam

`TEST_SCN`은 system-wide scenario를 구동하고 아래를 씁니다.
- `Test::scenarioResult`

`TEST_BAS`는 baseline result를 집계하고 아래를 씁니다.
- `Test::baseScenarioId`
- `Test::baseScenarioResult`
- `Test::baseFlowCoverageMask`
- `Test::baseTraceSnapshotId`
- `Test::baseTestHealth`

### 6.2 Diagnostic seam

diagnostic observation은 `Diag::*`로 mirror됩니다.

즉 product ECU 자체를 ad-hoc debug owner로 바꾸지 않고도 request/response evidence를 보이게 하는 구조입니다.

### 6.3 Evidence surface

verification evidence는 아래에서 기대합니다.
- trace / write-window observation
- `Test::*` verdict state
- `Diag::*` request/response mirror
- `docs/verification/*`의 official verification docs

## 7. 어디를 먼저 수정할지

| 질문 | 먼저 수정할 곳 |
|---|---|
| CAPL logic / runtime behavior | `src/capl/**` |
| CAPL sync 후 GUI mirror | `cfg/channel_assign/**` |
| bit-level Ethernet contract | `docs/contracts/ethernet-backbone.md` |
| message owner / multibus policy | `docs/contracts/11_*`, `docs/contracts/12_*`, `docs/contracts/13_*` |
| panel/system-variable binding | `docs/contracts/panel-sysvar-contract.md` |
| scenario pass criteria / evidence rule | `docs/verification/**` |

## 8. 설계 원칙

surface는 얇게 유지해야 합니다.

panel과 sysvar surface는 아래만 드러내야 합니다.
- controlled input
- readable output
- verification mirror

surface가 두 번째 runtime implementation이 되면 안 됩니다.
