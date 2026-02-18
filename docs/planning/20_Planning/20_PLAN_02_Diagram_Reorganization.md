# 아키텍처 다이어그램 Level 기반 재구성 계획

## 📋 현재 상황 분석

### 기존 파일 구조
```
puml/
├── 00_architecture_overview.puml (기존 - 재분류 필요)
├── 01_lighting_control.puml (기존 - Level 4)
├── 01_vehicle_system_architecture.puml (신규 - Level 1) ✅
├── 02_safety_system.puml (기존 - Level 4)
├── 03_ota_diagnostic.puml (기존 - Level 4)
├── 04_fault_injection.puml (기존 - Level 4)
├── 05_can_communication.puml (기존 - Level 3/4)
└── archive/ (29개 파일 - 이전 버전들)

rendered/ (35개 PNG 파일 - 정리 필요)
```

### 문제점
1. ❌ **Level 구분 없음** - 모든 파일이 한 폴더에 혼재
2. ❌ **명명 규칙 불일치** - 번호 기반 vs 기능 기반
3. ❌ **중복 PNG 파일** - rendered 폴더에 35개 PNG (버전별 중복)
4. ❌ **Level 1-2 누락** - 차량 시스템, 도메인 아키텍처 없음

---

## 🎯 Tier-1 OEM Level 정의 (업계 표준)

### ✅ 네, Tier-1도 이렇게 레벨별로 정의합니다!

**실제 사례**:
- **Bosch, Continental, Denso**: 모두 4-5 레벨 아키텍처 사용
- **ISO 26262 (ASIL)**: Level별 안전 분석 요구
- **AUTOSAR**: Layered Architecture (Level 구분 필수)

### Level 정의

#### Level 1: Vehicle System Architecture (차량 전체)
**목적**: 차량 시스템 전체 이해
- ✅ **이미 완성**: `01_vehicle_system_architecture.puml`
- 11개 ECU, 4개 도메인, 네트워크 구조
- **대상**: 경영진, 시스템 엔지니어, 멘토

#### Level 2: Domain Architecture (도메인별 상세)
**목적**: 각 도메인 내 ECU 협업 구조
- ❌ **아직 없음** - 새로 작성 필요
- 4개 파일: Powertrain, Chassis, Body, Infotainment
- **대상**: 도메인 아키텍트, 통합 엔지니어

#### Level 3: Communication Architecture (통신 구조)
**목적**: ECU 간 메시지 흐름 및 CAN DB
- ⚠️ **부분 존재**: `05_can_communication.puml` 활용 가능
- CAN 네트워크 토폴로지, 메시지 시퀀스, DBC 파일
- **대상**: 통신 엔지니어, 테스트 엔지니어

#### Level 4: ECU Internal Architecture (IVI ECU 상세)
**목적**: IVI ECU 내부 AUTOSAR 설계
- ✅ **대부분 존재**: 기존 다이어그램 활용
- ADAS 통합, UI, 조명, 안전, OTA, 진단
- **대상**: 소프트웨어 개발자, IVI 팀

---

## 🗂️ 새로운 폴더 구조 (제안)

```
architecture/system-architecture/diagrams/
│
├── level1_vehicle_system/
│   ├── 01_vehicle_system_architecture.puml ✅
│   └── 01_vehicle_system_architecture.png ✅
│
├── level2_domain/
│   ├── 02_powertrain_domain.puml (신규)
│   ├── 03_chassis_domain.puml (신규)
│   ├── 04_body_domain.puml (신규)
│   └── 05_infotainment_adas_domain.puml (신규)
│
├── level3_communication/
│   ├── 06_can_network_topology.puml (신규)
│   ├── 07_message_flow_scenarios.puml (신규)
│   ├── 08_can_signal_matrix.md (기존 활용)
│   └── vehicle_system.dbc (신규)
│
├── level4_ivi_ecu/
│   ├── autosar_layers/
│   │   └── 10_ivi_autosar_architecture.puml (00_architecture_overview.puml 재작성)
│   │
│   ├── functional_components/
│   │   ├── 11_lighting_control.puml (01_lighting_control.puml 이동)
│   │   ├── 12_adas_integration.puml (archive에서 가져오기)
│   │   ├── 13_ivi_ui_architecture.puml (archive에서 가져오기)
│   │   └── 14_safety_system.puml (02_safety_system.puml 이동)
│   │
│   ├── sequences/
│   │   ├── 20_adas_multi_event_sequence.puml (archive에서 가져오기)
│   │   ├── 21_ivi_theme_profile_sequence.puml (archive에서 가져오기)
│   │   └── 22_ota_diagnostic_sequence.puml (03_ota_diagnostic.puml 이동)
│   │
│   └── testing/
│       └── 30_fault_injection.puml (04_fault_injection.puml 이동)
│
├── archive/ (기존 유지 - 참고용)
│
└── docs/
    ├── level1_ecu_specification.md ✅
    ├── requirements_mapping_guide.md ✅
    └── architecture_overview.md (신규 - 전체 설명)
```

