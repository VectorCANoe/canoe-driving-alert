# project_profile.xml Description

- Location: `canoe/cfg/project_profile.xml`
- Role: metadata for structure explanation (not a runnable CANoe config)

## Path Baseline
- Runtime split DBC set: `..\databases\{chassis_can|body_can|infotainment_can|powertrain_can|test_can|eth_backbone_can_stub}.dbc`
- V1 legacy backup DBC: `..\databases\v1_legacy\v1_split_345bdb4\emergency_system.dbc`
- CAPL mirror source: `..\src\capl\{input|logic|output|ems|ecu|network}\*.can`
- System variables: `..\project\sysvars\project.sysvars`

## Runtime Profile
- Active runtime config: `canoe/cfg/CAN_v2_topology_wip.cfg`
- V1 legacy backup config: `canoe/cfg/v1_cfg/CAN_500kBaud_1ch.cfg`

## Note
- V1 was a single-bus flat architecture used for fast parallel development.
- V2 is domain-separated and uses `canoe/cfg/channel_assign/**` as runtime CAPL SoT.
