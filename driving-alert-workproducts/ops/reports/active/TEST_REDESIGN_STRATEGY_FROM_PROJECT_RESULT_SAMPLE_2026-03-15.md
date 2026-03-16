# Test Redesign Strategy from Project Result Sample

> [!IMPORTANT]
> This strategy note is a working redesign baseline.
> It uses `Project Result_Sample` as a structural reference, not as a direct content template.
> The current project includes CANoe SIL, CAN + Ethernet, arbitration, fail-safe, and evidence requirements that are broader than the sample and may require deeper decomposition.

## 1. Reference basis

Reviewed sample set:

- `Project Result_Sample/01.md`
- `Project Result_Sample/03.md`
- `Project Result_Sample/0301.md`
- `Project Result_Sample/0302.md`
- `Project Result_Sample/0303.md`
- `Project Result_Sample/0304.md`
- `Project Result_Sample/05.md`
- `Project Result_Sample/06.md`
- `Project Result_Sample/07.md`

## 2. What the sample is actually doing

The sample keeps the document chain simple and intentional:

1. `01`
   - defines customer-visible or system-level requirements
2. `03`, `0301`, `0302`, `0303`, `0304`
   - define implementation structure, ECU responsibilities, message paths, and variable surfaces
3. `05`
   - confirms that each node or unit behaves correctly
4. `06`
   - confirms that requirement-linked functions work across connected units
5. `07`
   - confirms that the whole user-visible scenario behaves correctly

This is the key design intent of the sample.

## 3. Design intent extracted from sample `05`, `06`, `07`

### 3.1 `05` Unit Test intent

Sample `05` is not a scenario document.
It is a node-centered verification sheet.

Its primary question is:

`Does each controller or unit do its own job correctly?`

Observed characteristics:

- rows are organized around ECU or unit names
- each row describes one unit responsibility
- the result is a local PASS/FAIL
- simulator inputs and outputs appear together because the sample is small and educational

### 3.2 `06` Integration Test intent

Sample `06` is not an ECU inventory.
It is a requirement-linked functional confirmation sheet.

Its primary question is:

`When connected together, does the required function work correctly?`

Observed characteristics:

- each row points back to requirement IDs
- each row describes one integrated function or behavior
- expected result is written in reviewer-facing plain language
- PASS/FAIL is based on connected behavior, not on a single ECU

### 3.3 `07` System Test intent

Sample `07` is the customer-visible scene sheet.

Its primary question is:

`From the user perspective, does the whole sequence behave correctly?`

Observed characteristics:

- the table is sequence-oriented
- rows are described as scenes
- user-visible state transitions dominate the wording
- implementation detail is intentionally hidden

## 4. What should be copied and what should not

### 4.1 Copy

The following intent should be kept:

- `05` = unit or node responsibility verification
- `06` = requirement-linked integrated behavior verification
- `07` = scenario and user-visible system verification

### 4.2 Do not copy directly

The following sample simplifications should not be copied as-is:

- mixing simulator rows into the official top-level unit test purpose
- using overly broad integrated rows that hide owner, route, timeout, and fail-safe boundaries
- using system scenes without explicit oracle, evidence, and recovery criteria

The current project is deeper than the sample.
It needs the same three-layer structure, but with stronger contract and evidence discipline.

## 5. Refinement direction for the current project

The sample review does not justify a full rewrite of the current `05`, `06`, and `07` tables.

The current project documents already follow the right high-level split:

- `05` shows controller, input, and output surfaces
- `06` shows requirement-linked integrated behavior
- `07` shows customer-visible system scenarios

The correct action is selective refinement, not structural replacement.

## 5.1 `05_Unit_Test.md`

Keep the current structure and strengthen readability.

Refinement principle:

`05` should continue to show controller, input, and output surfaces, while making the core product path easier to read.

Recommended structure:

- keep:
  - `제어기`
  - `가상 노드 (Simulator) 입력`
  - `가상 노드 (Simulator) 출력`
- keep the official top table reviewer-facing
- order the controller rows so the core concept appears first and extensions follow later
- prefer ECU or service wording first, with runtime module names only as supporting detail

Recommended grouping:

- core warning path first
- V2 and fail-safe extensions next
- broader vehicle expansion rows after that

## 5.2 `06_Integration_Test.md`

Keep the current requirement-link structure and reduce only the overly broad rows.

Refinement principle:

`06` should remain a requirement-linked integration table, but some rows should be narrowed so the reviewer can judge one integrated intent at a time.

Recommended structure:

- keep requirement IDs in the official top table
- keep reviewer-facing plain-language test purpose and expected result
- split only rows that currently cover too many behaviors at once
- let contract detail remain visible through wording and lower-level references, without turning `06` into a pure contract document

Recommended first-pass path set:

- vehicle state input path
- navigation context path
- emergency alert reception path
- warning arbitration path
- ambient output path
- cluster or HMI output path
- fail-safe and degradation path
- Ethernet external transmit path

## 5.3 `07_System_Test.md`

Keep the current scene-driven structure.

Refinement principle:

`07` should continue to show the product story from a reviewer perspective.

Recommended structure:

- keep scene-style wording
- keep low-level implementation detail out of the row text
- preserve the current narrative order:
  - core concept first
  - advanced warning and fail-safe behavior next
  - broader vehicle-function expansion after that

Recommended scenario families:

- power-on and baseline driving
- zone warning entry, sustain, clear
- emergency warning entry, priority, clear
- arbitration and return-to-previous-warning behavior
- fail-safe entry and recovery
- long-path continuous driving scenarios

## 6. Recommended decomposition model

For the current project, the clean split should be:

1. `05` = controller/input/output surface verification
2. `06` = requirement-linked integrated behavior verification
3. `07` = customer scenario verification

This preserves the sample's design logic while fitting the current project scale and the existing official template.

## 7. Immediate rewrite sequence

1. keep the current official table shapes
2. refine `05` row order so core concept and later extensions are easier to read
3. split only the over-broad rows in `06`
4. keep `07` narrative structure unless reviewer clarity clearly requires minor reordering
5. align all three with:
   - `canoe/docs/verification/oracle.md`
   - `canoe/docs/verification/acceptance-criteria.md`
   - `canoe/docs/verification/evidence-policy.md`

## 8. Final design decision

The sample confirms that the project should not collapse `05`, `06`, and `07` into one mixed verification table.

The correct direction is:

- preserve the current `05`, `06`, `07` role split
- avoid full rewrites when the official reviewer-facing structure is already valid
- apply only targeted refinements where readability or scope separation is weak

That separation should now be preserved and strengthened with minimal edits.
