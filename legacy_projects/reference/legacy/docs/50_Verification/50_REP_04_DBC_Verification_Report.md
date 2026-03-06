# DBC 파일 검증 보고서

## 🚨 중대한 문제 발견!

**검증 일자**: 2026-02-11 02:41
**검증 대상**: `a.dbc` vs Level 1 Architecture

---

## ❌ 핵심 문제: ECU 불일치

### 현재 DBC 파일 (`a.dbc`)
**출처**: Tesla CAN Database (commaai/opendbc)

**정의된 ECU 노드** (Line 36-47):
```
BU_:
	NEO      # Tesla 컴퓨터
	MCU      # Media Control Unit
	GTW      # Gateway
	EPAS     # Electric Power Assisted Steering
	DI       # Driver Interface
	ESP      # Electronic Stability Program
	SBW      # Steer-by-Wire
	STW      # Steering Wheel
	APP      # Application
	DAS      # Driver Assistance System
	XXX      # Unknown
```

### Level 1 아키텍처 (우리 프로젝트)
**출처**: `level1_ecu_specification.md`

**필요한 ECU 노드** (11개):
```
1. EMS  (Engine Management System)      ❌ DBC에 없음
2. TCU  (Transmission Control Unit)     ❌ DBC에 없음
3. ESP  (Electronic Stability Program)  ✅ DBC에 있음
4. MDPS (Motor Driven Power Steering)   ❌ DBC에는 EPAS (유사하지만 다름)
5. BCM  (Body Control Module)           ❌ DBC에 없음
6. IVI  (In-Vehicle Infotainment)       ❌ DBC에는 MCU (다른 목적)
7. Cluster                              ❌ DBC에는 DI (유사하지만 다름)
8. Camera                               ❌ DBC에는 DAS (통합 시스템)
9. Radar                                ❌ DBC에 없음
10. SCC  (Smart Cruise Control)         ❌ DBC에는 DAS (통합 시스템)
11. CGW  (Central Gateway)              ✅ DBC에 GTW 있음
```

**일치율**: **2/11 = 18%** ❌

---

## 🔍 상세 분석

### 1. Powertrain Domain (0/2 일치)

#### ❌ EMS (Engine Management System)
- **Level 1 요구사항**: CAN ID 0x100-0x17F
- **DBC 현황**: **없음**
- **DBC 대체**: `DI` (Driver Interface) - 하지만 역할이 다름
  - DI는 계기판/인터페이스 (ID 0x108, 0x118, 0x368)
  - EMS는 엔진 제어 (RPM, Torque, Throttle)

**누락된 신호**:
```
- Engine_RPM (0x100)
- Vehicle_Speed (0x101)
- Engine_Torque (0x102)
- Coolant_Temp (0x103)
- Throttle_Position (0x104)
```

#### ❌ TCU (Transmission Control Unit)
- **Level 1 요구사항**: CAN ID 0x180-0x1FF
- **DBC 현황**: **없음**
- **DBC 대체**: `DI_gear` 신호만 있음 (ID 0x118)

**누락된 신호**:
```
- Gear_Position (0x180)
- Shift_Status (0x181)
- Oil_Temperature (0x182)
- Torque_Converter_Lock (0x183)
```

---

### 2. Chassis Domain (1/2 일치)

#### ✅ ESP (Electronic Stability Program)
- **Level 1 요구사항**: CAN ID 0x200-0x27F
- **DBC 현황**: **있음** (ID 0x135, 0x155)
- **상태**: ✅ 부분 일치

**DBC 메시지**:
```
BO_ 309 ESP_135h: 5 ESP
BO_ 341 ESP_B: 8 ESP
```

**문제점**: CAN ID가 다름
- DBC: 0x135 (309), 0x155 (341)
- Level 1: 0x200-0x27F
- **해결**: CAN ID 재할당 필요

#### ❌ MDPS (Motor Driven Power Steering)
- **Level 1 요구사항**: CAN ID 0x280-0x2FF
- **DBC 현황**: `EPAS` 있음 (ID 0x101, 0x131, 0x370)
- **문제**: 이름과 ID 범위가 다름

**DBC 메시지**:
```
BO_ 257 GTW_epasControl: 3 NEO
BO_ 880 EPAS_sysStatus: 8 EPAS
BO_ 305 EPAS3P_sysStatus: 8 NEO
```

