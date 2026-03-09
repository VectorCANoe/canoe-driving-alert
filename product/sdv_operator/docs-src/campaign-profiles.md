# Campaign Profiles

## 목적

Campaign profile은 Jenkins scheduler를 복제하지 않고도 반복 실행 규약을 고정하기 위한 source contract입니다.

Console은 profile을 읽어 기본 실행값과 evidence 규약을 제공합니다. Jenkins는 이 profile을 참고해 언제, 얼마나 자주 실행할지 스케줄링합니다.

## 현재 제공 profile

- `quick_smoke`
  - 로컬 빠른 확인용
- `ci_preflight`
  - Jenkins 사전 점검용
- `nightly_regression`
  - 야간 반복 회귀용
- `soak_stability`
  - 장시간 안정성 evidence용

## 포함 필드

- `profile_id`
- `phase`
- `surface_scope`
- `repeat_count`
- `duration_minutes`
- `interval_seconds`
- `stop_on_fail`
- `owner_default`

## 원칙

- scheduler는 Jenkins가 담당합니다.
- Console은 campaign metadata와 evidence normalization을 담당합니다.
- profile은 실행 편의값이면서 동시에 reviewer-facing evidence 규약의 일부입니다.

## 관련 원본

- `product/sdv_operator/config/campaign_profiles.json`
- `product/sdv_operator/docs-src/role-boundary.md`
- `product/sdv_operator/docs-src/ci-bridge.md`
