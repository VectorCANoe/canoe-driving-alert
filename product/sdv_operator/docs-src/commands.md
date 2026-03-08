# ?? ??

? ??? `SDV Operator`? ?? ?? ??? ?????.

## ?? ??? ?

?? ???? ?? ? ?? ???? ???.

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
python scripts/run.py doctor
```

## ?? 4?

### Gate all

```powershell
python scripts/run.py gate all
```

?? ???:
- ???? ?? ?
- ??/DBC/CAPL ??? ?? ??? ?

### Scenario run

```powershell
python scripts/run.py scenario run --id 4
python scripts/run.py scenario run --id 4 --var testScenario
```

?? ???:
- CANoe measurement? ?? ?? ?
- ?? ????? Test sysvar ??? ??? ?

### Verify quick

```powershell
python scripts/run.py verify quick
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

?? ???:
- ???? ?? ??
- ?? ??, ?? ??, ?? ??? ? ?? ?? ?? ?

### Doctor

```powershell
python scripts/run.py doctor
python scripts/run.py doctor --ensure-running
```

?? ???:
- COM attach ??? ??? ?
- measurement / sysvar / runtime ??? ?? ??? ?

## ?? ??

### TUI

```powershell
python scripts/run.py
python scripts/run.py tui
```

??:
- ?? ??? ?? ???
- ??/??/COM ??? ? ???? ??

### Plain shell

```powershell
python scripts/run.py shell
```

??:
- TUI ?? ????? ??? ?
- ??? ???? ?? ??? ?

### Guided flow

```powershell
python scripts/run.py start guided
python scripts/run.py start demo --id 4
python scripts/run.py start precheck --owner DEV2
```

??:
- ?? ??? ??? ??? ??
- ??? fallback? ??? ??

<details>
<summary>?? ?? ??</summary>

### Verify pipeline

#### Prepare

```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
```

#### Batch

```powershell
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase post
python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase full
```

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
python scripts/run.py package build-exe --mode onefolder --clean
python scripts/run.py package build-exe --mode onefile --clean
python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe
```

</details>

## ?? ??

- ?? ??? canonical ??? ?????.
- hidden alias? ??? ??????.
- ?? ???? ???? ??? ????.
- ??? ??? `scripts/` ??? ??? ? ???? ?????.
