# 가상노드 Simulator (입출력 기능) — Function Definition

> SDV 기반 차량 경험(Experience) 플랫폼 — 가상 노드별 기능 정의

---

| 가상노드 Simulator | 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------------------|------|--------|---------|------|------|
| Panel | 입력 | 차속 조절 (TrackBar) | gVehicleSpeed(0~200 km/h) 조절. 제한속도 초과 시 WDM_ECU 과속 이벤트 감지. gRoadZone별 기준 자동 적용. | CAN-LS 0x100 연동 | Scene.B4~B6 |
| Panel | 입력 | 급가속 주입 (Button) | gAccelValue > 3.5 m/s² 강제 주입 → WDM_ECU A그룹 플래그 설정. | Switch/Indicator | Scene.B5 |
| Panel | 입력 | 차선이탈 주입 (Button) | sysvar::LDW::laneDeparture = 1 주입 → WDM_ECU B그룹 감지. | Switch/Indicator | Scene.B7 |
| Panel | 입력 | gRoadZone 설정 (Button×4) | 버튼 4개로 gRoadZone(0:일반/1:스쿨존/2:고속도로/3:IC출구) 설정. | WDM_ECU 즉시 반영 | Scene.Z1~Z4 |
| Panel | 입력 | 응시 복귀 주입 (Button) | sysvar::Driver::GazeActive 0→1 전환 → Level 3 경고 해제. (라엘) | Switch/Indicator | Scene.B11 |
| Panel | 입력 | 핸들 입력 주입 (Button) | sysvar::MDPS::SteeringInput = 1 주입 → Level 3 경고 해제. (현준) | Switch/Indicator | Scene.B12 |
| Panel | 입력 | 충돌 이벤트 (Button) | gCrashEvent = 1 → gWarningLevel = 3 강제 발령. | Level 3 트리거 | Scene.B10 |
| Panel | 입력 | OTA 구독 버튼 (Button×2) | [Drive Coach 설치] / [Seasonal Theme 동의] 버튼 → OTA_Server OTA_Param 전송 트리거. P 기어 상태에서만 활성화. | Switch/Indicator | Scene.O1, O3 |
| Panel | 출력 | gWarningLevel 표시 | gWarningLevel(0~3) 현재값 Indicator 출력. | 숫자 + 색상 표시 | 전체 |
| Panel | 출력 | Cluster 경고등 | 황색(Level 1) / 적색(Level 2/3) / 소등(Level 0). | LED Indicator | Scene.B4~B10 |
| Panel | 출력 | Ambient 상태 표시 | AmbientMode / AmbientColor / AmbientPattern 현재값 Indicator 출력. | Switch/Indicator | Scene.Z1~Z4 |
| Panel | 출력 | OTA 진행 상태 | ETH_OTA_Param 수신 중 → CRC8 검증 → 적용 완료 / 실패 표시. | Indicator | Scene.O1~O5 |
| Vehicle_ECU | ECU 동작 | 차속·가속·제동 보고 | gVehicleSpeed / gAccelValue / gBrakeValue를 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 전송. | CAPL on timer 100ms | Scene.B3~B6 |
| MDPS_ECU | ECU 동작 | 조향·급차선변경 보고 | SteeringInput / gLaneChangeAlert를 CAN-LS 0x110으로 100ms 주기 전송. 조향각속도 > 50°/s 시 gLaneChangeAlert = 1. | CAPL on timer 100ms | Scene.B8, B12 |
| LDW_ECU | ECU 동작 | 차선이탈 보고 | gLaneDeparture를 CAN-LS 0x120으로 100ms 주기 전송. | CAPL on timer 100ms | Scene.B7 |
| WDM_ECU | ECU 동작 | 위험 판단 + 경고 발령 | 입력층 신호 수신 → Rule-Based 판단 → gWarningLevel 0~3 설정 → 출력층 ECU 제어 명령 CAN-HS 전송. gRoadZone별 임계값 적용. FTTI ≤ 50ms. | CAPL 핵심 판단 로직 | Scene.B4~B12 |
| CGW | ECU 동작 | CAN-LS→HS 라우팅 | CAN-LS 입력 신호(0x100~0x120) → CAN-HS WDM_ECU 라우팅. 지연 ≤ 5ms. | CAPL on message | 전체 |
| Cluster_ECU | ECU 동작 | 경고등 제어 | WDM_Warning(0x200) 수신 → gWarningLevel에 따라 황색/적색/소등. 활성화 ≤ 50ms. | CAPL on message | Scene.B4~B10 |
| Ambient_ECU | ECU 동작 | 앰비언트 패턴 제어 | Ambient_Control(0x220) 수신 → AmbientMode별 패턴. 스쿨존: RED 점멸 / 고속도로: ORANGE 파동 / IC출구: 방향 흐름 / 경고: 단계별 색상. | CAPL on message | Scene.Z1~Z4, B9 |
| Sound_ECU | ECU 동작 | 경고음 출력 | Sound_Control(0x230) 수신 → Level 1: 단발음 / Level 2: 연속음 / Level 3: 긴급음. | CAPL on message | Scene.B4~B10 |
| IVI_ECU | ECU 동작 | 경고/OTA 팝업 표시 | IVI_Status(0x240) 수신 → 경고 정보 표시. CAN_OTA_Applied(0x600) 수신 → OTA 구독 완료/실패 팝업. | CAPL on message | Scene.O1~O5 |
| OTA_Server | ECU 동작 | SOTA 파라미터 전송 | Panel 구독 버튼 클릭 시 ETH_OTA_Param(UDP Port 6000, 8 bytes) 전송. gGearP = 1 조건 확인 후 전송. Drive Coach(PackageID=0x01) / Seasonal Theme(PackageID=0x02). | Ethernet UDP | Scene.O1~O3 |
| OTA_ECU | ECU 동작 | 파라미터 수신 + 적용 | ETH_OTA_Param 수신 → CRC8 검증 → 통과 시 sysvar 업데이트 → CAN_OTA_Applied(0x600) 전송. 실패 시 미적용 + IVI 오류 알림. | Ethernet → CAN 연동 | Scene.O1~O5 |
| 응시 복귀 (sysvar) | 해제층 | GazeActive 전환 감지 | sysvar::Driver::GazeActive 0→1 전환 시 gWarningLevel = 0 초기화. Level 3 전용. (라엘) | Panel Button 주입 | Scene.B11 |
| 핸들 입력 (MDPS) | 해제층 | SteeringInput 감지 | SteeringInput = 1 수신 시 gWarningLevel = 0 초기화. Level 3 전용. (현준) | MDPS_ECU 신호 | Scene.B12 |
