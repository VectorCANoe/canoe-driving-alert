# 컨셉 디자인 (Concept Design)

**Document ID**: SAMPLE-02-CD
**ISO 26262 Reference**: Part 3, Cl.7 — Hazard Analysis and Risk Assessment (HARA) 연계
**ASPICE Reference**: SYS.2 (System Context)
**Version**: 1.2
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 상단 — 개념 설계 단계 | — | — | `01_Requirements.md` |

본 문서는 프로젝트의 전체적인 **기능(Concept)**, **연결(Network)**, **흐름(Flow)**을 정의합니다.

---

## 1. Concept Design (What)
> **"무엇을 만드는가?"** — 시스템의 입력, 제어, 출력을 정의합니다.

### 1.1 시스템 구성도 (System Block Diagram)
![Concept Design](02_System_Architecture.puml)

### 1.2 주요 도메인 및 역할
| 도메인 | ECU | 역할 (Role) |
|--------|-----|-------------|
| **Body** | **BCM** (LIN Master) | LIN Slave로부터 Motor_Current 수신 → Window Motor 과전류(>50A) 감지 → DTC B1234 생성 및 CAN-LS 전파 |
| **Body** | **WindowMotorECU** (LIN Slave 0x21) | Motor_Current / Motor_Status / Motor_Direction을 10ms 주기로 BCM에 LIN 보고 |
| **Body** | **DoorModule FL/FR/RL/RR** (LIN Slave 0x22~0x25) | Door_Position / Lock_Status / Window_Position을 50ms 주기로 BCM에 LIN 보고 |
| **Gateway** | **CGW** | 이기종 네트워크(CAN-LS ↔ CAN-HS ↔ Ethernet) 간 메시지 라우팅 |
| **Infotainment** | **Cluster** | 사용자에게 고장 경고(RED Lamp) 및 상태 정보 표시 |
| **Diagnosis** | **Tester** | 외부 진단 장비 시뮬레이션 (UDS 서비스 요청: 0x10, 0x19, 0x14) |
| **Connectivity** | **OTA Server** | 펌웨어 무선 업데이트 서버 시뮬레이션 (DoIP 프로토콜) |

---

## 2. Network Architecture (How)
> **"어떻게 연결하는가?"** — 물리적/논리적 네트워크 토폴로지를 정의합니다.

### 2.1 네트워크 토폴로지 (Bus Topology)
![Network Topology](02_Network_Topology.puml)

### 2.2 통신 프로토콜 매핑
| 채널 | 프로토콜 | 속도 | 연결 ECU | 용도 |
|------|----------|------|----------|------|
| **LIN** | LIN 2.2A (ISO 17987) | 19.2 kbps | BCM(Master) ↔ WindowMotorECU / DoorModule ×4(Slave) | Fault Detection 출발점 — Motor 전류 및 Door 상태 수집 |
| **CAN-LS** | CAN 2.0B | 125kbps | BCM ↔ Gateway ↔ Tester | BCM Fault 전파, UDS 진단 통신 |
| **CAN-HS** | CAN 2.0B | 500kbps | Gateway ↔ Cluster | 경고등 제어 (Fault 메시지 라우팅) |
| **Ethernet** | DoIP (ISO 13400-2) | 100Mbps | OTA Server ↔ Gateway | 대용량 펌웨어 고속 전송 |

---

## 3. Signal Flow / Sequence (Scenario)
> **"데이터가 어떻게 흐르는가?"** — 핵심 시나리오(E2E)의 데이터 흐름을 정의합니다.

### 3.1 E2E 시나리오: Fault Detection → Diagnostics → OTA Update
![Process Sequence](02_Process_Sequence.puml)

### 3.2 시나리오 단계별 상세
0. **LIN 초기화 및 통신 이상 감지** (Scene.1~2c): 모든 ECU 초기화 후 WindowMotorECU(0x21) 10ms 주기 LIN 정상 수신 확인. 이후 LIN 프레임 50ms 이상 미수신 시뮬레이션 → BCM이 DTC U0100 생성 (H-01 / Req_018). LIN 복구 후 정상 통신 재개 확인.
1. **Fault Detection** (Scene.3~5): WindowMotorECU(LIN Slave 0x21)가 Motor_Current > 50A를 LIN으로 BCM에 보고 → BCM(LIN Master)이 DTC B1234 생성 → BCM_FaultStatus(0x500) CAN-LS 전송 → Gateway가 CAN-HS로 라우팅(≤5ms) → Cluster RED 경고등 활성화(≤50ms).
2. **Diagnostics** (Scene.7~9): Tester가 UDS 진단 서비스(0x10→0x19→0x14)를 통해 DTC를 확인하고 소거(Clear)하면 경고등이 소등됩니다.
3. **OTA Update** (Scene.10~17): OTA Server가 DoIP Routing Activation 후 UDS Programming Session(0x10 0x02)을 열고 0x34→0x36×N→0x37 순서로 펌웨어를 전송합니다. CRC-32 검증 통과 시 BCM을 재시작합니다. 실패 시 Rollback / Bus Off 시 세션 안전 중단.

---

## 4. HARA (Hazard Analysis and Risk Assessment) 요약
> **Safety Goals**: SG-01 (ASIL-B) — Motor 과전류 즉시 감지 및 안전 상태 전환 / SG-02 (ASIL-B) — OTA 실패 시 이전 펌웨어 자동 복구

| ID | Hazard | Operational Situation | Severity | Exposure | Controllability | ASIL | Safety Goal |
|----|--------|-----------------------|----------|----------|-----------------|------|-------------|
| H-01 | LIN 통신 오류로 Motor 과전류 미감지 → 윈도우 모터 과열/화재 → 운전자 부상 | 주행/정차 중 윈도우 조작 시 | S2 | E3 | C2 | **B** | SG-01: LIN Motor_Current 수신 이상 시 BCM이 즉시 과전류를 감지하고 안전 상태로 전환한다 (FTTI ≤50ms) |
| H-02 | OTA 중 통신 두절로 ECU Bricking | 펌웨어 업데이트 중 | S1 | E2 | C3 | **QM** | N/A — Rollback(Req_014)으로 완화. 안전목표 없음. |
| H-03 | OTA 업데이트 실패로 BCM 불능 → 차량 Body 기능 상실 | OTA 펌웨어 전송 중 (전원 차단 / CRC 오류) | S2 | E3 | C2 | **B** | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 |

---

## 5. Verification Environment
> **"어떻게 검증하는가?"**

*   **Tool**: Vector CANoe (SIL - Software In the Loop)
*   **Language**: CAPL (Communication Access Programming Language)
*   **Network**: Virtual CAN / Virtual Ethernet (Local Loopback)
*   **Panel**: 가상 스위치/LED를 통한 사용자 인터랙션 및 Fault Injection

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 |
| 1.1 | 2026-02-19 | HARA 정합성 — H-03 추가 (OTA 실패 ASIL-B), H-01/H-02 위험 설명 표준화, SG-01/SG-02 텍스트 통일 |
| 1.2 | 2026-02-19 | 섹션 3.2 시나리오 단계 0 추가 — LIN 초기화 및 통신 이상 감지 (Scene.1~2c, Req_018 / H-01) 추적성 반영 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
