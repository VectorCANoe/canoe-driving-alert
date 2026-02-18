# Technical Safety Concept (기술 안전 개념)

**Document ID**: PART4-01-TSC
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-17
**Status**: Released

---

## 1. 문서 목적

본 문서는 **ISO 26262-4:2018 Part 4, Clause 7**에 따라 **Technical Safety Concept (TSC)**를 정의합니다.

**FSC (Functional Safety Concept)에서 도출된 FSR을 시스템 구현 레벨의 Technical Safety Requirements (TSR)로 변환**하고, 각 하드웨어/소프트웨어 요소에 할당합니다.

> **ISO 26262-1:2018 §3.167**: Technical Safety Concept = Technical Safety Requirements의 명세 + 시스템 요소에의 할당 + 시스템 레벨 기능 안전 근거

**FSR → TSR 변환 원칙**:
- FSR (Implementation-independent): "무엇을 해야 하는가"
- TSR (Implementation-specific): "어떻게 구현해야 하는가"

---

## 2. ASIL 상승 근거 (ASIL Escalation Rationale)

> **ISO 26262-2:2018 §6.4.4**: ASIL 상승에는 문서화된 근거가 필요합니다.

| 항목 | HARA ASIL | 시스템요구사항 ASIL | 근거 |
|------|----------|------------------|------|
| H-04 도어경고 (REQ-A03) | ASIL-B | ASIL-B | v2.0 수정으로 일치됨 (구 ASIL-C는 HARA 오류) |
| H-03 후진경고 (REQ-F01) | ASIL-B | ASIL-B | 일치 |
| vECU CAN Driver | (하위 FSR-D) | ASIL-D | 근거: ASIL-D 컴포넌트 데이터 전달 경로이므로 동일 ASIL 적용 (ISO 26262-6 §7.4.2) |

---

## 3. Technical Safety Requirements (TSR)

### 3.1 ASIL-D Technical Safety Requirements

#### TSR-D01: AEB 경고 CAN 수신 및 처리 (FSR-D01 → 구현 명세)

- **Derives From**: FSR-D01 (AEB 충돌 경고)
- **System Requirement**: REQ-A02
- **ASIL**: ASIL-D
- **Technical Requirement**:
  1. vECU는 CAN-HS2 버스에서 SCC의 AEB_Event 메시지 (CAN ID: **0x380**, 50ms 주기)를 수신해야 한다.
  2. Alive Counter (1 byte, 0~255 순환) 및 CRC-8 (생성다항식: 0x1D) 검증을 수행해야 한다.
  3. 검증 실패 시 DTC_Set(DTC_AEB_MSG_ERROR) 및 경고 표시 실패 처리를 수행해야 한다.
  4. AEB_Event 수신 후 ASIL-D Task (Task_ADAS, 10ms 주기) 내 20ms 내에 경고 출력 명령을 생성해야 한다.
  5. 시각 채널 (Cluster CAN ID: 0x200) 과 청각 채널 (IVI Internal) 모두에 독립적으로 출력해야 한다.
- **Safe State Mechanism**: 두 채널 중 하나 실패 → 나머지 채널 단독 동작 유지
- **FDTI**: ≤ 20ms (AEB 메시지 2회 연속 미수신 → 오류 감지)
- **FRTI**: ≤ 80ms (오류 감지 후 청각 채널 Fallback 전환)
- **Watchdog**: External Watchdog IC, 100ms timeout, Window Watchdog 방식

#### TSR-D02: LDW 경고 듀얼채널 출력 (FSR-D02 → 구현 명세)

- **Derives From**: FSR-D02 (LDW 차선 이탈 경고)
- **System Requirement**: REQ-A01
- **ASIL**: ASIL-D
- **Technical Requirement**:
  1. vECU는 Camera_LDW 메시지 (CAN ID: **0x300**, 20ms 주기)를 수신해야 한다.
  2. 시각 채널: LDW_Visual_Cmd → Cluster ECU (CAN ID: 0x210)
  3. 촉각 채널: LDW_Haptic_Cmd → MDPS ECU (CAN ID: 0x220)
  4. 각 채널은 독립 메모리 영역 (MPU 보호), 독립 CAN ID 사용
  5. ASIL 분해: ASIL-D(d) → ASIL-C(d) 시각 + ASIL-C(d) 촉각
