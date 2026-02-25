# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 — 소프트웨어 단위 설계 및 구현
**ASPICE Reference**: SWE.3 (BP1: 상세 설계), SWE.6 (BP1: 구현)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 하단 — SWE.3/6 SW 구현 | `05_Unit_Test.md` (SWE.4) | `0304_System_Variables.md` | `05_Unit_Test.md` |

**구현 파일**: `canoe/nodes/` (CAPL) · `canoe/test_modules/` (Test CAPL) · **DBC**: `canoe/databases/project.dbc`

---

## 1. CAPL 노드 구성

| 노드 파일 | 담당 ECU | 위치 |
|----------|---------|------|
| `Vehicle_ECU.can` | 차속/가속도/제동 신호 생성 및 CAN-LS 전송 | `canoe/nodes/Vehicle_ECU.can` |
| `MDPS_ECU.can` | 조향 입력/급차선변경 신호 생성 및 CAN-LS 전송 | `canoe/nodes/MDPS_ECU.can` |
| `LDW_ECU.can` | 차선이탈 신호 생성 및 CAN-LS 전송 | `canoe/nodes/LDW_ECU.can` |
| `WDM_ECU.can` | Rule-Based 판단 → 경고 단계 설정 → 출력 ECU 제어 | `canoe/nodes/WDM_ECU.can` |
| `CGW.can` | CAN-LS→CAN-HS 라우팅, DoIP 처리, Bus Off 감지 | `canoe/nodes/CGW.can` |
| `Cluster_ECU.can` | 경고등 활성화/소등 | `canoe/nodes/Cluster_ECU.can` |
| `Ambient_ECU.can` | 앰비언트 패턴 제어 | `canoe/nodes/Ambient_ECU.can` |
| `Sound_ECU.can` | 단계별 경고음 출력 | `canoe/nodes/Sound_ECU.can` |
| `IVI_ECU.can` | OTA 팝업 / 진행률 표시 | `canoe/nodes/IVI_ECU.can` |
| `Door_ECU.can` | 3초 도어 잠금 + 미러 LED | `canoe/nodes/Door_ECU.can` |
| `OTA_Server.can` | OTA UDS 세션 — 펌웨어 전송, CRC 검증, Rollback | `canoe/nodes/OTA_Server.can` |

---

## 2. Vehicle_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tVehicleTx` | 100ms 주기 CAN-LS 0x100 Vehicle_Speed 메시지 전송 | `Vehicle::vehicleSpeed`, `Vehicle::accelValue`, `Vehicle::brakeValue` | In_Test_01, In_Test_02 |
| `void sendVehicleSpeed()` | gVehicleSpeed/gAccelValue/gBrakeValue/OverspeedFlag 조립 후 CAN-LS 전송 | Vehicle_Speed 0x100 (4 bytes) | In_Test_01 |
| `on sysvar Vehicle::vehicleSpeed` | Panel TrackBar 변경 시 즉시 CAN-LS 메시지에 반영. gRoadZone 기준 대비 OverspeedFlag 자동 계산. | `Vehicle::vehicleSpeed`, `WDM::roadZone` | In_Test_01 |
| `on sysvar Vehicle::accelValue` | 급가속 주입 시 즉시 반영. >3.5 m/s² 시 WDM_ECU 이벤트 발생. | `Vehicle::accelValue` | In_Test_02 |

---

## 3. MDPS_ECU.can / LDW_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tMDPSTx` | 100ms 주기 CAN-LS 0x110 Steering_Status 전송 | `MDPS::steeringInput`, `LDW::laneChangeAlert` | In_Test_03, In_Test_06 |
| `on sysvar MDPS::steeringInput` | Panel Button 변경 시 즉시 전송. 1 감지 시 WDM_ECU 경고 해제. | `MDPS::steeringInput` | In_Test_06 |
| `on timer tLDWTx` | 100ms 주기 CAN-LS 0x120 LDW_Status 전송 | `LDW::laneDeparture` | In_Test_03 |
| `on sysvar LDW::laneDeparture` | Panel Button 변경 시 즉시 전송. 1 감지 시 WDM_ECU B그룹 감지. | `LDW::laneDeparture` | In_Test_03 |

---

## 4. WDM_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC/sysvar) | 검증 |
|-----------|------|----------------|------|
| `on message Vehicle_Speed` | CAN-LS 0x100 수신 → 과속/급가속/급제동 이벤트 판단 | `Vehicle::vehicleSpeed`, `WDM::accelCount` | In_Test_01, In_Test_02 |
| `on message Steering_Status` | CAN-LS 0x110 수신 → 급차선변경/핸들입력 판단. SteeringInput=1 시 경고 해제. | `MDPS::steeringInput`, `LDW::laneChangeAlert` | In_Test_03, In_Test_06 |
| `on message LDW_Status` | CAN-LS 0x120 수신 → 차선이탈 감지 | `LDW::laneDeparture` | In_Test_03 |
| `void evaluateWarning()` | Rule-Based 판단. A단독→1단계, B단독→1단계, A+B→2단계, A+B+OTA조건→3단계. gWarningLevel 설정. | `WDM::warningLevel`, `WDM::warningType` | In_Test_01~04 |
| `void sendWarning()` | gWarningLevel 기반 WDM_Warning(0x200) CAN-HS 전송. Ambient/Sound/IVI/Door 제어 명령 포함. | 0x200/0x220/0x230/0x240/0x250 | In_Test_01~04 |
| `on sysvar Driver::gazeActive` | GazeActive 0→1 전환 감지 → 경고 해제(gWarningLevel=0) | `Driver::gazeActive`, `WDM::warningLevel` | In_Test_05 |
| `on timer tAccelTimer` | 10분 타이머. 만료 시 gAccelCount = 0 초기화. | `WDM::accelCount`, `WDM::accelTimerActive` | In_Test_02 |
| `on timer tSteerTimer` | 고속도로 핸들 미입력 타이머. 10초 초과 시 진동 경고 발령. | `WDM::steerTimer` | In_Test_08 |
| `void applyRoadZone()` | gRoadZone 변경 시 과속 임계값 및 앰비언트 동작 즉시 적용. | `WDM::roadZone` | In_Test_07~09 |

