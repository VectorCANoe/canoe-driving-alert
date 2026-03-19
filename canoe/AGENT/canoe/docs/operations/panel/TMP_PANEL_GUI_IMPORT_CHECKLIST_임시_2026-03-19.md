# TMP Panel GUI Import Checklist (임시)

## 0. Scope

This checklist is for the first real GUI-side integration pass only.

Target:

- keep `develop` logic and owner design intact
- replace current `develop` draft panels with donor panels gradually
- import P1 panels first
- postpone P2 panels until the first compile/measurement pass is stable

Related temporary docs:

- `TMP_PANEL_BRANCH_MERGE_임시_2026-03-19.md`
- `TMP_PANEL_BINDING_GAP_임시_2026-03-19.md`

## 1. Pre-Flight Gate

Do not start GUI import from the current dirty working tree.

Current local warning:

- `canoe/cfg/CAN_v2_topology.cfg` is dirty
- `canoe/src/capl/input/TEST_SCN.can` is dirty
- `canoe/src/capl/common/CAPL_COMMON.cin` is dirty
- `canoe/cfg/channel_assign/ETH_Backbone/TEST_SCN.can` is dirty
- `canoe/cfg/channel_assign/common/CAPL_COMMON.cin` is dirty

Required setup before GUI work:

1. Create a fresh integration branch from `develop`.
2. Use a separate worktree or otherwise isolate the panel integration environment.
3. Open only the `develop`-based config that belongs to that isolated branch.
4. Do not delete existing `develop` draft panels yet.

GUI config rule:

- open/save only through CANoe GUI
- use `canoe/cfg/CAN_v2_topology.cfg` as the starting config unless the team explicitly chooses another GUI-saved integration config
- if the config becomes unstable, use GUI `Save As` to a new temporary config name

## 2. First-Wave Import Order

Import in this order to maximize early success and reduce rework.

| Order | Panel | Why this order |
|---|---|---|
| 1 | `SDV_Ambient_Control.xvp` | already satisfied by `develop`; lowest risk |
| 2 | `input.xvp` | mostly satisfied; only one orphan binding |
| 3 | `cluster.xvp` | mostly satisfied; only raw-CAN cleanup |
| 4 | `v2xpanel.xvp` | one clean new render var |
| 5 | `Navigation.xvp` | useful, but has multiple orphan audio/render bindings |
| 6 | `SDV_Ambient_Top_View.xvp` | visual value is high, but sound contract is orphan |
| 7 | `scenariocontrol.xvp` | blocked until `Display::animFrame` decision is made |

Deferred:

- `sample_Dashboard.xvp`
- `windowstate.xvp`

## 3. Asset Staging Checklist

Stage only the assets needed by the imported panels.

### 3.1 Import set from `sh_rael_merge`

| Panel | Required assets |
|---|---|
| `Navigation.xvp` | `Bitmaps/IC.wav`, `Bitmaps/speed.mp3`, `Bitmaps/beep.wav`, `Bitmaps/lane.png`, `Bitmaps/zone.png`, `Bitmaps/roadFlowDirection.png`, `Bitmaps/gps.png`, `Bitmaps/bg.png`, `Bitmaps/vol.png` |
| `cluster.xvp` | `Bitmaps/alertType.png`, `Bitmaps/emergencyType.png`, `Bitmaps/roadZone.png`, `Bitmaps/zone.png` |
| `SDV_Ambient_Top_View.xvp` | `Bitmaps/Emergency Siren 7.mp3`, `Bitmaps/CarTop.png`, `Bitmaps/Group (1).png`, `Bitmaps/Group (2)(1).png`, `Bitmaps/Group (2)(2).png`, `Bitmaps/Group (3).png`, `Bitmaps/Group (4).png`, `Bitmaps/Group (5).png` |

### 3.2 Import set from `merge/lee`

| Panel | Required assets |
|---|---|
| `v2xpanel.xvp` | `Bitmaps/v2x.png` |

