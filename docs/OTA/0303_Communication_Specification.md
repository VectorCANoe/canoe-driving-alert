# 통신 명세서 (Communication Specification)

> SDV 기반 차량 경험(Experience) 플랫폼 — 메시지/신호 레벨 상세 명세

---

## CAN 통신 명세

| Message | Identifier | DLC | Signal | Signal Bit Position | Data 설명 | Data 범위 | Data 사용 |
|---------|-----------|-----|--------|-------------------|---------|---------|---------:|
| Vehicle_Speed | 0x100 (CAN-LS) | 4 | gVehicleSpeed | 0~7 (8bit) | 차량 속도 | 0~200 km/h | WDM_ECU 과속 판단. gRoadZone별 기준: 일반 80 / 스쿨존 30 / 고속도로 110 km/h. (→ Req_B04) |
| | | | gAccelValue | 8~15 (8bit signed) | 가속도 | -10~10 m/s² | WDM_ECU 급가속 판단. > 3.5 m/s² 시 A그룹 플래그. (→ Req_B05) |
| | | | gBrakeValue | 16~23 (8bit) | 제동 감속도 | 0~10 m/s² | WDM_ECU 급제동 판단. > 4.0 m/s² 시 A그룹 플래그. (→ Req_B06) |
| | | | OverspeedFlag | 24 (1bit) | 과속 플래그 | 0~1 | gRoadZone 기준 초과 시 1. WDM_ECU 직접 수신. |
| | | | (Reserved) | 25~31 | — | — | — |
| Steering_Status | 0x110 (CAN-LS) | 2 | SteeringInput | 0 (1bit) | 조향 입력 여부 | 0:미입력/1:입력 | WDM_ECU 해제 판단 + 고속도로 미입력 타이머. (→ Req_B16, Z03) |
| | | | gLaneChangeAlert | 1 (1bit) | 급차선변경 감지 | 0:정상/1:감지 | WDM_ECU B그룹 플래그. (→ Req_B08) |
| | | | SteeringAngleRate | 2~7 (6bit) | 조향각 속도 | 0~63 °/s | > 50°/s 시 gLaneChangeAlert = 1 자동 설정. |
| | | | (Reserved) | 8~15 | — | — | — |
| LDW_Status | 0x120 (CAN-LS) | 1 | gLaneDeparture | 0 (1bit) | 차선이탈 감지 | 0:정상/1:이탈 | WDM_ECU B그룹 플래그. (→ Req_B07) |
| | | | (Reserved) | 1~7 | — | — | — |
| WDM_Warning | 0x200 (CAN-HS) | 1 | gWarningLevel | 0~1 (2bit) | 경고 단계 | 0:없음/1:1단계/2:2단계/3:3단계 | Cluster_ECU Rx. 경고 단계별 경고등 제어. FTTI ≤ 50ms. (→ Req_B09~B10) |
| | | | gRoadZone | 2~3 (2bit) | 도로 구간 | 0:일반/1:스쿨존/2:고속도로/3:IC출구 | Ambient_ECU 구간별 패턴 연동. (→ Req_Z01) |
| | | | gWarningType | 4~6 (3bit) | 경고 원인 비트마스크 | bit0:A그룹/bit1:B그룹 | 원인 추적용. |
| | | | (Reserved) | 7 | — | — | — |
| Cluster_Warning | 0x210 (CAN-HS) | 1 | WarnLampLevel | 0~1 (2bit) | 경고등 레벨 | 0:소등/1:황색/2:적색 | Cluster_ECU Tx. (→ Req_B10) |
| | | | (Reserved) | 2~7 | — | — | — |
| Ambient_Control | 0x220 (CAN-HS) | 2 | AmbientMode | 0~2 (3bit) | 앰비언트 동작 모드 | 0:OFF/1:경고RED/2:ORANGE파동/3:방향안내/4:IC흐름 | WDM_ECU Tx → Ambient_ECU Rx. (→ Req_B12, Z02~Z04) |
| | | | AmbientColor | 3~5 (3bit) | 앰비언트 색상 | 0:OFF/1:RED/2:ORANGE/3:BLUE/4:WHITE | 색상 코드. |
| | | | AmbientPattern | 6~7 (2bit) | 점등 패턴 | 0:고정/1:점멸/2:파동/3:흐름 | 패턴 유형. |
| | | | AmbientSpeed | 8~15 (8bit) | 주기 속도 | 1~255 (×10ms) | 점멸/파동 주기. 20=200ms(빠름). |
| Sound_Control | 0x230 (CAN-HS) | 1 | SoundAlert | 0~1 (2bit) | 경고음 레벨 | 0:OFF/1:단발/2:연속/3:긴급 | WDM_ECU Tx → Sound_ECU Rx. (→ Req_B11) |
| | | | (Reserved) | 2~7 | — | — | — |
| IVI_Status | 0x240 (CAN-HS) | 1 | WarningDisplay | 0~1 (2bit) | 경고 표시 | 0:정상/1:주의/2:경고/3:긴급 | WDM_ECU Tx → IVI_ECU Rx. (→ Req_B13) |
| | | | gRoadZone | 2~3 (2bit) | 구간 정보 | 0:일반/1:스쿨존/2:고속도로/3:IC출구 | IVI 구간 표시용. |
| | | | gWarningType | 4~6 (3bit) | 경고 원인 비트마스크 | bit0:A그룹/bit1:B그룹 | IVI 경고 원인 표시용. (→ Req_B09) |
| | | | (Reserved) | 7 | — | — | — |
| CAN_OTA_Applied | 0x600 (CAN-HS) | 1 | PackageID | 0~1 (2bit) | 적용된 패키지 | 0:없음/1:DriveCoach/2:SeasonalTheme | OTA_ECU Tx → IVI_ECU Rx + WDM_ECU Rx. (→ Req_O01, O03) |
| | | | ApplySuccess | 2 (1bit) | 적용 성공 여부 | 0:실패/1:성공 | CRC8 검증 결과. |
| | | | (Reserved) | 3~7 | — | — | — |

