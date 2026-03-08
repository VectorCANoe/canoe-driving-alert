# ECU 명명 및 계층 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 3.1
**Date**: 2026-03-09
**Status**: Draft (Architecture Reset Baseline)
**Scope**: `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 1. 목적

- 양산차(OEM) 수준의 ECU 표면 구조를 문서 SoT로 고정한다.
- `Surface ECU`, `Runtime Module`, `Validation Harness`를 분리해 혼용을 방지한다.
- 프로젝트 핵심가치(구간/긴급차량 기반 실시간 경고)를 차량 전체 구조 안에서 일관되게 표현한다.

---

## 2. 핵심 원칙

1. 상위 표면은 생산 ECU처럼 보인다.
- 예: `ECM`, `TCM`, `VCU`, `ESP`, `EPS`, `BCM`, `IVI`, `CLUSTER`, `ADAS`, `V2X`, `CGW`

2. 구현 상세는 런타임 모듈로 분리한다.
- 예: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`

3. 검증 하네스는 생산 ECU와 분리한다.
- `VAL_*`
- reviewer-facing vehicle architecture와 섞지 않는다.

4. 이름 변경보다 계층 분리가 우선이다.
- `surface first -> runtime mapping -> evidence sync`

---

## 3. Naming Layer Model

### 3.1 Surface ECU Name

- reviewer-facing ECU 표면 이름
- `0301/0302/0303`의 기본 owner 언어
- 내부 접미사(`_TX/_RX/_MGR/_CTRL/_GW`) 직접 노출 금지

### 3.2 Runtime Implementation Module

- 실제 CAPL node / 구현 모듈 이름
- `04`와 코드 추적에서 유지
- 디버깅과 실제 구현 경계 설명의 기준

### 3.3 Validation Harness

- validation-only runtime
- `VAL_*` 규칙 유지
- 생산 ECU 계층에 흡수 금지

---

## 4. 표기 규칙

### 4.1 Surface ECU 표기

- `UPPER_SNAKE_CASE` 또는 업계 통용 약어 사용
- 기능/도메인 중심 명명, 구현 접미사 금지

### 4.2 Runtime Module 표기

- 기존 canonical runtime 이름 유지
- 구조 리셋 기간에는 surface rename 우선, runtime rename 후행

### 4.3 Validation 표기

- validation-only 노드는 `VAL_*` prefix 고정
- 문서에서 production ECU와 별도 섹션으로 표기

---

## 5. 금지 규칙

- 상위 문서에서 `_TX/_RX/_MGR/_CTRL/_GW`를 surface ECU처럼 직접 사용 금지
- 문서 baseline 없이 GUI/runtime rename 선행 금지
- cosmetic consistency만을 위한 대량 rename 금지
- validation harness를 production ECU처럼 설명 금지

---

## 6. Active Surface ECU Naming Table (Primary-56 + Validation)

| Surface ECU | Category | Runtime Anchor | Status | Notes |
|---|---|---|---|---|
| `CGW` | Infrastructure | `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER` | Anchored | central gateway surface |
| `ETH_BACKBONE` | Infrastructure | `ETH_SW` | Anchored | backbone monitor/transport health |
| `DCM` | Infrastructure | - | Placeholder | diagnostics breadth placeholder |
| `IBOX` | Infrastructure | - | Placeholder | telematics breadth placeholder |
| `SECURITY_GATEWAY` | Infrastructure | `DOMAIN_BOUNDARY_MGR` | Anchored | boundary/security runtime owner |
| `ECM` | Powertrain | `ENG_CTRL` | Anchored | engine runtime anchor |
| `TCM` | Powertrain | `TCM` | Anchored | transmission runtime anchor |
| `VCU` | Powertrain | `ACCEL_CTRL` | Anchored | surface rename first, runtime split 유지 |
| `AWD_4WD` | Powertrain | - | Placeholder | breadth placeholder |
| `BAT_BMS` | Powertrain | - | Placeholder | breadth placeholder |
| `FPCM` | Powertrain | - | Placeholder | breadth placeholder |
| `LVR` | Powertrain | - | Placeholder | breadth placeholder |
| `ISG` | Powertrain | - | Placeholder | breadth placeholder |
| `EOP` | Powertrain | - | Placeholder | breadth placeholder |
| `EWP` | Powertrain | - | Placeholder | breadth placeholder |
| `ESP` | Chassis/Safety | `BRK_CTRL` | Anchored | brake/stability surface |
| `EPS` | Chassis/Safety | `STEER_CTRL` | Anchored | steering surface |
| `ABS` | Chassis/Safety | - | Placeholder | folded into ESP breadth |
| `EPB` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `TPMS` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `SAS` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `ECS` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `ACU` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `ODS` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `VSM` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `EHB` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `CDC` | Chassis/Safety | - | Placeholder | breadth placeholder |
| `BCM` | Body/Comfort | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` | Anchored | body/comfort folded surface |
| `HVAC` | Body/Comfort | - | Placeholder | breadth placeholder |
| `SMK` | Body/Comfort | - | Placeholder | breadth placeholder |
| `AFLS` | Body/Comfort | - | Placeholder | breadth placeholder |
| `LIGHTING_ECU` | Body/Comfort | - | Placeholder | breadth placeholder |
| `WIPER_MODULE` | Body/Comfort | - | Placeholder | breadth placeholder |
| `SUNROOF_MODULE` | Body/Comfort | - | Placeholder | breadth placeholder |
| `DOOR_FL` | Body/Comfort | - | Placeholder | breadth placeholder |
| `DOOR_FR` | Body/Comfort | - | Placeholder | breadth placeholder |
| `TAILGATE_MODULE` | Body/Comfort | - | Placeholder | breadth placeholder |
| `IVI` | IVI/HMI | `IVI_GW`, `NAV_CTX_MGR` | Anchored | IVI surface owner |
| `CLUSTER` | IVI/HMI | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` | Anchored | cluster surface owner |
| `HUD` | IVI/HMI | - | Placeholder | breadth placeholder |
| `TMU` | IVI/HMI | - | Placeholder | deep-next placeholder |
| `AMP` | IVI/HMI | - | Placeholder | breadth placeholder |
| `PGS` | IVI/HMI | - | Placeholder | breadth placeholder |
| `NAV_MODULE` | IVI/HMI | - | Placeholder | represented inside IVI for now |
| `DIGITAL_KEY` | IVI/HMI | - | Placeholder | breadth placeholder |
| `ADAS` | ADAS/V2X | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` | Anchored | risk/arbitration runtime split |
| `V2X` | ADAS/V2X | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | Anchored | emergency/V2X runtime split |
| `SCC` | ADAS/V2X | - | Placeholder | next deep candidate |
| `LDWS_LKAS` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `FCA` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `BCW` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `LCA` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `SPAS` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `RSPA` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `AVM` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `FCAM` | ADAS/V2X | - | Placeholder | breadth placeholder |
| `VALIDATION_HARNESS` | Validation | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` | Active | outside primary production surface |

