# Interface Definition (인터페이스 정의)

**Document ID**: PART4-07-IF
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. System Interfaces Overview

### Interface Types

| Interface Type | Count | Protocol | ASIL |
|----------------|-------|----------|------|
| **CAN Bus** | 3 networks | CAN 2.0B | ASIL-D |
| **UDS Diagnostic** | 1 | ISO 14229 | ASIL-B |
| **User Interface** | 4 | IVI Touchscreen, Cluster | QM/ASIL-A |

---

## 2. Hardware-Software Interfaces (HSI)

### vECU HSI

| HSI ID | Interface Name | Type | Direction | Protocol | ASIL |
|--------|----------------|------|-----------|----------|------|
| **HSI-01** | CAN_RX_Interface | HW | ECU → vECU | CAN 2.0B | ASIL-D |
| **HSI-02** | CAN_TX_Interface | HW | vECU → ECU | CAN 2.0B | ASIL-D |
| **HSI-03** | Timer_Interface | HW | HW → vECU | Watchdog Timer | ASIL-C |
| **HSI-04** | Diagnostic_Interface | HW | Tester ↔ vECU | UDS | ASIL-B |

---

## 3. ECU 간 Interfaces

### vECU ↔ Cluster

| Interface ID | Signal | Direction | CAN ID | ASIL | Purpose |
|--------------|--------|-----------|--------|------|---------|
| **IF-01** | Warning_UI_Request | vECU → Cluster | 0x420 | ASIL-D | 경고 UI 표시 요청 |
| **IF-02** | Warning_Ack | Cluster → vECU | 0x421 | ASIL-D | 표시 완료 확인 |

### vECU ↔ BCM

| Interface ID | Signal | Direction | CAN ID | ASIL | Purpose |
|--------------|--------|-----------|--------|------|---------|
| **IF-03** | Ambient_Light_RGB | vECU → BCM | 0x400 | ASIL-B | 조명 색상 제어 |
| **IF-04** | Door_Status | BCM → vECU | 0x500 | ASIL-C | 도어 상태 정보 |
| **IF-05** | Light_Ack | BCM → vECU | 0x501 | ASIL-B | 조명 제어 확인 |

### vECU ↔ ADAS Sensors

| Interface ID | Signal | Direction | CAN ID | ASIL | Purpose |
|--------------|--------|-----------|--------|------|---------|
| **IF-06** | Camera_LDW_Event | Camera → vECU | 0x300 | ASIL-D | 차선 이탈 이벤트 |
| **IF-07** | Radar_BSD_Event | Radar → vECU | 0x340 | ASIL-B | 후측방 감지 |
| **IF-08** | SCC_AEB_Event | SCC → vECU | 0x380 | ASIL-D | 긴급 제동 이벤트 |

---

## 4. User Interfaces

### IVI Touchscreen (Input)

| UI Element | Type | Input Method | Purpose |
|------------|------|--------------|---------|
| Mode Selection | Button | Touch | 스포츠/에코/컴포트 모드 선택 |
| Color Picker | Slider | Touch | Ambient 조명 색상 선택 |
| Profile Menu | List | Touch | 운전자 프로필 관리 |

### Cluster Display (Output)

| UI Element | Type | Update Rate | Purpose |
|------------|------|-------------|---------|
| Warning Icon | Graphic | 50ms | ADAS 경고 아이콘 표시 |
| Warning Message | Text | 100ms | 경고 메시지 텍스트 |
| Gear Indicator | Graphic | 20ms | 기어 상태 표시 |

---

## 5. Diagnostic Interface (UDS)

### UDS Services

| Service ID | Service Name | Purpose | ASIL |
|------------|--------------|---------|------|
| **0x14** | ClearDiagnosticInformation | DTC 삭제 | ASIL-B |
| **0x19** | ReadDTCInformation | DTC 읽기 | ASIL-B |
| **0x22** | ReadDataByIdentifier | 데이터 읽기 | ASIL-B |
| **0x27** | SecurityAccess | 보안 접근 | QM |
| **0x34** | RequestDownload | OTA 다운로드 | ASIL-B |
| **0x36** | TransferData | 데이터 전송 | ASIL-B |
| **0x37** | RequestTransferExit | 전송 종료 | ASIL-B |

---

## 6. Interface Constraints

### Timing Constraints

| Interface | Min Latency | Max Latency | Jitter | Rationale |
|-----------|-------------|-------------|--------|-----------|
| Camera → vECU (AEB) | - | 30ms | <5ms | FTTI 100ms 준수 |
| vECU → Cluster (Warning) | - | 50ms | <10ms | FTTI 100ms 준수 |
| vECU → BCM (Light) | - | 100ms | <20ms | 사용자 경험 |

### Data Integrity Constraints

| Interface | Checksum | Alive Counter | Timeout | ASIL |
|-----------|----------|---------------|---------|------|
| Camera → vECU | CRC-8 | Yes (0-15) | 150ms | ASIL-D |
| vECU → Cluster | CRC-8 | Yes (0-15) | 150ms | ASIL-D |
| vECU → BCM | CRC-8 | No | 300ms | ASIL-B |

---

**Auto-generated**: 2026-02-14 14:59:03