---

## Ethernet UDP 통신 명세

| Message | Port | Data Length | Signal | Byte Position | Data 설명 | Data 범위 | Data 사용 |
|---------|------|------------|--------|--------------|---------|---------|---------|
| ETH_OTA_Param | 6000 | 8 bytes | PackageID | Byte 0 | 구독 패키지 식별자 | 0x01:DriveCoach / 0x02:SeasonalTheme | OTA_Server Tx → OTA_ECU Rx. P 기어 조건 후 전송. (→ Req_O01, O03) |
| | | | NoviceMode | Byte 1 | 초보 운전 모드 플래그 | 0:비활성 / 1:활성 | Drive Coach 적용 시 1. |
| | | | SpeedLimit | Byte 2 | 최고 속도 제한 | 0~200 (km/h, 0=제한없음) | Drive Coach: 100 km/h. Seasonal Theme: 0. |
| | | | TorqueLimit | Byte 3 | 최대 토크 제한 | 0~100 (%, 0=제한없음) | Drive Coach: 70%. Seasonal Theme: 0. |
| | | | LDWSensitivity | Byte 4 | LDW 경고 민감도 | 0:기본 / 1:강화 | Drive Coach: 1(강화). Seasonal Theme: 0. |
| | | | ThemeID | Byte 5 | 시즌 테마 ID | 0:없음/1:봄/2:여름/3:가을/4:겨울 | Seasonal Theme 전용. Drive Coach: 0. |
| | | | ApplyCondition | Byte 6 | 적용 전제조건 | 0x01=P 기어 필수 | OTA_ECU가 gGearP = 1 확인 후 적용. |
| | | | CRC8 | Byte 7 | 무결성 검증 | 0~255 | Byte 0~6의 XOR 결과값. 불일치 시 파라미터 미적용. (→ Req_O05) |
