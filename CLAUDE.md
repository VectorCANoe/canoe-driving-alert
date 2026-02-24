# CLAUDE.md — Mobis PBL 프로젝트 컨텍스트

> Claude Code가 매 세션 시작 시 자동으로 읽습니다.

---

## 프로젝트 기본 정보

- **저장소**: `/Users/juns/code/work/mobis/PBL` (git: `main` 브랜치)
- **개발 환경**: CANoe 17+, CAPL, dSPACE SCALEXIO HIL
- **참조용 sample 프로젝트**: `docs/sample/` — BCM 과전류 → DTC → OTA (완료된 예제)
- **새 프로젝트 문서**: `docs/project/` — sample 구조 그대로 미러링

---

## 프로젝트 정체성

> **"SDV 기반 차량 경험(Experience) 플랫폼 (3종 HMI/FoD 세트)"**

```
1. Safety (구간 인식) : 스쿨존/고속도로 상황에 맞는 즉각적인 앰비언트/진동 경고
2. FoD (초보자 코치) : 위험 운전 지속 시 'Drive Coach' 패키지 제안 및 OTA 다운로드
3. Personalization   : 크리스마스 등 특정 테마 OTA 다운로드 및 차량 HMI 일괄 동기화
```

비즈니스 모델 근거: 기아 EV9 라이팅 패턴 판매, BMW FOD(Feature on Demand) 등
양산차에서 가장 수익성이 좋고 현실적인 'UI/UX 및 테마 업데이트' 기반.

OTA 현실성 원칙:
- **불가**: 조향/제동 등 차량 제어권 강제 개입 (기능안전 ISO 26262 리스크), 차량이 자율적으로 OTA결정 (UNECE WP.29, ISO 26262 위반)
- **가능**: HMI(앰비언트, 음성, 클러스터 UI) 경험을 OTA로 다운로드하여 즉각적인 차량 분위기 전환

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
│  + OTA 조건  → 3단계 (성현 D 발동)       │
└──────────┬──────────────┬───────────────┘
           │              │
┌──────────▼───┐  ┌───────▼───────────────┐
│  해제층       │  │  출력층               │
│  라엘: 응시   │  │  Cluster / Ambient    │
│  현준: 핸들   │  │  Sound / IVI          │
└──────────────┘  └───────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  특화층 D — 준영 + 성현 (프로젝트 정체성) │
│                                         │
│  [준영] 1. Safety (구간 인식 컨텍스트)     │
│  gRoadZone → 경고 조건 + 앰비언트 연동   │
│                                         │
│  [성현] 2. FoD / 3. Personalization     │
│  위험 누적 → Drive Coach 패키지 제안      │
│  이벤트 기간 → 시즌 테마 패키지 제안        │
│  운전자 선택 → UDS 세션 → HMI 패키지 적용 │
└─────────────────────────────────────────┘
```

---

## 팀원 역할 확정

| 팀원 | 레이어 | 역할 | 핵심 구현 |
|------|--------|------|---------|
| **준영** | 특화층 D | 구간 인식 + 앰비언트 연동 | `gRoadZone` 4단계 + 구간별 경고·조명 패턴 |
| **택천** | 입력층 (A) | 급가속 감지 | `gAccelValue` > 3.5 m/s² A그룹 플래그 설정 |
| **라엘** | 해제층 | 응시 복귀 감지 | `sysvar::Driver::GazeActive` 0→1 → Level 3 해제 |
| **현준** | 해제층 | 핸들 입력 감지 | MDPS_ECU 조향 입력 0/1 → Level 3 해제 |
| **현준2** | 특화층 D | Smart Claim Python/Flask | Python COM API → Flask 보험사 서버 HTTP POST |
| **성현** | 특화층 D | OTA FoD/테마 구독 서비스 | UDS 0x10→0x27→0x34→0x36×N→0x37 (Drive Coach + Seasonal Theme) |

**WDM_ECU (판단층)**: 팀 전체 공동 구현 또는 준영(팀장) 담당 — 미확정

---

## 준영 상세 시나리오 (구간 인식 + 앰비언트)

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

## 성현 상세 시나리오 (OTA 구독 서비스)

### 제품명 확정

> **1. Drive Coach Package** (초보자 맞춤 운전 코치)
> **2. Seasonal Theme Package** (시즌별 차량 테마 - 예: 크리스마스 테마)

### 비즈니스 모델 (개발 관점)

> "제어권을 뺏는 위험한 OTA"가 아닌, 소비자가 원할 때 즉각적인 만족감을 주는 "HMI 경험 구독(FoD)" 모델.
> 기아 EV9 라이팅 패턴 판매, 벤츠 빛과 소리 테마 플랫폼 등 실제 양산차 비즈니스 흐름 완벽 반영.

```
[FoD 1: Drive Coach Package — 초보자 주행 보조 (Tesla/BMW Valet Mode 대응)]
  P 기어 정차 중 IVI 구독 메뉴 → [Drive Coach 설치] 선택 → 동의 → OTA 다운로드
  적용 후 (안전 파라미터 활성화):
    · LDW 경고 민감도 상향 (차선이탈 더 빠르게 감지·경고)
    · 급가속 토크 제한 (최대 토크 70%)
    · 최고 속도 리미터 (100 km/h)
    · 후진 속도 제한 (10 km/h)

