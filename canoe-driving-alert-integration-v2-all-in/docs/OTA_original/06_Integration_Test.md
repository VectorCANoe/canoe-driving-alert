# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 — 소프트웨어 통합 테스트 / Part 4, Cl.9 — 시스템 통합 테스트
**ASPICE Reference**: SWE.5 (BP1-BP3)
**Version**: 3.0
**Date**: 2026-02-24
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 우측 중단 — SWE.5 통합 테스트 | `03_Function_definition.md` + `0301_SysFuncAnalysis.md` (SYS.3) | `05_Unit_Test.md` | `07_System_Test.md` |

> **실행 원칙**: Base(In_Test_01~06) 전체 Pass 후 TS-준영(In_Test_07~09), TS-성현(In_Test_10~13)을 순서대로 실행한다.

---

## Part 1. Base 통합 테스트 — 입력층 + 판단층 + 출력층

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|----------|-----------|-----------|---------|--------------|--------|------|
| In_Test_01 | Req_B04, Req_B09, Req_B10 | 과속 감지 → 1단계 경고 발령 확인 | Vehicle::vehicleSpeed > 80km/h 주입 → WDM_ECU gWarningLevel = 1 → Cluster 황색 경고등 점등 (50ms 이내) | | | |
| In_Test_02 | Req_B05, Req_B06, Req_B09 | 급가속/급제동 감지 → 1단계 경고 발령 확인 | accelValue > 3.5 m/s² 주입 → gWarningLevel = 1 → 경고 발령. brakeValue > 4.0 m/s² 동일 검증. | | | |
| In_Test_03 | Req_B07, Req_B08, Req_B09 | 차선이탈/급차선변경 감지 → 1단계 경고 발령 확인 | LDW::laneDeparture = 1 또는 LDW::laneChangeAlert = 1 주입 → gWarningLevel = 1 → Cluster 황색 점등 | | | |
| In_Test_04 | Req_B09, Req_B12 | A+B 복합 → 2단계 경고 발령 확인 + gCrashEvent → 3단계 확인 | A그룹(과속) AND B그룹(차선이탈) 동시 주입 → gWarningLevel = 2 → Cluster 적색 + Sound 2단계 + Ambient AMBER 파동. gCrashEvent = 1 주입 → gWarningLevel = 3 → Cluster 적색 점멸 + Sound 긴급음 + Ambient RED 점멸 | | | |
| In_Test_05 | Req_B15 | 응시 복귀 → 경고 해제 확인 | gWarningLevel > 0 상태에서 Driver::gazeActive 0→1 전환 → gWarningLevel = 0 → Cluster 소등 | | | |
| In_Test_06 | Req_B16 | 핸들 입력 → 경고 해제 확인 | gWarningLevel > 0 상태에서 MDPS::steeringInput = 1 주입 → gWarningLevel = 0 → Cluster 소등 | | | |

---

## Part 2. TS-준영 통합 테스트 — 구간 인식 + Ambient 연동

> **전제조건**: In_Test_01~06 전체 Pass.

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|----------|-----------|-----------|---------|--------------|--------|------|
| In_Test_07 | Req_Z01, Req_Z02 | gRoadZone=1 스쿨존 앰비언트 RED 점멸 확인 | Panel 버튼으로 gRoadZone = 1 설정 → vehicleSpeed > 30km/h 과속 주입 → Ambient_ECU AmbientMode = 1 RED 200ms 점멸 활성화 확인 | | | |
| In_Test_08 | Req_Z03 | gRoadZone=2 고속도로 핸들 미입력 10초 진동 경고 확인 | gRoadZone = 2 + SteeringInput = 0 유지 → 10초 후 WDM_ECU tSteerTimer 만료 → Ambient ORANGE 파동 + Door_ECU 진동 활성화 확인 | | | |
| In_Test_09 | Req_Z04 | gRoadZone=3 IC출구 앰비언트 방향 안내 확인 | gRoadZone = 3 + gNavDirection = 1(우측) 설정 → Ambient_ECU 실도로 IC 유도선 색상(초록/분홍/빨강) + 우측 방향 흐름 애니메이션 즉시 활성화 확인. gWarningLevel = 1 주입 → 경고 앰비언트로 즉시 오버라이드 확인. 경고 해제 → IC 패턴 자동 복귀 확인. gRoadZone 변경 → 앰비언트 즉시 해제 확인. | | | |

