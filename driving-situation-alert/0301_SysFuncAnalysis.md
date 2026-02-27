# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.5
**Date**: 2026-02-26
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

## 작성 원칙

- 본 문서는 03_Function_definition.md의 Func_001~Func_043을 노드 내부 동작 관점으로 분해한다.
- 각 노드의 입력-처리-출력을 명확히 정의해 0302의 Tx/Rx 흐름 설계로 연결한다.
- 요구사항(What) 문장을 반복하지 않고, 시스템 동작 로직(How)만 기술한다.
- 상단 표는 공식 표준 양식의 열 구성(노드/기능 상세/비고)을 유지한다.
- 상세 추적 정보(Func/Req/실제 입출력)는 하단 표에 분리한다.
- 옵션1 아키텍처를 고정한다: 중앙 경고코어 + Ethernet 백본(ETH_SWITCH) + 도메인 게이트웨이 + 도메인 CAN.

---

## 노드별 기능 명세 (공식 표준 양식)

| 노드 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Powertrain |
| ADAS_WARN_CTRL | 차량 주행 상태 기반 경고 조건 판정 및 제어 상태 생성 | 경고 시작/해제 제어 |
|  |  | Chassis |
| EMS_ALERT_RX | 긴급 알림 수신 상태 및 해제 상태 관리 | 수신/타임아웃 해제 처리 |
| WARN_ARB_MGR | 긴급 경고와 구간 경고 충돌 시 우선순위 중재 수행 | Emergency > Zone, Ambulance > Police |
| EMS_POLICE_TX | 경찰 긴급차량 알림 생성 및 송신 제어 | EmergencyAlert 송신 제어 |
| EMS_AMB_TX | 구급 긴급차량 알림 생성 및 송신 제어 | EmergencyAlert 송신 제어 |
| SIL_TEST_CTRL | SIL 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드 |
|  |  | Network Infra |
| ETH_SWITCH | Ethernet 백본 스위칭 및 도메인 게이트웨이 전달 허브 | Ethernet 프레임 분배 |
| CHASSIS_GW | Chassis CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| INFOTAINMENT_GW | Infotainment CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| BODY_GW | 중재 결과 Ethernet 수신 후 Body CAN 출력 메시지 생성 | ETH->CAN 변환 |
| IVI_GW | 중재 결과 Ethernet 수신 후 Cluster CAN 출력 메시지 생성 | ETH->CAN 변환 |
|  |  | Body |
| BCM_AMBIENT_CTRL | 중재 결과 기반 앰비언트 경고 패턴 적용 | 색상/패턴 반영 |
|  |  | Infotainment |
| NAV_CONTEXT_MGR | 내비게이션 구간/방향/거리 기반 컨텍스트 갱신 | 구간 상태 전환 |
| CLU_HMI_CTRL | 운전자 경고 문구 및 안내 정보 표시 | 원인/방향/유형 표시 |
|  |  | Actual Device |
| Ambient Lights | 실제 앰비언트 장치가 제어 신호를 수신해 점등/패턴 동작 수행 | Ambient_Control 반영 |
| Cluster Display | 실제 클러스터 장치가 경고 문구/상태를 표시 | Cluster_WarningText 반영 |
| Navigation Panel | 사용자 입력(구간/방향/거리) 제공 및 시각화 | Panel UI 입력 소스 |

---

