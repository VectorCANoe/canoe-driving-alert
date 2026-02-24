# SW 구현 명세 (Software Implementation Specification)

> SDV 기반 차량 경험(Experience) 플랫폼 — CAPL 노드 구현 상세

**구현 파일**: `canoe/nodes/` (CAPL) · `canoe/test_modules/` (Test CAPL) · **DBC**: `canoe/databases/project.dbc`

---

## 1. CAPL 노드 구성

| 노드 파일 | 담당 ECU | 위치 |
|----------|---------|------|
| `Vehicle_ECU.can` | 차속/가속도/제동 신호 생성 및 CAN-LS 전송 | `canoe/nodes/Vehicle_ECU.can` |
| `MDPS_ECU.can` | 조향 입력/급차선변경 신호 생성 및 CAN-LS 전송 | `canoe/nodes/MDPS_ECU.can` |
| `LDW_ECU.can` | 차선이탈 신호 생성 및 CAN-LS 전송 | `canoe/nodes/LDW_ECU.can` |
| `WDM_ECU.can` | Rule-Based 판단 → 경고 단계 설정 → 출력 ECU 제어 | `canoe/nodes/WDM_ECU.can` |
| `CGW.can` | CAN-LS→CAN-HS 라우팅 | `canoe/nodes/CGW.can` |
| `Cluster_ECU.can` | 경고등 활성화/소등 | `canoe/nodes/Cluster_ECU.can` |
| `Ambient_ECU.can` | 앰비언트 패턴 제어 | `canoe/nodes/Ambient_ECU.can` |
| `Sound_ECU.can` | 단계별 경고음 출력 | `canoe/nodes/Sound_ECU.can` |
| `IVI_ECU.can` | 경고 표시 / OTA 구독 결과 팝업 | `canoe/nodes/IVI_ECU.can` |
| `OTA_Server.can` | SOTA 파라미터 패킷(ETH_OTA_Param) 생성 및 Ethernet UDP 전송 | `canoe/nodes/OTA_Server.can` |
| `OTA_ECU.can` | ETH_OTA_Param 수신 → CRC8 검증 → sysvar 업데이트 → CAN_OTA_Applied 전송 | `canoe/nodes/OTA_ECU.can` |

---

## 2. Vehicle_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tVehicleTx` | 100ms 주기 CAN-LS 0x100 Vehicle_Speed 메시지 전송 | `Vehicle::vehicleSpeed`, `Vehicle::accelValue`, `Vehicle::brakeValue` | In_Test_01, In_Test_02 |
| `void sendVehicleSpeed()` | gVehicleSpeed/gAccelValue/gBrakeValue/OverspeedFlag 조립 후 CAN-LS 전송 | Vehicle_Speed 0x100 (4 bytes) | In_Test_01 |
| `on sysvar Vehicle::vehicleSpeed` | Panel TrackBar 변경 시 즉시 CAN-LS에 반영. gRoadZone 기준 대비 OverspeedFlag 자동 계산. | `Vehicle::vehicleSpeed`, `WDM::roadZone` | In_Test_01 |
| `on sysvar Vehicle::accelValue` | 급가속 주입 시 즉시 반영. > 3.5 m/s² 시 WDM_ECU 이벤트. | `Vehicle::accelValue` | In_Test_02 |

---

## 3. MDPS_ECU.can / LDW_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on timer tMDPSTx` | 100ms 주기 CAN-LS 0x110 Steering_Status 전송 | `MDPS::steeringInput`, `LDW::laneChangeAlert` | In_Test_03, In_Test_06 |
| `on sysvar MDPS::steeringInput` | Panel Button 변경 시 즉시 전송. 1 감지 시 WDM_ECU 경고 해제. | `MDPS::steeringInput` | In_Test_06 |
| `on timer tLDWTx` | 100ms 주기 CAN-LS 0x120 LDW_Status 전송 | `LDW::laneDeparture` | In_Test_03 |
| `on sysvar LDW::laneDeparture` | Panel Button 변경 시 즉시 전송. 1 감지 시 WDM_ECU B그룹 감지. | `LDW::laneDeparture` | In_Test_03 |

---

## 4. WDM_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on message Vehicle_Speed` | CAN-LS 0x100 수신 → 과속/급가속/급제동 이벤트 판단 | `Vehicle::vehicleSpeed` | In_Test_01, In_Test_02 |
| `on message Steering_Status` | CAN-LS 0x110 수신 → 급차선변경/핸들입력 판단. SteeringInput=1 시 Level 3 경고 해제. | `MDPS::steeringInput`, `LDW::laneChangeAlert` | In_Test_03, In_Test_06 |
| `on message LDW_Status` | CAN-LS 0x120 수신 → 차선이탈 감지 | `LDW::laneDeparture` | In_Test_03 |
| `void evaluateWarning()` | Rule-Based 판단. A단독→1단계, B단독→1단계, A AND B→2단계, gCrashEvent=1→3단계. gWarningLevel 설정. | `WDM::warningLevel`, `WDM::warningType` | In_Test_01~04 |
| `void sendWarning()` | gWarningLevel 기반 WDM_Warning(0x200) + Ambient/Sound/IVI 제어 명령 CAN-HS 전송. | 0x200/0x220/0x230/0x240 | In_Test_01~04 |
| `on sysvar Driver::gazeActive` | GazeActive 0→1 전환 → Level 3 경고 해제(gWarningLevel=0). | `Driver::gazeActive` | In_Test_05 |
| `on timer tSteerTimer` | gRoadZone=2 핸들 미입력 타이머. 10초 초과 시 진동 경고 발령. | `WDM::steerTimer` | In_Test_08 |
| `void applyRoadZone()` | gRoadZone 변경 시 과속 임계값 및 앰비언트 동작 즉시 적용. | `WDM::roadZone` | In_Test_07~09 |
| `on message CAN_OTA_Applied` | 0x600 ApplySuccess=1 수신 → Drive Coach 파라미터(speedLimit/torqueLimit/ldwSensitivity) 즉시 적용. | `OTA::noviceMode`, `OTA::speedLimit` | In_Test_10, 12 |

