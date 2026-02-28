# CANoe (A안) 프로젝트 가이드

본 폴더는 문서(`driving-situation-alert`)와 분리된 구현 전용 영역입니다.

## 실행 기준
- CANoe 실행 cfg: `cfg/CAN_500kBaud_1ch.cfg`
- 시스템 변수: `project/sysvars/project.sysvars`
- CAN DB: `databases/emergency_system.dbc`
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

## 활성 CAPL 노드 (13)
- input: `SIL_TEST_CTRL`, `CHASSIS_GW`, `INFOTAINMENT_GW`
- logic: `NAV_CONTEXT_MGR`, `ADAS_WARN_CTRL`, `EMS_ALERT_RX`, `WARN_ARB_MGR`
- output: `BODY_GW`, `IVI_GW`, `BCM_AMBIENT_CTRL`, `CLU_HMI_CTRL`
- ems: `EMS_POLICE_TX`, `EMS_AMB_TX`

## 운영 원칙
- `00~07` 문서는 참고/검증 기준이며 구현 수정은 `canoe/`에서만 수행
- 검증 범위는 CANoe SIL, CAN + Ethernet
- busy 충돌 대응 절차는 `canoe/AGENTS.md` 준수
