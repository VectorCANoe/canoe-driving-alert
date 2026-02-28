# CAN Message Ownership Matrix

- Generated: 2026-03-01 04:24:35
- Scope: Active split CAN DBC set only
- Rule: Each message must have one clear sender in active runtime profile.

| Message | ID (hex) | DLC | Sender | DBC | Signals |
|---|---|---|---|---|---|
| frmVehicleStateCanMsg | 0x100 | 2 | SIL_TEST_CTRL | chassis_can.dbc | 3 |
| frmSteeringCanMsg | 0x101 | 1 | SIL_TEST_CTRL | chassis_can.dbc | 2 |
| frmPedalInputCanMsg | 0x102 | 2 | SIL_TEST_CTRL | chassis_can.dbc | 2 |
| frmSteeringStateCanMsg | 0x103 | 1 | CHASSIS_GW | chassis_can.dbc | 2 |
| frmWheelSpeedMsg | 0x104 | 4 | CHASSIS_GW | chassis_can.dbc | 4 |
| frmYawAccelMsg | 0x105 | 4 | CHASSIS_GW | chassis_can.dbc | 2 |
| frmBrakeStatusMsg | 0x106 | 2 | BRAKE_CTRL | chassis_can.dbc | 5 |
| frmAccelStatusMsg | 0x107 | 2 | ACCEL_CTRL | chassis_can.dbc | 2 |
| frmSteeringTorqueMsg | 0x108 | 2 | STEERING_CTRL | chassis_can.dbc | 2 |
| frmChassisHealthMsg | 0x109 | 2 | CHASSIS_GW | chassis_can.dbc | 3 |
| frmNavContextCanMsg | 0x110 | 3 | SIL_TEST_CTRL | infotainment_can.dbc | 5 |
| frmAmbientControlMsg | 0x210 | 1 | BODY_GW | body_can.dbc | 3 |
| frmHazardControlMsg | 0x211 | 1 | BODY_GW | body_can.dbc | 3 |
| frmWindowControlMsg | 0x212 | 1 | BODY_GW | body_can.dbc | 3 |
| frmDriverStateMsg | 0x213 | 1 | BODY_GW | body_can.dbc | 3 |
| frmDoorStateMsg | 0x214 | 2 | BODY_GW | body_can.dbc | 5 |
| frmLampControlMsg | 0x215 | 1 | BODY_GW | body_can.dbc | 5 |
| frmWiperStateMsg | 0x216 | 1 | BODY_GW | body_can.dbc | 3 |
| frmSeatBeltStateMsg | 0x217 | 1 | DRIVER_STATE_CTRL | body_can.dbc | 5 |
| frmCabinAirStateMsg | 0x218 | 2 | DRIVER_STATE_CTRL | body_can.dbc | 2 |
| frmBodyHealthMsg | 0x219 | 2 | BODY_GW | body_can.dbc | 3 |
| frmClusterWarningMsg | 0x220 | 1 | IVI_GW | infotainment_can.dbc | 1 |
| frmClusterBaseStateMsg | 0x221 | 2 | IVI_GW | infotainment_can.dbc | 3 |
| frmNaviGuideStateMsg | 0x222 | 1 | INFOTAINMENT_GW | infotainment_can.dbc | 2 |
| frmMediaStateMsg | 0x223 | 2 | IVI_GW | infotainment_can.dbc | 5 |
| frmCallStateMsg | 0x224 | 2 | IVI_GW | infotainment_can.dbc | 5 |
| frmNavigationRouteMsg | 0x225 | 3 | INFOTAINMENT_GW | infotainment_can.dbc | 5 |
| frmClusterThemeMsg | 0x226 | 1 | IVI_GW | infotainment_can.dbc | 2 |
| frmHmiPopupStateMsg | 0x227 | 1 | IVI_GW | infotainment_can.dbc | 3 |
| frmInfotainmentHealthMsg | 0x228 | 2 | INFOTAINMENT_GW | infotainment_can.dbc | 3 |
| frmTestResultMsg | 0x230 | 1 | SIL_TEST_CTRL | test_can.dbc | 2 |
| frmBaseTestResultMsg | 0x231 | 8 | VEHICLE_BASE_TEST_CTRL | test_can.dbc | 6 |
| frmEmergencyMonitorMsg | 0x232 | 2 | EMS_ALERT_RX | chassis_can.dbc | 3 |
| frmIgnitionEngineMsg | 0x300 | 1 | SIL_TEST_CTRL | powertrain_can.dbc | 3 |
| frmGearStateMsg | 0x301 | 1 | SIL_TEST_CTRL | powertrain_can.dbc | 3 |
| frmPowertrainGatewayMsg | 0x302 | 2 | DOMAIN_GW_ROUTER | powertrain_can.dbc | 2 |
| frmEngineSpeedTempMsg | 0x303 | 4 | ENGINE_CTRL | powertrain_can.dbc | 3 |
| frmFuelBatteryStateMsg | 0x304 | 3 | ENGINE_CTRL | powertrain_can.dbc | 4 |
| frmThrottleStateMsg | 0x305 | 2 | ENGINE_CTRL | powertrain_can.dbc | 2 |
| frmTransmissionTempMsg | 0x306 | 2 | TRANSMISSION_CTRL | powertrain_can.dbc | 2 |
| frmVehicleModeMsg | 0x307 | 2 | DOMAIN_GW_ROUTER | powertrain_can.dbc | 6 |
| frmPowerLimitMsg | 0x308 | 2 | DOMAIN_GW_ROUTER | powertrain_can.dbc | 2 |
| frmCruiseStateMsg | 0x309 | 2 | DOMAIN_GW_ROUTER | powertrain_can.dbc | 4 |
| frmPowertrainHealthMsg | 0x30A | 2 | DOMAIN_GW_ROUTER | powertrain_can.dbc | 3 |
