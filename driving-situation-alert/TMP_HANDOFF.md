# TMP Handoff (Next Codex Session)

## 0) Freshness Control
- Last Updated: 2026-03-09
- Freshness Status: FRESH
- Validity Window: 3 days
- Stale Criteria (any one = stale):
  - Freshness Status is marked `STALE`
  - Node baseline includes deprecated validation node names as active naming
  - Document version snapshot differs from current headers in 01/03/0301/0302/0303/0304/04/05/06/07
- Stale Recovery Rule:
  - Use canonical docs as temporary SoT:
    - `01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`
    - `tmp/mentoring/Mentoring_MET40.md`
  - Refresh this handoff and switch back to `FRESH`.

## 1) Project Direction (Reset In Progress)
- Title: 주행 상황 실시간 경고 시스템
- Subtitle: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보
- Current Working Objective:
  - closeout 중심 운영을 종료하고, 양산차 프로젝트 표면에 맞는 논리 ECU 구조를 다시 정의한다.
  - 현재 최우선은 `표면 ECU 고정 -> 구현 모듈/검증 하네스 분리 -> GUI/문서 재정렬`이다.
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
- Keep separation:
  - `01 = What`
  - `03+ = How`
- ECU naming governance is reopened and now follows the reset baseline:
  - `00e` defines `surface ECU / runtime module / validation harness`
  - runtime rename or GUI rename must not happen before the document chain is updated
- Random Req audit must not break the trace chain.
- Use V-model in both directions:
  - design to test
  - test failure back to source doc

## 4) Current Reset Baseline

### 4.1 Surface ECU Baseline
- `CGW`
- `ETH_BACKBONE`
- `ECM`
- `TCM`
- `VCU`
- `ESP`
- `EPS`
- `BCM`
- `HVAC` (placeholder)
- `IVI`
- `CLUSTER`
- `ADAS`
- `V2X`
- `VALIDATION_HARNESS`

### 4.2 Runtime Transition Baseline
- runtime canonical names remain reference baseline until runtime merge decisions are approved
- key examples:
  - `ENG_CTRL -> ECM`
  - `ACCEL_CTRL -> VCU`
  - `BRK_CTRL -> ESP`
  - `STEER_CTRL -> EPS`
  - `BODY_GW / AMBIENT_CTRL / HAZARD_CTRL / WINDOW_CTRL / DRV_STATE_MGR -> BCM`
  - `IVI_GW / NAV_CTX_MGR -> IVI`
  - `CLU_HMI_CTRL / CLU_BASE_CTRL -> CLUSTER`
  - `ADAS_WARN_CTRL / WARN_ARB_MGR -> ADAS`
  - `EMS_POLICE_TX / EMS_AMB_TX / EMS_ALERT_RX -> V2X`
  - `VAL_* -> VALIDATION_HARNESS`

## 5) Priority and Timing Rules
- Emergency > Navigation context
- Ambulance > Police
- If same class: shorter ETA first
- If ETA tie: SourceID ascending
- Timeout clear: 1000 ms

## 6) Current Status Snapshot
- `00e_ECU_Naming_Standard.md`: reset baseline rewrite in progress
- `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`: code-reviewed baseline complete
- `TARGET_SURFACE_ECU_INVENTORY_V2_2026-03-09.md`: reviewed inventory complete
- `ECU_RESET_DOC_PROPAGATION_RULES_2026-03-09.md`: propagation order fixed
- current implementation baseline commit before next rewrite step: `f1df423`

## 7) Immediate Next Steps
1. Freeze the reviewed surface ECU inventory in `00e`.
2. Rewrite `0301` with surface ECU owner language first.
3. Rewrite `0302/0303` so reviewer-facing flows use surface ECU ownership.
4. Update `0304` with `Var -> Runtime -> Surface` mapping.
5. Keep `04` as runtime reality and mark merge candidates there.
6. Apply GUI surface rename only after the document chain is updated.

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.
- Do not patch `canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg` by script unless explicitly requested for recovery.
- Do not rename runtime nodes in GUI before logical ECU grouping and mapping are approved in docs.

## 9) Temporary Note
- This handoff is temporary and must be refreshed continuously.
- Once stale causes are resolved, keep handoff as SoT (`FRESH`) for the next session.

## 10) Architecture Reset Mode (Active)

### 10.1 Reset Trigger
- 개발 초기 단계에서 유지비용이 낮은 시점에 구조를 바로잡기 위해, closeout 중심 운영을 종료하고 architecture reset을 시작했다.
- 기존 handoff baseline은 archive asset으로 보존한다.

### 10.2 Current Working Mode
- 현재 모드는 `architecture reset + baseline rebuild`다.
- 목표는 “기존 baseline 방어”가 아니라 “양산차 프로젝트 표면에 맞는 구조로 재설계”다.

### 10.3 Reset Checklist
1. 논리 ECU 그룹 고정
2. surface / runtime / validation 계층 분리
3. runtime merge candidate 확정
4. 문서 체인 재정렬
5. GUI 표면명 마지막 적용

### 10.4 Change Policy in This Mode
- 허용:
  - 정책 체계 재설계
  - 논리 ECU 재분류
  - 문서 체인 전면 재작성
  - 구현 모듈 경계 재판정
- 제한:
  - 근거 없이 GUI/runtime rename을 먼저 수행하는 것
  - traceability chain을 끊는 ad-hoc 약어 도입
- 원칙:
  - `surface first, runtime second, evidence last`