Do not stage P2 assets yet.

## 4. GUI Import Actions By Panel

### 4.1 `SDV_Ambient_Control.xvp`

Action:

1. Import panel into the GUI panel list.
2. Verify binding still points to `Body::ambientMode`.
3. Save panel registration in GUI.

Expected result:

- no rebind needed
- safe first compile candidate

### 4.2 `input.xvp`

Action:

1. Import panel.
2. Verify these bindings resolve without edit:
   - `Chassis::driveState`
   - `Core::vehicleSpeedNorm`
   - `Core::speedLimitNorm`
   - `Core::baseZoneContext`
   - `Core::selectedAlertType`
   - `Core::selectedAlertLevel`
   - `Chassis::vehicleSpeed`
   - `V2X::emergencyType`
   - `V2X::emergencyDirection`
   - `V2X::alertState`
   - `V2X::eta`
   - `Infotainment::speedLimit`
   - `Infotainment::zoneDistance`
   - `Infotainment::navDirection`
   - `Infotainment::roadZone`
3. For `Test::manualAlertOverride`, do one of these:
   - disable the widget
   - hide the widget
   - temporarily leave it unbound and mark it as unresolved

Do not:

- add `manualAlertOverride` just to make the panel import clean

### 4.3 `cluster.xvp`

Action:

1. Import panel.
2. Keep these bindings as-is:
   - `Core::selectedAlertType`
   - `Cluster::warningTextCode`
   - `UiRender::roadZoneColorCode`
   - `UiRender::renderColor`
3. Review these raw CAN bindings:
   - `adas_can/ADAS/ethEmergencyRiskMsg.EmergencyType`
   - `chassis_can/VCU/frmVehicleStateCanMsg.gVehicleSpeed`
4. Preferred GUI cleanup:
   - rebind speed display to `Chassis::vehicleSpeed`
   - if possible rebind alert-type display to a sysvar instead of direct CAN

Do not:

- change DBC owner or producer just to satisfy this panel

### 4.4 `v2xpanel.xvp`

Action:

1. Stage `Bitmaps/v2x.png`.
2. Import panel.
3. `V2X::v2xFrame` is now staged in the panel branch compat layer.
4. Keep this widget read-only.
5. If GUI still reports missing binding, treat it as a config reload issue first and reopen the branch-local cfg before debugging CAPL.

### 4.5 `Navigation.xvp`

Action:

1. Stage all audio/image assets first.
2. Import panel.
3. Keep these existing bindings:
   - `Test::alertVolumeSetting`
   - `UiRender::roadZoneColorCode`
   - `UiRender::roadFlowDirection`
   - `Core::vehicleSpeedNorm`
   - `Core::speedLimitNorm`
   - `Infotainment::zoneDistance`
4. `CoreState::baseVolume` display has already been rebased to `CoreState::volumeLevel`.
5. `UiRender::beepIC`, `UiRender::beepSpeed`, `UiRender::warningBeepState`, and `UiRender::beepEmergency` are now staged as compat read-only render vars.
6. Remaining unresolved candidates, if any, should still be treated conservatively:
   - `UiRender::renderVolumLevel`
   - `UiRender::navLaneFrame`
7. For the unresolved items above, choose one temporary treatment:
   - disable widget
   - hide widget
   - leave unresolved and document it

### 4.6 `SDV_Ambient_Top_View.xvp`

Action:

1. Stage all required image/audio assets first.
2. Import panel.
3. `Infotainment::emergencySound` is now staged in the panel branch compat layer.
4. Keep the media widget read-only and verify that GUI resolves the binding after cfg reopen.
5. If binding still appears broken, debug GUI reload/config state before changing CAPL again.

### 4.7 `scenariocontrol.xvp`

Action:

