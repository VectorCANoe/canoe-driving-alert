# 요구사항 분류 및 안전 프로파일 운영 기준 (Requirement Classification and Safety Profile)

**Document ID**: PROJ-00C-RCSP  
**ISO 26262 Reference**: Part 3 (Concept), Part 4 (System), Part 8 (Supporting Process)  
**ASPICE Reference**: SYS.2, SYS.3, SWE.3, SUP.1, SUP.10  
**Version**: 1.5  
**Date**: 2026-03-04  
**Status**: Draft (Internal Baseline Locked)  
**Project Title**: 주행 상황 실시간 경고 시스템  
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 문서 목적
- 본 문서는 01~07 문서 체인에서 요구사항 분류와 안전 프로파일을 일관되게 운영하기 위한 기준이다.
- 감사 시 "왜 이 요구가 필요한가", "어떤 검증으로 닫았는가"를 같은 기준으로 답변할 수 있게 한다.
- `Req -> VC -> Func -> Flow/Comm/Var -> UT/IT/ST` 체인에서 분류 누락과 안전성 근거 누락을 방지한다.

## 2. 적용 수준 선언 (중요)
- 본 프로젝트는 **학습/시연 목적의 CANoe SIL 프로젝트**이며, ISO 26262/ASPICE **인증 주장 문서가 아니다**.
- 다만 문서 구조와 추적성 운영은 ISO 26262/ASPICE 관점의 실무형 규칙을 따른다.
- 따라서 본 문서의 목적은 "인증"이 아니라 "감사 대응 가능한 근거 구조" 확보다.

## 3. 분류 체계 정의

| 항목 | 값 | 정의 | 본 프로젝트 예시 |
|---|---|---|---|
| Req Type | Functional | 사용자/시스템이 수행해야 하는 기능 요구 | Req_010, Req_022, Req_033 |
| Req Type | Non-Functional | 시간/안정성/반복억제/결정론 등 품질 속성 | Req_006, Req_024, Req_032, Req_034 |
| Req Type | Interface | 도메인 경계, 메시지 전달, 상태 반영 인터페이스 요구 | Req_007, Req_110, Req_111, Req_113~119 |
| Req Type | Verification-Acceptance | 고객 요구 검증을 수행/판정/기록하기 위한 인수 조건 | Req_041~043 |
| Req Type | Verification-Harness | SIL 검증 편의를 위한 자극/렌더/진단 보조 항목(제품 기능 요구와 분리) | `project.sysvars`의 `Test/*`, `UiRender/*`, `Driver/gazeActive`, `V2X/policeDispatch` |
| Safety Class | QM | 위해도 분석상 안전 무결성 등급이 필요하지 않은 항목 | 일부 표시 품질/운영 요구 |
| Safety Class | Provisional-QM | HARA 완료 전 임시 분류 | 현재 기본 운영값 |
| Safety Class | ASIL-A/B/C/D | HARA(S/E/C)로 확정된 안전 무결성 등급 | HARA 완료 후 확정 |
| HARA Status | Not Started / In Progress / Completed | HARA 진행 상태 | 현재 Completed (Internal Baseline) |

## 4. 분류 판정 규칙 (실행 규칙)

| 규칙 ID | 판정 질문 | Yes일 때 | No일 때 |
|---|---|---|---|
| CR-01 | 요구가 시스템 동작 결과를 직접 바꾸는가? | Functional 우선 분류 | CR-02로 이동 |
| CR-02 | 요구의 핵심이 시간/안정성/반복억제 기준인가? | Non-Functional 분류 | CR-03으로 이동 |
| CR-03 | 요구의 핵심이 메시지/경계/도메인 전달인가? | Interface 분류 | CR-04로 이동 |
| CR-04 | 요구의 핵심이 검증 수행성/판정/기록인가? | Verification-Acceptance 분류 | CR-05로 이동 |
| CR-05 | 항목이 SIL 전용 자극/렌더/보조 변수인가? | Verification-Harness로 분류하고 제품 Req 체인과 분리 | Review 필요 |

