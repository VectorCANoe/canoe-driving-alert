# Master Test Matrix

**Document ID**: PROJ-00G-MTM
**ISO 26262 Reference**: Part 4 / Part 6 (Verification Planning and Qualification)
**ASPICE Reference**: SYS.4 / SYS.5 / SWE.4 / SWE.5 / SWE.6
**Version**: 0.2
**Date**: 2026-03-15
**Status**: Draft Baseline
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 경고: `canoe/src/capl` 구현이 추가 개발 또는 업데이트되면, 같은 변경 범위의 `Master Test Matrix`, `05/06/07`, oracle/evidence 정의, executable TEST 자산도 동일 기준선으로 즉시 동기화해야 한다. CAPL과 TEST 기준선 불일치는 그대로 추적성 실패로 간주한다.
>
> 참고: 본 문서는 active executable baseline만 유지한다. retired umbrella row 이력은 `driving-alert-workproducts/governance/00g_Master_Test_Matrix_retired.md`에서 별도로 관리한다.

## 1. 목적

본 문서는 현재 프로젝트의 상위 테스트 통제 문서이다.

목적은 다음과 같다.

1. `Req -> UT/IT/ST` 추적성을 하나의 표에서 통제한다.
2. 안전 항목과 일반 기능 항목을 같은 테스트 표면에서 구분한다.
3. native CANoe Test Unit 구현 전에 상위 검증 기준을 먼저 고정한다.

## 2. 컬럼 운영 원칙

1. `Test Level`은 `UT / IT / ST`만 사용한다.
2. `ASIL/QM`는 `Test Level`에 넣지 않고 별도 컬럼으로 관리한다.
3. `Safety Goal`은 HARA 요약본 기준으로 연결한다.
4. HARA 직접 연결이 아직 없는 항목은 `QM` 또는 `TBD`로 시작한다.
5. `Status`는 `Planned -> Ready -> Pass/Fail` 순서로만 관리한다.
6. `05_Unit_Test.md`의 Simulator 입력/출력 지원 행은 formal requirement ownership이 잠기기 전까지 본 Matrix의 주 표면에 올리지 않는다.
7. `UT` 승격 판단은 `04_SW_Implementation.md` 대신 `canoe/src/capl` actual ownership을 우선 기준으로 사용한다.

## 3. 01 문서와의 관계

현재 `01_Requirements.md`는 `중요도/긴급도` 축을 가진다.

안전 추적성을 더 명확히 하려면 다음 열을 `중요도/긴급도` 옆에 별도로 두는 것이 좋다.

- `HARA ID`
- `ASIL/QM`
- `Safety Goal Ref`

이 축은 우선순위와 다르므로 같은 열에 섞지 않는다.

## 4. Master Test Matrix (Compact Appendix Baseline)

????? ?? ? row-level matrix? ??? ?? ??, ?? active executable baseline? tier? coverage group?? ?????.
?? per-ID row? ?? `05/06/07`? `test-asset-mapping.md`?? ?????.

### 4.1 Unit Test coverage groups

- chassis / gateway baseline
  - IDs: `UT_001`, `UT_002`, `UT_009`
  - req cluster: `Req_007~016`, `Req_037~042`
  - focus: vehicle-state, nav-context, route normalization
  - evidence: `evidence/UT_001~UT_002`, `UT_009`
- emergency and arbitration core
  - IDs: `UT_003~UT_015`
  - req cluster: `HC-01`, `HC-03`, `HC-04`
  - focus: zone decision, emergency ingest, selected alert, ambient/text render
  - evidence: `evidence/UT_003~UT_015`
- extended body / comfort / chassis context
  - IDs: `UT_016~UT_027`
  - req cluster: `Req_040~095`
  - focus: brake, occupant, comfort, propulsion, charge context
  - evidence: `evidence/UT_016~UT_027`
- input normalization family
  - IDs: `UT_028~UT_062`
  - req cluster: input seam verification
  - focus: domain input normalization and observer consistency
  - evidence: `evidence/UT_028~UT_062`
- diagnostic and service boundary
  - IDs: `UT_063~UT_065`
  - req cluster: `Req_093`
  - focus: security, diagnostic, backbone fail-safe interpretation
  - evidence: `evidence/UT_063~UT_065`
