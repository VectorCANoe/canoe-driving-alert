# assign

Bulk GUI import wrappers for active CANoe Test Unit registration.

Folders:
- `UT_ACTIVE_BASELINE`
- `IT_ACTIVE_BASELINE`
- `ST_ACTIVE_BASELINE`
- `FULL_ACTIVE_BASELINE`

Usage:
1. In CANoe Test Configuration, use `Add Test Unit`.
2. Open one of the folders above.
3. Multi-select all `*.vtestunit.yaml` files in that folder and import them together.
4. These wrappers point back to the original asset folders under `..\..\<TC_ID>\`.
5. Do not edit wrapper paths manually unless asset folders move.

Notes:
- `test_suites/TS_*/*.vtestunit.yaml` are repository suite manifests, not direct GUI bulk-import files.
- `common/` does not need to be copied into `assign/` because each wrapper resolves to the original asset-local `.can` and `.vtesttree.yaml` files.
