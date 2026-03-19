# TMP Panel Binding Gap Matrix (임시)

## 0. Purpose

This file is the follow-up working table for:

- `TMP_PANEL_BRANCH_MERGE_임시_2026-03-19.md`

Goal:

- lock the exact first-wave donor panels
- list the exact asset import set
- classify each binding as:
  - already satisfied by `develop`
  - missing on `develop`
  - donor-only temporary logic
  - direct CAN binding that should be kept or rewritten
- identify the real `develop` files to touch later

Rule:

- `develop` remains the logic and system-design baseline
- donor branches are not allowed to replace `develop` owner logic
- if a donor panel needs extra behavior, implement that behavior on top of `develop`

## 1. Selected First-Wave Panels

| Priority | Source | Panel | Adoption mode |
|---|---|---|---|
| P1 | `sh_rael_merge` | `Navigation.xvp` | keep with rebinding |
| P1 | `sh_rael_merge` | `cluster.xvp` | keep with rebinding |
| P1 | `sh_rael_merge` | `input.xvp` | keep with rebinding |
| P1 | `sh_rael_merge` | `SDV_Ambient_Control.xvp` | keep |
| P1 | `sh_rael_merge` | `SDV_Ambient_Top_View.xvp` | keep with rebinding |
| P1 | `merge/lee` | `scenariocontrol.xvp` | keep with one blocked binding |
| P1 | `merge/lee` | `v2xpanel.xvp` | keep with one new V2X render var |
| P2 | `merge/lee` | `sample_Dashboard.xvp` | partial donor |
| P2 | `merge/lee` | `windowstate.xvp` | partial donor |

## 2. Gap Legend

| Status | Meaning |
|---|---|
| `OK` | already present on `develop` |
| `ADD` | missing on `develop`; can be added if panel survives review |
| `REBIND` | do not add blindly; rebind panel to an existing `develop` contract |
| `RAW-CAN` | direct bus/message binding exists in panel |
| `ORPHAN` | panel binding exists but donor branch also does not define/produce it |
| `BLOCKED` | adoption requires a namespace/owner decision first |

## 3. Panel Detail Matrix

### 3.1 `sh_rael_merge/Navigation.xvp`

| Item | Detail |
|---|---|
| Assets already in `develop` | none |
| Assets to import | `Bitmaps/IC.wav`, `Bitmaps/speed.mp3`, `Bitmaps/beep.wav`, `Bitmaps/lane.png`, `Bitmaps/zone.png`, `Bitmaps/roadFlowDirection.png`, `Bitmaps/gps.png`, `Bitmaps/bg.png`, `Bitmaps/vol.png` |
| Existing bindings on `develop` | `Test::alertVolumeSetting`, `UiRender::roadZoneColorCode`, `UiRender::roadFlowDirection`, `Core::vehicleSpeedNorm`, `Core::speedLimitNorm` |
| Remaining unresolved bindings | `UiRender::renderVolumLevel`, `UiRender::navLaneFrame` |
| Newly staged compat bindings | `UiRender::beepIC`, `UiRender::beepSpeed`, `UiRender::warningBeepState`, `UiRender::beepEmergency`, `CoreState::volumeLevel` rebinding complete |
| Recommended action | keep the staged beep vars read-only; if `renderVolumLevel` or `navLaneFrame` still block GUI import, disable those widgets before expanding logic |
| `develop` files to touch if kept | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/output/IVI.can`, `canoe/cfg/channel_assign/Infotainment/IVI.can`, optional `canoe/src/capl/ecu/AMP.can`, optional `canoe/cfg/channel_assign/Infotainment/AMP.can` |
| DBC impact | none by default |

### 3.2 `sh_rael_merge/cluster.xvp`

| Item | Detail |
|---|---|
| Assets already in `develop` | `Bitmaps/StageDashboard.png` |
| Assets to import | `Bitmaps/alertType.png`, `Bitmaps/emergencyType.png`, `Bitmaps/roadZone.png`, `Bitmaps/zone.png` |
| Existing bindings on `develop` | `Core::selectedAlertType`, `Cluster::warningTextCode`, `UiRender::roadZoneColorCode`, `UiRender::renderColor`, `Chassis::vehicleSpeed` |
| Direct CAN bindings | `adas_can/ADAS/ethEmergencyRiskMsg.EmergencyType`, `chassis_can/VCU/frmVehicleStateCanMsg.gVehicleSpeed` |
| DBC availability on `develop` | `adas_can.dbc` has `ethEmergencyRiskMsg`; `chassis_can.dbc` has `frmVehicleStateCanMsg` with owner `VCU` |
| Recommended action | keep panel, but rebind the two `RAW-CAN` widgets to existing sysvar contracts where possible; do not add any new logic for this panel first |
| `develop` files to touch if kept | GUI rebind only preferred; no mandatory CAPL/sysvar change if CAN bindings are removed |
| DBC impact | none |

### 3.3 `sh_rael_merge/input.xvp`

| Item | Detail |
|---|---|
| Assets | none |
| Existing bindings on `develop` | `Chassis::driveState`, `Core::vehicleSpeedNorm`, `Core::speedLimitNorm`, `Core::baseZoneContext`, `Core::selectedAlertType`, `Core::selectedAlertLevel`, `Chassis::vehicleSpeed`, `V2X::emergencyType`, `V2X::emergencyDirection`, `V2X::alertState`, `V2X::eta`, `Infotainment::speedLimit`, `Infotainment::zoneDistance`, `Infotainment::navDirection`, `Infotainment::roadZone` |
| Compat-only binding | `Test::manualAlertOverride` |
| Current stance | added as dormant compat var for donor import, but panel widget is read-only and not part of official control flow |
| Recommended action | keep disabled/read-only unless the team later approves a formal manual override contract |
| `develop` files to touch if override is kept | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/input/TEST_SCN.can`, `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can` |
| DBC impact | none |

