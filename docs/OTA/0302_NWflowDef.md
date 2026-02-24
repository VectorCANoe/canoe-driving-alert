# 네트워크 플로우 정의 (Network Flow Definition)

> SDV 기반 차량 경험(Experience) 플랫폼 — 버스별 메시지 흐름 매트릭스

---

| Channel | ID hex | Symbolic Name | Byte no. | Function | Bit no. | signal name | Vehicle_ECU | MDPS_ECU | LDW_ECU | WDM_ECU | CGW | Cluster | Ambient | Sound | IVI | OTA_Server | OTA_ECU | [비고] |
|---------|--------|--------------|---------|----------|---------|-------------|:-----------:|:--------:|:-------:|:-------:|:---:|:-------:|:-------:|:-----:|:---:|:----------:|:-------:|--------|
| CAN-LS | 0x100 | Vehicle_Speed | 0 | 차량 속도 보고 | 0~7 | gVehicleSpeed (8bit, km/h) | Tx | | | Rx | Rx | | | | | | | 100ms 주기. gRoadZone별 기준 비교. |
| | | | 1 | 가속도 보고 | 0~7 | gAccelValue (8bit signed, m/s²) | Tx | | | Rx | Rx | | | | | | | 양수: 가속, 음수: 제동. |
| | | | 2 | 제동 감속도 보고 | 0~7 | gBrakeValue (8bit, m/s²) | Tx | | | Rx | Rx | | | | | | | |
| | | | 3 | 과속 플래그 | 0 | OverspeedFlag (1bit) | Tx | | | Rx | Rx | | | | | | | gRoadZone 기준 초과 시 1. |
| CAN-LS | 0x110 | Steering_Status | 0 | 조향 입력 / 급차선변경 | 0 | SteeringInput (1bit) | | Tx | | Rx | Rx | | | | | | | 0:미입력 / 1:입력. 100ms 주기. |
| | | | | | 1 | gLaneChangeAlert (1bit) | | Tx | | Rx | Rx | | | | | | | 조향각속도 > 50°/s 시 1. |
| | | | | | 2~7 | SteeringAngleRate (6bit, °/s) | | Tx | | Rx | Rx | | | | | | | |
| | | | 1 | | 0~7 | (Reserved) | | | | | | | | | | | | |
| CAN-LS | 0x120 | LDW_Status | 0 | 차선이탈 감지 | 0 | gLaneDeparture (1bit) | | | Tx | Rx | Rx | | | | | | | 0:정상 / 1:이탈. 100ms 주기. |
| | | | | | 1~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x200 | WDM_Warning | 0 | 경고 레벨 / 구간 정보 | 0~1 | gWarningLevel (2bit) | | | | Tx | | Rx | Rx | Rx | Rx | | | WDM_ECU Tx. FTTI ≤ 50ms. |
| | | | | | 2~3 | gRoadZone (2bit) | | | | Tx | | Rx | Rx | | Rx | | | 0:일반/1:스쿨존/2:고속도로/3:IC출구. |
| | | | | | 4~6 | gWarningType (3bit) | | | | Tx | | | | | | | | bit0:A그룹/bit1:B그룹. |
| | | | | | 7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x210 | Cluster_Warning | 0 | 경고등 상태 | 0~1 | WarnLampLevel (2bit) | | | | | | Tx | | | | | | 0:소등/1:황색/2:적색. |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x220 | Ambient_Control | 0 | 앰비언트 패턴 제어 | 0~2 | AmbientMode (3bit) | | | | Tx | | | Rx | | | | | 0:OFF/1:경고RED/2:ORANGE파동/3:방향안내/4:IC흐름. |
| | | | | | 3~5 | AmbientColor (3bit) | | | | Tx | | | Rx | | | | | 0:OFF/1:RED/2:ORANGE/3:BLUE/4:WHITE. |
| | | | | | 6~7 | AmbientPattern (2bit) | | | | Tx | | | Rx | | | | | 0:고정/1:점멸/2:파동/3:흐름. |
| | | | 1 | | 0~7 | AmbientSpeed (8bit, ×10ms) | | | | Tx | | | Rx | | | | | 점멸/파동 주기. |
| CAN-HS | 0x230 | Sound_Control | 0 | 경고음 제어 | 0~1 | SoundAlert (2bit) | | | | Tx | | | | Rx | | | | 0:OFF/1:단발/2:연속/3:긴급. |
| | | | | | 2~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x240 | IVI_Status | 0 | IVI 경고/OTA 표시 | 0~1 | WarningDisplay (2bit) | | | | Tx | | | | | Rx | | | 0:정상/1:주의/2:경고/3:긴급. |
| | | | | | 2~3 | gRoadZone (2bit) | | | | Tx | | | | | Rx | | | 구간 정보 표시용. |
| | | | | | 4~7 | (Reserved) | | | | | | | | | | | | |
| CAN-HS | 0x600 | CAN_OTA_Applied | 0 | OTA 파라미터 적용 결과 | 0~1 | PackageID (2bit) | | | | | | | | | Rx | | Tx | 0:없음/1:DriveCoach/2:SeasonalTheme. |
| | | | | | 2 | ApplySuccess (1bit) | | | | | | | | | Rx | | Tx | 0:실패/1:성공. |
| | | | | | 3~7 | (Reserved) | | | | | | | | | | | | |
| Ethernet | Port 6000 | ETH_OTA_Param | 0 | SOTA 파라미터 패킷 | Byte 0 | PackageID (0x01=DriveCoach/0x02=SeasonalTheme) | | | | | | | | | | Tx | Rx | UDP 브로드캐스트. P 기어 조건 후 전송. |
| | | | | | Byte 1 | NoviceMode (0:비활성/1:활성) | | | | | | | | | | Tx | Rx | Drive Coach 초보 모드 플래그. |
| | | | | | Byte 2 | SpeedLimit (km/h, 0=제한없음) | | | | | | | | | | Tx | Rx | Drive Coach: 100 km/h. |
| | | | | | Byte 3 | TorqueLimit (%, 0=제한없음) | | | | | | | | | | Tx | Rx | Drive Coach: 70%. |
| | | | | | Byte 4 | LDWSensitivity (0:기본/1:강화) | | | | | | | | | | Tx | Rx | Drive Coach: 1. |
| | | | | | Byte 5 | ThemeID (0:없음/1:봄/2:여름/3:가을/4:겨울) | | | | | | | | | | Tx | Rx | Seasonal Theme 전용. |
| | | | | | Byte 6 | ApplyCondition (0x01=P기어필수) | | | | | | | | | | Tx | Rx | 적용 전제조건. |
| | | | | | Byte 7 | CRC8 (XOR Byte 0~6) | | | | | | | | | | Tx | Rx | 파라미터 무결성 검증. |
