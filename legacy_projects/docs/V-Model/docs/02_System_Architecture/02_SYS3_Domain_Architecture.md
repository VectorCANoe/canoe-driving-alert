# Domain Architecture (도메인 아키텍처)

**Document ID**: PART4-03-DOM
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Domain Overview

총 5개 Domain으로 기능 분리하여 Fault Isolation 및 ASIL Compliance 확보.


### DOM-01: Infotainment Domain

- **ECU Count**: 4개
- **ASIL**: ASIL-B
- **Network**: CAN-HS2 (500 kbps)

#### ECUs:
1. IVI Control ECU
2. vECU (IVI vECU)
3. Cluster ECU
4. HUD ECU


### DOM-02: Body Domain

- **ECU Count**: 6개
- **ASIL**: ASIL-B
- **Network**: CAN-LS (125 kbps)

#### ECUs:
1. BCM
2. Lighting Control ECU
3. HVAC Control ECU
4. BDC
5. Door Sensors
6. Seat Control ECU


### DOM-03: ADAS Domain

- **ECU Count**: 6개
- **ASIL**: ASIL-D
- **Network**: CAN-HS2 (500 kbps)

#### ECUs:
1. ADAS Control ECU
2. Front Camera (LDW)
3. Rear Camera (RVC)
4. Radar (BSD)
5. SCC (AEB)
6. AVM ECU


### DOM-04: Powertrain Domain

- **ECU Count**: 3개
- **ASIL**: ASIL-C
- **Network**: CAN-HS1 (500 kbps)

#### ECUs:
1. EMS
2. TCU
3. Vehicle Speed Sensor


### DOM-05: Chassis Domain

- **ECU Count**: 4개
- **ASIL**: ASIL-D
- **Network**: CAN-HS1 (500 kbps)

#### ECUs:
1. ESP/ESC
2. MDPS
3. ABS
4. EPB



---

## 2. Domain 간 Communication

모든 Domain 간 통신은 **Central Gateway (CGW)**를 경유합니다.

### Routing Rules

| Source | Destination | Message Type | Rationale |
|--------|-------------|--------------|-----------|
| ADAS → Infotainment | LDW, AEB 이벤트 | 경고 필요 |
| Powertrain → Infotainment | 차량 속도, 기어 상태 | 조명 제어, 경고 조건 |
| Body → Infotainment | 도어 상태, 온도 | 경고, 조명 제어 |
| Infotainment → Body | 조명 제어 명령 | Ambient LED 제어 |

---

**Auto-generated**: 2026-02-14 14:59:03
