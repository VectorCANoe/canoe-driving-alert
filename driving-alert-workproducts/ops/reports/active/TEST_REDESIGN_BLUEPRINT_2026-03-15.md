# Test Redesign Blueprint

> [!IMPORTANT]
> This blueprint is a working redesign baseline.
> It reflects the current customer document chain and the current CANoe SIL scope.
> Some test structure, verdict decomposition, and native assets are still under development and may change.

## 1. Purpose

This document defines how the project test set should be rebuilt from the customer workproduct baseline.

The redesign source of truth is:

- `01_Requirements.md`
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`

The redesign does not start from current native test assets.
Native assets are execution means, not the top-level test architecture.

## 2. Current issues

### 2.1 Unit test (`05`)

- product ECU behavior and validation harness/input generator rows are mixed in one official table
- several rows describe data generation rather than the unit under test
- `Ready` and `Planned` are being used as progress markers, but many rows still need explicit ECU-level PASS/FAIL intent

### 2.2 Integration test (`06`)

- several rows bundle too many requirements and too many interfaces into one integration purpose
- the table is closer to a feature summary than an interface-contract verification set
- route, owner, timeout, and channel boundary checks are not separated clearly enough

### 2.3 System test (`07`)

- the scenario list is usable, but the PASS basis is not yet explicitly tied to the official oracle and acceptance model
- customer-visible scenarios and future pre-activation scenarios are currently listed together without a stronger boundary

## 3. Target redesign model

### 3.1 Unit test = ECU function PASS/FAIL

`05` should answer one question:

`Did this ECU or runtime owner perform its own documented responsibility correctly?`

Unit tests should be centered on:

- owner ECU or runtime owner
- local input condition
- local decision or output
- local timeout or guard rule
- ECU-level PASS/FAIL verdict

Validation harness stimulators are not the unit under test.
They may remain as support references, but the official top table should be driven by product-side ECU verification intent.

### 3.2 Integration test = contract path PASS/FAIL

`06` should answer one question:

`Did the documented path across ECU or service boundaries work correctly?`

Integration tests should be centered on:

- source owner
- destination owner
- bus or transport boundary
- timeout, update period, or fail-safe rule
- end-to-end contract PASS/FAIL verdict

Recommended primary split:

- vehicle state input path
- navigation context path
- emergency alert path
- arbitration path
- ambient output path
- cluster or HMI output path
- fail-safe and degradation path
- Ethernet transmit path

### 3.3 System test = customer scenario PASS/FAIL

`07` should answer one question:

`Did the full customer-visible scenario behave correctly from start to finish?`

System tests should be centered on:

- scenario precondition
- trigger
- final warning behavior
- recovery behavior
- user-visible PASS/FAIL verdict

`07` should remain scenario-facing.
It should not absorb low-level transport or harness detail unless needed for reviewer understanding.

## 4. Oracle linkage

The redesigned test set should use four aligned verdict layers:

1. requirement intent
2. ECU behavior verdict
3. interface-contract verdict
4. scenario verdict

Evidence is valid only when these layers do not contradict each other.

## 5. Rewrite rules for official tables

- keep the current top-level table headers as they are
- enrich cell content instead of changing the template shape
- do not explain behavior only through Flow IDs, Comm IDs, or internal chain language
- keep official rows reviewer-facing and understandable on their own
- use `Ready` and `Planned` only as temporary progress markers before executable assets are fixed
- once executable assets exist, replace temporary status with evidence-backed `PASS` or `FAIL`

## 6. Immediate rewrite sequence

1. derive requirement families from `01`
2. rebuild `05` around ECU-level responsibilities
3. rebuild `06` around owner/bus/timeout/route contracts
4. rebuild `07` around customer scenarios and recovery behavior
5. map every row to oracle and evidence fields

## 7. Requirement families for the rebuild

Recommended first-pass grouping:

- baseline vehicle state and activation
- zone warning behavior
- emergency warning behavior
- arbitration and priority
- HMI and output policy
- fail-safe and timeout
- extension domains kept as explicit planned scope

## 8. Immediate design decision

The rebuild should separate two verdict axes from the start:

- `ECU PASS/FAIL`
- `Scenario PASS/FAIL`

Without that split, the project will keep mixing local logic correctness with whole-system behavior and the test set will remain hard to scale.
