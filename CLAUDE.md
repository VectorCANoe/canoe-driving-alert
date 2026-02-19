# CLAUDE.md — Mobis PBL 프로젝트 컨텍스트

> Claude Code가 매 세션 시작 시 자동으로 읽습니다.

---

## 프로젝트 기본 정보

- **저장소**: `/Users/juns/code/work/mobis/PBL` (git: `main` 브랜치)
- **주제**: CANoe 기반 차량 통신 검증 — Fault → Diagnostics → OTA E2E 시뮬레이션
- **개발 환경**: CANoe 17+, CAPL, dSPACE SCALEXIO HIL

---

## 핵심 시나리오 (Red Thread — 전 문서의 중심)

```
BCM (CAN-LS 0x500 — BCM_FaultStatus)
  Window Motor Overcurrent (50A) → DTC B1234 저장 → CAN-LS 전송
      ↓
Central Gateway (CGW)
  CAN-LS → CAN-HS2 라우팅 (≤5ms)
  + Ethernet/DoIP → OTA 서버 경로 (ISO 13400-2)
      ↓
vECU
  Cluster 경고등 활성화 (FTTI < 50ms, REQ-F03)
      ↓
CANoe Tester (CAPL)
  UDS 0x10 0x03 (Extended Session) → BCM
  UDS 0x19 0x02 (Read DTC) → DTC B1234 수신
  TCP/IP → 가상 OTA 서버 전송
      ↓
OTA Server (CANoe 가상 노드)
  UDS 0x10 0x02 (Programming Session)
  UDS 0x34 → 0x36 × N → 0x37 (Download → Transfer → Exit)
  BCM 재시작 → DTC 소거 확인
```

---

## 완료된 작업

### V-Model 문서 (46개, ISO 26262 / ASPICE)
- **요구사항**: REQ-F/G/D/O/A/N 6-Group 체계 (40개 REQ)
- **HARA v3.0**: H-01~H-10 위험, SG-01~SG-09 Safety Goals
  - H-09: OTA 전원 차단 (ASIL-B, SG-08)
  - H-10: GW Protocol Translation 실패 (ASIL-A, SG-09)
- **Safety Validation Report v2.1**: SG-05~SG-09 검증 섹션 완성
- **전 문서 Narrative Alignment 완료**: Fault→Diag→OTA Red Thread 연결

### DBC 충돌 해결 ✅ (2026-02-13)
- `BCM_DoorStatus` → **0x501** (1281)로 이동
- `BCM_FaultStatus` → **0x500** (1280) 신규 정의 (10ms, ASIL-B)
  - Signals: `WindowMotorOvercurrent`, `DTC_Code`, `FaultSeverity`, `AliveCounter`, `Checksum`
- `vECU_WarningUI` → **0x420** (1056) 신규 정의 (50ms, ASIL-D)
  - Signals: `Warning_Type`, `Warning_Priority`, `Icon_ID`, `Warning_Active`

### Concept_design.drawio ✅ (2026-02-18) — 7페이지 V-Model 체계

| # | 페이지 이름 | 내용 | Cells |
|---|------------|------|-------|
| 1 | `REF_ConceptDesignOverview` | 개요 참조 | 51 |
| 2 | `REF_CANBusPrinciple` | CAN 원리 참조 | 58 |
| 3 | `SYS3_VHA_VehicleArchitecture` | 전체 차량 아키텍처 (도메인/ECU) | 92 |
| 4 | `SYS3_CBD_SystemFunctionalBlock` | 도메인별 기능 블록 I-C-O | 67 |
| 5 | `SYS3_FBD_FunctionalBlockDiagram` | 서비스별 기능 블록 I-C-O | 47 |
| 6 | `SYS3_NET_CANBusTopology` | CAN 버스 토폴로지 | 53 |
| 7 | `SYS3_SIG_E2EServiceFlow` | E2E 서비스 흐름 (시퀀스) | 39 |

### 폴더 구조
- CANoe 업계 표준으로 재설계 완료
- git: feature → develop → main PR 방식

---

## 다음 작업: CAPL 노드 개발

`canoe/nodes/` 에 생성할 파일:

| 파일 | 역할 | 상태 |
|------|------|------|
| `BCM_Sim.can` | Window Motor Overcurrent → DTC B1234 → BCM_FaultStatus(0x500) CAN-LS 전송 | ⬜ 미개발 |
| `CGW_Sim.can` | CAN-LS→CAN-HS2 라우팅 ≤5ms + DoIP TCP 소켓 | ⬜ 미개발 |
| `Tester_Sim.can` | UDS 0x10 0x03 Extended Session, UDS 0x19 0x02 Read DTC | ⬜ 미개발 |
| `OTA_Server_Sim.can` | UDS 0x34/0x36/0x37 + Rollback 검증 | ⬜ 미개발 |

