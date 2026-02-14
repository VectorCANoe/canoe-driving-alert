# System Architectural Design (시스템 아키텍처 설계)

**Document ID**: PART4-02-SAD
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. 시스템 아키텍처 개요

**Architecture Pattern**: Domain-Based with Central Gateway
**Total ECUs**: 23개 (+ 1 Gateway)
**Total Domains**: 5개

### Domain Summary

| Domain | ECU Count | ASIL | Network |
|--------|-----------|------|---------|
| Infotainment Domain | 4 | ASIL-B | CAN-HS2 (500 kbps) |
| Body Domain | 6 | ASIL-B | CAN-LS (125 kbps) |
| ADAS Domain | 6 | ASIL-D | CAN-HS2 (500 kbps) |
| Powertrain Domain | 3 | ASIL-C | CAN-HS1 (500 kbps) |
| Chassis Domain | 4 | ASIL-D | CAN-HS1 (500 kbps) |


---

## 2. Core System Element: vECU

**vECU**는 Infotainment Domain의 핵심 ECU로, 모든 Domain의 데이터를 수신하여 조명/경고/UI를 통합 제어합니다.

### vECU 내부 구조

| Module | ASIL | Responsibility |
|--------|------|----------------|
| ADAS UI Integration | ASIL-D | LDW, AEB, BSD 이벤트 처리 |
| Safety Warning Manager | ASIL-C | 후진, 도어 경고 처리 |
| Lighting Control | ASIL-B | Ambient 조명 제어 |
| Message Router | ASIL-B | 우선순위 기반 메시지 중재 |
| CAN Driver | ASIL-D | CAN 송수신, 오류 감지 |

---

## 3. Safety Architecture

### ASIL Decomposition

| Safety Goal | ASIL | Decomposed Elements | Independence |
|-------------|------|---------------------|--------------|
| SG-01 (AEB) | ASIL-D | vECU→Cluster (시각) + vECU→IVI (청각) | ✅ 하드웨어 분리 |
| SG-02 (LDW) | ASIL-D | vECU→Cluster (시각) + vECU→MDPS (Haptic) | ✅ 하드웨어 분리 |

---

## 4. Network Topology

### CAN Network Segmentation

- **CAN-HS1 (500 kbps)**: Powertrain + Chassis Domain
- **CAN-HS2 (500 kbps)**: Infotainment + ADAS Domain
- **CAN-LS (125 kbps)**: Body Domain

---

## 5. ASPICE SYS.3 Compliance

**Base Practices**:
- ✅ BP1: System architectural design developed
- ✅ BP2: System requirements allocated
- ✅ BP3: System interfaces defined
- ✅ BP6: Traceability established

---

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
