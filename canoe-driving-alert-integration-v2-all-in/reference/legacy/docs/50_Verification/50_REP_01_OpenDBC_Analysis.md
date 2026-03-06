# OpenDBC 분석 결과 - 실제 차량 ECU 구조

## 📊 분석 대상
- **Tesla**: `tesla_can.dbc` (commaai/opendbc)
- **Hyundai/Kia**: `hyundai_kia_generic.dbc` (commaai/opendbc)

---

## 🚗 Tesla 차량 ECU 구조

### 네트워크 노드 (ECUs)
분석 중인 DBC 파일에서 확인된 주요 ECU들:

1. **DI (Driver Interface / Instrument Cluster)**
   - 역할: 계기판, 운전자 정보 표시
   - 주요 메시지: 속도, RPM, 경고등

2. **EPAS (Electric Power Assisted Steering)**
   - 역할: 전동식 조향 제어
   - 주요 메시지: 조향각, 조향 토크

3. **ESP (Electronic Stability Program)**
   - 역할: 차체 안정성 제어
   - 주요 메시지: 요 레이트, 횡가속도, 휠 속도

4. **IC (Instrument Cluster)**
   - 역할: 계기판 표시
   - 주요 메시지: 차량 상태 정보

5. **GTW (Gateway)**
   - 역할: 네트워크 중계
   - 주요 메시지: 네트워크 간 메시지 라우팅

### 주요 CAN 메시지 예시

**메시지 ID 0x118: DI_torque2**
- 송신: DI (Driver Interface)
- 주기: 10ms
- 시그널:
  - `DI_torqueDriver`: 운전자 요청 토크
  - `DI_torqueMotor`: 모터 출력 토크

**메시지 ID 0x129: DI_state**
- 송신: DI
- 주기: 100ms
- 시그널:
  - `DI_gear`: 기어 위치 (P, R, N, D)
  - `DI_cruiseState`: 크루즈 컨트롤 상태

**메시지 ID 0x370: EPAS_sysStatus**
- 송신: EPAS (조향 ECU)
- 주기: 100ms
- 시그널:
  - `EPAS_steeringAngle`: 조향각 (-2048 ~ +2047)
  - `EPAS_steeringRate`: 조향 속도

---

## 🚗 Hyundai/Kia 차량 ECU 구조

### 네트워크 노드 (ECUs)

1. **SCC (Smart Cruise Control)**
   - 역할: 어댑티브 크루즈 컨트롤
   - ADAS 기능

2. **LKAS (Lane Keeping Assist System)**
   - 역할: 차선 유지 보조
   - ADAS 기능

3. **MDPS (Motor Driven Power Steering)**
   - 역할: 전동식 조향 제어
   - 조향 제어

4. **CLU (Cluster)**
   - 역할: 계기판
   - 정보 표시

5. **EMS (Engine Management System)**
   - 역할: 엔진 제어
   - Powertrain

6. **ESP (Electronic Stability Program)**
   - 역할: 차체 안정성 제어
   - Chassis

7. **BCM (Body Control Module)**
   - 역할: 바디 전장 제어
   - Body Domain

8. **FATC (Full Auto Temperature Control)**
   - 역할: 공조 시스템
   - Comfort

### 주요 CAN 메시지 예시

**메시지 ID 0x340: SCC11 (Smart Cruise Control)**
- 송신: SCC
- 주기: 50ms
- 시그널:
  - `MainMode_ACC`: ACC 메인 모드
  - `SCCInfoDisplay`: SCC 정보 표시
  - `AliveCounterACC`: Alive 카운터
  - `VSetDis`: 설정 속도

**메시지 ID 0x420: LKAS11 (Lane Keeping Assist)**
- 송신: LKAS
- 주기: 100ms
- 시그널:
  - `CF_Lkas_LdwsActivemode`: LDW 활성 모드
  - `CF_Lkas_LdwsSysState`: LDW 시스템 상태
  - `CF_Lkas_LdwsWarning`: LDW 경고

**메시지 ID 0x2B0: MDPS12 (Motor Driven Power Steering)**
- 송신: MDPS
- 주기: 20ms
- 시그널:
  - `CF_Mdps_ToiActive`: 조향 토크 활성
  - `CF_Mdps_ToiUnavail`: 조향 토크 불가
  - `CF_Mdps_FailStat`: 조향 실패 상태

**메시지 ID 0x4F1: CLU11 (Cluster)**
- 송신: CLU
- 주기: 50ms
- 시그널:
  - `CF_Clu_CruiseSwState`: 크루즈 스위치 상태
  - `CF_Clu_CruiseSwMain`: 크루즈 메인 스위치
  - `CF_Clu_SldMainSW`: 슬라이드 메인 스위치

**메시지 ID 0x371: EMS11 (Engine Management)**
- 송신: EMS
- 주기: 100ms
- 시그널:
  - `TPS`: 스로틀 위치 센서
  - `PV_AV_CAN`: 엔진 RPM
  - `AliveCounter`: Alive 카운터

**메시지 ID 0x386: ESP12 (Electronic Stability Program)**
- 송신: ESP
- 주기: 100ms
- 시그널:
  - `CYL_PRES`: 실린더 압력
  - `LAT_ACCEL`: 횡가속도
  - `YAW_RATE`: 요 레이트

---

## 🎯 프로젝트 적용 인사이트

### 1. 도메인별 ECU 분류

