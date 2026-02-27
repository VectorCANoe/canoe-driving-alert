# PANEL DEVELOPMENT SPEC (Aligned with 00~07)

## 1) 기준 문서
- 00_VModel_Mapping
- 01_Requirements
- 02_Concept_design
- 03_Function_definition
- 0301_SysFuncAnalysis
- 0302_NWflowDef
- 0303_Communication_Specification
- 0304_System_Variables
- 04_SW_Implementation
- 05_Unit_Test
- 06_Integration_Test
- 07_System_Test

본 스펙은 위 문서의 최신 정합(Option1, Comm_006 단계 분해, Cluster=Infotainment CAN)을 반영한다.

## 2) 아키텍처 고정점 (Panel 관점)
- Option1 고정: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어`
- 검증 범위: CANoe SIL, CAN + Ethernet(UDP)
- 핵심 출력:
  - Ambient: `frmAmbientControlMsg(0x210)`
  - Cluster: `frmClusterWarningMsg(0x220)` (Infotainment CAN 경로)

## 3) Panel 화면 구성

### Page A: Drive Input
- `Chassis::vehicleSpeed` (Slider, 0~255)
- `Chassis::driveState` (Combo: P/R/N/D -> 0/1/2/3)
- `Chassis::steeringInput` (Toggle 0/1)

### Page B: Navigation Input
- `Infotainment::roadZone` (0=Normal,1=School,2=Highway,3=Guide)
- `Infotainment::navDirection` (0=None,1=Left,2=Right,3=Other)
- `Infotainment::zoneDistance` (Slider, 0~255)

### Page C: Emergency Input
- `V2X::alertState` (Toggle 0/1)
- `V2X::emergencyDirection` (0/1/2/3)
- `V2X::eta` (0~255)

### Page D: Output Monitor
- `Body::ambientMode`
- `Body::ambientColor`
- `Body::ambientPattern`
- `Cluster::warningTextCode`
- (권장) `Core::selectedAlertLevel`, `Core::selectedAlertType`, `Core::timeoutClear`

## 4) 변수 명명 규칙 (문서 정합)
- Panel 바인딩 기준은 0304 표준 Name 계약을 따른다.
- 0302/0303의 g* 별칭은 구현/호환 매핑용으로만 해석한다.
- 신규 패널 위젯은 g* 네임스페이스를 직접 사용하지 않는다.

## 5) 시나리오 동선 (GUI)

### Scenario 1: Normal Idle
- 입력: driveState=D, roadZone=Normal, alertState=0
- 기대: ambient 0, cluster code 0

### Scenario 2: School Zone Overspeed
- 입력: roadZone=School, speed>30
- 기대: Zone 경고 출력(0x210/0x220 변화)

### Scenario 3: Highway No Steering
- 입력: roadZone=Highway, steeringInput=0
- 기대: Highway 경고 출력

### Scenario 4: Emergency Override
- 입력: Zone 경고 활성 상태에서 alertState=1
- 기대: Emergency > Navigation 우선 적용

### Scenario 5: Ambulance Priority
- 입력: 경찰/구급 충돌 조건
- 기대: Ambulance > Police

### Scenario 6: Timeout Recovery
- 입력: 긴급 갱신 중단
- 기대: 1000ms 후 timeoutClear 기반 복귀

## 6) 캡처 증적 규칙
각 시나리오마다 아래 2종 캡처를 남긴다.
- Panel 캡처: 입력값 + 출력값
- Trace 캡처: 해당 CAN/UDP 메시지 변화 구간

결과 기록은 `canoe/PANEL_PASS_CHECKLIST.md` 표를 사용한다.

## 7) 완료 정의 (DoD)
- Panel에서 FZ_001~FZ_007 시나리오를 연속 재현 가능
- 각 시나리오에 Panel+Trace 캡처 2종 증적 존재
- 출력 경로가 0302/0303/04/07 정의와 충돌하지 않음
- busy 트러블슈팅 규칙을 준수해 재현성 확보

## 8) 운영 규칙
- CANoe MCP 자동화는 `canoe/AGENTS.md` 규칙을 따른다.
- 병렬 제어 금지, `open -> wait -> compile -> wait -> start` 고정.
