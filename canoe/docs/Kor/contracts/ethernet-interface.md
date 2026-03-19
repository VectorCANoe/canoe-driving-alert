# ETH Interface Contract

원문:
- [../../contracts/ethernet-interface.md](../../contracts/ethernet-interface.md)

동기화 기준:
- `5d83ee7f`
- seam 이름, owner, consumer 이름, transport 값은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 active CANoe SIL profile에서 실제로 사용하는 Ethernet contract를 정의합니다.
> bit-level packing 문서가 아니라, active seam과 owner/consumer/fallback 규칙을 정리하는 운영 계약입니다.

## 1. 목적

이 문서는 active CANoe SIL profile에 대한 operational Ethernet contract를 정의합니다.

이 문서가 답하는 질문은 아래와 같습니다.

- 어떤 Ethernet seam이 active 상태인가
- 각 seam의 logical owner는 누구인가
- 누가 그 seam을 primary consumer로 읽는가
- 어떤 fallback path가 허용되는가
- 어떤 path가 validation-only seam인가

bit field, ID, signal packing 자체는 [ethernet-backbone.md](../../contracts/ethernet-backbone.md)를 기준으로 읽습니다.
owner, observer, validation, render 계층 분리는 [layer-separation-policy.md](./layer-separation-policy.md)를 기준으로 읽습니다.

## 2. Active transport baseline

현재 active backbone transport는 아래 하나로 고정합니다.

- `UDP multicast 239.0.2.1:5000`

이 transport가 현재 CANoe SIL profile의 inter-domain backbone seam입니다.
retired CAN stub seam을 primary architecture contract로 취급하면 안 됩니다.

현재 SIL validation baseline에서는 CANoe multicast runtime stack 동작에 따라 sender identity가 다르게 보일 수 있습니다.
그래서 ingress owner는 아래 원칙을 따릅니다.

- strict self-source check로 self-originated transport를 먼저 배제한다
- 문서화된 validation sender가 보이면 그 값을 우선 사용한다
- 예상과 다른 external source는 trace를 남긴 뒤 external ingress로 수용한다

## 3. Contract seam 분류

### 3.1 Input-context seam

이 seam은 raw context를 shared runtime으로 들여오는 입력 경로입니다.

| Seam | Logical owner | Primary consumer | 의도 |
| --- | --- | --- | --- |
| `ethVehicleStateMsg` | `VCU` | `CGW`, `IBOX` | vehicle speed 및 drive state context |
| `ethSteeringMsg` | `MDPS` | `CGW` | steering activity context |
| `ethNavContextMsg` | `IVI` | `CGW`, `IBOX` | road zone, direction, speed-limit context |
| `ETH_EmergencyAlert` | `V2X` | emergency-context runtime path | emergency ingress context |
| `ethObjectRiskInputMsg` | `TEST_SCN` | `ADAS` | validation-only object-risk stimulus |

### 3.2 Decision-output seam

이 seam은 arbitration 이후의 selected runtime meaning을 publish하는 출력 경로입니다.

| Seam | Logical owner | Primary consumer | 의도 |
| --- | --- | --- | --- |
| `ethSelectedAlertMsg` | `ADAS`가 active selected-alert state를 relay하는 transport seam | `BCM`, `IVI`, downstream warning consumer | 현재 boundary-shaped alert state를 반영한 selected alert result |
| `ethEmergencyRiskMsg` | `ADAS` | ADAS-side consumer, `TEST_SCN` | emergency proximity risk |
| `ethDecelAssistReqMsg` | `ADAS` | `ESC`, `TEST_SCN` | deceleration assist request |
| `ethObjectRiskStateMsg` | `ADAS` | ADAS-side consumer, `TEST_SCN` | object risk classification |
| `ethObjectScenarioAlertMsg` | `ADAS` | `BCM`, `IVI`, `TEST_SCN` | object-context warning result |

### 3.3 Boundary-health seam

이 seam은 health, degradation, observability 상태를 노출합니다.

| Seam | Logical owner | Primary consumer | 의도 |
| --- | --- | --- | --- |
| `ethFailSafeStateMsg` | `CGW` | `ADAS`, `TEST_SCN`, selected safety observer | path health 및 fail-safe mode |
| `ETH_EmergencyMonitor` | `V2X` | `TEST_SCN`, trace observer | emergency transport monitor |
| `ethObjectSafetyStateMsg` | `CGW` | `ADAS`, `TEST_SCN`, selected observer | object-path health 및 event code |

## 4. 핵심 규칙

### 4.1 Business meaning과 transport는 분리한다

- warning의 business meaning을 임시 stub 또는 mirror path에 직접 묶으면 안 됩니다.
- `ETH_EmergencyAlert`가 현재 active emergency ingress seam입니다.
- `Core::*` mirror는 SIL compatibility를 도울 수 있지만, published Ethernet contract를 대체하지 않습니다.

### 4.2 각 seam에는 logical owner를 하나만 둔다

- 각 active Ethernet seam은 current runtime에서 하나의 명확한 logical owner만 가져야 합니다.
- compatibility mirror나 observer가 추가되더라도 ownership은 바뀌지 않습니다.

### 4.3 Fallback은 문서화된 경우에만 허용한다

- 일부 downstream consumer는 fresh backbone result seam이 없을 때 `Core::*` 또는 normalized `CoreState::*` mirror로 fallback할 수 있습니다.
- 이 fallback은 documented compatibility path로만 취급합니다.
- fallback을 primary interface contract처럼 설명하면 안 됩니다.
- `ADAS`와 render node가 direction, ETA, source 메타데이터가 필요할 때는 `V2X` owner가 publish한 normalized `CoreState::*` ingress seam을 우선 사용합니다.

### 4.4 Validation-only seam은 명시적으로 남긴다

- `TEST_SCN`은 SIL validation을 위해 `ethObjectRiskInputMsg` 같은 Ethernet seam을 생성할 수 있습니다.
- 긴급차 ingress path 자체를 시험할 때는 `TEST_SCN`이 `ETH_EmergencyAlert`를 validation ingress stimulus로 emit할 수도 있습니다.
- 현재 executable baseline에서는 `V2X`가 emergency ingress를 validation injector path에서만 받고, `ADAS`도 `ethObjectRiskInputMsg`를 validation injector path에서만 받습니다.
- 그렇다고 `TEST_SCN`이 product ECU owner가 되는 것은 아닙니다.

### 4.5 Health와 timeout 상태는 boundary authority가 소유한다

health와 degradation state는 ad-hoc local guess가 아니라 boundary authority path에서 나와야 합니다.

대표 seam:
- `Core::timeoutClear`
- `CoreState::warningPathStatus`
- `CoreState::e2eHealthState`
- `CoreState::selectedAlertEffectiveLevel`
- `CoreState::selectedAlertEffectiveType`
- `CoreState::selectedAlertGateReason`
- `CoreState::driverReleaseReason`
- `V2X::ingressHeartbeat`
- `ethFailSafeStateMsg`

## 5. 사용 규칙

- seam owner를 판단할 때는 `owner-route`와 함께 읽습니다.
- cross-domain visibility 여부는 `multibus-policy`와 함께 읽습니다.
- frame/message 소유권과 source bus는 `communication-matrix`와 함께 읽습니다.
