# Item Definition (아이템 정의)

**Document ID**: PART3-00-ITEM
**ISO 26262 Reference**: Part 3, Clause 5
**ASPICE Reference**: N/A
**Version**: 3.0
**Date**: 2026-02-17
**Status**: Released (v3.0 — 시나리오 중심 완전 재정의)

---

## 1. 문서 목적 (Purpose)

본 문서는 **ISO 26262-3:2018 Part 3, Clause 5**에 따라 **Item의 정의 및 범위**를 명확히 하고,
개발 대상 시스템의 경계(Boundary)와 상호작용(Interaction)을 규정합니다.

> 본 프로젝트의 핵심 검증 시나리오 **Fault → Gateway Routing → UDS Diagnostics → OTA Update**가
> 모든 문서의 중심 실(Red Thread)입니다. 이하 모든 정의는 이 흐름을 기준으로 기술됩니다.

---

## 2. Item 정의 (Item Definition)

### 2.1 Item 명칭

**Vehicle vECU Communication & OTA Verification System**
(차량 통신 기반 vECU 진단 및 OTA 검증 시스템)

### 2.2 Item 설명

본 Item은 **Central Gateway (CGW)를 중심**으로 차량 내 BCM(Body Control Module)에서 발생하는
**고장 이벤트(DTC)를 감지**하고, **UDS 진단 통신**으로 수집한 뒤, **OTA 업데이트**로
소프트웨어를 갱신하는 전 과정을 검증하는 **가상 ECU (vECU)** 기반 시스템입니다.

**시스템 핵심 역할**:
1. **BCM 고장 감지**: Window Motor Overcurrent → DTC B1234 → CAN-LS 전송
2. **Central Gateway 라우팅**: CAN-LS → CAN-HS2 (vECU/Cluster) + Ethernet/DoIP (OTA Server)
3. **UDS 진단 수집**: 0x10 Session Control → 0x19 Read DTC → DTC 데이터 추출
4. **OTA 소프트웨어 갱신**: 0x10 Programming Session → 0x34 Download → 0x36 Transfer → 0x37 Exit
5. **ADAS 안전 경고 UI**: AEB/LDW/BSD 이벤트의 Cluster 시각 경고 (ISO 26262 ASIL-D 준수)

### 2.3 Item 범위 (Scope)

#### 포함 (In Scope):

| # | 컴포넌트 | 역할 | 시나리오 단계 |
|---|---------|------|-------------|
| 1 | **BCM (Body Control Module)** | 고장 감지 및 DTC 생성, CAN-LS 전송 | Phase 1: Fault |
| 2 | **Central Gateway (CGW)** | CAN 도메인 간 라우팅 허브, DoIP 경로 제공 | Phase 2: Routing |
| 3 | **vECU (IVI Virtual ECU)** | Cluster 경고 활성화, 내부 DTC 기록 | Phase 2: Routing |
| 4 | **CANoe Tester (진단 노드)** | UDS 세션/DTC Read, TCP/IP OTA 서버 연결 | Phase 3: Diagnostics |
| 5 | **OTA Server (가상 노드)** | UDS 프로그래밍 세션, 펌웨어 다운로드/전송 | Phase 4: OTA |
| 6 | **CAN 통신 인프라** | CAN-LS (125kbps), CAN-HS1 (500kbps), CAN-HS2 (500kbps) | 전 구간 |
| 7 | **Ethernet/DoIP 인터페이스** | OTA Server ↔ CGW 연결 (ISO 13400-2) | Phase 3-4 |
| 8 | **ADAS 센서 데이터 수신** | Camera (LDW), Radar (AEB/BSD) CAN 신호 수신 | 상시 |

#### 제외 (Out of Scope):

| # | 제외 항목 | 이유 |
|---|---------|------|
| 1 | IVI 하드웨어 (디스플레이) | 별도 Tier-1 공급 |
| 2 | Ambient LED 하드웨어 | BCM 담당 (입력 신호만 수신) |
| 3 | ADAS 센서 하드웨어 | Camera/Radar 물리 하드웨어 (ADAS Domain) |
| 4 | Powertrain ECU (EMS, TCU) | 기존 시스템 (입력 신호만 수신) |
| 5 | 실제 OTA 클라우드 서버 | CANoe CAPL 소켓으로 모사 |
| 6 | Zonal Controller 아키텍처 | 미래 SDV 방향 (본 프로젝트는 Central GW 기반) |

---

