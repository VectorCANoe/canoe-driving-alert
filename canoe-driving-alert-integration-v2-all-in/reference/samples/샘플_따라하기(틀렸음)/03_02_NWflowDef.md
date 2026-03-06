# 0302_NWflowDef (네트워크 흐름 정의)

## IVI vECU 프로젝트 네트워크 흐름 정의

> **작성 기준**: 멘토 샘플 형식 준수 (메시지 흐름 테이블)
> **작성일**: 2026-02-13

---

## CAN 메시지 정의 및 흐름

### 📊 메시지 목록 (Message List)

| Channel | ID (hex) | Message Name | DLC | Function | Cycle (ms) | Tx ECU | Rx ECU | 비고 |
|---------|----------|--------------|-----|----------|-----------|--------|--------|------|
| **Infotainment** | 0x100 | frmIVI_ModeSelect | 2 | IVI 모드 선택 (스포츠/에코/컴포트) | 100 | IVI Control ECU | vECU | 사용자 입력 |
| **Infotainment** | 0x101 | frmIVI_LightColorSet | 4 | 조명 색상 설정 (RGB) | 200 | IVI Control ECU | vECU | 사용자 입력 |
| **Infotainment** | 0x102 | frmIVI_ProfileSelect | 1 | 운전자 프로필 선택 (1/2/3) | 500 | IVI Control ECU | vECU | 사용자 입력 |
| **Infotainment** | 0x103 | frmIVI_UserFeedback | 2 | 사용자 피드백 (불만 신고) | Event | IVI Control ECU | vECU | 이벤트 기반 |
| **Body** | 0x200 | frmLighting_AmbientCtrl | 5 | 앰비언트 조명 제어 (RGB + 밝기) | 50 | vECU | Lighting Control ECU | 조명 제어 |
| **Body** | 0x201 | frmLighting_SeatCtrl | 1 | 시트조명 제어 (ON/OFF) | 100 | vECU | Lighting Control ECU | 조명 제어 |
| **Body** | 0x202 | frmLighting_RearCtrl | 1 | 후방 조명 제어 (ON/OFF) | 100 | vECU | Lighting Control ECU | 조명 제어 |
| **Body** | 0x203 | frmLighting_FootCtrl | 2 | 바닥·발판 조명 제어 (ON/OFF + 밝기) | 100 | vECU | Lighting Control ECU | 조명 제어 |
| **Body** | 0x210 | frmBDC_DoorStatus | 1 | 도어 개방 상태 (비트맵) | 100 | BDC | vECU, Gateway | 센서 입력 |
| **Body** | 0x211 | frmBDC_SeatOccupancy | 1 | 좌석 점유 상태 | 200 | BDC | vECU | 센서 입력 |
| **Body** | 0x212 | frmBDC_SeatPosCtrl | 1 | 시트 위치 제어 | Event | vECU | BDC | 제어 명령 |
| **ADAS** | 0x300 | frmADAS_LDW_Event | 1 | 차선 이탈 경고 이벤트 | 50 | ADAS Control ECU | vECU, Gateway | ADAS 이벤트 |
| **ADAS** | 0x301 | frmADAS_RearObstacle | 1 | 후방 장애물 거리 | 100 | ADAS Control ECU | vECU, Gateway | ADAS 센서 |
| **ADAS** | 0x302 | frmADAS_AEB_Event | 1 | 긴급 제동 이벤트 | 20 | ADAS Control ECU | vECU, Gateway | ADAS 이벤트 |
| **ADAS** | 0x303 | frmADAS_SideObject | 1 | 후측방 객체 감지 | 100 | ADAS Control ECU | vECU, Gateway | ADAS 센서 |
| **ADAS** | 0x304 | frmADAS_StatusIcon | 1 | ADAS 기능 활성 상태 | 500 | ADAS Control ECU | Cluster ECU | 상태 정보 |
| **Powertrain** | 0x400 | frmTrans_GearStatus | 1 | 변속 상태 (P/R/N/D) | 50 | Transmission Control ECU | vECU, Gateway, Cluster ECU | 변속 정보 |
| **Powertrain** | 0x401 | frmVehicle_Speed | 1 | 차량 속도 | 50 | Vehicle Speed Sensor | vECU, Gateway, Cluster ECU | 속도 정보 |
| **Chassis** | 0x500 | frmHVAC_Temp | 1 | 실내 온도 | 500 | HVAC Control ECU | vECU, Gateway | HVAC 정보 |
| **Chassis** | 0x501 | frmWiper_Status | 1 | 와이퍼 상태 | 200 | Wiper Control ECU | vECU | 와이퍼 정보 |
| **Chassis** | 0x502 | frmBrightness_Sensor | 1 | 외부 밝기 | 1000 | Brightness Sensor | vECU | 센서 정보 |
| **Diagnostic** | 0x7DF | frmDiag_Request | 8 | 진단 요청 (UDS) | Event | Tester | Diagnostic Service ECU | UDS 요청 |
| **Diagnostic** | 0x7E8 | frmDiag_Response | 8 | 진단 응답 (UDS) | Event | Diagnostic Service ECU | Tester | UDS 응답 |
| **Diagnostic** | 0x600 | frmDTC_Info | 8 | DTC 정보 | Event | Diagnostic Service ECU | vECU, Cluster ECU | DTC 관리 |
| **Diagnostic** | 0x601 | frmOTA_Progress | 2 | OTA 진행률 | 100 | Diagnostic Service ECU | vECU, Cluster ECU | OTA 상태 |
| **Safety** | 0x700 | frmWarning_UI | 2 | 경고 UI 제어 | Event | vECU | Cluster ECU | 경고 표시 |
| **Safety** | 0x701 | frmWarning_Sound | 1 | 경고음 제어 | Event | vECU | Warning Speaker | 경고음 |
| **Safety** | 0x702 | frmFailSafe_Status | 1 | Fail-Safe 상태 | 100 | Fail-Safe Manager | vECU, Cluster ECU | 안전 상태 |

