# Multi-Bus Visibility Policy

원문:
- [../../contracts/multibus-policy.md](../../contracts/multibus-policy.md)

동기화 기준:
- `5d83ee7f`
- node 이름, DBC 이름, bus 이름은 canonical technical identifier로 유지합니다.

> [!IMPORTANT]
> 이 문서는 active SIL baseline에서 어떤 node가 추가 bus/database visibility를 가져야 하는지 정리한 핵심 계약 문서입니다.
> GUI 배치, source/mirror 배치, 실제 runtime 참여 여부를 같은 뜻으로 읽으면 안 됩니다.

## 1. 목적

이 문서는 active CANoe SIL configuration에서 node별 multibus visibility 필요 여부를 정의합니다.

이 문서가 답하는 질문은 아래와 같습니다.

- 어떤 node가 자기 primary domain 밖의 CAN database를 추가로 봐야 하는가
- 어떤 node가 GUI Ethernet runtime placement까지 유지해야 하는가
- 어떤 node는 source/mirror에서는 `ETH_Backbone` 아래에 남되, GUI Ethernet runtime은 제거해야 하는가

## 2. 핵심 원칙

1. visible surface node는 OEM-style ECU 이름을 유지합니다.
2. 추가 bus/database visibility가 필요하다고 해서 별도의 top-level gateway ECU를 새로 만드는 것은 아닙니다.
3. `Primary source/mirror placement`, `GUI Ethernet runtime placement`, `extra CAN visibility`는 서로 다른 판단 축입니다.
4. multibus assignment는 old backbone stub seam이 아니라 실제 foreign-domain CAN message visibility 필요성으로 결정합니다.
5. direct Ethernet RX ownership은 현재 baseline에서 `CGW`, `ADAS`, `V2X`, `TEST_BAS`로 제한합니다.
6. owner, observer, validation 예외는 `contracts/layer-separation-policy.md` 기준으로 해석합니다.

## 3. GUI 해석 규칙

- `Ethernet runtime placement in GUI = required`
  - GUI에서 `ETH_Backbone`을 `Assigned buses`에 유지합니다.
  - 대응 TCP/IP stack interface도 함께 유지합니다.
- `Ethernet runtime placement in GUI = not required`
  - GUI에서 `ETH_Backbone`을 `Assigned buses`에서 제거합니다.
  - IPv4만 비우고 node를 backbone에 매단 채 두는 방식으로 처리하면 안 됩니다.

## 4. Multibus가 필요한 이유

### 4.1 Cross-domain runtime dependency

- 어떤 node는 다른 domain database에서 생산된 message를 소비합니다.
- 어떤 node는 자기 primary domain이 아닌 foreign-domain CAN database로 publish합니다.
- 이런 node는 visible owner는 하나로 유지하되, GUI visibility는 추가로 필요합니다.

### 4.2 Full-system validation harness

- `TEST_SCN`은 cross-domain scenario를 주입하고 관찰해야 합니다.
- 따라서 `Powertrain`, `Chassis`, `Body`, `Infotainment`, `ADAS` domain CAN을 모두 볼 수 있어야 합니다.
- 이는 product transport 설계가 아니라 validation architecture 요구사항입니다.

## 5. Node 분류

### 5.1 진성 multibus anchor

- `CGW`: cross-domain boundary와 fail-safe authority를 가지며 `frmChassisHealthMsg`, `frmBodyHealthMsg`, `frmInfotainmentHealthMsg`를 함께 소비
- `TEST_SCN`: full-system scenario orchestration을 수행하며 five-domain CAN contract를 모두 주입/관찰

### 5.2 CAN-primary이지만 cross-domain visibility가 필요한 node

- `PGS`
  - primary placement: `Infotainment`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `ADAS`
  - reason: `frmParkUltrasonicStateMsg` 소비
- `AFLS`
  - primary placement: `Body`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Chassis`
  - reason: `frmSteeringAngleMsg` 소비
- `DATC`
  - primary placement: `Body`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Infotainment`
  - reason: `frmTmuServiceStateMsg` 소비
- `ACU`
  - primary placement: `Chassis`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Body`
  - reason: `frmSeatBeltStateMsg` 소비
- `ODS`
  - primary placement: `Chassis`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Body`
  - reason: `frmSeatBeltStateMsg`, `frmSeatStateMsg` 동시 소비
