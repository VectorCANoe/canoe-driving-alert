# ECU 명명 및 계층 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 3.4
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
- 예: `EMS`, `TCU`, `VCU`, `ESC`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `CGW`, `SGW`

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

## 6. Active ECU Matrix (Commit `6cbb647`, Non-VAL)

`VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`는 컴파일/검증 마감 전이라 이번 동기화에서 제외했다.

| Surface ECU | Runtime Node | Domain | Owner/주요 송신 ID | 역할(요약) |
|---|---|---|---|---|
| `CGW` | `CGW` | Infrastructure | `ethFailSafeStateMsg(0x111)`, `ethObjectSafetyStateMsg(0x1C8)` | 도메인 경계 상태/Fail-safe 권한, 경계 Health 집계 |
| `ETH_BACKBONE` | *(no standalone node)* | Infrastructure | `CGW/V2X/VCU/MDPS/IVI` 내부 ETH seam | 현재 SIL에서는 독립 스위치가 아니라 각 ECU 내부 seam으로 운영 |
| `EMS` | `EMS` | Powertrain | `0x12A,0x12B,0x12C,0x12E,0x12F,0x131` | 엔진/열관리 상태 생성 |
| `TCU` | `TCU` | Powertrain | `0x12D,0x130` | 변속 상태/온도 생성 |
| `VCU` | `VCU` | Powertrain | `0x109,0x10A,0x10B,0x10C,0x10D,0x10E,0x10F,0x110,0x121,0x126,0x510` | 차량 상태/동력 정책/ETH vehicle-state seam |
| `ESC` | `ESC` | Chassis/Safety | `0x101~0x108,0x120,0x122~0x129` | 제동/차체 안정화 상태 생성 |
| `MDPS` | `MDPS` | Chassis/Safety | `0x100,0x102,0x103,0x104,0x511` | 조향 상태 생성 및 ETH steering seam |
| `BCM` | `BCM` | Body/Comfort | `0x260~0x277` | 바디/편의/실내 출력 통합 Owner |
| `IVI` | `IVI` | IVI/HMI | `0x280~0x295`, `0x512` | 내비 문맥/클러스터 출력/HMI 상태 Owner |
| `CLU` | `CLU` | IVI/HMI | *(consumer/mirror 중심, 현재 전용 Tx 없음)* | 클러스터 표시 소비/미러 계층 |
| `ADAS` | `ADAS` | ADAS/V2X | `0x1C1,0x1C3,0x1C4,0x1C6,0x1C7,0x206` | 위험도/경보 선택/감속요청 통합 판정 |
| `V2X` | `V2X` | ADAS/V2X | `0x1C0,0x1C2` | 긴급차량 브로드캐스트/모니터 통합 Owner |

### 6.1 Primary-56 Placeholder Policy

- Primary-56 중 위 표에 없는 ECU는 `Placeholder`로 유지한다.
- Placeholder는 아키텍처 폭 표현용이며, CAPL runtime node를 즉시 생성하지 않는다.

### 6.2 OEM Visible Bank Policy (Commit `56521c2`)

- 현재 CANoe visible import bank는 다음 3층으로 고정한다.
  - Deep runtime anchors: `13`
  - Validation harness nodes: `2` (`VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`)
  - Placeholder surface nodes: `87`
- 총 visible node 수는 `100`이며, placeholder는 `OEM 표면 폭` 표현만 담당한다.
- Placeholder 노드는 다음 규칙을 따른다.
  - deep runtime logic을 포함하지 않는다.
  - owner/ID/주기 계약은 할당하지 않는다.
  - 향후 승격 시 해당 surface ECU의 runtime anchor로 흡수한다(별도 내부 wrapper 재증설 금지).
- domain 분포(`16/23/13/14/8/26`)는 `canoe/cfg/channel_assign/DOMAIN_INDEX.md`와 동일하게 유지한다.

### 6.3 Domestic OEM Canonical Abbreviation Policy