---

## 신호 정의 (Signal Definition)

### frmIVI_ModeSelect (0x100)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| ModeSelected | 0-1 | 2 | uint | 0 | 3 | - | 1 | 0 | 0: 에코, 1: 컴포트, 2: 스포츠, 3: Reserved |
| ProfileSelected | 2-3 | 2 | uint | 1 | 3 | - | 1 | 0 | 1: 프로필1, 2: 프로필2, 3: 프로필3 |

### frmIVI_LightColorSet (0x101)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| ColorR | 0-7 | 8 | uint | 0 | 255 | - | 1 | 0 | Red 색상 값 |
| ColorG | 8-15 | 8 | uint | 0 | 255 | - | 1 | 0 | Green 색상 값 |
| ColorB | 16-23 | 8 | uint | 0 | 255 | - | 1 | 0 | Blue 색상 값 |
| Brightness | 24-31 | 8 | uint | 0 | 100 | % | 1 | 0 | 밝기 (0~100%) |

### frmLighting_AmbientCtrl (0x200)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| AmbientR | 0-7 | 8 | uint | 0 | 255 | - | 1 | 0 | 앰비언트 조명 Red |
| AmbientG | 8-15 | 8 | uint | 0 | 255 | - | 1 | 0 | 앰비언트 조명 Green |
| AmbientB | 16-23 | 8 | uint | 0 | 255 | - | 1 | 0 | 앰비언트 조명 Blue |
| AmbientBrightness | 24-31 | 8 | uint | 0 | 100 | % | 1 | 0 | 앰비언트 조명 밝기 |
| BlinkMode | 32-33 | 2 | uint | 0 | 3 | - | 1 | 0 | 0: 정상, 1: 느린 점멸, 2: 빠른 점멸, 3: Reserved |

### frmBDC_DoorStatus (0x210)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| DoorStatus | 0-7 | 8 | uint | 0 | 255 | - | 1 | 0 | Bit 0: 운전석, Bit 1: 조수석, Bit 2: 후석좌, Bit 3: 후석우 (0: 닫힘, 1: 열림) |

### frmTrans_GearStatus (0x400)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| GearStatus | 0-1 | 2 | uint | 0 | 3 | - | 1 | 0 | 0: P, 1: R, 2: N, 3: D |

### frmVehicle_Speed (0x401)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| VehicleSpeed | 0-7 | 8 | uint | 0 | 255 | km/h | 1 | 0 | 차량 속도 |

### frmADAS_LDW_Event (0x300)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| LDW_Event | 0 | 1 | bool | 0 | 1 | - | 1 | 0 | 0: 정상, 1: 차선 이탈 |
| LDW_Direction | 1-2 | 2 | uint | 0 | 2 | - | 1 | 0 | 0: 좌측, 1: 우측, 2: Reserved |