- `ADAS`
  - primary placement: `ADAS`
  - GUI Ethernet runtime: required
  - extra CAN visibility: `Chassis`, `Body`, `Infotainment`, `Powertrain`
  - reason: cross-domain context 소비와 ADAS-specific ETH ingress owner 유지
- `BCM`
  - primary placement: `Body`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Chassis`, `Infotainment`, `ADAS`
  - reason: `frmVehicleStateCanMsg`, `frmPhoneAsKeyStateMsg`, `frmTmuServiceStateMsg`, `frmTurnLampInputMsg`, `frmAdasDomainStateMsg` 소비
- `IVI`
  - primary placement: `Infotainment`
  - GUI Ethernet runtime: required
  - extra CAN visibility: `Chassis`, `ADAS`
  - reason: `frmVehicleStateCanMsg`, `frmAdasDomainStateMsg` 소비와 `ethNavContextMsg` publish
- `SCC`
  - primary placement: `ADAS`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Powertrain`, `Chassis`
  - reason: `frmCruiseStateMsg` publish와 `frmVehicleStateCanMsg` 소비
- `HWP`
  - primary placement: `ADAS`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Powertrain`
  - reason: `frmCruiseStateMsg` 소비
- `VCU`
  - primary placement: `Chassis`
  - GUI Ethernet runtime: required
  - extra CAN visibility: `Powertrain`, `Infotainment`
  - reason: vehicle-state 관련 CAN을 소비하며 `ethVehicleStateMsg` publish
- `MDPS`
  - primary placement: `Chassis`
  - GUI Ethernet runtime: required
  - extra CAN visibility: none
  - reason: foreign CAN은 필요 없지만 `ethSteeringMsg` publish를 위해 backbone runtime 유지
- `CLU`
  - primary placement: `Infotainment`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `ADAS`
  - reason: `frmAdasDomainStateMsg` 소비

### 5.3 ETH_Backbone-primary node

- `CGW`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: required
  - extra CAN visibility: `Chassis`, `Body`, `Infotainment`
  - reason: health seam과 cross-domain boundary contract 소유
- `TEST_SCN`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: required
  - extra CAN visibility: `Powertrain`, `Chassis`, `Body`, `Infotainment`, `ADAS`
  - reason: validation orchestration과 full-system signal injection/observation 수행
- `V2X`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: required
  - extra CAN visibility: none
  - reason: emergency backbone ingress와 monitor owner
- `DCM`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Infotainment`
  - reason: source/mirror에서는 backbone 아래 유지하지만 live runtime 참여는 제거
- `ETHB`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Infotainment`
  - reason: internal fail-safe contract만 읽고 live Ethernet runtime은 필요하지 않음
- `SGW`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Chassis`, `Infotainment`
  - reason: `frmVehicleStateCanMsg`, `frmNavModuleStateMsg`, `frmClusterNotifMsg` 소비
- `IBOX`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `Chassis`, `Infotainment`, `ADAS`
  - reason: vehicle, nav, ADAS context를 소비하지만 direct ETH RX/TX owner는 아님
- `EDR`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: not required
  - extra CAN visibility: `ADAS`
  - reason: object/fail-safe internal contract를 읽는 observer 성격
- `TEST_BAS`
  - primary placement: `ETH_Backbone`
  - GUI Ethernet runtime: required
  - extra CAN visibility: none
  - reason: shared observer와 sysvar aggregation seam 담당

## 6. `TEST_BAS` 단일-bus 유지 규칙

`TEST_BAS`는 `TEST_SCN`과 다르게 full-system stimulus를 만들지 않습니다.

- `TEST_SCN`
  - domain CAN과 backbone contract를 직접 주입/관찰합니다.
- `TEST_BAS`
  - `Test::scenarioResult`, `Test::base*` 같은 sysvar summary seam을 집계합니다.

따라서 `TEST_BAS`는 backbone runtime에는 남지만, foreign CAN database visibility를 무조건 늘릴 필요는 없습니다.

## 7. 사용 규칙

- source/mirror 구조를 바꾸기 전에 이 문서로 visibility 필요성을 먼저 판단합니다.
- GUI `Assigned buses` 변경은 이 문서의 `GUI Ethernet runtime` 판정에 따라 수행합니다.
- foreign-domain CAN visibility가 필요하면 `communication-matrix`와 `owner-route`에서 실제 owner/seam을 함께 확인합니다.
