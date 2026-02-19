# V-Model 문서 매핑표 (V-Model Document Mapping)

**Document ID**: SAMPLE-00-VMM
**ISO 26262 Reference**: Part 4, Cl.6 / Part 6, Cl.7 / Part 4, Cl.10
**ASPICE Reference**: SYS.2 / SYS.3 / SWE.2 / SWE.4 / SWE.5 / SYS.5 / SUP.10
**Version**: 1.5
**Date**: 2026-02-19
**Status**: Released

---

## V-Model 전체 흐름도

```
[좌측: 설계/명세]                              [우측: 검증/테스트]
─────────────────────────────────────────────────────────────────
SYS.2  01_Requirements.md          ◄──────►  07_System_Test.md       SYS.5
  │                                                                     │
SYS.3  03_Function_definition.md   ◄──────►  06_Integration_Test.md  SWE.5
       0301_SysFuncAnalysis.md
       0302_NWflowDef.md
  │                                                                     │
SWE.2  0303_Communication_Spec.md  ◄──────►  05_Unit_Test.md         SWE.4
       0304_System_Variables.md
─────────────────────────────────────────────────────────────────
```

---

## 문서별 상세 매핑

| 문서 | V-Model 단계 | ASPICE | ISO 26262 | 역할 | 대응 테스트 문서 |
|------|------------|--------|-----------|------|----------------|
| `01_Requirements.md` | 시스템 요구사항 정의 | SYS.2 | Part 4, Cl.6 | 시스템이 무엇을 해야 하는가 정의 | `07_System_Test.md` |
| `03_Function_definition.md` | 시스템 아키텍처 설계 | SYS.3 | Part 4, Cl.7 | 기능을 어떤 노드가 담당하는가 정의 | `06_Integration_Test.md` |
| `0301_SysFuncAnalysis.md` | 시스템 아키텍처 설계 | SYS.3 | Part 4, Cl.7 | 노드별 기능 상세 분해 | `06_Integration_Test.md` |
| `0302_NWflowDef.md` | 시스템 아키텍처 설계 | SYS.3 | Part 4, Cl.7 | 메시지/신호 Tx/Rx 흐름 정의 | `06_Integration_Test.md` |
| `0303_Communication_Specification.md` | SW 아키텍처 설계 | SWE.2 | Part 6, Cl.7 | 신호 ID/DLC/Bit 상세 명세 | `05_Unit_Test.md` |
| `0304_System_Variables.md` | SW 아키텍처 설계 | SWE.2 | Part 6, Cl.7 | CANoe System Variables 정의 | `05_Unit_Test.md` |
| `05_Unit_Test.md` | SW 단위 테스트 | SWE.4 | Part 6, Cl.9 | 노드별 단일 기능 검증 | ← `03_Function_definition.md` |
| `06_Integration_Test.md` | SW 통합 테스트 | SWE.5 | Part 6, Cl.10 | 노드 간 연동 시나리오 검증 | ← `0301_SysFuncAnalysis.md` |
| `07_System_Test.md` | 시스템 적격성 테스트 | SYS.5 | Part 4, Cl.10 | E2E 전체 시나리오 검증 | ← `01_Requirements.md` |

---

## ASPICE 프로세스 참조

| ASPICE 프로세스 | 설명 | 해당 문서 |
|---------------|------|---------|
| SYS.2 | System Requirements Analysis — 시스템 요구사항 도출 및 분석 | `01_Requirements.md` |
| SYS.3 | System Architectural Design — 시스템 아키텍처 및 인터페이스 설계 | `03_Function_definition.md`, `0301~0302` |
| SWE.2 | Software Architectural Design — SW 아키텍처 및 인터페이스 설계 | `0303_Communication_Specification.md`, `0304_System_Variables.md` |
| SWE.4 | Software Unit Verification — SW 단위 검증 | `05_Unit_Test.md` |
| SWE.5 | Software Integration and Integration Test — SW 통합 테스트 | `06_Integration_Test.md` |
| SYS.5 | System Qualification Test — 시스템 적격성 테스트 | `07_System_Test.md` |

---

## ISO 26262 참조

| ISO 26262 조항 | 설명 | 해당 문서 |
|--------------|------|---------|
| Part 3, Cl.7 | HARA — 위험 분석 및 위험 평가 | `02_Concept_design.md` (섹션 4) + `00b_Project_Scope.md` (섹션 3) |
| Part 4, Cl.6 | System Requirements Specification | `01_Requirements.md` |
| Part 4, Cl.7 | System Design | `03_Function_definition.md`, `0301~0302` |
| Part 4, Cl.10 | System Integration and Testing | `07_System_Test.md` |
| Part 6, Cl.7 | Software Architectural Design | `0303_Communication_Specification.md`, `0304_System_Variables.md` |
| Part 6, Cl.9 | Software Unit Testing | `05_Unit_Test.md` |
| Part 6, Cl.10 | Software Integration Testing | `06_Integration_Test.md` |

---

## HARA 안전목표 추적성

