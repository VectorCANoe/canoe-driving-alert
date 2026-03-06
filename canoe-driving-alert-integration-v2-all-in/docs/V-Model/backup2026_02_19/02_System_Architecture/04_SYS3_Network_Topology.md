# Network Topology (네트워크 토폴로지)

**Document ID**: PART4-05-NET
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. CAN Network Architecture

### Network Segmentation

| Network ID | Name | Baudrate | Domains | ECU Count | Utilization |
|------------|------|----------|---------|-----------|-------------|
| **CAN-HS1** | High-Speed 1 | 500 kbps | Powertrain, Chassis | 7 | ~40% |
| **CAN-HS2** | High-Speed 2 | 500 kbps | Infotainment, ADAS | 10 | ~35% |
| **CAN-LS** | Low-Speed | 125 kbps | Body | 6 | ~15% |
| **Ethernet** | DoIP (ISO 13400) | 100 Mbps | OTA Server (외부) | 1 | ~5% |

---

## 2. Physical Topology

```
CAN-HS1 (500 kbps):
 120Ω  ├─ EMS ─┬─ TCU ─┬─ ESP ─┬─ MDPS ─┬─ CGW  120Ω
             │       │       │        │
           Speed   ABS     EPB      ...

CAN-HS2 (500 kbps):
 120Ω  ├─ vECU ─┬─ IVI ─┬─ Cluster ─┬─ Camera ─┬─ CGW  120Ω
              │      │          │          │
            HUD   Radar       SCC       AVM

CAN-LS (125 kbps):
 Built-in ├─ BCM ─┬─ Lighting ─┬─ HVAC ─┬─ Doors ─┬─ CGW  Built-in
               │          │         │        │
             BDC        Seat      ...      ...
```

---

## 3. Gateway Routing Table

| Source Network | Destination Network | Routed Messages | Filtering |
|----------------|---------------------|-----------------|-----------|
| CAN-HS1 | CAN-HS2 | Vehicle Speed, Gear Status | ID 기반 |
| CAN-HS2 | CAN-HS1 | ADAS Events (경로 없음) | 차단 |
| CAN-HS2 | CAN-LS | Lighting Commands | ID 기반 |
| CAN-LS | CAN-HS2 | Door Status, Temperature | ID 기반 |

**Firewall**: Gateway에서 불필요한 메시지 필터링 (보안)

---

## 4. CAN Message Load Analysis

| Network | Total Messages/sec | Bandwidth | Margin | Status |
|---------|-------------------|-----------|--------|--------|
| CAN-HS1 | ~2000 | 40% | 60% | ✅ Safe |
| CAN-HS2 | ~1750 | 35% | 65% | ✅ Safe |
| CAN-LS | ~200 | 15% | 85% | ✅ Safe |

**Margin > 50%**: 향후 기능 추가 여유 확보

---

**Auto-generated**: 2026-02-14 14:59:03

---

## 5. OTA 통신 경로 상세 (E2E Message Flow)

```
Fault Injection → DTC 전파 → 진단 → OTA 업데이트 메시지 흐름

BCM (CAN-LS)
  │ BCM_FaultStatus (0x500, 100ms cycle)
  ▼
Central Gateway (CGW)
  │ [CAN-LS → CAN-HS2] BCM_FaultStatus 라우팅 (≤5ms)
  │ [CAN-LS → Ethernet] DoIP Routing Activation (0xE001)
  ▼
vECU (CAN-HS2)              OTA Server (Ethernet/DoIP)
  │ Cluster 경고등 활성화    │ DoIP Diagnostic Message (0xE004)
  │                         │ UDS 0x10 0x03 (Extended Session)
  │                         │ UDS 0x19 0x02 (Read DTC)
  │                         │   → DTC B1234 수신 확인
  │                         │ UDS 0x10 0x02 (Programming Session)
  │                         │ UDS 0x34 (Request Download, 64KB)
  │                         │ UDS 0x36 × 16 (Transfer Data, 4KB/block)
  │                         │ UDS 0x37 (Transfer Exit)
  │                         │ BCM 재시작 → DTC 소거 확인
```

**CANoe 구현**: CAPL TCP/IP 소켓 + OTA Server Node + CAPL Tester Node

