# CANoe Documentation System Blueprint

## 1. Decision

This repository will not bulk-import `canoe/AGENT/**` documents into the official documentation tree.

This repository will also not rewrite everything from zero without using the accumulated design work in `canoe/AGENT/**`.

The chosen policy is:

- keep `canoe/docs/**` as the small official document surface
- keep `canoe/AGENT/**` as the local research and archive bank
- promote only selected AGENT documents after rewriting them into stable, role-based official docs

## 2. Why this policy exists

The AGENT document set contains two very different classes of material:

- high-value system contracts and architecture notes
- time-bound audits, closure snapshots, migration notes, and research memos

Copying everything into the official tree would recreate the same clutter we just removed.

Ignoring everything and rewriting from zero would discard useful decisions that are still valid for the current Ethernet cutover architecture.

## 3. Official document roles

The official `canoe/docs/**` tree follows role separation.

### 3.1 `docs/architecture/`

Put only stable system structure and design boundaries here.

Examples:

- ECU classification and layer model
- surface/runtime/verification mapping
- runtime skeleton and path overview
- transport boundary explanation

### 3.2 `docs/contracts/`

Put operational contracts here.

Examples:

- communication matrix
- owner / bus / timeout / route policy
- Ethernet interface contract
- diagnostic sysvar contract
- panel / sysvar binding contract

### 3.3 `docs/verification/`

Put verification intent and evidence rules here.

Examples:

- execution guide
- pass criteria
- oracle policy
- evidence capture standard

### 3.4 `docs/operations/`

Put runtime working rules and maintenance runbooks here.

Examples:

- active workset
- GUI-only operation rules
- CAPL SoT vs mirror sync rules
- repair / recovery procedure

## 4. AGENT usage policy

`canoe/AGENT/**` is not official SoT.

It is a local bank for:

- design history
- migration rationale
- reference analysis
- reusable raw material for future official documents

Promotion rule:

- never copy AGENT documents into `canoe/docs/**` verbatim
- rewrite promoted content into present-tense, stable, reviewer-facing official docs
- remove dates, backlog noise, closure wording, and one-off execution commentary during promotion

## 5. Promotion map

### 5.1 Promote and rewrite first

These are strong source documents and should feed the next official docs.

| Target official doc | Primary AGENT source | Decision |
|---|---|---|
| `docs/architecture/10_ECU_CLASSIFICATION_AND_BOUNDARIES.md` | `AGENT/canoe/docs/operations/reference/OEM_4_LAYER_ECU_CLASSIFICATION_2026-03-10.md` | Rewrite into stable architecture doc |
| `docs/architecture/11_SURFACE_RUNTIME_VERIFICATION_MAP.md` | `AGENT/canoe/docs/architecture/project_explained.md` | Rewrite into stable system map |
| `docs/contracts/13_ETH_INTERFACE_CONTRACT.md` | `AGENT/canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | Rewrite into current Ethernet contract |
| `docs/contracts/14_COMMUNICATION_OWNERSHIP_MATRIX.md` | `AGENT/canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md` | Rewrite or regenerate into official matrix |
| `docs/contracts/15_MULTIBUS_ASSIGNMENT_POLICY.md` | `AGENT/canoe/docs/operations/MULTIBUS_ASSIGNMENT_POLICY.md` | Rewrite into official routing policy |
| `docs/contracts/16_DIAGNOSTIC_SYSVAR_CONTRACT.md` | `AGENT/canoe/docs/operations/verification/DIAGNOSTIC_SYSVAR_CONTRACT_2026-03-10.md` | Rewrite into stable contract |
| `docs/contracts/17_PANEL_SYSVAR_BINDING_CONTRACT.md` | `AGENT/canoe/docs/operations/panel/PANEL_DEVELOPMENT_SPEC.md` | Rewrite into binding contract focused on current panel/system variable surface |
| `docs/verification/23_EVIDENCE_LOGGING_STANDARD.md` | `AGENT/canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md` | Rewrite into official evidence policy |

### 5.2 Keep as research-only in AGENT

These may inform future work, but they should not be promoted as-is.

- `AGENT/canoe/docs/operations/CLI_PRODUCTIZATION_BP.md`
- `AGENT/canoe/docs/operations/reference/CAPL_coding_guideline.md`
- `AGENT/canoe/docs/operations/reference/OPEN_SOURCE_INTAKE_POLICY.md`
- `AGENT/canoe/docs/operations/reference/OSS_PANEL_REFERENCE_INDEX.md`
- `AGENT/canoe/docs/operations/unity/**`
- `AGENT/canoe/docs/operations/verification/CANOE_TEST_CI_BRIDGE_STRATEGY_2026-03-09.md`
- `AGENT/canoe/docs/operations/verification/TEST_AUTOMATION_REFERENCE_BASELINE_2026-03-09.md`

### 5.3 Keep as archive-only in AGENT

These are useful for history, but should not shape the official structure directly.

- `AGENT/canoe/docs/operations/audit/**`
- dated closure snapshots
- rename split plans
- placeholder migration waves
- temporary decision queues

## 6. Current quality bar for official docs

Any new official document under `canoe/docs/**` should satisfy all of the following:

- names a stable scope
- explains current active architecture, not past transition steps
- uses current folder and runtime terms
- avoids temporary owner tags such as `Dev1`, `wave1`, `phase1`, `closure`
- avoids backlog phrasing unless the document is explicitly an operations backlog
- is understandable without opening AGENT notes

## 7. Immediate next wave

Create these documents next, in this order:

1. `docs/architecture/10_ECU_CLASSIFICATION_AND_BOUNDARIES.md`
2. `docs/architecture/11_SURFACE_RUNTIME_VERIFICATION_MAP.md`
3. `docs/contracts/13_ETH_INTERFACE_CONTRACT.md`
4. `docs/contracts/16_DIAGNOSTIC_SYSVAR_CONTRACT.md`
5. `docs/contracts/17_PANEL_SYSVAR_BINDING_CONTRACT.md`

## 8. Non-goal

Do not try to make `canoe/docs/**` a full archive.

The official tree should stay small, readable, and current.

Historical depth belongs in `canoe/AGENT/**`.
