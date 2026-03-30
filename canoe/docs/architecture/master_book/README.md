# Vehicle ECU Architecture and Interaction Reference

Subtitle: Official publication surface for the CANoe SIL baseline.

This folder contains the reviewer-facing CANoe architecture book for the active SIL baseline.

It is a visual reading layer for:
- system overview
- grouped ECU architecture
- canonical action flows
- per-ECU overview and reference cards
- detailed signal-flow appendix assets

It does not replace the canonical functional and communication documents under `driving-alert-workproducts/0301~0304`.

## How To Read

Read the book in this order:
1. `ECU_METADATA_BOOK_2026-03-28.md`
2. `ECU_METADATA_BOOK_2026-03-28.pdf`
3. `svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg`
4. `svg/GROUP_*.svg`
5. `ACTION_FLOW_INDEX_2026-03-28.md`
6. `svg/flows/action/FLOW_*.svg`
7. `ECU_CARD_INDEX_2026-03-28.md`
8. `svg/ecu_cards/*.svg`
9. `SIGNAL_FLOW_INDEX_2026-03-28.md`

## Book Structure

- `overview maps`
  - full ECU surface and grouped architecture
- `action-flow summaries`
  - the 20 canonical behavior chapters used in the main book body
- `ECU catalog`
  - each ECU is shown as a layered set:
    - `ECU_CARD_<ECU>_2026-03-28.svg`
    - `ECU_CARD_<ECU>_2026-03-28_P2.svg`
    - dense ECU may add `P3` and `P4` reference pages
- `detailed signal flows`
  - per-signal appendix assets for deeper drill-down

## Flow Layers

- `svg/flows/action/FLOW_01~20_*.svg`
  - canonical behavior summaries for the main narrative
- `flows/signal/*.puml`
  - editable detailed signal-flow sources
- `svg/flows/signal/*.svg`
  - vector appendix views of the same detailed signal flows
- `png/flows/signal/*.png`
  - bitmap appendix views of the same detailed signal flows

## Core References

Use these documents together with the book:
- `driving-alert-workproducts/0301_SysFuncAnalysis.md`
- `driving-alert-workproducts/0302_NWflowDef.md`
- `driving-alert-workproducts/0303_Communication_Specification.md`
- `driving-alert-workproducts/0304_System_Variables.md`
- `canoe/docs/contracts/communication-matrix.md`
- `canoe/docs/contracts/owner-route.md`
- `canoe/docs/verification/test-asset-mapping.md`

## Key Files

- `ECU_METADATA_BOOK_2026-03-28.md`
- `ECU_METADATA_BOOK_2026-03-28.pdf`
- `ECU_CARD_INDEX_2026-03-28.md`
- `ACTION_FLOW_INDEX_2026-03-28.md`
- `SIGNAL_FLOW_INDEX_2026-03-28.md`