---

## 5. CGW.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message CAN1.Vehicle_Speed` | CAN-LS(0x100) 수신 → CAN-HS로 WDM_ECU에 라우팅 (지연 ≤5ms) | `Vehicle_Speed` | In_Test_13 |
| `on message CAN1.Steering_Status` | CAN-LS(0x110) 수신 → CAN-HS 라우팅 | `Steering_Status` | In_Test_13 |
| `on message DoIP_RoutingActivation` | DoIP 0xE001 수신 → 경로 활성화 응답 | `CGW::busOffDetected` | In_Test_11 |
| `void forwardUDS()` | UDS 메시지(0x7DF) CAN-LS ↔ CAN-HS 포워딩 | `UDS::currentSession` | In_Test_10 |
| `on message CGW_BusOff` | Bus Off 감지 → OTA 세션 중단 + DTC U0300 저장 | `CGW::busOffDetected` | In_Test_13 |

---

## 6. Ambient_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message Ambient_Control` | CAN-HS(0x220) 수신 → AmbientMode별 패턴 실행 | `Ambient::ambientMode`, `Ambient::ambientColor` | In_Test_07~09 |
| `void runSchoolZoneAlert()` | AmbientMode=1: RED 빠른 점멸 (200ms 주기). gRoadZone=1 과속 시. | `Ambient::ambientPattern` | In_Test_07 |
| `void runHighwayWarning()` | AmbientMode=2: ORANGE 파동 (1초 주기). gRoadZone=2 핸들 미입력 10초. | `Ambient::ambientPattern` | In_Test_08 |
| `void runICDirectional()` | AmbientMode=4: 좌→우 흐름 애니메이션. gRoadZone=3 IC출구 근접. | `Ambient::ambientPattern` | In_Test_09 |

---

## 7. OTA_Server.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `void activateDoIP()` | DoIP Routing Activation(0xE001) 전송 | `CGW::busOffDetected` | In_Test_11 |
| `void sendUDS_10_02()` | UDS 0x10 0x02 Programming Session 진입 | `UDS::currentSession` | In_Test_10 |
| `void sendUDS_27()` | UDS 0x27 Security Access (Seed 요청 → Key 응답) | `UDS::lastServiceID` | In_Test_10 |
| `void sendUDS_34()` | UDS 0x34 다운로드 요청 (메모리 주소/크기 포함) | `OTA::otaInProgress` | In_Test_10 |
| `void sendUDS_36(byte block)` | UDS 0x36 4KB 블록 순차 전송 | `OTA::blockSequenceCounter`, `OTA::otaProgress` | In_Test_10 |
| `void sendUDS_37()` | UDS 0x37 전송 완료 + CRC-32 검증 요청 | `OTA::crcMatch` | In_Test_10 |
| `void triggerRollback()` | CRC 불일치 또는 통신 단절 시 Rollback 실행 | `OTA::rollbackTriggered` | In_Test_12 |

---

## 8. 테스트 모듈 구성

| 테스트 모듈 폴더 | 내용 | 대응 테스트 |
|--------------|------|-----------|
| `TC_A_SpeedInput/` | 과속/급가속/급제동 감지 → WDM_ECU 1단계 경고 자동화 | In_Test_01, 02 |
| `TC_B_DirectionInput/` | 차선이탈/급차선변경 감지 → WDM_ECU 1단계 경고 | In_Test_03 |
| `TC_W_Warning/` | 2단계(A+B) / 경고 해제(응시/핸들) 검증 | In_Test_04, 05, 06 |
| `TC_Z_ZoneAmbient/` | gRoadZone 1~3 앰비언트 동작 검증 | In_Test_07, 08, 09 |
| `TC_O_OTA/` | OTA UDS 세션 / Rollback / Bus Off 안전 중단 | In_Test_10, 11, 12, 13 |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 (Scene.1~17) | Scene.1~17 |

[^1]: **ASIL B E2E Protection Note**: 본 프로젝트는 CANoe SIL 환경 시뮬레이션을 위해 AliveCounter(4bit)와 Checksum(2bit)을 간이 구현하였습니다. 실제 양산용 ASIL B 타겟 시스템에서는 ISO 26262 Part 6 및 ISO 11898 표준을 준수하는 E2E Profile 1 또는 2 기반의 전체 CRC/Counter 보호 메커니즘을 적용해야 합니다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — 구현 명세, CAPL 주요 로직 정의 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
