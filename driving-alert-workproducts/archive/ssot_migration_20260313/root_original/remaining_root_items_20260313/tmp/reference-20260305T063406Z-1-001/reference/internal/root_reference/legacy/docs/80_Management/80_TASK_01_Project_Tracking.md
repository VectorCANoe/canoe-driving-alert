# 차량 시스템 아키텍처 프로젝트 - Task List

## 📋 프로젝트 개요
**주제**: CANoe 기반 차량 분산 시스템 아키텍처 설계 및 통신 검증
**기간**: 2026년 2월 10일 ~ 2월 13일 (멘토링)
**목표**: 차량 전체 시스템 이해 + IVI ECU 개발 + CANoe 가상 환경

---

## ✅ Week 6: 프로젝트 방향 재정립 (2월 10일) - 완료

### [x] Phase 1: 멘토 피드백 분석 및 방향 전환
- [x] 핵심 피드백 분석
  - ✅ "IVI ECU 하나만 보지 말고 차량 전체 시스템 이해"
  - ✅ "ECU 간 통신이 왜 필요한지 설명"
  - ✅ "CANoe는 가상 차량 환경 구축 도구"
- [x] 프로젝트 재정의
  - ✅ `mentoring/Mentoring_01_Project_Definition.md` 작성 (1페이지 요약)
  - ✅ `mentoring/Mentoring_05_Project_Direction_Pivot.md` 작성 (상세 분석)
  - ✅ `mentoring/Mentoring_02_Next_Steps_Analysis.md` 작성 (3페이지 분석)
- [x] 핵심 질문 정리
  - ✅ Q1: 차량 시스템이란? → Level 1 다이어그램
  - ✅ Q2: 통신이 왜 필요한가? → Level 3 시나리오
  - ✅ Q3: CANoe의 역할은? → 가상 환경 구축

**완료일**: 2026-02-10

---

## ✅ Week 6: 연구 및 분석 (2월 10일) - 완료

### [x] Phase 1: OpenDBC 실제 차량 분석
- [x] Tesla CAN DB 분석 (`tesla_can.dbc`)
  - ✅ 15+ ECU 식별 (DI, EPAS, ESP, GTW 등)
  - ✅ CAN 메시지 구조 분석
  - ✅ 신호 정의 추출
- [x] Hyundai/Kia CAN DB 분석 (`hyundai_kia_generic.dbc`)
  - ✅ 20+ ECU 식별 (EMS, TCU, MDPS, BCM, IVI 등)
  - ✅ 도메인별 ECU 분류
  - ✅ CAN ID 할당 전략 파악
- [x] 분석 문서 작성
  - ✅ `50_Verification/50_REP_01_OpenDBC_Analysis.md` (400+ 라인)

**완료일**: 2026-02-10

---

## ✅ Week 6: 다이어그램 재구성 (2월 11일) - 완료

### [x] Phase 1: Level 기반 폴더 구조 생성
- [x] 4-Level 아키텍처 계획 수립
  - ✅ `20_Planning/20_PLAN_02_Diagram_Reorganization.md` 작성
  - ✅ Tier-1 OEM Best Practice 반영
- [x] 폴더 구조 생성
  - ✅ `level1_vehicle_system/`
  - ✅ `level2_domain/`
  - ✅ `level3_communication/`
  - ✅ `level4_ivi_ecu/` (4개 하위 폴더)
  - ✅ `docs/`

### [x] Phase 2: 기존 파일 재배치
- [x] Level 1 파일 이동
  - ✅ `01_vehicle_system_architecture.puml` → `level1_vehicle_system/`
  - ✅ PNG 파일 이동
- [x] Level 4 파일 이동 (9개 파일)
  - ✅ Functional Components (4개): 조명, ADAS, IVI UI, 안전
  - ✅ Sequences (3개): ADAS 이벤트, IVI 테마, OTA 진단
  - ✅ Testing (1개): Fault Injection
- [x] 문서 파일 정리
  - ✅ `level1_ecu_specification.md` → `docs/`
  - ✅ `requirements_mapping_guide.md` → `docs/`
  - ✅ `08_can_signal_matrix.md` → `level3_communication/`

### [x] Phase 3: PNG 렌더링 및 검증
- [x] 전체 다이어그램 렌더링
  - ✅ Level 1: 1개 PNG
  - ✅ Level 4: 20+ PNG
