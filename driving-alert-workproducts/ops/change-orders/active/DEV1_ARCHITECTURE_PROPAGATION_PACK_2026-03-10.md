# Dev1 Architecture Propagation Pack (2026-03-10)

## 목적
- `canoe/` 구현 기준으로 확정된 아키텍처 해석을 문서팀이 정본 체인(`00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04`)에 후행 반영할 수 있도록 전달한다.
- 본 문서는 SoT 본문이 아니라 Dev1 구현 사실 기반의 전파 패킷이다.

## Dev1 구현 기준 고정 사실

### 1. ECU 레이어 해석
- 현재 구현은 `순수 중앙집중형 CGW`가 아니다.
- 현재 구현은 `domain-controller style + CGW supervision`에 가깝다.
- 버스 구조는 그대로 유지한다.
  - `ETH_Backbone`
  - `Powertrain`
  - `Chassis`
  - `Body`
  - `Infotainment`
  - `ADAS`
- 즉, 이번 변경은 `버스 재정의`가 아니라 `ECU 역할 해석 재정의`다.

### 2. 내부 분류와 외부 설명 분리
- 내부 구현/운영 분류는 `4-layer`를 유지한다.
  - Layer 1: `Central Gateway / Backbone Services`
  - Layer 2: `Domain Controller / Primary Runtime Anchors`
  - Layer 3: `Leaf ECU / Feature ECU / Local Runtime Surfaces`
  - Layer 4: `Validation / Test`
- 외부/OEM 표면 설명은 `3-layer + validation overlay`로 정리한다.
  - Layer 1: `Central Gateway / Backbone Services`
  - Layer 2: `Domain Controllers / Vehicle Computers`
  - Layer 3: `Leaf / Feature ECUs`
  - Overlay: `Validation Harness`
- 즉 `4-layer`는 프로젝트 내부 분류 모델이고, 외부 발표/정본 설명에서는 차량 아키텍처 표준처럼 말하지 않는다.

근거 문서:
- `canoe/docs/operations/reference/OEM_4_LAYER_ECU_CLASSIFICATION_2026-03-10.md`
- `canoe/tmp/DOMAIN_CONTROLLER_VS_CENTRAL_CGW_VIEW_2026-03-10.md`

### 3. CGW 해석
- `CGW`는 모든 raw payload를 직접 relay하는 중앙 허브가 아니다.
- 현재 역할:
  - boundary supervision
  - fail-safe supervision
  - cross-domain health supervision
  - backbone-side state/monitoring
- 따라서 문서에서는 `CGW = central gateway / supervision / security / diag edge`로 설명하고,
  `모든 도메인 raw signal relay owner`로 쓰지 않는다.

### 4. Domain Controller 해석
- 현재 구현 기준으로 backbone seam 또는 cross-domain seam을 직접 publish/consume하는 핵심 ECU는 domain-controller 성격으로 해석한다.
- 대표:
  - `VCU`
  - `IVI`
  - `ADAS`
  - `V2X`
  - `BCM`
  - `MDPS`
- 이들은 leaf ECU보다 상위 계층으로 문서화해야 한다.

### 5. Validation Harness 해석
- `TEST_SCN`
  - tester + scenario harness
  - multibus
- `TEST_BAS`
  - summary-frame aggregator
  - single-bus (`ETH_Backbone`)
- 둘은 제품 ECU가 아니라 validation layer다.

## 00f / CAN ID 정책 해석

### 1. 유지해야 하는 정책
- `00f`의 `29-bit 3/5/21 (Tier/Block/Slot)`은 정책 SoT로 유지한다.
- 이 정책은 logical architecture ID 체계다.

### 2. 현재 실행 상태
- 현재 active DBC 6종은 `11-bit active compatibility execution`이다.
- 즉, 현재 `canoe/databases/*.dbc`를 문서에서 `전면 29-bit physical cutover 완료`처럼 쓰면 안 된다.

