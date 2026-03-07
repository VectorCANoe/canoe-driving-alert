# Verify Execution Runbook (Dev2)

This runbook reflects the Dev2 scope in `TEAM_SYNC_BOARD.md`:

- gate + test batch CLI
- UT/IT/ST result collection in `JSON + MD` standard (`CSV` optional)
- offline/portable execution path

## 1) Fast Start (Recommended)

### A. Pre phase (before scenario run)

```powershell
python scripts/run.py start precheck --run-id <RUN_ID> --owner <OWNER>
```

What it does:

1. gates (`doc-sync`, `cfg-hygiene`, `capl-sync`, `multibus-dbc`, `cli-readiness`)
2. `verify prepare`
3. `verify smoke`
4. `verify status`

### B. Manual CANoe execution

1. Run UT/IT/ST scenarios in CANoe.
2. Save Write Window logs to:
   - `canoe/logging/evidence/UT/<RUN_ID>/raw_write_window.txt`
   - `canoe/logging/evidence/IT/<RUN_ID>/raw_write_window.txt`
   - `canoe/logging/evidence/ST/<RUN_ID>/raw_write_window.txt`
3. Ensure logs include `[EVIDENCE_OUT]` markers.

### C. Post phase (after evidence logs are ready)

```powershell
python scripts/run.py verify batch --run-id <RUN_ID> --owner <OWNER> --phase post
```

What it does:

1. `verify finalize` (UT/IT/ST fill-score + insight + doc-fill)
2. `verify status`

## 2) Fixed Report Outputs (Dev2 Standard)

Recommended policy (final):

- Canonical machine format: `JSON`
- Human review format: `MD`
- Optional interchange format: `CSV` (only when needed for Excel/import)

Primary outputs:

- `canoe/tmp/reports/verification/dev2_batch_report.json` (canonical)
- `canoe/tmp/reports/verification/dev2_batch_report.md` (human review)

Optional output:

- `canoe/tmp/reports/verification/dev2_batch_report.csv`

Format option examples:

```powershell
python scripts/run.py verify batch --run-id <RUN_ID> --owner <OWNER> --phase pre --report-formats json,md
python scripts/run.py verify batch --run-id <RUN_ID> --owner <OWNER> --phase pre --report-formats json,md,csv
```

Batch CSV schema (optional export) is fixed:

- `row_type` (`step` or `artifact`)
- `run_id`, `phase`, `owner`, `run_date`, `status`
- `step_name`, `step_rc`
- `artifact_path`, `artifact_exists`, `artifact_size_bytes`, `artifact_last_modified`

## 3) One-Command Variants

### Doctor (before first run)

```powershell
python scripts/run.py doctor
python scripts/run.py doctor --ensure-running
```

### CAPL-linked sysvar check (no panel)

```powershell
python scripts/run.py capl sysvar-get --namespace Core --var failSafeMode
python scripts/run.py capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int
```

### CANoe control plane (measurement)

```powershell
python scripts/run.py canoe measure-status
python scripts/run.py canoe measure-start
python scripts/run.py canoe measure-stop
python scripts/run.py canoe measure-reset
```

### Full batch

Only use when raw evidence logs are already prepared.

```powershell
python scripts/run.py verify batch --run-id <RUN_ID> --owner <OWNER> --phase full
```

### Shell mode (slash commands)

```powershell
python scripts/run.py shell
```

Then:

1. `/verify batch <RUN_ID> <OWNER> pre`
2. `/verify batch <RUN_ID> <OWNER> post`
3. `/exit`

### Evidence shortcuts

```powershell
python scripts/run.py evidence status --run-id <RUN_ID>
python scripts/run.py evidence insight --run-id <RUN_ID>
```

## 4) Offline/Portable Execution

Build portable ZIP:

```powershell
python scripts/run.py release portable --mode onefolder --clean --rebuild-exe
```

Use portable shell:

```powershell
.\dist\portable\sdv_portable\run-sdv.bat shell
```

## 5) Troubleshooting

1. If scenario command ACK fails: align terminal/CANoe privilege level.
2. If finalize fails: check `[EVIDENCE_OUT]` marker exists in all UT/IT/ST raw logs.
3. If multibus gate fails: sync `CAN_v2_topology_wip.cfg` and domain DBC ownership first.
