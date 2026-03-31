# ECU Action Flow Matrix (2026-03-28)

Subtitle: compact ECU-to-flow summary for appendix layout.

Use this appendix note to find the representative action-flow family per ECU group.
The full row-level matrix is maintained in the ECU metadata book and architecture source package.

## Group summary

- `Group 01 Base Vehicle Dynamics`
  - domains: `Chassis`, `Powertrain`
  - representative primary flows: `FLOW_01`, `FLOW_02`, `FLOW_03`, `FLOW_05`
  - representative ECU set: `ESC`, `MDPS`, `VCU`, `EMS`, `TCU`, `BAT_BMS`
  - supporting flows: `FLOW_04`, `FLOW_07`
- `Group 02 ADAS AEB Brake Assist`
  - domain: `ADAS`
  - representative primary flow: `FLOW_06`
  - representative ECU set: `ADAS`, `AEB`, `FCA`, `SCC`, `BCW`, `LCA`, `LDWS_LKAS`, `AVM`, `DMS`, `OMS`
  - supporting flows: `FLOW_02`, `FLOW_07`, `FLOW_08`, `FLOW_09`, `FLOW_10`
- `Group 03 Display Warning Audio`
  - domain: `Infotainment`
  - representative primary flows: `FLOW_11`, `FLOW_15`
  - representative ECU set: `IVI`, `CLU`, `HUD`, `AMP`, `TMU`, `VCS`, `NAV`
  - supporting flows: `FLOW_01`, `FLOW_12`, `FLOW_13`, `FLOW_14`, `FLOW_17`
- `Group 04 Body Comfort Ambient`
  - domain: `Body`
  - representative primary flows: `FLOW_16`, `FLOW_17`, `FLOW_18`
  - representative ECU set: `BCM`, `DATC`, `AFLS`, `AHLS`, `DOOR_FL/FR/RL/RR`, `SEAT_DRV`, `SEAT_PASS`
  - supporting flows: local comfort and ambient auxiliary routes
- `Group 05 Validation Scenario`
  - domain: `ETH_Backbone`
  - representative primary flow: `FLOW_19`
  - representative ECU set: `TEST_SCN`, `TEST_BAS`
  - supporting flows: `FLOW_20`
- `Group 06 Backbone Gateway Diagnostics`
  - domain: `ETH_Backbone`
  - representative primary flow: `FLOW_20`
  - representative ECU set: `CGW`, `DCM`, `ETHB`, `EXT_DIAG`, `IBOX`, `SGW`, `V2X`
  - supporting flows: `FLOW_01`, `FLOW_12`, `FLOW_13`

## Reading rule

- exact ECU row lookup는 ECU metadata book을 우선 사용합니다.
- appendix에서는 그룹별 대표 흐름과 supporting flow family만 유지합니다.
- owner-route, communication contract, ECU book을 함께 읽으면 row-level contract를 복원할 수 있습니다.
