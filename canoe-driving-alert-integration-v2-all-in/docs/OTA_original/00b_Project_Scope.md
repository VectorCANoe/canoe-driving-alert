# 프로젝트 범위 및 검증 전략 (Project Scope and Verification Strategy)

**Document ID**: PROJ-00b-PS
**ISO 26262 Reference**: Part 2, Cl.6 — 기능 안전 관리 계획 / Part 4, Cl.5 — 시스템 수준 개발 착수
**ASPICE Reference**: MAN.3 (BP1: 프로젝트 범위 정의), SYS.5 (BP1: 시스템 테스트 전략)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 전체 — 프로젝트 범위 및 V&V 전략 | 전체 문서 참조 | Concept Design | `01_Requirements.md` |

---

## 1. 프로젝트 범위 (Project Scope)

본 프로젝트는 **Vector CANoe SIL(Software-in-the-Loop)** 환경에서 차량 운전 습관 기반 실시간 경고 및 양방향 OTA 보상/제한 시스템을 구현한다.

**프로젝트 정체성**:

```
운전 습관 기반 양방향 OTA 경고·보상 시스템
  위험 운전 반복  →  단계별 경고  →  안전모드 OTA (토크 제한)
  안전 운전 지속  →  경고 해제   →  퍼포먼스 언락 OTA (보상)
```

**E2E 핵심 흐름 (Red Thread)**:

```
입력층 A — Vehicle_ECU (CAN-LS 0x100)
  → 과속 / 급가속(gAccelCount) / 급제동 신호 제공

입력층 B — MDPS_ECU (CAN-LS 0x110), LDW_ECU (CAN-LS 0x120)
  → 급차선변경 / 차선이탈 신호 제공

Central Gateway (CGW)
  → CAN-LS 입력 신호 → CAN-HS로 WDM_ECU에 포워딩

WDM_ECU (판단층, CAN-HS)
  → A 단독 OR B 단독 → gWarningLevel = 1 (1단계 경고)
  → A AND B          → gWarningLevel = 2 (2단계 경고)
  → A+B + OTA 조건   → gWarningLevel = 3 (3단계 + OTA 제안)

출력층 — Cluster_ECU / Ambient_ECU / Sound_ECU / IVI_ECU / Door_ECU
  → 단계별 경고 출력

해제층 — Driver::GazeActive / SteeringInput
  → 운전자 개입 감지 → 경고 해제

특화층 D — 준영(gRoadZone 구간 인식 + Ambient 방향 안내)
  + 성현(OTA 구독 서비스 UDS 세션)
  → OTA Server (DoIP Ethernet)
  → UDS 0x10 → 0x27 → 0x34 → 0x36×N → 0x37
  → ECU 재시작 / Rollback (실패 시) / Bus Off 안전 중단
```

**대상 도메인**: Body (차량 동역학 입력 ECU) / Powertrain (WDM 판단) / Infotainment (Cluster/IVI/Ambient) / OTA Connectivity

---

## 2. 검증 환경 (Verification Environment)

| 항목 | 내용 |
|------|------|
| 검증 도구 | Vector CANoe 17+ (SIL — Software-in-the-Loop) |
| 구현 언어 | CAPL (Communication Access Programming Language) |
| 네트워크 | CAN-LS (125kbps) / CAN-HS (500kbps) / Ethernet DoIP (100Mbps) |
| 가상 노드 | Vehicle_ECU / MDPS_ECU / LDW_ECU / WDM_ECU / CGW / Cluster_ECU / Ambient_ECU / Sound_ECU / IVI_ECU / Door_ECU / OTA_Server |
| 입력 인터페이스 | CANoe Panel — TrackBar (속도/가속도 조절) / 버튼 4개 (gRoadZone) / Switch (Fault Injection, OTA 트리거) / Indicator (상태 출력) |
| DBC | `canoe/databases/project.dbc` |
| 구현 파일 | `canoe/nodes/` (CAPL 노드) / `canoe/test_modules/` (테스트 CAPL) |

**실제 센서 없는 SIL 구현 원칙**:

| 실제 신호 | SIL 대체 방법 |
|---------|------------|
| 네비게이션 구간 정보 | Panel 버튼 4개 → gRoadZone(0~3) |
| 레이더/BSD 거리 | sysvar::Radar::TTC 직접 주입 |
| 운전자 응시 감지 | sysvar::Driver::GazeActive 직접 주입 |
| 빗길 감지 | sysvar::Rain::rainMode 직접 주입 |
| 가속도 센서 | sysvar::Vehicle::accelValue Panel TrackBar |

**테스트 모듈 구성**:

