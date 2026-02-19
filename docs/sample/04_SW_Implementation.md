# SW 구현 명세 (Software Implementation Specification)

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
| `BCM.can` | BCM — 과전류 감지, DTC 생성, FaultStatus 전송 | `canoe/nodes/BCM.can` |
| `Gateway.can` | Central Gateway — CAN 라우팅, DoIP 처리 | `canoe/nodes/Gateway.can` |
| `Tester.can` | CANoe Tester — UDS 세션/DTC 조회/클리어 | `canoe/nodes/Tester.can` |
| `OTA_Server.can` | OTA Server — 펌웨어 전송, CRC 검증 | `canoe/nodes/OTA_Server.can` |
| `Cluster.can` | Cluster — 경고등 활성화/소등 | `canoe/nodes/Cluster.can` |

---

## 2. BCM.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on timer tFaultCheck` | 10ms 주기로 과전류 조건 확인 | `WindowMotorOvercurrent` (0x500, bit0) | In_Test_01 |
| `void detectOvercurrent()` | currentAmps > 50A 시 DTC B1234 생성 | `DTC_Code` (0x500, bit1~16) | In_Test_01 |
| `void sendFaultStatus()` | BCM_FaultStatus(0x500) CAN-LS 전송 | `FaultSeverity`, `AliveCounter`, `Checksum` | In_Test_01 |
| `on sysvar BCM::overcurrentDetected` | Fault Injection 신호 수신 시 즉시 DTC 생성 | System Variable | In_Test_12 |

---

## 3. Gateway.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message BCM_FaultStatus` | CAN-LS(0x500) 수신 → CAN-HS로 복사 전송 | `WindowMotorOvercurrent`, `DTC_Code` | In_Test_03 |
| `void routeMessage()` | 수신 메시지를 CAN-HS 채널로 포워딩 (지연 ≤5ms) | `Gateway::routingDelayMs` | In_Test_03 |
| `on message DoIP_RoutingActivation` | DoIP 0xE001 수신 → 경로 활성화 응답 | `Gateway::doipSessionActive` | In_Test_04 |
| `void forwardUDS()` | UDS 메시지(0x7DF) CAN-HS → CAN-LS 포워딩 | `CGW_Status::Diagnostic_Active` | In_Test_05 |
| `on message CGW_BusOff` | Bus Off 감지 → 세션 중단 및 DTC 저장 | `Gateway::busOffDetected` | In_Test_11 |

---

## 4. Tester.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `void sendUDS_10(byte session)` | UDS 0x10 세션 전환 요청 (0x01/0x02/0x03) | `UDS::currentSession` | In_Test_05 |
| `on message UDS_Response` | 0x7E8 응답 수신 및 ResponseCode 파싱 | `UDS::lastResponseCode` | In_Test_05~07 |
| `void sendUDS_19()` | UDS 0x19 0x02 DTC 조회 요청 | `UDS::lastServiceID` | In_Test_06 |
| `void parseDTCResponse()` | 응답에서 DTC_Code 및 상태 바이트 추출 | `UDS::dtcCleared` | In_Test_06 |
| `void sendUDS_14()` | UDS 0x14 0xFF 0xFF 0xFF DTC 클리어 요청 | `UDS::dtcCleared` | In_Test_07 |

---

## 5. OTA_Server.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `void activateDoIP()` | DoIP Routing Activation(0xE001) 전송 | `Gateway::doipSessionActive` | In_Test_04 |
| `void sendUDS_10_02()` | UDS 0x10 0x02 Programming Session 진입 | `UDS::currentSession` | In_Test_08 |
| `void sendUDS_34()` | UDS 0x34 다운로드 요청 (메모리 주소/크기 포함) | `OTA::otaInProgress` | In_Test_08 |
| `void sendUDS_36(byte block)` | UDS 0x36 4KB 블록 순차 전송 | `OTA::blockSequenceCounter` | In_Test_08 |
| `void sendUDS_37()` | UDS 0x37 전송 완료 및 CRC-32 검증 요청 | `OTA::crcMatch` | In_Test_09 |
| `void triggerRollback()` | CRC 불일치 또는 통신 단절 시 Rollback 실행 | `OTA::rollbackTriggered` | In_Test_10 |

---

## 6. Cluster.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 (DBC) | 검증 |
|-----------|------|--------------|------|
| `on message BCM_FaultStatus` | CAN-HS(0x500) 수신 → 경고등 활성화 판단 | `WindowMotorOvercurrent` | In_Test_02 |
| `void activateWarnLamp()` | RED 경고등 활성화 (50ms 이내) | `Cluster::warnLampRed` | In_Test_02 |
| `on message UDS_Response` | DTC 클리어 응답(0x54) 수신 → 경고등 소등 | `Cluster::warnLampRed` | In_Test_07 |

---

## 7. 테스트 모듈 구성

| 테스트 모듈 폴더 | 내용 | 대응 테스트 |
|--------------|------|-----------|
| `TC_F_Fault_Detection/` | Fault Injection 자동화 테스트 | In_Test_01, 02, 12 |
| `TC_G_Gateway_Routing/` | 라우팅 지연 측정 테스트 | In_Test_03, 04 |
| `TC_D_UDS_Diagnostics/` | UDS 세션/DTC 조회/클리어 테스트 | In_Test_05, 06, 07 |
| `TC_O_OTA_Programming/` | OTA 전송/CRC/Rollback 테스트 | In_Test_08, 09, 10, 11 |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 | Scene.1~18 |