- **Independence Proof**: MPU 위반 시 HW 예외 발생 → 채널 격리 확인
- **FDTI**: ≤ 50ms | **FRTI**: ≤ 150ms

---

### 3.2 ASIL-B Technical Safety Requirements

#### TSR-B01: 후진 경고 타이밍 (FSR-B01 → 구현 명세)

- **Derives From**: FSR-B01 (후진 경고)
- **System Requirement**: REQ-F01, REQ-F02, REQ-F03
- **ASIL**: ASIL-B
- **Technical Requirement**:
  1. TCU_GearStatus 메시지 (CAN ID: **0x180**, 100ms 주기) 수신 후 Gear=R 파싱
  2. Gear=R 감지 후 ≤ 500ms 내에 후진 경고 UI 활성화
  3. Timeout: TCU 메시지 3회 연속 미수신 → 마지막 유효 기어값 유지 + DTC
  4. 후방 카메라 영상 표시: 별도 비디오 경로 (ASIL-QM)

#### TSR-B02: 도어 개방 경고 타이밍 (FSR-B02 → 구현 명세)

- **Derives From**: FSR-B02 (도어 개방 경고)
- **System Requirement**: REQ-A03
- **ASIL**: ASIL-B (수정: 구 ASIL-D는 HARA v2.0에서 ASIL-B로 정정됨)
- **Technical Requirement**:
  1. BCM_DoorStatus 메시지 (CAN ID: **0x500**, 100ms 주기) 수신
  2. Door_Open 비트 = 1 감지 후 ≤ 200ms 내에 경고 UI + 경고음 동시 활성화
  3. CRC-8 검증 필수 (BCM 메시지 위변조 감지)
  4. 차속 ≤ 0 km/h (정차 중) 도어 개방은 경고 미발생 (주행 중 도어만 해당)
- **Safe State**: 시각 경고 + 청각 경고 동시 출력

#### TSR-B03: CAN Fail-Safe 전환 메커니즘 (FSR-B03 → 구현 명세)

- **Derives From**: FSR-B03 (CAN Fail-Safe)
- **System Requirement**: REQ-G04
- **ASIL**: ASIL-B
- **Technical Requirement**:
  1. CAN Bus Error Counter > 127 (Error Passive) → 즉시 DTC + Fail-Safe 플래그 설정
  2. CAN Bus Error Counter = 255 (Bus Off) → ≤ 100ms 내에 조명 기본값(White, 50%) 설정
  3. Bus Off Recovery: 128회 연속 recessive bit 후 자동 복구 시도 (ISO 11898-1)
  4. Fail-Safe 상태에서 비안전 기능(OTA, 멀티미디어) 비활성화

---

### 3.3 ASIL-A Technical Safety Requirements

#### TSR-A01: 조명 출력 모니터링 메커니즘 (FSR-A01 → 구현 명세)

- **Derives From**: FSR-A01 (조명 Fail-Safe)
- **System Requirement**: REQ-N03
- **ASIL**: ASIL-A
- **Technical Requirement**:
  1. Lighting_Control_Manager는 10ms마다 조명 출력 PWM 값을 읽어 임계값과 비교
  2. 임계값 (눈부심 기준: PWM ≥ 90%) 초과 시 즉시 PWM = 50% 설정
  3. 조명 HW 오류 (오픈/쇼트) 감지 → 조명 OFF + DTC
  4. Watchdog: Software Watchdog (200ms timeout)

---

## 4. Safety Mechanism Summary

