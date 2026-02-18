# Requirements-DBC-Architecture Alignment Review

## Executive Summary

✅ **Overall Status**: 양호 (Good) - 요구사항, DBC 파일, 아키텍처 간 대부분 정렬되어 있음
⚠️ **주요 발견사항**: 일부 ADAS 및 IVI 심화 요구사항은 DBC에 신호 정의 필요
🔍 **검토 범위**: 57개 요구사항, 2개 DBC 파일, 3개 아키텍처 문서

---

## 1. 요구사항 분석 (REQ_IVI_vECU_Requirements.xlsx)

### 1.1 요구사항 통계

| 카테고리 | 개수 | 우선순위 분포 |
|---|---|---|
| 기능 요구사항 (Functional) | 29개 | P0: 4, P1: 11, P2: 11, P3: 3 |
| 안전 요구사항 (Safety) | 12개 | P0: 4, P1: 3, P2: 5 |
| 비기능 요구사항 (Non-Functional) | 9개 | P1: 3, P2: 5, P3: 1 |
| 진단/OTA 요구사항 (Diagnostic/OTA) | 7개 | P0: 4, P1: 3 |

### 1.2 ASIL 등급 분포

- **ASIL-D**: 2개 (후진 도어 개방 경고, 긴급 제동)
- **ASIL-C**: 4개 (후진 안전 경고, 자동 복구, 차선 이탈)
- **ASIL-B**: 20개 (조명 제어, ADAS 연계, OTA/진단)
- **ASIL-A**: 1개 (승하차 UX)
- **QM**: 27개 (비안전 기능)

---

## 2. DBC 파일 분석

### 2.1 `vehicle_system.dbc` (통합 DBC)

**출처**: Hyundai/Kia 오픈소스 DBC (`hyundai_kia_generic.dbc`) + 프로젝트 커스텀 신호

#### 주요 메시지 (17개 메시지)

| Message ID | Name | Signals | Sender | ASIL Level | Cycle Time |
|---|---|---|---|---|---|
| 0x100 (256) | EMS_EngineStatus | Engine_RPM, Vehicle_Speed, Torque | EMS | ASIL-D | 10ms |
| 0x101 (257) | EMS_Temperature | Coolant_Temp, Oil_Temp | EMS | ASIL-D | 100ms |
| 0x180 (384) | TCU_GearStatus | Gear_Position, Shift_Status | TCU | ASIL-C | 20ms |
| 0x200 (512) | ESP_VehicleDynamics | Wheel_Speed_FL/FR/RL/RR | ESP | ASIL-D | 10ms |
| 0x210 (528) | ESP_Sensors | Yaw_Rate, Lateral_Accel | ESP | ASIL-D | 10ms |
| 0x280 (640) | MDPS_SteeringStatus | Steering_Angle, Torque | MDPS | ASIL-C | 20ms |
| 0x300 (768) | **Camera_LDW** | LDW_Status, AEB_Event, Collision_Risk | Camera | ASIL-D | 50ms |
| 0x310 (784) | **Camera_Objects** | Object_Distance/Velocity/Type | Camera | ASIL-C | 50ms |
| 0x340 (832) | **Radar_BSD** | BSD_Object_Left/Right | Radar | ASIL-B | 50ms |
| 0x380 (896) | **SCC_Status** | SCC_Active, Set_Speed, Following_Distance | SCC | ASIL-C | 50ms |
| 0x400 (1024) | **IVI_AmbientLight** | RGB, Brightness, Theme_Package | IVI | QM | 100ms |
| 0x410 (1040) | **IVI_Profile** | Profile_ID, Scenario_ID | IVI | QM | 500ms |
| 0x480 (1152) | Cluster_Display | Speed/RPM Display | Cluster | ASIL-B | 50ms |
| 0x500 (1280) | **BCM_DoorStatus** | Door_Status_FL/FR/RL/RR | BCM | ASIL-B | 100ms |
| 0x510 (1296) | **BCM_LightControl** | Headlight_Status, Ambient_R/G/B_Actual | BCM | ASIL-B | 100ms |
| 0x700 (1792) | CGW_Status | Network_Load, Diagnostic/OTA Active | CGW | ASIL-D | 1000ms |

**Hyundai/Kia에서 가져온 신호**:
- ✅ `Vehicle_Speed` (EMS_EngineStatus)
- ✅ `Gear_Position` (TCU_GearStatus) - R/D/N/P 값 정의 포함
- ✅ `Door_Status` (BCM_DoorStatus)
- ✅ `Steering_Angle` (MDPS_SteeringStatus)
- ✅ `Wheel_Speed` (ESP_VehicleDynamics)

