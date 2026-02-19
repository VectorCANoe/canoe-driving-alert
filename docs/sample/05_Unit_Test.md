# 단위 테스트 (Unit Test)

> **V-Model 위치**: 우측 하단 — 소프트웨어 단위 테스트 단계 (SWE.4)
> **대응 문서**: `03_Function_definition.md` + `0304_System_Variables.md` (SWE.2/SWE.3 설계 검증)
> **ISO 26262**: Part 6, Clause 9 — 소프트웨어 단위 테스트
> **ASPICE**: SWE.4 (BP1: 단위 테스트 명세, BP2: 단위 테스트 수행, BP3: 결과 평가)
> **상위 연결**: `03_Function_definition.md`(기능 정의) → 본 문서 → `06_Integration_Test.md`(통합 테스트)
> **검증 환경**: CANoe SIL (Software-in-the-Loop) — 각 CAPL 노드를 독립적으로 실행하여 검증

---

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|------|------|--------|---------|----------|--------|------|
| WindowMotorECU | 제어 | LIN Motor Current 전송 | Motor_Current 값을 LIN ID 0x21로 10ms 주기 BCM에 전송. 초기값 10A (정상 구동). | | | |
| WindowMotorECU | 제어 | 과전류 시뮬레이션 | LIN::motorCurrent = 55A 설정 시 BCM의 DTC B1234 생성 트리거 확인 | | | |
| WindowMotorECU | 제어 | Motor_Status 전송 | Motor_Status = STALL(2) 설정 시 LIN 프레임에 정상 반영 | | | |
| DoorModule | 제어 | LIN Door Status 전송 | Door_Position / Lock_Status / Window_Position을 LIN ID 0x22~0x25로 50ms 주기 전송 | | | |
| DoorModule | 제어 | Door 상태 변경 | LIN::doorPositionFL = OPEN(1) 설정 시 LIN 0x22 프레임에 즉시 반영 | | | |
| BCM | 제어 | LIN Motor Current 수신 | LIN Slave(0x21)로부터 Motor_Current 수신 → BCM::currentAmps 갱신 | | | |
| BCM | 제어 | 과전류 감지 | LIN::motorCurrent > 50A 수신 시 BCM::overcurrentDetected = 1, DTC B1234 생성 | | | |
| BCM | 제어 | LIN Door Status 수신 | LIN Slave(0x22~0x25)로부터 Door_Position 수신 → LIN::doorPositionFL/FR/RL/RR 갱신 | | | |
| BCM | 제어 | LIN 통신 이상 감지 | LIN Slave 프레임 50ms 이상 미수신 시 LIN::linCommFault = 1, DTC U0100 생성 | | | |
| BCM | 제어 | FaultStatus 전송 | BCM_FaultStatus(0x500) CAN-LS 10ms 주기 전송. LIN Motor_Current 기반 Fault 상태 반영. | | | |
| Gateway | 제어 | CAN 라우팅 | CAN-LS(0x500) 수신 → CAN-HS 라우팅 (지연 ≤5ms) | | | |
| Gateway | 제어 | DoIP 처리 | DoIP Routing Activation(0xE001) 처리 및 UDS 메시지 포워딩 | | | |
| Tester | 제어 | UDS 세션 전환 | UDS 0x10 Default/Extended/Programming 세션 전환 및 응답 처리 | | | |
| Tester | 제어 | DTC 조회 | UDS 0x19 DTC B1234 조회 및 상태 바이트 파싱 | | | |
| Tester | 제어 | DTC 클리어 | UDS 0x14 DTC 클리어 요청 및 응답 처리 | | | |
| OTA Server | 제어 | 다운로드 요청 | UDS 0x34 다운로드 요청 및 maxBlockLength 응답 처리 | | | |
| OTA Server | 제어 | 블록 전송 | UDS 0x36 4KB 블록 순차 전송 및 Block Sequence Counter 검증 | | | |
| OTA Server | 제어 | 전송 완료 | UDS 0x37 전송 완료 및 CRC-32 검증 후 BCM 재시작 | | | |
| OTA Server | 제어 | Rollback | OTA 실패(CRC 불일치/통신 단절) 시 자동 Rollback | | | |
| Cluster | 제어 | 경고등 활성화 | BCM_FaultStatus 수신 → 경고등(RED) 50ms 이내 활성화 | | | |
| Cluster | 제어 | 경고등 소등 | DTC 클리어 수신 후 경고등 소등 | | | |
| 가상 노드 (Simulator) | 입력 | Fault Injection | LIN::motorCurrent = 55A 강제 주입 → BCM 과전류 감지 트리거 (기존 직접 SysVar 방식 → LIN 경유 방식으로 변경) | | | |
| 가상 노드 (Simulator) | 입력 | OTA 트리거 | OTA 업데이트 시작 신호 주입 | | | |
| 가상 노드 (Simulator) | 입력 | UDS 서비스 선택 | 0x10/0x14/0x19 서비스 수동 선택 | | | |
| 가상 노드 (Simulator) | 출력 | DTC 상태 표시 | DTC B1234 생성/클리어 상태 Panel 출력 | | | |
| 가상 노드 (Simulator) | 출력 | 경고등 상태 표시 | RED 경고등 활성화 여부 Panel 출력 | | | |
| 가상 노드 (Simulator) | 출력 | OTA 진행률 표시 | 블록 전송 진행 상태 Panel 출력 | | | |
