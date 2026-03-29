# ECU Flow Appendix

> [!IMPORTANT]
> This appendix is the current reviewer-facing ECU interaction catalog for the active CANoe SIL baseline.
> It is generated from active `channel_assign` inventory, split DBC contracts, runtime ownership matrix, and native test assets.

## Purpose

Use this appendix when the question is:

- which ECU publishes active network-facing contracts
- which contracts each ECU consumes in the executable baseline
- which other ECUs each ECU is directly linked to through those contracts
- whether that ECU already has a direct native verification anchor

This document is appendix-grade and reviewer-facing.
Working notes, temporary hypotheses, or migration memos must stay outside `canoe/docs/**`.

## Source Assets

- inventory: `canoe/cfg/channel_assign/**`
- network contracts: `canoe/databases/*.dbc`
- runtime ownership supplement: `canoe/tmp/runtime_message_ownership_matrix.md`
- native test anchors: `canoe/tests/modules/test_units/**`
- regeneration command: `python canoe/tools/20_VERIFICATION/20_build_ecu_flow_appendix.py`

## Coverage Summary

- active ECU count: `101`
- direct network-contract ECUs: `93`
- semantic-only / non-network appendix rows: `8`
- ECUs with direct native test anchors: `47`
- ECUs without explicit direct native test anchors: `54`

| Domain | ECU count |
| --- | ---: |
| `ADAS` | `26` |
| `Body` | `23` |
| `Chassis` | `15` |
| `ETH_Backbone` | `10` |
| `Infotainment` | `13` |
| `Powertrain` | `14` |

## Reading Rule

- `Published contracts` are the ECU's active outbound message contracts in the current executable baseline.
- `Consumed contracts` are message contracts where the ECU appears as a DBC receiver in the active split databases.
- `Linked ECUs` are direct sender/receiver neighbors derived from the same contracts.
- `Direct native test anchors` are current explicit native assets whose IDs mention the ECU directly.
- `Direct native test anchors` are a direct-anchor index, not the full indirect coverage claim for that ECU.
- A row may still be valid when `Consumed contracts = -` or `Direct native test anchors = -`; that means the ECU is currently documented mainly as a publisher, semantic seam, or indirectly covered participant.

## Explicit Gaps To Close

- semantic-only / non-network appendix rows: `DCM, EDR, ETHB, EXT_DIAG, IBOX, SGW, TEST_BAS, V2X`
- no direct native anchor yet: `AEB, BCW, DMS, FCA, HWP, LCA, LDR, LDWS_LKAS, OMS, PKM, RPC, RRM, RSPA, SPAS, SPM, TRM, ADM, BIO, BSEC, CSM, HLM, MIR, MSC, PTG, RATC, SMK, WIP, ABS, ASM, ESC, MDPS, RWS, SAS, TPMS, VCU, EDR, EXT_DIAG, TEST_BAS, TEST_SCN, CPAY, DKEY, OTA, PAK, RSE, VCS, BAT_BMS, CPC, EOP, EWP, FPCM, ISG, LVR, TCU, _4WD`

## ECU Catalog

