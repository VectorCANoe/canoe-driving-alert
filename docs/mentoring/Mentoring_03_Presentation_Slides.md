# 차량 분산 시스템 아키텍처 프로젝트

**멘토링 발표 자료**
**날짜**: 2026년 2월 13일 (목)
**발표자**: 준수

---

## 슬라이드 1: 프로젝트 개요

### 프로젝트 주제
**CANoe 기반 차량 분산 시스템 아키텍처 설계 및 통신 검증**

### 핵심 학습 목표
1. **차량 전체 시스템 이해**
   - 다수 ECU의 분산 시스템 구조
   - 도메인별 역할 및 책임

2. **ECU 간 CAN 통신**
   - 통신 필요성 및 구조 파악
   - 메시지/신호 설계

3. **가상 차량 환경 구축**
   - CANoe 시뮬레이션
   - 통신 검증 테스트

4. **V-사이클 프로세스 경험**
   - 요구사항 → 설계 → 구현 → 테스트

### 프로젝트 범위
- **기반**: OpenDBC (Hyundai/Kia 실제 차량 데이터)
- **표준**: ISO 26262, AUTOSAR, Hyundai/Mobis
- **특화**: 앰비언트 라이팅 제어 시스템 ⭐

---

## 슬라이드 2: Level 1 - 차량 전체 시스템 아키텍처

### 시스템 구성

#### 7개 도메인, 47개 ECU
```
┌─────────────────────────────────────────────────────────┐
│                    OTA Server (External)                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
                  ┌──────────────┐
                  │   Gateway    │
                  │     (CGW)    │
                  └──────┬───────┘
         ┌───────────────┼───────────────┐
         ↓               ↓               ↓
    CAN-HS #1       CAN-HS #2        CAN-LS
    (500 kbps)      (500 kbps)      (125 kbps)
         │               │               │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │Powertrain│    │  ADAS   │     │  Body   │
    │ Chassis  │    │   IVI   │     │         │
    │ Safety   │    │         │     │         │
    └──────────┘    └──────────┘     └──────────┘
```

#### 도메인별 ECU 분류

| 도메인 | ECU 수 | 주요 ECU | ASIL |
|--------|--------|----------|------|
| **Powertrain** | 7 | EMS, TCU, OPI, LPI | D |
| **Chassis** | 6 | ESP, ABS, MDPS, SAS | D, C |
| **ADAS** | 7 | F_CAMERA, BSD_RADAR, SCC | B |
| **Body** | 8 | BCM, DATC, FATC, TPMS | QM |
| **Infotainment** | 5 | IVI, CLU, HUD | QM |
| **Safety** | 2 | ACU, ODS | D |
| **Gateway** | 1 | CGW | B |
| **Others** | 11 | LVR, EVP, DI_BOX, 4WD | - |

### 네트워크 구조
- **CAN-HS #1** (500 kbps): 안전 중요 (Powertrain, Chassis, Safety)
- **CAN-HS #2** (500 kbps): ADAS, Infotainment
- **CAN-LS** (125 kbps): Body, Comfort

### 핵심 포인트
✅ **CANoe는 다이어그램에 포함되지 않음** (시뮬레이션 도구)
✅ **Gateway 중심 아키텍처** (네트워크 간 중계)
✅ **ISO 26262 안전 도메인 분리** (ASIL-D/B/C/QM)

---

## 슬라이드 3: Level 2 - 도메인별 상세 아키텍처

### 7개 도메인 다이어그램 완성

#### 1. Powertrain Domain (7 ECU)
- **EMS**: 엔진 제어 → `EMS16 (0x260)` 메시지 (Vehicle_Speed, RPM, Torque)
- **TCU**: 변속기 제어 → `TCU11 (0x3BC)` 메시지 (Gear_Position)
- **OPI/LPI**: 오일/LPG 펌프
- **FPCM**: 연료 펌프
- **REA/AAF**: 배기가스 제어

#### 2. Chassis Domain (6 ECU)
- **ESP**: 차체 안정성 → `ESP12 (0x200)` 메시지 (Stability_Status)
- **ABS**: 제동 제어 → `ABS11 (0x38A)` 메시지 (Wheel_Speed)
- **MDPS**: 전동 조향 → `MDPS11 (0x381)` 메시지 (Steering_Angle)
- **SAS**: 조향각 센서
- **EPB**: 전자식 주차 브레이크
- **ECS**: 전자 제어 서스펜션