1. Import panel only after the first six panels are already checked.
2. Verify the existing `Test::scenarioCommand`, `Test::testScenario`, `Test::scenarioResult` bindings.
3. Keep `Test::scenarioCommand` as the only writable launch/stop path.
4. Keep `Test::testScenario` read-only as the current scenario mirror.
5. Stop on `Display::animFrame`.

Decision gate:

- if the team has not approved a replacement for `Display::animFrame`, do not fully activate this panel
- leave the animation widget disabled or postpone this panel entirely

Do not:

- add a `Display` namespace just to satisfy the donor panel
- copy donor `EMS` animation logic into `develop`

## 5. Compile Gates

Use staged compile gates. Do not import all panels first and debug later.

| Gate | Target set | Pass condition |
|---|---|---|
| G1 | `SDV_Ambient_Control.xvp` | GUI import succeeds and CAPL compile still passes |
| G2 | + `input.xvp`, `cluster.xvp` | GUI import succeeds, key bindings resolve, compile still passes |
| G3 | + `v2xpanel.xvp` | panel can exist unresolved but no accidental config corruption |
| G4 | + `Navigation.xvp` | unresolved orphan widgets are intentionally handled, compile still passes |
| G5 | + `SDV_Ambient_Top_View.xvp` | unresolved sound binding is intentional and recorded |
| G6 | `scenariocontrol.xvp` | only after animation binding decision |

After each gate:

1. Save in GUI.
2. Compile CAPL.
3. Start measurement.
4. Verify that existing `develop` logic still runs.

Important config note:

- If `project.sysvars` or panel assets changed in the worktree, close CANoe completely and reopen the branch-local [CAN_v2_topology.cfg](/C:/Users/이준영/.codex-tmp/panel-merge-20260319/canoe/cfg/CAN_v2_topology.cfg) before compile.
- If GUI reports many `Variable name ... not found` or broad `Database missing? / this not allowed in this context` errors across unrelated ECUs, treat that as stale GUI config state first, not as CAPL-wide logic failure.

## 6. Smoke Verification Set

For the first GUI pass, use a reduced smoke set before full panel validation.

| Check | What to verify |
|---|---|
| Ambient path | `Body::ambientMode` still changes correctly |
| Cluster path | `Cluster::warningTextCode` still changes correctly |
| Render path | `UiRender::roadZoneColorCode`, `UiRender::renderColor`, `UiRender::roadFlowDirection` still update |
| V2X path | `V2X::emergencyType`, `V2X::emergencyDirection`, `V2X::eta`, `V2X::alertState` still update |
| Scenario path | `Test::scenarioCommand`, `Test::scenarioResult` still behave as before |

Use `PANEL_PASS_CHECKLIST.md` only after the first import pass is stable.

## 7. Current Develop Draft Panel Deletion Gate

Do not delete the current `develop` draft panels until all conditions below are true.

1. P1 donor panels are imported in GUI.
2. The config saves cleanly from GUI.
3. CAPL compile passes.
4. Measurement starts cleanly.
5. Core smoke verification passes.
6. Any blocked panels are explicitly deferred, not silently broken.

Only after that:

- remove old draft panels from GUI registration first
- then delete retired XVP files from source control

## 8. Explicit No-Go Actions

Do not do these during the first GUI pass:

- full-merge any donor `CAPL_COMMON.cin`
- full-merge donor `TEST_SCN.can`
- full-merge donor `EMS.can`
- change DBC owner from product ECU to `TEST_SCN`
- delete current `develop` panel files before donor pass proof exists
- patch `.cfg`, `.cfg.ini`, `.stcfg` outside CANoe GUI

## 9. Expected Next Work After GUI Pass

Once the GUI import pass is complete, the next implementation batch should be:

1. `V2X::v2xFrame` support in `develop` V2X logic
2. optional navigation/audio render vars for `Navigation.xvp`
3. decision on `Display::animFrame` replacement or widget removal
4. only then P2 donor promotion review for `sample_Dashboard.xvp` and `windowstate.xvp`