> **DBC 충돌 해결 완료** ✅ — BCM_DoorStatus(0x501), BCM_FaultStatus(0x500), vECU_WarningUI(0x420) 정의 완료

---

## 핵심 참고 파일

| 용도 | 경로 |
|------|------|
| 구 CAPL 문법 패턴 | `reference/legacy/capl_nodes/BCM.can`, `CGW.can` |
| DBC | `canoe/databases/vehicle_system.dbc` |
| CANoe 프로젝트 파일 | `canoe/cfg/IVI_OTA_Project.cfg` |
| 시스템 요구사항 (SRS) | `docs/V-Model/준수/01_System_Requirements/01_SYS2_System_Requirements_Specification.md` |
| 통신 사양 (UDS/DoIP 테이블) | `docs/V-Model/준수/02_System_Architecture/05_SYS3_Communication_Specification.md` |
| 네트워크 토폴로지 | `docs/V-Model/준수/02_System_Architecture/04_SYS3_Network_Topology.md` |

### Legacy CAPL 재사용 가이드

**`BCM.can`**
- 재사용 가능: `variables{}`, `on start{}`, `on timer{}`, `on message{}` 기본 구조, `write()` 디버그
- 재사용 불가: 조명 로직 (`IVI_AmbientLight`, RGB 변수)

**`CGW.can`**
- 재사용 가능: `on message CAN1.xxx → output(CAN2, msg)` 라우팅 패턴, `gDiagnosticActive`, `gOTA_Active` 변수 선언
- 재사용 불가: EMS/ESP 라우팅 (구 조명 도메인)

---

## 아키텍처 제약

- **Central Gateway 중심** — Zonal은 미래 방향 맥락으로만 언급
- **ADAS 유지** — AEB/LDW/BSD 삭제 금지 (핵심 시나리오가 아닐 뿐)
- **ASIL**: AEB/LDW = ASIL-D / BCM Fault·OTA Rollback = ASIL-B / GW Translation = ASIL-A
- **CAN**: LS 125kbps / HS1·HS2 500kbps / Ethernet DoIP (ISO 13400-2)

---

## 미래 계획: 범위 축소 + LIN 추가 (V-Model 개편 시 적용)

> **⚠️ 현재 미적용** — sample 프로젝트 완료 후, V-Model 동역학 연동 시점에 실행할 계획.

### 목표
CAN + LIN + Ethernet 세 가지 통신만 사용, BCM(Body) + IVI(Infotainment) 두 도메인으로 한정.
`Fault Detection → Gateway Routing → UDS Diagnostics → OTA Update` Red Thread 집중 표현.

**LIN 추가 이유**: Window Motor ECU(LIN Slave) → BCM(LIN Master) → CAN-LS → CGW 실제 흐름 반영.

### 새 아키텍처 요약

```
[LIN Bus - BCM 도메인]
  BCM (LIN Master)
    ├── Window Motor ECU (LIN Slave 0x21) — Motor_Current 보고 → DTC 트리거
    ├── Door Module FL   (LIN Slave 0x22) — Door_Position 보고
    ├── Door Module FR   (LIN Slave 0x23)
    ├── Door Module RL   (LIN Slave 0x24)
    └── Door Module RR   (LIN Slave 0x25)

[CAN-LS 125kbps - Body Domain]
  BCM → CGW: BCM_FaultStatus (0x500, 10ms, ASIL-B)
  BCM → CGW: BCM_DoorStatus  (0x501, 100ms, ASIL-B)
  BCM → CGW/Cluster: BCM_LightControl (0x510)
  UDS_Request (0x7DF) / UDS_Response (0x7E8)

[CAN-HS 500kbps - Infotainment Domain]
  CGW → vECU: BCM_FaultStatus (0x500, routed ≤5ms)
  vECU → Cluster: vECU_WarningUI (0x420, 50ms, ASIL-B)  ← ASIL-D→B
  IVI → BCM: IVI_AmbientLight (0x400, 100ms)
  IVI → BCM: IVI_Profile (0x410, 500ms)
  Cluster_Display (0x480)
  CGW_Status (0x700)

[Ethernet 100Mbps - OTA]
  OTA Server (192.168.1.100) ↔ CGW (192.168.1.10) — DoIP ISO 13400-2
```

