# SW 구현 명세 (Software Implementation Specification)

**Document ID**: SAMPLE-04-SI
**ISO 26262 Reference**: Part 6, Cl.8
**ASPICE Reference**: SWE.3 (BP1: 상세 설계), SWE.6 (BP1: 구현)
**Version**: 1.1
**Date**: 2026-02-19
**Status**: Released

> **V-Model 위치**: 좌측 하단 — 소프트웨어 상세 설계 및 구현 단계 (SWE.3 / SWE.6)
> **대응 문서**: `05_Unit_Test.md` (SWE.4 단위 테스트로 검증)
> **ISO 26262**: Part 6, Clause 8 — 소프트웨어 단위 설계 및 구현
> **ASPICE**: SWE.3 (BP1: 소프트웨어 상세 설계), SWE.6 (BP1: 소프트웨어 구현)
> **상위 연결**: `0304_System_Variables.md` → 본 문서 → `05_Unit_Test.md`
> **구현 파일 위치**: `canoe/nodes/` (CAPL), `canoe/test_modules/` (Test CAPL)
> **DBC 참조**: `canoe/databases/vehicle_system.dbc`

---

## 1. CAPL 노드 구성

| 노드 파일 | 담당 ECU | 위치 |
|----------|---------|------|
| `WindowMotorECU.can` | WindowMotorECU — LIN Slave 0x21, Motor_Current/Status/Direction 보고 | `canoe/nodes/WindowMotorECU.can` |
| `DoorModule.can` | DoorModule FL/FR/RL/RR — LIN Slave 0x22~0x25, Door_Position/Lock_Status/Window_Position 보고 | `canoe/nodes/DoorModule.can` |
| `BCM.can` | BCM — LIN Master, Motor_Current 수신 → 과전류 판단, DTC 생성, FaultStatus CAN-LS 전송 | `canoe/nodes/BCM.can` |
| `Gateway.can` | Central Gateway — CAN 라우팅, DoIP 처리 | `canoe/nodes/Gateway.can` |
| `Tester.can` | CANoe Tester — UDS 세션/DTC 조회/클리어 | `canoe/nodes/Tester.can` |
| `OTA_Server.can` | OTA Server — 펌웨어 전송, CRC 검증 | `canoe/nodes/OTA_Server.can` |
| `Cluster.can` | Cluster — 경고등 활성화/소등 | `canoe/nodes/Cluster.can` |

---

## 2. WindowMotorECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tLIN_Motor` | 10ms 주기 LIN ID 0x21 프레임 전송 | `LIN::motorCurrent`, `LIN::motorStatus`, `LIN::motorDirection` | In_Test_13 |
| `void sendLIN_MotorStatus()` | Motor_Current/Status/Direction 값을 LIN 프레임으로 조립하여 전송 | LIN Frame 0x21 (2 bytes) | In_Test_13 |
| `on sysvar LIN::motorCurrent` | Panel TrackBar 값 변경 시 즉시 LIN 프레임에 반영. 55A로 설정 시 Fault Injection 효과. | `LIN::motorCurrent` | In_Test_01, In_Test_13 |

---

## 3. DoorModule.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tLIN_Door` | 50ms 주기 LIN ID 0x22~0x25 프레임 전송 (파라미터 gLIN_ID로 구분) | `LIN::doorPositionFL/FR/RL/RR` | In_Test_14 |
| `void sendLIN_DoorStatus()` | Door_Position/Lock_Status/Window_Position 값을 LIN 프레임으로 조립하여 전송 | LIN Frame 0x22~0x25 (2 bytes) | In_Test_14 |
| `on sysvar LIN::doorPositionFL` | Door FL 위치 변경 시 즉시 LIN 프레임에 반영 | `LIN::doorPositionFL` | In_Test_14 |

---

## 4. BCM.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC/LIN) | 검증 |
|-----------|------|----------------|------|
| `on linFrame 0x21` | LIN Slave(WindowMotorECU)로부터 Motor_Current 수신. >50A 시 DTC B1234 생성 트리거. | LIN Frame 0x21, `LIN::motorCurrent` | In_Test_13, In_Test_01 |
| `void detectOvercurrent()` | Motor_Current > 50A 판단 → DTC B1234 생성. LIN 통신 이상(>50ms 미수신) 시 DTC U0100 생성. | `BCM::overcurrentDetected`, `LIN::linCommFault` | In_Test_01, In_Test_13, **In_Test_15** |
| `on linFrame 0x22~0x25` | LIN Slave(DoorModule)로부터 Door_Position/Lock_Status 수신. 내부 상태 갱신. | `LIN::doorPositionFL/FR/RL/RR` | In_Test_14 |
| `on timer tFaultTx` | 10ms 주기 BCM_FaultStatus(0x500) CAN-LS 전송 | `FaultSeverity`, `AliveCounter`, `Checksum` | In_Test_01[^1] |
| `void sendFaultStatus()` | BCM_FaultStatus(0x500) CAN-LS 전송. Motor_Current 기반 Fault 상태 반영. | `WindowMotorOvercurrent`, `DTC_Code` (0x500) | In_Test_01 |
| `on sysvar LIN::motorCurrent` | Panel에서 직접 전류값 주입 시 (Fault Injection 대체) LIN 수신과 동일하게 처리 | `BCM::currentAmps` | In_Test_12 |

