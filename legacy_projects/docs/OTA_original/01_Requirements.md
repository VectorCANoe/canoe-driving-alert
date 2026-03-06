# 요구사항 명세서 (System Requirements Specification)

**Document ID**: PROJ-01-SRS
**ISO 26262 Reference**: Part 4, Cl.6 — 시스템 요구사항 명세
**ASPICE Reference**: SYS.2 (BP1: 요구사항 도출, BP2: 요구사항 분석, BP4: 추적성 확보)
**Version**: 3.1
**Date**: 2026-02-24
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 상단 — SYS.2 시스템 요구사항 | `07_System_Test.md` (SYS.5) | Concept Design | `03_Function_definition.md` |

> **구조 원칙**: Base 요구사항(Req_B01~B16)은 모든 Test Suite의 공통 실행 전제조건이다.
> Test Suite 요구사항(Req_Z/Req_O)은 Base가 완전히 동작하는 환경 위에서만 추가된다.

---

## Part 1. Base 요구사항 — 차량 동역학 입력층 (A+B)

> 모든 Test Suite가 공유하는 차량 신호 제공 인프라. SIL 환경에서 Panel + sysvar로 주입.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_B01 | 차량 동역학 신호 제공 | Vehicle_ECU는 gVehicleSpeed(0~200 km/h) / gAccelValue(-10~10 m/s²) / gBrakeValue(0~10 m/s²)를 CAN-LS(0x100)로 100ms 주기 WDM_ECU에 전송한다. Panel TrackBar로 값 조절 가능. | **입력층 A.** 실차 파워트레인·섀시 센서 대체. SIL 핵심 인프라. | ASIL-B | Scene.B1~B5 |
| Req_B02 | 조향 및 차선변경 신호 제공 | MDPS_ECU는 SteeringInput(0/1) / gLaneChangeAlert(0/1) / SteeringAngleRate(°/s)를 CAN-LS(0x110)로 100ms 주기 전송한다. 조향각속도 > 50°/s 시 gLaneChangeAlert = 1 자동 설정. | **입력층 B.** 실차 MDPS 조향 신호 대체. | ASIL-B | Scene.B1, B6, B7 |
| Req_B03 | 차선이탈 신호 제공 | LDW_ECU는 gLaneDeparture(0/1)를 CAN-LS(0x120)로 100ms 주기 전송한다. sysvar::LDW::laneDeparture = 1 직접 주입으로 구현. | **입력층 B.** 실차 카메라 기반 LDW 대체. | ASIL-B | Scene.B1, B6 |

---

## Part 2. Base 요구사항 — 위험 행동 감지 및 판단 (WDM_ECU)

> WDM_ECU가 A+B 입력 신호를 수신하여 위험 행동 여부와 단계를 판단하는 핵심 로직.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_B04 | 과속 감지 | WDM_ECU는 gVehicleSpeed가 구간별 제한속도(일반도로 80 / 스쿨존 30 / 고속도로 110 km/h)를 초과하면 과속 이벤트를 감지하고 A그룹 플래그를 설정한다. | 기준: gRoadZone 값에 따라 임계값 동적 변경. gRoadZone=0이 Base 기본값(80 km/h). | ASIL-B | Scene.B3 |
| Req_B05 | 급가속 감지 | WDM_ECU는 gAccelValue > 3.5 m/s² 감지 시 A그룹 플래그를 설정한다. | 급가속 = 추돌 위험 지표. 택천 담당. | ASIL-B | Scene.B4 |
| Req_B06 | 급제동 감지 | WDM_ECU는 gBrakeValue > 4.0 m/s² 감지 시 A그룹 플래그를 설정한다. | 급제동 = 추돌 위험 지표. | ASIL-B | Scene.B5 |
| Req_B07 | 차선이탈 감지 판단 | WDM_ECU는 gLaneDeparture = 1 수신 시 B그룹 플래그를 설정한다. | LDW_ECU 신호 직접 수신. | ASIL-B | Scene.B6 |
| Req_B08 | 급차선변경 감지 판단 | WDM_ECU는 gLaneChangeAlert = 1 수신 시 B그룹 플래그를 설정한다. | MDPS_ECU 신호 직접 수신. | ASIL-B | Scene.B7 |
| Req_B09 | 위험 단계 판단 규칙 + 자동 소거 | WDM_ECU는 아래 규칙으로 gWarningLevel을 결정하고 출력층에 즉시 반영한다. FTTI ≤ 50ms.<br>**판단 규칙:**<br>• A그룹 단독 OR B그룹 단독 → **gWarningLevel = 1**<br>• A그룹 AND B그룹 동시 → **gWarningLevel = 2**<br>• gCrashEvent = 1 → **gWarningLevel = 3** (충돌 이벤트. Panel 전용 버튼으로 주입)<br>**자동 소거 규칙:**<br>• Level 1 → 발령 후 **2초 타이머** 만료 시 자동 gWarningLevel = 0<br>• Level 2 → A·B 플래그 **동시 해제** 시 자동 gWarningLevel = 0<br>• Level 3 → **운전자 능동 개입만으로 해제** (Req_B15 또는 Req_B16) | **핵심 판단 로직.** gCrashEvent는 사고 시뮬레이션 전용. Level 3만 운전자 확인 필요. | ASIL-B | Scene.B3~B9 |

