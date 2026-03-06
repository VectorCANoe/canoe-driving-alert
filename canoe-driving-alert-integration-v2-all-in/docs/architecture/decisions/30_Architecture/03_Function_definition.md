# 03_Function definition (기능 정의)

## IVI vECU 프로젝트 기능 정의

> **작성 기준**: 멘토 샘플 형식 준수 (입력부, 제어부, 출력부 명확히 구분)
> **작성일**: 2026-02-13

---

## 1. 가상노드 (Simulator) - 입출력 기능

### 📥 입력 (Input)

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------|--------|----------|------|------|
| **입력** | 시동 스위치 | 차량의 시동 버튼 구현 (IGN ON/OFF) | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | 운전자 프로필 선택 | 운전자 프로필 (1/2/3) 선택 버튼 | Switch/Indicator 이용하여 프로필 전환 | ✅ |
| **입력** | IVI 모드 선택 | 스포츠/에코/컴포트 모드 선택 버튼 | Switch/Indicator 이용하여 모드 표현 | ✅ |
| **입력** | 조명 색상 선택 | 사용자가 선호하는 조명 색상 선택 (RGB) | ColorPicker 또는 TrackBar 사용 | ✅ |
| **입력** | 조명 밝기 조절 | 조명 밝기 값 입력 (0 ~ 100%) | TrackBar 사용하여 값 조절 | ✅ |
| **입력** | 차량 속도 입력 | 차량 속도 정보 입력 (0 ~ 255 km/h) | TrackBar 사용하여 값 조절 | ✅ |
| **입력** | 변속 기어 선택 | P/R/N/D 기어 상태 변경 | Switch/Indicator 이용하여 P/R/N/D 표현 | ✅ |
| **입력** | 도어 개방 신호 | 운전석/조수석/후석 도어 개방 여부 (0: 닫힘, 1: 열림) | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | HVAC 온도 설정 | 실내 온도 설정 값 입력 (-20 ~ 40°C) | TrackBar 사용하여 값 조절 | ✅ |
| **입력** | 와이퍼 동작 상태 | 와이퍼 동작 여부 및 속도 (0: OFF, 1~3: 속도) | Switch/Indicator 이용하여 상태 표현 | ✅ |
| **입력** | ADAS 차선 이탈 경고 | LDW 이벤트 발생 여부 (0: 정상, 1: 이탈) | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | ADAS 후방 장애물 거리 | 후방 장애물까지의 거리 (0 ~ 255 cm) | TrackBar 사용하여 값 조절 | ✅ |
| **입력** | ADAS 긴급 제동 이벤트 | AEB 이벤트 발생 여부 (0: 정상, 1: 긴급 제동) | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | 시트 점유 센서 | 뒷좌석 탑승 여부 감지 (0: 없음, 1: 있음) | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | 외부 조도 센서 | 외부 밝기 값 (0: 어두움 ~ 100: 밝음) | TrackBar 사용하여 값 조절 | ✅ |
| **입력** | 진단 모드 진입 | 정비 모드 진입 버튼 | Switch/Indicator 이용하여 ON/OFF 표현 | ✅ |
| **입력** | OTA 업데이트 시작 | OTA 업데이트 시작 트리거 버튼 | Button 사용 | ✅ |
| **입력** | 사용자 피드백 입력 | 경고/조명에 대한 사용자 불만 신고 버튼 | Button 사용 | ✅ |

---