- [x] README 작성
  - ✅ `diagrams/README.md` (전체 구조 설명)

**완료일**: 2026-02-11
**파일 수**: PUML 10개, PNG 20+개

---

## 🚧 Week 6-7: 시스템 아키텍처 작성 (2월 11-12일)

### [x] Level 1: 차량 전체 시스템 아키텍처 ✅
**목표**: 차량을 구성하는 모든 ECU와 네트워크 구조 표현

**완료 내용**:
- [x] 4개 도메인 박스 (Powertrain, Chassis, Body, Infotainment)
- [x] 11개 ECU 배치
  - Powertrain: EMS, TCU
  - Chassis: ESP, MDPS
  - Body: BCM
  - Infotainment: IVI, Cluster, Camera, Radar, SCC
  - Gateway: CGW
- [x] CAN 네트워크 연결
  - CAN-HS #1 (500 kbps) - Powertrain + Chassis
  - CAN-HS #2 (500 kbps) - Infotainment + ADAS
  - CAN-LS (125 kbps) - Body
  - Ethernet - Gateway ↔ IVI
  - Telematics - Gateway ↔ OTA Server
- [x] Gateway ECU 중계 구조
- [x] 외부 OTA 서버 연결
- [x] ASIL 레벨 색상 구분
- [x] CAN ID 범위 할당 (도메인별)

**완료 파일**:
- ✅ `level1_vehicle_system/01_vehicle_system_architecture.puml`
- ✅ `level1_vehicle_system/01_vehicle_system_architecture.png`
- ✅ `docs/level1_ecu_specification.md` (11개 ECU 상세 스펙)

**완료일**: 2026-02-11

---

### [x] Level 2: 도메인별 상세 아키텍처 ✅
**목표**: 각 도메인 내 ECU 구성 및 역할 상세화

**작성 예정**:
- [x] Powertrain 도메인 (`02_powertrain_domain.puml`)
  - EMS (Engine Management System)
  - TCU (Transmission Control Unit)
  - 엔진/변속기 제어 신호
  - CAN-HS #1 연결

- [x] Chassis 도메인 (`03_chassis_domain.puml`)
  - ESP (Electronic Stability Program)
  - MDPS (Motor Driven Power Steering)
  - 제동/조향 제어 신호
  - CAN-HS #1 연결

- [x] Body 도메인 (`04_body_domain.puml`)
  - BCM (Body Control Module)
  - 도어, 조명, 와이퍼 제어
  - CAN-LS 연결

- [x] Infotainment/ADAS 도메인 (`05_infotainment_adas_domain.puml`)
  - IVI (In-Vehicle Infotainment)
  - Cluster (Instrument Cluster)
  - Camera, Radar, SCC (ADAS 센서)
  - CAN-HS #2 + Ethernet 연결

**주의사항**:
- ✅ 각 도메인 내 ECU 간 협업 표현
- ✅ Gateway를 통한 도메인 간 통신 표시
- ❌ ECU 내부 구조는 표시하지 않음 (Level 4에서 다룸)

**완료일**: 2026-02-11

---

### [x] Level 3: 통신 구조 및 시나리오 ✅
**목표**: ECU 간 통신 필요성 설명 (멘토 질문 대응)

**완료 내용**:
- [x] **OpenDBC 통합** (Level 1 표준 우선 전략) ⭐
  - ✅ `hyundai_kia_base.dbc` (1676 lines, 47 ECU, 146 messages, 1325 signals)
  - ✅ OpenDBC 실차 검증 데이터 활용
  - ✅ Hyundai/Mobis 산업 표준 준수
  - ✅ 15개 Value Tables (Best Practice 패턴)

- [x] **프로젝트 특화 DBC** (`vehicle_system_custom.dbc`) ⭐
  - ✅ 130 lines, 4 ECU (IVI, BCM, CLU, CGW)
  - ✅ 3개 메시지 (앰비언트 라이팅 전용)
  - ✅ 20개 신호 (완전한 RGB 제어)
  - ✅ 4개 Value Tables (Enum 정의)
  - ✅ 포괄적 주석 (모든 신호 설명)

- [x] **ECU 네이밍 전략**
  - ✅ Hyundai/Mobis 산업 표준 준수
  - ✅ ESP, CLU, F_CAMERA, IVI, BSD_RADAR
  - ✅ `[위치]_[기능]_[타입]` 컨벤션

