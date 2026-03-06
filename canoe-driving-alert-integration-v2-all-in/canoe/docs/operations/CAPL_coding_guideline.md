# CAPL Coding Guideline (CANoe SIL)

이 문서는 `canoe/` 작업 시 AI/개발자가 동일하게 따라야 하는 코딩 기준입니다.
현재 Option1 아키텍처(FZ_00~07) 기준으로 정리합니다.

## 0) 우선 적용 규칙 (프로젝트 고정)
- 작업 범위: `canoe/` 폴더만 수정
- 통신 범위: CAN + Ethernet(UDP)만 사용
- ETH 포트: **5000 고정**
- ETH 프레임: **실제 UdpSocket 사용**, sysvar 경유 금지
  - 대상: `0x510`, `0x511`, `0x512`, `E100`, `E200`
- `BODY_GW`, `IVI_GW`: **udpReceive(5000) -> CAN 송신** (sysvar 브리지 금지)

## 1) 메시지 페이로드 규격 (고정)
- `E100` DLC=4
  - `b0 = (type | (dir << 2))`
  - `b1 = eta`
  - `b2 = sourceId`
  - `b3 = alertState`
- `E200` DLC=2
  - `b0 = (alertLevel | (alertType << 3))`
  - `b1 = timeoutClear`

## 2) sysvar 사용 원칙
- 허용: Panel I/O, 내부 상태 저장, 디버그/모니터링
- 금지: ETH 전송/수신 데이터 경유 채널로 사용
- CAN<->sysvar 게이트웨이 노드에서만 브리지 사용

## 3) CAPL 문법/스타일 규칙
- `variables {}`: 전역 선언만
- 이벤트 핸들러 내부 지역변수는 선언/대입 분리
- 배열 초기화는 `on start`에서 수행
- 타이머 재주기는 `on timer` 마지막에 `setTimer()` 호출
- 네이밍: 노드 역할이 드러나도록 `*_GW`, `*_CTRL`, `*_MGR`, `*_RX`, `*_TX`

## 4) 인코딩/로그 규칙 (필수)
- 파일 인코딩: UTF-8
- `write()` 문자열: **ASCII only** 권장
  - 금지: 이모지, 스마트쿼트, 특수 대시(—), 박스문자
- 로그 프리픽스 통일: `[NodeName]`

예시:
```c
write("[EMS_ALERT_RX] rx E100 type=%d dir=%d eta=%d", type, dir, eta);
write("[WARN_ARB_MGR] selected level=%d type=%d", level, alertType);
```

## 5) UdpSocket 사용 패턴
- 시작 시 소켓 생성/바인딩 실패 처리
- 전송 시 payload 길이(DLC)와 바이트 packing 명시
- 수신 시 길이 검증 후 파싱
- watchdog(1000ms) 타임아웃 처리 로직 분리

## 6) 구현 체크리스트
- [ ] UDP 포트 5000 하드코딩 반영
- [ ] E100/E200 packing 규격 일치
- [ ] ETH 경로에서 sysvar 경유 없음
- [ ] BODY_GW/IVI_GW가 udpReceive 기반
- [ ] watchdog 1000ms 동작
- [ ] WARN_ARB_MGR 우선순위(Ambulance > Police > Zone > Idle)
- [ ] FZ_001~007 시나리오 재현 가능

## 7) 검증 기준
- MCP `get_bus_nodes_info`에서 13개 노드 확인
- CAPL 컴파일 에러 0건
- FZ_001~007 모두 pass

## 8) MCP 자동화 충돌 방지 규칙 (필수)
- CANoe MCP 호출은 **순차 1개씩**만 실행 (병렬 호출 금지)
- 측정 시작 시퀀스 고정:
  - `open_configuration -> wait(2~3s) -> compile_capl_nodes -> wait(2~3s) -> start_measurement`
- `User interface is busy` 발생 시 즉시 중단 후 아래 순서만 수행:
  - `wait(2~3s) -> get_connection_status -> (running이면 stop_measurement 1회) -> open_configuration 1회 재시도`
- busy 재시도는 최대 2회까지만 허용하고, 실패 시 상태를 즉시 보고