### frmADAS_AEB_Event (0x302)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| AEB_Event | 0 | 1 | bool | 0 | 1 | - | 1 | 0 | 0: 정상, 1: 긴급 제동 |
| AEB_Level | 1-2 | 2 | uint | 0 | 3 | - | 1 | 0 | 0: 낮음, 1: 중간, 2: 높음, 3: 매우 높음 |

### frmWarning_UI (0x700)

| Signal Name | Bit Position | Length (bits) | Data Type | Min | Max | Unit | Factor | Offset | Description |
|-------------|-------------|---------------|-----------|-----|-----|------|--------|--------|-------------|
| WarningType | 0-3 | 4 | uint | 0 | 15 | - | 1 | 0 | 0: 없음, 1: 후진 경고, 2: LDW 경고, 3: AEB 경고, 4: 도어 개방 경고, ... |
| WarningLevel | 4-5 | 2 | uint | 0 | 3 | - | 1 | 0 | 0: 정보, 1: 주의, 2: 경고, 3: 위험 |
| DisplayDuration | 8-15 | 8 | uint | 0 | 255 | sec | 0.1 | 0 | 표시 지속 시간 (0: 영구 표시) |

---

## 네트워크 토폴로지

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAN Network Topology                          │
└─────────────────────────────────────────────────────────────────┘

Infotainment CAN (500 kbps)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  │                    │                    │
┌─▼──────────────┐ ┌──▼─────────────┐ ┌───▼────────────┐
│ IVI Control    │ │     vECU       │ │   Cluster      │
│      ECU       │ │   (IVI vECU)   │ │      ECU       │
└────────────────┘ └────────┬───────┘ └────────────────┘
                            │
                    ┌───────▼────────┐
                    │     Gateway    │
                    │   (Central)    │
                    └───────┬────────┘
        ┌───────────────────┼───────────────────┐
        │                   │                   │
Body CAN (500 kbps)    ADAS CAN (500 kbps)   Powertrain CAN (500 kbps)
━━━━━━━━━━━━━━━━━━     ━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━━━━
  │          │           │            │         │              │
┌─▼────┐ ┌──▼──┐     ┌──▼──────┐ ┌──▼──┐  ┌──▼──────┐   ┌──▼─────┐
│Light │ │ BDC │     │  ADAS   │ │ LDW │  │  Trans  │   │ Speed  │
│Ctrl  │ │     │     │  Ctrl   │ │Sensr│  │  Ctrl   │   │ Sensor │
│ ECU  │ │     │     │   ECU   │ │     │  │   ECU   │   │        │
└──────┘ └─────┘     └─────────┘ └─────┘  └─────────┘   └────────┘

Chassis CAN (500 kbps)       Diagnostic CAN (250 kbps)
━━━━━━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━━━━━━━━━━━━
  │          │                 │                │
┌─▼────┐ ┌──▼──┐           ┌──▼──────────┐ ┌──▼────────┐
│HVAC  │ │Wiper│           │  Diagnostic │ │ Fail-Safe │
│Ctrl  │ │Ctrl │           │   Service   │ │  Manager  │
│ ECU  │ │ ECU │           │     ECU     │ │           │
└──────┘ └─────┘           └─────────────┘ └───────────┘
```

---

## 메시지 라우팅 규칙 (Gateway)

| Source CAN | Message ID Range | Destination CAN | Filter Rule | 비고 |
|------------|------------------|-----------------|-------------|------|
| Infotainment | 0x100 - 0x1FF | Body, ADAS, Powertrain, Chassis | Pass All | IVI 명령은 모든 도메인에 전달 |
| Body | 0x200 - 0x2FF | Infotainment | Pass Selected (0x210, 0x211) | 센서 정보만 IVI로 전달 |
| ADAS | 0x300 - 0x3FF | Infotainment | Pass All | ADAS 이벤트는 모두 IVI로 전달 |
| Powertrain | 0x400 - 0x4FF | Infotainment | Pass All | 차량 정보는 모두 IVI로 전달 |
| Chassis | 0x500 - 0x5FF | Infotainment | Pass Selected (0x500, 0x501) | HVAC, 와이퍼 정보만 IVI로 전달 |
| Diagnostic | 0x600 - 0x6FF | Infotainment | Pass Selected (0x600, 0x601) | DTC, OTA 정보만 IVI로 전달 |
| Infotainment | 0x700 - 0x7FF | All | Pass All | 경고/안전 메시지는 모든 도메인에 전달 |

---

**다음 단계**: 0303_Communication Specification (통신 명세) 작성
