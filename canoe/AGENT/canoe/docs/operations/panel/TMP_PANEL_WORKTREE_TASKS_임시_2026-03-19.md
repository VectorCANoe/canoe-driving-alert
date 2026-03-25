# TMP Panel Worktree Tasks (임시)

## 0. Purpose

This is the shortest execution note before the real panel integration starts.

Use it only after reviewing:

- `TMP_PANEL_BRANCH_MERGE_임시_2026-03-19.md`
- `TMP_PANEL_BINDING_GAP_임시_2026-03-19.md`
- `TMP_PANEL_GUI_IMPORT_CHECKLIST_임시_2026-03-19.md`

## 1. Suggested Clean Worktree Setup

Recommended branch:

- `panel/p1-merge-20260319`

Recommended worktree path:

- `C:\Users\이준영\.codex-tmp\panel-merge-20260319`

Reason:

- current main workspace is dirty
- panel integration must not start from that dirty state
- no conflicting local branch with this name is currently present

Suggested commands:

```powershell
git -C "C:\Users\이준영\CANoe-IVI-OTA" worktree add "C:\Users\이준영\.codex-tmp\panel-merge-20260319" -b panel/p1-merge-20260319 develop
git -C "C:\Users\이준영\.codex-tmp\panel-merge-20260319" status --short --branch
```

Expected result:

- new worktree starts clean on `develop`
- no existing CAPL/config dirty state leaks into panel integration

## 2. Donor Asset Staging Commands

Run these from the new worktree only.

### 2.1 From `origin/sh_rael_merge`

```powershell
git -C "C:\Users\이준영\.codex-tmp\panel-merge-20260319" checkout origin/sh_rael_merge -- `
  "canoe/project/panel/Navigation.xvp" `
  "canoe/project/panel/cluster.xvp" `
  "canoe/project/panel/input.xvp" `
  "canoe/project/panel/SDV_Ambient_Control.xvp" `
  "canoe/project/panel/SDV_Ambient_Top_View.xvp" `
  "canoe/project/panel/Bitmaps/IC.wav" `
  "canoe/project/panel/Bitmaps/speed.mp3" `
  "canoe/project/panel/Bitmaps/beep.wav" `
  "canoe/project/panel/Bitmaps/lane.png" `
  "canoe/project/panel/Bitmaps/zone.png" `
  "canoe/project/panel/Bitmaps/roadFlowDirection.png" `
  "canoe/project/panel/Bitmaps/gps.png" `
  "canoe/project/panel/Bitmaps/bg.png" `
  "canoe/project/panel/Bitmaps/vol.png" `
  "canoe/project/panel/Bitmaps/alertType.png" `
  "canoe/project/panel/Bitmaps/emergencyType.png" `
  "canoe/project/panel/Bitmaps/roadZone.png" `
  "canoe/project/panel/Bitmaps/Emergency Siren 7.mp3" `
  "canoe/project/panel/Bitmaps/CarTop.png" `
  "canoe/project/panel/Bitmaps/Group (1).png" `
  "canoe/project/panel/Bitmaps/Group (2)(1).png" `
  "canoe/project/panel/Bitmaps/Group (2)(2).png" `
  "canoe/project/panel/Bitmaps/Group (3).png" `
  "canoe/project/panel/Bitmaps/Group (4).png" `
  "canoe/project/panel/Bitmaps/Group (5).png"
```

### 2.2 From `origin/merge/lee`

```powershell
git -C "C:\Users\이준영\.codex-tmp\panel-merge-20260319" checkout origin/merge/lee -- `
  "canoe/project/panel/scenariocontrol.xvp" `
  "canoe/project/panel/v2xpanel.xvp" `
  "canoe/project/panel/Bitmaps/v2x.png"
```

Do not stage P2 files yet:

- `sample_Dashboard.xvp`
- `windowstate.xvp`
- their extra bitmap packs

## 3. First GUI Panel Inventory

Register only these panels in the first pass:

| Source | Panel | First-pass status |
|---|---|---|
| `sh_rael_merge` | `SDV_Ambient_Control.xvp` | active |
| `sh_rael_merge` | `input.xvp` | active |
| `sh_rael_merge` | `cluster.xvp` | active |
| `merge/lee` | `v2xpanel.xvp` | imported but waiting for `V2X::v2xFrame` |
| `sh_rael_merge` | `Navigation.xvp` | active after orphan widgets are handled |
| `sh_rael_merge` | `SDV_Ambient_Top_View.xvp` | visual-only first |
| `merge/lee` | `scenariocontrol.xvp` | deferred or partially disabled |

## 4. GUI Rebind / Disable Task List

