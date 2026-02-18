# CANoe Simulation Nodes (CAPL)

이 디렉토리에는 **Fault → Diagnostics → OTA** 시나리오를 시뮬레이션하는
CANoe CAPL 노드 파일들이 위치합니다.

## 개발 예정 노드 목록

| 파일명 | 역할 | 구현 시나리오 | 우선순위 |
|--------|------|-------------|---------|
| `BCM_Sim.can` | BCM 시뮬레이션 | Window Motor Overcurrent → DTC B1234 → CAN-LS 0x500 전송 | Phase 1 |
| `CGW_Sim.can` | Central Gateway 시뮬레이션 | CAN-LS→CAN-HS2 라우팅 (≤5ms), DoIP 경로 제공 | Phase 2 |
| `Tester_Sim.can` | 진단 Tester 시뮬레이션 | UDS 0x10 (Session Control), 0x19 (Read DTC) | Phase 3 |
| `OTA_Server_Sim.can` | OTA 서버 시뮬레이션 | UDS 0x34/0x36×N/0x37 (Download/Transfer/Exit) + Rollback 검증 | Phase 4 |

## Master E2E Scenario (Red Thread)

```
Phase 1 — Fault Injection:
BCM_Sim → BCM_FaultStatus (0x500): DTC=B1234, Severity=0x60

Phase 2 — Gateway Routing:
CGW_Sim 수신 → CAN-HS2 전달 ≤5ms / vECU 경고등 활성화

Phase 3 — UDS Diagnostics:
Tester_Sim → UDS 0x10 0x03 (ExtendedDiag) → BCM
            → UDS 0x19 0x02 (ReadDTCByStatus) → DTC B1234 수신
            → TCP/IP → 가상 OTA 서버 알림

Phase 4 — OTA Programming:
OTA_Server_Sim → UDS 0x10 0x02 (ProgrammingSession)
               → UDS 0x34 (RequestDownload)
               → UDS 0x36 × N (TransferData)
               → UDS 0x37 (RequestTransferExit)
               → BCM 재시작 → DTC 소거 확인
```

## 관련 DBC 메시지

| Message | CAN ID | 방향 | 담당 노드 |
|---------|--------|------|---------|
| `BCM_FaultStatus` | 0x500 | BCM → CGW | BCM_Sim.can |
| `GW_RoutingStatus` | 0x600 | CGW → vECU | CGW_Sim.can |
| `UDS_Request` | 진단 CAN | Tester → ECU | Tester_Sim.can |
| `UDS_Response` | 진단 CAN | ECU → Tester | 각 ECU 노드 |

## 참고

- 구 CAPL 노드 (조명/UX 시나리오): `reference/legacy/capl_nodes/`
- DBC 파일: `../databases/vehicle_system.dbc`
- CANoe 설정: `../cfg/IVI_OTA_Project.cfg`
