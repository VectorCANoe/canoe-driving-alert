# 시스템 변수 정의 (System Variables)

**Document ID**: SAMPLE-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 — 소프트웨어 아키텍처 설계 (데이터 인터페이스 정의)
**ASPICE Reference**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, SWE.3 BP1: 상세 설계)
**Version**: 1.0
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 하단 — SWE.2 시스템 변수 | `05_Unit_Test.md` (SWE.4) | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

**CANoe 연관**: 본 문서의 변수는 CANoe System Variables로 직접 구현되며 CAPL에서 참조.

---

| ID | Namespace | Name | Data Type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|--------------|-------------|
| 1 | BCM | overcurrentDetected | uint32 | 0 | 1 | 0 | Window Motor 과전류 감지 여부 (0: 정상, 1: 감지). LIN::motorCurrent > 50A 시 자동 갱신. |
| 2 | BCM | faultActive | uint32 | 0 | 1 | 0 | DTC B1234 활성화 여부 |
| 3 | BCM | currentAmps | double | 0 | 100 | 0 | Window Motor 전류값 (A). LIN::motorCurrent 수신값과 동기화. Panel TrackBar로 직접 조절 시 LIN Slave 시뮬레이션 값으로 사용. |
| 4 | Gateway | routingActive | uint32 | 0 | 1 | 0 | CAN-LS → CAN-HS 라우팅 활성화 여부 |
| 5 | Gateway | routingDelayMs | double | 0 | 100 | 0 | 메시지 라우팅 지연 시간 (ms) |
| 6 | Gateway | doipSessionActive | uint32 | 0 | 1 | 0 | DoIP 세션 활성화 여부 |
| 7 | Gateway | busOffDetected | uint32 | 0 | 1 | 0 | CAN Bus Off 감지 여부 |
| 8 | UDS | currentSession | uint32 | 1 | 3 | 1 | 현재 UDS 세션 (1: Default, 2: Programming, 3: Extended) |
| 9 | UDS | lastServiceID | uint32 | 0 | 255 | 0 | 마지막 요청 UDS 서비스 ID |
| 10 | UDS | lastResponseCode | uint32 | 0 | 255 | 0 | 마지막 UDS 응답 코드 |
| 11 | UDS | dtcCleared | uint32 | 0 | 1 | 0 | DTC 클리어 완료 여부 |
| 12 | OTA | otaInProgress | uint32 | 0 | 1 | 0 | OTA 업데이트 진행 중 여부 |
| 13 | OTA | blockSequenceCounter | uint32 | 0 | 255 | 0 | 전송 블록 순서 카운터 |
| 14 | OTA | crcMatch | uint32 | 0 | 1 | 0 | CRC-32 검증 일치 여부 (0: 불일치, 1: 일치) |
| 15 | OTA | rollbackTriggered | uint32 | 0 | 1 | 0 | Rollback 실행 여부 |
| 16 | Cluster | warnLampRed | uint32 | 0 | 1 | 0 | RED 경고등 활성화 여부 (0: 소등, 1: 점등) |
| 17 | LIN | motorCurrent | double | 0 | 100 | 0 | WindowMotorECU(LIN Slave 0x21)에서 수신한 Motor 전류값 (A). >50A 시 BCM::overcurrentDetected = 1 자동 설정. |
| 18 | LIN | motorStatus | uint32 | 0 | 3 | 0 | Motor 동작 상태. 0:IDLE / 1:RUNNING / 2:STALL / 3:ERROR |
| 19 | LIN | motorDirection | uint32 | 0 | 1 | 0 | Motor 회전 방향. 0:UP / 1:DOWN |
| 20 | LIN | doorPositionFL | uint32 | 0 | 3 | 0 | Door FL 위치 (LIN 0x22 수신). 0:CLOSED / 1:OPEN / 2:AJAR / 3:ERROR |
| 21 | LIN | doorPositionFR | uint32 | 0 | 3 | 0 | Door FR 위치 (LIN 0x23 수신). 동일 인코딩. |
| 22 | LIN | doorPositionRL | uint32 | 0 | 3 | 0 | Door RL 위치 (LIN 0x24 수신). 동일 인코딩. |
| 23 | LIN | doorPositionRR | uint32 | 0 | 3 | 0 | Door RR 위치 (LIN 0x25 수신). 동일 인코딩. |
| 24 | LIN | linCommFault | uint32 | 0 | 1 | 0 | LIN 통신 이상 감지 여부. LIN Slave 프레임 미수신 >50ms 시 1로 설정 → BCM DTC U0100 생성 트리거. |

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
