# Multibus Assignment Policy

This document defines when a CANoe node may require visibility to more than one bus/database in the active SIL configuration.

## 1. Principle

The active CANoe runtime uses:

- domain CAN databases for ECU/runtime CAN messages
- UDP-based Ethernet transport for inter-domain backbone contracts

The key rule is:

- what is required is a **gateway/visibility function**
- not necessarily a separate top-level visible "gateway ECU"

Visible surface nodes remain OEM-style ECU names. Additional bus/database visibility is restored in GUI only where runtime code consumes or publishes messages outside the node's primary domain.

Important distinction:

- **Ethernet runtime placement** is not the same thing as **extra CAN DBC visibility**
- ETH-capable nodes may stay on the `ETH_Backbone` side of the topology without needing any backbone CAN DBC
- multibus assignment is driven by **foreign-domain CAN message visibility**, not by old backbone stub seams

## 2. Why Multibus Exists In This Project

Multibus visibility exists for two reasons:

1. Cross-domain runtime dependencies in SIL
- some nodes consume messages produced in another domain database
- some nodes publish to a foreign-domain CAN database while owning a different primary domain role
- these nodes need extra GUI visibility even if they remain a single visible ECU node

2. Full-system validation harness visibility
- `TEST_SCN` injects and observes a complete cross-domain scenario
- it must see the domain CAN contracts that it drives or checks
- this is a validation architecture need, not an Ethernet transport need

## 3. Node Categories

### 3.1 True multibus anchors

These nodes are expected to see multiple CAN databases as part of their normal runtime role.

| Node | Reason |
| --- | --- |
| `CGW` | cross-domain boundary and fail-safe authority; consumes `frmChassisHealthMsg`, `frmBodyHealthMsg`, and `frmInfotainmentHealthMsg`, so it requires `Chassis`, `Body`, and `Infotainment` CAN visibility in addition to its ETH runtime placement |
| `TEST_SCN` | validation scenario orchestration and full-system signal injection/observation; emits or observes `Powertrain`, `Chassis`, `Body`, `Infotainment`, and `ADAS` domain contracts, so it requires all five domain CAN databases in addition to its ETH runtime placement |

### 3.2 Cross-domain visibility consumers

These nodes remain single visible ECU nodes, but require additional GUI CAN/database visibility because they reference foreign-domain messages.

| Node | Primary domain | Extra CAN visibility | Compile-validated reason |
| --- | --- | --- | --- |
| `PGS` | Infotainment | `ADAS` | consumes `frmParkUltrasonicStateMsg` |
| `AFLS` | Body | `Chassis` | consumes `frmSteeringAngleMsg` |
| `DATC` | Body | `Infotainment` | consumes `frmTmuServiceStateMsg` |
| `ACU` | Chassis | `Body` | consumes `frmSeatBeltStateMsg` |
| `ODS` | Chassis | `Body` | consumes `frmSeatBeltStateMsg`, `frmSeatStateMsg` |
| `SCC` | ADAS | `Powertrain`, `Chassis` | publishes `frmCruiseStateMsg` and consumes `frmVehicleStateCanMsg` |
| `HWP` | ADAS | `Powertrain` | consumes `frmCruiseStateMsg` |
| `VCU` | Chassis | `Powertrain` | consumes `frmIgnitionEngineMsg`, `frmGearStateMsg`, `frmPowertrainGatewayMsg`, and `frmVehicleModeMsg` |

### 3.3 No extra CAN visibility needed for ETH transport alone

The following nodes participate in the real Ethernet backbone through UDP helpers, but should **not** receive extra CAN DBC visibility merely because they publish or consume ETH contracts:

- `MDPS`
- `IVI`
- `ADAS`
- `V2X`
- `IBOX`
- `BCM`
- `CLU`
- `AEB`
- `LDR`
- `EDR`

`VCU` is not a multibus anchor for Ethernet transport, but it still requires `Powertrain` foreign CAN visibility because of its active cross-domain CAN inputs.

If one of these nodes also consumes a foreign-domain CAN frame, add only the specific foreign CAN database that the code actually references.

## 4. Why `TEST_BAS` Stays Single-Bus

`TEST_BAS` is intentionally different from `TEST_SCN`.

### 4.1 What `TEST_BAS` actually does

`TEST_BAS`:

- receives `Test::scenarioResult`
- computes the baseline aggregate result
- writes summarized validation state to `Test::baseScenarioId`, `Test::baseScenarioResult`, `Test::baseFlowCoverageMask`, `Test::baseTraceSnapshotId`, and `Test::baseTestHealth`

This is now a **sysvar-only validation aggregation path**.

Source references:

- [TEST_BAS.can](C:\Users\이준영\CANoe-IVI-OTA\canoe\src\capl\ecu\TEST_BAS.can)
- [project.sysvars](C:\Users\이준영\CANoe-IVI-OTA\canoe\project\sysvars\project.sysvars)

### 4.2 Why this is still "system-wide" validation

`TEST_BAS` is not a raw multi-domain collector.

System-wide information is already condensed before it reaches `TEST_BAS`:

- `TEST_SCN` orchestrates scenario inputs across domains
- runtime ECUs evaluate and publish/reflect state
- `TEST_SCN` updates `Test::scenarioResult`
- `TEST_BAS` only aggregates the final baseline result state

So:

- the **validation meaning** is system-wide
- the **transport dependency** for `TEST_BAS` is intentionally narrow
- the **topology placement** stays on the backbone-side validation seam, not in a product chassis ECU and not inside `CGW`

That is why `TEST_BAS` remains single-bus while `TEST_SCN` remains multibus.

### 4.3 When `TEST_BAS` would need multibus

Only change this if `TEST_BAS` begins to directly consume raw cross-domain CAN messages instead of the current summarized sysvar chain.

Under the current design, widening `TEST_BAS` adds complexity without improving the validation architecture.

## 5. GUI Restore Rule

When rebuilding a fresh `.cfg`:

1. keep one visible node instance per ECU
2. attach the five domain CAN DBCs first
3. place ETH-capable nodes on the Ethernet topology as required by the configuration
4. restore extra CAN visibility only for the nodes listed in this document
5. do not duplicate nodes just to make message names visible

Compile-guided shortcut:

- if `CGW`, `TEST_SCN`, `HWP`, `SCC`, `ACU`, `ODS`, `AFLS`, `DATC`, `PGS`, or `VCU` show `Database missing?` errors, treat that as missing foreign-domain CAN visibility first
- if `TEST_BAS` shows `Test::base*` variable errors, reload `project.sysvars`
- do not reintroduce a retired backbone stub DBC as a workaround for missing foreign CAN visibility

## 6. Current DBC Set For Multibus Assignment

Use these as the primary multibus assignment set:

- `chassis_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `powertrain_can.dbc`
- `adas_can.dbc`

## 7. Design Intent

The active SIL design is intentionally Ethernet-ready at the seam:

- now: `UDP / Ethernet handler`
- local/domain CAN remains for domain-local ECU contracts

The target is to preserve downstream ECU decision logic and use multibus only where foreign-domain CAN visibility is genuinely required.
