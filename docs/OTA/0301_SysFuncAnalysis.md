# 시스템 기능 분석 (System Function Analysis)

> SDV 기반 차량 경험(Experience) 플랫폼 — ECU별 기능 상세

---

| 노드 | 기능 상세 | 비고 |
|------|---------|------|
| | | **입력층 A — CAN-LS (125 kbps)** |
| Vehicle_ECU | gVehicleSpeed(0~200 km/h) / gAccelValue(-10~10 m/s²) / gBrakeValue(0~10 m/s²)를 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 전송. 과속 기준은 gRoadZone에 따라 동적 변경. | 입력층 A. Req_B01 대응. |
| MDPS_ECU | SteeringInput(1bit) / gLaneChangeAlert(1bit) / SteeringAngleRate(°/s)를 CAN-LS 0x110으로 100ms 주기 전송. 조향각속도 > 50°/s 시 gLaneChangeAlert = 1 자동 설정. | 입력층 B + 해제층. Req_B02 대응. |
| LDW_ECU | gLaneDeparture(1bit)를 CAN-LS 0x120으로 100ms 주기 전송. | 입력층 B. Req_B03 대응. |
| | | **판단층 — CAN-HS (500 kbps)** |
| WDM_ECU | CAN-LS 입력 신호 수신 → Rule-Based 판단 → gWarningLevel(0~3) 설정 → 출력 ECU 제어 명령 CAN-HS 전송. A단독 OR B단독 → Level 1 / A AND B → Level 2 / gCrashEvent = 1 → Level 3. gRoadZone별 임계값 적용. FTTI ≤ 50ms. | 판단층 핵심. Req_B04~B09 대응. |
| | | **Gateway** |
| CGW | CAN-LS 입력 신호(0x100~0x120) → CAN-HS WDM_ECU 라우팅. 지연 ≤ 5ms. | Req_B01~B03 라우팅. |
| | | **출력층 — CAN-HS (500 kbps)** |
| Cluster_ECU | WDM_Warning(0x200) 수신 → Level 1: 황색(WarnLampLevel=1) / Level 2: 적색(WarnLampLevel=2) / Level 3: 적색 점멸 / Level 0: 소등. 활성화 ≤ 50ms. | Req_B10 대응. |
| Ambient_ECU | Ambient_Control(0x220) 수신 → AmbientMode별 패턴 출력. 스쿨존(gRoadZone=1) 과속: RED 점멸(200ms) / 고속도로(gRoadZone=2) 핸들 미입력: ORANGE 파동(1초) / IC출구(gRoadZone=3): 방향 안내 흐름. 경고 시 오버라이드 우선. | 준영 담당. Req_B12, Z02~Z04 대응. |
| Sound_ECU | Sound_Control(0x230) 수신 → Level 1: 단발 "띠딩!" / Level 2: 연속음(500ms) / Level 3: 긴급음(지속). | Req_B11 대응. |
| IVI_ECU | IVI_Status(0x240) 수신 → 경고 정보 표시. CAN_OTA_Applied(0x600) 수신 → 구독 결과 팝업 표시. | 성현 담당. Req_B13, O01~O05 대응. |
| | | **OTA Domain — Ethernet UDP** |
| OTA_Server | Panel 구독 버튼 클릭 → gGearP = 1 확인 → ETH_OTA_Param(UDP Port 6000, 8 bytes) 전송. Drive Coach(PackageID=0x01): NoviceMode + SpeedLimit + TorqueLimit + LDWSensitivity 포함. Seasonal Theme(PackageID=0x02): ThemeID 포함. | 성현 담당. Req_O01, O03 대응. |
| OTA_ECU | ETH_OTA_Param 수신 → CRC8 검증 → 통과: sysvar 업데이트 + CAN_OTA_Applied(0x600, ApplySuccess=1) 전송 / 실패: 미적용 + CAN_OTA_Applied(ApplySuccess=0) 전송. | Req_O01, O03, O05 대응. |
| | | **해제층** |
| 응시 복귀 (sysvar) | sysvar::Driver::GazeActive 0→1 전환 → WDM_ECU gWarningLevel = 0 초기화. Level 3 경고 전용. Panel Button 주입. | 라엘 담당. Req_B15 대응. |
| 핸들 입력 (MDPS_ECU) | SteeringInput = 1 수신 → WDM_ECU gWarningLevel = 0 초기화. Level 3 경고 전용. | 현준 담당. Req_B16 대응. |
| | | **CANoe Panel** |
| CANoe Panel | gRoadZone 버튼(4개) / 속도·가속도 TrackBar / 차선이탈·급차선변경 Switch / GazeActive·SteeringInput·gCrashEvent Button / OTA 구독 버튼(Drive Coach / Seasonal Theme) / 상태 Indicator | SIL 사용자 인터페이스 전체. |