#### 3. ADAS Domain (7 ECU)
- **F_CAMERA**: 전방 카메라 → `LDWS_LKAS11 (0x420)` 메시지 (LDW, LKA)
- **BSD_RADAR**: 후측방 레이더 → `LCA11 (0x485)` 메시지 (Blind_Spot)
- **SCC**: 스마트 크루즈 → `SCC11 (0x421)` 메시지 (Cruise_Control)
- **SPAS**: 주차 보조
- **AVM**: 어라운드 뷰 모니터

#### 4. Infotainment Domain (5 ECU) ⭐
- **IVI**: 인포테인먼트 → `IVI_AmbientLight (0x400)` 메시지 (프로젝트 특화)
- **CLU**: 계기판 → 속도, RPM 표시
- **HUD**: 헤드업 디스플레이
- **TMU**: 텔레매틱스
- **CUBIS**: 통합 제어

#### 5. Body Domain (8 ECU)
- **BCM**: 바디 제어 → `BCM_LightControl (0x520)` 메시지 (프로젝트 특화) ⭐
- **DATC/FATC**: 에어컨 제어
- **TPMS**: 타이어 압력 모니터링
- **AFLS/AHLS**: 조명 제어

#### 6. Safety Domain (2 ECU)
- **ACU**: 에어백 제어 → `ACU11 (0x547)` 메시지 (Airbag_Status)
- **ODS**: 탑승자 감지

#### 7. Gateway Domain (1 ECU)
- **CGW**: 중앙 게이트웨이 → 50+ 라우팅 규칙

---

## 슬라이드 4: Level 3 - 통신 아키텍처

### CAN 메시지 스펙

#### 네트워크별 메시지 분포
| 네트워크 | 대역폭 | 메시지 수 | 신호 수 | ASIL | 버스 로드 |
|---------|--------|----------|---------|------|----------|
| CAN-HS #1 | 500 kbps | ~60 | ~600 | D, C | 55% |
| CAN-HS #2 | 500 kbps | ~50 | ~500 | B, QM | 45% |
| CAN-LS | 125 kbps | ~36 | ~245 | QM | 30% |
| **총계** | - | **149** | **1345** | - | - |

#### 주요 메시지 예시

**CAN-HS #1 (안전 중요)**:
- `EMS16 (0x260)`: Vehicle_Speed, Engine_RPM, Torque (10ms, ASIL-D)
- `ABS11 (0x38A)`: Wheel_Speed_FL/FR/RL/RR (10ms, ASIL-D)
- `ESP12 (0x200)`: Stability_Status, TCS_Active (20ms, ASIL-D)
- `ACU11 (0x547)`: Airbag_Status, Crash_Detected (10ms, ASIL-D)

**CAN-HS #2 (ADAS, Infotainment)**:
- `LDWS_LKAS11 (0x420)`: LDW_Status, LKA_Event (100ms, ASIL-B)
- `SCC11 (0x421)`: Cruise_Active, Speed_Target (50ms, ASIL-B)
- `IVI_AmbientLight (0x400)`: RGB, Brightness, Theme (100ms, QM) ⭐
- `IVI_Profile (0x410)`: Profile_ID, Scenario_ID (1000ms, QM) ⭐

**CAN-LS (Body, Comfort)**:
- `BCM_LightControl (0x520)`: Ambient_RGB_Actual, Headlight_Status (100ms, QM) ⭐
- `TPMS11 (0x5C3)`: Tire_Pressure_FL/FR/RL/RR (1000ms, QM)
- `DATC11 (0x383)`: Cabin_Temp, Fan_Speed (500ms, QM)

### Gateway 라우팅 규칙

#### 주요 라우팅 규칙 (50+ rules)

