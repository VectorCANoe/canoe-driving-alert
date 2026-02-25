# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA  
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)  
**ASPICE Reference**: SYS.3 (System Architectural Design)  
**Version**: 2.0  
**Date**: 2026-02-25  
**Status**: Draft  
**Project Title**: 주행상황 연동 실시간 경고 시스템  
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

## 1. 목적

- 본 문서는 `03_Function_definition.md`의 `Func_001~Func_043`을 노드 내부 동작 관점으로 분해한다.
- 각 노드의 입력-처리-출력을 명확히 정의해 `0302`의 Tx/Rx 흐름 설계로 연결한다.
- 요구사항(What) 문장을 반복하지 않고, 시스템 동작 로직(How)만 기술한다.

---

## 2. 노드별 기능 분해

| 노드 | 입력 (Input) | 처리 (Processing) | 출력 (Output) | 연결 Func ID | 연결 Req ID | 비고 |
|---|---|---|---|---|---|---|
| NAV_CONTEXT_MGR | `gRoadZone`, `gNavDirection`, `gZoneDistance` | 구간 상태(일반/스쿨존/고속/유도구간) 판별, 구간 전환 시 현재 컨텍스트 갱신 | BaseZoneContext | Func_007, Func_013, Func_014, Func_015, Func_016 | Req_007, Req_013~Req_016 | 내비게이션 구간 인식의 기준 노드 |
| ADAS_WARN_CTRL | 차량 속도/조향 입력, BaseZoneContext | 스쿨존 과속/고속 무조향 경고 조건 판정, 경고 시작/해제 트리거 생성, 반복 경고 디바운스 처리 | WarningState, ZoneWarningEvent | Func_001~Func_004, Func_006, Func_010~Func_012 | Req_001~Req_004, Req_006, Req_010~Req_012 | Zone 기반 경고 엔진 |
| EMS_POLICE_TX | `Police_Active`, `Police_ETA`, `Police_Direction` | 경찰 긴급 알림 패킷 생성, 활성/해제 상태 관리, 주기 송신 이벤트 발생 | EmergencyAlert(Police) | Func_017 | Req_017 | Ethernet(UDP) 시뮬레이션 송신 |
| EMS_AMB_TX | `Ambulance_Active`, `Ambulance_ETA`, `Ambulance_Direction` | 구급 긴급 알림 패킷 생성, 활성/해제 상태 관리, 주기 송신 이벤트 발생 | EmergencyAlert(Ambulance) | Func_018 | Req_018 | Ethernet(UDP) 시뮬레이션 송신 |
| EMS_ALERT_RX | EmergencyAlert(Police/Ambulance) | 긴급 알림 수신/해제 상태 관리, 무갱신 타임아웃(1000ms) 처리 | EmergencyContextState | Func_023, Func_024 | Req_023, Req_024 | 수신 측 긴급 상태 저장소 |
| WARN_ARB_MGR | EmergencyContextState, WarningState, BaseZoneContext | 우선순위 중재 수행: Emergency > Zone, Ambulance > Police, 동률 시 ETA 우선, ETA 동률 시 SourceID 오름차순 | SelectedAlertContext | Func_022, Func_025~Func_032 | Req_022, Req_025~Req_032 | 핵심 충돌해결 노드 |
| BCM_AMBIENT_CTRL | SelectedAlertContext | 경고 등급별 색상/패턴 적용, 중재 전환 시 깜빡임 완화, 긴급 종료 후 직전 구간 상태 복원 | Ambient_Control | Func_008, Func_009, Func_033~Func_039 | Req_008, Req_009, Req_033~Req_039 | 시각 출력(앰비언트) |
| CLU_HMI_CTRL | SelectedAlertContext | 경고 원인 문구, 긴급차량 종류/방향, 양보 메시지 표시, 중복 팝업 억제, 문구 형식 고정 | Cluster_WarningText | Func_005, Func_019~Func_021, Func_026, Func_040 | Req_005, Req_019~Req_021, Req_026, Req_040 | 클러스터/HMI 출력 |
| SIL_TEST_CTRL | 테스트 시나리오 입력, 판정 기준 | CANoe SIL 환경에서 시나리오 실행, CAN+Ethernet 동시 검증, Pass/Fail 판정 기록 | TestResult, TraceRecord | Func_041~Func_043 | Req_041~Req_043 | 검증 자동화 제어 |

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
