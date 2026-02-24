# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 — 소프트웨어 아키텍처 설계 (인터페이스 명세)
**ASPICE Reference**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, BP4: 일관성 확보)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 하단 — SWE.2 통신 명세 | `05_Unit_Test.md` (SWE.4) | `0302_NWflowDef.md` | `0304_System_Variables.md` |

**DBC 연관**: CAN 메시지 Identifier/DLC/Signal은 `project.dbc`와 직접 대응. sysvar 신호는 CANoe System Variables(`project.sysvars`)로 구현.

---

| Message | Identifier | DLC | Signal | Signal Bit Position | Data 설명 | Data 범위 | Data 사용 |
|---------|-----------|-----|--------|-------------------|---------|---------|---------|
| Vehicle_Speed | 0x100 (CAN-LS) | 4 | gVehicleSpeed | 0~7 (8bit) | 차량 속도 | 0~200 km/h | WDM_ECU 과속 판단. gRoadZone별 기준: 일반 80 / 스쿨존 30 / 고속도로 110 km/h. (→ Req_001) |
| | | | gAccelValue | 8~15 (8bit signed) | 가속도 | -10~10 m/s² | WDM_ECU 급가속 판단. > 3.5 m/s² 시 gAccelCount++. (→ Req_002) |
| | | | gBrakeValue | 16~23 (8bit) | 제동 감속도 | 0~10 m/s² | WDM_ECU 급제동 판단. > 4.0 m/s² 시 이벤트 발생. (→ Req_003) |
| | | | OverspeedFlag | 24 (1bit) | 과속 플래그 | 0~1 | WDM_ECU 과속 이벤트 직접 수신. |
| | | | (Reserved) | 25~31 | — | — | — |
| Steering_Status | 0x110 (CAN-LS) | 2 | SteeringInput | 0 (1bit) | 조향 입력 여부 | 0:미입력 / 1:입력 | WDM_ECU 경고 해제 판단. (→ Req_010) |
| | | | gLaneChangeAlert | 1 (1bit) | 급차선변경 감지 | 0:정상 / 1:감지 | WDM_ECU B그룹 감지. (→ Req_005) |
| | | | SteeringAngleRate | 2~7 (6bit) | 조향각 속도 | 0~63 °/s | 50°/s 초과 시 gLaneChangeAlert = 1 |
| | | | (Reserved) | 8~15 | — | — | — |
| LDW_Status | 0x120 (CAN-LS) | 1 | gLaneDeparture | 0 (1bit) | 차선이탈 감지 | 0:정상 / 1:이탈 | WDM_ECU B그룹 감지. (→ Req_004) |
| | | | (Reserved) | 1~7 | — | — | — |
| WDM_Warning | 0x200 (CAN-HS) | 2 | gWarningLevel | 0~1 (2bit) | 경고 단계 | 0:없음 / 1:1단계 / 2:2단계 / 3:3단계 | 출력 ECU 전체 수신. FTTI ≤50ms. (→ Req_006~008) |
| | | | gRoadZone | 2~3 (2bit) | 도로 구간 | 0:일반 / 1:스쿨존 / 2:고속도로 / 3:IC출구 | Ambient_ECU 구간별 동작 연동. (→ Req_011) |
| | | | gWarningType | 4~6 (3bit) | 경고 원인 비트마스크 | bit0:A그룹 / bit1:B그룹 / bit2:OTA조건 | 원인 추적용. |
| | | | (Reserved) | 7~15 | — | — | — |
| Cluster_Warning | 0x210 (CAN-HS) | 1 | WarnLampLevel | 0~1 (2bit) | 경고등 레벨 | 0:소등 / 1:황색 / 2:적색 | Cluster_ECU Tx. (→ Req_006~007) |
| | | | (Reserved) | 2~7 | — | — | — |
| Ambient_Control | 0x220 (CAN-HS) | 2 | AmbientMode | 0~2 (3bit) | 앰비언트 동작 모드 | 0:OFF / 1:경고RED / 2:ORANGE파동 / 3:방향안내 / 4:IC흐름 | WDM_ECU Tx → Ambient_ECU Rx. (→ Req_012~014) |
| | | | AmbientColor | 3~5 (3bit) | 앰비언트 색상 | 0:OFF / 1:RED / 2:ORANGE / 3:BLUE / 4:WHITE | 색상 코드. |
| | | | AmbientPattern | 6~7 (2bit) | 점등 패턴 | 0:고정 / 1:점멸 / 2:파동 / 3:흐름 | 패턴 유형. |
| | | | AmbientSpeed | 8~15 (8bit) | 주기 속도 | 1~255 (×10ms) | 점멸/파동 주기. 20=200ms(빠름). |
| Sound_Control | 0x230 (CAN-HS) | 1 | SoundAlert | 0~1 (2bit) | 경고음 레벨 | 0:OFF / 1:1단계 / 2:2단계 / 3:긴급 | WDM_ECU Tx → Sound_ECU Rx. |
| | | | (Reserved) | 2~7 | — | — | — |
| IVI_Status | 0x240 (CAN-HS) | 1 | OTA_PopupTrigger | 0~1 (2bit) | OTA 팝업 트리거 | 0:없음 / 1:Level1제안 / 2:Level2제안 | WDM_ECU Tx → IVI_ECU Rx. (→ Req_008, Req_015~016) |
| | | | OTA_SubscriptionLevel | 2~3 (2bit) | 현재 구독 레벨 | 0:기본 / 1:Level1 / 2:Level2 | 구독 상태 표시. |
| | | | OTA_Progress | 4~7 (4bit) | OTA 진행률 | 0~15 (×6.25%) | 전송 블록 진행 상태. |
| Door_Control | 0x250 (CAN-HS) | 1 | DoorLockCmd | 0 (1bit) | 도어 잠금 명령 | 0:정상 / 1:3초 잠금 | WDM_ECU Tx → Door_ECU Rx. 3단계 물리 개입. |
| | | | MirrorLED | 1 (1bit) | 미러 LED | 0:OFF / 1:점멸 | 경고 시각화. |
| | | | (Reserved) | 2~7 | — | — | — |
| UDS_Request | 0x7DF (CAN-LS) | 8 | ServiceID | 0~7 | UDS 서비스 식별자 | 0x10/0x27/0x34/0x36/0x37 | OTA_Server → WDM_ECU 요청 |
| | | | SubFunction | 8~15 | 서비스 서브 기능 | 0x01/0x02/0x03/0x01/0x11 | 세션 유형 / Security Level / Block Sequence |
| | | | DataRecord | 16~63 | 데이터 레코드 (6 bytes) | 가변 | 서비스별 파라미터 |
| UDS_Response | 0x7E8 (CAN-LS) | 8 | ResponseCode | 0~7 | 응답 코드 | 0x50/0x67/0x74/0x76/0x77/0x7F | WDM_ECU → OTA_Server 응답 |
| | | | MaxBlockLength | 8~23 | 최대 블록 길이 | 0~65535 | 0x34 요청 응답 시 전달 |
| | | | ResponseData | 24~63 | 응답 데이터 (5 bytes) | 가변 | 서비스별 응답 데이터 |

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