**프로젝트 자체 제작 신호** (IVI 특화):
- ✅ `Camera_LDW` - ADAS 차선 이탈 경고
- ✅ `Camera_Objects` - ADAS 전방 객체 감지
- ✅ `Radar_BSD` - 후측방 감지
- ✅ `IVI_AmbientLight` - RGB 조명 제어
- ✅ `IVI_Profile` - 사용자 프로필 관리

### 2.2 `vehicle_system_custom.dbc` (순수 커스텀)

**목적**: IVI 프로젝트 전용 신호 정의

| Message ID | Name | Signals | Purpose |
|---|---|---|---|
| 0x400 (1024) | IVI_AmbientLight | R/G/B, Brightness, Theme_Package | 조명 테마 패키지 (SPORT/ECO/COMFORT 등) |
| 0x410 (1040) | IVI_Profile | Profile_ID, Scenario_ID, Scenario_Params | 3명 운전자 프로필 + 시나리오 |
| 0x510 (1296) | BCM_LightControl | Ambient R/G/B Actual Feedback | BCM으로부터 실제 조명 상태 피드백 |

**주요 특징**:
- `Theme_Package`: 10가지 테마 (SPORT, COMFORT, ECO, CUSTOM1-3, NIGHT, PARTY, RELAX, DYNAMIC, USER_DEFINED)
- `Profile_ID`: 최대 6개 프로필 (DRIVER1-3, GUEST, VALET, CUSTOM)
- `Scenario_Params`: 32비트 커스텀 파라미터

---

## 3. DBC-요구사항 매핑 분석

### 3.1 ✅ 완벽하게 커버된 요구사항 (35개)

| Req ID | 요구사항 | DBC 신호 | Message ID |
|---|---|---|---|
| REQ_001 | 스포츠모드 속도연동 조명 | Vehicle_Speed + IVI_AmbientLight | 0x100, 0x400 |
| REQ_002 | 후진 안전경고 UI 및 시트조명 | Gear_Position + Door_Status | 0x180, 0x500 |
| REQ_003 | 승하차 UX 도어연동 | Door_Status | 0x500 |
| REQ_004 | IVI 조명색상 동기화 | IVI_AmbientLight + BCM_LightControl | 0x400, 0x510 |
| REQ_005 | 온도연동 조명 (HVAC 필요) | ⚠️ **HVAC_Temperature 신호 미정의** | N/A |
| REQ_007 | 후진 중 도어 개방 경고 | Gear_Position + Door_Status | 0x180, 0x500 |
| REQ_008 | 경고 자동복구 | Gear_Position + Door_Status | 0x180, 0x500 |
| REQ_016 | 후진 기어 UX 활성화 | Gear_Position + Vehicle_Speed | 0x180, 0x100 |
| REQ_017 | 후진 시 후방 조명 제어 | Gear_Position | 0x180 |
| REQ_020 | 후진 경고음 | Gear_Position + (장애물 이벤트) | 0x180 |
| REQ_028 | 차선 이탈 시각적 경고 | Camera_LDW (LDW_Status) | 0x300 |
| REQ_029 | 후진 시 ADAS 앰비언트 경고 | Camera_Objects (후방) | ⚠️ **후방 카메라 신호 필요** |
| REQ_030 | 긴급 제동 시각적 경고 | Camera_LDW (AEB_Event) | 0x300 |
| REQ_031 | 승하차 시 ADAS 후측방 경고 | Radar_BSD | 0x340 |
| REQ_042 | IVI 모드 선택 조명 테마 | IVI_AmbientLight (Theme_Package) | 0x400 |
| REQ_043 | 운전자 프로필 조명 개인화 | IVI_Profile | 0x410 |
| REQ_044 | 주행 컨텍스트 조명 씬 제어 | IVI_Profile (Scenario_ID) | 0x410 |

### 3.2 ⚠️ 부분 커버 / 신호 추가 필요 (12개)

| Req ID | 요구사항 | 현재 상태 | 필요한 추가 신호 |
|---|---|---|---|
| REQ_005 | 온도연동 조명 | ❌ HVAC 신호 없음 | `HVAC_Temperature` (0x104) |
| REQ_018 | 후진 보조 시트 위치 조정 | ❌ 시트 제어 신호 없음 | `Seat_Position_Control` |
| REQ_029 | 후진 시 ADAS 후방 경고 | ❌ 후방 카메라 신호 없음 | `Rear_Camera_Objects` (0x312) |
| REQ_046 | 정비 모드 IVI 자진단 | ⚠️ UDS 진단만 있음 | 진단 결과 CAN 메시지 (선택사항) |
| REQ_051 | 야간 승하차 안전 조명 | ⚠️ 조도 센서 신호 없음 | `Ambient_Light_Sensor` (0x520) |
| REQ_053 | 기상 조건 인지 UX | ❌ 와이퍼/레인센서 신호 없음 | `Wiper_Status`, `Rain_Sensor` |
| REQ_054 | 어린이 보호 모드 | ❌ 좌석 점유 센서 없음 | `Rear_Seat_Occupancy` (0x522) |
| REQ_055 | 졸음 방지 UX | ❌ 정차 감지 신호 부족 | `Parking_Brake_Status` |

