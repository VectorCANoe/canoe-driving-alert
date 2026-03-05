# ECU 명명 및 약어 표준

**Document ID**: PROJ-00E-ECU-NAMING  
**Version**: 1.0  
**Date**: 2026-03-05  
**Status**: Draft  
**Scope**: `01 -> 03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 1. 목적

- ECU 명칭과 약어를 단일 규칙으로 통일한다.
- 문서/DBC/CAPL 간 명칭 불일치와 감사 리스크를 제거한다.

---

## 2. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | AUTOSAR CP SWC Modeling Guide | shortName 제약, 약어 정책 |
| 프로세스 | Automotive SPICE, ISO 26262 | 추적성/검증성/변경관리 |
| 내부 SoT | `0301`, `03`, `canoe/databases/*.dbc` | 실제 노드/소유 기준 |
| 멘토링 | MET40 | `VAL_*` 명명, 오해 유발 명칭 제거 |

---

## 3. 명명 규칙

## 3.1 기본 규칙

- 공식 표기는 `UPPER_SNAKE_CASE`.
- 형식은 `<DOMAIN_OR_FUNC>_<ROLE>`.
- 역할 접미사 허용 집합: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`, `_DEV`.
- Validation 노드는 `VAL_*` 접두를 사용한다.

## 3.2 금지 규칙

- `CONTROL`/`CTRL` 혼용 금지.
- 임의 축약 금지: `ACCL`, `STRG`, `BRK`, `ENG`, `CTX`, `SIL_TST`, `VEH_BASE_TST`.
- 공식 체인(Req->...->Test)에 연결된 노드명 임의 변경 금지.

## 3.3 통제 약어 사전

| 약어 | 의미 | 사용 규칙 |
|---|---|---|
| `CTRL` | Controller/Control | 제어/판단 주체 |
| `MGR` | Manager | 중재/상태관리 주체 |
| `GW` | Gateway | 도메인/버스 경계 변환 |
| `TX` | Transmit | 내부 송신 모듈 |
| `RX` | Receive | 내부 수신 모듈 |
| `VAL` | Validation | 검증 하네스 접두 |
| `EMS` | Emergency context | 긴급 경고 계열 |
| `ADAS` | ADAS | ADAS 기능 계열 |
| `HMI` | Human Machine Interface | 표시/UI 계열 |
| `BCM` | Body Control Module | Body 제어 계열 |
| `CLU` | Cluster | 클러스터 계열 |
| `IVI` | In-Vehicle Infotainment | IVI/도메인 계열 |
| `NAV` | Navigation | 내비게이션 계열 |
| `ARB` | Arbitration | 중재 계열 |
| `ETH` | Ethernet | 백본/경로 계열 |
| `PT` | Powertrain | 파워트레인 확장 식별 |
| `TCM` | Transmission Control Module | 외부 비교용 약어만 허용 |

## 3.4 AUTOSAR 정합

- 프로젝트 공식명은 `UPPER_SNAKE_CASE` 유지.
- AUTOSAR 연계 시 별도 shortName(UpperCamelCase) 매핑 사용.
- shortName 기본 제약: 영문, 1..128, namespace unique, 식별자 유효.

---

## 4. ECU 명명표 (Canonical Matrix)

| Domain | Canonical ECU Name | AUTOSAR shortName | Legacy/비권장 표기 | 상태 |
|---|---|---|---|---|
| Core | `ADAS_WARN_CTRL` | `AdasWarnCtrl` | - | Active |
| Core | `NAV_CONTEXT_MGR` | `NavContextMgr` | `NAV_CTX_MGR` | Active (legacy 금지) |
| Core | `WARN_ARB_MGR` | `WarnArbMgr` | - | Active |
| Core | `EMS_ALERT` | `EmsAlert` | - | Active |
| EMS Internal | `EMS_POLICE_TX` | `EmsPoliceTx` | - | Active |
| EMS Internal | `EMS_AMB_TX` | `EmsAmbTx` | - | Active |
| EMS Internal | `EMS_ALERT_RX` | `EmsAlertRx` | - | Active |
| Validation | `VAL_SCENARIO_CTRL` | `ValScenarioCtrl` | `SIL_TEST_CTRL`, `SIL_TST` | Active (legacy 금지) |
| Validation | `VAL_BASELINE_CTRL` | `ValBaselineCtrl` | `VEHICLE_BASE_TEST_CTRL`, `VEH_BASE_TST` | Active (legacy 금지) |
| Gateway/Infra | `CHASSIS_GW` | `ChassisGw` | `CHS_GW` | Active (legacy 금지) |
| Gateway/Infra | `INFOTAINMENT_GW` | `InfotainmentGw` | - | Active |
| Gateway/Infra | `BODY_GW` | `BodyGw` | - | Active |
| Gateway/Infra | `IVI_GW` | `IviGw` | - | Active |
| Gateway/Infra | `ETH_SWITCH` | `EthSwitch` | `ETH_SW` | Active (legacy 금지) |
| Gateway/Infra | `DOMAIN_GW_ROUTER` | `DomainGwRouter` | `DOMAIN_ROUTER` | Active (legacy 금지) |
| Gateway/Infra | `DOMAIN_BOUNDARY_MGR` | `DomainBoundaryMgr` | - | Active |
| Chassis | `ACCEL_CTRL` | `AccelCtrl` | `ACCL_CTRL` | Active (legacy 금지) |
| Chassis | `BRAKE_CTRL` | `BrakeCtrl` | `BRK_CTRL` | Active (legacy 금지) |
| Chassis | `STEERING_CTRL` | `SteeringCtrl` | `STRG_CTRL` | Active (legacy 금지) |
| Body | `BCM_AMBIENT_CTRL` | `BcmAmbientCtrl` | `AMBIENT_CTRL` | Active (legacy 금지) |
| Body | `HAZARD_CTRL` | `HazardCtrl` | - | Active |
| Body | `WINDOW_CTRL` | `WindowCtrl` | - | Active |
| Body | `DRIVER_STATE_CTRL` | `DriverStateCtrl` | `DRV_STATE_MGR` | Active (legacy 금지) |
| Infotainment | `CLU_HMI_CTRL` | `CluHmiCtrl` | - | Active |
| Infotainment | `CLUSTER_BASE_CTRL` | `ClusterBaseCtrl` | `CLU_BASE_CTRL` | Active (legacy 금지) |
| Powertrain | `ENGINE_CTRL` | `EngineCtrl` | `ENG_CTRL` | Active (legacy 금지) |
| Powertrain | `TRANSMISSION_CTRL` | `TransmissionCtrl` | `TCM` | Active (legacy 금지) |

---

## 5. 적용 정책

- 신규 ECU 포함 전체 ECU에 Canonical 명칭 적용.
- Legacy 표기는 검색/이관 alias 용도로만 유지, 신규 반영 금지.
- 개발팀 수용 기준:
  - cfg/channel_assign/CAPL/문서에서 legacy 표기 0건
  - `VAL_*` 명칭 일관성 100%

---

## 6. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-03-05 | 통합 문서에서 ECU 명명/약어 표준을 00e로 분리 |
