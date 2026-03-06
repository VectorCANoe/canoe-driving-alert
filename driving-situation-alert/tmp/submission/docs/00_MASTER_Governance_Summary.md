# 00 마스터 거버넌스 요약 (제출본)

**Document ID**: PROJ-00-MASTER-GOV  
**Version**: 1.1  
**Date**: 2026-03-07  
**Status**: Draft (Submission)  

---

> 제출용 축소본: `00c/00d/00e/00f/00g` 정책 SoT를 중간 제출 관점에서 통합한 문서입니다.

## 작성 원칙

- 본 문서는 정책/거버넌스 규칙을 “심사 가능 수준”으로 통합 요약한다.
- 각 정책의 상세 절차/전수 표는 원문 SoT에서 관리한다.
- 01~07 체인에서 직접 참조하는 고정 규칙만 유지한다.

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

## 3) HARA 요약 (00d 요약)

| HARA ID | 관련 요구 | 핵심 위험 이벤트 | ASIL Candidate (Locked) | 안전목표 |
|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연 | B | 과속 경고 150ms 내 반영 |
| HC-02 | Req_011~012 | 고속 무조향 의심 경고 미발생/해제 실패 | C | 발생/해제 150ms 내 반영 |
| HC-03 | Req_022, Req_027~031 | 중재 규칙 오류로 긴급경고 오선택 | C | Emergency>Zone 등 결정론 보장 |
| HC-04 | Req_024, Req_033~034 | 타임아웃/복귀 불안정으로 운전자 혼란 | B | 1000ms timeout + 150ms 복귀 |
| HC-05 | Req_110~111, Req_124 | 도메인 경계/전달 오류로 체인 단절 | C | 경계 유지 + fail-safe 150ms 전환 |

- Safety Goal과 VC/UT/IT/ST 연결은 원문 00d 및 05~07에서 전수 관리한다.

## 4) ECU 명명 거버넌스 (00e 요약)

### 고정 규칙

- 형식: `UPPER_SNAKE_CASE`, `<DOMAIN_OR_FUNC>_<ROLE>`
- 역할 접미사: `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`, `_DEV`
- Validation 노드: `VAL_*` 접두

### 금지 규칙

- `CONTROL/CTRL` 혼용 금지
- Legacy/풀네임 노드의 Active 체인 신규 도입 금지
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

## 7) 체인 운영 고정 규칙

- 고정 체인: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- 제출본은 대표 매핑 중심, 전수 매핑은 원문 SoT 유지
- `Legacy`/`Pre-Activation` 상태 표기는 원문과 동일하게 유지

## 8) 제출 시 사용 방식

- 00 정책 문서는 본 문서 1개로 통합 제출한다.
- 평가자가 상세 근거 요청 시 `00c/00d/00e/00f/00g` 축소 원문을 부록으로 추가 제출한다.

---