---

## Part 3. TS-성현 통합 테스트 — Drive Coach + Smart Claim + Seasonal Theme

> **전제조건**: In_Test_01~06 전체 Pass.

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|----------|-----------|-----------|---------|--------------|--------|------|
| In_Test_10 | Req_O01 | P 기어 상태에서 Drive Coach OTA UDS 세션 확인 | gGearP = 1 설정 → IVI 구독 메뉴 진입 → [Drive Coach 설치] 선택 → 운전자 동의 → OTA_Server: DoIP → 0x10 0x02 → 0x27 → 0x34 → 0x36×N → 0x37 정상 동작. CRC-32 일치 → PositiveResponse(0x77) → ECU 재시작 → LDW 민감도 상향 + 토크 제한(70%) + 속도 리미터(100km/h) + 후진 제한(10km/h) 적용 확인. | | | |
| In_Test_11 | Req_O02 | Smart Claim Telematics 활성화 → 충돌 데이터 전송 확인 | Drive Coach 설치 완료 상태에서 gCrashEvent = 1 재주입 → Python COM API HTTP POST 실행 → Flask 서버 수신 확인 → IVI "사고 데이터 전송 완료" 표시 확인. | | | |
| In_Test_12 | Req_O03 | Seasonal Theme OTA UDS 세션 확인 | OTA_Server Seasonal Theme 패키지 가용 감지 → IVI 알림 → 운전자 동의 → 동일 UDS 세션(DoIP→0x10→0x27→0x34→0x36×N→0x37) 실행 → 설치 완료 → 앰비언트 색상·IVI 배경 즉시 적용 확인. | | | |
| In_Test_13 | Req_O04 | OTA 실패 시 Rollback 확인 | OTA 전송 중 CRC 불일치 주입 → NegativeResponse(0x7F) → 자동 Rollback → 이전 펌웨어 유지 + OTA::rollbackTriggered = 1 확인 | | | |
| In_Test_14 | Req_O05 | Bus Off 발생 시 OTA 세션 안전 중단 확인 | OTA 진행 중 CGW::busOffDetected = 1 주입 → OTA 세션 즉시 중단 + DTC U0300 저장 + OTA::otaInProgress = 0 확인 | | | |

---

## 추가 테스트 — 빗길 임계값 (미확정)

> **상태**: 빗길 모드 임계값 수치 미확정 (CLAUDE.md 미확정 사항 #3). 수치 확정 후 Req_B04 하위 요구사항으로 신설 예정.

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|----------|-----------|-----------|---------|--------------|--------|------|
| In_Test_14 | Req_B04 (하위 예정) | 빗길 모드에서 임계값 하향 적용 확인 | Rain::rainMode = 1 설정 → 과속 기준 자동 하향(일반 80→64km/h) → 동일 속도에서 경고 더 빨리 발령 확인 | | | |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — In_Test_01~14 통합 테스트 명세 (Req_001~018) |
| 2.0 | 2026-02-23 | 요구사항 ID 전면 갱신 — Base(Req_B01~B16) / TS-준영(Req_Z01~Z04) / TS-성현(Req_O01~O05) 구조 반영. Part별 섹션 분리. In_Test_04 3단계 통합. 빗길 테스트 미확정 섹션 분리. |
| 3.0 | 2026-02-24 | gAccelCount 제거 — In_Test_02 단순화. Level 3 트리거 변경 — gCrashEvent = 1. In_Test_04 3단계 조건 갱신. Part 3 TS-성현 전면 재작성 — In_Test_10(Drive Coach) / In_Test_11(Smart Claim) / In_Test_12(Seasonal Theme) / In_Test_13(Rollback) / In_Test_14(Bus Off). |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
