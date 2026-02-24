# 요구사항 명세서

> SDV 기반 차량 경험(Experience) 플랫폼 — 요구사항 정의

---

## Part 1. Base — 차량 신호 입력층 (A + B)

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_B01 | 차속·가속·제동 신호 제공 | Vehicle_ECU는 gVehicleSpeed(0~200 km/h) / gAccelValue(-10~10 m/s²) / gBrakeValue(0~10 m/s²)를 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 전송한다. Panel TrackBar로 값 조절. | 상/상 | | | |
| Req_B02 | 조향·급차선변경 신호 제공 | MDPS_ECU는 SteeringInput(0/1) / gLaneChangeAlert(0/1) / SteeringAngleRate(°/s)를 CAN-LS 0x110으로 100ms 주기 전송한다. 조향각속도 > 50°/s 시 gLaneChangeAlert = 1 자동 설정. | 상/상 | | | |
| Req_B03 | 차선이탈 신호 제공 | LDW_ECU는 gLaneDeparture(0/1)를 CAN-LS 0x120으로 100ms 주기 전송한다. sysvar::LDW::laneDeparture 직접 주입으로 구현. | 상/상 | | | |

---

## Part 2. Base — 위험 감지 및 판단층 (WDM_ECU)

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_B04 | 과속 감지 | gVehicleSpeed가 구간별 기준(일반 80 / 스쿨존 30 / 고속도로 110 km/h)을 초과하면 A그룹 플래그를 설정한다. gRoadZone에 따라 임계값 동적 변경. | 상/상 | | | |
| Req_B05 | 급가속 감지 | gAccelValue > 3.5 m/s² 감지 시 A그룹 플래그를 설정한다. | 상/상 | | | |
| Req_B06 | 급제동 감지 | gBrakeValue > 4.0 m/s² 감지 시 A그룹 플래그를 설정한다. | 상/상 | | | |
| Req_B07 | 차선이탈 감지 | gLaneDeparture = 1 수신 시 B그룹 플래그를 설정한다. | 상/상 | | | |
| Req_B08 | 급차선변경 감지 | gLaneChangeAlert = 1 수신 시 B그룹 플래그를 설정한다. | 상/상 | | | |
| Req_B09 | 경고 단계 판단 + 자동 소거 | 판단 규칙: A단독 OR B단독 → gWarningLevel = 1 / A AND B → gWarningLevel = 2 / gCrashEvent = 1 → gWarningLevel = 3. 소거 규칙: Level 1 → 2초 후 자동 소거 / Level 2 → A·B 플래그 동시 해제 시 소거 / Level 3 → 운전자 능동 개입(Req_B15/B16)만으로 해제. FTTI ≤ 50ms. | 상/상 | | | |

---

## Part 3. Base — 경고 출력층

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_B10 | Cluster 경고등 | WDM_Warning(0x200) 수신 시: Level 0 → 소등 / Level 1 → 황색 / Level 2 → 적색 / Level 3 → 적색 빠른 점멸(200ms). 활성화 ≤ 50ms. | 상/상 | | | |
| Req_B11 | Sound 경고음 | Sound_Control(0x230) 수신 시: Level 0 → 무음 / Level 1 → 단발 "띠딩!" 1회(2초 후 자동 종료) / Level 2 → 연속음(500ms 간격) / Level 3 → 긴급 연속음(해제 시까지). | 상/상 | | | |
| Req_B12 | Ambient 경고 패턴 | Ambient_Control(0x220) 수신 시: Level 0 → OFF / Level 1 → 없음 / Level 2 → AMBER 파동(1초 주기) / Level 3 → RED 빠른 점멸(200ms). 구간별 패턴과 분리. | 상/상 | | | |
| Req_B13 | IVI 경고 표시 | IVI_Status(0x240) 수신 시: Level 0 → 정상 / Level 1 → "주의" / Level 2 → "경고" + 원인 / Level 3 → "긴급 경고". | 상/중 | | | |

---

## Part 4. Base — 경고 해제층 (Level 3 전용 능동 해제)

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_B15 | 응시 복귀 → Level 3 해제 | gWarningLevel = 3 상태에서 sysvar::Driver::GazeActive 0 → 1 전환 시 gWarningLevel = 0 초기화. Level 1/2에는 동작하지 않음. (라엘 담당) | 상/상 | | | |
| Req_B16 | 핸들 입력 → Level 3 해제 | gWarningLevel = 3 상태에서 SteeringInput = 1 수신 시 gWarningLevel = 0 초기화. Level 1/2에는 동작하지 않음. (현준 담당) | 상/상 | | | |

---

## Part 5. Test Suite 1 — 준영 (구간 인식 + Ambient 연동)

