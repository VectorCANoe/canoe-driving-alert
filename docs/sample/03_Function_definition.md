# 가상노드 Simulator (입출력 기능) — Function Definition

**Document ID**: SAMPLE-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 — 시스템 설계 (기능 분해 및 ECU 할당)
**ASPICE Reference**: SYS.3 (BP1: 시스템 아키텍처 설계, BP2: 인터페이스 정의, BP3: 기능 할당)
**Version**: 1.1
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 중단 — SYS.3 시스템 아키텍처 | `06_Integration_Test.md` (SWE.5) | `01_Requirements.md` | `0301_SysFuncAnalysis.md` |

---

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------|--------|---------|------|------|
| 입력 | LIN Motor Current 주입 | WindowMotorECU LIN Slave의 Motor_Current 값 조절 (0~100A). 50A 초과 시 BCM DTC B1234 자동 생성. | TrackBar 또는 Switch로 값 설정. 기존 Fault Injection 버튼은 LIN::motorCurrent = 55A 강제 주입으로 동작. | In_Test_13, In_Test_01, Scene.3 |
| 입력 | Fault Injection 버튼 | LIN::motorCurrent를 55A로 강제 주입하여 BCM 과전류 고장 상태를 시뮬레이션 (LIN Slave 정상 작동 전제) | Switch/Indicator 이용하여 ON/OFF 표현. BCM::overcurrentDetected는 LIN 수신 결과로 자동 갱신. | In_Test_01, In_Test_12, Scene.3 |
| | OTA 트리거 버튼 | OTA 업데이트 시작 신호 주입 | Switch/Indicator 이용하여 ON/OFF 표현 | In_Test_08, Scene.11 |
| | UDS 서비스 선택 | 0x10/0x14/0x19 서비스 수동 선택 | Switch/Indicator 이용하여 서비스 선택 | In_Test_05, In_Test_06, In_Test_07, Scene.7~9 |
| | Bus Load 조절 | CAN 버스 부하 수준 조절 (0~90%) | TrackBar 사용하여 값 조절 | In_Test_03 |
| 출력 | DTC 상태 | DTC B1234 생성/클리어 상태 표시 | Switch/Indicator 이용하여 ON/OFF 출력 | In_Test_01, In_Test_07, Scene.4, Scene.9 |
| | Cluster 경고등 | 경고등 활성화 여부 및 색상 표시 | Switch/Indicator 이용하여 RED/OFF 출력 | In_Test_02, In_Test_07, Scene.5, Scene.9 |
| | UDS 응답 코드 | PositiveResponse / NegativeResponse 표시 | Switch/Indicator 이용하여 응답 코드 출력 | In_Test_05~09, Scene.7~14 |
| | OTA 진행률 | 펌웨어 전송 블록 진행 상태 표시 | Switch/Indicator 이용하여 진행률 출력 | In_Test_08, In_Test_09, Scene.12~14 |
| | Rollback 상태 | OTA 실패 시 Rollback 완료 여부 표시 | Switch/Indicator 이용하여 ON/OFF 출력 | In_Test_10, Scene.15~17 |
| ECU 동작 | WindowMotorECU (LIN Slave 0x21) | Motor_Current / Motor_Status / Motor_Direction을 LIN ID 0x21로 BCM에 10ms 주기 보고. Motor_Current 값은 CANoe Panel TrackBar로 조절 가능. | CAPL LIN 프레임 전송 로직 (on timer 10ms). SysVar LIN::motorCurrent로 값 제어. | In_Test_13, Scene.2b, Scene.3 |
| ECU 동작 | DoorModule FL/FR/RL/RR (LIN Slave 0x22~0x25) | Door_Position / Lock_Status / Window_Position을 각 LIN ID 0x22~0x25로 BCM에 50ms 주기 보고. | CAPL LIN 프레임 전송 로직 (on timer 50ms). 4개 Slave를 파라미터화하여 단일 CAPL 파일로 구현. | In_Test_14, Scene.2b |
| ECU 동작 | BCM ECU | LIN Slave(WindowMotorECU, ID 0x21)로부터 Motor_Current 수신 → 50A 초과 감지 → DTC B1234 생성 → BCM_FaultStatus(0x500) CAN-LS 전송. LIN 프레임 50ms 이상 미수신 시 DTC U0100 생성 (Req_018). | CAPL LIN 수신 핸들러(on linFrame) + DTC 생성 + CAN 전송 로직. LIN 타임아웃 감지는 `detectOvercurrent()` 내 처리. | In_Test_01, In_Test_02, In_Test_13, **In_Test_15**, Scene.2c, Scene.3~5 |
| | Gateway ECU | CAN-LS(0x500) → CAN-HS 라우팅, DoIP Routing Activation 처리 | CAPL 메시지 복사 및 DoIP 포워딩 로직 추가 | In_Test_03, In_Test_04, Scene.6, Scene.10 |
| | Tester ECU | UDS 0x10/0x19/0x14 서비스 요청 및 응답 처리 | CAPL UDS 세션 및 DTC 조회 로직 추가 | In_Test_05, In_Test_06, In_Test_07, Scene.7~9 |
| | OTA Server ECU | UDS 0x34/0x36/0x37 시퀀스로 펌웨어 전송, CRC-32 검증 | CAPL OTA 전송 및 검증 로직 추가 | In_Test_08, In_Test_09, In_Test_10, Scene.11~17 |
| | Cluster ECU | BCM_FaultStatus 수신 → 경고등 활성화/소등 제어 | CAPL 경고등 제어 로직 추가 | In_Test_02, In_Test_07, Scene.5, Scene.9 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 |
| 1.1 | 2026-02-19 | BCM ECU 행 — LIN 타임아웃 DTC U0100(Req_018) 및 In_Test_15 추적성 추가 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
