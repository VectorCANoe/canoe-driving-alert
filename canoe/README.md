# CANoe (A안) 프로젝트 가이드

본 폴더는 문서(`driving-situation-alert`)와 분리된 구현 전용 영역입니다.

## 실행 기준
- CANoe 실행 cfg(활성): `cfg/CAN_v2_topology_wip.cfg`
- CANoe 실행 cfg(v1 레거시): `cfg/v1_cfg/CAN_500kBaud_1ch.cfg`
- 시스템 변수: `project/sysvars/project.sysvars`
- CAN DB(활성): `databases/{chassis_can, powertrain_can, body_can, infotainment_can, adas_can, eth_backbone_can_stub}.dbc`
- CAN DB(v1 레거시): `databases/v1_legacy/v1_split_345bdb4/emergency_system.dbc`
- 빠른 파일 찾기: `FILE_INDEX.md`

## 아키텍처 메모
- v2 운영은 도메인 분리 구조 + `channel_assign` 기반 런타임을 사용합니다.
- v1은 단일 버스 flat 구조 기반의 빠른 병렬 개발용 아키텍처였습니다.

## 소스 구조 (BP)
```text
canoe/
  cfg/
    channel_assign/
    v1_cfg/
  project/
    sysvars/
    panel/
  databases/
    v1_legacy/
  src/
    capl/
      ecu/
      ems/
      input/
      logic/
      network/
      output/
      v1_legacy/
  docs/
    architecture/
    operations/
```

## 활성 CAPL 노드 (26)
- input: `VAL_SCENARIO_CTRL`, `CHS_GW`, `INFOTAINMENT_GW`
- logic: `NAV_CTX_MGR`, `ADAS_WARN_CTRL`, `EMS_ALERT_RX`, `WARN_ARB_MGR`
- output: `BODY_GW`, `IVI_GW`, `AMBIENT_CTRL`, `CLU_HMI_CTRL`
- ems: `EMS_POLICE_TX`, `EMS_AMB_TX`
- ecu/network: `ACCEL_CTRL`, `BRK_CTRL`, `STEER_CTRL`, `ENG_CTRL`, `TCM`, `WINDOW_CTRL`, `HAZARD_CTRL`, `DRV_STATE_MGR`, `CLU_BASE_CTRL`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR`, `VAL_BASELINE_CTRL`, `ETH_SW`

## 운영 원칙
- `00~07` 문서는 참고/검증 기준이며 구현 수정은 `canoe/`에서만 수행
- 검증 범위는 CANoe SIL, CAN + Ethernet
- busy 충돌 대응 절차는 `canoe/AGENTS.md` 준수
