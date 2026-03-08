# ECU 명명 및 계층 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 3.0
**Date**: 2026-03-09
**Status**: Draft (Architecture Reset Baseline)
**Scope**: `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 1. 목적

- 양산차 프로젝트 표면에 맞는 ECU 계층을 재정의한다.
- `표면 ECU`, `런타임 구현 모듈`, `검증 하네스`를 분리한다.
- GUI, 상위 문서, 하위 구현 문서가 같은 레벨의 이름을 섞어 쓰지 않게 한다.
- architecture reset 기간의 ECU naming SoT로 사용한다.

---

## 2. 핵심 원칙

1. 상위 표면은 production-style ECU 중심으로 보인다.
- 예: `ECM`, `TCM`, `VCU`, `ESP`, `EPS`, `BCM`, `IVI`, `CLUSTER`, `ADAS`, `V2X`, `CGW`

2. 구현 상세는 런타임 모듈로 분리한다.
- 예: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`

3. 검증 하네스는 생산 ECU와 분리한다.
- `VAL_*`
- reviewer-facing vehicle architecture와 섞지 않는다.

4. 이름 변경보다 계층 분리가 먼저다.
- `logical model first, runtime mapping second, evidence update last`

---

## 3. Naming Layer Model

### 3.1 Surface ECU Name

- reviewer-facing vehicle ECU 표면 이름
- `0301/0302/0303`의 기본 owner 언어
- GUI의 상위 표현 이름
- 원칙:
  - 짧고 기능 중심
  - production ECU처럼 읽혀야 함
  - `_TX/_RX/_MGR/_CTRL/_GW`를 직접 노출하지 않음

### 3.2 Runtime Implementation Module

- 실제 CAPL node / 내부 구현 모듈 이름
- `04`, code trace, debugging, ownership 설명에서 유지
- 허용 접미사:
  - `_GW`
  - `_CTRL`
  - `_MGR`
  - `_TX`
  - `_RX`

### 3.3 Validation Harness

- validation-only runtime
- 생산 ECU 아키텍처와 분리 유지
- 명명 규칙:
  - `VAL_*`

---

## 4. 표기 규칙

### 4.1 Surface ECU 표기 규칙

- 공식 표기는 `UPPER_SNAKE_CASE` 또는 업계 통용 약어를 사용한다.
- 현재 승인 baseline:
  - `CGW`
  - `ETH_BACKBONE`
  - `ECM`
  - `TCM`
  - `VCU`
  - `ESP`
  - `EPS`
  - `BCM`
  - `HVAC`
  - `IVI`
  - `CLUSTER`
  - `ADAS`
  - `V2X`
  - `VALIDATION_HARNESS`

### 4.2 Runtime Module 표기 규칙

- 기존 Canonical runtime 이름은 transition baseline으로 유지한다.
- runtime node는 traceability를 위해 당분간 유지 가능하다.
- surface naming을 위해 runtime node를 즉시 rename할 필요는 없다.

### 4.3 Validation 표기 규칙

- validation-only 이름은 반드시 `VAL_*` prefix를 사용한다.
- 제품 ECU 명명층에 흡수하지 않는다.

---

## 5. 금지 규칙

- 상위 문서에서 `_TX/_RX/_MGR/_CTRL/_GW`를 surface ECU처럼 직접 사용하는 것 금지
- GUI rename을 문서 baseline보다 먼저 수행하는 것 금지
- variable/message를 cosmetic consistency만 위해 무리하게 rename하는 것 금지
- validation harness를 production ECU처럼 설명하는 것 금지

---

## 6. Reset Surface ECU Inventory (Approved Baseline)

| Surface ECU | Layer | Runtime Mapping | Status | Notes |
|---|---|---|---|---|
| `CGW` | Infrastructure | `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` | Active | central gateway / boundary surface |
| `ETH_BACKBONE` | Infrastructure | `ETH_SW` | Active | backbone monitor / transport health |
| `ECM` | Production | `ENG_CTRL` | Active | engine / powertrain state |
| `TCM` | Production | `TCM` | Active | transmission control |
| `VCU` | Production | `ACCEL_CTRL` | Active by runtime rename | vehicle longitudinal source surface |
| `ESP` | Production | `BRK_CTRL` | Active by runtime rename | brake / stability surface |
| `EPS` | Production | `STEER_CTRL` | Active by runtime rename | steering surface |
| `BCM` | Production | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` | Active by folded runtime | body / ambient / comfort surface |
| `HVAC` | Production | placeholder only | Placeholder | breadth-only surface for later optional activation |
| `IVI` | Production | `IVI_GW`, `NAV_CTX_MGR` | Active by folded runtime | infotainment / navigation service surface |
| `CLUSTER` | Production | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` | Active by folded runtime | cluster display / warning surface |
| `ADAS` | Production | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` | Active by folded runtime | risk evaluation and warning arbitration |
| `V2X` | Production | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | Active by folded runtime | emergency/V2X path surface |
| `VALIDATION_HARNESS` | Validation | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` | Active | non-production harness |