| 모듈 | 대상 시나리오 |
|------|------------|
| `TC_A_SpeedInput/` | 과속/급가속/급제동 감지 (In_Test_01, 02) |
| `TC_B_DirectionInput/` | 차선이탈/급차선변경 감지 (In_Test_03) |
| `TC_W_Warning/` | 1/2/3단계 경고 발령 및 해제 (In_Test_04~06) |
| `TC_Z_ZoneAmbient/` | gRoadZone 구간별 앰비언트 동작 (In_Test_07~09) |
| `TC_O_OTA/` | OTA 구독 UDS 세션 / Rollback / Bus Off (In_Test_10~13) |
| `TC_E2E_Master_Scenario/` | 전체 E2E 시나리오 순차 실행 (Scene.1~17) |

**E2E 시나리오 실행 순서**:

| 단계 | Scene | 내용 |
|------|-------|------|
| 초기화 | Scene.1~2 | ECU 초기화 + 정상 주행 상태 확인 |
| A단독 경고 | Scene.3 | 과속/급가속/급제동 → 1단계 경고 |
| B단독 경고 | Scene.4 | 차선이탈/급차선변경 → 1단계 경고 |
| 복합 경고 | Scene.5 | A+B → 2단계 경고 |
| 해제 | Scene.6~7 | 응시 복귀 / 핸들 입력 → 경고 해제 |
| 구간 앰비언트 | Scene.8~10 | gRoadZone 1(스쿨존) / 2(고속도로) / 3(IC출구) |
| OTA 제안 | Scene.11 | 3단계 → IVI 팝업 → 운전자 동의 |
| OTA 전송 | Scene.12~14 | 0x34 → 0x36×N → 0x37 + CRC-32 검증 |
| 안전 복구 | Scene.15~16 | Rollback (CRC 불일치) + Bus Off 안전 중단 |
| 재검증 | Scene.17 | 전체 E2E 2회 연속 정상 동작 확인 |

---

## 3. HARA 안전목표 요약 (Safety Goal Summary)

> **참조**: HARA 추적성 매트릭스 전체는 `00_VModel_Mapping.md` — HARA 안전목표 추적성 섹션 참조

| HARA ID | 위험 설명 | ASIL | 안전목표 (Safety Goal) | 대응 요구사항 | 검증 |
|---------|---------|------|----------------------|------------|------|
| H-01 | 위험 운전 미감지 → 경고 미발령 → 사고 → 운전자/보행자 부상 | **ASIL-B** | SG-01: 위험 운전 감지 시 WDM_ECU가 50ms 이내 단계별 경고를 발령한다 (FTTI ≤50ms) | Req_001~008, Req_012, Req_013 | Scene.3~9 |
| H-02 | OTA 중 통신 두절로 ECU Bricking | **QM** | N/A — 안전목표 없음. Rollback(Req_017)으로 완화. | Req_017 (완화 수단) | Scene.15 |
| H-03 | OTA 실패로 토크 제한 ECU 불능 → 차량 구동계 기능 이상 | **ASIL-B** | SG-02: OTA 실패 시 이전 펌웨어로 자동 복구하고 진행 중인 세션을 안전하게 종료한다 | Req_017, Req_018 | Scene.15~16 |

**최고 ASIL 등급**: ASIL-B — ASIL Decomposition 불필요

**ASIL 등급 근거**:

| ASIL | 해당 요구사항 | 근거 |
|------|------------|------|
| ASIL-B | Req_001~008, Req_012, Req_013, Req_015, Req_016, Req_017 | H-01/H-03 Safety Goal 직접 대응 |
| ASIL-A | Req_009, Req_010, Req_018 | 경고 해제 / Bus Off 안전 중단 (보조 안전 기능) |
| QM | Req_011, Req_014 | 안전목표와 무관한 구간 인식 / 앰비언트 안내 |

---

## 4. 적용 표준 (Applied Standards)

| 표준 | 버전 | 적용 범위 |
|------|------|---------|
| ISO 26262 | 2018 | 기능 안전 — HARA, ASIL 분류, V-Model, 요구사항 추적성 |
| Automotive SPICE PAM | 3.1 | 프로세스 개선 — SYS.2/3, SWE.2/4/5, SYS.5, SUP.10 |
| UNECE WP.29 | — | OTA 규제 — 차량이 자율적으로 OTA 결정 불가, 운전자 동의 필수 |
| ISO 14229-1 (UDS) | — | UDS 서비스 (0x10 / 0x27 / 0x34 / 0x36 / 0x37) |
| ISO 13400-2 (DoIP) | — | OTA Server ↔ CGW Ethernet 통신 |
| ISO 11898-1 (CAN) | — | CAN Bus Off 감지 및 복구 절차 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 — 프로젝트 범위, 검증 환경, HARA 요약, ASIL 근거, 적용 표준 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
