# 요구사항 분류 및 안전 프로파일 (Requirement Classification and Safety Profile)

**Document ID**: PROJ-00C-RCSP  
**ISO 26262 Reference**: Part 3 (Concept), Part 4 (Product Development at System Level)  
**ASPICE Reference**: SYS.2, SYS.3, SWE.1, SWE.2  
**Version**: 1.0  
**Date**: 2026-03-02  
**Status**: Draft  
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 목적
- 요구사항을 `요구 유형(Req Type)`과 `안전등급(Safety Class)`으로 일관되게 관리한다.
- `Req -> VC -> UT/IT/ST` 추적 과정에서 안전/검증 성격 혼선을 방지한다.
- ISO 26262(안전 근거)와 ASPICE(요구-설계-검증 체인) 운영 기준을 문서로 고정한다.

## 2. 분류 체계 정의

| 항목 | 값 | 설명 |
|---|---|---|
| Req Type | Functional | 사용자/시스템 기능 요구 |
| Req Type | Non-Functional | 성능/품질/제약 요구(지연, 주기, 안정성 등) |
| Req Type | Interface | 신호/메시지/도메인 경계/연계 규칙 요구 |
| Req Type | Verification-Acceptance | 검증 수행성/인수 조건 요구 |
| Safety Class | QM | HARA 결과 ASIL 대상이 아닌 품질관리 항목 |
| Safety Class | ASIL-A/B/C/D | HARA로 위해도 분석 후 확정되는 안전등급 |
| Safety Class | Provisional-QM | HARA 완료 전 임시 분류 |
| HARA Status | Not Started / In Progress / Completed | HARA 수행 상태 |

## 3. 운영 원칙 (ISO 26262 / ASPICE)

| 원칙 ID | 원칙 | 적용 문서 |
|---|---|---|
| RCP-01 | QM/ASIL 확정은 HARA 근거가 있어야 한다. HARA 전에는 `Provisional`만 사용한다. | 00c, 01 |
| RCP-02 | 01은 What, 03+는 How, 05~07은 Verification 역할을 분리한다. | 01, 03~07 |
| RCP-03 | 모든 활성 Req는 최소 1개 VC와 연결되어야 한다. | 01, 05~07 |
| RCP-04 | 검증/인수 조건(Req_041~043)은 제품 기능 요구와 분리해 관리한다. | 01, 00b |
| RCP-05 | 추적 체인은 `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`를 유지한다. | 01~07 |

## 4. Req 그룹별 분류/안전 프로파일

| Req 범위 | 내용 요약 | Req Type | Safety Class | HARA Status | 근거 문서 |
|---|---|---|---|---|---|
| Req_001~Req_006 | 경고 활성/해제/반복 억제 공통 로직 | Functional + Non-Functional | Provisional-QM | Not Started | 01, 03, 05 |
| Req_007~Req_016 | 구간 인식/전환/복귀 | Functional | Provisional-QM | Not Started | 01, 03, 07 |
| Req_017~Req_026 | 긴급차량 경고/종료/중복 억제 | Functional + Interface | Provisional-QM | Not Started | 01, 0302, 0303 |
| Req_027~Req_034 | 우선순위/충돌 중재/전환 안정화 | Functional + Non-Functional | Provisional-QM | Not Started | 01, 03, 0301 |
| Req_035~Req_040 | 표시 정책(색상/패턴/문구) | Functional | Provisional-QM | Not Started | 01, 03, 07 |
| Req_041~Req_043 | SIL/CAN+ETH 검증 수행성 및 판정 기록 | Verification-Acceptance | QM | N/A (검증 조건) | 01, 05, 06, 07 |
| Req_101~Req_112 | 차량 기본 기능(시동/기어/입력/표시/도메인 경계) | Functional + Interface | Provisional-QM | In Progress | 01, 03, 0302 |
| Req_113~Req_119 | HVAC/Seat/Mirror/Door/Wiper/Security/Audio 상태 반영 | Functional + Interface | Provisional-QM | In Progress | 01, 03, 0303, 0304 |

## 5. HARA 후보 우선 목록 (초안)

| 후보 ID | 대상 Req | 위험 시나리오(요약) | 권장 조치 |
|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 미표시로 경고 타이밍 상실 | HARA 우선 분석 후보 등록 |
| HC-02 | Req_011, Req_012 | 무조향 경고 오동작/미동작 | HARA 우선 분석 후보 등록 |
| HC-03 | Req_022, Req_028~Req_031 | 중재 우선순위 오류로 잘못된 경고 출력 | HARA 우선 분석 후보 등록 |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃/복귀/전환 오류로 운전자 혼란 유발 | HARA 우선 분석 후보 등록 |
| HC-05 | Req_101~Req_105 | 기본 주행입력 반영 오류 | HARA 후보 등록 및 영향도 검토 |
| HC-06 | Req_110, Req_111 | 도메인 경계/라우팅 오류로 메시지 전달 실패 | HARA 후보 등록 및 경계조건 검토 |

## 6. 문서 반영 규칙

| 문서 | 반영 내용 |
|---|---|
| 01 | Req 본문 + VC(검증 기준) + Req Type/Safety Class는 00c 참조 |
| 03/0301 | 기능/노드 분해 시 Req Type이 Verification-Acceptance인 항목은 Validation Harness로 한정 |
| 0302/0303/0304 | Interface 요구(Flow/Comm/Var)와 기능 요구 연결 근거 유지 |
| 05/06/07 | VC 기반 검증 증적과 Req Type별 검증 레벨(UT/IT/ST) 일치 유지 |

## 7. 후속 작업

| 작업 | 산출물 | 상태 |
|---|---|---|
| HARA 상세 수행 | `00d_HARA_Worksheet.md` (신규 예정) | Planned |
| Safety Class 확정(QM/ASIL) | 01/00c 동기화 업데이트 | Planned |
| 05/06/07 미커버 Req 보강 | 테스트 상세표 업데이트 | Planned |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-03-02 | 신규 작성: Req Type/Safety Class/HARA Status 운영 기준 및 Req 그룹별 안전 프로파일 초안 정의. |
