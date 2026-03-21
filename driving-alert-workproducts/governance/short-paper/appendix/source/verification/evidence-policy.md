# 검증 증빙 로그 표준 (CANoe SIL)

원문:
- [../../verification/evidence-policy.md](../../verification/evidence-policy.md)

동기화 기준:
- `5d83ee7f`
- 원문이 이미 한국어 중심으로 유지되므로 `ko/` mirror는 canonical 내용을 그대로 따라갑니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> runtime, diagnostic, verification 세부사항 가운데 일부는 아직 구현 중이며 변경될 수 있습니다.

관련 운영 표준:
- `canoe/docs/verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`

## 1) 목적
- `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md`에 입력할 증빙 로그 포맷을 단일화합니다.
- 검증 축을 `로직(Logic) / 통신(Comm) / 주기(Period)`로 분리해 PASS 근거를 명확히 합니다.
- 실측값 없이 PASS가 기록되는 것을 방지합니다.

## 2) 고정 실행 순서
1. 개발완성도 체크: 컴파일 성공 + 핵심 경로 동작 확인(`Core/Body/Cluster/UiRender`)
2. 로그 표준 고정: `verification_log.csv` 필드 채우기
3. 시간 규칙 채점: `50/100/150/1000ms`
4. 패널 캡처: `차량화면 -> 제어패널 -> 상태모니터`
5. 05/06/07 반영: `Pass/Fail + 증빙 링크` 입력

## 3) 개발완성도 체크 기준 (Step 1)
- 컴파일 에러 0건
- 측정 시작 성공
- scenario 주입 시 아래 파생 출력이 유효값으로 변해야 합니다.
  - `Core::selectedAlertLevel`, `Core::selectedAlertType`
  - `Body::ambientMode`, `Body::ambientColor`, `Body::ambientPattern`
  - `Cluster::warningTextCode`
  - `UiRender::renderMode`, `UiRender::renderColor`, `UiRender::renderTextCode`

## 4) 증빙 폴더 규칙
- 루트: `canoe/logging/evidence/`
- 계층:
  - `UT/<run_id>/`
  - `IT/<run_id>/`
  - `ST/<run_id>/`
  - `FULL/<run_id>/` (`FULL`은 회귀 전용이며 공식 closeout seed는 없습니다.)
- 각 run 폴더의 최소 필수 파일:
  - `verification_log.csv`
  - `raw_write_window.txt`
  - `capture_index.csv`
  - `captures/`
  - `native_reports/`
  - `native_report_manifest.json`
  - `supplementary/trace/`
  - `supplementary/logging/`

### Write Window Drop Root
- 루트: `canoe/logging/evidence/incoming/`
- tier별 표준 저장 파일:
  - `UT/raw_write_window.txt`
  - `IT/raw_write_window.txt`
  - `ST/raw_write_window.txt`
  - `FULL/raw_write_window.txt`
- GUI의 Write Window export 기본 경로는 위 경로로 고정합니다.
- `post-run` 자동화는 위 표준 경로를 우선 수집하고, 기존 `canoe/tmp/write_window/`는 migration fallback으로만 사용합니다.

### Trace and Logging Drop Root
- 루트: `canoe/logging/evidence/incoming/`
- tier별 표준 supplementary 경로:
  - `UT/trace/`, `IT/trace/`, `ST/trace/`, `FULL/trace/`
  - `UT/logging/`, `IT/logging/`, `ST/logging/`, `FULL/logging/`
- CAN/Ethernet trace export, logging block output, BLF/ASC/MF4/PCAP 계열 산출물은 위 경로에 저장합니다.
- `post-run`은 위 경로를 자동 수집해 run-local `supplementary/trace`, `supplementary/logging`으로 복사합니다.

### Write Window 키워드 규칙
- 입력 이벤트: `[EVIDENCE_IN] scenario=<id> inputTsMs=<ms>`
- 출력 이벤트: `[EVIDENCE_OUT] scenario=<id> outputTsMs=<ms> result=<0|1> ...`
- `inputTsMs`, `outputTsMs`를 이용해 `latency_ms`를 계산합니다.

### Seed Source 규칙
- `verification_log.csv` 초기 row는 수동 템플릿 복사가 아니라 `scripts/quality/init_evidence_run.py`로 생성합니다.
- seed SoT:
  - `driving-alert-workproducts/05_Unit_Test.md`
  - `driving-alert-workproducts/06_Integration_Test.md`
  - `driving-alert-workproducts/07_System_Test.md`
  - `canoe/docs/verification/test-asset-mapping.md`
  - `canoe/tests/modules/test_units/<asset>/<asset>.can`