| TSR ID | Safety Mechanism | ASIL | ISO 26262 기법 |
|--------|-----------------|------|----------------|
| TSR-D01 | Alive Counter + CRC-8 | ASIL-D | E2E Protection (ISO 26262-6 §7.4.9) |
| TSR-D01 | External Window Watchdog | ASIL-D | HW Watchdog Timer |
| TSR-D02 | MPU 메모리 분리 | ASIL-D | Freedom from Interference |
| TSR-B01 | CAN Timeout Detection | ASIL-B | Plausibility Check |
| TSR-B02 | CRC-8 메시지 검증 | ASIL-B | E2E Protection |
| TSR-B03 | Bus Off Recovery | ASIL-B | ISO 11898-1 |
| TSR-A01 | SW Watchdog | ASIL-A | Software Watchdog |

---

## 5. Traceability (FSR → TSR → System Requirements)

| FSR | TSR | System Req | SW Req | ASIL |
|-----|-----|------------|--------|------|
| FSR-D01 | TSR-D01 | REQ-A02 | SWR-001 | ASIL-D |
| FSR-D02 | TSR-D02 | REQ-A01 | SWR-002 | ASIL-D |
| FSR-B01 | TSR-B01 | REQ-F01, REQ-F02, REQ-F03 | SWR-003 | ASIL-B |
| FSR-B02 | TSR-B02 | REQ-A03 | SWR-007 | ASIL-B |
| FSR-B03 | TSR-B03 | REQ-G04 | SWR-009 | ASIL-B |
| FSR-A01 | TSR-A01 | REQ-N03 | SWR-010 | ASIL-A |

---

## 6. 검증 방법 (Verification Methods)

| TSR | 검증 방법 | 기준 |
|-----|---------|------|
| TSR-D01 | HIL Fault Injection (CAN 메시지 손실, Counter 오류) | FTTI 100ms 내 경고 출력 |
| TSR-D02 | MPU 위반 테스트, 채널 차단 테스트 | 단일 채널 실패 시 다른 채널 정상 |
| TSR-B01, B02 | CAN Fault Injection, Timeout 시나리오 | FTTI 이내 Fail-Safe 전환 |
| TSR-B03 | CAN Bus Off 시뮬레이션 (CANoe) | 100ms 내 Fail-Safe 전환 |
| TSR-A01 | 조명 PWM 초과 시나리오 | 즉시 PWM 50% 제한 |

---

## 7. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-17 | Technical Review | 신규 생성 — ISO 26262-4 Clause 7 TSR 계층 추가 |

---

**Document End**

---

## TSR-B04: Central Gateway Protocol Translation 안전 요구사항

- **Source FSR**: FSR-B04
- **ASIL**: QM (ASPICE 레벨 관리)
- **Allocation**: Central Gateway ECU

### 기술 안전 요구사항

| TSR ID | 요구사항 | 검증 기준 |
|--------|---------|---------|
| **TSR-B04-01** | CAN-LS ↔ CAN-HS2 메시지 변환 지연 ≤ 5ms | CANoe Trace 타임스탬프 측정 |
| **TSR-B04-02** | CAN → DoIP 변환 지연 ≤ 10ms | TCP/IP 패킷 타임스탬프 |
| **TSR-B04-03** | 메시지 손실률 < 0.001% (1,000,000 메시지 중 < 10개) | 장시간 부하 테스트 |
| **TSR-B04-04** | DoIP 연결 실패 시 Graceful Abort (OTA 세션 정상 종료) | Fault Injection: TCP 연결 차단 |
| **TSR-B04-05** | Gateway CAN Bus Off 시 Fail-Safe: DTC 저장 후 대기 | CAN Bus Off 주입 테스트 |

### CANoe 검증 환경

```
[CANoe Simulation]
  Node: BCM_Sim (CAPL) → CAN-LS 0x500 BCM_FaultStatus
  Node: CGW_Sim (CAPL) → CAN-LS 수신 → CAN-HS2 라우팅
                        → TCP/IP 소켓 → OTA_Server_Sim
  Node: vECU_Sim (CAPL) → CAN-HS2 수신 → Cluster 경고
  Node: OTA_Server_Sim (CAPL/.NET) → DoIP 수신 → UDS OTA
```

