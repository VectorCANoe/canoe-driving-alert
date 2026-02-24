# 단위 테스트 (Unit Test)

**Document ID**: PROJ-05-UT
**ISO 26262 Reference**: Part 6, Cl.9 — 소프트웨어 단위 테스트
**ASPICE Reference**: SWE.4 (BP1: 단위 테스트 명세, BP2: 단위 테스트 수행, BP3: 결과 평가)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 우측 하단 — SWE.4 단위 테스트 | `04_SW_Implementation.md` (SWE.3/6) | `03_Function_definition.md` | `06_Integration_Test.md` |

---

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|------|------|--------|---------|----------|--------|------|
| Vehicle_ECU | 제어 | 차속 CAN-LS 전송 | gVehicleSpeed 값을 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 전송. 초기값 60 km/h. | | | |
| Vehicle_ECU | 제어 | 과속 플래그 설정 | gVehicleSpeed > gRoadZone 기준(일반:80/스쿨존:30/고속도로:110) 시 OverspeedFlag = 1 자동 설정 | | | |
| Vehicle_ECU | 제어 | 급가속 시뮬레이션 | Vehicle::accelValue = 4.0 m/s² 설정 시 WDM_ECU gAccelCount 증가 트리거 확인 | | | |
| Vehicle_ECU | 제어 | 급제동 시뮬레이션 | Vehicle::brakeValue = 5.0 m/s² 설정 시 WDM_ECU 급제동 이벤트 감지 확인 | | | |
| MDPS_ECU | 제어 | 조향 입력 CAN-LS 전송 | SteeringInput / gLaneChangeAlert를 CAN-LS 0x110으로 100ms 주기 전송 | | | |
| MDPS_ECU | 제어 | 핸들 입력 주입 | MDPS::steeringInput = 1 설정 시 WDM_ECU 경고 해제 트리거 확인 | | | |
| MDPS_ECU | 제어 | 급차선변경 시뮬레이션 | LDW::laneChangeAlert = 1 설정 시 WDM_ECU B그룹 감지 확인 | | | |
| LDW_ECU | 제어 | 차선이탈 CAN-LS 전송 | gLaneDeparture를 CAN-LS 0x120으로 100ms 주기 전송 | | | |
| LDW_ECU | 제어 | 차선이탈 시뮬레이션 | LDW::laneDeparture = 1 설정 시 WDM_ECU B그룹 감지 확인 | | | |
| WDM_ECU | 제어 | 1단계 경고 발령 (A단독) | OverspeedFlag = 1 수신 → gWarningLevel = 1 설정 → WDM_Warning(0x200) CAN-HS 전송. 50ms 이내. | | | |
| WDM_ECU | 제어 | 1단계 경고 발령 (B단독) | gLaneDeparture = 1 수신 → gWarningLevel = 1 설정 → WDM_Warning(0x200) CAN-HS 전송. | | | |
| WDM_ECU | 제어 | 2단계 경고 발령 (A+B) | A그룹 AND B그룹 동시 감지 → gWarningLevel = 2 설정 → WDM_Warning 전송. | | | |
| WDM_ECU | 제어 | 3단계 경고 발령 + OTA | A+B 복합 + gAccelCount ≥ 3 → gWarningLevel = 3 → IVI OTA 팝업 트리거 | | | |
| WDM_ECU | 제어 | 경고 해제 (응시 복귀) | Driver::gazeActive 0→1 전환 감지 → gWarningLevel = 0 초기화 | | | |
| WDM_ECU | 제어 | 경고 해제 (핸들 입력) | MDPS::steeringInput = 1 감지 → gWarningLevel = 0 초기화 | | | |
| WDM_ECU | 제어 | gRoadZone 구간 적용 | gRoadZone = 1 설정 시 과속 기준 30km/h 적용, Ambient RED 점멸 활성화 확인 | | | |
| WDM_ECU | 제어 | 급가속 타이머 관리 | gAccelCount 3회 누적 후 10분 타이머 만료 시 gAccelCount = 0 초기화 확인 | | | |
| WDM_ECU | 제어 | 고속도로 핸들 미입력 타이머 | gRoadZone = 2 + SteeringInput = 0 지속 → 10초 후 진동 경고 발령 | | | |
| CGW | 제어 | CAN-LS→CAN-HS 라우팅 | CAN-LS 입력 신호(0x100~0x120) 수신 → CAN-HS WDM_ECU로 라우팅 (지연 ≤5ms) | | | |
| CGW | 제어 | DoIP 처리 | DoIP Routing Activation(0xE001) 처리 및 UDS 메시지 포워딩 | | | |
| Cluster_ECU | 제어 | 1단계 황색 경고등 | WDM_Warning(gWarningLevel=1) 수신 → WarnLampLevel = 1 황색. 50ms 이내. | | | |
| Cluster_ECU | 제어 | 2단계 적색 경고등 | WDM_Warning(gWarningLevel=2) 수신 → WarnLampLevel = 2 적색. | | | |
| Cluster_ECU | 제어 | 경고등 소등 | gWarningLevel = 0 수신 → WarnLampLevel = 0 소등. | | | |
| Ambient_ECU | 제어 | 스쿨존 RED 점멸 | AmbientMode = 1 수신 → RED 200ms 주기 점멸. gRoadZone=1 과속 시. | | | |
| Ambient_ECU | 제어 | 고속도로 ORANGE 파동 | AmbientMode = 2 수신 → ORANGE 1초 주기 파동. gRoadZone=2 핸들 미입력. | | | |
| Ambient_ECU | 제어 | IC출구 방향 애니메이션 | AmbientMode = 4 수신 → 좌→우 흐름 애니메이션. gRoadZone=3 IC출구. | | | |
| Sound_ECU | 제어 | 단계별 경고음 | SoundAlert = 1(단발) / 2(연속) / 3(긴급) 수신 → 해당 경고음 출력 | | | |
| IVI_ECU | 제어 | OTA 팝업 표시 | OTA_PopupTrigger = 1 수신 → Level 1 무료 안전모드 팝업 표시 | | | |
| IVI_ECU | 제어 | OTA 진행률 표시 | OTA_Progress 갱신 시 → IVI 진행률 바 업데이트 | | | |
| Door_ECU | 제어 | 3초 도어 잠금 | DoorLockCmd = 1 수신 → 3초 도어 잠금 → 자동 해제 | | | |
| Door_ECU | 제어 | 미러 LED 점멸 | MirrorLED = 1 수신 → 미러 LED 점멸 활성화 | | | |
| OTA_Server | 제어 | DoIP Routing Activation | DoIP 0xE001 전송 → CGW 경로 활성화 응답 수신 | | | |
| OTA_Server | 제어 | Programming Session 진입 | UDS 0x10 0x02 → PositiveResponse(0x50 0x02) 수신 | | | |
| OTA_Server | 제어 | Security Access | UDS 0x27 Seed 요청 → Key 응답 → PositiveResponse(0x67) | | | |
| OTA_Server | 제어 | Download Request | UDS 0x34 다운로드 요청 → maxBlockLength 포함 응답(0x74) | | | |
| OTA_Server | 제어 | 블록 전송 | UDS 0x36 4KB 블록 순차 전송 → 각 블록 PositiveResponse(0x76) | | | |
| OTA_Server | 제어 | 전송 완료 + CRC | UDS 0x37 → CRC-32 검증 통과 → PositiveResponse(0x77) → ECU 재시작 | | | |
| OTA_Server | 제어 | Rollback | CRC 불일치 주입 시 자동 Rollback → 이전 펌웨어 유지 | | | |
| 가상 노드 (Simulator) | 입력 | 속도 주입 (TrackBar) | Vehicle::vehicleSpeed TrackBar 조절 → WDM_ECU 과속 이벤트 트리거 | | | |
| 가상 노드 (Simulator) | 입력 | 차선이탈 주입 (Button) | LDW::laneDeparture = 1 강제 주입 → WDM_ECU B그룹 감지 트리거 | | | |
| 가상 노드 (Simulator) | 입력 | gRoadZone 변경 (Button×4) | Panel 버튼 4개 → gRoadZone 0~3 설정 → WDM_ECU 즉시 적용 | | | |
| 가상 노드 (Simulator) | 출력 | 경고 레벨 표시 | gWarningLevel 0~3 Panel Indicator 실시간 출력 | | | |
| 가상 노드 (Simulator) | 출력 | OTA 진행률 표시 | OTA_Progress Panel 진행률 바 출력 | | | |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
