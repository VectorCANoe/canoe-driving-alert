# Manual Contract Check (2026-03-01)

## Scope
- CAN DBC: `chassis_can.dbc`, `powertrain_can.dbc`, `body_can.dbc`, `infotainment_can.dbc`, `test_can.dbc`
- Backup DBC: `emergency_system.dbc` (legacy compatibility only)
- CAPL: `canoe/src/capl/**/*.can`
- Docs: `0302`, `0303`, `0304`, `ETH_INTERFACE_CONTRACT.md`

## Manual Checks

1. Split SoT structure
- Result: PASS
- Active split DBC set exists and is loaded in CANoe UI.
- Backup single DBC exists separately and can be kept for fallback.

2. Core chain ownership (manual CAPL vs DBC cross-check)
- Result: PASS (core chain)
- Verified sender and CAPL output alignment:
  - `frmVehicleStateCanMsg` (SIL_TEST_CTRL -> `output(mVeh)`)
  - `frmSteeringCanMsg` (SIL_TEST_CTRL -> `output(mStr)`)
  - `frmNavContextCanMsg` (SIL_TEST_CTRL -> `output(mNav)`)
  - `frmAmbientControlMsg` (BODY_GW -> `output(mAmbient)`)
  - `frmClusterWarningMsg` (IVI_GW -> `output(mCluster)`)
  - `frmTestResultMsg` (SIL_TEST_CTRL -> `output(mRes)`)

3. Expanded frame runtime ownership readiness
- Result: PARTIAL (design-ready, runtime profile split needed)
- `*_can.dbc` canonical set now uses split-domain contract IDs and does not include legacy aggregate base frames.
- Core runtime CAPL chain remains clean (`frmVehicleStateCanMsg`, `frmSteeringCanMsg`, `frmNavContextCanMsg`, `frmAmbientControlMsg`, `frmClusterWarningMsg`, `frmTestResultMsg`).
- `CANoeIL ... TxFrameUpdateRequest` errors are tied to legacy `CAN_500kBaud_1ch.cfg` + `emergency_system.dbc` IL profile, not to the split canonical DBC set.

4. Document vs DBC ID consistency (Comm_101/105/106 subset)
- Result: PASS
- Manual cross-check (split canonical set):
  - `frmIgnitionEngineMsg` = `0x300`
  - `frmGearStateMsg` = `0x301`
  - `frmPowertrainGatewayMsg` = `0x302`
  - `frmEngineSpeedTempMsg` = `0x303`
  - `frmBaseTestResultMsg` = `0x231`
- Manual duplicate audit:
  - Active messages: `94`
  - Duplicate IDs: `0`
  - Duplicate names: `0`

5. Document vs DBC full synchronization (0302 + 0303 frm(ID) references)
- Result: PASS
- Auto-assisted manual check summary:
  - `0302/0303` unique `frm(ID)` references: `81`
  - Missing in split DBC set: `0`
  - ID mismatch vs split DBC set: `0`
- Note:
  - Split DBC set contains additional defined frames (`13`) not explicitly enumerated in current 0302/0303 `frm(ID)` list (design-reserved/extended internal frames).

6. Ethernet contract SoT statement
- Result: FIXED
- `ETH_INTERFACE_CONTRACT.md` is present and used as Ethernet SoT.
- CAN SoT is split to `chassis/body/infotainment/powertrain/test` DBC set.

## Immediate Action Recommendation

1. Keep runtime profile strict:
- Use split canonical DBC runtime profile (`CAN_500kBaud_1ch_split.cfg`) as default.
- Keep `CAN_500kBaud_1ch.cfg` + `emergency_system.dbc` as legacy backup profile only.

2. Resolve one-source ID map:
- Keep `0303` and split `*_can.dbc` IDs synchronized as single source of truth.

3. Re-run startup gate:
- If running legacy cfg, either disable IL profile for unsupported Tx ownership or switch to split runtime profile.
- Then proceed to scenario validation.

