# ECU 명명 및 약어 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 2.6
**Date**: 2026-03-05
**Status**: Released (SoT Fixed)
**Scope**: `01 -> 03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 1. 목적

- ECU 명칭과 약어를 단일 규칙으로 통일한다.
- 문서/DBC/CAPL 간 명칭 불일치와 감사 리스크를 제거한다.
- 본 문서를 ECU 명명 정책 SoT로 고정한다.

---

## 2. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | AUTOSAR CP SWC Modeling Guide (R24-11, 6.3.1/6.3.3) | shortName 제약, 명명 일관성 |
| 프로세스 | Automotive SPICE, ISO 26262 | 추적성/검증성/변경관리 |
| 연계 SoT | `00g_RTE_Name_Mapping_Standard.md` | RTE 생성명 규칙 분리 적용 |
| 내부 SoT | `0301`, `04`, `canoe/databases/*.dbc` | 실제 노드/소유/구현 기준 |
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
- 본 문서 Canonical로 정의된 약어형을 임의 변형해 사용 금지.
- 풀네임 노드명(`NAV_CONTEXT_MGR`, `CHASSIS_GW`, `ETH_SWITCH`, `DOMAIN_GW_ROUTER`, `ACCEL_CTRL`, `BRAKE_CTRL`, `STEERING_CTRL`, `BCM_AMBIENT_CTRL`, `DRIVER_STATE_CTRL`, `CLUSTER_BASE_CTRL`, `ENGINE_CTRL`, `TRANSMISSION_CTRL`)을 Active 체인에 신규 사용 금지.
- `AMB`는 `Ambient` 의미 축약으로 사용 금지(혼선 방지). `Ambient`는 항상 `AMBIENT` 풀토큰을 사용한다.
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
| `TCM` | Transmission Control Module | Canonical 약어로 허용 |
| `AMB` | Ambulance | `EMS_AMB_TX` 구현 literal에서만 허용 (Ambient 의미로 사용 금지) |

## 3.4 AUTOSAR shortName 적용 원칙

- 프로젝트 공식명(Canonical)은 `UPPER_SNAKE_CASE`를 유지한다.
- AUTOSAR 모델명은 `UpperCamelCase` shortName을 사용한다.
- shortName 기본 제약: 영문 기반 식별자, 1..128, namespace unique.
- RTE 생성 함수명 규칙/길이 예산/샘플 검토는 `00g_RTE_Name_Mapping_Standard.md`를 단일 SoT로 적용한다.

---

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
| Chassis | `ACCL_CTRL` | `ACCELERATION_CONTROLLER` | `AcclCtrl` | - | Active |
| Chassis | `BRK_CTRL` | `BRAKE_CONTROLLER` | `BrkCtrl` | - | Active |
| Chassis | `STRG_CTRL` | `STEERING_CONTROLLER` | `StrgCtrl` | - | Active |
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

## 5. 적용 정책/운영 경계

- 신규 ECU 포함 전체 ECU에 Canonical 명칭 적용.
- Full Name(확장형) 열은 가독성/온보딩/리뷰용 매핑 기준으로 유지한다.
- Legacy Alias는 폐기/이관 대상 표기만 유지하고, 신규 반영 금지한다.
- Project-Specific ECU는 4.1 간략 등록 표로 유지하고, 상세 근거 아티팩트는 운영 문서(03/04/0302/0303)에서 관리한다.
- ECU 명명 규칙의 명시적 관리 문서는 `00e`로 고정하고, 참조 문서는 `03`(ECU 적용)으로 한정한다.
- RTE 생성명 정책은 `00g_RTE_Name_Mapping_Standard.md`를 SoT로 하고, 참조 문서는 `04`로 한정한다.
- `01/0301/0302/0303/0304/05/06/07`은 Canonical 명칭만 사용하고, 규칙 본문은 중복 정의하지 않는다.
- 개발팀 수용 기준:
  - cfg/channel_assign/CAPL/문서에서 legacy 표기 0건
  - `VAL_*` 명칭 일관성 100%

---

## 6. SoT 필수 섹션 체크리스트 (Baseline Gate)

| 체크 항목 | 기준 | 상태 |
|---|---|---|
| Scope/Status 고정 | `Status=Released (SoT Fixed)` 유지 | Locked |
| 계층 분리 | Canonical/shortName 계층 분리 정의 (RTE는 00g 분리) | Locked |
| AUTOSAR 근거 | R24-11 shortName 제약 반영 | Locked |
| 약어 사전 | Canonical 약어 + Full Name 확장 규칙 명시 | Locked |
| Canonical Matrix | 활성 ECU Canonical/Full Name/shortName/Legacy 매핑 표 보유 | Locked |
| 운영 경계 | 명시 관리 `00e`, 참조 `03(ECU)` 한정 | Locked |
| 추적 가능성 | 신규 ECU 시 Canonical+shortName 등록 | Locked |

---

## 7. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.6 | 2026-03-05 | 4.1을 간략 등록 표로 축약하고 근거 아티팩트 열을 제거(요약형 유지). |
| 2.5 | 2026-03-05 | `canoe/src·databases·docs` 근거를 사용한 `Project-Specific ECU Registry`(4.1) 추가. |
| 2.4 | 2026-03-05 | Full Name(확장형) 열을 약어 없는 명시적 풀네임으로 전면 정규화. |
| 2.3 | 2026-03-05 | 현업 매핑 가독성 강화를 위해 Canonical Matrix에 `Full Name(확장형)` 열을 추가하고, Legacy는 폐기 Alias 전용으로 분리. |
| 2.2 | 2026-03-05 | 멘토 피드백 반영: Canonical을 약어형으로 전환하고, 풀네임은 Legacy 매핑으로 유지. 01~07 체인 약어형 정합 기준으로 갱신. |
| 2.1 | 2026-03-05 | RTE 매핑 규칙을 `00g_RTE_Name_Mapping_Standard.md`로 분리하고, 00e는 ECU 명명/약어/Canonical 정책 SoT로 재정렬. |
| 2.0 | 2026-03-05 | SoT 확정본 고정: Status를 `Released (SoT Fixed)`로 전환하고, 운영 경계를 `00e(관리)+03(ECU 참조)+04(RTE 참조)`로 정리, Baseline Gate 체크리스트를 추가. |
| 1.2 | 2026-03-05 | AUTOSAR 6.3.1 길이제약 연계, Canonical->shortName 변환 규칙, RTE name budget 운영기준 추가. |
| 1.1 | 2026-03-05 | AUTOSAR RTE name mapping(`SWS_Rte_1153/3837`) 기반 제약(토큰 길이/계층 분리/리뷰 체크포인트) 추가. |
| 1.0 | 2026-03-05 | 통합 문서에서 ECU 명명/약어 표준을 00e로 분리 |
