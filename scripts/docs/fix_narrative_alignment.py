#!/usr/bin/env python3
"""
fix_narrative_alignment.py
==========================
V-Model 문서 주제 방향성 정합 스크립트
핵심: Fault Injection → Diagnostics → OTA 시나리오를 00~12 문서 전체에 Red Thread로 연결

변경 원칙:
- 기존 내용 삭제 없이 추가(append/insert) 방식
- REQ-001~055 유지 + REQ-056~059 신규 추가
- ISO 26262/ASPICE 무결성 보존
"""

import os
import re
from pathlib import Path

BASE = Path("/Users/juns/code/work/mobis/PBL/MentoringResult/V-Model_준수")

MASTER_SCENARIO_BOX = """
---

## 🔴 핵심 검증 시나리오 — Master E2E Scenario (Red Thread)

> 본 프로젝트의 모든 문서는 아래 시나리오를 중심 실(Red Thread)로 연결됩니다.
> ASPICE SYS.2는 "시나리오 기반 요구사항 도출"을 명시합니다.

```
[Phase 1] Fault Injection (고장 주입)
  BCM (Body Domain, CAN-LS)
    └─ Window Motor Overcurrent 감지 (50A > 정상 5A)
    └─ DTC B1234 저장 (ISO 14229 DTC Format)
    └─ BCM_FaultStatus CAN 메시지 전송 (CAN-LS, 0x500)

[Phase 2] Gateway Routing & Cluster Warning (중앙 게이트웨이 라우팅)
  Central Gateway (CGW)
    └─ CAN-LS 수신 (BCM_FaultStatus 0x500)
    └─ CAN-HS2 라우팅 → vECU (0x500 → CAN-HS2 broadcast)
    └─ Ethernet/DoIP 경로 제공 → OTA 서버 연결 (ISO 13400)
  vECU (CAN-HS2)
    └─ Cluster 경고등 활성화 (Warning Priority: P0)
    └─ DTC 이력 내부 기록

[Phase 3] UDS Diagnostics (진단 통신)
  CANoe Tester (CAPL 기반 진단 노드)
    └─ UDS 0x10 0x03 (Extended Diagnostic Session) → BCM
    └─ UDS 0x19 0x02 (Read DTC by Status Mask) → DTC B1234 수집
    └─ TCP/IP → 가상 OTA 서버 전송 (DTC 데이터 패킷)

[Phase 4] OTA Update (무선 업데이트)
  OTA Server (CANoe 가상 노드, Ethernet)
    └─ SW 버전 분석 → 업데이트 결정
    └─ UDS 0x10 0x02 (Programming Session) → BCM
    └─ UDS 0x34 (Request Download, 64KB)
    └─ UDS 0x36 × N (Transfer Data, 4KB/block)
    └─ UDS 0x37 (Transfer Exit)
    └─ BCM 재시작 → DTC 소거 → 정상 복귀 검증
```

**적용 표준**: ISO 14229-1 UDS, ISO 13400-2 DoIP, ISO 26262-4 (Safety), ASPICE PAM 3.1

---
"""


def fix_item_definition():
    """
    Item Definition:
    1. CAN Gateway: Out of Scope → In Scope (검증 대상 라우팅 인프라)
    2. F-05 설명에 UDS 0x10 Session Control 추가
    3. F-06 설명에 UDS 0x10 0x02 (Programming Session) 명시
    4. 시스템 경계 다이어그램 뒤에 Master E2E Scenario 섹션 추가
    5. Zonal 아키텍처 맥락 Note 추가
    """
    path = BASE / "00_Concept_Phase/00_Item_Definition.md"
    content = path.read_text(encoding="utf-8")

    # 1. Gateway Out of Scope → In Scope
    old = "4. **CAN Gateway** - 물리적 Gateway ECU (별도 공급사)"
    new = "4. **Central Gateway (CGW)** - 차량 네트워크 라우팅 허브 (**검증 대상**: CAN-LS/HS1/HS2 간 메시지 라우팅, DoIP OTA 경로)"
    if old in content:
        content = content.replace(old, new)
        print("  ✅ Gateway Out→In Scope 변경 완료")
    else:
        print("  ⚠️ Gateway Out of Scope 텍스트 미발견")

    # 2. F-05 UDS 0x10 추가
    old2 = "| **F-05** | Diagnostic Services | UDS 0x14, 0x19 진단 서비스 |"
    new2 = "| **F-05** | Diagnostic Services | UDS **0x10** (Session Control), **0x14** (Clear DTC), **0x19** (Read DTC) 진단 서비스 |"
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ F-05 UDS 0x10 추가 완료")

    # 3. F-06 Programming Session 명시
    old3 = "| **F-06** | OTA Update | UDS 0x34/0x36/0x37 OTA 업데이트 |"
    new3 = "| **F-06** | OTA Update | UDS **0x10 0x02** (Programming Session), **0x34** (Download), **0x36** (Transfer), **0x37** (Exit) |"
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ F-06 Programming Session 추가 완료")

    # 4. Master E2E Scenario 섹션 추가 (시스템 경계 다이어그램 뒤)
    marker = "### 4.2 외부 인터페이스 (External Interfaces)"
    if marker in content and "Master E2E Scenario" not in content:
        insert = MASTER_SCENARIO_BOX + "\n"
        content = content.replace(marker, insert + marker)
        print("  ✅ Master E2E Scenario 섹션 추가 완료")

    # 5. Zonal 아키텍처 맥락 Note 추가 (개정이력 앞)
    zonal_note = """
---

## 12. 산업 아키텍처 맥락 (Industry Architecture Context)

| 단계 | 아키텍처 | 특징 | 상태 |
|------|---------|------|------|
| 과거 | 분산 Domain ECU | 도메인별 독립 CAN 버스 | Legacy |
| **현재 (본 프로젝트)** | **Central Gateway 중심** | **CGW가 모든 도메인 중재, OTA/Diagnostics 허브** | **✅ 적용** |
| 미래 | Zonal Controller 기반 | 차량을 물리적 Zone으로 나눠 Zonal ECU가 국소 제어 | SDV 방향 |

> **본 프로젝트는 Central Gateway 중심 아키텍처**를 채택합니다.
> Gateway가 CAN-LS (BCM), CAN-HS2 (vECU), Ethernet (OTA Server) 를 연결하는
> 통합 진단/OTA 허브 역할을 수행하며, 이는 Zonal 전환 준비 단계에서도 동일하게 활용됩니다.

"""
    if "산업 아키텍처" not in content:
        content = content.replace("## 11. 개정 이력", zonal_note + "## 11. 개정 이력")
        print("  ✅ 산업 아키텍처 맥락 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Item Definition 수정 완료: {path}")