## 기능 정의 상세 표 (추적성/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 입력 (Input) | 처리 (Processing) | 출력 (Output) | 실제값 정의 |
|---|---|---|---|---|---|---|
| Func_007 | Req_007 | NAV_CONTEXT_MGR | gRoadZone, gNavDirection, gZoneDistance | 구간 상태 판별 및 전환 컨텍스트 갱신 | BaseZoneContext | 입력: gRoadZone, gNavDirection, gZoneDistance |
| Func_001~004,006,010~012 | Req_001~004,006,010~012 | ADAS_WARN_CTRL | gVehicleSpeed, SteeringInput, BaseZoneContext | 스쿨존 과속/고속 무조향 조건 판정, 경고 트리거 생성, 디바운스 | WarningState, ZoneWarningEvent | 입력: gVehicleSpeed, SteeringInput, BaseZoneContext |
| Func_013, Func_014, Func_015, Func_016 | Req_013, Req_014, Req_015, Req_016 | BCM_AMBIENT_CTRL | gNavDirection, gRoadZone, SelectedAlertContext | 유도구간 전환/방향 분기/구간 전환 완화/종료 복귀 처리 | Ambient_Control | 입력: gNavDirection, gRoadZone, SelectedAlertContext |
| Func_017 | Req_017 | EMS_POLICE_TX | Police_Active, Police_ETA, Police_Direction | 경찰 긴급 알림 패킷 생성 및 송신 관리 | EmergencyAlert(Police) | 출력: ETH_EmergencyAlert(UDP) |
| Func_018 | Req_018 | EMS_AMB_TX | Ambulance_Active, Ambulance_ETA, Ambulance_Direction | 구급 긴급 알림 패킷 생성 및 송신 관리 | EmergencyAlert(Ambulance) | 출력: ETH_EmergencyAlert(UDP) |
| Func_023,024 | Req_023,024 | EMS_ALERT_RX | EmergencyAlert(Police/Ambulance) | 수신/해제 상태 관리, 1000ms 타임아웃 처리 | EmergencyContextState | 입력: ETH_EmergencyAlert(UDP) |
| Func_022,025~032 | Req_022,025~032 | WARN_ARB_MGR | EmergencyContextState, WarningState, BaseZoneContext | 우선순위 중재 수행 | SelectedAlertContext | 입력: EmergencyContextState, WarningState, BaseZoneContext |
| Func_008,009,033~039 | Req_008,009,033~039 | BCM_AMBIENT_CTRL | SelectedAlertContext | 경고 등급별 색상/패턴 적용, 전환 완화, 복원 | Ambient_Control | 출력: Ambient_Control |
| Func_005,019~021,026,040 | Req_005,019~021,026,040 | CLU_HMI_CTRL | SelectedAlertContext | 경고 문구/종류/방향/양보 메시지 표시 | Cluster_WarningText | 출력: Cluster_WarningText |
| Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | SIL_TEST_CTRL | TestScenario | 시나리오 실행, CAN+ETH 검증, 판정 기록 | TestResult, TraceRecord | 출력: TestResult |

## 2-1. Req-Func 1:1 감사 매핑 표

| Req ID | Func ID | 실제 노드명 | 기능명 |
|---|---|---|---|
| Req_001 | Func_001 | ADAS_WARN_CTRL | 주행시 경고엔진 활성 |
| Req_002 | Func_002 | ADAS_WARN_CTRL | 비주행 경고 억제 |
| Req_003 | Func_003 | ADAS_WARN_CTRL | 경고 시작 트리거 |
| Req_004 | Func_004 | ADAS_WARN_CTRL | 경고 종료 트리거 |
| Req_005 | Func_005 | CLU_HMI_CTRL | 경고 원인 전달 |
| Req_006 | Func_006 | ADAS_WARN_CTRL | 반복 경고 디바운스 |
| Req_007 | Func_007 | NAV_CONTEXT_MGR | 구간값 변경 반영 |
| Req_008 | Func_008 | BCM_AMBIENT_CTRL | 일반구간 정책 적용 |
| Req_009 | Func_009 | BCM_AMBIENT_CTRL | 스쿨존 강화 경고 |
| Req_010 | Func_010 | ADAS_WARN_CTRL | 스쿨존 과속 경고 |
| Req_011 | Func_011 | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 |
| Req_012 | Func_012 | ADAS_WARN_CTRL | 무조향 경고 해제 |
| Req_013 | Func_013 | BCM_AMBIENT_CTRL | 유도구간 진입 전환 |
| Req_014 | Func_014 | BCM_AMBIENT_CTRL | 좌우 방향 구분 표시 |
| Req_015 | Func_015 | BCM_AMBIENT_CTRL | 구간 전환 완화 |
| Req_016 | Func_016 | BCM_AMBIENT_CTRL | 구간경고 종료 복귀 |
| Req_017 | Func_017 | EMS_POLICE_TX | 경찰 접근 경고 송신 |
| Req_018 | Func_018 | EMS_AMB_TX | 구급 접근 경고 송신 |
| Req_019 | Func_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 |
| Req_020 | Func_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 |
| Req_021 | Func_021 | CLU_HMI_CTRL | 양보 유도 메시지 |
| Req_022 | Func_022 | WARN_ARB_MGR | 긴급경고 우선 출력 |
| Req_023 | Func_023 | EMS_ALERT_RX | 종료 신호 처리 |
| Req_024 | Func_024 | EMS_ALERT_RX | 타임아웃 보호해제 |
| Req_025 | Func_025 | WARN_ARB_MGR | 다중긴급 단일선택 |
| Req_026 | Func_026 | CLU_HMI_CTRL | 중복 팝업 억제 |
| Req_027 | Func_027 | WARN_ARB_MGR | 충돌중재 개시 |
| Req_028 | Func_028 | WARN_ARB_MGR | 긴급>구간 우선 적용 |
| Req_029 | Func_029 | WARN_ARB_MGR | 구급>경찰 우선 적용 |
| Req_030 | Func_030 | WARN_ARB_MGR | ETA 우선 적용 |
| Req_031 | Func_031 | WARN_ARB_MGR | SourceID 동률판정 |
| Req_032 | Func_032 | WARN_ARB_MGR | 중재결과 결정론 보장 |
| Req_033 | Func_033 | BCM_AMBIENT_CTRL | 종료후 이전상태 복원 |
| Req_034 | Func_034 | BCM_AMBIENT_CTRL | 전환 깜빡임 완화 |
| Req_035 | Func_035 | BCM_AMBIENT_CTRL | 긴급 색상 정책 |
| Req_036 | Func_036 | BCM_AMBIENT_CTRL | 긴급 패턴 정책 |
| Req_037 | Func_037 | BCM_AMBIENT_CTRL | 스쿨존 패턴 정책 |
| Req_038 | Func_038 | BCM_AMBIENT_CTRL | 고속도로 패턴 정책 |
| Req_039 | Func_039 | BCM_AMBIENT_CTRL | 유도선 패턴 정책 |
| Req_040 | Func_040 | CLU_HMI_CTRL | 문구 길이 제한 |
| Req_041 | Func_041 | SIL_TEST_CTRL | SIL 시나리오 실행 |
| Req_042 | Func_042 | SIL_TEST_CTRL | CAN+ETH 동시 검증 |
| Req_043 | Func_043 | SIL_TEST_CTRL | 판정 결과 산출 |

