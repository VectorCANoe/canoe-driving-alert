# Level 1: Vehicle System Architecture Specification

## 📋 개요

**문서 목적**: 47개 ECU 도메인 분류 및 전체 차량 시스템 아키텍처 정의
**기준**: Hyundai/Kia OpenDBC + Tier1 Best Practices
**표준**: ISO 26262, AUTOSAR, Hyundai/Mobis 네이밍 컨벤션

---

## 🏗️ 도메인 분류 (7 Domains)

### 1. Powertrain Domain (동력계) - 7 ECUs

**목적**: 엔진 및 변속기 제어

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| EMS | Engine Management System | 엔진 제어, 연료 분사, 점화 타이밍 | D |
| TCU | Transmission Control Unit | 변속 제어, 기어 선택 | C |
| OPI | Oil Pump Inverter | 오일 펌프 인버터 제어 | B |
| LPI | LPG Injection | LPG 연료 분사 제어 | C |
| FPCM | Fuel Pump Control Module | 연료 펌프 제어 | C |
| REA | Rear Engine Actuator | 후방 엔진 액추에이터 | B |
| AAF | Active Air Flap | 능동형 에어 플랩 (공기역학) | QM |

**네트워크**: CAN-HS #1 (500 kbps)
**특징**: 실시간 제어, 10-100ms 주기, 최고 안전 등급

---

### 2. Chassis Domain (섀시) - 6 ECUs

**목적**: 차량 주행 안정성 및 조향 제어

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| ESP | Electronic Stability Program | 차량 자세 제어, 미끄럼 방지 | D |
| ABS | Anti-lock Braking System | 급제동 시 바퀴 잠김 방지 | D |
| MDPS | Motor Driven Power Steering | 전동식 파워 스티어링 | C |
| SAS | Steering Angle Sensor | 조향각 센서 | C |
| EPB | Electronic Parking Brake | 전자식 주차 브레이크 | C |
| ECS | Electronic Control Suspension | 전자 제어 서스펜션 | B |

**네트워크**: CAN-HS #1 (500 kbps)
**특징**: 안전 최우선, 고속 통신, 실시간 제어

---

### 3. ADAS Domain (첨단 운전자 지원) - 7 ECUs

**목적**: 운전자 보조 및 자율주행 기능

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| F_CAMERA | Front Camera (LDWS/LKAS) | 차선 이탈 경고, 차선 유지 보조 | B |
| BSD_RADAR | Blind Spot Detection (LCA) | 사각지대 감지, 차선 변경 보조 | B |
| SCC | Smart Cruise Control | 스마트 크루즈 컨트롤 | B |
| SPAS | Smart Parking Assist System | 스마트 주차 보조 | B |
| AVM | Around View Monitor | 어라운드 뷰 모니터 (360도 카메라) | QM |
| PGS | Parking Guidance System | 주차 가이드 시스템 | QM |
| SNV | Surround Night Vision | 서라운드 나이트 비전 | QM |

**네트워크**: CAN-HS #2 (500 kbps)
**특징**: 센서 융합, 고대역폭, 이미지/레이더 데이터

---

### 4. Body Domain (바디) - 8 ECUs

**목적**: 차체 제어 및 편의 기능

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| BCM | Body Control Module | 도어, 조명, 와이퍼 제어 | QM |
| DATC | Dual Auto Temperature Control | 듀얼 오토 에어컨 제어 | QM |
| FATC | Full Auto Temperature Control | 풀 오토 에어컨 제어 | QM |
| AFLS | Adaptive Front Lighting System | 적응형 전방 조명 시스템 | QM |
| AHLS | Adaptive High-beam Light System | 적응형 하이빔 조명 시스템 | QM |
| PSB | Pre-Safe Belt | 프리세이프 벨트 (사고 전 벨트 긴장) | B |
| TPMS | Tire Pressure Monitoring System | 타이어 공기압 모니터링 | QM |
| SMK | Smart Key | 스마트 키 (키리스 엔트리) | QM |

**네트워크**: CAN-LS (125 kbps)
**특징**: 편의 기능, 이벤트 기반, 낮은 우선순위

---

### 5. Infotainment Domain (인포테인먼트) - 5 ECUs

**목적**: 사용자 인터페이스 및 엔터테인먼트

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| IVI | In-Vehicle Infotainment (IBOX) | 미디어, 내비게이션, 앰비언트 라이팅 ⭐ | QM |
| CLU | Cluster Unit | 계기판 (속도, RPM, 경고등) | QM |
| HUD | Head-Up Display | 헤드업 디스플레이 | QM |
| TMU | Telematics Unit | 텔레매틱스 (통신, 원격 제어) | QM |
| CUBIS | Connected User Box Infotainment | 커넥티드 유저 박스 | QM |

**네트워크**: CAN-HS #2 (500 kbps)
**특징**: 사용자 경험, 멀티미디어, 높은 대역폭

---

### 6. Safety Domain (안전) - 2 ECUs

**목적**: 승객 안전 시스템

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| ACU | Airbag Control Unit | 에어백 제어, 충돌 감지 | D |
| ODS | Occupant Detection System | 승객 감지 시스템 (에어백 최적화) | C |

**네트워크**: CAN-HS #1 (500 kbps)
**특징**: 최고 안전 등급, 실시간 충돌 감지

---

### 7. Gateway Domain (게이트웨이) - 1 ECU

