# TMP Handoff (Next Codex Session)

## 0) Freshness Control
- Last Updated: 2026-03-06
- Freshness Status: FRESH
- Validity Window: 7 days
- Stale Criteria (any one = stale):
  - Freshness Status is marked `STALE`
  - Node baseline includes deprecated validation node names as active naming
  - Document version snapshot differs from current headers in 01/03/0301/0302/0303/0304/04/05/06/07
- Stale Recovery Rule:
  - Use canonical docs as temporary SoT:
    - `01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`
    - `tmp/mentoring/Mentoring_MET40.md`
  - Refresh this handoff and switch back to `FRESH`.

## 1) Project Direction (Fixed)
- Title: 주행 상황 실시간 경고 시스템
- Subtitle: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보
- Scope In:
  - Navigation zone recognition (school zone, highway, guide lane)
  - V2V emergency alerts (police, ambulance)
  - Ambient/alert-priority decision
  - Vehicle baseline functions (`Req_101~119`) and V2 extension (`Req_120~121`, `Req_123`, `Req_125~129`)
  - ADAS object-risk extension (`Req_130~139`, Pre-Activation)
- Scope Out:
  - OTA/UDS subscription
  - platooning/logistics OTA
  - legacy risk-score warning features

## 2) Verification Constraints (Fixed)
- CANoe SIL only (no physical hardware)
- Network only: CAN + Ethernet (UDP, CAN-stub allowed in SIL constraints)
- Required doc chain:
  - `01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`

## 3) Non-Negotiable Rules (Mentoring)
- Mandatory 1:1 traceability:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- Active Req range in this cycle:
  - `Req_001~043`, `Req_101~107`, `Req_109~113`, `Req_116`, `Req_118~121`, `Req_123`, `Req_125~129`
  - `Req_130~139` (Pre-Activation)
- Keep separation:
  - `01 = What`
  - `03+ = How`
- ECU naming governance is fixed:
  - Explicit rule management only in `00e`, `0301`, `04`
  - Other chain docs use Canonical names only
- Random Req audit must not break the trace chain.
- Use V-model in both directions:
  - design to test
  - test failure back to source doc

## 4) Node Naming Baseline (Current)
- ADAS_WARN_CTRL
- NAV_CTX_MGR
- WARN_ARB_MGR
- EMS_ALERT (logical terminal)
- EMS_POLICE_TX / EMS_AMB_TX / EMS_ALERT_RX (internal implementation modules, `AMB` = Ambulance)
- AMBIENT_CTRL
- CLU_HMI_CTRL
- VAL_SCENARIO_CTRL
- VAL_BASELINE_CTRL

## 5) Priority and Timing Rules
- Emergency > Navigation context
- Ambulance > Police
- If same class: shorter ETA first
- If ETA tie: SourceID ascending
- Timeout clear: 1000 ms

## 6) Current Status Snapshot
- 00_VModel_Mapping.md: Version 4.3 (Released)
- 00a_Audit_Readiness_Checklist.md: Version 1.12 (Draft)
- 00b_Project_Scope.md: Version 2.8 (Released)
- 00c_Req_Classification_and_Safety_Profile.md: Version 1.5 (Draft, Internal Baseline Locked)
- 00d_HARA_Worksheet.md: Version 1.3 (Draft, Internal Baseline Approved)
- 00e_ECU_Naming_Standard.md: Version 2.0 (Released, SoT Fixed)
- 00f_CAN_ID_Allocation_Standard.md: Version 3.5 (Draft, Policy SoT)
- 01_Requirements.md: Version 5.27 (Draft)
- 02_Concept_design.md: Version 2.6 (In Progress, Figure Build)
- 03_Function_definition.md: Version 4.28 (Draft)
- 0301_SysFuncAnalysis.md: Version 3.24 (Draft)
- 0302_NWflowDef.md: Version 3.20 (Draft)
- 0303_Communication_Specification.md: Version 3.23 (Draft)
- 0304_System_Variables.md: Version 2.21 (Draft)
- 04_SW_Implementation.md: Version 2.20 (Draft)
- 05_Unit_Test.md: Version 2.18 (Draft)
- 06_Integration_Test.md: Version 4.16 (Draft)
- 07_System_Test.md: Version 5.16 (Draft)
- Development Baseline Commit: `d7e2a70` (G3 CLOSED + G4 HOLD, 2026-03-06)

## 7) Immediate Next Steps
1. Finalize `02_Concept_design.md` figure evidence and keep star topology consistency.
2. Fill execution evidence in `05/06/07` (`Pass/Fail`, owner, date, trace/log refs, panel capture links).
3. Complete DBC naming/ownership alignment:
   - Validation path: remove `test_can` dependency in active path
   - Validation ECU naming: legacy validation labels -> `VAL_*`
   - ADAS domain directive: apply `adas_can.dbc` creation and ownership split via dev change order
4. Apply naming/ID SoT:
   - Use `00e_ECU_Naming_Standard.md` as canonical ECU naming policy
   - Use `00f_CAN_ID_Allocation_Standard.md` as canonical CAN-ID policy
   - Gate status 운영: G1/G2/G3 closed, G4 hold(전체 개발 종료 후 재개)
   - Use `00g_RTE_Name_Mapping_Standard.md` as canonical RTE name mapping policy
   - Keep Canonical node names in trace docs; do not introduce unofficial abbreviations
5. Keep SoT sync rule active:
   - Domain CAN DBC (`*_can.dbc`) + Ethernet contract (`ETH_INTERFACE_CONTRACT.md`) -> `0302/0303/0304`
   - `Comm_130~Comm_133`는 `ETH_INTERFACE_CONTRACT.md v1.2`에 `E213~E216`이 반영되기 전까지 Pre-Activation/Pending 상태로 유지
6. Reflect Mentoring MET40 open items in docs/evidence:
   - `M40-01`, `M40-02`, `M40-04`, `M40-05`, `M40-06`, `M40-11`, `M40-14`

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.
- Do not patch `canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg` by script unless explicitly requested for recovery.

## 9) Temporary Note
- This handoff is temporary and must be refreshed continuously.
- Once stale causes are resolved, keep handoff as SoT (`FRESH`) for the next session.
