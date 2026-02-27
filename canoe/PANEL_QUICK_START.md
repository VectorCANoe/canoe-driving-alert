# CANoe Panel Quick Start (FZ_001~FZ_007)

이 문서는 CANoe GUI 패널을 통해 경고 시나리오를 바로 확인하기 위한 실사용 가이드입니다.
범위: CANoe SIL, CAN + Ethernet(UDP), `feature/fz00-07-development`.

## 1) 핵심 개념
- Panel = CANoe의 시각 UI 화면입니다.
- 사용자는 Panel에서 sysvar 값을 바꾸고, CAPL 노드가 CAN/UDP를 통해 처리합니다.
- 결과는 다음 두 경로로 확인합니다.
  - 시각 확인: Panel 인디케이터/텍스트
  - 기술 확인: Trace/Signal (`0x210`, `0x220`, `0xE100`, `0xE200`)

## 2) 입력 바인딩 (Panel -> System Variable)
아래 변수로 패널 컨트롤을 연결하면 됩니다.

- `Chassis::vehicleSpeed` (Slider, 0~255)
- `Chassis::driveState` (Combo: 0=P,1=R,2=N,3=D)
- `Chassis::steeringInput` (Toggle: 0/1)
- `Infotainment::roadZone` (Combo: 0=Normal,1=School,2=Highway,3=Guide)
- `Infotainment::navDirection` (Combo: 0=None,1=Left,2=Right,3=Other)
- `Infotainment::zoneDistance` (Slider, 0~255)
- `V2X::alertState` (Toggle: 0=Clear,1=Active)
- `V2X::emergencyDirection` (Combo: 0=Front,1=Left,2=Right,3=Rear)
- `V2X::eta` (Slider, 0~255)

## 3) 출력 바인딩 (System Variable -> Panel)
- `Body::ambientMode` (Numeric/State)
- `Body::ambientColor` (Numeric/Palette)
- `Body::ambientPattern` (Numeric/Pattern)
- `Cluster::warningTextCode` (Numeric/Text)

## 4) 네트워크/노드 확인 체크
측정 시작 후 아래가 만족되어야 정상입니다.
- Simulation Setup 노드 13개 active
- UDP 포트 5000 사용
- CAPL compile error 0
- CAN 통신 프레임 관측 가능

관측 추천 메시지:
- 입력 CAN: `frmVehicleStateCanMsg(0x100)`, `frmSteeringCanMsg(0x101)`, `frmNavContextCanMsg(0x110)`
- 코어 UDP: `E100`, `E200`
- 출력 CAN: `frmAmbientControlMsg(0x210)`, `frmClusterWarningMsg(0x220)`

## 5) 시나리오 실행 순서 (GUI)
### S0. 기본 상태
- `driveState=3`, `roadZone=0`, `alertState=0`
- 기대: `ambientMode=0`, `warningTextCode=0`

### S1. 스쿨존 과속
- `roadZone=1`, `vehicleSpeed>30`, `alertState=0`
- 기대: Zone 경고 출력(`0x210/0x220` 변화)

### S2. 고속도로 무조향
- `roadZone=2`, `steeringInput=0`, `alertState=0`
- 기대: Highway 경고 출력

### S3. 경찰 경고
- `alertState=1`, (경찰 노드 활성 상태)
- 기대: Emergency 경고가 Zone보다 우선

### S4. 구급 경고
- `alertState=1`, (구급 노드 활성 상태)
- 기대: Emergency 경고 우선 + 구급 타입 반영

경찰/구급을 개별 확인하려면:
- S3(경찰 단독): `EMS_AMB_TX` 노드를 비활성화하고 측정
- S4(구급 단독): `EMS_POLICE_TX` 노드를 비활성화하고 측정

### S5. 우선순위 확인
- 경찰/구급 경고가 동시에 들어오는 조건
- 기대: Ambulance > Police

### S6. 타임아웃 해제
- 긴급 입력 갱신 중단 후 1000ms 경과
- 기대: `timeoutClear` 기반 복귀, 경고 해제

## 6) 트러블슈팅 (MCP 자동화)
반드시 아래 순서를 유지합니다.
- 병렬 호출 금지 (순차 1개씩)
- `open -> wait(2~3s) -> compile -> wait(2~3s) -> start`
- busy 발생 시 즉시 중단 후:
  - wait(2~3s)
  - `get_connection_status`
  - running이면 `stop_measurement` 1회
  - `open_configuration` 1회 재시도
- 재시도 최대 2회

## 7) 중요 주의
- SIL 결과는 "시뮬레이션 표시"입니다. 실제 차량 하드웨어 점등/표시는 아닙니다.
- `00~07` 문서는 구현 참조용이며, 구현/운영 변경은 `canoe/`에서만 수행합니다.