---

## Part 3. Base 요구사항 — 경고 시스템 출력층

> Base 경고 시스템은 gWarningLevel 값만으로 자동 작동한다. Test Suite가 없어도 독립적으로 동작해야 한다.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_B10 | Cluster 경고등 제어 | Cluster_ECU는 WDM_Warning(0x200) 수신 시 gWarningLevel에 따라 즉시 경고등을 제어한다.<br>• Level 0 → 소등<br>• Level 1 → 황색 점등<br>• Level 2 → 적색 점등<br>• Level 3 → 적색 빠른 점멸(200ms) | 경고등 활성화 지연 ≤ 50ms. 운전자 즉각 인지 기준. | ASIL-B | Scene.B3~B9 |
| Req_B11 | Sound 경고음 발령 | Sound_ECU는 Sound_Control(0x230) 수신 시 gWarningLevel에 따라 경고음을 출력한다.<br>• Level 0 → 무음<br>• Level 1 → **단발 단음 1회 ("띠딩!") — 반복 없음. 2초 후 자동 소거와 동시에 종료.**<br>• Level 2 → 연속음 (500ms 간격, 조건 해제 시 종료)<br>• Level 3 → 긴급 연속음 (지속, 운전자 능동 해제 시까지) | **독립 요구사항.** Level 1은 일회성 알림 — 반복 경고음으로 운전 방해 최소화. | ASIL-B | Scene.B3~B9 |
| Req_B12 | Ambient 기본 경고 패턴 | Ambient_ECU는 Ambient_Control(0x220) 수신 시 gWarningLevel에 따라 기본 경고 패턴을 출력한다.<br>• Level 0 → OFF<br>• Level 1 → 없음 (Cluster/Sound만으로 충분)<br>• Level 2 → AMBER 파동 (1초 주기, 전체 조명)<br>• Level 3 → RED 빠른 점멸 (200ms, 전체 조명) | **독립 요구사항.** Base Ambient는 경고 단계에만 반응. 구간별 패턴(준영 TS)과 완전히 분리. | ASIL-B | Scene.B8, B9 |
| Req_B13 | IVI 기본 경고 정보 표시 | IVI_ECU는 IVI_Status(0x240) 수신 시 gWarningLevel을 HUD/화면에 표시한다.<br>• Level 0 → 정상 주행 표시<br>• Level 1 → "주의" 텍스트 표시<br>• Level 2 → "경고" 텍스트 + 원인 표시<br>• Level 3 → "긴급 경고" 표시 | **독립 요구사항.** IVI의 Base 역할은 정보 표시. OTA 팝업(성현 TS)과 분리. | QM | Scene.B3~B9 |

---

## Part 4. Base 요구사항 — 경고 해제 (해제층)