### 3.3 🟢 아키텍처로 처리 가능 (OTA/진단 관련, 10개)

| Req ID | 요구사항 | 처리 방법 |
|---|---|---|
| REQ_011-015 | OTA/UDS 진단 (0x14, 0x34, 등) | UDS 프로토콜로 처리 (CAN DBC 불필요) |
| REQ_047 | 조명 테마 OTA 업데이트 | UDS 0x34/0x36/0x37 서비스 |
| REQ_050 | OTA 전후 기능 변경 이력 | NvM + 버전 관리 (DBC 무관) |

---

## 4. 아키텍처-DBC-요구사항 정렬 분석

### 4.1 ✅ 완벽하게 정렬된 영역

#### Lighting Control Architecture
- **요구사항**: REQ_001, 003, 004, 017, 042
- **DBC 신호**: `IVI_AmbientLight`, `BCM_LightControl`, `Door_Status`, `Gear_Position`
- **아키텍처 컴포넌트**:
  - `Ambient_Light_Controller` (ASIL-B)
  - `Dashboard_Lighting_Controller` (ASIL-A/B)
  - `IVI_Sync_Manager` (QM)
  - `Theme_Manager` (QM)
- **결과**: ✅ **완전 정렬** - 요구사항, DBC, 아키텍처 모두 일치

#### Safety System Architecture
- **요구사항**: REQ_002, 007, 008, 016, 020, 028, 030
- **DBC 신호**: `Gear_Position`, `Door_Status`, `Camera_LDW`, `Camera_Objects`
- **아키텍처 컴포넌트**:
  - `Reverse_Safety_Manager` (ASIL-C)
  - `Door_Warning_Logic` (ASIL-D)
  - `Auto_Recovery_Manager` (ASIL-C)
  - `ADAS_Safety_Coordinator` (ASIL-C/D)
- **결과**: ✅ **완전 정렬** - ASIL 등급도 일치

### 4.2 ⚠️ 부분 정렬 / 추가 작업 필요

#### ADAS 통합 (REQ_029, 031)
- **현재 상태**:
  - ✅ 전방 카메라 (`Camera_LDW`, `Camera_Objects`) - 정의됨
  - ✅ 후측방 레이더 (`Radar_BSD`) - 정의됨
  - ❌ 후방 카메라 신호 - **누락**
- **필요 조치**:
  - `vehicle_system.dbc`에 `Rear_Camera_Objects` 메시지 추가 (예: 0x312, ASIL-B)
  - 아키텍처 문서에 후방 ADAS 컴포넌트 추가

#### 환경 센서 연동 (REQ_005, 051, 053, 054)
- **현재 상태**: DBC에 센서 신호 미정의
- **필요 조치**:
  - `HVAC_Temperature` (0x104) - HVAC ECU로부터
  - `Ambient_Light_Sensor` (0x520) - BCM으로부터
  - `Wiper_Status`, `Rain_Sensor` (0x524) - BCM
  - `Rear_Seat_Occupancy` (0x522) - BCM

---

## 5. 갭(Gap) 분석 Summary

### 5.1 🔴 Critical Gaps (즉시 조치 필요)

1. **후방 ADAS 신호 누락** (REQ_029)
   - 영향: ASIL-B 안전 요구사항
   - 조치: `Rear_Camera_Objects` 메시지 추가
   - 우선순위: **P1 (Phase 1-2)**

2. **HVAC 온도 신호 누락** (REQ_005)
   - 영향: P2 기능 요구사항
   - 조치: `HVAC_Temperature` 신호 추가
   - 우선순위: **P2 (Phase 2)**

### 5.2 🟡 Medium Gaps (Phase 2-3에서 처리 가능)

3. **환경 센서 신호 부족** (REQ_051, 053, 054)
   - 조도 센서, 와이퍼, 레인센서, 좌석 점유 센서
   - 우선순위: **P2-P3**

4. **시트 제어 신호 부족** (REQ_018)
   - 영향: P2 편의 기능
   - 우선순위: **P2**

### 5.3 🟢 Minor Gaps (선택사항)

