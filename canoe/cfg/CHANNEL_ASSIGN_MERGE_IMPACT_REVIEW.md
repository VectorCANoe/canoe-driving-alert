# Channel Assign Merge Impact Review

## 1. Scope

- 기준 브랜치 비교: `develop...HEAD`
- 분석 대상: `canoe/cfg/channel_assign/` 하위 변경 파일
- 목적:
  - 이번 브랜치 수정으로 영향받는 메시지/시그널 정리
  - 기존 owner 로직과 충돌 가능성이 큰 파일 식별

## 2. Changed Files

- `canoe/cfg/channel_assign/ADAS/ADAS.can`
- `canoe/cfg/channel_assign/Body/BCM.can`
- `canoe/cfg/channel_assign/Body/DOOR_FL.can`
- `canoe/cfg/channel_assign/Body/WIP.can`
- `canoe/cfg/channel_assign/Chassis/ESC.can`
- `canoe/cfg/channel_assign/Chassis/VCU.can`
- `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can`
- `canoe/cfg/channel_assign/Infotainment/AMP.can`
- `canoe/cfg/channel_assign/Infotainment/CLU.can`
- `canoe/cfg/channel_assign/Infotainment/OTA.can`
- `canoe/cfg/channel_assign/Infotainment/TMU.can`
- `canoe/cfg/channel_assign/Powertrain/EMS.can`

## 3. Impacted Messages And Signals

### 3.1 Powertrain / Display

File: [EMS.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Powertrain/EMS.can)

- 입력 메시지
  - `frmIgnitionEngineMsg.IgnitionState`
  - `frmIgnitionEngineMsg.EngineState`
  - `frmPedalInputCanMsg.AccelPedal`
  - `frmPedalInputCanMsg.BrakePedal`
  - `frmVehicleStateCanMsg.gVehicleSpeed`
- 출력 메시지
  - `frmEngineSpeedTempMsg.EngineRpm`
  - `frmEngineSpeedTempMsg.CoolantTemp`
  - `frmEngineSpeedTempMsg.OilTemp`
  - `frmFuelBatteryStateMsg.FuelLevel`
  - `frmFuelBatteryStateMsg.BatterySoc`
  - `frmThrottleStateMsg.ThrottlePos`
  - `frmThrottleStateMsg.ThrottleReq`
  - `frmEngineTorqueMsg.EngineTorqueAct`
  - `frmEngineLoadMsg.EngineLoad`
  - `frmThermalMgmtStateMsg.ThermalMode`
  - `frmThermalMgmtStateMsg.FanDuty`
  - `frmThermalMgmtStateMsg.CoolantTarget`
- 영향 sysvar
  - `Display::animFrame`
  - `Powertrain::fuelLevel`
  - `Powertrain::coolantTemp`
  - `Core::selectedAlertLevel`
  - `Core::selectedAlertType`
  - `CoreState::seatBeltWarnLvl`
  - `Body::doorOpenCmd`
  - `Body::doorLockCmd`
  - `V2X::policePos`
  - `V2X::ambulancePos`
  - `Infotainment::roadZone`
  - `Chassis::ignitionCmd`

메모:
- `animFrame` owner 역할과 powertrain 표시 로직이 같은 파일에 공존한다.
- 시동 상태, 연료 게이지, 경고 표시가 함께 바뀌므로 병합 충돌 후 부작용이 크다.

### 3.2 Vehicle State / Drive Mode / Speed

File: [VCU.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Chassis/VCU.can)

- 입력 메시지
  - `frmPedalInputCanMsg.AccelPedal`
  - `frmPedalInputCanMsg.BrakePedal`
  - `frmIgnitionEngineMsg.IgnitionState`
  - `frmIgnitionEngineMsg.EngineState`
  - `frmGearStateMsg.GearInput`
  - `frmGearStateMsg.GearState`
  - `frmVehicleModeMsg.DriveMode`
  - `frmVehicleModeMsg.PowertrainState`
  - `frmNavModuleStateMsg.NavSpeedLimit`
  - `frmWheelSpeedMsg.WheelSpdFL`
  - `frmWheelSpeedMsg.WheelSpdFR`
  - `frmWheelSpeedMsg.WheelSpdRL`
  - `frmWheelSpeedMsg.WheelSpdRR`
