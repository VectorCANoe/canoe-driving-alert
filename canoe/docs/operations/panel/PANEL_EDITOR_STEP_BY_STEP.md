# PANEL EDITOR STEP-BY-STEP (Click Guide)

이 문서는 CANoe Panel Editor에서 패널을 실제로 만드는 클릭 순서를 제공합니다.
기준: `canoe/PANEL_DEVELOPMENT_SPEC.md`.

## 0) 시작 전
1. CANoe 실행
2. `File -> Open Configuration` 에서 `canoe/cfg/CAN_v2_topology_wip.cfg` 열기
3. 측정은 정지 상태 유지 (`F9` Off)

## 1) Panel 생성
1. `View -> Panel Designer` 열기
2. `Panels` 트리에서 새 Panel 생성 (`New Panel`)
3. 패널 이름: `Main_Control_Panel`
4. 캔버스 크기: 가로 1400, 세로 900 권장

## 2) Page A (Drive Input) 구성
### A-1. 그룹 박스
1. `Toolbox -> Group Box` 드래그
2. 제목: `Drive Input`

### A-2. vehicleSpeed
1. `Toolbox -> Slider` 추가
2. Label: `vehicleSpeed`
3. Properties -> Data Binding -> System Variable 선택
4. 변수: `Chassis::vehicleSpeed`
5. Min=0, Max=255

### A-3. driveState
1. `Toolbox -> ComboBox` 추가
2. Label: `driveState`
3. Binding: `Chassis::driveState`
4. Items 추가:
   - `0:P`
   - `1:R`
   - `2:N`
   - `3:D`

### A-4. steeringInput
1. `Toolbox -> Toggle Button` 추가
2. Label: `steeringInput`
3. Binding: `Chassis::steeringInput`
4. Off=0, On=1

## 3) Page B (Navigation Input) 구성
### B-1. 그룹 박스
1. `Group Box` 추가, 제목 `Navigation Input`

### B-2. roadZone
1. `ComboBox` 추가, Binding: `Infotainment::roadZone`
2. Items:
   - `0:Normal`
   - `1:School`
   - `2:Highway`
   - `3:Guide`

### B-3. navDirection
1. `ComboBox` 추가, Binding: `Infotainment::navDirection`
2. Items:
   - `0:None`
   - `1:Left`
   - `2:Right`
   - `3:Other`

### B-4. zoneDistance
1. `Slider` 추가, Binding: `Infotainment::zoneDistance`
2. Min=0, Max=255

## 4) Page C (Emergency Input) 구성
### C-1. 그룹 박스
1. `Group Box` 추가, 제목 `Emergency Input`

### C-2. alertState
1. `Toggle Button` 추가, Binding: `V2X::alertState`
2. Off=0, On=1

### C-3. emergencyDirection
1. `ComboBox` 추가, Binding: `V2X::emergencyDirection`
2. Items:
   - `0:Front`
   - `1:Left`
   - `2:Right`
   - `3:Rear`

### C-4. eta
1. `Slider` 추가, Binding: `V2X::eta`
2. Min=0, Max=255

### C-5. emergencyType
1. `ComboBox` 추가, Binding: `V2X::emergencyType`
2. Items:
   - `0:None`
   - `1:Police`
   - `2:Ambulance`

### C-6. testScenario
1. `ComboBox` 또는 `Numeric Input` 추가, Binding: `Test::testScenario`
2. 권장 항목:
   - `0:Manual`
   - `1:Normal`
   - `2:School`
   - `3:Highway`
   - `4:Police`
   - `5:Ambulance`
   - `6:Timeout Prep`
   - `100:Auto Demo`

## 5) Page D (Output Monitor) 구성
### D-1. 그룹 박스
1. `Group Box` 추가, 제목 `Output Monitor`

### D-2. Ambient 출력 표시
1. `Numeric Display` 3개 추가
2. Binding:
   - `Body::ambientMode`
   - `Body::ambientColor`
   - `Body::ambientPattern`

### D-3. Cluster 출력 표시
1. `Numeric Display` 추가
2. Binding: `Cluster::warningTextCode`

### D-4. Core 디버그(권장)
1. `Numeric Display` 3개 추가
2. Binding:
   - `Core::selectedAlertLevel`
   - `Core::selectedAlertType`
   - `Core::timeoutClear`

## 6) 저장 및 실행
1. `Ctrl+S` 저장
2. 측정 시작 (`F9`)
3. 입력 변경 시 출력 변화를 확인:
   - Ambient: `Body::*`
   - Cluster: `Cluster::warningTextCode`

## 7) 빠른 검증 시퀀스
1. 기본: `driveState=3`, `roadZone=0`, `alertState=0`
2. 스쿨존: `roadZone=1`, `vehicleSpeed=45`
3. 고속도로: `roadZone=2`, `steeringInput=0`
4. 긴급: `alertState=1`
5. 복귀: `alertState=0`
6. 자동 데모: `testScenario=100` 시작, `testScenario=0` 중지

## 8) 흔한 실수 체크
- g* 변수(`gRoadZone`)에 직접 바인딩하지 않기
- `Chassis/Infotainment/V2X` 표준 변수에 바인딩했는지 재확인
- 출력은 `Body/Cluster/Core`에서 확인
- 반응이 없으면 Measurement 상태와 노드 Active 상태 먼저 확인

## 9) 증적 기록
- 캡처 기준은 `canoe/PANEL_PASS_CHECKLIST.md` 사용
- 시나리오별 Panel 화면 + Trace 화면 2종 캡처 저장