### 4.1 `Navigation.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `Media Player 3` | `UiRender::beepIC` | disable or hide |
| `Media Player 2` | `UiRender::beepSpeed` | disable or hide |
| `Input/Output Box 3` | `CoreState::baseVolume` | rebind to `CoreState::volumeLevel` |
| `LED Control 1` | `UiRender::warningBeepState` | disable or hide |
| `Media Player 1` | `UiRender::beepEmergency` | disable or hide |
| `Input/Output Box 2` | `UiRender::renderVolumLevel` | rebind to `CoreState::volumeLevel` or disable |
| `Switch / Indicator 1` | `UiRender::navLaneFrame` | disable or hide |

Keep as-is:

- `Test::alertVolumeSetting`
- `UiRender::roadZoneColorCode`
- `UiRender::roadFlowDirection`
- `Core::vehicleSpeedNorm`
- `Core::speedLimitNorm`
- `Infotainment::zoneDistance`

### 4.2 `cluster.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `Switch / Indicator 2` | `adas_can/ADAS/ethEmergencyRiskMsg.EmergencyType` | prefer rebind to sysvar if easy; otherwise leave read-only for first pass |
| `Meter 1` | `chassis_can/VCU/frmVehicleStateCanMsg.gVehicleSpeed` | prefer rebind to `Chassis::vehicleSpeed` |

Keep as-is:

- `Core::selectedAlertType`
- `Cluster::warningTextCode`
- `UiRender::roadZoneColorCode`
- `UiRender::renderColor`

### 4.3 `input.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `Switch / Indicator 1` | `Test::manualAlertOverride` | disable or hide |

Visual cue:

- label text nearby is `manualAlertOverride:`

### 4.4 `SDV_Ambient_Top_View.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `emergencySound` | `Infotainment::emergencySound` | disable sound widget or leave unresolved intentionally |

### 4.5 `scenariocontrol.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `Display_AnimFrame` | `Display::animFrame` | disable or postpone whole panel |

### 4.6 `v2xpanel.xvp`

| ControlName | Current donor binding | First GUI action |
|---|---|---|
| `Switch / Indicator 1` | `V2X::v2xFrame` | keep imported, mark unresolved until code patch |

## 5. Code Patch Queue After First GUI Pass

Do not patch these before the first GUI import observation unless absolutely necessary.

Queue order:

1. add `V2X::v2xFrame` to `project.sysvars`
2. produce `V2X::v2xFrame` in:
   - `canoe/src/capl/logic/V2X.can`
   - `canoe/cfg/channel_assign/ETH_Backbone/V2X.can`
3. decide whether `Navigation.xvp` audio-related orphan widgets should:
   - get real render vars
   - be rebound to existing volume/audio state
   - be removed from first release
4. decide whether `scenariocontrol.xvp` should:
   - lose the `animFrame` display
   - or gain a replacement existing render/debug binding

## 6. First Compile / Measurement Task

After every GUI gate:

1. Save in CANoe GUI.
2. Compile CAPL.
3. Start measurement.
4. Verify:
   - `Body::ambientMode`
   - `Cluster::warningTextCode`
   - `UiRender::roadZoneColorCode`
   - `UiRender::renderColor`
   - `UiRender::roadFlowDirection`
   - `V2X::emergencyType`
   - `V2X::emergencyDirection`
   - `V2X::eta`
   - `V2X::alertState`
   - `Test::scenarioCommand`
   - `Test::scenarioResult`

## 7. Explicit Hold Points

Stop and do not continue the GUI session if any of these happen:

- config save touches unexpected unrelated panel registrations
- compile fails after importing a panel that should have been GUI-only
- a donor panel implies changing DBC owner to `TEST_SCN`
- a donor panel requires copying donor `EMS`, `TEST_SCN`, `BCM`, `CAPL_COMMON.cin` wholesale
- current `develop` smoke behavior regresses

## 8. Delete-Later Candidates

These are still delete-later only.  
Do not remove them during the first import session.

- `canoe/project/panel/SDV_Ambient_View.xvp`
- `canoe/project/panel/SDV_Cabin_Panorama_View.xvp`
- `canoe/project/panel/SDV_Cluster_View.xvp`
- `canoe/project/panel/SDV_Control.xvp`
- `canoe/project/panel/SDV_Demo_Stage.xvp`
- `canoe/project/panel/SDV_External_Road_View.xvp`
- `canoe/project/panel/SDV_Monitor.xvp`
- `canoe/project/panel/SDV_Navigation_View.xvp`
- `canoe/project/panel/SDV_Render_Debug.xvp`
- `canoe/project/panel/SDV_Test_Operator.xvp`

## 9. Next Practical Step After This Note

Once the new worktree is created, the next concrete action is:

1. stage the donor XVPs and assets with the commands above
2. open the clean worktree config in CANoe GUI
3. import `SDV_Ambient_Control.xvp` first
4. follow the gate order from `TMP_PANEL_GUI_IMPORT_CHECKLIST_임시_2026-03-19.md`