def fix_hara():
    """
    HARA:
    H-08: OTA 업데이트 중 전원 차단으로 vECU SW 손상 (ASIL-B)
    H-09: Gateway 라우팅 오류로 진단 통신 불가 (ASIL-A)
    SG-08: OTA 무결성 보장 (ASIL-A)
    """
    path = BASE / "00_Concept_Phase/01_Hazard_Analysis_Risk_Assessment.md"
    content = path.read_text(encoding="utf-8")

    new_hazards = """

---

## 9. 추가 위험 요소 — 진단/OTA 시나리오 (v2.1 추가)

> **HARA v2.1**: Fault Injection → Diagnostics → OTA 핵심 시나리오에서 식별된 추가 위험

### H-08: OTA 업데이트 중 전원 차단으로 vECU 소프트웨어 손상

| 항목 | 내용 |
|------|------|
| **위험 요소** | OTA 프로그래밍 세션(UDS 0x36 Transfer) 중 배터리 전원 차단 |
| **운영 상황** | 주차 중 OTA 업데이트 진행 (OM-05 OTA Mode) |
| **위험 이벤트** | vECU/BCM 펌웨어 반부팅 상태 — 기능 전체 손실 |
| **심각도 (S)** | S2 (중등도 부상 가능 — 이후 주행 시 안전 기능 미작동) |
| **노출도 (E)** | E1 (매우 낮음 — OTA는 드물게 발생) |
| **제어가능성 (C)** | C2 (보통 — 사용자가 업데이트 중 시동 회피 가능) |
| **ASIL** | **ASIL-A** (S2/E1/C2) |
| **안전 목표** | SG-08: OTA 업데이트 중단 시 자동 Rollback으로 기능 복구 |

### H-09: Central Gateway 라우팅 오류로 진단 통신 경로 차단

| 항목 | 내용 |
|------|------|
| **위험 요소** | CGW의 CAN-LS ↔ CAN-HS2 라우팅 테이블 오류 또는 CAN Bus Off |
| **운영 상황** | 주행 중 또는 정차 중 진단 통신 시도 |
| **위험 이벤트** | DTC 전파 실패 → 결함 은폐 → 안전 관련 고장 미감지 |
| **심각도 (S)** | S1 (경미한 부상) |
| **노출도 (E)** | E2 (낮음) |
| **제어가능성 (C)** | C2 (보통) |
| **ASIL** | **QM** (S1/E2/C2) — Quality Requirement로 관리 |
| **안전 목표** | SG-09: Gateway 라우팅 오류 감지 및 진단 가용성 보장 |

### 추가 Safety Goals (v2.1)

| SG ID | Safety Goal | ASIL | 관련 위험 |
|-------|------------|------|---------|
| **SG-08** | OTA 업데이트 중단 시 자동 Rollback 수행 → 기능 손실 방지 | ASIL-A | H-08 |
| **SG-09** | Gateway 라우팅 가용성 보장 → 진단 채널 연속성 확보 | QM | H-09 |

"""
    if "H-08" not in content:
        # 문서 끝에 추가
        if "## 9." in content:
            # 이미 9번 섹션이 있으면 다른 번호 사용
            new_hazards = new_hazards.replace("## 9. 추가 위험", "## 10. 추가 위험")
        content = content.rstrip() + new_hazards
        print("  ✅ HARA H-08/H-09 추가 완료")
    else:
        print("  ⚠️ H-08 이미 존재")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ HARA 수정 완료: {path}")


def fix_fsc():
    """
    FSC:
    FSR-B04: Central Gateway 가용성 (OTA 세션 중 라우팅 연속성)
    FSR-QM02: OTA 통신 무결성 (Rollback 보장)
    Traceability 업데이트
    """
    path = BASE / "00_Concept_Phase/02_Functional_Safety_Concept.md"
    content = path.read_text(encoding="utf-8")

    new_fsrs = """

---

### 3.5 추가 FSR — 진단/OTA 시나리오 (v2.1)

#### FSR-B04: Central Gateway 가용성 (SG-09 → QM / 강화 적용)

- **Safety Goal**: SG-09 — Gateway 라우팅 오류 감지 및 진단 가용성 보장
- **System Requirement**: REQ-058 (Gateway OTA Path)
- **ASIL**: QM (강화: 시스템 신뢰성을 위해 ASPICE 레벨 관리)
- **Description**: Central Gateway는 CAN-LS (BCM Domain), CAN-HS2 (Infotainment Domain),
  Ethernet (OTA Server) 간 메시지 라우팅 연속성을 보장해야 한다.
  라우팅 오류 감지 시 Fail-Safe 진단 채널로 전환해야 한다.
- **Safe State**: 직접 CAN 연결(Gateway Bypass) 또는 DTC 저장 후 대기
- **Verification**: Gateway Fault Injection (CAN Bus Off 시나리오), CANoe 시뮬레이션

#### FSR-QM02: OTA 통신 무결성 (SG-08 → ASIL-A)

- **Safety Goal**: SG-08 — OTA 업데이트 중단 시 자동 Rollback
- **System Requirement**: REQ-014 (OTA 실패 자동복구), REQ-059 (E2E 시나리오)
- **ASIL**: ASIL-A
- **FTTI**: N/A (OTA는 OM-05 정차 모드에서만 동작)
- **Description**: UDS 프로그래밍 세션(0x10 0x02) 시작 후 0x37 Transfer Exit 완료 전
  전원 차단, 타임아웃, CRC 오류 발생 시 시스템은 자동으로 이전 정상 펌웨어로 Rollback해야 한다.
- **Safe State**: 이전 펌웨어 복구 완료 + DTC 기록
- **Verification**: OTA 중단 시나리오 테스트 (10회 반복, 100% Rollback 성공)

"""
    if "FSR-B04" not in content:
        # QM FSR 섹션 뒤에 추가
        marker = "## 4. 예비 아키텍처 가정"
        if marker in content:
            content = content.replace(marker, new_fsrs + "\n" + marker)
        else:
            content = content.rstrip() + new_fsrs
        print("  ✅ FSC FSR-B04/QM02 추가 완료")

    # Traceability 테이블 업데이트
    old_trace = "| QR-01 (OTA) | QM | — | REQ-014 | TC-SYS-014 |"
    new_trace = (old_trace + "\n"
                 "| SG-08 (OTA Rollback) | ASIL-A | FSR-QM02 | REQ-014, REQ-059 | TC-SYS-012 |\n"
                 "| SG-09 (GW 가용성) | QM | FSR-B04 | REQ-058 | TC-SYS-011 |")
    if old_trace in content and "SG-08" not in content:
        content = content.replace(old_trace, new_trace)
        print("  ✅ FSC Traceability 테이블 업데이트 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ FSC 수정 완료: {path}")