**제거 대상 ECU**: EMS, TCU, ESP, MDPS, Camera, Rear_Camera, Radar, SCC, AVM, HUD
**제거 대상 CAN 메시지**: 0x100~0x280 (Powertrain/Chassis), 0x300~0x380 (ADAS)
**제거 대상 네트워크**: CAN-HS1

### LIN 신호 정의

```
LIN Bus: BCM (Master) ↔ Window Motor ECU + Door Modules (Slaves)
Protocol: LIN 2.2A, 19.2 kbps

[Window Motor ECU — LIN ID 0x21, 10ms cycle]
  Motor_Current:   10bit [0|100] A  — 50A 초과 시 BCM이 DTC B1234 생성
  Motor_Status:     2bit enum (IDLE/RUNNING/STALL/ERROR)
  Motor_Direction:  1bit (UP/DOWN)

[Door Module FL/FR/RL/RR — LIN ID 0x22~0x25, 50ms cycle]
  Door_Position:    2bit enum (CLOSED/OPEN/AJAR/ERROR)
  Lock_Status:      1bit (LOCKED/UNLOCKED)
  Window_Position:  8bit [0|100] %
```

### HARA 재편 (10개 → 8개, ASIL-D 제거)

| 새 ID | 위험 | ASIL | Safety Goal |
|-------|------|------|-------------|
| H-01 | LIN Window Motor 통신 오류 → 과전류 미감지 | ASIL-B | SG-01 |
| H-02 | LIN Door Module 통신 오류 → 도어 개방 경고 미표시 | ASIL-B | SG-02 |
| H-03 | IVI 조명 오작동 → 눈부심 | ASIL-A | SG-03 |
| H-04 | Fail-Safe 미작동 | ASIL-B | SG-04 |
| H-05 | 다중 경고 혼란 | QM | SG-05 |
| H-06 | OTA 실패 후 기능 상실 | QM | QR-01 |
| H-07 | OTA 중 전원 차단 → BCM SW 손상 | ASIL-B | SG-06 |
| H-08 | Gateway Protocol Translation 실패 | ASIL-A | SG-07 |

**최고 ASIL: ASIL-B** (ASIL-D 없음 → ASIL Decomposition 불필요)

### REQ 변경 (40개 → 34개)

| 변경 | 항목 |
|------|------|
| 제거 | REQ-A01~A11 (11개 ADAS) |
| ASIL 수정 | REQ-F03: ASIL-D→B / REQ-N03, N04: ASIL-D→B / vECU_WarningUI: ASIL-D→B |
| 강화 | REQ-F01: "LIN Window Motor ECU로부터 전류값 수신" |
| 추가 | REQ-F06: LIN Door Module 상태 수신 및 BCM_DoorStatus 생성 |
| 추가 | REQ-F07: LIN 통신 이상 시 DTC 생성 및 Fail-Safe |

### 수정 대상 파일 (적용 시)

**Phase 1 (개념/요구사항)**:
- `00_Concept_Phase/00_Item_Definition.md` → v4.0
- `00_Concept_Phase/01_Hazard_Analysis_Risk_Assessment.md` → v4.0
- `00_Concept_Phase/02_Functional_Safety_Concept.md` → v3.0
- `01_System_Requirements/01_SYS2_System_Requirements_Specification.md` → v4.0
- `01_System_Requirements/02_SYS2_Safety_Requirements.md` → v3.0

**Phase 2 (아키텍처)**:
- `02_System_Architecture/01_SYS3_System_Architectural_Design.md` → v3.0
- `02_System_Architecture/02_SYS3_Domain_Architecture.md` → v3.0
- `02_System_Architecture/03_SYS3_ECU_Allocation.md` → v3.0
- `02_System_Architecture/04_SYS3_Network_Topology.md` → v3.0
- `02_System_Architecture/05_SYS3_Communication_Specification.md` → v3.0

**Phase 3 (지원 프로세스 + DBC)**:
- `99_Supporting_Processes/01_Traceability_Matrix.md` → v4.0
- `canoe/databases/vehicle_system.dbc`

**Phase 4 (Drawio)**:
- 7페이지 전체 — ADAS/Powertrain/Chassis 제거, LIN 추가

### 검증 포인트 (적용 시)

- [ ] 모든 문서에서 ADAS 단어 잔여 없음
- [ ] H-01~H-08 + SG-01~SG-07 번호 일관
- [ ] REQ-F/G/D/O/N 총 34개 (A 그룹 없음)
- [ ] CAN 메시지 ID 0x300~0x380, 0x100~0x280 모두 제거
- [ ] ASIL 최고값이 ASIL-B (D는 없음)
- [ ] Red Thread: LIN Motor → BCM → CAN-LS 0x500 → CGW → CAN-HS → UDS → OTA 명확