#### Powertrain Domain
- **EMS** (Engine Management System)
  - 엔진 RPM, 스로틀 위치, 토크
  - CAN ID 범위: 0x300-0x3FF (예상)

#### Chassis Domain
- **ESP** (Electronic Stability Program)
  - 휠 속도, 요 레이트, 횡가속도
- **MDPS** (Motor Driven Power Steering)
  - 조향각, 조향 토크
  - CAN ID 범위: 0x200-0x2FF (예상)

#### Body Domain
- **BCM** (Body Control Module)
  - 도어 상태, 조명 제어
- **FATC** (Full Auto Temperature Control)
  - 공조 제어
  - CAN ID 범위: 0x500-0x5FF (예상)

#### Infotainment / ADAS Domain
- **SCC** (Smart Cruise Control)
  - ACC 기능
- **LKAS** (Lane Keeping Assist)
  - LDW 경고
- **CLU** (Cluster)
  - 계기판 표시
  - CAN ID 범위: 0x400-0x4FF (예상)

### 2. 통신 필요성 시나리오 (실제 예시)

#### 시나리오 1: 속도 표시
```
EMS (0x371) → RPM 정보 송신
    ↓
CLU (Cluster) → 계기판에 RPM 표시
```

#### 시나리오 2: ADAS 경고
```
LKAS (0x420) → LDW 경고 송신
    ↓
CLU (Cluster) → 경고등 표시
IVI → 시각적 경고 표시
```

#### 시나리오 3: 크루즈 컨트롤
```
CLU (0x4F1) → 크루즈 스위치 상태 송신
    ↓
SCC (0x340) → 크루즈 제어 활성화
    ↓
EMS → 속도 제어
```

### 3. CAN 메시지 ID 할당 전략

**우리 프로젝트 CAN ID 할당**:
- 0x100-0x1FF: Powertrain (엔진, 변속기)
- 0x200-0x2FF: Chassis (조향, 제동, 차체 제어)
- 0x300-0x3FF: ADAS (LDW, AEB, BSD)
- 0x400-0x4FF: Infotainment (IVI, Cluster)
- 0x500-0x5FF: Body (BCM, 도어, 조명)
- 0x600-0x6FF: Comfort (공조, 시트)
- 0x700-0x7FF: Gateway / Diagnostic

### 4. 주요 시그널 타입

**Alive Counter**:
- 목적: 메시지 신선도 확인
- 범위: 0-15 (4-bit)
- 매 메시지마다 +1 증가

**Checksum**:
- 목적: 메시지 무결성 확인
- 범위: 0-255 (8-bit)
- CRC 또는 XOR 기반

**State / Status**:
- 목적: ECU 상태 표시
- 예: ACTIVE, STANDBY, FAULT, UNAVAILABLE

**Physical Values**:
- 목적: 센서 측정값
- 예: 속도 (km/h), 각도 (deg), 토크 (Nm)
- Resolution, Offset, Unit 정의 필요

---

## 📋 차주 과제 적용

### OpenDBC 기반 ECU 목록 작성 ✅

| 도메인 | ECU 이름 | 역할 | 참고 차량 |
|--------|---------|------|----------|
| Powertrain | EMS | 엔진 제어 | Hyundai/Kia |
| Powertrain | TCU | 변속기 제어 | (추가 조사 필요) |
| Chassis | ESP | 차체 안정성 | Tesla, Hyundai |
| Chassis | MDPS/EPAS | 전동 조향 | Hyundai (MDPS), Tesla (EPAS) |
| Chassis | ABS | 제동 제어 | (ESP 통합 가능) |
| Body | BCM | 바디 제어 | Hyundai/Kia |
| Body | Door ECU | 도어 제어 | (BCM 통합 가능) |
| Body | Light ECU | 조명 제어 | (BCM 통합 가능) |
| Infotainment | IVI | 인포테인먼트 | **우리 프로젝트 특화** |
| Infotainment | CLU/IC | 계기판 | Hyundai (CLU), Tesla (IC) |
| ADAS | SCC | 크루즈 컨트롤 | Hyundai/Kia |
| ADAS | LKAS | 차선 유지 | Hyundai/Kia |
| ADAS | Camera ECU | 카메라 센서 | **우리 프로젝트 추가** |
| Gateway | GTW | 네트워크 중계 | Tesla |
| Comfort | FATC | 공조 시스템 | Hyundai/Kia |

### 통신 필요성 설명 준비 ✅

**실제 차량 예시 기반 설명**:
1. Hyundai LKAS → CLU: LDW 경고 전달
2. EMS → CLU: 엔진 RPM 전달
3. SCC → EMS: 크루즈 컨트롤 속도 제어

---

## 🚀 다음 단계

1. **Level 1 아키텍처 작성**
   - 위 ECU 목록 기반
   - 도메인별 그룹화
   - CAN 네트워크 연결

2. **CAN 데이터베이스 초안**
   - OpenDBC 구조 참고
   - 우리 프로젝트 메시지 정의
   - BO_, SG_ 형식 작성

3. **통신 시나리오 다이어그램**
   - 실제 차량 예시 활용
   - 시퀀스 다이어그램 작성

---

**분석 완료**: 2026-02-10
**참고 자료**: commaai/opendbc GitHub

---

## 📝 Document Status
**Status**: Released
**Review**: Pending Mentoring Session (2026-02-13)
**Verification**: Artificial Intelligence Assistant
**Last Updated**: 2026-02-11
