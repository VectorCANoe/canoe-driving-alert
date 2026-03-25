# TMP Panel Branch Merge Matrix (임시)

## 0. Status

- Date: 2026-03-19
- Phase: planning only
- Baseline branch: `develop`
- Donor branches:
  - `origin/sh_rael_merge`
  - `origin/merge/lee`
- This file is temporary and should be deleted after the actual panel merge is stabilized and reflected into stable panel docs.

## 1. Non-Negotiable Merge Rules

| Rule | Decision |
|---|---|
| Logic/system baseline | `develop` is the only source of truth. |
| Current develop panel XVPs | Treat as disposable drafts. Retire all current `develop` panel UI after donor panels are linked and smoke-verified. |
| Donor branch scope | Donor branches are panel/UI donors first. Their CAPL/sysvar/DBC changes are reference only. |
| CAPL merge mode | Never wholesale-merge `canoe/src/capl/**` from donor branches. Mine required behavior only, then rewrite on top of `develop`. |
| Sysvar merge mode | Never replace `canoe/project/sysvars/project.sysvars` wholesale. Add only missing variables required by selected donor panels. |
| Scenario control path | Official launch/stop stays on `Test::scenarioCommand`; `Test::testScenario` is status mirror/read-only only. |
| Channel assign merge mode | Never accept donor `channel_assign/*.can` wholesale. Re-apply only the minimum missing owner/input/output hooks on top of `develop`. |
| DBC merge mode | Never accept donor owner changes that weaken the `develop` owner model. |
| CANoe cfg | `.cfg`, `.cfg.ini`, `.stcfg` registration/save remains GUI-only. |

## 2. Current Develop Panel Retirement Set

The files below are current `develop` draft UI and are planned for retirement.  
Delete only after donor panels are imported in GUI, linked, and compiled.

| Current develop file | Action | Delete gate |
|---|---|---|
| `canoe/project/panel/SDV_Ambient_View.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Cabin_Panorama_View.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Cluster_View.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Control.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Demo_Stage.xvp` | retire develop draft | no longer referenced in GUI |
| `canoe/project/panel/SDV_External_Road_View.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Monitor.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Navigation_View.xvp` | retire develop draft | donor replacement linked in GUI |
| `canoe/project/panel/SDV_Render_Debug.xvp` | retire develop draft | debug needs re-covered elsewhere |
| `canoe/project/panel/SDV_Test_Operator.xvp` | retire develop draft | donor replacement linked in GUI |

## 3. Donor Panel Keep/Drop/Migrate Matrix

### 3.1 Primary keep candidates

| Source | Donor panel | Role | Decision | Develop guardrail | Required follow-up |
|---|---|---|---|---|---|
| `sh_rael_merge` | `canoe/project/panel/Navigation.xvp` | navigation alert + audio UI | keep whole | keep `develop` logic; do not port donor alert logic blindly | add missing render/audio sysvars or rebind to existing `UiRender::*` contract |
| `sh_rael_merge` | `canoe/project/panel/cluster.xvp` | cluster warning UI | keep whole with rebinding review | remove dependency on donor-temp direct CAN assumptions where possible | prefer `Cluster/Core/UiRender` binding over raw CAN binding |
| `sh_rael_merge` | `canoe/project/panel/input.xvp` | operator/control panel | keep whole with manual-control review | `develop` scenario/input owner chain must remain | add only missing control vars; do not let panel branch redefine owner flow |
| `sh_rael_merge` | `canoe/project/panel/SDV_Ambient_Control.xvp` | ambient control/detail | keep whole | ambient output meaning stays on `develop` side | confirm `Body::ambientMode` contract only |
| `sh_rael_merge` | `canoe/project/panel/SDV_Ambient_Top_View.xvp` | ambient/emergency top view | keep whole with rebinding review | no donor-specific sound logic takeover | add or remap `emergencySound` path |
| `merge/lee` | `canoe/project/panel/scenariocontrol.xvp` | scenario launcher | keep whole | scenario execution stays on `develop` test flow | reconcile `Display::animFrame` with current namespace policy |
| `merge/lee` | `canoe/project/panel/v2xpanel.xvp` | V2X frame view | keep whole | V2X decision logic stays on `develop` | add `V2X::v2xFrame` or adapt to existing render path |

