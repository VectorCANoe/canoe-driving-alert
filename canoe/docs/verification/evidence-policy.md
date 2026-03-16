# 검증 증빙 로그 표준 (CANoe SIL)

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## 1) 목적
- `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md`에 입력할 증빙 로그 포맷을 단일화한다.
- 검증 축을 `로직(Logic) / 통신(Comm) / 주기(Period)`로 분리해 PASS 근거를 명확히 한다.
- 실측값 없이 PASS가 나오는 것을 방지한다.

## 2) 고정 실행 순서
1. 개발완성도 체크: 컴파일 성공 + 핵심 경로 동작 확인(`Core/Body/Cluster/UiRender`)
2. 로그 표준 고정: `verification_log.csv` 필드 채우기
3. 시간 규칙 채점: `50/100/150/1000ms`
4. 패널 캡처: `차량화면 -> 제어패널 -> 상태모니터`
5. 05/06/07 반영: `Pass/Fail + 증빙 링크` 입력

## 3) 개발완성도 체크 기준 (Step 1)
- 컴파일 에러 0건
- 측정 시작 성공
- 시나리오 주입 시 아래 파생 출력이 유효값으로 변한다.
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
- 각 run 폴더 최소 파일:
  - `verification_log.csv`
  - `raw_write_window.txt`
  - `capture_index.csv`

### Write Window 키워드 규칙
- 입력 이벤트: `[EVIDENCE_IN] scenario=<id> inputTsMs=<ms>`
- 출력 이벤트: `[EVIDENCE_OUT] scenario=<id> outputTsMs=<ms> result=<0|1> ...`
- `inputTsMs`, `outputTsMs`를 이용해 `latency_ms`를 계산한다.

## 5) verification_log.csv 필수 컬럼
- `tier`: `UT|IT|ST`
- `test_id`
- `scenario_id`
- `input_ts_ms`
- `output_ts_ms`
- `latency_ms` (비워도 채점기가 계산)
- `rule_type`: `LE|GE|BETWEEN|EQ`
- `rule_ms`: 예) `150`, `1000`, `1000:1300`
- `expected`
- `observed`
- `logic_verdict`: `PASS|FAIL`
- `comm_verdict`: `PASS|FAIL`
- `verdict`: 수동 입력값(선택), 최종 판정은 채점기 결과(`computed_verdict`)를 기준으로 한다.
- `owner`
- `run_date`: `YYYY-MM-DD`
- `evidence_log_path`
- `evidence_capture_path`
- `note`

## 6) 판정 규칙
### 6.1 주기(Period)
- `LE`: `latency_ms <= rule_ms`
- `GE`: `latency_ms >= rule_ms`
- `BETWEEN`: `min <= latency_ms <= max`
- `EQ`: `latency_ms == rule_ms`

### 6.2 로직(Logic)
- 로직 기대값(`expected`)과 실제 상태(`observed`)를 비교해 `logic_verdict`를 기록한다.

### 6.3 통신(Comm)
- 기대 경로의 파생 출력 반영 여부를 `comm_verdict`로 기록한다.
- 예: `Core -> Body -> UiRender`, `Core -> Cluster -> UiRender`

### 6.4 최종 판정
- `computed_verdict = PASS` 조건:
  - 주기 판정 PASS
  - `logic_verdict=PASS`
  - `comm_verdict=PASS`
  - `owner`, `run_date`, `evidence_*` 공란 아님
- 위 조건 중 하나라도 위반하면 FAIL.

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
- `capture_index.csv`에 파일 경로와 설명을 반드시 매핑한다.

## 9) 실행 명령 예시
```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner <OWNER>
```

## 10) 05/06/07 반영 규칙
- `computed_verdict` 기준으로 문서 상단 `Pass/Fail` 입력
- `evidence_log_path`, `evidence_capture_path`를 테스트 ID와 1:1로 연결
- 문서 값과 scored report 값이 다르면 문서를 FAIL로 처리한다.