---

## 3. 핵심 시나리오 동작 체인

| 시나리오 | 노드 동작 체인 | 연결 Func ID |
|---|---|---|
| 스쿨존 과속 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_007, Func_010, Func_027, Func_037, Func_040 |
| 고속도로 무조향 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_011, Func_012, Func_027, Func_038, Func_040 |
| 유도구간 방향 안내 | NAV_CONTEXT_MGR -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_013, Func_014, Func_039, Func_040 |
| 경찰 긴급차량 접근 | EMS_POLICE_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_017, Func_023, Func_022, Func_035, Func_019 |
| 구급 긴급차량 접근 | EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_018, Func_023, Func_022, Func_035, Func_019 |
| 경찰+구급 동시 충돌 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR(우선순위/동률처리) -> 출력 노드 | Func_025~Func_031 |
| 긴급 해제 후 복귀 | EMS_ALERT_RX(해제/타임아웃) -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL/CLU_HMI_CTRL | Func_024, Func_033, Func_034 |

---

## 3-1. 네트워크 전달 체인 (옵션1 고정)

| 시나리오 | 네트워크 전달 체인 |
|---|---|
| Chassis 상태 입력 | SIL_TEST_CTRL -> Chassis CAN -> CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| Nav 구간 입력 | SIL_TEST_CTRL -> Infotainment CAN -> INFOTAINMENT_GW -> ETH_SWITCH -> NAV_CONTEXT_MGR/WARN_ARB_MGR |
| 긴급 신호 처리 | EMS_POLICE_TX/EMS_AMB_TX -> ETH_SWITCH -> EMS_ALERT_RX -> WARN_ARB_MGR |
| Ambient 출력 | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW -> Body CAN -> BCM_AMBIENT_CTRL |
| Cluster 출력 | WARN_ARB_MGR -> ETH_SWITCH -> IVI_GW -> Infotainment CAN -> CLU_HMI_CTRL |

---

## 4. 0302 연계 체크포인트

- 각 노드의 출력은 `0302_NWflowDef.md`에서 반드시 Flow ID로 정의한다.
- 최소 연계 규칙:
- `SelectedAlertContext` -> `Ambient_Control` 송신 Flow 존재
- `SelectedAlertContext` -> `Cluster_Warning` 송신 Flow 존재
- `EmergencyAlert` 송신/수신/해제 Flow 존재
- 타임아웃(1000ms) 해제 Flow 존재

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.0 | 2026-02-25 | 프로젝트 최신 스코프 기준 전면 재작성. 노드별 Input-Processing-Output 구조, Func/Req 연결, 핵심 시나리오 체인, 0302 연계 체크포인트 추가 |
| 3.0 | 2026-02-25 | 상단 공식 표준 양식 반영, 하단 상세 추적 표 분리 |
| 3.1 | 2026-02-25 | 상단 표를 이미지 표준 구조로 재정렬, 도메인 묶음(Powertrain/Chassis/Body/Infotainment/Actual Device) 반영 |
| 3.2 | 2026-02-25 | 상단 헤더를 표준(기능 상세)로 정렬, Actual Device를 실제 장치 기준으로 수정, Func_013~016 추적 보완 |
| 3.3 | 2026-02-25 | 옵션1 아키텍처 기준으로 Network Infra 노드(ETH_SWITCH/도메인 GW)와 네트워크 전달 체인 섹션 추가 |
| 3.4 | 2026-02-25 | Req_001~Req_043 / Func_001~Func_043 1:1 감사용 매핑 표(개별 행) 추가 |
| 3.5 | 2026-02-26 | Cluster 출력 전달체인을 Infotainment CAN 경로로 정합화(IVI_GW -> CLU_HMI_CTRL) |
