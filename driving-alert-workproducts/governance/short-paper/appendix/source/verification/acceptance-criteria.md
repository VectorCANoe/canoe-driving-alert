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

## Scenario verdict 요약

별첨에서는 scenario table을 좁게 유지하고, 긴 PASS 식은 표 아래에서 별도로 유지합니다.

| ID | Scenario | Requirement refs | PASS anchor |
| --- | --- | --- | --- |
| `S01` | Idle normal | `Req_001`, `Req_002` | idle zero state |
| `S02` | School-zone overspeed | `Req_009`, `Req_010`, `Req_037` | school-zone level/type |
| `S03` | Highway steering inactivity | `Req_011`, `Req_012`, `Req_038` | highway warning level/type |
| `S04` | Police emergency | `Req_017`, `Req_022`, `Req_035`, `Req_036` | police emergency render |
| `S05` | Ambulance emergency | `Req_018`, `Req_022`, `Req_035`, `Req_036` | ambulance emergency render |
| `S06` | Timeout clear | `Req_024` | timeout clear to zero |
| `S07` | Guided section left | `Req_013`, `Req_014`, `Req_039` | left guide render |
| `S08` | Guided section right | `Req_013`, `Req_014`, `Req_039` | right guide render |
| `S09` | ETA priority | `Req_030` | ETA takeover rule |
| `S10` | Source ID tie-break | `Req_031` | SourceID tie-break |
| `S11` | Transition moderation | `Req_034` | bounded arbitration churn |
| `S12` | Duplicate warning suppression | `Req_006`, `Req_026` | duplicate-popup guard |
| `S13` | Section-transition stability | `Req_015` | stable school-zone restore |
| `S14` | Domain boundary integrity | `Req_110`, `Req_111`, `Req_112` | healthy boundary and routing |

### Full PASS expressions

- `S01`: `selectedAlertLevel==0 AND warningTextCode==0`
- `S02`: `level==3 AND type==3 AND ambientColor==3 AND ambientPattern==5`
- `S03`: `level==2 AND type==4 AND ambientColor==4 AND ambientPattern==4`
- `S04`: `level==6 AND type==1 AND code==101 AND guard>0 AND ambientColor==6 AND ambientPattern==6`
- `S05`: `level==7 AND type==2 AND code==202 AND guard>0 AND ambientColor==7 AND ambientPattern==7`
- `S06`: `timeoutClear==1 AND level==0 AND code==0`
- `S07`: `level==2 AND type==5 AND ambientColor==5 AND ambientPattern==2 AND code==31`
- `S08`: `level==2 AND type==6 AND ambientColor==5 AND ambientPattern==3 AND code==32`
- `S09`: `V2X::eta==10 AND V2X::sourceId==99 AND level==6`
- `S10`: `V2X::sourceId==5 AND V2X::eta==10 AND level==6`
- `S11`: `level==6 AND type==1 AND snapshotDelta<=3`
- `S12`: `level==3 AND type==3 AND duplicatePopupGuard>0`
- `S13`: `level==3 AND type==3 AND snapshotDelta<=3`
- `S14`: `domainBoundaryStatus==1 AND routingPolicy==1 AND level==0`

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

### Scenario / baseline verdict anchor

- `Test::scenarioResult`: 현재 scenario 단위 PASS/FAIL
- `Test::baseScenarioId`: baseline aggregation target
- `Test::baseScenarioResult`: aggregate PASS/FAIL 결과
- `Test::baseFlowCoverageMask`: aggregate coverage summary
- `Test::baseTraceSnapshotId`: aggregate trace anchor
- `Test::baseTestHealth`: aggregate harness health

### Output / policy oracle anchor

- `Core::selectedAlertLevel`: 최종 선택 경고 레벨
- `Core::selectedAlertType`: 최종 선택 경고 타입
- `Cluster::warningTextCode`: reviewer-visible warning text 결과
- `Body::ambientColor`: ambient output color
- `Body::ambientPattern`: ambient output pattern
- `CoreState::duplicatePopupGuard`: duplicate-warning suppression state
- `CoreState::arbitrationSnapshotId`: arbitration transition counter
- `CoreState::domainBoundaryStatus`: boundary health state
- `CoreState::routingPolicy`: routing policy state
- `V2X::eta`: active emergency ETA
- `V2X::sourceId`: active emergency source identifier

## Output-style reference

- `emergency police`: police emergency warning, color `6`, pattern `6`
- `emergency ambulance`: ambulance emergency warning, color `7`, pattern `7`
- `school-zone`: school-zone warning, color `3`, pattern `5`
- `highway steering`: highway steering warning, color `4`, pattern `4`
- `guide left`: directional guidance left, color `5`, pattern `2`
- `guide right`: directional guidance right, color `5`, pattern `3`
- `generic normal`: nominal state, color `1`, pattern `1`
- `none`: no warning, color `0`, pattern `0`

## 개발 메모

이 문서는 현재 executable baseline 기준입니다.
향후 `01`, `05`, `06`, `07`을 기준으로 full architecture가 다시 정리되면 이 문서도 scenario-level acceptance baseline으로 함께 갱신해야 합니다.