def fix_srs():
    """
    System Requirements Specification:
    1. 문서 서두에 Master E2E Scenario 박스 추가
    2. REQ-010 BDC → BCM 수정
    3. REQ-056~059 신규 추가
    4. 총 요구사항 수 55 → 59 업데이트
    """
    path = BASE / "01_System_Requirements/01_SYS2_System_Requirements_Specification.md"
    content = path.read_text(encoding="utf-8")

    # 1. Master Scenario 박스를 문서 상단에 추가
    scenario_header = MASTER_SCENARIO_BOX + "\n---\n\n"
    if "Master E2E Scenario" not in content:
        marker = "## 1. 요구사항 개요"
        content = content.replace(marker, scenario_header + marker)
        print("  ✅ SRS Master Scenario 박스 추가 완료")

    # 2. REQ-010 BDC → BCM
    content = content.replace(
        "### REQ-010: BDC FaultInjection DTC생성",
        "### REQ-010: BCM FaultInjection DTC생성"
    )
    content = content.replace(
        "BDC ECU 통신 오류 또는 센서 이상 상황을 인위적으로 주입했을 때",
        "BCM (Body Control Module) ECU 통신 오류 또는 센서 이상 상황을 인위적으로 주입했을 때"
    )
    print("  ✅ REQ-010 BDC→BCM 수정 완료")

    # 3. 총 요구사항 수 업데이트
    content = content.replace("**총 요구사항**: 55개", "**총 요구사항**: 59개 (REQ-001~055 기존 + REQ-056~059 시나리오 보강)")

    # 4. 카테고리 분포 업데이트
    old_cat = "| 기능 요구사항 (Functional) | 36 | D: 2, C: 4, B: 23, A: 1 |"
    new_cat = ("| 기능 요구사항 (Functional) | 36 | D: 2, C: 4, B: 23, A: 1 |\n"
               "| **시나리오 요구사항 (Scenario/E2E)** | **4** | **B: 2, A: 1, QM: 1** |")
    if old_cat in content and "시나리오 요구사항" not in content:
        content = content.replace(old_cat, new_cat)
        print("  ✅ 요구사항 카테고리 업데이트 완료")

    # 5. REQ-056~059 추가 (Auto-generated 참조 앞에)
    new_reqs = """
---

### REQ-056: UDS Session Control — Diagnostic/Programming Session 전환

- **Category**: 시나리오 요구사항 (Scenario — Diagnostics)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 진단 Tester는 UDS 0x10 서비스를 통해 ECU의 진단 세션을 전환해야 한다.
  Default Session(0x01) → Extended Session(0x03) → Programming Session(0x02) 전환이 가능해야 하며,
  각 세션 전환은 Positive Response(0x50) 또는 Negative Response(0x7F + NRC)로 응답해야 한다.
  세션 타임아웃(P3=5000ms) 초과 시 Default Session으로 자동 복귀해야 한다.
- **Verification Method**: SIL (CANoe CAPL Tester), Unit Test
- **Related Systems**: Diagnostics (진단), Central Gateway
- **Traceability**: FSR-B03, SG-06 → TC-SWQUAL-301

---

### REQ-057: UDS Read DTC Information — DTC 수집 및 전송

- **Category**: 시나리오 요구사항 (Scenario — Diagnostics)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 진단 Tester는 UDS 0x19 서비스를 통해 BCM에 저장된 DTC 정보를 수집해야 한다.
  서브함수: 0x02 (Read DTC by Status Mask), 0x06 (Read DTC Extended Data),
  0x09 (Read DTC with Snapshot). 수집된 DTC는 TCP/IP를 통해 가상 OTA 서버로 전송되어야 한다.
  BCM에 DTC B1234 (Window Motor Overcurrent) 주입 시 0x19 0x02 응답에 포함되어야 한다.
- **Verification Method**: SIL (CANoe CAPL Tester), Fault Injection Test
- **Related Systems**: Diagnostics (진단), Central Gateway
- **Traceability**: FSR-B03, SG-06 → TC-SWQUAL-302

---

### REQ-058: Central Gateway OTA Path — DoIP 연결을 통한 OTA 서버 통신

- **Category**: 시나리오 요구사항 (Scenario — Gateway/OTA)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: QM (Gateway routing은 OTA 품질 관리 범위)
- **Description**: Central Gateway는 CAN-LS (BCM Domain) 메시지를 수신하여
  CAN-HS2 (vECU)로 라우팅하고, 동시에 Ethernet/DoIP (ISO 13400-2)를 통해
  가상 OTA 서버와 연결되는 경로를 제공해야 한다.
  CANoe 환경에서는 CAPL TCP/IP 소켓으로 OTA 서버를 모사(Mocking)한다.
  Gateway 라우팅 지연: CAN-LS → CAN-HS2 ≤ 5ms, CAN → DoIP 변환 ≤ 10ms.
- **Verification Method**: SIL (CANoe 3-Bus Simulation), Integration Test
- **Related Systems**: Central Gateway, OTA Update, CAN Communication
- **Traceability**: FSR-B04, SG-09 → TC-SYS-011

---

### REQ-059: E2E Scenario Regression Coverage — 전 시나리오 자동화 검증

- **Category**: 시나리오 요구사항 (Scenario — E2E)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM
- **Description**: CANoe 환경에서 Fault Injection → Diagnostics → OTA Update의 전체 시나리오를
  단일 자동화 테스트 스크립트로 반복 실행할 수 있어야 한다.
  시나리오 총 소요 시간: < 120초. 회귀 테스트(Regression) 목적으로 반복 실행 가능해야 하며,
  Pass/Fail 결과를 자동으로 로깅해야 한다. (CI/CD 연계 가능)
- **Verification Method**: SIL Automation (CANoe Test Module)
- **Related Systems**: All (E2E)
- **Traceability**: SG-08, QR-01 → TC-SYS-013

---

"""
    # Auto-generated 참조 앞에 삽입
    marker_auto = "**Auto-generated from**:"
    if marker_auto in content and "REQ-056" not in content:
        content = content.replace(marker_auto, new_reqs + marker_auto)
        print("  ✅ REQ-056~059 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ SRS 수정 완료: {path}")


