# channel_assign

`channel_assign` is the GUI import surface for the active CANoe runtime.

- source of truth for runtime code: `canoe/src/capl/**`
- GUI import mirror: `canoe/cfg/channel_assign/**`
- rule: both trees must stay `1:1` synchronized for active `*.can`

Do not edit files here directly. Edit `canoe/src/capl/**` first, then mirror into this tree.

## Active runtime profile

The absorbed runtime now exposes `16` active CAPL nodes.

| Domain | Folder | Active nodes |
| --- | --- | --- |
| Chassis | `Chassis/` | `CHGW`, `VCU`, `ESC`, `MDPS`, `VAL_BASELINE_CTRL` |
| Body | `Body/` | `BCM` |
| Infotainment | `Infotainment/` | `IVI`, `CLU` |
| Powertrain | `Powertrain/` | `EMS`, `TCU`, `PTGW` |
| ETH Backbone | `ETH_Backbone/` | `CGW`, `ETHM`, `V2X`, `VAL_SCENARIO_CTRL` |
| ADAS | `ADAS/` | `ADAS` |

## GUI import order

1. Open the active CANoe configuration in GUI.
2. For each network, insert CAPL nodes from the matching folder below.
3. Re-apply multibus assignments for anchor nodes.
4. Compile and save from GUI.

| Network | Import folder | Count |
| --- | --- | --- |
| Chassis | `Chassis/` | 5 |
| Body | `Body/` | 1 |
| Infotainment | `Infotainment/` | 2 |
| Powertrain | `Powertrain/` | 3 |
| ETH_Backbone | `ETH_Backbone/` | 4 |
| ADAS | `ADAS/` | 1 |

## Multibus anchors

These anchors still need extra bus assignments restored in GUI.

| Node | Primary folder | Extra bus context to restore in GUI |
| --- | --- | --- |
| `CHGW` | `Chassis/` | chassis + backbone |
| `BCM` | `Body/` | body + backbone |
| `IVI` | `Infotainment/` | infotainment + backbone |
| `PTGW` | `Powertrain/` | powertrain + backbone |
| `CGW` | `ETH_Backbone/` | backbone + cross-domain visibility |
| `VAL_SCENARIO_CTRL` | `ETH_Backbone/` | validation multibus setup |

## Node intent

### Chassis
- `CHGW.can` ? chassis ingress normalization, state synthesis, chassis diag boundary
- `VCU.can` ? propulsion / accel command owner
- `ESC.can` ? brake / stability owner
- `MDPS.can` ? steering owner
- `VAL_BASELINE_CTRL.can` ? validation baseline aggregation

### Body
- `BCM.can` ? body output owner after hazard/window/ambient/driver-state absorption

### Infotainment
- `IVI.can` ? IVI route, navigation, infotainment output owner
- `CLU.can` ? cluster display / HMI owner

### Powertrain
- `EMS.can` ? engine management runtime
- `TCU.can` ? transmission control runtime
- `PTGW.can` ? powertrain gateway / routing policy anchor

### ETH Backbone
- `CGW.can` ? cross-domain boundary, fail-safe, and gateway authority
- `ETHM.can` ? Ethernet path freshness monitor
- `V2X.can` ? V2X emergency input / arbitration ingress
- `VAL_SCENARIO_CTRL.can` ? validation scenario orchestrator

### ADAS
- `ADAS.can` ? integrated risk, warning, and assist decision runtime

## Validation

- `python scripts/gates/text_integrity_gate.py`
- `python scripts/gates/cfg_hygiene_gate.py`

`check_capl_sync.py` still needs the new ECU inventory update outside Dev1 scope.
Local runtime verification result for this rename wave:

- `src/capl` active files: `16`
- `cfg/channel_assign` active files: `16`
- name diff: `0`
- content diff: `0`
