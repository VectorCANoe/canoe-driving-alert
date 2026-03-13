# M40 Evidence Index

## 1) Network Diagram Evidence (M40-05)

- Concept doc: `driving-alert-workproducts/02_Concept_design.md`
- Current diagram: `driving-alert-workproducts/ops/assets/current/02_networkflow.png`
- Source diagram: `driving-alert-workproducts/ops/assets/source/02_Make_Diagrams.drawio`
- 판정 기준: Ethernet 버스형 표현 제거, 스타형 연결 유지

## 2) Panel Priority Evidence (M40-06)

- Rule doc: `driving-alert-workproducts/04_SW_Implementation.md`
- ST execution rule: `driving-alert-workproducts/07_System_Test.md`
- Priority order lock:
  - `차량 화면` -> `제어 패널` -> `상태 모니터`
- ST evidence path rule:
  - `canoe/logging/evidence/ST/`

## 3) Mid-Report Package Lock (M40-01, M40-15)

- Package lock doc: `driving-alert-workproducts/ops/handoff/TMP_MID_AUDIT_MAIN.md`
- Lock anchor: `main@8eb020e`
- Excel gate: first-sheet project overview + comparable tab/column format PASS

## 4) Pre-Activation Evidence Closure Status (M40-18)

- Target range: `Req_130~Req_155`
- Document readiness:
  - `04/05/06/07` 추적 체인 및 테스트 항목 정의 완료
  - 상태값은 Pre-Activation(`Planned`) 기준으로 유지
- Runtime evidence readiness:
  - `canoe/logging/evidence/UT/`, `IT/`, `ST/` 폴더 구조만 생성됨(`.gitkeep`)
  - 실측 로그/캡처 파일 반영 후 `Pass/Fail`, 담당자, 일자 기입으로 폐쇄