- `expected`는 공식 `05/06/07` 표에서 추출합니다.
- `scenario_id`는 native CAPL의 `launchScenarioAndWait(...)` 호출에서 시드합니다.
- `rule_type` / `rule_ms`는 공식 표 문장에 대한 deterministic seed이며, 애매한 row는 `note`에 manual confirmation을 남깁니다.
- `FULL`은 regression tier이므로 `prepare` seed 대상이 아니며, `collect/post-run`으로 native report와 raw log만 저장합니다.

## 5) verification_log.csv 필수 컬럼
- `tier`: `UT|IT|ST`
- `test_id`
- `native_asset`
- `scenario_id`
- `input_ts_ms`
- `output_ts_ms`
- `latency_ms` (비어 있어도 채점기가 계산)
- `rule_type`: `LE|GE|BETWEEN|EQ`
- `rule_ms`: 예) `150`, `1000`, `1000:1300`
- `expected`
- `observed`
- `logic_verdict`: `PASS|FAIL`
- `comm_verdict`: `PASS|FAIL`
- `verdict`: 수동 입력값(선택)이며, 최종 판정은 채점기 결과(`computed_verdict`)를 기준으로 합니다.
- `owner`
- `run_date`: `YYYY-MM-DD`
- `evidence_log_path`
- `evidence_capture_path`
- `note`

### 관찰 문자열(observed) 표준
- `observed`는 현재 `[EVIDENCE_OUT]`의 핵심 필드를 key/value 문자열로 저장합니다.
- 기본 포함 필드:
  - `level`, `type`, `code`, `timeout`, `risk`, `decel`, `failSafe`, `renderType`, `renderCode`
- 선택 포함 필드:
  - `release`, `objValid`, `objClass`, `objTtc`, `objEvent`

## 6) 판정 규칙
### 6.1 주기(Period)
- `LE`: `latency_ms <= rule_ms`
- `GE`: `latency_ms >= rule_ms`
- `BETWEEN`: `min <= latency_ms <= max`
- `EQ`: `latency_ms == rule_ms`

### 6.2 로직(Logic)
- 로직 기대값(`expected`)과 실제 상태(`observed`)를 비교해 `logic_verdict`를 기록합니다.

### 6.3 통신(Comm)
- 기대 경로의 파생 출력 반영 여부를 `comm_verdict`로 기록합니다.
- 예: `Core -> Body -> UiRender`, `Core -> Cluster -> UiRender`

### 6.4 최종 판정
- `computed_verdict = PASS` 조건:
  - 주기 판정 PASS
  - `logic_verdict=PASS`
  - `comm_verdict=PASS`
  - `owner`, `run_date`, `evidence_*`가 비어 있지 않을 것
- 위 조건 중 하나라도 위반하면 FAIL입니다.

## 7) 표준 시간 기준
- `50ms`: 출력 주기
- `100ms`: 입력/통신 주기
- `150ms`: 즉시 반영 상한(`100ms + 50ms`)
- `1000ms`: timeout clear 기준

## 8) 캡처 규칙
- 테스트당 최소 3장:
  - `{test_id}_01_vehicle.png`
  - `{test_id}_02_control.png`
  - `{test_id}_03_monitor.png`
- `capture_index.csv`에 파일 경로와 설명을 반드시 매핑합니다.

## 9) 실행 명령 예시
```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner <OWNER>
```

## 10) 05/06/07 반영 규칙
- `computed_verdict`를 기준으로 문서 상단 `Pass/Fail`을 입력합니다.
- `evidence_log_path`, `evidence_capture_path`를 테스트 ID와 1:1로 연결합니다.
- 문서 값과 scored report 값이 다르면 문서를 FAIL로 처리합니다.
- trace/log 관련 테스트는 `supplementary/trace` 또는 `supplementary/logging` 없이 closeout 완료로 보지 않습니다.

## 11) 승인 규칙
- 자동화는 candidate verdict까지만 생성합니다.
- 공식 `PASS/FAIL` 반영 전에는 reviewer approval이 필요합니다.
- `FAIL` 또는 `ERROR`는 `templates/fail_disposition_template.md` 기준 disposition을 남깁니다.