**해결 방안**: EPAS → MDPS 이름 변경 + ID 재할당

---

### 3. Body Domain (0/1 일치)

#### ❌ BCM (Body Control Module)
- **Level 1 요구사항**: CAN ID 0x500-0x57F
- **DBC 현황**: **없음**
- **DBC 대체**: `GTW_carState` (ID 0x318) - 일부 기능만

**DBC에 있는 바디 신호** (GTW가 송신):
```
BO_ 792 GTW_carState: 8 GTW
 SG_ DOOR_STATE_FL
 SG_ DOOR_STATE_FR
 SG_ DOOR_STATE_RL
 SG_ DOOR_STATE_RR
 SG_ BC_headLightLStatus
 SG_ BC_headLightRStatus
```

**누락된 BCM 기능**:
```
- Window_Position (0x520)
- Central_Lock_Status (0x521)
- Ambient_Light_RGB 수신 (0x410)
```

---

### 4. Infotainment & ADAS Domain (0/5 일치)

#### ❌ IVI (In-Vehicle Infotainment)
- **Level 1 요구사항**: CAN ID 0x400-0x47F
- **DBC 현황**: `MCU` 있음 (ID 0x218, 0x388, 0x68, 0x3D8)
- **문제**: MCU는 Media Control Unit (다른 역할)

**DBC MCU 메시지**:
```
BO_ 536 MCU_chassisControl: 8 GTW
BO_ 904 MCU_clusterBacklightRequest: 3 NEO
BO_ 984 MCU_locationStatus: 8 MCU
```

**누락된 IVI 신호**:
```
- Ambient_Light_RGB (0x410)
- Theme_Package (0x411)
- Profile_Data (0x412)
- Scenario_Params (0x413)
```

#### ❌ Cluster (Instrument Cluster)
- **Level 1 요구사항**: CAN ID 0x480-0x4FF
- **DBC 현황**: `DI` (Driver Interface) - 유사하지만 다름
- **문제**: DI는 Tesla 특화, Cluster는 일반 계기판

#### ❌ Camera ECU
- **Level 1 요구사항**: CAN ID 0x300-0x33F
- **DBC 현황**: `DAS` (Driver Assistance System) - 통합 시스템
- **문제**: DAS는 Tesla Autopilot (Camera + Radar + 제어 통합)

**DBC DAS 메시지**:
```
BO_ 1160 DAS_steeringControl: 4 NEO
BO_ 697 DAS_control: 8 NEO
BO_ 521 DAS_longControl: 8 NEO
BO_ 569 DAS_lanes: 8 NEO
```

**누락된 Camera 신호**:
```
- LDW_Status (0x300)
- Lane_Position (0x301)
- AEB_Event (0x302)
- Collision_Risk (0x303)
```

#### ❌ Radar ECU
- **Level 1 요구사항**: CAN ID 0x340-0x37F
- **DBC 현황**: **없음** (DAS에 통합)

**누락된 Radar 신호**:
```
- BSD_Object_Left (0x340)
- BSD_Object_Right (0x341)
- Object_Distance (0x342)
- Object_Velocity (0x343)
```

#### ❌ SCC (Smart Cruise Control)
- **Level 1 요구사항**: CAN ID 0x380-0x3BF
- **DBC 현황**: **없음** (DAS에 통합)

**누락된 SCC 신호**:
```
- SCC_Active (0x380)
- Set_Speed (0x381)
- Following_Distance (0x382)
```

---

### 5. Gateway (1/1 일치)

#### ✅ CGW (Central Gateway)
- **Level 1 요구사항**: CAN ID 0x700-0x7FF
- **DBC 현황**: `GTW` 있음
- **상태**: ✅ 일치

**DBC GTW 메시지**:
```
BO_ 257 GTW_epasControl: 3 NEO
BO_ 792 GTW_carState: 8 GTW
BO_ 840 GTW_status: 8 GTW
BO_ 920 GTW_carConfig: 8 GTW
```

---

## 📊 CAN ID 범위 비교

