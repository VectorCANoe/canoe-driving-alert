# 단위 테스트 (Unit Test)

**Document ID**: PROJ-05-UT
**ISO 26262 Reference**: Part 6, Cl.9 (Software Unit Verification)
**ASPICE Reference**: SWE.4 (Software Unit Verification)
**Version**: 2.21
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 하단 (SWE.4) | `05_Unit_Test.md` | `04_SW_Implementation.md` | `06_Integration_Test.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 단위 테스트(UT) 관점의 검증 항목을 정리한다.
- 제출본은 상단 공식 UT 표를 유지하고, 상세 분기는 축소한다.
- 경계값/세부 케이스 전수는 원문 05에서 관리한다.
- Req/VC 추적 키는 원문과 동일하게 유지한다.
- Pre-Activation 라벨은 원문과 동일하게 유지한다.
- 대조군/우수성 비교 실험은 제출본 범위 밖으로 두고 Pass/Fail 중심으로 제시한다.
- 검증 배치 실행/리포트 생성은 `scripts/run.py verify batch` 기준(기본 `json,md`, 옵션 `csv`)으로 운영한다.

---

## 단위 테스트 표 (공식 표준 양식)

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| 제어기 | 제어 | CHS_GW | CAN(0x2A0/0x2A1) 수신값을 ETH(0x510/0x511)로 100ms 주기 변환 송신 |  |  |  |
|  |  | INFOTAINMENT_GW | CAN(0x2A3) 구간/방향/거리/제한속도 입력을 ETH(0x512)로 100ms 주기 변환 송신 |  |  |  |
|  |  | ADAS_WARN_CTRL | 주행/비주행, 과속(vehicleSpeed>speedLimit), 무조향 조건을 판정해 150ms 이내 경고 상태 반영 |  |  |  |
|  |  | ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR (V2 확장) | 긴급차량 방향/ETA/자차속도 기반 위험도 산정, 감속 보조 요청/해제, Fail-safe 강등 동기화 | Ready |  |  |
|  |  | ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR (ADAS 객체 확장, Planned) | 객체 목록 수용, TTC/상대속도 기반 단계화, 교차로/합류 위험 경고, 신뢰도 저하 강등/이벤트 기록 | Planned |  |  |
|  |  | WARN_ARB_MGR + EMS_ALERT + CLU_HMI_CTRL (차량 경보 편의 확장, Planned) | 방향지시등/주행모드/안전벨트 기반 경보 보정, 접근거리 표시, 이벤트 기록·이력, 표시/음량 설정 반영 | Planned |  |  |
|  |  | WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR + CLU_HMI_CTRL (경고 강건성·인지성 확장, Planned) | 입력 유효성/신선도 보호, 상태 전이 안정화, 채널 가용성·대체 출력, 오디오 경합/팝업 과밀/채널 동기 복원 정책 검증 | Planned |  |  |
|  |  | NAV_CTX_MGR | roadZone/navDirection/zoneDistance/speedLimit 입력으로 컨텍스트 계산 및 speedLimitNorm 갱신 |  |  |  |
|  |  | EMS_ALERT | 경찰/구급 긴급 이벤트의 송신/수신/해제/타임아웃(1000ms) 모듈 로직을 유닛 단위로 검증 |  |  |  |
|  |  | WARN_ARB_MGR | Emergency>Zone, Ambulance>Police, ETA, SourceID 규칙으로 단일 경고 결과 결정 |  |  |  |
|  |  | BODY_GW | 중재 결과(E200)를 Ambient CAN(0x289)으로 50ms 주기 변환 송신 |  |  |  |
|  |  | IVI_GW | 중재 결과(E200)를 Cluster CAN(0x280)으로 50ms 주기 변환 송신 |  |  |  |
|  |  | AMBIENT_CTRL | selectedAlert 결과에 따라 ambientMode/color/pattern 정책 출력(전환 안정화 포함) |  |  |  |
|  |  | CLU_HMI_CTRL | warningTextCode/방향 표시/중복팝업 억제 정책 적용 |  |  |  |
|  |  | VAL_SCENARIO_CTRL | testScenario 실행, 통신 조건(CAN+Ethernet 또는 대체 백본) 판정, scenarioResult 기록 |  |  |  |
|  |  | VAL_BASELINE_CTRL | 차량 기본 기능(시동/기어/입력/표시) 단위 검증 및 결과 반영 |  |  |  |
| 가상 노드 (Simulator) | 입력 | Vehicle/Steering Input | `gVehicleSpeed`, `gDriveState`, `SteeringInput` 입력 생성 |  |  |  |
|  |  | Nav Context Input | `gRoadZone`, `gNavDirection`, `gZoneDistance`, `gSpeedLimit` 입력 생성 |  |  |  |
|  |  | Emergency Input | Police/Ambulance Active/Clear, ETA, Direction, SourceID 입력 생성 |  |  |  |
|  | 출력 | Ambient Output | `AmbientMode`, `AmbientColor`, `AmbientPattern` 출력 확인(50ms 주기) |  |  |  |
|  |  | Cluster Output | `WarningTextCode` 출력 확인(50ms 주기) |  |  |  |
|  |  | Scenario Result | `ScenarioResult` 및 로그 결과 확인 |  |  |  |

---

## 단위 테스트 대표 추적 표 (축소본)

- 제출본은 대표 UT만 유지하고, 전수 UT 추적은 원문 SoT(`driving-situation-alert/05_Unit_Test.md`)에서 관리한다.

| UT ID | 대상 모듈 | Req/VC(대표) | 검증 포인트 | 상태 |
|---|---|---|---|---|
| UT_ADAS_001 | ADAS_WARN_CTRL | Req_001~012 / VC_001~012 | 경고 시작/해제/디바운스 (`150ms`) | Active |
| UT_EMS_RX_001 | EMS_ALERT_RX | Req_023, Req_024 / VC_023, VC_024 | 긴급 수신/해제/타임아웃(`1000ms`) | Active |
| UT_ARB_001 | WARN_ARB_MGR | Req_022, Req_025~032 / VC_022, VC_025~032 | 경보 우선순위 판정 결정론 | Active |
| UT_BCM_001 | AMBIENT_CTRL | Req_008~009, Req_033~037 / VC_008~009, VC_033~037 | 패턴/색상/복귀 정책 | Active |
| UT_CLU_001 | CLU_HMI_CTRL | Req_005, Req_019~021, Req_040 / VC_005, VC_019~021, VC_040 | 문구/중복억제 정책 | Active |
| UT_GW_001 | CHS_GW, INFOTAINMENT_GW | Req_007, Req_010~012 / VC_007, VC_010~012 | CAN->ETH 변환 정확성 | Active |
| UT_SIL_001 | VAL_SCENARIO_CTRL | Req_041~043 / VC_041~043 | SIL 실행/판정/기록 | Active |
| UT_BASE_001 | Baseline 노드군 | Req_101~119 / VC_101~119 | 기본 차량 기능 총괄 커버리지 | Active |
| UT_V2_RISK_001 | ADAS_WARN_CTRL, WARN_ARB_MGR | Req_120, Req_121, Req_123, Req_125, Req_126 | 위험도-보조요청-해제-동기화 | Ready |
| UT_V2_FAILSAFE_001 | DOMAIN_BOUNDARY_MGR | Req_127~129 | 단절 강등/자동감속 금지 | Ready |
| UT_ADAS_OBJ_RISK_001 | ADAS_WARN_CTRL | Req_130~139 / VC_130~139 | 객체기반 위험 경고/강등 | Planned |
| UT_BASE_ROBUST_EXT_001 | WARN_ARB_MGR, CLU_HMI_CTRL | Req_148~155 / VC_148~155 | 강건성/인지성 정책 | Planned |
