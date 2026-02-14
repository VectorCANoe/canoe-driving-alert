# 0301_SysFuncAnalysis (시스템 기능 분석)

## IVI vECU 프로젝트 시스템 기능 분석

> **작성 기준**: 멘토 샘플 형식 준수 (도메인별 노드 기능 상세)
> **작성일**: 2026-02-13

---

## 도메인별 ECU 기능 분석

### 🔷 Infotainment Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **IVI Control ECU** | IVI 화면 입력 처리 (모드 선택, 조명 설정, 프로필 관리, 사용자 피드백 등), 사용자 입력을 vECU로 전송 | CANoe Panel 연동 |
| **vECU (IVI vECU)** | 전체 조명/경고/ADAS 연계 UI 제어 로직 수행, 조명 테마 적용, 속도/온도/기상 조건 기반 조명 제어, ADAS 연계 경고 UI 제어, OTA 업데이트 관리, 진단 기능 수행 | 메인 제어 노드 |
| **Cluster ECU** | 클러스터 UI 제어, 차량 속도/기어 상태 표시, 경고 메시지 표시 (후진 안내, 휴식 권장), ADAS 상태 아이콘 표시 | 운전자 정보 표시 |

---

### 🔷 Body Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Lighting Control ECU** | 앰비언트 조명, 시트조명, 후방 조명, 바닥·발판 조명 제어, PWM 신호 생성, RGB 색상 제어, 밝기 제어, 점멸 패턴 제어 | 실제 조명 액추에이터 제어 |
| **BDC (Body Domain Controller)** | 도어 락 제어, 창문 제어, 시트 위치 제어, 도어 개방/폐쇄 상태 모니터링, 승하차 UX 연동, 어린이 보호 모드 실행 | 바디 통합 제어 |
| **Door Status Sensor** | 운전석/조수석/후석 도어 개방 여부 감지 (0: 닫힘, 1: 열림), CAN 신호로 전송 | 센서 노드 |
| **Seat Occupancy Sensor** | 뒷좌석 탑승 여부 감지 (0: 없음, 1: 있음), CAN 신호로 전송 | 센서 노드 |
| **Exterior Brightness Sensor** | 외부 밝기 측정 (0: 어두움 ~ 100: 밝음), CAN 신호로 전송 | 센서 노드 |

---

### 🔷 ADAS Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **ADAS Control ECU** | ADAS 센서 데이터 처리 및 이벤트 생성, 차선 이탈 경고 (LDW), 후방 장애물 감지, 긴급 제동 (AEB), 후측방 객체 감지 | ADAS 통합 제어 |
| **LDW Sensor** | 차선 이탈 여부 감지 (0: 정상, 1: 이탈), CAN 신호로 전송 | 차선 감지 센서 |
| **Rear Obstacle Sensor** | 후방 장애물까지의 거리 측정 (0~255 cm), CAN 신호로 전송 | 초음파/레이더 센서 |
| **AEB Sensor** | 전방 충돌 위험 감지 및 긴급 제동 이벤트 생성 (0: 정상, 1: 긴급 제동), CAN 신호로 전송 | 카메라/레이더 센서 |
| **Side Object Sensor** | 후측방 이동 객체 감지 (0: 없음, 1: 있음), CAN 신호로 전송 | 후측방 레이더 센서 |

---

### 🔷 Powertrain Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Transmission Control ECU** | 변속 상태 관리 및 전송, P/R/N/D 상태 관리, 후진 시 UX 제어 신호 전송 | 변속기 제어 |
| **Vehicle Speed Sensor** | 차량 속도 측정 (0~255 km/h), CAN 신호로 전송 | 속도 센서 |

---

### 🔷 Chassis Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **HVAC Control ECU** | 온도 정보 수신 및 조명 연동, 실내 온도 측정, 온도 구간별 조명 색상 제어 신호 전송 | HVAC 제어 |
| **Wiper Control ECU** | 와이퍼 동작 상태 관리 (0: OFF, 1~3: 속도), 레인센서 정보 수신, CAN 신호로 전송 | 와이퍼 제어 |
| **Rain Sensor** | 비/눈 감지 (0: 없음, 1~3: 강도), CAN 신호로 전송 | 레인 센서 |

---

### 🔷 Gateway

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Central Gateway** | Powertrain, Chassis, Body, Infotainment, ADAS 도메인 간 CAN 메시지 라우팅, 메시지 필터링, 메시지 전달, 버스 간 중계 | 중앙 게이트웨이 |

---

### 🔷 Diagnostic Domain

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Diagnostic Service ECU** | 진단 서비스 제공, UDS 0x14 (ClearDTC), UDS 0x22 (ReadDataByIdentifier), UDS 0x2E (WriteDataByIdentifier), UDS 0x34/0x36/0x37 (OTA Download), DTC 생성 및 관리 | 진단 서비스 노드 |
| **Fail-Safe Manager** | 오류 감지 및 Fail-Safe 모드 진입, 센서 오류 감지, CAN 통신 오류 감지, 조명 제어 실패 감지, 안전 상태 전이 | 안전 관리 노드 |

---

