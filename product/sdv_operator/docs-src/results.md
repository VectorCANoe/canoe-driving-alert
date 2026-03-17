# 결과 해석

운영 원칙:

- `canoe/tmp/reports/verification`는 실행 중간 결과를 쌓는 staging 영역입니다.
- reviewer/Jenkins 기준 최종 보관은 `artifacts/verification_runs/<run_id>/<phase>/`만 봅니다.
- staging 결과는 Git에 커밋하지 않습니다.

## 판정 체계

- `PASS`
  - 명령이 정상 종료되었고 핵심 결과가 기대 범위에 있습니다.
- `WARN`
  - 실행은 끝났지만 추가 조치가 필요합니다.
  - 예: measurement stopped, missing marker, PREPARED_PARTIAL
- `FAIL`
  - 실행 자체가 실패했거나 핵심 경로가 끊겼습니다.

## 주요 결과 카드

Results 화면은 먼저 아래 4블록을 읽는 구조입니다.

- `Verdict`
- `Reason`
- `Evidence`
- `Actions`

### Verdict

- 가장 최근 실행의 최종 판정
- 상세 사유
- 연결된 증빙 경로

### Reason

- 현재 단계
- 병목 1줄
- 다음 액션 1줄

### Evidence

- 최근 증빙 경로
- native report 경로
- supplementary trace/logging 경로
- execution manifest 경로
- 원본 기준 경로

### Actions

- `증빙 열기`
- `supplementary trace`
- `supplementary logging`
- `surface archive`
- `native report 열기`
- `execution manifest`
- `원본 기준 열기`
- `staging 정리`

## 지원 카드

아래 줄은 support 정보입니다.

- `Recent Runs`
- `Batch Snapshot`
- `Tier Readiness`
- `Runtime`

### Runtime

- CANoe COM attach 상태
- measurement 상태
- doctor 기반 핵심 런타임 확인 결과
- Gate / Scenario / Verify 타임라인

### Tier Readiness

- `UT / IT / ST` 별 marker / filled / scored 상태
- `run_readiness.json` 기준으로 표시

### Batch Snapshot

- `dev2_batch_report.json` 기준
- phase / status / pass-fail 요약
- `pre`에서는 advisory gate 실패가 `WARN`으로 남을 수 있습니다.
- `full`에서는 같은 항목이 `FAIL`이 될 수 있습니다.

### Surface Evidence Bundle

- reviewer-facing 결과 묶음
- runtime module 이름이 아니라 `BCM / IVI / CLUSTER / ADAS / V2X / ...` 기준으로 표시
- `surface_evidence_bundle.json/md`와 `surface/<bundle_key>/bundle.*`를 기준으로 해석
- 각 surface bundle에는 다음이 함께 들어갑니다.
  - `mapping_status`
  - `req_ids`
  - `test_case_ids`
  - `scenario_ids`
  - `native_test_assets`
  - `doc_refs`
- `profile_id`
- `pack_id`

즉 Results 화면에서 보이는 surface 결과는 단순 실행 로그가 아니라:

- 어떤 `campaign profile`로 돌렸는지
- 어떤 `verification pack`을 기준으로 묶였는지
- 어떤 `source contract`에서 왔는지

까지 같이 읽는 구조입니다.

### Execution Manifest

- 실행 인스턴스 식별자와 reviewer-facing 식별자를 함께 묶는 최종 manifest입니다.
- `run_id`는 이번 한 번의 실행 묶음을 식별합니다.
- `Req / TestCase / Surface ECU / Scenario`는 고정 traceability 키입니다.
- 즉 OEM식으로 보면:
  - `run_id` = execution key
  - `Req/TestCase/Surface/Scenario` = stable review key
  - `phase policy` = 이번 실행에서 무엇이 blocking인지 정의하는 verdict policy

## 증빙 경로

주요 산출물은 아래 경로에 생성됩니다.

- staging:
  - `canoe/tmp/reports/verification/*`
