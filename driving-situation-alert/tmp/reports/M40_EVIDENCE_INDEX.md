# M40 Evidence Index

## 1) Network Diagram Evidence (M40-05)

- Concept doc: `driving-situation-alert/02_Concept_design.md`
- Current diagram: `driving-situation-alert/tmp/assets/current/02_networkflow.png`
- Source diagram: `driving-situation-alert/tmp/assets/source/02_Make_Diagrams.drawio`
- 판정 기준: Ethernet 버스형 표현 제거, 스타형 연결 유지

## 2) Panel Priority Evidence (M40-06)

- Rule doc: `driving-situation-alert/04_SW_Implementation.md`
- ST execution rule: `driving-situation-alert/07_System_Test.md`
- Priority order lock:
  - `차량 화면` -> `제어 패널` -> `상태 모니터`
- ST evidence path rule:
  - `canoe/logging/evidence/ST/`

## 3) Mid-Report Package Lock (M40-01, M40-15)

- Package lock doc: `driving-situation-alert/TMP_MID_AUDIT_MAIN.md`
- Lock anchor: `main@3ef849a`
- Excel gate: first-sheet project overview + comparable tab/column format PASS
