# Item Definition (아이템 정의)

**Document ID**: PART3-00-ITEM
**ISO 26262 Reference**: Part 3, Clause 5
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: 2026-02-17
**Status**: Released (v2.0 — ASIL pre-assignment removed; mandatory sections added)

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
7. **Central Gateway (CGW)** - 차량 네트워크 라우팅 허브 (**검증 핵심 인프라**: CAN-LS/HS1/HS2 간 메시지 라우팅, Ethernet/DoIP OTA 경로 제공)

#### 제외 (Out of Scope):
1. **IVI Hardware** - 디스플레이 하드웨어 (별도 Tier-1)
2. **Lighting Hardware** - Ambient LED 하드웨어 (BCM 담당)
3. **ADAS Sensor** - Camera, Radar 하드웨어 (ADAS Domain)
4. **Powertrain ECU** - EMS, TCU (기존 시스템, 입력 신호만 수신)
5. **실제 OTA 클라우드 서버** - 물리적 클라우드 서버 (CANoe CAPL 소켓으로 모사)

---

## 3. Item의 기능 (Functions of the Item)

### 3.1 주요 기능 목록

| Function ID | Function Name | Description |
|-------------|---------------|-------------|
| **F-01** | Ambient Lighting Control | 주행 모드/속도 기반 조명 색상 자동 제어 |
| **F-02** | Safety Warning Display | 후진, 도어 개방 등 안전 경고 UI 표시 |
| **F-03** | ADAS UI Integration | LDW, AEB, BSD 이벤트 시각적 경고 |
| **F-04** | User Profile Management | 운전자별 조명/경고 설정 저장 |
| **F-05** | Diagnostic Services | UDS **0x10** (Session Control), **0x14** (Clear DTC), **0x19** (Read DTC) 진단 서비스 |
| **F-06** | OTA Update | UDS **0x10 0x02** (Programming Session), **0x34** (Download), **0x36** (Transfer), **0x37** (Exit) |
| **F-07** | Fault Detection & Handling | CAN 통신 오류, 센서 고장 감지 |

> **Note v2.0**: ASIL은 Item Definition 단계에서 사전 할당할 수 없습니다 (ISO 26262-3:2018, Clause 7).
> ASIL은 HARA 결과로 결정되며, HARA 완료 후 도출된 ASIL 할당 결과는 HARA 문서를 참조하십시오.
> - F-01: ASIL-A (SG-05 기반) | F-02: ASIL-B (SG-03, SG-04 기반) | F-03: ASIL-D (SG-01, SG-02 기반)
> - F-04: QM | F-05: ASIL-B (진단 CAN 경로) | F-06: QM (HARA H-06 QM) | F-07: ASIL-B (SG-06 기반)

### 3.2 기능 우선순위

**안전 기능 우선순위** (높음 → 낮음):
1. **F-03** (ADAS UI) - ASIL-D - 충돌 경고 최우선
2. **F-02** (Safety Warning) - ASIL-C - 안전 경고
3. **F-06** (OTA Update) - QM - 시스템 복구 (HARA: QM)
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


---

## 🔴 핵심 검증 시나리오 — Master E2E Scenario (Red Thread)

> 본 프로젝트의 모든 문서는 아래 시나리오를 중심 실(Red Thread)로 연결됩니다.
> ASPICE SYS.2는 "시나리오 기반 요구사항 도출"을 명시합니다.

```
[Phase 1] Fault Injection (고장 주입)
  BCM (Body Domain, CAN-LS)
    └─ Window Motor Overcurrent 감지 (50A > 정상 5A)
    └─ DTC B1234 저장 (ISO 14229 DTC Format)
    └─ BCM_FaultStatus CAN 메시지 전송 (CAN-LS, 0x500)

[Phase 2] Gateway Routing & Cluster Warning (중앙 게이트웨이 라우팅)
  Central Gateway (CGW)
    └─ CAN-LS 수신 (BCM_FaultStatus 0x500)
    └─ CAN-HS2 라우팅 → vECU (0x500 → CAN-HS2 broadcast)
    └─ Ethernet/DoIP 경로 제공 → OTA 서버 연결 (ISO 13400)
  vECU (CAN-HS2)
    └─ Cluster 경고등 활성화 (Warning Priority: P0)
    └─ DTC 이력 내부 기록

[Phase 3] UDS Diagnostics (진단 통신)
  CANoe Tester (CAPL 기반 진단 노드)
    └─ UDS 0x10 0x03 (Extended Diagnostic Session) → BCM
    └─ UDS 0x19 0x02 (Read DTC by Status Mask) → DTC B1234 수집
    └─ TCP/IP → 가상 OTA 서버 전송 (DTC 데이터 패킷)

[Phase 4] OTA Update (무선 업데이트)
  OTA Server (CANoe 가상 노드, Ethernet)
    └─ SW 버전 분석 → 업데이트 결정
    └─ UDS 0x10 0x02 (Programming Session) → BCM
    └─ UDS 0x34 (Request Download, 64KB)
    └─ UDS 0x36 × N (Transfer Data, 4KB/block)
    └─ UDS 0x37 (Transfer Exit)
    └─ BCM 재시작 → DTC 소거 → 정상 복귀 검증
```