### Level 1 아키텍처 (우리 프로젝트)
```
0x100-0x17F: EMS (Powertrain)
0x180-0x1FF: TCU (Powertrain)
0x200-0x27F: ESP (Chassis)
0x280-0x2FF: MDPS (Chassis)
0x300-0x33F: Camera (ADAS)
0x340-0x37F: Radar (ADAS)
0x380-0x3BF: SCC (ADAS)
0x400-0x47F: IVI (Infotainment)
0x480-0x4FF: Cluster (Infotainment)
0x500-0x57F: BCM (Body)
0x700-0x7FF: CGW (Gateway)
```

### DBC 파일 (Tesla 기반)
```
0x003: STW_ANGL_STAT (조향각)
0x00E: STW_ANGLHP_STAT (고정밀 조향각)
0x045: STW_ACTN_RQ (조향 액션)
0x06D: SBW_RQ_SCCM (Steer-by-Wire)
0x101: GTW_epasControl
0x108: DI_torque1
0x118: DI_torque2
0x131: EPAS3P_sysStatus
0x135: ESP_135h
0x155: ESP_B
0x201: SDM1 (Seatbelt)
0x214: EPB_epasControl
0x218: MCU_chassisControl
0x283: BODY_R1
0x318: GTW_carState
0x348: GTW_status
0x370: EPAS_sysStatus
0x388: MCU_clusterBacklightRequest
0x399: AutopilotStatus
0x3D8: MCU_locationStatus
0x488: DAS_steeringControl
0x2B9: DAS_control
0x209: DAS_longControl
0x239: DAS_lanes
```

**문제**: CAN ID 범위가 완전히 다름!

---

## 🎯 권장 사항

### 즉시 조치 필요 (Critical)

#### 1. 새로운 DBC 파일 생성 ✅
**파일명**: `vehicle_system.dbc`
**위치**: `level3_communication/`

**필수 포함 사항**:
```
BU_:
    EMS      # Engine Management System
    TCU      # Transmission Control Unit
    ESP      # Electronic Stability Program
    MDPS     # Motor Driven Power Steering
    BCM      # Body Control Module
    IVI      # In-Vehicle Infotainment
    Cluster  # Instrument Cluster
    Camera   # Front Camera (ADAS)
    Radar    # Blind Spot Radar
    SCC      # Smart Cruise Control
    CGW      # Central Gateway
```

#### 2. CAN ID 재할당
Level 1 아키텍처에 맞춰 모든 메시지 ID 재정의:
```
BO_ 256 EMS_EngineStatus: 8 EMS
 SG_ Engine_RPM : 0|16@1+ (1,0) [0|8000] "rpm" Cluster,IVI
 SG_ Vehicle_Speed : 16|16@1+ (0.01,0) [0|300] "km/h" Cluster,IVI
 SG_ Engine_Torque : 32|16@1- (0.1,0) [-500|1000] "Nm" CGW
 SG_ Throttle_Position : 48|8@1+ (0.4,0) [0|100] "%" CGW

BO_ 384 TCU_GearStatus: 4 TCU
 SG_ Gear_Position : 0|4@1+ (1,0) [0|7] "" Cluster,IVI
 SG_ Shift_Status : 4|2@1+ (1,0) [0|3] "" CGW
 SG_ Oil_Temperature : 8|8@1+ (1,-40) [-40|150] "C" CGW

BO_ 512 ESP_VehicleDynamics: 8 ESP
 SG_ Wheel_Speed_FL : 0|16@1+ (0.01,0) [0|300] "km/h" CGW
 SG_ Wheel_Speed_FR : 16|16@1+ (0.01,0) [0|300] "km/h" CGW
 SG_ Yaw_Rate : 32|16@1- (0.01,0) [-100|100] "deg/s" Camera,SCC
 SG_ Lateral_Accel : 48|16@1- (0.01,0) [-15|15] "m/s2" Camera,SCC

BO_ 768 Camera_LDW: 4 Camera
 SG_ LDW_Status : 0|2@1+ (1,0) [0|3] "" IVI,Cluster
 SG_ Lane_Position : 2|16@1- (0.01,0) [-2|2] "m" SCC
 SG_ AEB_Event : 18|2@1+ (1,0) [0|3] "" IVI,Cluster,ESP

BO_ 1024 IVI_AmbientLight: 8 IVI
 SG_ Ambient_Light_R : 0|8@1+ (1,0) [0|255] "" BCM
 SG_ Ambient_Light_G : 8|8@1+ (1,0) [0|255] "" BCM
 SG_ Ambient_Light_B : 16|8@1+ (1,0) [0|255] "" BCM
 SG_ Theme_Package : 24|8@1+ (1,0) [0|10] "" BCM
```

