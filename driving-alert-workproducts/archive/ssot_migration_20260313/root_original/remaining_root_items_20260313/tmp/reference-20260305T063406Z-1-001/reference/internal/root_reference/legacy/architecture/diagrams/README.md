# 차량 시스템 아키텍처 다이어그램

## 📁 폴더 구조 (4-Level Architecture)

```
diagrams/
├── level1_vehicle_system/      # Level 1: 차량 전체 시스템
├── level2_domain/              # Level 2: 도메인별 상세 (작성 예정)
├── level3_communication/       # Level 3: 통신 구조 (작성 예정)
├── level4_ivi_ecu/            # Level 4: IVI ECU 내부
│   ├── autosar_layers/        # AUTOSAR 계층 구조
│   ├── functional_components/ # 기능별 컴포넌트
│   ├── sequences/             # 시퀀스 다이어그램
│   └── testing/               # 테스트 및 검증
├── docs/                      # 문서
├── puml/archive/              # 이전 버전 (참고용)
└── rendered/                  # 이전 PNG (삭제 예정)
```

---

## 🎯 Level 정의

### Level 1: Vehicle System Architecture
**목적**: 차량 전체 시스템 이해
**파일**: `level1_vehicle_system/01_vehicle_system_architecture.puml`

**내용**:
- 11개 ECU 배치 (Powertrain, Chassis, Body, Infotainment)
- 4개 도메인 구조
- CAN 네트워크 토폴로지 (CAN-HS x2, CAN-LS, Ethernet)
- Central Gateway 아키텍처

**대상**: 경영진, 시스템 엔지니어, 멘토

---

### Level 2: Domain Architecture (작성 예정)
**목적**: 각 도메인 내 ECU 협업 구조
**파일**: `level2_domain/`

**작성 예정**:
- `02_powertrain_domain.puml` - EMS, TCU 상세
- `03_chassis_domain.puml` - ESP, MDPS 상세
- `04_body_domain.puml` - BCM 상세
- `05_infotainment_adas_domain.puml` - IVI, Cluster, ADAS 상세

**대상**: 도메인 아키텍트, 통합 엔지니어

---

### Level 3: Communication Architecture (작성 예정)
**목적**: ECU 간 메시지 흐름 및 CAN DB
**파일**: `level3_communication/`

**현재**:
- `08_can_signal_matrix.md` ✅ (ADAS 신호 매트릭스)

**작성 예정**:
- `06_can_network_topology.puml` - CAN 네트워크 구조
- `07_message_flow_scenarios.puml` - 통신 시나리오 3개
- `vehicle_system.dbc` - CAN 데이터베이스

**대상**: 통신 엔지니어, 테스트 엔지니어

---

### Level 4: IVI ECU Internal Architecture
**목적**: IVI ECU 내부 AUTOSAR 설계
**폴더**: `level4_ivi_ecu/`

#### 4.1 AUTOSAR Layers
**파일**: `autosar_layers/`
- (작성 예정) `10_ivi_autosar_architecture.puml` - ASW/RTE/BSW 구조

#### 4.2 Functional Components
**파일**: `functional_components/`
- `11_lighting_control.puml` ✅ - 조명 제어 아키텍처
- `12_adas_integration.puml` ✅ - ADAS 통합
- `13_ivi_ui_architecture.puml` ✅ - IVI UI 구조
- `14_safety_system.puml` ✅ - 안전 시스템

#### 4.3 Sequences
**파일**: `sequences/`
- `20_adas_multi_event_sequence.puml` ✅ - ADAS 멀티 이벤트
- `21_ivi_theme_profile_sequence.puml` ✅ - IVI 테마/프로필
- `22_ota_diagnostic_sequence.puml` ✅ - OTA 진단

#### 4.4 Testing
**파일**: `testing/`
- `30_fault_injection.puml` ✅ - Fault Injection 워크플로우

**대상**: 소프트웨어 개발자, IVI 팀

---

## 📊 현재 상태

### ✅ 완료
- [x] Level 1: 차량 시스템 아키텍처 (1개 파일)
- [x] Level 4: IVI ECU 상세 (9개 파일)
- [x] PNG 렌더링 (20+ 파일)
- [x] 문서 정리 (docs 폴더)

### 🚧 작성 예정
- [ ] Level 2: 도메인별 아키텍처 (4개 파일)
- [ ] Level 3: 통신 구조 (3개 파일 + DBC)
- [ ] Level 4: AUTOSAR 계층 (1개 파일)

---

## 🚀 다이어그램 렌더링

### 전체 렌더링
```bash
# Level 1
cd level1_vehicle_system && plantuml -tpng *.puml

# Level 4 - Functional Components
cd level4_ivi_ecu/functional_components && plantuml -tpng *.puml

# Level 4 - Sequences
cd level4_ivi_ecu/sequences && plantuml -tpng *.puml

# Level 4 - Testing
cd level4_ivi_ecu/testing && plantuml -tpng *.puml
```

### 개별 렌더링
```bash
plantuml -tpng [파일명].puml
```

---

## 📖 주요 문서

### Level 1 관련
- `docs/level1_ecu_specification.md` - 11개 ECU 상세 스펙
- `docs/requirements_mapping_guide.md` - 요구사항 매핑 가이드

### Level 4 관련
- `docs/lighting_control_architecture.md` - 조명 제어 설명
- `docs/safety_system_architecture.md` - 안전 시스템 설명
- `docs/ota_diagnostic_sequence.md` - OTA 진단 설명
- `docs/can_communication_stack.md` - CAN 통신 스택
- `docs/fault_injection_workflow.md` - Fault Injection 워크플로우
- `docs/critical_issues_implementation.md` - 주요 이슈 구현 내역

### 기타
- `docs/README.md` - 전체 문서 인덱스
- `docs/USAGE_GUIDE.md` - PlantUML 사용 가이드
- `docs/TROUBLESHOOTING.md` - 문제 해결 가이드

---

## 🎯 프로젝트 목표

### 최종 목표
**"CANoe 기반 차량 분산 시스템 아키텍처 설계 및 통신 검증"**

### 핵심 질문 답변
1. **차량 시스템이란?** → Level 1 다이어그램
2. **통신이 왜 필요한가?** → Level 3 시나리오
3. **CANoe의 역할은?** → 가상 차량 환경 구축

### IVI 개발 흐름
1. **조명 제어** (Level 4) - 기본 CAN 통신
2. **ADAS 통합** (Level 4) - 안전 통신
3. **OTA/진단** (Level 4) - UDS 프로토콜
4. **Fault Injection** (Level 4) - 테스트 검증

---

## 📅 일정

### 2월 11-12일 (Level 2 작성)
- [ ] Powertrain 도메인
- [ ] Chassis 도메인
- [ ] Body 도메인
- [ ] Infotainment/ADAS 도메인

### 2월 12-13일 (Level 3 작성)
- [ ] CAN 네트워크 토폴로지
- [ ] 통신 시나리오 3개
- [ ] DBC 파일 초안

### 2월 13일 (멘토링)
- Level 1-3 발표
- 통신 필요성 설명
- CANoe 역할 설명

---

## 🔗 관련 링크

- **PlantUML 공식**: https://plantuml.com
- **AUTOSAR**: https://www.autosar.org
- **ISO 26262**: 차량 기능 안전 표준
- **OpenDBC**: https://github.com/commaai/opendbc

---

**최종 업데이트**: 2026-02-11
**상태**: Level 1, 4 완료 / Level 2, 3 작성 예정
