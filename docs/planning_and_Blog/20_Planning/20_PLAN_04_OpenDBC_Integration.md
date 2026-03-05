# OpenDBC 통합 계획 - 프로덕션급 DBC 파일 생성

## 🎯 목표

**실차 검증된 Hyundai/Kia OpenDBC를 베이스로 우리 프로젝트 특화 신호를 추가하여 최고 완성도의 DBC 파일 생성**

---

## 📊 OpenDBC 분석 결과

### 다운로드 파일
- **파일**: `hyundai_kia_base.dbc`
- **크기**: 1676 라인, 93KB
- **출처**: commaai/opendbc (실차 검증됨)

### ECU 구조 (40+ ECUs)

**프로덕션급 ECU 목록**:
```
EMS, TCU, ESP (ESC), MDPS, BCM, CLU (Cluster), SCC,
LDWS_LKAS (Camera), ABS, EPB, FATC (DATC), CGW,
IBOX (IVI), SPAS, LCA, AVM, PGS, HUD, TPMS,
ACU, SAS, AAF, REA, OPI, LPI, EVP, FPCM,
AHLS, AFLS, PSB, SNV, ECS, ODS, LVR, DI_BOX,
CUBIS, TMU, SMK, _4WD, MTS, AEMC, AAF_Tester, Dummy
```

### 메시지 개수
- **총 메시지**: 150+ 개
- **총 신호**: 1000+ 개
- **실차 검증**: ✅ 완료

---

## ✅ Level 1 아키텍처 매핑

### 우리 Level 1 ECU → OpenDBC ECU

| Level 1 ECU | OpenDBC ECU | 상태 | 비고 |
|------------|-------------|------|------|
| EMS | ✅ EMS | 완전 일치 | Engine Management System |
| TCU | ✅ TCU | 완전 일치 | Transmission Control Unit |
| ESP | ✅ ESC | 이름 다름 | Electronic Stability Control |
| MDPS | ✅ MDPS | 완전 일치 | Motor Driven Power Steering |
| BCM | ✅ BCM | 완전 일치 | Body Control Module |
| IVI | ✅ IBOX | 이름 다름 | In-Vehicle Infotainment Box |
| Cluster | ✅ CLU | 이름 다름 | Cluster Unit |
| Camera | ✅ LDWS_LKAS | 이름 다름 | Lane Departure Warning System / Lane Keeping Assist System |
| Radar | ✅ LCA | 이름 다름 | Lane Change Assist (Radar 기반) |
| SCC | ✅ SCC | 완전 일치 | Smart Cruise Control |
| CGW | ✅ CGW | 완전 일치 | Central Gateway |

**일치율**: 11/11 (100%) ✅

---

## 🔧 통합 전략

### 전략 1: ECU 이름 매핑 (권장 ⭐)

**방법**: OpenDBC ECU 이름을 우리 Level 1 이름으로 변경

**변경 사항**:
```dbc
# Before (OpenDBC)
BU_: ... ESC ... CLU ... LDWS_LKAS ... IBOX ... LCA ...

# After (우리 프로젝트)
BU_: ... ESP ... Cluster ... Camera ... IVI ... Radar ...
```

**장점**:
- ✅ Level 1 아키텍처와 100% 일치
- ✅ 멘토링 때 설명 용이
- ✅ 프로젝트 일관성 유지

**단점**:
- ⚠️ 모든 메시지의 송신자/수신자 이름 변경 필요

---

### 전략 2: Level 1 아키텍처 수정 (대안)

**방법**: Level 1 다이어그램의 ECU 이름을 OpenDBC에 맞춤

**변경 사항**:
```
# Level 1 아키텍처 수정
ESP → ESC
Cluster → CLU
Camera → LDWS_LKAS
IVI → IBOX
Radar → LCA
```

**장점**:
- ✅ DBC 파일 수정 최소화
- ✅ 실차 용어 그대로 사용

**단점**:
- ❌ Level 1 다이어그램 재작성 필요
- ❌ 기존 문서 모두 수정 필요

---

## 🎯 최종 선택: **전략 1 (ECU 이름 매핑)** ⭐