- 출력 메시지
  - `frmVehicleStateCanMsg.gVehicleSpeed`
  - `frmVehicleStateCanMsg.gDriveState`
  - `frmAccelStatusMsg.AccelRequest`
  - `frmAccelStatusMsg.TorqueRequest`
  - `frmTcsStateMsg.TcsCtrlState`
  - `frmWheelPulseMsg.WheelPulseFront`
  - `frmWheelPulseMsg.WheelPulseRear`
  - `frmPowertrainGatewayMsg.RoutingPolicy`
  - `frmPowertrainGatewayMsg.BoundaryStatus`
  - `frmVehicleModeMsg.DriveMode`
  - `frmVehicleModeMsg.EcoMode`
  - `frmVehicleModeMsg.SportMode`
  - `frmVehicleModeMsg.SnowMode`
  - `frmVehicleModeMsg.PowertrainState`
  - `frmPowerLimitMsg.TorqueLimit`
  - `frmPowerLimitMsg.SpeedLimit`
  - `frmEnergyFlowStateMsg.EnergyFlowMode`
  - `frmEnergyFlowStateMsg.RegenLevel`
  - `frmEnergyFlowStateMsg.PowerBalance`
- 영향 sysvar
  - `Chassis::vehicleSpeed`
  - `Chassis::driveState`
  - `Chassis::throttlePosition`
  - `Chassis::brakePressure`
  - `Chassis::ignitionCmd`
  - `Chassis::transGear`
  - `CoreState::domainBoundaryStatus`
  - `Core::failSafeMode`
  - `Core::emergencyContext`

메모:
- 수동 패널 입력과 테스트 시나리오 입력이 모두 모이는 핵심 owner 파일이다.
- `driveMode`, `gearState`, `vehicleSpeed`가 병합 충돌의 중심이다.

### 3.3 Brake / Suspension / Chassis Output

File: [ESC.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Chassis/ESC.can)

- 입력 메시지
  - `frmVehicleStateCanMsg.gVehicleSpeed`
  - `frmVehicleStateCanMsg.gDriveState`
  - `frmSteeringCanMsg.SteeringInput`
  - `frmPedalInputCanMsg.BrakePedal`
  - `frmAebDomainStateMsg.StopReq`
  - `frmAebDomainStateMsg.DecelProfile`
  - `frmAebDomainStateMsg.DomainHealth`
- 출력 메시지
  - `frmWheelSpeedMsg`
  - `frmYawAccelMsg`
  - `frmBrakeStatusMsg.BrakePressure`
  - `frmBrakeStatusMsg.BrakeMode`
  - `frmEscStateMsg`
  - `frmBrakeTempMsg`
  - `frmBrakeWearMsg`
  - `frmSuspensionStateMsg`
  - `frmRoadFrictionMsg`
- 영향 sysvar
  - `Chassis::brakePedalBtn`
  - `Chassis::brakePressure`
  - `Chassis::brakeLamp`
  - `Chassis::absActive`

메모:
- `brakePressure`와 `frmSuspensionStateMsg` owner라서 다른 ECU 및 `TEST_SCN`과 충돌하기 쉽다.

### 3.4 Body / Lamp / Comfort

File: [BCM.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/BCM.can)

- 입력 메시지
  - `frmDoorFlStateMsg`
  - `frmDoorFrStateMsg`
  - `frmDoorRlStateMsg`
  - `frmDoorRrStateMsg`
  - `frmTailgateStateMsg`
  - `frmPhoneAsKeyStateMsg`
  - `frmTmuServiceStateMsg`
  - `frmHvacStateMsg`
  - `frmVehicleStateCanMsg`
  - `frmAdasDomainStateMsg`
  - `frmTurnLampInputMsg`
