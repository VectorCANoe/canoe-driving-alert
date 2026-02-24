# V-Model 문서 매핑표 (V-Model Document Mapping)

**Document ID**: PROJ-00-VMM
**ISO 26262 Reference**: Part 4, Cl.6 / Part 6, Cl.7 / Part 4, Cl.10
**ASPICE Reference**: SYS.2 / SYS.3 / SWE.2 / SWE.4 / SWE.5 / SYS.5 / SUP.10
**Version**: 3.0
**Date**: 2026-02-24
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
| H-01 | 위험 운전(과속/급가속/급제동/차선이탈) 미감지 → 경고 미발령 → 사고 → 운전자/보행자 부상 | SG-01: 위험 운전 감지 시 WDM_ECU가 50ms 이내 단계별 경고를 발령한다 (FTTI ≤50ms) | Req_B01~B09 (입력+판단), Req_B10~B13 (출력) | Scene.B3~B9 |
| H-02 | OTA 중 통신 두절로 ECU Bricking | N/A — **QM** 등급. Rollback(Req_O04)으로 완화. 안전목표 없음. | Req_O04 (완화 수단) | Scene.O4 |
| H-03 | OTA 실패로 토크 제한 ECU 불능 → 차량 구동계 기능 이상 | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 | Req_O04, Req_O05 | Scene.O4, O5 |

---

## 문서 추적성 매트릭스 (Traceability Matrix)

### Base — 입력층 (A+B)

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_B01 | 차량 동역학 신호 제공 | Vehicle_ECU | CAN-LS 0x100 | Vehicle_Speed / AccelValue / BrakeValue | 차속 CAN-LS 전송 | In_Test_01, In_Test_02 | Scene.B1~B5 |
| Req_B02 | 조향 및 차선변경 신호 제공 | MDPS_ECU | CAN-LS 0x110 | Steering_Status / LaneChangeAlert | 조향 CAN-LS 전송 | In_Test_03 | Scene.B1, B7, B8 |
| Req_B03 | 차선이탈 신호 제공 | LDW_ECU | CAN-LS 0x120 | LDW_Status | 차선이탈 CAN-LS 전송 | In_Test_03 | Scene.B1, B6 |

### Base — 판단층 (WDM_ECU)

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_B04 | 과속 감지 | WDM_ECU | CAN-HS 0x200 | WDM_Warning | 과속 플래그 설정 | In_Test_01 | Scene.B3 |
| Req_B05 | 급가속 감지 | WDM_ECU | CAN-LS 0x100 | AccelValue | 급가속 시뮬레이션 | In_Test_02 | Scene.B4 |
| Req_B06 | 급제동 감지 | WDM_ECU | CAN-LS 0x100 | BrakeValue | 급제동 시뮬레이션 | In_Test_02 | Scene.B5 |
| Req_B07 | 차선이탈 감지 판단 | WDM_ECU | CAN-LS 0x120 | LDW_Status | 차선이탈 감지 | In_Test_03 | Scene.B6 |
| Req_B08 | 급차선변경 감지 판단 | WDM_ECU | CAN-LS 0x110 | Steering_Status | 급차선변경 감지 | In_Test_03 | Scene.B7 |
| Req_B09 | 위험 단계 판단 규칙 | WDM_ECU | CAN-HS 0x200 | WDM_Warning | 1/2/3단계 경고 발령 | In_Test_01~04 | Scene.B3~B9 |

