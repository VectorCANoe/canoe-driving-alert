# 통신 명세서 (Communication Specification)

> **V-Model 위치**: 좌측 하단 — 소프트웨어 아키텍처 설계 단계 (SWE.2)
> **대응 문서**: `05_Unit_Test.md` (SWE.4 단위 테스트로 검증)
> **ISO 26262**: Part 6, Clause 7 — 소프트웨어 아키텍처 설계 (인터페이스 명세)
> **ASPICE**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, BP4: 일관성 확보)
> **상위 연결**: `0302_NWflowDef.md` → 본 문서 → `0304_System_Variables.md`(변수 정의)
> **DBC 연관**: 본 문서의 Identifier/DLC/Signal은 `vehicle_system.dbc`의 메시지 정의와 직접 대응

---

| Message | Identifier | DLC | Signal | Signal Bit Position | Data 설명 | Data 범위 | Data 사용 |
|---------|-----------|-----|--------|-------------------|---------|---------|---------| 
| BCM_FaultStatus | 0x500 | 2 | WindowMotorOvercurrent | 0 | Window Motor 과전류 발생 여부 | 0~1 | 고장 상태를 Gateway, Cluster로 전송 |
| | | | FaultActive | 1 | DTC 활성화 여부 | 0~1 | DTC B1234 활성 상태 전달 |
| | | | DTCCode | 8~23 | DTC 코드 (B1234 = 0xB234) | 0~65535 | DTC 식별자 전달 |
| Cluster_WarnStatus | 0x510 | 1 | WarnLampRed | 0 | 경고등 RED 활성화 여부 | 0~1 | 경고등 상태를 Cluster로 전송 |
| UDS_Request | 0x7DF | 8 | ServiceID | 0~7 | UDS 서비스 식별자 | 0x10/0x14/0x19/0x34/0x36/0x37 | Tester/OTA Server → BCM 요청 |
| | | | SubFunction | 8~15 | 서비스 서브 기능 | 0x01/0x02/0x03/0xFF | 세션 유형 또는 DTC 그룹 마스크 |
| UDS_Response | 0x7E8 | 8 | ResponseCode | 0~7 | 응답 코드 | 0x50/0x54/0x59/0x74/0x76/0x77/0x7F | BCM → Tester/OTA Server 응답 |
| | | | DTCStatus | 8~15 | DTC 상태 바이트 | 0x00~0xFF | DTC 활성/비활성 상태 |
