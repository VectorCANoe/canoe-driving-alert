# ECU Reset Document Propagation Rules (2026-03-09)

## Purpose

- Define exactly how the approved surface ECU inventory must propagate through the SoT chain.
- Prevent the team from renaming GUI/runtime first and repairing docs later.
- Keep `surface ECU`, `runtime module`, and `validation harness` separated by document layer.

## Base Principle

- Surface first, runtime second, evidence last.
- Upper docs must show reviewer-facing logical ECUs.
- Lower docs may preserve runtime module names where ownership/debug value is real.

## Propagation Order

1. `00e_ECU_Naming_Standard.md`
2. `0301_SysFuncAnalysis.md`
3. `0302_NWflowDef.md`
4. `0303_Communication_Specification.md`
5. `0304_System_Variables.md`
6. `04_SW_Implementation.md`
7. `05/06/07` evidence remap
8. GUI surface rename and grouping

## Document-by-Document Rule

### 1. 00e_ECU_Naming_Standard.md

What to change:
- Add a formal three-layer naming policy:
  - `Surface ECU Name`
  - `Runtime Implementation Module`
  - `Validation Harness`
- Keep current canonical runtime names as transition baseline.
- Add an explicit surface inventory table based on the approved reset sheet.

What not to do:
- Do not silently replace every runtime node with a surface name.
- Do not delete the current runtime canonical matrix before cross-reference is preserved.

### 2. 0301_SysFuncAnalysis.md

What to show:
- Function ownership should primarily reference the approved surface ECU.
- Runtime module names may appear in `implementation note` or `internal module` columns only.

Recommended rule:
- `Owner ECU` = surface ECU
- `Internal Runtime Module` = current CAPL node name (optional supporting column)

### 3. 0302_NWflowDef.md

What to change:
- The reviewer-facing understanding of the network must reflect the surface ECU model.
- The current `Tx/Rx node columns` should be reviewed carefully.

Recommended rule:
- Upper/top network interpretation = surface ECU ownership
- Detailed implementation/cross-bus relay note = runtime module name

Practical interpretation:
- `BODY_GW -> AMBIENT_CTRL` should not dominate the reviewer-facing story.
- The story should read as `BCM owns body/ambient output path`, with `BODY_GW` and `AMBIENT_CTRL` retained as internal runtime modules in detailed notes.

### 4. 0303_Communication_Specification.md

What to change:
- `Owner` and `Data use` must use surface ECU as primary language.
- Runtime sender/receiver names should be preserved in implementation notes, not as the first public owner label.

Recommended rule:
- Primary owner = surface ECU
- Runtime sender/receiver = sub-note or lower tracking table

Example direction:
- `ADAS_WARN_CTRL -> WARN_ARB_MGR` becomes `ADAS_ECU internal warning path`
- `EMS_POLICE_TX / EMS_AMB_TX / EMS_ALERT_RX` become `V2X_ECU internal emergency path`

### 5. 0304_System_Variables.md

What to keep:
- Namespace should remain domain/function oriented where already stable.
- Do not rename variables just to mimic the new surface ECU names.

What to add:
- Lower mapping table should show:
  - `Var -> Runtime Module -> Surface ECU`
- Validation variables stay explicitly under `Test` / `Validation Harness`

### 6. 04_SW_Implementation.md

What to show:
- This is the correct place to expose runtime detail.
- Preserve CAPL path, implementation module names, ownership split, merge candidates.

Recommended structure:
- `Surface ECU`
- `Runtime Module`
- `CAPL Path`
- `Reason to Keep Split / Merge Candidate`

This is the document where the matrix and second sheet should become implementation truth.

### 7. 05 / 06 / 07 Test Docs

What to do later:
- Remap evidence from runtime-centric wording to reset baseline.
- Test case title may use surface ECU language.
- Evidence detail may still mention runtime module names where debugging requires it.

Rule:
- `test title / objective / pass condition` = surface ECU language first
- `log / trace / implementation evidence` = runtime module name allowed

## GUI Rule

- GUI rename and node grouping must be last.
- Before GUI change:
  - classification matrix approved
  - target surface inventory approved
  - `00e/0301/0302/0303/0304/04` baseline updated
- GUI should show surface ECU names.
- Internal runtime nodes may remain in code and lower implementation docs.

## Review Checklist

Before approving each document, check the following:

1. Is the reviewer-facing owner a surface ECU, not an implementation module?
2. Is the runtime module still traceable somewhere below?
3. Is Validation Harness still separated from production architecture?
4. Did we avoid renaming variables/messages only for cosmetic consistency?
5. Did we preserve `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`?

## Short Decision Summary

- `00e` defines names and layers.
- `0301/0302/0303` speak in surface ECU language first.
- `0304` preserves variable stability and adds surface mapping below.
- `04` preserves runtime reality.
- `05/06/07` reconnect evidence after the new baseline is frozen.
- GUI comes last.
