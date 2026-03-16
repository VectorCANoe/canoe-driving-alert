# Oracle

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the oracle model used to decide whether the CANoe SIL baseline is correct.

The oracle is not a single signal check.
It is the combined decision across contract, behavior, harness, and evidence layers.

## Oracle model

| Oracle layer | Main source | PASS expectation |
| --- | --- | --- |
| Contract oracle | communication matrix, owner/route contract, multibus policy, interface contracts | runtime follows the documented owner, bus, route, timeout, and observation seam |
| ECU behavior oracle | ECU classification, panel/sysvar contract, diagnostic-sysvar contract | each active ECU or surface behaves within its documented responsibility boundary |
| Scenario oracle | acceptance criteria | the scenario result matches the expected alert, clear, fail-safe, and routing behavior |
| Harness oracle | `TEST_SCN`, `TEST_BAS`, native Test Unit verdicts | the native harness verdict is consistent with the expected scenario result |
| Evidence oracle | evidence policy and captured artifacts | the evidence package is complete enough for review and traceability |

## Oracle sources

- `../architecture/ecu-classification.md`
- `../contracts/communication-matrix.md`
- `../contracts/owner-route.md`
- `../contracts/multibus-policy.md`
- `../contracts/panel-sysvar-contract.md`
- `../contracts/diagnostic-sysvar-contract.md`
- `acceptance-criteria.md`
- `execution-guide.md`
- `evidence-policy.md`

## Current decision rule

A verification item is a true PASS only when all of the following are true:

1. the runtime follows the documented contract path
2. the ECU or surface behavior stays within the documented ownership boundary
3. the scenario result matches the expected acceptance criteria
4. the harness verdict is consistent with that expected result
5. the required evidence is present and reviewable

## Harness-based oracle interpretation

The current baseline uses these decision seams:

| Harness seam | Interpretation |
| --- | --- |
| `Test::scenarioResult` | scenario-level PASS/FAIL decision from `TEST_SCN` |
| `Test::baseScenarioResult` | aggregate baseline verdict from `TEST_BAS` |
| `Test::baseFlowCoverageMask` | coverage summary for review completeness |
| `Test::baseTraceSnapshotId` | trace anchor for evidence navigation |
| `Test::baseTestHealth` | health summary for harness trustworthiness |

The harness verdict alone is not sufficient.

For example, a run is not a true PASS when:

- the verdict passes but the contract path is undocumented
- the verdict passes but required evidence is missing
- the visible output looks correct once, but repeatability or timeout rules fail

## Current oracle boundary

The active oracle is intentionally scoped to:

- CANoe SIL
- CAN + Ethernet runtime seams
- current documented product and validation surfaces

It does not yet claim that every future ECU and every future customer test case is fully covered.

## Development note

The oracle model in this document should remain stable even if the project later redesigns the full test architecture from the customer workproduct chain.

What may change later:

- detailed scenario coverage
- ECU-level verdict decomposition
- diagnostic depth
- native asset set and evidence packaging shape

What should not change:

- layered oracle structure
- separation between product behavior and validation behavior
- requirement that PASS means contract, behavior, harness, and evidence all agree
