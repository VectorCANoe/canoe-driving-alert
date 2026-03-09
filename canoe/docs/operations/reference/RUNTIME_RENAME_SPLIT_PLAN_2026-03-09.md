# Runtime Rename Split Plan (2026-03-09)

## Status

This plan is closed on the current Dev1 active baseline (`56521c2` aligned).

## Final active runtime names (current)
- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `CGW`
- `BCM`
- `IVI`
- `CLU`
- `ADAS`
- `V2X`
- `TST_SCN`
- `TST_BAS`

Count: `13`

## Historical note (retired working labels)

The following labels were used in an intermediate design discussion and are now retired from active runtime:
- `CHGW`
- `PTGW`
- `ETHM`

Current ownership for those concerns is implemented in:
- `VCU` (powertrain/vehicle-state seam)
- `MDPS` (steering seam)
- `CGW` (cross-domain boundary/freshness/fail-safe authority)

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
Import from `canoe/cfg/channel_assign/**` must keep:
- active runtime names above
- OEM placeholder surface names
- wrapper-only names excluded
