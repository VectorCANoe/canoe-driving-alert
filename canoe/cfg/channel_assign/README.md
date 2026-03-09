# channel_assign

`channel_assign` is the GUI import surface for the active CANoe runtime and the full OEM breadth runtime bank.

- source of truth for runtime code: `canoe/src/capl/**`
- GUI import mirror: `canoe/cfg/channel_assign/**`
- rule: both trees must stay `1:1` synchronized for active `*.can`

Do not edit files here directly. Edit `canoe/src/capl/**` first, then mirror into this tree.

## Current visible import bank

The current import bank exposes:

- deep runtime anchors: `100`
- shallow placeholder surfaces: `0`
- total visible nodes: `100`

| Domain | Folder | Active nodes |
| --- | --- | --- |
| Chassis | `Chassis/` | `16` |
| Body | `Body/` | `24` |
| Infotainment | `Infotainment/` | `13` |
| Powertrain | `Powertrain/` | `15` |
| ETH Backbone | `ETH_Backbone/` | `8` |
| ADAS | `ADAS/` | `26` |

## Active deep runtime anchors

| Domain | Visible deep nodes |
| --- | --- |
| Chassis | `VCU`, `ESC`, `MDPS`, `ABS`, `EPB`, `TPMS`, `SAS`, `VSM`, `EHB`, `ECS`, `CDC`, `ASM`, `RWS`, `ACU`, `ODS`, `TST_BAS` |
| Body | `BCM`, `DATC`, `SMK`, `AFLS`, `WIP`, `BSEC`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `SEAT_DRV`, `SEAT_PASS`, `TGM`, `MIR`, `RATC`, `SRF`, `HLM`, `CSM`, `AHLS`, `ADM`, `PTG`, `BIO`, `MSC` |
| Infotainment | `IVI`, `CLU`, `HUD`, `AMP`, `VCS`, `TMU`, `NAV`, `OTA`, `DKEY`, `RSE`, `PGS`, `PAK`, `CPAY` |
| Powertrain | `EMS`, `TCU`, `_4WD`, `BAT_BMS`, `FPCM`, `LVR`, `ISG`, `EOP`, `EWP`, `OBC`, `DCDC`, `MCU`, `INVERTER`, `CPC` |
| ETH Backbone | `CGW`, `V2X`, `SGW`, `IBOX`, `DCM`, `EDR`, `ETHB`, `TST_SCN` |
| ADAS | `ADAS`, `SCC`, `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PUS`, `DMS`, `OMS`, `AEB`, `PKM`, `RPC`, `RRM`, `SPM`, `HWP`, `LDR`, `TRM` |

## GUI import order

1. Open the active CANoe configuration in GUI.
2. Import deep runtime anchors first.
3. Import the remaining active nodes by domain as needed.
4. Re-apply multibus assignments for anchor nodes.
5. Compile and save from GUI.

| Network | Import folder | Visible node count |
| --- | --- | --- |
| Chassis | `Chassis/` | `16` |
| Body | `Body/` | `24` |
| Infotainment | `Infotainment/` | `13` |
| Powertrain | `Powertrain/` | `15` |
| ETH_Backbone | `ETH_Backbone/` | `8` |
| ADAS | `ADAS/` | `26` |

## Multibus anchors

These anchors still need extra bus assignments restored in GUI.

| Node | Primary folder | Extra bus context to restore in GUI |
| --- | --- | --- |
| `BCM` | `Body/` | body + backbone |
| `IVI` | `Infotainment/` | infotainment + backbone |
| `CGW` | `ETH_Backbone/` | backbone + cross-domain visibility |
| `TST_SCN` | `ETH_Backbone/` | validation multibus setup |

## Node intent

### Chassis
- `VCU.can` ? propulsion / accel command owner
- `ESC.can` ? brake / stability owner
- `MDPS.can` ? steering owner
- `ABS.can`, `EPB.can`, `TPMS.can`, `SAS.can`, `VSM.can`, `EHB.can`, `ECS.can`, `CDC.can`, `ASM.can`, `RWS.can` ? chassis/safety runtime anchors
- `TST_BAS.can` ? validation baseline aggregation

### Body
- `BCM.can` ? body output owner after hazard/window/ambient/driver-state absorption
- `DATC.can`, `SMK.can`, `AFLS.can`, `WIP.can`, `BSEC.can`, `DOOR_FL.can`, `DOOR_FR.can`, `DOOR_RL.can`, `DOOR_RR.can`, `SEAT_DRV.can`, `SEAT_PASS.can`, `TGM.can`, `MIR.can`, `RATC.can`, `SRF.can`, `HLM.can`, `CSM.can`, `AHLS.can`, `ADM.can`, `PTG.can`, `BIO.can` ? comfort/security runtime anchors

### Infotainment
- `IVI.can` ? IVI display/connectivity/diagnostic owner after navigation owner split
- `NAV.can`, `OTA.can`, `DKEY.can`, `RSE.can`, `PGS.can`, `PAK.can`, `CPAY.can` ? infotainment service/runtime anchors
- `CLU.can` ? cluster display / HMI owner
- `HUD.can`, `AMP.can`, `VCS.can`, `TMU.can` ? HMI/connectivity runtime anchors

### Powertrain
- `EMS.can` ? engine management runtime
- `TCU.can` ? transmission control runtime
- `_4WD.can`, `BAT_BMS.can`, `FPCM.can`, `LVR.can`, `ISG.can`, `EOP.can`, `EWP.can`, `OBC.can`, `DCDC.can`, `MCU.can`, `INVERTER.can`, `CPC.can` ? driveline and power electronics runtime anchors

### ETH Backbone
- `CGW.can` ? cross-domain boundary, fail-safe, and gateway authority
- `V2X.can` ? V2X emergency input / arbitration ingress
- `SGW.can`, `IBOX.can`, `DCM.can`, `EDR.can`, `ETHB.can` ? security/infra/connectivity anchors
- `TST_SCN.can` ? validation scenario orchestrator

### ADAS
- `ADAS.can` ? integrated risk, warning, and assist decision runtime
- `SCC.can`, `LDWS_LKAS.can`, `FCA.can`, `BCW.can`, `LCA.can`, `SPAS.can`, `RSPA.can`, `AVM.can`, `FCAM.can`, `FRADAR.can`, `SRR_FL.can`, `SRR_FR.can`, `SRR_RL.can`, `SRR_RR.can`, `PUS.can`, `DMS.can`, `OMS.can`, `AEB.can`, `PKM.can`, `RPC.can`, `RRM.can`, `SPM.can`, `HWP.can`, `LDR.can`, `TRM.can` ? ADAS feature/sensor/runtime anchors

## Placeholder note

The original placeholder bank is fully promoted. Placeholder source files remain only under `retired_placeholders/` for history.

## Validation

- `python scripts/gates/text_integrity_gate.py`
- `python scripts/gates/cfg_hygiene_gate.py`

`check_capl_sync.py` still needs the new ECU inventory update outside Dev1 scope.
Local runtime verification result for the current visible bank:

- `src/capl` visible files: `100`
- `cfg/channel_assign` visible files: `100`
- name diff: `0`
- content diff: `0`