운영 규칙:
- 하나의 Req는 복합 성격을 가질 수 있다. 이 경우 `Primary/Secondary`로 관리한다.
- 01 본문은 고객 관점(What)으로 유지하고, 분류 근거는 본 문서에서 관리한다.
- 분류 근거 없는 Req는 리뷰 게이트에서 Reject한다.
- Verification-Harness 항목은 01의 고객 요구 본문에 직접 추가하지 않고, 04/0304의 구현 보강 섹션에서 관리한다.

## 5. Safety Profile 운영 규칙

| 규칙 ID | 내용 | 게이트 기준 |
|---|---|---|
| SP-01 | 초기 생성 Req는 `Provisional-QM`으로 등록 | 등록 누락 0건 |
| SP-02 | 안전 영향 가능 Req는 HARA 후보로 등록 | 후보 등록 누락 0건 |
| SP-03 | ASIL 확정은 HARA 결과(S/E/C) 근거가 있을 때만 허용 | 근거 없는 ASIL 표기 금지 |
| SP-04 | HARA 후보 Req는 VC에 정량 기준(지연/타임아웃/반복 억제)이 있어야 함 | VC 정량 기준 100% |
| SP-05 | HARA 상태 변경 시 01, 00a, 00c 동시 업데이트 | 문서 불일치 0건 |

### 5.1 HARA 후보군 (현재 프로젝트 기준)

| HARA 후보 ID | 대상 Req | 위험 시나리오(요약) | 현재 분류 | 다음 조치 |
|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연 | ASIL Candidate-B (Locked) | HARA 워크시트 승인 완료(00d) |
| HC-02 | Req_011, Req_012 | 무조향 경고 오동작 또는 해제 실패 | ASIL Candidate-C (Locked) | HARA 워크시트 승인 완료(00d) |
| HC-03 | Req_022, Req_027~031 | 중재 규칙 오류로 잘못된 우선 경고 출력 | ASIL Candidate-C (Locked) | HARA 워크시트 승인 완료(00d) |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃/복귀/전환 불안정으로 운전자 혼란 유발 | ASIL Candidate-B (Locked) | HARA 워크시트 승인 완료(00d) |
| HC-05 | Req_110, Req_111, Req_124 | 도메인 경계/전달 오류로 경고 체인 단절 | ASIL Candidate-C (Locked) | 인터페이스 FMEA + HARA 승인 완료(00d) |

## 6. ASPICE 운영 매핑 (프로세스 근거)

| ASPICE | 핵심 BP | 본 프로젝트 산출물 | 판정 포인트 |
|---|---|---|---|
| SYS.2 | BP1, BP2, BP5, BP6 | `01_Requirements.md`, VC 표 | Req 품질/VC/추적성 |
| SYS.3 | BP1, BP2, BP3, BP4 | `03`, `0301`, `0302`, `0303`, `0304` | 기능 할당/인터페이스 정합 |
| SWE.3 | BP1, BP5 | `04_SW_Implementation.md`(요구-구현 계약) | 상세 설계 계약과 요구 일치 |
| SUP.1 | BP1, BP2 | `00a_Audit_Readiness_Checklist.md` | 이슈/액션 관리 |
| SUP.10 | BP1, BP2 | 00~07 추적성 체인 | 양방향 추적 확인 |

## 7. Req 그룹별 분류/안전 프로파일 (현재 기준)

| Req 범위 | Primary Type | Secondary Type | Safety Class | HARA Status | 근거 문서 |
|---|---|---|---|---|---|
| Req_001~009, Req_013~021, Req_026, Req_035~043 | Functional / Interface / Verification-Acceptance | Non-Functional | QM (Locked) | Completed (Internal) | 01, 03, 05~07 |
| Req_010 | Functional | Non-Functional | ASIL Candidate-B (Locked) | Completed (Internal) | 00d(HC-01), 01, 03, 07 |
| Req_011~012 | Functional | Non-Functional | ASIL Candidate-C (Locked) | Completed (Internal) | 00d(HC-02), 01, 03, 07 |
| Req_022, Req_027~031 | Functional | Non-Functional | ASIL Candidate-C (Locked) | Completed (Internal) | 00d(HC-03), 01, 03, 06, 07 |
| Req_024, Req_033, Req_034 | Non-Functional | Functional | ASIL Candidate-B (Locked) | Completed (Internal) | 00d(HC-04), 01, 03, 06, 07 |
| Req_101~109, Req_112~118, Req_120~123 | Functional / Interface | Non-Functional | QM (Locked) | Completed (Internal) | 01, 03, 0302~0304 |
| Req_110~111, Req_124 | Interface | Functional / Non-Functional | ASIL Candidate-C (Locked) | Completed (Internal) | 00d(HC-05), 01, 03, 0302~0304, 06, 07 |
| Req_119 | Interface | Functional | QM (Locked) | Completed (Internal) | 01, 03, 0303, 0304, 06, 07 |
| N/A (Harness Vars) | Verification-Harness | Interface | QM | N/A | 04, 0304, `canoe/project/sysvars/project.sysvars` |

