# PANEL PASS CHECKLIST (Capture Sheet)

이 문서는 CANoe GUI 캡처만으로 FZ_001~FZ_007 판정을 빠르게 남기기 위한 1페이지 체크리스트입니다.

## 0) 공통 준비
- Configuration: `canoe/cfg/CAN_v2_topology_wip.cfg`
- Measurement: Start
- Active Nodes: 13개 (`SIL_TEST_CTRL` 포함)
- Trace 창에 아래 메시지 표시:
  - `0x100`, `0x101`, `0x110`, `0x210`, `0x220`
- Panel 출력 표시:
  - `Body::ambientMode`, `Body::ambientColor`, `Body::ambientPattern`, `Cluster::warningTextCode`

## 1) FZ_001 Ethernet 전달
- 입력: `V2X::alertState=1`, `V2X::eta=10`, `V2X::emergencyDirection=1`
- 확인: Trace에서 `E100` 계열 수신/중계 이벤트가 주기적으로 갱신
- 캡처: Trace(E100 이벤트), Panel(경고 출력 활성)
- 판정: Pass / Fail

## 2) FZ_002 CAN->ETH 변환
- 입력: `Chassis::driveState=3`, `Chassis::vehicleSpeed=45`, `Chassis::steeringInput=1`
- 확인: 입력 CAN(`0x100`,`0x101`) 변화 후 코어 판단 반영
- 캡처: Trace(`0x100`,`0x101`), Panel(경고/비경고 상태)
- 판정: Pass / Fail

## 3) FZ_003 ETH->CAN 변환
- 입력: 경고 상황 1건 유도(예: 스쿨존 과속)
- 확인: 출력 CAN `0x210`(Ambient), `0x220`(Cluster) 동시 변화
- 캡처: Trace(`0x210`,`0x220`), Panel 출력 값
- 판정: Pass / Fail

## 4) FZ_004 주기 성능
- 입력: 경고 상태 유지 5초
- 확인: 출력 프레임 주기가 설정 범위 내(문서 기준)
- 캡처: Trace 타임스탬프 간격 화면
- 판정: Pass / Fail

## 5) FZ_005 타임아웃(1000ms)
- 입력: 긴급 입력 활성 후 갱신 중단
- 확인: 약 1000ms 후 해제(복귀) 동작
- 캡처: 해제 직전/직후 Trace, Panel 복귀 상태
- 판정: Pass / Fail

## 6) FZ_006 중재 규칙 1 (Emergency > Navigation)
- 입력: Zone 경고 활성 상태에서 Emergency 활성
- 확인: 최종 출력이 Emergency 우선으로 변경
- 캡처: 전환 전/후 Panel + Trace
- 판정: Pass / Fail

## 7) FZ_007 중재 규칙 2 (Ambulance > Police)
- 입력: 경찰/구급 동시 조건
- 확인: 최종 선택이 Ambulance
- 캡처: 동시 조건 입력 화면 + 최종 출력 화면
- 판정: Pass / Fail

## 8) 결과 표 (복붙용)
| Test ID | Result | Capture File | Note |
|---|---|---|---|
| FZ_001 |  |  |  |
| FZ_002 |  |  |  |
| FZ_003 |  |  |  |
| FZ_004 |  |  |  |
| FZ_005 |  |  |  |
| FZ_006 |  |  |  |
| FZ_007 |  |  |  |

## 9) 운영 메모
- 판정은 반드시 캡처(Trace + Panel) 2종 증적을 남긴다.
- busy 충돌 시 `canoe/AGENTS.md` 복구 절차를 그대로 따른다.

