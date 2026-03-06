# 05_Unit Test (단위 테스트)

## IVI vECU 프로젝트 단위 테스트

> **작성 기준**: 멘토 샘플 형식 준수 (노드별 개별 기능 검증)
> **작성일**: 2026-02-13

---

## 노드별 단위 테스트

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|------|------|--------|----------|-----------|--------|------|
| **제어기** | 제어 | IVI Control ECU | 사용자 입력 수신 및 CAN 메시지 전송 (모드 선택, 조명 색상, 프로필) | - | IVI 팀 | - |
| | | vECU (IVI vECU) | 조명 제어 로직, ADAS 연계 경고 로직, OTA 관리, 진단 기능 수행 | - | IVI 팀 | - |
| | | Lighting Control ECU | RGB LED PWM 신호 생성, 밝기 제어, 점멸 패턴 제어 | - | Body 팀 | - |
| | | BDC | 도어 락 제어, 창문 제어, 시트 위치 제어 | - | Body 팀 | - |
| | | Gateway | 도메인 간 CAN 메시지 라우팅, 메시지 필터링 | - | Gateway 팀 | - |
| | | Cluster ECU | 클러스터 UI 표시 (속도, 기어, 경고 메시지, ADAS 상태) | - | Cluster 팀 | - |
| | | ADAS Control ECU | ADAS 센서 데이터 처리 및 이벤트 생성 (LDW, AEB, 후방 장애물) | - | ADAS 팀 | - |
| | | Transmission Control ECU | 변속 상태 관리 및 전송 (P/R/N/D) | - | Powertrain 팀 | - |
| | | HVAC Control ECU | 온도 정보 수신 및 조명 연동 신호 전송 | - | Chassis 팀 | - |
| | | Diagnostic Service ECU | UDS 서비스 처리, DTC 관리, OTA 다운로드 | - | Diagnostic 팀 | - |
| | | Fail-Safe Manager | 오류 감지 및 Fail-Safe 모드 진입, 안전 상태 전이 | - | Safety 팀 | - |
| **가상 노드 (Simulator)** | 입력 | 시동 스위치 | 차량 시동 ON/OFF | - | 공통 | - |
| | | 운전자 프로필 선택 | 프로필 1/2/3 선택 | - | 공통 | - |
| | | IVI 모드 선택 | 스포츠/에코/컴포트 모드 선택 | - | 공통 | - |
| | | 조명 색상 선택 | RGB 색상 선택 (0~255) | - | 공통 | - |
| | | 차량 속도 입력 | 속도 값 입력 (0~255 km/h) | - | 공통 | - |
| | | 변속 기어 선택 | P/R/N/D 기어 선택 | - | 공통 | - |
| | | 도어 개방 신호 | 도어 개방/폐쇄 입력 | - | 공통 | - |
| | | ADAS 이벤트 입력 | LDW, AEB, 후방 장애물 이벤트 입력 | - | 공통 | - |
| | 출력 | 앰비언트 조명 표시 | RGB 색상 및 밝기 출력 | - | 공통 | - |
| | | 시트조명 표시 | 시트조명 ON/OFF 출력 | - | 공통 | - |
| | | 후방 조명 표시 | 후방 조명 ON/OFF 출력 | - | 공통 | - |
| | | 경고 UI 표시 | 클러스터 경고 UI 출력 | - | 공통 | - |
| | | 경고음 출력 | 경고음 재생 여부 출력 | - | 공통 | - |
| | | 진단 결과 표시 | 진단 Pass/Fail 출력 | - | 공통 | - |
| | | OTA 진행률 표시 | OTA 진행률 0~100% 출력 | - | 공통 | - |

---

## 단위 테스트 케이스 상세

