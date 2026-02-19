# 시스템 변수 정의 (System Variables)

> **V-Model 위치**: 좌측 하단 — 소프트웨어 아키텍처 설계 단계 (SWE.2)
> **대응 문서**: `05_Unit_Test.md` (SWE.4 단위 테스트로 검증)
> **ISO 26262**: Part 6, Clause 7 — 소프트웨어 아키텍처 설계 (데이터 인터페이스 정의)
> **ASPICE**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, SWE.3 BP1: 상세 설계)
> **상위 연결**: `0303_Communication_Specification.md` → 본 문서 → `05_Unit_Test.md`(단위 테스트)
> **CANoe 연관**: 본 문서의 변수는 CANoe System Variables로 직접 구현되며 CAPL에서 참조

---

| ID | Namespace | Name | Data Type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|--------------|-------------|
| 1 | BCM | overcurrentDetected | uint32 | 0 | 1 | 0 | Window Motor 과전류 감지 여부 (0: 정상, 1: 감지) |
| 2 | BCM | faultActive | uint32 | 0 | 1 | 0 | DTC B1234 활성화 여부 |
| 3 | BCM | currentAmps | double | 0 | 100 | 0 | Window Motor 전류값 (A) |
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