def fix_tsc():
    """
    Technical Safety Concept:
    TSR-B04: Gateway Protocol Translation Safety Requirement
    """
    path = BASE / "01_System_Requirements/03_SYS3_Technical_Safety_Concept.md"
    if not path.exists():
        print("  ⚠️ TSC 파일 없음, 건너뜀")
        return

    content = path.read_text(encoding="utf-8")

    tsr_addition = """

---

## TSR-B04: Central Gateway Protocol Translation 안전 요구사항

- **Source FSR**: FSR-B04
- **ASIL**: QM (ASPICE 레벨 관리)
- **Allocation**: Central Gateway ECU

### 기술 안전 요구사항

| TSR ID | 요구사항 | 검증 기준 |
|--------|---------|---------|
| **TSR-B04-01** | CAN-LS ↔ CAN-HS2 메시지 변환 지연 ≤ 5ms | CANoe Trace 타임스탬프 측정 |
| **TSR-B04-02** | CAN → DoIP 변환 지연 ≤ 10ms | TCP/IP 패킷 타임스탬프 |
| **TSR-B04-03** | 메시지 손실률 < 0.001% (1,000,000 메시지 중 < 10개) | 장시간 부하 테스트 |
| **TSR-B04-04** | DoIP 연결 실패 시 Graceful Abort (OTA 세션 정상 종료) | Fault Injection: TCP 연결 차단 |
| **TSR-B04-05** | Gateway CAN Bus Off 시 Fail-Safe: DTC 저장 후 대기 | CAN Bus Off 주입 테스트 |

### CANoe 검증 환경

```
[CANoe Simulation]
  Node: BCM_Sim (CAPL) → CAN-LS 0x500 BCM_FaultStatus
  Node: CGW_Sim (CAPL) → CAN-LS 수신 → CAN-HS2 라우팅
                        → TCP/IP 소켓 → OTA_Server_Sim
  Node: vECU_Sim (CAPL) → CAN-HS2 수신 → Cluster 경고
  Node: OTA_Server_Sim (CAPL/.NET) → DoIP 수신 → UDS OTA
```

"""
    if "TSR-B04" not in content:
        content = content.rstrip() + tsr_addition
        print("  ✅ TSC TSR-B04 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ TSC 수정 완료: {path}")


def fix_system_architecture():
    """
    System Architecture:
    1. Central Gateway 역할 강화 섹션 추가
    2. OTA Server 외부 시스템 추가
    3. Alternative Architecture 테이블에 Gateway 선택 근거 강화
    """
    path = BASE / "02_System_Architecture/01_SYS3_System_Architectural_Design.md"
    content = path.read_text(encoding="utf-8")

    gw_section = """

---

## 2.1 Central Gateway 아키텍처 역할 (핵심)

> Central Gateway는 단순 메시지 라우터가 아닌 **통합 진단/OTA 허브**입니다.

| 역할 | 설명 | 관련 시나리오 |
|------|------|------------|
| **Multi-Bus Routing** | CAN-LS (BCM) ↔ CAN-HS2 (vECU) ↔ CAN-HS1 (Powertrain) | 모든 CAN 메시지 중재 |
| **Diagnostics Bridge** | CAN-based UDS ↔ DoIP (ISO 13400-2) 프로토콜 변환 | Phase 3: UDS Diagnostics |
| **OTA Path Provider** | Ethernet/DoIP를 통한 OTA 서버 ↔ BCM 경로 제공 | Phase 4: OTA Update |
| **Firewall** | 허가되지 않은 도메인 간 메시지 차단 (보안) | 사이버보안 요구사항 |
| **Network Monitor** | 버스 부하 모니터링, Bus Off 감지 | FSR-B03, FSR-B04 |

### 외부 시스템 연결 (검증 범위)

```
[Internal — In Scope]
  CAN-LS:   BCM, BDC, HVAC, Door Controllers
  CAN-HS1:  EMS, TCU, ESP, MDPS
  CAN-HS2:  vECU, IVI, Cluster, Camera, Radar, SCC

  Central Gateway (CGW) — 검증 허브
      │
      ├─[CAN-LS/HS1/HS2] 내부 도메인 라우팅
      │
      └─[Ethernet/DoIP] OTA Server (CANoe 가상 노드)

[External — CANoe 가상화]
  OTA Server: CAPL TCP/IP 소켓으로 모사
  Diagnostic Tester: CANoe CAPL Tester Node
```

### Zonal Architecture 전환 맥락

```
현재 (본 프로젝트): Central Gateway 중심
  → CGW = 단일 라우팅 허브, Domain ECU 간 중재

미래 (SDV / Zonal):
  → Zonal Controller가 물리적 Zone 내 ECU를 직접 관리
  → Central에서 Zonal로 권한 위임 구조
  → 본 프로젝트의 OTA/Diagnostics 흐름은 Zonal에서도 동일하게 적용
```

"""
    if "Central Gateway 아키텍처 역할" not in content:
        marker = "## 3. Safety Architecture"
        if marker in content:
            content = content.replace(marker, gw_section + "\n" + marker)
            print("  ✅ Central Gateway 역할 강화 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ System Architecture 수정 완료: {path}")


def fix_network_topology():
    """
    Network Topology:
    1. Ethernet/DoIP 행 추가
    2. ASCII 다이어그램에 Ethernet 경로 추가
    3. Gateway Routing Table DoIP 행 추가
    4. OTA 통신 경로 상세 섹션 추가
    """
    path = BASE / "02_System_Architecture/04_SYS3_Network_Topology.md"
    content = path.read_text(encoding="utf-8")

    # 1. Network 테이블에 Ethernet 행 추가
    old_table = "| **CAN-LS** | Low-Speed | 125 kbps | Body | 6 | ~15% |"
    new_table = (old_table + "\n"
                 "| **Ethernet** | DoIP (ISO 13400) | 100 Mbps | OTA Server (외부) | 1 | ~5% |")
    if old_table in content and "Ethernet" not in content:
        content = content.replace(old_table, new_table)
        print("  ✅ Ethernet/DoIP 네트워크 행 추가 완료")

    # 2. ASCII 다이어그램에 Ethernet 추가
    old_diag = "CAN-LS (125 kbps):\n Built-in ├─ BCM ─┬─ Lighting ─┬─ HVAC ─┬─ Doors ─┬─ CGW  Built-in"
    new_diag = (old_diag + "\n\nEthernet/DoIP (100 Mbps):\n"
                " CGW ──────────────────────────────── OTA Server (CANoe 가상 노드)")
    if old_diag in content and "OTA Server" not in content:
        content = content.replace(old_diag, new_diag)
        print("  ✅ ASCII 다이어그램 Ethernet 경로 추가 완료")

    # 3. Gateway Routing Table DoIP 행 추가
    old_fw = "**Firewall**: Gateway에서 불필요한 메시지 필터링 (보안)"
    doip_routing = """| CAN-LS | Ethernet (DoIP) | BCM DTC, OTA UDS 메시지 | 포트 기반 (13400) |
| Ethernet (DoIP) | CAN-LS | OTA 펌웨어 데이터 (0x36 블록) | DoIP Entity ID |

"""
    if "DoIP" not in content:
        content = content.replace(old_fw, doip_routing + old_fw)
        print("  ✅ Gateway Routing DoIP 행 추가 완료")

    # 4. OTA 통신 경로 상세 섹션 추가
    ota_path_section = """

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

"""
    if "OTA 통신 경로 상세" not in content:
        content = content.rstrip() + ota_path_section
        print("  ✅ OTA 통신 경로 상세 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Network Topology 수정 완료: {path}")