- `canoe/tmp/reports/verification/doctor_report.json`
- `canoe/tmp/reports/verification/run_readiness.json`
- `canoe/tmp/reports/verification/dev2_batch_report.json`
- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`
- `canoe/tmp/reports/verification/run_insight_report.json`
- `canoe/tmp/reports/verification/run_insight_report.md`
- `canoe/tmp/reports/verification/doc_binding_bundle.csv`
- `canoe/tmp/reports/verification/doc_binding_bundle.json`
- `canoe/tmp/reports/verification/doc_binding_bundle.md`
- `canoe/tmp/reports/verification/doc_fill_template.csv`
- `canoe/tmp/reports/verification/doc_fill_template.md`
- `canoe/tmp/reports/verification/surface_evidence_bundle.json`
- `canoe/tmp/reports/verification/surface_evidence_bundle.md`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.json`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.md`
- `canoe/logging/evidence/<UT|IT|ST|FULL>/<run-id>/...`
- `canoe/logging/evidence/incoming/<UT|IT|ST|FULL>/raw_write_window.txt`
- `canoe/logging/evidence/incoming/<UT|IT|ST|FULL>/trace/**/*`
- `canoe/logging/evidence/incoming/<UT|IT|ST|FULL>/logging/**/*`

- final archive:
  - `artifacts/verification_runs/<run-id>/<phase>/reports/*`
  - `artifacts/verification_runs/<run-id>/<phase>/surface/<bundle_key>/*`
  - `artifacts/verification_runs/<run-id>/<phase>/native_reports/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/evidence/<UT|IT|ST|FULL>/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/evidence/<UT|IT|ST|FULL>/supplementary/trace/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/evidence/<UT|IT|ST|FULL>/supplementary/logging/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/manifests/artifact_manifest.json`
  - `artifacts/verification_runs/<run-id>/<phase>/manifests/execution_manifest.json`

`dev2_batch_report.junit.xml`은 Jenkins 수집용 ingress 포맷입니다.

## 권장 확인 순서

1. 하단 Log 패널에서 실행 흐름 확인
2. Results에서 verdict 확인
3. COM Runtime과 Tier Readiness 확인
4. Batch Snapshot의 Surface 요약에서 `BCM / IVI / CLUSTER / ADAS / V2X` 우선순위를 확인
5. 필요하면 `surface archive`로 archive 내부 surface bundle을 직접 연다
6. 필요한 경우 Artifacts 화면에서 증빙 파일과 원본 기준 파일을 직접 연다
7. CI/Jenkins 역할 분리는 Automation 화면에서 확인한다

## 제품 안에서 바로 하는 작업

Verification Console 안에서는 아래 흐름을 바로 사용할 수 있습니다.

- 결과 보기
  - `Results` 화면에서 verdict / insight / surface bundle / execution timeline 확인
  - `증빙 열기` 버튼으로 최근 증빙 바로 열기
  - `surface archive` 버튼으로 archive 내부 surface bundle 폴더 바로 열기
  - `native report 열기` 버튼으로 archive 내부 native CANoe report 확인
  - `supplementary trace` 버튼으로 archive 내부 supplementary trace evidence 확인
  - `supplementary logging` 버튼으로 archive 내부 supplementary logging evidence 확인
  - `execution manifest` 버튼으로 이번 실행의 최종 manifest 확인
  - `원본 기준 열기` 버튼으로 source contract 바로 열기
  - `staging 정리` 버튼으로 generated staging output 정리
  - closeout 단계에서는 `run insight / doc binding bundle / doc fill template`를 함께 보고 문서 반영 준비 상태를 확인
- Artifacts 화면
  - `Staging Outputs / Final Archive / Source Contracts / Build Outputs`를 나눠서 확인
  - `최근 증빙 열기`, `native report 열기`, `execution manifest`, `최신 archive 열기`, `원본 기준 열기`, `빌드 출력 열기` 버튼으로 바로 이동
  - `surface archive` 버튼으로 최신 archive의 `surface/` 하위 경로 바로 열기
- 산출물 열기
  - `artifact open --target batch-report`
  - `artifact open --target run-insight`
  - `artifact open --target doc-binding-bundle`
  - `artifact open --target doc-fill-template`
  - `artifact open --target surface-bundle`
  - `artifact open --target surface-dir --latest`
  - `artifact open --target execution-manifest --latest`
  - `artifact open --target native-reports --latest`
  - `artifact open --target evidence-dir --latest`
  - `artifact open --target supplementary-trace --latest`
  - `artifact open --target supplementary-logging --latest`
- 원본 계약 파일 열기
  - `artifact open --target surface-inventory`
  - `artifact open --target unit-test-doc`
  - `artifact open --target integration-test-doc`
  - `artifact open --target system-test-doc`
  - `artifact open --target active-test-units-guide`
  - `artifact open --target active-test-suites-guide`
  - `artifact open --target execution-guide`
  - `artifact open --target capability-matrix-json`
  - `artifact open --target traceability-profile`
  - `artifact open --target artifact-layout`
  - `artifact open --target results-doc`
- 산출물 정리
  - `artifact clean --scope staging`
- `artifact clean --scope staging --yes`

즉, 결과를 본 뒤 같은 제품 표면에서 산출물과 원본 계약 파일까지 바로 따라갈 수 있어야 합니다.

## Closeout Carry-Forward

`bind-doc / fill-template / finalize` 단계에서는 아래 필드가 문서 closeout 기준으로 함께 전달됩니다.

- `scenario_id`
- `native_asset`
- `expected`
- `rule_type`
- `rule_ms`

즉 Results는 단순 PASS/FAIL 확인 화면이 아니라, 문서 팀이 바로 넘겨받을 closeout 기준값까지 추적하는 운영 표면입니다.

## Supplementary Evidence Rule

transport/timing-visible tests는 `vtestreport + verification_log.csv`만으로 닫지 않습니다.

- archive evidence는 `native report + supplementary trace/logging + verification log + reviewer approval`
  묶음으로 해석합니다.
- Write Window는 current score-gate의 parser source로 유지되지만, reviewer-facing evidence의 주력은
  archive 내부 supplementary trace/logging입니다.

## Verification Pack과 Results의 관계

현재 Results는 아래 active suite 축을 기준으로 읽습니다.

1. `ts_canoe_ut_active_baseline`
- 05 Unit Test executable baseline

2. `ts_canoe_it_active_baseline`
- 06 Integration Test executable baseline

3. `ts_canoe_st_active_baseline`
- 07 System Test executable baseline

4. `ts_canoe_full_active_baseline`
- UT/IT/ST wrapper baseline

즉 Results에서는 pack 이름만 보는 것이 아니라, 해당 run이 어떤 suite wrapper와 어떤 문서 매핑 기준으로 묶였는지 함께 확인해야 합니다.
