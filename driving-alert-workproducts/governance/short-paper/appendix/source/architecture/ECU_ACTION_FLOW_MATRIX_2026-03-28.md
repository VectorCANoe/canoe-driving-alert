# ECU Action Flow Matrix (2026-03-28)

Subtitle: ECU-to-flow lookup across the full runtime surface.

Use this matrix to find the primary action flow for one ECU and to see its supporting flow family.

| ECU | Domain | Group | Primary action flow | Supporting action flows |
| --- | --- | --- | --- | --- |
| `ABS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_02` | FLOW_05 |
| `ACU` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `ASM` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `CDC` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `ECS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `EHB` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_02` | FLOW_05<br>FLOW_07 |
| `EPB` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_02` | FLOW_05 |
| `ESC` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_01` | FLOW_02<br>FLOW_05<br>FLOW_07 |
| `MDPS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_01` | FLOW_05 |
| `ODS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `RWS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_01` | FLOW_05 |
| `SAS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_01` | FLOW_05 |
| `TPMS` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_05` | - |
| `VCU` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_02` | FLOW_03<br>FLOW_04<br>FLOW_05 |
| `VSM` | `Chassis` | `Group 01 Base Vehicle Dynamics` | `FLOW_02` | FLOW_05<br>FLOW_07 |
| `BAT_BMS` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `CPC` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `DCDC` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `EMS` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | FLOW_04 |
| `EOP` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `EWP` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `FPCM` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `INVERTER` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `ISG` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `LVR` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `MCU` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `OBC` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `TCU` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | FLOW_04 |
| `_4WD` | `Powertrain` | `Group 01 Base Vehicle Dynamics` | `FLOW_03` | - |
| `ADAS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_07<br>FLOW_08<br>FLOW_09 |
| `AEB` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_07<br>FLOW_02 |
| `AVM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `BCW` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `DMS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_10 |
| `FCA` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_07<br>FLOW_02 |
| `FCAM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | - |
| `FRADAR` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | - |
| `HWP` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | - |
| `LCA` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `LDR` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | - |
| `LDWS_LKAS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `OMS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_10 |
| `PKM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `PUS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `RPC` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `RRM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `RSPA` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `SCC` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_07<br>FLOW_04 |
| `SPAS` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `SPM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_09 |
| `SRR_FL` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `SRR_FR` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `SRR_RL` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `SRR_RR` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | FLOW_08 |
| `TRM` | `ADAS` | `Group 02 ADAS AEB Brake Assist` | `FLOW_06` | - |
| `AMP` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_12 |
| `CLU` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_01 |
| `CPAY` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_15` | - |
| `DKEY` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_15` | FLOW_17 |
| `HUD` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_12 |
| `IVI` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_15 |
| `NAV` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_15 |
| `OTA` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_15` | - |
| `PAK` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_15` | FLOW_17 |
| `PGS` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_15` | FLOW_17 |
| `RSE` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_15 |
| `TMU` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_15 |
| `VCS` | `Infotainment` | `Group 03 Display Warning Audio` | `FLOW_11` | FLOW_13<br>FLOW_14<br>FLOW_15 |
| `ADM` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `AFLS` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `AHLS` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `BCM` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | FLOW_17<br>FLOW_18 |
| `BIO` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `BSEC` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `CSM` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `DATC` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_18` | - |
| `DOOR_FL` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `DOOR_FR` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `DOOR_RL` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `DOOR_RR` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `HLM` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `MIR` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `MSC` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `PTG` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `RATC` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_18` | - |
| `SEAT_DRV` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_18` | - |
| `SEAT_PASS` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_18` | - |
| `SMK` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_17` | - |
| `SRF` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `TGM` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `WIP` | `Body` | `Group 04 Body Comfort Ambient` | `FLOW_16` | - |
| `TEST_BAS` | `ETH_Backbone` | `Group 05 Validation Scenario` | `FLOW_19` | FLOW_20 |
| `TEST_SCN` | `ETH_Backbone` | `Group 05 Validation Scenario` | `FLOW_19` | FLOW_20 |
| `CGW` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | FLOW_12<br>FLOW_13<br>FLOW_01 |
| `DCM` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | - |
| `EDR` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | - |
| `ETHB` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | FLOW_12 |
| `EXT_DIAG` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | - |
| `IBOX` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | - |
| `SGW` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | - |
| `V2X` | `ETH_Backbone` | `Group 06 Backbone Gateway Diagnostics` | `FLOW_20` | FLOW_12<br>FLOW_13 |
