# 다음 작업 분석 및 계획 (2026-02-11)

## 📊 현재 프로젝트 완료 상태

### ✅ 완료된 Phase (Level 1-3)

#### Phase 1: Level 1 - 차량 전체 시스템 아키텍처 ✅
**완료일**: 2026-02-11

**산출물**:
- ✅ `01_vehicle_system_overview.puml` - 47개 ECU 전체 개요 (C4 모델)
- ✅ `02_domain_communication.puml` - 도메인 간 통신 및 네트워크 토폴로지
- ✅ `README.md` - Level 1 문서화 (ECU 분류표, 도메인 스펙)
- ✅ PNG 파일 생성 완료

**주요 성과**:
- 47개 ECU를 7개 도메인으로 분류
- Hyundai/Mobis 표준 준수
- ISO 26262 안전 도메인 분리 (ASIL-D/B/C/QM)
- 3-tier CAN 네트워크 구조 (CAN-HS #1, #2, CAN-LS)

---

#### Phase 2: Level 2 - 도메인별 상세 아키텍처 ✅
**완료일**: 2026-02-11

**산출물**:
- ✅ `level2_powertrain.puml` - 7개 ECU (EMS, TCU, OPI, LPI, FPCM, REA, AAF)
- ✅ `level2_chassis.puml` - 6개 ECU (ESP, ABS, MDPS, SAS, EPB, ECS)
- ✅ `level2_adas.puml` - 7개 ECU (F_CAMERA, BSD_RADAR, SCC, SPAS, AVM, PGS, SNV)
- ✅ `level2_infotainment.puml` - 5개 ECU (IVI, CLU, HUD, TMU, CUBIS) + 앰비언트 라이팅 ⭐
- ✅ `level2_body.puml` - 8개 ECU (BCM, DATC, FATC, AFLS, AHLS, PSB, TPMS, SMK)
- ✅ `level2_safety.puml` - 2개 ECU (ACU, ODS)
- ✅ `level2_gateway.puml` - 1개 ECU (CGW) + 라우팅 규칙
- ✅ `README.md` - Level 2 문서화
- ✅ 7개 PNG 파일 생성 완료

**주요 성과**:
- 도메인별 ECU 내부 구조 상세화
- ECU 간 메시지 플로우 정의
- OpenDBC 메시지 매핑
- PlantUML 문법 오류 수정 (7건)

---

#### Phase 3: Level 3 - 통신 아키텍처 ✅
**완료일**: 2026-02-11

**산출물**:
- ✅ `network_message_flow.puml` - 네트워크 메시지 플로우 다이어그램
- ✅ `signal_flow_ambient_lighting.puml` - 앰비언트 라이팅 시퀀스 다이어그램
- ✅ `can_hs1_messages.md` - CAN-HS #1 메시지 테이블 (~60 messages)
- ✅ `can_hs2_messages.md` - CAN-HS #2 메시지 테이블 (~50 messages)
- ✅ `can_ls_messages.md` - CAN-LS 메시지 테이블 (~36 messages)
- ✅ `signal_definitions.md` - 신호 정의 테이블 (1345 signals)
- ✅ `signal_naming_convention.md` - Hyundai/Mobis 네이밍 표준
- ✅ `gateway_routing_table.md` - Gateway 라우팅 규칙 (50+ rules)
- ✅ `README.md` - Level 3 문서화
- ✅ 2개 PNG 파일 생성 완료

**주요 성과**:
- 149개 메시지 문서화 (146 OpenDBC + 3 프로젝트)
- 1345개 신호 정의 (데이터 타입, 범위, 스케일링)
- 50+ Gateway 라우팅 규칙 (우선순위, 레이턴시, 필터링)
- 앰비언트 라이팅 양방향 통신 (IVI ↔ BCM via Gateway) ⭐

---

## 🎯 다음 작업: Phase 4 및 통합

### 우선순위 분석

| 우선순위 | 작업 | 목적 | 예상 시간 | 중요도 |
|---------|------|------|----------|--------|
| **P0** | 멘토링 준비 (2월 13일) | 프로젝트 방향 검증 | 4시간 | 🔴 Critical |
| **P1** | CANoe 프로젝트 통합 | 실제 시뮬레이션 환경 구축 | 8시간 | 🟠 High |
| **P2** | Level 4: IVI ECU 상세 설계 | ECU 내부 아키텍처 | 6시간 | 🟡 Medium |
| **P3** | DBC 파일 통합 | 완전한 CAN 데이터베이스 | 4시간 | 🟡 Medium |
| **P4** | 테스트 케이스 작성 | 검증 및 품질 보증 | 6시간 | 🟢 Low |

---

## 📋 Phase 4: 상세 작업 계획

### P0: 멘토링 준비 (2월 11-13일) 🔴

#### 목표
2월 13일 멘토링에서 프로젝트 방향성과 완성도를 검증받기

#### 작업 항목

**1. 발표 자료 준비** (2시간)
- [ ] PPT 또는 Markdown 슬라이드 작성
  - 슬라이드 1: 프로젝트 개요 (차량 분산 시스템 아키텍처)
  - 슬라이드 2: Level 1 - 47개 ECU 전체 시스템
  - 슬라이드 3: Level 2 - 도메인별 상세 (7개 다이어그램)
  - 슬라이드 4: Level 3 - 통신 아키텍처 (149 messages, 1345 signals)
  - 슬라이드 5: 프로젝트 특화 기능 (앰비언트 라이팅) ⭐
  - 슬라이드 6: 다음 단계 (CANoe 통합, Level 4)

**2. 핵심 질문 답변 준비** (1시간)
- [ ] Q1: "차량 시스템이란 무엇인가?"
  - **답변**: "차량은 47개의 ECU가 CAN 네트워크로 연결된 분산 시스템입니다. Powertrain, Chassis, ADAS, Body, Infotainment, Safety, Gateway 7개 도메인으로 구성되며, 각 ECU는 독립적인 기능을 수행하지만 차량 전체 서비스를 위해 CAN 메시지로 데이터를 주고받습니다."
  - **시각 자료**: `01_vehicle_system_overview.png`

- [ ] Q2: "통신이 왜 필요한가?"
  - **시나리오 1**: 속도 표시 (EMS → CLU, IVI)
    - EMS가 `EMS16 (0x260)` 메시지로 `Vehicle_Speed` 전송
    - CLU와 IVI가 수신하여 속도계 표시
  - **시나리오 2**: ADAS 경고 (F_CAMERA → IVI)
    - F_CAMERA가 `LDWS_LKAS11 (0x420)` 메시지로 차선 이탈 감지
    - IVI가 수신하여 시각적 경고 표시
  - **시나리오 3**: 앰비언트 라이팅 (IVI ↔ BCM) ⭐
    - IVI가 `IVI_AmbientLight (0x400)` 메시지로 RGB 명령 전송
    - Gateway가 CAN-HS #2 → CAN-LS로 라우팅
    - BCM이 LED 제어 후 `BCM_LightControl (0x520)` 피드백
    - Gateway가 CAN-LS → CAN-HS #2로 라우팅하여 IVI에 표시
  - **시각 자료**: `signal_flow_ambient_lighting.png`

- [ ] Q3: "CANoe의 역할은?"
  - **답변**: "CANoe는 실제 차량 없이 가상 차량 환경을 구축하는 시뮬레이션 도구입니다. 47개 ECU를 CAPL 노드로 구현하고, CAN 메시지 송수신을 검증하며, 통신 오류 및 성능을 테스트할 수 있습니다. 아키텍처 다이어그램에는 포함되지 않으며, 개발 및 테스트 도구로만 사용됩니다."

**3. 데모 시나리오 준비** (1시간)
- [ ] 앰비언트 라이팅 시나리오 시연 준비
  - 사용자가 IVI에서 "SPORT" 테마 선택
  - IVI_AmbientLight (0x400) 메시지 전송 (Red, 80%)
  - Gateway 라우팅 (Rule R011)
  - BCM LED 제어
  - BCM_LightControl (0x520) 피드백
  - Gateway 라우팅 (Rule R021)
  - IVI 화면에 "Ambient Light: SPORT (Red, 80%) ✓ Active" 표시

**4. 프로젝트 통계 정리** (30분)
- [ ] 산출물 통계
  - Level 1: 2개 다이어그램 + 1개 문서
  - Level 2: 7개 다이어그램 + 1개 문서
  - Level 3: 2개 다이어그램 + 6개 문서 + 1개 README
  - 총 11개 PlantUML 다이어그램, 9개 문서
  - 47개 ECU, 149개 메시지, 1345개 신호, 50+ 라우팅 규칙

---

### P1: CANoe 프로젝트 통합 (2월 14-15일) 🟠

#### 목표
Level 1-3 아키텍처를 실제 CANoe 시뮬레이션 환경으로 구현

#### 작업 항목

**1. CANoe 프로젝트 생성** (2시간)
- [ ] 새 CANoe 프로젝트 생성 (`vehicle_system_architecture.cfg`)
- [ ] DBC 파일 임포트
  - `hyundai_kia_base.dbc` (OpenDBC 146 messages)
  - `vehicle_system_custom.dbc` (프로젝트 3 messages)
- [ ] 네트워크 구성
  - CAN-HS #1 (500 kbps)
  - CAN-HS #2 (500 kbps)
  - CAN-LS (125 kbps)

**2. 주요 ECU 노드 구현** (4시간)
- [ ] **EMS (Engine ECU)** - CAPL 노드
  - `EMS16 (0x260)` 메시지 주기 전송 (10ms)
  - Vehicle_Speed, Engine_RPM, Torque 시뮬레이션

- [ ] **IVI (Infotainment)** - CAPL 노드
  - `IVI_AmbientLight (0x400)` 메시지 전송 (100ms)
  - 사용자 입력 시뮬레이션 (테마 선택)

- [ ] **BCM (Body Control Module)** - CAPL 노드
  - `IVI_AmbientLight (0x400)` 메시지 수신
  - LED 제어 로직 시뮬레이션
  - `BCM_LightControl (0x520)` 피드백 전송 (100ms)

- [ ] **Gateway (CGW)** - CAPL 노드
  - 라우팅 규칙 구현 (Rule R011, R021)
  - CAN-HS #2 ↔ CAN-LS 메시지 중계
  - CRC 검증 로직

**3. 시뮬레이션 Panel 구성** (1시간)
- [ ] Control Panel
  - IVI 테마 선택 버튼 (SPORT, COMFORT, ECO, CUSTOM)
  - Brightness 슬라이더 (0-100%)

- [ ] Display Panel
  - 현재 RGB 값 표시
  - BCM 피드백 상태 표시
  - 메시지 송수신 로그

**4. 기본 테스트 시나리오** (1시간)
- [ ] 시나리오 1: 속도 표시
  - EMS가 속도 전송 → CLU 수신 확인

- [ ] 시나리오 2: 앰비언트 라이팅 제어
  - IVI 테마 선택 → BCM LED 제어 → 피드백 확인

- [ ] 시나리오 3: Gateway 라우팅
  - CAN-HS #2 → CAN-LS → CAN-HS #2 메시지 흐름 확인

---

### P2: Level 4 - IVI ECU 상세 설계 (2월 16-17일) 🟡

#### 목표
IVI ECU 내부 AUTOSAR 아키텍처 상세 설계 (선택적)

#### 작업 항목

**1. AUTOSAR 레이어 다이어그램** (3시간)
- [ ] `10_ivi_autosar_architecture.puml` 작성
  - **ASW (Application Software Layer)**
    - Ambient Lighting Manager
    - User Profile Manager
    - ADAS Integration Manager
    - UI Rendering Engine
  - **RTE (Runtime Environment)**
    - Component 간 통신 인터페이스
    - Port 정의 (Sender/Receiver, Client/Server)
  - **BSW (Basic Software Layer)**
    - COM (Communication)
    - CanIf (CAN Interface)
    - CanTp (CAN Transport Protocol)
    - Dcm (Diagnostic Communication Manager)
    - NvM (Non-Volatile Memory Manager)

**2. 기존 다이어그램 통합** (2시간)
- [ ] 기존 작업물 재활용
  - `11_lighting_control.puml` → ASW 레이어 상세
  - `12_adas_integration.puml` → ASW 레이어 상세
  - `13_ivi_ui_architecture.puml` → ASW 레이어 상세
  - `14_safety_system.puml` → ASW 레이어 상세

- [ ] Level 4 README 작성
  - IVI ECU 역할 및 책임
  - AUTOSAR 레이어 설명
  - 주요 소프트웨어 컴포넌트

**3. 상태 머신 다이어그램** (1시간)
- [ ] Ambient Lighting 상태 머신
  - IDLE → THEME_SELECTED → LED_CONTROL → FEEDBACK
  - 에러 상태 처리 (CRC_ERROR, TIMEOUT, LED_FAULT)

---

### P3: DBC 파일 통합 (2월 18일) 🟡

#### 목표
OpenDBC와 프로젝트 DBC를 하나의 통합 DBC 파일로 병합

#### 작업 항목

**1. DBC 파일 병합** (2시간)
- [ ] `vehicle_system_integrated.dbc` 생성
  - `hyundai_kia_base.dbc` (146 messages) 병합
  - `vehicle_system_custom.dbc` (3 messages) 병합
  - 메시지 ID 충돌 확인 및 해결

**2. DBC 검증** (1시간)
- [ ] CANdb++ 에디터로 열기
- [ ] 네트워크 노드 확인 (47 ECUs)
- [ ] 메시지 정의 확인 (149 messages)
- [ ] 신호 정의 확인 (1345 signals)
- [ ] 문법 오류 확인

**3. CANoe 프로젝트 업데이트** (1시간)
- [ ] 통합 DBC 파일 임포트
- [ ] 기존 시뮬레이션 재테스트
- [ ] 메시지 송수신 확인

---

### P4: 테스트 케이스 작성 (2월 19-20일) 🟢

#### 목표
통신 검증 및 품질 보증을 위한 테스트 케이스 작성

#### 작업 항목

**1. 기능 테스트** (2시간)
- [ ] TC001: 속도 표시 테스트
  - EMS가 `EMS16 (0x260)` 전송
  - CLU, IVI가 수신 확인
  - 속도 값 정확성 검증 (0-300 km/h)

- [ ] TC002: 앰비언트 라이팅 제어 테스트
  - IVI가 `IVI_AmbientLight (0x400)` 전송
  - Gateway 라우팅 확인
  - BCM LED 제어 확인
  - BCM 피드백 수신 확인

- [ ] TC003: Gateway 라우팅 테스트
  - 50+ 라우팅 규칙 검증
  - 우선순위별 메시지 처리 확인
  - 레이턴시 측정 (<1ms, <2ms, <5ms)

**2. 오류 주입 테스트** (2시간)
- [ ] TC004: CRC 오류 테스트
  - 잘못된 CRC 값 전송
  - Gateway가 메시지 폐기 확인

- [ ] TC005: AliveCounter 타임아웃 테스트
  - AliveCounter 증가 중단
  - BCM이 타임아웃 감지 (3x cycle time)
  - 마지막 유효 값 사용 확인

- [ ] TC006: LED 드라이버 오류 테스트
  - LED 드라이버 고장 시뮬레이션
  - BCM이 `BCM_LightControl` 오류 플래그 설정
  - IVI가 오류 메시지 표시

**3. 성능 테스트** (2시간)
- [ ] TC007: 버스 로드 측정
  - CAN-HS #1: 목표 <60%, 실제 측정
  - CAN-HS #2: 목표 <50%, 실제 측정
  - CAN-LS: 목표 <40%, 실제 측정

- [ ] TC008: 메시지 손실률 측정
  - 목표: <0.01%
  - 1000개 메시지 전송 후 손실 확인

- [ ] TC009: Gateway 라우팅 레이턴시 측정
  - High Priority: 목표 <1ms
  - Medium Priority: 목표 <2ms
  - Low Priority: 목표 <5ms

---

## 📅 타임라인

### Week 7 (2월 11-13일)
**목표**: 멘토링 준비 및 방향성 검증

| 날짜 | 작업 | 시간 | 우선순위 |
|------|------|------|---------|
| 2월 11일 (화) | 발표 자료 준비 | 2시간 | P0 |
| 2월 11일 (화) | 핵심 질문 답변 준비 | 1시간 | P0 |
| 2월 12일 (수) | 데모 시나리오 준비 | 1시간 | P0 |
| 2월 12일 (수) | 프로젝트 통계 정리 | 30분 | P0 |
| 2월 13일 (목) | **멘토링** | - | - |

### Week 8 (2월 14-20일)
**목표**: CANoe 통합 및 Level 4 설계

| 날짜 | 작업 | 시간 | 우선순위 |
|------|------|------|---------|
| 2월 14일 (금) | CANoe 프로젝트 생성 | 2시간 | P1 |
| 2월 14일 (금) | 주요 ECU 노드 구현 (1/2) | 2시간 | P1 |
| 2월 15일 (토) | 주요 ECU 노드 구현 (2/2) | 2시간 | P1 |
| 2월 15일 (토) | 시뮬레이션 Panel 구성 | 1시간 | P1 |
| 2월 15일 (토) | 기본 테스트 시나리오 | 1시간 | P1 |
| 2월 16일 (일) | AUTOSAR 레이어 다이어그램 | 3시간 | P2 |
| 2월 17일 (월) | 기존 다이어그램 통합 | 2시간 | P2 |
| 2월 17일 (월) | 상태 머신 다이어그램 | 1시간 | P2 |
| 2월 18일 (화) | DBC 파일 통합 | 4시간 | P3 |
| 2월 19일 (수) | 기능 테스트 작성 | 2시간 | P4 |
| 2월 19일 (수) | 오류 주입 테스트 작성 | 2시간 | P4 |
| 2월 20일 (목) | 성능 테스트 작성 | 2시간 | P4 |

---

## 🎯 성공 지표

### 멘토링 (2월 13일)
- [ ] "차량 시스템이란?" 질문에 명확히 답변 (47 ECU, 7 도메인)
- [ ] 통신 필요성을 3가지 시나리오로 설명 (속도, ADAS, 앰비언트)
- [ ] Level 1-3 다이어그램 제시 및 설명
- [ ] 프로젝트 방향성 검증 완료

### CANoe 통합 (2월 15일)
- [ ] CANoe 프로젝트 생성 완료
- [ ] 주요 ECU 4개 이상 구현 (EMS, IVI, BCM, Gateway)
- [ ] 앰비언트 라이팅 시나리오 시뮬레이션 성공
- [ ] 메시지 송수신 확인

### Level 4 설계 (2월 17일)
- [ ] IVI ECU AUTOSAR 아키텍처 다이어그램 완성
- [ ] 기존 다이어그램 통합 완료
- [ ] 상태 머신 다이어그램 작성

### 테스트 (2월 20일)
- [ ] 기능 테스트 3개 이상 작성
- [ ] 오류 주입 테스트 3개 이상 작성
- [ ] 성능 테스트 3개 이상 작성
- [ ] 모든 테스트 통과

---

## 💡 핵심 포인트

### 멘토링 대비
1. **차량 시스템 이해 강조**
   - 단일 ECU가 아닌 47개 ECU의 분산 시스템
   - 도메인별 역할 및 책임 명확화
   - CAN 통신의 필요성 실제 사례로 설명

2. **프로젝트 특화 기능**
   - 앰비언트 라이팅 양방향 통신 ⭐
   - Gateway 라우팅 규칙 (Rule R011, R021)
   - 실시간 피드백 메커니즘

3. **V-사이클 프로세스 경험**
   - 요구사항 → 시스템 설계 (Level 1-3) → 상세 설계 (Level 4) → 구현 (CANoe) → 테스트

### CANoe 통합
1. **실제 시뮬레이션 환경**
   - 아키텍처를 실제 동작하는 시스템으로 구현
   - 메시지 흐름 시각화
   - 통신 오류 및 성능 검증

2. **점진적 구현**
   - 주요 ECU 4개부터 시작 (EMS, IVI, BCM, Gateway)
   - 기본 시나리오 검증 후 확장
   - 복잡도 관리

### Level 4 설계
1. **선택적 상세화**
   - IVI ECU만 AUTOSAR 레이어 상세 설계
   - 기존 작업물 최대한 재활용
   - 프로젝트 후반부 작업

---

## 📊 프로젝트 전체 통계 (예상)

### 산출물
- **다이어그램**: 13개 PlantUML (Level 1: 2, Level 2: 7, Level 3: 2, Level 4: 2)
- **문서**: 11개 Markdown (Level 1-4 README, 메시지/신호 테이블, 라우팅 규칙)
- **DBC 파일**: 1개 통합 DBC (149 messages, 1345 signals)
- **CANoe 프로젝트**: 1개 (4+ ECU 노드, 3+ 시나리오)
- **테스트 케이스**: 9개 이상 (기능 3, 오류 3, 성능 3)

### 커버리지
- **ECU**: 47개 (Level 1-2)
- **메시지**: 149개 (Level 3)
- **신호**: 1345개 (Level 3)
- **라우팅 규칙**: 50+ (Level 3)
- **시뮬레이션 ECU**: 4+ (CANoe)

---

## 🚀 즉시 실행 항목 (오늘 - 2월 11일)

### 멘토링 준비 (P0)
- [ ] PPT 슬라이드 6장 작성 (2시간)
- [ ] 핵심 질문 답변 정리 (1시간)
- [ ] 앰비언트 라이팅 시나리오 리허설 (30분)

### 선택 사항
- [ ] CANoe 프로젝트 생성 시작 (멘토링 후 진행 권장)
- [ ] DBC 파일 병합 준비 (멘토링 후 진행 권장)

---

**마지막 업데이트**: 2026-02-11
**다음 마일스톤**: 2026-02-13 멘토링
**프로젝트 완료 예정**: 2026-02-20