### 📤 출력 (Output)

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------|--------|----------|------|------|
| **출력** | 차량 속도 표시 | 현재 차량 속도 출력 (0 ~ 255 km/h) | Switch/Indicator 이용하여 속도 값 출력 | ✅ |
| **출력** | 기어 상태 표시 | P/R/N/D 기어 상태 변화 출력 | Switch/Indicator 이용하여 기어 현재상태 값 출력 | ✅ |
| **출력** | 앰비언트 조명 색상 | 실내 앰비언트 조명 현재 색상 (RGB) | ColorIndicator 이용하여 색상 출력 | ✅ |
| **출력** | 앰비언트 조명 밝기 | 실내 앰비언트 조명 현재 밝기 (0 ~ 100%) | Switch/Indicator 이용하여 밝기 값 출력 | ✅ |
| **출력** | 시트조명 상태 | 시트조명 ON/OFF 상태 | Switch/Indicator 이용하여 ON/OFF 출력 | ✅ |
| **출력** | 후방 조명 상태 | 후방 조명 ON/OFF 상태 | Switch/Indicator 이용하여 ON/OFF 출력 | ✅ |
| **출력** | 바닥·발판 조명 상태 | 바닥·발판 조명 ON/OFF 상태 및 밝기 | Switch/Indicator 이용하여 상태 출력 | ✅ |
| **출력** | 경고 UI 표시 | 대시보드/센터페시아 경고 UI 표시 여부 | Switch/Indicator 이용하여 경고 UI ON/OFF 출력 | ✅ |
| **출력** | 경고음 출력 | 경고음 재생 여부 (0: OFF, 1: ON) | Switch/Indicator 이용하여 ON/OFF 출력 | ✅ |
| **출력** | ADAS 상태 아이콘 | 현재 ADAS 기능 활성 상태 아이콘 표시 | Switch/Indicator 이용하여 아이콘 출력 | ✅ |
| **출력** | 클러스터 메시지 | 클러스터 영역에 텍스트 메시지 출력 (후진 안내, 휴식 권장 등) | TextIndicator 이용하여 메시지 출력 | ✅ |
| **출력** | 진단 결과 표시 | 자가진단 수행 결과 (Pass/Fail) 그래픽 표시 | Switch/Indicator 이용하여 Pass/Fail 출력 | ✅ |
| **출력** | OTA 진행 상태 | OTA 업데이트 진행률 (0 ~ 100%) | ProgressBar 이용하여 진행률 출력 | ✅ |
| **출력** | 시트 위치 상태 | 현재 시트 위치 (정상/후진용) | Switch/Indicator 이용하여 위치 출력 | ✅ |
| **출력** | 페일세이프 상태 | Fail-Safe 모드 진입 여부 (0: 정상, 1: Fail-Safe) | Switch/Indicator 이용하여 ON/OFF 출력 | ✅ |

---

## 2. ECU 동작 (Control Logic)

### 🔧 제어 ECU

| 분류 | ECU명 | 기능설명 | 비고 | 검증 |
|------|-------|----------|------|------|
| **제어** | **IVI Control ECU** | 사용자 입력 수신 및 vECU로 제어 명령 전달 (모드 선택, 조명 색상/밝기, 프로필 관리, 설정 변경 등) | CAPL 로직 추가 (사용자 입력 처리) | ✅ |
| **제어** | **vECU (IVI vECU)** | 전체 조명, 경고, ADAS 연계 UI 제어 로직 수행 <br> - 조명 테마 적용 <br> - 속도/온도/기상 조건 기반 조명 제어 <br> - ADAS 연계 경고 UI 제어 <br> - OTA 업데이트 관리 <br> - 진단 기능 수행 | CAPL 메인 로직 (모든 요구사항 구현) | ✅ |
| **제어** | **Lighting Control ECU** | 앰비언트 조명, 시트조명, 후방 조명, 바닥·발판 조명 실제 제어 <br> - PWM 신호 생성 <br> - RGB 색상 제어 <br> - 밝기 제어 <br> - 점멸 패턴 제어 | CAPL PWM 로직 추가 | ✅ |
| **제어** | **BDC (Body Domain Controller)** | 도어 락, 창문, 시트 위치 제어 <br> - 도어 개방/폐쇄 상태 모니터링 <br> - 승하차 UX 연동 <br> - 어린이 보호 모드 실행 | CAPL 바디 제어 로직 추가 | ✅ |
| **제어** | **Gateway** | Powertrain, Chassis, Body, Infotainment, ADAS 도메인 간 CAN 메시지 라우팅 <br> - 메시지 필터링 <br> - 메시지 전달 <br> - 버스 간 중계 | CAPL 메시지 복사 및 전달 | ✅ |
| **제어** | **Cluster ECU** | 클러스터 UI 제어 <br> - 차량 속도, 기어 상태 표시 <br> - 경고 메시지 표시 (후진 안내, 휴식 권장) <br> - ADAS 상태 아이콘 표시 | CAPL UI 제어 로직 추가 | ✅ |
| **제어** | **ADAS Control ECU** | ADAS 센서 데이터 처리 및 이벤트 생성 <br> - 차선 이탈 경고 (LDW) <br> - 후방 장애물 감지 <br> - 긴급 제동 (AEB) <br> - 후측방 객체 감지 | CAPL ADAS 로직 추가 (센서 시뮬레이션) | ✅ |
| **제어** | **HVAC Control ECU** | 온도 정보 수신 및 조명 연동 <br> - 실내 온도 측정 <br> - 온도 구간별 조명 색상 제어 신호 전송 | CAPL 온도 연동 로직 추가 | ✅ |
| **제어** | **Transmission Control ECU** | 변속 상태 관리 및 전송 <br> - P/R/N/D 상태 관리 <br> - 후진 시 UX 제어 신호 전송 | CAPL 변속 로직 추가 | ✅ |
| **제어** | **Diagnostic Service ECU** | 진단 서비스 제공 <br> - UDS 0x14 (ClearDTC) <br> - UDS 0x22 (ReadDataByIdentifier) <br> - UDS 0x2E (WriteDataByIdentifier) <br> - UDS 0x34/0x36/0x37 (OTA Download) <br> - DTC 생성 및 관리 | CAPL UDS 서비스 로직 추가 | ✅ |
| **제어** | **Fail-Safe Manager** | 오류 감지 및 Fail-Safe 모드 진입 <br> - 센서 오류 감지 <br> - CAN 통신 오류 감지 <br> - 조명 제어 실패 감지 <br> - 안전 상태 전이 | CAPL Fail-Safe 로직 추가 | ✅ |

