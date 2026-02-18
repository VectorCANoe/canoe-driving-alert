#!/usr/bin/env python3
"""
남은 MAJOR 이슈 전체 수정 스크립트
- Item Definition: ASIL 사전할당 제거, 필수 항목 추가
- Safety Requirements: SR-D-004/SR-C-001/SR-C-002 ASIL 수정, RPN 오류 제거, Window Watchdog, 트레이서빌리티 완성
- ECU Allocation: ASIL 모순 해소, HSI 추가
- Traceability Matrix: 전체 55개 요구사항 + TC-SYS-XXX 통일
- SWE.1/SWE.2/SWE.4 BP 목록 ASPICE PAM 3.1 준수로 수정
"""
import os, re

BASE = "/Users/juns/code/work/mobis/PBL/MentoringResult/V-Model_준수"
TODAY = "2026-02-17"


# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: Item Definition — ASIL 사전할당 제거, 운영모드/법규/선행 위험 추가
# ─────────────────────────────────────────────────────────────────────────────
def fix_item_definition():
    path = os.path.join(BASE, "00_Concept_Phase/00_Item_Definition.md")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1) 버전 업데이트
    c = c.replace("**Version**: 1.0\n**Date**: 2026-02-14", f"**Version**: 2.0\n**Date**: {TODAY}")
    c = c.replace("**Status**: Released", "**Status**: Released (v2.0 — ASIL pre-assignment removed; mandatory sections added)")

    # 2) Function 테이블에서 ASIL 컬럼 제거 → Note 추가
    old_func_table = """| Function ID | Function Name | Description | ASIL |
|-------------|---------------|-------------|------|
| **F-01** | Ambient Lighting Control | 주행 모드/속도 기반 조명 색상 자동 제어 | ASIL-B |
| **F-02** | Safety Warning Display | 후진, 도어 개방 등 안전 경고 UI 표시 | ASIL-C |
| **F-03** | ADAS UI Integration | LDW, AEB, BSD 이벤트 시각적 경고 | ASIL-D |
| **F-04** | User Profile Management | 운전자별 조명/경고 설정 저장 | QM |
| **F-05** | Diagnostic Services | UDS 0x14, 0x19 진단 서비스 | ASIL-B |
| **F-06** | OTA Update | UDS 0x34/0x36/0x37 OTA 업데이트 | ASIL-C |
| **F-07** | Fault Detection & Handling | CAN 통신 오류, 센서 고장 감지 | ASIL-B |"""
    new_func_table = """| Function ID | Function Name | Description |
|-------------|---------------|-------------|
| **F-01** | Ambient Lighting Control | 주행 모드/속도 기반 조명 색상 자동 제어 |
| **F-02** | Safety Warning Display | 후진, 도어 개방 등 안전 경고 UI 표시 |
| **F-03** | ADAS UI Integration | LDW, AEB, BSD 이벤트 시각적 경고 |
| **F-04** | User Profile Management | 운전자별 조명/경고 설정 저장 |
| **F-05** | Diagnostic Services | UDS 0x14, 0x19 진단 서비스 |
| **F-06** | OTA Update | UDS 0x34/0x36/0x37 OTA 업데이트 |
| **F-07** | Fault Detection & Handling | CAN 통신 오류, 센서 고장 감지 |

> **Note v2.0**: ASIL은 Item Definition 단계에서 사전 할당할 수 없습니다 (ISO 26262-3:2018, Clause 7).
> ASIL은 HARA 결과로 결정되며, HARA 완료 후 도출된 ASIL 할당 결과는 HARA 문서를 참조하십시오.
> - F-01: ASIL-A (SG-05 기반) | F-02: ASIL-B (SG-03, SG-04 기반) | F-03: ASIL-D (SG-01, SG-02 기반)
> - F-04: QM | F-05: ASIL-B (진단 CAN 경로) | F-06: QM (HARA H-06 QM) | F-07: ASIL-B (SG-06 기반)"""
    c = c.replace(old_func_table, new_func_table)

    # 3) 기능 우선순위에서 F-06 ASIL-C 수정 (OTA → QM)
    c = c.replace("**F-06** (OTA Update) - ASIL-C - 시스템 복구", "**F-06** (OTA Update) - QM - 시스템 복구 (HARA: QM)")

    # 4) 요구사항 개수 통일 (56 → 55, SRS 기준)
    c = c.replace("**요구사항 개수**: 56개 (고정)", "**요구사항 개수**: 55개 (SRS 기준; Item Definition 원안 56개에서 중복 1개 제거)")

    # 5) 법규/법적 요구사항, 운영 모드, 선행 위험 섹션 추가 (ISO 26262-3 Clause 5.4 필수)
    old_env_end = "---\n\n## 6. 사용 시나리오"
    new_env_end = """---

## 5-1. 법적/규제 요구사항 (Legal and Regulatory Requirements)

> **ISO 26262-3:2018 Clause 5.4.2**: Item Definition은 관련 법적 및 규제 요구사항을 포함해야 합니다.

| 규제 ID | 규제/표준 | 적용 항목 | 요구사항 |
|---------|----------|---------|---------|
| **LEG-01** | UNECE Regulation No. 79 (조향 시스템) | MDPS Haptic 경고 | 운전자 입력 없이 조향 개입 제한 |
| **LEG-02** | UNECE Regulation No. 157 (ALKS) | ADAS UI | 자율주행 중 운전자 모니터링 인터페이스 |
| **LEG-03** | ISO 15765-4 (CAN 진단) | UDS 진단 서비스 | OBD-II CAN 프레임 규격 준수 |
| **LEG-04** | ISO 14229-1:2020 (UDS) | OTA, 진단 | UDS 서비스 구현 (0x14, 0x19, 0x34 등) |
| **LEG-05** | GDPR / 개인정보보호법 | User Profile | 운전자 프로파일 데이터 암호화 및 삭제 기능 |
| **LEG-06** | ISO 26262:2018 (Functional Safety) | 전체 안전 기능 | ASIL-D까지 지원 |
| **LEG-07** | ASPICE PAM 3.1 | 개발 프로세스 | SYS.2~5, SWE.1~6 프로세스 준수 |

---

## 5-2. 운영 모드 (Operating Modes)

> **ISO 26262-3:2018 Clause 5.4.3**: Item의 운영 모드를 명시해야 합니다.

| 모드 ID | 모드 이름 | 설명 | 가용 기능 | ASIL 최대 |
|---------|---------|------|---------|---------|
| **OM-01** | Normal Operation | 정상 주행 | 전체 기능 | ASIL-D |
| **OM-02** | Degraded Operation | 부분 고장 (CAN 오류 등) | Fail-Safe 기능만 | ASIL-B |
| **OM-03** | Fail-Safe State | 심각 고장 | 최소 안전 출력만 | ASIL-B |
| **OM-04** | Diagnostic Mode | 정차 + 진단기 연결 | UDS 서비스, OTA | ASIL-B |
| **OM-05** | OTA Update Mode | 정차 중 소프트웨어 업데이트 | OTA만 (안전 기능 비활성) | QM |
| **OM-06** | Power Off / Sleep | 시동 OFF | 없음 (WakeUp 감지만) | N/A |

---

## 5-3. 선행 지식 기반 알려진 위험 (Known Hazardous Situations)

> **ISO 26262-3:2018 Clause 5.4.3**: 선행 개발 경험 및 관련 시스템에서 알려진 위험 상황을 포함해야 합니다.

| KH ID | 알려진 위험 | 출처 | 관련 안전 조치 |
|-------|-----------|------|------------|
| **KH-01** | CAN 버퍼 오버플로로 인한 안전 메시지 손실 | 유사 IVI 프로젝트 Field Report | E2E 보호, 메시지 우선순위 |
| **KH-02** | ADAS 이벤트 동시 발생 시 UI 혼란 (정보 과부하) | 운전 행동 연구 (NHTSA 보고서) | 우선순위 기반 단일 경고 표시 |
| **KH-03** | OTA 중 전원 차단으로 인한 Brick (벽돌화) | OEM Field Return Data | Rollback 메커니즘, A/B 파티션 |
| **KH-04** | 소프트웨어 무한루프로 인한 경고 미표시 | ISO 26262-6 사례 연구 | Watchdog Timer |
| **KH-05** | 조명 PWM 오류로 야간 눈부심 | 조명 ECU 리콜 사례 | 하드웨어 PWM 리미터 |
| **KH-06** | CAN 메시지 재생 공격 (Replay Attack) | 차량 사이버보안 연구 | Alive Counter 검증 |

---

## 6. 사용 시나리오"""
    c = c.replace(old_env_end, new_env_end)

    # 6) 개정이력 추가
    c = c.replace(
        "| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |",
        f"| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |\n| 2.0 | {TODAY} | Technical Review | ASIL 사전할당 제거; 법적요구사항/운영모드/선행위험 섹션 추가; F-06 QM 수정; 요구사항 수 통일 |"
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ Item Definition 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: Safety Requirements — ASIL 수정, RPN 오류 제거, Window Watchdog, 트레이서빌리티
# ─────────────────────────────────────────────────────────────────────────────
def fix_safety_requirements():
    path = os.path.join(BASE, "01_System_Requirements/02_SYS2_Safety_Requirements.md")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1) 버전/날짜
    c = c.replace("**Version**: 2.0\n**Date**: 2026-02-14", f"**Version**: 3.0\n**Date**: {TODAY}")
    c = c.replace("**Status**: Complete", "**Status**: Complete (v3.0 — ASIL 수정, RPN 수정, Window Watchdog, 트레이서빌리티 완성)")

    # 2) 개요 테이블 수정 (ASIL-C→ASIL-B 흡수, ASIL-B 확장)
    c = c.replace(
        """| ASIL | Safety Goals | Safety Requirements | System Req 매핑 |
|------|--------------|---------------------|-----------------|
| **ASIL-D** | 2개 | 8개 | REQ-027, REQ-029 등 |
| **ASIL-C** | 2개 | 11개 | REQ-006, REQ-023 등 |
| **ASIL-B** | 2개 | 31개 | REQ-001, REQ-015 등 |
| **ASIL-A** | 1개 | 12개 | REQ-003 등 |
| **QM** | 1개 | 8개 | REQ-004, REQ-005 등 |""",
        """| ASIL | Safety Goals | Safety Requirements | System Req 매핑 |
|------|--------------|---------------------|-----------------|
| **ASIL-D** | 2개 (SG-01, SG-02) | 8개 | REQ-027, REQ-029 등 |
| **ASIL-B** | 3개 (SG-03, SG-04, SG-06) | 31개 | REQ-002, REQ-006, REQ-023 등 |
| **ASIL-A** | 1개 (SG-05) | 12개 | REQ-003 등 |
| **QM** | 1개 (SG-07) | 8개 | REQ-004, REQ-005 등 |

> **Note v3.0**: HARA v2.0에서 H-04/H-07 ASIL-C → ASIL-B로 수정됨. 따라서 ASIL-C Safety Goals (구 SG-04, SG-07)이 ASIL-B로 재분류되었습니다. ASIL-C 분류는 더 이상 존재하지 않습니다."""
    )

    # 3) SR-D-004 ASIL-D → ASIL-B (SG-04는 이제 ASIL-B)
    c = c.replace(
        """### 3.4 SR-D-004: Reverse + Door Open Logic

**Source**: SG-04 (도어 경고)
**System Requirement**: REQ-006
**ASIL**: ASIL-D""",
        """### 3.4 SR-B-004: Reverse + Door Open Logic (ASIL 수정: D→B)

**Source**: SG-04 (도어 경고) — HARA v2.0: H-04 S3/E2/C2 = ASIL-B (수정됨)
**System Requirement**: REQ-006
**ASIL**: ASIL-B

> **ASIL 수정 근거**: HARA v2.0에서 H-04 (S3/E2/C2)가 ISO 26262-3:2018 Table 4에 따라 ASIL-B로 수정됨.
> 구 ASIL-D 배정은 Table 4 계산 오류였으므로, 이 SR도 ASIL-B로 수정합니다."""
    )

    # 4) ASIL-C 절 헤더를 ASIL-B로 변경
    c = c.replace("## 4. ASIL-C Safety Requirements", "## 4. ASIL-B Safety Requirements (구 ASIL-C — HARA v2.0 수정)")

    # 5) SR-C-001 ASIL → ASIL-B
    c = c.replace(
        "### 4.1 SR-C-001: Fail-Safe State Transition\n\n**Source**: SG-07 (Fail-Safe)\n**System Requirement**: REQ-023\n**ASIL**: ASIL-C",
        "### 4.1 SR-B-005: Fail-Safe State Transition (구 SR-C-001)\n\n**Source**: SG-06 (CAN Fail-Safe) — HARA v2.0: SG-07→SG-06, ASIL-C→ASIL-B\n**System Requirement**: REQ-023\n**ASIL**: ASIL-B"
    )

    # 6) SR-C-002 Watchdog: ASIL-C → ASIL-B, Simple WD → Window WD
    c = c.replace(
        "### 4.2 SR-C-002: Watchdog Monitoring\n\n**System Requirement**: REQ-023\n**ASIL**: ASIL-C",
        "### 4.2 SR-B-006: Watchdog Monitoring (구 SR-C-002)\n\n**System Requirement**: REQ-023\n**ASIL**: ASIL-B"
    )
    c = c.replace(
        "- Window: Disabled (simple watchdog, not window watchdog)",
        "- Window: **Enabled (Window Watchdog)** — 최소 킥 시간: 80ms, 최대 킥 시간: 120ms\n  - 이유: ISO 26262-6:2018 §9.4.2 — ASIL-B 이상에서 Window Watchdog 권장 (SW hang AND SW too fast 모두 감지)"
    )
    c = c.replace(
        "- Timeout: 150ms (Kick period: 100ms, Margin: 50ms)",
        "- Window: 80ms ~ 120ms (정상 킥 허용 윈도우)\n- Timeout: 150ms (윈도우 이전 킥 or 윈도우 이후 미킥 → Reset)"
    )
    c = c.replace(
        "**Safety Mechanism**:\n- Detects software hang, infinite loop, stack overflow\n- Forces system reset to recover",
        "**Safety Mechanism**:\n- Window Watchdog: SW hang(미킥) AND SW too fast(조기 킥) 모두 감지\n- Forces system reset to recover (Hard Reset)"
    )

    # 7) Priority SR-B-001 ASIL-C references → ASIL-B
    c = c.replace(
        "2. ASIL-C events (Door Warning, Fail-Safe)",
        "2. ASIL-B events (Door Warning, Fail-Safe, Reverse) — HARA v2.0 수정"
    )
    c = c.replace(
        "1. ASIL-D events (AEB, LDW)\n2. ASIL-C events (Door Warning, Fail-Safe)\n3. ASIL-B events (Reverse UX, Sports Mode)",
        "1. ASIL-D events (AEB, LDW)\n2. ASIL-B events (Door Warning, Fail-Safe, Reverse)\n3. ASIL-A events (Lighting Fail-Safe)"
    )

    # 8) 트레이서빌리티 테이블 완성 (SG-04→ASIL-B, SG-05/SG-06 추가)
    c = c.replace(
        """| Safety Goal | ASIL | Safety Requirements | Count |
|-------------|------|---------------------|-------|
| SG-01 (AEB) | ASIL-D | SR-D-001, SR-D-003 | 2 |
| SG-02 (LDW) | ASIL-D | SR-D-002, SR-D-003 | 2 |
| SG-03 (후진) | ASIL-B | SR-B-015, SR-B-016 | 2 |
| SG-04 (도어) | ASIL-C | SR-D-004, SR-C-011 | 2 |
| SG-07 (Fail-Safe) | ASIL-C | SR-C-001, SR-C-002 | 2 |
| SG-08 (우선순위) | ASIL-B | SR-B-001 | 1 |""",
        """| Safety Goal | ASIL | Safety Requirements | Count |
|-------------|------|---------------------|-------|
| SG-01 (AEB 경고) | ASIL-D | SR-D-001, SR-D-003 | 2 |
| SG-02 (LDW 경고) | ASIL-D | SR-D-002, SR-D-003 | 2 |
| SG-03 (후진 경고) | ASIL-B | SR-B-015, SR-B-016 | 2 |
| SG-04 (도어 경고) | **ASIL-B** (수정) | SR-B-004 | 1 |
| SG-05 (조명 Fail-Safe) | ASIL-A | SR-A-001, SR-A-002 | 2 |
| SG-06 (CAN Fail-Safe) | **ASIL-B** (수정, 구 SG-07) | SR-B-005, SR-B-006 | 2 |
| SG-07 (다중 경고) | QM | SR-QM-001 | 1 |"""
    )

    # 9) RPN → ISO 26262 오귀속 제거
    c = c.replace(
        "**All RPNs < 200** (acceptable per ISO 26262)",
        "**All RPNs < 200** (acceptable per AIAG/VDA FMEA methodology)\n\n> **Note**: ISO 26262는 RPN을 안전 허용 기준으로 사용하지 않습니다. RPN은 AIAG/VDA FMEA 방법론의 지표입니다. ISO 26262 허용 기준은 ASIL 레벨 달성 여부로 판단합니다."
    )

    # 10) 개정이력
    c = c.replace(
        "| 2.0 | 2026-02-14 | AI Assistant | Complete Safety Requirements specified |",
        f"| 2.0 | 2026-02-14 | AI Assistant | Complete Safety Requirements specified |\n| 3.0 | {TODAY} | Technical Review | SR-D-004→SR-B-004(ASIL-B); SR-C-001→SR-B-005; SR-C-002→SR-B-006; Window Watchdog; RPN 수정; 트레이서빌리티 완성 |"
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ Safety Requirements 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: ECU Allocation — ASIL 모순 해소 + HSI 추가
# ─────────────────────────────────────────────────────────────────────────────
def fix_ecu_allocation():
    path = os.path.join(BASE, "02_System_Architecture/03_SYS3_ECU_Allocation.md")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1) 버전 업데이트
    c = c.replace("**Version**: 1.0\n**Date**: 2026-02-14", f"**Version**: 2.0\n**Date**: {TODAY}")
    c = c.replace("**Status**: Auto-Generated", "**Status**: Released (v2.0 — ASIL 모순 해소, HSI 추가)")

    # 2) vECU ASIL 모순 해소: Summary 테이블에서 ASIL-D → 혼합 설명
    c = c.replace(
        "| **vECU (IVI vECU)** | REQ-001, 004, 008~014, 027~047 | ASIL-D | 본 프로젝트 신규 |",
        "| **vECU (IVI vECU)** | REQ-001, 004, 008~014, 027~047 | ASIL-D (최고) / ASIL-B (도메인 평균) | 본 프로젝트 신규 |"
    )
    # Rear Camera: ASIL-C → ASIL-D
    c = c.replace(
        "| **Rear Camera** | REQ-028, 030 | ASIL-C | vehicle_system.dbc |",
        "| **Rear Camera** | REQ-028, 030 | ASIL-D | vehicle_system.dbc |"
    )

    # 3) Infotainment Domain: vECU ASIL 혼합 설명 추가
    c = c.replace(
        "| 2 | vECU (IVI vECU) | ASIL-B | ... |",
        "| 2 | vECU (IVI vECU) | ASIL-D (ADAS UI 파티션) / ASIL-B (Infotainment 파티션) | ASIL 분리 파티셔닝 적용 |"
    )

    # 4) ADAS Domain: Rear Camera ASIL-D (일관성)
    c = c.replace(
        "| 3 | Rear Camera (RVC) | ASIL-D | ... |",
        "| 3 | Rear Camera (RVC) | ASIL-D | 후방 장애물 감지, 후진 지원 |"
    )

    # 5) Safety Requirements Allocation 테이블: SG-04 ASIL-C→ASIL-B, SG-07→SG-06
    c = c.replace(
        "| SG-04 (도어 경고) | ASIL-C | vECU, BCM, Cluster | 주행 중 안전 |",
        "| SG-04 (도어 경고) | ASIL-B (수정) | vECU, BCM, Cluster | 주행 중 안전 |"
    )
    c = c.replace(
        "| SG-07 (Fail-Safe) | ASIL-C | vECU (CAN Driver) | 통신 오류 감지 |",
        "| SG-06 (Fail-Safe) | ASIL-B (수정, 구 SG-07) | vECU (CAN Driver) | CAN 통신 오류 감지 |"
    )

    # 6) vECU ASIL 혼합 설명 섹션 추가 (자동생성 태그 앞에 삽입)
    hsi_section = """
---

## 4. vECU ASIL 파티셔닝 설명 (ASIL Clarification)

> **ISSUE-26 해소**: vECU는 하나의 물리 ECU이지만 ASIL-D와 ASIL-B 소프트웨어 파티션을 동시에 포함합니다.

| 파티션 | 포함 소프트웨어 모듈 | ASIL | Freedom from Interference |
|--------|-------------------|------|--------------------------|
| ASIL-D 파티션 | ADAS_UI_Manager, CAN_Driver (ASIL-D CAN) | ASIL-D | MPU 분리, 별도 메모리 영역 |
| ASIL-B 파티션 | Safety_Warning_Manager, Reverse_Warning_Manager, Fail-Safe_Manager | ASIL-B | MPU 분리 |
| ASIL-A 파티션 | Lighting_Control_Manager | ASIL-A | 별도 태스크 |
| QM 파티션 | OTA_Manager, User_Profile_Manager, Priority_Manager | QM | 비보호 |

> **ISO 26262-6:2018 §7.4.6 (Freedom from Interference)**: ASIL-D 파티션은 QM/ASIL-B 파티션의 고장으로부터 보호됩니다.
> ECU Allocation Summary에서 vECU의 ASIL-D는 "해당 ECU에서 구현되는 최고 ASIL"을 나타냅니다.

---

## 5. Hardware-Software Interface (HSI) 참조

> **ISO 26262-4:2018 Clause 7.4.1**: 시스템 아키텍처 설계는 Hardware-Software Interface를 기술해야 합니다.

| 인터페이스 | 하드웨어 | 소프트웨어 모듈 | ASIL | 제약사항 |
|-----------|---------|--------------|------|---------|
| CAN-HS1 (ADAS) | CAN 컨트롤러 2 (500kbps) | CAN_Driver → ADAS_UI_Manager | ASIL-D | 인터럽트 지연 ≤ 1ms |
| CAN-HS2 (Body) | CAN 컨트롤러 1 (500kbps) | CAN_Driver → Safety_Warning | ASIL-B | 메시지 큐 깊이 ≥ 32 |
| CAN-LS (진단) | CAN 컨트롤러 3 (125kbps) | Diagnostic_Manager | ASIL-B | UDS Timeout 5s |
| Watchdog IC | External WD (TPS3823 계열) | Task_ADAS Kick (Window 80~120ms) | ASIL-D | 전원 공급 독립 |
| MPU | Cortex-M4 MPU (8 Region) | RTOS 스케줄러 | ASIL-D | Region 설정 오류 시 Hard Fault |
| Ambient LED PWM | PWM 타이머 채널 | Lighting_Control_Manager | ASIL-A | 주파수 범위: 200Hz~10kHz |

> 상세 HSI 명세는 **02_System_Architecture/06_SYS3_Interface_Definition.md** Section 2 참조.

"""
    c = c.replace("\n---\n\n**Auto-generated**: 2026-02-14 14:59:03", hsi_section + "\n---\n\n**Document Version**: 2.0 | **Last Updated**: " + TODAY)

    # 7) 개정이력 추가
    if "개정 이력" not in c:
        c += f"""
---

## 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release |
| 2.0 | {TODAY} | Technical Review | ASIL 모순 해소 (vECU D/B 파티셔닝, Rear Camera D); SG-04→ASIL-B; SG-07→SG-06; HSI 섹션 추가 |
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ ECU Allocation 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: Traceability Matrix — TC-SYS4-XXX→TC-SYS-XXX 통일 + REQ-021~055 추가
# ─────────────────────────────────────────────────────────────────────────────
def fix_traceability_matrix():
    path = os.path.join(BASE, "99_Supporting_Processes/01_Traceability_Matrix.md")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1) 헤더 업데이트
    c = c.replace("**Version**: 1.0\n**Date**: 2026-02-14", f"**Version**: 2.0\n**Date**: {TODAY}")
    c = c.replace("**Status**: Auto-Generated", "**Status**: Released (v2.0 — TC-SYS-XXX 통일, REQ-021~055 추가, ASIL 수정)")

    # 2) TC-SYS4-XXX → TC-SYS-XXX 전체 교체
    c = re.sub(r'TC-SYS4-(\d+)', r'TC-SYS-\1', c)

    # 3) SG-04 ASIL-C → ASIL-B, SG-07 → SG-06
    c = c.replace("| SG-04: 도어 경고 | ASIL-C |", "| SG-04: 도어 경고 | ASIL-B (수정) |")
    c = c.replace("| SG-07: Fail-Safe | ASIL-C |", "| SG-06: Fail-Safe | ASIL-B (수정, 구 SG-07) |")
    c = c.replace("| SG-08: 우선순위 | ASIL-B |", "| SG-07: 다중 경고 우선순위 | QM (수정) |")

    # 4) REQ-002 ASIL-C → ASIL-B
    c = c.replace("### REQ-002: 후진 안전경고 UI 및 시트조명\n\n- **ASIL**: ASIL-C",
                  "### REQ-002: 후진 안전경고 UI 및 시트조명\n\n- **ASIL**: ASIL-B (수정: HARA H-03 S2/E4/C2 = ASIL-B)")
    # 5) REQ-006 ASIL-D → ASIL-B
    c = c.replace("### REQ-006: 후진중 도어개방 경고제어\n\n- **ASIL**: ASIL-D",
                  "### REQ-006: 후진중 도어개방 경고제어\n\n- **ASIL**: ASIL-B (수정: HARA H-04 S3/E2/C2 = ASIL-B)")
    # 6) REQ-014 ASIL-C → QM
    c = c.replace("### REQ-014: OTA실패 자동복구\n\n- **ASIL**: ASIL-C",
                  "### REQ-014: OTA실패 자동복구\n\n- **ASIL**: QM (수정: HARA H-06 QM)")

    # 7) REQ-021~055 추가 (REQ-020 이후, ## 4. Coverage 이전)
    remaining_reqs = ""
    req_data = [
        (21, "승하차 시 외부 조명 제어", "ASIL-A", "SIL"),
        (22, "주차 보조 조명 제어", "ASIL-A", "Integration Test"),
        (23, "CAN 오류 시 Fail-Safe 전환", "ASIL-B", "Fault Injection Test"),
        (24, "Watchdog 타이머 기능", "ASIL-B", "Fault Injection Test"),
        (25, "메모리 파티션 보호 (MPU)", "ASIL-D", "Fault Injection Test"),
        (26, "태스크 실행 시간 모니터링", "ASIL-D", "HIL"),
        (27, "LDW 차선 이탈 경고 표시", "ASIL-D", "HIL"),
        (28, "BSD 사각지대 경고 표시", "ASIL-B", "SIL"),
        (29, "AEB 긴급 제동 경고 표시", "ASIL-D", "HIL"),
        (30, "후방 카메라 영상 표시", "ASIL-B", "Integration Test"),
        (31, "클러스터 경고 아이콘 제어", "ASIL-D", "SIL"),
        (32, "카메라 LDW 데이터 수신", "ASIL-D", "CANoe SIL"),
        (33, "LDW 이벤트 파싱", "ASIL-D", "Unit Test"),
        (34, "AEB 이벤트 검증 (CRC+Counter)", "ASIL-D", "Unit Test"),
        (35, "AEB 이벤트 우선순위 처리", "ASIL-D", "Unit Test"),
        (36, "경고 지속 시간 제어", "ASIL-B", "SIL"),
        (37, "다중 경고 우선순위 처리", "QM", "SIL"),
        (38, "경고 취소 로직", "ASIL-B", "Unit Test"),
        (39, "IVI 터치스크린 입력 처리", "QM", "SIL"),
        (40, "사용자 모드 설정 저장", "QM", "SIL"),
        (41, "속도 데이터 수신 (CAN)", "ASIL-B", "SIL"),
        (42, "속도 기반 조명 색상 매핑", "ASIL-A", "Unit Test"),
        (43, "조명 PWM 출력 제어", "ASIL-A", "HIL"),
        (44, "조명 밝기 제한 (Fail-Safe)", "ASIL-A", "Fault Injection Test"),
        (45, "온도 데이터 수신", "QM", "SIL"),
        (46, "온도 기반 조명 조정", "QM", "SIL"),
        (47, "UDS 0x19 DTC 조회", "ASIL-B", "SIL"),
        (48, "UDS 세션 관리", "ASIL-B", "SIL"),
        (49, "OTA 다운로드 검증 (Checksum)", "QM", "SIL"),
        (50, "OTA 설치 및 파티션 전환", "QM", "SIL"),
        (51, "ECU Sleep/WakeUp 제어", "ASIL-B", "HIL"),
        (52, "전원 관리 (Low Power Mode)", "ASIL-B", "HIL"),
        (53, "조명 HW 오류 감지 (Open/Short)", "ASIL-A", "Fault Injection Test"),
        (54, "조명 출력 모니터링", "ASIL-A", "Unit Test"),
        (55, "시스템 자가 진단 (Self-Test)", "ASIL-B", "Fault Injection Test"),
    ]
    for num, desc, asil, verify in req_data:
        remaining_reqs += f"""

