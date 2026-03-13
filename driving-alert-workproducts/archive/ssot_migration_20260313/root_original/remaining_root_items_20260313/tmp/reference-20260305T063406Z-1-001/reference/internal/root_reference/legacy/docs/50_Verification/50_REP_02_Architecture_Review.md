# 시스템 아키텍처 검토 리포트

## 📋 검토 개요

**검토 일자**: 2026-02-10
**검토 대상**: IVI vECU 시스템 아키텍처 및 PlantUML 다이어그램
**요구사항 기준**: REQ_IVI_vECU_Requirements.xlsx (총 56개 요구사항)

---

## 🎯 요구사항 분석 요약

### 요구사항 분류

| 카테고리 | 개수 | 주요 내용 |
|---------|------|----------|
| **기능 요구사항** | 28개 | 조명 제어, ADAS 연계, UX 기능 |
| **안전 요구사항** | 11개 | 후진 경고, ADAS 안전, 어린이 보호 |
| **진단/OTA 요구사항** | 9개 | UDS 서비스, OTA 업데이트, 자가진단 |
| **비기능 요구사항** | 8개 | 성능, 안정성, 추적성, 확장성 |

### ASIL 레벨 분포

- **ASIL-D**: 3개 (긴급 제동, 후진 중 도어 개방)
- **ASIL-C**: 4개 (후진 안전 경고, 차선 이탈)
- **ASIL-B**: 16개 (대부분의 안전 기능)
- **ASIL-A**: 1개 (도어 연동 조명)
- **QM**: 32개 (비안전 기능)

---

## ✅ 잘 구성된 부분

### 1. AUTOSAR 아키텍처 구조 ✓

**파일**: `architecture_overview_02.puml`

**장점**:
- AUTOSAR Classic 3계층 구조 명확히 표현 (ASW → RTE → BSW)
- Application Software 컴포넌트가 요구사항과 연계됨
  - `Ambient_Light_Controller` → REQ_IVI_001 (ASIL-B)
  - `Safety_Alert_Manager` → REQ_IVI_002, 007 (ASIL-C/D)
  - `OTA_Update_Agent` → REQ_IVI_013, 015 (ASIL-B)
- BSW 계층에 Communication Stack, Diagnostic Stack, Memory 모듈 포함

### 2. 조명 제어 아키텍처 ✓

**파일**: `lighting_control_architecture_01.puml`

**장점**:
- 4개의 조명 제어 컴포넌트 명확히 분리
  - `Ambient_Light_Controller`: 속도/모드/온도 기반 조명
  - `Dashboard_Lighting_Controller`: 도어/기어 연동
  - `IVI_Sync_Manager`: IVI 색상 동기화
  - `Theme_Manager`: 테마 자동 적용
- 각 컴포넌트에 요구사항 ID 명시 (REQ_IVI_001, 003, 004, 017, 042)
- Port 기반 인터페이스 설계 (portin/portout)
- CAN 신호 매핑 명확 (0x100-0x104, 0x200)

### 3. 안전 시스템 아키텍처 ✓

**파일**: `safety_system_architecture_01.puml`

**장점**:
- 5개의 안전 컴포넌트 구성
  - `Reverse_Safety_Manager` (ASIL-C)
  - `Door_Warning_Logic` (ASIL-D)
  - `Auto_Recovery_Manager` (ASIL-C)
  - `ADAS_Safety_Coordinator` (ASIL-C/D)
  - `Child_Protection_Manager` (ASIL-B)
