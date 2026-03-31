# canoe-driving-alert 프로젝트 관리 가이드

> **Hyundai Mobis Bootcamp × Vector Korea**
> ISO 26262 & ASPICE 준수 프로젝트 운영 매뉴얼

---

## 📋 목차

1. [프로젝트 구조 이해하기](#1-프로젝트-구조-이해하기)
2. [V-Model 개발 프로세스](#2-v-model-개발-프로세스)
3. [V-Model 산출물 관리](#3-v-model-산출물-관리)
4. [CANoe 개발 가이드](#4-canoe-개발-가이드)
5. [코드 작성 가이드 (CAPL)](#5-코드-작성-가이드-capl)
6. [형상 관리](#6-형상-관리)
7. [품질 보증](#7-품질-보증)
8. [안전 관리 (ISO 26262)](#8-안전-관리-iso-26262)

---

## 1. 프로젝트 구조 이해하기

### 1.1 핵심 디렉토리 구조

```
canoe-driving-alert/
├── canoe/                        # CANoe 프로젝트 파일
│   ├── cfg/                      # CANoe 설정 (.cfg)
│   │   └── IVI_OTA_Project.cfg
│   ├── databases/                # DBC 파일
│   │   └── vehicle_system.dbc   ← 핵심 CAN DB
│   ├── nodes/                    # CAPL 노드 (.can) ← 개발 예정
│   │   ├── BCM_Sim.can          (BCM-Fault 시뮬레이션)
│   │   ├── CGW_Sim.can          (GW-Routing 브리지)
│   │   ├── Tester_Sim.can       (UDS Tester 시나리오)
│   │   └── OTA_Server_Sim.can   (OTA Update 서비스)
│   ├── panels/                   # CANoe 패널 (.xvp)
│   ├── environments/             # 채널 매핑, 하드웨어 설정
│   ├── test_modules/             # 테스트 모듈 (TFS)
│   └── logging/                  # 로그 설정 (.blf, .asc)
├── docs/                         # 프로젝트 문서
│   ├── V-Model/
│   │   └── 준수/                 # V-Model 산출물 (46개)
│   │       ├── 00_Concept_Phase/
│   │       ├── 01_System_Requirements/
│   │       ├── 02_System_Architecture/
│   │       ├── 03_Software_Requirements/
│   │       ├── 04_Software_Architecture/
│   │       ├── 05_Software_Detailed_Design/
│   │       ├── 06_Implementation/
│   │       ├── 07_Unit_Test/
│   │       ├── 08_SW_Integration_Test/
│   │       ├── 09_SW_Qualification_Test/
│   │       ├── 10_System_Integration_Test/
│   │       ├── 11_System_Qualification_Test/
│   │       ├── 12_Safety_Validation/
│   │       └── 99_Supporting_Processes/
│   └── meeting-notes/            # 멘토 미팅 노트
├── reference/                    # 참조 자료
│   ├── legacy/                   # 구 CAPL 노드 (재사용 참고)
│   │   └── capl_nodes/
│   │       ├── BCM.can
│   │       └── CGW.can
│   └── samples/                  # 멘토 제공 샘플
├── reports/                      # 보고서 산출물
├── scripts/                      # 유틸리티 스크립트 (Python, Batch)
├── Concept_design.drawio         # 시스템 설계 다이어그램 (7페이지)
├── .claude/CLAUDE.md             # AI 컨텍스트 (내부 운영용)
├── CHANGELOG.md                  # 변경 이력 (Keep a Changelog 방식)
├── CONTRIBUTING.md               # 기여 가이드
└── README.md                     # 프로젝트 개요
```

### 1.2 핵심 시나리오 (Red Thread)

모든 문서와 코드는 이 흐름을 중심으로 작성됩니다:

```
BCM (CAN-LS 0x500 — BCM_FaultStatus)
  Window Motor Overcurrent (50A) → DTC B1234 저장 → CAN-LS 전송
      ↓
Central Gateway (CGW)
  CAN-LS → CAN-HS2 라우팅 (≤5ms)
  + Ethernet/DoIP → OTA 서버 경로 (ISO 13400-2)
      ↓
vECU (IVI Virtual ECU)
  Cluster 경고등 활성화 (FTTI < 50ms, REQ-F03)
      ↓
CANoe Tester (CAPL)
  UDS 0x10 0x03 (Extended Session) → BCM
  UDS 0x19 0x02 (Read DTC) → DTC B1234 수신
      ↓
OTA Server (CANoe 가상 노드)
  UDS 0x10 0x02 (Programming Session)
  UDS 0x34 → 0x36 × N → 0x37 (Download → Transfer → Exit)
  BCM 재시작 → DTC 소거 확인
```

### 1.3 핵심 DBC 메시지 사양

| CAN ID | 메시지명 | 주기 | ASIL | 물리 신호 예시 |
|--------|---------|------|------|------|
| 0x500 | `BCM_FaultStatus` | 10ms | B | `WindowMotorOvercurrent` (bool), `DTC_Code` (int) |
| 0x501 | `BCM_DoorStatus` | 20ms | QM | `DoorOpenStatus_FL` (bool) |
| 0x420 | `vECU_WarningUI` | 50ms | D | `Warning_Type` (int), `Warning_Active` (bool) |

---

## 2. V-Model 개발 프로세스

### 2.1 V-Model 단계별 산출물 구조

```
요구사항 정의 (SYS.2) ──────────────────────────→ 시스템 검증 (SYS.6)
     ↓                                             ↑
시스템 아키텍처 (SYS.3) ──────────────────────→ 시스템 통합 테스트 (SYS.5)
     ↓                                             ↑
SW 요구사항 (SWE.1) ──────────────────────→ SW 적격성 테스트 (SWE.6)
     ↓                                             ↑
SW 아키텍처 (SWE.2) ──────────────────────→ SW 통합 테스트 (SWE.5)
     ↓                                             ↑
SW 상세 설계 (SWE.3) ─────────────────────→ SW 단위 테스트 (SWE.4)
     ↓                                             ↑
     └─────────────→ 구현 (CAPL 코딩) ──────────────┘
```

### 2.2 현 단계 진행 상황 (Baseline v1.2)

| 단계 | 주요 산출물 | 상태 |
|------|------------|------|
| SYS.2 | 시스템 요구사항 명세 (SRS) | ✅ 완료 (40개 REQ) |
| SYS.2 | HARA v3.0 | ✅ 완료 (H-01~H-10) |
| SYS.3 | 시스템 설계 (VHA/CBD/FBD/NET/SIG) | ✅ 완료 (drawio 7p) |
| SYS.3 | 통신 사양 (UDS/DoIP) | ✅ 완료 |
| SYS.5 | Safety Validation Report v2.1 | ✅ 완료 |
| SWE.3 | CAPL 노드 개발 (BCM/CGW/Test/OTA) | ⬜ 진행 예정 |

---

## 3. V-Model 산출물 관리

### 3.1 산출물 위치 및 파일명 규칙

**경로**: `docs/V-Model/준수/`

- **요구사항**: `01_System_Requirements/01_SYS2_System_Requirements_Specification.md`
- **아키텍처**: `02_System_Architecture/01_SYS3_System_Architectural_Design.md`
- **네트워크**: `02_System_Architecture/04_SYS3_Network_Topology.md`
- **DBC**: `canoe/databases/vehicle_system.dbc`

### 3.2 Concept_design.drawio 페이지 구조

| # | 페이지 이름 | 내용 | 주요 목적 |
|---|------------|------|----------|
| 1 | `REF_ConceptDesignOverview` | 전체 개요 | 컨텍스트 이해 |
| 2 | `REF_CANBusPrinciple` | CAN 원리 | 하드웨어 계층 이해 |
| 3 | `SYS3_VHA_VehicleArchitecture` | 차량 아키텍처 | 도메인/ECU 배치 |
| 4 | `SYS3_CBD_SystemFunctionalBlock` | 도메인 블록 | 논리적 기능 분할 (I-C-O) |
| 5 | `SYS3_FBD_FunctionalBlockDiagram` | 서비스 블록 | 서비스별 상세 Flow (I-C-O) |
| 6 | `SYS3_NET_CANBusTopology` | 네트워크 위상 | 실제 배선 및 버스 구성 |
| 7 | `SYS3_SIG_E2EServiceFlow` | 서비스 흐름 | 시퀀스 다이어그램 (신호 흐름) |

---

## 4. CANoe 개발 가이드

### 4.1 시뮬레이션 노드 구성

| 노드 | 소스 파일 | 주요 역할 |
|------|----------|----------|
| **BCM** | `BCM_Sim.can` | 결함 주입 시 DTC 생성 및 0x500 전송 |
| **CGW** | `CGW_Sim.can` | CAN-LS ↔ CAN-HS2 라우팅 및 DoIP 브리지 |
| **Tester** | `Tester_Sim.can` | 외부 진단기 역할 (UDS Service 호출) |
| **OTA Server** | `OTA_Server_Sim.can` | 소프트웨어 업데이트 서비스 관리 |

### 4.2 개발 예시 (CAPL)

#### **BCM 결함 시뮬레이션 로직**
```capl
/* BCM_Sim.can */
variables {
  message BCM_FaultStatus faultMsg; // 0x500
  msTimer tDiagnosticTimer;
}

on message WindowMotor_Control {
  if (this.CurrentDraw > 50) { // 50A 초과 시 과전류 판정
    faultMsg.WindowMotorOvercurrent = 1;
    faultMsg.DTC_Code = 0xB1234;
    output(faultMsg);
    setTimer(tDiagnosticTimer, 10);
  }
}
```

#### **CGW 라우팅 로직 (Latency ≤ 5ms 지향)**
```capl
/* CGW_Sim.can */
on message CAN1.BCM_FaultStatus {
  message BCM_FaultStatus hsMsg;
  hsMsg = this;
  output(CAN2, hsMsg); // CAN2 (HS2) 버스로 즉시 라우팅
}
```

---

## 5. 코드 작성 가이드 (CAPL)

### 5.1 명명 규칙 (Naming Convention)

- **전역 변수**: `g` 접두어 + CamelCase (예: `gDiagnosticStatus`)
- **지역 변수**: CamelCase (예: `currentValue`)
- **상수/매크로**: 전체 대문자 + 언더바 (예: `MAX_MOTOR_CURRENT`)
- **함수**: Verb + Noun 구성 (예: `SendWarningSignal()`)

### 5.2 ASIL 등급별 구현 주의사항

- **ASIL-D (Cluster/ADAS)**: Alive Counter 및 Checksum 필수 검증
- **ASIL-B (BCM/OTA)**: 주기 시간(Cycle Time) 모니터링 및 상호 감시 로직
- **QM (Generic IVI)**: 표준 로직 구현

---

## 6. 형상 관리 (Git Branching)

### 6.1 브랜치 전략

- **`main`**: 최종 멘토 제출용 (Stable)
- **`develop`**: 개발 통합용
- **`feature/xxx`**: 단위 기능 개발용 (예: `feature/bcm-uds`)
- **`hotfix/xxx`**: 긴급 오류 수정용

### 6.2 커밋 메시지 표준

```text
feat(nodes): add UDS 0x19 service to Tester_Sim.can
- Implement ReadDTCByStatusMask
- Map DTC B1234 to Cluster UI
- REQ-D02, REQ-F03 compliance
```

---

## 7. 품질 보증 (QA)

### 7.1 품질 게이트 (Quality Gate)

1. **Gate 1 (Requirement)**: SRS 40개 요구사항 확정 및 HARA 승인 ✅
2. **Gate 2 (Design)**: drawio 7페이지 설계서 및 DBC 설계 완료 ✅
3. **Gate 3 (Implementation)**: 모든 CAPL 노드 에러 없이 컴파일 완료 ⬜
4. **Gate 4 (Verification)**: E2E 시나리오(Fault→OTA) 시뮬레이션 성공 ⬜

### 7.2 테스트 시나리오 예시

| ID | 시나리오 명 | 예상 결과 |
|---|------------|----------|
| TS-01 | 과전류 결함 주입 | BCM에서 DTC B1234 생성 및 0x500 메시지 전송 확인 |
| TS-02 | GW 라우팅 지연 측정 | CAN-LS 전송 시점 대비 CAN-HS2 수신 시점 차이 ≤ 5ms |
| TS-03 | UDS 진단 세션 전환 | 0x10 0x03 호출 시 BCM이 0x50 positive response 반환 |

---

## 8. 안전 관리 (ISO 26262)

### 8.1 HARA 요약 표

| ID | 위험 원인 (Hazard) | ASIL | 안전 목표 (Safety Goal) |
|----|-------------------|-----|------------------------|
| H-01 | 모터 과전류 감지 실패 | B | 과전류 발생 시 100ms 내 차단 |
| H-03 | 클러스터 경고 표시 오류 | D | 안전 경고는 50ms 내 정확히 표시 |
| H-09 | OTA 업데이트 중 전원 차단 | B | 업데이트 중단 시 안전한 Rollback 보장 |
| H-10 | 게이트웨이 신호 유실 | A | 데이터 라우팅 무결성 유지 |

---
**Last Updated**: 2026-02-18
**Author**: Antigravity Project Agent
**Status**: Revised Detailed Version
