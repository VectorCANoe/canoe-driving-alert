# VCU `86~199` 코드 설명

## 메시지 요약

### CAN Rx 메시지

| Message |
| --- |
| `frmPedalInputCanMsg` |
| `frmIgnitionEngineMsg` |
| `frmGearStateMsg` |
| `frmPowertrainGatewayMsg` |
| `frmVehicleModeMsg` |

### CAN Tx 메시지

| Message |
| --- |
| `frmVehicleStateCanMsg` |
| `frmAccelStatusMsg` |
| `frmTcsStateMsg` |
| `frmWheelPulseMsg` |
| `frmPowertrainGatewayMsg` |
| `frmVehicleModeMsg` |
| `frmPowerLimitMsg` |
| `frmPowertrainHealthMsg` |
| `frmEnergyFlowStateMsg` |
| `frmPowertrainCtrlAuthMsg` |

### Ethernet Rx 메시지

| Message |
| --- |
| 없음 |

### Ethernet Tx 메시지

| Message |
| --- |
| `ethMsgVehicleState` |

## 개요

이 범위의 코드는 VCU가 페달 입력과 Core 상태를 바탕으로 차량 속도, 파워트레인 모드, TCS 상태, 에너지 흐름 등을 계산해 송신하는 구간이다.

즉, 차량 주행 상태를 여러 파워트레인/섀시 메시지로 분배하는 중심 출력 블록이다.

## 단계별 설명

### 1. 페달 입력을 목표 속도로 변환한다.

먼저 가속 페달 값을 기반으로 `targetSpeed`를 만든다.

- 가속 페달이 클수록 목표 속도 증가
- 상한은 200
- 브레이크 입력이 크면 목표 속도를 0으로 강제

즉, 운전자 입력을 속도 제어용 목표값으로 바꾸는 단계다.

### 2. 현재 속도를 목표 속도 방향으로 완만하게 이동시킨다.

그 다음 `delta = targetSpeed - gSpeed`를 계산한 뒤, 증가/감소량에 제한을 둔다.

- 가속 방향은 완만하게 증가
- 감속 방향은 조금 더 크게 감소 허용

이후 `gSpeed`에 반영하고 최종 범위를 `0..255`로 제한한다.

즉, 속도 변화가 한 번에 튀지 않도록 간단한 slew rate를 적용하는 단계다.

### 3. 주행 상태와 정책 입력을 계산한다.

속도가 정해진 뒤에는 다음 값을 계산한다.

- `driveState`
- `gDriveMode`
- `gSpeedLimitNorm`
- `selectedAlertLevel`
- `timeoutClear`
- `failSafeMode`
- `gBoundaryStatus`

이 값들은 이후 routing policy와 파워트레인 출력값을 결정하는 기반이 된다.

### 4. fail-safe와 경고 레벨을 기반으로 routing policy를 결정한다.

이 블록에서는:

- fail-safe 또는 timeout clear이면 가장 보수적인 정책
- 경고 레벨이 높으면 강화된 정책
- 그 외에는 기본 정책

을 선택한다.

즉, 현재 시스템 위험 상태를 파워트레인 routing 동작으로 변환하는 단계다.

### 5. 정규화된 차량 상태를 Core와 chassis 출력에 반영한다.

계산된 속도와 drive state는:

- `@Core::*`
- `@CoreState::routingPolicy`
- chassis-facing 메시지
- `@Chassis::*`

로 동시에 반영된다.

즉, 현재 차량 상태를 여러 계층에서 공통으로 볼 수 있게 미러링한다.

### 6. 가속 요청과 토크 요청을 송신한다.

가속 페달 값에서 토크 요청을 계산하고, 이를 `frmAccelStatusMsg`에 넣어 송신한다.

즉, 운전자 입력을 파워트레인 제어량으로 변환해 내보내는 단계다.

### 7. 단순 TCS 개입 상태를 계산한다.

저속 상태에서 가속 페달이 큰 경우 `tcsActive`를 활성화하고,

- TCS 제어 상태
- 토크 컷
- 슬립 비율

을 메시지에 담아 송신한다.

즉, 간단한 traction control 개입 상황을 흉내 내는 블록이다.

### 8. 휠 펄스와 파워트레인 게이트웨이 상태를 송신한다.

현재 차량 속도를 기반으로 전/후륜 wheel pulse를 만들고,

동시에 routing policy와 boundary status를 powertrain gateway 메시지로 송신한다.

즉, 주행 속도와 도메인 경계 상태를 외부에 배포하는 단계다.

### 9. Drive mode와 파생 모드를 계산한다.

`frmVehicleModeMsg`에서는 다음 값을 구성한다.

- DriveMode
- EcoMode
- SportMode
- SnowMode
- PowertrainState

그리고 일부 값은 `@CoreState::*`에도 미러링한다.

즉, 현재 주행 모드와 파생 운전 특성을 상태값으로 정리하는 단계다.

### 10. 토크/속도 제한, health, 에너지 흐름, 제어 권한을 송신한다.

마지막 구간에서는 순서대로:

- 토크/속도 제한
- powertrain health와 alive counter
- 에너지 흐름과 regen 레벨
- 제어 권한 수준

을 송신한다.

즉, 이 범위의 마지막은 현재 파워트레인 상태를 여러 보조 메시지로 세분화해 출력하는 단계다.

## 정리

이 범위의 코드는 다음 순서로 동작한다.

1. 페달 입력에서 목표 속도 계산
2. 현재 속도 업데이트
3. routing policy 계산
4. 차량 상태 publish
5. TCS/모드/제한/health/energy 상태 publish

즉, 운전자 입력과 Core 상태를 실제 파워트레인 출력 메시지 집합으로 바꾸는 VCU 중심 로직이다.