#### 3. 기존 `a.dbc` 처리
- ❌ **삭제하지 말 것** (참고 자료로 보존)
- ✅ `archive/tesla_reference.dbc`로 이름 변경
- ✅ 신호 정의 형식 참고용으로 활용

---

## 🔄 Level 간 일관성 확인

### Level 1 ↔ Level 3 매핑

| Level 1 ECU | CAN ID Range | Level 3 DBC Node | 상태 |
|------------|-------------|------------------|------|
| EMS | 0x100-0x17F | EMS | ❌ 생성 필요 |
| TCU | 0x180-0x1FF | TCU | ❌ 생성 필요 |
| ESP | 0x200-0x27F | ESP | ⚠️ ID 재할당 |
| MDPS | 0x280-0x2FF | MDPS | ❌ 생성 필요 |
| BCM | 0x500-0x57F | BCM | ❌ 생성 필요 |
| IVI | 0x400-0x47F | IVI | ❌ 생성 필요 |
| Cluster | 0x480-0x4FF | Cluster | ❌ 생성 필요 |
| Camera | 0x300-0x33F | Camera | ❌ 생성 필요 |
| Radar | 0x340-0x37F | Radar | ❌ 생성 필요 |
| SCC | 0x380-0x3BF | SCC | ❌ 생성 필요 |
| CGW | 0x700-0x7FF | CGW | ✅ 유지 가능 |

---

## 📝 작업 계획

### Phase 1: DBC 파일 재작성 (우선순위: High)
1. ✅ `vehicle_system.dbc` 생성
2. ✅ 11개 ECU 노드 정의
3. ✅ Level 1 CAN ID 범위 준수
4. ✅ 주요 메시지 20+ 개 정의
5. ✅ 신호 50+ 개 정의

### Phase 2: 검증 (우선순위: High)
1. ✅ Level 1 ECU 목록과 100% 일치 확인
2. ✅ CAN ID 범위 충돌 없음 확인
3. ✅ 통신 시나리오 3개 커버 확인
4. ✅ CANoe에서 로드 테스트

### Phase 3: 문서화 (우선순위: Medium)
1. ✅ DBC 파일 설명서 작성
2. ✅ 메시지 매트릭스 업데이트
3. ✅ Level 3 다이어그램 연동

---

## ⚠️ 위험 요소

### 1. 시간 압박
- **멘토링**: 2026-02-13 (2일 남음)
- **작업량**: DBC 파일 전체 재작성 필요
- **권장**: Level 2 작성과 병행

### 2. 기술적 복잡도
- **신호 정의**: 50+ 신호의 정확한 스케일/오프셋 필요
- **메시지 주기**: 각 메시지의 적절한 주기 설정
- **Checksum/Counter**: 메시지 무결성 확인 로직

### 3. 일관성 유지
- **Level 1-4 동기화**: 모든 레벨에서 같은 ECU 이름 사용
- **요구사항 추적**: 56개 요구사항과 DBC 신호 매핑

---

## ✅ 결론

**현재 `a.dbc` 파일은 프로젝트에 사용 불가능합니다.**

**이유**:
1. ❌ Tesla 기반 (우리는 Hyundai/Kia 스타일)
2. ❌ ECU 이름 불일치 (18% 일치율)
3. ❌ CAN ID 범위 완전히 다름
4. ❌ 필수 ECU 9개 누락

**해결책**:
✅ **새로운 `vehicle_system.dbc` 파일 작성 필수**
✅ Level 1 아키텍처 기반으로 처음부터 재작성
✅ OpenDBC 분석 결과 활용 (신호 형식 참고)

---

**검증 완료**: 2026-02-11 02:45
**다음 단계**: `vehicle_system.dbc` 생성 시작

---

## 📝 Document Status
**Status**: Released
**Review**: Pending Mentoring Session (2026-02-13)
**Verification**: Artificial Intelligence Assistant
**Last Updated**: 2026-02-11
