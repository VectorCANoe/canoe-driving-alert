# Change Orders Index

이 폴더는 개발팀-문서팀 동기화 문서를 관리한다.

## Folder Policy

- `active/`: 현재 스프린트와 즉시 협업에 쓰는 문서
- `baseline/`: architecture reset 기준선 문서
- `history/`: 옵션 검토 및 종료 이력 문서

## Active Sync Docs (`active/`)

- `TEAM_SYNC_BOARD.md`
- `FINAL_PHASE_TEAM_SPLIT_2026-03-08.md`
- `DEV1_TO_DOC_BATCH_2026-03-08.md`
- `DEV1_CANOE_TEST_DOC_IMPACT_2026-03-08.md`
- `DEV1_ARCHITECTURE_PROPAGATION_PACK_2026-03-10.md`
- `DEV2_NATIVE_TEST_CASE_DESIGN_6_2026-03-10.md`
- `DEV2_NATIVE_TEST_HARNESS_PORTFOLIO_6_2026-03-09.md`
- `DEV2_NETWORK_GATEWAY_VERIFICATION_PACK_V1_2026-03-10.md`

## Active Architecture Reset Baseline (`baseline/`)

- `ARCHITECTURE_RESET_DECISION_2026-03-08.md`
- `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`
- `TARGET_SURFACE_ECU_INVENTORY_V2_2026-03-09.md`
- `ECU_RESET_DOC_PROPAGATION_RULES_2026-03-09.md`

## Historical / Option Study (`history/`)

- `ECU_ARCHITECTURE_RESET_GROUPING_V1_2026-03-08.md`
- `LOGICAL_ECU_SURFACE_MAPPING_V1_2026-03-08.md`
- `VEHICLE_ECU_REFACTOR_OPTIONS_2026-03-08.md`
- `LEGACY_REQ_RETIREMENT_2026-03-10.md`

## Operation Rules

1. 신규 change-order는 기본 `active/`에 생성한다.
2. 기준선으로 확정된 문서는 `baseline/`으로 이동한다.
3. 적용 종료 또는 대체된 문서는 `history/`로 이동한다.
4. reviewer-facing 정본 근거는 `driving-alert-workproducts/` 루트 SSoT에서만 사용한다.
