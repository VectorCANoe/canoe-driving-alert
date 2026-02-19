# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: SAMPLE-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 — 시스템 설계 (인터페이스 및 통신 정의)
**ASPICE Reference**: SYS.3 (BP2: 인터페이스 정의, BP4: 일관성 및 추적성 확보)
**Version**: 1.0
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 중단 — SYS.3 네트워크 플로우 | `06_Integration_Test.md` (SWE.5) | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

**DBC 연관**: CAN 메시지/신호는 `sample_project.dbc` 정의와 일치. LIN 신호는 LIN 2.2A (ISO 17987) 프레임 구조를 따르며 CAPL `on linFrame` 이벤트로 처리.

---

| Channel | ID hex | Symbolic Name (message name) | Byte no. | Function | Bit no. | signal name | BCM | Gateway | Tester | OTA Server | Cluster | [비고] |
|---------|--------|------------------------------|----------|----------|---------|-------------|-----|---------|--------|------------|---------|--------|
| LIN | 0x21 | LIN_MotorStatus | 0 | Motor 전류/상태 보고 | 0~9 | Motor_Current (10bit) | Rx | | | | | WindowMotorECU(LIN Slave) Tx → BCM(LIN Master) Rx. 10ms 주기. |
| | | | | | 10~11 | Motor_Status (2bit) | Rx | | | | | 0:IDLE / 1:RUNNING / 2:STALL / 3:ERROR |
| | | | | | 12 | Motor_Direction (1bit) | Rx | | | | | 0:UP / 1:DOWN |
| | | | | | 13~15 | (Reserved) | | | | | | |
| LIN | 0x22 | LIN_DoorStatus_FL | 0 | Door FL 상태 보고 | 0~1 | Door_Position (2bit) | Rx | | | | | DoorModule_FL(LIN Slave 0x22) Tx → BCM Rx. 50ms 주기. 0:CLOSED/1:OPEN/2:AJAR/3:ERROR |
| | | | | | 2 | Lock_Status (1bit) | Rx | | | | | 0:LOCKED / 1:UNLOCKED |
| | | | | | 3~7 | (Reserved) | | | | | | |
| | | | 1 | | 0~7 | Window_Position (8bit) | Rx | | | | | 0~100% |
| LIN | 0x23 | LIN_DoorStatus_FR | 0 | Door FR 상태 보고 | 0~1 | Door_Position (2bit) | Rx | | | | | DoorModule_FR(LIN Slave 0x23) Tx → BCM Rx. 50ms 주기. 동일 신호 구조. |
| | | | | | 2 | Lock_Status (1bit) | Rx | | | | | |
| | | | 1 | | 0~7 | Window_Position (8bit) | Rx | | | | | |
| LIN | 0x24 | LIN_DoorStatus_RL | 0 | Door RL 상태 보고 | 0~1 | Door_Position (2bit) | Rx | | | | | DoorModule_RL(LIN Slave 0x24) Tx → BCM Rx. 50ms 주기. |
| | | | | | 2 | Lock_Status (1bit) | Rx | | | | | |
| | | | 1 | | 0~7 | Window_Position (8bit) | Rx | | | | | |
| LIN | 0x25 | LIN_DoorStatus_RR | 0 | Door RR 상태 보고 | 0~1 | Door_Position (2bit) | Rx | | | | | DoorModule_RR(LIN Slave 0x25) Tx → BCM Rx. 50ms 주기. |
| | | | | | 2 | Lock_Status (1bit) | Rx | | | | | |
| | | | 1 | | 0~7 | Window_Position (8bit) | Rx | | | | | |
| CAN-LS | 0x500 | BCM_FaultStatus | 0 | Fault 상태 전송 | 0 | WindowMotorOvercurrent | Tx | Rx | | | | LIN 0x21 Motor_Current > 50A 감지 후 생성 |
| | | | | | 1 | FaultActive | Tx | Rx | | | | |
| | | | | | 2 | DTCCode (Low) | Tx | Rx | | | | |
| | | | | | 3 | DTCCode (High) | Tx | Rx | | | | |
| | | | | | 4 | | | | | | | |
| | | | | | 5 | | | | | | | |
| | | | | | 6 | | | | | | | |
| | | | | | 7 | | | | | | | |
| CAN-HS | 0x500 | BCM_FaultStatus (라우팅) | 0 | Fault 상태 라우팅 | 0 | WindowMotorOvercurrent | | Tx | Rx | | Rx | Gateway가 CAN-LS→CAN-HS 라우팅 |
| | | | | | 1 | FaultActive | | Tx | Rx | | Rx | |
| | | | | | 2 | DTCCode (Low) | | Tx | Rx | | Rx | |
| | | | | | 3 | DTCCode (High) | | Tx | Rx | | Rx | |
| | | | | | 4 | | | | | | | |
| | | | | | 5 | | | | | | | |
| | | | | | 6 | | | | | | | |
| | | | | | 7 | | | | | | | |
| CAN-HS | 0x510 | Cluster_WarnStatus | 0 | 경고등 상태 전송 | 0 | WarnLampRed | | | | | Tx | |
| | | | | | 1 | | | | | | | |
| | | | | | 2 | | | | | | | |
| | | | | | 3 | | | | | | | |
| | | | | | 4 | | | | | | | |
| | | | | | 5 | | | | | | | |
| | | | | | 6 | | | | | | | |
| | | | | | 7 | | | | | | | |
| CAN-LS | 0x7DF | UDS_Request | 0 | UDS 서비스 요청 | 0 | ServiceID | Rx | Rx→Tx | Tx | Tx | | 0x10/0x14/0x19/0x34/0x36/0x37 |
| | | | | | 1 | SubFunction | Rx | Rx→Tx | Tx | Tx | | 세션 유형 또는 DTC 마스크 |
| | | | | | 2 | DataRecord (Low) | Rx | Rx→Tx | Tx | Tx | | |
| | | | | | 3 | DataRecord (High) | Rx | Rx→Tx | Tx | Tx | | |
| | | | | | 4 | | | | | | | |
| | | | | | 5 | | | | | | | |
| | | | | | 6 | | | | | | | |
| | | | | | 7 | | | | | | | |
| CAN-LS | 0x7E8 | UDS_Response | 0 | UDS 서비스 응답 | 0 | ResponseCode | Tx | | Rx | Rx | | 0x50/0x54/0x59/0x74/0x76/0x77/0x7F |
| | | | | | 1 | DTCStatus | Tx | | Rx | | | DTC 상태 바이트 (0x19 응답 시) |
| | | | | | 2 | DTCCode (Low) | Tx | | Rx | | | |
| | | | | | 3 | DTCCode (High) | Tx | | Rx | | | |
| | | | | | 4 | MaxBlockLength (Low) | Tx | | | Rx | | 0x34 응답 시 |
| | | | | | 5 | MaxBlockLength (High) | Tx | | | Rx | | |
| | | | | | 6 | | | | | | | |
| | | | | | 7 | | | | | | | |
| DoIP | 0xE001 | DoIP_RoutingActivation | - | DoIP 경로 활성화 | - | RoutingActivationType | | Rx | | Tx | | OTA Server → Gateway 경로 요청 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
