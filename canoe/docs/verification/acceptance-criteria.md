# Acceptance Criteria

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the current CANoe SIL scenario-level PASS/FAIL criteria for the active baseline.

The criteria below are aligned to the present `TEST_SCN` verdict logic and the current baseline aggregation flow through `TEST_BAS`.

## Scenario verdict table

| ID | Scenario | Requirement refs | PASS condition | Main intent |
| --- | --- | --- | --- | --- |
| `S01` | Idle normal | `Req_001`, `Req_002` | `selectedAlertLevel==0 AND warningTextCode==0` | no warning in normal drive state |
| `S02` | School-zone overspeed | `Req_009`, `Req_010`, `Req_037` | `level==3 AND type==3 AND ambientColor==3 AND ambientPattern==5` | school-zone warning path |
| `S03` | Highway steering inactivity | `Req_011`, `Req_012`, `Req_038` | `level==2 AND type==4 AND ambientColor==4 AND ambientPattern==4` | highway steering warning path |
| `S04` | Police emergency | `Req_017`, `Req_022`, `Req_035`, `Req_036` | `level==6 AND type==1 AND code==101 AND guard>0 AND ambientColor==6 AND ambientPattern==6` | police emergency warning |
| `S05` | Ambulance emergency | `Req_018`, `Req_022`, `Req_035`, `Req_036` | `level==7 AND type==2 AND code==202 AND guard>0 AND ambientColor==7 AND ambientPattern==7` | ambulance emergency warning |
| `S06` | Timeout clear | `Req_024` | `timeoutClear==1 AND level==0 AND code==0` | clear path after stale input timeout |
| `S07` | Guided section left | `Req_013`, `Req_014`, `Req_039` | `level==2 AND type==5 AND ambientColor==5 AND ambientPattern==2 AND code==31` | left guidance path |
| `S08` | Guided section right | `Req_013`, `Req_014`, `Req_039` | `level==2 AND type==6 AND ambientColor==5 AND ambientPattern==3 AND code==32` | right guidance path |
| `S09` | ETA priority | `Req_030` | `V2X::eta==10 AND V2X::sourceId==99 AND level==6` | ETA-based takeover rule |
| `S10` | Source ID tie-break | `Req_031` | `V2X::sourceId==5 AND V2X::eta==10 AND level==6` | source-ID tie-break rule |
| `S11` | Transition moderation | `Req_034` | `level==6 AND type==1 AND snapshotDelta<=3` | bounded arbitration churn during transition |
| `S12` | Duplicate warning suppression | `Req_006`, `Req_026` | `level==3 AND type==3 AND duplicatePopupGuard>0` | popup suppression guard behavior |
| `S13` | Section-transition stability | `Req_015` | `level==3 AND type==3 AND snapshotDelta<=3` | stable return into school-zone path |
| `S14` | Domain boundary integrity | `Req_110`, `Req_111`, `Req_112` | `domainBoundaryStatus==1 AND routingPolicy==1 AND level==0` | healthy boundary and routing state |

## Verdict flow

```text
Test::testScenario = N
  -> applyScenarioPreset(N)
  -> scheduleScenarioEvaluation(N)
  -> evaluateScenarioResult()
  -> Test::scenarioResult = PASS / FAIL
  -> TEST_BAS aggregates Test::scenarioResult
  -> Test::baseScenarioResult and Test::baseTestHealth are updated
```

## Current oracle signals

| Signal or variable | Role |
| --- | --- |
| `Test::scenarioResult` | current per-scenario PASS/FAIL |
| `Test::baseScenarioId` | baseline aggregation target |
| `Test::baseScenarioResult` | aggregate PASS/FAIL result |
| `Test::baseFlowCoverageMask` | aggregate coverage summary |
| `Test::baseTraceSnapshotId` | aggregate trace anchor |
| `Test::baseTestHealth` | aggregate harness health |
| `Core::selectedAlertLevel` | selected alert level |
| `Core::selectedAlertType` | selected alert type |
| `Cluster::warningTextCode` | reviewer-visible warning text result |
| `Body::ambientColor` | ambient output color |
| `Body::ambientPattern` | ambient output pattern |
| `CoreState::duplicatePopupGuard` | duplicate-warning suppression state |
| `CoreState::arbitrationSnapshotId` | arbitration transition counter |
| `CoreState::domainBoundaryStatus` | boundary health state |
| `CoreState::routingPolicy` | routing policy state |
| `V2X::eta` | active emergency ETA |
| `V2X::sourceId` | active emergency source identifier |

## Output-style reference

| Alert type | Meaning | Ambient color | Ambient pattern |
| --- | --- | --- | --- |
| emergency police | police emergency warning | `6` | `6` |
| emergency ambulance | ambulance emergency warning | `7` | `7` |
| school-zone | school-zone warning | `3` | `5` |
| highway steering | highway steering warning | `4` | `4` |
| guide left | directional guidance left | `5` | `2` |
| guide right | directional guidance right | `5` | `3` |
| generic normal | nominal state | `1` | `1` |
| none | no warning | `0` | `0` |

## Development note

These criteria define the current executable baseline only.

If the project later redesigns the full customer test architecture from `01`, `05`, `06`, and `07`, this document should be updated as the official scenario-level acceptance baseline for that new design.
