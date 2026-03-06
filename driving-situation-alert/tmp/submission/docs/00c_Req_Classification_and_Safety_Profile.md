# 요구사항 분류 및 안전 프로파일 운영 기준 (Requirement Classification and Safety Profile)

**Document ID**: PROJ-00C-RCSP  
**ISO 26262 Reference**: Part 3 (Concept), Part 4 (System), Part 8 (Supporting Process)  
**ASPICE Reference**: SYS.2, SYS.3, SWE.3, SUP.1, SUP.10  
**Version**: 1.6  
**Date**: 2026-03-04  
**Status**: Draft (Internal Baseline Locked)  
**Project Title**: 주행 상황 실시간 경고 시스템  
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

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
| Req Type | Verification-Harness | SIL 검증 편의를 위한 자극/렌더/진단 보조 항목(제품 기능 요구와 분리) | `project.sysvars`의 `Test/*`, `UiRender/*`, `V2X/policeDispatch` |
| Safety Class | QM | 위해도 분석상 안전 무결성 등급이 필요하지 않은 항목 | 일부 표시 품질/운영 요구 |
| Safety Class | Provisional-QM | HARA 완료 전 임시 분류 | 현재 기본 운영값 |
| Safety Class | ASIL-A/B/C/D | HARA(S/E/C)로 확정된 안전 무결성 등급 | HARA 완료 후 확정 |
| HARA Status | Not Started / In Progress / Completed | HARA 진행 상태 | 현재 Completed (Internal Baseline) |

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