- [x] **통합 결과**
  - ✅ 총 1806 lines (OpenDBC 1676 + Custom 130)
  - ✅ 49 ECU, 149 messages, 1345 signals
  - ✅ 19 Value Tables
  - ✅ 실차 검증 + 신규 기능 개발

- [x] **포트폴리오 어필**
  - ✅ "Hyundai Level 1 실차 DBC 기반 vECU 개발"
  - ✅ OEM/Tier1 호환 구조
  - ✅ 산업 표준 ECU 네이밍
  - ✅ ISO 26262 Best Practice 적용

**작성 예정** (선택):
- [ ] CAN 네트워크 토폴로지 (`06_can_network_topology.puml`)
  - 물리적 네트워크 구조
  - CAN-HS #1, #2, CAN-LS 분리 이유
  - Gateway 라우팅 규칙

- [ ] 통신 시나리오 다이어그램 (`07_message_flow_scenarios.puml`)
  - 시퀀스 다이어그램으로 시간 흐름 표현
  - 3가지 시나리오 시각화 (OpenDBC + Custom)

## Phase 2: Level 2 Domain-Specific Architecture ✅ COMPLETE
- [x] Create Powertrain domain diagram (7 ECU)
- [x] Create Chassis domain diagram (6 ECU)
- [x] Create ADAS domain diagram (7 ECU)
- [x] Create Infotainment domain diagram (5 ECU)
- [x] Create Body domain diagram (8 ECU)
- [x] Create Safety domain diagram (2 ECU)
- [x] Create Gateway architecture diagram (1 ECU)
- [x] Fix PlantUML syntax errors (7 fixes)
- [x] Generate PNG files for all domains (7 PNG files)
- [x] Create Level 2 README.md

**완료일**: 2026-02-11

---

## Phase 3: Level 3 Communication Architecture ✅ COMPLETE
- [x] Create CAN message specification tables
  - [x] CAN-HS #1 message table (~60 messages)
  - [x] CAN-HS #2 message table (~50 messages)
  - [x] CAN-LS message table (~36 messages)
- [x] Create signal definition tables
  - [x] Signal naming convention (Hyundai/Mobis)
  - [x] Signal definitions (1345 signals)
  - [x] Data types, ranges, scaling, units
- [x] Create gateway routing table
  - [x] 50+ routing rules
  - [x] Priority levels and latency requirements
  - [x] Ambient lighting bidirectional routing ⭐
- [x] Create Level 3 README.md

**완료일**: 2026-02-11

---

**목표**: IVI ECU 내부 AUTOSAR 설계 (기존 작업 활용)

**완료 내용**:
- [x] Functional Components (4개)
  - ✅ `11_lighting_control.puml` - 조명 제어
  - ✅ `12_adas_integration.puml` - ADAS 통합
  - ✅ `13_ivi_ui_architecture.puml` - IVI UI
  - ✅ `14_safety_system.puml` - 안전 시스템

- [x] Sequences (3개)
  - ✅ `20_adas_multi_event_sequence.puml` - ADAS 멀티 이벤트
  - ✅ `21_ivi_theme_profile_sequence.puml` - IVI 테마/프로필
  - ✅ `22_ota_diagnostic_sequence.puml` - OTA 진단

- [x] Testing (1개)
  - ✅ `30_fault_injection.puml` - Fault Injection

**작성 예정**:
- [ ] AUTOSAR Layers (`10_ivi_autosar_architecture.puml`)
  - ASW (Application Software)
  - RTE (Runtime Environment)
  - BSW (Basic Software)

**완료일**: 2026-02-11 (재구성)

---

### [x] Level 1-4: DBC 기반 아키텍처 재정의 (신규) 🔥
**목표**: OpenDBC 기반 프로덕션급 아키텍처 재구성 (Tier1 BP 벤치마킹)

**전략**:
- ✅ DBC 기반 설계 (47 ECU, 1325 signals)
- ✅ Hyundai/Mobis 표준 준수
- ✅ ISO 26262 도메인 분류
- ✅ AUTOSAR 아키텍처 패턴

#### [x] Phase 1: Level 1 재정의 (완료) ⭐
**목표**: 47개 ECU 도메인별 분류 및 전체 시스템 개요

