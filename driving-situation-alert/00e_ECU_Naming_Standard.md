# ECU 명명 및 약어 표준

**Document ID**: PROJ-00E-ECU-NAMING  
**Version**: 2.0  
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
| 국제/산업 | AUTOSAR CP SWC Modeling Guide (R24-11, 6.3.1/6.3.3) | shortName 제약, RTE 생성명 연결 규칙 |
| 프로세스 | Automotive SPICE, ISO 26262 | 추적성/검증성/변경관리 |
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

## 3.4 AUTOSAR 정합 (3계층 이름체계)

- 프로젝트 공식명(Canonical)은 `UPPER_SNAKE_CASE`를 유지한다.
- AUTOSAR 모델명은 `UpperCamelCase` shortName을 사용한다.
- RTE C API 명칭은 shortName 연결 결과로 생성된 값을 사용한다.
- shortName 기본 제약: 영문 기반 식별자, 1..128, namespace unique.

| 계층 | 목적 | 규칙 | 예시 |
|---|---|---|---|
| Project Canonical | 문서/DBC/CAPL/리뷰 기준명 | `UPPER_SNAKE_CASE` | `WARN_ARB_MGR` |
| AUTOSAR shortName | SW-C/Port/Runnable 모델링명 | `UpperCamelCase` | `WarnArbMgr` |
| RTE Generated | 코드 생성 API명 | `Rte_*` 연결 규칙 | `Rte_IRead_WarnArbMgr_InAlert_AlertState` |

## 3.5 RTE Name Mapping 규칙 (AUTOSAR CP R24-11 반영)

- AUTOSAR CP SWC Modeling Guide 6.3.3 기준으로, 모델 shortName은 RTE C 함수명으로 연결된다.
- 적용 근거: `SWS_Rte_1153`, `SWS_Rte_3837`.
- 생성명 패턴(대표):
  - `Rte_IRead_<Runnable>_<Port>_<DataElement>`
  - `Rte_IRead_<Component>_<Runnable>_<Port>_<DataElement>`
- 원문 예시 토큰: `Wshr`, `WshrFrnt`, `Monr`, `OutdT`, `Val`.
- 원문 예시 생성명:
  - `Rte_IRead_Monr_OutdT_Val`
  - `Rte_IRead_Wshr_Monr_OutdT_Val`

### 3.5.1 Length Restriction 연계 (6.3.1)

- RTE 생성명은 모델 요소명 연결 길이에 비례해 급격히 길어질 수 있다.
- AUTOSAR 원문 예시: 단일 모델명이 최대 128일 경우 `Rte_IWrite_<Runnable>_<Port>_<Data>` 형식은 이론상 최대 397자까지 증가 가능하다.
- 프로젝트 품질 규칙(가독성/리뷰성):
  - `Rte_IRead/IWrite_<Runnable>_<Port>_<DataElement>`: 권장 `<= 64`
  - `Rte_IRead/IWrite_<Component>_<Runnable>_<Port>_<DataElement>`: 권장 `<= 80`
  - 권장값 초과 시 shortName 재설계(토큰 길이 축소, 중복 어근 제거)를 우선 적용한다.

### 3.5.2 프로젝트 적용 제약

- Canonical ECU명(`UPPER_SNAKE_CASE`)은 문서/DBC/CAPL 표준으로 유지한다.
- AUTOSAR shortName은 RTE 생성명 충돌/과장길이 방지를 위해 토큰 길이를 관리한다.
- shortName 토큰 권장 길이:
  - SW-C/Prototype: `<= 16`
  - Runnable: `<= 12`
  - Port/DataElement: `<= 12`
- 토큰은 의미 기반 약어만 허용하고, 임의 축약/모음제거형은 금지한다.
- 대소문자만 다른 shortName 금지(사람/도구 혼동 방지).

### 3.5.3 Canonical -> shortName 변환 규칙

- Canonical 토큰(`_`)을 기준으로 단어 경계를 유지한다.
- shortName은 각 토큰의 의미를 유지한 `UpperCamelCase`로 변환한다.
- 역할 토큰(`CTRL`, `MGR`, `GW`, `TX`, `RX`, `DEV`)은 축약 해제 없이 그대로 보존한다.
- 예시:
  - `NAV_CONTEXT_MGR` -> `NavContextMgr`
  - `VAL_SCENARIO_CTRL` -> `ValScenarioCtrl`
  - `DOMAIN_GW_ROUTER` -> `DomainGwRouter`

### 3.5.4 설계/리뷰 체크포인트

- ECU 신규/변경 시 Canonical + AUTOSAR shortName을 동시에 등록한다.
- RTE 함수명 샘플 2개 이상을 산출해 과도한 길이/중복을 사전 점검한다.
- 포트/데이터명 변경 시 기존 생성 함수명과의 역추적 가능성을 유지한다.

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

## 5. 적용 정책/운영 경계

- 신규 ECU 포함 전체 ECU에 Canonical 명칭 적용.
- Legacy 표기는 검색/이관 alias 용도로만 유지, 신규 반영 금지.
- ECU 명명 규칙의 명시적 관리 문서는 `00e`, `0301`, `04`로 한정한다.
- `01/03/0302/0303/0304/05/06/07`은 Canonical 명칭만 사용하고, 규칙 본문은 중복 정의하지 않는다.
- 개발팀 수용 기준:
  - cfg/channel_assign/CAPL/문서에서 legacy 표기 0건
  - `VAL_*` 명칭 일관성 100%

---

## 6. SoT 필수 섹션 체크리스트 (Baseline Gate)

| 체크 항목 | 기준 | 상태 |
|---|---|---|
| Scope/Status 고정 | `Status=Released (SoT Fixed)` 유지 | Locked |
| 3계층 이름체계 | Canonical/shortName/RTE 계층 분리 정의 | Locked |
| AUTOSAR 근거 | R24-11 `6.3.1`, `6.3.3`, `SWS_Rte_1153/3837` 반영 | Locked |
| 약어 사전 | 허용 약어 + 금지 축약 규칙 명시 | Locked |
| Canonical Matrix | 활성 ECU Canonical/shortName/Legacy 매핑 표 보유 | Locked |
| 운영 경계 | 명시적 관리 문서 `00e/0301/04` 한정 | Locked |
| 추적 가능성 | 신규 ECU 시 Canonical+shortName+RTE 샘플 2건 등록 | Locked |

---

## 7. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.0 | 2026-03-05 | SoT 확정본 고정: Status를 `Released (SoT Fixed)`로 전환하고, 운영 경계(`00e/0301/04`)와 Baseline Gate 체크리스트를 추가. |
| 1.2 | 2026-03-05 | AUTOSAR 6.3.1 길이제약 연계, Canonical->shortName 변환 규칙, RTE name budget 운영기준 추가. |
| 1.1 | 2026-03-05 | AUTOSAR RTE name mapping(`SWS_Rte_1153/3837`) 기반 제약(토큰 길이/계층 분리/리뷰 체크포인트) 추가. |
| 1.0 | 2026-03-05 | 통합 문서에서 ECU 명명/약어 표준을 00e로 분리 |
