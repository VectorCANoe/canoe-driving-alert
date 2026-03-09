# Multibus Assignment Policy

This document defines when a CANoe node may require visibility to more than one bus/database in the active SIL configuration.

## 1. Principle

The active CANoe runtime uses:

- domain CAN databases for primary ECU/runtime messages
- `eth_backbone_can_stub.dbc` as the current CAN-stub transport seam for the future Ethernet backbone

The key rule is:

- what is required is a **gateway/visibility function**
- not necessarily a separate top-level visible "gateway ECU"

Visible surface nodes remain OEM-style ECU names. Additional bus/database visibility is restored in GUI only where runtime code consumes or publishes messages outside the node's primary domain.

## 2. Why Multibus Exists In This Project

Multibus visibility exists for two reasons:

1. Future Ethernet cutover preparation
- today: CAN-stub messages are used on the backbone seam
- later: the seam should be replaced by real Ethernet transport/binding
- goal: downstream ECU logic should remain unchanged
- only the transport-facing handler/binding should change

2. Cross-domain runtime dependencies in SIL
- some nodes consume messages produced in another domain database
- some nodes publish to the backbone stub while owning a primary domain role
- these nodes need extra GUI visibility even if they remain a single visible ECU node

## 3. Node Categories

### 3.1 True multibus anchors

These nodes are expected to see multiple buses as part of their normal runtime role.

| Node | Reason |
| --- | --- |
| `CGW` | cross-domain boundary, fail-safe authority, backbone seam supervision |
| `TST_SCN` | validation scenario orchestration and full-system signal injection/observation |

### 3.2 Cross-domain visibility consumers

These nodes remain single visible ECU nodes, but require additional GUI bus/database visibility because they reference foreign-domain or backbone messages.

| Node | Primary domain | Extra visibility |
| --- | --- | --- |
| `IVI` | Infotainment | ETH backbone |
| `PGS` | Infotainment | ADAS |
| `AFLS` | Body | Chassis |
| `DATC` | Body | Infotainment |
| `ACU` | Chassis | Body |
| `ODS` | Chassis | Body |
| `VCU` | Chassis-facing runtime node | Powertrain, ETH backbone |
| `MDPS` | Chassis | ETH backbone |
| `SCC` | ADAS | Chassis |
| `AEB` | ADAS | ETH backbone |
| `HWP` | ADAS | Powertrain |
| `LDR` | ADAS | ETH backbone |

## 4. Why `TST_BAS` Stays Single-Bus

`TST_BAS` is intentionally different from `TST_SCN`.

### 4.1 What `TST_BAS` actually does

`TST_BAS`:

- receives `frmTestResultMsg (0x2A5)`
- computes the baseline aggregate result
- transmits `frmBaseTestResultMsg (0x2A6)`

Both messages live in `chassis_can.dbc`.

Source references:

- [TST_BAS.can](C:\Users\이준영\CANoe-IVI-OTA\canoe\src\capl\ecu\TST_BAS.can)
- [chassis_can.dbc](C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\chassis_can.dbc)

### 4.2 Why this is still "system-wide" validation

`TST_BAS` is not a raw multi-domain collector.

System-wide information is already condensed before it reaches `TST_BAS`:

- `TST_SCN` orchestrates scenario inputs across domains
- runtime ECUs evaluate and publish/reflect state
- `TST_SCN` emits `frmTestResultMsg`
- `TST_BAS` only aggregates the final baseline result frame

So:

- the **validation meaning** is system-wide
- the **transport boundary** for `TST_BAS` is intentionally narrow

That is why `TST_BAS` remains single-bus while `TST_SCN` remains multibus.

### 4.3 When `TST_BAS` would need multibus

Only change this if `TST_BAS` begins to directly consume raw cross-domain messages instead of the current summarized result chain.

Under the current design, widening `TST_BAS` adds complexity without improving the validation architecture.

## 5. GUI Restore Rule

When rebuilding a fresh `.cfg`:

1. keep one visible node instance per ECU
2. re-attach the six current DBCs
3. restore multibus/extra visibility only for the nodes listed in this document
4. do not duplicate nodes just to make message names visible

## 6. Current DBC Set

- `chassis_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `powertrain_can.dbc`
- `adas_can.dbc`
- `eth_backbone_can_stub.dbc`

## 7. Design Intent

The active SIL design is intentionally Ethernet-ready at the seam:

- today: `CAN-stub handler`
- later: `UDP / Ethernet handler`

The target is to preserve downstream ECU decision logic and replace only transport-facing binding/handler code.