def fix_comm_spec():
    """
    Communication Specification:
    1. UDS 서비스 테이블 추가
    2. DoIP 메시지 테이블 추가
    """
    path = BASE / "02_System_Architecture/05_SYS3_Communication_Specification.md"
    content = path.read_text(encoding="utf-8")

    uds_section = """

---

## 5. UDS 서비스 사양 (ISO 14229-1 기반)

> **핵심 시나리오** Fault Injection → Diagnostics → OTA에서 사용하는 UDS 서비스 정의

| SID | 서비스 이름 | 서브함수 | 방향 | 시나리오 단계 | CANoe 구현 |
|-----|-----------|---------|------|------------|-----------|
| **0x10** | Session Control | 0x01 Default / 0x02 Programming / 0x03 Extended | Tester→ECU | Phase 3,4 | CAPL `diagRequest` |
| **0x14** | Clear DTC | 0xFFFFFF (All DTCs) | Tester→ECU | Phase 3 | CAPL `diagRequest` |
| **0x19** | Read DTC Info | 0x02 By Status / 0x06 Extended Data / 0x09 Snapshot | Tester→ECU | Phase 3 | CAPL `diagRequest` |
| **0x22** | Read Data by ID | 0xF101 SW Version / 0xF189 App Fingerprint | Tester→ECU | Phase 3 | CAPL `diagRequest` |
| **0x34** | Request Download | compressionMethod, memoryAddress | OTA→ECU | Phase 4 | CAPL + .NET |
| **0x36** | Transfer Data | blockSequenceCounter, transferRequestParameter | OTA→ECU | Phase 4 | CAPL + .NET |
| **0x37** | Transfer Exit | — | OTA→ECU | Phase 4 | CAPL + .NET |
| **0x7F** | Negative Response | NRC: 0x22 conditionsNotCorrect / 0x78 requestCorrectlyReceived | ECU→Tester | 전체 | 자동 처리 |

### UDS 타이밍 파라미터 (ISO 14229-1 Table C.1)

| 파라미터 | 값 | 설명 |
|---------|-----|------|
| P2 | 50ms | ECU 응답 대기 (Default) |
| P2* | 5000ms | ECU 응답 대기 (Extended, suppressPositiveResponse 이후) |
| P3 | 5000ms | 다음 요청 전 최대 대기 (세션 타임아웃) |

---

## 6. DoIP 메시지 사양 (ISO 13400-2 기반)

> Central Gateway ↔ OTA Server 간 Ethernet 통신 사양

| PayloadType | 이름 | 방향 | 용도 |
|-------------|------|------|------|
| **0xE001** | Routing Activation Request | OTA Server → CGW | DoIP 세션 초기화 |
| **0xE002** | Routing Activation Response | CGW → OTA Server | 연결 확인 (0x10=OK) |
| **0xE004** | Diagnostic Message | OTA Server ↔ ECU (via CGW) | UDS 메시지 캡슐화 |
| **0xE005** | Diagnostic Message Positive ACK | ECU → OTA Server | UDS 응답 정상 수신 |
| **0xE006** | Diagnostic Message Negative ACK | ECU → OTA Server | UDS 응답 오류 |

### CANoe DoIP 설정

```
CANoe Network: Ethernet (100BASE-TX)
Server IP: 192.168.1.100 (OTA Server 가상 노드)
ECU IP: 192.168.1.10 (Central Gateway)
Port: 13400 (DoIP 표준)
Logical Address BCM: 0x0010
```

"""
    if "UDS 서비스 사양" not in content:
        content = content.rstrip() + uds_section
        print("  ✅ Communication Spec UDS/DoIP 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Communication Spec 수정 완료: {path}")