---

## 3. 시스템 변수 (System Variables)

CANoe 시스템 변수를 통해 ECU 간 정보 공유 및 UI 제어

| Namespace | 변수명 | 데이터 타입 | 설명 | 검증 |
|-----------|--------|------------|------|------|
| **IVI** | IgnStart | uint32 | 시동 여부 판단 (0: OFF, 1: ON) | ✅ |
| **IVI** | ProfileSelected | uint32 | 선택된 프로필 (1/2/3) | ✅ |
| **IVI** | ModeSelected | uint32 | 선택된 모드 (0: 에코, 1: 컴포트, 2: 스포츠) | ✅ |
| **Lighting** | AmbientColorR | uint8 | 앰비언트 조명 색상 R (0~255) | ✅ |
| **Lighting** | AmbientColorG | uint8 | 앰비언트 조명 색상 G (0~255) | ✅ |
| **Lighting** | AmbientColorB | uint8 | 앰비언트 조명 색상 B (0~255) | ✅ |
| **Lighting** | AmbientBrightness | uint8 | 앰비언트 조명 밝기 (0~100%) | ✅ |
| **Lighting** | SeatLightOn | uint8 | 시트조명 ON/OFF (0: OFF, 1: ON) | ✅ |
| **Lighting** | RearLightOn | uint8 | 후방 조명 ON/OFF (0: OFF, 1: ON) | ✅ |
| **Lighting** | FootLightOn | uint8 | 바닥·발판 조명 ON/OFF (0: OFF, 1: ON) | ✅ |
| **Vehicle** | VehicleSpeed | uint8 | 차량 속도 (0~255 km/h) | ✅ |
| **Vehicle** | GearStatus | uint8 | 기어 상태 (0: P, 1: R, 2: N, 3: D) | ✅ |
| **Vehicle** | DoorStatus | uint8 | 도어 개방 상태 (비트맵: 0x01=운전석, 0x02=조수석, 0x04=후석) | ✅ |
| **HVAC** | InteriorTemp | int8 | 실내 온도 (-20~40°C) | ✅ |
| **Weather** | WiperStatus | uint8 | 와이퍼 상태 (0: OFF, 1~3: 속도) | ✅ |
| **Weather** | ExteriorBrightness | uint8 | 외부 밝기 (0~100) | ✅ |
| **ADAS** | LDW_Event | uint8 | 차선 이탈 경고 (0: 정상, 1: 이탈) | ✅ |
| **ADAS** | RearObstacleDistance | uint8 | 후방 장애물 거리 (0~255 cm) | ✅ |
| **ADAS** | AEB_Event | uint8 | 긴급 제동 이벤트 (0: 정상, 1: 긴급 제동) | ✅ |
| **Safety** | WarningUIActive | uint8 | 경고 UI 활성 여부 (0: OFF, 1: ON) | ✅ |
| **Safety** | WarningSoundActive | uint8 | 경고음 활성 여부 (0: OFF, 1: ON) | ✅ |
| **Safety** | FailSafeMode | uint8 | Fail-Safe 모드 (0: 정상, 1: Fail-Safe) | ✅ |
| **Diagnostic** | DTCCount | uint16 | 저장된 DTC 개수 | ✅ |
| **Diagnostic** | DiagModeActive | uint8 | 진단 모드 활성 (0: 비활성, 1: 활성) | ✅ |
| **OTA** | OTAProgress | uint8 | OTA 진행률 (0~100%) | ✅ |
| **OTA** | OTAStatus | uint8 | OTA 상태 (0: 대기, 1: 진행중, 2: 성공, 3: 실패) | ✅ |