- 출력 메시지
  - `frmHazardControlMsg`
  - `frmWindowControlMsg`
  - `frmLampControlMsg`
  - `frmSeatBeltStateMsg`
  - `frmCabinAirStateMsg`
  - `frmDoorControlMsg`
  - `frmBodyComfortStateMsg`
  - `frmRainLightAutoMsg`
- 영향 sysvar
  - `Body::manualTurnCmd`
  - `Body::blinkLeft`
  - `Body::blinkRight`
  - `Body::ambientMode`
  - `Body::ambientColor`
  - `Body::ambientPattern`
  - `Infotainment::navDirection`
  - `Core::selectedAlertLevel`
  - `CoreState::turnLampState`
  - `CoreState::seatBeltWarnLvl`

메모:
- turn lamp, seat belt, cabin air, comfort control이 함께 걸려 있다.
- 상위 경고 상태와 바디 상태가 같이 묶여 있어 side effect가 잘 발생한다.

### 3.5 Door Front Left Owner

File: [DOOR_FL.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/DOOR_FL.can)

- 입력 메시지
  - `frmDoorControlMsg.DoorControlCmd`
  - `frmVehicleStateCanMsg.gDriveState`
  - `frmDigitalKeyStateMsg.VehicleAccessState`
  - `frmDigitalKeyStateMsg.KeyPresence`
  - `frmImmobilizerStateMsg.ImmobilizerState`
  - `frmImmobilizerStateMsg.KeyAuthState`
- 출력 메시지
  - `frmDoorFlStateMsg.DoorFlOpenState`
  - `frmDoorFlStateMsg.DoorFlLockState`
  - `frmDoorFlStateMsg.DoorFlWindowPos`
- 영향 sysvar
  - `Body::windowCmd`
  - `Body::windowPos`
  - `Core::timeoutClear`

메모:
- 도어 최종 상태 owner라서 `TEST_SCN`이 같은 도어 상태 메시지를 직접 뿌리면 충돌한다.

### 3.6 Wiper / Panel Animation

File: [WIP.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/WIP.can)

- 입력 메시지
  - `frmRainLightAutoMsg.RainSenseLevel`
  - `frmRainLightAutoMsg.AutoLightState`
- 출력 메시지
  - `frmWiperStateMsg`
- 영향 sysvar
  - `Body::wiperCmd`
  - `Body::wiperPos`
  - `Body::frontWiperAnimFrame`
  - `Core::timeoutClear`

메모:
- 와이퍼 상태와 패널 애니메이션 프레임 sysvar가 함께 바뀐다.
- 이번 브랜치에서 panel 표시 경로 변경 영향이 직접 들어간 파일이다.

### 3.7 Warning Arbitration / Cluster Chain

Files:
- [ADAS.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/ADAS/ADAS.can)
- [CLU.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Infotainment/CLU.can)

- `ADAS` 영향 sysvar
  - `Core::selectedAlertLevel`
  - `Core::selectedAlertType`
  - `Core::warningState`
  - `Core::decelAssistReq`
  - `Core::decelAssistDecisionReq`
  - `CoreState::decelGateReason`
- `CLU` 소비 메시지
  - `frmAdasDomainStateMsg.SelectedAlertLevel`
  - `frmAdasDomainStateMsg.SelectedAlertType`
  - `frmAdasDomainStateMsg.TimeoutClear`
  - `frmClusterWarningMsg.WarningTextCode`
- `CLU` 영향 sysvar
  - `Cluster::warningTextCode`
  - `CoreState::duplicatePopupGuard`
  - `CoreState::clusterNotifPrio`
  - `CoreState::alertHistoryCount`

메모:
- `ADAS -> CLU` 체인은 표시 체인의 핵심이다.
- 이번 브랜치의 `EMS.animFrame` 수정도 결국 이 체인의 `selectedAlertLevel/Type`에 의존한다.

### 3.8 Test Input Producer

File: [TEST_SCN.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can)