## 8. 문서 반영 규칙 (01~07)

| 문서 | 필수 반영 항목 | 금지 항목 |
|---|---|---|
| 01 | 고객 관점 What + VC + Req ID | 구현 코드/내부 변수 상세 |
| 03/0301 | Func/노드 책임 + Req 연결 | 제품 요구 재서술만 반복 |
| 0302/0303/0304 | Flow/Comm/Var 계약 + 추적 매핑 | 근거 없는 메시지/변수 추가 |
| 04 | 구현 책임/타이밍/예외 처리 계약 + Verification-Harness 경계 명시 | 디버그 절차 나열 |
| 05/06/07 | VC 기준 테스트/판정/증적 | Req 미연결 테스트 케이스 |

## 9. 감사 게이트 (이 문서 기준)

| 게이트 ID | 점검 항목 | 합격 기준 |
|---|---|---|
| G-01 | Req 분류 누락 | 0건 |
| G-02 | Safety Class 누락 | 0건 |
| G-03 | Safety Class 변경 근거 | HARA 근거 100% 첨부 |
| G-04 | Req-VC-UT/IT/ST 연결 누락 | 0건 |
| G-05 | 01(What)/03+(How) 혼합 | 혼합 위반 0건 |

## 10. 후속 작업

| 작업 | 산출물 | 목표일 |
|---|---|---|
| HARA 상세 시트 작성 | `00d_HARA_Worksheet.md` | 완료(2026-03-04, v1.3) |
| Req별 분류 메타(Primary/Secondary) 잠금 | `01_Requirements.md` 부록 표 | 중간감사 이후 반영 (Planned) |
| Safety Class 확정 반영 | 00a/00b/00c/01 동기화 | 완료(2026-03-04, 내부 Baseline) |
| VC-테스트 증적 100% 연결 | 05/06/07 상단 Pass/Fail 포함 | 2026-03-12 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.5 | 2026-03-04 | Safety Class 내부 Baseline 잠금 반영: Req 그룹을 QM/ASIL Candidate로 확정하고 HARA 상태를 `Completed (Internal)`로 갱신. 활성 범위를 `Req_001~043`, `Req_101~124`로 동기화. |
| 1.4 | 2026-03-02 | 중간감사 운영 반영: 후속 작업 항목 `Req별 분류 메타 잠금` 상태를 `중간감사 이후 반영 (Planned)`으로 명확화. |
| 1.3 | 2026-03-02 | ISO26262/ASPICE 운영 경계 보강: `Verification-Harness` 분류를 추가하고, SIL 전용 변수(`UiRender/*`, `Driver/gazeActive`, `V2X/policeDispatch`)를 제품 Req 체인과 분리 관리하는 규칙(CR-05)을 명시. |
| 1.2 | 2026-03-02 | 00d HARA 워크시트 생성 반영: 후속 작업 상태를 생성 완료로 갱신하고 운영 연계 기준 보강. |
| 1.1 | 2026-03-02 | 프로젝트 실무 운영 기준으로 전면 보강: 적용 수준 선언, 분류 판정 규칙, Safety Profile 게이트, ASPICE 운영 매핑, 감사 게이트, 후속 일정 추가. |
| 1.0 | 2026-03-02 | 신규 작성: Req Type/Safety Class/HARA Status 운영 기준 및 Req 그룹별 안전 프로파일 초안 정의. |