## 9) 신호 접근 패턴 (Signal Access BP)

> **근거**: Vector CANoe 19.4 공식 샘플 직접 분석
> - `canoe/reference/vector_samples_19_4_10/CAN/CANBasic/Nodes/engine.can`
> - `canoe/reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Nodes/Gateway.can`
> - `canoe/reference/vector_samples_19_4_10/CAN/CANBasic/Nodes/display.can`

### 두 가지 패턴 비교

| 항목 | `$` 시그널 접근 | `message` + `output()` |
|------|----------------|------------------------|
| 레이어 | IL (Interaction Layer) 경유 | Raw CAN 직접 송신 |
| TX 방식 | `$MsgName::SignalName = value;` | `message M m; m.Signal = v; output(m);` |
| 주기 관리 | IL이 자동으로 사이클 관리 | 노드가 타이머로 직접 관리 |
| Vector 권장 용도 | 패널 제어 스크립트, 테스트 시퀀스 | ECU 시뮬레이션 노드 (자체 사이클) |
| IL 설정 필요 | **필요** (CFG에 IL 구성 필요) | 불필요 |

### Vector 공식 샘플 실사례

```c
/* CANBasic/engine.can — $ 패턴 (TX, panel-driven) */
on sysvar sysvar::Engine::EngineStateSwitch
{
  $EngineState::OnOff = @this;                              // 신호 직접 대입
  $EngineState::EngineSpeed = @sysvar::Engine::EngineSpeedEntry;
}

/* CANBasic/display.can — this 패턴 (RX, on message 내부) */
on message EngineState
{
  if (this.dir == RX)
    @sysvar::Engine::EngineSpeedDspMeter = this.EngineSpeed / 1000.0;
}

/* CANSystem/Gateway.can — 완전 한정 $ 패턴 (크로스 버스 게이트웨이) */
on pdu msgchannel1.EngineData
{
  $Comfort::Gateway::Gateway_2::CarSpeed =
      0.621371 * $PowerTrain::Engine::ABSdata::CarSpeed;   // 버스 간 신호 라우팅
  $EngineRunning = $IdleRunning;
}
```

### 우리 프로젝트 적용 기준

**ECU 시뮬레이션 노드** (`*_CTRL`, `*_GW`, `*_MGR`) → **`message` + `output()` 유지**
- IL 없이 단일 채널 SIL 환경에서 자체 타이머로 사이클을 직접 관리함
- `$` 는 IL이 설정된 CFG에서만 실제 CAN 버스에 출력됨
- 현재 구현이 더 안전하고 동작 보장됨

```c
/* 우리 프로젝트 표준 — ECU 시뮬 노드 TX */
on timer tBrakeCycle
{
  message frmBrakeStatusMsg mStatus;
  mStatus.BrakePressure = brakePressure;
  output(mStatus);               // 직접 송신 — IL 불필요
  setTimer(tBrakeCycle, 100);
}
```

**패널 연동 / 테스트 스크립트** → **`$` 패턴 권장**
- sysvar 변경에 반응해서 CAN 신호 하나를 즉시 바꿀 때
- 테스트 시퀀스에서 자극값을 주입할 때

```c
/* 패널/테스트 스크립트에서 신호 하나 주입할 때 */
on sysvar sysvar::Chassis::vehicleSpeed
{
  $frmVehicleStateCanMsg::gVehicleSpeed = (int)@this;
}
```

**RX 신호 읽기** → 항상 **`this.SignalName`** (`on message` 내부)

```c
on message frmPedalInputCanMsg
{
  gAccelPedal = this.AccelPedal;    // on message 내부에서 this 사용
}
```

### 요약

| 상황 | 권장 패턴 |
|------|----------|
| ECU 시뮬 노드 TX (주기 타이머) | `message` + `output()` ✅ |
| 패널/sysvar 변화 → 신호 즉시 반영 | `$SignalName = value;` ✅ |
| 크로스 버스 게이트웨이 라우팅 | `$Cluster::Node::Msg::Signal` ✅ |
| on message 내 수신 신호 읽기 | `this.SignalName` ✅ |

---
최종 업데이트: 2026-03-02