- output and external transmission
  - IDs: `UT_070~UT_077`
  - req cluster: `Req_033~035`, `Req_096~097`
  - focus: ambient/HMI/audio render and external TX observation
  - evidence: `evidence/UT_070~UT_077`

### 4.2 Integration Test coverage groups

- baseline warning activation
  - IDs: `IT_001~IT_009`
  - req cluster: `HC-01`, `HC-02`, `HC-03`, `HC-04`
  - focus: base activation, school-zone path, emergency priority, timeout clear
  - evidence: `evidence/IT_001~IT_009`
- output policy and assist coupling
  - IDs: `IT_010~IT_018`
  - req cluster: warning output / assist policy
  - focus: decel assist, fail-safe minimum warning, display/audio policy
  - evidence: `evidence/IT_010~IT_018`
- vehicle baseline and body control
  - IDs: `IT_019~IT_030`
  - req cluster: chassis, body, comfort baseline
  - focus: parked/drive baseline, door/window/wiper/security context
  - evidence: `evidence/IT_019~IT_030`
- output stability and service integration
  - IDs: `IT_031~IT_043`
  - req cluster: HMI / output robustness
  - focus: audio runtime, fallback, duplicate suppression, display/service integration
  - evidence: `evidence/IT_031~IT_043`
- diagnostic and Ethernet TX
  - IDs: `IT_040`, `IT_044`, `IT_045`
  - req cluster: `Req_093`, `Req_096`, `Req_097`
  - focus: service/security/diag context and external TX continuity
  - evidence: `evidence/IT_040`, `IT_044`, `IT_045`

### 4.3 System Test coverage groups

- power-on and zone transition
  - IDs: `ST_001~ST_010`
  - req cluster: baseline + `HC-01`, `HC-02`
  - focus: no-warning baseline, school/highway transition, guide render
  - evidence: `evidence/ST_001~ST_010`
- emergency precedence and restore
  - IDs: `ST_011~ST_021`
  - req cluster: `HC-03`, `HC-04`
  - focus: emergency override, tie-break, TX period, timeout clear, restore
  - evidence: `evidence/ST_011~ST_021`
- object-risk and fail-safe path
  - IDs: `ST_022~ST_029`
  - req cluster: `HC-05`, `HC-06`
  - focus: decel coupling, fail-safe entry/recovery, object-risk scenario
  - evidence: `evidence/ST_022~ST_029`
- HMI stability and history
  - IDs: `ST_030~ST_038`
  - req cluster: `HC-07`, `HC-08`
  - focus: seatbelt context, distance/history, popup guard, audio/visual stability
  - evidence: `evidence/ST_030~ST_038`
- extended context and trip sequence
  - IDs: `ST_039~ST_046`
  - req cluster: extended service / trip scenario
  - focus: chassis/body/service/charge context, trip sequence, fail-safe round-trip
  - evidence: `evidence/ST_039~ST_046`
## 5. 운영 규칙

1. 본 문서의 `Req ID`는 `01_Requirements.md`와 항상 동기화한다.
2. `05/06/07`에서 Test ID가 바뀌면 본 문서를 먼저 갱신한다.
3. `Pass/Fail` 전환 전에 반드시 `Oracle`, `Timing`, `Evidence`가 고정되어 있어야 한다.
4. `ASIL/QM`는 `HARA`와 분리된 우선순위 정보가 아니므로 `중요도/긴급도`와 혼합하지 않는다.
5. 진단 항목은 `diagnostic-matrix.md`와 함께 관리하되, 핵심 경고 체인은 진단 비의존으로 유지한다.
6. `UT_028 ~ UT_069`와 같은 stimulus/support asset은 `05_Unit_Test.md`에는 유지하되, formal requirement ownership이 잠기기 전까지는 본 Matrix의 baseline row로 승격하지 않는다.

## 6. 다음 단계

1. `01_Requirements.md`에 `HARA ID`, `ASIL/QM`, `Safety Goal Ref` 열 추가 검토
2. `05/06/07`과 본 Matrix의 `Req ID / Status / Evidence` 동기화를 유지
3. `canoe/src/capl` actual ownership 기준으로 direct requirement ownership이 확인된 `UT`만 후속 승격
4. `test-asset-mapping.md`와 `native-test-asset-naming.md` 기준으로 executable asset 연결