| Rule ID | Source | Message | Destination | Priority | Latency |
|---------|--------|---------|-------------|----------|---------|
| R001 | CAN-HS #1 | EMS16 (0x260) | CAN-HS #2 (CLU, HUD) | High | <1ms |
| R002 | CAN-HS #1 | ESP12 (0x200) | CAN-HS #2 (IVI, CLU) | High | <1ms |
| **R011** | **CAN-HS #2** | **IVI_AmbientLight (0x400)** | **CAN-LS (BCM)** | **Low** | **<5ms** ⭐ |
| **R021** | **CAN-LS** | **BCM_LightControl (0x520)** | **CAN-HS #2 (IVI, CLU)** | **Low** | **<5ms** ⭐ |

#### 필터링 및 보안
- **CRC 검증**: ASIL-B/C/D 메시지
- **AliveCounter 체크**: 메시지 손실 감지
- **Rate Limiting**: 메시지 ID별 전송 속도 제한
- **Security Filtering**: 비인가 메시지 차단

### 신호 정의 표준

#### Hyundai/Mobis 네이밍 규칙
**형식**: `<ECU>_<Function>_<Parameter>[_<Index>]`

**예시**:
- ✅ `EMS_Vehicle_Speed` (명확, 표준 준수)
- ✅ `IVI_Ambient_Light_R` (프로젝트 특화)
- ✅ `ABS_Wheel_Speed_FL` (배열 인덱스)
- ❌ `VehicleSpeed` (ECU 접두사 누락)
- ❌ `EMS_Spd` (비표준 약어)

---

## 슬라이드 5: 프로젝트 특화 기능 - 앰비언트 라이팅 ⭐

### 시스템 개요

#### 목적
사용자가 IVI에서 실내 앰비언트 조명을 제어하고, 실시간 피드백을 받는 시스템

