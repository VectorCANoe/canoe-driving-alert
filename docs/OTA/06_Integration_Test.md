# 통합 테스트 (Integration Test)

> SDV 기반 차량 경험(Experience) 플랫폼 — 모듈 간 연동 테스트

> 실행 원칙: Base(In_Test_01~06) 전체 Pass 후 TS-준영(In_Test_07~09), TS-성현(In_Test_10~13)을 순서대로 실행한다.

---

## Part 1. Base — 입력층 + 판단층 + 출력층

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 |
|----------|-----------|-----------|---------|--------------|--------|
| In_Test_01 | Req_B04, B09, B10 | 과속 → Level 1 경고 연동 확인 | Vehicle::vehicleSpeed > 80 km/h 주입 → WDM_ECU gWarningLevel = 1 → CAN-HS 0x200 Bit 0~1 = 1 → Cluster 황색 경고등(0x210 WarnLampLevel=1). 50ms 이내. | | |
| In_Test_02 | Req_B05, B06, B09 | 급가속/급제동 → Level 1 경고 연동 확인 | accelValue > 3.5 m/s² 주입 → gWarningLevel = 1. brakeValue > 4.0 m/s² 동일 검증. | | |
| In_Test_03 | Req_B07, B08, B09 | 차선이탈/급차선변경 → Level 1 경고 연동 확인 | LDW::laneDeparture = 1 OR LDW::laneChangeAlert = 1 → gWarningLevel = 1 → Cluster 황색 점등. | | |
| In_Test_04 | Req_B09, B11, B12 | A+B 복합 → Level 2 / gCrashEvent → Level 3 연동 확인 | A(과속) AND B(차선이탈) 동시 주입 → gWarningLevel = 2 → Cluster 적색 + Sound 연속음(0x230 SoundAlert=2) + Ambient AMBER 파동(0x220 AmbientMode=2). gCrashEvent = 1 → gWarningLevel = 3 → Cluster 적색 점멸 + Sound 긴급음(SoundAlert=3) + Ambient RED 점멸(AmbientMode=1). | | |
| In_Test_05 | Req_B15 | 응시 복귀 → Level 3 경고 해제 확인 | gWarningLevel = 3 상태에서 Driver::gazeActive 0→1 전환 → gWarningLevel = 0 → 전 출력층 소거(Cluster 소등/Sound 무음/Ambient OFF). | | |
| In_Test_06 | Req_B16 | 핸들 입력 → Level 3 경고 해제 확인 | gWarningLevel = 3 상태에서 MDPS::steeringInput = 1 주입 → gWarningLevel = 0 → 전 출력층 소거 확인. | | |

---

## Part 2. TS-준영 — 구간 인식 + Ambient 연동

> 전제조건: In_Test_01~06 전체 Pass.

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 |
|----------|-----------|-----------|---------|--------------|--------|
| In_Test_07 | Req_Z01, Z02 | 스쿨존 구간 → 과속 감지 → Ambient RED 점멸 연동 확인 | gRoadZone = 1 설정 → vehicleSpeed = 35 km/h → OverspeedFlag = 1 → WDM_ECU Ambient_Control(0x220) AmbientMode = 1(RED 점멸) 전송 → Ambient_ECU 200ms 주기 RED 점멸 출력 확인. | | |
| In_Test_08 | Req_Z01, Z03 | 고속도로 구간 → 핸들 미입력 10초 → Ambient ORANGE 파동 + 진동 연동 확인 | gRoadZone = 2 + SteeringInput = 0 유지 → 10초 후 Ambient_Control AmbientMode = 2(ORANGE 파동) + 진동 패턴 전송 → Ambient_ECU 출력 확인. SteeringInput = 1 입력 시 즉시 해제 확인. | | |
| In_Test_09 | Req_Z01, Z04 | IC출구 구간 → gNavDirection별 Ambient 방향 안내 확인 | gRoadZone = 3 → WDM_Warning Bit 2~3(gRoadZone=3) + Ambient_Control AmbientMode = 4 전송 → gNavDirection = 0(좌) / 1(우) 설정에 따라 Ambient 방향 흐름 애니메이션 출력 확인. gRoadZone ≠ 3 시 즉시 소거. | | |

---

## Part 3. TS-성현 — SOTA OTA 구독 서비스

> 전제조건: In_Test_01~06 전체 Pass.

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 |
|----------|-----------|-----------|---------|--------------|--------|
| In_Test_10 | Req_O01 | P 기어 → Drive Coach 구독 → 파라미터 즉시 적용 E2E 확인 | gGearP = 1 → [Drive Coach 설치] 클릭 → OTA_Server ETH_OTA_Param(Port 6000, PackageID=0x01) 전송 → OTA_ECU CRC8 검증 통과 → sysvar 업데이트(noviceMode=1, speedLimit=100, torqueLimit=70, ldwSensitivity=1) → CAN_OTA_Applied(0x600 ApplySuccess=1) → IVI "Drive Coach 적용 완료" 팝업 확인. WDM_ECU LDW 민감도 강화 + 속도/토크 제한 즉시 적용 확인. | | |
| In_Test_11 | Req_O02 | Smart Claim → 충돌 이벤트 → Flask 서버 데이터 전송 확인 | Drive Coach 적용 상태에서 gCrashEvent = 1 주입 → Python CANoe COM API HTTP POST 실행 → Flask 서버 수신 확인 → IVI "사고 데이터 전송 완료" 표시 확인. | | |
| In_Test_12 | Req_O03 | Seasonal Theme 구독 → 즉시 적용 E2E 확인 | gGearP = 1 → IVI Seasonal Theme 알림 → 운전자 동의 → OTA_Server ETH_OTA_Param(PackageID=0x02, ThemeID=예: 4/겨울) 전송 → OTA_ECU CRC8 통과 → Ambient 색상 변경 + IVI 배경 즉시 적용 확인. | | |
| In_Test_13 | Req_O04, O05 | P 기어 이탈 → 세션 중단 / CRC8 오류 → 파라미터 미적용 확인 | ① ETH_OTA_Param 수신 중 gGearP = 0 전환 → OTA 세션 즉시 중단, 파라미터 미적용 확인. ② 의도적 CRC8 오류 주입(Byte 7 변조) → OTA_ECU 미적용 + CAN_OTA_Applied ApplySuccess=0 + IVI "OTA 실패 — 이전 설정 유지" 표시 확인. | | |
