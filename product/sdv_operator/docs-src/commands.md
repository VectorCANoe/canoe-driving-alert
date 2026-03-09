# 명령 표면

운영자는 아래 4개 명령만 먼저 익히면 됩니다.

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
python scripts/run.py doctor
```

Campaign / CI 확장 표면:

```powershell
python scripts/run.py verify batch --run-id 20260310_0900 --campaign-id CMP_20260310 --owner DEV2 --phase pre --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0 --report-formats json,md,junit
python scripts/run.py artifact open --target campaign-profiles
python scripts/run.py artifact open --target role-boundary-doc
```

## 핵심 4개

### Gate all

```powershell
python scripts/run.py gate all
```

사용 시점:
- 런타임 조작 전에 전체 gate를 먼저 확인할 때
- 문서/DBC/CAPL/Verification Console 정합성을 먼저 점검할 때

### Scenario run

```powershell
python scripts/run.py scenario run --id 4
python scripts/run.py scenario run --id 4 --var testScenario
```

사용 시점:
- CANoe measurement가 이미 올라와 있을 때
- Test namespace sysvar로 시나리오를 주입할 때

### Verify quick

```powershell
python scripts/run.py verify quick
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

사용 시점:
- 시나리오 직후 첫 증빙을 빠르게 수집할 때
- 준비 상태, 누락 항목, 증빙 경로를 바로 확인할 때
- 현재 붙은 CANoe 세션이 올바른 cfg/measurement인지 함께 확인할 때

참고:
- `verify quick`는 `doctor(auto-start) -> prepare -> smoke -> status` 순서로 동작합니다.

### Doctor

```powershell
python scripts/run.py doctor
python scripts/run.py doctor --ensure-running
```

사용 시점:
- COM attach 가능 여부를 확인할 때
- measurement, sysvar, runtime 경계를 빠르게 점검할 때

## 운영 모드

### Verification Console

```powershell
python scripts/run.py
python scripts/run.py tui
```

용도:
- 운영 콘솔로 핵심 작업을 클릭/입력 기반으로 실행
- 결과, 로그, COM 상태, 증빙 경로를 한 화면에서 검토
- `Results`와 `Artifacts`에서 최근 증빙, native report, execution manifest, 원본 기준 파일을 바로 연다

### Plain shell

```powershell
python scripts/run.py shell
```

용도:
- 화면형 Verification Console이 맞지 않는 터미널 환경에서 fallback으로 사용
- 반복 명령을 빠르게 직접 입력할 때 사용

### Guided flow

```powershell
python scripts/run.py start guided
python scripts/run.py start demo --id 4
python scripts/run.py start precheck --owner DEV2
```

용도:
- 단계형 안내가 필요한 경우
- 터미널 fallback이나 운영 시연용 흐름이 필요할 때

<details>
<summary>확장 명령 보기</summary>

### Verify pipeline

#### Prepare

```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
```

#### Batch

```powershell
python scripts/run.py verify batch --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --phase pre --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0
python scripts/run.py verify batch --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --phase post --surface-scope ADAS --repeat-count 3 --duration-minutes 30 --interval-seconds 10
python scripts/run.py verify batch --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --phase full --surface-scope BCM --repeat-count 1 --duration-minutes 0 --interval-seconds 0
python scripts/run.py verify batch --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --phase pre --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0 --report-formats json,md,junit
```

권장:

- 내부 검토: `json,md`
- Jenkins 연계: `json,md,junit`
- `phase`에 따라 verdict policy가 달라집니다.
  - `pre`: advisory gate 허용 (`WARN`)
  - `full`: closeout strict (`FAIL`)
- `campaign_id`는 build/nightly/repeat 묶음 식별자입니다.
- `surface_scope`는 reviewer-facing으로 집중해서 볼 surface ECU 범위입니다.
- `repeat_count / duration_minutes / interval_seconds`는 반복 실행 의도와 운영 profile 기록입니다.

참고:
- `verify batch --phase pre/full`은 pre 단계 시작 전에 `doctor(auto-start)`를 같이 실행합니다.
- 현재 CANoe 세션에 validation harness sysvar가 없으면 `doctor` 단계에서 먼저 드러나고, pre batch는 그 지점에서 종료됩니다.
- batch가 끝나면 staging 산출물은 `artifacts/verification_runs/<run_id>/<phase>/`로 다시 materialize됩니다.

#### Precheck batch

```powershell
python scripts/run.py start precheck --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0
```

사용 시점:

- full batch 전에 현재 작업 상태를 한 번에 스냅샷하고 싶을 때
- gate + prepare + smoke + status를 같은 execution metadata로 묶고 싶을 때

#### Surface bundle

```powershell
python scripts/run.py verify surface-bundle
```

사용 시점:
- reviewer-facing 결과를 runtime module이 아니라 surface ECU 기준으로 다시 묶을 때
- Jenkins archive를 `BCM / IVI / CLUSTER / ADAS / V2X ...` 번들로 정리할 때

참고:
- `verify batch`는 내부적으로 이 단계를 자동 수행합니다.
- 단독 실행은 기존 staging 결과만 다시 rollup하고 싶을 때 사용합니다.
- 기본 입력:
  - `product/sdv_operator/config/surface_ecu_inventory.json`
  - `product/sdv_operator/config/surface_traceability_profile.json`
  - `canoe/tmp/reports/verification/dev_completeness_smoke.csv`
- 핵심 출력:
  - `canoe/tmp/reports/verification/surface_evidence_bundle.json`
  - `canoe/tmp/reports/verification/surface_evidence_bundle.md`
  - `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.json`
  - `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.md`
- 의미:
  - `run_id / phase / owner / run_date`는 이번 실행을 식별하는 execution key입니다.
  - `Req ID / Test Case ID / Scenario ID / Surface ECU`는 reviewer가 계속 추적하는 stable key입니다.
  - surface bundle은 이 두 층을 하나의 reviewer-facing 결과로 합칩니다.

#### Smoke

```powershell
python scripts/run.py verify smoke --owner DEV1
```

#### Fill and score

```powershell
python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1
```

#### Insight

```powershell
python scripts/run.py verify insight --run-id 20260306_1930
python scripts/run.py verify insight --run-id 20260306_1930 --baseline-run-id 20260305_1800
```

#### Bind documentation

```powershell
python scripts/run.py verify bind-doc --run-id 20260306_1930
python scripts/run.py verify fill-template --run-id 20260306_1930 --owner-fallback DEV1
```

#### Status and finalize

```powershell
python scripts/run.py verify status --run-id 20260306_1930
python scripts/run.py verify finalize --run-id 20260306_1930 --owner DEV1
```

### Gate command set

```powershell
python scripts/run.py gate doc-sync
python scripts/run.py gate cfg-hygiene
python scripts/run.py gate capl-sync
python scripts/run.py gate multibus-dbc
python scripts/run.py gate cli-readiness
```

### CAPL / CANoe COM

#### SysVar access

```powershell
python scripts/run.py capl sysvar-get --namespace Core --var failSafeMode
python scripts/run.py capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int
```

#### Measurement control

```powershell
python scripts/run.py canoe measure-status
python scripts/run.py canoe measure-start
python scripts/run.py canoe measure-stop
python scripts/run.py canoe measure-reset
```

#### CAPL function call

```powershell
python scripts/run.py canoe capl-call --function-name MyFunction --args 1 2 --arg-type int
```

### Packaging

```powershell
python scripts/run.py artifact list --scope staging
python scripts/run.py artifact list --scope archive --latest
python scripts/run.py artifact list --scope source
python scripts/run.py artifact open --target surface-bundle
python scripts/run.py artifact open --target execution-manifest --latest
python scripts/run.py artifact open --target native-reports --latest
python scripts/run.py artifact open --target surface-inventory
python scripts/run.py artifact open --target results-doc
python scripts/run.py package validate-contract
python scripts/run.py package clean --scope staging --yes
python scripts/run.py package build-exe --mode onefolder --clean
python scripts/run.py package build-exe --mode onefile --clean
python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe
```

의미:

- `artifact list`
  - staging / archive / source 기준으로 현재 확인 가능한 산출물과 원본 계약 파일을 나열합니다.
- `artifact open`
  - 결과 문서, execution manifest, native reports, surface inventory 같은 원본/산출물 파일을 외부 편집기/탐색기로 바로 엽니다.
- `artifact clean`
  - generated output만 정리합니다. 기본은 preview이고 실제 삭제는 `--yes`가 필요합니다.

</details>

## 운영 규칙

- 공개 표면은 canonical 명령 중심으로 유지합니다.
- compatibility alias는 내부 호환용으로만 유지합니다.
- 결과 해석은 Verification Console 또는 generated docs에서 우선 확인합니다.
- 구현 세부사항은 `scripts/` 내부 모듈에서 관리합니다.
