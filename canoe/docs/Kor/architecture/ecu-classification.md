# ECU Classification 한글판

원문:
- [../../architecture/ecu-classification.md](../../architecture/ecu-classification.md)

## 목적

이 문서는 active CANoe SIL baseline에서 실무적으로 사용할 ECU role classification을 정의합니다.

분류 목적은 아래 네 가지를 명확히 하는 것입니다.
- 누가 runtime decision을 소유하는가
- 누가 cross-domain boundary behavior를 소유하는가
- 어떤 surface가 local feature 또는 presentation 전용인가
- 어떤 surface가 validation-only이며 product ownership 밖에 있어야 하는가

이 문서는 runtime architecture 문서입니다.
- vehicle-program inventory가 아닙니다.
- GUI regrouping guide도 아닙니다.

## 왜 필요한가

프로젝트는 아래 질문에 일관되게 답해야 합니다.
- 이 node는 product owner인가 validation harness인가
- 이 node는 contract owner인가 단순 consumer인가
- timeout / route authority는 local인가 boundary surface인가
- product runtime인가 verification system인가

이 분류가 없으면 owner, route, timeout, oracle 판단이 file-by-file 예외로 흩어집니다.

## 역할 클래스

현재 baseline은 4개 role class를 사용합니다.

| 역할 클래스 | 의미 | 대표 예 |
| --- | --- | --- |
| Gateway / Backbone | cross-domain boundary, routing, backbone health, service edge | `CGW`, `SGW`, `DCM`, `IBOX`, `ETHB` |
| Domain Runtime Owner | domain state와 주요 runtime decision의 1차 owner | `VCU`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `SCC` |
| Local Feature / Output Surface | 상위 runtime boundary 아래의 local control 또는 output surface | `ABS`, `EPB`, `AFLS`, `WIP`, `HUD`, `PGS`, `FCAM`, `SPAS` |
| Validation Harness | scenario injection, verdict aggregation, evidence support 전용 | `TEST_SCN`, `TEST_BAS` |

## 해석 규칙

### Gateway / Backbone

이 클래스는 아래 역할이 중심일 때 사용합니다.
- domain bridge
- boundary health enforcement
- cross-domain route authority
- backbone / service-edge behavior 노출

이 surface는 domain runtime owner가 가져야 할 product meaning까지 흡수하면 안 됩니다.

### Domain Runtime Owner

이 클래스는 아래 중 하나 이상을 실질적으로 소유할 때 사용합니다.
- normalized domain state
- alert / feature decision input
- major output meaning
- domain-level timeout / fail-safe behavior

contract ownership의 1차 후보는 기본적으로 이 클래스입니다.

### Local Feature / Output Surface

이 클래스는 아래 성격일 때 사용합니다.
- local control 수행
- 상위 runtime result 반영
- 좁은 범위의 feature output publish
- 최종 business meaning은 상위 owner에 의존

출력을 publish할 수는 있지만, silent하게 arbitration owner로 승격되면 안 됩니다.

### Validation Harness

이 클래스는 아래만 할 때 사용합니다.
- scenario injection
- verdict aggregation
- evidence-oriented mirror
- product behavior가 아니라 test execution 지원

validation harness는 product ECU ownership과 분리되어야 합니다.

## 현재 프로젝트 읽는 법

- `CGW`와 backbone 관련 surface: gateway / backbone
- `VCU`, `IVI`, `ADAS`, `V2X`, `BCM`, `CLU`, `SCC`: domain runtime owner
- comfort, body, chassis, parking, HMI, sensor leaf surface: local feature / output surface
- `TEST_SCN`, `TEST_BAS`: validation harness

핵심 원칙:
- product ownership과 validation ownership을 분리합니다.
- transport 위치만으로 ECU 역할을 정의하지 않습니다.
- observation, evidence, stimulus 전용 surface는 validation으로 분류합니다.
