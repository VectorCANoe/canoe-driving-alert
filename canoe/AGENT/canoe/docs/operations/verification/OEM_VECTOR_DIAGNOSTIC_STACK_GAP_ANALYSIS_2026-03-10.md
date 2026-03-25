# OEM/Vector Diagnostic Stack Gap Analysis (2026-03-10)

## Scope

This note compares the current CANoe SIL diagnostic implementation against an OEM-style diagnostic stack and Vector's standard tester/gateway/simulated-ECU split.

Reference set used for this analysis:
- Vector local docs:
  - `C:\Program Files\Vector CANoe 19\Doc\AN-IND-1-001_CANoe_CANalyzer_as_Diagnostic_Tools.pdf`
  - `C:\Program Files\Vector CANoe 19\Doc\AN-IND-1-004_Diagnostics_via_Gateway_in_CANoe.pdf`
  - `C:\Program Files\Vector CANoe 19\Doc\AN-IND-1-026_DoIP_in_CANoe.pdf`
- AUTOSAR:
  - `AUTOSAR_SWS_DCM.pdf`
  - `AUTOSAR_CP_SWS_PDURouter.pdf`

## Current Baseline

- Tester / harness: `TEST_SCN`
- Result aggregator: `TEST_BAS`
- Backbone diagnostic services: `DCM`, `SGW`, `CGW`
- ECU-local diagnostic responders: `30` request/response paths
- Stable Dev2-facing evidence surface: `Diag::*`
- Native CANoe diagnostic testcase status:
  - runnable anchor assets: `2`
  - draft skeleton assets: `9`
  - diagnostic route skeleton exists but still uses `oracle-hook`

## Gap Table

| Area | Current Implementation | OEM / Vector Standard Direction | Gap | Action |
| --- | --- | --- | --- | --- |
| Tester role | `TEST_SCN` sends request frames and mirrors request/response into `Diag::*` | External tester or CANoe tester role separated from ECU responders | Low | Keep `TEST_SCN` as tester/harness. Do not turn it into a diagnostic ECU. |
| ECU-local diagnostic responders | `ESC/VCU/IVI/BCM/TMU/DATC/SCC` plus 13 basic leaf responders implemented | Each ECU owns its own diagnostic response logic | Medium | Expand leaf/basic responders only where active runtime or review surface requires it. |
| Gateway / transport edge | `SGW`, `CGW`, `DCM` exist, but routing policy is custom CAPL and partial | Gateway routes requests across bus boundaries; security edge and DoIP edge are explicit | Medium | Keep gateway/security split; add documented route ownership and response path policy. |
| Diagnostic description assets | No `CDD`, `ODX`, `PDX`, or minimal machine-readable diagnostic catalog found | OEM/Vector-grade workflows usually use a diagnostic description source | High | Introduce a minimal diagnostic description baseline before attempting full ODX/PDX adoption. |
| Session / security / NRC depth | Current responders are mostly lightweight positive-response/state paths | OEM stacks usually implement session control, security access, NRC behavior, timing behavior | High | Add minimum common behavior spec first; do not hand-code ECU-specific variants blindly. |
| Native CANoe diagnostic testcase asserts | Diagnostic skeleton exists, but concrete oracle/assert wiring is not finished | Vector-native tests should assert request, response, route, timeout, and wrong-route failure | High | Dev1 wires concrete message/sysvar/assert hooks into the diagnostic route testcase(s). |
| Dev2 pipeline aggregation key | `Diag::*` exists, but final pipeline key freeze was not yet formalized in docs/code | CI wants stable aggregation keys across reports and runs | Medium | Dev2 to freeze key schema using `Diag::*` contract as source. |
| Result aggregation topology | `TEST_BAS` aggregates summary frames on backbone seam | Validation overlay is acceptable, but should stay clearly non-production | Low | Keep as validation overlay; document separately from production ECU layers. |
| Addressing / physical transport | Active execution is custom CAN-stub request/response over current DBCs | OEM programs often separate logical addressing from transport realization (CAN / DoIP) | Medium | Keep current CAN-stub for SIL, but define future transport swap boundary explicitly. |

## What Is Already Good Enough

- Tester vs ECU-local responder split is present.
- Backbone/service nodes (`DCM`, `SGW`, `CGW`) are separated from most ECU-local response logic.
- `Diag::*` gives Dev2 a stable observer surface without frame parsing every ECU-specific response.
- The design is consistent with `tester + gateway + simulated ECU` roles described in Vector documentation.

## What Is Still Missing For An OEM-Grade Story

1. A machine-readable diagnostic description source.
2. Common session / security / NRC behavior rules.
3. Native diagnostic testcases with finished assertions.
4. A frozen Dev2 pipeline key and report schema.
5. Explicit separation between:
   - production ECU diagnostic behavior
   - validation overlay behavior

## CDD / ODX / Basic Diagnostic Description Adoption Review

### Option A. Basic Diagnostic Description (Recommended Next Step)

Use a simple repo-local catalog per ECU containing:
- ECU qualifier / canonical short name
- request frame name
- response frame name
- supported SID list
- supported DID list
- expected positive response code
- basic negative response / timeout rule
- source bus / target bus

Why this is the right next step:
- small enough to add without destabilizing CAPL
- enough for Dev2 pipeline keys and testcase oracle generation
- enough for docs team to describe diagnostic scope consistently
- does not lock the project into a CANoe-only format too early

### Option B. ODX / PDX (Good OEM Alignment, Higher Cost)

Pros:
- strongest OEM/external-tool alignment
- natural fit if the team later wants description-driven tester generation or DoIP growth

Cons:
- heavy for the current custom CAPL diagnostic baseline
- would require process/tooling changes, not just file addition
- overkill until testcase/assert and session model are stabilized

Recommended use:
- phase 2, limited to core diagnostic ECUs first (`ESC`, `VCU`, `BCM`, `IVI`, `CGW`, `SCC`)

### Option C. CDD-Only / CANoe-Centric Description

Pros:
- can fit CANoe-focused internal development
- lower immediate friction if team stays inside CANoe/Vector toolchain

Cons:
- weaker external interchange story than ODX/PDX
- easier to become tool-specific rather than architecture-specific

Recommended use:
- only if the program intentionally stays CANoe-internal and does not need stronger OEM exchange artifacts soon

## Recommendation

1. Keep the current CAPL-based tester/responder baseline.
2. Add a **Basic Diagnostic Description** first.
3. Use that description to finish native diagnostic testcase asserts.
4. Let Dev2 freeze the CI/report aggregation key on top of `Diag::*`.
5. Re-evaluate ODX/PDX only after the above is stable.

## Immediate Next Actions

### Dev1
- Finish concrete diagnostic native testcase oracle/assert hookup.
- Add common session/NRC baseline rules for active responder ECUs.

### Dev2
- Freeze pipeline aggregation keys using `Diag::*`.
- Bind native diagnostic testcase evidence into CLI/TUI/Jenkins packaging.

### Docs
- Reflect that diagnostics are currently:
  - CAPL-based
  - tester/responder separated
  - `11-bit active execution`
  - future description-driven expansion candidate
