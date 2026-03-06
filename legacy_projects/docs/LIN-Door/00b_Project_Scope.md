# 프로젝트 범위 및 검증 전략 (Project Scope and Verification Strategy)

**Document ID**: SAMPLE-00b-PS
**ISO 26262 Reference**: Part 2, Cl.6 — 기능 안전 관리 계획 / Part 4, Cl.5 — 시스템 수준 개발 착수
**ASPICE Reference**: MAN.3 (BP1: 프로젝트 범위 정의), SYS.5 (BP1: 시스템 테스트 전략)
**Version**: 1.2
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 전체 — 프로젝트 범위 및 V&V 전략 | 전체 문서 참조 | Concept Design | `01_Requirements.md` |

---

## 1. 프로젝트 범위 (Project Scope)

본 프로젝트는 **Vector CANoe SIL(Software-in-the-Loop)** 환경에서 차량 통신 프로토콜(LIN / CAN-LS / CAN-HS / Ethernet/DoIP)을 활용한 BCM Fault Detection 및 OTA 검증 시스템을 구현한다.

**E2E 핵심 흐름 (Red Thread)**:

```
WindowMotorECU (LIN Slave 0x21)
  → Motor_Current > 50A 보고 (LIN 2.2A, 10ms 주기)
BCM (LIN Master)
  → DTC B1234 생성 + BCM_FaultStatus(0x500) CAN-LS 전송 (10ms)
Central Gateway
  → CAN-LS → CAN-HS 라우팅 (≤5ms)
Cluster
  → RED 경고등 활성화 (FTTI ≤50ms, ASIL-B)
Tester (CANoe)
  → UDS 0x10 0x03 (Extended Session)
  → UDS 0x19 0x02 (Read DTC B1234)
  → UDS 0x14 (Clear DTC)
OTA Server
  → DoIP Routing Activation (0xE001)
  → UDS 0x10 0x02 (Programming Session)
  → UDS 0x34 → 0x36×N → 0x37 (펌웨어 전송 + CRC-32 검증)
  → BCM 재시작 / Rollback (실패 시)
```

**대상 도메인**: Body (BCM + LIN Slaves) / Gateway / Infotainment (Cluster) / Diagnostics / OTA Connectivity

---

## 2. 검증 환경 (Verification Environment)

| 항목 | 내용 |
|------|------|
| 검증 도구 | Vector CANoe 17+ (SIL — Software-in-the-Loop) |
| 구현 언어 | CAPL (Communication Access Programming Language) |
| 네트워크 | LIN 2.2A (19.2kbps) / CAN-LS (125kbps) / CAN-HS (500kbps) / Ethernet DoIP (100Mbps) |
| 가상 노드 | WindowMotorECU / DoorModule×4 / BCM / Gateway / Tester / OTA Server / Cluster |
| 입력 인터페이스 | CANoe Panel — TrackBar (전류값 조절) / Switch (Fault Injection, OTA 트리거) / Indicator (상태 출력) |
| DBC | `canoe/databases/vehicle_system.dbc` |
| 구현 파일 | `canoe/nodes/` (CAPL 노드) / `canoe/test_modules/` (테스트 CAPL) |

**테스트 모듈 구성**:

| 모듈 | 대상 시나리오 |
|------|------------|
| `TC_L_LIN_Interface/` | LIN Motor Current / Door Status 수신 (In_Test_13, 14, 15) |
| `TC_F_Fault_Detection/` | Fault Injection → DTC 생성 자동화 (In_Test_01, 02, 12) |
| `TC_G_Gateway_Routing/` | 라우팅 지연 측정, DoIP 처리 (In_Test_03, 04) |
| `TC_D_UDS_Diagnostics/` | UDS 세션 / DTC 조회 / 클리어 (In_Test_05, 06, 07) |
| `TC_O_OTA_Programming/` | OTA 전송 / CRC / Rollback / Bus Off (In_Test_08~11) |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 (Scene.1~18) |

**E2E 시나리오 실행 순서**:

| 단계 | Scene | 내용 |
|------|-------|------|
| 초기화 | Scene.1~2c | ECU 초기화 + LIN 정상 통신 확인 + LIN 통신 이상 감지 |
| Fault Detection | Scene.3~5 | LIN Motor Current 55A → DTC B1234 → 경고등 |
| Gateway | Scene.6 | CAN-LS→CAN-HS 라우팅 ≤5ms |
| Diagnostics | Scene.7~9 | UDS Extended Session → DTC 조회 → 클리어 |
| OTA 준비 | Scene.10~11 | DoIP Routing Activation → Programming Session |
| OTA 전송 | Scene.12~14 | 0x34 → 0x36×N → 0x37 + CRC-32 검증 |
| 안전 복구 | Scene.15~17 | Rollback (CRC 불일치) + Bus Off 안전 중단 |
| 재검증 | Scene.18 | 전체 E2E 2회 연속 정상 동작 확인 |

---

## 3. HARA 안전목표 요약 (Safety Goal Summary)

> **참조**: HARA 추적성 매트릭스 전체는 `00_VModel_Mapping.md` — HARA 안전목표 추적성 섹션 참조

| HARA ID | 위험 설명 | ASIL | 안전목표 (Safety Goal) | 대응 요구사항 | 검증 |
|---------|---------|------|----------------------|------------|------|
| H-01 | LIN 통신 오류로 Motor 과전류 미감지 → 윈도우 모터 과열/화재 → 운전자 부상 | **ASIL-B** | SG-01: LIN Motor_Current 수신 이상 시 BCM이 즉시 과전류를 감지하고 안전 상태로 전환한다 (FTTI ≤50ms) | Req_001, Req_002, Req_003, Req_016, Req_018 | Scene.2b, Scene.2c, Scene.3~5, In_Test_15 |
| H-02 | OTA 중 통신 두절로 ECU Bricking | **QM** | N/A — 안전목표 없음. Rollback(Req_014)으로 완화. | Req_014 (완화 수단) | Scene.15, Scene.17 |
| H-03 | OTA 업데이트 실패로 BCM 불능 → 차량 Body 기능 상실 | **ASIL-B** | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 | Req_014, Req_015 | Scene.15~17 |

**최고 ASIL 등급**: ASIL-B — ASIL Decomposition 불필요

**ASIL 등급 근거**:

| ASIL | 해당 요구사항 | 근거 |
|------|------------|------|
| ASIL-B | Req_001~003, Req_014~016, Req_018 | H-01/H-03 Safety Goal 직접 대응 |
| ASIL-A | Req_005, Req_006 | Gateway Protocol Translation (안전 메시지 라우팅 타이밍) |
| QM | Req_004, Req_007~013, Req_017 | 안전목표와 무관한 진단/OTA 인프라/편의 기능 |

---

## 4. 적용 표준 (Applied Standards)

| 표준 | 버전 | 적용 범위 |
|------|------|---------|
| ISO 26262 | 2018 | 기능 안전 — HARA, ASIL 분류, V-Model, 요구사항 추적성 |
| Automotive SPICE PAM | 3.1 | 프로세스 개선 — SYS.2/3, SWE.2/4/5, SYS.5, SUP.10 |
| LIN 2.2A (ISO 17987) | — | LIN 통신 프레임 구조 및 이상 감지 (DTC U0100) |
| ISO 14229-1 (UDS) | — | UDS 서비스 (0x10 / 0x14 / 0x19 / 0x34 / 0x36 / 0x37) |
| ISO 13400-2 (DoIP) | — | OTA Server ↔ Gateway Ethernet 통신 |
| ISO 11898-1 (CAN) | — | CAN Bus Off 감지 및 복구 절차 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 — 프로젝트 범위, 검증 환경, HARA 요약, ASIL 근거, 적용 표준 |
| 1.1 | 2026-02-19 | HARA 정합성 — H-09→H-03, SG-08→SG-02 재번호 (sample 독립 프로젝트 일련번호 정렬), H-01 위험 설명 표준화 |
| 1.2 | 2026-02-19 | Scene.2c 추가 — H-01 검증 항목에 Req_018 시스템 테스트 Scene 반영 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