- ASIL 레벨 명시 및 색상 구분 (#Red, #DarkRed)
- 안전 메커니즘 포함 (FIM, DEM, WdgM)
- Fault Injection Interface 연계

### 4. OTA/진단 시퀀스 ✓

**파일**: `ota_diagnostic_sequence_01.puml`, `ota_diagnostic_sequence_02.puml`

**장점**:
- UDS 0x14 (Clear DTC) 프로토콜 상세 표현
- UDS 0x34 (Request Download) 전체 플로우
- Security Access (0x27) 포함
- 성공/실패 시나리오 분기 처리
- 요구사항 연계 (REQ_IVI_012, 013, 047)

---

## ⚠️ 발견된 이슈 및 개선 권장사항

### 🔴 Critical Issues

#### 1. ADAS 통합 아키텍처 누락

**문제**:
- 요구사항에 ADAS 관련 항목 11개 존재 (REQ_IVI_028-038, 051-053)
  - 차선 이탈 경고 (LDW) - ASIL-C, 응답시간 <80ms
  - 긴급 제동 (AEB) - ASIL-D, 응답시간 <50ms
  - 후측방 경고 (BSD) - ASIL-B, 응답시간 <70ms
  - 다중 ADAS 이벤트 우선순위 처리 - ASIL-B
- `safety_system_architecture_01.puml`에 `ADAS_Safety_Coordinator` 컴포넌트는 있으나:
  - **ADAS 센서 데이터 입력 경로 미정의**
  - **ADAS CAN 메시지 ID 범위 (0x300-0x30F) 언급만 있고 상세 신호 정의 없음**
  - **LDW, AEB, BSD 각각의 처리 로직 분리 없음**

**권장사항**:
```
새로운 다이어그램 필요: adas_integration_architecture.puml
- ADAS 센서 인터페이스 정의
- LDW_Handler, AEB_Handler, BSD_Handler 컴포넌트 분리
- ADAS 이벤트 우선순위 매니저 (Priority_Arbitrator)
- CAN 신호 상세 정의 (0x300: LDW_Status, 0x301: AEB_Event 등)
```

#### 2. IVI 사용자 인터페이스 아키텍처 부재

**문제**:
- 요구사항에 IVI UI 관련 항목 다수 (REQ_IVI_042-050, 056)
  - 모드 선택 시 조명 테마 적용 (응답 <100ms)
  - 운전자 프로필 기반 개인화 (로드 <200ms)
  - 주행 컨텍스트 씬 제어 (전환 <120ms)
  - 사용자 정의 시나리오 편집
  - 이벤트 시뮬레이션 재생 (CANoe 연계)
  - 피드백 로깅 및 태깅
- **현재 다이어그램에 IVI HMI 레이어 구조 없음**
- `architecture_overview_01.puml`에 "IVI HMI Application" 박스만 있고 내부 구조 미정의

**권장사항**:
```
새로운 다이어그램 필요: ivi_ui_architecture.puml
- Theme_Selection_UI
- Profile_Manager_UI
- Scene_Controller_UI
- Scenario_Editor_UI
- Feedback_Logger_UI
- IVI ↔ vECU 통신 인터페이스 상세화
```

#### 3. Fault Injection 시나리오 상세 부족

**문제**:
- 요구사항에 Fault Injection 필요 항목 15개
- `fault_injection_workflow_01.puml`은 일반적인 워크플로우만 표현
- **구체적인 고장 모드별 시나리오 미정의**:
  - CAN 메시지 손실 (Message Drop)
  - 신호 고정 (Stuck-at Fault)
  - 타임아웃 (Timeout)
  - 간헐 고장 (Intermittent)
  - 값 오류 (Value Error)

**권장사항**:
```
각 고장 모드별 시퀀스 다이어그램 추가:
- fault_injection_can_message_drop.puml
- fault_injection_signal_stuck_at.puml
- fault_injection_timeout.puml
- fault_injection_intermittent.puml
```

### 🟡 High Priority Issues

#### 4. OTA 실패 복구 메커니즘 미흡

**문제**:
- REQ_IVI_015: OTA 실패 시 자동 롤백 (복구율 100%, ASIL-C)
- REQ_IVI_014: OTA 후 기능 검증 (성공률 >99%, ASIL-B)
- 현재 `ota_diagnostic_sequence_02.puml`은 정상 다운로드만 표현
- **롤백 메커니즘 시퀀스 없음**
- **업데이트 후 자동 검증 프로세스 없음**

**권장사항**:
```
추가 시퀀스 다이어그램:
- ota_rollback_sequence.puml (전원 차단 시나리오 포함)
- ota_post_update_verification.puml
```

#### 5. 성능 요구사항 검증 구조 부재

**문제**:
- 요구사항에 엄격한 응답시간 명시
  - 긴급 제동: <50ms (ASIL-D)
  - 후진 경고: <300ms (ASIL-C)
  - 차선 이탈: <80ms (ASIL-C)
  - 조명 전환: <500ms (ASIL-B)
- **현재 아키텍처에 타이밍 분석 또는 성능 모니터링 컴포넌트 없음**

**권장사항**:
```
추가 컴포넌트:
- Timing_Monitor (BSW 계층)
- Performance_Logger (진단 목적)
- 타이밍 다이어그램 추가 (timing_analysis.puml)
```

#### 6. 어린이 보호 모드 구현 상세 부족

**문제**:
- REQ_IVI_054: 어린이 보호 모드 (ASIL-B, 응답 <200ms)
  - 후석 탑승 감지
  - 도어 락 + 조명 + 알림 + 환기 통합 관리
  - 시동 OFF 후 실내 모니터링
- `safety_system_architecture_01.puml`에 `Child_Protection_Manager` 있으나:
  - **후석 점유 센서 인터페이스 미정의**
  - **도어 락, 환기 제어 연계 없음**
  - **모니터링 주기 (1초) 구현 방법 불명확**

**권장사항**:
```
상세 다이어그램 추가:
- child_protection_detailed.puml
  - Rear_Occupancy_Sensor 인터페이스
  - Door_Lock_Controller 연계
  - HVAC_Controller 연계
  - Monitoring_Timer (1초 주기)
```

### 🟢 Medium Priority Issues

#### 7. CAN 메시지 ID 할당 불완전

**문제**:
- 다이어그램에서 CAN ID 범위만 언급
  - 0x100-0x104: 차량 신호
  - 0x200-0x20F: 조명 명령
  - 0x300-0x30F: ADAS 이벤트
- **개별 신호별 ID 미할당**
- **메시지 주기, 우선순위 미정의**

**권장사항**:
```
CAN 매트릭스 문서 추가:
- can_signal_matrix.md
  - 각 신호별 ID, 주기, 길이, 바이트 오더
  - 우선순위 (ASIL 레벨 기반)
```

#### 8. 진단 DTC 코드 체계 불명확

**문제**:
- REQ_IVI_011: BDC Fault Injection DTC 생성 (검출 >99%, ASIL-B)
- `safety_system_architecture_01.puml`에 DTC 범위 언급 (0xC00000-0xC0FFFF)
- **개별 고장 모드별 DTC 코드 미할당**
- **DTC 우선순위, 저장 전략 미정의**

**권장사항**:
```
DTC 매핑 문서 추가:
- dtc_code_mapping.md
  - 고장 모드별 DTC 코드
  - 저장 우선순위 (ASIL 기반)
  - Freeze Frame 데이터 정의
```

#### 9. 온도 연동 조명 제어 누락

**문제**:
- REQ_IVI_005: 온도 연동 조명 제어 (오차 <5%, QM)
  - HVAC 온도 정보 수신
  - 구간별 색상 변경
- `lighting_control_architecture_01.puml`에 `Temp_Signal_In` 포트 있으나:
  - **온도 구간 정의 없음**
  - **색상 매핑 테이블 없음**

**권장사항**:
```
상세 로직 추가:
- temperature_lighting_mapping.md
  - 온도 구간 (예: <18°C, 18-22°C, >22°C)
  - 각 구간별 RGB 값
```

#### 10. 주차장 위치 찾기 기능 누락

**문제**:
- REQ_IVI_052: 주차장 위치 찾기 조명 모드 (활성화 <100ms, QM)
  - 헤드/테일 조명 깜빡임
  - 사이드 조명 펄스
- **현재 아키텍처에 해당 기능 없음**

**권장사항**:
```
컴포넌트 추가:
- Vehicle_Locator_Manager (Lighting Control 계층)
- 외부 조명 제어 인터페이스 정의
```

---

## 📊 요구사항 커버리지 분석

### 아키텍처 반영 현황

| 카테고리 | 반영됨 | 부분 반영 | 미반영 | 커버리지 |
|---------|--------|----------|--------|----------|
| 기능 요구사항 (28개) | 15 | 8 | 5 | 82% |
| 안전 요구사항 (11개) | 6 | 3 | 2 | 82% |
| 진단/OTA (9개) | 5 | 2 | 2 | 78% |
| 비기능 (8개) | 2 | 4 | 2 | 75% |
| **전체 (56개)** | **28** | **17** | **11** | **80%** |

### 미반영 요구사항 목록

1. **REQ_IVI_028-038**: ADAS 통합 (11개) - 부분 반영
2. **REQ_IVI_042-050**: IVI UI 기능 (9개) - 미반영
3. **REQ_IVI_052**: 주차장 위치 찾기 - 미반영
4. **REQ_IVI_053**: 기상 조건 인지 UX - 미반영
5. **REQ_IVI_054**: 어린이 보호 모드 - 부분 반영
6. **REQ_IVI_055**: 졸음 방지 알림 - 미반영

---

## 🔧 PlantUML 코드 품질 검토

### 코드 스타일 일관성 ✓

**장점**:
- 모든 파일에 `@startuml` / `@enduml` 태그 사용
- 테마 일관성 (`!theme silver`, `!theme materia-outline`)
- 컴포넌트 스타일 통일 (`skinparam componentStyle uml2`)

### 색상 코딩 ✓

**장점**:
- ASIL 레벨별 색상 구분
  - ASIL-D: #DarkRed
  - ASIL-C: #Red
  - ASIL-B: #Orange, #LightCoral
  - QM: #LightBlue, #LightGreen
- 계층별 색상 구분
  - ASW: #LightBlue
  - BSW: #LightGray
  - Virtual HW: #LightYellow

### 개선 필요 사항

#### 1. 주석 및 문서화 부족

**문제**:
- 일부 다이어그램에 `note` 사용하나 일관성 부족
- 컴포넌트 간 인터페이스 설명 부족

**권장사항**:
```plantuml
' 각 컴포넌트에 책임 명시
note right of Component
    **Responsibility**:
    - 기능 1
    - 기능 2

    **Requirements**:
    - REQ_IVI_XXX

    **ASIL**: B
    **Response Time**: <100ms
end note
```

#### 2. 인터페이스 정의 불명확

**문제**:
- Port 이름이 일반적 (`portin`, `portout`)
- 데이터 타입, 단위 미명시

**권장사항**:
```plantuml
portin "Speed_Signal_In\\n[uint16, km/h, 0-300]" as SPEED_IN
portout "RGB_Command_Out\\n[struct RGB, 0-255]" as RGB_OUT
```

#### 3. 시퀀스 다이어그램 타이밍 정보 부족

**문제**:
- 응답시간 요구사항 있으나 다이어그램에 타이밍 표시 없음

**권장사항**:
```plantuml
A -> B : Request
activate B
B -> B : Process (50ms)
B --> A : Response
deactivate B

note right
    **Total Time**: <80ms
    **Requirement**: REQ_IVI_028
end note
```

---

## 🎯 우선순위별 개선 로드맵

### Phase 1: Critical (1-2주)

1. **ADAS 통합 아키텍처 추가**
   - `adas_integration_architecture.puml` 생성
   - LDW, AEB, BSD 핸들러 정의
   - CAN 신호 상세화

2. **IVI UI 아키텍처 정의**
   - `ivi_ui_architecture.puml` 생성
   - 사용자 인터페이스 컴포넌트 구조화

3. **OTA 롤백 메커니즘**
   - `ota_rollback_sequence.puml` 생성
   - 실패 시나리오 처리

### Phase 2: High Priority (2-3주)

4. **Fault Injection 시나리오 상세화**
   - 고장 모드별 시퀀스 다이어그램 추가

5. **성능 모니터링 구조 추가**
   - Timing Monitor 컴포넌트
   - 타이밍 분석 다이어그램

6. **어린이 보호 모드 상세 설계**
   - 센서 인터페이스 정의
   - 통합 제어 로직

### Phase 3: Medium Priority (3-4주)

7. **CAN 매트릭스 문서화**
8. **DTC 코드 체계 정립**
9. **누락 기능 추가** (주차장 찾기, 기상 조건 UX 등)
10. **PlantUML 코드 품질 개선**

---

## 📝 결론

### 전체 평가

**강점**:
- AUTOSAR 기본 구조 잘 구성됨
- 조명 제어 및 안전 시스템 핵심 기능 반영
- OTA/진단 프로토콜 상세 표현
- 요구사항 연계성 양호 (80% 커버리지)

**약점**:
- ADAS 통합 아키텍처 부족 (11개 요구사항 미반영)
- IVI UI 계층 구조 부재 (9개 요구사항 미반영)
- 성능/타이밍 검증 메커니즘 없음
- 일부 안전 기능 상세 설계 부족

### 최종 권장사항

> **즉시 조치 필요**: ADAS 통합 및 IVI UI 아키텍처 추가
> **단기 개선**: OTA 롤백, Fault Injection 상세화
> **중기 개선**: 성능 모니터링, 문서화 강화

**검토 완료 시점**: 2026-02-10
**다음 검토 예정**: Phase 1 완료 후
