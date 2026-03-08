# OEM Runtime Anchor Naming Audit (2026-03-09)

## Scope
This audit rechecks the remaining runtime anchors that were intentionally not absorbed:
- `CHS_GW`
- `DOMAIN_ROUTER`
- `DOMAIN_BOUNDARY_MGR`
- `ETH_SW`

The goal is to decide:
1. whether the current name is only ugly or structurally misleading
2. whether the node should remain split
3. what OEM-normalized runtime name should be used later during GUI/runtime rename

## Summary Decision

| Current Runtime Node | Keep Split | Prior Mapping | Rechecked Result | Proposed OEM-Normalized Runtime Name | Reason |
| --- | --- | --- | --- | --- | --- |
| `CHS_GW` | Yes | `CGW` | prior mapping too broad | `CHASSIS_DOMAIN_CTRL` | not a central gateway; owns chassis state synthesis and chassis diagnostic response |
| `DOMAIN_ROUTER` | Yes | `CGW` | prior mapping too broad | `PT_DOMAIN_CTRL` | routes powertrain policy and publishes drive mode / powertrain health |
| `DOMAIN_BOUNDARY_MGR` | Yes | `CGW` | keep under gateway/infrastructure | `DOMAIN_BOUNDARY_CTRL` | owns cross-domain health, fail-safe, boundary authority |
| `ETH_SW` | Yes | `ETH_BACKBONE` | keep under Ethernet backbone | `ETH_PATH_MONITOR` | monitors freshness/age only, not a real switch/router |

## Detailed Readback

### 1. `CHS_GW`
Source: [CHS_GW.can](../../src/capl/input/CHS_GW.can)

Observed responsibilities:
- normalizes `frmVehicleStateCanMsg`, `frmSteeringCanMsg`, `frmPedalInputCanMsg` into `@Core::*`
- publishes wheel speed, yaw/accel, brake, accel, EPS, ABS, ESC, TCS, suspension, tire pressure, brake wear, road friction
- serves `frmChassisDiagReqMsg -> frmChassisDiagResMsg`

Decision:
- this is not a thin CAN gateway
- this is the active chassis domain runtime anchor
- therefore `CGW` classification is misleading

Recommended naming direction:
- surface owner remains chassis-side
- runtime normalized name: `CHASSIS_DOMAIN_CTRL`
- OEM surface alias later: `ESP`, `EPS`, `ABS`, `TPMS`, `SAS`, `ECS` remain as breadth ECUs, but this anchor is the current chassis domain controller

### 2. `DOMAIN_ROUTER`
Source: [DOMAIN_ROUTER.can](../../src/capl/ecu/DOMAIN_ROUTER.can)

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
- runtime normalized name: `PT_DOMAIN_CTRL`
- surface alignment later: `ECM`, `TCM`, `VCU`, `AWD_4WD` remain separate surface ECUs, but current active anchor is powertrain-domain level

### 3. `DOMAIN_BOUNDARY_MGR`
Source: [DOMAIN_BOUNDARY_MGR.can](../../src/capl/ecu/DOMAIN_BOUNDARY_MGR.can)

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
- runtime normalized name: `DOMAIN_BOUNDARY_CTRL`
- surface classification may stay under infrastructure/gateway domain, not under body/chassis/powertrain

### 4. `ETH_SW`
Source: [ETH_SW.can](../../src/capl/network/ETH_SW.can)

Observed responsibilities:
- tracks age for vehicle/nav/steering/emergency monitor messages
- computes only `gEthPathHealthy`
- does not route payloads

Decision:
- keep split
- current name overstates switch behavior
- active SIL meaning is path freshness monitor, not switch fabric

Recommended naming direction:
- runtime normalized name: `ETH_PATH_MONITOR`
- surface owner remains `ETH_BACKBONE`

## Structural Issues Found
No urgent code defect requiring immediate refactor was found in this audit.

However, two classification issues were corrected:
1. `CHS_GW` should not be treated as `CGW`
2. `DOMAIN_ROUTER` should not be treated as `CGW`

## Next Dev1 Action
1. update runtime-to-surface mapping documents in `canoe/docs/operations/reference`
2. keep actual file rename deferred until GUI/runtime rename wave
3. use the normalized names above for future reviewer-facing GUI labels