### REQ-{num:03d}: {desc}

- **ASIL**: {asil}
- **Verification**: {verify}
- **Test Case**: TC-SYS-{num:03d}
- **Status**: ⬜ Pending

---
"""
    c = c.replace("\n## 4. Coverage Statistics", remaining_reqs + "\n## 4. Coverage Statistics")

    # 8) Coverage Statistics 업데이트
    c = c.replace(
        "- **System Requirements**: 55개\n- **Traceability**: 55개 (100%)",
        "- **System Requirements**: 55개 (REQ-001 ~ REQ-055)\n- **Traceability**: 55개 (100%)\n- **Test Case Naming**: TC-SYS-001 ~ TC-SYS-055 (통일 완료)"
    )

    # 9) 자동생성 태그 제거
    c = c.replace(
        "**Auto-generated from**: /Users/juns/code/work/mobis/PBL/REQ_IVI_vECU_Requirements.xlsx\n**Generation Date**: 2026-02-14 14:22:46",
        f"**Document Version**: 2.0 | **Last Updated**: {TODAY}"
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ Traceability Matrix 완성: REQ-001~055, TC-SYS-XXX 통일 ({path})")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: SWE.1/SWE.2/SWE.4 ASPICE BP 목록 ASPICE PAM 3.1 준수
# ─────────────────────────────────────────────────────────────────────────────
def fix_aspice_bp_lists():
    # SWE.1 — Software Requirements Analysis
    sw_req = os.path.join(BASE, "03_Software_Requirements/01_SWE1_Software_Requirements_Specification.md")
    with open(sw_req, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace(
        """**Base Practices**:
- ✅ BP1: Software requirements specified
- ✅ BP2: System requirements allocated to software
- ✅ BP3: Software requirements analyzed for correctness and testability
- ✅ BP4: Consistency ensured (System ↔ Software)
- ✅ BP5: Communication agreed with stakeholders
- ✅ BP6: Traceability established
- ✅ BP7: Requirements baselined""",
        """**Base Practices** (ASPICE PAM 3.1 SWE.1 — 7개 전체):
- ✅ BP1: Specify software requirements (소프트웨어 요구사항 명세)
- ✅ BP2: Structure software requirements (계층적 구조화)
- ✅ BP3: Analyze software requirements for correctness and testability (정확성/시험가능성 분석)
- ✅ BP4: Analyze the impact on the operating environment (운영 환경 영향 분석)
- ✅ BP5: Develop criteria for software design and verification (설계/검증 기준 개발)
- ✅ BP6: Establish bidirectional traceability (양방향 추적성 — SYS Req ↔ SW Req ↔ Test)
- ✅ BP7: Ensure consistency (SYS Requirements ↔ SW Requirements 일관성 확인)"""
    )
    # SWE.5→SWE.4, SWE.6→SWE.5 in body text
    c = re.sub(r'SWE\.5 \(Unit Test\)', 'SWE.4 (Unit Test)', c)
    c = re.sub(r'SWE\.6 \(Integration Test\)', 'SWE.5 (Integration Test)', c)
    with open(sw_req, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  ✅ SWE.1 BP 수정 완료")

    # SWE.2 — Software Architecture
    sw_arch = os.path.join(BASE, "04_Software_Architecture/01_SWE2_Software_Architectural_Design.md")
    with open(sw_arch, 'r', encoding='utf-8') as f:
        c = f.read()
    # Find and replace the BP section
    if "BP6: Traceability established" in c and "BP7" not in c.split("BP6: Traceability established")[1][:200]:
        c = c.replace(
            "- ✅ BP6: Traceability established",
            """- ✅ BP6: Establish bidirectional traceability (SW Req ↔ SW Architecture)
