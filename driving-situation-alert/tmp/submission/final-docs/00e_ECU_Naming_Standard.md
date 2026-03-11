# ECU 명명 및 계층 표준

**Document ID**: PROJ-00E-ECU-NAMING
**Version**: 3.9
**Date**: 2026-03-09
**Status**: Draft (Submission Summary)
**Scope**: `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05 -> 06 -> 07`

---

> 제출용 정리본: 원본 SoT에서 문서 표기에 필요한 명명 규칙과 주요 표면 ECU만 유지한 문서입니다.

## 1. 목적

본 문서는 제출 문서에서 사용할 ECU 표면 이름과 기본 명명 규칙을 정리한다.
상위 문서에서는 차량 관점의 표면 ECU 이름을 사용하고, 구현 상세 이름은 필요한 경우에만 괄호로 병기한다.

## 2. 기본 원칙

- 상위 문서에서는 표면 ECU 이름을 우선 사용한다.
- 구현 상세 이름은 상위 문서의 기본 표기로 사용하지 않는다.
- Validation Harness는 제품 기능 ECU와 분리해 관리한다.
- 문서 전반에서는 국내 OEM 관행 약어형을 Canonical로 사용한다.

## 3. 표기 규칙

| 항목 | 규칙 |
|---|---|
| Surface ECU | `EMS`, `VCU`, `ESC`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `CGW`처럼 업계 통용 약어를 사용한다. |
| Runtime Module | `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`와 같은 구현 이름은 필요 시 괄호로만 병기한다. |
| Validation | Validation 전용 노드는 production ECU와 섞지 않고 별도로 설명한다. |
| 문서 작성 | 상단 표와 reviewer-facing 설명은 표면 ECU 기준으로 읽히도록 작성한다. |

## 4. Canonical 약어 기준

| Canonical (고정) | Alias (설명용) | 비고 |
|---|---|---|
| `SGW` | `SECURITY_GATEWAY` | 보안 게이트웨이 |
| `_4WD` | `AWD_4WD` | 4WD 제어 표면명 |
| `DATC` | `HVAC` | 공조 제어 |
| `AHLS` | `LIGHTING_ECU` | 조명 제어 |
| `EDR` | `EDGE_LOGGER` | 이벤트 기록 |
| `EMS` | `ECM` | 엔진 제어 표면명 |
| `TCU` | `TCM` | 변속 제어 표면명 |
| `ESC` | `ESP` | 제동/차체 제어 표면명 |
| `MDPS` | `EPS` | 조향 제어 표면명 |
| `CLU` | `CLUSTER` | 클러스터 표면명 |

## 5. 주요 표면 ECU 기준

| Domain | 주요 표면 ECU | 설명 |
|---|---|---|
| Integration | `CGW`, `ETH_BACKBONE`, `DCM`, `IBOX`, `SGW` | 도메인 연결, 진단, 보안, 서비스 경계 역할 |
| Powertrain | `EMS`, `TCU`, `VCU`, `_4WD`, `BAT_BMS`, `OBC`, `DCDC`, `MCU`, `INVERTER` | 동력, 전력 변환, 충전, 열관리 관련 기능 |
| Chassis/Safety | `ESC`, `MDPS`, `ABS`, `EPB`, `EHB`, `VSM`, `ECS`, `CDC`, `RWS` | 제동, 조향, 차체 안정화 관련 기능 |
| Body/Comfort | `BCM`, `DATC`, `AFLS`, `AHLS`, `DOOR_FL/FR/RL/RR`, `TAILGATE_MODULE`, `SEAT_DRV`, `SEAT_PASS` | 출입, 조명, 공조, 실내 편의 관련 기능 |
| IVI/HMI | `IVI`, `CLU`, `HUD`, `TMU`, `AMP`, `NAV_MODULE`, `DIGITAL_KEY`, `RSE` | 표시, 안내, 연결 서비스 관련 기능 |
| ADAS/V2X | `ADAS`, `V2X`, `SCC`, `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `DMS`, `OMS` | 주행 보조, 주차 보조, 센서 기반 경고 기능 |

## 6. 문서 적용 기준

- `0301`, `0302`, `0303`의 상단 공식 표는 표면 ECU 이름을 먼저 쓴다.
- 구현 이름이 필요한 경우에는 괄호 안에만 병기한다.
- 제출 문서에서는 표면 ECU 이름만 읽어도 기능 흐름을 이해할 수 있어야 한다.
