# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 3.5  
**Date**: 2026-03-06  
**Status**: Draft (Policy SoT)  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

## 1. 목적

- CAN ID 정책을 `3/3/5` 인코딩으로 통일한다.
- 도메인 분리 DBC 구조를 유지한 상태에서 ID 거버넌스를 고도화한다.
- 문서/DBC/CAPL/테스트의 추적 체인을 단일 규칙으로 동기화한다.

---

## 2. 핵심 원칙 (고정)

- 본 프로젝트는 `도메인 분리 구조`와 `3/3/5 ID 인코딩`을 **병행**한다.
- 정의:
  - 도메인 분리 = 네트워크/소유 경계(어느 DBC가 어떤 메시지를 소유하는가)
  - 3/3/5 = 11-bit CAN ID 번호체계(어떤 비트 의미로 ID를 배정하는가)
- 즉, 도메인 DBC 파일 분할은 유지하고, `BO_ ID`만 3/3/5 정책으로 재배정한다.

---

## 3. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | ISO 11898 series, ISO 15765-2(ISO-TP), SAE J1939-21, AUTOSAR CP(COM/CanIf/CanTp/PduR) | arbitration/ID 해석/전송계층 정합 |
| 공개 구현 | Linux kernel CAN/ISO-TP/J1939 docs | 구현/검증 관점 참고 |
| 내부 SoT | `canoe/databases/*.dbc` | 최종 실행 ID 기준 |
| 내부 문서 | `0302`, `0303`, `0304`, `04` | Flow/Comm/Var/구현 연동 |
| 명명 표준 | `00e_ECU_Naming_Standard.md` | ECU Canonical 고정 |
| 레퍼런스 카탈로그 | `reference/catalogs/ID_REFERENCE_CATALOG.md` | 출처/근거 관리 |

---

## 4. 레이어드 운영 모델

### 4.1 Layer-A: 도메인 분리(Architecture)

- 활성 DBC 집합:
  - `chassis_can.dbc`
  - `body_can.dbc`
  - `infotainment_can.dbc`
  - `powertrain_can.dbc`
  - `adas_can.dbc`
  - `eth_backbone_can_stub.dbc`
- 정책:
  - 메시지 owner는 도메인 DBC 기준으로 유지한다.
  - 3/3/5 전환은 owner/도메인 파일 구조를 변경하는 작업이 아니다.

### 4.2 Layer-B: ID 인코딩(Governance)

- CAN 11-bit ID 비트 분해:
  - `[10:8]` = Tier (3bit)
  - `[7:5]` = Group (3bit)
  - `[4:0]` = Index (5bit)
- 계산식:
  - `ID = (Tier << 8) | (Group << 5) | Index`
- 용량:
  - Tier당 256개
  - Group당 32개 슬롯

### 4.3 Assignment Decision Priority (Normative)

- ID 배정 의사결정은 아래 우선순위를 따른다.
  - 1) Owner/도메인 경계
  - 2) 안전/검증 경로(Fail-safe/Validation 영향)
  - 3) Tier/Group/Index 인코딩 규칙
- 주의: `Group`은 단독 최상위 기준이 아니며, 1)과 2)를 만족한 뒤 적용되는 분류/정렬 축이다.

### 4.4 Arbitration Scope and Constraints (Normative)

- 본 표준은 버스 레벨 중재와 애플리케이션 레벨 중재를 분리하여 정의한다.
- 버스 중재 범위(CAN 컨트롤러/프로토콜 레벨):
  - 중재 우선순위는 CAN Identifier 값으로만 결정되어야 한다(SHALL).
  - Payload 신호/비트필드는 버스 중재 순서에 영향을 주어서는 안 된다(SHALL NOT).
  - 본 프로젝트에서 ID 배정 이후의 버스 우선순위 해석은 `Tier -> Group -> Index` 순서를 따른다.
- 애플리케이션 중재 범위(소프트웨어 로직 레벨):
  - 경고/감속보조/Fail-safe 판단은 payload 신호, 타이머, 상태 로직으로 결정되어야 한다(SHALL).
  - 애플리케이션 중재는 기능 상태/출력을 변경할 수 있으나(MAY), 버스 레벨 중재 순서를 재정의해서는 안 된다(SHALL NOT).
