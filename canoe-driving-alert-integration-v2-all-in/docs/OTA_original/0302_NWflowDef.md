# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: PROJ-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 — 시스템 설계 (인터페이스 및 통신 정의)
**ASPICE Reference**: SYS.3 (BP2: 인터페이스 정의, BP4: 일관성 및 추적성 확보)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 중단 — SYS.3 네트워크 플로우 | `06_Integration_Test.md` (SWE.5) | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

**DBC 연관**: CAN 메시지/신호는 `project.dbc` 정의와 일치. sysvar 신호는 CANoe System Variables로 직접 처리.

---

| Channel | ID hex | Symbolic Name (message name) | Byte no. | Function | Bit no. | signal name | Vehicle_ECU | MDPS_ECU | LDW_ECU | WDM_ECU | CGW | Cluster | Ambient | Sound | IVI | Door | OTA_Server | [비고] |
|---------|--------|------------------------------|----------|----------|---------|-------------|------------|---------|--------|--------|-----|---------|---------|-------|-----|------|------------|--------|
| CAN-LS | 0x100 | Vehicle_Speed | 0 | 차량 속도/가속도 보고 | 0~7 | gVehicleSpeed (8bit, km/h) | Tx | | | Rx | Rx | | | | | | | Vehicle_ECU Tx → CGW → WDM_ECU Rx. 100ms 주기. |
| | | | 1 | | 0~7 | gAccelValue (8bit signed, m/s²) | Tx | | | Rx | Rx | | | | | | | 양수: 가속, 음수: 제동 |
| | | | 2 | | 0~7 | gBrakeValue (8bit, m/s²) | Tx | | | Rx | Rx | | | | | | | |
| | | | 3 | | 0~1 | OverspeedFlag (1bit) | Tx | | | Rx | Rx | | | | | | | gRoadZone 기준 초과 시 1 |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-LS | 0x110 | Steering_Status | 0 | 조향 입력 / 급차선변경 보고 | 0 | SteeringInput (1bit) | | Tx | | Rx | Rx | | | | | | | MDPS_ECU Tx → CGW → WDM_ECU Rx. 100ms 주기. 0:미입력/1:입력 |
| | | | | | 1 | gLaneChangeAlert (1bit) | | Tx | | Rx | Rx | | | | | | | 조향각속도 >50°/s 시 1 |
| | | | | | 2~7 | SteeringAngleRate (6bit, °/s) | | Tx | | Rx | Rx | | | | | | | |
| | | | 1 | | 0~7 | (Reserved) | | | | | | | | | | | | |
| CAN-LS | 0x120 | LDW_Status | 0 | 차선이탈 감지 보고 | 0 | gLaneDeparture (1bit) | | | Tx | Rx | Rx | | | | | | | LDW_ECU Tx → CGW → WDM_ECU Rx. 100ms 주기. 0:정상/1:이탈 |
| | | | | | 1~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x200 | WDM_Warning | 0 | 경고 레벨 / 구간 정보 | 0~1 | gWarningLevel (2bit) | | | | Tx | | Rx | Rx | Rx | Rx | Rx | | WDM_ECU Tx → 전체 출력 ECU Rx. 50ms 이내. 0:없음/1:1단계/2:2단계/3:3단계 |
| | | | | | 2~3 | gRoadZone (2bit) | | | | Tx | | Rx | Rx | Rx | Rx | Rx | | 0:일반/1:스쿨존/2:고속도로/3:IC출구 |
| | | | | | 4~6 | gWarningType (3bit) | | | | Tx | | Rx | Rx | Rx | Rx | Rx | | bit0:A그룹/bit1:B그룹/bit2:OTA조건 |
| | | | | | 7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x210 | Cluster_Warning | 0 | 경고등 상태 | 0~1 | WarnLampLevel (2bit) | | | | | | Tx | | | | | | Cluster_ECU Tx. 0:소등/1:황색/2:적색 |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x220 | Ambient_Control | 0 | 앰비언트 패턴 제어 | 0~2 | AmbientMode (3bit) | | | | Tx | | | Rx | | | | | 0:OFF/1:경고RED/2:ORANGE파동/3:방향안내/4:IC흐름/5:사용자정의 |
| | | | | | 3~5 | AmbientColor (3bit) | | | | Tx | | | Rx | | | | | 0:OFF/1:RED/2:ORANGE/3:BLUE/4:WHITE/5~7:기타 |
| | | | | | 6~7 | AmbientPattern (2bit) | | | | Tx | | | Rx | | | | | 0:고정/1:점멸/2:파동/3:흐름 |
| | | | 1 | | 0~7 | AmbientSpeed (8bit, ms/cycle) | | | | Tx | | | Rx | | | | | 점멸/파동 주기 (200ms~2000ms) |
| CAN-HS | 0x230 | Sound_Control | 0 | 경고음 제어 | 0~1 | SoundAlert (2bit) | | | | Tx | | | | Rx | | | | 0:OFF/1:1단계/2:2단계/3:3단계(긴급) |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x240 | IVI_Status | 0 | IVI OTA 팝업 제어 | 0~1 | OTA_PopupTrigger (2bit) | | | | Tx | | | | | Rx | | | 0:없음/1:Level1제안/2:Level2제안 |
| | | | | | 2~3 | OTA_SubscriptionLevel (2bit) | | | | Tx | | | | | Rx | | | 현재 구독 레벨 |
| | | | | | 4~7 | OTA_Progress (4bit, ×6.25%) | | | | Tx | | | | | Rx | | | OTA 진행률 |
| CAN-HS | 0x250 | Door_Control | 0 | 도어/미러 제어 | 0 | DoorLockCmd (1bit) | | | | Tx | | | | | | Rx | | 1: 3초 도어 잠금 (3단계 물리 개입) |
| | | | | | 1 | MirrorLED (1bit) | | | | Tx | | | | | | Rx | | 1: 미러 LED 점멸 |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-LS | 0x7DF | UDS_Request | 0 | UDS 서비스 요청 | 0~7 | ServiceID | | | | Rx | Rx→Tx | | | | | | Tx | 0x10/0x27/0x34/0x36/0x37 |
| | | | 1 | | 0~7 | SubFunction | | | | Rx | Rx→Tx | | | | | | Tx | 세션 유형 / Security Access 서브 |
| | | | 2~7 | | 0~7 | DataRecord (6 bytes) | | | | Rx | Rx→Tx | | | | | | Tx | 서비스별 파라미터 |
| CAN-LS | 0x7E8 | UDS_Response | 0 | UDS 서비스 응답 | 0~7 | ResponseCode | | | | Tx | | | | | | | Rx | 0x50/0x67/0x74/0x76/0x77/0x7F |
| | | | 1~7 | | 0~7 | ResponseData (7 bytes) | | | | Tx | | | | | | | Rx | 서비스별 응답 데이터 |
| DoIP | 0xE001 | DoIP_RoutingActivation | - | DoIP 경로 활성화 | - | RoutingActivationType | | | | | Rx | | | | | | Tx | OTA_Server → CGW 경로 요청 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
