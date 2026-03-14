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

## 4. Master Test Matrix (Draft Baseline)

| Req ID | HARA ID | Safety Goal | ASIL/QM | Test Level | Test Case ID | Stimulus | Oracle | Timing | Evidence | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Req_007, Req_008, Req_009, Req_010` | `HC-01` | 구간 정보와 제한속도 조건은 기본 경고 판단에 직접 반영되어야 한다 | `ASIL B (Locked)` | `UT` | `UT_003` | 구간 타입, 방향, 거리, 제한속도, 차량 속도 입력 | `ADAS.can`의 base zone 판단과 `warningState`가 기본/스쿨존 조건에 맞게 결정된다 | `100ms/150ms` | `evidence/UT_003/*` | `Validation` | `Ready` |
| `Req_017, Req_018, Req_019, Req_020, Req_022, Req_023` | `HC-03, HC-04` | 긴급 이벤트 수신, 유지, 종료, timeout clear는 직접 관리되어야 한다 | `ASIL C / B (Locked)` | `UT` | `UT_004` | 경찰/구급 이벤트 수신, 종료 신호, 무갱신 timeout 입력 | `V2X.can`이 활성 이벤트, 방향, ETA, timeout clear를 일관되게 갱신한다 | `1000ms + 200ms pulse` | `evidence/UT_004/*` | `Validation` | `Ready` |
| `Req_049, Req_050, Req_051, Req_052, Req_053` | `-` | 위험도와 감속 보조 요청은 긴급 맥락과 운전자 개입 조건에 따라 직접 결정되어야 한다 | `TBD` | `UT` | `UT_005` | ETA, 방향, 자차 속도, 근접 위험도, 운전자 개입 입력 | `ADAS.can`의 `proximityRiskLevel`, `decelAssistReq`, `driverReleaseReason`가 정책에 맞게 결정된다 | `<=150ms` | `evidence/UT_005/*` | `Validation` | `Ready` |
| `Req_021, Req_024, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031` | `HC-03` | 일반 경고와 긴급 경고 충돌 시 단일 최종 경고가 중재 규칙에 따라 결정되어야 한다 | `ASIL C (Locked)` | `UT` | `UT_011` | 일반 경고, 경찰/구급 긴급 경고, ETA, SourceID 동시 입력 | `ADAS.can`의 `selectedAlertLevel`과 `selectedAlertType`이 우선순위 규칙에 따라 일관되게 결정된다 | `<=150ms` | `evidence/UT_011/*` | `Validation` | `Ready` |
| `Req_033, Req_034, Req_035` | `HC-04 / Safety-support` | 앰비언트 색상과 패턴은 긴급/구간 정책에 따라 고정 규칙으로 출력되어야 한다 | `ASIL B (Locked) / QM` | `UT` | `UT_014` | 선택 경고 레벨/타입과 timeout/fail-safe 조건 입력 | `BCM.can`의 `ambientColor`와 `ambientPattern`이 긴급/스쿨존/고속/유도구간 규칙에 맞게 결정된다 | `50ms` | `evidence/UT_014/*` | `Validation` | `Ready` |
| `Req_018, Req_019, Req_020, Req_036` | `HC-03 / Safety-support` | 경고 문구와 방향 표시는 긴급 종류와 방향 맥락에 따라 일관되게 출력되어야 한다 | `ASIL C (Locked) / QM` | `UT` | `UT_015` | 경고 레벨/타입, 긴급 종류, 방향, timeout 입력 | `IVI.can`의 warning text code 생성과 `CLU.can`의 최종 표시 반영이 일관되게 유지된다 | `50ms` | `evidence/UT_015/*` | `Validation` | `Ready` |
| `Req_093` | `-` | 보안 게이트웨이 상태는 경고 전달 가용성과 서비스 강등 정책에 직접 반영되어야 한다 | `QM / Serviceability` | `UT` | `UT_063` | 경계 상태, fail-safe, 주행 구간, 경고 활성 상태 입력 | `SGW.can`의 session, auth, fault, route, service 상태가 정책에 맞게 계산된다 | `100ms` | `evidence/UT_063/*` | `Validation` | `Planned` |
| `Req_093` | `-` | 진단 제어 상태는 경고 전달 가용성과 서비스 강등 정책에 직접 반영되어야 한다 | `QM / Serviceability` | `UT` | `UT_064` | 경계 상태, fail-safe, 주행 구간, 경고 활성 상태 입력 | `DCM.can`의 session, auth, fault, policy 상태가 정책에 맞게 계산된다 | `100ms` | `evidence/UT_064/*` | `Validation` | `Planned` |
| `Req_096` | `-` | 경찰 긴급 이벤트는 외부 송신 채널로 직접 송신되어야 한다 | `QM` | `UT` | `UT_076` | 경찰 긴급 이벤트 활성/해제 입력 | `V2X.can`이 경찰 긴급 알림 프레임을 송신하고 종료 시 clear를 송신한다 | `100ms` | `evidence/UT_076/*` | `Validation` | `Ready` |
| `Req_097` | `-` | 구급 긴급 이벤트는 외부 송신 채널로 직접 송신되어야 한다 | `QM` | `UT` | `UT_077` | 구급 긴급 이벤트 활성/해제 입력 | `V2X.can`이 구급 긴급 알림 프레임을 송신하고 종료 시 clear를 송신한다 | `100ms` | `evidence/UT_077/*` | `Validation` | `Ready` |
| `Req_001, Req_002, Req_003, Req_004, Req_005, Req_006` | `-` | 기본 주행 조건에서 경고 활성 경로가 올바르게 진입/해제되어야 한다 | `QM` | `IT` | `IT_001` | 주행 상태 변경, 기본 활성/비활성 조건 입력 | 동일 조건 반복 시 진동 없이 경고 활성/해제 | `100ms/150ms` | `evidence/IT_001/*` | `Validation` | `Planned` |
| `Req_007, Req_008, Req_009, Req_010` | `HC-01` | 스쿨존 제한속도 초과 시 경고가 지연 없이 표시되어야 한다 | `ASIL B (Locked)` | `IT` | `IT_002` | 구간, 방향, 거리, 제한속도, 과속 조건 입력 | 스쿨존 및 제한속도 초과 조건이 `150ms` 이내 경고 판단에 반영 | `<=150ms` | `evidence/IT_002/*` | `Validation` | `Planned` |
| `Req_011, Req_012` | `HC-02` | 무조향 의심 경고는 조건 성립 시 발생하고 조향 복귀 시 즉시 해제되어야 한다 | `ASIL C (Locked)` | `IT` | `IT_003` | 고속 구간 무조향 지속 후 조향 복귀 입력 | 경고 발생/해제가 각각 `150ms` 이내 일치 | `<=150ms` | `evidence/IT_003/*` | `Validation` | `Planned` |
| `Req_017, Req_018, Req_019, Req_020` | `HC-03` | 긴급 경고는 구간 경고보다 우선 적용되어야 한다 | `ASIL C (Locked)` | `IT` | `IT_004` | 경찰 긴급 알림 수신 입력 | 수신 후 `150ms` 이내 경찰 경고와 안내 반영 | `<=150ms` | `evidence/IT_004/*` | `Validation` | `Planned` |
| `Req_017, Req_018, Req_019, Req_020` | `HC-03` | 긴급 경고는 구간 경고보다 우선 적용되어야 한다 | `ASIL C (Locked)` | `IT` | `IT_005` | 구급 긴급 알림 수신 입력 | 수신 후 `150ms` 이내 구급 경고와 안내 반영 | `<=150ms` | `evidence/IT_005/*` | `Validation` | `Planned` |
| `Req_021, Req_024, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031` | `HC-03` | 긴급 경고는 일반 경고보다 우선 적용되고 동급 간에는 정해진 규칙으로 단일 결정되어야 한다 | `ASIL C (Locked)` | `IT` | `IT_006` | 일반 경고와 경찰/구급 긴급 경고 동시 입력 | 긴급 우선, 구급 우선, ETA/SourceID 단일 결정 일관성 확보 | `<=150ms` | `evidence/IT_006/*` | `Validation` | `Planned` |
| `Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_021, Req_026, Req_033, Req_034, Req_035` | `HC-01, HC-03` | 선택된 경고가 출력 채널에 일관되게 전달되어야 한다 | `QM / Safety-support` | `IT` | `IT_007` | 기본 경고와 긴급 경고 결과 입력 | 앰비언트 색상, 패턴, 전환 동작이 일치 | `50ms` | `evidence/IT_007/*` | `Validation` | `Planned` |
| `Req_005, Req_018, Req_019, Req_020, Req_021, Req_026, Req_036` | `HC-03` | 선택된 경고가 표시 채널에 일관되게 전달되어야 한다 | `QM / Safety-support` | `IT` | `IT_008` | 기본 경고와 긴급 경고 결과 입력 | 문구, 긴급차량 종류, 방향 정보가 안정적으로 일치 | `50ms/150ms` | `evidence/IT_008/*` | `Validation` | `Planned` |
| `Req_022, Req_023, Req_025, Req_032, Req_076, Req_077` | `HC-04` | 긴급 신호 무갱신 시 경고를 안전하게 해제하고 정상 상태로 복귀해야 한다 | `ASIL B (Locked)` | `IT` | `IT_009` | 종료 신호 또는 `1000ms` 무갱신 입력 | stale 보호 후 안전 해제, 직전 유효 상태 또는 기본 상태 복귀 | `1000ms + <=150ms` | `evidence/IT_009/*` | `Validation` | `Planned` |
| `Req_049, Req_050, Req_051, Req_052, Req_053` | `-` | 위험도 기반 감속 보조 요청과 경고 출력이 함께 일치해야 한다 | `TBD` | `IT` | `IT_010` | 긴급차량 근접 위험도 상승, 운전자 개입 입력 | 감속 보조 요청 생성, 출력 채널 간 동기 유지, 개입 시 해제 | `<=150ms, <=50ms` | `evidence/IT_010/*` | `Validation` | `Ready` |
| `Req_054, Req_055, Req_056` | `HC-05` | 전달 단절 시 강등 동작이 즉시 적용되어야 한다 | `ASIL C (Locked)` | `IT` | `IT_011` | 경고 전달 이상 또는 경계 오류 입력 | fail-safe 진입, 자동 감속 차단, 최소 경고 채널 유지 | `<=150ms` | `evidence/IT_011/*` | `Validation` | `Ready` |
| `Req_057, Req_058, Req_059, Req_060, Req_061, Req_062, Req_063, Req_064, Req_065, Req_075` | `HC-06` | 객체 기반 위험 경고는 기준 시간 내 발생, 강등, 해제되어야 한다 | `ASIL C (Provisional)` | `IT` | `IT_012` | 객체 입력, 신뢰도 저하, 유효성 미달 입력 | 위험 경고 발생, 유효성 미달 제외, 강등과 이벤트 기록 일치 | `100ms + <=150ms` | `evidence/IT_012/*` | `Validation` | `Planned` |
| `Req_067, Req_068, Req_069, Req_073, Req_074` | `-` | 운전자 상태와 경고 설정이 출력 정책에 반영되어야 한다 | `QM` | `IT` | `IT_013` | 방향지시등, 주행모드, 안전벨트, 표시/음량 설정 입력 | `150ms` 이내 표시 및 출력 정책 반영 | `<=150ms` | `evidence/IT_013/*` | `Validation` | `Planned` |
| `Req_049, Req_050, Req_057, Req_058, Req_059, Req_060, Req_061, Req_062, Req_063, Req_066` | `HC-06` | 긴급차량 접근과 TTC 충돌 위험 동시 입력 시 단일 최종 경고가 선택되어야 한다 | `ASIL C (Provisional)` | `IT` | `IT_014` | 긴급 접근 + 교차로/합류 TTC 위험 동시 입력 | 자동 감속 보조 생성, 우선 경고 단일 선택, 출력 채널 상충 없음 | `<=150ms` | `evidence/IT_014/*` | `Validation` | `Planned` |
| `Req_037, Req_038` | `-` | 시동 및 기어 상태는 경고 판단 경로에 일관되게 반영되어야 한다 | `QM` | `IT` | `IT_015` | 시동 ON/OFF, 기어 상태 변화 입력 | 시동과 기어 상태가 `100ms` 주기로 누락 없이 반영 | `100ms` | `evidence/IT_015/*` | `Validation` | `Planned` |
| `Req_039, Req_040, Req_041` | `HC-02` | 가속, 제동, 조향 입력은 주행 판단 경로에 정확히 반영되어야 한다 | `QM / Safety-support` | `IT` | `IT_016` | 가속, 제동, 조향 입력 변화 | 입력 상태가 `100ms` 기준으로 일관되게 반영되고 주행 판단 경로에 전달 | `100ms` | `evidence/IT_016/*` | `Validation` | `Planned` |
| `Req_042, Req_043` | `-` | 비상등과 창문 상태는 경고 맥락에 일관되게 반영되어야 한다 | `QM` | `IT` | `IT_017` | 비상등, 창문 상태 변화 입력 | 관련 상태 변화가 누락 없이 반영 | `100ms` | `evidence/IT_017/*` | `Validation` | `Planned` |
| `Req_044` | `-` | 기본 표시 및 UI 연동은 주기 규칙을 만족해야 한다 | `QM` | `IT` | `IT_018` | 기본 표시 및 UI 연동 조건 입력 | 표시 상태와 연계 이벤트가 `50/100ms` 규칙을 만족 | `50ms/100ms` | `evidence/IT_018/*` | `Validation` | `Planned` |
| `Req_045, Req_046, Req_047` | `-` | 실내 제어와 보안 상태는 경고 정책에 일관되게 반영되어야 한다 | `QM` | `IT` | `IT_019` | 공조, 시트, 미러, 도어, 와이퍼, 보안 상태 입력 | 관련 상태와 제어 정보가 `100ms` 주기로 연계되고 `150ms` 이내 정책에 반영 | `100ms/150ms` | `evidence/IT_019/*` | `Validation` | `Planned` |
| `Req_048` | `HC-08` | 오디오 경합 상황에서도 경고 인지성이 유지되어야 한다 | `ASIL B (Provisional)` | `IT` | `IT_020` | 오디오 동시 실행 환경 입력 | 경고 인지가 가능하고 오디오 환경이 HMI 정책에 반영 | `50ms/100ms/150ms` | `evidence/IT_020/*` | `Validation` | `Planned` |
| `Req_078, Req_079, Req_081, Req_082` | `HC-07, HC-08` | 채널 장애와 팝업 과밀 상황에서도 우선 경고 인지성과 채널 동기가 유지되어야 한다 | `ASIL C / B (Provisional)` | `IT` | `IT_021` | 출력 채널 장애, 팝업 과밀, 대체 출력 조건 입력 | 대체 출력 전환, 과밀 억제, 채널 불일치 복원 | `<=150ms` | `evidence/IT_021/*` | `Validation` | `Planned` |
| `Req_070, Req_071, Req_072` | `-` | 접근거리 표시와 경고 이력 조회는 일관되게 제공되어야 한다 | `QM` | `IT` | `IT_022` | 접근거리 변화, 경고 이력 조회 요청 입력 | 거리 표시 갱신, 이벤트 공통 포맷 기록, 이력 응답 누락 없음 | `<=200ms` | `evidence/IT_022/*` | `Validation` | `Planned` |
| `Req_083, Req_084` | `-` | 제동 및 차체 제어 상태가 경고 맥락에 일관되게 반영되어야 한다 | `QM` | `IT` | `IT_023` | EPB/EHB/VSM/ECS/CDC 상태 입력 | 제동과 차체 제어 상태가 경고 맥락에 반영 | `100ms/150ms` | `evidence/IT_023/*` | `Validation` | `Ready` |
| `Req_085, Req_086, Req_087` | `-` | 도어, 탑승자, 실내 편의 상태가 정책에 일관되게 반영되어야 한다 | `QM` | `IT` | `IT_024` | 도어, 테일게이트, 에어백, 탑승자, 공조, 시트, 선루프 입력 | 상태가 `100ms` 주기로 반영되고 정책에 반영 | `100ms/150ms` | `evidence/IT_024/*` | `Validation` | `Ready` |
| `Req_088, Req_089` | `-` | 표시 및 안내 서비스 상태가 경고 정책에 반영되어야 한다 | `QM` | `IT` | `IT_025` | HUD, AMP, TMU, 디지털 접근 서비스 상태 입력 | 표시와 안내 서비스 상태 반영 | `100ms/150ms` | `evidence/IT_025/*` | `Validation` | `Ready` |
| `Req_090, Req_091, Req_092` | `-` | 주행 보조, 주차 보조, 인지 센서 상태가 위험 판단과 가용성에 반영되어야 한다 | `QM / Safety-support` | `IT` | `IT_026` | 주행 보조, 주차 보조, 인지 센서 상태 입력 | 위험, 가용성, 강등 정책 반영 | `100ms/150ms` | `evidence/IT_026/*` | `Validation` | `Ready` |
| `Req_093` | `-` | 서비스, 보안, 진단 상태가 경고 전달 가용성과 강등 상태에 반영되어야 한다 | `QM / Serviceability` | `IT` | `IT_027` | IBOX, SGW, DCM 관련 서비스/보안/진단 상태 입력 | 서비스 강등과 전달 가용성 상태가 즉시 반영 | `100ms` | `evidence/IT_027/*` | `Validation` | `Ready` |
| `Req_094, Req_095` | `-` | 충전, 전력 변환, 구동, 변속·열관리 상태가 경고 맥락에 반영되어야 한다 | `QM` | `IT` | `IT_028` | OBC, DCDC, MCU, INVERTER, 변속·열관리 상태 입력 | 구동 준비와 서비스 경고 맥락 반영 | `100ms/150ms` | `evidence/IT_028/*` | `Validation` | `Ready` |
| `Req_067, Req_069, Req_070, Req_073, Req_088, Req_089` | `-` | 표시 채널과 안내 서비스 상태는 출력 정책에 일관되게 연동되어야 한다 | `QM` | `IT` | `IT_029` | 경고 문구, 접근거리, 표시 방식, 표시/서비스 상태 입력 | 표시 채널 간 출력 차이가 `50ms` 이내이고 정책 반영이 일관됨 | `50ms/150ms` | `evidence/IT_029/*` | `Validation` | `Ready` |
| `Req_048, Req_074, Req_075, Req_076, Req_077, Req_080` | `HC-08` | 오디오 안내와 입력 강건성은 경고 인지성과 출력 안정성을 유지해야 한다 | `ASIL B (Provisional)` | `IT` | `IT_030` | 오디오 경합, 음량 설정, stale/무효 입력 조건 | 경고 인지가 유지되고 무효 또는 stale 입력은 판정에서 제외되며 반복 진동이 억제됨 | `50ms/100ms/150ms` | `evidence/IT_030/*` | `Validation` | `Ready` |
| `Req_096` | `-` | 경찰 긴급 알림은 외부 송신 채널로 일관되게 송신되어야 한다 | `QM` | `IT` | `IT_031` | 경찰 긴급 이벤트 발생 입력 | 외부 송신 프레임 출력, 송신 주기 유지 | `100ms` | `evidence/IT_031/*` | `Validation` | `Ready` |
| `Req_097` | `-` | 구급 긴급 알림은 외부 송신 채널로 일관되게 송신되어야 한다 | `QM` | `IT` | `IT_032` | 구급 긴급 이벤트 발생 입력 | 외부 송신 프레임 출력, 송신 주기 유지 | `100ms` | `evidence/IT_032/*` | `Validation` | `Ready` |
| `Req_049, Req_050, Req_051, Req_052, Req_053` | `-` | 교차로 위험과 긴급 접근이 동시 발생해도 시스템 레벨에서 감속 보조와 경고 출력이 함께 일치해야 한다 | `TBD` | `ST` | `ST_021` | 교차로에서 긴급 접근과 TTC 위험 동시 입력 | 감속 보조 요청과 경고 출력이 함께 활성 | `<=150ms` | `evidence/ST_021/*` | `Validation` | `Ready` |
| `Req_049, Req_050, Req_051, Req_052, Req_053` | `-` | 합류 위험과 긴급 접근이 동시 발생해도 시스템 레벨에서 감속 보조와 경고 출력이 함께 일치해야 한다 | `TBD` | `ST` | `ST_022` | 합류 구간에서 긴급 접근과 TTC 위험 동시 입력 | 감속 보조 요청과 경고 출력이 함께 활성 | `<=150ms` | `evidence/ST_022/*` | `Validation` | `Ready` |
| `Req_049, Req_050, Req_051, Req_052, Req_053` | `-` | 운전자 개입 시 시스템 레벨에서 감속 보조와 경고 상태가 함께 해제되어야 한다 | `TBD` | `ST` | `ST_023` | 자동 감속 보조 활성 상태에서 운전자 개입 입력 | 감속 보조 요청과 경고 상태가 함께 해제 | `<=150ms` | `evidence/ST_023/*` | `Validation` | `Ready` |
| `Req_054, Req_055, Req_056` | `HC-05` | 전달 단절 시 강등 동작이 즉시 적용되어야 한다 | `ASIL C (Locked)` | `ST` | `ST_024` | 시스템 시나리오 중 경고 전달 이상 발생 | fail-safe 진입, 최소 채널 유지, 자동 감속 차단 | `<=150ms` | `evidence/ST_024/*` | `Validation` | `Ready` |
| `Req_054, Req_055, Req_056` | `HC-05` | 전달 이상 해제 후 시스템은 정상 경로로 복귀해야 한다 | `ASIL C (Locked)` | `ST` | `ST_025` | fail-safe 이후 전달 이상 해제 | 정상 경로 복귀와 출력 정책 정상화 | `<=150ms` | `evidence/ST_025/*` | `Validation` | `Ready` |
| `Req_057, Req_058, Req_059, Req_060, Req_061, Req_062, Req_063, Req_064, Req_065, Req_075` | `HC-06` | 객체 급접근 위험 시 시스템 레벨에서 경고와 이벤트 기록이 일관되게 동작해야 한다 | `ASIL C (Provisional)` | `ST` | `ST_026` | 전방 객체 급접근 입력 | 위험 경고와 이벤트 기록이 일관되게 동작 | `<=150ms` | `evidence/ST_026/*` | `Validation` | `Planned` |
| `Req_057, Req_058, Req_059, Req_060, Req_061, Req_062, Req_063, Req_064, Req_065, Req_075` | `HC-06` | 측방 접근 위험 시 시스템 레벨에서 경고와 이벤트 기록이 일관되게 동작해야 한다 | `ASIL C (Provisional)` | `ST` | `ST_027` | 교차로 측방 접근 입력 | 위험 경고와 이벤트 기록이 일관되게 동작 | `<=150ms` | `evidence/ST_027/*` | `Validation` | `Planned` |
| `Req_057, Req_058, Req_059, Req_060, Req_061, Req_062, Req_063, Req_064, Req_065, Req_075` | `HC-06` | 합류 및 끼어들기 위험 시 시스템 레벨에서 경고와 이벤트 기록이 일관되게 동작해야 한다 | `ASIL C (Provisional)` | `ST` | `ST_028` | 합류 또는 끼어들기 위험 입력 | 위험 경고와 이벤트 기록이 일관되게 동작 | `<=150ms` | `evidence/ST_028/*` | `Validation` | `Planned` |
| `Req_067, Req_068, Req_069, Req_070, Req_073` | `-` | 운전자 상태와 접근거리 정보가 시스템 레벨 경고 안내에 기대대로 반영되어야 한다 | `QM` | `ST` | `ST_029` | 방향지시등, 주행모드, 안전벨트, 접근거리 표시 조건 입력 | 사용자 기대와 일치하는 안내 보정 | `<=150ms` | `evidence/ST_029/*` | `Validation` | `Planned` |
| `Req_073, Req_074` | `-` | 표시 설정과 음량 설정은 시스템 레벨 경고 정책에 즉시 반영되어야 한다 | `QM` | `ST` | `ST_030` | 표시 설정 및 음량 설정 변경 입력 | 설정 변경이 경고 안내 정책에 즉시 반영 | `<=150ms` | `evidence/ST_030/*` | `Validation` | `Planned` |
| `Req_071, Req_072` | `-` | 경고 이력 조회는 시스템 레벨에서 최근 경고 순서와 원인 정보를 일관되게 제공해야 한다 | `QM` | `ST` | `ST_031` | 경고 발생 후 이력 조회 요청 입력 | 최근 경고 순서와 원인 정보가 일관되게 제공 | `<=200ms` | `evidence/ST_031/*` | `Validation` | `Planned` |
| `Req_075, Req_076, Req_077, Req_080` | `HC-08` | 입력 지연과 상태 전이 상황에서도 경고 안내는 안정적으로 유지되어야 한다 | `ASIL B (Provisional)` | `ST` | `ST_032` | 입력 지연, stale, 상태 전이 조건 입력 | 경고 안내가 안정적으로 유지되고 반복 진동이 억제 | `<=150ms` | `evidence/ST_032/*` | `Validation` | `Planned` |
| `Req_078, Req_079, Req_080, Req_081, Req_082` | `HC-07, HC-08` | 경고 인지성과 채널 동기가 다중 부하 상황에서도 유지되어야 한다 | `ASIL C / B (Provisional)` | `ST` | `ST_033` | 채널 전환, 오디오 경합, 팝업 과밀 입력 | 안정적 출력, 우선 경고 인지성 유지, 채널 동기 유지 | `<=150ms` | `evidence/ST_033/*` | `Validation` | `Planned` |
| `Req_083, Req_084` | `-` | 제동 및 차체 안정화 상태 변화는 시스템 시나리오에서 경고 맥락에 일관되게 반영되어야 한다 | `QM` | `ST` | `ST_034` | 제동 및 차체 안정화 상태 변화 입력 | 경고 맥락 반영이 시스템 레벨에서 일관됨 | `100ms/150ms` | `evidence/ST_034/*` | `Validation` | `Ready` |
| `Req_085, Req_086, Req_087` | `-` | 출입, 탑승자 보호, 실내 편의 상태 변화는 시스템 시나리오에서 일관되게 반영되어야 한다 | `QM` | `ST` | `ST_035` | 출입, 탑승자, 실내 편의 상태 변화 입력 | 시스템 레벨 정책 반영이 일관됨 | `100ms/150ms` | `evidence/ST_035/*` | `Validation` | `Ready` |
| `Req_088, Req_089` | `-` | 표시 및 안내 서비스 상태 변화는 시스템 시나리오에서 경고 표시와 안내 정책에 일관되게 반영되어야 한다 | `QM` | `ST` | `ST_036` | 표시 및 안내 서비스 상태 변화 입력 | 시스템 레벨 정책 반영이 일관됨 | `100ms/150ms` | `evidence/ST_036/*` | `Validation` | `Ready` |
| `Req_090, Req_091, Req_092` | `-` | 주행 보조, 주차 보조, 주변 인지 상태는 시스템 시나리오에서 위험 판단과 기능 가용성에 일관되게 반영되어야 한다 | `QM / Safety-support` | `ST` | `ST_037` | 주행 보조, 주차 보조, 인지 상태 변화 입력 | 위험 판단과 기능 가용성 반영이 일관됨 | `100ms/150ms` | `evidence/ST_037/*` | `Validation` | `Ready` |
| `Req_093` | `-` | 서비스, 보안, 진단 상태 변화가 시스템 시나리오에 일관되게 반영되어야 한다 | `QM / Serviceability` | `ST` | `ST_038` | 시스템 시나리오 중 서비스/보안/진단 상태 변화 입력 | 경고 전달 가용성과 fail-safe 정책 일관 반영 | `100ms/150ms` | `evidence/ST_038/*` | `Validation` | `Ready` |
| `Req_094, Req_095` | `-` | 충전, 전력 변환, 구동 상태 변화는 시스템 시나리오에서 구동 준비와 서비스 경고 맥락에 일관되게 반영되어야 한다 | `QM` | `ST` | `ST_039` | 충전, 전력 변환, 구동 상태 변화 입력 | 구동 준비와 서비스 경고 맥락 반영이 일관됨 | `100ms/150ms` | `evidence/ST_039/*` | `Validation` | `Ready` |
| `Req_001~Req_032` | `-` | 전원 ON부터 경고 개입과 복귀까지 연속 주행에서 시스템이 일관되게 동작해야 한다 | `QM / Integration` | `ST` | `ST_040` | 전원 ON, 일반 주행, 긴급 개입, 경고 복귀, 정지, 전원 OFF | 연속 시나리오 전체에서 일관된 동작 유지 | `scenario-based` | `evidence/ST_040/*` | `Validation` | `Planned` |
| `Req_054, Req_055, Req_056, Req_093` | `HC-05` | fail-safe 진입과 복귀를 포함한 연속 시나리오에서 시스템이 일관되게 동작해야 한다 | `ASIL C (Locked)` | `ST` | `ST_041` | 정상 주행 중 전달 이상 발생, fail-safe 진입/복귀, 정지, 전원 OFF | 연속 시나리오 전체에서 fail-safe 진입/복귀가 일관되게 유지 | `scenario-based` | `evidence/ST_041/*` | `Validation` | `Planned` |

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
