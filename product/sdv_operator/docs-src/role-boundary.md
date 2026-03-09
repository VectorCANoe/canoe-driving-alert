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

- testcase portfolio 선정
- testcase intent / oracle / timing / evidence blueprint 작성
- `profile_id / pack_id / campaign_id`와 native asset 연결
- batch/JUnit/archive/manifest 연결
- testcase blueprint source contract 관리
  - `product/sdv_operator/config/native_testcase_blueprints_v1.json`

### Dev1

- 공통 harness 구현
- native CANoe testcase source 실체화
  - `.can`
  - `.vtestunit.yaml`
  - `.vtesttree.yaml`
- blueprint를 실제 runtime signal/message/assert로 연결
- native `.vtestreport` 생성

즉 Dev2는 **무엇을 어떤 기준으로 검증할지**를 정하고, Dev1은 **그 설계를 CANoe native asset으로 구현**합니다.

## testcase blueprint source

Dev2가 작성하는 testcase 설계의 정본은 아래 JSON입니다.

- `product/sdv_operator/config/native_testcase_blueprints_v1.json`

이 파일은 다음을 담습니다.

- functional 6 / network core 4 / diagnostic draft 1 자산 목록
- testcase intent
- oracle summary
- timing target
- evidence expectation

즉 문서 설명과 별개로, Console/CI/packaging이 읽을 수 있는 기계 가독 계약은 이 JSON이 담당합니다.

## 왜 이렇게 나누는가

Console은 CANoe TEST를 대체하지 않고, Jenkins를 복제하지 않습니다.
Console은 두 시스템 사이에서 검증 운영 규칙과 증빙 구조를 고정하는 제품입니다.