---

## 5. CGW.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on message CAN1.Vehicle_Speed` | CAN-LS(0x100) 수신 → CAN-HS WDM_ECU 라우팅 (지연 ≤ 5ms) | `Vehicle_Speed` | In_Test_01 |
| `on message CAN1.Steering_Status` | CAN-LS(0x110) 수신 → CAN-HS 라우팅 | `Steering_Status` | In_Test_03 |
| `on message CAN1.LDW_Status` | CAN-LS(0x120) 수신 → CAN-HS 라우팅 | `LDW_Status` | In_Test_03 |

---

## 6. Ambient_ECU.can — 주요 함수/이벤트

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on message Ambient_Control` | CAN-HS(0x220) 수신 → AmbientMode별 패턴 실행 | `Ambient::ambientMode`, `Ambient::ambientColor` | In_Test_07~09 |
| `void runSchoolZoneAlert()` | AmbientMode=1: RED 빠른 점멸 (200ms 주기). gRoadZone=1 과속 시. | `Ambient::ambientPattern` | In_Test_07 |
| `void runHighwayWarning()` | AmbientMode=2: ORANGE 파동 (1초 주기). gRoadZone=2 핸들 미입력 10초. | `Ambient::ambientPattern` | In_Test_08 |
| `void runICDirectional()` | AmbientMode=4: gNavDirection 방향 흐름 애니메이션. gRoadZone=3 IC출구 근접. | `Ambient::ambientPattern`, `WDM::navDirection` | In_Test_09 |

---

## 7. OTA_Server.can / OTA_ECU.can — 주요 함수/이벤트

**OTA_Server.can (SOTA 파라미터 전송)**

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on sysvar OTA::packageID` | 구독 버튼 클릭(packageID 설정) → gGearP = 1 확인 → `sendOTA_Param()` 호출 | `OTA::packageID`, `Vehicle::gGearP` | In_Test_10, 12 |
| `void sendOTA_Param()` | ETH_OTA_Param(Port 6000, 8 bytes) 조립 및 Ethernet UDP 전송. Byte 0~6 세팅 후 Byte 7=CRC8(XOR 0~6). | `OTA::noviceMode`, `OTA::speedLimit`, `OTA::torqueLimit`, `OTA::themeID` | In_Test_10, 12 |
| `byte calcCRC8(byte[]data, int len)` | Byte 0~6의 XOR 결과 반환. Byte 7에 삽입. | CRC8 계산 | In_Test_10, 12 |

**OTA_ECU.can (파라미터 수신 및 검증)**

| 함수/이벤트 | 설명 | 관련 신호 | 검증 |
|-----------|------|---------|------|
| `on ethFrame Port 6000` | ETH_OTA_Param 수신 → `validateCRC8()` 호출. gGearP = 1 재확인. | `OTA::otaInProgress` | In_Test_10, 12 |
| `void validateCRC8()` | 수신 Byte 7 vs XOR(Byte 0~6) 비교. 일치 → `applyParams()`. 불일치 → `sendApplyResult(0)`. | `OTA::applySuccess` | In_Test_13 |
| `void applyParams()` | sysvar 업데이트: noviceMode / speedLimit / torqueLimit / ldwSensitivity / themeID / subscriptionLevel. 완료 후 `sendApplyResult(1)`. | 전체 OTA sysvar | In_Test_10, 12 |
| `void sendApplyResult(byte success)` | CAN_OTA_Applied(0x600): Bit 0~1=PackageID, Bit 2=ApplySuccess 전송. | CAN_OTA_Applied 0x600 | In_Test_10, 12, 13 |
| `on sysvar Vehicle::gGearP` | OTA 세션 중 gGearP = 0 감지 시 세션 즉시 중단 + 파라미터 미적용 + IVI 알림. | `OTA::otaInProgress` | In_Test_13 |

---

## 8. 테스트 모듈 구성

| 테스트 모듈 폴더 | 내용 | 대응 테스트 |
|--------------|------|-----------|
| `TC_A_SpeedInput/` | 과속/급가속/급제동 감지 → WDM_ECU Level 1 경고 자동화 | In_Test_01, 02 |
| `TC_B_DirectionInput/` | 차선이탈/급차선변경 감지 → WDM_ECU Level 1 경고 | In_Test_03 |
| `TC_W_Warning/` | Level 2(A+B) / Level 3(gCrashEvent) / 경고 해제(응시/핸들) 검증 | In_Test_04, 05, 06 |
| `TC_Z_ZoneAmbient/` | gRoadZone 1~3 앰비언트 동작 검증 | In_Test_07, 08, 09 |
| `TC_O_OTA/` | SOTA 파라미터 전송 / CRC8 검증 / P 기어 세션 중단 검증 | In_Test_10, 12, 13 |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 (Scene.B1~Z4~O5) | Scene.B~Z~O |