---

## 7. Runtime Transition Baseline

| Current Runtime Node | Target Surface ECU | Runtime Policy | Notes |
|---|---|---|---|
| `ENG_CTRL` | `ECM` | Keep split | already ECU-like |
| `TCM` | `TCM` | Keep split | already ECU-like |
| `ACCEL_CTRL` | `VCU` | Keep split for now | surface rename first, merge later optional |
| `BRK_CTRL` | `ESP` | Keep split | good standalone brake/stability runtime |
| `STEER_CTRL` | `EPS` | Keep split | good standalone steering runtime |
| `CHS_GW` | `CGW` | Keep split | infrastructure ingress gateway |
| `INFOTAINMENT_GW` | `CGW` | Keep split | infrastructure ingress gateway |
| `DOMAIN_ROUTER` | `CGW` | Keep split | routing / integration |
| `DOMAIN_BOUNDARY_MGR` | `CGW` | Keep split | path health / fail-safe |
| `ETH_SW` | `ETH_BACKBONE` | Keep split | backbone health monitor |
| `BODY_GW` | `BCM` | Keep split | internal BCM frame producer |
| `AMBIENT_CTRL` | `BCM` | Keep split | internal BCM output owner |
| `HAZARD_CTRL` | `BCM` | Merge candidate | too small as standalone runtime surface |
| `WINDOW_CTRL` | `BCM` | Merge candidate | body comfort subfunction |
| `DRV_STATE_MGR` | `BCM` | Merge candidate | currently placeholder |
| `IVI_GW` | `IVI` | Keep split | internal IVI frame producer |
| `NAV_CTX_MGR` | `IVI` | Merge candidate | pure context logic |
| `CLU_HMI_CTRL` | `CLUSTER` | Keep split | main cluster state owner |
| `CLU_BASE_CTRL` | `CLUSTER` | Merge candidate | cluster subfunction |
| `ADAS_WARN_CTRL` | `ADAS` | Keep split | core logic with debug value |
| `WARN_ARB_MGR` | `ADAS` | Keep split | arbitration / fail-safe split valuable |
| `EMS_POLICE_TX` | `V2X` | Merge candidate | internal producer path |
| `EMS_AMB_TX` | `V2X` | Merge candidate | internal producer path |
| `EMS_ALERT_RX` | `V2X` | Keep split (merge base) | watchdog / timeout / priority core |
| `VAL_SCENARIO_CTRL` | `VALIDATION_HARNESS` | Keep split | validation only |
| `VAL_BASELINE_CTRL` | `VALIDATION_HARNESS` | Keep split | validation only |

---

## 8. 문서 전파 규칙

- 전파 순서:
  - `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07 -> GUI`
- 상위 문서(`0301/0302/0303`)는 surface ECU 언어를 먼저 사용한다.
- `0304`는 변수 안정성을 유지하고 `Var -> Runtime -> Surface` 매핑을 추가한다.
- `04`는 runtime module reality를 유지한다.
- 세부 규칙은 다음 문서를 따른다.
  - `tmp/change-orders/ECU_RESET_DOC_PROPAGATION_RULES_2026-03-09.md`

---

## 9. 적용 경계

- `01`은 ECU naming 세부 구현을 설명하지 않는다.
- `0301/0302/0303`은 reviewer-facing surface를 우선한다.
- `04`는 implementation module을 유지한다.
- `05/06/07`은 test title은 surface 중심, log/evidence는 runtime 이름 허용.

---

## 10. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.0 | 2026-03-09 | architecture reset baseline으로 전면 재작성. `surface ECU / runtime module / validation harness` 3층 구조와 target surface inventory 확정. |
| 2.9 | 2026-03-08 | Architecture reset 승인 반영: Status를 `Draft (Architecture Reset In Progress)`로 전환하고, 기존 Canonical Matrix를 transition baseline으로 재정의. logical ECU surface / implementation module / validation harness 분리 원칙 추가. |
| 2.8 | 2026-03-08 | 멘토 D11 해석 반영: `_TX/_RX` 사용 경계를 상위 체인/구현 계층으로 분리 명시. 팀 내부 개발 편의용 `3-글자 Quick Tag` 섹션(보조 식별자)을 추가. |