**이유**:
1. ✅ Level 1 아키텍처는 이미 완성 (PNG 생성 완료)
2. ✅ DBC 파일만 수정하면 됨
3. ✅ 프로젝트 일관성 유지
4. ✅ 멘토링 설명 용이

---

## 📝 구현 계획

### Phase 1: ECU 이름 변경

**작업 파일**: `hyundai_kia_base.dbc`

**변경 목록**:
```bash
# 1. BU_ 라인 수정 (Line 36)
ESC → ESP
CLU → Cluster
LDWS_LKAS → Camera
IBOX → IVI
LCA → Radar

# 2. 모든 메시지의 송신자 변경
BO_ xxx XXX: 8 ESC → BO_ xxx XXX: 8 ESP
BO_ xxx XXX: 8 CLU → BO_ xxx XXX: 8 Cluster
BO_ xxx XXX: 8 LDWS_LKAS → BO_ xxx XXX: 8 Camera
BO_ xxx XXX: 8 IBOX → BO_ xxx XXX: 8 IVI
BO_ xxx XXX: 8 LCA → BO_ xxx XXX: 8 Radar

# 3. 모든 신호의 수신자 변경
SG_ xxx : ... \"\" ESC → SG_ xxx : ... \"\" ESP
SG_ xxx : ... \"\" CLU → SG_ xxx : ... \"\" Cluster
SG_ xxx : ... \"\" LDWS_LKAS → SG_ xxx : ... \"\" Camera
SG_ xxx : ... \"\" IBOX → SG_ xxx : ... \"\" IVI
SG_ xxx : ... \"\" LCA → SG_ xxx : ... \"\" Radar
```

---

### Phase 2: 프로젝트 특화 신호 추가

**추가할 메시지**:

#### 1. IVI_AmbientLight (0x400)
```dbc
BO_ 1024 IVI_AmbientLight: 8 IVI
 SG_ Ambient_Light_R : 0|8@1+ (1,0) [0|255] "" BCM
 SG_ Ambient_Light_G : 8|8@1+ (1,0) [0|255] "" BCM
 SG_ Ambient_Light_B : 16|8@1+ (1,0) [0|255] "" BCM
 SG_ Brightness : 24|8@1+ (0.4,0) [0|100] "%" BCM
 SG_ Theme_Package : 32|8@1+ (1,0) [0|10] "" BCM
 SG_ AliveCounter : 56|4@1+ (1,0) [0|15] "" CGW
 SG_ Checksum : 60|4@1+ (1,0) [0|15] "" CGW
```

#### 2. IVI_Profile (0x410)
```dbc
BO_ 1040 IVI_Profile: 8 IVI
 SG_ Profile_ID : 0|8@1+ (1,0) [0|5] "" BCM
 SG_ Scenario_ID : 8|8@1+ (1,0) [0|20] "" BCM
 SG_ Scenario_Params : 16|32@1+ (1,0) [0|4294967295] "" BCM
```

#### 3. BCM_LightControl (0x510)
```dbc
BO_ 1296 BCM_LightControl: 8 BCM
 SG_ Headlight_Status : 0|2@1+ (1,0) [0|3] "" Cluster
 SG_ Ambient_Light_Active : 2|1@1+ (1,0) [0|1] "" Cluster
 SG_ Ambient_R_Actual : 8|8@1+ (1,0) [0|255] "" CGW
 SG_ Ambient_G_Actual : 16|8@1+ (1,0) [0|255] "" CGW
 SG_ Ambient_B_Actual : 24|8@1+ (1,0) [0|255] "" CGW
```

**Value Tables**:
```dbc
VAL_ 1024 Theme_Package 0 "SPORT" 1 "COMFORT" 2 "ECO" 3 "CUSTOM1" 4 "CUSTOM2" 5 "CUSTOM3";
VAL_ 1040 Profile_ID 0 "DRIVER1" 1 "DRIVER2" 2 "DRIVER3" 3 "GUEST" 4 "VALET";
VAL_ 1296 Headlight_Status 0 "OFF" 1 "PARKING" 2 "LOW_BEAM" 3 "HIGH_BEAM";
```

---

