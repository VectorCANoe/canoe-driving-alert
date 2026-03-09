# ECU Parallel Execution Strategy (2026-03-09)

## Decision

The program should not wait until the very end to validate everything once.

Use this execution model instead:

1. Keep one final full-vehicle verification pass at the end.
2. Run compile/smoke/integration verification at each domain wave.
3. Split Dev1 implementation by domain-owned active ECU groups, not by `active vs placeholder`.
4. Let Docs handle placeholder breadth as a later documentation batch after active runtime ownership is stable.

## Why `final-only verification` is wrong

If all ECU additions are implemented first and verified only once at the end:

- contract drift is discovered too late
- DBC owner mistakes pile up
- shared SysVar/backbone seams become hard to isolate
- CGW / V2X / ADAS regressions become mixed together
- Dev2 automation has no stable intermediate baseline

Final verification is still required, but only as the last gate after wave-level verification.

## Split Principle

### Use domain-first split for active runtime work

This is the correct split for Dev1 because active ECUs share:

- domain-local messages
- shared backbone stub contracts
- owner/state mirrors
- transport seam logic

### Do not use `active vs placeholder` as the main split

That split is weak for implementation because it mixes unrelated domains into one batch.

Use it only for planning status:

- `Active`: implemented now
- `Placeholder`: present in vehicle surface, shallow/no runtime
- `Deferred`: future candidate

## Recommended Wave Structure

### Wave A: Core Motion + Powertrain + Central Boundary

Primary ECUs:

- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `CGW`

Focus:

- vehicle state ownership
- powertrain/chassis source signals
- central boundary/fail-safe contract
- backbone state publishing seam

### Wave B: Body + HMI

Primary ECUs:

- `BCM`
- `IVI`
- `CLU`

Focus:

- body outputs
- cluster/HMI presentation
- navigation context publishing seam
- user-visible warning synchronization

### Wave C: Feature ECUs

Primary ECUs:

- `ADAS`
- `V2X`

Focus:

- risk/arbitration
- emergency broadcast path
- alert selection
- object-risk path

### Wave D: Validation Harness

Primary runtime:

- `TST_SCN`
- `TST_BAS`

Focus:

- native CANoe Test Unit compatibility
- Dev2 external runner compatibility
- scenario/result/evidence contract stability

### Wave E: Placeholder Breadth Expansion

Examples:

- `HVAC`
- `TMU`
- `IBOX`
- `HUD`
- `EPB`
- `TPMS`
- `ACU`
- `ODS`
- `SCC`
- `FCA`
- `AVM`

Rule:

- add only shallow placeholder/runtime shell unless a real owner path is needed now
- do not let placeholder breadth block active ECU stabilization

## Team Split

### Dev1

Owns:

- `canoe/`

Does:

- active ECU runtime changes
- backbone seam stabilization
- native CANoe test compatibility
- wave-level compile/smoke verification

### Dev2

Owns:

- `scripts/`
- `product/sdv_operator/`

Does:

- operator/CLI/TUI
- external execution flow
- evidence packaging
- CI/Jenkins bridge

### Docs

Owns:

- `driving-situation-alert/`

Does:

- SoT propagation after Dev1 wave baselines are frozen
- placeholder breadth batch documentation
- final 04/05/06/07 closeout

## Verification Cadence

For every wave:

1. runtime code change
2. source/mirror sync
3. CAPL compile
4. quick smoke scenario
5. interface sanity check

Only after all waves:

6. full-vehicle verification
7. final evidence package

## Immediate Recommendation

Use this order now:

1. Wave D first enough to stabilize harness contract
2. Wave A next
3. Wave B next
4. Wave C next
5. Wave E only after A/B/C are stable

This keeps downstream ECU logic stable while the future Ethernet seam remains swappable at the transport boundary only.
