# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 — 시스템 설계 (기능 분해 및 ECU 할당)
**ASPICE Reference**: SYS.3 (BP1: 시스템 아키텍처 개발, BP2: 인터페이스 정의, BP3: 기능 할당)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 중단 — SYS.3 시스템 아키텍처 | `06_Integration_Test.md` (SWE.5) | `01_Requirements.md` | `0302_NWflowDef.md` |

---

| 노드 | 기능 상세 | 비고 |
|------|---------|------|
| | | **입력층 A — CAN-LS (125 kbps)** |
| Vehicle_ECU | gVehicleSpeed(0~200 km/h, 8bit) / gAccelValue(-10~10 m/s², 8bit signed) / gBrakeValue(0~10 m/s², 8bit)를 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 보고. 과속 기준은 gRoadZone에 따라 다름. | 입력층 A 핵심 노드. Req_001~003 대응. |
| MDPS_ECU | SteeringInput(1bit: 0/1) / gLaneChangeAlert(1bit: 0/1) / SteeringAngleRate(8bit, °/s)를 CAN-LS 0x110으로 100ms 주기 보고. 조향각속도 > 50°/s 시 gLaneChangeAlert = 1. | 입력층 B + 해제층(핸들 입력). Req_005, Req_010 대응. |
| LDW_ECU | gLaneDeparture(1bit: 0/1)를 CAN-LS 0x120으로 100ms 주기 보고. 차선이탈 감지 시 1 설정. | 입력층 B. Req_004 대응. |
| | | **판단층 — CAN-HS (500 kbps)** |
| WDM_ECU | CAN-LS 입력 신호 수신 → Rule-Based 판단 → gWarningLevel(0~3) 설정 → 출력 ECU 제어 명령 CAN-HS 전송. A 단독 OR B 단독 → 1단계. A AND B → 2단계. A+B+OTA조건 → 3단계. gRoadZone별 임계값 적용. gAccelCount 타이머(10분) 관리. | 판단층 핵심. Req_006~008, Req_011~013 대응. |
| | | **Gateway Domain** |
| CGW | CAN-LS(입력층 신호) → CAN-HS(WDM_ECU) 라우팅 (지연 ≤5ms). DoIP Routing Activation(0xE001) 처리. UDS 메시지 포워딩. Bus Off 감지 → 세션 중단 + DTC U0300 저장. | Req_018 대응 (Bus Off). |
| | | **출력층 — CAN-HS (500 kbps)** |
| Cluster_ECU | WDM_Warning(0x200) 수신 → gWarningLevel에 따라 경고등 제어. 1단계: 황색(WarnLampLevel=1). 2단계: 적색(WarnLampLevel=2). 0단계: 소등. 50ms 이내 활성화. | Req_006, Req_007 대응. |
| Ambient_ECU | Ambient_Control(0x220) 수신 → AmbientMode별 패턴 출력. 스쿨존: RED 빠른 점멸(200ms). 고속도로: ORANGE 파동(1초). IC출구: 좌→우 흐름 애니메이션. | 준영 담당. Req_012~014 대응. |
| Sound_ECU | Sound_Control(0x230) 수신 → 단계별 경고음 출력. 1단계: 단발음. 2단계: 연속음. 3단계: 긴급음. | Req_006, Req_007 대응. |
| IVI_ECU | IVI_Status(0x240) 수신 → OTA 구독 팝업 표시. [지금 무료 체험] / [나중에] 선택. 진행률 바 표시. | 성현 담당. Req_008, Req_015, Req_016 대응. |
| Door_ECU | Door_Control(0x250) 수신 → 3초 도어 잠금 + Mirror LED 점멸. 3단계 물리 개입. | 현준2 담당. Req_008 부속 출력. |
| | | **OTA Domain** |
| OTA_Server | DoIP Routing Activation → UDS 0x10 0x02(Programming Session) → 0x27(Security Access) → 0x34(Download Request) → 0x36 4KB 블록 전송 → 0x37(Transfer Exit) → CRC-32 검증 → ECU 재시작. 실패 시 Rollback. | 성현 담당. Req_015~017 대응. |
| | | **해제층** |
| 응시 복귀 (sysvar) | sysvar::Driver::GazeActive = 0 → 1 전환 시 WDM_ECU가 gWarningLevel = 0으로 초기화. CANoe Panel Button으로 주입. | 라엘 담당. Req_009 대응. |
| 핸들 입력 (MDPS_ECU) | SteeringInput = 1 수신 시 WDM_ECU가 gWarningLevel = 0으로 초기화. | 현준 담당. Req_010 대응. |
| | | **CANoe Panel** |
| CANoe Panel | gRoadZone 버튼(4개) / 속도·가속도 TrackBar / 차선이탈·급차선변경 Switch / GazeActive·SteeringInput Button / OTA 트리거 Button / 상태 Indicator | SIL 환경 사용자 인터페이스 전체. |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
