# AGENT Document Triage

## Purpose

This file helps future agents decide which local AGENT documents are worth mining and which ones should remain archive-only.

Rule:

- do not bulk-copy AGENT docs into `canoe/docs/**`
- use AGENT docs as source material
- rewrite promoted content into stable official docs

## High-value source documents

Promote by rewrite, not by copy.

### Architecture

- `AGENT/canoe/docs/architecture/project_explained.md`
- `AGENT/canoe/docs/operations/reference/OEM_4_LAYER_ECU_CLASSIFICATION_2026-03-10.md`

### Contracts

- `AGENT/canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- `AGENT/canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`
- `AGENT/canoe/docs/operations/MULTIBUS_ASSIGNMENT_POLICY.md`
- `AGENT/canoe/docs/operations/verification/DIAGNOSTIC_SYSVAR_CONTRACT_2026-03-10.md`
- `AGENT/canoe/docs/operations/panel/PANEL_DEVELOPMENT_SPEC.md`

### Verification

- `AGENT/canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md`
- `AGENT/canoe/docs/operations/verification/SIL_PASS_CRITERIA.md`
- `AGENT/canoe/docs/operations/verification/CANOE_TEST_UNIT_RUNBOOK.md`

## Research-only documents

Keep for ideas and later productization work.

- `AGENT/canoe/docs/operations/CLI_PRODUCTIZATION_BP.md`
- `AGENT/canoe/docs/operations/reference/CAPL_coding_guideline.md`
- `AGENT/canoe/docs/operations/reference/OPEN_SOURCE_INTAKE_POLICY.md`
- `AGENT/canoe/docs/operations/reference/OSS_PANEL_REFERENCE_INDEX.md`
- `AGENT/canoe/docs/operations/unity/**`
- `AGENT/canoe/docs/operations/verification/CANOE_TEST_CI_BRIDGE_STRATEGY_2026-03-09.md`
- `AGENT/canoe/docs/operations/verification/TEST_AUTOMATION_REFERENCE_BASELINE_2026-03-09.md`

## Archive-only documents

Keep only for history and decision trace.

- `AGENT/canoe/docs/operations/audit/**`
- `AGENT/canoe/docs/operations/reference/OEM_PLACEHOLDER_*`
- `AGENT/canoe/docs/operations/reference/RUNTIME_*`
- `AGENT/canoe/docs/operations/reference/PRIMARY56_RUNTIME26_MAPPING_2026-03-09.md`
- dated closure / queue / snapshot documents

## Decision standard

When deciding whether an AGENT doc should be promoted:

- if it describes a stable active contract, rewrite and promote
- if it describes a candidate plan, keep as research
- if it records a dated closure or audit event, keep as archive

## First official documents to build from AGENT

1. `docs/architecture/10_ECU_CLASSIFICATION_AND_BOUNDARIES.md`
2. `docs/architecture/11_SURFACE_RUNTIME_VERIFICATION_MAP.md`
3. `docs/contracts/13_ETH_INTERFACE_CONTRACT.md`
4. `docs/contracts/16_DIAGNOSTIC_SYSVAR_CONTRACT.md`
5. `docs/contracts/17_PANEL_SYSVAR_BINDING_CONTRACT.md`