- 설계 일관성 규칙:
  - 안전 핵심 경로는 애플리케이션 긴급도와 버스 우선순위 배정을 동시에 만족해야 한다(SHALL).
  - 긴급 기능이 요구 수준보다 낮은 버스 우선순위로 배정된 경우, Annex A와 게이트 심사(G1~G4)를 통해 ID 매핑을 수정해야 한다(SHALL).

### 4.5 긴급 우선 요구 해석 규칙 (Normative)

- `Req_022/Req_028/Req_029/Req_030/Req_031`의 기본 판정 축은 애플리케이션 중재 규칙이다.
- 위 요구의 기본 적합성은 `WARN_ARB_MGR` 선택 로직(Emergency > Zone, Ambulance > Police, ETA, SourceID)으로 검증한다.
- 버스 우선순위 상향(더 낮은 CAN ID 강제)은 별도 요구/게이트 근거가 있을 때만 적용한다.

---

## 5. 3/3/5 사전

### 5.1 Tier 사전 (`[10:8]`)

| Tier | ID 대역 | 의미 | 우선순위 |
|---|---|---|---|
| 1 | `0x100~0x1FF` | 실시간 제어/핵심 상태 루프 | High |
| 2 | `0x200~0x2FF` | 출력/표시/Body/Validation 결과 | Medium |
| 3 | `0x300~0x3FF` | 파워트레인 확장/V2 Stub/진단 확장 | Low |
| 0,4~7 | 예약 | 미래 확장 | Reserved |

### 5.2 Group 사전 (`[7:5]`)

