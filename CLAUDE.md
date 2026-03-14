# CLAUDE.md — Mobis PBL 프로젝트 컨텍스트

> Claude Code가 매 세션 시작 시 자동으로 읽습니다.

---

## 프로젝트 기본 정보

- **저장소**: `C:\Users\이준영\canoe-driving-alert` (git: `main` 브랜치)
- **개발 환경**: CANoe 19.4, CAPL, Windows 11

> **⚠️ 단일 활성 프로젝트 — 아래 경로만 읽고 수정한다:**

### 활성 문서 (유일한 현행 기준)
- **프로젝트 문서 전체**: `driving-alert-workproducts/` — 01~07 전 문서 현행 기준
  - `driving-alert-workproducts/01_Requirements.md` — Req_001~Req_043 확정
  - `driving-alert-workproducts/02_Concept_design.md`
  - `driving-alert-workproducts/03_Function_definition.md` + `0301~0304`
  - `driving-alert-workproducts/04_SW_Implementation.md`
  - `driving-alert-workproducts/05_Unit_Test.md` — UT_*_001 체계
  - `driving-alert-workproducts/06_Integration_Test.md` — IT_*_001 체계
  - `driving-alert-workproducts/07_System_Test.md` — ST_*_001 체계
  - `driving-alert-workproducts/ops/` — 임시 작업 파일 (완료 후 삭제)
  - `driving-alert-workproducts/compact/` — 요약본

- **CAPL 노드**: `canoe/nodes/*.can` — 현행 구현 소스
- **DBC**: `canoe/databases/emergency_system.dbc`
- **CANoe 설정**: `canoe/cfg/CAN_500kBaud_1ch.cfg`

### 레거시 (읽기 전용 — 절대 수정 금지, 참조만)
- `docs/LIN-Door/` — BCM/Door 샘플 프로젝트 (구조·형식 참조용)
- `docs/OTA_original/` — 구 OTA 문서 백업
- `docs/v2x/`, `docs/v2x_original/` — 구 V2X 문서
- `docs/OTA/`, `docs/architecture/`, `docs/V-Model/`, `docs/mentoring/` — 전부 레거시
- `reference/` — 참조 DBC/CAPL 예제 (구조 참조용)

**규칙: `driving-alert-workproducts/` 외의 문서를 현행 기준으로 혼동하지 않는다.**

---

## CANoe 설정 직접 편집 금지 (필수 — 매 세션 확인)

> **⚠️ 이 규칙을 어기면 .cfg 파일이 깨집니다. 반드시 지킬 것.**

| 파일/작업 | 허용 주체 | 비고 |
|-----------|----------|------|
| `canoe/cfg/*.cfg` | **GUI 전용** | 에이전트 직접 편집·패치 절대 금지 |
| `*.cfg.ini`, `*.stcfg` | **GUI 자동생성** | 커밋 금지, 에이전트 생성 금지 |
| Panel (`.xvp`) | **GUI 전용** | 레이아웃·바인딩은 CANoe Panel Editor에서만 |
| `project.sysvars` | 텍스트 편집 가능 | 단, 편집 후 반드시 CANoe GUI에서 로드·동기화·저장 필요 |
| `canoe/src/capl/**/*.can` | 에이전트 편집 가능 | CAPL 소스는 자유롭게 수정 가능 |
| `canoe/databases/*.dbc` | 에이전트 편집 가능 | DBC 소스는 자유롭게 수정 가능 |

**cfg 복구 순서**: 측정 중지 → CANoe 완전 종료 → GUI에서 .cfg 재오픈 → sysvar/패널 변경사항 GUI에서 적용 → Save → 커밋

상세 규칙: `canoe/cfg/GUI_ONLY_OPERATIONS.md`

---

## CANoe 파일 작성 레퍼런스 (반드시 참조)

> **규칙**: CANoe 관련 파일(.sysvars, .dbc, .can, .cfg) 작성 전 반드시 아래 레퍼런스를 먼저 읽고 동일한 형식으로 작성한다.

### 핵심 레퍼런스 위치

