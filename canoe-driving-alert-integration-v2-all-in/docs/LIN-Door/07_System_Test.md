# 시스템 테스트 (System Test)

**Document ID**: SAMPLE-07-ST
**ISO 26262 Reference**: Part 4, Cl.10 — 시스템 적격성 테스트
**ASPICE Reference**: SYS.5 (BP1: 시스템 테스트 명세, BP2: 시스템 테스트 수행, BP3: 결과 평가)
**Version**: 1.1
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 우측 상단 — SYS.5 시스템 테스트 | `01_Requirements.md` (SYS.2) | `06_Integration_Test.md` | 릴리즈/검수 |

---

| Scene. ID | 설명 | Pass/Fail | 담당자 | 일자 |
|-----------|------|----------|--------|------|
| Scene. 1 | CANoe 프로젝트 실행 후 모든 ECU 노드(WindowMotorECU, DoorModule×4, BCM, Gateway, Tester, OTA Server, Cluster) 초기화 확인 | | | |
| Scene. 2 | 초기 상태에서 DTC 없음, 경고등 소등, 세션 Default 상태 확인. LIN::motorCurrent = 10A (정상 구동), Door_Position = CLOSED 확인. | | | |
| Scene. 2b | LIN 버스 정상 동작 확인 — WindowMotorECU(0x21) 10ms 주기 LIN 프레임 수신, DoorModule FL~RR(0x22~0x25) 50ms 주기 LIN 프레임 수신 확인 | | | |
| Scene. 2c | LIN 통신 이상 감지 확인 — WindowMotorECU(0x21) LIN 프레임 전송 중단 시뮬레이션 (50ms 이상 미수신) → LIN::linCommFault = 1 → BCM DTC U0100 생성 확인. LIN 복구 후 linCommFault = 0 및 정상 통신 재개 확인. (Req_018) | | | |
| Scene. 3 | LIN::motorCurrent = 55A 주입 → WindowMotorECU LIN 0x21 전송 → BCM LIN 수신 → DTC B1234 생성 → BCM_FaultStatus(0x500) CAN-LS 전송 확인 | | | |
| Scene. 4 | BCM_FaultStatus 전송 후 DTC B1234 생성 및 저장 확인 | | | |
| Scene. 5 | DTC 생성 후 50ms 이내 Cluster RED 경고등 활성화 확인 | | | |
| Scene. 6 | Gateway가 CAN-LS(0x500)를 CAN-HS로 5ms 이내 라우팅하는 모습 확인 | | | |
| Scene. 7 | Tester가 UDS 0x10 0x03으로 Extended Session 전환 및 PositiveResponse(0x50 0x03) 수신 확인 | | | |
| Scene. 8 | Extended Session에서 UDS 0x19 0x02 요청 → DTC B1234 포함 응답 확인 | | | |
| Scene. 9 | UDS 0x14 0xFF 0xFF 0xFF 요청 → DTC 클리어 및 Cluster 경고등 소등 확인 | | | |
| Scene. 10 | DoIP Routing Activation(0xE001) → Gateway 경로 활성화 확인 | | | |
| Scene. 11 | UDS 0x10 0x02 Programming Session 진입 → PositiveResponse(0x50 0x02) 확인 | | | |
| Scene. 12 | UDS 0x34 다운로드 요청 → maxBlockLength 포함 응답(0x74) 확인 | | | |
| Scene. 13 | UDS 0x36으로 4KB 블록 순차 전송 → 각 블록 PositiveResponse(0x76) 확인 | | | |
| Scene. 14 | UDS 0x37 전송 완료 → CRC-32 검증 통과 → PositiveResponse(0x77) 및 BCM 재시작 확인 | | | |
| Scene. 15 | OTA 중 CRC 불일치 주입 → NegativeResponse(0x7F 0x37 0x70) 및 Rollback 확인 | | | |
| Scene. 16 | OTA 중 Bus Off 주입 → 세션 안전 중단 및 DTC 저장 확인 | | | |
| Scene. 17 | Rollback 완료 후 이전 펌웨어 버전으로 BCM 정상 동작 확인 | | | |
| Scene. 18 | Fault Injection 재실행 → 전체 시나리오(LIN Motor Current→BCM Fault→CAN-LS 0x500→Gateway→CAN-HS→UDS→OTA) 2회 연속 정상 동작 확인 | | | |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 |
| 1.1 | 2026-02-19 | Scene.2c 추가 — LIN 통신 이상 감지(Req_018 / DTC U0100) 시스템 테스트 추적성 완결 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