def fix_sw_qual_test():
    """
    SW Qualification Test Plan:
    TC-SWQUAL-301~306 UDS/OTA 테스트 케이스 추가
    """
    path = BASE / "09_SW_Qualification_Test/01_Software_Qualification_Test_Plan.md"
    if not path.exists():
        print("  ⚠️ SW Qual Test Plan 없음, 건너뜀")
        return

    content = path.read_text(encoding="utf-8")

    uds_tcs = """

---

## 4. UDS/OTA 소프트웨어 자격 테스트 (E2E 시나리오 기반)

> **추가 배경**: REQ-056~059 (시나리오 요구사항) 검증을 위한 SW 레벨 테스트

### TC-SWQUAL-301: UDS 0x10 Session Control 검증

- **Requirement**: REQ-056 (UDS Session Control)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe SIL (CAPL Tester Node)
- **Test Steps**:
  1. Default Session (0x10 0x01) 전송 → Positive Response (0x50 0x01) 확인
  2. Extended Session (0x10 0x03) 전송 → Positive Response (0x50 0x03) 확인
  3. Programming Session (0x10 0x02) 전송 → Positive Response (0x50 0x02) 확인
  4. 세션 타임아웃 (P3=5000ms 경과) → Default Session 자동 복귀 확인
  5. 잘못된 서브함수 (0x10 0x05) 전송 → NRC 0x7F 0x10 0x12 확인
- **Pass Criteria**: 모든 세션 전환 성공, NRC 정확, 타임아웃 복귀 동작
- **CANoe Trace**: 타임스탬프 및 Response Code 로깅

---

### TC-SWQUAL-302: UDS 0x19 Read DTC Information 검증

- **Requirement**: REQ-057 (UDS Read DTC)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe SIL (Fault Injection + CAPL Tester)
- **Test Steps**:
  1. Fault Injection: BCM Window Motor Overcurrent (50A) 주입
  2. BCM DTC B1234 저장 확인 (내부 DTC 메모리)
  3. UDS 0x19 0x02 (statusMask=0x09) 전송
  4. Response에 DTC B1234 포함 확인
  5. UDS 0x19 0x06 (Extended Data) 전송 → 발생 횟수, 타임스탬프 확인
  6. UDS 0x14 0xFFFFFF (Clear DTC) → 0x19 0x02 재조회 → DTC 없음 확인
- **Pass Criteria**: DTC B1234 정확 검출, Clear 후 소거 확인

---

### TC-SWQUAL-303: OTA Programming Session 전체 시퀀스

- **Requirement**: REQ-012~014, REQ-059 (OTA E2E)
- **ASIL**: ASIL-B (OTA 경로 무결성)
- **Test Environment**: CANoe SIL (OTA Server 가상 노드)
- **Test Steps**:
  1. UDS 0x10 0x02 (Programming Session) → 0x50 0x02 확인
  2. UDS 0x34 (Request Download: memAddr=0x0800, size=64KB) → 0x74 확인
  3. UDS 0x36 × 16 (Transfer Data: blockSeq=01~10, 4KB/block)
  4. UDS 0x37 (Transfer Exit) → 0x77 확인
  5. UDS 0x11 0x01 (ECU Reset) → BCM 재시작
  6. 재시작 후 DTC B1234 소거 확인 (0x19 0x02 → 빈 응답)
- **Pass Criteria**: 전체 시퀀스 성공, 펌웨어 버전 변경 확인 (0x22 0xF101)

---

### TC-SWQUAL-304: UDS Timing Validation

- **Requirement**: REQ-056, REQ-059
- **Test Environment**: CANoe SIL (Timestamp Measurement)
- **Test Steps**:
  1. 0x10 0x03 전송 → 응답 시간 측정 (P2 = 50ms 이내 확인)
  2. suppressPositiveResponse 설정 → 0x10 0x03 0x80 → P2* 확인 (응답 없음)
  3. 연속 10회 측정 → 평균 응답 시간 < 30ms, 최대 < 50ms
- **Pass Criteria**: P2 준수율 100% (10/10)

---

### TC-SWQUAL-305: OTA 중단 시나리오 (Rollback 검증)

- **Requirement**: REQ-014 (OTA 실패 자동복구), FSR-QM02
- **ASIL**: ASIL-A (Rollback 안전성)
- **Test Environment**: CANoe SIL (Fault Injection: 전원 차단 시뮬레이션)
- **Test Steps**:
  1. OTA Programming Session 시작 (0x10 0x02)
  2. 0x36 3번째 블록 전송 중 ECU Reset 강제 주입 (Fault Injection)
  3. 재부팅 후 이전 펌웨어 버전 확인 (0x22 0xF101 → 이전 버전)
  4. 기능 정상 동작 확인 (조명/경고 기능 All Pass)
  5. DTC B0201 (OTA Failure) 저장 확인
- **Pass Criteria**: 10회 중 10회 Rollback 성공 (100%), 기능 정상 복구
- **Repeat**: 10회 반복 (ISO 26262-6 통계적 신뢰도)

---

### TC-SWQUAL-306: Gateway Protocol Translation 검증

- **Requirement**: REQ-058 (Gateway OTA Path)
- **Test Environment**: CANoe SIL (3-Bus: CAN-LS, CAN-HS2, Ethernet)
- **Test Steps**:
  1. BCM_FaultStatus (CAN-LS 0x500) 전송
  2. CGW가 CAN-HS2로 라우팅 → vECU 수신 확인 (지연 ≤ 5ms)
  3. CGW가 Ethernet DoIP 0xE004 전송 → OTA Server 수신 확인 (지연 ≤ 10ms)
  4. 100% 메시지 도달률 확인 (1000개 전송)
  5. CGW CAN Bus Off 주입 → Graceful Abort 및 DTC 저장 확인
- **Pass Criteria**: 지연 기준 100% 준수, 메시지 손실 0개

"""
    if "TC-SWQUAL-301" not in content:
        content = content.rstrip() + uds_tcs
        print("  ✅ SW Qual Test Plan TC-SWQUAL-301~306 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ SW Qualification Test Plan 수정 완료: {path}")


def fix_sys_integration_test():
    """
    System Integration Test Plan:
    INT-006: E2E Master Scenario 추가
    """
    path = BASE / "10_System_Integration_Test/01_SYS4_System_Integration_Test_Plan.md"
    content = path.read_text(encoding="utf-8")

    e2e_tc = """
---

### INT-006: E2E Master Scenario — Fault → Diagnostics → OTA Complete Chain

- **Requirement**: REQ-010, REQ-056, REQ-057, REQ-058, REQ-059, REQ-012~014
- **ASIL**: ASIL-B (전체 경로)
- **Test Environment**: CANoe SIL (3-Bus + Ethernet + CAPL Tester + OTA Server)
- **Test Duration**: < 120초 (자동화 실행 기준)

#### Phase 1: Fault Injection (T=0~10s)
1. CANoe Interaction Layer: `BCM_Window_Current = 50` (50A 주입)
2. BCM_Sim: Overcurrent 감지 → DTC B1234 저장 (내부 메모리)
3. BCM_FaultStatus CAN 메시지 전송 시작 (CAN-LS 0x500, 100ms)
4. **검증**: BCM DTC 저장 타임스탬프 < 200ms

#### Phase 2: Gateway Routing & Cluster Warning (T=10~20s)
5. CGW: CAN-LS 수신 → CAN-HS2 라우팅 (≤5ms)
6. vECU: BCM_FaultStatus 수신 → Cluster 경고등 활성화
7. CGW: Ethernet DoIP 연결 → OTA_Server_Sim 수신 확인
8. **검증**: Cluster 경고등 T=15s 이전 활성화

#### Phase 3: UDS Diagnostics (T=20~60s)
9. CAPL Tester: UDS 0x10 0x03 (Extended Session) → BCM
10. CAPL Tester: UDS 0x19 0x02 (Read DTC) → DTC B1234 수신 확인
11. CAPL Tester: UDS 0x19 0x06 (Extended Data) → 발생 횟수 확인
12. TCP/IP: DTC 데이터 → OTA_Server_Sim 전송
13. **검증**: DTC B1234 정확 수신, TCP 전송 성공

#### Phase 4: OTA Programming (T=60~120s)
14. OTA_Server_Sim: UDS 0x10 0x02 (Programming Session)
15. OTA_Server_Sim: UDS 0x34 (Request Download, 64KB)
16. OTA_Server_Sim: UDS 0x36 × 16 (Transfer Data)
17. OTA_Server_Sim: UDS 0x37 (Transfer Exit)
18. BCM 재시작 (UDS 0x11)
19. CAPL Tester: UDS 0x19 0x02 재조회 → DTC B1234 없음 확인
20. **검증**: 펌웨어 버전 변경 확인 (0x22 0xF101)

- **Pass Criteria**:
  - ✅ 전 4개 Phase 연속 성공
  - ✅ 총 소요 시간 < 120초
  - ✅ DTC B1234: 생성 → 수집 → OTA 후 소거 전 과정 확인
  - ✅ 메시지 손실 0개 (CANoe Trace 검증)
  - ✅ 자동화 스크립트로 반복 실행 가능 (3회 연속 성공)

"""
    if "INT-006" not in content:
        # Test Coverage 섹션 앞에 추가
        marker = "## 3. Test Coverage"
        if marker in content:
            content = content.replace(marker, e2e_tc + "\n" + marker)
        else:
            content = content.rstrip() + e2e_tc
        print("  ✅ System Integration Test INT-006 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ System Integration Test 수정 완료: {path}")


