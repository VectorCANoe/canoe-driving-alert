# project/panel

CANoe panel artifacts for this project.

<<<<<<< HEAD
## Files
- Legacy `develop` draft XVP panels were retired and removed.
- Active donor-panel integration work is maintained in the dedicated merge branch/worktree.
- `develop` no longer keeps placeholder panel drafts as an in-repo baseline.
=======
## Donor Intake Status

### GUI-activated donor set
- `Ambient_Control.xvp`: adopted from `sh_rael_merge`
- `input.xvp`: adopted from `sh_rael_merge`
- `cluster.xvp`: adopted from `sh_rael_merge`
- `Navigation.xvp`: adopted from `sh_rael_merge`
- `Ambient_Top_View.xvp`: adopted from `sh_rael_merge`
- `v2xpanel.xvp`: adopted from `merge/lee`
- `scenariocontrol.xvp`: adopted from `merge/lee`

### Source-staged donor set
- `sample_Dashboard.xvp`: source-staged only, dashboard bindings were normalized onto panel/sysvar contracts, but GUI/operator review is still pending
- `sample_Control.xvp`: source-staged only, cruise widgets now bind via `Powertrain::*` compat sysvars and GUI/operator review is still pending
- `MyDriverPanel.xvp`: source-staged only, refreshed from latest `origin/lee`
- `car_inner.xvp`: source-staged only, cabin panel bindings were normalized onto panel/sysvar contracts, but GUI/operator review is still pending
- `windowstate.xvp`: source-staged only, body display bindings were moved to sysvars, but GUI/operator review is still pending

### Draft-panel note
- Unchanged `develop` draft XVP carry-overs were removed again after donor union intake
- Exact `main/develop` carry-over `SDV_Control.xvp` was removed from this branch
- Only donor-new or donor-modified panels remain in this branch
- Bitmap assets are kept broadly to avoid donor panel breakage, even when some files also exist in older baselines
>>>>>>> origin/panel/p1-merge-20260319

## Skin Assets (Project)
- `Bitmaps/DashboardCombi.png`
- `Bitmaps/DashboardCircleBlack.png`
- `Bitmaps/DashboardABS.png`
- `Bitmaps/DashboardFlasherLeft.png`
- `Bitmaps/DashboardFlasherRight.png`
- `Bitmaps/CruiseControlIndicator.bmp`
- `Bitmaps/brakelamp.png`
- `Bitmaps/brake.bmp`
- `Bitmaps/StageDashboard.png`
- `Bitmaps/ivi.png`
- `Bitmaps/left flash.png`
- `Bitmaps/right flash.png`
- `Bitmaps/left window.png`
- `Bitmaps/pedal.bmp`
- `Bitmaps/wifer.png`
- `Bitmaps/ControlIgnition.png`
- `Bitmaps/KakaoTalk_20260310_003301280_10 (1).bmp`
- `Bitmaps/KakaoTalk_20260310_003458323.bmp`
- `Bitmaps/reference_pack_v1/*`: curated Vector sample pack for external/cabin upgrade

## Legacy Carry-Over Status
- Legacy XVP carry-overs are removed aggressively.
- Bitmap assets are retained if they may support current donor panels or future GUI activation work.

## Reference Source Matrix (Adopted)
- External vehicle/light base: `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels`
- External top-view/road line icons: `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel`
- V2X traffic icon set: `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels`
- Cabin panorama/window animation strips: `reference/vector_samples_19_4_10/LIN/LINSystem/Panels`
- Additional control idioms: `reference/vector_code_sample`

<<<<<<< HEAD
## Panel Split (Target)
- `develop` does not preserve draft-panel structure.
- Final active panel registration is resolved through the donor merge branch and GUI registration cleanup.
=======
## Panel Split (Integration Branch)
- Donor union intake was pruned to exclude unchanged `develop` draft XVP carry-overs
- GUI-activated donor panels: `Ambient_Control.xvp`, `input.xvp`, `cluster.xvp`, `Navigation.xvp`, `Ambient_Top_View.xvp`, `v2xpanel.xvp`, `scenariocontrol.xvp`
- Source-staged donor panels still need GUI/operator review before activation: `sample_Dashboard.xvp`, `sample_Control.xvp`, `MyDriverPanel.xvp`, `car_inner.xvp`, `windowstate.xvp`

## Interaction Model

### Official Scenario Control
- `scenariocontrol.xvp`
- Official automated flow stays on `Test::scenarioCommand`
- `Test::testScenario` is status mirror only
- `Test::scenarioResult` is verdict display only

### Manual Sandbox / Operator Input
- `input.xvp`
  - direct operator inputs such as `Chassis::driveState`, `Chassis::vehicleSpeed`, `Infotainment::speedLimit`
- `MyDriverPanel.xvp`
  - broad exploratory control surface for doors, locks, ignition, wiper, windows, turn command, steering, belt-off flags, and emergency vehicle positions
- `sample_Control.xvp`
  - raw/manual driving controls such as throttle and brake inputs
- `Navigation.xvp`
  - keeps writable `Test::alertVolumeSetting` for exploratory panel-side tuning

### Display-Only Panels
- `Ambient_Control.xvp`
- `Ambient_Top_View.xvp`
- `cluster.xvp`
- `v2xpanel.xvp`
- Compat outputs like `V2X::v2xFrame`, `Infotainment::emergencySound`, and `UiRender::beep*` are panel-read-only

### Source-Staged Review Set
- `car_inner.xvp`
- `sample_Dashboard.xvp`
- `windowstate.xvp`
- These are not yet part of the official GUI-activated set and still require operator/layout review.
>>>>>>> origin/panel/p1-merge-20260319

## BP (Renderer-Only Contract)
- Decision/arbitration logic stays in `ADAS` and `ADAS`
- `IVI` and XVP panels are display-only
- No priority/timeout logic in renderer layer
- Renderer binds derived outputs only (`UiRender::*`)
- Do not bind raw inputs (`vehicleSpeed`, `eta`) directly to skin controls
- Add/modify `UiRender_*` only with SSoT update in `0304`

## GUI-Only Scope
- `.xvp` layout/property/binding changes must be done in CANoe GUI Panel Editor
- `.cfg`, `.cfg.ini`, `.stcfg` save/generation must be done in CANoe GUI
- Agent may edit text docs, CAPL logic, and bitmap assets only

## GUI Cleanup Pending
- `CAN_v2_topology.cfg` must reflect the final donor registration set on the next CANoe GUI panel-registration save

## Compat Guardrail
- Donor panel compat outputs such as `V2X::v2xFrame`, `Infotainment::emergencySound`, `Display::steeringFrame`, and `UiRender::beep*` are display-only at the panel layer
- Producer-owned compat sysvars may remain writable for CAPL publishers, but panel widgets must keep read-only bindings
- Manual exploration inputs stay under `Test::*` or approved operator input namespaces
- Current donor XVP set is normalized onto sysvar contracts; no direct `SymbolConfiguration` CAN bindings remain in active donor files
- Do not lock manual sandbox widgets just because official scenario widgets are read-only; exploratory operator inputs are intentional.

## Render Variables
Use these derived sysvars for animation-ready visualization:
- `UiRender::renderMode`
- `UiRender::renderColor`
- `UiRender::renderPattern`
- `UiRender::renderTextCode`
- `UiRender::renderDirection`
- `UiRender::roadZoneColorCode`
- `UiRender::roadFlowDirection`
- `UiRender::vehicleObjectPos`
- `UiRender::emsBlinkPhase`
- `UiRender::ambientPulsePhase`
- `UiRender::icFlowPhase`
- `UiRender::activeAlertType`