**완료 내용**:
- [x] 도메인 분류 (7개 도메인)
  - ✅ Powertrain (7 ECU): EMS, TCU, OPI, LPI, FPCM, REA, AAF
  - ✅ Chassis (6 ECU): ESP, ABS, MDPS, SAS, EPB, ECS
  - ✅ ADAS (7 ECU): F_CAMERA, BSD_RADAR, SCC, SPAS, AVM, PGS, SNV
  - ✅ Body (8 ECU): BCM, DATC, FATC, AFLS, AHLS, PSB, TPMS, SMK
  - ✅ Infotainment (5 ECU): IVI, CLU, HUD, TMU, CUBIS
  - ✅ Safety (2 ECU): ACU, ODS
  - ✅ Gateway (1 ECU): CGW
  - ✅ Others (11 ECU): LVR, EVP, DI_BOX, _4WD, MTS, AEMC, IAP, 등

- [x] PlantUML 다이어그램 작성
  - ✅ `01_vehicle_system_overview.puml` (C4 모델, 47 ECU 전체 개요)
  - ✅ `02_domain_communication.puml` (도메인 간 통신, 네트워크 토폴로지)
  - ✅ PNG 생성 완료

- [x] Tier1 BP 벤치마킹
  - ✅ Hyundai/Mobis 도메인 분류 표준
  - ✅ ISO 26262 안전 도메인 분리 (ASIL-D, B, C, QM)
  - ✅ AUTOSAR 아키텍처 패턴 (Gateway 중심)
  - ✅ 네트워크 분리 (CAN-HS #1, #2, CAN-LS)

- [x] 문서화
  - ✅ `README.md` (도메인 상세 스펙, 47 ECU 분류표)

**완료일**: 2026-02-11

## 🎯 Week 7: 멘토링 준비 (2월 13일)

### [ ] Phase 1: 발표 자료 준비
- [ ] Level 1 다이어그램 설명 준비
  - 11개 ECU 역할 설명
  - 4개 도메인 구조 설명
  - Gateway 역할 설명

- [ ] Level 3 시나리오 설명 준비
  - 통신 필요성 3가지 사례
  - 실제 사용자 경험 연결

- [ ] 핵심 질문 답변 준비
  - Q1: 차량 시스템이란?
  - Q2: 통신이 왜 필요한가?
  - Q3: CANoe의 역할은?

### [ ] Phase 2: 데모 준비 (선택)
- [ ] CANoe 환경 설정
- [ ] 간단한 시뮬레이션 준비

---

## 📊 진행 상황 요약

### ✅ 완료 (2월 10-11일)
- [x] 프로젝트 방향 재정립
- [x] OpenDBC 실제 차량 분석
- [x] 다이어그램 재구성 (4-Level)
- [x] Level 1 차량 시스템 아키텍처
- [x] Level 4 IVI ECU 아키텍처 (재구성)

### 🚧 진행 중 (2월 11-12일)
- [ ] Level 2 도메인별 아키텍처 (4개)
- [ ] Level 3 통신 구조 (3개 + DBC)

### 📅 예정 (2월 13일)
- [ ] 멘토링 발표 준비
- [ ] 핵심 질문 답변 연습

---

## 🎯 성공 지표

### Level 1
- [x] 11개 ECU 정의 완료
- [x] 4개 도메인 구조 완료
- [x] CAN 네트워크 토폴로지 완료
- [x] ECU 상세 스펙 문서 완료

### Level 2
- [x] 4개 도메인 다이어그램 완료
- [x] 도메인별 ECU 협업 표현

### Level 3
- [ ] 3개 통신 시나리오 완료
- [ ] DBC 파일 초안 완료
- [ ] "통신 필요성" 명확히 설명 가능

### Level 4
- [x] 9개 다이어그램 재구성 완료
- [ ] AUTOSAR 계층 다이어그램 완료

### 멘토링
- [ ] 핵심 질문 3개 답변 준비 (mentoring/Mentoring_04_QA_Preparation.md)
- [ ] Level 1-3 발표 자료 준비 (mentoring/Mentoring_03_Presentation_Slides.md)
- [ ] CANoe 역할 설명 준비 (mentoring/Mentoring_04_QA_Preparation.md)

---

**최종 업데이트**: 2026-02-11 16:30 (Tier-1 표준 폴더 구조 반영 완료)
**다음 작업**: 멘토링 데모 시나리오 스크립트 기반 시뮬레이션 환경 구축 (20_Planning/20_PLAN_06_Demo_Scenario.md)
