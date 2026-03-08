# CI / Jenkins 연계

## 목적

Dev2의 역할은 CANoe native test를 대체하는 것이 아니라, native 결과와 외부 검증 산출물을
Jenkins가 바로 수집할 수 있는 형태로 정규화하는 것입니다.

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
```

### 3. Jenkins ingestion

Jenkins는 아래 세 종류를 각각 다르게 취급합니다.

- `dev2_batch_report.junit.xml`
  - 빌드 판정 / trend / history
- `*.json`, `*.md`
  - 상세 분석 / 추적성 / 운영 검토
- native `.vtestreport`, screenshot
  - 원본 증빙 archive

## 현재 권장 산출물

- `canoe/tmp/reports/verification/dev2_batch_report.json`
- `canoe/tmp/reports/verification/dev2_batch_report.md`
- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`
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
      archiveArtifacts artifacts: 'canoe/tmp/reports/verification/*, canoe/**/*.vtestreport', fingerprint: true
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
4. native `.vtestreport`는 원본 증빙으로 그대로 남긴다.

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
