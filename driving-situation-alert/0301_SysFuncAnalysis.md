# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.30
**Date**: 2026-03-09
**Status**: Draft (Architecture Reset In Progress)
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

## 작성 원칙

- 본 문서는 03_Function_definition.md의 Func_001~Func_121, Func_123, Func_125~Func_155를 노드 내부 동작 관점으로 분해한다.
- V2 확장 요구(`Req_120~Req_121`, `Req_123`, `Req_125~Req_129`)는 `Func_120~Func_121`, `Func_123`, `Func_125~Func_129`로 구현 활성 상태에서 관리한다.
- ADAS 객체 인지 확장 요구(`Req_130~Req_139`)는 `Func_130~Func_139`로 Pre-Activation(설계 선반영) 상태에서 관리한다.
- 차량 경보 편의 확장 요구(`Req_140~Req_147`)는 `Func_140~Func_147`로 Pre-Activation(설계 선반영) 상태에서 관리한다.
- 경고 강건성·인지성 확장 요구(`Req_148~Req_155`)는 `Func_148~Func_155`로 Pre-Activation(설계 선반영) 상태에서 관리한다.
- 각 기능의 owner는 surface ECU를 먼저 사용하고, runtime module은 하위 추적 열에서만 유지한다.
- 요구사항(What) 문장을 반복하지 않고, 시스템 동작 로직(How)만 기술한다.
- 상단 표는 공식 표준 양식의 열 구성(노드/기능 상세/비고)을 유지한다.
- 상세 추적 정보(Func/Req/실제 입출력)는 하단 표에 분리한다.
- 옵션1 아키텍처를 고정한다: 중앙 경고코어 + Ethernet 백본(ETH_SW) + 도메인 게이트웨이 + 도메인 CAN.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`는 Validation Harness(검증 전용)이며, Gateway/도메인 통신 경로의 기능 노드로 해석하지 않는다.
- 변수명은 0304 표준 Name(`vehicleSpeed`, `roadZone`, `speedLimit`) 기준으로 작성하고, 코드 별칭(`g*`)은 구현 문서에서만 사용한다.
- ECU 노드명은 ISO 기능 분리 원칙(센싱/판단/중재/출력/게이트웨이)을 따르고, OEM 레퍼런스는 `reference/dbc/level3_communication/reference/*.dbc`를 참고한다.
- architecture reset 기간에는 `surface ECU -> runtime module -> validation harness` 3층 구조를 기본 서술 규칙으로 사용한다.
- 상위 문서 계층에서는 `V2X`, `ADAS`, `BCM`, `IVI`, `CLU`, `CGW` 같은 surface ECU를 먼저 사용하고, 내부 구현 모듈은 supporting note로만 노출한다.
- 현재 runtime canonical name은 transition baseline으로 유지하며, GUI/runtime rename은 `0301~04` 문서 재정렬 후 마지막에 수행한다.
- OEM100 전체 Surface ECU 정의는 `00e` 6.4 표를 단일 기준으로 사용한다.
- 본 문서는 Active ECU만 상세 동작을 기술하며, Placeholder ECU는 `미구현` 상태로 유지하고 승격 전에는 추적체인을 강제하지 않는다.

---

## OEM100 Surface ECU 적용 상태 (0301 기준)
| 구분 | 내용 |
|---|---|
| 기준 SoT | `00e_ECU_Naming_Standard.md` 6.4 (100 ECU 전수표) |
| 전체 Surface ECU | 100 |
| 활성(상세 정의) | 16 |
| 미구현(Placeholder) | 84 |

### OEM100 전수표 (100개)

| Surface ECU | Group | Domain Bucket | Surface Type | 구현 상태 | Runtime Binding | 문서 반영 정책 |
|---|---|---|---|---|---|---|
| `CGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `CGW` | 추적체인 반영 대상 |
| `ETH_BACKBONE` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `ETH_SW(Seam monitor)` | 추적체인 반영 대상 |
| `DCM` | A1 | Infrastructure/Integration | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `IBOX` | A1 | Infrastructure/Integration | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EMS` | 추적체인 반영 대상 |
| `TCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `TCU` | 추적체인 반영 대상 |
| `VCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `VCU` | 추적체인 반영 대상 |
| `_4WD` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `BAT_BMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `FPCM` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `LVR` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ISG` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EOP` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EWP` | A2 | Powertrain | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ESC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ESC` | 추적체인 반영 대상 |
| `MDPS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `MDPS` | 추적체인 반영 대상 |
| `ABS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EPB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `TPMS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SAS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ECS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ACU` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ODS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `VSM` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EHB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `CDC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `BCM` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `BCM` | 추적체인 반영 대상 |
| `DATC` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DATC` | 추적체인 반영 대상 |
| `SMK` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AFLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AHLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `WIPER_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SUNROOF_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DOOR_FL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DOOR_FR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DOOR_RL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DOOR_RR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `TAILGATE_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SEAT_DRV` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SEAT_PASS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `MIRROR_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `BODY_SECURITY_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `IVI` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `IVI` | 추적체인 반영 대상 |
| `CLU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `CLU` | 추적체인 반영 대상 |
| `HUD` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `TMU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `TMU` | 추적체인 반영 대상 |
| `AMP` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `PGS` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `NAV_MODULE` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `VOICE_ASSIST` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `RSE` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DIGITAL_KEY` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ADAS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `ADAS` | 추적체인 반영 대상 |
| `V2X` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `V2X` | 추적체인 반영 대상 |
| `SCC` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `SCC` | 추적체인 반영 대상 |
| `LDWS_LKAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `FCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `BCW` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `LCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SPAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `RSPA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AVM` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `FCAM` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `FRADAR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SRR_FL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SRR_FR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SRR_RL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SRR_RR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `PARK_ULTRASONIC` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `OMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `VALIDATION_HARNESS` | B | Validation | VALIDATION | 활성(상세 정의) | `VAL_SCENARIO_CTRL + VAL_BASELINE_CTRL` | 추적체인 반영 대상 |
| `OBC` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `DCDC` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `MCU` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `INVERTER` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `CHARGE_PORT_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AIR_SUSPENSION` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `RWS` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `NIGHT_VISION` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AEB_DOMAIN` | C | Premium Option | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `HIGHWAY_PILOT` | C | Premium Option | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `PARK_MASTER` | C | Premium Option | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `TRAILER_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `HEADLAMP_LEVELING` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AUTO_DOOR_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `POWER_TAILGATE_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `MASSAGE_SEAT_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `REAR_CLIMATE_MODULE` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `CABIN_SENSING` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `BIOMETRIC_AUTH` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `CARPAY_CTRL` | C | Premium Option | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `PHONE_AS_KEY` | C | Premium Option | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `OTA_MASTER` | C | Premium Option | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `EDR` | C | Premium Option | INFRA_SERVICE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `ROAD_PREVIEW_CAMERA` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `LIDAR` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `REAR_RADAR_MASTER` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `SURROUND_PARK_MASTER` | C | Premium Option | FUNCTION_SURFACE | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |


- Placeholder ECU는 승격 전까지 상세 추적(Req/Func/Flow/Comm/Var/Test)을 강제하지 않는다.
- Placeholder ECU 승격 시 `03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07` 순서로 동일 커밋 편입한다.
---

## 노드별 기능 명세 (공식 표준 양식)

| 노드 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Production Surface ECU |
| `EMS` | 시동/엔진 상태 반영 및 powertrain 기준 상태 제공 | runtime: `ENG_CTRL` |
| `TCU` | 기어/변속 상태 유지 및 전달 | runtime: `TCU` |
| `VCU` | 가속 요구와 종방향 차량 상태 입력 제공 | runtime: `ACCEL_CTRL` |
| `ESC` | 제동/차량 안정화 경로 제공 | runtime: `BRK_CTRL` |
| `MDPS` | 조향 입력/조향 상태 경로 제공 | runtime: `STEER_CTRL` |
| `BCM` | 앰비언트/비상등/창문/도어/운전자 상태를 포함한 차체 출력 및 바디 상태 관리 | runtime: `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` |
| `DATC` | 실내 공조 상태/제어 입력을 수신해 차체 정책과 연동 | runtime: `DATC` (활성 전개 중) |
| `IVI` | 내비게이션/인포테인먼트 컨텍스트 관리 및 cluster 입력 프레임 생성 | runtime: `IVI_GW`, `NAV_CTX_MGR` |
| `TMU` | 원격 연결/텔레매틱스 이벤트 수집 및 상위 알림 연계 | runtime: `TMU` (활성 전개 중) |
| `CLU` | 경고 문구/기본 표시/HMI 상태를 표시 표면으로 제공 | runtime: `CLU_HMI_CTRL`, `CLU_BASE_CTRL` |
| `ADAS` | 주행 위험 판단, TTC/위험도 계산, 경보 우선순위 중재 수행 | runtime: `ADAS_WARN_CTRL`, `WARN_ARB_MGR` |
| `SCC` | 종방향 안전거리/속도 보조 판단을 위한 보조 안전 제어 표면 | runtime: `SCC` (활성 전개 중) |
| `V2X` | 긴급차량 접근 신호 송수신/타임아웃/이벤트 기록 경로 제공 | runtime: `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` |
|  |  | Infrastructure Surface |
| `CGW` | 도메인 CAN 입력 정규화, 도메인 간 라우팅, 경계/헬스 정책 유지 | runtime: `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` |
| `ETH_BACKBONE` | Ethernet 백본 경로 상태와 freshness를 감시하는 전달 인프라 | runtime: `ETH_SW` |
|  |  | Validation Harness |
| `VALIDATION_HARNESS` | SIL 시나리오 실행, baseline 판정, 테스트 결과 기록 | runtime: `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` |
|  |  | Actual Device |
| Ambient Lights | 실제 앰비언트 장치가 제어 신호를 수신해 점등/패턴 동작 수행 | `BCM` 출력 반영 |
| Cluster Display | 실제 클러스터 장치가 경고 문구/상태를 표시 | `CLU` 출력 반영 |
| Navigation Panel | 사용자 입력(구간/방향/거리/제한속도) 제공 및 시각화 | `IVI` 입력 소스 |

- 시스템 아키텍처 관점에서 `ETH_BACKBONE`은 reviewer-facing surface이고, `ETH_SW`는 active runtime monitor다.
- `VALIDATION_HARNESS`는 생산 ECU 인벤토리와 분리 유지하며, reviewer-facing vehicle architecture에 포함하지 않는다.

---

## 기능 정의 상세 표 (추적성/입출력 정의)
| Func ID | Req ID | Surface ECU | Runtime/Transition Baseline | 입력 (Input) | 처리 (Processing) | 출력 (Output) | 실제값 정의 |
|---|---|---|---|---|---|---|---|
| Func_007 | Req_007 | IVI | NAV_CTX_MGR | roadZone, navDirection, zoneDistance, speedLimit | 구간 상태 판별 및 전환 컨텍스트 갱신 | baseZoneContext, speedLimitNorm | 입력: roadZone, navDirection, zoneDistance, speedLimit |
| Func_001~004,006,010~012 | Req_001~004,006,010~012 | ADAS | ADAS_WARN_CTRL | vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext | 스쿨존 과속/고속 무조향 조건 판정, 경고 트리거 생성, 디바운스 | warningState | 입력: vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext |
| Func_013~016 | Req_013~Req_016 | BCM | AMBIENT_CTRL | selectedAlertType, selectedAlertLevel, navDirection, timeoutClear | 유도구간 진입 전환/방향 분기/전환 완화/종료 복귀 처리 | ambientMode, ambientPattern | 입력: selectedAlertType, selectedAlertLevel, navDirection, timeoutClear |
| Func_017 | Req_017 | V2X | EMS_POLICE_TX | testScenario | 경찰 긴급 알림 패킷 생성 및 송신 관리(내부 Tx 모듈) | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_018 | Req_017 | V2X | EMS_AMB_TX | testScenario | 구급 긴급 알림 패킷 생성 및 송신 관리(내부 Tx 모듈) | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_023,024 | Req_023,024 | V2X | EMS_ALERT_RX | alertState, emergencyType, lastEmergencyRxMs | 수신/해제 상태 관리, 1000ms 타임아웃 처리(내부 Rx 모듈) | emergencyContext, timeoutClear | 입력: alertState, emergencyType, lastEmergencyRxMs |
| Func_022,025~032 | Req_022,025~032 | ADAS | WARN_ARB_MGR | emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId | 경보 우선순위 판정 수행 | selectedAlertLevel, selectedAlertType | 입력: emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId |
| Func_008,009,033~039 | Req_008,009,033,034,035,037 | BCM | AMBIENT_CTRL | selectedAlertLevel, selectedAlertType, navDirection, baseZoneContext, timeoutClear | 경고 등급별 색상/패턴 적용, 전환 완화, 복원 | ambientMode, ambientColor, ambientPattern | 출력: ambientMode, ambientColor, ambientPattern |
| Func_005,019~021,026,040 | Req_005,019~021,026,040 | CLU | CLU_HMI_CTRL | selectedAlertType, emergencyDirection, duplicatePopupGuard, warningTextCode | 경고 문구/종류/방향/양보 메시지 표시 | warningTextCode | 출력: warningTextCode |
| Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | VALIDATION_HARNESS | VAL_SCENARIO_CTRL | testScenario | 시나리오 실행, CAN+ETH 검증, 판정 기록 | scenarioResult | 출력: scenarioResult |
| Func_101 | Req_101 | EMS | ENG_CTRL | IgnitionState | 시동 상태 반영 | EngineState | 입력: IgnitionState / 출력: EngineState |
| Func_102 | Req_102 | TCU | TCU | GearInput | 기어 상태 반영 | GearState | 입력: GearInput / 출력: GearState |
| Func_103 | Req_103 | VCU | ACCEL_CTRL | AccelPedal | 가속 입력 반영 | AccelRequest | 입력: AccelPedal / 출력: AccelRequest |
| Func_104 | Req_104 | ESC | BRK_CTRL | BrakePedal | 제동 입력 반영 | BrakePressure | 입력: BrakePedal / 출력: BrakePressure |
| Func_105 | Req_105 | MDPS | STEER_CTRL | steeringInput | 조향 입력 반영 | SteeringState | 입력: steeringInput / 출력: SteeringState |
| Func_106 | Req_106 | BCM | HAZARD_CTRL | HazardSwitch | 비상등 기본 제어 | HazardState | 입력: HazardSwitch / 출력: HazardState |
| Func_107 | Req_107 | BCM | WINDOW_CTRL | WindowCommand | 창문 기본 제어 | WindowState | 입력: WindowCommand / 출력: WindowState |
| Func_109 | Req_109 | CLU | CLU_BASE_CTRL | ClusterSpeed, ClusterGear, warningTextCode | 클러스터 기본 표시 | ClusterStatus | 입력: ClusterSpeed, ClusterGear, warningTextCode / 출력: ClusterStatus |
| Func_110 | Req_110 | CGW | DOMAIN_ROUTER | RoutingPolicy | 도메인 게이트웨이 전달 | BodyGatewayRoute | 입력: RoutingPolicy / 출력: BodyGatewayRoute |
| Func_111 | Req_111 | CGW | DOMAIN_BOUNDARY_MGR | RoutingPolicy | 도메인 경계 유지 | BoundaryStatus | 입력: RoutingPolicy / 출력: BoundaryStatus |
| Func_112 | Req_112 | VALIDATION_HARNESS | VAL_BASELINE_CTRL | BaseScenarioId | 차량 기본 기능 SIL 검증 | BaseScenarioResult | 입력: BaseScenarioId / 출력: BaseScenarioResult |
| Func_113 | Req_113 | BCM | BODY_GW | CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode | DATC 상태/제어 프레임 반영 | CabinTemp | 입력: CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode / 출력: CabinTemp |
| Func_114 | Req_113 | BCM | DRV_STATE_MGR | DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel | 시트 상태/제어 프레임 반영 | DriverStateInfo | 입력: DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel / 출력: DriverStateInfo |
| Func_115 | Req_113 | BCM | WINDOW_CTRL | MirrorFoldState, MirrorHeatState, MirrorAdjAxis | 미러 상태 프레임 반영 | WindowState | 입력: MirrorFoldState, MirrorHeatState, MirrorAdjAxis / 출력: WindowState |
| Func_116 | Req_116 | BCM | WINDOW_CTRL | DoorUnlockCmd, DoorLockState, DoorOpenWarn | 도어 제어/잠금/열림 상태 반영 | DoorStateMask | 입력: DoorUnlockCmd, DoorLockState, DoorOpenWarn / 출력: DoorStateMask |
| Func_117 | Req_116 | BCM | AMBIENT_CTRL | FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq | 와이퍼/우적 연동 상태 반영 | WiperInterval | 입력: FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq / 출력: WiperInterval |
| Func_118 | Req_118 | BCM | DRV_STATE_MGR | ImmoState, AlarmArmed, AlarmTrigger, AlarmZone | 이모빌라이저/경보 상태 반영 | DriverStateInfo | 입력: ImmoState, AlarmArmed, AlarmTrigger, AlarmZone / 출력: DriverStateInfo |
| Func_119 | Req_119 | CLU | CLU_HMI_CTRL | AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId | 오디오 포커스/음성비서/TTS 상태 반영 | warningTextCode | 입력: AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId / 출력: warningTextCode |
| Func_120 | Req_120 | ADAS | ADAS_WARN_CTRL | emergencyDirection, eta, vehicleSpeedNorm | 긴급차량 방향/ETA/자차속도 결합 기반 근접 위험도 산정 | proximityRiskLevel | 입력: emergencyDirection, eta, vehicleSpeedNorm / 출력: proximityRiskLevel |
| Func_121 | Req_121 | ADAS | WARN_ARB_MGR | proximityRiskLevel, failSafeMode, driveStateNorm | 위험도 임계 초과 시 감속 보조 요청 생성 | decelAssistReq | 입력: proximityRiskLevel, failSafeMode, driveStateNorm / 출력: decelAssistReq |
| Func_125 | Req_125 | ADAS | WARN_ARB_MGR | decelAssistReq, selectedAlertType, selectedAlertLevel | 감속 보조 활성 시 긴급 경고 우선 유지 | selectedAlertLevel, selectedAlertType | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertLevel, selectedAlertType |
| Func_126 | Req_126 | ADAS | WARN_ARB_MGR | decelAssistReq, selectedAlertType, selectedAlertLevel | 감속 보조 활성 시 Ambient/Cluster 동기화 유지 | selectedAlertLevel, selectedAlertType | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertLevel, selectedAlertType |
| Func_123 | Req_123 | ADAS | WARN_ARB_MGR | steeringInputNorm, brakePedalNorm | 운전자 제동/조향 회피 입력 시 감속 보조 요청 해제 | decelAssistReq | 입력: steeringInputNorm, brakePedalNorm / 출력: decelAssistReq |
| Func_127 | Req_127 | CGW | DOMAIN_BOUNDARY_MGR | domainPathStatus, e2eHealthState | 도메인 경로 단절 감지 시 자동 감속 보조 금지 | decelAssistReq | 입력: domainPathStatus, e2eHealthState / 출력: decelAssistReq |
| Func_128 | Req_128 | CGW | DOMAIN_BOUNDARY_MGR | domainPathStatus, e2eHealthState | 도메인 경로 단절 감지 시 최소 경고 채널 유지 | selectedAlertLevel, selectedAlertType | 입력: domainPathStatus, e2eHealthState / 출력: selectedAlertLevel, selectedAlertType |
| Func_129 | Req_129 | CGW | DOMAIN_BOUNDARY_MGR | domainPathStatus, e2eHealthState | 도메인 경로 단절 감지 시 안전 강등 모드 전환 | failSafeMode | 입력: domainPathStatus, e2eHealthState / 출력: failSafeMode |
| Func_130 | Req_130 | ADAS | ADAS_WARN_CTRL | objectTrackValid, objectRange, objectRelSpeed, objectConfidence | 주변 객체 목록 입력 정규화 및 판단 입력 구성 | objectTrackValid, objectRange, objectRelSpeed | 입력: objectTrackValid, objectRange, objectRelSpeed, objectConfidence / 출력: objectTrackValid, objectRange, objectRelSpeed |
| Func_131 | Req_131 | ADAS | ADAS_WARN_CTRL | objectTrackValid, objectRange, objectRelSpeed | 자차 경로 기반 대표 위험 객체 선정 | objectRiskClass, objectTtcMin | 입력: objectTrackValid, objectRange, objectRelSpeed / 출력: objectRiskClass, objectTtcMin |
| Func_132 | Req_132 | ADAS | ADAS_WARN_CTRL | objectTtcMin, objectRiskClass | TTC 임계 기반 전방 충돌 경고 트리거 생성 | selectedAlertLevel, objectRiskClass | 입력: objectTtcMin, objectRiskClass / 출력: selectedAlertLevel, objectRiskClass |
| Func_133 | Req_133 | ADAS | ADAS_WARN_CTRL | objectRelSpeed, objectRange, objectRiskClass | 상대속도/거리 기반 경고 단계 상하향 | selectedAlertLevel, objectRiskClass | 입력: objectRelSpeed, objectRange, objectRiskClass / 출력: selectedAlertLevel, objectRiskClass |
| Func_134 | Req_134 | ADAS | WARN_ARB_MGR | intersectionConflictFlag, objectRiskClass | 교차로 측방 접근 객체 위험 경고 판정 | selectedAlertType, selectedAlertLevel | 입력: intersectionConflictFlag, objectRiskClass / 출력: selectedAlertType, selectedAlertLevel |
| Func_135 | Req_135 | ADAS | WARN_ARB_MGR | mergeCutInFlag, objectRiskClass | 합류/끼어들기 객체 위험 경고 판정 | selectedAlertType, selectedAlertLevel | 입력: mergeCutInFlag, objectRiskClass / 출력: selectedAlertType, selectedAlertLevel |
| Func_136 | Req_136 | ADAS | ADAS_WARN_CTRL | objectTrackValid, objectAlertHoldMs, objectRiskClass | 추적 손실 시 경고 보수 유지시간 적용 | selectedAlertLevel, objectRiskClass | 입력: objectTrackValid, objectAlertHoldMs, objectRiskClass / 출력: selectedAlertLevel, objectRiskClass |
| Func_137 | Req_137 | CGW | DOMAIN_BOUNDARY_MGR | objectConfidence, decelAssistReq | 객체 신뢰도 저하 시 자동 감속 보조 차단 및 경고 강등 | decelAssistReq, selectedAlertLevel, failSafeMode | 입력: objectConfidence, decelAssistReq / 출력: decelAssistReq, selectedAlertLevel, failSafeMode |
| Func_138 | Req_138 | V2X | EMS_ALERT_RX | objectRiskClass, selectedAlertType, selectedAlertLevel | 객체 기반 경고 이벤트 코드 생성/기록 | objectEventCode | 입력: objectRiskClass, selectedAlertType, selectedAlertLevel / 출력: objectEventCode |
| Func_139 | Req_139 | ADAS | WARN_ARB_MGR | objectRiskClass, emergencyContext, baseZoneContext | 객체 경고와 기존 경고의 우선순위 정합 판정 | selectedAlertType, selectedAlertLevel | 입력: objectRiskClass, emergencyContext, baseZoneContext / 출력: selectedAlertType, selectedAlertLevel |
| Func_140 | Req_140 | ADAS | WARN_ARB_MGR | TurnLampState, selectedAlertType | 방향지시등 상태 기반 경보 맥락 보정 | selectedAlertType, warningTextCode | 입력: TurnLampState, selectedAlertType / 출력: selectedAlertType, warningTextCode |
| Func_141 | Req_141 | ADAS | WARN_ARB_MGR | DriveMode, EcoMode, SportMode, selectedAlertLevel | 주행모드 기반 경보 민감도 프로파일 보정 | selectedAlertLevel | 입력: DriveMode, EcoMode, SportMode, selectedAlertLevel / 출력: selectedAlertLevel |
| Func_142 | Req_142 | ADAS | WARN_ARB_MGR | DriverSeatBelt, PassengerSeatBelt, SeatBeltWarnLvl, selectedAlertLevel | 안전벨트 상태 기반 경보 강조 레벨 보정 | selectedAlertLevel, selectedAlertType | 입력: DriverSeatBelt, PassengerSeatBelt, SeatBeltWarnLvl, selectedAlertLevel / 출력: selectedAlertLevel, selectedAlertType |
| Func_143 | Req_143 | CLU | CLU_HMI_CTRL | eta, vehicleSpeedNorm, selectedAlertType | 긴급차량 접근 거리 등급/문구 표시 | warningTextCode | 입력: eta, vehicleSpeedNorm, selectedAlertType / 출력: warningTextCode |
| Func_144 | Req_144 | V2X | EMS_ALERT_RX | selectedAlertType, selectedAlertLevel, warningTextCode | 경보 이벤트 공통 포맷 기록 | arbitrationSnapshotId | 입력: selectedAlertType, selectedAlertLevel, warningTextCode / 출력: arbitrationSnapshotId |
| Func_145 | Req_145 | CLU | CLU_HMI_CTRL | arbitrationSnapshotId, ClusterNotifType, ClusterNotifPrio | 경보 이벤트 이력 조회/표시 | warningTextCode | 입력: arbitrationSnapshotId, ClusterNotifType, ClusterNotifPrio / 출력: warningTextCode |
| Func_146 | Req_146 | CLU | CLU_HMI_CTRL | ThemeMode, PopupType, PopupPriority, PopupActive | 경보 표시 방식 설정 반영 | warningTextCode, ClusterNotifPrio | 입력: ThemeMode, PopupType, PopupPriority, PopupActive / 출력: warningTextCode, ClusterNotifPrio |
| Func_147 | Req_147 | CLU | CLU_HMI_CTRL | VolumeLevel, AudioFocusOwner | 경보 음량 설정 반영 | warningTextCode, ClusterNotifPrio | 입력: VolumeLevel, AudioFocusOwner / 출력: warningTextCode, ClusterNotifPrio |
| Func_148 | Req_148 | ADAS | ADAS_WARN_CTRL | objectTrackValid, objectConfidence, objectRiskClass | 경고 입력 유효성/신뢰도 필터링 | objectRiskClass, selectedAlertLevel | 입력: objectTrackValid, objectConfidence, objectRiskClass / 출력: objectRiskClass, selectedAlertLevel |
| Func_149 | Req_149 | ADAS | WARN_ARB_MGR | lastEmergencyRxMs, timeoutClear, warningState | 핵심 입력 신선도(stale) 감지 및 보수 정책 전환 | warningState, selectedAlertLevel | 입력: lastEmergencyRxMs, timeoutClear, warningState / 출력: warningState, selectedAlertLevel |
| Func_150 | Req_150 | ADAS | WARN_ARB_MGR | warningState, selectedAlertLevel, duplicatePopupGuard | 경고 상태 전이 진동 억제(안정화) | selectedAlertLevel, selectedAlertType | 입력: warningState, selectedAlertLevel, duplicatePopupGuard / 출력: selectedAlertLevel, selectedAlertType |
| Func_151 | Req_151 | CGW | DOMAIN_BOUNDARY_MGR | domainPathStatus, e2eHealthState, BoundaryStatus | 출력 채널 가용성 판정 | domainPathStatus, failSafeMode | 입력: domainPathStatus, e2eHealthState, BoundaryStatus / 출력: domainPathStatus, failSafeMode |
| Func_152 | Req_152 | ADAS | WARN_ARB_MGR | failSafeMode, selectedAlertType, selectedAlertLevel | 주 출력 채널 장애 시 대체 출력 정책 적용 | selectedAlertType, selectedAlertLevel, warningTextCode | 입력: failSafeMode, selectedAlertType, selectedAlertLevel / 출력: selectedAlertType, selectedAlertLevel, warningTextCode |
| Func_153 | Req_153 | CLU | CLU_HMI_CTRL | AudioFocusOwner, AudioDuckLevel, TtsState | 오디오 경합 시 경고 인지성 보호 | warningTextCode, ClusterNotifPrio | 입력: AudioFocusOwner, AudioDuckLevel, TtsState / 출력: warningTextCode, ClusterNotifPrio |
| Func_154 | Req_154 | CLU | CLU_HMI_CTRL | PopupType, PopupPriority, PopupActive, duplicatePopupGuard | 팝업 과밀 억제 및 우선 경고 선표시 | warningTextCode, ClusterNotifPrio | 입력: PopupType, PopupPriority, PopupActive, duplicatePopupGuard / 출력: warningTextCode, ClusterNotifPrio |
| Func_155 | Req_155 | CLU | CLU_HMI_CTRL | ClusterSyncState, ClusterSyncSeq, selectedAlertType, selectedAlertLevel | 앰비언트/클러스터 경고 동기 일관성 관리 | warningTextCode, ClusterNotifPrio | 입력: ClusterSyncState, ClusterSyncSeq, selectedAlertType, selectedAlertLevel / 출력: warningTextCode, ClusterNotifPrio |

## 2-1. Req-Func 감사 매핑 표 (N:M 허용)

| Req ID | Func ID | Surface ECU | Runtime/Transition Baseline | 기능명 |
|---|---|---|---|---|
| Req_001 | Func_001 | ADAS | ADAS_WARN_CTRL | 주행시 경고엔진 활성 |
| Req_002 | Func_002 | ADAS | ADAS_WARN_CTRL | 비주행 경고 억제 |
| Req_003 | Func_003 | ADAS | ADAS_WARN_CTRL | 경고 시작 트리거 |
| Req_004 | Func_004 | ADAS | ADAS_WARN_CTRL | 경고 종료 트리거 |
| Req_005 | Func_005 | CLU | CLU_HMI_CTRL | 경고 원인 전달 |
| Req_006 | Func_006 | ADAS | ADAS_WARN_CTRL | 반복 경고 디바운스 |
| Req_007 | Func_007 | IVI | NAV_CTX_MGR | 구간값 변경 반영 |
| Req_008 | Func_008 | BCM | AMBIENT_CTRL | 일반구간 정책 적용 |
| Req_009 | Func_009 | BCM | AMBIENT_CTRL | 스쿨존 강화 경고 |
| Req_010 | Func_010 | ADAS | ADAS_WARN_CTRL | 스쿨존 과속 경고 |
| Req_011 | Func_011 | ADAS | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 |
| Req_012 | Func_012 | ADAS | ADAS_WARN_CTRL | 무조향 경고 해제 |
| Req_013 | Func_013 | BCM | AMBIENT_CTRL | 유도구간 진입 전환 |
| Req_014 | Func_014 | BCM | AMBIENT_CTRL | 좌우 방향 구분 표시 |
| Req_015 | Func_015 | BCM | AMBIENT_CTRL | 구간 전환 완화 |
| Req_016 | Func_016 | BCM | AMBIENT_CTRL | 구간경고 종료 복귀 |
| Req_017 | Func_017 | V2X | EMS_POLICE_TX | 경찰 접근 경고 송신 |
| Req_017 | Func_018 | V2X | EMS_AMB_TX | 구급 접근 경고 송신 |
| Req_019 | Func_019 | CLU | CLU_HMI_CTRL | 긴급차량 종류 표시 |
| Req_020 | Func_020 | CLU | CLU_HMI_CTRL | 긴급차량 방향 표시 |
| Req_021 | Func_021 | CLU | CLU_HMI_CTRL | 양보 유도 메시지 |
| Req_022 | Func_022 | ADAS | WARN_ARB_MGR | 긴급경고 우선 출력 |
| Req_023 | Func_023 | V2X | EMS_ALERT_RX | 종료 신호 처리 |
| Req_024 | Func_024 | V2X | EMS_ALERT_RX | 타임아웃 보호해제 |
| Req_025 | Func_025 | ADAS | WARN_ARB_MGR | 다중긴급 단일선택 |
| Req_026 | Func_026 | CLU | CLU_HMI_CTRL | 중복 팝업 억제 |
| Req_027 | Func_027 | ADAS | WARN_ARB_MGR | 충돌중재 적용 |
| Req_028 | Func_028 | ADAS | WARN_ARB_MGR | 긴급>구간 우선 적용 |
| Req_029 | Func_029 | ADAS | WARN_ARB_MGR | 구급>경찰 우선 적용 |
| Req_030 | Func_030 | ADAS | WARN_ARB_MGR | ETA 우선 적용 |
| Req_031 | Func_031 | ADAS | WARN_ARB_MGR | SourceID 동률판정 |
| Req_032 | Func_032 | ADAS | WARN_ARB_MGR | 중재결과 결정론 보장 |
| Req_033 | Func_033 | BCM | AMBIENT_CTRL | 종료후 이전상태 복원 |
| Req_034 | Func_034 | BCM | AMBIENT_CTRL | 전환 깜빡임 완화 |
| Req_035 | Func_035 | BCM | AMBIENT_CTRL | 긴급 색상 정책 |
| Req_035 | Func_036 | BCM | AMBIENT_CTRL | 긴급 패턴 정책 |
| Req_037 | Func_037 | BCM | AMBIENT_CTRL | 스쿨존 패턴 정책 |
| Req_037 | Func_038 | BCM | AMBIENT_CTRL | 고속도로 패턴 정책 |
| Req_037 | Func_039 | BCM | AMBIENT_CTRL | 유도선 패턴 정책 |
| Req_040 | Func_040 | CLU | CLU_HMI_CTRL | 문구 길이 제한 |
| Req_041 | Func_041 | VALIDATION_HARNESS | VAL_SCENARIO_CTRL | SIL 시나리오 실행 |
| Req_042 | Func_042 | VALIDATION_HARNESS | VAL_SCENARIO_CTRL | CAN+ETH 동시 검증 |
| Req_043 | Func_043 | VALIDATION_HARNESS | VAL_SCENARIO_CTRL | 판정 결과 산출 |
| Req_101 | Func_101 | EMS | ENG_CTRL | 시동 상태 반영 |
| Req_102 | Func_102 | TCU | TCU | 기어 상태 반영 |
| Req_103 | Func_103 | VCU | ACCEL_CTRL | 가속 입력 반영 |
| Req_104 | Func_104 | ESC | BRK_CTRL | 제동 입력 반영 |
| Req_105 | Func_105 | MDPS | STEER_CTRL | 조향 입력 반영 |
| Req_106 | Func_106 | BCM | HAZARD_CTRL | 비상등 기본 제어 |
| Req_107 | Func_107 | BCM | WINDOW_CTRL | 창문 기본 제어 |
| Req_109 | Func_109 | CLU | CLU_BASE_CTRL | 클러스터 기본 표시 |
| Req_110 | Func_110 | CGW | DOMAIN_ROUTER | 도메인 게이트웨이 전달 |
| Req_111 | Func_111 | CGW | DOMAIN_BOUNDARY_MGR | 도메인 경계 유지 |
| Req_112 | Func_112 | VALIDATION_HARNESS | VAL_BASELINE_CTRL | 차량 기본 기능 SIL 검증 |
| Req_113 | Func_113 | BCM | BODY_GW | 공조 상태 반영 |
| Req_113 | Func_114 | BCM | DRV_STATE_MGR | 시트 상태 반영 |
| Req_113 | Func_115 | BCM | WINDOW_CTRL | 미러 상태 반영 |
| Req_116 | Func_116 | BCM | WINDOW_CTRL | 도어 제어 상태 반영 |
| Req_116 | Func_117 | BCM | AMBIENT_CTRL | 와이퍼/우적 연동 반영 |
| Req_118 | Func_118 | BCM | DRV_STATE_MGR | 보안 상태 반영 |
| Req_119 | Func_119 | CLU | CLU_HMI_CTRL | 오디오 상태 반영 |
| Req_120 | Func_120 | ADAS | ADAS_WARN_CTRL | 긴급차량 근접 위험 판단 |
| Req_121 | Func_121 | ADAS | WARN_ARB_MGR | 위험도 기반 감속 보조 요청 |
| Req_125 | Func_125 | ADAS | WARN_ARB_MGR | 감속 보조 시 긴급경고 최우선 유지 |
| Req_126 | Func_126 | ADAS | WARN_ARB_MGR | 감속 보조 시 경고 채널 동기화 |
| Req_123 | Func_123 | ADAS | WARN_ARB_MGR | 운전자 개입 우선 해제 |
| Req_127 | Func_127 | CGW | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 자동감속 금지 |
| Req_128 | Func_128 | CGW | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 최소 경고 유지 |
| Req_129 | Func_129 | CGW | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 안전 강등 전환 |
| Req_130 | Func_130 | ADAS | ADAS_WARN_CTRL | 주변 객체 목록 수용 |
| Req_131 | Func_131 | ADAS | ADAS_WARN_CTRL | 대표 위험 객체 선정 |
| Req_132 | Func_132 | ADAS | ADAS_WARN_CTRL | TTC 기반 전방 충돌 경고 |
| Req_133 | Func_133 | ADAS | ADAS_WARN_CTRL | 상대속도/거리 기반 경보 단계화 |
| Req_134 | Func_134 | ADAS | WARN_ARB_MGR | 교차로 측방 접근 위험 경고 |
| Req_135 | Func_135 | ADAS | WARN_ARB_MGR | 합류/끼어들기 위험 경고 |
| Req_136 | Func_136 | ADAS | ADAS_WARN_CTRL | 객체 추적 손실 보수 유지 |
| Req_137 | Func_137 | CGW | DOMAIN_BOUNDARY_MGR | 신뢰도 저하 시 경고 강등 |
| Req_138 | Func_138 | V2X | EMS_ALERT_RX | 객체 기반 경고 이벤트 기록 |
| Req_139 | Func_139 | ADAS | WARN_ARB_MGR | 객체 경고 우선순위 정합 |
| Req_140 | Func_140 | ADAS | WARN_ARB_MGR | 방향지시등 기반 경보 맥락 반영 |
| Req_141 | Func_141 | ADAS | WARN_ARB_MGR | 주행모드 기반 경보 민감도 반영 |
| Req_142 | Func_142 | ADAS | WARN_ARB_MGR | 안전벨트 상태 기반 경보 강조 반영 |
| Req_143 | Func_143 | CLU | CLU_HMI_CTRL | 긴급차량 접근 거리 표시 |
| Req_144 | Func_144 | V2X | EMS_ALERT_RX | 경보 이벤트 공통 기록 |
| Req_145 | Func_145 | CLU | CLU_HMI_CTRL | 경보 이벤트 이력 조회 |
| Req_146 | Func_146 | CLU | CLU_HMI_CTRL | 경보 표시 방식 설정 반영 |
| Req_147 | Func_147 | CLU | CLU_HMI_CTRL | 경보 음량 설정 반영 |
| Req_148 | Func_148 | ADAS | ADAS_WARN_CTRL | 경고 입력 유효성 필터링 |
| Req_149 | Func_149 | ADAS | WARN_ARB_MGR | 경고 입력 신선도 보호 |
| Req_150 | Func_150 | ADAS | WARN_ARB_MGR | 경고 상태 전이 안정화 |
| Req_151 | Func_151 | CGW | DOMAIN_BOUNDARY_MGR | 출력 채널 가용성 판정 |
| Req_152 | Func_152 | ADAS | WARN_ARB_MGR | 출력 채널 장애 시 대체 경고 유지 |
| Req_153 | Func_153 | CLU | CLU_HMI_CTRL | 오디오 경합 시 경고 인지성 보호 |
| Req_154 | Func_154 | CLU | CLU_HMI_CTRL | 팝업 과밀 억제 및 우선 표시 |
| Req_155 | Func_155 | CLU | CLU_HMI_CTRL | 경고 채널 동기 일관성 |

---

## 2-2. Legacy Req 상속 매핑 (감사 보강)

| Legacy Req ID | Active Req ID | Func ID | 상속 규칙 |
|---|---|---|---|
| Req_018 | Req_017 | Func_018 | 구급차 분리 요구는 긴급차량 접근 통합 요구(Req_017) 결과를 상속한다. |
| Req_036 | Req_035 | Func_036 | 긴급 패턴 분리 요구는 긴급 시각표현 통합 요구(Req_035) 결과를 상속한다. |
| Req_038 | Req_037 | Func_038 | 고속도로 패턴 분리 요구는 구간 패턴 통합 요구(Req_037) 결과를 상속한다. |
| Req_039 | Req_037 | Func_039 | 유도선 패턴 분리 요구는 구간 패턴 통합 요구(Req_037) 결과를 상속한다. |
| Req_108 | Req_113,Req_116,Req_118 | Func_113,Func_116,Func_118 | 운전자 상태 단일 레벨 전달 요구는 Body 확장 상태 통합 요구(Req_113/Req_116/Req_118) 결과를 상속한다. |
| Req_114 | Req_113 | Func_114 | 시트 상태 단독 요구는 실내편의 통합 요구(Req_113) 결과를 상속한다. |
| Req_115 | Req_113 | Func_115 | 미러 상태 단독 요구는 실내편의 통합 요구(Req_113) 결과를 상속한다. |
| Req_117 | Req_116 | Func_117 | 와이퍼/우적 연동 단독 요구는 차체 제어 통합 요구(Req_116) 결과를 상속한다. |
| Req_122 | Req_125 | Func_125 | 감속 보조 중 긴급 최우선 단독 요구는 V2 통합 요구(Req_125) 결과를 상속한다. |
| Req_124 | Req_127,Req_128,Req_129 | Func_127,Func_128,Func_129 | 도메인 단절 대응 단일 요구는 금지/최소유지/강등 3분할 요구 결과를 상속한다. |

---

## 3. 핵심 시나리오 동작 체인

| 시나리오 | Surface ECU 동작 체인 | Runtime Reference | 연결 Func ID |
|---|---|---|---|
| 스쿨존 과속 | `IVI -> ADAS -> BCM + CLU` | `NAV_CTX_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_007, Func_010, Func_027, Func_037, Func_040 |
| 고속도로 무조향 | `IVI -> ADAS -> BCM + CLU` | `NAV_CTX_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_011, Func_012, Func_027, Func_038, Func_040 |
| 유도구간 방향 안내 | `IVI -> ADAS -> BCM + CLU` | `NAV_CTX_MGR -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_013, Func_014, Func_039, Func_040 |
| 경찰 긴급차량 접근 | `V2X -> ADAS -> BCM + CLU` | `EMS_POLICE_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_017, Func_023, Func_022, Func_035, Func_019 |
| 구급 긴급차량 접근 | `V2X -> ADAS -> BCM + CLU` | `EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_018, Func_023, Func_022, Func_035, Func_019 |
| 경찰+구급 동시 충돌 | `V2X -> ADAS -> BCM + CLU` | `EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> output path` | Func_025~Func_031 |
| 긴급 해제 후 복귀 | `V2X -> ADAS -> BCM + CLU` | `EMS_ALERT_RX(clear/timeout) -> WARN_ARB_MGR -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_024, Func_033, Func_034 |
| 교차로/합류구간 근접위험 감속 보조 | `V2X + ADAS -> ESC + BCM + CLU` | `EMS_ALERT_RX + ADAS_WARN_CTRL + WARN_ARB_MGR -> BRK_CTRL + AMBIENT_CTRL + CLU_HMI_CTRL` | Func_120, Func_121, Func_125, Func_126, Func_123 |
| 도메인 경로 단절 강등 | `CGW -> ADAS + BCM + CLU` | `DOMAIN_BOUNDARY_MGR -> DOMAIN_ROUTER -> WARN_ARB_MGR / output nodes` | Func_127, Func_128, Func_129 |
| 객체 기반 교차로/합류 위험 경고 | `ADAS + CGW + V2X -> BCM + CLU` | `ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR + EMS_ALERT_RX -> AMBIENT_CTRL + CLU_HMI_CTRL` | Func_130, Func_131, Func_132, Func_133, Func_134, Func_135, Func_136, Func_137, Func_138, Func_139 |
| 차량 경보 편의 확장 | `CGW + ADAS + V2X + CLU` | `BODY_GW / DOMAIN_ROUTER + WARN_ARB_MGR + EMS_ALERT_RX + CLU_HMI_CTRL` | Func_140, Func_141, Func_142, Func_143, Func_144, Func_145, Func_146, Func_147 |
| 경고 강건성·인지성 확장 | `ADAS + CGW + CLU` | `ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR + CLU_HMI_CTRL` | Func_148, Func_149, Func_150, Func_151, Func_152, Func_153, Func_154, Func_155 |

---
## 3-1. 네트워크 전달 체인 (옵션1 고정)

| 시나리오 | Surface ECU 전달 체인 | Runtime Reference |
|---|---|---|
| Chassis 상태 입력 | `VALIDATION_HARNESS -> CGW -> ETH_BACKBONE -> ADAS` | `VAL_SCENARIO_CTRL -> Chassis CAN -> CHS_GW -> ETH_SW -> ADAS_WARN_CTRL` |
| Nav 구간 입력 | `VALIDATION_HARNESS -> CGW -> ETH_BACKBONE -> IVI / ADAS` | `VAL_SCENARIO_CTRL -> Infotainment CAN -> INFOTAINMENT_GW -> ETH_SW -> NAV_CTX_MGR / WARN_ARB_MGR` |
| 긴급 신호 처리 | `V2X -> ETH_BACKBONE -> ADAS` | `EMS_*_TX -> ETH_SW -> EMS_ALERT_RX -> WARN_ARB_MGR` |
| Ambient 출력 | `ADAS -> ETH_BACKBONE -> CGW -> BCM` | `WARN_ARB_MGR -> ETH_SW -> BODY_GW -> Body CAN -> AMBIENT_CTRL` |
| Cluster 출력 | `ADAS -> ETH_BACKBONE -> CGW -> CLU` | `WARN_ARB_MGR -> ETH_SW -> IVI_GW -> Infotainment CAN -> CLU_HMI_CTRL` |

---
## 4. 0302 연계 체크포인트

- 각 노드의 출력은 `0302_NWflowDef.md`에서 반드시 Flow ID로 정의한다.
- 최소 연계 규칙:
- `selectedAlertLevel/selectedAlertType` -> `frmAmbientControlMsg(0x260)` 송신 Flow 존재
- `selectedAlertLevel/selectedAlertType` -> `frmClusterWarningMsg(0x280)` 송신 Flow 존재
- `ETH_EmergencyAlert(0xE100)` 송신/수신/해제 Flow 존재
- 타임아웃(1000ms) 해제 Flow 존재

---

## 5. ECU 명명 기준 (Architecture Reset Baseline)

- 본 장의 단일 SoT는 `00e_ECU_Naming_Standard.md`다.
- 본 문서는 `surface ECU -> runtime module -> validation harness` 3층 구조를 적용한 첫 번째 하위 문서다.
- reviewer-facing 기본 owner는 surface ECU를 사용하고, runtime module은 supporting trace로만 유지한다.
- 변수/메시지 이름은 cosmetic consistency만을 위해 rename하지 않는다.

| 계층 | 적용 규칙 | 현재 적용 예시 |
|---|---|---|
| Surface ECU | reviewer-facing owner, GUI 상위 표현, 상위 SoT 본문에 우선 사용 | `CGW`, `EMS`, `VCU`, `ESC`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `VALIDATION_HARNESS` |
| Runtime Module | CAPL/code trace/debugging/merge candidate 판정에서 유지 | `CHS_GW`, `BODY_GW`, `ADAS_WARN_CTRL`, `WARN_ARB_MGR`, `EMS_ALERT_RX` |
| Validation Harness | non-production validation-only runtime, 생산 ECU 표면과 분리 | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` |

### V2X / ADAS / BCM 대표 매핑

| Surface ECU | Runtime Module | 역할 |
|---|---|---|
| `V2X` | `EMS_POLICE_TX` | 경찰 긴급 이벤트 송신 |
| `V2X` | `EMS_AMB_TX` | 구급 긴급 이벤트 송신 |
| `V2X` | `EMS_ALERT_RX` | 긴급 이벤트 수신/해제/타임아웃 처리, V2X merge base |
| `ADAS` | `ADAS_WARN_CTRL` | 위험도/TTC/객체 기반 판단 |
| `ADAS` | `WARN_ARB_MGR` | 경고 중재/감속보조/fail-safe |
| `BCM` | `BODY_GW` | body output frame producer |
| `BCM` | `AMBIENT_CTRL` | ambient output owner |
| `CLU` | `IVI_GW` | cluster frame producer(transition baseline) |
| `CLU` | `CLU_HMI_CTRL` | cluster display-state owner |

- runtime canonical name은 transition baseline으로 유지하며, GUI/runtime rename은 `0301 -> 0302 -> 0303 -> 0304 -> 04` 정렬 후 마지막에 수행한다.

---
## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.30 | 2026-03-09 | OEM100 선행 문서화 보강: `0301`에 100 ECU 기준(활성 16/미구현 84) 적용 상태 섹션과 100 ECU 전수표(각 ECU 상태 명시)를 추가하고 Placeholder 승격 전 미추적 원칙을 명시. |
| 3.29 | 2026-03-09 | OEM100 병렬 문서화 정책 반영: `00e` 6.4를 100 ECU 단일 정의 기준으로 연결하고, node 표에 `DATC/TMU/SCC` 활성 전개 상태를 추가. Placeholder는 미구현 유지/승격 후 편입 원칙 명시. |
| 3.28 | 2026-03-09 | Architecture reset baseline 반영: `0301`을 surface ECU owner 언어(`CGW/BCM/IVI/CLU/ADAS/V2X`) 기준으로 재작성하고, 상세/감사 표에 `Surface ECU + Runtime/Transition Baseline` 2층 추적을 추가. |
| 3.27 | 2026-03-06 | Legacy 누락군 보강: `Req_018/036/038/039/114/115/117/122/124` 상속 관계를 `2-2` 섹션으로 추가해 Req-Func 감사 추적을 보강. |
| 3.26 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `Func_148~Func_155`를 상세표/Req-Func 매핑/핵심 시나리오 체인에 추가하고 `Req_148~Req_155` 추적 경로를 고정. |
| 3.25 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `Func_140~Func_147`를 상세표/Req-Func 매핑/핵심 시나리오 체인에 추가하고 `Req_140~Req_147` 추적 경로를 고정. |
| 3.24 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `Func_130~Func_139`를 상세표/Req-Func 매핑/핵심 시나리오 체인에 추가하고 `Req_130~Req_139` 추적 경로를 고정. |
| 3.23 | 2026-03-06 | 미사용 체인 정리: `Req_108/Func_108`(운전자 상태 전달) 매핑 행을 삭제하고 01/03/0303/0304/04/05/06/07 기준과 동기화. |
| 3.22 | 2026-03-05 | ECU 명명 거버넌스를 `00e(SoT)+03(ECU 참조)`로 정리하고, RTE 규칙은 `00g`/`04` 적용 체계로 분리. |
| 3.20 | 2026-03-05 | Validation Harness 노드 명칭을 `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`로 정리하고 `VAL_*` 접두 규칙으로 표기 통일. |
| 3.19 | 2026-03-03 | ETH_SW 역할을 시스템 관점으로 명확화하고, 구현 관점(헬스 모니터링)은 04 문서에서 분리 관리하도록 정합화. |
| 3.18 | 2026-03-03 | V2 확장 `Func_121/Func_123` 노드 소유를 `WARN_ARB_MGR`로 정정하고, 노드 표/Req-Func/시나리오 체인을 코드 구현 기준으로 동기화. |
| 3.17 | 2026-03-02 | 감사 정합 보강: 문서 범위를 `Func_001~Func_127,Func_128,Func_129`로 명확화하고 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구를 추가. |
| 3.16 | 2026-03-02 | V2 확장 제어 책임 분리: `DECEL_ASSIST_CTRL` 노드를 Chassis에 추가하고 `Func_121/Func_123` 실제 노드/시나리오 체인을 갱신. |
| 3.15 | 2026-03-02 | V2 확장(Pre-Activation) 반영: `Func_120~Func_121, Func_123, Func_125~Func_129`(근접위험/감속보조/동기화/운전자개입해제/도메인단절강등) 상세표, Req-Func 매핑, 시나리오 체인 추가. |
| 3.14 | 2026-03-02 | `Func_101~Func_119` 상세표의 입출력 변수를 0304 표준 Name으로 정합화(`BaseScenarioId/BaseScenarioResult`, `AcCompressorReq`, `DoorUnlockCmd`, `ImmoState`, `TtsLangId` 등)하고 누락 변수명을 제거. |
| 3.13 | 2026-03-02 | V2 추적 밀도 보강 1차: `Req_113~Req_119`에 대응하는 `Func_113~Func_119`(DATC/Seat/Mirror/Door/Wiper-Rain/Security/Audio)를 하단 상세표 및 1:1 감사 매핑에 추가. 상단 노드 설명도 기본 기능 확장 범위로 정합화. |
| 2.0 | 2026-02-25 | 프로젝트 최신 스코프 기준 전면 재작성. 노드별 Input-Processing-Output 구조, Func/Req 연결, 핵심 시나리오 체인, 0302 연계 체크포인트 추가 |
| 3.0 | 2026-02-25 | 상단 공식 표준 양식 반영, 하단 상세 추적 표 분리 |
| 3.1 | 2026-02-25 | 상단 표를 이미지 표준 구조로 재정렬, 도메인 묶음(Powertrain/Chassis/Body/Infotainment/Actual Device) 반영 |
| 3.2 | 2026-02-25 | 상단 헤더를 표준(기능 상세)로 정렬, Actual Device를 실제 장치 기준으로 수정, Func_013~016 추적 보완 |
| 3.3 | 2026-02-25 | 옵션1 아키텍처 기준으로 Network Infra 노드(ETH_SW/도메인 GW)와 네트워크 전달 체인 섹션 추가 |
| 3.4 | 2026-02-25 | Req_001~Req_043 / Func_001~Func_043 1:1 감사용 매핑 표(개별 행) 추가 |
| 3.5 | 2026-02-26 | Cluster 출력 전달체인을 Infotainment CAN 경로로 정합화(IVI_GW -> CLU_HMI_CTRL) |
| 3.6 | 2026-02-26 | 0304 표준 변수명 기준으로 상세 표기 통일(`g*` 별칭 제거) |
| 3.7 | 2026-02-28 | 03/0304 정합 기준으로 하단 상세표 입출력 변수를 재정렬(비정의 변수 제거, Core/State 변수명 통일) |
| 3.8 | 2026-02-28 | 스쿨존 과속 판정 정합을 위해 NAV/ADAS 입력에 `speedLimit/speedLimitNorm`을 반영하고 Navigation Panel 입력 항목을 확장. |
| 3.9 | 2026-02-28 | ISO/OEM 정합을 위한 ECU 명명 기준 섹션을 추가하고 노드 접미사 규칙(GW/CTRL/MGR/TX/RX)을 명문화. |
| 3.10 | 2026-02-28 | 차량 기본 기능 확장 대응으로 기본 차량 ECU 노드와 Req_101~Req_112 / Func_101~Func_112 매핑을 추가. |
| 3.11 | 2026-02-28 | 03 문서와의 노드 정합을 위해 `VAL_BASELINE_CTRL`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR`를 상단 공식 노드 표에 추가. |
| 3.12 | 2026-03-01 | 멘토 피드백 반영: EMS 노드를 단일 논리 단말(`EMS_ALERT`)로 통합 표기하고, 내부 TX/RX 모듈은 하단 감사 보강표로 분리. |
