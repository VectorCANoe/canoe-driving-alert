# CI / Jenkins 연계

## 목적

Dev2의 역할은 CANoe native test를 대체하는 것이 아니라, native 결과와 외부 검증 산출물을
Jenkins가 바로 수집할 수 있는 형태로 정규화하는 것입니다. reviewer-facing 결과는 runtime module이 아니라
`BCM / IVI / CLUSTER / ADAS / V2X ...` 같은 surface ECU 기준으로 다시 묶습니다.

정리하면:

- Dev1: native CANoe Test Unit / `.vtestreport` / GUI 실행 증빙
- Dev2: `JSON + MD + JUnit XML` / evidence bundle / Jenkins bridge

## 권장 구조

### 1. Native test authoring

native CANoe Test Unit은 계속 CANoe 방식으로 유지합니다.

- `*.can`
- `*.vtestunit.yaml`
- `*.vtesttree.yaml`
- native `.vtestreport`

이 자산은 Dev1이 소유합니다.

### 2. External orchestration

Dev2는 아래 경로를 유지합니다.

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify batch --run-id 20260309_0900 --owner DEV2 --phase pre --report-formats json,md,junit
python scripts/run.py verify surface-bundle
```

`verify batch`가 끝나면 staging 산출물(`canoe/tmp/reports/verification`)을 기반으로
최종 reviewer/Jenkins 아카이브를 아래 경로에 재배치합니다.

- `artifacts/verification_runs/<run_id>/<phase>/reports`
- `artifacts/verification_runs/<run_id>/<phase>/surface`
- `artifacts/verification_runs/<run_id>/<phase>/native_reports`
- `artifacts/verification_runs/<run_id>/<phase>/evidence`
- `artifacts/verification_runs/<run_id>/<phase>/manifests`

phase별 판정은 동일하지 않습니다.

- `pre`
  - 런타임/툴링 안정성 중심
  - `doc-sync`, `capl-sync`는 architecture reset 동안 advisory(`WARN`)로 처리 가능
- `full`
  - closeout/release grade
  - 문서/코드/증빙 드리프트까지 hard fail로 처리

### 3. Jenkins ingestion

Jenkins는 아래 세 종류를 각각 다르게 취급합니다.

- `dev2_batch_report.junit.xml`
  - 빌드 판정 / trend / history
- `*.json`, `*.md`
  - 상세 분석 / 추적성 / 운영 검토
- `surface_evidence_bundle.*`, `surface/<bundle_key>/*`
  - surface ECU 기준 reviewer package / Jenkins archive
- `execution_manifest.*`
  - `run_id + phase + owner + scenario + Req/TestCase/Surface`를 같이 보는 최종 실행 메타데이터
  - `phase policy` 정보도 포함되어 실행의 판정 기준을 함께 남깁니다.
- native `.vtestreport`, screenshot
  - 원본 증빙 archive

## 현재 권장 산출물

- `canoe/tmp/reports/verification/dev2_batch_report.json`
- `canoe/tmp/reports/verification/dev2_batch_report.md`
- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`
- `canoe/tmp/reports/verification/surface_evidence_bundle.json`
- `canoe/tmp/reports/verification/surface_evidence_bundle.md`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.json`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.md`
- `artifacts/verification_runs/<run_id>/<phase>/reports/*`
- `artifacts/verification_runs/<run_id>/<phase>/surface/<bundle_key>/*`
- `artifacts/verification_runs/<run_id>/<phase>/manifests/artifact_manifest.json`
- `artifacts/verification_runs/<run_id>/<phase>/manifests/execution_manifest.json`
- `canoe/tmp/reports/verification/run_readiness.json`
- `canoe/tmp/reports/verification/doctor_report.json`
- native `.vtestreport` (Dev1 archive)

## Jenkins 예시

```groovy
pipeline {
  agent any
  stages {
    stage('SDV Verify Pre') {
      steps {
        bat 'python scripts/run.py verify batch --run-id %RUN_ID% --owner DEV2 --phase pre --report-formats json,md,junit'
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'canoe/tmp/reports/verification/dev2_batch_report.junit.xml'
      archiveArtifacts artifacts: 'artifacts/verification_runs/%RUN_ID%/**/*', fingerprint: true
    }
  }
}
```

샘플 파일 경로:

- `product/sdv_operator/examples/Jenkinsfile.verify`

## 왜 이렇게 나누는가

이 구조가 가장 교과서적인 이유는 다음과 같습니다.

1. native CANoe tool chain은 유지한다.
2. Dev2는 CI 친화 포맷만 추가한다.
3. Jenkins는 JUnit XML을 바로 읽을 수 있다.
4. reviewer-facing 묶음은 surface ECU 기준으로 다시 제공할 수 있다.
5. native `.vtestreport`는 final archive 내부 `native_reports/`로 복사되어 함께 보관된다.

즉, `vTESTstudio/CANoe native test`와 `Dev2 CI bridge`를 경쟁시키지 않고 직렬로 연결합니다.

## 참고 기준

- Vector automated testing:
  - https://www.vector.com/kr/ko/know-how/automated-testing/
- Vector Python interface for test automation:
  - https://www.vector.com/int/en/know-how/test-automation-using-the-python-interface/
- Jenkins JUnit step:
  - https://www.jenkins.io/doc/pipeline/steps/junit/
- Jenkins archiveArtifacts step:
  - https://www.jenkins.io/doc/pipeline/steps/core/#archiveartifacts-archive-the-artifacts
