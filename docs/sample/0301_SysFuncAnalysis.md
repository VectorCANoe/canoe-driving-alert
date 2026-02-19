# 시스템 기능 분석 (System Function Analysis)

> **V-Model 위치**: 좌측 중단 — 시스템 아키텍처 설계 단계 (SYS.3)
> **대응 문서**: `06_Integration_Test.md` (SWE.5 통합 테스트로 검증)
> **ISO 26262**: Part 4, Clause 7 — 시스템 설계 (기능 분해 및 ECU 할당)
> **ASPICE**: SYS.3 (BP1: 시스템 아키텍처 개발, BP2: 인터페이스 정의, BP3: 기능 할당)
> **상위 연결**: `01_Requirements.md` → 본 문서 → `0302_NWflowDef.md`(네트워크 플로우)
> **HARA 연관**: BCM/Gateway 기능은 HARA H-01(과전류) 및 H-09(OTA 실패)에서 도출된 안전목표 SG-01, SG-08에 대응. H-01의 Fault Detection 출발점은 LIN Slave(WindowMotorECU) → BCM(LIN Master) Motor_Current 보고 흐름.

---

| 노드 | 기능 상세 | 비고 |
|------|---------|------|
| | | **Body Domain — LIN Bus (19.2 kbps)** |
| WindowMotorECU | Motor_Current(10bit, 0~100A) / Motor_Status(2bit: IDLE/RUNNING/STALL/ERROR) / Motor_Direction(1bit: UP/DOWN)을 LIN ID 0x21로 10ms 주기 BCM에 보고 | LIN Slave. Fault Detection 출발점. |
| DoorModule FL/FR/RL/RR | Door_Position(2bit: CLOSED/OPEN/AJAR/ERROR) / Lock_Status(1bit) / Window_Position(8bit, 0~100%)을 LIN ID 0x22~0x25로 50ms 주기 BCM에 보고 | LIN Slave. 4개 Slave 동일 구조, ID만 상이. |
| | | **Body Domain — CAN-LS (125 kbps)** |
| BCM | LIN Slave(WindowMotorECU, 0x21)로부터 Motor_Current 수신 → 50A 초과 시 DTC B1234 생성 → `BCM_FaultStatus`(0x500) CAN-LS 10ms 주기 전송. LIN 통신 이상(프레임 미수신 >50ms) 시 DTC U0100 생성. | LIN Master. |
| Cluster | `BCM_FaultStatus`(0x500) CAN-HS 수신 → 경고등(RED) 50ms 이내 활성화. UDS 0x14 DTC 클리어 수신 시 경고등 소등. | |
| | | **Gateway Domain** |
| Central Gateway | CAN-LS(0x500) → CAN-HS 메시지 라우팅 (지연 ≤5ms). DoIP Routing Activation(0xE001) 처리 및 UDS 메시지 CAN-LS 포워딩 | |
| | | **Diagnostic Domain** |
| CANoe Tester | UDS 0x10 세션 전환, 0x19 DTC 조회, 0x14 DTC 클리어 요청 및 응답 처리 | |
| | | **OTA Domain** |
| OTA Server | UDS 0x10 0x02 Programming Session 진입 → 0x34 다운로드 요청 → 0x36 4KB 블록 전송 → 0x37 전송 완료 및 CRC-32 검증 → BCM 재시작 | |
| | | **Actual Device** |
| Cluster Panel | UI를 통해 DTC 경고등 상태를 사용자에게 표시 | |
| CANoe Panel | Fault Injection, UDS 서비스 선택, OTA 트리거 버튼 및 상태 표시 | |
