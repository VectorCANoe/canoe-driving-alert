# Campaign Profiles

## 목적

Campaign profile은 `언제 돌릴지`를 결정하는 Jenkins scheduler를 대체하지 않습니다.

대신 Console이 아래를 일관되게 기록하도록 고정하는 실행 계약입니다.

- `phase`
- `surface_scope`
- `repeat_count`
- `duration_minutes`
- `interval_seconds`
- `stop_on_fail`
- `owner_default`
- 필요 시 `pack_id`

즉 Jenkins는 **스케줄링**, Console은 **실행 메타데이터와 증빙 규약**을 담당합니다.

## 프로필 2종

Campaign profile은 성격상 두 그룹으로 나뉩니다.

### 1. 운영 profile

- `quick_smoke`
  - 로컬 빠른 확인용
- `ci_preflight`
  - Jenkins 사전 점검용
- `nightly_regression`
  - 야간 반복 회귀용
- `soak_stability`
  - 장시간 안정성 증빙용

### 2. verification pack profile

- `native_functional_6`
  - Native Functional Portfolio 6 실행용
- `network_gateway_core_4`
  - Network/Gateway Core 4 실행용
- `network_plus_diag_draft_5`
  - Network/Gateway Core + Diagnostic draft 실행용

운영 profile은 실행 방식에 초점을 두고, verification pack profile은 **무슨 테스트 묶음을 돌리는지**까지 같이 고정합니다.

## `profile_id -> pack_id -> contract_ref`

Verification pack profile에는 아래 3개가 같이 들어갑니다.

- `profile_id`
  - 이번 실행에 적용한 campaign 규약
- `pack_id`
  - 어떤 테스트 포트폴리오를 돌리는지 나타내는 reviewer-facing 묶음
- `contract_ref`
  - 그 pack의 source contract JSON 경로

예:

- `profile_id=native_functional_6`
- `pack_id=native_functional_6`
- `contract_ref=product/sdv_operator/config/native_canoe_test_portfolio_v1.json`

즉 profile은 **실행 규약**, pack은 **검증 포트폴리오**, contract는 **정본 기준**입니다.

## 포함 필드

- `profile_id`
- `title`
- `purpose`
- `recommended_command`
- `phase`
- `surface_scope`
- `repeat_count`
- `duration_minutes`
- `interval_seconds`
- `stop_on_fail`
- `owner_default`
- `pack_id` (선택)
- `review_focus` (선택)
- `contract_ref` (선택)

## 원칙

- scheduler는 Jenkins가 담당합니다.
- Console은 campaign metadata와 evidence normalization을 담당합니다.
- profile은 실행 편의값이면서 동시에 reviewer-facing evidence 규약의 일부입니다.
- verification pack profile은 `surface bundle`, `execution manifest`, `archive`에 그대로 반영됩니다.

## 관련 원본

- `product/sdv_operator/config/campaign_profiles.json`
- `product/sdv_operator/config/verification_pack_matrix.json`
- `product/sdv_operator/docs-src/verification-packs.md`
- `product/sdv_operator/docs-src/role-boundary.md`
- `product/sdv_operator/docs-src/ci-bridge.md`