| ECU | Domain | Published contracts | Consumed contracts | Linked ECUs | Direct native test anchors |
| --- | --- | --- | --- | --- | --- |
| `ADAS` | `ADAS` | ethDecelAssistReqMsg<br>ethEmergencyRiskMsg<br>ethObjectRiskStateMsg<br>ethObjectScenarioAlertMsg<br>ethSelectedAlertMsg<br>+3 more | ethEmergencyRiskMsg<br>ethObjectRiskInputMsg<br>ethObjectRiskStateMsg<br>frmAbsStateMsg<br>frmAdasDiagReqMsg<br>+38 more | ABS<br>AEB<br>ASM<br>BCM<br>BCW<br>CDC<br>CLU<br>ECS<br>+29 more | TC_CANOE_IT_EXT_039_ADAS_PERCEPTION_CONTEXT<br>TC_CANOE_ST_EXT_042_ADAS_PERCEPTION_CONTEXT<br>TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST<br>+3 more |
| `AEB` | `ADAS` | frmAebDomainStateMsg | frmAdasDomainStateMsg | ADAS<br>CLU<br>ESC | - |
| `AVM` | `ADAS` | frmAvmStateMsg | - | CLU<br>IVI | TC_CANOE_UT_INP_055_AVM_INPUT |
| `BCW` | `ADAS` | frmBcwStateMsg | frmAdasDomainStateMsg | ADAS<br>CLU | - |
| `DMS` | `ADAS` | frmDmsDiagResMsg<br>frmDmsStateMsg | frmDmsDiagReqMsg<br>frmHighwayPilotStateMsg | CLU<br>HWP<br>TEST_SCN | - |
| `FCA` | `ADAS` | frmFcaStateMsg | frmAdasDomainStateMsg | ADAS<br>CLU<br>ESC | - |
| `FCAM` | `ADAS` | frmFcamStateMsg | frmAdasDomainStateMsg<br>frmFcamInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_056_FCAM_INPUT |
| `FRADAR` | `ADAS` | frmFradarStateMsg | frmAdasDomainStateMsg<br>frmFradarInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_057_FRADAR_INPUT |
| `HWP` | `ADAS` | frmHighwayPilotStateMsg | - | ADAS<br>CLU<br>DMS | - |
| `LCA` | `ADAS` | frmLcaStateMsg | frmAdasDomainStateMsg | ADAS<br>CLU | - |
| `LDR` | `ADAS` | frmLidarStateMsg | frmAdasDomainStateMsg<br>frmLidarInputMsg | ADAS<br>CLU<br>TEST_SCN | - |
| `LDWS_LKAS` | `ADAS` | frmLdwsLkasStateMsg | frmAdasDomainStateMsg | ADAS<br>CLU | - |
| `OMS` | `ADAS` | frmOmsDiagResMsg<br>frmOmsStateMsg | frmOmsDiagReqMsg | BCM<br>CLU<br>TEST_SCN | - |
| `PKM` | `ADAS` | frmParkMasterStateMsg | - | ADAS<br>CLU<br>IVI | - |
| `PUS` | `ADAS` | frmParkUltrasonicStateMsg | - | BCM<br>CLU<br>IVI | TC_CANOE_UT_INP_054_PUS_INPUT |
| `RPC` | `ADAS` | frmRoadPreviewCameraStateMsg | - | ADAS<br>CLU | - |
| `RRM` | `ADAS` | frmRearRadarMasterStateMsg | - | ADAS<br>CLU | - |
| `RSPA` | `ADAS` | frmRspaStateMsg | - | ADAS<br>CLU<br>ESC | - |
| `SCC` | `ADAS` | frmCruiseStateMsg<br>frmSccDiagResMsg | frmAdasDomainStateMsg<br>frmSccDiagReqMsg | ADAS<br>EMS<br>TCU<br>TEST_SCN | TC_CANOE_UT_INP_052_SCC_INPUT |
| `SPAS` | `ADAS` | frmSpasStateMsg | - | ADAS<br>CLU<br>MDPS | - |
| `SPM` | `ADAS` | frmSurroundParkMasterStateMsg | - | ADAS<br>CLU<br>IVI | - |
| `SRR_FL` | `ADAS` | frmSrrFlStateMsg | frmAdasDomainStateMsg<br>frmSrrFlInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_058_SRR_FL_INPUT |
| `SRR_FR` | `ADAS` | frmSrrFrStateMsg | frmAdasDomainStateMsg<br>frmSrrFrInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_059_SRR_FR_INPUT |
| `SRR_RL` | `ADAS` | frmSrrRlStateMsg | frmAdasDomainStateMsg<br>frmSrrRlInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_060_SRR_RL_INPUT |
| `SRR_RR` | `ADAS` | frmSrrRrStateMsg | frmAdasDomainStateMsg<br>frmSrrRrInputMsg | ADAS<br>CLU<br>TEST_SCN | TC_CANOE_UT_INP_061_SRR_RR_INPUT |
| `TRM` | `ADAS` | frmTrailerCtrlStateMsg | - | ADAS<br>CLU<br>VCU | - |
| `ADM` | `Body` | frmAutoDoorCtrlStateMsg | frmAutoDoorCtrlStateMsg | - | - |
| `AFLS` | `Body` | frmAflsDiagResMsg<br>frmAflsStateMsg | frmAflsDiagReqMsg<br>frmAflsStateMsg | TEST_SCN | TC_CANOE_UT_INP_043_AFLS_INPUT |
| `AHLS` | `Body` | frmAhlsStateMsg | frmAhlsStateMsg | - | TC_CANOE_UT_INP_044_AHLS_INPUT |
| `BCM` | `Body` | frmAmbientControlMsg<br>frmBcmDiagResMsg<br>frmBodyComfortStateMsg<br>frmBodyGatewayStateMsg<br>frmBodyHealthMsg<br>+12 more | ethObjectScenarioAlertMsg<br>ethSelectedAlertMsg<br>frmAcuStateMsg<br>frmAdasDomainStateMsg<br>frmAmbientControlMsg<br>+20 more | ACU<br>ADAS<br>CGW<br>DATC<br>MIR<br>MSC<br>ODS<br>OMS<br>+3 more | TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY<br>TC_CANOE_UT_OUT_070_BCM_AMBIENT |
| `BIO` | `Body` | frmBiometricAuthStateMsg | frmBiometricAuthStateMsg | - | - |
| `BSEC` | `Body` | frmAlarmStateMsg | frmAlarmStateMsg | - | - |
| `CSM` | `Body` | frmCabinSensingStateMsg | frmCabinSensingStateMsg | - | - |
| `DATC` | `Body` | frmDatcDiagResMsg<br>frmHvacActuatorMsg<br>frmHvacStateMsg | frmDatcDiagReqMsg<br>frmTmuServiceStateMsg | BCM<br>TEST_SCN<br>TMU | TC_CANOE_UT_INP_045_DATC_INPUT |
| `DOOR_FL` | `Body` | frmDoorFlStateMsg | frmDoorFlStateMsg | - | TC_CANOE_UT_INP_036_DOOR_FL_INPUT |
| `DOOR_FR` | `Body` | frmDoorFrStateMsg | frmDoorFrStateMsg | - | TC_CANOE_UT_INP_037_DOOR_FR_INPUT |
| `DOOR_RL` | `Body` | frmDoorRlStateMsg | frmDoorRlStateMsg | - | TC_CANOE_UT_INP_038_DOOR_RL_INPUT |
| `DOOR_RR` | `Body` | frmDoorRrStateMsg | frmDoorRrStateMsg | - | TC_CANOE_UT_INP_039_DOOR_RR_INPUT |
| `HLM` | `Body` | frmHeadlampLevelStateMsg | frmHeadlampLevelStateMsg | - | - |
| `MIR` | `Body` | frmMirrorStateMsg | - | BCM | - |
| `MSC` | `Body` | frmMassageSeatCtrlStateMsg | - | BCM<br>CLU<br>SEAT_DRV | - |
| `PTG` | `Body` | frmPowerTailgateCtrlStateMsg | frmPowerTailgateCtrlStateMsg | - | - |
| `RATC` | `Body` | frmRearClimateStateMsg | frmRearClimateStateMsg | - | - |
| `SEAT_DRV` | `Body` | frmSeatDrvStateMsg | frmMassageSeatCtrlStateMsg<br>frmSeatDrvStateMsg | MSC | TC_CANOE_UT_INP_046_SEAT_DRV_INPUT |
| `SEAT_PASS` | `Body` | frmSeatPassStateMsg | frmSeatPassStateMsg | - | TC_CANOE_UT_INP_047_SEAT_PASS_INPUT |
| `SMK` | `Body` | frmImmobilizerStateMsg<br>frmSmkDiagResMsg | frmImmobilizerStateMsg<br>frmSmkDiagReqMsg | TEST_SCN | - |
| `SRF` | `Body` | frmSunroofStateMsg | frmSunroofControlMsg<br>frmSunroofStateMsg | BCM | TC_CANOE_UT_INP_048_SRF_INPUT |
| `TGM` | `Body` | frmTailgateStateMsg | frmTailgateStateMsg | - | TC_CANOE_UT_INP_040_TGM_INPUT |
| `WIP` | `Body` | frmWipDiagResMsg<br>frmWiperStateMsg | frmWipDiagReqMsg<br>frmWiperStateMsg | TEST_SCN | - |
| `ABS` | `Chassis` | frmAbsDiagResMsg<br>frmAbsStateMsg | frmAbsDiagReqMsg | ADAS<br>ESC<br>TEST_SCN | - |
| `ACU` | `Chassis` | frmAcuDiagResMsg<br>frmAcuStateMsg | frmAcuDiagReqMsg | BCM<br>CGW<br>TEST_SCN | TC_CANOE_UT_INP_041_ACU_INPUT |
| `ASM` | `Chassis` | frmAirSuspensionStateMsg | - | ADAS<br>ESC | - |
| `CDC` | `Chassis` | frmCdcDiagResMsg<br>frmCdcStateMsg | frmCdcDiagReqMsg | ADAS<br>TEST_SCN | TC_CANOE_UT_INP_035_CDC_INPUT |
| `ECS` | `Chassis` | frmEcsDiagResMsg<br>frmEcsStateMsg | frmEcsDiagReqMsg | ADAS<br>TEST_SCN | TC_CANOE_UT_INP_034_ECS_INPUT |
| `EHB` | `Chassis` | frmEhbDiagResMsg<br>frmEhbStateMsg | frmEhbDiagReqMsg | ADAS<br>TEST_SCN | TC_CANOE_UT_INP_032_EHB_INPUT |
| `EPB` | `Chassis` | frmEpbDiagResMsg<br>frmEpbStateMsg | frmEpbDiagReqMsg | CLU<br>TEST_SCN | TC_CANOE_UT_INP_031_EPB_INPUT |
| `ESC` | `Chassis` | frmBrakeStatusMsg<br>frmBrakeTempMsg<br>frmBrakeWearMsg<br>frmChassisDiagResMsg<br>frmChassisHealthMsg<br>+5 more | ethDecelAssistReqMsg<br>frmAbsStateMsg<br>frmAccelStatusMsg<br>frmAdasChassisStatusMsg<br>frmAebDomainStateMsg<br>+18 more | ABS<br>ADAS<br>AEB<br>ASM<br>CGW<br>FCA<br>MDPS<br>RSPA<br>+4 more | - |
| `MDPS` | `Chassis` | frmEpsStateMsg<br>frmSteeringStateCanMsg<br>frmSteeringTorqueMsg | frmSpasStateMsg<br>frmSteeringCanMsg<br>frmSteeringStateCanMsg<br>frmWheelSpeedMsg<br>frmYawAccelMsg | ADAS<br>ESC<br>SPAS<br>TEST_SCN | - |
| `ODS` | `Chassis` | frmOdsDiagResMsg<br>frmOdsStateMsg | frmOdsDiagReqMsg | BCM<br>CGW<br>TEST_SCN | TC_CANOE_UT_INP_042_ODS_INPUT |
| `RWS` | `Chassis` | frmRwsStateMsg | - | ADAS<br>ESC | - |
| `SAS` | `Chassis` | frmSasDiagResMsg<br>frmSteeringAngleMsg | frmSasDiagReqMsg | ADAS<br>ESC<br>TEST_SCN | - |
| `TPMS` | `Chassis` | frmTirePressureMsg<br>frmTpmsDiagResMsg | frmTpmsDiagReqMsg | ADAS<br>TEST_SCN | - |
| `VCU` | `Chassis` | frmAccelStatusMsg<br>frmEnergyFlowStateMsg<br>frmPowerLimitMsg<br>frmPowertrainCtrlAuthMsg<br>frmPowertrainGatewayMsg<br>+6 more | frm4wdStateMsg<br>frmBatBmsStateMsg<br>frmChargePortCtrlStateMsg<br>frmDcdcStateMsg<br>frmEngineLoadMsg<br>+19 more | ADAS<br>BAT_BMS<br>CPC<br>DCDC<br>EMS<br>EOP<br>ESC<br>EWP<br>+10 more | - |
| `VSM` | `Chassis` | frmVsmDiagResMsg<br>frmVsmStateMsg | frmVsmDiagReqMsg | ADAS<br>TEST_SCN | TC_CANOE_UT_INP_033_VSM_INPUT |
| `CGW` | `ETH_Backbone` | - | frmAcuStateMsg<br>frmBodyHealthMsg<br>frmChassisHealthMsg<br>frmInfotainmentHealthMsg<br>frmOdsStateMsg | ACU<br>BCM<br>ESC<br>IVI<br>ODS | TC_CANOE_UT_CORE_001_CGW_CHS_GW<br>TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW<br>TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS |
| `DCM` | `ETH_Backbone` | - | - | - | TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE |
| `EDR` | `ETH_Backbone` | - | - | - | - |
| `ETHB` | `ETH_Backbone` | - | - | - | TC_CANOE_UT_INP_065_ETHB_INPUT |
| `EXT_DIAG` | `ETH_Backbone` | - | - | - | - |
| `IBOX` | `ETH_Backbone` | - | - | - | TC_CANOE_UT_INP_062_IBOX_INPUT |
| `SGW` | `ETH_Backbone` | - | - | - | TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE |
| `TEST_BAS` | `ETH_Backbone` | - | - | - | - |
| `TEST_SCN` | `ETH_Backbone` | ethObjectRiskInputMsg<br>frmAbsDiagReqMsg<br>frmAcuDiagReqMsg<br>frmAdasDiagReqMsg<br>frmAflsDiagReqMsg<br>+35 more | ethDecelAssistReqMsg<br>ethEmergencyRiskMsg<br>ethObjectRiskStateMsg<br>ethObjectScenarioAlertMsg<br>ethSelectedAlertMsg<br>+37 more | ABS<br>ACU<br>ADAS<br>AFLS<br>AMP<br>BCM<br>CDC<br>CLU<br>+31 more | - |
| `V2X` | `ETH_Backbone` | - | - | - | TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN |
| `AMP` | `Infotainment` | frmAmpDiagResMsg<br>frmAmpStateMsg | frmAmpDiagReqMsg | CLU<br>IVI<br>TEST_SCN<br>VCS | TC_CANOE_UT_INP_050_AMP_INPUT<br>TC_CANOE_UT_OUT_074_AMP_AUDIO |
| `CLU` | `Infotainment` | frmCluDiagResMsg | frmAdasDomainStateMsg<br>frmAebDomainStateMsg<br>frmAmpStateMsg<br>frmAudioFocusMsg<br>frmAvmStateMsg<br>+44 more | ADAS<br>AEB<br>AMP<br>AVM<br>BCW<br>DKEY<br>DMS<br>EPB<br>+30 more | TC_CANOE_UT_EXT_007_CLU_CONTEXT_ADJUST<br>TC_CANOE_UT_OUT_072_CLU_DISPLAY |
| `CPAY` | `Infotainment` | frmCarpayCtrlStateMsg | - | IVI<br>TMU | - |
| `DKEY` | `Infotainment` | frmDigitalKeyStateMsg | frmPhoneAsKeyStateMsg | CLU<br>IVI<br>PAK<br>TEST_SCN | - |
| `HUD` | `Infotainment` | frmHudDiagResMsg<br>frmHudStateMsg | frmHudDiagReqMsg | CLU<br>IVI<br>TEST_SCN | TC_CANOE_UT_INP_049_HUD_INPUT<br>TC_CANOE_UT_OUT_073_HUD_DISPLAY |
| `IVI` | `Infotainment` | frmAudioFocusMsg<br>frmCallStateMsg<br>frmClusterBaseStateMsg<br>frmClusterNotifMsg<br>frmClusterSyncStateMsg<br>+10 more | ethObjectScenarioAlertMsg<br>ethSelectedAlertMsg<br>frmAdasDomainStateMsg<br>frmAmpStateMsg<br>frmAvmStateMsg<br>+19 more | ADAS<br>AMP<br>AVM<br>CGW<br>CLU<br>CPAY<br>DKEY<br>HUD<br>+9 more | TC_CANOE_UT_CORE_013_IVI_GW_ROUTE<br>TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING<br>TC_CANOE_UT_EXT_021_IVI_DISPLAY_SERVICE<br>+2 more |
| `NAV` | `Infotainment` | frmMapRenderStateMsg<br>frmNavModuleStateMsg<br>frmNaviGuideStateMsg<br>frmNavigationRouteMsg<br>frmRouteAlertMsg<br>+1 more | - | CLU<br>IVI<br>TEST_SCN | TC_CANOE_UT_CORE_009_NAV_CTX_MGR<br>TC_CANOE_UT_INP_029_NAV_CONTEXT |
| `OTA` | `Infotainment` | frmOtaMasterStateMsg | - | CLU<br>IVI<br>TEST_SCN<br>TMU | - |
| `PAK` | `Infotainment` | frmPhoneAsKeyStateMsg | - | DKEY<br>TMU | - |
| `PGS` | `Infotainment` | frmPgsStateMsg | - | CLU<br>IVI | TC_CANOE_UT_INP_053_PGS_INPUT |
| `RSE` | `Infotainment` | frmRseStateMsg | - | CLU<br>IVI | - |
| `TMU` | `Infotainment` | frmTmuDiagResMsg<br>frmTmuServiceStateMsg | frmCarpayCtrlStateMsg<br>frmOtaMasterStateMsg<br>frmPhoneAsKeyStateMsg<br>frmTmuDiagReqMsg | CLU<br>CPAY<br>DATC<br>IVI<br>OTA<br>PAK<br>TEST_SCN | TC_CANOE_UT_INP_051_TMU_INPUT |
| `VCS` | `Infotainment` | frmSpeechTtsStateMsg<br>frmVoiceAssistStateMsg | frmAmpStateMsg | AMP<br>CLU | - |
| `BAT_BMS` | `Powertrain` | frmBatBmsStateMsg | frmChargePortCtrlStateMsg | CPC<br>DCDC<br>OBC<br>VCU | - |
| `CPC` | `Powertrain` | frmChargePortCtrlStateMsg | - | BAT_BMS<br>OBC<br>VCU | - |
| `DCDC` | `Powertrain` | frmDcdcStateMsg | frmBatBmsStateMsg | BAT_BMS<br>VCU | TC_CANOE_UT_INP_067_DCDC_INPUT |
| `EMS` | `Powertrain` | frmEngineLoadMsg<br>frmEngineSpeedTempMsg<br>frmEngineTorqueMsg<br>frmFuelBatteryStateMsg<br>frmThermalMgmtStateMsg<br>+1 more | frmCruiseStateMsg<br>frmEnergyFlowStateMsg<br>frmEopStateMsg<br>frmEwpStateMsg<br>frmFpcmStateMsg<br>+9 more | EOP<br>EWP<br>FPCM<br>INVERTER<br>ISG<br>MCU<br>SCC<br>TCU<br>+2 more | TC_CANOE_UT_CORE_010_EMS_ALERT_TXRX |
| `EOP` | `Powertrain` | frmEopStateMsg | - | EMS<br>VCU | - |
| `EWP` | `Powertrain` | frmEwpStateMsg | - | EMS<br>VCU | - |
| `FPCM` | `Powertrain` | frmFpcmStateMsg | - | EMS<br>VCU | - |
| `INVERTER` | `Powertrain` | frmInverterStateMsg | - | EMS<br>VCU | TC_CANOE_UT_INP_069_INVERTER_INPUT |
| `ISG` | `Powertrain` | frmIsgStateMsg | - | EMS<br>VCU | - |
| `LVR` | `Powertrain` | frmLvrStateMsg | - | TCU<br>VCU | - |
| `MCU` | `Powertrain` | frmMcuStateMsg | - | EMS<br>VCU | TC_CANOE_UT_INP_068_MCU_INPUT |
| `OBC` | `Powertrain` | frmObcStateMsg | frmBatBmsStateMsg<br>frmChargePortCtrlStateMsg | BAT_BMS<br>CPC<br>VCU | TC_CANOE_UT_INP_066_OBC_INPUT |
| `TCU` | `Powertrain` | frmTransShiftStateMsg<br>frmTransmissionTempMsg | frmCruiseStateMsg<br>frmEnergyFlowStateMsg<br>frmEngineSpeedTempMsg<br>frmGearStateMsg<br>frmLvrStateMsg<br>+5 more | EMS<br>LVR<br>SCC<br>TEST_SCN<br>VCU | - |
| `_4WD` | `Powertrain` | frm4wdStateMsg | - | VCU | - |

## Usage Boundary

- Use `contracts/communication-matrix.md` and `contracts/owner-route.md` for authoritative ownership and routing decisions.
- Use `verification/test-asset-mapping.md`, `verification/execution-guide.md`, and `verification/oracle.md` for executable test interpretation.
- Use this appendix as the ECU-by-ECU reviewer summary that bridges those assets.