---

## 📊 파일 매핑 계획

### Level 1 (완료 ✅)
| 기존 파일 | 새 위치 | 상태 |
|---------|--------|------|
| 01_vehicle_system_architecture.puml | level1_vehicle_system/ | ✅ 완료 |

### Level 2 (신규 작성 필요)
| 파일명 | 내용 | 우선순위 |
|-------|------|---------|
| 02_powertrain_domain.puml | EMS, TCU 상세 | High |
| 03_chassis_domain.puml | ESP, MDPS 상세 | High |
| 04_body_domain.puml | BCM 상세 | Medium |
| 05_infotainment_adas_domain.puml | IVI, Cluster, ADAS 상세 | High |

### Level 3 (부분 활용 + 신규)
| 기존 파일 | 새 위치 | 작업 |
|---------|--------|------|
| 05_can_communication.puml | level3_communication/06_can_network_topology.puml | 재작성 |
| (신규) | 07_message_flow_scenarios.puml | 3개 시나리오 작성 |
| adas_can_signal_matrix.md | 08_can_signal_matrix.md | 이동 |
| (신규) | vehicle_system.dbc | DBC 파일 작성 |

### Level 4 (기존 활용)
| 기존 파일 | 새 위치 | 작업 |
|---------|--------|------|
| 00_architecture_overview.puml | level4_ivi_ecu/autosar_layers/10_ivi_autosar_architecture.puml | 재작성 |
| 01_lighting_control.puml | level4_ivi_ecu/functional_components/11_lighting_control.puml | 이동 |
| archive/adas_integration_architecture.puml | level4_ivi_ecu/functional_components/12_adas_integration.puml | 이동 |
| archive/ivi_ui_architecture.puml | level4_ivi_ecu/functional_components/13_ivi_ui_architecture.puml | 이동 |
| 02_safety_system.puml | level4_ivi_ecu/functional_components/14_safety_system.puml | 이동 |
| archive/adas_multi_event_sequence.puml | level4_ivi_ecu/sequences/20_adas_multi_event_sequence.puml | 이동 |
| archive/ivi_theme_profile_sequence.puml | level4_ivi_ecu/sequences/21_ivi_theme_profile_sequence.puml | 이동 |
| 03_ota_diagnostic.puml | level4_ivi_ecu/sequences/22_ota_diagnostic_sequence.puml | 이동 |
| 04_fault_injection.puml | level4_ivi_ecu/testing/30_fault_injection.puml | 이동 |

---

## 🎯 명명 규칙

### 파일명 형식
```
[Level번호][순서]_[기능명].puml
```

**예시**:
- Level 1: `01_vehicle_system_architecture.puml`
- Level 2: `02_powertrain_domain.puml`, `03_chassis_domain.puml`
- Level 3: `06_can_network_topology.puml`
- Level 4: `11_lighting_control.puml`, `20_adas_multi_event_sequence.puml`

### PNG 파일 관리
- ✅ **자동 생성**: PlantUML이 `.puml`과 같은 이름으로 생성
- ✅ **위치**: 각 level 폴더 내에 함께 보관
- ❌ **rendered 폴더**: 삭제 (중복 방지)

---

## 🚀 실행 계획

### Phase 1: 폴더 구조 생성 (즉시)
```bash
mkdir -p level1_vehicle_system
mkdir -p level2_domain
mkdir -p level3_communication
mkdir -p level4_ivi_ecu/{autosar_layers,functional_components,sequences,testing}
mkdir -p docs
```

