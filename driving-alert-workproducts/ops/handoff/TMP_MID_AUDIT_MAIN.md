# TMP Mid-Audit Pack (main)

- Baseline branch: `main`
- Baseline commit: `8eb020e`
- Baseline date: `2026-03-08 01:48:18 +0900`
- Purpose: Mid-audit frozen reference + one-page answer + random rehearsal set

## 0) Mid-Report Submission Lock (M40-01, M40-15)

- Lock timestamp: `2026-03-08`
- Lock anchor: `main@8eb020e`
- Scope lock:
  - `PPT`: `driving-situation-alert/02_Concept_design.md`, `driving-situation-alert/tmp/assets/current/02_concept.png`, `driving-situation-alert/tmp/assets/current/02_networkflow.png`
  - `Excel`: 제출본 원본은 외부 저장소(비Git) 관리, 본 문서에서 점검 결과와 포맷 기준을 잠금
  - `DBC`: `canoe/databases/*.dbc` (도메인 분리 제출 기준)

### Excel format gate (submission checklist)

| Check ID | 점검 항목 | 기준 | 결과 | 비고 |
|---|---|---|---|---|
| XL-01 | 첫 탭 프로젝트 개요 | 첫 탭에 프로젝트 개요 존재 | PASS | 멘토 지시 반영 항목 잠금 |
| XL-02 | 팀 간 비교 가능한 탭/컬럼 구조 | 요구/기능/통신/검증 탭 구조 일관성 | PASS | 비교 평가 가능 형태 유지 |
| XL-03 | 주기/이벤트 명시 | Comm 항목에 Period/Event 누락 없음 | PASS | `0302/0303` SoT 기반 점검 |

## 1) Mid-Audit Baseline Freeze (03/0301/0302/0303/0304)

### Frozen set
- `driving-situation-alert/03_Function_definition.md`
- `driving-situation-alert/0301_SysFuncAnalysis.md`
- `driving-situation-alert/0302_NWflowDef.md`
- `driving-situation-alert/0303_Communication_Specification.md`
- `driving-situation-alert/0304_System_Variables.md`

### Freeze rule
- During mid-audit, the five files above are treated as control baseline.
- If any update is unavoidable, update as one change-set with explicit chain impact:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- No standalone single-file patch is allowed in the frozen set.
- DBC/contract sync check remains mandatory for this baseline:
  - `0302/0303 <-> canoe/databases/*.dbc`
  - `0302/0303 <-> canoe/docs/operations/10_ETHERNET_BACKBONE_INTERFACE_SPEC.md`

## 2) One-Page Audit Answer (Ready-to-use)

### A. Architecture answer (what we fixed and why)
- Decision logic stays in logic nodes: `ADAS_WARN_CTRL`, `WARN_ARB_MGR`, `NAV_CTX_MGR`, `EMS_ALERT`.
- Rendering stays in gateway/panel side as derived output only (`IVI_GW`, panel variables).
- Priority/timeout logic is not placed in rendering layer.
- Validation scope is fixed to CANoe SIL, CAN + Ethernet(Stub contract).

### B. Traceability chain answer (template)
- `Req -> Func`: defined in `03`, decomposed in `0301`.
- `Func -> Flow`: defined in `0302`.
- `Flow -> Comm`: defined in `0303`.
- `Comm -> Var`: defined in `0304`.
- `Var -> Code`: implemented in CAPL nodes (`canoe/src/capl/...`), traced via `04`.
- `Code -> UT/IT/ST`: validated by `05/06/07`.

### C. EMS logical terminal mapping principle (audit wording)
- Top-level documents use one logical terminal name: `EMS_ALERT`.
- Internal implementation is split only in mapping/detail sections:
  - `EMS_POLICE_TX` (Police Tx)
  - `EMS_AMB_TX` (Ambulance Tx)
  - `EMS_ALERT_RX` (Rx/Clear/Timeout)
- Evidence:
  - `03_Function_definition.md:24`, `03_Function_definition.md:150`
  - `0301_SysFuncAnalysis.md:30`, `0301_SysFuncAnalysis.md:209`, `0301_SysFuncAnalysis.md:211`
  - `0304_System_Variables.md:27`, `0304_System_Variables.md:334`

## 3) Random Sample Rehearsal (5)

- Sampling method: pseudo-random (`seed=20260303`) from `Req_001..Req_043`
- Sampled set: `Req_009`, `Req_031`, `Req_024`, `Req_027`, `Req_010`
- Rehearsal result: `PASS` (all 5 keep end-to-end chain evidence)

| Req | Func/Node | Flow/Comm | Var | Code | UT/IT/ST rehearsal anchors |
|---|---|---|---|---|---|
| Req_009 | `Func_009` / `AMBIENT_CTRL` (`0301:112`, `04:130`) | `Flow_007` / `Comm_007` (`0302:314`, `0303:311`) | `Var_021` (`0304:408`) | `canoe/src/capl/output/AMBIENT_CTRL.can` | `UT_BCM_001` (`05:78`) / `IT_OUT_001` (`06:38`) / `ST_ZONE_001` (`07:65`) |
| Req_031 | `Func_031` / `WARN_ARB_MGR` (`0301:134`, `04:152`) | `Flow_006` / `Comm_006` (`0302:313`, `0303:310`) | `Var_010` (`0304:396`) | `canoe/src/capl/logic/WARN_ARB_MGR.can` | `UT_ARB_001` (`05:77`) / `IT_ARB_030_031_A` (`06:75`) / `ST_ARB_ETA_001` (`07:73`) |
| Req_024 | `Func_024` / `EMS_ALERT`(`0301`) + `EMS_ALERT_RX`(`04`) (`0301:127`, `04:145`) | `Flow_006` / `Comm_006` (`0302:313`, `0303:310`) | `Var_011`,`Var_020`,`Var_027` (`0304:397`,`0304:407`,`0304:414`) | `canoe/src/capl/logic/EMS_ALERT_RX.can` | `UT_EMS_RX_001` (`05:76`) / `IT_TIMEOUT_001` (`06:39`) / `ST_TIMEOUT_001` (`07:75`) |
| Req_027 | `Func_027` / `WARN_ARB_MGR` (`0301:130`, `04:148`) | `Flow_006` / `Comm_006` (`0302:313`, `0303:310`) | `Var_016` (`0304:403`) | `canoe/src/capl/logic/WARN_ARB_MGR.can` | `UT_ARB_001` (`05:77`) / `IT_ARB_001` (`06:37`) / `ST_POLICY_001` (`07:76`) |
| Req_010 | `Func_010` / `ADAS_WARN_CTRL` (`0301:113`, `04:131`) | `Flow_001,Flow_003` / `Comm_001,Comm_003` (`0302:308`, `0303:305`) | `Var_001`,`Var_031` (`0304:386`, `0304:402`) | `canoe/src/capl/logic/ADAS_WARN_CTRL.can` | `UT_ADAS_001` (`05:72`) / `IT_CORE_001` (`06:35`, Req range) / `ST_SPEED_001` (`07:64`) |

## 4) Quick Audit Script Line (operator memo)

1. Confirm branch/hash: `git branch --show-current && git rev-parse --short HEAD`
2. Open only baseline five docs + this TMP file
3. For each requested Req, answer in this exact order:
   - Req -> Func (`03`,`0301`)
   - Flow/Comm (`0302`,`0303`)
   - Var (`0304`)
   - Code file (`canoe/src/capl/...`)
   - UT/IT/ST (`05`,`06`,`07`)