### 3.2 Partial donor candidates

| Source | Donor panel | Role | Decision | Why partial only |
|---|---|---|---|---|
| `merge/lee` | `canoe/project/panel/sample_Dashboard.xvp` | dashboard cluster/body indicators | partial donor | mixes useful widgets with raw CAN bindings and new namespaces not present on `develop` |
| `merge/lee` | `canoe/project/panel/windowstate.xvp` | body/window/wiper display | partial donor | useful display surface, but contains direct `DOOR_FL` CAN binding and several missing sysvars |
| `merge/lee` | `canoe/project/panel/MyDriverPanel.xvp` | large all-in-one driver panel | widget donor only | too broad, mixes manual control, raw CAN, and donor-temp design assumptions |

### 3.3 Do not import as a branch-level concept

| Source | Item | Decision | Reason |
|---|---|---|---|
| `merge/lee` | donor practice of replacing SDV split with a single broad driver panel stack | reject | current merge target is `develop` architecture, not donor temporary UI architecture |
| `sh_rael_merge` / `merge/lee` | donor CAPL/channel assign as-is | reject | too much temporary logic for panel bring-up |

## 4. Panel Asset Matrix

| Source | Asset group | Decision | Note |
|---|---|---|---|
| `sh_rael_merge` | `CarTop.png`, `Group*.png`, `alertType.png`, `direction.png`, `emergency*.png`, `gps.png`, `lane.png`, `road*.png`, `zone.png`, `IC.wav`, `beep.wav`, `speed.mp3`, `Emergency Siren 7.mp3`, `vol.png`, `bg.png` | import with kept `sh` panels | treat as the visual/audio pack for nav/cluster/input/ambient |
| `merge/lee` | dashboard/body/v2x/window bitmap pack including `v2x.png`, `combined_warning_icons.png`, `window_frame_*`, `blink*.bmp`, `VCar*.bmp`, `Dashboard*.png`, `Control*.png` | selective import only | copy only for actually adopted `lee` panels |
| `merge/lee` | screenshot-like `KakaoTalk_*` references | optional | keep only if directly referenced by an adopted panel |

## 5. Sysvar Contract Matrix

`develop` currently has namespaces:
- `Chassis`
- `Infotainment`
- `V2X`
- `Core`
- `Body`
- `Cluster`
- `Test`
- `Diag`
- `CoreState`
- `UiRender`

### 5.1 Missing vars required by selected `sh_rael_merge` panels

| Var | Status vs develop | Recommended action |
|---|---|---|
| `UiRender::beepIC` | missing | add only if the chosen audio path needs a dedicated trigger |
| `UiRender::beepSpeed` | missing | add only if speed alert sound is preserved |
| `UiRender::warningBeepState` | missing | add or remap to an existing warning/audio state |
| `UiRender::renderVolumLevel` | missing | rename/rebind carefully; fix spelling before adoption if needed |
| `Test::manualAlertOverride` | missing | add only if operator panel really needs manual override |
| `Infotainment::emergencySound` | missing | prefer an existing render/audio abstraction if one already covers this |

### 5.2 Missing vars required by selected `merge/lee` panels