## 3. 핵심 검증 시나리오 (Master E2E Scenario)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Master E2E Scenario — Red Thread                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [Phase 1] FAULT DETECTION                                              │
│  BCM (CAN-LS, 0x500)                                                    │
│    ├─ Window Motor Overcurrent 감지: 50A > 정상 5A                       │
│    ├─ DTC B1234 저장 (ISO 14229 DTC Format)                             │
│    └─ BCM_FaultStatus CAN 메시지 전송 (매 10ms)                          │
│         │                                                               │
│         ▼  CAN-LS (125kbps)                                             │
│  [Phase 2] GATEWAY ROUTING                                              │
│  Central Gateway (CGW)                                                  │
│    ├─ CAN-LS 수신 → CAN-HS2 라우팅 (≤ 5ms, REQ-G02)                    │
│    ├─ vECU → Cluster 경고등 활성화 (FTTI < 50ms, REQ-F03)               │
│    └─ Ethernet/DoIP 경로 제공 (ISO 13400-2, REQ-G03)                    │
│         │                                                               │
│         ▼  DoIP / TCP                                                   │
│  [Phase 3] UDS DIAGNOSTICS                                              │
│  CANoe Tester (CAPL 진단 노드)                                           │
│    ├─ UDS 0x10 0x03 (Extended Diagnostic Session) → BCM                 │
│    ├─ UDS 0x19 0x02 (Read DTC by Status Mask) → DTC B1234 수신          │
│    └─ TCP/IP → 가상 OTA 서버 DTC 데이터 전송                             │
│         │                                                               │
│         ▼  UDS over DoIP                                                │
│  [Phase 4] OTA UPDATE                                                   │
│  OTA Server (CANoe 가상 노드, Ethernet)                                  │
│    ├─ UDS 0x10 0x02 (Programming Session) → BCM                         │
│    ├─ UDS 0x34 (Request Download, 64KB 펌웨어)                           │
│    ├─ UDS 0x36 × N (Transfer Data, 4KB/block)                           │
│    ├─ UDS 0x37 (Transfer Exit)                                          │
│    └─ BCM 재시작 → DTC 소거 → 정상 복귀 검증                             │
│                                                                         │
│  합격 기준: 전 단계 연속 성공 | 총 소요 시간 < 120초 | Rollback 100%     │
└─────────────────────────────────────────────────────────────────────────┘
```

**적용 표준**:
- ISO 14229-1 UDS (진단 통신)
- ISO 13400-2 DoIP (Ethernet 진단)
- ISO 26262-4 (기능 안전 — ASIL-D for ADAS)
- ASPICE PAM 3.1 (프로세스 품질)

---

## 4. Item의 기능 (Functions of the Item)

### 4.1 시나리오 단계별 기능

| Function ID | 기능 | 시나리오 단계 | ASIL (HARA) |
|-------------|------|-------------|-------------|
| **F-01** | Fault Detection | Phase 1 | ASIL-B (SG-06) |
| **F-02** | Gateway Routing | Phase 2 | QM (SG-09) |
| **F-03** | Cluster Warning | Phase 2 | ASIL-D (SG-01/02) |
| **F-04** | UDS Diagnostics | Phase 3 | ASIL-B (SG-08) |
| **F-05** | OTA Update | Phase 4 | ASIL-A (SG-08) |
| **F-06** | ADAS Safety UI | 상시 | ASIL-D (SG-01, SG-02) |
| **F-07** | Fail-Safe / Self-Test | 상시 | ASIL-B (SG-06) |

> **Note (ISO 26262-3:2018, Clause 7)**: ASIL은 HARA 결과로 결정됩니다.
> 상기 값은 HARA 완료 후 도출된 참조값 — 상세는 HARA 문서를 참조하십시오.

### 4.2 기능 우선순위 (Safety-Critical First)

1. **F-06** ADAS Safety UI — ASIL-D — 충돌/이탈 경고 최우선
2. **F-01** Fault Detection — ASIL-B — 고장 감지 및 DTC 생성
3. **F-03** Cluster Warning — ASIL-D — 운전자 시각 경보
4. **F-07** Fail-Safe / Self-Test — ASIL-B — 시스템 안전 상태 진입
5. **F-04** UDS Diagnostics — ASIL-B — 진단 데이터 수집
6. **F-05** OTA Update — ASIL-A — 소프트웨어 갱신
7. **F-02** Gateway Routing — QM — 통신 인프라

---

## 5. 시스템 컨텍스트 다이어그램 (System Context)

```
  ┌────────────────────────────────────────────────────────┐
  │               External Systems (입력)                   │
  │  Camera (LDW) ──┐                                      │
  │  Radar (AEB/BSD)┤─── CAN-HS1/HS2 ──► vECU            │
  │  BCM (DTC) ─────┤                                      │
  │  IVI (Mode) ────┘                                      │
  └────────────────────────────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Central Gateway (CGW) │  ◄── 핵심 라우팅 허브
              │   CAN-LS │ CAN-HS2     │
              │   Ethernet/DoIP ────────┼──► OTA Server (가상)
              └────────────┬────────────┘
                           │ CAN-HS2
              ┌────────────▼────────────┐
              │   vECU (검증 대상)       │
              │   Cluster 경고 │ 진단    │
              └─────────────────────────┘
```

---

## 6. 아키텍처 전략 컨텍스트

| 아키텍처 시대 | 특징 | 본 프로젝트 |
|------------|------|-----------|
| **Domain ECU 분산형** | 도메인별 독립 ECU | — |
| **Central Gateway 중심** ← | CGW 집중 라우팅 | **✅ 현재 (본 프로젝트)** |
| **Zonal Controller** | 물리 구역 기반 통합 | — (미래 SDV 방향) |

> **설계 의도**: Central Gateway는 현재 양산차 표준 아키텍처입니다.
> Zonal Architecture는 미래 SDV(Software Defined Vehicle) 방향이며,
> 본 프로젝트는 **Central GW 기반 검증 환경**을 구축합니다.

---

## 7. 개발 환경

| 도구 | 용도 | 역할 |
|------|------|------|
| **CANoe 17+** | 검증 플랫폼 | 전 시나리오 자동화, CAPL 기반 노드 시뮬레이션 |
| **CAPL** | 스크립트 언어 | BCM_Sim, CGW_Sim, vECU_Sim, OTA_Server_Sim |
| **dSPACE SCALEXIO** | HIL 플랫폼 | 하드웨어 수준 검증 (Level 2) |
| **Logic Analyzer** | FTTI 측정 | T1(Fault) ~ T4(Cluster) 측정 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Safety Manager** | Sarah Lee | ✅ Approved | 2026-02-17 |
| **Chief Engineer** | Mike Park | ✅ Approved | 2026-02-17 |
| **Project Manager** | John Kim | ✅ Approved | 2026-02-17 |

---

**Document Version**: 3.0 | **Last Updated**: 2026-02-17