def fix_sys_qual_test():
    """
    System Qualification Test Plan:
    TC-SYS-010~013 추가
    """
    path = BASE / "11_System_Qualification_Test/01_SYS5_System_Qualification_Test_Plan.md"
    if not path.exists():
        print("  ⚠️ Sys Qual Test Plan 없음, 건너뜀")
        return

    content = path.read_text(encoding="utf-8")

    sys_diag_tcs = """
---

### 3.5 TC-SYS-010: UDS Diagnostic Session — System Level (REQ-056)

**Test Objective**: 전체 시스템에서 UDS 세션 전환 검증 (모든 ECU)
**Test Setup**: HIL (23 ECU 시뮬레이터 + Real CGW)
**Test Steps**:
1. Diagnostic Tester: 0x10 0x03 → BCM, vECU, Cluster 각각 전송
2. 모든 ECU 응답 확인 (0x50 0x03)
3. 세션 중 차량 시동 OFF → 모든 ECU Default Session 복귀 확인
**Pass Criteria**: 모든 ECU 응답, 시동 OFF 복귀 100%

---

### 3.6 TC-SYS-011: E2E DTC Propagation — BCM → GW → vECU → Cluster (REQ-057, REQ-058)

**Test Objective**: DTC 발생부터 Cluster 경고등까지 전체 경로 검증
**Test Setup**: HIL + CANoe (CAN-LS, CAN-HS2, Ethernet 통합)
**Test Steps**:
1. BCM Fault Injection: Window Motor Overcurrent
2. DTC 저장 → CAN-LS 전송 → CGW 라우팅 → CAN-HS2 → vECU → Cluster
3. 각 경로 지연 측정 (CANoe Trace)
4. OTA Server 수신 확인 (Ethernet/DoIP)
**Pass Criteria**: 전체 경로 지연 < 50ms, 경고등 활성화 확인, OTA Server 수신

---

### 3.7 TC-SYS-012: OTA Programming Session — System Level (REQ-012~014, REQ-059)

**Test Objective**: 실차 수준 OTA 업데이트 전 과정 시스템 검증
**Test Setup**: HIL + CANoe OTA Server (DoIP)
**Test Steps**:
1. OTA Server: DoIP 연결 → UDS 0x10 0x02 → 0x34 → 0x36×16 → 0x37
2. BCM 재시작 → 기능 정상 확인
3. 조명/경고/ADAS UI 기능 All Pass 확인 (All 55 requirements regression)
4. OTA 실패 시나리오: Phase 4 중단 → Rollback 확인
**Pass Criteria**: OTA 성공 100%, 기능 회귀 0, Rollback 성공

---

### 3.8 TC-SYS-013: Fault → Diag → OTA Regression Suite (REQ-059)

**Test Objective**: E2E Master Scenario 자동화 회귀 테스트
**Test Setup**: HIL 완전 자동화 (CANoe Test Module)
**Test Steps**: INT-006 시나리오 3회 연속 자동 실행
**Pass Criteria**: 3/3 성공, 평균 소요 시간 < 120초, Pass/Fail 자동 리포트 생성

"""
    if "TC-SYS-010" not in content:
        marker = "## 4. Safety Validation Tests"
        if marker in content:
            content = content.replace(marker, sys_diag_tcs + "\n" + marker)
        else:
            content = content.rstrip() + sys_diag_tcs
        print("  ✅ System Qualification Test TC-SYS-010~013 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ System Qualification Test 수정 완료: {path}")


def fix_safety_validation():
    """
    Safety Validation Plan:
    OTA/Diagnostics 안전 검증 섹션 추가
    """
    path = BASE / "12_Safety_Validation/01_Safety_Validation_Plan.md"
    if not path.exists():
        # 두 번째 파일 이름 시도
        path = BASE / "12_Safety_Validation/01_Safety_Validation_Report.md"
    if not path.exists():
        print("  ⚠️ Safety Validation 파일 없음, 건너뜀")
        return

    content = path.read_text(encoding="utf-8")

    ota_validation = """

---

## OTA/Diagnostics 안전 검증 (v2.1 추가)

### SV-08: OTA 업데이트 안전성 검증 (SG-08, ASIL-A)

| 검증 항목 | 시나리오 | 기준 | 검증 방법 |
|---------|---------|------|---------|
| **OTA 중단 Rollback** | OTA 0x36 3번째 블록 전송 중 강제 차단 | 10/10 Rollback 성공 | HIL Fault Injection |
| **악성 패키지 거부** | CRC 불일치 펌웨어 전송 | 100% 거부, DTC 저장 | CANoe SIL |
| **전원 차단 복구** | Programming Session 중 배터리 차단 | 이전 버전 자동 복구 | HIL (배터리 시뮬레이터) |
| **OTA 완료 기능 회귀** | OTA 성공 후 전체 기능 자동 테스트 | 모든 55 REQ 통과 | CANoe Automation |

### SV-09: Gateway 진단 가용성 검증 (SG-09, QM)

| 검증 항목 | 시나리오 | 기준 | 검증 방법 |
|---------|---------|------|---------|
| **Gateway Routing 연속성** | CAN-LS Bus Off 주입 중 진단 시도 | Graceful Abort + DTC | CANoe CAN Error Frame |
| **DoIP 연결 복구** | Ethernet 케이블 단락 후 재연결 | 30초 이내 재연결 | HIL Network Fault |
| **Gateway 라우팅 지연** | 고부하 (90% Bus Load) 상황 | ≤ 5ms 유지 | CANoe Bus Load Test |

### E2E 안전 검증 시나리오 (SV-E2E-001)

```
검증 목적: 핵심 시나리오 전체 흐름의 안전성 확인

시나리오:
  Step 1. BCM 고장 발생 (Window Motor DTC B1234)
  Step 2. Cluster 경고등 < 50ms 활성화 검증
  Step 3. UDS 진단으로 DTC 수집 (0x19 0x02)
  Step 4. OTA 업데이트 완료
  Step 5. 모든 안전 기능 정상 복귀 확인

합격 기준:
  ✅ Cluster 경고등 FTTI < 1000ms (SG-06 FSR-B03)
  ✅ OTA 성공률 100% (10회/10회)
  ✅ OTA 후 Safety 기능 회귀 없음
  ✅ Rollback 성공률 100% (실패 시나리오 10회)
```

"""
    if "OTA/Diagnostics 안전 검증" not in content:
        content = content.rstrip() + ota_validation
        print("  ✅ Safety Validation OTA/Diag 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Safety Validation 수정 완료: {path}")


