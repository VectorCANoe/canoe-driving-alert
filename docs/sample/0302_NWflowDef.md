# 네트워크 플로우 정의 (Network Flow Definition)

> **V-Model 위치**: 좌측 중단 — 시스템 아키텍처 설계 단계 (SYS.3)
> **대응 문서**: `06_Integration_Test.md` (SWE.5 통합 테스트로 검증)
> **ISO 26262**: Part 4, Clause 7 — 시스템 설계 (인터페이스 및 통신 정의)
> **ASPICE**: SYS.3 (BP2: 인터페이스 정의, BP4: 일관성 및 추적성 확보)
> **상위 연결**: `0301_SysFuncAnalysis.md` → 본 문서 → `0303_Communication_Specification.md`(신호 상세)
> **DBC 연관**: 본 문서의 메시지/신호는 `vehicle_system.dbc` 정의와 일치

---

| Channel | ID hex | Symbolic Name (message name) | Byte no. | Function | Bit no. | signal name | BCM | Gateway | Tester | OTA Server | Cluster | [비고] |
|---------|--------|------------------------------|----------|----------|---------|-------------|-----|---------|--------|------------|---------|--------|
| CAN-LS | 0x500 | BCM_FaultStatus | 0 | Fault 상태 전송 | 0 | WindowMotorOvercurrent | Tx | Rx | | | | |
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
