# Item Definition (아이템 정의)

**Document ID**: PART3-00-ITEM
**ISO 26262 Reference**: Part 3, Clause 5
**ASPICE Reference**: N/A
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Released

---

## 1. 문서 목적 (Purpose)

본 문서는 **ISO 26262-3:2018 Part 3, Clause 5**에 따라 **Item의 정의 및 범위**를 명확히 하고, 개발 대상 시스템의 경계(Boundary)와 상호작용(Interaction)을 규정합니다.

---

## 2. Item 정의 (Item Definition)

### 2.1 Item 명칭

**IVI vECU Integrated Control System**
(가상 ECU 기반 차량 통합 제어 시스템)

### 2.2 Item 설명

본 Item은 **In-Vehicle Infotainment (IVI) 시스템**과 연동하여 차량의 **조명, 경고, ADAS UI, 진단** 기능을 통합 제어하는 **가상 ECU (vECU)** 기반 소프트웨어 시스템입니다.

**핵심 기능**:
- 주행 모드 및 속도에 따른 **Ambient 조명 자동 제어**
- 후진, 도어 개방 등 안전 상황 시 **시각적/청각적 경고**
- ADAS 센서 데이터 기반 **운전자 경고 UI 제공**
- **UDS 진단** 및 **OTA 업데이트** 지원

### 2.3 Item 범위 (Scope)

#### 포함 (In Scope):
1. **vECU (IVI vECU)** - 가상 ECU 소프트웨어
2. **CAN 통신 인터페이스** - 5개 Domain ECU와의 메시지 교환
3. **조명 제어 로직** - Ambient LED 제어 알고리즘
4. **경고 제어 로직** - 안전 경고 우선순위 관리
5. **ADAS UI 연동** - LDW, AEB, BSD 이벤트 처리
6. **진단/OTA 기능** - UDS 프로토콜 구현

#### 제외 (Out of Scope):
1. **IVI Hardware** - 디스플레이 하드웨어 (별도 Tier-1)
2. **Lighting Hardware** - Ambient LED 하드웨어 (BCM 담당)
3. **ADAS Sensor** - Camera, Radar 하드웨어 (ADAS Domain)
4. **CAN Gateway** - 물리적 Gateway ECU (별도 공급사)
5. **Powertrain ECU** - EMS, TCU (기존 시스템)

---

## 3. Item의 기능 (Functions of the Item)

### 3.1 주요 기능 목록

| Function ID | Function Name | Description | ASIL |
|-------------|---------------|-------------|------|
| **F-01** | Ambient Lighting Control | 주행 모드/속도 기반 조명 색상 자동 제어 | ASIL-B |
| **F-02** | Safety Warning Display | 후진, 도어 개방 등 안전 경고 UI 표시 | ASIL-C |
| **F-03** | ADAS UI Integration | LDW, AEB, BSD 이벤트 시각적 경고 | ASIL-D |
| **F-04** | User Profile Management | 운전자별 조명/경고 설정 저장 | QM |
| **F-05** | Diagnostic Services | UDS 0x14, 0x19 진단 서비스 | ASIL-B |
| **F-06** | OTA Update | UDS 0x34/0x36/0x37 OTA 업데이트 | ASIL-C |
| **F-07** | Fault Detection & Handling | CAN 통신 오류, 센서 고장 감지 | ASIL-B |

### 3.2 기능 우선순위

**안전 기능 우선순위** (높음 → 낮음):
1. **F-03** (ADAS UI) - ASIL-D - 충돌 경고 최우선
2. **F-02** (Safety Warning) - ASIL-C - 안전 경고
3. **F-06** (OTA Update) - ASIL-C - 시스템 복구
4. **F-01** (Lighting Control) - ASIL-B - 편의 기능
5. **F-05** (Diagnostic) - ASIL-B - 유지보수
6. **F-07** (Fault Handling) - ASIL-B - 안전 전환
7. **F-04** (User Profile) - QM - 사용자 편의

---

## 4. Item의 경계 및 인터페이스 (Boundary & Interfaces)

### 4.1 시스템 경계 (System Boundary)