---

## 4. 기능별 상세 설명

### 4.1 조명 제어 기능

#### 스포츠모드 속도연동 앰비언트조명 (Req_001)
- **입력**: IVI 모드 선택 (스포츠), 차량 속도
- **제어**: vECU에서 속도 구간 판단
  - 0~50km/h → RGB(0, 255, 0) 녹색
  - 50~100km/h → RGB(0, 0, 255) 파란색
  - 100km/h 이상 → RGB(255, 0, 0) 빨간색
- **출력**: Lighting Control ECU로 RGB 값 전송 → 앰비언트 조명 색상 변경

#### 온도연동 조명제어 (Req_005)
- **입력**: HVAC 실내 온도
- **제어**: vECU에서 온도 구간 판단
  - 18°C 이하 → RGB(0, 100, 255) 차가운 파란색
  - 18~24°C → RGB(255, 255, 255) 중립 흰색
  - 24°C 이상 → RGB(255, 100, 0) 따뜻한 주황색
- **출력**: Lighting Control ECU로 RGB 값 전송

#### 조명 테마 자동 적용 (Req_038)
- **입력**: IVI 모드 선택 (스포츠/에코/컴포트)
- **제어**: vECU에서 모드별 테마 패키지 로드
  - 스포츠: 높은 밝기, 역동적 색상 (빨강, 주황)
  - 에코: 낮은 밝기, 차분한 색상 (녹색, 파란색)
  - 컴포트: 중간 밝기, 편안한 색상 (흰색, 베이지)
- **출력**: Lighting Control ECU로 색상·밝기·효과 패키지 전송

---

### 4.2 안전 경고 기능

#### 후진 안전경고 UI 및 시트조명 (Req_002)
- **입력**: 변속 상태 (D → R), 차량 속도
- **제어**: vECU에서 후진 진입 감지 → 경고 UI 활성화, 시트조명 ON
- **출력**: Cluster ECU로 경고 UI 표시, Lighting Control ECU로 시트조명 ON (최소 3초 유지)

#### 후진중 도어개방 경고제어 (Req_006)
- **입력**: 변속 상태 (R), 도어 개방 신호
- **제어**: vECU에서 위험 상황 판단 → 경고 UI 활성화, 경고 조명 점멸
- **출력**: Cluster ECU로 경고 UI 표시, Lighting Control ECU로 경고 조명 점멸 (빨간색)

#### 차선 이탈 시 ADAS 연계 시각적 경고 (Req_027)
- **입력**: ADAS 차선 이탈 경고 (LDW_Event = 1)
- **제어**: vECU에서 ADAS 이벤트 수신 → 시각적 경고 UI 활성화
- **출력**: Cluster ECU로 경고 UI 표시, Lighting Control ECU로 앰비언트 조명 점멸 (노란색)

---

### 4.3 진단/OTA 기능

#### UDS0x14 DTC삭제 (Req_011)
- **입력**: 진단 테스터에서 UDS 0x14 명령 수신
- **제어**: Diagnostic Service ECU에서 DTC 메모리 초기화
- **출력**: Positive Response (0x54) 전송