### Phase 2: Level 1 정리 (완료 ✅)
- [x] `01_vehicle_system_architecture.puml` → `level1_vehicle_system/`
- [x] PNG 파일 정리

### Phase 3: Level 4 파일 이동 (우선)
**이유**: 기존 작업물 보존 + IVI 개발 흐름 유지

```bash
# Functional Components
mv 01_lighting_control.puml level4_ivi_ecu/functional_components/11_lighting_control.puml
mv 02_safety_system.puml level4_ivi_ecu/functional_components/14_safety_system.puml

# Sequences
mv 03_ota_diagnostic.puml level4_ivi_ecu/sequences/22_ota_diagnostic_sequence.puml

# Testing
mv 04_fault_injection.puml level4_ivi_ecu/testing/30_fault_injection.puml

# Archive에서 가져오기
cp archive/adas_integration_architecture.puml level4_ivi_ecu/functional_components/12_adas_integration.puml
cp archive/ivi_ui_architecture.puml level4_ivi_ecu/functional_components/13_ivi_ui_architecture.puml
cp archive/adas_multi_event_sequence.puml level4_ivi_ecu/sequences/20_adas_multi_event_sequence.puml
cp archive/ivi_theme_profile_sequence.puml level4_ivi_ecu/sequences/21_ivi_theme_profile_sequence.puml
```

### Phase 4: Level 2 작성 (2월 11-12일)
- [ ] 4개 도메인 다이어그램 작성
- [ ] PNG 렌더링

### Phase 5: Level 3 작성 (2월 12-13일)
- [ ] CAN 네트워크 토폴로지
- [ ] 메시지 흐름 시나리오 3개
- [ ] DBC 파일 초안

### Phase 6: rendered 폴더 정리 (마지막)
```bash
# 모든 PNG가 각 level 폴더에 있으면
rm -rf rendered/
```

---

## ✅ 검증 계획

### 1. 폴더 구조 검증
```bash
tree -L 2 architecture/system-architecture/diagrams/
```
**기대 결과**: 4개 level 폴더 + archive + docs

### 2. PNG 렌더링 검증
```bash
cd level1_vehicle_system && plantuml -tpng *.puml
cd level2_domain && plantuml -tpng *.puml
cd level3_communication && plantuml -tpng *.puml
cd level4_ivi_ecu && find . -name "*.puml" -exec plantuml -tpng {} \;
```
**기대 결과**: 모든 PNG 정상 생성

### 3. 파일 개수 검증
```bash
find . -name "*.puml" | wc -l
find . -name "*.png" | wc -l
```
**기대 결과**: PUML과 PNG 개수 일치

### 4. 요구사항 커버리지 검증
- Level 1: 차량 시스템 이해 ✅
- Level 2: 도메인별 ECU 역할 ✅
- Level 3: 통신 필요성 설명 ✅
- Level 4: IVI 개발 (조명, ADAS, OTA, 진단) ✅

---

## 🎯 최종 목표

### 멘토링 발표 (2월 13일)
- ✅ Level 1: 차량 전체 시스템 (완료)
- ✅ Level 2: 도메인별 상세 (작성 예정)
- ✅ Level 3: 통신 시나리오 3개 (작성 예정)
- ✅ Level 4: IVI ECU 상세 (기존 활용)

### 프로젝트 완료 시
- ✅ 4-Level 아키텍처 완성
- ✅ IVI 개발 흐름 유지 (조명 → ADAS → OTA → 진단)
- ✅ Tier-1 수준 문서화
- ✅ CANoe 가상 차량 환경 구축

---

## 📝 User Review Required

> [!IMPORTANT]
> **폴더 구조 재구성 승인 필요**
>
> 이 계획은 기존 파일들을 Level 기반으로 재구성합니다.
> - 파일 이동 및 이름 변경
> - 새로운 폴더 구조 생성
> - rendered 폴더 삭제 (중복 제거)
>
> **승인 후 진행하시겠습니까?**

---

**작성일**: 2026-02-11
**다음 단계**: 사용자 승인 후 Phase 1-3 실행

---

## 📝 Document Status
**Status**: Released
**Review**: Pending Mentoring Session (2026-02-13)
**Verification**: Artificial Intelligence Assistant
**Last Updated**: 2026-02-11
