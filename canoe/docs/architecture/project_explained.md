# project_profile.xml 설명

- 위치: `canoe/project/cfg/project_profile.xml`
- 역할: 구조 설명용 XML 메타 파일 (CANoe 실행 파일 아님)
- 경로 기준:
  - DBC(실행): `..\..\network\dbc\{chassis_can|body_can|infotainment_can|powertrain_can|test_can}.dbc`
  - DBC(백업): `..\..\network\dbc\emergency_system.dbc`
  - CAPL: `..\..\src\capl\{input|logic|output|ems}\*.can`
  - SysVar: `..\sysvars\project.sysvars`

실행 기준은 `canoe/project/cfg/CAN_500kBaud_1ch_split.cfg`입니다.
