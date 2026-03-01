# CANoe (A안) 프로젝트 가이드

본 폴더는 문서(`driving-situation-alert`)와 분리된 구현 전용 영역입니다.

## 실행 기준
- CANoe 실행 cfg(활성): `cfg/CAN_500kBaud_1ch_split.cfg`
- CANoe 실행 cfg(레거시 백업): `cfg/legacy/LEGACY_CAN_500kBaud_1ch.cfg`
- 시스템 변수: `project/sysvars/project.sysvars`
- CAN DB(활성): `databases/{chassis_can, powertrain_can, body_can, infotainment_can, test_can}.dbc`
- CAN DB(레거시 백업): `databases/legacy/LEGACY_emergency_system.dbc`
- 빠른 파일 찾기: `FILE_INDEX.md`

## 소스 구조 (BP)
```text
canoe/
  project/
    cfg/
    sysvars/
    panel/
  network/
    dbc/
  src/
    capl/
      input/
      logic/
      output/
      ems/
  tests/
    scenarios/
    modules/
  docs/
    architecture/
    operations/
  legacy/
    nodes/
```

## 활성 CAPL 노드 (26)
- input: `SIL_TEST_CTRL`, `CHASSIS_GW`, `INFOTAINMENT_GW`
- logic: `NAV_CONTEXT_MGR`, `ADAS_WARN_CTRL`, `EMS_ALERT_RX`, `WARN_ARB_MGR`
- output: `BODY_GW`, `IVI_GW`, `BCM_AMBIENT_CTRL`, `CLU_HMI_CTRL`
- ems: `EMS_POLICE_TX`, `EMS_AMB_TX`
- ecu/network: `ACCEL_CTRL`, `BRAKE_CTRL`, `STEERING_CTRL`, `ENGINE_CTRL`, `TRANSMISSION_CTRL`, `WINDOW_CTRL`, `HAZARD_CTRL`, `DRIVER_STATE_CTRL`, `CLUSTER_BASE_CTRL`, `DOMAIN_GW_ROUTER`, `DOMAIN_BOUNDARY_MGR`, `VEHICLE_BASE_TEST_CTRL`, `ETH_SWITCH`
- 역할 메모: `DOMAIN_BOUNDARY_MGR`는 Health/Boundary 프레임을 수신만 하는 Rx-only 모니터링 노드(Tx 없음)

## 운영 원칙
- `00~07` 문서는 참고/검증 기준이며 구현 수정은 `canoe/`에서만 수행
- 검증 범위는 CANoe SIL, CAN + Ethernet
- busy 충돌 대응 절차는 `canoe/AGENTS.md` 준수