[FoD 2: Seasonal Theme Package — 개인화 및 감성 만족]
  P 기어 정차 중 IVI 알림 (OTA 서버 패키지 가용) → 동의 → OTA 다운로드
  적용 후 (차량 분위기 전환):
    · 앰비언트 라이트가 시즌 테마(봄/여름/가을/겨울)로 색상 동기화
    · 시동 사운드 및 IVI 배경 테마 변경
```

### OTA 공통 조건

```
P 기어(gGearP = 1) 상태에서만 UDS 세션 허용
→ 주행 중 OTA 불가 (UNECE WP.29 준수)
→ 기어 변경 감지 시 세션 즉시 중단
```

### OTA UDS 세션 흐름

```
UDS 0x10 (Programming Session)
  → 0x27 (Security Access)
  → 0x34 (Request Download)
  → 0x36 × N (Transfer Data)
  → 0x37 (Transfer Exit)
  → ECU Restart → 새 파라미터 적용
```

---

## D 선택 근거

| 후보 | 탈락/확정 이유 |
|------|-------------|
| 준영 단독 | 구간단속 경고만으로는 기존 양산 기능과 동일 → 앰비언트 방향 안내로 차별화 후 확정 |
| **준영 + 성현** | **구간 인식(컨텍스트) + OTA 구독(비즈니스) = 현재 양산차에 없는 조합. 확정** |
| 택천 | 급가속 감지(A그룹 플래그)만 담당. 누적 카운팅 제거. 플랫폼 기여 역할. |
| 라엘 | 해제층. D 아님 |
| 현준 | 해제층 + 기존 LKA. D 아님 |
| 현준2 | 기존 BSD 기능 재구현. 출력층으로 전환 |

---

## Base Setup (공통 초기화)

**공통 ECU** (모든 팀원 공유):
- `Vehicle_ECU` — 차속·가속 초기화
- `Cluster_ECU` — 계기판 경고
- `Ambient_ECU` — 앰비언트 라이트
- `Sound_ECU` — 경고음
- `IVI_ECU` — 화면 팝업

**공통 변수**:
```
gVehicleSpeed  = 60 km/h  (정상 주행)
gRoadZone      = 0         (일반도로 80km/h)
gRainMode      = 0         (맑음)
gWarningLevel  = 0         (경고 없음)
gCrashEvent    = 0         (충돌 이벤트 — Level 3 트리거, Panel 버튼)
```

**CAN 버스**:
```
CAN-HS 500kbps: WDM_ECU ↔ Cluster / IVI / Ambient / Sound / Door
CAN-LS 125kbps: Accel_ECU / Vehicle_ECU / MDPS_ECU → CGW → WDM_ECU
Ethernet DoIP : OTA_Server ↔ WDM_ECU (성현 OTA 세션)
```

---

## 미확정 사항

| # | 항목 | 상태 |
|---|------|------|
| 1 | 프로젝트 최종 제목 | ✅ **"SDV 기반 차량 경험(Experience) 플랫폼"** 확정 |
| 2 | WDM_ECU 담당자 | ⬜ 준영 단독 vs 공동 |
| 3 | 빗길 임계값 하향 수치 | ⬜ 60% vs 80% (Req_B04 하위 예정) |
| 4 | Smart Claim Flask 서버 구현 범위 | ⬜ 현준2 담당 — 로컬 Flask vs 외부 서버 |

---

## 문서 작업 가이드

**새 프로젝트 문서 위치**: `docs/project/`
**템플릿 참조**: `docs/sample/` 파일 구조·표 형식 그대로 복사
**문서 순서**:
```
01_Requirements.md          ← 요구사항 (내일 시작)
02_Concept_design.md        ← 개념 설계
02_Make_Diagrams.drawio     ← 아키텍처 다이어그램
0301_SysFuncAnalysis.md     ← 기능 분석
0302_NWflowDef.md           ← 네트워크 흐름
0303_Communication_Specification.md
0304_System_Variables.md
05_Unit_Test.md
06_Integration_Test.md
07_System_Test.md
```

**재사용 가능 패턴 (docs/sample/canoe/nodes/)**:
- `BCM.can` → variables{}, on start{}, on timer{}, on message{} 구조
- `Gateway.can` → CAN 라우팅 패턴
- `OTA_Server.can` → UDS 세션 흐름 전체