- 개발/문서 SoT의 Surface ECU는 국내 OEM 관행 약어형을 Canonical로 고정한다.
- reviewer-facing 문서에서도 아래 Canonical을 우선 사용한다.
- 풀네임(영문 설명형)은 alias(설명/주석)로만 허용하고, canonical 치환용으로 사용하지 않는다.

| Canonical (고정) | Alias (설명용) | 비고 |
|---|---|---|
| `SGW` | `SECURITY_GATEWAY` | 보안 게이트웨이 |
| `_4WD` | `AWD_4WD` | 4WD 제어 표면명 |
| `DATC` | `HVAC` | 공조 제어 |
| `AHLS` | `LIGHTING_ECU` | 조명 제어 |
| `EDR` | `EDGE_LOGGER` | 이벤트 기록/로그 |

추가 canonical 기준:
- `EMS`, `TCU`, `ESC`, `MDPS`, `CLU`를 표면명으로 사용한다.
- `ECM`, `TCM`, `ESP`, `EPS`, `CLUSTER`는 legacy alias로만 관리한다.

---

## 7. Runtime Assignment Policy (Non-VAL)

| Runtime Node | Target Surface ECU | Runtime Policy | 비고 |
|---|---|---|---|
| `EMS` | `EMS` | Keep split | legacy `ENG_CTRL` 흡수 후 정착 |
| `TCU` | `TCU` | Keep split | legacy `TCM` rename 정착 |
| `VCU` | `VCU` | Keep split | 내부 PTGW seam 유지 |
| `ESC` | `ESC` | Keep split | legacy `BRK_CTRL` 흡수 |
| `MDPS` | `MDPS` | Keep split | legacy `STEER_CTRL` 흡수 |
| `CGW` | `CGW` | Keep split | 경계/Failsafe 권한 고정 |
| `BCM` | `BCM` | Keep split | body wrapper 흡수 완료 |
| `IVI` | `IVI` | Keep split | infotainment wrapper 흡수 완료 |
| `CLU` | `CLU` | Keep split | cluster helper 흡수 완료 |
| `ADAS` | `ADAS` | Keep split | arbitration helper 흡수 완료 |
| `V2X` | `V2X` | Keep split | emergency tx/rx wrapper 흡수 완료 |

Wrapper 제거 상태(활성 트리 제외):
- `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR`, `AMBIENT_CTRL`
- `INFOTAINMENT_GW`, `NAV_CTX_MGR`, `CLU_BASE_CTRL`
- `EMS_POLICE_TX`, `EMS_AMB_TX`, `WARN_ARB_MGR`

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
| 3.4 | 2026-03-09 | 국내 OEM 약어형 canonical 고정 정책 추가(`SGW/_4WD/DATC/AHLS/EDR`) 및 표면명 기준을 `EMS/TCU/ESC/MDPS/CLU`로 정렬. legacy 풀네임은 alias로 한정. |
| 3.3 | 2026-03-09 | `56521c2` 기준 OEM visible bank(`13 deep + 2 validation + 87 placeholder = 100`) 운영 정책 추가. Placeholder를 표면폭 전용 계층으로 고정하고 승격 규칙을 명시. |
| 3.2 | 2026-03-09 | `6cbb647` 기준 Non-VAL 활성 ECU 매트릭스(명칭/Owner/도메인/역할)로 정리. Wrapper 흡수 결과와 ETH 내부 seam 운영 원칙 반영. |
| 3.1 | 2026-03-09 | OEM 확장 반영: `Primary-56 + Validation` 표면 ECU 명명표와 `Runtime-26` 매핑을 SoT 기준으로 재작성. |
| 3.0 | 2026-03-09 | architecture reset baseline으로 전면 재작성. `surface ECU / runtime module / validation harness` 3층 구조 확정. |
| 2.9 | 2026-03-08 | Architecture reset 승인 반영: status를 draft 전환, logical ECU surface / implementation module / validation harness 분리 원칙 추가. |