### 3.4 `sh_rael_merge/SDV_Ambient_Control.xvp`

| Item | Detail |
|---|---|
| Assets | none |
| Existing bindings on `develop` | `Body::ambientMode` |
| Producer on `develop` | `canoe/src/capl/output/BCM.can`, mirrored in `canoe/cfg/channel_assign/Body/BCM.can` |
| Recommended action | import directly; no contract gap |
| `develop` files to touch if kept | none required for first import |
| DBC impact | none |

### 3.5 `sh_rael_merge/SDV_Ambient_Top_View.xvp`

| Item | Detail |
|---|---|
| Assets already in `develop` | none |
| Assets to import | `Bitmaps/Emergency Siren 7.mp3`, `Bitmaps/CarTop.png`, `Bitmaps/Group (1).png`, `Bitmaps/Group (2)(1).png`, `Bitmaps/Group (2)(2).png`, `Bitmaps/Group (3).png`, `Bitmaps/Group (4).png`, `Bitmaps/Group (5).png` |
| Existing bindings on `develop` | none used directly by this donor panel |
| Compat binding | `Infotainment::emergencySound` |
| Current stance | staged in panel branch as read-only compat surface produced by V2X compat layer |
| Recommended action | keep as compat render/sound hook; do not let this surface become a product audio owner |
| `develop` files to touch if kept | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/ecu/AMP.can`, `canoe/cfg/channel_assign/Infotainment/AMP.can`, optional `canoe/src/capl/output/IVI.can`, optional `canoe/cfg/channel_assign/Infotainment/IVI.can` |
| DBC impact | none by default |

### 3.6 `merge/lee/scenariocontrol.xvp`

| Item | Detail |
|---|---|
| Assets | none |
| Existing bindings on `develop` | `Test::scenarioCommand`, `Test::testScenario`, `Test::scenarioResult` |
| Current producer on `develop` | `canoe/src/capl/input/TEST_SCN.can`, mirrored in `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can` |
| Missing binding | `Display::animFrame` |
| Donor producer path | donor writes `@Display::animFrame` in `merge/lee` `Powertrain/EMS.can` |
| Decision | `BLOCKED` |
| Why blocked | `develop` has no `Display` namespace, and donor EMS-based animation ownership is temporary panel logic |
| Recommended action | keep the panel only after either removing the `animFrame` widget or rebinding it to an approved existing render/debug variable |
| `develop` files to touch if kept with animation | first `project.sysvars` namespace decision, then the approved producer path only; do not copy donor EMS animation logic as-is |
| DBC impact | none |

### 3.7 `merge/lee/v2xpanel.xvp`

| Item | Detail |
|---|---|
| Assets already in `develop` | none |
| Assets to import | `Bitmaps/v2x.png` |
| Compat binding | `V2X::v2xFrame` |
| Current producer path | staged in panel branch `V2X.can` compat layer, not EMS |
| Recommended action | keep producer in V2X only; keep panel widget read-only |
| `develop` files to touch if kept | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/logic/V2X.can`, `canoe/cfg/channel_assign/ETH_Backbone/V2X.can` |
| Optional extra vars | only if slider-driven control is adopted later: `V2X::policePos`, `V2X::ambulancePos` |
| DBC impact | none |

