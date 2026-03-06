# 새 프로젝트 방향성 및 구조 결정 Q&A
# "운전자 위험 행동 실시간 경고 시스템"

**작성일**: 2026-02-21
**반영 사항**: 멘토 피드백 — Test Suite 구조, Base Setup + 시나리오 독립 운영

> 이 문서는 새 프로젝트 방향 전환 과정에서 결정된 사항과 그 근거를,
> **현업 자동차 SW 개발 표준(ISO 26262 / ASPICE / CANoe / OEM 실무)** 기준으로 정리합니다.

---

## Q1. "Test Suite 구조"가 무엇이고, 왜 대기업 표준인가?

> 멘토님께서 "대기업 표준도 Test Suite 구조"라고 하셨는데, 구체적으로 어떤 의미인가요?

### 현업 답변: CANoe Test Suite = Vector 공식 테스트 프레임워크

**Test Suite**는 CANoe의 공식 검증 구조입니다. 현대모비스, Bosch, Continental, BMW, Stellantis 등
모든 Tier-1/OEM이 ECU 검증에 사용하는 **업계 표준 방식**입니다.

```
[CANoe Test Suite 계층 구조 — 현업 표준]

Test Suite (프로젝트 전체 검증 묶음)
  ├── Test Environment Setup  ← Base Setup (공통 초기화)
  │     차량 초기 상태, 네트워크 초기화, 공통 변수 선언
  │
  ├── Test Group A  ← Scenario A (독립 기능 검증)
  │     Test Case A-1  (Pass/Fail)
  │     Test Case A-2
  │     ...
  │
  ├── Test Group B  ← Scenario B
  │     Test Case B-1
  │     ...
  ├── Test Group C  ← Scenario C
  ├── Test Group D  ← Scenario D
  └── Test Group E  ← Scenario E
```

**현업에서 이 구조를 쓰는 이유:**

| 이유 | 설명 |
|------|------|
| 독립 실행 | Scenario B가 실패해도 C, D, E는 정상 실행 |
| 회귀 테스트 | 코드 수정 후 특정 Scenario만 재실행 가능 |
| 병렬 처리 | 여러 ECU 팀이 각자 Scenario 담당 |
| 추적성 | 요구사항 ↔ Test Case 1:1 매핑 (ASPICE SUP.10) |
| 자동화 보고서 | CANoe가 HTML/XML 테스트 리포트 자동 생성 |

**ASPICE 매핑:**
- `Base Setup` → SWE.4 BP3: 테스트 환경 구축
- `Scenario (Test Group)` → SWE.4 단위 검증 + SWE.5 통합 테스트
- `Test Case Pass/Fail` → SYS.5 시스템 적격성 테스트 증거

---

## Q2. Base Setup (차량 동역학 공통)은 왜 분리하는가?

> 모든 시나리오에 공통으로 차량이 달리는 상황이 필요한데, 이걸 왜 따로 빼야 하나요?

### 현업 답변: 중복 제거 + 일관성 보장 = 테스트 신뢰도 확보

**문제 상황 (Base Setup 없이 각 시나리오에 중복 작성 시):**
```
Scenario A: 차속 60km/h 설정, 기어 D, 네트워크 초기화... (50줄)
Scenario B: 차속 60km/h 설정, 기어 D, 네트워크 초기화... (50줄 반복)
Scenario C: 차속 60km/h 설정, 기어 D, 네트워크 초기화... (50줄 반복)
→ 하나를 수정하면 나머지도 수정해야 함 → 불일치 발생 → 테스트 신뢰도 붕괴
```

**Base Setup으로 분리 시:**
```
Base Setup: 차속 60km/h, 기어 D, 네트워크 초기화 (1번 작성)
Scenario A: Base Setup 호출 → A 전용 조건 추가
Scenario B: Base Setup 호출 → B 전용 조건 추가
→ 수정은 Base Setup 한 곳만
```

**본 프로젝트 Base Setup 구성 요소:**

```
[Base Setup — 차량 동역학 공통]

차량 기본 상태:
  - 기어: D (주행)
  - 초기 차속: 60 km/h (일반도로 정상 주행)
  - 가속페달 개도율: 20% (정상 크루징)
  - 브레이크 압력: 0 bar
  - 조향각: 0° (직선 주행)
  - 도로 제한속도: 80 km/h (기본값)

네트워크 초기화:
  - CAN-HS 500kbps 활성화
  - CAN-LS 125kbps 활성화
  - 모든 ECU 노드 정상 응답 확인

공통 변수 선언:
  - gVehicleSpeed, gAccelPedal, gBrakePressure
  - gSteeringAngle, gSpeedLimit
  - gWarningLevel (0: 정상, 1: 1단계, 2: 2단계, 3: 긴급)
```