#### UDS0x34 OTA다운로드 (Req_012)
- **입력**: 진단 테스터에서 UDS 0x34 명령 + 데이터 수신
- **제어**: Diagnostic Service ECU에서 OTA 패키지 수신 및 저장
- **출력**: Positive Response (0x74) 전송, OTA 진행률 업데이트

#### OTA실패 자동복구 (Req_014)
- **입력**: OTA 업데이트 중 오류 발생 (전원 차단, 통신 오류 등)
- **제어**: vECU에서 오류 감지 → 이전 버전으로 자동 롤백
- **출력**: OTA 상태 = 3 (실패), 시스템 재시작 후 이전 버전으로 복구

---

### 4.4 페일세이프 기능

#### 조명 제어 안전 모니터링 (Req_053)
- **입력**: Lighting Control ECU로 제어 명령 2회 이상 연속 실패
- **제어**: Fail-Safe Manager에서 오류 감지 → Fail-Safe 모드 진입
- **출력**: 모든 조명 기본값 50% 밝기로 설정, FailSafeMode = 1

#### 오류 발생 시 안전 상태 전이 (Req_023)
- **입력**: 센서 오류 (Timeout, Invalid Value), CAN 통신 오류 (Message Loss)
- **제어**: Fail-Safe Manager에서 오류 감지 → 안전 상태로 전이
- **출력**: UX 기능 비활성화, 기본 조명 유지, FailSafeMode = 1

---

## 5. CANoe 구현 가이드

### 5.1 CAPL 노드 구조

```
IVI Control ECU (CAPL)
  └─ 사용자 입력 처리 (버튼, TrackBar, ColorPicker 등)

vECU (IVI vECU) (CAPL)
  ├─ 조명 제어 로직
  ├─ ADAS 연계 경고 로직
  ├─ 진단/OTA 로직
  └─ Fail-Safe 로직

Lighting Control ECU (CAPL)
  ├─ PWM 신호 생성
  ├─ RGB 색상 제어
  └─ 밝기 제어

BDC (Body Domain Controller) (CAPL)
  ├─ 도어 락 제어
  ├─ 창문 제어
  └─ 시트 위치 제어

Gateway (CAPL)
  └─ 메시지 라우팅 (Powertrain, Chassis, Body, Infotainment, ADAS)

Cluster ECU (CAPL)
  └─ UI 표시 (속도, 기어, 경고 메시지, ADAS 상태)

ADAS Control ECU (CAPL)
  ├─ LDW 이벤트 생성
  ├─ 후방 장애물 감지
  └─ AEB 이벤트 생성

HVAC Control ECU (CAPL)
  └─ 온도 정보 전송

Transmission Control ECU (CAPL)
  └─ 변속 상태 전송

Diagnostic Service ECU (CAPL)
  ├─ UDS 서비스 처리
  ├─ DTC 관리
  └─ OTA 다운로드

Fail-Safe Manager (CAPL)
  ├─ 오류 감지
  └─ 안전 상태 전이
```

### 5.2 시스템 변수 활용

- CANoe Panel에서 시스템 변수를 통해 실시간 모니터링
- Switch/Indicator로 입출력 시각화
- CAPL에서 `@sysvar` 키워드로 시스템 변수 접근

---

## 6. 검증 방법

| 분류 | 검증 방법 | 비고 |
|------|----------|------|
| **입력 기능** | CANoe Panel에서 입력 버튼/TrackBar 조작 후 CAN 메시지 확인 | 모든 입력이 정상적으로 CAN 메시지로 변환되는지 확인 |
| **출력 기능** | CAN 메시지 전송 후 CANoe Panel Indicator 변화 확인 | 모든 출력이 정상적으로 표시되는지 확인 |
| **ECU 동작** | Trace 윈도우에서 CAN 메시지 흐름 확인 | 각 ECU가 정상적으로 메시지를 송수신하는지 확인 |
| **시스템 변수** | Watch 윈도우에서 시스템 변수 값 실시간 모니터링 | 변수 값이 예상대로 변경되는지 확인 |
| **통합 테스트** | 요구사항 기반 시나리오 테스트 (06_Integration Test 참고) | 여러 ECU가 협력하는 시나리오 검증 |

---

**다음 단계**: 0301_SysFuncAnalysis (시스템 기능 분석) 작성