| Group | 의미 | 대표 ECU/기능 |
|---|---|---|
| 0 | Gateway/Boundary/Manager | `CHS_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` |
| 1 | Driver command + baseline state loop | `ACCEL_CTRL`, `BRK_CTRL`, `STEER_CTRL`, `ENG_CTRL`, `TCM`의 입력/요청/상태 핵심 프레임 |
| 2 | Chassis dynamics + actuator feedback | EPS/ABS/ESC/TCS/휠속/요레이트/조향각 등 동역학/제어반환 프레임 |
| 3 | Body comfort/control | `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` |
| 4 | IVI/Cluster/HMI context | `NAV_CTX_MGR`, `CLU_HMI_CTRL`, `CLU_BASE_CTRL` |
| 5 | Validation harness/result | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` |
| 6 | Emergency/V2 assist | `EMS_*`, `WARN_ARB_MGR` |
| 7 | Diag/Reserve | 진단/예약 |

- 해석 규칙: 메시지 이름에 `Diag`가 포함되어도 Group 7 강제 배정 사유가 되지 않는다.
- Group 결정은 `Owner/도메인 경계 -> 안전/검증 경로 -> Group 사전` 순서로 수행한다.

### 5.3 Index 사전 (`[4:0]`)

- 범위: `0~31`
- 규칙:
  - 동일 Tier/Group 내 Index 중복 금지
  - `31`은 기본 예약(예외는 변경승인 필요)

### 5.4 예외 규칙 (Legacy Stub/Transition)

- Tier `0`은 신규 할당 금지다.
- 전환 전 베이스라인의 저대역 ID(`0x064` 포함)는 `Old ID`로만 인정하며 Cutover 대상에 포함한다.
- 전환 완료 후 `0x000~0x0FF` 활성 운영 ID는 0건이어야 한다.
- 논리 Ethernet ID(`0xE1xx/0xE2xx`)는 CAN 11-bit 3/3/5 대상이 아니다.
- `E213~E216`(`Comm_130~Comm_133`)은 Pre-Activation Ethernet 논리 ID이며, `ETH_INTERFACE_CONTRACT.md v1.2` 반영 전에는 활성 계약으로 취급하지 않는다.

---

## 6. SoT 및 우선순위 (Phase 고정)

- P0 설계/합의 단계:
  1. `00f` Annex A 매핑표
  2. `00f` Tier/Group 규칙
  3. `0303` 현행 스펙
- P1 구현/검증 단계(Cutover 후보 브랜치):
  1. Branch 내 `canoe/databases/*.dbc`
  2. Branch 내 `0302/0303/0304/04/05/06/07`
  3. `00f` Annex A
- P2 Cutover 완료 후(main):
  1. `canoe/databases/*.dbc`
  2. `00f`
  3. `0303`

---

## 7. 현행 베이스라인 (전환 전 스냅샷)

- 현행 구조: 도메인 블록 대역형
- 메시지 수: `98`
- ID 범위(신규 3/3/5 배치 결과): `0x100 ~ 0x2AA`
- Old baseline 참고 범위(전환 전): `0x064 ~ 0x315`
- 중복: `0건`
- 대표 블록:
  - `0x100~0x2A6` Chassis
  - `0x260~0x277` Body
  - `0x280~0x2A7` Infotainment
  - `0x109~0x2AA` Powertrain
  - `0x111~0x1C4` ADAS + ETH Stub

---

## 8. 실행 거버넌스 분리 원칙

- 본 문서는 ID 정책(원칙/분류/우선순위/용어)의 SoT다.
- 실행 항목(Cutover/Rollback/승인 게이트/수용 기준/제출물)은 변경지시서 SoT를 따른다:
  - `driving-situation-alert/tmp/change-orders/DEV_CHANGE_ORDER_CAN_ID_335_FULL_RENUMBERING_2026-03-05.md`
- 정책 변경 없이 실행 절차만 조정하는 경우, 변경지시서만 개정한다.
- 정책 자체(Tier/Group/Index, 중재 경계, SoT 우선순위)를 변경하는 경우에만 00f를 개정한다.

---

## 9. Annex A (98개 전수 매핑)

- 파일: `driving-situation-alert/tmp/ID_335_AnnexA_Mapping_98_Template.csv`
- 목적: `Old ID -> New ID` 전수 매핑의 단일 근거 파일
- 운영 원칙: 실제 할당 상태(`status/approver/approved_date`)는 Annex A CSV를 단일 운영 테이블로 사용한다.
- 필수 컬럼:
  - `new_tier`, `new_group`, `new_index`, `new_id_hex`, `new_id_dec`
  - `flow_ref`, `comm_ref`, `var_ref`, `code_ref`, `test_ref`
  - `status`, `approver`, `approved_date`
- 상태/승인 규칙(G1~G4)은 변경지시서 기준으로 운영한다.

---

## 10. 점검 명령 (권장)

```bash
awk '/^BO_ /{print $2}' canoe/databases/*.dbc | sort -n | uniq -d
```

```bash
rg -n "0x[0-9A-Fa-f]{2,3}" driving-situation-alert/{0302_NWflowDef.md,0303_Communication_Specification.md,0304_System_Variables.md,04_SW_Implementation.md,05_Unit_Test.md,06_Integration_Test.md,07_System_Test.md}
```

---

## 11. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.5 | 2026-03-06 | Ethernet 계약 정합 보강: `E213~E216`(`Comm_130~Comm_133`)을 Pre-Activation 논리 ID로 명시하고 `ETH_INTERFACE_CONTRACT.md v1.2` 반영 전 비활성 규칙을 추가. |
| 3.4 | 2026-03-06 | 감사/운영 해석 보강: 긴급 우선 요구의 기본 판정 축을 기능중재로 명시하고, `Diag` 명칭과 Group 7 강제 배정을 분리하는 규칙을 추가. |
| 3.3 | 2026-03-06 | 정책 문서 슬림화: 실행 절차(Cutover/Rollback/Gate/Acceptance)는 변경지시서 SoT로 이관하고 00f는 정책 원문 중심으로 재구성. |
| 3.2 | 2026-03-05 | 실행력 보강: Annex A(98건 매핑 파일) 연결, Group 경계 명확화, Tier0 예외 규칙, 승인 게이트(G1~G4), Cutover/Rollback 절차를 추가. |
| 3.1 | 2026-03-05 | 정책을 레이어드 모델로 재정의: `도메인 분리 구조 유지 + 3/3/5 인코딩 전면 적용` 병행 방식을 고정. |
| 3.0 | 2026-03-05 | 3/3/5 인코딩 전면 전환 승인본으로 재정의(전면 교체 게이트/검증 기준 추가). |
| 2.0 | 2026-03-05 | SoT 확정본 고정: 11-bit/29-bit 정책·운영 경계·변경 게이트 체계화. |
| 1.2 | 2026-03-05 | ID 레퍼런스 운영 카탈로그 연동 항목 추가. |
| 1.1 | 2026-03-05 | 규격 단위 레퍼런스 구체화 및 베이스라인 점검 결과 추가. |
| 1.0 | 2026-03-05 | 통합 문서에서 CAN ID 배정 표준을 00f로 분리. |