**목적**: 네트워크 간 메시지 라우팅 및 보안

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| CGW | Central Gateway | 네트워크 라우팅, 메시지 필터링, 진단 | C |

**네트워크**: CAN-HS #1, CAN-HS #2, CAN-LS (모두 연결)
**특징**: 네트워크 허브, 보안 게이트웨이, UDS 진단

---

### 8. Other ECUs (기타) - 11 ECUs

**목적**: 특수 기능 및 테스트

| ECU | 전체 이름 | 주요 기능 | ASIL |
|-----|----------|----------|------|
| LVR | Lever | 레버 (기어 레버, 와이퍼 레버) | QM |
| EVP | Electric Vacuum Pump | 전동 진공 펌프 | B |
| DI_BOX | Direct Injection Box | 직분사 박스 | C |
| _4WD | 4-Wheel Drive Control | 4륜 구동 제어 | B |
| MTS | Manual Transmission System | 수동 변속기 시스템 | C |
| AEMC | Active Engine Mount Control | 능동형 엔진 마운트 제어 | QM |
| IAP | Intake Air Pressure | 흡기 압력 센서 | C |
| AAF_Tester | AAF Test Equipment | AAF 테스트 장비 | - |
| Dummy | Virtual ECU | 시뮬레이션 노드 | - |

---

## 🌐 네트워크 토폴로지

### CAN-HS #1 (500 kbps) - Safety-Critical Network

**연결 ECU**:
- Powertrain: EMS, TCU, OPI, LPI, FPCM, REA
- Chassis: ESP, ABS, MDPS, SAS, EPB, ECS
- Safety: ACU, ODS

**특징**:
- ✅ 최고 우선순위
- ✅ ASIL-D 메시지
- ✅ 10-100ms 주기
- ✅ 실시간 제어

---

### CAN-HS #2 (500 kbps) - User Interface Network

**연결 ECU**:
- ADAS: F_CAMERA, BSD_RADAR, SCC, SPAS, AVM, PGS, SNV
- Infotainment: IVI, CLU, HUD, TMU, CUBIS

**특징**:
- ✅ 사용자 인터페이스
- ✅ 센서 데이터 (이미지, 레이더)
- ✅ 멀티미디어
- ✅ 100-1000ms 주기

---

### CAN-LS (125 kbps) - Comfort Network

**연결 ECU**:
- Body: BCM, DATC, FATC, AFLS, AHLS, PSB, TPMS, SMK

**특징**:
- ✅ 편의 기능
- ✅ 이벤트 기반
- ✅ 낮은 우선순위
- ✅ 100-1000ms 주기

---

## 🔀 Gateway 라우팅 규칙

### CAN-HS #1 → CAN-HS #2

**메시지 예시**:
```
EMS (0x316) → Vehicle_Speed → CGW → CLU
- 목적: 계기판에 속도 표시
- 주기: 10ms
- ASIL: D
```

### CAN-HS #2 → CAN-LS

**메시지 예시**:
```
IVI (0x400) → Ambient_Light_RGB → CGW → BCM (0x520) ⭐
- 목적: 앰비언트 라이팅 제어 (프로젝트 특화)
- 주기: 100ms
- ASIL: QM
```

### CAN-HS #1 → CAN-LS

**메시지 예시**:
```
ESP (0x200) → Stability_Status → CGW → BCM
- 목적: ESP 경고등 표시
- 주기: 100ms
- ASIL: D → QM (다운그레이드)
```

---

## 📊 도메인별 통계

| 도메인 | ECU 수 | 네트워크 | ASIL 레벨 | 주기 |
|--------|--------|----------|-----------|------|
| Powertrain | 7 | CAN-HS #1 | B-D | 10-100ms |
| Chassis | 6 | CAN-HS #1 | B-D | 10-100ms |
| ADAS | 7 | CAN-HS #2 | B-QM | 100-1000ms |
| Body | 8 | CAN-LS | QM-B | 100-1000ms |
| Infotainment | 5 | CAN-HS #2 | QM | 100-1000ms |
| Safety | 2 | CAN-HS #1 | C-D | 10-100ms |
| Gateway | 1 | All | C | - |
| Others | 11 | Various | QM-C | - |
| **합계** | **47** | **3 networks** | **QM-D** | **10-1000ms** |

---

## 🎯 Tier1 Best Practices 적용

### 1. Hyundai/Mobis 도메인 분류
- ✅ Powertrain, Chassis, ADAS, Body, Infotainment, Safety 분리
- ✅ 산업 표준 ECU 네이밍 (ESP, CLU, F_CAMERA, IVI, BSD_RADAR)

### 2. ISO 26262 안전 도메인
- ✅ ASIL-D: Powertrain, Chassis, Safety (CAN-HS #1)
- ✅ ASIL-B/C: ADAS (CAN-HS #2)
- ✅ QM: Body, Infotainment (CAN-LS, CAN-HS #2)

### 3. AUTOSAR 아키텍처 패턴
- ✅ Gateway 중심 토폴로지
- ✅ 네트워크 분리 (안전/편의)
- ✅ 메시지 필터링 및 라우팅

---

**작성일**: 2026-02-11
**기준**: Hyundai/Kia OpenDBC (47 ECU, 1325 signals)
**표준**: ISO 26262, AUTOSAR, Hyundai/Mobis