| 파일 | 경로 | 용도 |
|------|------|------|
| **sysvars** | `docs/LIN-Door/canoe/cfg/sample_project.sysvars` | System Variables 표준 형식 |
| **dbc** | `docs/LIN-Door/canoe/databases/sample_project.dbc` | DBC 표준 형식 |
| **CAPL 노드** | `docs/LIN-Door/canoe/nodes/*.can` | CAPL 노드 구조 (BCM, Gateway, Tester 등 7개) |
| **CAPL 레거시** | `reference/legacy/capl_nodes/*.can` | 추가 CAPL 예제 (EMS, ESP, IVI 등 13개) |
| **cfg** | `docs/LIN-Door/canoe/cfg/sample_project.cfg` | CANoe cfg 형식 |

### sysvars 필수 형식 규칙

```xml
<?xml version="1.0" encoding="utf-8"?>
<SystemVariables version="4.0">            <!-- version="4.0" 필수 -->
  <Namespace name="MyNS" comment="...">
    <Variable name="myVar"
              type="uint32"               <!-- int → uint32 -->
              initValue="0"              <!-- value= 아님, initValue= -->
              minValue="0"
              maxValue="1"
              unit=""
              comment="설명"/>
    <Variable name="myFloat"
              type="float64"              <!-- float → float64 -->
              initValue="0.0"
              minValue="0.0"
              maxValue="100.0"
              unit="km/h"
              comment="설명"/>
  </Namespace>
</SystemVariables>
```

### DBC 필수 형식 규칙

- 블록 주석 `/* */` **절대 금지** → 파싱 에러
- 화살표 `→` 유니코드 **금지** → `->` 사용
- 주석은 `CM_` 섹션에만 작성
- 참조: `canoe/databases/emergency_system_explained.md`

---

## CANoe 19 로컬 설치 레퍼런스 경로

> Vector CANoe 19 설치 시 포함된 공식 파일들. 신규 파일 작성 전 반드시 확인.

### Templates (공식 빈 템플릿)

```
C:/Users/Public/Documents/Vector/CANoe/19 (x64)/Templates/
  Database/
    CANTemplate.dbc          ← DBC 공식 빈 템플릿 (NS_ 섹션 전체 포함)
    EmptyTemplate.dbc        ← 최소 DBC 템플릿
    CANoeTemplate.dbc        ← CANoe 전용 속성 포함 DBC 템플릿
    CAN_FD Template.dbc      ← CAN FD 템플릿
  CANoe/
    CAN_500kBaud_1ch.tcn/.tcx   ← 우리 프로젝트와 동일한 cfg 원본 템플릿
    CAN_500kBaud_2ch.tcn/.tcx
```

### Reusable CAPL Includes (공식 재사용 라이브러리)

```
C:/Users/Public/Documents/Vector/CANoe/19 (x64)/Reusable/
  CAPL_Includes/
    Diagnostics/CCI_CanTP.cin    ← CAN Transport Protocol 라이브러리
    Diagnostics/CCI_DoIP.cin     ← DoIP 라이브러리
    Diagnostics/CCI_LINTP.cin    ← LIN TP 라이브러리
  LINCaplLibs/
    J2602_Slave_Conformance_Test_Lib.can
```

### CANoe Sample Configurations (레포 내 완비)

```
canoe/reference/vector_samples_19_4_10/   ← Vector CANoe 19.4.10 공식 샘플 전체 복사본
  CAN/          CAN 기본·시스템·진단 샘플
  Ethernet/     Ethernet·DoIP·진단 샘플
  LIN/          LIN 샘플
  SIL/          SIL Kit 샘플
  Python/       Python COM API 샘플
  ADAS/         ADAS 시나리오 샘플
  (총 7,883 파일 — .can 738개, .dbc 115개, .xvp 977개, .vsysvar 202개, .cfg 298개)
```
> **✅ 완비** — `canoe/reference/vector_samples_19_4_10/` 에 원본과 동일하게 전부 복사됨.

### Vector 샘플 핵심 참조 경로 (용도별)

> CANoe 파일 작성 전, 아래 경로의 실제 파일을 Read로 먼저 열어 패턴을 확인한다.

