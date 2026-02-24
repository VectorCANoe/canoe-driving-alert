# 가상노드 Simulator (입출력 기능) — Function Definition

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 — 시스템 설계 (기능 분해 및 ECU 할당)
**ASPICE Reference**: SYS.3 (BP1: 시스템 아키텍처 설계, BP2: 인터페이스 정의, BP3: 기능 할당)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 중단 — SYS.3 시스템 아키텍처 | `06_Integration_Test.md` (SWE.5) | `01_Requirements.md` | `0301_SysFuncAnalysis.md` |

---

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------|--------|---------|------|------|
| 입력 | 차속 조절 (TrackBar) | Vehicle_ECU 속도(gVehicleSpeed, 0~200 km/h) 조절. 제한속도 초과 시 WDM_ECU 과속 이벤트 감지. | Panel TrackBar. gRoadZone별 기준 자동 적용. | In_Test_01, Scene.3 |
| 입력 | 급가속 주입 (Button) | gAccelValue > 3.5 m/s² 강제 주입 → gAccelCount 카운팅. 10분 타이머 연동. | Switch/Indicator. gAccelCount 패널 표시. | In_Test_02, Scene.3 |
| 입력 | 차선이탈 주입 (Button) | sysvar::LDW::laneDeparture = 1 강제 주입 → WDM_ECU B그룹 감지 트리거. | Switch/Indicator. | In_Test_03, Scene.4 |
| 입력 | gRoadZone 설정 (Button×4) | Panel 버튼 4개로 gRoadZone(0:일반/1:스쿨존/2:고속도로/3:IC출구) 설정. | 버튼 클릭 시 WDM_ECU에 즉시 전달. | In_Test_07~09, Scene.8~10 |
| 입력 | 응시 복귀 주입 (Button) | sysvar::Driver::GazeActive = 0 → 1 전환 주입 → 경고 해제 트리거. | Switch/Indicator. 라엘 담당. | In_Test_05, Scene.6 |
| 입력 | 핸들 입력 주입 (Button) | sysvar::MDPS::SteeringInput = 1 주입 → 경고 해제 트리거. | Switch/Indicator. 현준 담당. | In_Test_06, Scene.7 |
| 입력 | OTA 트리거 (Button) | OTA 구독 동의 시뮬레이션 → OTA_Server UDS 세션 시작. | Switch/Indicator. 성현 담당. | In_Test_10, Scene.11 |
| 출력 | 경고 레벨 표시 | gWarningLevel(0~3) 현재값 Panel Indicator 출력. | 숫자 표시 및 색상 Indicator. | In_Test_04, Scene.3~5 |
| 출력 | Cluster 경고등 | 1단계: 황색 / 2단계: 적색 / 해제: 소등. Panel LED 표시. | Switch/Indicator. | In_Test_01~04, Scene.3~5 |
| 출력 | Ambient 상태 표시 | AmbientMode / AmbientColor / AmbientPattern 현재값 출력. | Switch/Indicator. | In_Test_07~09, Scene.8~10 |
| 출력 | OTA 진행률 | 펌웨어 전송 블록 진행 상태 표시 (0~100%). | Switch/Indicator 진행률 출력. | In_Test_10, Scene.12~14 |
| 출력 | Rollback 상태 | OTA 실패 시 Rollback 완료 여부 표시. | Switch/Indicator. | In_Test_12, Scene.15 |
| ECU 동작 | Vehicle_ECU | gVehicleSpeed / gAccelValue / gBrakeValue를 CAN-LS 0x100으로 WDM_ECU에 100ms 주기 보고. 속도 임계값 초과 시 과속 플래그 설정. | CAPL on timer 100ms. sysvar::Vehicle로 값 제어. | In_Test_01, In_Test_02, Scene.3 |
| ECU 동작 | MDPS_ECU | SteeringInput / gLaneChangeAlert를 CAN-LS 0x110으로 100ms 주기 보고. 급차선변경(조향각속도 >50°/s) 감지 시 alert 플래그. | CAPL on timer 100ms. sysvar::MDPS로 값 제어. | In_Test_03, In_Test_06, Scene.4, Scene.7 |
| ECU 동작 | LDW_ECU | gLaneDeparture를 CAN-LS 0x120으로 100ms 주기 보고. | CAPL on timer 100ms. sysvar::LDW로 값 제어. | In_Test_03, Scene.4 |
| ECU 동작 | WDM_ECU | 입력층 신호 수신 → Rule-Based 판단(A/B/복합) → gWarningLevel 0~3 설정 → 출력층 ECU 제어 명령 CAN-HS 전송. gRoadZone별 임계값 적용. gAccelCount 타이머 관리. | CAPL on message + on timer. 핵심 판단 로직. | In_Test_01~10, Scene.3~11 |
| ECU 동작 | CGW | CAN-LS 신호 → CAN-HS WDM_ECU 라우팅 (≤5ms). DoIP Routing Activation(0xE001) 처리. UDS 메시지 포워딩. | CAPL on message 라우팅 로직. | In_Test_13, Scene.11 |
| ECU 동작 | Cluster_ECU | WDM_Warning(0x200) 수신 → gWarningLevel에 따라 황색/적색/소등 제어. 50ms 이내 활성화. | CAPL on message + warnLamp 제어. | In_Test_01~04, Scene.3~5 |
| ECU 동작 | Ambient_ECU | Ambient_Control(0x220) 수신 → AmbientMode별 패턴 출력(RED 점멸/ORANGE 파동/방향 흐름). | CAPL on message. gRoadZone 연동. | In_Test_07~09, Scene.8~10 |
| ECU 동작 | Sound_ECU | Sound_Control(0x230) 수신 → 단계별 경고음 출력. | CAPL on message. | In_Test_04, Scene.3~5 |
| ECU 동작 | IVI_ECU | IVI_Status(0x240) 수신 → OTA 구독 팝업 표시 / 진행률 갱신. | CAPL on message. 성현 UX 흐름 구현. | In_Test_10, Scene.11~14 |
| ECU 동작 | Door_ECU | Door_Control(0x250) 수신 → 3초 도어 잠금 + Mirror LED. 3단계 물리 개입. | CAPL on message. 현준2 담당. | In_Test_04, Scene.5 |
| ECU 동작 | OTA_Server | DoIP Routing Activation → UDS 0x10(Programming Session) → 0x27(Security Access) → 0x34(Download Request) → 0x36×N(Transfer Data, 4KB 블록) → 0x37(Transfer Exit) → CRC-32 검증 → ECU 재시작. 실패 시 Rollback. | CAPL OTA 전송 로직. Ethernet DoIP 채널 사용. | In_Test_10~12, Scene.11~16 |

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
