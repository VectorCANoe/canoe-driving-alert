# 컨셉 디자인 (Concept Design)

**Document ID**: PROJ-02-CD
**ISO 26262 Reference**: Part 3, Cl.7 — Hazard Analysis and Risk Assessment (HARA) 연계
**ASPICE Reference**: SYS.2 (System Context)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 상단 — 개념 설계 단계 | — | — | `01_Requirements.md` |

본 문서는 프로젝트의 전체적인 **기능(Concept)**, **연결(Network)**, **흐름(Flow)**을 정의합니다.

---

## 1. Concept Design (What)
> **"무엇을 만드는가?"** — 시스템의 입력, 제어, 출력을 정의합니다.

### 1.1 시스템 구성도 (System Block Diagram)

```
┌──────────────────────────────────────────────────────────────┐
│                    입력층 (Foundation)                        │
│  A: Vehicle_ECU ── 속도/가속도/제동 (스칼라)                  │
│  B: MDPS_ECU ───── 조향 입력/급차선변경 (벡터)               │
│     LDW_ECU ────── 차선이탈 감지                             │
└──────────────────────────┬───────────────────────────────────┘
                           │ CAN-LS (125kbps) → CGW → CAN-HS
┌──────────────────────────▼───────────────────────────────────┐
│                    판단층 WDM_ECU (Rule-Based)                │
│  A 단독 OR B 단독  → 1단계 (Cluster 황색 + Sound)            │
│  A AND B           → 2단계 (Cluster 적색 + Sound + Ambient)  │
│  A+B + OTA 조건    → 3단계 (무조건, IVI OTA 팝업)            │
└───────────────┬──────────────────────────────────────────────┘
                │ CAN-HS (500kbps)
┌───────────────▼──────────────────────────────────────────────┐
│  출력층                                                       │
│  Cluster_ECU ─ 경고등 (황색/적색)                            │
│  Ambient_ECU ─ 앰비언트 라이트 (패턴/색상)                   │
│  Sound_ECU ── 경고음 (1~3단계)                               │
│  IVI_ECU ──── OTA 팝업 / 진행률                              │
│  Door_ECU ─── 시트 진동 (3단계)                              │
└──────────────────────────────────────────────────────────────┘
    │ 해제 조건                                                  │ 특화층 D
    │                                                            │
┌───▼──────────────┐        ┌───────────────────────────────────▼──┐
│  해제층           │        │  특화층 D                            │
│  라엘: 응시 복귀  │        │  준영: gRoadZone 구간 인식           │
│  현준: 핸들 입력  │        │    0:일반 / 1:스쿨존 / 2:고속도로   │
└──────────────────┘        │    3:IC출구 앰비언트 방향 안내       │
                            │                                      │
                            │  성현: OTA 구독 서비스               │
                            │    위험 누적 → Level1/2 구독 제안    │
                            │    UDS 0x10→0x27→0x34→0x36→0x37    │
                            └──────────────────────────────────────┘
```

### 1.2 주요 도메인 및 역할

| 도메인 | ECU | 역할 (Role) |
|--------|-----|-------------|
| **입력 A** | **Vehicle_ECU** | 차량 속도(gVehicleSpeed) / 가속도(gAccelValue) / 제동(gBrakeValue)을 CAN-LS 100ms 주기 WDM_ECU에 보고 |
| **입력 B** | **MDPS_ECU** | 조향 입력(SteeringInput) / 급차선변경(gLaneChangeAlert)을 CAN-LS로 WDM_ECU에 보고 |
| **입력 B** | **LDW_ECU** | 차선이탈(gLaneDeparture)을 CAN-LS로 WDM_ECU에 보고 |
| **Gateway** | **CGW** | CAN-LS(입력층) → CAN-HS(WDM_ECU) 신호 라우팅 / OTA DoIP 경로 활성화 |
| **판단층** | **WDM_ECU** | Rule-Based 위험 판단 → gWarningLevel 0~3 설정 → 출력 ECU 제어 명령 |
| **출력** | **Cluster_ECU** | 경고등 활성화 (1단계: 황색, 2단계: 적색) |
| **출력** | **Ambient_ECU** | 앰비언트 라이트 패턴 제어 (구간/경고 단계별) |
| **출력** | **Sound_ECU** | 단계별 경고음 출력 |
| **출력** | **IVI_ECU** | OTA 구독 팝업 / 진행률 표시 |
| **출력** | **Door_ECU** | 3단계 도어 잠금(3초) + 미러 LED |
| **OTA** | **OTA_Server** | 구독형 펌웨어 업데이트 서버 시뮬레이션 (DoIP 프로토콜) |

---

## 2. Network Architecture (How)
> **"어떻게 연결하는가?"** — 물리적/논리적 네트워크 토폴로지를 정의합니다.

### 2.1 네트워크 토폴로지 (Bus Topology)

```
[CAN-LS 125kbps] ─────────────────────────────────── CGW ──────
  Vehicle_ECU  (0x100 — Vehicle_Speed)                          │
  MDPS_ECU     (0x110 — Steering_Status)                        │ CAN-HS
  LDW_ECU      (0x120 — LDW_Status)                            │ 500kbps
  Tester/OTA   (0x7DF — UDS_Request)                            │
                                                              WDM_ECU
                                                                 │
[CAN-HS 500kbps] ─────────────────────────────────────────────────
  WDM_ECU      (0x200 — WDM_Warning)
  Cluster_ECU  (0x210 — Cluster_Warning)
  Ambient_ECU  (0x220 — Ambient_Control)
  Sound_ECU    (0x230 — Sound_Control)
  IVI_ECU      (0x240 — IVI_Status)
  Door_ECU     (0x250 — Door_Control)

[Ethernet DoIP 100Mbps]
  OTA_Server ──────────────────── CGW ── WDM_ECU (UDS 세션)
```

