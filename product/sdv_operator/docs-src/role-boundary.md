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

## 왜 이렇게 나누는가

Console은 CANoe TEST를 대체하지 않고, Jenkins를 복제하지 않습니다.
Console은 두 시스템 사이에서 검증 운영 규칙과 증빙 구조를 고정하는 제품입니다.