```
┌─────────────────────────────────────────────────────────────┐
│                    Vehicle System                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            IVI vECU (Item)                           │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │ Lighting    │  │ Safety       │  │ ADAS UI    │  │   │
│  │  │ Control     │  │ Warning      │  │ Integration│  │   │
│  │  │ Logic       │  │ Manager      │  │ Module     │  │   │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │ Diagnostic  │  │ OTA Update   │  │ CAN Driver │  │   │
│  │  │ Services    │  │ Manager      │  │            │  │   │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│           ▲                                                  │
│           │ CAN Bus (500 kbps)                               │
│  ┌────────┴─────────────────────────────────────────────┐   │
│  │  ECU Interfaces (Out of Scope)                       │   │
│  │  • IVI Control ECU   • Cluster ECU                   │   │
│  │  • BCM               • ADAS Sensors                  │   │
│  │  • TCU               • EMS                           │   │
│  │  • Central Gateway                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 외부 인터페이스 (External Interfaces)

| Interface ID | Interface Name | Type | Protocol | ASIL | Direction |
|--------------|----------------|------|----------|------|-----------|
| **IF-01** | IVI_CAN_TX | CAN 2.0B | CAN (500 kbps) | ASIL-B | vECU → BCM |
| **IF-02** | IVI_CAN_RX | CAN 2.0B | CAN (500 kbps) | ASIL-B | IVI → vECU |
| **IF-03** | ADAS_CAN_RX | CAN 2.0B | CAN (500 kbps) | ASIL-D | Camera/Radar → vECU |
| **IF-04** | Powertrain_CAN_RX | CAN 2.0B | CAN (500 kbps) | ASIL-C | TCU/EMS → vECU |
| **IF-05** | Diagnostic_CAN | CAN 2.0B | UDS (ISO 14229) | ASIL-B | Tester ↔ vECU |

### 4.3 사용자 인터페이스 (User Interface)

| UI ID | UI Element | Type | User Action |
|-------|------------|------|-------------|
| **UI-01** | IVI Touchscreen | Input | 모드 선택, 색상 선택 |
| **UI-02** | Cluster Display | Output | 경고 아이콘, 메시지 표시 |
| **UI-03** | Ambient LED | Output | 색상, 밝기 제어 |
| **UI-04** | Warning Sound | Output | 청각 경고 출력 |

---

## 5. 운영 환경 (Operating Environment)

### 5.1 물리적 환경 (Physical Environment)

| 항목 | 값 | 기준 |
|------|-----|------|
| **동작 온도** | -40°C ~ +85°C | ISO 16750-4 |
| **보관 온도** | -40°C ~ +105°C | ISO 16750-4 |
| **상대 습도** | 5% ~ 95% (비응축) | ISO 16750-4 |
| **진동** | 10~2000 Hz | ISO 16750-3 |
| **전원 전압** | 9V ~ 16V (공칭 12V) | ISO 16750-2 |

### 5.2 전자기 환경 (EMC Environment)

| 항목 | 기준 |
|------|------|
| **EMC 적합성** | ISO 11452 (내성), ISO 11451 (방사) |
| **ESD** | ISO 10605 (±8 kV 접촉 방전) |

### 5.3 소프트웨어 환경

| 항목 | 사양 |
|------|------|
| **개발 환경** | CANoe 16.0 (Vector) |
| **시뮬레이션** | Software-in-the-Loop (SIL) |
| **타겟 플랫폼** | vECU (Virtual ECU) |
| **RTOS** | N/A (시뮬레이션 환경) |
| **컴파일러** | N/A (CANoe CAPL) |

---

## 6. 사용 시나리오 (Use Cases)

### 6.1 정상 운영 시나리오 (Normal Use Cases)

#### UC-01: 스포츠 모드 주행
1. 운전자가 IVI에서 **스포츠 모드** 선택
2. vECU가 차량 속도를 실시간 수신
3. 속도 구간에 따라 조명 색상 자동 변경:
   - 0~50 km/h: 녹색
   - 50~100 km/h: 파란색
   - 100+ km/h: 빨간색
4. 색상 변경은 **500ms 이내** 반영

#### UC-02: 후진 시 안전 경고
1. 운전자가 기어를 **R (후진)**으로 변경
2. vECU가 TCU로부터 기어 상태 수신
3. Cluster에 **후진 경고 UI** 표시
4. 시트 조명 자동 점등 (최소 3초 유지)
5. 후방 카메라 장애물 감지 시 **조명 점멸**

#### UC-03: 차선 이탈 경고 (LDW)
1. ADAS Camera가 **LDW 이벤트** 감지
2. vECU가 Camera로부터 CAN 메시지 수신
3. Cluster에 **LDW 경고 아이콘** 표시
4. Ambient 조명을 이탈 방향으로 **점멸**
5. 운전자 조향 조작 시 경고 해제

### 6.2 비정상 시나리오 (Abnormal Use Cases)

#### UC-ERR-01: CAN 통신 오류
1. vECU가 3회 연속 CAN 메시지 수신 실패
2. **Fail-Safe 모드** 진입
3. 조명을 기본 값 (50% 밝기 백색)으로 전환
4. Cluster에 **통신 오류 경고** 표시
5. DTC 코드 저장 (예: P0A00)

#### UC-ERR-02: OTA 업데이트 실패
1. OTA 업데이트 중 **전원 차단** 발생
2. vECU가 Checksum 불일치 감지
3. **자동 Rollback** 실행 → 이전 버전 복구
4. 재부팅 후 정상 기능 복귀
5. DTC 코드 저장 및 로그 기록

---

## 7. 가정 및 제약사항 (Assumptions & Constraints)

### 7.1 가정 (Assumptions)

1. **CAN 버스 가용성**: Central Gateway가 정상 동작하며 CAN 버스 통신이 안정적
2. **전원 공급**: 차량 배터리가 정상 범위 (9V~16V) 유지
3. **센서 신뢰성**: ADAS 센서 (Camera, Radar)의 데이터가 신뢰 가능
4. **시간 동기화**: 모든 ECU의 시간이 ±10ms 이내로 동기화
5. **사전 교정**: Ambient LED 하드웨어가 공장에서 사전 교정 완료

### 7.2 제약사항 (Constraints)

1. **개발 기간**: 4주 (2026-02-05 ~ 2026-03-05)
2. **개발 도구**: CANoe 16.0만 사용 (실차 테스트 불가)
3. **요구사항 개수**: 56개 (고정)
4. **DBC 파일**: Hyundai-Kia Generic DBC 기반
5. **ASIL 적용**: ASIL-D까지 지원 (ISO 26262-6 준수)
6. **메모리**: vECU 메모리 제한 없음 (시뮬레이션)
7. **처리 성능**: 실시간 응답 (<100ms)

---

## 8. 의존성 (Dependencies)

### 8.1 외부 의존성

| Dependency ID | Item | Supplier | Status |
|---------------|------|----------|--------|
| **DEP-01** | Central Gateway ECU | Tier-1 Supplier A | Available |
| **DEP-02** | BCM (Body Control Module) | Tier-1 Supplier B | Available |
| **DEP-03** | ADAS Camera ECU | Tier-1 Supplier C | Available |
| **DEP-04** | Hyundai-Kia Generic DBC | OpenDBC Community | Available |
| **DEP-05** | CANoe 16.0 License | Vector Informatik | Available |

### 8.2 내부 의존성

- **요구사항 명세서**: REQ_IVI_vECU_Requirements.xlsx (56 requirements)
- **시스템 아키텍처**: Domain-based 5 domains, 23 ECUs
- **통신 규격**: CAN 2.0B (500 kbps)

---

## 9. 추적성 (Traceability)

### 9.1 다음 단계 산출물

본 Item Definition은 다음 단계 문서와 연결됩니다:

| 다음 단계 | 문서 | ISO 26262 |
|-----------|------|-----------|
| **HARA** | 00_Hazard_Analysis_Risk_Assessment.md | Part 3-7 |
| **Safety Goals** | 02_Functional_Safety_Concept.md | Part 3-8 |
| **System Requirements** | 01_SYS2_System_Requirements_Specification.md | Part 4-6 |

### 9.2 추적성 매트릭스

| Item Function | Safety Goal | System Requirement |
|---------------|-------------|-------------------|
| F-03 (ADAS UI) | SG-01 (충돌 회피 지원) | SYS-REQ-027~037 |
| F-02 (Safety Warning) | SG-02 (안전 상황 인지) | SYS-REQ-002, 006 |
| F-06 (OTA Update) | SG-03 (시스템 가용성) | SYS-REQ-012~014 |

---

## 10. 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Item Owner** | | | |
| **Functional Safety Manager** | | | |
| **System Architect** | | | |
| **Project Manager** | | | |

---

## 11. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |

---

**Document End**
