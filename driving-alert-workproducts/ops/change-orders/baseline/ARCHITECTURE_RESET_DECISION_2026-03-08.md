# Architecture Reset Decision (2026-03-08)

## Why This Reset Was Opened

- The project is still early enough that structural change cost is lower than late-stage migration cost.
- Current runtime logic is stronger than the legacy demo baseline, but the public/runtime surface is still too implementation-driven.
- The team decided to stop defending the current naming baseline and instead rebuild the logical ECU model toward a production-style vehicle project surface.

## Decision

1. Keep the existing handoff baseline as an archive asset.
2. Reopen ECU naming governance and move `00e` from fixed SoT to active refactor mode.
3. Redesign the project around:
   - logical ECU surface names
   - runtime implementation module mapping
   - validation harness separation
4. Do not rename GUI/runtime nodes before the logical ECU grouping is approved.

## Immediate Working Order

1. Reclassify active nodes into logical ECU groups.
2. Approve surface naming rules for GUI, docs, and presentation.
3. Decide which runtime splits remain for ownership/debuggability.
4. Rebuild `0301/0302/0303/0304/04` on the new baseline.
5. Reconnect `05/06/07` evidence to the reset baseline.

## Archive Asset

- Previous handoff baseline:
  - `driving-alert-workproducts/ops/archive/handoff/TMP_HANDOFF_pre_architecture_reset_2026-03-08.md`
