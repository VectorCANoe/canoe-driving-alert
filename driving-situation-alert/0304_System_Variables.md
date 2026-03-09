# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 / SWE.3
**Version**: 2.29
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2/SWE.3) | `0304_System_Variables.md` | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0304.md`)과 동일하게 `ID/Namespace/Name/Data type/Min/Max/Initial Value/Description` 열만 사용한다.
- 상단 표의 `Namespace`는 도메인명(`Chassis/Infotainment/V2X/Core/Body/Cluster/Test`)을 사용하고, `Name`은 순수 기능 변수명으로 유지한다.
- 통신 계층/버스 경로/구현 식별자(`*_CAN_IN`, `*_ETH_CORE`, `*_CAN_OUT`)는 하단 매핑 표와 추적표에서 관리한다.
- 하단 추적표에서 `Var -> Comm -> Flow -> Func -> Req` 추적 연결을 명시하고, 누락 없는 커버리지 기준으로 N:M 매핑을 허용한다.
- DBC 신호명이 OEM 관례(`gVehicleSpeed`, `gRoadZone`)를 사용하더라도, 상단 표준 Name은 기능 중심 이름(`vehicleSpeed`, `roadZone`)으로 유지한다.
- 제출 전 현대/기아 및 OEM 기준 명칭으로 일괄 대체하되, Var ID/추적 ID 체계는 유지한다.
- `Namespace=Test` 변수는 Validation Harness 전용(Non-Production)으로 관리하며, 사용자 기능/양산 기능 변수와 구분한다.
- EMS 관련 변수는 상위 문서 계층에서 논리 단말 `EMS_ALERT` 기준으로 관리하고, 내부 TX/RX 모듈 분해는 하단 보강 매핑에서만 관리한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- V2 확장 변수(`Req_120~Req_121, Req_123, Req_125~Req_129`)는 구현 활성 상태로 추적하며, 0302/0303/05~07과 코드/DBC를 동일 커밋에서 동기화한다.
- ADAS 객체 인지 확장 변수(`Req_130~Req_139`)는 `Var_330~Var_339` Pre-Activation(설계 선반영) 상태로 추적하며, 구현 착수 시 0302/0303/04/05/06/07과 동일 커밋에서 동기화한다.
- 차량 경보 편의 확장 변수(`Req_140~Req_147`)는 `Var_009/012/024/029/133/138~141/155/164/166~168/191~193/268/281/282` Pre-Activation 매핑으로 추적하며, 구현 착수 시 0302/0303/04/05/06/07과 동일 커밋에서 동기화한다.
- 경고 강건성·인지성 확장 변수(`Req_148~Req_155`)는 `Var_330/333/334`, `Var_016/020/021/024/027/028`, `Var_180/326/327/328`, `Var_166/167/168/268/269/289/296/297` Pre-Activation 매핑으로 추적하며, 구현 착수 시 0302/0303/04/05/06/07과 동일 커밋에서 동기화한다.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- SoT 계층은 분리 관리한다: CAN 실프레임은 도메인 DBC(`chassis_can.dbc`/`powertrain_can.dbc`/`body_can.dbc`/`infotainment_can.dbc`/`adas_can.dbc` + `eth_backbone_can_stub.dbc`)를 따르고, Validation 결과 프레임(`0x2A5`,`0x2A6`)은 `chassis_can.dbc`에 통합 관리한다. Ethernet 논리 계약은 `ETH_INTERFACE_CONTRACT.md`를 따른다.
- OEM100 Surface ECU 전체 전수(100개)와 구현 상태(`활성/미구현`)는 `00e` 6.4를 단일 기준으로 사용한다.
- 본 문서는 활성(상세 정의) Surface ECU의 변수 계약만 상세 정의하고, 미구현(Placeholder) Surface ECU는 변수 owner를 강제하지 않는다.

---

## OEM100 Surface ECU 적용 상태 (0304 기준)
| 구분 | 내용 |
|---|---|
| 기준 SoT | `00e_ECU_Naming_Standard.md` 6.4 (100 ECU 전수표) |
| 전체 Surface ECU | 100 |
| 활성(상세 정의) | 99 |
| 미구현(Placeholder) | 1 |

### OEM100 전수표 (100개)

| Surface ECU | Group | Domain Bucket | Surface Type | 구현 상태 | Runtime Binding | 문서 반영 정책 |
|---|---|---|---|---|---|---|
| `CGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `CGW` | 추적체인 반영 대상 |
| `ETH_BACKBONE` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `ETH_SW(Health/Freshness monitor)` | 추적체인 반영 대상 |
| `DCM` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `DCM` | 추적체인 반영 대상 |
| `IBOX` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `IBOX` | 추적체인 반영 대상 |
| `SGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `SGW` | 추적체인 반영 대상 |
| `EMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EMS` | 추적체인 반영 대상 |
| `TCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `TCU` | 추적체인 반영 대상 |
| `VCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `VCU` | 추적체인 반영 대상 |
| `_4WD` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `_4WD` | 추적체인 반영 대상 |
| `BAT_BMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `BAT_BMS` | 추적체인 반영 대상 |
| `FPCM` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `FPCM` | 추적체인 반영 대상 |
| `LVR` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `LVR` | 추적체인 반영 대상 |
| `ISG` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `ISG` | 추적체인 반영 대상 |
| `EOP` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EOP` | 추적체인 반영 대상 |
| `EWP` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EWP` | 추적체인 반영 대상 |
| `ESC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ESC` | 추적체인 반영 대상 |
| `MDPS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `MDPS` | 추적체인 반영 대상 |
| `ABS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ABS` | 추적체인 반영 대상 |
| `EPB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `EPB` | 추적체인 반영 대상 |
| `TPMS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `TPMS` | 추적체인 반영 대상 |
| `SAS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `SAS` | 추적체인 반영 대상 |
| `ECS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ECS` | 추적체인 반영 대상 |
| `ACU` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ACU` | 추적체인 반영 대상 |
| `ODS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ODS` | 추적체인 반영 대상 |
| `VSM` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `VSM` | 추적체인 반영 대상 |
| `EHB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `EHB` | 추적체인 반영 대상 |
| `CDC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `CDC` | 추적체인 반영 대상 |
| `BCM` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `BCM` | 추적체인 반영 대상 |
| `DATC` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DATC` | 추적체인 반영 대상 |
| `SMK` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SMK` | 추적체인 반영 대상 |
| `AFLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `AFLS` | 추적체인 반영 대상 |
| `AHLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `AHLS` | 추적체인 반영 대상 |
| `WIPER_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `WIPER_MODULE` | 추적체인 반영 대상 |
| `SUNROOF_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SUNROOF_MODULE` | 추적체인 반영 대상 |
| `DOOR_FL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_FL` | 추적체인 반영 대상 |
| `DOOR_FR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_FR` | 추적체인 반영 대상 |
| `DOOR_RL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_RL` | 추적체인 반영 대상 |
| `DOOR_RR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_RR` | 추적체인 반영 대상 |
| `TAILGATE_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `TAILGATE_MODULE` | 추적체인 반영 대상 |
| `SEAT_DRV` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SEAT_DRV` | 추적체인 반영 대상 |
| `SEAT_PASS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SEAT_PASS` | 추적체인 반영 대상 |
| `MIRROR_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `MIRROR_MODULE` | 추적체인 반영 대상 |
| `BODY_SECURITY_MODULE` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `BODY_SECURITY_MODULE` | 추적체인 반영 대상 |
| `IVI` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `IVI` | 추적체인 반영 대상 |
| `CLU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `CLU` | 추적체인 반영 대상 |
| `HUD` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `HUD` | 추적체인 반영 대상 |
| `TMU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `TMU` | 추적체인 반영 대상 |
| `AMP` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `AMP` | 추적체인 반영 대상 |
| `PGS` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `PGS` | 추적체인 반영 대상 |
| `NAV_MODULE` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `NAV_MODULE` | 추적체인 반영 대상 |
| `VOICE_ASSIST` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `VOICE_ASSIST` | 추적체인 반영 대상 |
| `RSE` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `RSE` | 추적체인 반영 대상 |
| `DIGITAL_KEY` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `DIGITAL_KEY` | 추적체인 반영 대상 |
| `ADAS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `ADAS` | 추적체인 반영 대상 |
| `V2X` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `V2X` | 추적체인 반영 대상 |
| `SCC` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `SCC` | 추적체인 반영 대상 |
| `LDWS_LKAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `LDWS_LKAS` | 추적체인 반영 대상 |
| `FCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `FCA` | 추적체인 반영 대상 |
| `BCW` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `BCW` | 추적체인 반영 대상 |
| `LCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `LCA` | 추적체인 반영 대상 |
| `SPAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `SPAS` | 추적체인 반영 대상 |
| `RSPA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `RSPA` | 추적체인 반영 대상 |
| `AVM` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `AVM` | 추적체인 반영 대상 |
| `FCAM` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `FCAM` | 추적체인 반영 대상 |
| `FRADAR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `FRADAR` | 추적체인 반영 대상 |
| `SRR_FL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_FL` | 추적체인 반영 대상 |
| `SRR_FR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_FR` | 추적체인 반영 대상 |
| `SRR_RL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_RL` | 추적체인 반영 대상 |
| `SRR_RR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_RR` | 추적체인 반영 대상 |
| `PARK_ULTRASONIC` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `PARK_ULTRASONIC` | 추적체인 반영 대상 |
| `DMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `DMS` | 추적체인 반영 대상 |
| `OMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `OMS` | 추적체인 반영 대상 |
| `VALIDATION_HARNESS` | B | Validation | VALIDATION | 활성(상세 정의) | `VAL_SCENARIO_CTRL + VAL_BASELINE_CTRL` | 추적체인 반영 대상 |
| `OBC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `OBC` | 추적체인 반영 대상 |
| `DCDC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `DCDC` | 추적체인 반영 대상 |
| `MCU` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `MCU` | 추적체인 반영 대상 |
| `INVERTER` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `INVERTER` | 추적체인 반영 대상 |
| `CHARGE_PORT_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `CHARGE_PORT_CTRL` | 추적체인 반영 대상 |
| `AIR_SUSPENSION` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `AIR_SUSPENSION` | 추적체인 반영 대상 |
| `RWS` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `RWS` | 추적체인 반영 대상 |
| `NIGHT_VISION` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AEB_DOMAIN` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `AEB_DOMAIN` | 추적체인 반영 대상 |
| `HIGHWAY_PILOT` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `HIGHWAY_PILOT` | 추적체인 반영 대상 |
| `PARK_MASTER` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `PARK_MASTER` | 추적체인 반영 대상 |
| `TRAILER_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `TRAILER_CTRL` | 추적체인 반영 대상 |
| `HEADLAMP_LEVELING` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `HEADLAMP_LEVELING` | 추적체인 반영 대상 |
| `AUTO_DOOR_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `AUTO_DOOR_CTRL` | 추적체인 반영 대상 |
| `POWER_TAILGATE_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `POWER_TAILGATE_CTRL` | 추적체인 반영 대상 |
| `MASSAGE_SEAT_CTRL` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `MASSAGE_SEAT_CTRL` | 추적체인 반영 대상 |
| `REAR_CLIMATE_MODULE` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `REAR_CLIMATE_MODULE` | 추적체인 반영 대상 |
| `CABIN_SENSING` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `CABIN_SENSING` | 추적체인 반영 대상 |
| `BIOMETRIC_AUTH` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `BIOMETRIC_AUTH` | 추적체인 반영 대상 |
| `CARPAY_CTRL` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `CARPAY_CTRL` | 추적체인 반영 대상 |
| `PHONE_AS_KEY` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `PHONE_AS_KEY` | 추적체인 반영 대상 |
| `OTA_MASTER` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `OTA_MASTER` | 추적체인 반영 대상 |
| `EDR` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `EDR` | 추적체인 반영 대상 |
| `ROAD_PREVIEW_CAMERA` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `ROAD_PREVIEW_CAMERA` | 추적체인 반영 대상 |
| `LIDAR` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `LIDAR` | 추적체인 반영 대상 |
| `REAR_RADAR_MASTER` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `REAR_RADAR_MASTER` | 추적체인 반영 대상 |
| `SURROUND_PARK_MASTER` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `SURROUND_PARK_MASTER` | 추적체인 반영 대상 |


- Placeholder ECU는 승격 전까지 상세 추적(Req/Func/Flow/Comm/Var/Test)을 강제하지 않는다.
- Placeholder ECU 승격 시 `03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07` 순서로 동일 커밋 편입한다.
---

## 시스템 변수 표 (공식 표준 양식)

| ID | Namespace | Name | Data type | Min | Max | Initial Value | Description |
|---|---|---|---|---|---|---|---|
| 1 | Chassis | vehicleSpeed | uint32 | 0 | 255 | 0 | 차량 속도 입력값 |
| 2 | Chassis | driveState | uint32 | 0 | 3 | 0 | 주행 상태(P/R/N/D) 입력값 |
| 3 | Chassis | steeringInput | uint32 | 0 | 1 | 0 | 조향 입력 여부 |
| 4 | Infotainment | roadZone | uint32 | 0 | 3 | 0 | 구간 타입 입력값 |
| 5 | Infotainment | navDirection | uint32 | 0 | 3 | 0 | 내비게이션 방향 정보 |
| 6 | Infotainment | zoneDistance | uint32 | 0 | 255 | 0 | 구간 잔여 거리 |
| 30 | Infotainment | speedLimit | uint32 | 0 | 255 | 30 | 구간 제한속도(km/h) |
| 7 | V2X | emergencyType | uint32 | 0 | 3 | 0 | 긴급차량 종류 |
| 8 | V2X | emergencyDirection | uint32 | 0 | 3 | 0 | 긴급차량 접근 방향 |
| 9 | V2X | eta | uint32 | 0 | 255 | 0 | 긴급차량 ETA(유효값 0~255, 내부 invalid sentinel 65535) |
| 10 | V2X | sourceId | uint32 | 0 | 255 | 0 | 긴급 메시지 Source ID |
| 11 | V2X | alertState | uint32 | 0 | 1 | 0 | 긴급 메시지 Active/Clear 상태 |
| 12 | Core | vehicleSpeedNorm | uint32 | 0 | 255 | 0 | 게이트웨이 정규화 후 차량 속도 |
| 13 | Core | driveStateNorm | uint32 | 0 | 3 | 0 | 게이트웨이 정규화 후 주행 상태 |
| 14 | Core | steeringInputNorm | uint32 | 0 | 1 | 0 | 게이트웨이 정규화 후 조향 입력 |
| 31 | Core | speedLimitNorm | uint32 | 0 | 255 | 30 | 게이트웨이 정규화 후 구간 제한속도 |
| 32 | Core | proximityRiskLevel | uint32 | 0 | 100 | 0 | 긴급차량 근접 위험도 산정값 |
| 33 | Core | decelAssistReq | uint32 | 0 | 1 | 0 | 감속 보조 요청 플래그 |
| 34 | Core | failSafeMode | uint32 | 0 | 2 | 0 | 도메인 경로 단절 강등 모드 |
| 35 | CoreState | domainPathStatus | uint32 | 0 | 2 | 0 | 도메인 경로 상태(정상/열화/단절) |
| 36 | CoreState | e2eHealthState | uint32 | 0 | 2 | 0 | E2E 경로 헬스 상태 |
| 37 | Core | brakePedalNorm | uint32 | 0 | 100 | 0 | CHS_GW에서 정규화한 브레이크 입력 |
| 38 | Test | forceFailSafe | uint32 | 0 | 1 | 0 | Fail-safe 강제 주입(Validation-only) |
| 49 | Test | displayModeSetting | uint32 | 0 | 2 | 0 | 표시 모드 수동 설정 입력(Validation-only) |
| 50 | Test | alertVolumeSetting | uint32 | 0 | 100 | 50 | 경고 음량 수동 설정 입력(Validation-only) |
| 51 | Test | seatBeltOverride | uint32 | 0 | 2 | 0 | 안전벨트 상태 오버라이드 입력(Validation-only) |
| 52 | Test | historyQueryOffset | uint32 | 0 | 255 | 0 | 경고 이력 조회 오프셋 입력(Validation-only) |
| 53 | Test | historyQueryCode | uint32 | 0 | 65535 | 0 | 경고 이력 조회 코드 입력(Validation-only) |
| 39 | Core | objectTrackValid | uint32 | 0 | 1 | 0 | 객체 추적 유효 플래그 |
| 40 | Core | objectRange | uint32 | 0 | 500 | 0 | 대표 위험 객체 상대 거리(m) |
| 41 | Core | objectRelSpeed | int32 | -200 | 200 | 0 | 대표 위험 객체 상대 속도(km/h) |
| 42 | Core | objectConfidence | uint32 | 0 | 100 | 0 | 객체 인지 신뢰도(%) |
| 43 | Core | objectRiskClass | uint32 | 0 | 7 | 0 | 객체 위험 분류 코드 |
| 44 | Core | objectTtcMin | uint32 | 0 | 10000 | 10000 | 대표 위험 객체 최소 TTC(ms) |
| 45 | Core | intersectionConflictFlag | uint32 | 0 | 1 | 0 | 교차로 측방 접근 충돌 플래그 |
| 46 | Core | mergeCutInFlag | uint32 | 0 | 1 | 0 | 합류/끼어들기 급간섭 플래그 |
| 47 | Core | objectAlertHoldMs | uint32 | 0 | 5000 | 300 | 객체 추적 손실 시 경고 유지시간(ms) |
| 48 | Core | objectEventCode | uint32 | 0 | 65535 | 0 | 객체 기반 경고 이벤트 코드 |
| 15 | Core | baseZoneContext | uint32 | 0 | 255 | 0 | 구간 컨텍스트 계산 결과 |
| 16 | Core | warningState | uint32 | 0 | 255 | 0 | 경고 조건 판정 상태 |
| 17 | Core | emergencyContext | uint32 | 0 | 255 | 0 | 긴급 수신 컨텍스트 상태 |
| 18 | Core | selectedAlertLevel | uint32 | 0 | 7 | 0 | 중재 결과 경고 레벨 |
| 19 | Core | selectedAlertType | uint32 | 0 | 7 | 0 | 중재 결과 경고 타입 |
| 20 | Core | timeoutClear | uint32 | 0 | 1 | 0 | 1000ms 무갱신 해제 플래그 |
| 21 | Body | ambientMode | uint32 | 0 | 7 | 0 | 앰비언트 제어 모드 |
| 22 | Body | ambientColor | uint32 | 0 | 7 | 0 | 앰비언트 색상 코드 |
| 23 | Body | ambientPattern | uint32 | 0 | 3 | 0 | 앰비언트 패턴 코드 |
| 24 | Cluster | warningTextCode | uint32 | 0 | 255 | 0 | 클러스터 경고 코드 |
| 25 | Test | testScenario | uint32 | 0 | 255 | 0 | SIL 테스트 시나리오 선택값(Validation-only) |
| 26 | Test | scenarioResult | uint32 | 0 | 1 | 0 | SIL 시나리오 Pass/Fail 결과(Validation-only) |
| 27 | CoreState | lastEmergencyRxMs | uint32 | 0 | 4294967295 | 0 | 마지막 긴급 신호 수신 시각(ms) |
| 28 | CoreState | duplicatePopupGuard | uint32 | 0 | 5000 | 0 | 중복 팝업 억제 타이머(ms) |
| 29 | CoreState | arbitrationSnapshotId | uint32 | 0 | 65535 | 0 | 중재 스냅샷 식별자 |
| 101 | Chassis | AccelPedal | uint32 | 0 | 100 | 0 | 가속 페달 입력 |
| 102 | Chassis | BrakePedal | uint32 | 0 | 100 | 0 | 브레이크 페달 입력 |
| 103 | Chassis | SteeringState | uint32 | 0 | 3 | 0 | 조향 상태 |
| 104 | Chassis | WheelSpdFL | uint32 | 0 | 255 | 0 | 전륜 좌 휠속도 |
| 105 | Chassis | WheelSpdFR | uint32 | 0 | 255 | 0 | 전륜 우 휠속도 |
| 106 | Chassis | WheelSpdRL | uint32 | 0 | 255 | 0 | 후륜 좌 휠속도 |
| 107 | Chassis | WheelSpdRR | uint32 | 0 | 255 | 0 | 후륜 우 휠속도 |
| 108 | Chassis | YawRate | uint32 | 0 | 65535 | 0 | 요레이트 |
| 109 | Chassis | LatAccel | uint32 | 0 | 65535 | 0 | 횡가속도 |
| 110 | Chassis | BrakePressure | uint32 | 0 | 255 | 0 | 브레이크 압력 |
| 111 | Chassis | BrakeMode | uint32 | 0 | 3 | 0 | 브레이크 동작 모드 |
| 112 | Chassis | AbsActive | uint32 | 0 | 1 | 0 | ABS 활성 상태 |
| 113 | Chassis | EspActive | uint32 | 0 | 1 | 0 | ESC 활성 상태 |
| 114 | Chassis | AccelRequest | uint32 | 0 | 100 | 0 | 가속 요청 |
| 115 | Chassis | TorqueRequest | uint32 | 0 | 255 | 0 | 토크 요청 |
| 116 | Chassis | SteeringTorque | uint32 | 0 | 4095 | 0 | 조향 토크 |
| 117 | Chassis | SteeringAssistLv | uint32 | 0 | 15 | 0 | 조향 보조 레벨 |
| 118 | Chassis | ChassisAliveCnt | uint32 | 0 | 255 | 0 | Chassis Alive Counter |
| 119 | Chassis | ChassisDiagState | uint32 | 0 | 15 | 0 | Chassis 진단 상태 |
| 120 | Chassis | ChassisFailCode | uint32 | 0 | 15 | 0 | Chassis 오류 코드 |
| 121 | Body | HazardSwitch | uint32 | 0 | 1 | 0 | 비상등 스위치 |
| 122 | Body | HazardState | uint32 | 0 | 1 | 0 | 비상등 상태 |
| 123 | Body | WindowCommand | uint32 | 0 | 3 | 0 | 창문 제어 명령 |
| 124 | Body | WindowState | uint32 | 0 | 3 | 0 | 창문 상태 |
| 127 | Body | DoorStateMask | uint32 | 0 | 255 | 0 | 도어 상태 비트맵 |
| 128 | Body | DoorLockState | uint32 | 0 | 3 | 0 | 도어 잠금 상태 |
| 129 | Body | ChildLockState | uint32 | 0 | 1 | 0 | 아동 잠금 상태 |
| 130 | Body | DoorOpenWarn | uint32 | 0 | 1 | 0 | 도어 열림 경고 |
| 131 | Body | HeadLampState | uint32 | 0 | 3 | 0 | 전조등 상태 |
| 132 | Body | TailLampState | uint32 | 0 | 3 | 0 | 후미등 상태 |
| 133 | Body | TurnLampState | uint32 | 0 | 3 | 0 | 방향지시등 상태 |
| 134 | Body | HazardLampReq | uint32 | 0 | 1 | 0 | 비상등 요청 |
| 135 | Body | FrontWiperState | uint32 | 0 | 3 | 0 | 전면 와이퍼 상태 |
| 136 | Body | RearWiperState | uint32 | 0 | 3 | 0 | 후면 와이퍼 상태 |
| 137 | Body | WiperInterval | uint32 | 0 | 15 | 0 | 와이퍼 인터벌 |
| 138 | Body | DriverSeatBelt | uint32 | 0 | 1 | 0 | 운전석 안전벨트 상태 |
| 139 | Body | PassengerSeatBelt | uint32 | 0 | 1 | 0 | 동승석 안전벨트 상태 |
| 140 | Body | RearSeatBelt | uint32 | 0 | 3 | 0 | 후석 안전벨트 상태 |
| 141 | Body | SeatBeltWarnLvl | uint32 | 0 | 3 | 0 | 안전벨트 경고 레벨 |
| 142 | Body | CabinTemp | uint32 | 0 | 100 | 0 | 실내 온도 |
| 143 | Body | AirQualityIndex | uint32 | 0 | 255 | 0 | 실내 공기질 지수 |
| 144 | Body | BodyAliveCnt | uint32 | 0 | 255 | 0 | Body Alive Counter |
| 145 | Body | BodyDiagState | uint32 | 0 | 15 | 0 | Body 진단 상태 |
| 146 | Body | BodyFailCode | uint32 | 0 | 15 | 0 | Body 오류 코드 |
| 147 | Cluster | ClusterSpeed | uint32 | 0 | 255 | 0 | 클러스터 표시 속도 |
| 148 | Cluster | ClusterGear | uint32 | 0 | 7 | 0 | 클러스터 표시 기어 |
| 149 | Cluster | ClusterStatus | uint32 | 0 | 31 | 0 | 클러스터 기본 상태 |
| 150 | Infotainment | GuideLaneState | uint32 | 0 | 3 | 0 | 유도선 상태 |
| 151 | Infotainment | GuideConfidence | uint32 | 0 | 63 | 0 | 유도 신뢰도 |
| 152 | Infotainment | MediaSource | uint32 | 0 | 7 | 0 | 미디어 소스 |
| 153 | Infotainment | MediaState | uint32 | 0 | 7 | 0 | 미디어 재생 상태 |
| 154 | Infotainment | MuteState | uint32 | 0 | 1 | 0 | 음소거 상태 |
| 155 | Infotainment | VolumeLevel | uint32 | 0 | 100 | 0 | 볼륨 레벨 |
| 156 | Infotainment | CallState | uint32 | 0 | 7 | 0 | 통화 상태 |
| 157 | Infotainment | MicMute | uint32 | 0 | 1 | 0 | 마이크 음소거 |
| 158 | Infotainment | SignalQuality | uint32 | 0 | 15 | 0 | 통신 품질 |
| 159 | Infotainment | BtDeviceCount | uint32 | 0 | 15 | 0 | 블루투스 연결 수 |
| 160 | Infotainment | RouteClass | uint32 | 0 | 3 | 0 | 경로 분류 |
| 161 | Infotainment | GuideType | uint32 | 0 | 3 | 0 | 안내 유형 |
| 162 | Infotainment | RouteProgress | uint32 | 0 | 100 | 0 | 경로 진행률 |
| 163 | Infotainment | EtaMinutes | uint32 | 0 | 255 | 0 | 도착 예상 시간(분) |
| 164 | Cluster | ThemeMode | uint32 | 0 | 7 | 0 | 클러스터 테마 모드 |
| 165 | Cluster | ClusterBrightness | uint32 | 0 | 31 | 0 | 클러스터 밝기 |
| 166 | Cluster | PopupType | uint32 | 0 | 15 | 0 | 팝업 유형 |
| 167 | Cluster | PopupPriority | uint32 | 0 | 7 | 0 | 팝업 우선순위 |
| 168 | Cluster | PopupActive | uint32 | 0 | 1 | 0 | 팝업 활성 상태 |
| 169 | Infotainment | InfoAliveCnt | uint32 | 0 | 255 | 0 | Infotainment Alive Counter |
| 170 | Infotainment | InfoDiagState | uint32 | 0 | 15 | 0 | Infotainment 진단 상태 |
| 171 | Infotainment | InfoFailCode | uint32 | 0 | 15 | 0 | Infotainment 오류 코드 |
| 172 | Test | BaseScenarioId | uint32 | 0 | 255 | 0 | 기본 시나리오 ID |
| 173 | Test | BaseScenarioResult | uint32 | 0 | 1 | 0 | 기본 시나리오 판정 |
| 174 | Test | TimeoutClearMon | uint32 | 0 | 1 | 0 | 타임아웃 모니터 플래그 |
| 175 | Powertrain | IgnitionState | uint32 | 0 | 1 | 0 | 시동 입력 상태 |
| 176 | Powertrain | EngineState | uint32 | 0 | 3 | 0 | 엔진 동작 상태 |
| 177 | Powertrain | GearInput | uint32 | 0 | 7 | 0 | 기어 입력값 |
| 178 | Powertrain | GearState | uint32 | 0 | 7 | 0 | 기어 상태값 |
| 179 | Powertrain | RoutingPolicy | uint32 | 0 | 255 | 0 | 도메인 라우팅 정책 |
| 180 | Powertrain | BoundaryStatus | uint32 | 0 | 255 | 0 | 도메인 경계 상태 |
| 181 | Powertrain | EngineRpm | uint32 | 0 | 65535 | 0 | 엔진 회전수 |
| 182 | Powertrain | CoolantTemp | uint32 | 0 | 255 | 0 | 냉각수 온도 |
| 183 | Powertrain | OilTemp | uint32 | 0 | 255 | 0 | 엔진오일 온도 |
| 184 | Powertrain | FuelLevel | uint32 | 0 | 100 | 0 | 연료 잔량 |
| 185 | Powertrain | BatterySoc | uint32 | 0 | 100 | 0 | 배터리 SOC |
| 186 | Powertrain | ChargingState | uint32 | 0 | 3 | 0 | 충전 상태 |
| 187 | Powertrain | ThrottlePos | uint32 | 0 | 100 | 0 | 스로틀 위치 |
| 188 | Powertrain | ThrottleReq | uint32 | 0 | 100 | 0 | 스로틀 요청 |
| 189 | Powertrain | TransOilTemp | uint32 | 0 | 255 | 0 | 변속기 오일 온도 |
| 190 | Powertrain | ClutchTemp | uint32 | 0 | 255 | 0 | 클러치 온도 |
| 191 | Powertrain | DriveMode | uint32 | 0 | 7 | 0 | 주행 모드 |
| 192 | Powertrain | EcoMode | uint32 | 0 | 1 | 0 | 에코 모드 |
| 193 | Powertrain | SportMode | uint32 | 0 | 1 | 0 | 스포츠 모드 |
| 194 | Powertrain | SnowMode | uint32 | 0 | 1 | 0 | 스노우 모드 |
| 195 | Powertrain | PowertrainState | uint32 | 0 | 255 | 0 | 파워트레인 상태 |
| 196 | Powertrain | TorqueLimit | uint32 | 0 | 255 | 0 | 토크 제한값 |
| 197 | Powertrain | SpeedLimit | uint32 | 0 | 255 | 30 | 속도 제한값 |
| 198 | Powertrain | CruiseState | uint32 | 0 | 3 | 0 | 크루즈 상태 |
| 199 | Powertrain | GapLevel | uint32 | 0 | 3 | 0 | 차간 거리 레벨 |
| 200 | Powertrain | CruiseSetSpeed | uint32 | 0 | 255 | 0 | 크루즈 설정 속도 |
| 201 | Powertrain | PtAliveCnt | uint32 | 0 | 255 | 0 | Powertrain Alive Counter |
| 202 | Powertrain | PtDiagState | uint32 | 0 | 15 | 0 | Powertrain 진단 상태 |
| 203 | Powertrain | PtFailCode | uint32 | 0 | 15 | 0 | Powertrain 오류 코드 |
| 204 | Chassis | EpsAssistState | uint32 | 0 | 7 | 0 | MDPS 보조 상태 |
| 205 | Chassis | EpsFault | uint32 | 0 | 1 | 0 | MDPS 고장 상태 |
| 206 | Chassis | EpsTorqueReq | uint32 | 0 | 255 | 0 | MDPS 토크 요청 |
| 207 | Chassis | AbsCtrlState | uint32 | 0 | 7 | 0 | ABS 제어 상태 |
| 208 | Chassis | AbsSlipLevel | uint32 | 0 | 255 | 0 | ABS 슬립 레벨 |
| 209 | Chassis | EscCtrlState | uint32 | 0 | 7 | 0 | ESC 제어 상태 |
| 210 | Chassis | YawCtrlReq | uint32 | 0 | 255 | 0 | 요 모멘트 제어 요구 |
| 211 | Chassis | TcsActive | uint32 | 0 | 1 | 0 | TCS 활성 상태 |
| 212 | Chassis | TcsSlipRatio | uint32 | 0 | 255 | 0 | TCS 슬립 비율 |
| 213 | Chassis | BrakeTempFL | uint32 | 0 | 255 | 0 | 브레이크 전륜좌 온도 |
| 214 | Chassis | BrakeTempFR | uint32 | 0 | 255 | 0 | 브레이크 전륜우 온도 |
| 215 | Chassis | BrakeTempRL | uint32 | 0 | 255 | 0 | 브레이크 후륜좌 온도 |
| 216 | Chassis | BrakeTempRR | uint32 | 0 | 255 | 0 | 브레이크 후륜우 온도 |
| 217 | Chassis | SteeringAngle | int32 | -720 | 720 | 0 | 조향각 |
| 218 | Chassis | SteeringAngleRate | int32 | -1024 | 1023 | 0 | 조향각속도 |
| 219 | Chassis | WheelPulseFL | uint32 | 0 | 65535 | 0 | 전륜좌 휠 펄스 |
| 220 | Chassis | WheelPulseFR | uint32 | 0 | 65535 | 0 | 전륜우 휠 펄스 |
| 221 | Chassis | DamperMode | uint32 | 0 | 7 | 0 | 댐퍼 모드 |
| 222 | Chassis | RideHeight | uint32 | 0 | 255 | 0 | 차고 높이 |
| 223 | Chassis | TirePressFL | uint32 | 0 | 255 | 0 | 전륜좌 타이어 압력 |
| 224 | Chassis | TirePressFR | uint32 | 0 | 255 | 0 | 전륜우 타이어 압력 |
| 225 | Chassis | TirePressRL | uint32 | 0 | 255 | 0 | 후륜좌 타이어 압력 |
| 226 | Chassis | TirePressRR | uint32 | 0 | 255 | 0 | 후륜우 타이어 압력 |
| 227 | Chassis | ChassisDiagReqId | uint32 | 0 | 255 | 0 | Chassis 진단 요청 ID |
| 228 | Chassis | ChassisDiagReqAct | uint32 | 0 | 1 | 0 | Chassis 진단 요청 활성 |
| 229 | Chassis | ChassisDiagResId | uint32 | 0 | 255 | 0 | Chassis 진단 응답 ID |
| 230 | Chassis | ChassisDiagStatus | uint32 | 0 | 15 | 0 | Chassis 진단 결과 |
| 231 | Chassis | AdasChassisState | uint32 | 0 | 255 | 0 | ADAS 섀시 상태 코드 |
| 232 | Chassis | AdasHealthLevel | uint32 | 0 | 255 | 0 | ADAS 헬스 상태 코드 |
| 234 | Chassis | BrakePadWearFL | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜좌) |
| 235 | Chassis | BrakePadWearFR | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜우) |
| 236 | Chassis | RoadFrictionEst | uint32 | 0 | 255 | 0 | 노면 마찰 추정치 |
| 237 | Chassis | SurfaceType | uint32 | 0 | 15 | 0 | 노면 타입 |
| 238 | Body | CabinSetTemp | uint32 | 0 | 63 | 0 | 실내 설정 온도 |
| 239 | Body | BlowerLevel | uint32 | 0 | 15 | 0 | 블로워 레벨 |
| 240 | Body | VentMode | uint32 | 0 | 7 | 0 | 공조 벤트 모드 |
| 241 | Body | AcCompressorReq | uint32 | 0 | 1 | 0 | A/C 컴프레서 요청 |
| 242 | Body | MirrorFoldState | uint32 | 0 | 1 | 0 | 미러 폴딩 상태 |
| 243 | Body | MirrorHeatState | uint32 | 0 | 1 | 0 | 미러 열선 상태 |
| 244 | Body | MirrorAdjAxis | uint32 | 0 | 3 | 0 | 미러 조정 축 |
| 245 | Body | DriverSeatPos | uint32 | 0 | 255 | 0 | 운전석 시트 위치 |
| 246 | Body | PassengerSeatPos | uint32 | 0 | 255 | 0 | 동승석 시트 위치 |
| 247 | Body | SeatHeatLevel | uint32 | 0 | 7 | 0 | 시트 히터 레벨 |
| 248 | Body | SeatVentLevel | uint32 | 0 | 7 | 0 | 시트 통풍 레벨 |
| 249 | Body | DoorUnlockCmd | uint32 | 0 | 3 | 0 | 도어 언락 명령 |
| 250 | Body | TrunkOpenCmd | uint32 | 0 | 1 | 0 | 트렁크 오픈 명령 |
| 251 | Body | InteriorLampMode | uint32 | 0 | 7 | 0 | 실내등 모드 |
| 252 | Body | InteriorLampLevel | uint32 | 0 | 255 | 0 | 실내등 밝기 |
| 253 | Body | RainSensorLevel | uint32 | 0 | 255 | 0 | 우적 센서 레벨 |
| 254 | Body | AutoHeadlampReq | uint32 | 0 | 1 | 0 | 오토 헤드램프 요청 |
| 255 | Body | BcmDiagReqId | uint32 | 0 | 255 | 0 | BCM 진단 요청 ID |
| 256 | Body | BcmDiagReqAct | uint32 | 0 | 1 | 0 | BCM 진단 요청 활성 |
| 257 | Body | BcmDiagResId | uint32 | 0 | 255 | 0 | BCM 진단 응답 ID |
| 258 | Body | BcmDiagStatus | uint32 | 0 | 15 | 0 | BCM 진단 결과 |
| 259 | Body | ImmoState | uint32 | 0 | 3 | 0 | 이모빌라이저 상태 |
| 260 | Body | KeyAuthState | uint32 | 0 | 3 | 0 | 키 인증 상태 |
| 261 | Body | AlarmArmed | uint32 | 0 | 1 | 0 | 알람 경계 상태 |
| 262 | Body | AlarmTrigger | uint32 | 0 | 1 | 0 | 알람 트리거 상태 |
| 263 | Body | AlarmZone | uint32 | 0 | 15 | 0 | 알람 존 정보 |
| 264 | Body | BodyGatewayLoad | uint32 | 0 | 100 | 0 | Body GW 부하율 |
| 265 | Body | BodyGatewayRoute | uint32 | 0 | 255 | 0 | Body GW 라우팅 상태 |
| 266 | Body | ComfortMode | uint32 | 0 | 7 | 0 | 컴포트 모드 |
| 267 | Body | ChildSafetyState | uint32 | 0 | 1 | 0 | 아동 안전 상태 |
| 268 | Infotainment | AudioFocusOwner | uint32 | 0 | 7 | 0 | 오디오 포커스 소유자 |
| 269 | Infotainment | AudioDuckLevel | uint32 | 0 | 255 | 0 | 오디오 덕킹 레벨 |
| 270 | Infotainment | VoiceAssistState | uint32 | 0 | 7 | 0 | 음성비서 상태 |
| 271 | Infotainment | VoiceWakeSource | uint32 | 0 | 15 | 0 | 음성 깨우기 소스 |
| 272 | Infotainment | MapZoomLevel | uint32 | 0 | 255 | 0 | 지도 줌 레벨 |
| 273 | Infotainment | MapTheme | uint32 | 0 | 15 | 0 | 지도 테마 |
| 274 | Infotainment | NextTurnType | uint32 | 0 | 15 | 0 | 다음 회전 유형 |
| 275 | Infotainment | NextTurnDist | uint32 | 0 | 255 | 0 | 다음 회전 잔여 거리 |
| 276 | Infotainment | TrafficEventType | uint32 | 0 | 15 | 0 | 교통 이벤트 유형 |
| 277 | Infotainment | TrafficSeverity | uint32 | 0 | 7 | 0 | 교통 이벤트 심각도 |
| 278 | Infotainment | TrafficDist | uint32 | 0 | 255 | 0 | 이벤트 잔여 거리 |
| 279 | Infotainment | ProjectionType | uint32 | 0 | 7 | 0 | 프로젝션 유형 |
| 280 | Infotainment | ProjectionState | uint32 | 0 | 3 | 0 | 프로젝션 상태 |
| 281 | Cluster | ClusterNotifType | uint32 | 0 | 15 | 0 | 클러스터 알림 유형 |
| 282 | Cluster | ClusterNotifPrio | uint32 | 0 | 7 | 0 | 클러스터 알림 우선순위 |
| 283 | Infotainment | IviDiagReqId | uint32 | 0 | 255 | 0 | IVI 진단 요청 ID |
| 284 | Infotainment | IviDiagReqAct | uint32 | 0 | 1 | 0 | IVI 진단 요청 활성 |
| 285 | Infotainment | IviDiagResId | uint32 | 0 | 255 | 0 | IVI 진단 응답 ID |
| 286 | Infotainment | IviDiagStatus | uint32 | 0 | 15 | 0 | IVI 진단 결과 |
| 287 | Infotainment | MediaGenre | uint32 | 0 | 15 | 0 | 미디어 장르 |
| 288 | Infotainment | TrackProgress | uint32 | 0 | 100 | 0 | 트랙 진행률 |
| 289 | Infotainment | TtsState | uint32 | 0 | 7 | 0 | TTS 상태 |
| 290 | Infotainment | TtsLangId | uint32 | 0 | 255 | 0 | TTS 언어 ID |
| 291 | Infotainment | LteState | uint32 | 0 | 7 | 0 | LTE 연결 상태 |
| 292 | Infotainment | WifiState | uint32 | 0 | 1 | 0 | Wi-Fi 연결 상태 |
| 293 | Infotainment | BtState | uint32 | 0 | 1 | 0 | Bluetooth 연결 상태 |
| 294 | Infotainment | CpuLoad | uint32 | 0 | 100 | 0 | IVI CPU 부하율 |
| 295 | Infotainment | MemLoad | uint32 | 0 | 100 | 0 | IVI 메모리 부하율 |
| 296 | Cluster | ClusterSyncState | uint32 | 0 | 7 | 0 | 클러스터 동기화 상태 |
| 297 | Cluster | ClusterSyncSeq | uint32 | 0 | 255 | 0 | 클러스터 동기화 시퀀스 |
| 298 | Powertrain | EngineTorqueAct | uint32 | 0 | 65535 | 0 | 엔진 실제 토크 |
| 299 | Powertrain | EngineTorqueReq | uint32 | 0 | 65535 | 0 | 엔진 요구 토크 |
| 300 | Powertrain | EngineLoad | uint32 | 0 | 100 | 0 | 엔진 부하율 |
| 301 | Powertrain | ManifoldPressure | uint32 | 0 | 255 | 0 | 흡기 매니폴드 압력 |
| 302 | Powertrain | ShiftState | uint32 | 0 | 7 | 0 | 변속 상태 |
| 303 | Powertrain | ShiftInProgress | uint32 | 0 | 1 | 0 | 변속 진행 상태 |
| 304 | Powertrain | ShiftTargetGear | uint32 | 0 | 7 | 0 | 목표 기어 |
| 305 | Powertrain | PtDiagReqId | uint32 | 0 | 255 | 0 | Powertrain 진단 요청 ID |
| 306 | Powertrain | PtDiagReqAct | uint32 | 0 | 1 | 0 | Powertrain 진단 요청 활성 |
| 307 | Powertrain | PtDiagResId | uint32 | 0 | 255 | 0 | Powertrain 진단 응답 ID |
| 308 | Powertrain | PtDiagStatus | uint32 | 0 | 15 | 0 | Powertrain 진단 결과 |
| 309 | Powertrain | ThermalMode | uint32 | 0 | 7 | 0 | 열관리 모드 |
| 310 | Powertrain | FanSpeedCmd | uint32 | 0 | 255 | 0 | 팬 속도 명령 |
| 311 | Powertrain | RegenLevel | uint32 | 0 | 15 | 0 | 회생 제동 레벨 |
| 312 | Powertrain | EnergyFlowDir | uint32 | 0 | 3 | 0 | 에너지 흐름 방향 |
| 313 | Powertrain | PtCtrlAuthState | uint32 | 0 | 3 | 0 | 파워트레인 제어 권한 상태 |
| 314 | Powertrain | PtCtrlSource | uint32 | 0 | 15 | 0 | 파워트레인 제어 출처 |
---

## 표준 Name-내부 구현 Name 매핑 표

| ID | Namespace(표준) | Name(표준) | Internal Name(구현) | 계층 | Bus Path |
|---|---|---|---|---|---|
| 1 | Chassis | vehicleSpeed | vehicleSpeed_CAN_IN | CAN_IN | Chassis CAN -> CHS_GW |
| 2 | Chassis | driveState | driveState_CAN_IN | CAN_IN | Chassis CAN -> CHS_GW |
| 3 | Chassis | steeringInput | steeringInput_CAN_IN | CAN_IN | Chassis CAN -> CHS_GW |
| 4 | Infotainment | roadZone | roadZone_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 5 | Infotainment | navDirection | navDirection_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 6 | Infotainment | zoneDistance | zoneDistance_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 30 | Infotainment | speedLimit | speedLimit_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 7 | V2X | emergencyType | emergencyType_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT(Rx) |
| 8 | V2X | emergencyDirection | emergencyDirection_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT(Rx) |
| 9 | V2X | eta | eta_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT(Rx) |
| 10 | V2X | sourceId | sourceId_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT(Rx) |
| 11 | V2X | alertState | alertState_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT(Rx) |
| 12 | Core | vehicleSpeedNorm | vehicleSpeed_ETH_CORE | ETH_CORE | CHS_GW -> ETH_SW -> ADAS_WARN_CTRL |
| 13 | Core | driveStateNorm | driveState_ETH_CORE | ETH_CORE | CHS_GW -> ETH_SW -> ADAS_WARN_CTRL |
| 14 | Core | steeringInputNorm | steeringInput_ETH_CORE | ETH_CORE | CHS_GW -> ETH_SW -> ADAS_WARN_CTRL |
| 31 | Core | speedLimitNorm | speedLimit_ETH_CORE | ETH_CORE | INFOTAINMENT_GW -> ETH_SW -> NAV_CTX_MGR/ADAS_WARN_CTRL |
| 15 | Core | baseZoneContext | baseZoneContext_ETH_CORE | ETH_CORE | INFOTAINMENT_GW -> ETH_SW -> NAV_CTX_MGR |
| 16 | Core | warningState | warningState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL 내부 계산 |
| 17 | Core | emergencyContext | emergencyContext_ETH_CORE | ETH_CORE | EMS_ALERT 내부 계산 |
| 18 | Core | selectedAlertLevel | selectedAlertLevel_ETH_CORE | ETH_CORE | WARN_ARB_MGR 내부 계산 |
| 19 | Core | selectedAlertType | selectedAlertType_ETH_CORE | ETH_CORE | WARN_ARB_MGR 내부 계산 |
| 20 | Core | timeoutClear | timeoutClear_ETH_CORE | ETH_CORE | EMS_ALERT 생성 -> WARN_ARB_MGR 소비(타임아웃 해제) |
| 21 | Body | ambientMode | ambientMode_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SW -> BODY_GW -> AMBIENT_CTRL |
| 22 | Body | ambientColor | ambientColor_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SW -> BODY_GW -> AMBIENT_CTRL |
| 23 | Body | ambientPattern | ambientPattern_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SW -> BODY_GW -> AMBIENT_CTRL |
| 24 | Cluster | warningTextCode | warningTextCode_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SW -> IVI_GW -> CLU_HMI_CTRL |
| 25 | Test | testScenario | testScenario_INPUT | TEST | VAL_SCENARIO_CTRL Panel Input (Validation-only) |
| 26 | Test | scenarioResult | scenarioResult_OUTPUT | TEST | VAL_SCENARIO_CTRL Test Result Output (Validation-only) |
| 49 | Test | displayModeSetting | displayModeSetting_TEST_INPUT | TEST | Panel/Test 입력 -> BODY_GW, IVI_GW, CLU_HMI_CTRL(Validation-only) |
| 50 | Test | alertVolumeSetting | alertVolumeSetting_TEST_INPUT | TEST | Panel/Test 입력 -> BODY_GW, IVI_GW, CLU_HMI_CTRL(Validation-only) |
| 51 | Test | seatBeltOverride | seatBeltOverride_TEST_INPUT | TEST | Panel/Test 입력 -> BODY_GW, WARN_ARB_MGR(Validation-only) |
| 52 | Test | historyQueryOffset | historyQueryOffset_TEST_INPUT | TEST | Panel/Test 입력 -> CLU_HMI_CTRL(Validation-only) |
| 53 | Test | historyQueryCode | historyQueryCode_TEST_INPUT | TEST | Panel/Test 입력 -> CLU_HMI_CTRL(Validation-only) |
| 27 | CoreState | lastEmergencyRxMs | lastEmergencyRxMs | CORE_STATE | EMS_ALERT 내부 상태 |
| 28 | CoreState | duplicatePopupGuard | duplicatePopupGuard | CORE_STATE | CLU_HMI_CTRL 내부 상태 |
| 29 | CoreState | arbitrationSnapshotId | arbitrationSnapshotId | CORE_STATE | WARN_ARB_MGR 내부 상태 |

---

## DBC Signal Alias 매핑 (OEM 관례 대응)

| 표준 Name(문서) | DBC Signal Name | 비고 |
|---|---|---|
| vehicleSpeed | gVehicleSpeed | CAN 입력 신호(0x2A0) |
| driveState | gDriveState | CAN 입력 신호(0x2A0) |
| roadZone | gRoadZone | CAN 입력 신호(0x2A3) |
| navDirection | gNavDirection | CAN 입력 신호(0x2A3) |
| zoneDistance | gZoneDistance | CAN 입력 신호(0x2A3) |
| speedLimit | gSpeedLimit | CAN 입력 신호(0x2A3) |
| steeringInput | SteeringInput | CAN 입력 신호(0x2A1) |

- 기준: 문서 추적은 표준 Name으로 고정하고, DBC/코드 구현은 Alias 병기로 연결한다.

### EMS 논리 단말-내부 모듈 매핑 (감사 보강)

| 논리 단말(Owner 표기) | 내부 구현 모듈 | 변수 처리 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 이벤트 송신 payload 생성 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 이벤트 송신 payload 생성 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 이벤트 수신/해제/타임아웃 상태 관리 |

---

## 변수 구현 속성 보강 표 (Unit/Scale/Endian/Invalid)

| Name(표준) | Internal Name(구현) | Unit | Scale | Endian | Invalid Value | 비고 |
|---|---|---|---|---|---|---|
| vehicleSpeed | vehicleSpeed_CAN_IN | km/h | 1 | Little | 255 | 센서 단절 시 최대값 예약 |
| driveState | driveState_CAN_IN | enum | 1 | Little | 255 | 0:P,1:R,2:N,3:D |
| steeringInput | steeringInput_CAN_IN | bool | 1 | Little | 255 | 0/1 외 값은 invalid |
| roadZone | roadZone_CAN_IN | enum | 1 | Little | 255 | 0:일반,1:스쿨존,2:고속,3:유도 |
| navDirection | navDirection_CAN_IN | enum | 1 | Little | 255 | 0:없음,1:좌,2:우,3:기타 |
| zoneDistance | zoneDistance_CAN_IN | m | 1 | Little | 65535 | 거리 미수신 시 invalid |
| speedLimit | speedLimit_CAN_IN | km/h | 1 | Little | 255 | 구간 제한속도 미수신 시 기본값 30 적용 |
| emergencyType | emergencyType_ETH_IN | enum | 1 | Little | 255 | 0:none,1:police,2:ambulance |
| emergencyDirection | emergencyDirection_ETH_IN | enum | 1 | Little | 255 | 0:front,1:left,2:right,3:rear |
| eta | eta_ETH_IN | s | 1 | Little | 65535 | 유효범위 0~255, 내부 처리에서 65535를 invalid sentinel로 사용 |
| sourceId | sourceId_ETH_IN | id | 1 | Little | 65535 | 송신원 미식별 값 |
| alertState | alertState_ETH_IN | bool | 1 | Little | 255 | 0:clear,1:active |
| vehicleSpeedNorm | vehicleSpeed_ETH_CORE | km/h | 1 | Little | 255 | GW 정규화 후 값 |
| driveStateNorm | driveState_ETH_CORE | enum | 1 | Little | 255 | GW 정규화 후 값 |
| steeringInputNorm | steeringInput_ETH_CORE | bool | 1 | Little | 255 | GW 정규화 후 값 |
| speedLimitNorm | speedLimit_ETH_CORE | km/h | 1 | Little | 255 | 과속 판정 비교용 정규화 제한속도 |
| baseZoneContext | baseZoneContext_ETH_CORE | context_id | 1 | Little | 65535 | 컨텍스트 계산 실패 값 |
| warningState | warningState_ETH_CORE | state_id | 1 | Little | 65535 | 경고 판정 실패 값 |
| emergencyContext | emergencyContext_ETH_CORE | state_id | 1 | Little | 65535 | 긴급 컨텍스트 미유효 값 |
| selectedAlertLevel | selectedAlertLevel_ETH_CORE | level | 1 | Little | 255 | 0~7 이외 invalid |
| selectedAlertType | selectedAlertType_ETH_CORE | type | 1 | Little | 255 | 0~7 이외 invalid |
| timeoutClear | timeoutClear_ETH_CORE | bool | 1 | Little | 255 | 0/1 외 값 invalid |
| ambientMode | ambientMode_CAN_OUT | mode | 1 | Little | 255 | 안전 기본값은 0 |
| ambientColor | ambientColor_CAN_OUT | color_id | 1 | Little | 255 | palette 외 값 invalid |
| ambientPattern | ambientPattern_CAN_OUT | pattern_id | 1 | Little | 255 | 패턴 코드 외 invalid |
| warningTextCode | warningTextCode_CAN_OUT | text_id | 1 | Little | 65535 | 메시지 테이블 미매칭 값 |
| testScenario | testScenario_INPUT | scenario_id | 1 | Little | 65535 | 미등록 시나리오 값 |
| scenarioResult | scenarioResult_OUTPUT | bool | 1 | Little | 255 | 0:fail,1:pass |
| lastEmergencyRxMs | lastEmergencyRxMs | ms | 1 | Little | 4294967295 | 타임스탬프 미기록 값 |
| duplicatePopupGuard | duplicatePopupGuard | ms | 1 | Little | 4294967295 | 타이머 비활성 예약값 |
| arbitrationSnapshotId | arbitrationSnapshotId | seq | 1 | Little | 4294967295 | 스냅샷 미생성 값 |

---

## 변수 추적 상세 표 (Var/Comm/Flow/Func/Req)

| Var ID | 표준 Name | Internal Name | 계층 | Owner Node | Comm ID | Flow ID | Func ID | Req ID | 갱신 규칙 |
|---|---|---|---|---|---|---|---|---|---|
| Var_001 | vehicleSpeed | vehicleSpeed_CAN_IN | CAN_IN | CHS_GW | Comm_001 | Flow_001 | Func_001, Func_010 | Req_001, Req_010 | 100ms CAN 수신 시 갱신 |
| Var_002 | driveState | driveState_CAN_IN | CAN_IN | CHS_GW | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | 100ms CAN 수신 시 갱신 |
| Var_003 | steeringInput | steeringInput_CAN_IN | CAN_IN | CHS_GW | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | 100ms CAN 수신 시 갱신 |
| Var_004 | roadZone | roadZone_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_005 | navDirection | navDirection_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_006 | zoneDistance | zoneDistance_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_030 | speedLimit | speedLimit_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007, Func_010 | Req_007, Req_010 | 100ms CAN 수신 시 갱신(미수신 시 기본값 30) |
| Var_007 | emergencyType | emergencyType_ETH_IN | ETH_IN | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_025, Func_029 | Req_017, Req_023, Req_025, Req_029 | E100 수신 시 즉시 갱신 |
| Var_008 | emergencyDirection | emergencyDirection_ETH_IN | ETH_IN | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_020, Func_023 | Req_017, Req_020, Req_023 | E100 수신 시 즉시 갱신 |
| Var_009 | eta | eta_ETH_IN | ETH_IN | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_030, Func_143 | Req_017, Req_023, Req_030, Req_143 | E100 수신 시 즉시 갱신 |
| Var_010 | sourceId | sourceId_ETH_IN | ETH_IN | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_031 | Req_017, Req_023, Req_031 | E100 수신 시 즉시 갱신 |
| Var_011 | alertState | alertState_ETH_IN | ETH_IN | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_023, Req_024 | Active/Clear 변화 시 갱신 |
| Var_012 | vehicleSpeedNorm | vehicleSpeed_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_003, Func_004, Func_006, Func_010, Func_143 | Req_001, Req_003, Req_004, Req_006, Req_010, Req_143 | CHS_GW 변환 메시지 수신 시 갱신 |
| Var_013 | driveStateNorm | driveState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | CHS_GW 변환 메시지 수신 시 갱신 |
| Var_014 | steeringInputNorm | steeringInput_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | CHS_GW 변환 메시지 수신 시 갱신 |
| Var_031 | speedLimitNorm | speedLimit_ETH_CORE | ETH_CORE | NAV_CTX_MGR | Comm_003 | Flow_003 | Func_007, Func_010 | Req_007, Req_010 | NAV 입력 수신 시 정규화 갱신(기본값 30) |
| Var_015 | baseZoneContext | baseZoneContext_ETH_CORE | ETH_CORE | NAV_CTX_MGR | Comm_003 | Flow_003 | Func_007 | Req_007 | NAV 컨텍스트 계산 후 갱신 |
| Var_016 | warningState | warningState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001, Comm_002, Comm_006 | Flow_001, Flow_002, Flow_006 | Func_003, Func_004, Func_006, Func_010, Func_011, Func_012, Func_027, Func_149, Func_150 | Req_003, Req_004, Req_006, Req_010, Req_011, Req_012, Req_027, Req_149, Req_150 | 경고 조건 계산/신선도 보호/전이 안정화 시 갱신 |
| Var_017 | emergencyContext | emergencyContext_ETH_CORE | ETH_CORE | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_023, Req_024 | E100 수신/해제/타임아웃 시 갱신 |
| Var_018 | selectedAlertLevel | selectedAlertLevel_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025, Func_026, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032, Func_150, Func_152 | Req_022, Req_025, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032, Req_150, Req_152 | 중재 결과 생성/전이 안정화/대체 출력 정책 적용 시 갱신 |
| Var_019 | selectedAlertType | selectedAlertType_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025, Func_026, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032, Func_150, Func_152, Func_155 | Req_022, Req_025, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032, Req_150, Req_152, Req_155 | 중재 결과 생성/전이 안정화/대체 출력 정책 및 채널 동기 기준 반영 시 갱신 |
| Var_020 | timeoutClear | timeoutClear_ETH_CORE | ETH_CORE | EMS_ALERT | Comm_006 | Flow_006 | Func_024, Func_033, Func_034, Func_149 | Req_024, Req_033, Req_034, Req_149 | 1000ms 무갱신 시 1로 전환(WARN_ARB_MGR 전달), stale 보호 정책 입력으로 반영 |
| Var_021 | ambientMode | ambientMode_CAN_OUT | CAN_OUT | BODY_GW/AMBIENT_CTRL | Comm_007 | Flow_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039, Func_152 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_037, Req_152 | 50ms 출력 주기 갱신(채널 대체 정책 반영 포함) |
| Var_022 | ambientColor | ambientColor_CAN_OUT | CAN_OUT | BODY_GW/AMBIENT_CTRL | Comm_007 | Flow_007 | Func_014, Func_035, Func_037, Func_038, Func_039 | Req_014, Req_035, Req_037 | 50ms 출력 주기 갱신 |
| Var_023 | ambientPattern | ambientPattern_CAN_OUT | CAN_OUT | BODY_GW/AMBIENT_CTRL | Comm_007 | Flow_007 | Func_014, Func_015, Func_036, Func_037, Func_038, Func_039 | Req_014, Req_015, Req_035, Req_037 | 50ms 출력 주기 갱신 |
| Var_024 | warningTextCode | warningTextCode_CAN_OUT | CAN_OUT | WARN_ARB_MGR(원천), IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_008 | Flow_008 | Func_005, Func_019~Func_021, Func_026, Func_040, Func_143, Func_145, Func_146, Func_147, Func_152, Func_153, Func_154, Func_155 | Req_005, Req_019~Req_021, Req_026, Req_040, Req_143, Req_145, Req_146, Req_147, Req_152, Req_153, Req_154, Req_155 | 50ms 출력 주기 갱신(대체 출력/인지성 보호/과밀 억제/동기 복원 포함) |
| Var_025 | testScenario | testScenario_INPUT | TEST | VAL_SCENARIO_CTRL | Comm_009 | Flow_009 | Func_041, Func_042 | Req_041, Req_042 | 시나리오 시작 시 설정 |
| Var_026 | scenarioResult | scenarioResult_OUTPUT | TEST | VAL_SCENARIO_CTRL | Comm_009 | Flow_009 | Func_043 | Req_043 | 시나리오 종료 시 판정 기록 |
| Var_027 | lastEmergencyRxMs | lastEmergencyRxMs | CORE_STATE | EMS_ALERT | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_023, Func_024, Func_149 | Req_023, Req_024, Req_149 | E100 수신 시각(ms) 기록, 1000ms 타임아웃 기준 및 입력 신선도 보호 기준 |
| Var_028 | duplicatePopupGuard | duplicatePopupGuard | CORE_STATE | CLU_HMI_CTRL | Comm_008 | Flow_008 | Func_026, Func_150, Func_154 | Req_026, Req_150, Req_154 | 동일 Alert 반복 시 타이머 갱신, 전이 안정화/과밀 억제 입력으로 반영 |
| Var_029 | arbitrationSnapshotId | arbitrationSnapshotId | CORE_STATE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_032, Func_144, Func_145 | Req_032, Req_144, Req_145 | 중재 수행 시 스냅샷 ID 증가 |
| Var_BASE_A | --- Baseline Comm_101~Comm_106 추적 확장 --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Var_101 | AccelPedal | accelPedal_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_102 | BrakePedal | brakePedal_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_103 | SteeringState | steeringState_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_104 | WheelSpdFL | wheelSpdFL_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_105 | WheelSpdFR | wheelSpdFR_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_106 | WheelSpdRL | wheelSpdRL_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_107 | WheelSpdRR | wheelSpdRR_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_108 | YawRate | yawRate_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_109 | LatAccel | latAccel_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_110 | BrakePressure | brakePressure_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_111 | BrakeMode | brakeMode_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_112 | AbsActive | absActive_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_113 | EspActive | espActive_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_114 | AccelRequest | accelRequest_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_115 | TorqueRequest | torqueRequest_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_116 | SteeringTorque | steeringTorque_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_117 | SteeringAssistLv | steeringAssistLv_CAN_BASE | CAN_BASE | CHS_GW | Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | 100ms 주기 수신 시 갱신 |
| Var_118 | ChassisAliveCnt | chassisAliveCnt_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_119 | ChassisDiagState | chassisDiagState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_120 | ChassisFailCode | chassisFailCode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_121 | HazardSwitch | hazardSwitch_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_122 | HazardState | hazardState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_123 | WindowCommand | windowCommand_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_124 | WindowState | windowState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_127 | DoorStateMask | doorStateMask_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_128 | DoorLockState | doorLockState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_129 | ChildLockState | childLockState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_130 | DoorOpenWarn | doorOpenWarn_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_131 | HeadLampState | headLampState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_132 | TailLampState | tailLampState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_133 | TurnLampState | turnLampState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107, Func_140 | Req_106, Req_107, Req_140 | 100ms 주기 수신 시 갱신 |
| Var_134 | HazardLampReq | hazardLampReq_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_135 | FrontWiperState | frontWiperState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_136 | RearWiperState | rearWiperState_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_137 | WiperInterval | wiperInterval_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_138 | DriverSeatBelt | driverSeatBelt_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107, Func_142 | Req_106, Req_107, Req_142 | 100ms 주기 수신 시 갱신 |
| Var_139 | PassengerSeatBelt | passengerSeatBelt_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107, Func_142 | Req_106, Req_107, Req_142 | 100ms 주기 수신 시 갱신 |
| Var_140 | RearSeatBelt | rearSeatBelt_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107, Func_142 | Req_106, Req_107, Req_142 | 100ms 주기 수신 시 갱신 |
| Var_141 | SeatBeltWarnLvl | seatBeltWarnLvl_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107, Func_142 | Req_106, Req_107, Req_142 | 100ms 주기 수신 시 갱신 |
| Var_142 | CabinTemp | cabinTemp_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_143 | AirQualityIndex | airQualityIndex_CAN_BASE | CAN_BASE | BODY_GW | Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | 100ms 주기 수신 시 갱신 |
| Var_144 | BodyAliveCnt | bodyAliveCnt_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_145 | BodyDiagState | bodyDiagState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_146 | BodyFailCode | bodyFailCode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_147 | ClusterSpeed | clusterSpeed_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_148 | ClusterGear | clusterGear_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_149 | ClusterStatus | clusterStatus_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_150 | GuideLaneState | guideLaneState_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_151 | GuideConfidence | guideConfidence_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_152 | MediaSource | mediaSource_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_153 | MediaState | mediaState_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_154 | MuteState | muteState_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_155 | VolumeLevel | volumeLevel_CAN_BASE | CAN_BASE | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_104 | Flow_104 | Func_109, Func_147 | Req_109, Req_147 | 50ms 주기 수신 시 갱신 |
| Var_156 | CallState | callState_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_157 | MicMute | micMute_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_158 | SignalQuality | signalQuality_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_159 | BtDeviceCount | btDeviceCount_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_160 | RouteClass | routeClass_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_161 | GuideType | guideType_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_162 | RouteProgress | routeProgress_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_163 | EtaMinutes | etaMinutes_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_164 | ThemeMode | themeMode_CAN_BASE | CAN_BASE | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_104 | Flow_104 | Func_109, Func_146 | Req_109, Req_146 | 50ms 주기 수신 시 갱신 |
| Var_165 | ClusterBrightness | clusterBrightness_CAN_BASE | CAN_BASE | INFOTAINMENT_GW/IVI_GW | Comm_104 | Flow_104 | Func_109 | Req_109 | 50ms 주기 수신 시 갱신 |
| Var_166 | PopupType | popupType_CAN_BASE | CAN_BASE | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_104 | Flow_104 | Func_109, Func_146, Func_154 | Req_109, Req_146, Req_154 | 50ms 주기 수신 시 갱신(팝업 과밀 억제 입력 포함) |
| Var_167 | PopupPriority | popupPriority_CAN_BASE | CAN_BASE | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_104 | Flow_104 | Func_109, Func_146, Func_154 | Req_109, Req_146, Req_154 | 50ms 주기 수신 시 갱신(팝업 과밀 억제 입력 포함) |
| Var_168 | PopupActive | popupActive_CAN_BASE | CAN_BASE | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_104 | Flow_104 | Func_109, Func_146, Func_154 | Req_109, Req_146, Req_154 | 50ms 주기 수신 시 갱신(팝업 과밀 억제 입력 포함) |
| Var_169 | InfoAliveCnt | infoAliveCnt_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_170 | InfoDiagState | infoDiagState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_171 | InfoFailCode | infoFailCode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_172 | BaseScenarioId | baseScenarioId_CAN_BASE | CAN_BASE | VAL_SCENARIO_CTRL | Comm_106 | Flow_106 | Func_112 | Req_112 | Event 발생 시 갱신 |
| Var_173 | BaseScenarioResult | baseScenarioResult_CAN_BASE | CAN_BASE | VAL_SCENARIO_CTRL | Comm_106 | Flow_106 | Func_112 | Req_112 | Event 발생 시 갱신 |
| Var_174 | TimeoutClearMon | timeoutClearMon_CAN_BASE | CAN_BASE | VAL_SCENARIO_CTRL | Comm_106 | Flow_106 | Func_112 | Req_112 | Event 발생 시 갱신 |
| Var_175 | IgnitionState | ignitionState_CAN_BASE | CAN_BASE | ENG_CTRL/TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_176 | EngineState | engineState_CAN_BASE | CAN_BASE | ENG_CTRL/TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_177 | GearInput | gearInput_CAN_BASE | CAN_BASE | ENG_CTRL/TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_178 | GearState | gearState_CAN_BASE | CAN_BASE | ENG_CTRL/TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_179 | RoutingPolicy | routingPolicy_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_180 | BoundaryStatus | boundaryStatus_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111, Func_151 | Req_110, Req_111, Req_151 | 100ms 주기 수신 시 갱신(출력 채널 가용성 판정 입력 포함) |
| Var_181 | EngineRpm | engineRpm_CAN_BASE | CAN_BASE | ENG_CTRL | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_182 | CoolantTemp | coolantTemp_CAN_BASE | CAN_BASE | ENG_CTRL | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_183 | OilTemp | oilTemp_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_184 | FuelLevel | fuelLevel_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_185 | BatterySoc | batterySoc_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_186 | ChargingState | chargingState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_187 | ThrottlePos | throttlePos_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_188 | ThrottleReq | throttleReq_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_189 | TransOilTemp | transOilTemp_CAN_BASE | CAN_BASE | TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_190 | ClutchTemp | clutchTemp_CAN_BASE | CAN_BASE | TCU | Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | 100ms 주기 수신 시 갱신 |
| Var_191 | DriveMode | driveMode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111, Func_141 | Req_110, Req_111, Req_141 | 100ms 주기 수신 시 갱신 |
| Var_192 | EcoMode | ecoMode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111, Func_141 | Req_110, Req_111, Req_141 | 100ms 주기 수신 시 갱신 |
| Var_193 | SportMode | sportMode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111, Func_141 | Req_110, Req_111, Req_141 | 100ms 주기 수신 시 갱신 |
| Var_194 | SnowMode | snowMode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_195 | PowertrainState | powertrainState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_196 | TorqueLimit | torqueLimit_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_197 | SpeedLimit | speedLimit_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_198 | CruiseState | cruiseState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_199 | GapLevel | gapLevel_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_200 | CruiseSetSpeed | cruiseSetSpeed_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_201 | PtAliveCnt | ptAliveCnt_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_202 | PtDiagState | ptDiagState_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_203 | PtFailCode | ptFailCode_CAN_BASE | CAN_BASE | DOMAIN_ROUTER | Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | 100ms 주기 수신 시 갱신 |
| Var_BASE_B | --- Phase-B Comm_201~Comm_205 추적 확장 --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Var_204 | EpsAssistState | epsAssistState_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_205 | EpsFault | epsFault_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_206 | EpsTorqueReq | epsTorqueReq_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_207 | AbsCtrlState | absCtrlState_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_208 | AbsSlipLevel | absSlipLevel_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_209 | EscCtrlState | escCtrlState_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_210 | YawCtrlReq | yawCtrlReq_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_211 | TcsActive | tcsActive_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_212 | TcsSlipRatio | tcsSlipRatio_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_213 | BrakeTempFL | brakeTempFL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_214 | BrakeTempFR | brakeTempFR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_215 | BrakeTempRL | brakeTempRL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_216 | BrakeTempRR | brakeTempRR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_217 | SteeringAngle | steeringAngle_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_218 | SteeringAngleRate | steeringAngleRate_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_219 | WheelPulseFL | wheelPulseFL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_220 | WheelPulseFR | wheelPulseFR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_221 | DamperMode | damperMode_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_222 | RideHeight | rideHeight_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_223 | TirePressFL | tirePressFL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_224 | TirePressFR | tirePressFR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_225 | TirePressRL | tirePressRL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_226 | TirePressRR | tirePressRR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_227 | ChassisDiagReqId | chassisDiagReqId_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_228 | ChassisDiagReqAct | chassisDiagReqAct_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_229 | ChassisDiagResId | chassisDiagResId_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_230 | ChassisDiagStatus | chassisDiagStatus_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_231 | AdasChassisState | adasChassisState_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_232 | AdasHealthLevel | adasHealthLevel_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_234 | BrakePadWearFL | brakePadWearFL_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_235 | BrakePadWearFR | brakePadWearFR_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_236 | RoadFrictionEst | roadFrictionEst_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_237 | SurfaceType | surfaceType_CAN_EXT | CAN_EXT | CHS_GW | Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_238 | CabinSetTemp | cabinSetTemp_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_239 | BlowerLevel | blowerLevel_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_240 | VentMode | ventMode_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_241 | AcCompressorReq | acCompressorReq_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_242 | MirrorFoldState | mirrorFoldState_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_243 | MirrorHeatState | mirrorHeatState_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_244 | MirrorAdjAxis | mirrorAdjAxis_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_245 | DriverSeatPos | driverSeatPos_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_246 | PassengerSeatPos | passengerSeatPos_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_247 | SeatHeatLevel | seatHeatLevel_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_248 | SeatVentLevel | seatVentLevel_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_249 | DoorUnlockCmd | doorUnlockCmd_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_250 | TrunkOpenCmd | trunkOpenCmd_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_251 | InteriorLampMode | interiorLampMode_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_252 | InteriorLampLevel | interiorLampLevel_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_253 | RainSensorLevel | rainSensorLevel_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_254 | AutoHeadlampReq | autoHeadlampReq_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_255 | BcmDiagReqId | bcmDiagReqId_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_256 | BcmDiagReqAct | bcmDiagReqAct_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_257 | BcmDiagResId | bcmDiagResId_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_258 | BcmDiagStatus | bcmDiagStatus_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_259 | ImmoState | immoState_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_260 | KeyAuthState | keyAuthState_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_261 | AlarmArmed | alarmArmed_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_262 | AlarmTrigger | alarmTrigger_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_263 | AlarmZone | alarmZone_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_264 | BodyGatewayLoad | bodyGatewayLoad_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_265 | BodyGatewayRoute | bodyGatewayRoute_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_266 | ComfortMode | comfortMode_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_267 | ChildSafetyState | childSafetyState_CAN_EXT | CAN_EXT | BODY_GW | Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | 100ms 주기 수신 + Event 발생 시 갱신 |
| Var_268 | AudioFocusOwner | audioFocusOwner_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_119, Func_147, Func_153 | Req_109, Req_111, Req_119, Req_147, Req_153 | 50/100ms 주기 수신 시 갱신(오디오 경합 인지성 보호 입력 포함) |
| Var_269 | AudioDuckLevel | audioDuckLevel_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_119, Func_153 | Req_109, Req_111, Req_119, Req_153 | 50/100ms 주기 수신 시 갱신(오디오 경합 인지성 보호 입력 포함) |
| Var_270 | VoiceAssistState | voiceAssistState_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111, Func_119 | Req_109, Req_111, Req_119 | 50/100ms 주기 수신 시 갱신 |
| Var_271 | VoiceWakeSource | voiceWakeSource_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111, Func_119 | Req_109, Req_111, Req_119 | 50/100ms 주기 수신 시 갱신 |
| Var_272 | MapZoomLevel | mapZoomLevel_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_273 | MapTheme | mapTheme_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_274 | NextTurnType | nextTurnType_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_275 | NextTurnDist | nextTurnDist_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_276 | TrafficEventType | trafficEventType_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_277 | TrafficSeverity | trafficSeverity_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_278 | TrafficDist | trafficDist_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_279 | ProjectionType | projectionType_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_280 | ProjectionState | projectionState_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_281 | ClusterNotifType | clusterNotifType_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_145 | Req_109, Req_111, Req_145 | 50/100ms 주기 수신 시 갱신 |
| Var_282 | ClusterNotifPrio | clusterNotifPrio_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_145, Func_146, Func_147, Func_153, Func_154, Func_155 | Req_109, Req_111, Req_145, Req_146, Req_147, Req_153, Req_154, Req_155 | 50/100ms 주기 수신 시 갱신(인지성 보호/과밀 억제/채널 동기 출력 포함) |
| Var_283 | IviDiagReqId | iviDiagReqId_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_284 | IviDiagReqAct | iviDiagReqAct_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_285 | IviDiagResId | iviDiagResId_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_286 | IviDiagStatus | iviDiagStatus_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_287 | MediaGenre | mediaGenre_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_288 | TrackProgress | trackProgress_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_289 | TtsState | ttsState_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_119, Func_153 | Req_109, Req_111, Req_119, Req_153 | 50/100ms 주기 수신 시 갱신(오디오 경합 인지성 보호 입력 포함) |
| Var_290 | TtsLangId | ttsLangId_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111, Func_119 | Req_109, Req_111, Req_119 | 50/100ms 주기 수신 시 갱신 |
| Var_291 | LteState | lteState_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_292 | WifiState | wifiState_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_293 | BtState | btState_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_294 | CpuLoad | cpuLoad_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_295 | MemLoad | memLoad_CAN_EXT | CAN_EXT | INFOTAINMENT_GW/IVI_GW | Comm_203 | Flow_203 | Func_109, Func_111 | Req_109, Req_111 | 50/100ms 주기 수신 시 갱신 |
| Var_296 | ClusterSyncState | clusterSyncState_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_155 | Req_109, Req_111, Req_155 | 50/100ms 주기 수신 시 갱신(채널 동기 복원 입력 포함) |
| Var_297 | ClusterSyncSeq | clusterSyncSeq_CAN_EXT | CAN_EXT | IVI_GW(프레임 생성), CLU_HMI_CTRL(미러/표시 상태) | Comm_203 | Flow_203 | Func_109, Func_111, Func_155 | Req_109, Req_111, Req_155 | 50/100ms 주기 수신 시 갱신(채널 동기 복원 입력 포함) |
| Var_298 | EngineTorqueAct | engineTorqueAct_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_299 | EngineTorqueReq | engineTorqueReq_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_300 | EngineLoad | engineLoad_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_301 | ManifoldPressure | manifoldPressure_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_302 | ShiftState | shiftState_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_303 | ShiftInProgress | shiftInProgress_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_304 | ShiftTargetGear | shiftTargetGear_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_305 | PtDiagReqId | ptDiagReqId_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_306 | PtDiagReqAct | ptDiagReqAct_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_307 | PtDiagResId | ptDiagResId_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_308 | PtDiagStatus | ptDiagStatus_CAN_EXT | CAN_EXT | VAL_SCENARIO_CTRL | Comm_205 | Flow_205 | Func_112 | Req_112 | Event + 100ms 진단 프레임 수신/송신 시 갱신 |
| Var_309 | ThermalMode | thermalMode_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_310 | FanSpeedCmd | fanSpeedCmd_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_311 | RegenLevel | regenLevel_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_312 | EnergyFlowDir | energyFlowDir_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_313 | PtCtrlAuthState | ptCtrlAuthState_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_314 | PtCtrlSource | ptCtrlSource_CAN_EXT | CAN_EXT | DOMAIN_ROUTER | Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | 100ms 주기 수신 시 갱신 |
| Var_320 | proximityRiskLevel | proximityRiskLevel_ETH_V2 | ETH_V2 | ADAS_WARN_CTRL | Comm_120 | Flow_120 | Func_120 | Req_120 | 100ms 주기 위험도 산정 시 갱신 |
| Var_321 | decelAssistReq | decelAssistReq_ETH_V2 | ETH_V2 | WARN_ARB_MGR | Comm_121 | Flow_121 | Func_121, Func_123 | Req_121, Req_123 | Event + 50ms 요청/해제 시 갱신 |
| Var_322 | selectedAlertLevel | selectedAlertLevel_V2_SYNC | ETH_V2 | WARN_ARB_MGR | Comm_122 | Flow_122 | Func_125, Func_126 | Req_125, Req_126 | 50ms 주기 경고 동기화 시 갱신 |
| Var_323 | selectedAlertType | selectedAlertType_V2_SYNC | ETH_V2 | WARN_ARB_MGR | Comm_122 | Flow_122 | Func_125, Func_126 | Req_125, Req_126 | 50ms 주기 경고 동기화 시 갱신 |
| Var_324 | steeringInputNorm | steeringInputNorm_V2_RELEASE | CAN_V2 | CHS_GW | Comm_123 | Flow_123 | Func_123 | Req_123 | 운전자 개입 이벤트 수신 시 갱신 |
| Var_325 | brakePedalNorm | brakePedalNorm_V2_RELEASE | CAN_V2 | CHS_GW | Comm_123 | Flow_123 | Func_123 | Req_123 | 운전자 제동 입력 이벤트 수신 시 갱신 |
| Var_326 | domainPathStatus | domainPathStatus_V2_FAILSAFE | CAN_V2 | DOMAIN_BOUNDARY_MGR | Comm_124 | Flow_124 | Func_127, Func_128, Func_129, Func_151 | Req_127, Req_128, Req_129, Req_151 | 100ms 주기 경로상태 수신 시 갱신(채널 가용성 판정 입력 포함) |
| Var_327 | e2eHealthState | e2eHealthState_V2_FAILSAFE | CAN_V2 | DOMAIN_BOUNDARY_MGR | Comm_124 | Flow_124 | Func_127, Func_128, Func_129, Func_151 | Req_127, Req_128, Req_129, Req_151 | 100ms 주기 헬스상태 수신 시 갱신(채널 가용성 판정 입력 포함) |
| Var_328 | failSafeMode | failSafeMode_V2_FAILSAFE | ETH_V2 | DOMAIN_BOUNDARY_MGR | Comm_124 | Flow_124 | Func_127, Func_128, Func_129, Func_151, Func_152 | Req_127, Req_128, Req_129, Req_151, Req_152 | 단절 감지/가용성 판정/대체 출력 정책 적용 시 즉시 갱신 |
| Var_329 | decelAssistReq | decelAssistReq_V2_BLOCK | ETH_V2 | DOMAIN_BOUNDARY_MGR | Comm_124 | Flow_124 | Func_127, Func_128, Func_129 | Req_127, Req_128, Req_129 | failSafeMode=1 전환 시 0 강제 갱신 |
| Var_330 | objectTrackValid | objectTrackValid_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL | Comm_130 | Flow_130 | Func_130, Func_131, Func_136, Func_148 | Req_130, Req_131, Req_136, Req_148 | 객체 목록 수신 시 유효성 갱신(입력 유효성 필터링 포함) |
| Var_331 | objectRange | objectRange_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL | Comm_130 | Flow_130 | Func_130, Func_131, Func_133 | Req_130, Req_131, Req_133 | 100ms 주기 객체 거리 갱신 |
| Var_332 | objectRelSpeed | objectRelSpeed_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL | Comm_130 | Flow_130 | Func_130, Func_131, Func_133 | Req_130, Req_131, Req_133 | 100ms 주기 상대속도 갱신 |
| Var_333 | objectConfidence | objectConfidence_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL, DOMAIN_BOUNDARY_MGR | Comm_130, Comm_133 | Flow_130, Flow_133 | Func_130, Func_137, Func_148 | Req_130, Req_137, Req_148 | 객체 신뢰도 갱신 및 강등 판정 입력(유효성 필터링 포함) |
| Var_334 | objectRiskClass | objectRiskClass_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL, WARN_ARB_MGR | Comm_131, Comm_132, Comm_133 | Flow_131, Flow_132, Flow_133 | Func_131, Func_132, Func_133, Func_134, Func_135, Func_136, Func_138, Func_139, Func_148 | Req_131, Req_132, Req_133, Req_134, Req_135, Req_136, Req_138, Req_139, Req_148 | 위험 분류 갱신 시 즉시 반영(입력 유효성 필터링 포함) |
| Var_335 | objectTtcMin | objectTtcMin_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL | Comm_131 | Flow_131 | Func_131, Func_132 | Req_131, Req_132 | TTC 계산 주기(100ms) 갱신 |
| Var_336 | intersectionConflictFlag | intersectionConflictFlag_ETH_ADAS | ETH_ADAS | WARN_ARB_MGR | Comm_132 | Flow_132 | Func_134 | Req_134 | 교차로 위험 조건 성립 시 Event 갱신 |
| Var_337 | mergeCutInFlag | mergeCutInFlag_ETH_ADAS | ETH_ADAS | WARN_ARB_MGR | Comm_132 | Flow_132 | Func_135 | Req_135 | 합류/끼어들기 위험 조건 성립 시 Event 갱신 |
| Var_338 | objectAlertHoldMs | objectAlertHoldMs_ETH_ADAS | ETH_ADAS | ADAS_WARN_CTRL | Comm_131 | Flow_131 | Func_136 | Req_136 | 추적 손실 보수 유지시간 갱신 |
| Var_339 | objectEventCode | objectEventCode_ETH_ADAS | ETH_ADAS | EMS_ALERT | Comm_133 | Flow_133 | Func_138 | Req_138 | 객체 경고 발생/해제/강등 이벤트 기록 시 갱신 |

---

## Legacy Req 상속 매핑 (Var 기준)

| Legacy Req ID | Active Req ID | 상속 Var | 상속 규칙 |
|---|---|---|---|
| Req_018 | Req_017 | Var_007~Var_011 | 구급차 분리 요구는 긴급차량 접근 통합 요구(Req_017)의 입력 변수 결과를 상속한다. |
| Req_036 | Req_035 | Var_021, Var_023 | 긴급 패턴 분리 요구는 긴급 시각표현 통합 요구(Req_035)의 출력 변수 결과를 상속한다. |
| Req_038 | Req_037 | Var_021~Var_023 | 고속도로 패턴 분리 요구는 구간 패턴 통합 요구(Req_037)의 출력 변수 결과를 상속한다. |
| Req_039 | Req_037 | Var_021~Var_023 | 유도선 패턴 분리 요구는 구간 패턴 통합 요구(Req_037)의 출력 변수 결과를 상속한다. |
| Req_108 | Req_113,Req_116,Req_118 | Var_238~Var_267 | 운전자 상태 단일 레벨 전달 요구는 Body 확장 상태 통합 요구(Req_113/Req_116/Req_118)의 변수 결과를 상속한다. |
| Req_114 | Req_113 | Var_238~Var_267 | 시트 상태 단독 요구는 실내편의 통합 요구(Req_113)의 Body 확장 변수 결과를 상속한다. |
| Req_115 | Req_113 | Var_238~Var_267 | 미러 상태 단독 요구는 실내편의 통합 요구(Req_113)의 Body 확장 변수 결과를 상속한다. |
| Req_117 | Req_116 | Var_238~Var_267 | 와이퍼/우적 연동 단독 요구는 차체 제어 통합 요구(Req_116)의 Body 확장 변수 결과를 상속한다. |
| Req_122 | Req_125 | Var_322, Var_323 | 감속 보조 중 긴급 최우선 단독 요구는 V2 통합 요구(Req_125)의 출력 변수 결과를 상속한다. |
| Req_124 | Req_127,Req_128,Req_129 | Var_326, Var_327, Var_328, Var_329 | 도메인 단절 대응 단일 요구는 금지/최소유지/강등 3분할 요구의 변수 결과를 상속한다. |

---

## 0303/코드 연계 체크포인트

- `0303`의 모든 Signal은 본 문서 변수와 1개 이상 매핑되어야 하며, `Comm_101~Comm_106`, `Comm_201~Comm_205` 확장 신호도 Var 추적표에 동기화되어야 한다.
- `Comm_120~Comm_124`는 `Var_320~Var_329`와 구현 추적을 유지하고, 변경 시 0302/0303/05~07을 동일 커밋으로 동기화한다.
- `Comm_130~Comm_133`는 `Var_330~Var_339` Pre-Activation 추적을 유지하고, 구현 착수 시 0302/0303/04/05/06/07을 동일 커밋으로 동기화한다.
- `Req_140~Req_147`는 `Var_009/012/024/029/133/138~141/155/164/166~168/191~193/268/281/282` Pre-Activation 추적을 유지하고, 구현 착수 시 0302/0303/04/05/06/07을 동일 커밋으로 동기화한다.
- `Req_148~Req_155`는 `Var_330/333/334`, `Var_016/020/021/024/027/028`, `Var_180/326/327/328`, `Var_166/167/168/268/269/289/296/297` Pre-Activation 추적을 유지하고, 구현 착수 시 0302/0303/04/05/06/07을 동일 커밋으로 동기화한다.
- `Comm_004~Comm_006`, `Comm_120~Comm_124`, `Comm_201(0x1C1)` 구간은 CANoe.CAN 환경에서 `adas_can.dbc`(0x1C1/0x1C3) + `eth_backbone_can_stub.dbc`(0x1C0/0x1C2/0x1C4/0x111) 운반 경로와 논리 Ethernet 계약(`ETH_INTERFACE_CONTRACT.md`)을 동시에 만족해야 한다.
- `timeoutClear`(내부 구현: `timeoutClear_ETH_CORE`)는 `Req_024(1000ms)` 검증 로직과 직접 연결되어야 한다.
- `selectedAlertLevel`, `selectedAlertType`(내부 구현: `selectedAlertLevel_ETH_CORE`, `selectedAlertType_ETH_CORE`)는 `WARN_ARB_MGR` 출력의 단일 소스로 유지한다.
- `speedLimit`/`speedLimitNorm`은 Req_010 과속 판정 비교 입력으로 0303 Comm_003과 정합되어야 한다.
- 구현 단계에서 코드 레벨 변수 키는 `Internal Name`을 기준으로 통일하고, 문서 간 추적은 `표준 Name`과 함께 병기한다.

## Verification-Harness 변수 운영 메모 (Req 비연계)

| Namespace/Name | 용도 | 코드 기준 위치 | 관리 원칙 |
|---|---|---|---|
| `V2X/policeDispatch`, `V2X/ambulanceDispatch` | SIL Panel 수동 긴급 이벤트 주입 | `EMS_POLICE_TX.can`, `EMS_AMB_TX.can` | 제품 Req 체인 미연계(검증 자극 전용) |
| `Test/displayModeSetting`, `Test/alertVolumeSetting`, `Test/seatBeltOverride` | 표시/음량/안전벨트 검증 시나리오 제어 입력 | `BODY_GW.can`, `IVI_GW.can`, `CLU_HMI_CTRL.can` | 제품 Req 체인 미연계(Validation-only runtime control) |
| `Test/historyQueryOffset`, `Test/historyQueryCode` | 경고 이력 조회 오프셋/코드 필터 제어 입력 | `CLU_HMI_CTRL.can` | 제품 Req 체인 미연계(Validation-only runtime control) |
| `UiRender/*` | 패널 렌더링 파생 상태 전달 | `IVI_GW.can` | 제품 Req 체인 미연계(렌더 전용) |

- 본 표 항목은 `00c`의 `Verification-Harness` 분류를 따르며, 01/03의 제품 기능 요구 누락으로 판정하지 않는다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.30 | 2026-03-09 | 03~0304 정합 점검 반영: `ETH_BACKBONE` 표기(`ETH_SW(Health/Freshness monitor)`)를 통일하고, 개정 이력 `2.18` 중복 항목을 단일 행으로 병합해 버전 이력 중복을 해소. |
| 2.29 | 2026-03-09 | Dev1 최종 승격(`1fda129`) 동기화: OEM100 상태를 `99 활성/1 미구현(NIGHT_VISION)`으로 갱신하고 Var owner/상태표를 최신 runtime anchor 기준으로 반영. |
| 2.28 | 2026-03-09 | Dev1 추가 승격(`f61cb26`, rebased from `e4f69a2`) 동기화: `VSM/EHB/ECS/CDC`를 활성(상세 정의)로 전환하고 OEM100 전수표를 `38 활성/62 미구현`으로 갱신. |
| 2.27 | 2026-03-09 | Dev1 추가 승격(`2216335`) 동기화: `DOOR_FL/DOOR_FR/SEAT_DRV/SEAT_PASS`를 활성(상세 정의)로 전환하고 OEM100 전수표를 `34 활성/66 미구현`으로 갱신. |
| 2.26 | 2026-03-09 | Dev1 최신 승격(`a6fecf1`) 동기화: OEM100 전수표 상태를 30 활성/70 미구현으로 갱신하고 `0304` 문서의 OEM100 섹션을 최신화. |
| 2.25 | 2026-03-09 | OEM100 선행 문서화 반영: `00e` 6.4(100 ECU 전수) 기준을 0304에 명시하고, 활성 16/미구현 84 운영 규칙과 100 ECU 전수표(각 ECU 상태 명시), Placeholder 승격 전 미추적 원칙을 추가. |
| 2.24 | 2026-03-06 | Legacy 누락군 보강: `Req_018/036/038/039/114/115/117/122/124` 상속 관계를 `Legacy Req 상속 매핑` 섹션으로 추가해 Var 추적 누락을 해소. |
| 2.23 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `Req_148~Req_155` 매핑을 위해 `Var_330/333/334`, `Var_016/020/021/024/027/028`, `Var_180/326/327/328`, `Var_166/167/168/268/269/289/296/297` 추적 행을 확장하고 연계 체크포인트를 동기화. |
| 2.22 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `Req_140~Req_147` 매핑을 위해 `Var_009/012/024/029/133/138~141/155/164/166~168/191~193/268/281/282` 추적 행을 확장하고 연계 체크포인트를 동기화. |
| 2.21 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: 상단 변수(`ID 39~48`)와 추적 변수(`Var_330~Var_339`), `Comm_130~Comm_133` 체크포인트를 추가해 `Req_130~Req_139` 체인을 선반영. |
| 2.20 | 2026-03-06 | 용어/범위 정리: Verification-Harness 운영 메모에서 Driver 네임스페이스 자극 항목을 제거하고 제품 체인을 `고속 무조향 의심 경고` 중심으로 정렬. |
| 2.19 | 2026-03-06 | 미사용 체인 정리: `Req_108/Func_108` 연계 변수(`Var_125/Var_126`, `DriverStateLevel/DriverStateInfo` 전달 경로)를 삭제하고 Baseline 추적 범위를 `108 제외` 기준으로 동기화. |
| 2.18 | 2026-03-05 | Validation 결과 프레임(`0x2A5`,`0x2A6`)의 SoT를 `chassis_can.dbc` 통합 기준으로 갱신하고 Validation 노드 명칭을 `VAL_*`로 정리. ADAS 도메인 분리(`adas_can.dbc`)를 반영해 V2/긴급 경로의 CAN-stub 운반 규칙을 ADAS 소유(0x1C1/0x1C3)와 ETH Backbone(0x1C0/0x1C2/0x1C4/0x111)로 분리 고정. |
| 2.17 | 2026-03-04 | DBC SoT 정합 보강: 작성 원칙/체크포인트에 `eth_backbone_can_stub.dbc` + `ETH_INTERFACE_CONTRACT.md` 병행 규칙을 명시하고 V2/긴급 경로(`Comm_004~006`, `Comm_120~124`, `Comm_201(0x1C1)`)의 변수 추적 해석 기준을 고정. |
| 2.16 | 2026-03-03 | V2 변수(`Var_320~329`)를 구현 기준으로 전환: `Var_321/324/325` Owner를 `WARN_ARB_MGR/CHS_GW`로 정정하고 `brakePedalNorm`, `forceFailSafe` 상단 표준 변수를 추가. |
| 2.15 | 2026-03-02 | 감사 정합 보강: 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구를 작성 원칙에 추가. |
| 2.14 | 2026-03-02 | V2 확장 제어 책임 분리 반영: `Var_321/324/325` Owner Node를 `DECEL_ASSIST_CTRL`로 조정해 `Func_121/123`과 정합화. |
| 2.13 | 2026-03-02 | V2 확장(Pre-Activation) 변수 반영: 상단 표준 변수 `proximityRiskLevel/decelAssistReq/failSafeMode/domainPathStatus/e2eHealthState` 추가, 하단 추적 `Var_320~Var_329` 및 `Comm_120~Comm_124` 연계 추가. |
| 2.12 | 2026-03-02 | ISO26262/ASPICE 분류 정합 보강: `V2X/policeDispatch`, `V2X/ambulanceDispatch`, `Test/*`, `UiRender/*`를 Verification-Harness(Req 비연계) 운영 메모로 추가. |
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 옵션1 아키텍처 기준으로 전면 재작성. 변수 계층(CAN_IN/ETH_CORE/CAN_OUT) 분리, Var-Comm-Flow-Func-Req 추적 표 추가 |
| 2.1 | 2026-02-25 | 상단 29개 변수와 하단 추적표를 1:1 대응하도록 누락 변수(emergency*_ETH_IN, driveState_ETH_CORE, warningState_ETH_CORE, lastEmergencyRxMs) 직접 매핑 추가 |
| 2.2 | 2026-02-25 | 변수 구현 속성 보강 표(Unit/Scale/Endian/Invalid) 추가로 04 구현 시 해석 오차 방지 기준 명시 |
| 2.3 | 2026-02-25 | 상단 공식표를 도메인 Namespace + 순수 Name 구조로 정리하고, 통신/구현 식별자는 하단 매핑/추적 표로 분리 |
| 2.4 | 2026-02-28 | `timeoutClear` 생성 주체를 EMS_ALERT_RX로 명확화, `selectedAlertLevel/Type` Func/Req 범위표기를 명시 나열로 전환, `eta` 유효범위/invalid sentinel 규칙을 분리 명시 |
| 2.5 | 2026-02-28 | Nav 제한속도 변수 `speedLimit`/`speedLimitNorm` 및 Var_030/Var_031 추적 항목을 추가해 Req_010 과속 판정 체인을 보강. |
| 2.6 | 2026-02-28 | DBC OEM 신호명(`g*`)과 문서 표준 Name 간 Alias 매핑 표를 추가해 변수 명칭 혼선을 제거. |
| 2.7 | 2026-02-28 | 0303 상단 통신 신호 기준으로 시스템 변수 상단표를 확장(99 Message 연계), OEM 일괄 대체를 고려한 Namespace/Name 체계를 보강. |
| 2.8 | 2026-02-28 | 하단 변수 추적 상세표를 Comm_201~Comm_205(Flow_201~Flow_205, Func_101~Func_112, Req_101~Req_112)까지 동기화하고 Phase-B 확장 변수 추적 행을 추가. |
| 2.9 | 2026-02-28 | 하단 변수 추적 상세표를 Comm_101~Comm_106(Flow_101~Flow_106, Func_101~Func_112, Req_101~Req_112)까지 추가 동기화해 차량 기본 기능 체인을 폐쇄. |
| 2.10 | 2026-03-01 | 멘토 피드백 반영: EMS 변수 Owner/Bus Path를 논리 단말(`EMS_ALERT`) 기준으로 통합 표기하고, 내부 TX/RX 모듈은 별도 매핑 표로 분리. |
| 2.11 | 2026-03-02 | V2 추적 밀도 보강 1차: `Comm_202` 변수군에 `Req_113~Req_118`, `Func_113~Func_118` 매핑을 확장하고, Audio/Voice/TTS 변수(`Var_268/269/270/271/289/290`)에 `Req_119`, `Func_119` 연계를 추가. |