| Var | Status vs develop | Recommended action |
|---|---|---|
| `V2X::v2xFrame` | missing | strong candidate to add if `v2xpanel.xvp` is kept |
| `Powertrain::coolantTemp` | missing | add only if dashboard panel is adopted |
| `Powertrain::fuelLevel` | missing | add only if dashboard panel is adopted |
| `Chassis::absActive` | missing | add only if dashboard/body indicator panel is adopted |
| `Body::blinkLeft` | missing | add only if body indicator panel is adopted |
| `Body::blinkRight` | missing | add only if body indicator panel is adopted |
| `Body::frontWiperAnimFrame` | missing | prefer sysvar-level animation output over DBC owner changes |
| `Chassis::brakeLamp` | missing | add only if body indicator panel is adopted |
| `Display::animFrame` | missing namespace | do not add blindly; first decide whether this should live under `UiRender`, `CoreState`, or a new approved namespace |
| `Body::doorLockCmd` | missing | add only if door control UI is really kept |
| `Body::doorOpenCmd` | missing | add only if door control UI is really kept |
| `Body::wiperCmd` | missing | add only if manual body control is really kept |
| `Body::windowCmd` | missing | add only if manual body control is really kept |
| `Body::manualTurnCmd` | missing | add only if manual body control is really kept |
| `Chassis::ignitionCmd` | missing | add only if manual ignition control is really kept |
| `V2X::policePos` / `V2X::ambulancePos` | missing | add only if slider-based V2X control is preserved |
| `Test::driverBeltOff` | missing | optional, not default |

### 5.3 Variables already present on `develop`

These can be reused directly by donor panels with rebinding cleanup only:

- `Core::selectedAlertLevel`
- `Core::selectedAlertType`
- `Core::vehicleSpeedNorm`
- `Core::speedLimitNorm`
- `Core::baseZoneContext`
- `Infotainment::roadZone`
- `Infotainment::navDirection`
- `Infotainment::zoneDistance`
- `Infotainment::speedLimit`
- `V2X::alertState`
- `V2X::emergencyType`
- `V2X::emergencyDirection`
- `V2X::eta`
- `Body::ambientMode`
- `Cluster::warningTextCode`
- `UiRender::roadZoneColorCode`
- `UiRender::roadFlowDirection`
- `UiRender::renderColor`

## 6. CAPL / Channel Assign Merge Matrix

These files are high-risk because donor branches changed them for panel bring-up.  
Policy: inspect manually, re-apply only the minimum panel contract needed, preserve `develop` owner logic.

| File | Donor branches | Policy | Reason |
|---|---|---|---|
| `canoe/project/sysvars/project.sysvars` | both | manual line-by-line merge | central contract file |
| `canoe/src/capl/input/TEST_SCN.can` | both | do not wholesale-merge | donor branches use temporary scenario/manual injection paths |
| `canoe/src/capl/output/BCM.can` | both | manual extraction only | body control temp logic likely mixed with panel needs |
| `canoe/src/capl/output/CLU.can` | both | manual extraction only | cluster rendering must stay aligned with `develop` arbitration |
| `canoe/src/capl/output/IVI.can` | both | manual extraction only | IVI output/render bridge is baseline-critical |
| `canoe/src/capl/logic/ADAS.can` | both | manual extraction only | alert arbitration is baseline-critical |
| `canoe/src/capl/logic/V2X.can` | both | manual extraction only | emergency interpretation must remain on `develop` |
| `canoe/src/capl/ecu/VCU.can` | both | manual extraction only | vehicle state ownership is baseline-critical |
| `canoe/src/capl/ecu/MDPS.can` | both | manual extraction only | chassis interaction path |
| `canoe/src/capl/ecu/AMP.can` | both | manual extraction only | audio trigger path only if required |
| `canoe/src/capl/ecu/HUD.can` | both | manual extraction only | display surface only |
| `canoe/src/capl/ecu/CGW.can` | both | manual extraction only | gateway baseline-critical |
| `canoe/src/capl/ecu/TEST_BAS.can` | both | do not wholesale-merge | donor test harness temp logic |
| `canoe/src/capl/common/CAPL_COMMON.cin` | both | do not wholesale-merge | shared utility contract risk |
| `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can` | both | manual extraction only | biggest owner-collision risk |
| `canoe/cfg/channel_assign/Chassis/VCU.can` | both | manual extraction only | owner of vehicle state path |
| `canoe/cfg/channel_assign/Chassis/ESC.can` | both | manual extraction only | brake/ABS path |
| `canoe/cfg/channel_assign/Powertrain/EMS.can` | both | manual extraction only | dashboard/anim state easily mixed with engine owner logic |
| `canoe/cfg/channel_assign/Body/BCM.can` | both | manual extraction only | turn lamp / belt / comfort state owner |
| `canoe/cfg/channel_assign/Body/DOOR_FL.can` | `merge/lee` | manual extraction only | direct door/window owner path |
| `canoe/cfg/channel_assign/Body/WIP.can` | `merge/lee` | manual extraction only | wiper animation path |
| `canoe/cfg/channel_assign/ETH_Backbone/V2X.can` | both | manual extraction only | V2X UI hooks must not replace baseline transport logic |
| `canoe/cfg/channel_assign/Infotainment/CLU.can` | both | manual extraction only | cluster output consumer |
| `canoe/cfg/channel_assign/Infotainment/IVI.can` | both | manual extraction only | IVI surface path |
| `canoe/cfg/channel_assign/Infotainment/AMP.can` | both | manual extraction only | audio path |

