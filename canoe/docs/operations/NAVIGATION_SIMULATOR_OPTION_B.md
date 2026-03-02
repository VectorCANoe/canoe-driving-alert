# Navigation Simulator (Option B)

## 목적
- Grid 기반 좌표 이동으로 `Infotainment::roadZone`/`navDirection`를 자동 생성한다.
- CANoe COM API로 sysvar를 주입해 SIL 시나리오를 반복 재현한다.
- XVP는 CAPL이 생성한 `UiRender::*` 파생 출력만 바인딩한다.

## 스크립트
- `canoe/scripts/navigation_simulator.py`

## 권장 패널
- `canoe/project/panel/SDV_Render_Debug.xvp`
- `canoe/project/panel/SDV_Demo_Stage.xvp`
- `canoe/project/panel/SDV_Cluster_View.xvp`
- 렌더 파생값(`UiRender::*`)이 50ms 주기로 갱신되는지 확인한다.

## 사전 조건
1. CANoe 실행 상태
2. `canoe/cfg/CAN_500kBaud_1ch_split.cfg` 로드
3. `project.sysvars`에 `UiRender` 네임스페이스 반영
4. 측정 시작(F9)

## 기본 실행
```powershell
python canoe/scripts/navigation_simulator.py --loop --interval-ms 250
```

## 주요 옵션
- `--width`, `--height`: Grid 크기
- `--interval-ms`: 스텝 주기(ms)
- `--steps`: 실행 스텝 수 (`0`=무한)
- `--loop`: path 끝까지 가면 반복
- `--random-walk`: 지그재그 path 대신 랜덤 이동
- `--no-speed-update`: `Chassis::*` 주입 생략
- `--dry-run`: COM 주입 없이 로그만 출력

## 주입 변수
- Navigation 입력:
  - `Infotainment::roadZone`
  - `Infotainment::navDirection`
  - `Infotainment::zoneDistance`
  - `Infotainment::speedLimit`
- 선택 주입(기본 활성):
  - `Chassis::vehicleSpeed`
  - `Chassis::driveState`
  - `Chassis::steeringInput`

## 운영 메모
- 본 스크립트는 입력 시뮬레이터다. 경고 우선순위/타임아웃/중재 판정은 CAPL이 담당한다.
- `Test::testScenario`를 자동으로 `0`으로 맞춘 뒤 수동/외부 입력 모드로 동작한다.
- 랜덤 모드는 재현성을 위해 `--seed`를 함께 기록한다.