---

## Q3. 새 프로젝트 Scenario A–E는 어떻게 구성하는가?

> 팀원들이 제안한 6개 시나리오를 Test Suite 구조에 어떻게 배치하나요?

### 확정 구조 (멘토 피드백 반영 + 팀 합의 방향)

```
Base Setup (차량 동역학 공통)
  ├── Scenario A : 과속 감지 경고           (준영)
  ├── Scenario B : 급가속 감지 + 안전모드   (택천 + 성현 통합)
  ├── Scenario C : 시선/차선 이탈 경고      (라엘 + 현준-1 통합)
  ├── Scenario D : BSD 후방 충돌 도어 잠금  (현준-2)
  └── Scenario E : 복합 위험 통합 경고      (기본 동역학 연계)
```

**각 시나리오 요구사항 5~6개 구성 원칙:**

| 번호 | 요구사항 유형 | 예시 |
|------|------------|------|
| REQ-x01 | 감지 조건 (임계값) | 차속 > 제한속도 시 과속 감지 |
| REQ-x02 | 1단계 경고 정의 | 10% 초과 → Cluster 경고 텍스트 |
| REQ-x03 | 2단계 경고 정의 | 20% 초과 → 경고음 + 계기판 적색 |
| REQ-x04 | 3단계 경고 정의 | 40% 초과 → 긴급 경고 + 감속 권고 |
| REQ-x05 | 해제 조건 | 임계값 이하 복귀 시 경고 해제 |
| REQ-x06 | 타이밍 / 통신 | 경고 발생 ≤ 50ms, CAN ID/주기 |

---

## Q4. CANoe에서 "네비게이션 정보"와 "카메라"를 어떻게 구현하는가?

> 현준님 피드백: "CANoe에서 네비게이션 정보 수신이 가능한지?"
> 준영님 시나리오에 네비 제한속도, 라엘님 시나리오에 전방 카메라가 있는데
> 실제 외부 센서/앱 없이 CANoe만으로 구현이 되나요?

### 현업 답변: CANoe 내부에서 "신호 주입"으로 완전 구현 가능

현업에서도 실제 네비게이션/카메라를 연결하지 않습니다.
**CANoe CAPL 노드가 해당 ECU를 시뮬레이션**합니다.

```
[실제 구현 방법]

1. 네비게이션 시뮬레이션 (Scenario A용)
   → CANoe Panel에 TrackBar/Button 추가
   → 운전자가 슬라이더로 "현재 도로 제한속도" 값 직접 설정
   → CAPL 노드가 CAN 메시지로 제한속도 신호 전송
   → "스쿨존 진입" = 버튼 1개로 30km/h로 즉시 전환

   실제 패널 예시:
   [일반도로 80km/h] [스쿨존 30km/h] [고속도로 110km/h] (버튼 3개)

2. 카메라/시선 이탈 시뮬레이션 (Scenario C용)
   → 실제 카메라 없음 → CANoe System Variable로 대체
   → sysvar::Camera::GazeDetected = 0 (시선 이탈)
   → sysvar::Camera::LaneDeviation = 1 (차선 이탈)
   → CAPL onSysVar 이벤트로 감지 신호 CAN 전송

   현업 용어: "Sensor Abstraction" — 실제 HW 없이 신호 레벨에서 동일 동작 검증

3. 조향각/가속도 시뮬레이션 (Base Setup용)
   → sysvar::Vehicle::SteeringAngle, AccelPedal 직접 제어
   → Panel TrackBar로 테스터가 실시간 조작
```

**핵심 원칙**: CANoe 시뮬레이션에서 "실제 센서"는 **CANoe Panel + CAPL 노드**로 100% 대체 가능.
이것이 **HIL(Hardware-In-the-Loop) 이전 단계인 SIL(Software-In-the-Loop)** 방식이며,
현업에서 ECU 납품 전 사전 검증에 표준으로 사용됩니다.

---

## Q5. 성현님 "OTA 안전모드"는 Scenario B에 어떻게 통합하는가?

> 급가속(택천) + OTA 안전모드(성현)를 하나의 Scenario B로 합칠 때
> 요구사항 5~6개 안에 OTA를 넣을 수 있나요?

