# Change Orders Index

이 폴더는 개발팀-문서팀 동기화 문서를 관리한다.

## Active Sync Docs

- `TEAM_SYNC_BOARD.md`
- `FINAL_PHASE_TEAM_SPLIT_2026-03-08.md`
- `DEV1_TO_DOC_BATCH_2026-03-08.md`
- `DEV1_CANOE_TEST_DOC_IMPACT_2026-03-08.md`

## Active Architecture Reset Baseline

- `ARCHITECTURE_RESET_DECISION_2026-03-08.md`
- `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`
- `TARGET_SURFACE_ECU_INVENTORY_V2_2026-03-09.md`
- `ECU_RESET_DOC_PROPAGATION_RULES_2026-03-09.md`

## Historical / Option Study

- `ECU_ARCHITECTURE_RESET_GROUPING_V1_2026-03-08.md`
- `LOGICAL_ECU_SURFACE_MAPPING_V1_2026-03-08.md`
- `VEHICLE_ECU_REFACTOR_OPTIONS_2026-03-08.md`

원칙:
- Active Sync Docs는 팀 간 즉시 협업 기준이다.
- Active Architecture Reset Baseline은 현재 SoT를 재작성할 때만 직접 참조한다.
- Historical / Option Study는 의사결정 히스토리이며, reviewer-facing 문서의 기준선으로 직접 사용하지 않는다.

## Current Usage

- `TEAM_SYNC_BOARD.md`
  - 실시간 상태판과 open item 관리
- `ARCHITECTURE_RESET_DECISION_2026-03-08.md`
  - architecture reset 전환 결정과 범위 선언
- `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`
  - active runtime node의 surface/runtime/validation 분류표
- `TARGET_SURFACE_ECU_INVENTORY_V2_2026-03-09.md`
  - reviewer-facing target surface ECU inventory
- `ECU_RESET_DOC_PROPAGATION_RULES_2026-03-09.md`
  - `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07 -> GUI` 전파 규칙
- `DEV1_TO_DOC_BATCH_2026-03-08.md`
  - Dev1 -> Docs 일괄 반영 요청
- `DEV1_CANOE_TEST_DOC_IMPACT_2026-03-08.md`
  - native CANoe Test Unit 반영 범위 정리
