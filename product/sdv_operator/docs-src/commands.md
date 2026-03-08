# 명령 참고

이 문서는 `SDV Operator`의 공개 명령 표면만 설명합니다.

## 핵심 4개

### Gate all

```powershell
python scripts/run.py gate all
```

언제 쓰는가:
- 시나리오 실행 전
- 문서/DBC/CAPL 정합을 먼저 확인할 때

### Scenario run

```powershell
python scripts/run.py scenario run --id 4
python scripts/run.py scenario run --id 4 --var testScenario
```

언제 쓰는가:
- CANoe measurement가 실행 중일 때
- 특정 시나리오를 Test sysvar 경로로 주입할 때

### Verify quick

```powershell
python scripts/run.py verify quick
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

언제 쓰는가:
- 시나리오 실행 직후
- 준비 상태, 증빙 상태, 기본 판정을 한 번에 보고 싶을 때

### Doctor

```powershell
python scripts/run.py doctor
python scripts/run.py doctor --ensure-running
```

언제 쓰는가:
- COM attach 상태가 의심될 때
- measurement / sysvar / runtime 상태를 먼저 확인할 때

## 실행 모드

### TUI

```powershell
python scripts/run.py
python scripts/run.py tui
```

용도:
- 일일 운영용 기본 진입점
- 결과/로그/COM 상태를 한 화면에서 검토

### Plain shell

```powershell
python scripts/run.py shell
```

용도:
- TUI 없이 보수적으로 사용할 때
- 터미널 중심으로 반복 실행할 때

### Guided flow

```powershell
python scripts/run.py start guided
python scripts/run.py start demo --id 4
python scripts/run.py start precheck --owner DEV2
```

용도:
- 숫자 선택형 흐름이 필요한 경우
- 보수적 fallback이 필요한 경우

## 검증 파이프라인 명령

### Prepare

```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
```

### Batch

```powershell
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase post
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase full
```

### Smoke

```powershell
python scripts/run.py verify smoke --owner DEV1
```

### Fill and score

```powershell
python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1
```

### Insight

```powershell
python scripts/run.py verify insight --run-id 20260306_1930
python scripts/run.py verify insight --run-id 20260306_1930 --baseline-run-id 20260305_1800
```

### Bind documentation

```powershell
python scripts/run.py verify bind-doc --run-id 20260306_1930
python scripts/run.py verify fill-template --run-id 20260306_1930 --owner-fallback DEV1
```

### Status and finalize

```powershell
python scripts/run.py verify status --run-id 20260306_1930
python scripts/run.py verify finalize --run-id 20260306_1930 --owner DEV1
```

## Gate 명령

```powershell
python scripts/run.py gate doc-sync
python scripts/run.py gate cfg-hygiene
python scripts/run.py gate capl-sync
python scripts/run.py gate multibus-dbc
python scripts/run.py gate cli-readiness
```

## CAPL / CANoe COM

### SysVar access

```powershell
python scripts/run.py capl sysvar-get --namespace Core --var failSafeMode
python scripts/run.py capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int
```

### Measurement control

```powershell
python scripts/run.py canoe measure-status
python scripts/run.py canoe measure-start
python scripts/run.py canoe measure-stop
python scripts/run.py canoe measure-reset
```

### CAPL function call

```powershell
python scripts/run.py canoe capl-call --function-name MyFunction --args 1 2 --arg-type int
```

## Packaging

```powershell
python scripts/run.py package build-exe --mode onefolder --clean
python scripts/run.py package build-exe --mode onefile --clean
python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe
```

## 운영 원칙

- 공개 표면은 canonical 명령만 사용합니다.
- hidden alias는 호환성 유지용입니다.
- 생성 산출물은 소스처럼 다루지 않습니다.
- 자세한 예시는 `scripts/` 루트가 아니라 이 문서에서 유지합니다.
