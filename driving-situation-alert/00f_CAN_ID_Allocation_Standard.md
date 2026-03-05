# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 3.2  
**Date**: 2026-03-05  
**Status**: Draft (Execution Gate Pending)  
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

### 5.3 Index 사전 (`[4:0]`)

- 범위: `0~31`
- 규칙:
  - 동일 Tier/Group 내 Index 중복 금지
  - `31`은 기본 예약(예외는 변경승인 필요)

### 5.4 예외 규칙 (Legacy Stub/Transition)

- Tier `0`은 신규 할당 금지다.
- 전환 전 베이스라인의 저대역 ID(`0x064` 등)는 `Old ID`로만 인정하며 Cutover 대상에 포함한다.
- 전환 완료 후 `0x000~0x0FF` 활성 운영 ID는 0건이어야 한다.
- 논리 Ethernet ID(`0xE1xx/0xE2xx`)는 CAN 11-bit 3/3/5 대상이 아니다.

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
- ID 범위: `0x064 ~ 0x315`
- 중복: `0건`
- 대표 블록:
  - `0x100~0x12F` Chassis
  - `0x210~0x24F` Body
  - `0x220~0x26F` Infotainment
  - `0x300~0x31F` Powertrain+V2
  - `0x330~0x34F` ADAS reserve

---

## 8. 전환 정책 (Full Renumbering)

- 전환 범위:
  - 활성 메시지 `98`개 전량
- 전환 방식:
  - 단일 릴리즈 동시 Cutover
  - dual schema(구 ID+신 ID 병행 운영) 금지
- 유지 사항:
  - 도메인 DBC 분리 구조
  - Ethernet 논리 ID/Stub ID 분리 원칙

### 8.1 Cutover/Rollback 규칙

- Cutover 전 필수:
  - Annex A 매핑표 98건 `Approved`
  - 충돌 검사 0건
  - 핵심 시나리오 회귀 PASS
- Rollback 조건:
  - 충돌 1건 이상
  - Tier 우선순위 역전으로 타이밍 불합격
  - 핵심 시나리오 Fail
- Rollback 방법:
  - Cutover 직전 Git tag로 즉시 복귀
  - DBC/문서/CAPL을 동일 커밋 단위로 원복

### 8.2 승인 게이트 (변경 통제)

| 게이트 | 산출물 | 책임 | 승인 기준 |
|---|---|---|---|
| G1 Mapping Freeze | Annex A 98건 | 문서팀 | Tier/Group/Index 완전 기입, 중복 0건 |
| G2 Implementation Freeze | DBC/CAPL/문서 동기화 PR | 개발팀 | `BO_` 전량 반영, 구 ID 잔존 0건 |
| G3 Cutover Approval | 회귀 리포트 | PM/QA | 기능 동등성/타이밍 합격 |
| G4 Post-Cutover Audit | 최종 증적 패키지 | 문서팀+개발팀 | 추적 체인 단절 0건 |

---

## 9. 필수 작업 패키지

1. `00f` Annex A 및 매핑 파일(`tmp/ID_335_AnnexA_Mapping_98_Template.csv`) 98개 전수 확정  
2. `0302/0303/0304/04/05/06/07` ID 전량 동기화  
3. 활성 DBC 6종 `BO_` ID 전량 재배정  
4. CAPL/panel/sysvar/log raw ID 상수 전수 치환  
5. 회귀검증(충돌/기능/타이밍/중재) 수행

---

## 10. 수용 기준 (Acceptance)

1. 정합성
- ID 중복 0건
- Tier/Group/Index 규칙 위반 0건
- 구 ID 잔존 참조 0건
- Tier 우선순위 역전(중요 제어 프레임이 저우선 Tier에 배치) 0건

2. 기능 동등성
- SIL 시나리오 Pass/Fail 동등
- 경고 중재/해제/타이밍 동등

3. 추적성
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 단절 0건

---

## 11. Annex A (98개 전수 매핑)

- 파일: `driving-situation-alert/tmp/ID_335_AnnexA_Mapping_98_Template.csv`
- 목적: `Old ID -> New ID` 전수 매핑의 단일 근거 파일
- 필수 컬럼:
  - `new_tier`, `new_group`, `new_index`, `new_id_hex`, `new_id_dec`
  - `flow_ref`, `comm_ref`, `var_ref`, `code_ref`, `test_ref`
  - `status`, `approver`, `approved_date`
- 규칙:
  - 구현 착수 전 `status=Approved` 98건 완료
  - Cutover 전 승인자/일자 누락 0건

---

## 12. 점검 명령 (권장)

```bash
awk '/^BO_ /{print $2}' canoe/databases/*.dbc | sort -n | uniq -d
```

```bash
rg -n "0x[0-9A-Fa-f]{2,3}" driving-situation-alert/{0302_NWflowDef.md,0303_Communication_Specification.md,0304_System_Variables.md,04_SW_Implementation.md,05_Unit_Test.md,06_Integration_Test.md,07_System_Test.md}
```

---

## 13. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.2 | 2026-03-05 | 실행력 보강: Annex A(98건 매핑 파일) 연결, Group 경계 명확화, Tier0 예외 규칙, 승인 게이트(G1~G4), Cutover/Rollback 절차를 추가. |
| 3.1 | 2026-03-05 | 정책을 레이어드 모델로 재정의: `도메인 분리 구조 유지 + 3/3/5 인코딩 전면 적용` 병행 방식을 고정. |
| 3.0 | 2026-03-05 | 3/3/5 인코딩 전면 전환 승인본으로 재정의(전면 교체 게이트/검증 기준 추가). |
| 2.0 | 2026-03-05 | SoT 확정본 고정: 11-bit/29-bit 정책·운영 경계·변경 게이트 체계화. |
| 1.2 | 2026-03-05 | ID 레퍼런스 운영 카탈로그 연동 항목 추가. |
| 1.1 | 2026-03-05 | 규격 단위 레퍼런스 구체화 및 베이스라인 점검 결과 추가. |
| 1.0 | 2026-03-05 | 통합 문서에서 CAN ID 배정 표준을 00f로 분리. |