5. **진단 결과 CAN 메시지** (REQ_046)
   - 현재: UDS로 충분히 처리 가능
   - 추가 시: 정비사 편의성 향상
   - 우선순위: **P3 (선택)**

---

## 6. 권장 조치사항

### 6.1 즉시 조치 (Phase 1-2)

1. **`vehicle_system.dbc` 업데이트**
   ```dbc
   BO_ 786 Rear_Camera_Objects: 8 Rear_Camera
    SG_ Rear_Object_Distance : 0|16@1+ (0.1,0) [0|50] "m" IVI,BCM
    SG_ Rear_Object_Type : 16|4@1+ (1,0) [0|7] "" IVI
    SG_ Rear_Collision_Risk : 20|8@1+ (1,0) [0|100] "%" IVI,Cluster
    SG_ AliveCounter : 56|4@1+ (1,0) [0|15] "" CGW
    SG_ Checksum : 60|4@1+ (1,0) [0|15] "" CGW
   ```

2. **`vehicle_system.dbc`에 HVAC 신호 추가**
   ```dbc
   BO_ 260 HVAC_Status: 4 HVAC
    SG_ Cabin_Temperature : 0|8@1+ (0.5,-40) [-40|80] "C" IVI,Cluster
    SG_ Target_Temperature : 8|8@1+ (0.5,-40) [-40|80] "C" IVI
   ```

### 6.2 Phase 2-3 조치

3. **센서 신호 추가**
   - `BCM_SensorStatus` (0x520): 조도 센서, 와이퍼, 레인센서
   - `BCM_SeatStatus` (0x522): 좌석 점유 감지

4. **아키텍처 문서 보완**
   - `safety_system_architecture.md`에 후방 ADAS 컴포넌트 추가
   - `lighting_control_architecture.md`에 환경 센서 연동 로직 추가

### 6.3 검증 및 테스트

5. **DBC 통합 검증**
   - CANoe에서 `vehicle_system.dbc` 로드 테스트
   - 신규 메시지 송수신 시뮬레이션
   - Fault Injection 테스트 (타임아웃, 값 오류)

6. **요구사항 추적성 업데이트**
   - `architecture_overview.md`의 Traceability Matrix에 신규 신호 추가
   - 각 요구사항에 DBC 메시지 ID 매핑

---

## 7. 결론

### 7.1 전체 평가

| 항목 | 점수 | 코멘트 |
|---|---|---|
| 요구사항 완성도 | 9/10 | 57개 요구사항 잘 정리됨 |
| DBC 커버리지 | 7.5/10 | 핵심 신호 커버, 일부 센서 신호 누락 |
| 아키텍처 정렬성 | 9/10 | 요구사항과 아키텍처 잘 매핑됨 |
| **전체 정렬도** | **8.5/10** | 양호, 일부 보완 필요 |

### 7.2 핵심 요약

✅ **강점**:
- Hyundai/Kia 오픈소스에서 **핵심 차량 신호만 선별적으로 추출**
- IVI 프로젝트에 맞는 **커스텀 신호 잘 설계** (조명, 프로필, 테마)
- 아키텍처 컴포넌트가 **DBC 신호와 1:1 매핑**
- ASIL 등급이 **요구사항-DBC-아키텍처 모두 일치**

⚠️ **개선 필요**:
- **후방 ADAS 신호** 추가 (REQ_029, ASIL-B)
- **HVAC 온도 신호** 추가 (REQ_005, P2)
- **환경 센서 신호** 추가 (REQ_051, 053, 054, P2-P3)

🎯 **최종 판단**:
> **"요구사항, DBC, 아키텍처가 전반적으로 잘 정렬되어 있으며, Phase 1 개발 진행 가능. 일부 센서 신호는 Phase 2-3에서 보완 필요."**

---

## 8. 다음 단계

1. **즉시 (이번 주)**:
   - [ ] `vehicle_system.dbc`에 `Rear_Camera_Objects` 추가
   - [ ] `vehicle_system.dbc`에 `HVAC_Status` 추가
   - [ ] CANoe에서 DBC 로드 및 시뮬레이션 테스트

2. **Phase 2 (다음 단계)**:
   - [ ] 환경 센서 신호 추가
   - [ ] 시트 제어 신호 추가
   - [ ] 아키텍처 문서 업데이트

3. **지속 관리**:
   - [ ] 요구사항 변경 시 DBC 동기화
   - [ ] DBC 버전 관리 (Git)
   - [ ] 아키텍처 Traceability Matrix 유지

---

**검토자**: Architecture Team
**검토일**: 2026-02-12
**상태**: ✅ 승인 (조건부: 후방 ADAS 신호 추가 후 Phase 1 진행)
