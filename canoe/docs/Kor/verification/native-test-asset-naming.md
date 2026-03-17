# Native Test Asset Naming

원문:
- [../../verification/native-test-asset-naming.md](../../verification/native-test-asset-naming.md)

동기화 기준:
- `5d83ee7f`
- asset ID, suite 이름, folder naming rule은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 executable native CANoe SIL test asset의 naming convention을 정의합니다.
> 최종 test tree, harness layout, execution packaging이 고정되면 일부 naming 세부사항은 조정될 수 있습니다.

## 1. 목적

이 문서는 다음 reviewer-facing test ID를 구현하는 executable native test asset의 naming convention을 정의합니다.

- `driving-alert-workproducts/05_Unit_Test.md`
- `driving-alert-workproducts/06_Integration_Test.md`
- `driving-alert-workproducts/07_System_Test.md`

목표는 다음 세 가지를 동시에 유지하는 것입니다.

- `05/06/07`은 reviewer-facing 표면으로 유지
- native asset은 implementation-facing 표면으로 유지
- 둘 사이 매핑은 안정적이고 읽기 쉽게 유지

## 2. Naming pattern

native test asset은 다음 형식을 사용합니다.

`TC_CANOE_<LEVEL>_<GROUP>_<SEQ>_<SLUG>`

의미:

- `<LEVEL>` = `UT` | `IT` | `ST`
- `<GROUP>` = `CORE` | `V2` | `EXT` | `BASE` | `ETH` | `FULL`
- `<SEQ>` = `001` 같은 세 자리 번호
- `<SLUG>` = business-readable short identifier

예시:

- `TC_CANOE_UT_CORE_003_ADAS_WARN_CTRL`
- `TC_CANOE_IT_EXT_040_SERVICE_SECURITY_DIAG`
- `TC_CANOE_ST_FULL_002_CONTINUOUS_TRIP_WITH_FAILSAFE`

## 3. Preset / stimulus asset naming

scenario preset 또는 stimulus-only helper는 다음 형식을 사용합니다.

`TEST_SCN_<GROUP>_<SLUG>`

예시:

- `TEST_SCN_CORE_INPUT_PRESET`
- `TEST_SCN_SGW_SECURITY_PRESET`
- `TEST_SCN_DCM_DIAGNOSTIC_PRESET`

`TEST_SCN_*`는 다음 용도로만 사용합니다.

- input preset
- stimulus profile
- reusable scenario setup block

`UT/IT/ST`의 최종 executable verdict asset 이름으로 `TEST_SCN_*`를 사용하면 안 됩니다.

## 4. Group 의미

| Group | 의미 |
|---|---|
| `CORE` | core driving-alert baseline behavior |
| `V2` | current feature deepening and emergency/arbitration behavior |
| `EXT` | minimal core concept를 넘어서는 extension behavior |
| `BASE` | vehicle baseline context integration |
| `ETH` | Ethernet-facing observation 또는 transport verification |
| `FULL` | whole-trip 또는 full-system composed scenario |

## 5. Slug 규칙

1. business-readable name을 우선 사용합니다.
2. internal variable name보다 ECU/service/function wording을 우선합니다.
3. internal implementation이 바뀌어도 slug는 안정적으로 유지합니다.
4. 임시 requirement range나 flow ID를 slug 안에 넣지 않습니다.
5. 표기 형식은 uppercase snake case만 사용합니다.

좋은 예:

- `ZONE_WARNING`
- `FAILSAFE_MIN_WARNING`
- `DISPLAY_SERVICE_CONTEXT`

피해야 할 예:

- `FLOW_0302_CASE_4`
- `SYSVAR_WARNSTATE_TEST`
- `TMP_NEW_CHAIN`

## 6. 권장 logical tree

향후 native test tree는 다음 logical grouping을 따르는 것이 좋습니다.

```text
verification/
├─ unit/
│  ├─ core/
│  ├─ v2/
│  ├─ ext/
│  ├─ out/
│  └─ presets/
├─ integration/
│  ├─ core/
│  ├─ v2/
│  ├─ base/
│  ├─ ext/
│  └─ eth/
└─ system/
   ├─ core/
   ├─ v2/
   ├─ ext/
   ├─ eth/
   └─ full/
```

이 규칙은 logical organization rule이며, 물리 folder를 강제하는 것은 아닙니다.

## 7. 현재 build order

native asset build 순서는 다음과 같습니다.

1. `UT` core verdict asset
   - `UT_003`
   - `UT_009`
   - `UT_011`
   - `UT_014`
   - `UT_015`
2. `IT` core composed asset
   - `IT_001` to `IT_008`
3. `ST` core scenario asset
   - `ST_001` to `ST_021`
4. diagnostic-linked asset
   - `UT_063`
   - `UT_064`
   - `IT_040`
   - `ST_043`

## 8. 관련 verification 문서

이 문서는 다음 문서와 함께 사용합니다.

- `test-asset-mapping.md`
- `diagnostic-coverage.md`
- `execution-guide.md`