**적용 표준**: ISO 14229-1 UDS, ISO 13400-2 DoIP, ISO 26262-4 (Safety), ASPICE PAM 3.1

---

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

## 5-1. 법적/규제 요구사항 (Legal and Regulatory Requirements)

> **ISO 26262-3:2018 Clause 5.4.2**: Item Definition은 관련 법적 및 규제 요구사항을 포함해야 합니다.

| 규제 ID | 규제/표준 | 적용 항목 | 요구사항 |
|---------|----------|---------|---------|
| **LEG-01** | UNECE Regulation No. 79 (조향 시스템) | MDPS Haptic 경고 | 운전자 입력 없이 조향 개입 제한 |
| **LEG-02** | UNECE Regulation No. 157 (ALKS) | ADAS UI | 자율주행 중 운전자 모니터링 인터페이스 |
| **LEG-03** | ISO 15765-4 (CAN 진단) | UDS 진단 서비스 | OBD-II CAN 프레임 규격 준수 |
| **LEG-04** | ISO 14229-1:2020 (UDS) | OTA, 진단 | UDS 서비스 구현 (0x14, 0x19, 0x34 등) |
| **LEG-05** | GDPR / 개인정보보호법 | User Profile | 운전자 프로파일 데이터 암호화 및 삭제 기능 |
| **LEG-06** | ISO 26262:2018 (Functional Safety) | 전체 안전 기능 | ASIL-D까지 지원 |
| **LEG-07** | ASPICE PAM 3.1 | 개발 프로세스 | SYS.2~5, SWE.1~6 프로세스 준수 |

---

## 5-2. 운영 모드 (Operating Modes)

> **ISO 26262-3:2018 Clause 5.4.3**: Item의 운영 모드를 명시해야 합니다.

| 모드 ID | 모드 이름 | 설명 | 가용 기능 | ASIL 최대 |
|---------|---------|------|---------|---------|
| **OM-01** | Normal Operation | 정상 주행 | 전체 기능 | ASIL-D |
| **OM-02** | Degraded Operation | 부분 고장 (CAN 오류 등) | Fail-Safe 기능만 | ASIL-B |
| **OM-03** | Fail-Safe State | 심각 고장 | 최소 안전 출력만 | ASIL-B |
| **OM-04** | Diagnostic Mode | 정차 + 진단기 연결 | UDS 서비스, OTA | ASIL-B |
| **OM-05** | OTA Update Mode | 정차 중 소프트웨어 업데이트 | OTA만 (안전 기능 비활성) | QM |
| **OM-06** | Power Off / Sleep | 시동 OFF | 없음 (WakeUp 감지만) | N/A |

---

## 5-3. 선행 지식 기반 알려진 위험 (Known Hazardous Situations)

> **ISO 26262-3:2018 Clause 5.4.3**: 선행 개발 경험 및 관련 시스템에서 알려진 위험 상황을 포함해야 합니다.

| KH ID | 알려진 위험 | 출처 | 관련 안전 조치 |
|-------|-----------|------|------------|
| **KH-01** | CAN 버퍼 오버플로로 인한 안전 메시지 손실 | 유사 IVI 프로젝트 Field Report | E2E 보호, 메시지 우선순위 |
| **KH-02** | ADAS 이벤트 동시 발생 시 UI 혼란 (정보 과부하) | 운전 행동 연구 (NHTSA 보고서) | 우선순위 기반 단일 경고 표시 |
| **KH-03** | OTA 중 전원 차단으로 인한 Brick (벽돌화) | OEM Field Return Data | Rollback 메커니즘, A/B 파티션 |
| **KH-04** | 소프트웨어 무한루프로 인한 경고 미표시 | ISO 26262-6 사례 연구 | Watchdog Timer |
| **KH-05** | 조명 PWM 오류로 야간 눈부심 | 조명 ECU 리콜 사례 | 하드웨어 PWM 리미터 |
| **KH-06** | CAN 메시지 재생 공격 (Replay Attack) | 차량 사이버보안 연구 | Alive Counter 검증 |

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
3. **요구사항 개수**: 55개 (SRS 기준; Item Definition 원안 56개에서 중복 1개 제거)
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


---

## 12. 산업 아키텍처 맥락 (Industry Architecture Context)

| 단계 | 아키텍처 | 특징 | 상태 |
|------|---------|------|------|
| 과거 | 분산 Domain ECU | 도메인별 독립 CAN 버스 | Legacy |
| **현재 (본 프로젝트)** | **Central Gateway 중심** | **CGW가 모든 도메인 중재, OTA/Diagnostics 허브** | **✅ 적용** |
| 미래 | Zonal Controller 기반 | 차량을 물리적 Zone으로 나눠 Zonal ECU가 국소 제어 | SDV 방향 |

> **본 프로젝트는 Central Gateway 중심 아키텍처**를 채택합니다.
> Gateway가 CAN-LS (BCM), CAN-HS2 (vECU), Ethernet (OTA Server) 를 연결하는
> 통합 진단/OTA 허브 역할을 수행하며, 이는 Zonal 전환 준비 단계에서도 동일하게 활용됩니다.

## 11. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |
| 2.0 | 2026-02-17 | Technical Review | ASIL 사전할당 제거; 법적요구사항/운영모드/선행위험 섹션 추가; F-06 QM 수정; 요구사항 수 통일 |

---

**Document End**