| 용도 | 참조 경로 | 설명 |
|------|-----------|------|
| **vsysvar 포맷** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/SysVar/SystemDefSysVar.vsysvar` | Namespace·Variable 포맷 실사례 |
| **CAN Gateway 패턴** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Nodes/Gateway.can` | 2-클러스터 CAN 라우팅 |
| **CAN ECU 노드** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Nodes/Engine.can` | ECU 노드 기본 구조 |
| **Ethernet Gateway** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/CAPL/VGW.can` | Ethernet↔CAN 변환 게이트웨이 |
| **Ethernet ECU 노드** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/CAPL/ADAS.can` | Ethernet 송수신 노드 패턴 |
| **Ethernet HU 노드** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/CAPL/HU.can` | Head Unit (복합 Ethernet 노드) |
| **Panel 복잡 예제** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/ConceptCar.xvp` | 가장 복잡한 다중 위젯 Panel |
| **Panel 기본 예제** | `canoe/reference/vector_samples_19_4_10/CAN/CANBasic/Panels/Control.xvp` | SwitchControl·TrackBar 기본 |
| **SIL Kit** | `canoe/reference/vector_samples_19_4_10/SIL/SilKitCAN/` | SIL 시뮬레이션 구성 |
| **Python COM API** | `canoe/reference/vector_samples_19_4_10/Python/` | CANoe COM API Python 예제 |
| **DoIP / UDS 진단** | `canoe/reference/vector_samples_19_4_10/Ethernet/Diagnostics/DoIPSystem/Nodes/DoIP_ECU.can` | Ethernet 진단 노드 |
| **CAN 기본 구성** | `canoe/reference/vector_samples_19_4_10/CAN/CANBasic/` | CANBasic 전체 (cfg+dbc+panel+nodes) |

---

### OpenDBC — GitHub 오픈소스 실차 DBC (commaai/opendbc)

```
reference/dbc/level3_communication/reference/
  hyundai_kia_base.dbc      ← 핵심 ⭐ 현대/기아 실차 DBC (ECU 47개, 신호 1325개)
  hyundai_2015_ccan.dbc     ← 2015 C-CAN (113메시지, 1154신호)
  hyundai_2015_mcan.dbc     ← 2015 M-CAN (171메시지, 1184신호)
  hyundai_i30_2014.dbc      ← 2014 i30
  hyundai_santafe_2007.dbc  ← 2007 Santa Fe
  tesla_reference.dbc       ← Tesla 참조
  README.md                 ← 파일별 상세 설명