### TC_UT_001: IVI Control ECU - 모드 선택

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_001 |
| **Test Name** | IVI Control ECU 모드 선택 기능 테스트 |
| **Pre-condition** | IVI Control ECU 초기화 완료 |
| **Test Steps** | 1. 스포츠 모드 버튼 클릭<br>2. CAN 메시지 frmIVI_ModeSelect (0x100) 확인<br>3. ModeSelected 신호 값 확인 (2: 스포츠) |
| **Expected Result** | frmIVI_ModeSelect 메시지 전송, ModeSelected = 2 |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_002: vECU - 속도 기반 조명 색상 제어

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_002 |
| **Test Name** | vECU 속도 기반 조명 색상 제어 로직 테스트 |
| **Pre-condition** | vECU 초기화 완료, 스포츠 모드 선택 |
| **Test Steps** | 1. 차량 속도 30km/h 입력<br>2. vECU에서 frmLighting_AmbientCtrl (0x200) 메시지 확인<br>3. AmbientR=0, AmbientG=255, AmbientB=0 (녹색) 확인 |
| **Expected Result** | 0~50km/h: 녹색 (R=0, G=255, B=0) |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_003: Lighting Control ECU - RGB LED 제어

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_003 |
| **Test Name** | Lighting Control ECU RGB LED PWM 신호 생성 테스트 |
| **Pre-condition** | Lighting Control ECU 초기화 완료 |
| **Test Steps** | 1. frmLighting_AmbientCtrl (0x200) 메시지 수신 (R=255, G=0, B=0)<br>2. PWM 신호 출력 확인<br>3. 실제 LED 색상 확인 (빨간색) |
| **Expected Result** | PWM 신호 정상 출력, LED 빨간색 점등 |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_004: Gateway - 메시지 라우팅

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_004 |
| **Test Name** | Gateway 도메인 간 메시지 라우팅 테스트 |
| **Pre-condition** | Gateway 초기화 완료 |
| **Test Steps** | 1. Infotainment CAN에서 frmIVI_ModeSelect (0x100) 메시지 송신<br>2. Gateway에서 메시지 수신 확인<br>3. Body CAN으로 메시지 전달 확인 |
| **Expected Result** | 메시지가 Infotainment CAN에서 Body CAN으로 정상 라우팅 |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_005: ADAS Control ECU - LDW 이벤트 생성

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_005 |
| **Test Name** | ADAS Control ECU 차선 이탈 경고 이벤트 생성 테스트 |
| **Pre-condition** | ADAS Control ECU 초기화 완료 |
| **Test Steps** | 1. 차선 이탈 센서 입력 (LDW=1, Direction=0)<br>2. frmADAS_LDW_Event (0x300) 메시지 확인<br>3. LDW_Event=1, LDW_Direction=0 확인 |
| **Expected Result** | frmADAS_LDW_Event 메시지 전송, LDW_Event=1 |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_006: Diagnostic Service ECU - UDS 0x14 (ClearDTC)

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_006 |
| **Test Name** | Diagnostic Service ECU UDS 0x14 DTC 삭제 테스트 |
| **Pre-condition** | Diagnostic Service ECU 초기화 완료, DTC 3개 저장 |
| **Test Steps** | 1. frmDiag_Request (0x7DF) 메시지 송신 (Service ID=0x14)<br>2. Diagnostic Service ECU에서 DTC 메모리 초기화<br>3. frmDiag_Response (0x7E8) 메시지 확인 (Positive Response 0x54) |
| **Expected Result** | Positive Response (0x54) 수신, DTC 개수 = 0 |
| **Actual Result** | - |
| **Pass/Fail** | - |

### TC_UT_007: Fail-Safe Manager - Fail-Safe 모드 진입

| 항목 | 내용 |
|------|------|
| **Test ID** | TC_UT_007 |
| **Test Name** | Fail-Safe Manager 오류 감지 및 Fail-Safe 모드 진입 테스트 |
| **Pre-condition** | Fail-Safe Manager 초기화 완료 |
| **Test Steps** | 1. Lighting Control ECU로 제어 명령 2회 연속 실패 시뮬레이션<br>2. Fail-Safe Manager에서 오류 감지<br>3. frmFailSafe_Status (0x702) 메시지 확인 (FailSafeMode=1) |
| **Expected Result** | Fail-Safe 모드 진입, 조명 50% 밝기로 설정 |
| **Actual Result** | - |
| **Pass/Fail** | - |

---

**다음 단계**: 06_Integration Test (통합 테스트) 작성