### 🔷 Actual Devices (실제 장치)

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Ambient Light** | 실제 앰비언트 조명, RGB LED 제어 신호 수신하여 색상 및 밝기 조정 | 실제 LED 액추에이터 |
| **Seat Light** | 실제 시트조명, ON/OFF 신호 수신하여 점등/소등 | 실제 LED 액추에이터 |
| **Rear Light** | 실제 후방 조명, ON/OFF 신호 수신하여 점등/소등 | 실제 LED 액추에이터 |
| **Foot Light** | 실제 바닥·발판 조명, ON/OFF 및 밝기 신호 수신하여 점등/소등 | 실제 LED 액추에이터 |
| **Cluster Display** | 실제 클러스터 디스플레이, UI 표시 명령 수신하여 화면 렌더링 | 실제 TFT LCD |
| **Door Lock Actuator** | 실제 도어 락 액추에이터, 락/언락 신호 수신하여 동작 | 실제 모터 |
| **Window Actuator** | 실제 창문 액추에이터, 개폐 신호 수신하여 동작 | 실제 모터 |
| **Seat Actuator** | 실제 시트 위치 액추에이터, 위치 변경 신호 수신하여 동작 | 실제 모터 |
| **Warning Speaker** | 실제 경고음 스피커, 경고음 출력 신호 수신하여 재생 | 실제 스피커 |

---

## 도메인 간 데이터 흐름 (High-Level)

```
┌────────────────────────────────────────────────────────────────┐
│                     Infotainment Domain                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │ IVI Control  │ → │   vECU       │ ← │  Cluster     │      │
│  │     ECU      │   │ (IVI vECU)   │   │     ECU      │      │
│  └──────────────┘   └──────┬───────┘   └──────────────┘      │
└────────────────────────────┼────────────────────────────────────┘
                              │
                      ┌───────┴────────┐
                      │ Central Gateway│
                      └───────┬────────┘
          ┌───────────────────┼───────────────────┐
          │                   │                   │
┌─────────▼─────────┐ ┌───────▼────────┐ ┌───────▼────────┐
│   Body Domain     │ │ ADAS Domain    │ │ Powertrain     │
│ ┌───────────────┐ │ │ ┌────────────┐ │ │ ┌────────────┐ │
│ │ Lighting Ctrl │ │ │ │ ADAS Ctrl  │ │ │ │ Trans Ctrl │ │
│ │      ECU      │ │ │ │     ECU    │ │ │ │     ECU    │ │
│ └───────────────┘ │ │ └────────────┘ │ │ └────────────┘ │
│ ┌───────────────┐ │ │ ┌────────────┐ │ │ ┌────────────┐ │
│ │      BDC      │ │ │ │ LDW Sensor │ │ │ │   Speed    │ │
│ └───────────────┘ │ │ └────────────┘ │ │ │   Sensor   │ │
└───────────────────┘ └────────────────┘ │ └────────────┘ │
                                          └────────────────┘
┌─────────────────────────────────────────────────────────┐
│   Diagnostic Domain                                     │
│ ┌──────────────────┐   ┌──────────────────┐           │
│ │ Diagnostic Svc   │   │  Fail-Safe Mgr   │           │
│ │       ECU        │   │                  │           │
│ └──────────────────┘   └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

---

## 주요 시나리오별 노드 협력

### 시나리오 1: 스포츠모드 속도연동 조명 (Req_001)

```
IVI Control ECU (모드 선택: 스포츠)
  → vECU (모드 수신, 속도 기반 색상 계산)
  → Lighting Control ECU (RGB 값 수신)
  → Ambient Light (실제 색상 출력)

Vehicle Speed Sensor (속도 전송)
  → Central Gateway (메시지 라우팅)
  → vECU (속도 수신)
```

### 시나리오 2: 후진 안전경고 UI 및 시트조명 (Req_002)

```
Transmission Control ECU (기어 변경: D → R)
  → Central Gateway (메시지 라우팅)
  → vECU (후진 진입 감지)
    ├─→ Cluster ECU (경고 UI 표시)
    └─→ Lighting Control ECU (시트조명 ON)
         → Seat Light (실제 점등)
```

### 시나리오 3: 차선 이탈 시 ADAS 연계 경고 (Req_027)

```
LDW Sensor (차선 이탈 감지)
  → ADAS Control ECU (LDW 이벤트 생성)
  → Central Gateway (메시지 라우팅)
  → vECU (LDW 이벤트 수신)
    ├─→ Cluster ECU (경고 UI 표시)
    └─→ Lighting Control ECU (조명 점멸)
         → Ambient Light (실제 점멸)
```

### 시나리오 4: OTA 업데이트 (Req_012)

```
진단 테스터 (UDS 0x34 명령 전송)
  → Diagnostic Service ECU (OTA 패키지 수신)
  → vECU (OTA 진행 상태 업데이트)
  → Cluster ECU (진행률 표시)
```

### 시나리오 5: 조명 제어 실패 시 Fail-Safe (Req_053)

```
vECU (조명 제어 명령 전송)
  → Lighting Control ECU (제어 실패 응답)
  → vECU (2회 연속 실패 감지)
  → Fail-Safe Manager (Fail-Safe 모드 진입)
  → Lighting Control ECU (기본값 50% 밝기 설정)
```

---

**다음 단계**: 0302_NWflowDef (네트워크 흐름 정의) 작성
