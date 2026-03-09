# channel_assign

`channel_assign` is the GUI import surface for the active CANoe runtime and OEM breadth placeholder bank.

- source of truth for runtime code: `canoe/src/capl/**`
- GUI import mirror: `canoe/cfg/channel_assign/**`
- rule: both trees must stay `1:1` synchronized for active `*.can`

Do not edit files here directly. Edit `canoe/src/capl/**` first, then mirror into this tree.

## Current visible import bank

The current import bank exposes:

- deep runtime anchors: `74`
- shallow placeholder surfaces: `26`
- total visible nodes: `100`

| Domain | Folder | Active nodes |
| --- | --- | --- |
| Chassis | `Chassis/` | `16` |
| Body | `Body/` | `23` |
| Infotainment | `Infotainment/` | `13` |
| Powertrain | `Powertrain/` | `14` |
| ETH Backbone | `ETH_Backbone/` | `8` |
| ADAS | `ADAS/` | `26` |

## Active deep runtime anchors

| Domain | Visible deep nodes |
| --- | --- |
| Chassis | `VCU`, `ESC`, `MDPS`, `ABS`, `EPB`, `TPMS`, `SAS`, `VSM`, `EHB`, `ECS`, `CDC`, `VAL_BASELINE_CTRL` |
| Body | `BCM`, `DATC`, `SMK`, `AFLS`, `WIPER_MODULE`, `BODY_SECURITY_MODULE`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `SEAT_DRV`, `SEAT_PASS`, `TAILGATE_MODULE`, `MIRROR_MODULE`, `REAR_CLIMATE_MODULE`, `SUNROOF_MODULE`, `HEADLAMP_LEVELING`, `CABIN_SENSING`, `AHLS`, `AUTO_DOOR_CTRL`, `POWER_TAILGATE_CTRL`, `BIOMETRIC_AUTH` |
| Infotainment | `IVI`, `CLU`, `HUD`, `AMP`, `VOICE_ASSIST`, `TMU`, `NAV_MODULE`, `OTA_MASTER`, `DIGITAL_KEY`, `RSE` |
| Powertrain | `EMS`, `TCU`, `OBC`, `DCDC`, `MCU`, `INVERTER` |
| ETH Backbone | `CGW`, `V2X`, `SGW`, `IBOX`, `DCM`, `VAL_SCENARIO_CTRL` |
| ADAS | `ADAS`, `SCC`, `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PARK_ULTRASONIC`, `DMS`, `OMS` |

## GUI import order

1. Open the active CANoe configuration in GUI.
2. Import deep runtime anchors first.
3. Import placeholder surface nodes by domain as needed.
4. Re-apply multibus assignments for anchor nodes.
5. Compile and save from GUI.

| Network | Import folder | Visible node count |
| --- | --- | --- |
| Chassis | `Chassis/` | `16` |
| Body | `Body/` | `23` |
| Infotainment | `Infotainment/` | `13` |
| Powertrain | `Powertrain/` | `14` |
| ETH_Backbone | `ETH_Backbone/` | `8` |
| ADAS | `ADAS/` | `26` |

## Multibus anchors

These anchors still need extra bus assignments restored in GUI.

| Node | Primary folder | Extra bus context to restore in GUI |
| --- | --- | --- |
| `BCM` | `Body/` | body + backbone |
| `IVI` | `Infotainment/` | infotainment + backbone |
| `CGW` | `ETH_Backbone/` | backbone + cross-domain visibility |
| `VAL_SCENARIO_CTRL` | `ETH_Backbone/` | validation multibus setup |

## Node intent

### Chassis
- `VCU.can` ? propulsion / accel command owner
- `ESC.can` ? brake / stability owner
- `MDPS.can` ? steering owner
- `ABS.can`, `EPB.can`, `TPMS.can`, `SAS.can`, `VSM.can`, `EHB.can`, `ECS.can`, `CDC.can` ? chassis/safety runtime anchors
- `VAL_BASELINE_CTRL.can` ? validation baseline aggregation

### Body
- `BCM.can` ? body output owner after hazard/window/ambient/driver-state absorption
- `DATC.can`, `SMK.can`, `AFLS.can`, `WIPER_MODULE.can`, `BODY_SECURITY_MODULE.can`, `DOOR_FL.can`, `DOOR_FR.can`, `DOOR_RL.can`, `DOOR_RR.can`, `SEAT_DRV.can`, `SEAT_PASS.can`, `TAILGATE_MODULE.can`, `MIRROR_MODULE.can`, `REAR_CLIMATE_MODULE.can`, `SUNROOF_MODULE.can`, `HEADLAMP_LEVELING.can`, `CABIN_SENSING.can`, `AHLS.can`, `AUTO_DOOR_CTRL.can`, `POWER_TAILGATE_CTRL.can`, `BIOMETRIC_AUTH.can` ? comfort/security runtime anchors

### Infotainment
- `IVI.can` ? IVI display/connectivity/diagnostic owner after navigation owner split
- `NAV_MODULE.can`, `OTA_MASTER.can`, `DIGITAL_KEY.can`, `RSE.can` ? infotainment service/runtime anchors
- `CLU.can` ? cluster display / HMI owner
- `HUD.can`, `AMP.can`, `VOICE_ASSIST.can`, `TMU.can` ? HMI/connectivity runtime anchors

### Powertrain
- `EMS.can` ? engine management runtime
- `TCU.can` ? transmission control runtime
- `OBC.can`, `DCDC.can`, `MCU.can`, `INVERTER.can` ? power electronics runtime anchors

### ETH Backbone
- `CGW.can` ? cross-domain boundary, fail-safe, and gateway authority
- `V2X.can` ? V2X emergency input / arbitration ingress
- `SGW.can`, `IBOX.can`, `DCM.can` ? security/infra/connectivity anchors
- `VAL_SCENARIO_CTRL.can` ? validation scenario orchestrator

### ADAS
- `ADAS.can` ? integrated risk, warning, and assist decision runtime
- `SCC.can`, `LDWS_LKAS.can`, `FCA.can`, `BCW.can`, `LCA.can`, `SPAS.can`, `RSPA.can`, `AVM.can`, `FCAM.can`, `FRADAR.can`, `SRR_FL.can`, `SRR_FR.can`, `SRR_RL.can`, `SRR_RR.can`, `PARK_ULTRASONIC.can`, `DMS.can`, `OMS.can` ? ADAS feature/sensor runtime anchors

## Placeholder note

Placeholder nodes are OEM surface breadth only. They do not carry deep runtime logic in this wave.

## Validation

- `python scripts/gates/text_integrity_gate.py`
- `python scripts/gates/cfg_hygiene_gate.py`

`check_capl_sync.py` still needs the new ECU inventory update outside Dev1 scope.
Local runtime verification result for the current visible bank:

- `src/capl` visible files: `100`
- `cfg/channel_assign` visible files: `100`
- name diff: `0`
- content diff: `0`
