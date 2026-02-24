# 단위 테스트 (Unit Test)

> SDV 기반 차량 경험(Experience) 플랫폼 — 노드별 단위 테스트

---

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|------|------|--------|---------|----------|--------|------|
| Vehicle_ECU | 입력 | 차속 CAN-LS 전송 | gVehicleSpeed 초기값 60 km/h → CAN-LS 0x100 Byte 0에 100ms 주기 WDM_ECU 전송 확인 | | | |
| Vehicle_ECU | 입력 | 과속 플래그 설정 | gVehicleSpeed = 85 km/h (gRoadZone=0, 기준 80) → OverspeedFlag = 1 자동 설정 + 0x100 Byte 3 Bit 0 전송 확인 | | | |
| Vehicle_ECU | 입력 | 급가속 시뮬레이션 | Vehicle::accelValue = 4.0 m/s² 주입 → CAN-LS 0x100 Byte 1 전송 → WDM_ECU A그룹 플래그 설정 확인 | | | |
| Vehicle_ECU | 입력 | 급제동 시뮬레이션 | Vehicle::brakeValue = 5.0 m/s² 주입 → CAN-LS 0x100 Byte 2 전송 → WDM_ECU A그룹 플래그 설정 확인 | | | |
| MDPS_ECU | 입력 | 조향 신호 CAN-LS 전송 | SteeringInput / gLaneChangeAlert → CAN-LS 0x110 Byte 0 Bit 0/1에 100ms 주기 전송 확인 | | | |
| MDPS_ECU | 입력 | 핸들 입력 해제 트리거 | MDPS::steeringInput = 1 → 0x110 Bit 0 = 1 → WDM_ECU Level 3 경고 해제 확인 | | | |
| MDPS_ECU | 입력 | 급차선변경 감지 | LDW::laneChangeAlert = 1 → 0x110 Bit 1 = 1 → WDM_ECU B그룹 플래그 설정 확인 | | | |
| LDW_ECU | 입력 | 차선이탈 CAN-LS 전송 | gLaneDeparture → CAN-LS 0x120 Byte 0 Bit 0에 100ms 주기 전송 확인 | | | |
| LDW_ECU | 입력 | 차선이탈 감지 | LDW::laneDeparture = 1 → 0x120 Bit 0 = 1 → WDM_ECU B그룹 플래그 설정 확인 | | | |
| WDM_ECU | 판단 | Level 1 경고 발령 (A단독) | OverspeedFlag = 1 수신 → gWarningLevel = 1 → WDM_Warning(0x200) Bit 0~1 = 1 CAN-HS 전송. 50ms 이내. | | | |
| WDM_ECU | 판단 | Level 1 경고 발령 (B단독) | gLaneDeparture = 1 수신 → gWarningLevel = 1 → WDM_Warning(0x200) Bit 0~1 = 1. 50ms 이내. | | | |
| WDM_ECU | 판단 | Level 2 경고 발령 (A+B) | A그룹 AND B그룹 동시 감지 → gWarningLevel = 2 → 0x200 Bit 0~1 = 2 전송 확인 | | | |
| WDM_ECU | 판단 | Level 3 경고 발령 (gCrashEvent) | gCrashEvent = 1 주입 → gWarningLevel = 3 → 0x200 Bit 0~1 = 3 전송 확인 | | | |
| WDM_ECU | 판단 | Level 1 자동 소거 | gWarningLevel = 1 발령 후 2초 경과 → gWarningLevel = 0 자동 초기화 확인 | | | |
| WDM_ECU | 해제 | Level 3 해제 (응시 복귀) | gWarningLevel = 3 상태에서 Driver::gazeActive 0→1 전환 → gWarningLevel = 0 초기화 확인 | | | |
| WDM_ECU | 해제 | Level 3 해제 (핸들 입력) | gWarningLevel = 3 상태에서 MDPS::steeringInput = 1 → gWarningLevel = 0 초기화 확인 | | | |
| WDM_ECU | 구간 | gRoadZone 구간 적용 | gRoadZone = 1(스쿨존) 설정 → 과속 기준 30 km/h 적용. gVehicleSpeed = 35 → OverspeedFlag = 1 확인 | | | |
| WDM_ECU | 구간 | 고속도로 핸들 미입력 타이머 | gRoadZone = 2 + SteeringInput = 0 지속 → 10초 후 Ambient ORANGE 파동 + 진동 발령 확인 | | | |
| CGW | 라우팅 | CAN-LS→HS 라우팅 | CAN-LS 0x100~0x120 수신 → CAN-HS WDM_ECU 전달 지연 ≤ 5ms 확인 | | | |
| Cluster_ECU | 출력 | Level 1 황색 경고등 | WDM_Warning(gWarningLevel=1) 수신 → Cluster_Warning 0x210 WarnLampLevel = 1 황색. 50ms 이내. | | | |
| Cluster_ECU | 출력 | Level 2 적색 경고등 | WDM_Warning(gWarningLevel=2) 수신 → WarnLampLevel = 2 적색 확인 | | | |
| Cluster_ECU | 출력 | Level 0 소등 | gWarningLevel = 0 수신 → WarnLampLevel = 0 소등 확인 | | | |
| Ambient_ECU | 출력 | 스쿨존 RED 점멸 | AmbientMode = 1 수신 → RED 200ms 주기 점멸. gRoadZone = 1 과속 시 WDM_ECU가 설정. | | | |
| Ambient_ECU | 출력 | 고속도로 ORANGE 파동 | AmbientMode = 2 수신 → ORANGE 1초 주기 파동. gRoadZone = 2 핸들 미입력. | | | |
| Ambient_ECU | 출력 | IC출구 방향 안내 | AmbientMode = 4 수신 → gNavDirection에 따라 좌/우 방향 흐름 애니메이션. gRoadZone = 3. | | | |
| Sound_ECU | 출력 | 단계별 경고음 | SoundAlert = 1 → 단발 "띠딩!" / SoundAlert = 2 → 연속음(500ms) / SoundAlert = 3 → 긴급음(지속) 확인 | | | |
| IVI_ECU | 출력 | 경고 정보 표시 | WarningDisplay = 1(주의) / 2(경고) / 3(긴급) 수신 시 해당 메시지 팝업 표시 확인 | | | |
| IVI_ECU | 출력 | OTA 적용 결과 팝업 | CAN_OTA_Applied(0x600) ApplySuccess = 1 수신 → "Drive Coach 적용 완료" 팝업 표시 확인 | | | |
| OTA_Server | OTA | P 기어 조건 확인 | gGearP = 0 상태에서 구독 버튼 클릭 → ETH_OTA_Param 전송 안 됨. gGearP = 1 상태에서만 전송 확인 | | | |
| OTA_Server | OTA | Drive Coach 파라미터 전송 | [Drive Coach 설치] 클릭 → ETH_OTA_Param Port 6000, Byte 0=0x01, Byte 1=1(NoviceMode), Byte 2=100(SpeedLimit), Byte 3=70(TorqueLimit), Byte 4=1(LDWSensitivity), Byte 5=0, Byte 7=CRC8 전송 확인 | | | |
| OTA_Server | OTA | Seasonal Theme 파라미터 전송 | [Seasonal Theme 동의] 클릭 → ETH_OTA_Param Byte 0=0x02, Byte 5=ThemeID(1~4), 나머지 파라미터=0 전송 확인 | | | |
| OTA_ECU | OTA | CRC8 검증 통과 | 정상 ETH_OTA_Param 수신 → CRC8 Byte 7 = XOR(Byte 0~6) 일치 확인 → sysvar 업데이트 → CAN_OTA_Applied(0x600) ApplySuccess=1 전송 | | | |
| OTA_ECU | OTA | CRC8 검증 실패 복구 | 의도적 CRC8 오류 주입 → 파라미터 미적용 → CAN_OTA_Applied ApplySuccess=0 전송 → 이전 sysvar 그대로 유지 확인 | | | |
| OTA_ECU | OTA | P 기어 이탈 시 세션 중단 | ETH_OTA_Param 수신 중 gGearP = 0 전환 → OTA 세션 즉시 중단 + 파라미터 미적용 확인 | | | |
