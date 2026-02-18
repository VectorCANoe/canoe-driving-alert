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
BCM (CAN-LS 0x500)
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

### 폴더 구조
- CANoe 업계 표준으로 재설계 완료
- git: feature → develop → main PR 방식

---

## 다음 작업: CAPL 노드 개발

`canoe/nodes/` 에 생성할 파일:

| 파일 | 역할 |
|------|------|
| `BCM_Sim.can` | Window Motor Overcurrent → DTC B1234 → CAN-LS(0x500) 전송 |
| `CGW_Sim.can` | CAN-LS→CAN-HS2 라우팅 ≤5ms + DoIP TCP 소켓 |
| `Tester_Sim.can` | UDS 0x10 0x03 Extended Session, UDS 0x19 0x02 Read DTC |
| `OTA_Server_Sim.can` | UDS 0x34/0x36/0x37 + Rollback 검증 |

### 먼저 해결해야 할 DBC 충돌

파일: `canoe/databases/vehicle_system.dbc`

```
문제: BCM_DoorStatus  → BO_ 1280 (0x500) 이미 점유
     BCM_FaultStatus → SRS(REQ-F01)에서 0x500 요구
해결: BCM_DoorStatus를 0x501로 이동 + SRS 문서 동시 수정
```

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
