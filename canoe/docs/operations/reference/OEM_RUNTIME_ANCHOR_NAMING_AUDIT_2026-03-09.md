# OEM Runtime Anchor Naming Audit (2026-03-09)

## Scope
This audit rechecks the remaining runtime anchors that were intentionally not absorbed:
- `CHGW`
- `PTGW`
- `CGW`
- `ETHM`

The goal is to decide:
1. whether the current name is only ugly or structurally misleading
2. whether the node should remain split
3. what OEM-normalized runtime name should be used later during GUI/runtime rename

## Summary Decision

| Current Runtime Node | Keep Split | Prior Mapping | Rechecked Result | Proposed OEM-Normalized Runtime Name | Reason |
| --- | --- | --- | --- | --- | --- |
| `CHGW` | Yes | `CGW` | prior mapping too broad | `CHGW` | not a central gateway; owns chassis state synthesis and chassis diagnostic response |
| `PTGW` | Yes | `CGW` | prior mapping too broad | `PTGW` | routes powertrain policy and publishes drive mode / powertrain health |
| `CGW` | Yes | `CGW` | keep under gateway/infrastructure | `CGW` | owns cross-domain health, fail-safe, boundary authority |
| `ETHM` | Yes | `ETH_BACKBONE` | keep under Ethernet backbone | `ETHM` | monitors freshness/age only, not a real switch/router |

## Detailed Readback

### 1. `CHGW`
Source: [CHGW.can](../../src/capl/input/CHGW.can)

Observed responsibilities:
- normalizes `frmVehicleStateCanMsg`, `frmSteeringCanMsg`, `frmPedalInputCanMsg` into `@Core::*`
- publishes wheel speed, yaw/accel, brake, accel, MDPS, ABS, ESC, TCS, suspension, tire pressure, brake wear, road friction
- serves `frmChassisDiagReqMsg -> frmChassisDiagResMsg`

Decision:
- this is not a thin CAN gateway
- this is the active chassis domain runtime anchor
- therefore `CGW` classification is misleading

Recommended naming direction:
- surface owner remains chassis-side
- runtime normalized name: `CHGW`
- OEM surface alias later: `ESC`, `MDPS`, `ABS`, `TPMS`, `SAS`, `ECS` remain as breadth ECUs, but this anchor is the current chassis domain controller

### 2. `PTGW`
Source: [PTGW.can](../../src/capl/ecu/PTGW.can)

Observed responsibilities:
- derives `routingPolicy`
- publishes `frmVehicleModeMsg`, `frmPowerLimitMsg`, `frmCruiseStateMsg`, `frmEnergyFlowStateMsg`, `frmPowertrainCtrlAuthMsg`
- mirrors `driveMode`, `ecoMode`, `sportMode`
- handles `frmPtDiagReqMsg -> frmPtDiagResMsg`

Decision:
- this is not a central gateway either
- it is closer to a powertrain domain coordinator/controller
- therefore `CGW` classification is misleading

Recommended naming direction:
- runtime normalized name: `PTGW`
- surface alignment later: `EMS`, `TCU`, `VCU`, `AWD_4WD` remain separate surface ECUs, but current active anchor is powertrain-domain level

### 3. `CGW`
Source: [CGW.can](../../src/capl/ecu/CGW.can)

Observed responsibilities:
- monitors chassis/body/infotainment health age
- owns `domainBoundaryStatus`, `domainPathStatus`, `e2eHealthState`
- owns fail-safe escalation and clears `decelAssistReq`
- emits `ethFailSafeStateMsg`, `ethObjectSafetyStateMsg`

Decision:
- keep split
- this is the correct safety/boundary authority anchor
- current name is implementation-heavy but structurally valid

Recommended naming direction:
- runtime normalized name: `CGW`
- surface classification may stay under infrastructure/gateway domain, not under body/chassis/powertrain

### 4. `ETHM`
Source: [ETHM.can](../../src/capl/network/ETHM.can)

Observed responsibilities:
- tracks age for vehicle/nav/steering/emergency monitor messages
- computes only `gEthPathHealthy`
- does not route payloads

Decision:
- keep split
- current name overstates switch behavior
- active SIL meaning is path freshness monitor, not switch fabric

Recommended naming direction:
- runtime normalized name: `ETHM`
- surface owner remains `ETH_BACKBONE`

## Structural Issues Found
No urgent code defect requiring immediate refactor was found in this audit.

However, two classification issues were corrected:
1. `CHGW` should not be treated as `CGW`
2. `PTGW` should not be treated as `CGW`

## Next Dev1 Action
1. update runtime-to-surface mapping documents in `canoe/docs/operations/reference`
2. keep actual file rename deferred until GUI/runtime rename wave
3. use the normalized names above for future reviewer-facing GUI labels