#### 관련 ECU
- **IVI** (CAN-HS #2): 사용자 인터페이스, 테마 선택
- **Gateway** (CGW): 네트워크 간 메시지 라우팅
- **BCM** (CAN-LS): LED 드라이버 제어, 실제 조명 제어

### 메시지 정의

#### 1. IVI_AmbientLight (0x400) - IVI → BCM
**송신**: IVI (CAN-HS #2)
**수신**: BCM (CAN-LS, via Gateway)
**주기**: 100ms
**DLC**: 8 bytes

| 신호 | Start Bit | Length | Type | Range | Unit | 설명 |
|------|-----------|--------|------|-------|------|------|
| Ambient_Light_R | 0 | 8 | unsigned | 0-255 | - | Red 컴포넌트 |
| Ambient_Light_G | 8 | 8 | unsigned | 0-255 | - | Green 컴포넌트 |
| Ambient_Light_B | 16 | 8 | unsigned | 0-255 | - | Blue 컴포넌트 |
| Brightness | 24 | 8 | unsigned | 0-100 | % | 전체 밝기 |
| Theme_Package | 32 | 8 | enum | 0-10 | - | 테마 선택 |
| AliveCounter | 56 | 4 | unsigned | 0-15 | - | 메시지 카운터 |
| Checksum | 60 | 4 | unsigned | 0-15 | - | CRC |

**테마 패키지**:
- 0: SPORT (Red)
- 1: COMFORT (Blue)
- 2: ECO (Green)
- 3: CUSTOM (사용자 정의)

#### 2. IVI_Profile (0x410) - IVI → BCM
**송신**: IVI (CAN-HS #2)
**수신**: BCM (CAN-LS, via Gateway)
**주기**: 1000ms (이벤트 기반)
**DLC**: 8 bytes

| 신호 | Start Bit | Length | Type | Range | 설명 |
|------|-----------|--------|------|-------|------|
| Profile_ID | 0 | 8 | enum | 0-5 | 사용자 프로필 |
| Scenario_ID | 8 | 8 | enum | 0-10 | 시나리오 (주행, 주차 등) |

#### 3. BCM_LightControl (0x520) - BCM → IVI
**송신**: BCM (CAN-LS)
**수신**: IVI, CLU (CAN-HS #2, via Gateway)
**주기**: 100ms
**DLC**: 8 bytes

| 신호 | Start Bit | Length | Type | Range | 설명 |
|------|-----------|--------|------|-------|------|
| Headlight_Status | 0 | 2 | enum | 0-3 | 헤드라이트 상태 |
| Ambient_Light_Active | 8 | 1 | bool | 0-1 | 앰비언트 활성 상태 |
| Ambient_R_Actual | 16 | 8 | unsigned | 0-255 | 실제 Red 출력 |
| Ambient_G_Actual | 24 | 8 | unsigned | 0-255 | 실제 Green 출력 |
| Ambient_B_Actual | 32 | 8 | unsigned | 0-255 | 실제 Blue 출력 |

### 통신 흐름 (시퀀스)

```
User → IVI → Gateway → BCM → LED → BCM → Gateway → IVI → User
                (R011)              (R021)
```

#### 단계별 설명

**1. 사용자 입력** (0ms)
- 사용자가 IVI 화면에서 "SPORT" 테마 선택

**2. IVI 메시지 생성** (1-2ms)
- IVI가 `IVI_AmbientLight (0x400)` 메시지 생성
  - Ambient_Light_R = 255 (Red)
  - Ambient_Light_G = 0
  - Ambient_Light_B = 0
  - Brightness = 80 (80%)
  - Theme_Package = 0 (SPORT)

**3. Gateway 라우팅 (Rule R011)** (3-5ms)
- Gateway가 CAN-HS #2에서 메시지 수신
- CRC 및 AliveCounter 검증
- CAN-LS로 라우팅 (BCM으로 전송)

**4. BCM LED 제어** (2-3ms)
- BCM이 메시지 수신 및 파싱
- LED 드라이버에 PWM 신호 전송
- RGB(255, 0, 0), Brightness 80% 적용

**5. BCM 피드백 생성** (1-2ms)
- BCM이 `BCM_LightControl (0x520)` 메시지 생성
  - Ambient_Light_Active = 1 (ACTIVE)
  - Ambient_R_Actual = 255
  - Ambient_G_Actual = 0
  - Ambient_B_Actual = 0

**6. Gateway 라우팅 (Rule R021)** (3-5ms)
- Gateway가 CAN-LS에서 메시지 수신
- CAN-HS #2로 라우팅 (IVI, CLU로 전송)

**7. IVI 피드백 표시** (1-2ms)
- IVI가 메시지 수신
- 화면에 "Ambient Light: SPORT (Red, 80%) ✓ Active" 표시

**총 레이턴시**: ~10-15ms

### 에러 처리

#### 1. CRC 오류
- Gateway가 잘못된 CRC 감지
- 메시지 폐기, 라우팅하지 않음
- IVI에 타임아웃 경고 (3x cycle time = 300ms)

#### 2. AliveCounter 타임아웃
- BCM이 AliveCounter 증가 중단 감지
- 마지막 유효 값 유지 (Fail-Safe)
- 3초 후 기본 테마로 복귀

#### 3. LED 드라이버 고장
- BCM이 LED 드라이버 오류 감지
- `BCM_LightControl` 메시지에 오류 플래그 설정
- IVI가 "Ambient Light Error" 표시

---

## 슬라이드 6: 프로젝트 통계 및 다음 단계

### 완료된 작업 (2월 11일 기준)

#### 산출물
- **PlantUML 다이어그램**: 11개
  - Level 1: 2개 (차량 전체, 도메인 통신)
  - Level 2: 7개 (도메인별 상세)
  - Level 3: 2개 (네트워크 플로우, 앰비언트 시퀀스)
- **문서**: 9개
  - Level 1-3 README (3개)
  - 메시지 테이블 (3개)
  - 신호 정의 (1개)
  - 네이밍 규칙 (1개)
  - 라우팅 테이블 (1개)
- **PNG 파일**: 11개 (모든 다이어그램)

#### 커버리지
- **ECU**: 47개 정의 및 분류
- **메시지**: 149개 (146 OpenDBC + 3 프로젝트)
- **신호**: 1345개 (1325 OpenDBC + 20 프로젝트)
- **라우팅 규칙**: 50+ (Gateway)
- **네트워크**: 3개 (CAN-HS #1, #2, CAN-LS)

#### 표준 준수
- ✅ ISO 26262 (안전 도메인 분리, ASIL 레벨)
- ✅ AUTOSAR (아키텍처 패턴, 네이밍 규칙)
- ✅ ISO 11898 (CAN 프로토콜)
- ✅ Hyundai/Mobis (ECU 분류, 도메인 구조)

### 다음 단계 (2월 14일 - 2월 20일)

#### Phase 4-1: CANoe 프로젝트 통합 (2월 14-15일)
**목표**: 실제 시뮬레이션 환경 구축

- [ ] CANoe 프로젝트 생성 (2시간)
  - DBC 파일 임포트 (OpenDBC + 프로젝트)
  - 3개 네트워크 구성 (CAN-HS #1, #2, CAN-LS)

- [ ] 주요 ECU 노드 구현 (4시간)
  - EMS: `EMS16 (0x260)` 주기 전송 (10ms)
  - IVI: `IVI_AmbientLight (0x400)` 전송 (100ms)
  - BCM: LED 제어 + `BCM_LightControl (0x520)` 피드백
  - Gateway: 라우팅 규칙 (R011, R021)

- [ ] 시뮬레이션 Panel 구성 (1시간)
  - Control Panel: 테마 선택, Brightness 슬라이더
  - Display Panel: RGB 값, 피드백 상태

- [ ] 기본 테스트 시나리오 (1시간)
  - 속도 표시 (EMS → CLU)
  - 앰비언트 라이팅 (IVI → BCM → IVI)
  - Gateway 라우팅 검증

#### Phase 4-2: Level 4 - IVI ECU 상세 설계 (2월 16-17일)
**목표**: AUTOSAR 아키텍처 상세화 (선택적)

- [ ] AUTOSAR 레이어 다이어그램 (3시간)
  - ASW: Ambient Lighting Manager, User Profile Manager
  - RTE: Component 간 통신 인터페이스
  - BSW: COM, CanIf, CanTp, Dcm, NvM

- [ ] 기존 다이어그램 통합 (2시간)
  - `11_lighting_control.puml` → ASW 레이어
  - `12_adas_integration.puml` → ASW 레이어

- [ ] 상태 머신 다이어그램 (1시간)
  - Ambient Lighting 상태 머신
  - 에러 상태 처리

#### Phase 4-3: DBC 파일 통합 (2월 18일)
- [ ] `vehicle_system_integrated.dbc` 생성 (2시간)
  - OpenDBC + 프로젝트 DBC 병합
  - 메시지 ID 충돌 확인

- [ ] CANdb++ 검증 (1시간)
  - 네트워크 노드 확인 (47 ECUs)
  - 메시지/신호 정의 확인

#### Phase 4-4: 테스트 케이스 작성 (2월 19-20일)
- [ ] 기능 테스트 (2시간)
  - TC001: 속도 표시
  - TC002: 앰비언트 라이팅
  - TC003: Gateway 라우팅

- [ ] 오류 주입 테스트 (2시간)
  - TC004: CRC 오류
  - TC005: AliveCounter 타임아웃
  - TC006: LED 드라이버 고장

- [ ] 성능 테스트 (2시간)
  - TC007: 버스 로드 측정
  - TC008: 메시지 손실률
  - TC009: Gateway 레이턴시

### 핵심 질문 답변

#### Q1: 차량 시스템이란 무엇인가?
**답변**: "차량은 47개의 ECU가 CAN 네트워크로 연결된 분산 시스템입니다. Powertrain, Chassis, ADAS, Body, Infotainment, Safety, Gateway 7개 도메인으로 구성되며, 각 ECU는 독립적인 기능을 수행하지만 차량 전체 서비스를 위해 CAN 메시지로 데이터를 주고받습니다."

#### Q2: 통신이 왜 필요한가?
**답변**:
1. **속도 표시**: EMS가 측정한 속도를 CLU와 IVI가 표시하기 위해
2. **ADAS 경고**: F_CAMERA가 감지한 차선 이탈을 IVI가 시각화하기 위해
3. **앰비언트 라이팅**: IVI의 사용자 입력을 BCM이 LED 제어에 반영하고, 피드백을 IVI에 표시하기 위해

#### Q3: CANoe의 역할은?
**답변**: "CANoe는 실제 차량 없이 가상 차량 환경을 구축하는 시뮬레이션 도구입니다. 47개 ECU를 CAPL 노드로 구현하고, CAN 메시지 송수신을 검증하며, 통신 오류 및 성능을 테스트할 수 있습니다. 아키텍처 다이어그램에는 포함되지 않으며, 개발 및 테스트 도구로만 사용됩니다."

---

## 감사합니다!

**질문 환영합니다** 🙋‍♂️