> **Level 1/2는 Req_B09의 자동 소거 규칙으로 해제된다.**
> 운전자 능동 개입(Req_B15/B16)은 **Level 3 전용**. Level 3는 타이머 소거 없이 운전자 확인만으로 해제.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_B15 | 응시 복귀 감지 → **Level 3** 경고 해제 | WDM_ECU는 **gWarningLevel = 3** 상태에서 sysvar::Driver::GazeActive가 0 → 1로 전환될 경우 gWarningLevel을 0으로 초기화하고 모든 출력층 경고를 해제한다. Level 1/2에서는 동작하지 않음. | 라엘 담당. CAPL sysvar Panel Button으로 주입. 전방 주시 복귀 = 3단계 위험 상황 운전자 정상 복귀 확인. | ASIL-A | Scene.B10 |
| Req_B16 | 핸들 입력 감지 → **Level 3** 경고 해제 | WDM_ECU는 **gWarningLevel = 3** 상태에서 MDPS_ECU로부터 SteeringInput = 1을 수신할 경우 gWarningLevel을 0으로 초기화하고 모든 출력층 경고를 해제한다. Level 1/2에서는 동작하지 않음. | 현준 담당. 능동 조향 입력 = 3단계 위험 상황 운전자 대응 확인. | ASIL-A | Scene.B11 |

---

## Part 5. Test Suite 1 — 준영 (구간 인식 + Ambient 연동)

> **전제조건**: Base 요구사항(Req_B01~B16) 전체 충족 상태에서만 유효.
> **앰비언트 우선순위**: gWarningLevel > 0(경고 발령) 시 경고 앰비언트(Req_B12)가 모든 구간별 패턴보다 즉시 우선 적용된다. 경고 해제 후 gRoadZone 구간별 패턴으로 자동 복귀.
> Base Ambient(Req_B12)의 기본 패턴 위에 구간별 특화 패턴을 오버레이하는 방식으로 동작.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_Z01 | gRoadZone 구간 설정 | WDM_ECU는 CANoe Panel 버튼(4개)으로 gRoadZone(0:일반도로/1:스쿨존/2:고속도로/3:IC출구)을 실시간 설정한다. gRoadZone 변경 시 Req_B04의 과속 임계값이 즉시 갱신된다. | 준영 담당. 네비게이션 대체. Panel 버튼 = 구간 진입 시뮬레이션. | QM | Scene.Z1~Z4 |
| Req_Z02 | 스쿨존 Ambient RED 점멸 | gRoadZone = 1 상태에서 과속(gVehicleSpeed > 30 km/h) 감지 시 Ambient_ECU에 RED 빠른 점멸(200ms 주기) 패턴을 즉시 적용한다. Ambient 활성화 ≤ 50ms. | 준영 담당. 어린이 보호구역 즉각 시각 경고. Base Ambient(AMBER 파동) 대신 RED 점멸로 오버라이드. | ASIL-B | Scene.Z1 |
| Req_Z03 | 고속도로 핸들 미입력 진동 경고 | gRoadZone = 2 상태에서 SteeringInput = 0이 10초 이상 지속될 경우 Ambient_ECU에 ORANGE 파동(1초 주기) + Door_ECU에 진동 패턴을 적용한다. SteeringInput = 1 감지 시 즉시 해제. | 준영 담당. 졸음운전/전방 주시 태만 대응. gSteerTimer 10초 타이머 기반. | ASIL-B | Scene.Z2 |
| Req_Z04 | IC출구 Ambient 방향 안내 | gRoadZone = 3 상태 진입 즉시 Ambient_ECU에 실도로 IC 진출입 유도선 색상 패턴(초록/분홍/빨강)을 적용한다. **색상**: 실도로 IC 유도선 고정 색상 그대로 재현 — 경로 상태와 무관. **방향**: gNavDirection(0=좌, 1=우)에 따라 해당 방향으로 흐르는 애니메이션 적용. gRoadZone 변경 시 즉시 해제. **우선순위**: gWarningLevel > 0 발생 시 경고 앰비언트가 즉시 오버라이드. 경고 해제 후 IC 패턴으로 자동 복귀. | 준영 담당. 실도로 IC 유도선 색상(초록/분홍/빨강)을 앰비언트로 재현. 안전 기능 아님. | QM | Scene.Z3 |