### Phase 3: 주석 추가

**각 ECU에 주석 추가**:
```dbc
CM_ BU_ EMS "Engine Management System - Powertrain Domain";
CM_ BU_ TCU "Transmission Control Unit - Powertrain Domain";
CM_ BU_ ESP "Electronic Stability Program - Chassis Domain";
CM_ BU_ MDPS "Motor Driven Power Steering - Chassis Domain";
CM_ BU_ BCM "Body Control Module - Body Domain";
CM_ BU_ IVI "In-Vehicle Infotainment - Infotainment Domain";
CM_ BU_ Cluster "Instrument Cluster - Infotainment Domain";
CM_ BU_ Camera "Front Camera (ADAS) - ADAS Domain";
CM_ BU_ Radar "Blind Spot Detection Radar - ADAS Domain";
CM_ BU_ SCC "Smart Cruise Control - ADAS Domain";
CM_ BU_ CGW "Central Gateway - Gateway Domain";
```

**프로젝트 특화 메시지에 주석 추가**:
```dbc
CM_ BO_ 1024 "IVI Ambient Lighting Control - Project Specific";
CM_ BO_ 1040 "IVI User Profile Management - Project Specific";
CM_ BO_ 1296 "BCM Light Control with Ambient Feedback - Project Specific";
```

---

## 📊 예상 결과

### 최종 DBC 파일 구성

| 항목 | OpenDBC 원본 | 우리 추가 | 최종 합계 |
|------|-------------|----------|----------|
| **ECU 개수** | 40+ | 0 | 40+ |
| **메시지 개수** | 150+ | 3 | 153+ |
| **신호 개수** | 1000+ | 20 | 1020+ |
| **Value Tables** | 50+ | 3 | 53+ |
| **주석** | 0 | 14 | 14 |

### 완성도 비교

| 항목 | 기존 커스텀 DBC | OpenDBC 통합 | 개선율 |
|------|----------------|-------------|--------|
| 메시지 개수 | 17 | 153+ | **900%** ⬆️ |
| 신호 개수 | 85 | 1020+ | **1200%** ⬆️ |
| 실차 검증 | ❌ | ✅ | **100%** ⬆️ |
| 프로젝트 특화 | ✅ | ✅ | 유지 |
| Level 1 일치 | ✅ | ✅ | 유지 |

---

## 🚀 실행 단계

### Step 1: ECU 이름 일괄 변경
```bash
# sed 명령어로 일괄 변경
sed -i '' 's/\bESC\b/ESP/g' hyundai_kia_base.dbc
sed -i '' 's/\bCLU\b/Cluster/g' hyundai_kia_base.dbc
sed -i '' 's/\bLDWS_LKAS\b/Camera/g' hyundai_kia_base.dbc
sed -i '' 's/\bIBOX\b/IVI/g' hyundai_kia_base.dbc
sed -i '' 's/\bLCA\b/Radar/g' hyundai_kia_base.dbc
```

### Step 2: 프로젝트 특화 메시지 추가
- `IVI_AmbientLight` 메시지 추가
- `IVI_Profile` 메시지 추가
- `BCM_LightControl` 메시지 추가

### Step 3: 주석 및 Value Tables 추가
- ECU 주석 추가
- 메시지 주석 추가
- Value Tables 추가

### Step 4: 검증
- CANoe 로드 테스트
- Level 1 아키텍처 일치성 확인
- 통신 시나리오 커버리지 확인

---

## ✅ 성공 지표

1. ✅ **프로덕션급 완성도**: 1000+ 신호, 실차 검증
2. ✅ **Level 1 일치**: ECU 이름 100% 일치
3. ✅ **프로젝트 특화**: 앰비언트 라이팅 신호 포함
4. ✅ **멘토링 준비**: 실차 기반 + 신규 기능 개발 어필

---

**계획 작성 완료**: 2026-02-11 03:20
**다음 단계**: 사용자 승인 후 EXECUTION 모드로 전환

---

## 📝 Document Status
**Status**: Released
**Review**: Pending Mentoring Session (2026-02-13)
**Verification**: Artificial Intelligence Assistant
**Last Updated**: 2026-02-11
