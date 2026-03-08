# 00 마스터 거버넌스 요약

**Document ID**: PROJ-00-MASTER-GOV  
**Version**: 1.1  
**Date**: 2026-03-07  
**Status**: Draft (Submission)  

## 작성 원칙

- 외부 심사자가 문서 관리 체계와 안전 관점을 빠르게 이해할 수 있도록 구성한다.
- 상세 운영 절차보다 심사에 필요한 핵심 정책과 판단 근거를 우선 제시한다.
- 문서 간 역할 구분과 변경 통제 규칙을 명확하게 유지한다.

---

## 1) 적용 수준 선언 (00c 요약)

- 본 프로젝트는 학습/시연 목적의 CANoe SIL 프로젝트이며 인증 주장 문서가 아니다.
- 다만 ISO 26262 / ASPICE 관점의 실무형 문서 구조와 추적성 운영 규칙을 적용한다.
- 목적은 인증 취득이 아니라, 감사 대응 가능한 근거 구조 확보다.

## 2) 요구 분류/안전 프로파일 (00c 요약)

| 구분 | 적용 정책 |
|---|---|
| Req Type | Functional / Non-Functional / Interface / Verification-Acceptance / Verification-Harness 분리 |
| Safety Class | QM, Provisional-QM, ASIL Candidate를 요구군별로 분류 |
| Harness 분리 | SIL 자극/렌더/진단 보조 항목은 제품 기능 요구와 분리 관리 |
| 추적성 | 분류 결과는 01~07 문서 체인과 연결 유지 |

## 3) HARA/안전등급 요약 (00d + 00c 요약)

### 3.1 ASIL Candidate 항목 (HARA 핵심 이벤트)

| HARA ID | 관련 요구 | 핵심 위험 이벤트 | ASIL/QM 단계 | 안전목표 |
|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연 | B | 과속 경고 150ms 내 반영 |
| HC-02 | Req_011~012 | 고속 무조향 의심 경고 미발생/해제 실패 | C | 발생/해제 150ms 내 반영 |
| HC-03 | Req_022, Req_027~031 | 중재 규칙 오류로 긴급경고 오선택 | C | Emergency>Zone 등 결정론 보장 |
| HC-04 | Req_024, Req_033~034 | 타임아웃/복귀 불안정으로 운전자 혼란 | B | 1000ms timeout + 150ms 복귀 |
| HC-05 | Req_110~111, Req_124 | 도메인 경계/전달 오류로 체인 단절 | C | 경계 유지 + fail-safe 150ms 전환 |

### 3.2 QM 항목 (기능/운영 요구군)

| Req 범위 | 안전등급 | 해석 |
|---|---|---|
| Req_001~009, Req_013~021, Req_026, Req_035~043 | QM (Locked) | 기능/표시/인수 조건 중심 요구군 |
| Req_101~109, Req_112~119, Req_120~123 | QM (Locked) | 기본 차량 상태/표시/편의/연동 요구군 |
| Validation Harness Vars (N/A) | QM | SIL 검증 보조 항목(제품 기능 요구와 분리) |

- Safety Goal, S/E/C 산정과 시험 연계 근거는 거버넌스 부록 문서에서 상세 확인한다.

## 4) ECU 명명 거버넌스 (00e 요약)

### 고정 규칙

- 형식: `UPPER_SNAKE_CASE`, `<DOMAIN_OR_FUNC>_<ROLE>`
- 역할 접미사: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`, `_DEV`
- Validation 노드: `VAL_*` 접두

### 금지 규칙

- `CONTROL/CTRL` 혼용 금지
- 비권장 과거 명칭의 신규 도입 금지
- `AMB`는 `Ambient` 의미 축약으로 사용 금지 (`AMBIENT` 풀토큰 강제)

### Canonical 기준

- 핵심 노드군: `ADAS_WARN_CTRL`, `NAV_CTX_MGR`, `WARN_ARB_MGR`, `EMS_ALERT`
- 검증 노드군: `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`
- 경계 노드군: `CHS_GW`, `INFOTAINMENT_GW`, `BODY_GW`, `IVI_GW`, `ETH_SW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR`

## 5) CAN ID 거버넌스 (00f 요약)

### 핵심 원칙

- 도메인 분리 구조와 3/3/5 ID 인코딩을 병행한다.
- DBC 도메인 분할은 유지하고, CAN 11-bit `BO_ ID`만 정책 기준으로 관리한다.

### 3/3/5 정책

- Tier `[10:8]`: 우선순위/성격(High/Medium/Low/Reserved)
- Group `[7:5]`: 기능 군집(GW, Driver loop, Dynamics, Body, IVI, Validation, Emergency, Reserve)
- Index `[4:0]`: 그룹 내 슬롯(중복 금지)

### 예외

- Tier 0 신규 할당 금지
- 전환 전 저대역 ID는 Old baseline으로만 인정
- Ethernet 논리 ID(`0xE1xx/0xE2xx`)는 CAN 11-bit 3/3/5 대상 제외

## 6) RTE 명명 거버넌스 (00g 요약)

- 3계층 이름체계 유지: `Canonical -> AUTOSAR shortName -> RTE Generated`
- RTE 생성명은 AUTOSAR CP SWC Modeling Guide(SWS_Rte_1153, SWS_Rte_3837) 기준 적용
- shortName 길이/가독성 제한을 적용해 코드 생성명 폭주를 방지
- Canonical에서 shortName 변환 시 의미 토큰 유지(임의 축약 금지)

## 7) 체인 운영 규칙

- 고정 체인: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- 문서 간 식별자(Req/Func/Flow/Comm/Var)는 일관된 참조 규칙으로 유지
- 상태 표기는 `Active`, `Implemented`, `Planned` 기준으로 통일

## 8) 제출 시 사용 방식

- 00 정책 문서는 본 문서 1개로 통합 제출한다.
- 평가자가 상세 근거 요청 시 `00c/00d/00e/00f/00g` 부록 문서를 추가 제출한다.

---
