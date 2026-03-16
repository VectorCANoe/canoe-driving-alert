# 역할 경계

## 원칙

- CANoe TEST는 native test authoring, execution, native report를 담당합니다.
- Jenkins는 scheduling, retry, timeout, junit ingest, artifact archive를 담당합니다.
- CANoe Test Verification Console은 campaign metadata, evidence normalization, surface ECU rollup, execution manifest를 담당합니다.

## CANoe TEST가 담당하는 것

- Test Module / Test Unit / Test Case
- native `.vtestreport`
- CANoe 내부 stimulus / measurement / verdict

## Jenkins가 담당하는 것

- schedule / nightly / periodic trigger
- stage orchestration
- `junit`
- `archiveArtifacts`
- build history / trend

## Console이 담당하는 것

- `gate all`
- `doctor`
- `scenario run`
- `verify batch`
- `surface_evidence_bundle.*`
- `execution_manifest.*`
- reviewer-facing artifact navigation

## Dev1 / Dev2 실무 분리

현재 native test 운영은 아래처럼 나눕니다.

### Dev2

- active suite portfolio 선정
- execution metadata / oracle / evidence binding 기준 작성
- `profile_id / pack_id / campaign_id`와 native asset 연결
- batch/JUnit/archive/manifest 연결
- source contract 관리
  - `product/sdv_operator/config/verification_pack_matrix.json`
  - `product/sdv_operator/config/campaign_profiles.json`
  - `canoe/docs/verification/test-asset-mapping.md`
  - `canoe/docs/verification/execution-guide.md`

### Dev1

- 공통 harness 구현
- native CANoe testcase source 실체화
  - `.can`
  - `.vtestunit.yaml`
  - `.vtesttree.yaml`
- blueprint를 실제 runtime signal/message/assert로 연결
- native `.vtestreport` 생성

즉 Dev2는 **어떤 active suite를 어떤 execution/profile 기준으로 운영할지**를 정하고, Dev1은 **그 설계를 CANoe native asset으로 구현**합니다.

## current source contracts

Dev2가 운영 표면에서 직접 참조하는 정본은 아래와 같습니다.

- `product/sdv_operator/config/verification_pack_matrix.json`
- `product/sdv_operator/config/campaign_profiles.json`
- `canoe/tests/modules/test_units/README.md`
- `canoe/tests/modules/test_suites/README.md`
- `canoe/docs/verification/test-asset-mapping.md`
- `canoe/docs/verification/execution-guide.md`

이 문서/계약은 다음을 담습니다.

- active suite 수량과 wrapper 구조
- 05/06/07과 native asset 매핑
- native execution / harness / evidence 기준
- batch/profile/pack 메타데이터 연결

즉 Console/CI/packaging은 더 이상 옛 포트폴리오 설계 JSON보다 현재 active suite와 mapping 문서를 기준으로 움직입니다.

## 왜 이렇게 나누는가

Console은 CANoe TEST를 대체하지 않고, Jenkins를 복제하지 않습니다.
Console은 두 시스템 사이에서 검증 운영 규칙과 증빙 구조를 고정하는 제품입니다.