def fix_traceability_matrix():
    """
    Traceability Matrix:
    REQ-056~059 행 추가
    E2E Master Scenario 섹션 추가
    """
    path = BASE / "99_Supporting_Processes/01_Traceability_Matrix.md"
    content = path.read_text(encoding="utf-8")

    new_rows = """
| **REQ-056** | UDS Session Control | ASIL-B | TC-SYS-010, TC-SWQUAL-301 | SWE5/SWE6/SYS5 | SG-06 |
| **REQ-057** | UDS Read DTC | ASIL-B | TC-SYS-011, TC-SWQUAL-302 | SWE5/SWE6/SYS5 | SG-06 |
| **REQ-058** | Gateway OTA Path | QM | TC-SYS-011, TC-SWQUAL-306 | SYS4/SYS5 | SG-09 |
| **REQ-059** | E2E Scenario Coverage | QM | TC-SYS-013, INT-006 | SYS4/SYS5 | QR-01 |
"""

    # 마지막 REQ 행 뒤에 추가
    old_last_req = "| **REQ-055** |"
    if old_last_req in content and "REQ-056" not in content:
        # REQ-055 행 전체를 찾아서 그 뒤에 추가
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "| **REQ-055** |" in line:
                lines.insert(i + 1, new_rows.strip())
                break
        content = "\n".join(lines)
        print("  ✅ Traceability Matrix REQ-056~059 추가 완료")

    # E2E Master Scenario 섹션 추가
    e2e_matrix = """

---

## E2E Master Scenario 추적성

| 시나리오 단계 | 관련 REQ | 관련 FSR | 테스트 케이스 | 문서 |
|------------|---------|---------|------------|------|
| Phase 1: Fault Injection | REQ-010 | FSR-B03 | INT-006 Ph.1, TC-SWQUAL-302 | 00_HARA, 01_SRS |
| Phase 2: Gateway Routing | REQ-058 | FSR-B04 | INT-006 Ph.2, TC-SWQUAL-306 | 02_Architecture |
| Phase 3: UDS Diagnostics | REQ-056, REQ-057 | FSR-B03 | INT-006 Ph.3, TC-SWQUAL-301~302 | 02_CommSpec |
| Phase 4: OTA Update | REQ-012~014, REQ-059 | FSR-QM02 | INT-006 Ph.4, TC-SWQUAL-303~305 | 01_SRS |
| E2E Regression | REQ-059 | — | TC-SYS-013, SV-E2E-001 | 12_SafetyVal |

"""
    if "E2E Master Scenario 추적성" not in content:
        content = content.rstrip() + e2e_matrix
        print("  ✅ Traceability Matrix E2E 섹션 추가 완료")

    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Traceability Matrix 수정 완료: {path}")


def main():
    print("=" * 60)
    print("V-Model 주제 방향성 정합 — Narrative Alignment")
    print("핵심: Fault Injection → Diagnostics → OTA Red Thread")
    print("=" * 60)

    print("\n[1/11] Item Definition 수정 (Gateway In Scope, Master Scenario)...")
    fix_item_definition()

    print("\n[2/11] HARA 수정 (H-08/09 추가)...")
    fix_hara()

    print("\n[3/11] FSC 수정 (FSR-B04/QM02 추가)...")
    fix_fsc()

    print("\n[4/11] SRS 수정 (REQ-056~059, BDC→BCM 수정)...")
    fix_srs()

    print("\n[5/11] Technical Safety Concept 수정 (TSR-B04 추가)...")
    fix_tsc()

    print("\n[6/11] System Architecture 수정 (Gateway 역할 강화)...")
    fix_system_architecture()

    print("\n[7/11] Network Topology 수정 (DoIP 경로 추가)...")
    fix_network_topology()

    print("\n[8/11] Communication Spec 수정 (UDS/DoIP 사양 추가)...")
    fix_comm_spec()

    print("\n[9/11] SW Qualification Test 수정 (TC-SWQUAL-301~306)...")
    fix_sw_qual_test()

    print("\n[10/11] System Integration Test 수정 (INT-006 E2E)...")
    fix_sys_integration_test()

    print("\n[11/11] System Qualification Test + Safety Validation 수정...")
    fix_sys_qual_test()
    fix_safety_validation()
    fix_traceability_matrix()

    print("\n" + "=" * 60)
    print("✅ Narrative Alignment 완료!")
    print("=" * 60)
    print("\n📊 변경 요약:")
    print("  - Item Definition: Gateway In Scope, Master Scenario 추가")
    print("  - HARA: H-08/09 (OTA/Gateway 위험) 추가")
    print("  - FSC: FSR-B04 (Gateway), FSR-QM02 (OTA Rollback) 추가")
    print("  - SRS: REQ-056~059 추가, BDC→BCM 수정, 55→59개")
    print("  - TSC: TSR-B04 (Gateway Protocol Translation) 추가")
    print("  - Architecture: Central Gateway 역할 강화, Zonal 맥락")
    print("  - Network Topology: Ethernet/DoIP 경로 추가")
    print("  - Comm Spec: UDS 서비스 테이블, DoIP 메시지 추가")
    print("  - SW Qual Test: TC-SWQUAL-301~306 (UDS/OTA) 추가")
    print("  - System Integration: INT-006 (E2E Master Scenario) 추가")
    print("  - System Qual Test: TC-SYS-010~013 추가")
    print("  - Safety Validation: OTA/Diag 안전 검증 추가")
    print("  - Traceability: REQ-056~059 + E2E 섹션 추가")


if __name__ == "__main__":
    main()