---

## 5. Gateway.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message BCM_FaultStatus` | CAN-LS(0x500) 수신 → CAN-HS로 복사 전송 | `WindowMotorOvercurrent`, `DTC_Code` | In_Test_03 |
| `void routeMessage()` | 수신 메시지를 CAN-HS 채널로 포워딩 (지연 ≤5ms) | `Gateway::routingDelayMs` | In_Test_03 |
| `on message DoIP_RoutingActivation` | DoIP 0xE001 수신 → 경로 활성화 응답 | `Gateway::doipSessionActive` | In_Test_04 |
| `void forwardUDS()` | UDS 메시지(0x7DF) CAN-HS → CAN-LS 포워딩 | `CGW_Status::Diagnostic_Active` | In_Test_05 |
| `on message CGW_BusOff` | Bus Off 감지 → 세션 중단 및 DTC 저장 | `Gateway::busOffDetected` | In_Test_11 |

---

## 6. Tester.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `void sendUDS_10(byte session)` | UDS 0x10 세션 전환 요청 (0x01/0x02/0x03) | `UDS::currentSession` | In_Test_05 |
| `on message UDS_Response` | 0x7E8 응답 수신 및 ResponseCode 파싱 | `UDS::lastResponseCode` | In_Test_05~07 |
| `void sendUDS_19()` | UDS 0x19 0x02 DTC 조회 요청 | `UDS::lastServiceID` | In_Test_06 |
| `void parseDTCResponse()` | 응답에서 DTC_Code 및 상태 바이트 추출 | `UDS::dtcCleared` | In_Test_06 |
| `void sendUDS_14()` | UDS 0x14 0xFF 0xFF 0xFF DTC 클리어 요청 | `UDS::dtcCleared` | In_Test_07 |

---

## 7. OTA_Server.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `void activateDoIP()` | DoIP Routing Activation(0xE001) 전송 | `Gateway::doipSessionActive` | In_Test_04 |
| `void sendUDS_10_02()` | UDS 0x10 0x02 Programming Session 진입 | `UDS::currentSession` | In_Test_08 |
| `void sendUDS_34()` | UDS 0x34 다운로드 요청 (메모리 주소/크기 포함) | `OTA::otaInProgress` | In_Test_08 |
| `void sendUDS_36(byte block)` | UDS 0x36 4KB 블록 순차 전송 | `OTA::blockSequenceCounter` | In_Test_08 |
| `void sendUDS_37()` | UDS 0x37 전송 완료 및 CRC-32 검증 요청 | `OTA::crcMatch` | In_Test_09 |
| `void triggerRollback()` | CRC 불일치 또는 통신 단절 시 Rollback 실행 | `OTA::rollbackTriggered` | In_Test_10 |

---

## 8. Cluster.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message BCM_FaultStatus` | CAN-HS(0x500) 수신 → 경고등 활성화 판단 | `WindowMotorOvercurrent` | In_Test_02 |
| `void activateWarnLamp()` | RED 경고등 활성화 (50ms 이내) | `Cluster::warnLampRed` | In_Test_02 |
| `on message UDS_Response` | DTC 클리어 응답(0x54) 수신 → 경고등 소등 | `Cluster::warnLampRed` | In_Test_07 |

---

## 9. 테스트 모듈 구성

| 테스트 모듈 폴더 | 내용 | 대응 테스트 |
|--------------|------|-----------|
| `TC_L_LIN_Interface/` | LIN Motor Current 수신, Door Status 수신 테스트 | In_Test_13, 14 |
| `TC_F_Fault_Detection/` | LIN 기반 Fault Injection → DTC 생성 자동화 테스트 | In_Test_01, 02, 12 |
| `TC_G_Gateway_Routing/` | 라우팅 지연 측정 테스트 | In_Test_03, 04 |
| `TC_D_UDS_Diagnostics/` | UDS 세션/DTC 조회/클리어 테스트 | In_Test_05, 06, 07 |
| `TC_O_OTA_Programming/` | OTA 전송/CRC/Rollback 테스트 | In_Test_08, 09, 10, 11 |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 (LIN→CAN→UDS→OTA) | Scene.1~18 |

[^1]: **ASIL B E2E Protection Note**: 본 프로젝트는 CANoe SIL 환경 시뮬레이션을 위해 AliveCounter(4bit)와 Checksum(2bit)을 간이 구현하였습니다. 실제 양산용 ASIL B 타겟 시스템에서는 ISO 26262 Part 6 및 ISO 11898 표준을 준수하는 E2E Profile 1 또는 2 기반의 전체 CRC/Counter 보호 메커니즘을 적용해야 합니다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 — 구현 명세, CAPL 주요 로직 정의 |
| 1.1 | 2026-02-19 | E2E 보호 수준 근거(ASIL B) 각주 추가, In_Test_15(LIN Fault) 추적성 반영 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
