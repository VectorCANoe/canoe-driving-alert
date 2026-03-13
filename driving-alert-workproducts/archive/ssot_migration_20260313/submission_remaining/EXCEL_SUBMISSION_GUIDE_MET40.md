# 중간 제출용 엑셀 구성 가이드 (MET40 반영)

기준:
- 회의록 `docs/meeting-notes/MET_40_2026.03.03.txt`
- 현재 문서 SoT `01/03/0301/0302/0303/0304/04/05/06/07`
- 제출 편집본 고정 경로 `tmp/submission/final-docs`

적용 목적:
- `00~07` 원문을 그대로 제출하지 않고, 중간 제출용 엑셀 포맷으로 재구성한다.
- 비교 가능한 탭 구조를 유지하면서 팀 산출물의 완성도/추적성을 명확히 보여준다.

---

## 1) 제출 패키지 (중간)

필수:
1. PPT (발표용)
2. 엑셀 (비교 평가용 통합 시트)
3. DBC (도메인 분리 제출본)

참고:
- `tmp/*` 운영 메모/내부 리포트는 제출본 본문이 아니라 내부 관리 자료다.

---

## 2) 엑셀 시트 권장 구조

샘플 구조를 유지하되 내용은 프로젝트 기준으로 교체:
1. `일정표` (첫 탭: 프로젝트 개요 + 일정 + 현재 진행률)
2. `00_MASTER_Project_Framework`
3. `00_MASTER_Governance_Summary`
4. `01_Requirements`
5. `02_Concept_design`
6. `03_Function definition`
7. `0301_SysFuncAnalysis`
8. `0302_NWflowDef`
9. `0303_Communication Specification`
10. `0304_System Variables`
11. `04_System implementation`
12. `05_Unit Test`
13. `06_Integration Test`
14. `07_System Test`
15. `messages` (선택: DBC 요약표)

---

## 3) 시트별 입력 원칙

### 3.1 일정표 (첫 탭, 필수)
- 프로젝트 개요(문제/목표/범위 In/Out) 1페이지 요약
- 현재 상태: 완료/진행/대기
- 멘토 피드백 반영 항목 체크

### 3.2 01_Requirements
- 고객 요구(What)만 유지
- 검증/인수 성격 항목은 Part 6로 분리된 상태 유지
- Legacy 매핑 항목은 삭제하지 말고 매핑 근거만 명시

### 3.3 03~0304
- `Req -> Func -> Flow -> Comm -> Var` 체인 일치 필수
- ECU 명칭은 Canonical만 사용 (`00e` 기준)
- ID 정책은 `00f`와 충돌 없이 유지 (Pre-Activation ETH 논리 ID 포함)

### 3.4 04
- 구현 경로/모듈 책임/추적 링크 중심
- RTE 규칙은 `00g`를 참조 기준으로 명시

### 3.5 05/06/07
- 현재 실측 전이면 `Planned/Ready` 유지
- `Pass` 확정은 실측 로그/캡처 확보 후에만 기입
- Pre-Activation(`Req_130~155`)은 상태를 명확히 표기

---

## 4) 00 계열 문서 반영 방식 (현재 제출 구조)

원칙:
- 현재 제출본은 `final-docs`에 필요한 00 계열 문서를 직접 포함한다.
- 이전 통합본과 구조 잠금 문서는 `mid-docs`에 보관한다.

제출 본편(현재):
1. `00d_HARA_Worksheet.md`
2. `00e_ECU_Naming_Standard.md`
3. `00f_CAN_ID_Allocation_Standard.md`

보관본/참고:
- `tmp/submission/mid-docs/00_MASTER_Project_Framework.md`
- `tmp/submission/mid-docs/00_MASTER_Governance_Summary.md`
- `tmp/submission/mid-docs/governance/*`

제외:
- `00a_Audit_Readiness_Checklist.md` (내부 운영)
- `00e_ID_Naming_and_CAN_ID_Standard.md` (인덱스 성격)

---

## 5) DBC 제출 정리 원칙

- 도메인 분리 제출 유지 (`canoe/databases/*.dbc`)
- `test_can`은 별도 도메인처럼 보이지 않게 설명문으로 처리
- Ethernet은 DBC 직접 적용 대상이 아님:
  - 통신 계약/매트릭스는 `10_ETHERNET_BACKBONE_INTERFACE_SPEC.md` 기준

---

## 6) 제출 전 최종 체크리스트

1. 첫 탭 프로젝트 개요 존재
2. 탭 구조가 샘플 대비 비교 가능
3. 01~07 체인에서 Req/Func/Flow/Comm/Var 누락 없음
4. Canonical ECU naming 위반 없음
5. CAN ID 정책 문구와 통신표 충돌 없음
6. 05/06/07의 실측 여부 표기 일관성(`Planned/Ready` vs `Pass`)
7. DBC 제출 폴더 구성 및 설명 문구 완료

---

## 7) 현재 프로젝트 권장 제출 상태 문구 (복붙용)

- 본 제출본은 `PPT + 엑셀 + 도메인 분리 DBC` 기준으로 구성하였다.
- 엑셀은 비교 평가 목적에 맞춰 샘플 탭 구조를 유지하고, 내용은 프로젝트 SoT(01~07) 기준으로 재구성하였다.
- `Req_130~Req_155`는 Pre-Activation 범위로 관리하며, 실측 증빙 반영 전까지 테스트 상태는 `Planned/Ready`로 유지한다.
- Ethernet 통신은 DBC 직접 적용이 아닌 계약/매트릭스 기준으로 관리한다.

---

## 8) 제출 편집본 운영 규칙 (고정)

1. 편집은 `tmp/submission/final-docs`에서만 수행한다.
2. 엑셀 변환 입력 경로도 `final-docs`를 기준으로 사용한다.
