# CANoe Sample Project — 실행 가이드

> **프로젝트**: CANoe IVI OTA — Fault Detection → Gateway Routing → UDS Diagnostics → OTA Update
> **CANoe 버전**: 17.0 이상 권장 (SIL — Software-in-the-Loop)

---

## 폴더 구조

```
canoe/
├── cfg/
│   ├── sample_project.cfg        ← CANoe 설정 파일 (여기서 시작)
│   └── sample_project.sysvars   ← System Variables 정의
├── databases/
│   └── sample_project.dbc       ← 경량 DBC (5개 ECU: BCM/CGW/Cluster/Tester/OTA_Server)
└── nodes/
    ├── BCM.can                   ← 과전류 감지, DTC B1234 생성
    ├── Gateway.can               ← CAN-LS→CAN-HS 라우팅, DoIP 처리
    ├── Tester.can                ← UDS 0x10/0x19/0x14 요청
    ├── OTA_Server.can            ← UDS 0x34/0x36/0x37 펌웨어 전송
    └── Cluster.can               ← RED 경고등 제어
```

---

## CANoe 프로젝트 열기 순서

### 1단계 — 새 Configuration 생성
1. CANoe 실행 → `File` → `New Configuration`
2. `cfg/sample_project.cfg` 참고하여 설정

### 2단계 — DBC 데이터베이스 연결
1. `Configuration` → `Networks and ECUs`
2. `Add Network` → CAN-LS (125kbps), CAN-HS (500kbps) 생성
3. 각 네트워크에 `databases/sample_project.dbc` 연결

### 3단계 — CAPL 노드 추가
1. CAN-LS 네트워크에 노드 추가:
   - `BCM` → `nodes/BCM.can`
   - `CGW` → `nodes/Gateway.can`
   - `Tester` → `nodes/Tester.can`
   - `OTA_Server` → `nodes/OTA_Server.can`
2. CAN-HS 네트워크에 노드 추가:
   - `Cluster` → `nodes/Cluster.can`
   - `CGW` → `nodes/Gateway.can` (동일 파일, 양쪽 채널 연결)

### 4단계 — System Variables 로드
1. `Environment` → `System Variables` → `Import`
2. `cfg/sample_project.sysvars` 선택

### 5단계 — Panel 구성 (CANoe GUI에서 직접 생성)
| Panel 이름 | 컨트롤 | 연결 변수 |
|-----------|--------|---------|
| Fault Injection | Switch | `BCM::overcurrentDetected` |
| | Indicator | `BCM::faultActive` |
| UDS Control | Switch (0x10/0x19/0x14) | `UDS::lastServiceID` |
| | Indicator | `UDS::currentSession`, `UDS::lastResponseCode` |
| OTA Control | Switch | `OTA::otaInProgress` |
| | Numeric | `OTA::blockSequenceCounter` |
| | Indicator | `OTA::crcMatch`, `OTA::rollbackTriggered` |
| System Status | Indicator | `Gateway::routingActive`, `Cluster::warnLampRed` |
| | Numeric | `Gateway::routingDelayMs` |

---

## E2E 시나리오 실행 순서

```
1. CANoe 측정 시작 (▶ Start)
2. [Fault Injection Panel] overcurrentDetected = 1 설정
   → BCM: DTC B1234 생성, FaultStatus(0x500) 전송
   → Gateway: CAN-LS → CAN-HS 라우팅
   → Cluster: RED 경고등 점등
3. [UDS Panel] lastServiceID = 0x10 (Extended Session 전환)
   → Tester: UDS 0x10 0x03 전송 → PositiveResponse(0x50) 확인
4. [UDS Panel] lastServiceID = 0x19 (DTC 조회)
   → Tester: UDS 0x19 0x02 전송 → DTC B1234 포함 응답 확인
5. [UDS Panel] lastServiceID = 0x14 (DTC 클리어)
   → Tester: UDS 0x14 전송 → PositiveResponse(0x54) 확인
   → Cluster: 경고등 소등
6. [OTA Panel] otaInProgress = 1 설정
   → OTA_Server: DoIP → 0x10 0x02 → 0x34 → 0x36(×4) → 0x37
   → BCM: CRC 검증 → 재시작
```

---

## 주요 메시지 ID 참조

| 메시지 | ID (hex) | ID (dec) | 채널 | 주기 |
|--------|---------|---------|------|------|
| BCM_FaultStatus | 0x500 | 1280 | CAN-LS | 10ms |
| UDS_Request | 0x7DF | 2015 | CAN-LS | Event |
| UDS_Response | 0x7E8 | 2024 | CAN-LS | Event |
| Cluster_WarnStatus | 0x510 | 1296 | CAN-HS | Event |
| CGW_Status | 0x700 | 1792 | CAN-HS | 100ms |
| DoIP_RoutingActivation | 0xE001 | 57345 | Ethernet | Event |

---

## 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| CAPL 컴파일 에러 `@BCM::overcurrentDetected` | sysvars 미로드 | `cfg/sample_project.sysvars` Import |
| 메시지 수신 안됨 | DBC 채널 불일치 | CAN-LS/CAN-HS 채널 확인 |
| Gateway 라우팅 안됨 | CGW 노드 양쪽 채널 미연결 | Gateway.can을 CAN-LS, CAN-HS 모두 연결 |
| OTA 타임아웃 | 응답 5000ms 초과 | BCM 노드 정상 실행 여부 확인 |
