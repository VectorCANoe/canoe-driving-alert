# Panel and SysVar Binding Contract

원문:
- [../../contracts/panel-sysvar-contract.md](../../contracts/panel-sysvar-contract.md)

동기화 기준:
- `5d83ee7f`
- SysVar namespace와 binding target 이름은 canonical technical identifier로 유지합니다.

> [!IMPORTANT]
> 이 문서는 panel input, system-variable namespace, runtime-visible output monitor 사이의 stable binding contract를 정의합니다.
> panel editor의 클릭 절차가 아니라, 무엇을 쓰고 읽어야 하는지에 대한 계약 문서입니다.

## 1. 목적

이 문서는 아래 항목 사이의 stable binding contract를 정의합니다.

- CANoe panel input
- system-variable namespace
- runtime-visible output monitor

핵심 목적은 두 가지입니다.

1. panel이 어떤 namespace에 써도 되는지 고정한다.
2. panel이 어떤 monitor namespace를 읽어야 하는지 고정한다.

## 2. Active binding 원칙

1. panel은 stable system-variable 이름에 바인딩해야 합니다.
2. temporary alias나 transport-specific internal에 새 widget을 직접 연결하면 안 됩니다.
3. panel source of truth는 `cfg/channel_assign/**`가 아니라 이 binding contract입니다.
4. 입력 widget은 approved input namespace에만 씁니다.
5. 관찰 widget은 approved monitor namespace에서만 읽습니다.

## 3. Write surface

### 3.1 Chassis 입력 binding

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Chassis::vehicleSpeed` | panel input speed | panel writes |
| `Chassis::driveState` | drive selector state | panel writes |
| `Chassis::steeringInput` | steering activity flag | panel writes |

### 3.2 Infotainment 입력 binding

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Infotainment::roadZone` | road-zone context | panel writes |
| `Infotainment::navDirection` | navigation direction | panel writes |
| `Infotainment::zoneDistance` | zone boundary까지의 거리 | panel writes |
| `Infotainment::speedLimit` | 필요 시 speed-limit context | panel writes 또는 scripted input |

### 3.3 V2X 입력 binding

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `V2X::emergencyType` | emergency vehicle type | panel reads |
| `Test::compatEmergencyDirection` | dispatch-only compat 방향 입력 | panel writes |
| `Test::compatEmergencyEta` | dispatch-only compat ETA 입력 | panel writes |
| `Test::compatEmergencySourceId` | dispatch-only compat source identifier 입력 | tie-break 검증 시 panel writes |
| `V2X::alertState` | emergency active/clear state | panel reads |
| `Test::compatPoliceDispatch` | police dispatch compat toggle | dispatch flow 검증 시 panel writes |
| `Test::compatAmbulanceDispatch` | ambulance dispatch compat toggle | dispatch flow 검증 시 panel writes |

### 3.4 Test control binding

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Test::testScenario` | selected SIL scenario id | panel 또는 automation writes |
| `Test::scenarioCommand` | execute command | panel 또는 automation writes |
| `Test::forceFailSafe` | validation override | panel 또는 automation writes |
| `Test::displayModeSetting` | test-only HMI mode override | panel 또는 automation writes |
| `Test::alertVolumeSetting` | test-only audio override | panel 또는 automation writes |
| `Test::compatPoliceDispatch` | dispatch-only compatibility stimulus | panel 또는 automation writes |
| `Test::compatAmbulanceDispatch` | dispatch-only compatibility stimulus | panel 또는 automation writes |
| `Test::compatEmergencyDirection` | dispatch-only compatibility direction | panel 또는 automation writes |
| `Test::compatEmergencyEta` | dispatch-only compatibility ETA | panel 또는 automation writes |
| `Test::compatEmergencySourceId` | dispatch-only compatibility source id | panel 또는 automation writes |

## 4. Read surface

### 4.1 Primary product-visible output

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Body::ambientMode` | ambient output mode | panel reads |
| `Body::ambientColor` | ambient output color | panel reads |
| `Body::ambientPattern` | ambient output pattern | panel reads |
| `Cluster::warningTextCode` | cluster warning result | panel reads |

### 4.2 Runtime status mirror

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Core::selectedAlertLevel` | selected alert level | panel reads |
| `Core::selectedAlertType` | selected alert type | panel reads |
| `Core::timeoutClear` | timeout clear state | panel reads |
| `Core::proximityRiskLevel` | emergency proximity risk | panel reads |
| `Core::decelAssistReq` | deceleration assist request | panel reads |
| `Core::failSafeMode` | fail-safe mode | panel reads |

### 4.3 Health 및 traceability mirror

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `CoreState::warningPathStatus` | warning-path health state | panel reads |
| `CoreState::e2eHealthState` | end-to-end health state | panel reads |
| `CoreState::domainBoundaryStatus` | boundary alive summary | panel reads |
| `CoreState::lastEmergencyRxMs` | emergency receive timestamp mirror | panel reads |
| `CoreState::alertHistoryCount` | alert history accumulation | panel reads |

### 4.4 Verification 및 render mirror

| SysVar | 의미 | 방향 |
| --- | --- | --- |
| `Test::scenarioResult` | per-scenario PASS/FAIL summary | panel reads |
| `Test::baseScenarioResult` | baseline aggregate PASS/FAIL | panel reads |
| `Diag::*` | diagnostic observation seam | panel 또는 tools read |
| `UiRender::*` | presentation-only derived render state | demo rendering 사용 시 panel reads |

## 5. Binding 규칙

1. 입력 widget은 input namespace에만 씁니다.
2. product output monitor는 stable output namespace를 우선 읽습니다.
3. `g*` alias나 temporary debug var에 새 widget을 직접 묶지 않습니다.
4. panel은 transport-specific detail보다 reviewer-readable namespace를 우선 보여줘야 합니다.
5. binding contract가 바뀌면 panel README와 `0304` 추적도 함께 갱신해야 합니다.
