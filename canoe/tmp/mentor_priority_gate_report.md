# Mentor Priority Gate Report

- Generated: 2026-03-12 22:46:26
- Scope: `canoe/databases` active split set validation
- Backup DBC (`legacy/LEGACY_emergency_system.dbc`) present: NO

## Gate Summary

- Result: PASS
- Active message count: 234

| Check | Result |
|---|---|
| Split CAN DBC files present | PASS |
| Ethernet SoT document present | PASS |
| No duplicate message IDs within an active DBC | PASS |
| No duplicate message names across active DBCs | PASS |
| Mandatory message IDs match contract | PASS |
| Active CAN message volume >= 40 | PASS |
| Mandatory core/baseline message set present | PASS |

## Shared IDs Across DBCs (Allowed In Split Profile)

- These overlaps are informational. In the active split profile, ID reuse across different domain DBCs is allowed.

- 0x12A: chassis_can.dbc:frmEpbStateMsg, powertrain_can.dbc:frmEngineSpeedTempMsg
- 0x12B: chassis_can.dbc:frmVsmStateMsg, powertrain_can.dbc:frmFuelBatteryStateMsg
- 0x12C: chassis_can.dbc:frmEhbStateMsg, powertrain_can.dbc:frmThrottleStateMsg
- 0x12D: chassis_can.dbc:frmEcsStateMsg, powertrain_can.dbc:frmTransmissionTempMsg
- 0x12E: chassis_can.dbc:frmCdcStateMsg, powertrain_can.dbc:frmEngineTorqueMsg
- 0x12F: chassis_can.dbc:frmAirSuspensionStateMsg, powertrain_can.dbc:frmEngineLoadMsg
- 0x130: chassis_can.dbc:frmRwsStateMsg, powertrain_can.dbc:frmTransShiftStateMsg
- 0x1C8: adas_can.dbc:frmLdwsLkasStateMsg, eth_backbone_can_stub.dbc:ethObjectSafetyStateMsg
- 0x280: body_can.dbc:frmRearClimateStateMsg, infotainment_can.dbc:frmClusterWarningMsg
- 0x281: body_can.dbc:frmSunroofStateMsg, infotainment_can.dbc:frmClusterBaseStateMsg
- 0x282: body_can.dbc:frmHeadlampLevelStateMsg, infotainment_can.dbc:frmNaviGuideStateMsg
- 0x283: body_can.dbc:frmCabinSensingStateMsg, infotainment_can.dbc:frmMediaStateMsg
- 0x284: body_can.dbc:frmAhlsStateMsg, infotainment_can.dbc:frmCallStateMsg
- 0x285: body_can.dbc:frmAutoDoorCtrlStateMsg, infotainment_can.dbc:frmNavigationRouteMsg
- 0x286: body_can.dbc:frmPowerTailgateCtrlStateMsg, infotainment_can.dbc:frmClusterThemeMsg
- 0x287: body_can.dbc:frmBiometricAuthStateMsg, infotainment_can.dbc:frmHmiPopupStateMsg
- 0x288: body_can.dbc:frmAcuStateMsg, infotainment_can.dbc:frmInfotainmentHealthMsg
- 0x289: body_can.dbc:frmOdsStateMsg, infotainment_can.dbc:frmAudioFocusMsg
- 0x28A: body_can.dbc:frmMassageSeatCtrlStateMsg, infotainment_can.dbc:frmVoiceAssistStateMsg
- 0x28B: body_can.dbc:frmDatcDiagReqMsg, infotainment_can.dbc:frmMapRenderStateMsg
- 0x28C: body_can.dbc:frmDatcDiagResMsg, infotainment_can.dbc:frmRouteAlertMsg
- 0x299: infotainment_can.dbc:frmOtaMasterStateMsg, eth_backbone_can_stub.dbc:ethIboxStateMsg
- 0x29A: infotainment_can.dbc:frmDigitalKeyStateMsg, eth_backbone_can_stub.dbc:ethSecurityStateMsg
- 0x29B: infotainment_can.dbc:frmRseStateMsg, eth_backbone_can_stub.dbc:ethDiagStateMsg
- 0x29C: infotainment_can.dbc:frmNavModuleStateMsg, eth_backbone_can_stub.dbc:ethEdrStateMsg
- 0x29D: infotainment_can.dbc:frmPgsStateMsg, eth_backbone_can_stub.dbc:ethBackboneStateMsg
- 0x29E: infotainment_can.dbc:frmPhoneAsKeyStateMsg, eth_backbone_can_stub.dbc:ethV2xDiagReqMsg
- 0x29F: infotainment_can.dbc:frmCarpayCtrlStateMsg, eth_backbone_can_stub.dbc:ethV2xDiagResMsg
- 0x2A0: chassis_can.dbc:frmVehicleStateCanMsg, infotainment_can.dbc:frmTmuDiagReqMsg, eth_backbone_can_stub.dbc:ethCgwDiagReqMsg
- 0x2A1: chassis_can.dbc:frmSteeringCanMsg, infotainment_can.dbc:frmTmuDiagResMsg, eth_backbone_can_stub.dbc:ethCgwDiagResMsg
- 0x2A2: chassis_can.dbc:frmPedalInputCanMsg, eth_backbone_can_stub.dbc:ethSgwDiagReqMsg
- 0x2A3: infotainment_can.dbc:frmNavContextCanMsg, eth_backbone_can_stub.dbc:ethSgwDiagResMsg
- 0x2A7: infotainment_can.dbc:frmIviDiagReqMsg, eth_backbone_can_stub.dbc:ethDcmDiagReqMsg
- 0x2A8: powertrain_can.dbc:frmIgnitionEngineMsg, infotainment_can.dbc:frmCluDiagReqMsg, eth_backbone_can_stub.dbc:ethDcmDiagResMsg
- 0x2A9: powertrain_can.dbc:frmGearStateMsg, infotainment_can.dbc:frmCluDiagResMsg
- 0x2AA: powertrain_can.dbc:frmPtDiagReqMsg, infotainment_can.dbc:frmHudDiagReqMsg
- 0x2AB: powertrain_can.dbc:frmSccDiagReqMsg, infotainment_can.dbc:frmHudDiagResMsg
- 0x2AC: powertrain_can.dbc:frmSccDiagResMsg, infotainment_can.dbc:frmAmpDiagReqMsg
