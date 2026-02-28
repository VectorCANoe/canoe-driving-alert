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
- 00_VModel_Mapping.md: active and updated
- 00b_Project_Scope.md: active and updated
- 01_Requirements.md: active, Version 5.4
- 02_Concept_design.md: active
- 03_Function_definition.md: active
- 0301~0304: next refinement target

## 7) Immediate Next Steps
1. Refine 0301 with Vector table style and current node names.
2. Refine 0302 with Flow ID, Tx/Rx, period, active/clear conditions.
3. Refine 0303 with Comm ID and testable signal specs.
4. Refine 0304 with Var ID, type, init, owner, and trace links.
5. Finalize 07 with strict Req 1:1 system-test mapping.

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.

## 9) Temporary Note
- This is a temporary handoff note and should be deleted after stabilization.
