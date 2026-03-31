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

| 항목 | 기준 |
| --- | --- |
| 표면 ECU 우선 | 상위 문서에서는 표면 ECU 이름을 우선 사용한다. |
| 구현명 제한 | 구현 상세 이름은 상위 문서의 기본 표기로 사용하지 않는다. |
| Validation 분리 | Validation Harness는 제품 기능 ECU와 분리해 관리한다. |
| 약어 기준 | 문서 전반에서는 국내 OEM 관행 약어형을 Canonical로 사용한다. |

## 3. 표기 규칙

| 구분 | 규칙 |
| --- | --- |
| Surface ECU | 업계 통용 표면 약어를 사용한다. |
| Runtime Module | 구현 이름은 필요 시 괄호로만 병기한다. |
| Validation | validation 노드는 제품 ECU와 분리해 설명한다. |
| 문서 작성 | reviewer-facing 설명은 표면 ECU 기준으로 작성한다. |

대표 표면 약어 예시는 `EMS`, `VCU`, `ESC`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `CGW`다.

## 4. Canonical 약어 기준

| 표면 약어 | Alias | 설명 |
| --- | --- | --- |
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
| `ETHB` | `ETH_BACKBONE` | Ethernet 경계 표면명 |

## 5. 주요 표면 ECU 기준

| 도메인 | 주요 표면 ECU | 설명 |
| --- | --- | --- |
| `Integration` | `CGW`, `ETHB`, `DCM`, `IBOX`, `SGW` | 경계·진단·보안 |
| `Powertrain` | `EMS`, `TCU`, `VCU`, `_4WD` | 동력·전력·충전 |
| `Chassis/Safety` | `ESC`, `MDPS`, `ABS`, `EPB` | 제동·조향·안정화 |
| `Body/Comfort` | `BCM`, `DATC`, `AFLS`, `AHLS` | 출입·조명·공조 |
| `IVI/HMI` | `IVI`, `CLU`, `HUD`, `TMU`, `AMP` | 표시·안내·연결 |
| `ADAS/V2X` | `ADAS`, `V2X`, `SCC`, `FCA` | 주행 보조·경고 |

세부 표면 ECU는 본문 `0301~0304`와 ECU metadata book을 따른다.

## 6. 문서 적용 기준

| 적용 항목 | 기준 |
| --- | --- |
| `0301`, `0302`, `0303` 상단 공식 표 | 표면 ECU 이름을 먼저 쓴다. |
| 구현 이름 병기 | 구현 이름이 필요한 경우에는 괄호 안에만 병기한다. |
| reviewer-facing 설명 | 표면 ECU 이름만 읽어도 기능 흐름을 이해할 수 있어야 한다. |