### 현업 답변: 감지→경고→안전모드 활성(OTA) 한 흐름으로 연결

OTA를 별도 시나리오로 빼지 않고, Scenario B의 **최종 단계**로 연결하면 자연스럽습니다.

```
[Scenario B: 급가속 감지 + 안전모드 흐름]

REQ-B01: 급가속 감지 조건
          → Accel 개도율 변화율 > 임계값/초 (Gear D 상태)

REQ-B02: 1단계 경고 (즉시)
          → Cluster 경고 + Ambient Light 주황색

REQ-B03: 누적 감지 시 경고 단계 상승
          → 급가속 N회 반복 → 2단계: 경고음 + 적색 점멸

REQ-B04: 안전모드 권장 팝업 (IVI)
          → "급가속 N회 감지 — Level 1 안전모드를 권장합니다"
          → 운전자 선택: [지금 활성화] / [나중에]

REQ-B05: Level 1 안전모드 활성 (동의 시, P기어 상태에서)
          → 토크 제한 0.85 적용
          → Cluster: "Level 1 안전모드 실행 중" 표시

REQ-B06: Level 2 안전모드 OTA 업데이트 (Level 1 적용 후 재발생 시)
          → P기어 활성 시 OTA 업데이트 권장 팝업
          → UDS 0x34/0x36/0x37 프로그래밍 세션 → 토크 0.75 적용
```

**현준님 피드백 반영**: OTA는 반드시 P기어 활성 후 진행 (주행 중 OTA = 안전 위반).
**성현님 설명 반영**: Level 1은 기본 탑재, Level 2는 OTA 동의 후 정책 활성화.

---

## Q6. 새 프로젝트의 ISO 26262 / ASPICE 연결 구조는?

> 주제가 바뀌어도 ISO 26262, HARA, ASIL 적용 방식은 동일한가요?

### 현업 답변: 주제가 바뀌어도 V-Model 구조는 동일. 위험 내용만 바뀜

**새 프로젝트 HARA 핵심 (예상):**

| 위험 ID | 위험 상황 | ASIL | Safety Goal |
|---------|---------|------|------------|
| H-01 | 과속 감지 실패 → 경고 미발생 | ASIL-B | SG-01: 과속 감지 후 50ms 내 경고 |
| H-02 | 급가속 누적 카운트 오류 → 안전모드 미전환 | ASIL-B | SG-02: N회 누적 정확 감지 |
| H-03 | 차선 이탈 감지 실패 → 경고 미발생 | ASIL-B | SG-03: 이탈 감지 후 즉시 경고 |
| H-04 | BSD 후방 감지 오류 → 도어 잠금 실패 | ASIL-B | SG-04: TTC ≤2초 시 도어 잠금 |
| H-05 | 복합 위험 시 경고 우선순위 혼란 | QM | SG-05: 최고 위험 경고 우선 출력 |

**ASIL 최고값: ASIL-B** → sample 프로젝트와 동일 수준, Decomposition 불필요

**V-Model 문서 구조 (구조 그대로, 내용만 교체):**
```
01_Requirements.md         ← 5개 시나리오 × REQ 5-6개 = 총 25~30개 요구사항
02_Concept_design.md       ← 새 시스템 아키텍처 (입출력 ECU 재정의)
0301_SysFuncAnalysis.md    ← 5개 Scenario 기능 분해
0302_NWflowDef.md          ← 위험 감지 → 경고 ECU 신호 흐름 정의
0303_Communication_Spec.md ← 새 CAN 메시지 ID/신호 명세 (DBC 기반)
0304_System_Variables.md   ← CANoe Panel 변수 (속도, 개도율, 조향각 등)
05_Unit_Test.md            ← Scenario별 단위 검증 케이스
06_Integration_Test.md     ← Scenario 간 연동 + 복합 위험 검증
07_System_Test.md          ← E2E 전체 흐름 (Base→A→B→C→D→E)
```

---

## Q7. 새 프로젝트 ECU 구성은 어떻게 되는가?

> 주제가 "운전자 위험 행동 경고"로 바뀌면 어떤 ECU들이 등장하나요?
> sample에서 BCM/CGW/WindowMotor가 핵심이었다면, 새 프로젝트는?

### 확정 ECU 구성 (CANoe 노드로 구현)