- 직접 송신하는 주요 메시지
  - `frmSteeringCanMsg`
  - `frmNavContextCanMsg`
  - `frmIgnitionEngineMsg`
  - `frmGearStateMsg`
  - `frmPedalInputCanMsg`
  - `frmDoorFlStateMsg`
  - `frmDoorFrStateMsg`
  - `frmDoorControlMsg`
  - `frmDigitalKeyStateMsg`
  - `frmImmobilizerStateMsg`
  - `frmSeatBeltStateMsg`
  - `frmSuspensionStateMsg`
  - `frmConnectivityStateMsg`
  - `frmIviHealthDetailMsg`
  - `frmSteeringAngleMsg`
  - `frmLampControlMsg`
  - `frmTurnLampInputMsg`
  - `frmFuelBatteryStateMsg`
  - `frmEngineSpeedTempMsg`
  - `frmVehicleModeMsg`

메모:
- 여러 ECU의 최종 입력 owner 메시지를 직접 주입한다.
- 과거 실패 사례 대부분이 이 파일과 실제 ECU owner 파일의 producer 충돌에서 시작되었다.

## 4. High Conflict Risk Files

### 4.1 Very High Risk

- [VCU.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Chassis/VCU.can)
  - `driveMode`, `gearState`, `vehicleSpeed` owner
  - 수동 패널 경로와 테스트 시나리오 경로가 동시에 얽힘
- [EMS.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Powertrain/EMS.can)
  - `animFrame`, `fuelLevel`, `ignition/engine state` 동시 담당
  - 표시 로직과 파워트레인 로직이 섞여 있음
- [TEST_SCN.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can)
  - 다양한 최종 입력 메시지를 직접 생산
  - owner ECU와 충돌 가능성이 가장 높음

### 4.2 High Risk

- [ESC.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Chassis/ESC.can)
  - `brakePressure`, `frmBrakeStatusMsg`, `frmSuspensionStateMsg` owner
- [BCM.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/BCM.can)
  - turn lamp, belt, comfort state, rain/light 출력 owner
- [DOOR_FL.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/DOOR_FL.can)
  - front left door 최종 상태 owner
- [WIP.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Body/WIP.can)
  - 와이퍼 CAN 상태와 패널 애니메이션 sysvar가 같이 걸림

### 4.3 Medium Risk

- [ADAS.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/ADAS/ADAS.can)
  - arbitration owner라 영향 범위는 넓지만 직접적인 panel/manual 충돌은 상대적으로 적음
- [CLU.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Infotainment/CLU.can)
  - 표시 소비자 성격이 강함
- [AMP.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Infotainment/AMP.can)
- [OTA.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Infotainment/OTA.can)
- [TMU.can](/C:/Users/Kimtaekcheon/Documents/workspace/canoe-driving-alert/canoe/cfg/channel_assign/Infotainment/TMU.can)

## 5. Merge Review Summary

- 이번 브랜치에서 가장 많이 흔들린 축은 아래와 같다.
  - `driveMode / gear / vehicleSpeed`
  - `ignition / engine state`
  - `brakePressure`
  - `door / window / wiper state`
  - `selectedAlertLevel / selectedAlertType`
  - `Display::animFrame`
- 다음 병합에서 가장 우선 검토해야 할 파일은 아래와 같다.
  - `EMS.can`
  - `VCU.can`
  - `TEST_SCN.can`
  - `ESC.can`
  - `BCM.can`

## 6. Recommended Merge Focus

1. `TEST_SCN`이 직접 송신하는 메시지와 실제 owner ECU 메시지가 겹치는지 먼저 확인한다.
2. `VCU`, `ESC`, `EMS`에서 panel/manual mode와 scenario mode의 owner가 분리되어 있는지 확인한다.
3. `Core::selectedAlertLevel`, `Core::selectedAlertType`, `Display::animFrame`, `Cluster::warningTextCode` 체인이 끊기지 않았는지 확인한다.
4. `brakePressure`, `door state`, `suspension state`, `steering angle`처럼 과거 충돌 이력이 있는 메시지를 우선 확인한다.
