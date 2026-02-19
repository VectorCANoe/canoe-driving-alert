# 통신 명세서 (Communication Specification)

**Document ID**: SAMPLE-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7
**ASPICE Reference**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, BP4: 일관성 확보)
**Version**: 1.0
**Date**: 2026-02-19
**Status**: Released

> **V-Model 위치**: 좌측 하단 — 소프트웨어 아키텍처 설계 단계 (SWE.2)
> **대응 문서**: `05_Unit_Test.md` (SWE.4 단위 테스트로 검증)
> **ISO 26262**: Part 6, Clause 7 — 소프트웨어 아키텍처 설계 (인터페이스 명세)
> **ASPICE**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, BP4: 일관성 확보)
> **상위 연결**: `0302_NWflowDef.md` → 본 문서 → `0304_System_Variables.md`(변수 정의)
> **DBC 연관**: CAN 메시지의 Identifier/DLC/Signal은 `sample_project.dbc`의 메시지 정의와 직접 대응. LIN 메시지(0x21~0x25)는 LIN 2.2A (ISO 17987) 프레임 구조를 따르며 CAPL `on linFrame` 이벤트로 처리.

---

| Message | Identifier | DLC | Signal | Signal Bit Position | Data 설명 | Data 범위 | Data 사용 |
|---------|-----------|-----|--------|-------------------|---------|---------|---------|
| LIN_MotorStatus | 0x21 (LIN ID) | 2 | Motor_Current | 0~9 (10bit) | Window Motor 전류값 | 0~100 A | BCM 과전류 판단. >50A → DTC B1234 생성. (→ Req_016) |
| | | | Motor_Status | 10~11 (2bit) | Motor 동작 상태 | 0:IDLE / 1:RUNNING / 2:STALL / 3:ERROR | BCM 상태 모니터링 |
| | | | Motor_Direction | 12 (1bit) | Motor 회전 방향 | 0:UP / 1:DOWN | BCM 상태 모니터링 |
| | | | (Reserved) | 13~15 | — | — | — |
| LIN_DoorStatus | 0x22~0x25 (LIN ID) | 2 | Door_Position | 0~1 (2bit) | 도어 개폐 위치 | 0:CLOSED / 1:OPEN / 2:AJAR / 3:ERROR | BCM 도어 상태 관리. (→ Req_017) |
| | | | Lock_Status | 2 (1bit) | 도어 잠금 상태 | 0:LOCKED / 1:UNLOCKED | BCM 잠금 상태 관리 |
| | | | (Reserved) | 3~7 | — | — | — |
| | | | Window_Position | 8~15 (8bit) | 창문 개방 위치 | 0~100 % | BCM 창문 위치 관리 |
| BCM_FaultStatus | 0x500 (CAN-LS) | 4 | WindowMotorOvercurrent | 0 | Window Motor 과전류 발생 여부 | 0~1 | LIN Motor_Current >50A 감지 후 Gateway, Cluster로 전송 |
| | | | FaultActive | 1 | DTC 활성화 여부 | 0~1 | DTC B1234 활성 상태 전달 |
| | | | DTCCode | 8~23 | DTC 코드 (B1234 = 0xB234) | 0~65535 | DTC 식별자 전달 |
| | | | FaultSeverity | 24~25 | 고장 심각도 | 0:없음 / 1:경고 / 2:고장 / 3:위험 | 심각도 등급 전달 |
| | | | AliveCounter | 26~29 (4bit) | 생존 카운터 | 0~15 순환 | 메시지 신뢰성 확인 |
| | | | Checksum | 30~31 (2bit) | 체크섬 (간이) | 0~3 | 데이터 무결성 간이 검증 |
| Cluster_WarnStatus | 0x510 (CAN-HS) | 1 | WarnLampRed | 0 | 경고등 RED 활성화 여부 | 0~1 | 경고등 상태를 Cluster로 전송 |
| UDS_Request | 0x7DF (CAN-LS) | 8 | ServiceID | 0~7 | UDS 서비스 식별자 | 0x10/0x14/0x19/0x34/0x36/0x37 | Tester/OTA Server → BCM 요청 |
| | | | SubFunction | 8~15 | 서비스 서브 기능 | 0x01/0x02/0x03/0xFF | 세션 유형 또는 DTC 그룹 마스크 |
| | | | DataRecord | 16~63 | 데이터 레코드 (6 bytes) | 가변 | 서비스별 파라미터 |
| UDS_Response | 0x7E8 (CAN-LS) | 8 | ResponseCode | 0~7 | 응답 코드 | 0x50/0x54/0x59/0x74/0x76/0x77/0x7F | BCM → Tester/OTA Server 응답 |
| | | | DTCStatus | 8~15 | DTC 상태 바이트 | 0x00~0xFF | DTC 활성/비활성 상태 (0x19 응답 시) |
| | | | DTCCode_High | 16~23 | DTC 코드 상위 바이트 | 0x00~0xFF | DTC 식별자 (0x19 응답 시) |
| | | | DTCCode_Low | 24~31 | DTC 코드 하위 바이트 | 0x00~0xFF | DTC 식별자 (0x19 응답 시) |
| | | | MaxBlockLength | 32~47 | 최대 블록 길이 | 0~65535 | 0x34 요청 응답 시 전달 |

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