### Base — 출력층 (경고 시스템)

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_B10 | Cluster 경고등 제어 | Cluster_ECU | CAN-HS 0x200 | WarnLampLevel | 황색/적색 경고등 | In_Test_01~04 | Scene.B3~B9 |
| Req_B11 | Sound 경고음 발령 | Sound_ECU | CAN-HS 0x230 | Sound_Control | 단계별 경고음 | In_Test_01~04 | Scene.B3~B9 |
| Req_B12 | Ambient 기본 경고 패턴 | Ambient_ECU | CAN-HS 0x220 | Ambient_Control | AMBER파동/RED점멸 | In_Test_04 | Scene.B8, B9 |
| Req_B13 | IVI 기본 경고 정보 표시 | IVI_ECU | CAN-HS 0x240 | IVI_Status | 경고 레벨 표시 | In_Test_01~04 | Scene.B3~B9 |
### Base — 해제층

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_B15 | 응시 복귀 감지 → 경고 해제 | WDM_ECU | sysvar::Driver | GazeActive | 경고 해제 (응시) | In_Test_05 | Scene.B10 |
| Req_B16 | 핸들 입력 감지 → 경고 해제 | WDM_ECU + MDPS_ECU | CAN-LS 0x110 | Steering_Status | 경고 해제 (핸들) | In_Test_06 | Scene.B11 |

### Test Suite 1 — 준영 (구간 인식 + Ambient 연동)

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_Z01 | gRoadZone 구간 설정 | WDM_ECU | sysvar::gRoadZone | — | gRoadZone 변경 버튼 | In_Test_07~09 | Scene.Z1~Z4 |
| Req_Z02 | 스쿨존 Ambient RED 점멸 | Ambient_ECU | CAN-HS 0x220 | Ambient_Control | 스쿨존 RED 점멸 | In_Test_07 | Scene.Z1 |
| Req_Z03 | 고속도로 핸들 미입력 진동 경고 | Ambient_ECU + Door_ECU | CAN-HS 0x220, 0x250 | — | 고속도로 ORANGE 파동 | In_Test_08 | Scene.Z2 |
| Req_Z04 | IC출구 Ambient 방향 안내 | Ambient_ECU | CAN-HS 0x220 | Ambient_Control | IC출구 방향 애니메이션 | In_Test_09 | Scene.Z3 |

### Test Suite 2 — 성현 (Drive Coach + Smart Claim + Seasonal Theme)

| Req. ID | 요약 | 기능 정의 | 네트워크 플로우 | 통신 명세 | 단위 테스트 | 통합 테스트 | 시스템 테스트 |
|---------|------|---------|--------------|---------|-----------|-----------|------------|
| Req_O01 | Drive Coach Package OTA | WDM_ECU + IVI_ECU + OTA_Server | DoIP + Ethernet | UDS_Request | Drive Coach UDS 세션 | In_Test_10 | Scene.O1, O2 |
| Req_O02 | Smart Claim Telematics 활성화 | Python COM API + Flask 서버 | HTTP/Ethernet | — | Smart Claim 전송 | In_Test_11 | Scene.O3 |
| Req_O03 | Seasonal Theme OTA | OTA_Server | DoIP + Ethernet | UDS_Request | Seasonal Theme UDS 세션 | In_Test_12 | Scene.O4 |
| Req_O04 | OTA 실패 시 Rollback | OTA_Server | — | — | Rollback | In_Test_13 | Scene.O5 |
| Req_O05 | Bus Off 안전 중단 | CGW | — | — | Bus Off 중단 | In_Test_14 | Scene.O6 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — V-Model 매핑, ASPICE/ISO-26262 참조, HARA 추적성 매트릭스 (Req_001~018) |
| 2.0 | 2026-02-23 | 트레이서빌리티 매트릭스 전면 갱신 — Base(Req_B01~B16) / TS-준영(Req_Z01~Z04) / TS-성현(Req_O01~O05) 구조 반영. 매트릭스 계층별 섹션 분리. HARA 검증 Scene 갱신. |
| 3.0 | 2026-02-24 | Req_B05 단순화(gAccelCount 제거), Req_B14 삭제(도어잠금). TS-성현 매트릭스 갱신 — Drive Coach(Req_O01) / Smart Claim(Req_O02) / Seasonal Theme(Req_O03) / Rollback(Req_O04) / Bus Off(Req_O05). |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
