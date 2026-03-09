# ECU 명명 및 약어 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 2.7
**Date**: 2026-03-05
**Status**: Released (SoT Fixed)
**Scope**: `01 -> 03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 3.1 기본 규칙

- 공식 표기는 `UPPER_SNAKE_CASE`.
- 형식은 `<DOMAIN_OR_FUNC>_<ROLE>`.
- 역할 접미사 허용 집합: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`, `_DEV`.
- Validation 노드는 `VAL_*` 접두를 사용한다.

## 3.2 금지 규칙

- `CONTROL`/`CTRL` 혼용 금지.
- 본 문서 Canonical로 정의된 약어형을 임의 변형해 사용 금지.
- 풀네임/Legacy 노드명(`NAV_CONTEXT_MGR`, `CHASSIS_GW`, `ETH_SWITCH`, `DOMAIN_GW_ROUTER`, `BRAKE_CTRL`, `STEERING_CTRL`, `BCM_AMBIENT_CTRL`, `DRIVER_STATE_CTRL`, `CLUSTER_BASE_CTRL`, `ENGINE_CTRL`, `TRANSMISSION_CTRL`, `ACCL_CTRL`, `STRG_CTRL`)을 Active 체인에 신규 사용 금지.
- `AMB`는 `Ambient` 의미 축약으로 사용 금지(혼선 방지). `Ambient`는 항상 `AMBIENT` 풀토큰을 사용한다.
- 공식 체인(Req->...->Test)에 연결된 노드명 임의 변경 금지.

## 4. ECU 명명표 (Canonical Matrix)

| Domain | Canonical ECU Name (약어형) | Full Name (확장형) | AUTOSAR shortName | Legacy/비권장 Alias | 상태 |
|---|---|---|---|---|---|
| Core | `ADAS_WARN_CTRL` | `ADAS_WARNING_CONTROLLER` | `AdasWarnCtrl` | - | Active |
| Core | `NAV_CTX_MGR` | `NAVIGATION_CONTEXT_MANAGER` | `NavCtxMgr` | - | Active |
| Core | `WARN_ARB_MGR` | `WARNING_ARBITRATION_MANAGER` | `WarnArbMgr` | - | Active |
| Core | `EMS_ALERT` | `EMERGENCY_ALERT` | `EmsAlert` | - | Active |
| EMS Internal | `EMS_POLICE_TX` | `EMERGENCY_POLICE_TRANSMIT` | `EmsPoliceTx` | - | Active |
| EMS Internal | `EMS_AMB_TX` | `EMERGENCY_AMBULANCE_TRANSMIT` | `EmsAmbTx` | - | Active (`AMB=Ambulance` literal) |
| EMS Internal | `EMS_ALERT_RX` | `EMERGENCY_ALERT_RECEIVE` | `EmsAlertRx` | - | Active |
| Validation | `VAL_SCENARIO_CTRL` | `VALIDATION_SCENARIO_CONTROLLER` | `ValScenarioCtrl` | `SIL_TEST_CTRL`, `SIL_TST` | Active (legacy 금지) |
| Validation | `VAL_BASELINE_CTRL` | `VALIDATION_BASELINE_CONTROLLER` | `ValBaselineCtrl` | `VEHICLE_BASE_TEST_CTRL`, `VEH_BASE_TST` | Active (legacy 금지) |
| Gateway/Infra | `CHS_GW` | `CHASSIS_GATEWAY` | `ChsGw` | - | Active |
| Gateway/Infra | `INFOTAINMENT_GW` | `INFOTAINMENT_GATEWAY` | `InfotainmentGw` | - | Active |
| Gateway/Infra | `BODY_GW` | `BODY_GATEWAY` | `BodyGw` | - | Active |
| Gateway/Infra | `IVI_GW` | `IN_VEHICLE_INFOTAINMENT_GATEWAY` | `IviGw` | - | Active |
| Gateway/Infra | `ETH_SW` | `ETHERNET_SWITCH` | `EthSw` | - | Active |
| Gateway/Infra | `DOMAIN_ROUTER` | `DOMAIN_GATEWAY_ROUTER` | `DomainRouter` | - | Active |
| Gateway/Infra | `DOMAIN_BOUNDARY_MGR` | `DOMAIN_BOUNDARY_MANAGER` | `DomainBoundaryMgr` | - | Active |
| Chassis | `ACCEL_CTRL` | `ACCELERATION_CONTROLLER` | `AccelCtrl` | `ACCL_CTRL` | Active |
| Chassis | `BRK_CTRL` | `BRAKE_CONTROLLER` | `BrkCtrl` | - | Active |
| Chassis | `STEER_CTRL` | `STEERING_CONTROLLER` | `SteerCtrl` | `STRG_CTRL` | Active |
| Body | `AMBIENT_CTRL` | `BODY_CONTROL_MODULE_AMBIENT_CONTROLLER` | `AmbientCtrl` | - | Active |
| Body | `HAZARD_CTRL` | `HAZARD_CONTROLLER` | `HazardCtrl` | - | Active |
| Body | `WINDOW_CTRL` | `WINDOW_CONTROLLER` | `WindowCtrl` | - | Active |
| Body | `DRV_STATE_MGR` | `DRIVER_STATE_MANAGER` | `DrvStateMgr` | - | Active |
| Infotainment | `CLU_HMI_CTRL` | `CLUSTER_HUMAN_MACHINE_INTERFACE_CONTROLLER` | `CluHmiCtrl` | - | Active |
| Infotainment | `CLU_BASE_CTRL` | `CLUSTER_BASE_CONTROLLER` | `CluBaseCtrl` | - | Active |
| Powertrain | `ENG_CTRL` | `ENGINE_CONTROLLER` | `EngCtrl` | - | Active |
| Powertrain | `TCM` | `TRANSMISSION_CONTROL_MODULE` | `Tcm` | - | Active |

### 4.1 Project-Specific ECU (프로젝트 신설 ECU 정의)

| 구분 | Canonical 묶음 | 설명 |
|---|---|---|
| 경고 코어 | `ADAS_WARN_CTRL`, `NAV_CTX_MGR`, `WARN_ARB_MGR` | 프로젝트 경고 판단/중재 핵심 노드 |
| 긴급 처리 | `EMS_ALERT`, `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | 긴급 신호 송수신/해제 처리 노드 |
| 검증 하네스 | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` | SIL 시나리오 실행/판정 노드 |
| 경계/강등 | `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` | 도메인 경계 및 Fail-safe 강등 노드 |

---

