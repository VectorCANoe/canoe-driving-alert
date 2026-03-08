# Test Automation Reference Baseline (2026-03-09)

## Purpose

Freeze the Dev2 reference baseline for CANoe-native test authoring support, external orchestration,
and Jenkins/CI bridging.

This document does not replace native CANoe or vTESTstudio workflows.
It defines how this project should split responsibilities and what external references Dev2 should follow.

## Reference Summary

### Vector (official)

1. CANoe / vTESTstudio native automated testing remains the official authoring path.
2. Python automation is valid for external orchestration and repeated execution.
3. CI ingestion should prefer standard machine-readable formats rather than proprietary report parsing.

### Jenkins (official)

1. `junit` is the canonical test result ingestion surface.
2. raw artifacts should be archived separately with `archiveArtifacts`.

## Recommended Project Split

### Dev1

Owns native CANoe test assets and GUI execution evidence.

- `*.can`
- `*.vtestunit.yaml`
- `*.vtesttree.yaml`
- native `.vtestreport`
- GUI screenshots

### Dev2

Owns orchestration, normalization, and CI bridge.

- `gate all`
- `scenario run`
- `verify batch`
- `JSON + MD + JUnit XML`
- Jenkins archive/publish contract

## Why This Is the Right Split

1. It preserves the native CANoe toolchain.
2. It avoids overlap between Dev1 native tests and Dev2 automation.
3. It gives Jenkins a standard ingestion format (`JUnit XML`).
4. It keeps native `.vtestreport` as the original evidence source.

## Explicit Do / Do Not

### Do

- keep native CANoe Test Unit authoring in Dev1 scope
- use Dev2 CLI/TUI for repeated execution support and evidence normalization
- publish `dev2_batch_report.junit.xml` into Jenkins
- archive native `.vtestreport`, screenshots, JSON, and Markdown together

### Do Not

- rebuild native CANoe Test Units inside Dev2 tooling
- parse `.vtestreport` as the first CI integration step
- build a separate control GUI that competes with CANoe Panel

## Canonical Dev2 Flow

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify batch --run-id 20260309_0900 --owner DEV2 --phase pre --report-formats json,md,junit
```

## Jenkins Ingress Contract

### Publish

- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`

### Archive

- `canoe/tmp/reports/verification/*.json`
- `canoe/tmp/reports/verification/*.md`
- `canoe/tmp/reports/verification/*.xml`
- `canoe/**/*.vtestreport`
- screenshot path

## Near-Term Dev2 Priorities

1. make `verify batch` robust across `scenarioCommand` / `testScenario` runtime differences
2. keep `JSON + MD + JUnit XML` stable
3. avoid touching native CANoe test authoring scope
4. support Jenkins pipeline samples and packaging only at the bridge layer

## External References

- Vector automated testing:
  - https://www.vector.com/kr/ko/know-how/automated-testing/
- Vector Python interface for test automation:
  - https://www.vector.com/int/en/know-how/test-automation-using-the-python-interface/
- Jenkins JUnit step:
  - https://www.jenkins.io/doc/pipeline/steps/junit/
- Jenkins archiveArtifacts step:
  - https://www.jenkins.io/doc/pipeline/steps/core/#archiveartifacts-archive-the-artifacts