```

> 출처: [github.com/commaai/opendbc](https://github.com/commaai/opendbc)
> 용도: 실차 신호 네이밍, Value Table, Alive Counter, Checksum 패턴 참조
> **DBC 작성 시 신호 정의·단위·스케일 Best Practice는 이 파일들을 먼저 확인한다.**

---

### 결론: 우리 프로젝트 최우선 레퍼런스 (우선순위 순)

| 용도 | 참조 파일 |
|------|-----------|
| **sysvars 형식** | `docs/LIN-Door/canoe/cfg/sample_project.sysvars` |
| **vsysvar 실사례** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/SysVar/SystemDefSysVar.vsysvar` |
| **DBC 구조·문법** | `docs/LIN-Door/canoe/databases/sample_project.dbc` |
| **DBC 신호 Best Practice** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/` 내 .dbc 파일 또는 hyundai_kia_base.dbc |
| **CAPL 노드 구조** | `docs/LIN-Door/canoe/nodes/*.can` (BCM/Gateway/Tester 등 7개) |
| **CAPL CAN Gateway** | `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Nodes/Gateway.can` |
| **CAPL Ethernet Gateway** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/CAPL/VGW.can` |
| **CAPL Ethernet ECU** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/CAPL/ADAS.can` |
| **Panel 기본** | `canoe/reference/vector_samples_19_4_10/CAN/CANBasic/Panels/Control.xvp` |
| **Panel 고급** | `canoe/reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/ConceptCar.xvp` |
| **DBC 빈 템플릿** | `C:/Users/Public/Documents/Vector/CANoe/19 (x64)/Templates/Database/CANTemplate.dbc` |
| **Python COM 예제** | `canoe/reference/vector_samples_19_4_10/Python/` |

---

## 프로젝트 정체성

> **"SDV 기반 차량 경험(Experience) 플랫폼"**

```
1. Safety (구간 인식) : 스쿨존/고속도로 상황에 맞는 즉각적인 앰비언트/진동 경고
2. V2V 알림 (긴급차량 감지) : 경찰차·구급차 Ethernet 수신 → 앰비언트 즉시 오버라이드
```

> **OTA 완전 제거**: Drive Coach Package, Seasonal Theme Package — 개발 범위에서 제외.
> 이유: 구현 깊이 대비 포트폴리오 가치 낮음 + 벡터 담당자 피드백 반영.

---

## 시스템 아키텍처 (레이어 구조)

```
┌─────────────────────────────────────────┐
│  입력층 (Foundation — A + B)             │
│  A: 속도 스칼라 (과속/급가속/급제동)       │
│  B: 방향 벡터  (차선이탈/급차선변경)       │
│  → 차량 자체 거동 감지 (내부 신호만 사용)  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  판단층 (WDM_ECU — Rule-Based)           │
│  A단독/B단독 → 1단계                     │
│  A+B         → 2단계                    │
│  Emergency 수신 → 앰비언트 오버라이드     │
└──────────┬──────────────┬───────────────┘
           │              │
┌──────────▼───┐  ┌───────▼───────────────┐
│  해제층       │  │  출력층               │
│  응시 감지    │  │  Cluster / Ambient    │
│  핸들 입력    │  │  Sound / IVI          │
└──────────────┘  └───────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  특화층 D (프로젝트 정체성)               │
│                                         │
│  1. Safety (구간 인식 컨텍스트)           │
│  gRoadZone → 경고 조건 + 앰비언트 연동   │
│                                         │
│  2. V2V 긴급차량 알림 + 앰비언트 중재     │
│  Police/Ambulance_ECU                   │
│    → Ethernet 브로드캐스트               │
│    → Civ_ECU 수신                       │
│    → EmergencyType → 앰비언트 우선순위 중재│
│  (gRoadZone 앰비언트와 우선순위 통합)     │
└─────────────────────────────────────────┘
```

---

## 팀 역할

| 팀 | 담당 범위 |
|------|---------|
| **개발팀** | ECU 구현 전반 (CAPL 노드, DBC, 시스템 변수, 시뮬레이터) |
| **문서팀** | 문서 전반 (01~07 workproducts, 요구사항, 설계, 테스트 케이스) |

---

## 개발팀 상세 시나리오 A — 구간 인식 + 앰비언트

### gRoadZone 4단계 정의

| gRoadZone | 구간 | 제한속도 | 특이 동작 |
|-----------|------|---------|---------|
| 0 | 일반도로 | 80km/h | 기본 경고 |
| 1 | 스쿨존 | 30km/h | 과속 시 앰비언트 즉시 RED 점멸 |
| 2 | 고속도로 | 110km/h | 핸들 입력 없으면 바디 진동 경고 |
| 3 | 고속도로 IC/휴게소 근접 | — | 앰비언트 방향 안내 (좌→우 흐름) |

### 구간별 앰비언트 동작

```
스쿨존 (gRoadZone=1) 과속 시:
  Ambient → RED 빠른 점멸 (즉각 경고)

고속도로 (gRoadZone=2) 핸들 미입력 시:
  SteeringInput = 0 + 10초 → Seat_ECU 진동 + Ambient ORANGE 파동

고속도로 IC/휴게소 근접 (gRoadZone=3):
  Ambient → 좌측에서 우측으로 흐르는 방향 애니메이션
  (Mercedes EQS "Navigation by Ambient Light"과 동일 개념)
  운전자가 시각적으로 출구 방향 인지
```

### gRoadZone=3 앰비언트 구현 상세

```
실도로 IC 진출입 유도선 색상 재현:
  한국 고속도로 IC 출구에 표시된 바닥 유도선 색상을 앰비언트로 그대로 재현.
  색상은 고정값(경로 상태/네비 연동 없음):
    초록 — 직진 유지 차선
    분홍 — 전환 구간
    빨강 — 출구 진입 차선

  gNavDirection (Panel sysvar):
    0 = 좌측 진출 → 앰비언트가 좌측으로 흐르는 방향 애니메이션
    1 = 우측 진출 → 앰비언트가 우측으로 흐르는 방향 애니메이션

  앰비언트 우선순위:
    gWarningLevel > 0 → 경고 앰비언트(AMBER/RED) 즉시 오버라이드
    경고 해제 후 → IC 패턴 자동 복귀
    gRoadZone ≠ 3 → 즉시 소거
```

### CANoe 구현 방식

**gRoadZone 주입 방식 — Option A/B 병행 설계**

인터페이스(CAN 신호, sysvar)는 동일. 자극 소스(Stimulus Source)만 교체 가능.

```
Option A (현재 구현 — 발표용):
  Panel 버튼 4개 [일반도로] [스쿨존] [고속도로] [IC출구 근접]
  → sysvar::gRoadZone 직접 설정 → CAN 신호 → WDM_ECU → Ambient_ECU

Option B (고도화 — 선택적):
  Python Navigation Simulator → CANoe COM API
  → sysvar::gRoadZone 자동 설정 → 동일 CAN 신호 흐름
```

**Option B 설계 방향 (Python Grid Map)**:

```python
# 도로 구간을 N×M 행렬로 정의
# 각 셀(x, y) → gRoadZone 값 매핑

zone_map = {
  (0, 0): 0,   # 일반도로 (80km/h)
  (2, 3): 1,   # 스쿨존   (30km/h)
  (5, 1): 2,   # 고속도로 (110km/h)
  (5, 4): 3,   # IC출구 근접
}

# 차량 위치 (x, y) → zone_map 조회 → gRoadZone 결정
# 구간 진입 감지 시 → CANoe COM API로 sysvar 자동 전송
```

구현 포인트:
- 차량 위치는 sysvar::Vehicle::posX, posY (Panel TrackBar 또는 Python 시뮬)
- 구간 경계 진입 = 이전 셀과 다른 gRoadZone 값으로 변경된 순간
- CANoe COM API (`canoe.application.bus.set_variable()`) 로 sysvar 주입
- WDM_ECU 이하 로직 변경 없음 — 인터페이스 동일 보장

문서 처리 원칙:
- `01_Requirements.md`: "gRoadZone 구간 설정 기능" — 방식 언급 안 함 (요구사항 아님)
- `04_SW_Implementation.md`: Option A/B 구조 명시
- CANoe .car / ADASIS v3는 별도 라이선스 필요 → 우리 구현 범위 밖
- Python COM 연동은 CANoe 19 기본 라이선스로 사용 가능

---

## 개발팀 상세 시나리오 B — V2V 긴급차량 알림 + 앰비언트 중재

> **OTA 완전 제거. docs/OTA/ 문서 전면 교체.**

### 프로젝트 한 줄 정의

> 경찰차·구급차가 Ethernet으로 주변 차량에 긴급 상태를 브로드캐스트하면,
> 수신 차량의 앰비언트 라이트가 즉시 해당 긴급 패턴으로 오버라이드된다.
> 긴급 해제 시 gRoadZone 기반 앰비언트로 자동 복귀.

---

### Core 구현 (필수 — 이것만 완성해도 됨)

#### 노드 구성

| 노드 | 역할 | 통신 |
|------|------|------|
| `Police_ECU` | 경찰차. 긴급 출동 버튼 → Ethernet 브로드캐스트 | Ethernet 송신 |
| `Ambulance_ECU` | 구급차. 출동 버튼 → Ethernet 브로드캐스트 | Ethernet 송신 |
| `Civ_ECU` | 일반 수신차. Ethernet 수신 → CAN으로 Ambient_ECU 제어 | Ethernet 수신 → CAN |

#### 통신 메시지 정의

```
EmergencyVehicleMsg (Ethernet, 브로드캐스트):
  byte VehicleType  // 1 = POLICE, 2 = AMBULANCE
  byte Status       // 0 = CLEAR, 1 = ACTIVE
```

#### Civ_ECU 수신 로직

```
on message EmergencyVehicleMsg:
  if Status == ACTIVE:
    gEmergencyType = VehicleType
    → Ambient_ECU: 우선순위 중재 즉시 실행
  if Status == CLEAR:
    gEmergencyType = 0
    → Ambient_ECU: gRoadZone 앰비언트 복귀
```

#### 앰비언트 우선순위 중재 테이블

| 우선순위 | 조건 | 앰비언트 패턴 |
|---------|------|-------------|
| 1 (최고) | gEmergencyType = AMBULANCE (2) | RED / WHITE 교차 점멸 |
| 2 | gEmergencyType = POLICE (1) | RED / BLUE 교차 점멸 |
| 3 | gWarningLevel > 0 | AMBER / RED (기존 경고) |
| 4 (최저) | gRoadZone 기본값 | 구간별 색상 |

**규칙**: 높은 우선순위 조건이 사라지면 → 즉시 다음 우선순위로 자동 강등.
긴급차량 해제 → gWarningLevel 있으면 경고 앰비언트, 없으면 gRoadZone 앰비언트.

#### 시나리오 흐름

```
[Scene 1 — 경찰차 긴급 출동]
  Police_ECU Panel [긴급 출동] 버튼 누름
    → EmergencyVehicleMsg { POLICE, ACTIVE } 브로드캐스트
    → Civ_ECU 수신 → Ambient RED/BLUE 교차 점멸
    → Cluster: "긴급 차량 접근 — 우측 양보" 팝업

[Scene 2 — 긴급 해제]
  Police_ECU Panel [해제] 버튼 누름
    → EmergencyVehicleMsg { POLICE, CLEAR } 브로드캐스트
    → Civ_ECU: gEmergencyType = 0
    → Ambient → gRoadZone 기본 패턴으로 자동 복귀

[Scene 3 — 구급차와 경찰차 동시 접근]
  두 메시지 동시 수신 시 → 우선순위 1 (AMBULANCE) 적용
  구급차 해제 → 우선순위 2 (POLICE) 자동 승격

[Scene 4 — 긴급차량 접근 중 스쿨존 과속]
  gEmergencyType = POLICE + gWarningLevel > 0 동시 발생
  → 우선순위 2 (POLICE 패턴) 유지 — 경고보다 긴급차량이 항상 우선
```

---

### V2V ACK 양방향 확장 — CLAUDE.md에만 정의, 문서화 금지

> **⚠️ 이 섹션은 CLAUDE.md에만 존재한다. docs/OTA/ 문서에 절대 먼저 작성하지 않는다.**
> Core 구현(경찰차·구급차 단방향 + 앰비언트 중재) 완전 완료 후에만 시도한다.
> 구현 성공 시 → docs/OTA/ 해당 섹션에 추가.
> 구현 실패 또는 시간 부족 시 → 이 섹션 그대로 유지, docs에는 없는 것으로 처리.

```
[확장 메시지]
AckMsg (Ethernet, Civ_ECU → Police/Ambulance_ECU):
  byte VehicleID    // 수신차 ID
  byte Status       // 1 = 수신 확인, 2 = 실행 완료

[Lead 노드 추가 로직]
  ackReceived[N] 배열로 수신차 확인 추적
  타임아웃 500ms → 미수신 노드에 재전송 (최대 3회)
  Panel: "차량 A ✓ / 차량 B ✓ / 차량 C ⏳" 표시
```

ACK 구현 완료 시 포트폴리오 표현:
> "요청-응답 프로토콜 직접 설계 — 타임아웃/재전송 로직 포함"

---

## D 선택 근거

**구간 인식(내부 컨텍스트) + V2V 긴급 알림(외부 컨텍스트) = 두 입력이 하나의 앰비언트에서 중재. 확정**

- 구간단속 경고만으로는 기존 양산 기능과 동일 → 앰비언트 방향 안내로 차별화
- OTA 탈락: 구현 깊이가 얕으면 포트폴리오 가치 낮음. 벡터 담당자 피드백 수용.

> **OTA 탈락 이유**: 구현 깊이가 얕으면 포트폴리오 가치 낮음. 깊게 하면 UDS 전체 프로토콜 학습 필요. 벡터 담당자 "수면 밑 기반 내용이 너무 많다" 피드백 수용.

---

## Base Setup (공통 초기화)

**공통 ECU** (개발팀 공유):
- `Vehicle_ECU` — 차속·가속 초기화
- `Cluster_ECU` — 계기판 경고
- `Ambient_ECU` — 앰비언트 라이트
- `Sound_ECU` — 경고음
- `IVI_ECU` — 화면 팝업

**공통 변수**:
```
gVehicleSpeed    = 60 km/h  (정상 주행)
gRoadZone        = 0         (일반도로 80km/h)
gRainMode        = 0         (맑음)
gWarningLevel    = 0         (경고 없음)
gCrashEvent      = 0         (충돌 이벤트 — Level 3 트리거, Panel 버튼)
gEmergencyType   = 0         (긴급차량 없음 / 1=경찰 / 2=구급)
```

**CAN 버스**:
```
CAN-HS 500kbps: WDM_ECU ↔ Cluster / IVI / Ambient / Sound / Door
CAN-LS 125kbps: Accel_ECU / Vehicle_ECU / MDPS_ECU → CGW → WDM_ECU
Ethernet       : Police_ECU / Ambulance_ECU → Civ_ECU (V2V 긴급차량 알림)
```

---

## 미확정 사항

| # | 항목 | 상태 |
|---|------|------|
| 1 | 프로젝트 최종 제목 | ✅ **"SDV 기반 차량 경험(Experience) 플랫폼"** 확정 |
| 2 | WDM_ECU 구현 범위 | ⬜ 개발팀 공동 |
| 3 | 빗길 임계값 하향 수치 | ⬜ 60% vs 80% (Req_B04 하위 예정) |
| 4 | Smart Claim Flask 서버 구현 범위 | ⬜ 로컬 Flask vs 외부 서버 |
| 5 | V2V ACK 양방향 구현 여부 | ⬜ Core 완성 후 시간 여유 시 도전 — 완성 시 문서 추가, 미완성 시 제거 |

---

## docs/OTA 전면 재작성 지시

> **현재 상태**: docs/OTA/ 안의 모든 문서는 OTA(Drive Coach / Seasonal Theme) 기준으로 작성되어 있다.
> **목표**: 경찰차·구급차 V2V 긴급 알림 + 네비게이션 앰비언트 라이팅 시나리오로 전부 교체한다.
> **백업**: docs/OTA_original/ — 절대 수정 금지. 참조 전용.

### 재작성 원칙

1. **파일명·구조 유지**: docs/OTA/ 파일명과 폴더 구조를 그대로 쓴다. 새 파일을 만들지 않는다.
2. **표 형식 유지**: docs/OTA_original/의 테이블 형식(비트 포지션, 메시지 ID 등)을 그대로 가져와 내용만 교체한다.
3. **내용 참조**: 시나리오 개념은 docs/v2x/ 참조. 막히면 docs/V-Model/ 따라 진행.
4. **V2V ACK 문서화 금지**: ACK 양방향은 CLAUDE.md에만 있다. Core 완성 전까지 docs에 쓰지 않는다.

### 재작성 순서 (이 순서 준수)

```
Step 1.  01_Requirements.md     ← 요구사항 재설계 (OTA 요구사항 전부 삭제, 새 시나리오로)
Step 2.  02_Concept_design.md   ← 개념 설계 (아키텍처: 경찰차·구급차 → Civ_ECU → Ambient)
Step 3.  0301_SysFuncAnalysis.md
Step 4.  0302_NWflowDef.md      ← Ethernet 브로드캐스트 + CAN 내부 흐름
Step 5.  0303_Communication_Specification.md  ← EmergencyVehicleMsg 메시지 정의
Step 6.  0304_System_Variables.md             ← gEmergencyType 등 신규 변수
Step 7.  04_SW_Implementation.md              ← CAPL 구현 (Police/Ambulance/Civ ECU)
Step 8.  05_Unit_Test.md
Step 9.  06_Integration_Test.md
Step 10. 07_System_Test.md
```

### 각 Step에서 OTA → 신규 매핑

| OTA 원본 내용 | 교체할 내용 |
|-------------|-----------|
| OTA_ECU, PackageID, UDS 세션 | Police_ECU, Ambulance_ECU, EmergencyType |
| ETH_OTA_Param (Port 6000) | ETH_Emergency_Cmd (신규 포트) |
| CAN_OTA_Applied (0x600) | 삭제 — 기존 Ambient_Control (0x220) 재활용 |
| gGearP 조건 | 삭제 |
| CRC8 검증 | 삭제 |

---

## 문서 작업 가이드

**프로젝트 문서 (문서팀)**: `driving-alert-workproducts/` — 01~07 전체
**V2V 관련 문서 (문서팀)**: `docs/OTA/` — 위 재작성 지시에 따라 순서대로 진행
**원본 백업**: `docs/OTA_original/` — 표 형식·구조 참조용, 수정 금지
**추가 참조**: `docs/v2x/` — V2V 시나리오 개념 텍스트 참조

**재사용 가능 패턴 (docs/sample/canoe/nodes/)**:
- `BCM.can` → variables{}, on start{}, on timer{}, on message{} 구조
- `Gateway.can` → CAN 라우팅 패턴
