# Runtime Rename Split Plan (2026-03-09)

## Final rename result

The runtime rename wave is now closed on the active Dev1 baseline.

## Final active runtime names
- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `CHGW`
- `PTGW`
- `CGW`
- `ETHM`
- `BCM`
- `IVI`
- `CLU`
- `ADAS`
- `V2X`
- `VAL_SCENARIO_CTRL`
- `VAL_BASELINE_CTRL`

## Removed wrapper-only names
These no longer belong in the active tree.
- `HAZARD_CTRL`
- `WINDOW_CTRL`
- `DRV_STATE_MGR`
- `AMBIENT_CTRL`
- `INFOTAINMENT_GW`
- `NAV_CTX_MGR`
- `CLU_BASE_CTRL`
- `EMS_POLICE_TX`
- `EMS_AMB_TX`
- `WARN_ARB_MGR`

## Import rule
The user can now import directly from `canoe/cfg/channel_assign/**` without reintroducing wrapper-only nodes.