---

## 7. Runtime-26 Assignment Baseline

| Active Runtime Node | Target Surface ECU | Runtime Policy | Notes |
|---|---|---|---|
| `ENG_CTRL` | `ECM` | Keep split | production-like runtime |
| `TCM` | `TCM` | Keep split | production-like runtime |
| `ACCEL_CTRL` | `VCU` | Keep split | surface rename first |
| `BRK_CTRL` | `ESP` | Keep split | brake/stability nucleus |
| `STEER_CTRL` | `EPS` | Keep split | steering nucleus |
| `CHS_GW` | `CGW` | Keep split | chassis ingress gateway |
| `INFOTAINMENT_GW` | `CGW` | Keep split | IVI ingress gateway |
| `DOMAIN_ROUTER` | `CGW` | Keep split | cross-domain routing |
| `DOMAIN_BOUNDARY_MGR` | `SECURITY_GATEWAY` | Keep split | boundary/security role |
| `ETH_SW` | `ETH_BACKBONE` | Keep split | backbone health monitor |
| `BODY_GW` | `BCM` | Keep split | BCM internal producer |
| `AMBIENT_CTRL` | `BCM` | Keep split | BCM ambient owner |
| `HAZARD_CTRL` | `BCM` | Merge candidate | absorb into BCM later |
| `WINDOW_CTRL` | `BCM` | Merge candidate | absorb into BCM later |
| `DRV_STATE_MGR` | `BCM` | Merge candidate | absorb into BCM later |
| `IVI_GW` | `IVI` | Keep split | IVI frame producer |
| `NAV_CTX_MGR` | `IVI` | Merge candidate | absorb into IVI later |
| `CLU_HMI_CTRL` | `CLUSTER` | Keep split | cluster primary owner |
| `CLU_BASE_CTRL` | `CLUSTER` | Merge candidate | absorb into CLUSTER later |
| `ADAS_WARN_CTRL` | `ADAS` | Keep split | risk/trigger stage |
| `WARN_ARB_MGR` | `ADAS` | Keep split | alert priority stage |
| `EMS_POLICE_TX` | `V2X` | Merge candidate | fold into V2X producer stack |
| `EMS_AMB_TX` | `V2X` | Merge candidate | fold into V2X producer stack |
| `EMS_ALERT_RX` | `V2X` | Keep split / merge base | watchdog/timeout nucleus |
| `VAL_SCENARIO_CTRL` | `VALIDATION_HARNESS` | Keep split | validation only |
| `VAL_BASELINE_CTRL` | `VALIDATION_HARNESS` | Keep split | validation only |

---

## 8. 문서 전파 규칙

- 전파 순서:
  - `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07 -> GUI`
- 상위 문서(`0301/0302/0303`)는 surface ECU 언어를 우선 사용한다.
- `0304`는 `Var -> Runtime -> Surface` 매핑을 유지한다.
- `04`는 runtime reality를 유지하고 merge candidate를 명시한다.

---

## 9. 적용 경계

- `01`은 ECU naming 구현 상세를 다루지 않는다.
- `0301/0302/0303`은 reviewer-facing surface 중심으로 작성한다.
- `04`는 runtime module 현실을 반영한다.
- `05/06/07`은 test title은 surface 중심, log/evidence는 runtime 이름 허용.

---

## 10. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.1 | 2026-03-09 | OEM 확장 반영: `Primary-56 + Validation` 표면 ECU 명명표와 `Runtime-26` 매핑을 SoT 기준으로 재작성. |
| 3.0 | 2026-03-09 | architecture reset baseline으로 전면 재작성. `surface ECU / runtime module / validation harness` 3층 구조 확정. |
| 2.9 | 2026-03-08 | Architecture reset 승인 반영: status를 draft 전환, logical ECU surface / implementation module / validation harness 분리 원칙 추가. |