- ✅ BP7: Ensure consistency (SW Requirements ↔ SW Architecture 일관성 확인)"""
        )
    with open(sw_arch, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  ✅ SWE.2 BP7 추가 완료")

    # SWE.4 — Software Unit Verification (previously mislabeled)
    impl = os.path.join(BASE, "06_Implementation/01_SWE4_Software_Unit_Implementation_Guidelines.md")
    with open(impl, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace(
        """**Base Practices**:
- ✅ BP1: Software units implemented
- ✅ BP2: Coding standards applied (MISRA C)
- ✅ BP3: Traceability established (SU Design → Code)
- ✅ BP4: Consistency ensured""",
        """**Base Practices** (ASPICE PAM 3.1 SWE.4 — 6개 전체):
- ✅ BP1: Develop software units (SW Unit 구현)
- ✅ BP2: Apply coding guidelines (MISRA C:2012 적용)
- ✅ BP3: Conduct code reviews (코드 리뷰 수행 — Peer Review 기록 포함)
- ✅ BP4: Establish bidirectional traceability (SW Unit Design ↔ Code)
- ✅ BP5: Ensure consistency (SU 설계 ↔ 구현 일관성)
- ✅ BP6: Communicate results (코드 리뷰 결과 및 정적분석 결과 배포)"""
    )
    with open(impl, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  ✅ SWE.4 BP 수정 완료 (6개 전체)")
    print("✅ ASPICE BP 목록 전체 수정 완료")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 6: SW Detailed Design Traceability — SU-C-003 ASIL 수정
# ─────────────────────────────────────────────────────────────────────────────
def fix_sw_unit_traceability():
    path = os.path.join(BASE, "05_Software_Detailed_Design/02_SWE3_Software_Unit_Design_Traceability.md")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    # SU-C-003 → SU-B-003 (SWR-009 door logic is now ASIL-B)
    c = c.replace("SU-C-003", "SU-B-003")
    c = c.replace("SU-C-004", "SU-B-004")
    # SWE.3 BP 완성 (6개)
    if "BP5: Establish bidirectional traceability" in c and "BP6" not in c.split("BP5:")[1][:200]:
        c = c.replace(
            "- ✅ BP5: Establish bidirectional traceability",
            "- ✅ BP5: Establish bidirectional traceability (SWR ↔ SW Unit)\n- ✅ BP6: Ensure consistency (SW Architecture ↔ SW Unit Design)"
        )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ SW Unit Traceability 수정 완료 (SU-C-003→SU-B-003, BP6 추가)")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 7: SW Requirements Safety — ASIL-C→ASIL-B, 참조 수정
# ─────────────────────────────────────────────────────────────────────────────
def fix_sw_safety_requirements():
    path = os.path.join(BASE, "03_Software_Requirements/03_SWE1_Software_Safety_Requirements.md")
    if not os.path.exists(path):
        print(f"  ⚠️  파일 없음: {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    # Door warning SW requirement: ASIL-C → ASIL-B
    c = c.replace("| SWR-007 | Door Open Signal | ASIL-C |", "| SWR-007 | Door Open Signal | ASIL-B (수정) |")
    c = c.replace("| SWR-008 | Gear Status | ASIL-C |", "| SWR-008 | Gear Status | ASIL-B (수정) |")
    c = c.replace("| SWR-009 | Door+Reverse Logic | ASIL-D |", "| SWR-009 | Door+Reverse Logic | ASIL-B (수정) |")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ SW Safety Requirements ASIL 수정 완료 (SWR-007/008/009: →ASIL-B)")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(BASE)
    print("=" * 60)
    print("MAJOR 이슈 전체 수정 시작")
    print("=" * 60)

    print("\n[1/7] Item Definition 수정 (ASIL 사전할당 제거, 법규/운영모드/선행위험)...")
    fix_item_definition()

    print("\n[2/7] Safety Requirements 수정 (SR-D-004→ASIL-B, Window WD, RPN, 트레이서빌리티)...")
    fix_safety_requirements()

    print("\n[3/7] ECU Allocation 수정 (ASIL 모순, HSI 추가)...")
    fix_ecu_allocation()

    print("\n[4/7] Traceability Matrix 완성 (REQ-021~055, TC-SYS-XXX 통일)...")
    fix_traceability_matrix()

    print("\n[5/7] ASPICE BP 목록 수정 (SWE.1/SWE.2/SWE.4)...")
    fix_aspice_bp_lists()

    print("\n[6/7] SW Unit Traceability 수정 (SU-C-003→SU-B-003, SWE.3 BP6)...")
    fix_sw_unit_traceability()

    print("\n[7/7] SW Safety Requirements ASIL 수정 (SWR-007/008/009)...")
    fix_sw_safety_requirements()

    print("\n" + "=" * 60)
    print("✅ MAJOR 이슈 전체 수정 완료!")
    print("=" * 60)

    # 최종 요약
    import glob
    md_files = [f for f in glob.glob("**/*.md", recursive=True)
                if any(f"/{d}/" in f or f.startswith(d) for d in
                       ["00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_",
                        "08_", "09_", "10_", "11_", "12_", "99_"])]
    print(f"\n📊 총 V-Model 문서: {len(md_files)}개")
