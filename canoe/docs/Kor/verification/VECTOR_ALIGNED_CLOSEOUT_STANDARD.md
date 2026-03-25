# Vector-Aligned Verification Closeout Standard

원문:
- [../../verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md](../../verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md)

동기화 기준:
- `5d83ee7f`
- Vector 제품명, command, path, asset 이름은 원문과 동일하게 유지합니다.

## 1. 목적

이 표준은 이 저장소에서 CANoe SIL verification closeout을 마감하는 공식 운영 모델을 정의합니다.

이 표준이 고정하는 항목은 다음과 같습니다.
- execution authority
- run/evidence path layout
- post-run automation boundary
- PASS/FAIL state transition rule
- FAIL disposition format
- reviewer approval flow

## 2. Vector-aligned 원칙

이 운영 모델은 Vector의 공개 가이드와 제품 포지셔닝을 따릅니다.

1. `CANoe`는 simulation, stimulation, testing, analysis를 위한 core execution platform입니다.
2. `vTESTstudio`와 native test asset은 authoritative automated test asset입니다.
3. authoritative test report artifact는 native test execution에서 생성됩니다.
4. CANoe는 open platform이므로 외부 toolchain, CI, lab environment와 연동될 수 있습니다.
5. 외부 자동화는 artifact를 수집하고 정규화하고 문서에 묶을 수 있지만, native execution과 native report authority를 대체하면 안 됩니다.

## 3. 출처

이 운영 모델이 따르는 주요 공식 출처는 아래와 같습니다.

1. Vector, CANoe as the core platform for executing tests and simulating/stimulating the environment  
   https://medical.vector.com/articles/simulation-of-surrounding-systems-for-the-extracorporeal-life-support-system-rotaflow
2. Vector, vTESTstudio supports reusable tests and automatic test reports  
   https://medical.vector.com/articles/vteststudio-comfortable-design-of-automated-test-sequences-for-embedded-systems
3. Vector, CANoe is a scalable platform from development to system-level tests  
   https://medical.vector.com/
4. Vector, CANoe open interfaces and extensibility allow integration into toolchains, CI, and lab environments  
   https://medical.vector.com/articles/sdc-validation
5. Vector tutorial snippet, test execution is started in CANoe and the resulting test report is opened afterward  
   https://support.vector.com/sys_attachment.do?sys_id=3a157dec876401d0b9f233770cbb354b

## 4. 실행 권한

### 4.1 Authoritative execution layer

authoritative execution layer은 아래로 고정합니다.
- CANoe measurement
- CANoe Test Configuration
- native test asset
- native Vector report output

### 4.2 External automation boundary

외부 자동화는 아래 범위까지만 허용합니다.

- run folder initialization
- native report collection
- Write Window evidence parsing
- verdict normalization
- document binding bundle generation
- fill template generation

외부 자동화가 해서는 안 되는 작업은 아래와 같습니다.

- CANoe native execution 대체
- native verdict authority 덮어쓰기
- reviewer 승인 없이 공식 `05/06/07` verdict 직접 변경

## 5. Tier 모델

### 5.1 공식 closeout tier

공식 closeout tier는 아래 세 개뿐입니다.

- `UT`
- `IT`
- `ST`

이 tier만 아래 공식 문서의 `PASS/FAIL` state transition을 직접 구동할 수 있습니다.

- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`
- `00g_Master_Test_Matrix.md`

### 5.2 Regression tier

`FULL`은 regression 전용 tier입니다.

규칙:
- `FULL`은 별도의 run/configuration context를 사용해야 합니다.
- `FULL`은 `UT/IT/ST`와 동시에 실행하면 안 됩니다.
- `FULL`은 `UT/IT/ST`의 per-ID closeout evidence를 대체하지 못합니다.
- `FULL`은 추가 regression evidence로만 첨부할 수 있습니다.

## 6. Run 모델

### 6.1 표준 실행 순서

1. `prepare`
2. CANoe GUI measurement start
3. CANoe GUI test execution
4. CANoe native logging/trace export를 canonical incoming path에 저장
5. GUI Write Window export를 canonical incoming path에 저장
6. `post-run`
7. `bind-doc`
8. `fill-template`
9. reviewer approval
10. 공식 문서 업데이트

### 6.2 GUI-first 규칙

아래 항목은 계속 GUI-authoritative 상태로 유지합니다.

- `.cfg` open/save/save as
- `.cfg.ini`, `.stcfg`
- measurement start/stop
- test execution start
- native report generation

## 7. Canonical evidence path

### 7.1 Canonical evidence root

`canoe/logging/evidence/`

### 7.2 Run 단위 root

run별 root는 아래와 같습니다.

- `canoe/logging/evidence/UT/<run_id>/`
- `canoe/logging/evidence/IT/<run_id>/`
- `canoe/logging/evidence/ST/<run_id>/`
- `canoe/logging/evidence/FULL/<run_id>/`

### 7.3 Canonical incoming drop root

canonical incoming root는 아래와 같습니다.

- `canoe/logging/evidence/incoming/`

Write Window export는 아래 경로에만 저장합니다.

- `incoming/UT/raw_write_window.txt`
- `incoming/IT/raw_write_window.txt`
- `incoming/ST/raw_write_window.txt`
- `incoming/FULL/raw_write_window.txt`

supplementary native export는 아래 경로에만 저장합니다.

- `incoming/UT/trace/`
- `incoming/IT/trace/`
- `incoming/ST/trace/`
- `incoming/FULL/trace/`
- `incoming/UT/logging/`
- `incoming/IT/logging/`
- `incoming/ST/logging/`
- `incoming/FULL/logging/`

legacy `canoe/tmp/write_window/`는 migration fallback으로만 사용합니다.

### 7.4 Run 단위 필수 artifact

`UT/IT/ST` closeout의 최소 필수 artifact는 아래와 같습니다.

- `verification_log.csv`
- `capture_index.csv`
- `raw_write_window.txt`
- `native_reports/`
- `native_report_manifest.json`

trace/log 관련 ID에서 요구하는 supplementary artifact:

- `supplementary/trace/`
- `supplementary/logging/`

권장 artifact:

- `captures/`
- scored summary output
- doc binding bundle
- fill template bundle

## 8. Native report 규칙

native CANoe/Vector report는 authoritative execution artifact입니다.

규칙:
- summary `Report_<TIER>_ACTIVE_BASELINE.vtestreport`를 수집합니다.
- 가능한 per-test `Report_*.vtestreport`를 함께 수집합니다.
- 대응하는 report settings file도 함께 수집합니다.
- run-local `native_reports/` tree 아래에 저장합니다.

어떤 custom external script도 native report verdict generation을 대체할 수 없습니다.

## 8A. Native logging 및 trace 규칙

transport-visible test와 timing-visible test에서는 native CANoe logging/trace export를 first-class supplementary evidence로 취급합니다.

규칙:
- transport evidence는 Write Window text 단독보다 CANoe native trace/logging export를 우선합니다.
- logging block export와 trace export는 run-local supplementary tree로 수집합니다.
- `post-run`은 아래 경로를 수집해야 합니다.
  - `incoming/<TIER>/trace/**/*`
  - `incoming/<TIER>/logging/**/*`
- 현재 score-gate는 `[EVIDENCE_IN]` / `[EVIDENCE_OUT]` marker를 Write Window에서 파싱하므로 Write Window는 여전히 필수입니다.
- reviewer closeout은 `native report + supplementary trace/logging + verification_log.csv` 조합을 우선하고, Write Window는 parser/evidence support로 사용합니다.

## 9. PASS/FAIL state transition 규칙

### 9.1 Candidate verdict

자동화는 candidate verdict만 생성할 수 있습니다.

candidate verdict는 아래를 기준으로 계산합니다.

- native run 존재 여부
- `verification_log.csv`
- parsed evidence
- computed scoring
- document binding alignment

### 9.2 Final verdict

공식 final verdict는 reviewer 승인 후에만 변경할 수 있습니다.

필수 조건:
- native report가 존재할 것
- 공식 test ID에 대한 evidence row가 존재할 것
- candidate verdict가 비어 있지 않을 것
- evidence link가 있을 것
- 실패가 있다면 disposition record가 있을 것

## 10. FAIL disposition 표준

모든 `FAIL` 또는 `ERROR` row는 disposition record를 가져야 합니다.

필수 필드:
- `tier`
- `test_id`
- `scenario_id`
- `native_asset`
- `run_id`
- `failure_class`
- `symptom`
- `root_cause_summary`
- `reproduction_steps`
- `native_report_path`
- `evidence_log_path`
- `trace_or_capture_path`
- `fix_status`
- `retest_required`
- `retest_run_id`
- `final_decision`
- `owner`
- `reviewer`
- `decision_date`

## 11. Reviewer 승인 흐름

### 11.1 Candidate 생성

자동화는 아래를 생성합니다.

- scored verification log
- doc binding bundle
- fill template

### 11.2 Engineering review

validation/test owner는 아래를 검토합니다.

- candidate verdict
- evidence completeness
- failure disposition 존재 여부

### 11.3 문서 승인

문서 owner는 review 승인 이후에만 공식 `05/06/07`과 `00g`를 업데이트합니다.

## 12. 운영 명령

표준 흐름:

```powershell
python scripts/quality/run_verification_pipeline.py prepare --run-id <RUN_ID>
python scripts/quality/run_verification_pipeline.py post-run --run-id <RUN_ID> --tier <UT|IT|ST|FULL> --owner <OWNER>
python scripts/quality/run_verification_pipeline.py bind-doc --run-id <RUN_ID>
python scripts/quality/run_verification_pipeline.py fill-template --run-id <RUN_ID>
```

## 13. 프로젝트 고정 결정

이 저장소는 Vector 기본 가이드 위에 아래 제약을 추가로 고정합니다.

1. verification scope는 CANoe SIL, CAN + Ethernet only로 고정합니다.
2. `UT/IT/ST`만 공식 closeout tier입니다.
3. `FULL`은 regression-only입니다.
4. 공식 문서 verdict 변경은 reviewer 승인 후에만 가능합니다.