### 3. 문서 반영 원칙
- `00f`에는 아래 문장을 유지/강화한다.
  - `Primary policy = 29-bit`
  - `Active/SIL execution = 11-bit compatibility`
- `0303`과 `04`에는 아래를 명시한다.
  - backbone seam은 logical ID와 SIL stub ID를 분리해서 관리
  - 현재 실행은 compatibility ID 기반
  - 실제 29-bit physical cutover는 별도 전환 wave

근거 문서:
- `driving-alert-workproducts/governance/00f_CAN_ID_Allocation_Standard.md`
- `canoe/docs/operations/10_ETHERNET_BACKBONE_INTERFACE_SPEC.md`

## 문서별 수정 포인트

### 00e_ECU_Naming_Standard.md
- `surface ECU / runtime module / validation harness` 3분리를 유지
- `TEST_SCN`, `TEST_BAS`는 validation-only 이름으로 명시
- `_GW`, `_CTRL`, `_MGR` 같은 내부 구현명은 surface ECU명으로 올리지 않음

### 0301_SysFuncAnalysis.md
- 내부 상세 분석에서는 `4-layer` 분류를 유지 가능
- `CGW`는 supervision/gateway edge
- `VCU/IVI/ADAS/V2X/BCM`는 domain-controller 성격으로 기술

### 0302_NWflowDef.md
- 버스 구조는 기존 6도메인 유지
- 외부/OEM 표면 설명은 `3-layer + validation overlay` 기준으로 기술
- flow 설명에서 `CGW가 모든 raw payload를 relay`하는 듯한 문장을 제거
- domain controller가 seam을 직접 publish하는 현재 구조를 반영

### 0303_Communication_Specification.md
- backbone seam contract에 대해 `Logical ID` vs `SIL Stub ID`를 분리해 서술
- active DBC가 11-bit execution임을 명시
- `TEST_SCN`/`TEST_BAS`를 validation seam으로 분리
- 외부 설명에서는 `Validation Harness`를 차량 ECU 레이어가 아닌 overlay로 표현

### 0304_System_Variables.md
- `TEST_SCN`/`TEST_BAS` 관련 변수는 validation-only로 유지
- domain-controller seam state와 local ECU state를 구분

### 04_SW_Implementation.md
- 현재 구현은 `centralized CGW`가 아니라 `domain-controller + CGW supervision`
- 외부/OEM 설명은 `3-layer + validation overlay` 기준으로 표현
- Ethernet cutover 시 `CAN-stub handler -> Ethernet handler` 교체를 기준으로 설명
- downstream ECU 로직 유지 전략을 명시

## 문서팀 전달 문장
- `canoe/` 구현 기준으로 현재 아키텍처는 `domain-controller + CGW supervision`으로 고정되었습니다.
- 내부 상세 분석에는 `4-layer` 분류를 유지할 수 있지만, 외부/OEM 표면 설명은 `3-layer + validation overlay`로 정리해 주세요.
- 버스 구조는 `ETH_Backbone / Powertrain / Chassis / Body / Infotainment / ADAS` 그대로 유지합니다.
- `00f`의 `29-bit 3/5/21`은 정책 SoT로 유지하되, 현재 active DBC 실행은 `11-bit compatibility` 기준으로 문서화해 주세요.
- `TEST_SCN`, `TEST_BAS`는 제품 ECU가 아니라 validation harness overlay로 분리해 주세요.

## 근거 파일
- `canoe/docs/operations/reference/OEM_4_LAYER_ECU_CLASSIFICATION_2026-03-10.md`
- `canoe/tmp/DOMAIN_CONTROLLER_VS_CENTRAL_CGW_VIEW_2026-03-10.md`
- `canoe/docs/operations/10_ETHERNET_BACKBONE_INTERFACE_SPEC.md`
- `canoe/docs/operations/reference/OEM_ACTIVE_TARGET_PROFILE_2026-03-09.md`
