# Vehicle ECU Refactor Options (2026-03-08)

## Decision Questions

1. Should the current mixed-network architecture stay?
2. How should the project define production-style ECUs?
3. How wide should the full-vehicle scope become without destroying readability and maintenance cost?

## External Reference Summary

### What public references consistently show

- Modern vehicle software is usually presented as a mixed-network system:
  - Ethernet backbone / gateway layer
  - CAN domain networks for many body, chassis, and powertrain signals
- Public-facing ECU names are usually short and function-oriented:
  - `BCM`, `CGW`, `HVAC`, `IVI`, `Cluster`, `TCU`, `ESP/EPS`, `EMS/ECM`
- Internal implementation is still modular:
  - controller, manager, tx/rx, gateway, service, monitor

### What public OSS does not usually provide

- OEM-grade full production vehicle application partitioning is rarely open-sourced.
- Public OSS usually shows one of these instead:
  - AUTOSAR/basic software stacks
  - open vehicle control projects
  - demo vehicle network architectures

## Option A - Keep Current Architecture, Rename Surface Only

### Structure
- Keep `ETH_SW + domain GW + domain CAN + warning core`
- Keep runtime module split mostly as-is
- Introduce logical ECU surface grouping only

### Pros
- Lowest implementation risk
- Reuses current CAPL and DBC heavily
- Fastest path to a production-looking surface

### Cons
- Runtime structure remains more implementation-driven than production ECU modeling
- Some project complexity remains visible under the surface

### Verdict
- Good short-term stabilization option
- Not enough if the goal is a true architecture reset

## Option B - Keep Mixed-Network Backbone, Rebuild ECU Model Around Logical Production ECUs

### Structure
- Keep the current mixed network principle:
  - Ethernet backbone
  - CAN domain buses
  - gateways between domains and backbone
- Redefine the project around logical ECUs first
- Map current runtime modules behind those logical ECUs

### Logical ECU target set
- `CGW/BACKBONE`
- `EMS/V2X`
- `ADAS_FUSION`
- `NAV/IVI`
- `CLUSTER`
- `BCM/BODY`
- `HVAC`
- `CHASSIS`
- `POWERTRAIN`
- `VALIDATION` (non-production)

### Pros
- Best balance of production readability and implementation realism
- Preserves existing technical value
- Makes GUI, docs, and presentation easier to understand
- Supports later Ethernet cutover cleanly

### Cons
- Requires document reset across `00e/0301/0302/0303/0304/04`
- Requires a surface-to-runtime mapping table and possibly GUI regrouping

### Verdict
- Recommended

## Option C - Rebuild Toward a Very Wide Vehicle Topology With 50 Deep Runtime ECUs

### Structure
- Make the project look like a full vehicle with many individual ECUs all implemented in CAPL

### Pros
- Looks large on paper
- Can resemble a full vehicle inventory

### Cons
- High maintenance cost
- Low signal-to-noise ratio
- Weakens focus on the actual project value
- Production projects do not custom-develop 50 ECUs deeply inside one student-scale integration project

### Verdict
- Not recommended

## Recommended Scope Model

### 1. Full vehicle surface inventory
- Show a wide vehicle topology with about `20~30` logical ECUs
- This is enough to look like a vehicle project rather than a feature demo

### 2. Active implemented ECUs
- Keep about `10~15` CAPL runtime nodes with meaningful behavior
- These should cover:
  - domain gateways
  - warning core / fusion
  - body/cluster output ownership
  - baseline vehicle functions
  - validation harness

### 3. Project-specific new feature ECUs
- Keep about `5~8` high-value logical ECUs where the project's real differentiation lives
- Recommended candidates:
  - `EMS/V2X`
  - `ADAS_FUSION`
  - `WARN_ARB`
  - `NAV/IVI`
  - `BCM_AMBIENT`
  - `CLUSTER_HMI`

### 4. Native test assets
- Keep `3~6` scenario-level tests
- Good categories:
  - baseline vehicle state
  - school-zone overspeed
  - emergency vehicle priority
  - fail-safe downgrade
  - cluster/ambient consistency

## Architecture Recommendation

### Keep
- Ethernet backbone concept
- Domain CAN buses
- Gateway boundaries
- Validation harness separation

### Refactor
- Replace implementation-first naming with logical ECU surface naming
- Reduce direct visibility of `_TX/_RX/_MGR/_CTRL` at the project surface
- Rebuild `0301/0302/0303/0304/04` on the new logical ECU model

### Do not do
- Do not implement 50 deep ECUs just to increase count
- Do not merge runtime modules blindly just to make names short
- Do not destroy the existing ownership/debug traceability structure

## Final Recommendation

- Choose **Option B**.
- Present the project as a full vehicle architecture with `20~30` logical ECUs.
- Keep only `10~15` active implemented runtime modules.
- Keep the project-specific differentiation in `5~8` logical feature ECUs.
- Use tests to tell the story, not raw ECU count.

## Immediate Next Step

1. Produce the target logical ECU inventory.
2. Map current runtime nodes to that inventory.
3. Decide which nodes become production-style GUI surface names.
4. Then rewrite `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04` in that order.
