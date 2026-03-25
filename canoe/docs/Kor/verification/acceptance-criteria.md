# Acceptance Criteria

원문:
- [../../verification/acceptance-criteria.md](../../verification/acceptance-criteria.md)

동기화 기준:
- `5d83ee7f`
- scenario ID, PASS condition 식, signal 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 active baseline에 대한 current CANoe SIL scenario-level PASS/FAIL criteria를 정의합니다.
> `TEST_SCN` verdict logic과 `TEST_BAS` aggregation flow를 읽을 때 기준이 되는 핵심 문서입니다.

## 목적

이 문서는 active baseline의 scenario-level PASS/FAIL 기준을 정의합니다.

판정 기준은 두 축에 맞춰 읽습니다.

- 현재 `TEST_SCN` verdict logic
- 현재 `TEST_BAS` baseline aggregation flow

## Scenario verdict 표

| ID | Scenario | Requirement refs | PASS condition | 주요 의도 |
| --- | --- | --- | --- | --- |
| `S01` | Idle normal | `Req_001`, `Req_002` | `selectedAlertLevel==0 AND warningTextCode==0` | normal drive state에서 경고가 없어야 합니다. |
| `S02` | School-zone overspeed | `Req_009`, `Req_010`, `Req_037` | `level==3 AND type==3 AND ambientColor==3 AND ambientPattern==5` | school-zone warning path가 정확히 올라와야 합니다. |
| `S03` | Highway steering inactivity | `Req_011`, `Req_012`, `Req_038` | `level==2 AND type==4 AND ambientColor==4 AND ambientPattern==4` | highway steering warning path가 정확히 올라와야 합니다. |
| `S04` | Police emergency | `Req_017`, `Req_022`, `Req_035`, `Req_036` | `level==6 AND type==1 AND code==101 AND guard>0 AND ambientColor==6 AND ambientPattern==6` | police emergency warning이 정확히 반영되어야 합니다. |
| `S05` | Ambulance emergency | `Req_018`, `Req_022`, `Req_035`, `Req_036` | `level==7 AND type==2 AND code==202 AND guard>0 AND ambientColor==7 AND ambientPattern==7` | ambulance emergency warning이 정확히 반영되어야 합니다. |
| `S06` | Timeout clear | `Req_024` | `timeoutClear==1 AND level==0 AND code==0` | stale input timeout 이후 clear path가 정상 동작해야 합니다. |
| `S07` | Guided section left | `Req_013`, `Req_014`, `Req_039` | `level==2 AND type==5 AND ambientColor==5 AND ambientPattern==2 AND code==31` | left guidance path가 정확히 반영되어야 합니다. |
| `S08` | Guided section right | `Req_013`, `Req_014`, `Req_039` | `level==2 AND type==6 AND ambientColor==5 AND ambientPattern==3 AND code==32` | right guidance path가 정확히 반영되어야 합니다. |
| `S09` | ETA priority | `Req_030` | `V2X::eta==10 AND V2X::sourceId==99 AND level==6` | ETA-based takeover rule이 유지되어야 합니다. |
| `S10` | Source ID tie-break | `Req_031` | `V2X::sourceId==5 AND V2X::eta==10 AND level==6` | SourceID tie-break rule이 유지되어야 합니다. |
| `S11` | Transition moderation | `Req_034` | `level==6 AND type==1 AND snapshotDelta<=3` | transition 중 arbitration churn이 제한되어야 합니다. |
| `S12` | Duplicate warning suppression | `Req_006`, `Req_026` | `level==3 AND type==3 AND duplicatePopupGuard>0` | duplicate warning suppression guard가 유지되어야 합니다. |
| `S13` | Section-transition stability | `Req_015` | `level==3 AND type==3 AND snapshotDelta<=3` | school-zone path로 복귀할 때 안정성이 유지되어야 합니다. |
| `S14` | Domain boundary integrity | `Req_110`, `Req_111`, `Req_112` | `domainBoundaryStatus==1 AND routingPolicy==1 AND level==0` | boundary health와 routing policy가 정상이어야 합니다. |

## Verdict 흐름

```text
Test::testScenario = N
  -> applyScenarioPreset(N)
  -> scheduleScenarioEvaluation(N)
  -> evaluateScenarioResult()
  -> Test::scenarioResult = PASS / FAIL
  -> TEST_BAS aggregates Test::scenarioResult
  -> Test::baseScenarioResult and Test::baseTestHealth are updated
```

즉 scenario-level verdict와 baseline aggregate verdict를 구분해서 읽어야 합니다.

## 현재 oracle signal

| Signal 또는 변수 | 역할 |
| --- | --- |
| `Test::scenarioResult` | 현재 scenario 단위 PASS/FAIL |
| `Test::baseScenarioId` | baseline aggregation target |
| `Test::baseScenarioResult` | aggregate PASS/FAIL 결과 |
| `Test::baseFlowCoverageMask` | aggregate coverage summary |
| `Test::baseTraceSnapshotId` | aggregate trace anchor |
| `Test::baseTestHealth` | aggregate harness health |
| `Core::selectedAlertLevel` | 최종 선택 경고 레벨 |
| `Core::selectedAlertType` | 최종 선택 경고 타입 |
| `Cluster::warningTextCode` | reviewer-visible warning text 결과 |
| `Body::ambientColor` | ambient output color |
| `Body::ambientPattern` | ambient output pattern |
| `CoreState::duplicatePopupGuard` | duplicate-warning suppression state |
| `CoreState::arbitrationSnapshotId` | arbitration transition counter |
| `CoreState::domainBoundaryStatus` | boundary health state |
| `CoreState::routingPolicy` | routing policy state |
| `V2X::eta` | active emergency ETA |
| `V2X::sourceId` | active emergency source identifier |

## Output-style reference

| Alert type | 의미 | Ambient color | Ambient pattern |
| --- | --- | --- | --- |
| emergency police | police emergency warning | `6` | `6` |
| emergency ambulance | ambulance emergency warning | `7` | `7` |
| school-zone | school-zone warning | `3` | `5` |
| highway steering | highway steering warning | `4` | `4` |
| guide left | directional guidance left | `5` | `2` |
| guide right | directional guidance right | `5` | `3` |
| generic normal | nominal state | `1` | `1` |
| none | no warning | `0` | `0` |

## 개발 메모

이 문서는 현재 executable baseline 기준입니다.
향후 `01`, `05`, `06`, `07`을 기준으로 full architecture가 다시 정리되면 이 문서도 scenario-level acceptance baseline으로 함께 갱신해야 합니다.