| HARA 항목 | 위험 설명 | 안전목표 | 대응 요구사항 | 검증 Scene |
|----------|---------|--------|------------|-----------|
| H-01 | LIN 통신 오류로 Motor 과전류 미감지 → 윈도우 모터 과열/화재 → 운전자 부상 | SG-01: LIN Motor_Current 수신 이상 시 BCM이 즉시 과전류를 감지하고 안전 상태로 전환한다 (FTTI ≤50ms) | Req_001, Req_002, Req_003, **Req_016**, **Req_018** | Scene.2b, **Scene.2c**, Scene.3~5 / In_Test_15 (Req_018) |
| H-02 | OTA 중 통신 두절로 ECU Bricking | N/A — **QM** 등급. Rollback(Req_014)으로 완화. 안전목표 없음. | Req_014 (완화 수단) | Scene.15, Scene.17 |
| H-03 | OTA 업데이트 실패로 BCM 불능 → 차량 Body 기능 상실 | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 | Req_014, Req_015 | Scene.15~17 |

---

## 문서 추적성 매트릭스 (Traceability Matrix)

| Req. ID | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|---------|--------------|---------|-----------|-----------|------------|
| Req_001 | BCM ECU | CAN-LS 0x500 | BCM_FaultStatus | BCM-과전류 감지 | In_Test_01 | Scene.3 |
| Req_002 | BCM ECU | CAN-LS 0x500 | BCM_FaultStatus | BCM-FaultStatus 전송 | In_Test_01 | Scene.4 |
| Req_003 | Cluster ECU | CAN-HS 0x510 | Cluster_WarnStatus | Cluster-경고등 활성화 | In_Test_02 | Scene.5 |
| Req_004 | 가상 노드 | — | — | Fault Injection | In_Test_12 | Scene.3 |
| Req_005 | Gateway ECU | CAN-HS 0x500 | BCM_FaultStatus(라우팅) | Gateway-CAN 라우팅 | In_Test_03 | Scene.6 |
| Req_006 | Gateway ECU | CAN-HS 0x500 | — | Gateway-CAN 라우팅 | In_Test_03 | Scene.6 |
| Req_007 | Gateway ECU | DoIP 0xE001 | — | Gateway-DoIP 처리 | In_Test_04 | Scene.10 |
| Req_008 | Tester ECU | CAN-LS 0x7DF | UDS_Request | Tester-UDS 세션 전환 | In_Test_05 | Scene.7 |
| Req_009 | Tester ECU | CAN-LS 0x7DF/7E8 | UDS_Request/Response | Tester-DTC 조회 | In_Test_06 | Scene.8 |
| Req_010 | Tester ECU | CAN-LS 0x7DF | UDS_Request | Tester-DTC 클리어 | In_Test_07 | Scene.9 |
| Req_011 | OTA Server ECU | CAN-LS 0x7DF | UDS_Request | OTA-다운로드 요청 | In_Test_08 | Scene.11 |
| Req_012 | OTA Server ECU | CAN-LS 0x7DF | UDS_Request | OTA-블록 전송 | In_Test_08 | Scene.12~13 |
| Req_013 | OTA Server ECU | CAN-LS 0x7E8 | UDS_Response | OTA-전송 완료 | In_Test_09 | Scene.14 |
| Req_014 | OTA Server ECU | — | — | OTA-Rollback | In_Test_10 | Scene.15~17 |
| Req_015 | Gateway ECU | — | — | Gateway-Bus Off | In_Test_11 | Scene.16 |
| Req_016 | WindowMotorECU / BCM | LIN 0x21 | LIN_MotorStatus | BCM-LIN Motor Current 수신 | In_Test_13 | Scene.2b, Scene.3 |
| Req_017 | DoorModule / BCM | LIN 0x22~0x25 | LIN_DoorStatus | BCM-LIN Door Status 수신 | In_Test_14 | Scene.2b |
| Req_018 | BCM — LIN 통신 이상 감지 | LIN 0x21 | DTC U0100 | BCM-LIN 통신 이상 감지 | In_Test_15 | Scene.2c |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 — V-Model 매핑, ASPICE/ISO-26262 참조, HARA 추적성 매트릭스 |
| 1.1 | 2026-02-19 | H-02(QM) HARA 표 추가, SUP.10 개정 이력 신설 (교차검증 반영) |
| 1.2 | 2026-02-19 | In_Test_15 추적성 반영 — HARA H-01 검증 Scene 추가, 추적성 매트릭스 구현 파생 행 추가 |
| 1.3 | 2026-02-19 | Req_018 정식 등록 — 구현 파생 → 공식 요구사항 추적. H-01 대응 요구사항에 Req_018 추가 |
| 1.4 | 2026-02-19 | HARA 정합성 — H-09→H-03, SG-08→SG-02 재번호 (sample 독립 프로젝트 일련번호 정렬), H-01 위험 설명/SG-01 텍스트 표준화 |
| 1.5 | 2026-02-19 | Scene.2c 추가 — Req_018 시스템 테스트 추적성 완결 (추적성 매트릭스 및 HARA H-01 검증 Scene 업데이트) |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
