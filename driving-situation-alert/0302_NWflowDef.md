# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: PROJ-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 2.8
**Date**: 2026-02-26
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0302_NWflowDef.md` | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

---

## 작성 원칙

- 상단 표는 공식 표준 양식(`Channel/ID hex/Symbolic Name/Byte/Function/Bit/signal/노드 TxRx`) 구조를 유지한다.
- 상단 표의 `signal name`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 옵션1 아키텍처를 고정한다: `중앙 경고코어 + Ethernet 백본(ETH_SWITCH) + 도메인 게이트웨이 + 도메인 CAN`.
- 상세 추적 정보(`Flow/Func/Req/주기/활성/해제`)는 하단 표에 분리한다.
- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)만 사용한다.
- OTA/UDS/DoIP 관련 플로우는 본 문서 범위에서 제외한다.

---

## 네트워크 플로우 표 (공식 표준 양식)

| Channel | ID hex | Symbolic Name(message name) | Byte no. | Function | Bit no. | signal name | SIL_TEST_CTRL | CHASSIS_GW | INFOTAINMENT_GW | ETH_SWITCH | ADAS_WARN_CTRL | NAV_CONTEXT_MGR | EMS_POLICE_TX | EMS_AMB_TX | EMS_ALERT_RX | WARN_ARB_MGR | BODY_GW | IVI_GW | BCM_AMBIENT_CTRL | CLU_HMI_CTRL | [비고] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chassis CAN | 0x100 | frmVehicleStateCanMsg | 0 | Vehicle State Check | 0 | vehicleSpeed | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  | CAN 입력, 100ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | driveState | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x101 | frmSteeringCanMsg | 0 | Steering Input Check | 0 | SteeringInput | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  | CAN 입력, 100ms |
| Infotainment CAN | 0x110 | frmNavContextCanMsg | 0 | Zone Context Check | 0 | roadZone | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN 입력, 100ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 2 | navDirection | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | zoneDistance | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0x510 | ethVehicleStateMsg | 0 | Gateway Normalized Vehicle State | 0 | vehicleSpeed |  | Tx |  | Rx | Rx |  |  |  |  |  |  |  |  |  | UDP, 100ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | driveState |  | Tx |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0x511 | ethSteeringMsg | 0 | Gateway Normalized Steering | 0 | SteeringInput |  | Tx |  | Rx | Rx |  |  |  |  |  |  |  |  |  | UDP, 100ms |
| Ethernet | 0x512 | ethNavContextMsg | 0 | Gateway Normalized Nav Context | 0 | roadZone |  |  | Tx | Rx |  | Rx |  |  |  | Rx |  |  |  |  | UDP, 100ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 2 | navDirection |  |  | Tx | Rx |  | Rx |  |  |  | Rx |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | zoneDistance |  |  | Tx | Rx |  | Rx |  |  |  | Rx |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0xE100 | ETH_EmergencyAlert | 0 | Emergency Alert Tx/Rx | 0 | EmergencyType |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  | UDP, 100ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 2 | EmergencyDirection |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | ETA |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 |  | 0 | SourceID |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 |  | 0 | AlertState(Active/Clear) |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |
| Ethernet | 0xE200 | ethSelectedAlertMsg | 0 | Arbitration Result Distribution | 0 | AlertLevel |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  | UDP, 50ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 3 | AlertType |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 |  | 0 | TimeoutClear |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  |  |
| Body CAN | 0x210 | frmAmbientControlMsg | 0 | Ambient Pattern Control | 0 | AmbientMode |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  | CAN 출력, 50ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 3 | AmbientColor |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 |  | 6 | AmbientPattern |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x220 | frmClusterWarningMsg | 0 | Cluster Warning Display | 0 | WarningTextCode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx | CAN 출력, 50ms |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Test CAN | 0x230 | frmTestResultMsg | 0 | Scenario Result Report | 0 | ScenarioResult | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  | Event |
|  |  |  |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

> 참고: 본 문서는 샘플 표준(`reference/standards/Project Result_Sample/0302.md`) 형식에 맞춰 Bit no.를 `0/1/2/...` 개별 행으로 전개했다. 실문서 이관 시에도 동일 형식을 유지한다.

---

## 하단 보강표 (감사/추적 전용)

- 상단 공식 표준 양식은 변경하지 않고 유지한다.
- 아래 표들은 추적성/감사 해석 명확화를 위한 하단 보강 정보다.

---

## 플로우 상세 추적 표 (Flow/Func/Req)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | Tx Node | Rx Node | Channel | Period | Active Condition | Clear Condition |
|---|---|---|---|---|---|---|---|---|---|---|
| Flow_001 | Comm_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x100), ethVehicleStateMsg(0x510) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 | 경고 조건 해제 또는 입력 무효 |
| Flow_002 | Comm_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x101), ethSteeringMsg(0x511) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 | 조향 복귀 또는 경고 해제 |
| Flow_003 | Comm_003 | Func_007 | Req_007 | frmNavContextCanMsg(0x110), ethNavContextMsg(0x512) | SIL_TEST_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CONTEXT_MGR, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리 입력 갱신 | 다음 컨텍스트 수신 시 갱신 |
| Flow_004 | Comm_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | Police_Active=1 | AlertState=Clear 또는 송신 중지 |
| Flow_005 | Comm_005 | Func_018 | Req_018 | ETH_EmergencyAlert(0xE100) | EMS_AMB_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | Ambulance_Active=1 | AlertState=Clear 또는 송신 중지 |
| Flow_006 | Comm_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT_RX, WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | EmergencyAlert 수신 또는 Zone 충돌 발생 | Clear 수신 또는 1000ms 무갱신 |
| Flow_007 | Comm_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_036, Req_037, Req_038, Req_039 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210) | WARN_ARB_MGR, BODY_GW | BODY_GW, BCM_AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | SelectedAlertContext 수신 | TimeoutClear=1 또는 기본 상태 복귀 |
| Flow_008 | Comm_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x220) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | SelectedAlertContext 수신 | Alert 해제 또는 문구 만료 |
| Flow_009 | Comm_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x230) | SIL_TEST_CTRL | SIL_TEST_CTRL(Log/Panel) | CAN | Event | 시나리오 실행 시작 | 판정 결과 기록 완료 |

---

## Flow_006 메시지 단계 분해 (감사용 명확화)

| 단계 | 상위 Flow ID | Message(ID) | Tx Node | Rx Node | 목적 |
|---|---|---|---|---|---|
| Ingress | Flow_006 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX, WARN_ARB_MGR | 긴급 이벤트 수신/정규화 |
| Egress | Flow_006 | ethSelectedAlertMsg(0xE200) | WARN_ARB_MGR | BODY_GW, IVI_GW | 중재 결과 배포 |

- 주의: `Flow_006`은 긴급 수신(E100)과 중재 결과 배포(E200)를 하나의 논리 플로우로 묶은 항목이며, 감사 시에는 위 단계 표를 기준으로 해석한다.

### 표준명-별칭(g*) 매핑 (문서/코드 정합용)

| 표준 signal name(0302/0304) | 코드/런타임 별칭 |
|---|---|
| vehicleSpeed | gVehicleSpeed |
| driveState | gDriveState |
| roadZone | gRoadZone |
| navDirection | gNavDirection |
| zoneDistance | gZoneDistance |

---

## 0303 연계 체크포인트

- 각 `Flow ID`는 `0303_Communication_Specification.md`의 `Comm ID`와 1:1로 연결한다.
- 필수 연결:
- `SelectedAlertContext -> Ambient_Control` 송신 Flow 존재
- `SelectedAlertContext -> Cluster_Warning` 송신 Flow 존재
- `EmergencyAlert` 송신/수신/해제 Flow 존재
- 타임아웃(1000ms) 해제 Flow 존재
- `ETH_SWITCH` 경유 신호가 `BODY_GW/IVI_GW`에서 CAN으로 분배되는 Flow 존재

---

## 예외/장애 처리 규칙

| 장애 시나리오 | 감지 지점 | 처리 규칙 | 추적 링크 |
|---|---|---|---|
| CHASSIS_GW CAN->ETH 변환 실패 | CHASSIS_GW Tx watchdog | 마지막 정상값 1주기 유지 후 `WarningState` 강등, Fault 이벤트 기록 | Flow_001, Flow_002 / Comm_001, Comm_002 / Req_001, Req_011 |
| INFOTAINMENT_GW CAN->ETH 변환 실패 | INFOTAINMENT_GW Tx watchdog | `BaseZoneContext`를 일반구간으로 복귀하고 유도 경고 해제 | Flow_003 / Comm_003 / Req_007, Req_016 |
| EmergencyAlert 유실(1000ms 초과) | EMS_ALERT_RX timeout monitor | `TimeoutClear=1` 생성 후 중재 결과 해제 전파 | Flow_006 / Comm_006 / Req_024 |
| BODY_GW CAN 송신 실패 | BODY_GW CAN Tx ack monitor | Ambient 출력을 안전 기본패턴으로 강등하고 재시도 3회 수행 | Flow_007 / Comm_007 / Req_033, Req_034 |
| IVI_GW CAN 송신 실패 | IVI_GW CAN Tx ack monitor | Cluster 경고코드를 최소 메시지(양보 안내)로 축소해 1회 재송신 | Flow_008 / Comm_008 / Req_040 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 공식 표준 양식 기반으로 전면 재작성. CAN+Ethernet 범위 고정, OTA/UDS/DoIP 항목 제거, Flow/Func/Req 추적 표 추가 |
| 2.1 | 2026-02-25 | 공식 0302 표준 샘플 구조에 맞춰 상단 표를 재정렬하고, 하단 추적 표에 Comm 연계/메시지 ID/활성·해제 조건을 보강 |
| 2.2 | 2026-02-25 | 실문서 이관 시 Bit no. 행 단위(0/1/2...)로 확장 작성해야 함을 상단 공식표 하단 주석으로 추가 |
| 2.3 | 2026-02-25 | 옵션1 아키텍처(ETH_SWITCH + 도메인 GW + 도메인 CAN)로 네트워크 플로우 전면 통일 |
| 2.4 | 2026-02-25 | 상단 공식표 Bit no.를 개별 비트 행(0/1/2/...)으로 전개하고, GW/ETH/CAN 장애 처리 규칙 섹션 추가 |
| 2.5 | 2026-02-26 | Cluster 경고 메시지(0x220) 채널을 Infotainment CAN으로 정합화(IVI_GW -> CLU_HMI_CTRL 경로 기준) |
| 2.6 | 2026-02-26 | Flow_006 단계 분해 표(E100 Ingress / E200 Egress) 추가로 감사 해석 모호성 제거 |
| 2.7 | 2026-02-26 | 상단 공식표 비변경 원칙을 명시하고 하단 보강표 구역(감사/추적 전용)으로 분리 |
| 2.8 | 2026-02-26 | 상단 signal name을 0304 표준명(vehicleSpeed 등)으로 통일하고, g* 별칭은 하단 매핑표로 분리 |
