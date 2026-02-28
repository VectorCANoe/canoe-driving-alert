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
- Result: FAIL (not runtime-ready)
- Messages such as `frmSteeringStateCanMsg`, `frmWheelSpeedMsg`, `frmYawAccelMsg`, `frmChassisHealthMsg`, `frmChassisBaseMsg` are defined in DBC.
- Current CAPL does not publish these frames.
- If CANoeIL runtime tries to own/register them without valid owner setup, `TxFrameUpdateRequest` resource error occurs.

4. Document vs DBC ID consistency (Comm_101/105/106 subset)
- Result: FAIL (traceability mismatch)
- In `0303`, several IDs are still written with older mapping (example: `frmIgnitionEngineMsg(0x300)`, `frmBaseTestResultMsg(0x231)`).
- In current DBC:
  - `frmIgnitionEngineMsg` = `0x305`
  - `frmGearStateMsg` = `0x306`
  - `frmPowertrainGatewayMsg` = `0x307`
  - `frmEngineSpeedTempMsg` = `0x308`
  - `frmBaseTestResultMsg` = `0x304`
- Manual conclusion: before final freeze, docs and DBC IDs must be re-synced to one authoritative map.

5. Ethernet contract SoT statement
- Result: FIXED
- `ETH_INTERFACE_CONTRACT.md` previously referenced single DBC path.
- Updated to reference split DBC set as CAN SoT.

## Immediate Action Recommendation

1. Keep runtime profile strict:
- Activate only Runtime-Core frames in IL/CAPL ownership.
- Keep extended frames as design-defined but runtime-disabled until owner implementation is ready.

2. Resolve one-source ID map:
- Decide authoritative ID map (current DBC vs 0303 table).
- Update the non-authoritative side immediately.

3. Re-run startup gate:
- No `CANoeIL ... TxFrameUpdateRequest` errors.
- Then proceed to scenario validation.

