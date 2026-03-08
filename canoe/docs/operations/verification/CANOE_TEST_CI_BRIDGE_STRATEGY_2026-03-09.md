# CANoe Test CI Bridge Strategy (2026-03-09)

## 목적

Dev1이 native CANoe Test Unit 자산을 작성하고, Dev2가 그 결과를 외부 CLI/TUI와 Jenkins로
연결하는 표준 경계를 고정한다.

이 문서는 `vTESTstudio/CANoe native test`를 대체하려는 문서가 아니다.  
목표는 native tool chain을 유지하면서, Dev2가 CI-friendly 산출물을 추가하는 것이다.

## 최종 판단

1. native test authoring은 Dev1이 계속 담당한다.
2. Dev2는 native 결과를 대체하지 않고 정규화한다.
3. Jenkins ingress 포맷은 `JUnit XML`을 기본으로 사용한다.
4. native `.vtestreport`와 GUI 캡처는 원본 증빙으로 별도 archive한다.

## 권장 역할 분리

### Dev1

- `*.can`
- `*.vtestunit.yaml`
- `*.vtesttree.yaml`
- native `.vtestreport`
- CANoe GUI 실행 및 스크린샷

### Dev2

- `gate all`
- `scenario run`
- `verify batch`
- `JSON + MD + JUnit XML`
- Jenkins archive / publish contract

## 왜 이 구조가 맞는가

### 1. CANoe native 자산은 그대로 둔다

현재 repo는 이미 native Test Unit PoC를 보유한다.

- `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
- `TC_CANOE_IT_V2_FAILSAFE_001_CGW`

즉, Dev1은 CANoe 내부 test authoring capability를 이미 확보하는 방향이다.

### 2. Dev2는 CI bridge만 맡아야 겹치지 않는다

Dev2가 native test framework까지 다시 만들면 Dev1과 중복된다.  
반대로 Dev2가 다음만 맡으면 역할이 분리된다.

- 결과 수집
- evidence normalization
- Jenkins ingest format 생성
- operator-facing review surface

### 3. Jenkins는 JUnit XML을 가장 잘 소화한다

Jenkins는 기본 `junit` step으로 XML을 바로 읽는다.  
따라서 Dev2는 `dev2_batch_report.junit.xml`을 canonical CI ingress로 두는 것이 가장 단순하다.

## 권장 실행 구조

### 개발/로컬 운영

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify batch --run-id 20260309_0900 --owner DEV2 --phase pre --report-formats json,md,junit
```

### Jenkins / CI

1. native CANoe test 실행 또는 native 증빙 확보
2. Dev2 batch 실행
3. `JUnit XML` publish
4. native `.vtestreport` / screenshot / JSON / MD archive

## Jenkins 수집 기준

### Publish

- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`

### Archive

- `canoe/tmp/reports/verification/*.json`
- `canoe/tmp/reports/verification/*.md`
- `canoe/tmp/reports/verification/*.xml`
- `canoe/**/*.vtestreport`
- screenshot path

## 단계별 산출물

### Native source of truth

- CANoe Test Unit verdict
- native `.vtestreport`
- GUI capture

### Dev2 normalized outputs

- `dev2_batch_report.json`
- `dev2_batch_report.md`
- `dev2_batch_report.junit.xml`
- `run_readiness.json`
- `doctor_report.json`

## 하지 말아야 할 것

1. Dev2가 CANoe Test Unit 자체를 다시 설계하는 것
2. Jenkins를 위해 native `.vtestreport`를 억지로 직접 파싱하는 것
3. PyQt 등으로 CANoe Panel을 재구현하는 것

## 향후 확장

향후 라이선스/시간이 허용되면 검토할 수 있는 것:

1. native test 실행 자동화 고도화
2. `.vtestreport` 메타데이터 요약 추출
3. Jenkins nightly baseline regression

단, 현재 단계의 목표는 `native proof + CI bridge`이며, 전체 test stack 재구축이 아니다.

## 참고 기준

### 내부 기준

- `canoe/docs/operations/verification/CANOE_TEST_POC_SCOPE_2026-03-08.md`
- `canoe/docs/operations/verification/CANOE_TEST_UNIT_RUNBOOK.md`
- `canoe/docs/operations/verification/FINAL_PHASE_EXECUTION_FLOW.md`

### 외부 기준

- Vector automated testing:
  - https://www.vector.com/kr/ko/know-how/automated-testing/
- Vector Python interface for test automation:
  - https://www.vector.com/int/en/know-how/test-automation-using-the-python-interface/
- Jenkins JUnit step:
  - https://www.jenkins.io/doc/pipeline/steps/junit/
- Jenkins archiveArtifacts step:
  - https://www.jenkins.io/doc/pipeline/steps/core/#archiveartifacts-archive-the-artifacts
