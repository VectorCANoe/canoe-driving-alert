# Verification Packs

`CANoe Test Verification Console`은 native test harness 자체를 만들지 않습니다.  
대신 아래 3축을 **pack**으로 고정하고, Dev2가 testcase blueprint/oracle 계약을 정의해서 Dev1 native CANoe test 구현과 Dev2 batch/archive를 같은 운영 축으로 묶습니다.

## 3축 구조

1. `native_functional_6`
- 핵심 운전자 경고 컨셉 검증
- 스쿨존, ETA priority, timeout clear, fail-safe, sync, ADAS object risk
- source:
  - `product/sdv_operator/config/native_canoe_test_portfolio_v1.json`

2. `network_gateway_core_4`
- 네트워크/게이트웨이 필수 검증
- `CAN bus arbitration`, route forwarding, stale chain, load/jitter
- source:
  - `product/sdv_operator/config/network_gateway_verification_pack_v1.json`

3. `network_plus_diag_draft_5`
- network/gateway core + diagnostic route draft
- diagnostic routing은 구현 가능하지만 현재는 `draft_pre_gate`
- source:
  - `product/sdv_operator/config/network_gateway_verification_pack_v1.json`

## testcase blueprint 기준

각 pack은 단순 목록이 아니라 Dev2가 정의한 testcase blueprint와 함께 읽어야 합니다.

- testcase blueprint source:
  - `product/sdv_operator/config/native_testcase_blueprints_v1.json`

여기에는 아래가 들어 있습니다.

- testcase intent
- oracle summary
- timing target
- evidence expectation
- Dev1 / Dev2 구현 분리 기준

## 왜 이렇게 나누는가

- 기능 검증과 네트워크 검증을 섞지 않기 위해서입니다.
- reviewer는 `기능 핵심가치`와 `인프라 건전성`을 분리해서 읽어야 합니다.
- diagnostic routing은 네트워크와 연결되어 있지만, owner/route 문서가 안정화되기 전까지는 draft로 유지하는 편이 OEM식 운영에 더 맞습니다.

## 용어 규칙

- `ETA priority`
  - 기능 선택 규칙
  - functional pack에서 사용
- `CAN bus arbitration`
  - 프로토콜/버스 충돌 규칙
  - network pack에서만 사용

즉 `scenario 9`는 `ETA priority`이지 `CAN arbitration`이 아닙니다.

## Campaign profile 연결

각 pack은 별도 campaign profile로 바로 실행할 수 있습니다.

- `native_functional_6`
- `network_gateway_core_4`
- `network_plus_diag_draft_5`

profile source:
- `product/sdv_operator/config/campaign_profiles.json`

matrix source:
- `product/sdv_operator/config/verification_pack_matrix.json`

## Console에서 하는 일

Console은 다음만 담당합니다.

- 어떤 pack/profile을 실행했는지 기록
- `run_id / campaign_id / profile_id / pack_id`를 결과물에 넣기
- native report, surface bundle, execution manifest, archive를 같은 run 기준으로 묶기

Console이 하지 않는 일:

- CANoe native test authoring 대체
- Jenkins scheduler 대체

## 권장 읽기 순서

1. `Campaign Profiles`
2. `Verification Packs`
3. `Role Boundary`
4. `Capability Boundary`
5. `Results`