---

## Part 6. Test Suite 2 — 성현 (Drive Coach + Smart Claim + Seasonal Theme)

> **전제조건**: Base 요구사항(Req_B01~B16) 전체 충족 상태에서만 유효.
> **OTA 공통 조건**: 차량 P 기어(gGearP = 1) 상태에서만 UDS 세션 허용. 주행 중 OTA 불가.
> 동일한 UDS OTA 파이프라인(DoIP → 0x10 → 0x27 → 0x34 → 0x36×N → 0x37)으로 3종 패키지를 검증한다.

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 |
|---------|------|------|-----------------|------|--------|
| Req_O01 | Drive Coach Package OTA | 차량 P 기어 상태(gGearP = 1)에서 IVI 구독 메뉴 진입 → 운전자가 [Drive Coach 설치] 버튼 선택 → 동의 화면 확인 → UDS 세션 실행: DoIP → 0x10 0x02 → 0x27 → 0x34 → 0x36×N → 0x37 → CRC-32 검증 → ECU 재시작. **설치 패키지(초보자 맞춤 주행 보조)**: LDW 경고 민감도 상향 + 급가속 토크 제한(최대 토크 70%) + 최고 속도 리미터(100 km/h) + 후진 속도 제한(10 km/h). | 성현 담당. 경고 트리거 없이 사용자 주도 설치. Tesla/BMW Valet Mode 대응 개념. UNECE WP.29 준수. | ASIL-B | Scene.O1, O2 |
| Req_O02 | Smart Claim Telematics 활성화 | Drive Coach 설치 완료 시 Smart Claim 기능이 함께 활성화된다. gCrashEvent = 1 감지 시 Python CANoe COM API를 통해 충돌 데이터(타임스탬프, 속도, 경고 이력)를 Flask 보험사 서버로 HTTP POST 전송한다. 전송 성공 시 IVI에 "사고 데이터 전송 완료" 표시. | 성현 담당. OTA(클라우드→차량)가 아닌 Telematics(차량→클라우드). Python COM API + Flask 연동. | QM | Scene.O3 |
| Req_O03 | Seasonal Theme OTA | 차량 P 기어 상태에서 IVI 알림 표시(OTA_Server 패키지 가용 감지). 운전자 동의 후 Req_O01과 동일 UDS 세션으로 설치. 설치 패키지: 앰비언트 색상 프리셋(봄/여름/가을/겨울) + IVI 배경 + 시동 사운드. 설치 완료 후 즉시 적용. | 성현 담당. P 기어 조건 동일 적용. OTA 파이프라인 재사용 검증. 콘텐츠 스텁 허용. | QM | Scene.O4 |
| Req_O04 | OTA 실패 시 Rollback | OTA 진행 중 CRC 불일치 또는 통신 단절 시 이전 펌웨어로 자동 복구. OTA::rollbackTriggered = 1, IVI에 복구 완료 메시지 표시. | Dual Bank 기반 복구. | ASIL-B | Scene.O5 |
| Req_O05 | Bus Off 안전 중단 | OTA 진행 중 CGW::busOffDetected = 1 감지 시 UDS 세션 즉시 중단, DTC U0300 저장, OTA::otaInProgress = 0. | ISO 11898-1 참조. | ASIL-A | Scene.O6 |

---

---

## [발표용] Drive Coach Package 확장 로드맵

> **이 섹션은 요구사항이 아닙니다.** 개발 범위 밖이며 발표 자료용 참고 정보입니다.
> OTA 메커니즘이 검증되면 동일한 UDS 세션 구조로 아래 기능들을 추후 패키지 형태로 배포 가능합니다.