> 전제조건: Base(Req_B01~B16) 전체 충족. Ambient 우선순위: gWarningLevel > 0 시 경고 패턴이 즉시 오버라이드.

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_Z01 | gRoadZone 구간 설정 | Panel 버튼 4개로 gRoadZone(0:일반/1:스쿨존/2:고속도로/3:IC출구)을 실시간 설정한다. 변경 즉시 Req_B04 과속 임계값 갱신. (준영 담당) | 상/상 | | | |
| Req_Z02 | 스쿨존 Ambient RED 점멸 | gRoadZone = 1 상태에서 gVehicleSpeed > 30 km/h 시 Ambient RED 빠른 점멸(200ms) 즉시 적용. 활성화 ≤ 50ms. | 상/상 | | | |
| Req_Z03 | 고속도로 핸들 미입력 진동 경고 | gRoadZone = 2 상태에서 SteeringInput = 0 이 10초 이상 지속 시 Ambient ORANGE 파동(1초 주기) + 진동 패턴 적용. SteeringInput = 1 감지 시 즉시 해제. | 상/상 | | | |
| Req_Z04 | IC출구 Ambient 방향 안내 | gRoadZone = 3 진입 즉시 IC 유도선 색상(초록/분홍/빨강)으로 전환. gNavDirection(0=좌, 1=우)에 따라 해당 방향 흐름 애니메이션 적용. gRoadZone 변경 시 즉시 소거. gWarningLevel > 0 시 경고 패턴으로 오버라이드, 해제 후 자동 복귀. | 상/중 | | | |

---

## Part 6. Test Suite 2 — 성현 (OTA 구독 서비스)

> 전제조건: Base(Req_B01~B16) 전체 충족. OTA는 P 기어(gGearP = 1) 상태에서만 허용.
> 방식: SOTA(Software OTA) — 소규모 파라미터 패킷 전송으로 미리 내장된 기능을 즉시 활성화.

| Req. ID | 요약 | 설명 | 중요도/긴급도 | 요청자 | 검토자 | 변경사항 |
|---------|------|------|-------------|--------|--------|---------|
| Req_O01 | Drive Coach Package 구독 | P 기어 정차 중 IVI 구독 메뉴 → [Drive Coach 설치] 선택 → 동의 → OTA_Server가 ETH_OTA_Param(Port 6000, 8 bytes) 전송 → OTA_ECU CRC8 검증 통과 시 파라미터 즉시 활성화. 적용 내용: LDW 민감도 강화 / 최고 속도 리미터 100 km/h / 토크 제한 70% / 후진 속도 제한 10 km/h. IVI에 "Drive Coach 적용 완료" 표시. (성현 담당) | 상/상 | | | |
| Req_O02 | Smart Claim Telematics 활성화 | Drive Coach 적용 후 Smart Claim 기능 함께 활성화. gCrashEvent = 1 감지 시 Python CANoe COM API로 충돌 데이터(타임스탬프/속도/경고 이력)를 Flask 보험사 서버에 HTTP POST 전송. 전송 성공 시 IVI에 "사고 데이터 전송 완료" 표시. (현준2 담당) | 상/중 | | | |
| Req_O03 | Seasonal Theme Package 구독 | P 기어 정차 중 IVI 알림(OTA 서버 패키지 가용) → 운전자 동의 → OTA_Server ETH_OTA_Param 전송 → 파라미터 즉시 활성화. 적용 내용: Ambient 색상 프리셋(봄/여름/가을/겨울) + IVI 배경 + 시동 사운드 테마. (성현 담당) | 상/중 | | | |
| Req_O04 | P 기어 이탈 시 OTA 중단 | OTA 세션 진행 중 gGearP = 0 감지 시 세션 즉시 중단. IVI에 "P 기어 이탈 — OTA 중단" 표시. 파라미터 미적용 상태로 이전 유지. | 상/상 | | | |
| Req_O05 | OTA 파라미터 검증 실패 복구 | ETH_OTA_Param CRC8 불일치 감지 시 파라미터 적용 거부. 이전 상태(파라미터) 그대로 유지. IVI에 "OTA 실패 — 이전 설정 유지" 표시. | 상/상 | | | |

---

## 요구사항 구조 요약

| 구분 | Req. ID 범위 | 수량 |
|------|------------|------|
| Base 입력층 | Req_B01~B03 | 3 |
| Base 판단층 | Req_B04~B09 | 6 |
| Base 출력층 | Req_B10~B13 | 4 |
| Base 해제층 | Req_B15~B16 | 2 |
| TS-준영 | Req_Z01~Z04 | 4 |
| TS-성현 | Req_O01~O05 | 5 |
| **합계** | | **24** |