```
[입력 ECU — 위험 행동 감지]
  ├── ADAS_ECU        : 차선 이탈, BSD 후방 감지 (Scenario C, D)
  ├── Accel_ECU       : 가속페달 개도율, 급가속 감지 (Scenario B)
  ├── Vehicle_ECU     : 차속, 가속도, 조향각 (Base Setup 전체)
  └── Nav_ECU         : 도로 제한속도 신호 제공 (Scenario A, CANoe Panel 시뮬)

[제어 ECU — 경고 판단 / 중심]
  └── WDM_ECU         : Warning Decision Module — 경고 레벨 판단 및 배분
      (새 프로젝트의 핵심 노드. sample의 BCM 역할)

[출력 ECU — 경고 전달]
  ├── Cluster_ECU     : 계기판 경고 텍스트/아이콘 (모든 Scenario)
  ├── IVI_ECU         : 화면 팝업, 안전모드 UX (Scenario B, C)
  ├── Ambient_ECU     : 앰비언트 라이트 색상 (Scenario A, B, D)
  ├── Sound_ECU       : 경고음 (Scenario A, B, C, D)
  ├── Seat_ECU        : 시트 진동 (Scenario C)
  ├── Door_ECU        : 도어 잠금/지연 (Scenario D)
  └── OTA_Server      : 안전모드 정책 업데이트 (Scenario B)

[게이트웨이]
  └── CGW             : 도메인 간 메시지 라우팅 (sample과 동일 역할)
```

**CAN 버스 구성:**
```
CAN-HS (500kbps): WDM_ECU ↔ Cluster / IVI / Ambient / Sound / Door
CAN-LS (125kbps): ADAS_ECU / Accel_ECU / Vehicle_ECU → CGW → WDM_ECU
Ethernet (DoIP) : OTA_Server ↔ WDM_ECU (Scenario B OTA 세션)
```

---

## Q8. 새 프로젝트를 비전공자에게 한 줄로 설명하면?

### 권장 한 줄 요약

> **"운전자가 과속, 급가속, 차선 이탈, 후방 충돌 위험 등 위험 행동을 하면,
> 차량 내부 통신(CAN)을 통해 단계별 경고가 즉시 발생하고
> 반복 위험 행동 시 OTA로 안전 모드가 자동 업데이트되는 전 과정을
> 가상 환경(CANoe)에서 검증합니다."**

**비전공자 이해 포인트:**
- "과속/급가속" → 누구나 아는 상황
- "단계별 경고" → 1단계(경보) → 2단계(경고음+조명) → 3단계(긴급)
- "OTA 안전 모드" → Tesla/스마트폰 업데이트로 이미 아는 개념
- "CANoe 가상 환경" → 실제 차 없이 안전하게 테스트

---

## 종합 결론: 전환 이후 포지셔닝

| 항목 | 이전 (sample) | 새 프로젝트 | 변경 여부 |
|------|------------|-----------|--------|
| 주제 | BCM 과전류 → DTC → OTA | 운전자 위험 행동 → 다단계 경고 → OTA | 변경 |
| V-Model 구조 | 9개 문서 체계 | 동일 9개 문서 체계 | **유지** |
| Test Suite 구조 | 단일 시나리오 흐름 | Base + Scenario A~E | **강화** |
| 핵심 ECU | BCM / CGW / Cluster | WDM_ECU / CGW / 다수 출력 ECU | 변경 |
| ASIL 최고값 | ASIL-B | ASIL-B (예상) | 유지 |
| CANoe 구현 방식 | CAPL 노드 시뮬레이션 | 동일 (Panel + CAPL) | **유지** |
| 가시적 결과물 | CAN 트레이스 + 테스트 리포트 | 동일 + 다감각 경고 Panel | 강화 |
| 발표 임팩트 | "창문 모터 고장" (기술적) | "운전자 안전" (직관적) | **강화** |

> **핵심 메시지**: 구조와 프로세스는 그대로입니다. 주제가 "운전자 안전"으로 바뀌면서
> 비전공자 심사위원에게 더 직관적이고, 팀원 각자의 아이디어가 독립 시나리오로
> 온전히 살아나는 구조가 됩니다.

---

## 다음 작업 순서

1. **시나리오 A~E 최종 확정** — 팀 합의 (이번 주 완료)
2. **sample 프로젝트 복제** → 새 폴더 생성
3. **내용 전체 삭제** (표 구조/섹션 헤더만 유지)
4. **Base Setup 정의** → 01_Requirements.md 시작
5. **DBC 신규 정의** → 새 CAN 메시지 ID 체계
6. **CAPL 노드 개발** → WDM_ECU.can 중심