| 확장 기능 | 분류 | 설명 |
|---------|------|------|
| 방향 전환 진입 신호 알림 | 편의 | 깜빡이 작동 시 진입 가능 타이밍을 조향 진동으로 안내 |
| 전방 추돌 방지 (FCW/AEB) | ADAS | 전방 차량 TTC 기반 경고 및 자동 제동 보조 |
| 차선 이탈 방지 (LKA) | ADAS | 차선 이탈 감지 시 조향 토크 보조로 차선 복귀 |
| 사각지대 경고 (BSD) | ADAS | 후측방 차량 접근 시 미러/앰비언트 경고 |
| 스마트 크루즈 컨트롤 (ACC) | ADAS | 앞차와의 거리 유지 자동 가감속 |

비즈니스 모델 확장 방향:
- 제조사는 위 기능들을 OTA 구독 패키지로 출시 → BMW FOD 동일 구조
- 운전자는 필요한 기능만 선택 구독 → 불필요한 기능 비용 없음
- 차량 출고 후 기능 추가 가능 → 제조사·소비자 모두 이점

---

## 요구사항 분류 요약

| 구분 | Req. ID 범위 | 수량 | 목적 |
|------|------------|------|------|
| **Base — 입력층 (A+B)** | Req_B01~B03 | 3 | 차량 동역학 신호 제공 인프라 |
| **Base — 판단층 (WDM)** | Req_B04~B09 | 6 | 위험 행동 감지 및 단계 판단 |
| **Base — 출력층 (경고 시스템)** | Req_B10~B13 | 4 | Cluster / Sound / Ambient / IVI |
| **Base — 해제층** | Req_B15~B16 | 2 | 응시 복귀 / 핸들 입력 |
| **Test Suite 1 — 준영** | Req_Z01~Z04 | 4 | 구간 인식 + Ambient 연동 |
| **Test Suite 2 — 성현** | Req_O01~O05 | 5 | Drive Coach OTA + Smart Claim Telematics + Seasonal Theme OTA |
| **합계** | | **24** | |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — Req_001~018 |
| 2.0 | 2026-02-23 | 전면 재구조화 — Base(Req_B01~B16) / TS-준영(Req_Z01~Z04) / TS-성현(Req_O01~O05) 분리. Sound(Req_B11) · Ambient Base(Req_B12) · IVI Base(Req_B13) 독립 요구사항 신설. 3단계 경고(Req_B09)와 OTA 팝업(Req_O01) 분리. |
| 2.1 | 2026-02-23 | TS-성현 제품명 리네이밍 — "운전 습관 안전모드" → **Drive Coach Package (DCP)**. OTA 콘텐츠 변경 — 토크 제한 → 촉각 피드백 + 음성 코치 + IVI UI 스킨. |
| 2.2 | 2026-02-23 | Req_O03 재정의 — 유료 구독 제거 → Drive Coach v2 버전 업그레이드 흐름으로 대체. 발표용 확장 로드맵 섹션 신설 (요구사항 외 참고용). |
| 3.0 | 2026-02-24 | gAccelCount 완전 제거 (Req_B05 단순화). Level 3 트리거 변경 — gAccelCount ≥ 3 → gCrashEvent = 1 (충돌 이벤트 Panel 버튼). Req_B14 도어잠금 삭제. Part 6 TS-성현 전면 재구성 — Drive Coach Package(Req_O01) + Smart Claim Telematics(Req_O02) + Seasonal Theme OTA(Req_O03) + Rollback(Req_O04) + Bus Off(Req_O05). |
| 3.1 | 2026-02-24 | Req_O01 OTA 트리거 변경 — 경고 기반 팝업 제거 → P 기어 + 사용자 주도 IVI 구독 메뉴 설치. Drive Coach 콘텐츠 변경 — HMI(시트진동/음성) → 안전 파라미터(LDW 민감도 상향 / 토크 제한 70% / 속도 리미터 100km/h / 후진 제한 10km/h). OTA 공통 P 기어 조건 Part 6 헤더 명시. Req_Z04 앰비언트 방향 안내 고도화 — gNavDirection(좌/우) + gNavColor(초록/분홍/빨강) 연동 동작형 파동 애니메이션. |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
