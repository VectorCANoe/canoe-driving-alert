# TMP Handoff (Next Codex Session)

## 0) Freshness Control
- Last Updated: 2026-03-07
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
  - Vehicle alert convenience extension (`Req_140~147`, Pre-Activation)
  - Warning robustness/cognitive extension (`Req_148~155`, Pre-Activation)
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
  - `Req_140~147` (Pre-Activation)
  - `Req_148~155` (Pre-Activation)
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
- 00c_Req_Classification_and_Safety_Profile.md: Version 1.6 (Draft, Internal Baseline Locked)
- 00d_HARA_Worksheet.md: Version 1.4 (Draft, Internal Baseline Approved)
- 00e_ECU_Naming_Standard.md: Version 2.7 (Released, SoT Fixed)
- 00f_CAN_ID_Allocation_Standard.md: Version 3.5 (Draft, Policy SoT)
- 01_Requirements.md: Version 5.30 (Draft)
- 02_Concept_design.md: Version 2.7 (Draft, Figure Finalized)
- 03_Function_definition.md: Version 4.31 (Draft)
- 0301_SysFuncAnalysis.md: Version 3.27 (Draft)
- 0302_NWflowDef.md: Version 3.23 (Draft)
- 0303_Communication_Specification.md: Version 3.26 (Draft)
- 0304_System_Variables.md: Version 2.24 (Draft)
- 04_SW_Implementation.md: Version 2.22 (Draft)
- 05_Unit_Test.md: Version 2.21 (Draft)
- 06_Integration_Test.md: Version 4.19 (Draft)
- 07_System_Test.md: Version 5.19 (Draft)
- Development Baseline Commit: `2678c58` (review-first freeze guidance added, 2026-03-07)

## 7) Immediate Next Steps
1. Keep `02_Concept_design.md` figure baseline fixed and ensure PPT sync consistency (star topology).
2. Close `M40-18`: fill Pre-Activation execution evidence in `05/06/07` (`Pass/Fail`, owner, date, trace/log refs, panel capture links) and sync with `04`.
3. Refresh submission lock anchors to current baseline:
   - `TMP_MID_AUDIT_MAIN.md` lock anchor
   - `tmp/reports/M40_EVIDENCE_INDEX.md` lock anchor
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
   - `M40-18`

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.
- Do not patch `canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg` by script unless explicitly requested for recovery.

## 9) Temporary Note
- This handoff is temporary and must be refreshed continuously.
- Once stale causes are resolved, keep handoff as SoT (`FRESH`) for the next session.

## 10) Expansion Freeze + Review-First Mode (Added)

### 10.1 Expansion Freeze Rule
- 문서 확장(신규 Req/Func/Flow/Comm/Var 추가)은 기본적으로 종료한다.
- 아래 조건 중 하나를 만족할 때만 확장 재개:
  - `M40-18` 실행증빙 폐쇄 완료
  - 멘토/리뷰어의 명시적 확장 지시

### 10.2 Current Working Mode
- 현재 모드는 `체크 중심 점검 모드`로 고정한다.
- 목표는 “새 내용 추가”가 아니라 “기존 논리의 오류/불일치 제거”다.

### 10.3 Review Checklist (문서팀 우선순위)
1. 체인 정합 점검:
   - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 링크 단절/역참조 오류 확인
2. 표현/수준 점검:
   - `01=What`, `03+=How` 분리 위반 문장 제거
   - 모호어(즉시/적절히/충분히) 대비 수치/조건 근거 확인
3. 정책 일관성 점검:
   - ECU 명칭(`00e`), CAN ID(`00f`), RTE 이름(`00g`)과 본문 불일치 확인
4. 표준 대조 점검:
   - `reference/standards/ISO26262*`, `ASPICE*`, `Project Result_Sample*` 대비 누락/과잉 확인
5. 증빙 링크 점검:
   - `05/06/07`의 VC/테스트 ID, 로그 경로, 캡처 참조의 유효성 확인

### 10.4 Change Policy in This Mode
- 허용: 오탈자 수정, 용어 통일, 추적 링크 보정, 근거/참조 정합화
- 제한: 기능 축 추가, 새로운 요구군 신설, 정책 체계 재설계
- 원칙: “noise 감소” 우선, “신규 내용 추가” 최소화