### 3.8 `merge/lee/sample_Dashboard.xvp` (P2 partial donor)

| Item | Detail |
|---|---|
| Assets already in `develop` | `Bitmaps/DashboardCircleBlack.png`, `Bitmaps/DashboardCombi.png` |
| Assets to import | `Bitmaps/ivi.png`, `Bitmaps/DashboardABS.png`, `Bitmaps/DashboardFlasherRight.png`, `Bitmaps/DashboardFlasherLeft.png` |
| Existing bindings on `develop` | `Chassis::vehicleSpeed` |
| Missing bindings | `Display::animFrame`, `Powertrain::coolantTemp`, `Chassis::absActive`, `Body::blinkRight`, `Body::blinkLeft`, `Powertrain::fuelLevel` |
| Direct CAN bindings | `powertrain_can/TEST_SCN/frmGearStateMsg.GearState`, `powertrain_can/EMS/frmEngineSpeedTempMsg.EngineRpm` |
| DBC availability on `develop` | `powertrain_can.dbc` has `frmEngineSpeedTempMsg`; raw `GearState` binding exists without owner change |
| Recommended action | use only as a widget donor until `Powertrain/Chassis/Body` display sysvars are approved on `develop`; do not accept donor all-in-one dashboard logic |
| `develop` files to touch if promoted later | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/ecu/EMS.can`, `canoe/cfg/channel_assign/Powertrain/EMS.can`, `canoe/src/capl/ecu/ESC.can`, `canoe/cfg/channel_assign/Chassis/ESC.can`, `canoe/src/capl/output/BCM.can`, `canoe/cfg/channel_assign/Body/BCM.can` |
| DBC impact | none by default; keep owner model unchanged |

### 3.9 `merge/lee/windowstate.xvp` (P2 partial donor)

| Item | Detail |
|---|---|
| Assets already in `develop` | none |
| Assets to import | `Bitmaps/brakelamp.png`, `Bitmaps/wifer.png`, `Bitmaps/right flash.png`, `Bitmaps/left flash.png`, `Bitmaps/left window.png`, `Bitmaps/KakaoTalk_20260310_003301280_10 (1).bmp`, `Bitmaps/KakaoTalk_20260310_003458323.bmp` |
| Missing bindings | `Chassis::brakeLamp`, `Body::frontWiperAnimFrame`, `Body::blinkRight`, `Body::blinkLeft` |
| Direct CAN binding | `body_can/DOOR_FL/frmDoorFlStateMsg.DoorFlWindowPos` |
| DBC availability on `develop` | `body_can.dbc` has `frmDoorFlStateMsg` with owner `DOOR_FL` |
| Recommended action | use as partial donor after `blink/brake/wiper` display vars are added to `develop`; current direct window position binding can remain read-only |
| `develop` files to touch if promoted later | `canoe/project/sysvars/project.sysvars`, `canoe/src/capl/ecu/WIP.can`, `canoe/cfg/channel_assign/Body/WIP.can`, `canoe/src/capl/output/BCM.can`, `canoe/cfg/channel_assign/Body/BCM.can`, `canoe/src/capl/ecu/ESC.can`, `canoe/cfg/channel_assign/Chassis/ESC.can` |
| DBC impact | none by default |

## 4. Orphan Binding List

These bindings appear in donor panels but are not defined in the donor branch contract either.  
Treat them as UI placeholders, not donor truth.

| Source panel | Orphan binding | Recommended handling |
|---|---|---|
| `Navigation.xvp` | `CoreState::baseVolume` | already rebased to `CoreState::volumeLevel` |
| `Navigation.xvp` | `UiRender::beepIC` | staged compat render var, keep read-only |
| `Navigation.xvp` | `UiRender::beepSpeed` | staged compat render var, keep read-only |
| `Navigation.xvp` | `UiRender::warningBeepState` | staged compat render var, keep read-only |
| `Navigation.xvp` | `UiRender::beepEmergency` | staged compat render var, keep read-only |
| `Navigation.xvp` | `UiRender::renderVolumLevel` | rebind to `CoreState::volumeLevel` or rename to approved render var |
| `Navigation.xvp` | `UiRender::navLaneFrame` | map to an approved nav render state only after owner decision |
| `input.xvp` | `Test::manualAlertOverride` | keep dormant/read-only or formally add later; do not use for official flow |
| `SDV_Ambient_Top_View.xvp` | `Infotainment::emergencySound` | staged compat hook; keep read-only |

## 5. Direct CAN Binding Watchlist

These panel bindings can work without new sysvars because the messages already exist on `develop`, but they increase coupling and should be reviewed before finalizing the panel set.

| Panel | Direct binding | Current `develop` state | Recommendation |
|---|---|---|---|
| `cluster.xvp` | `adas_can/ADAS/ethEmergencyRiskMsg.EmergencyType` | message exists in `adas_can.dbc` | rebind to sysvar if possible |
| `cluster.xvp` | `chassis_can/VCU/frmVehicleStateCanMsg.gVehicleSpeed` | message exists in `chassis_can.dbc` with owner `VCU` | rebind to `Chassis::vehicleSpeed` if possible |
| `sample_Dashboard.xvp` | `powertrain_can/TEST_SCN/frmGearStateMsg.GearState` | message exists | leave only if dashboard stays P2 |
| `sample_Dashboard.xvp` | `powertrain_can/EMS/frmEngineSpeedTempMsg.EngineRpm` | message exists in `powertrain_can.dbc` | acceptable read-only binding |
| `windowstate.xvp` | `body_can/DOOR_FL/frmDoorFlStateMsg.DoorFlWindowPos` | message exists in `body_can.dbc` with owner `DOOR_FL` | acceptable read-only binding |

## 6. Real `develop` Touch Set By Domain

| Domain | Real file set to modify later |
|---|---|
| Sysvar contract | `canoe/project/sysvars/project.sysvars` |
| Scenario/test harness | `canoe/src/capl/input/TEST_SCN.can`, `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can` |
| V2X render support | `canoe/src/capl/logic/V2X.can`, `canoe/cfg/channel_assign/ETH_Backbone/V2X.can` |
| IVI render support | `canoe/src/capl/output/IVI.can`, `canoe/cfg/channel_assign/Infotainment/IVI.can` |
| Audio support | `canoe/src/capl/ecu/AMP.can`, `canoe/cfg/channel_assign/Infotainment/AMP.can` |
| Ambient/body display support | `canoe/src/capl/output/BCM.can`, `canoe/cfg/channel_assign/Body/BCM.can` |
| Chassis display support | `canoe/src/capl/ecu/ESC.can`, `canoe/cfg/channel_assign/Chassis/ESC.can` |
| Wiper/window display support | `canoe/src/capl/ecu/WIP.can`, `canoe/cfg/channel_assign/Body/WIP.can`, `canoe/src/capl/ecu/DOOR_FL.can`, `canoe/cfg/channel_assign/Body/DOOR_FL.can` |
| Powertrain display support | `canoe/src/capl/ecu/EMS.can`, `canoe/cfg/channel_assign/Powertrain/EMS.can` |

## 7. DBC Guardrail Follow-Up

| DBC file | Current conclusion |
|---|---|
| `canoe/databases/chassis_can.dbc` | do not accept donor owner drift from `VCU` to `TEST_SCN` |
| `canoe/databases/body_can.dbc` | keep current shape unless wiper animation truly requires CAN payload expansion |
| `canoe/databases/adas_can.dbc` | no change required for first-wave panel import |
| `canoe/databases/powertrain_can.dbc` | no change required for first-wave panel import |

## 8. Immediate Execution Order After This Doc

1. Import first-wave donor XVPs and only their required assets.
2. In GUI, rebind obvious `ORPHAN` and `RAW-CAN` items before touching logic files.
3. Update `project.sysvars` only for the surviving gaps.
4. Patch `develop` CAPL/channel_assign in the file sets listed above.
5. Review DBC only if a surviving panel still cannot be satisfied by sysvar or existing message contracts.
