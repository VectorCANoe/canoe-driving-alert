# TMP Handoff (Next Codex Session)

## 1) Project Direction (Fixed)
- Title: 주행 상황 실시간 경고 시스템
- Subtitle: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보
- Scope In:
  - Navigation zone recognition (school zone, highway, guide lane)
  - V2V emergency alerts (police, ambulance)
  - Ambient arbitration (priority and conflict resolution)
- Scope Out:
  - OTA/UDS subscription
  - platooning/logistics OTA
  - legacy risk-score warning features

## 2) Verification Constraints (Fixed)
- CANoe SIL only (no physical hardware)
- Network only: CAN + Ethernet (UDP)
- Required doc chain:
  - 01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07

## 3) Non-Negotiable Rules (Mentoring)
- Mandatory 1:1 traceability:
  - Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST
- Active Req range is locked for this cycle:
  - Req_001~043, Req_101~124
- Keep separation:
  - 01 = What
  - 03+ = How
- Random Req audit must not break the trace chain.
- Use V-model in both directions:
  - design to test
  - test failure back to source doc

## 4) Node Naming Baseline
- ADAS_WARN_CTRL
- NAV_CONTEXT_MGR
- WARN_ARB_MGR
- EMS_POLICE_TX
- EMS_AMB_TX
- EMS_ALERT_RX
- BCM_AMBIENT_CTRL
- CLU_HMI_CTRL
- SIL_TEST_CTRL

## 5) Priority and Timing Rules
- Emergency > Navigation context
- Ambulance > Police
- If same class: shorter ETA first
- If ETA tie: SourceID ascending
- Timeout clear: 1000 ms

## 6) Current Status
- 00_VModel_Mapping.md: Version 4.3 (Released)
- 00a_Audit_Readiness_Checklist.md: Version 1.11 (Draft)
- 00b_Project_Scope.md: Version 2.6 (Released)
- 00c_Req_Classification_and_Safety_Profile.md: Version 1.4 (Draft)
- 00d_HARA_Worksheet.md: Version 1.2 (Draft)
- 01_Requirements.md: Version 5.17 (Draft)
- 02_Concept_design.md: Version 2.4 (In Progress, figure build)
- 03_Function_definition.md: Version 4.21 (Draft)
- 0301_SysFuncAnalysis.md: Version 3.18 (Draft)
- 0302_NWflowDef.md: Version 3.14 (Draft)
- 0303_Communication_Specification.md: Version 3.14 (Draft, DBC synced to SoT)
- 0304_System_Variables.md: Version 2.16 (Draft)
- 04_SW_Implementation.md: Version 2.10 (Draft)
- 05_Unit_Test.md: Version 2.15 (Draft)
- 06_Integration_Test.md: Version 4.14 (Draft)
- 07_System_Test.md: Version 5.13 (Draft)
- Traceability audit status: `Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST` coverage aligned for active Req set (`Req_001~043`, `Req_101~124`)

## 7) Immediate Next Steps
1. Finalize `02_Concept_design.md` with fixed final figures (architecture + network flow).
2. Populate execution evidence in `05/06/07` (`Pass/Fail`, owner, date, trace/log refs).
3. Keep SoT sync rule active: domain CAN DBC (`*_can.dbc`) + Ethernet contract (`ETH_INTERFACE_CONTRACT.md`) -> `0302/0303/0304`.
4. Continue CANoe implementation/evidence loop on 04 and link UT/IT/ST real logs.
5. Remove this temporary handoff after stabilization and switch to permanent project index.

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.

## 9) Temporary Note
- This is a temporary handoff note and should be deleted after stabilization.