## 7. DBC Guardrail Matrix

| File | Donor branch | Observed donor change | Decision |
|---|---|---|---|
| `canoe/databases/chassis_can.dbc` | `merge/lee` | changes `frmVehicleStateCanMsg` owner from `VCU` to `TEST_SCN` | reject |
| `canoe/databases/body_can.dbc` | `merge/lee` | expands `frmWiperStateMsg.FrontWiperState` to support more animation states | conditional review only |

DBC rule:
- never allow donor panel work to move canonical message ownership from product ECU to test harness
- if panel animation needs more states, prefer `sysvar -> panel` first
- touch DBC only when CAN-level payload expansion is truly required by the active design

## 8. Recommended Actual Merge Order

| Step | Action | Rule |
|---|---|---|
| 1 | create a fresh integration branch from `develop` or use a separate worktree | do not merge from current dirty worktree |
| 2 | import selected donor `.xvp` and only the asset files they really reference | no CAPL/sysvar/DBC yet |
| 3 | decide final panel inventory and GUI registration list | current develop draft panels still remain until replacement works |
| 4 | update `project.sysvars` manually for the selected donor panel contract | add only the minimum missing vars |
| 5 | patch CAPL/channel assign manually on top of `develop` | no donor wholesale file replacement |
| 6 | review DBC only if selected panels still need CAN payload/state expansion | reject owner drift |
| 7 | register panels in CANoe GUI and compile | `.cfg` save/generation is GUI-only |
| 8 | after GUI smoke pass, retire old `develop` draft panel files | delete only after proof |

## 9. First Working Selection Proposal

Use this as the first integration candidate set:

| Priority | Keep set | Reason |
|---|---|---|
| P1 | `sh_rael_merge/Navigation.xvp` | closest to current SDV navigation purpose |
| P1 | `sh_rael_merge/cluster.xvp` | closest to current cluster purpose |
| P1 | `sh_rael_merge/input.xvp` | practical operator panel base |
| P1 | `merge/lee/scenariocontrol.xvp` | clean scenario launcher |
| P1 | `merge/lee/v2xpanel.xvp` | isolated and low-risk visual donor |
| P2 | `sh_rael_merge/SDV_Ambient_Control.xvp` | small ambient-specific surface |
| P2 | `sh_rael_merge/SDV_Ambient_Top_View.xvp` | visual add-on after basic path works |
| P2 | `merge/lee/sample_Dashboard.xvp` | useful only after sysvar contract is stable |
| P2 | `merge/lee/windowstate.xvp` | useful only after body signal contract is stable |
| P3 | `merge/lee/MyDriverPanel.xvp` | do not integrate whole; mine widgets only if needed |

## 10. Immediate Next Document

After this matrix, the next useful temporary doc is:

- `TMP_PANEL_BINDING_GAP_임시_2026-03-19.md`

That follow-up document should map:
- selected donor panel
- actual referenced asset files
- exact sysvar names to add or rename
- exact CAPL/channel_assign file touched to support each selected panel