### 2.2 통신 프로토콜 매핑

| 채널 | 프로토콜 | 속도 | 연결 ECU | 용도 |
|------|----------|------|----------|------|
| **CAN-LS** | CAN 2.0B | 125kbps | Vehicle_ECU / MDPS_ECU / LDW_ECU → CGW | 입력층 신호 수집 |
| **CAN-HS** | CAN 2.0B | 500kbps | WDM_ECU ↔ Cluster / Ambient / Sound / IVI / Door | 경고 출력 제어 |
| **Ethernet** | DoIP (ISO 13400-2) | 100Mbps | OTA_Server ↔ CGW ↔ WDM_ECU | OTA 펌웨어 고속 전송 |

---

## 3. Signal Flow / Sequence (Scenario)
> **"데이터가 어떻게 흐르는가?"** — 핵심 시나리오(E2E)의 데이터 흐름을 정의합니다.

### 3.1 E2E 시나리오: 위험 감지 → 단계별 경고 → OTA 구독

### 3.2 시나리오 단계별 상세

0. **초기화** (Scene.1~2): 모든 ECU 초기화 후 정상 주행(gVehicleSpeed = 60km/h, gWarningLevel = 0, gRoadZone = 0) 상태 확인.

1. **A단독 1단계 경고** (Scene.3): Vehicle_ECU가 과속(gVehicleSpeed > 80km/h) 또는 급가속(gAccelValue > 3.5 m/s²)을 감지 → WDM_ECU가 gWarningLevel = 1 → Cluster 황색 경고등 + Sound 1단계 경고음 발령 (FTTI ≤50ms).

2. **B단독 1단계 경고** (Scene.4): LDW_ECU가 차선이탈(gLaneDeparture = 1) 또는 MDPS_ECU가 급차선변경(gLaneChangeAlert = 1)을 감지 → WDM_ECU가 gWarningLevel = 1 → 동일 경고 출력.

3. **A+B 2단계 경고** (Scene.5): A와 B 동시 감지 → WDM_ECU가 gWarningLevel = 2 → Cluster 적색 + Sound 2단계 + Ambient 경고 패턴.

4. **경고 해제** (Scene.6~7): GazeActive 0→1(라엘) 또는 SteeringInput = 1(현준) 감지 → gWarningLevel = 0 초기화.

5. **gRoadZone 구간 앰비언트** (Scene.8~10): Panel 버튼으로 gRoadZone 변경 → 스쿨존(1): Ambient RED 점멸 / 고속도로(2): 핸들 미입력 10초 → ORANGE 파동 + 진동 / IC출구(3): Ambient 좌→우 흐름 애니메이션.

6. **3단계 OTA 제안** (Scene.11~14): gAccelCount ≥ 3 → gWarningLevel = 3 → IVI 팝업 → 운전자 동의 → OTA_Server DoIP Routing Activation → UDS 0x10 → 0x27 → 0x34 → 0x36×N → 0x37 → CRC-32 검증 → ECU 재시작.

7. **안전 복구** (Scene.15~16): CRC 불일치 → Rollback / Bus Off → 세션 안전 중단 + DTC U0300.

---

## 4. HARA (Hazard Analysis and Risk Assessment) 요약
> **Safety Goals**: SG-01 (ASIL-B) — 위험 운전 50ms 이내 경고 발령 / SG-02 (ASIL-B) — OTA 실패 시 이전 펌웨어 자동 복구

| ID | Hazard | Operational Situation | Severity | Exposure | Controllability | ASIL | Safety Goal |
|----|--------|-----------------------|----------|----------|-----------------|------|-------------|
| H-01 | 위험 운전(과속/급가속/차선이탈) 미감지 → 경고 미발령 → 사고 → 운전자/보행자 부상 | 일반/스쿨존/고속도로 주행 중 | S2 | E4 | C2 | **B** | SG-01: 위험 운전 감지 시 WDM_ECU가 50ms 이내 단계별 경고를 발령한다 (FTTI ≤50ms) |
| H-02 | OTA 중 통신 두절로 ECU Bricking | 펌웨어 업데이트 중 | S1 | E2 | C3 | **QM** | N/A — Rollback(Req_017)으로 완화. 안전목표 없음. |
| H-03 | OTA 실패로 토크 제한 ECU 불능 → 차량 구동계 기능 이상 | OTA 펌웨어 전송 중 (전원 차단 / CRC 오류) | S2 | E3 | C2 | **B** | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 |

---

## 5. Verification Environment
> **"어떻게 검증하는가?"**

*   **Tool**: Vector CANoe 17+ (SIL - Software In the Loop)
*   **Language**: CAPL (Communication Access Programming Language)
*   **Network**: Virtual CAN-LS / CAN-HS / Virtual Ethernet (Local Loopback)
*   **Panel**: gRoadZone 버튼(4개) / 속도·가속도 TrackBar / Fault Injection Switch / 상태 Indicator

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — 시스템 구성도, 네트워크 토폴로지, E2E 시나리오, HARA |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
