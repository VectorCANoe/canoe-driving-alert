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
- System-level viewpoint is mandatory:
  - 문서/구현 판단 기준은 `단일 시나리오 최적화`가 아니라 `완성차 시스템 관점`이다.
  - ECU/메시지/흐름은 특정 데모 장면이 아니라 차량 전반 동작(입력->판정->출력->진단/검증)을 기준으로 설계한다.

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

### 10.5 Tool Execution Discipline
- 파일 `쓰기/복사/삭제`와 그 직후 `읽기 검증`은 병렬로 돌리지 않는다.
- 수정 작업은 `write -> immediate read/hash/diff verification` 순서로 순차 처리한다.
- 병렬 실행은 `read-only` 작업에만 사용한다.
  - 예: `search`, `git status/log`, `gate`, `read-only diff`
- 긴 중첩 PowerShell 래핑보다 `apply_patch` 또는 단일 직접 명령을 우선한다.
- 문서/코드 반영 후에는 실제 파일 기준으로 `git diff` 또는 핵심 문자열 검증을 반드시 남긴다.

## 11) Team Instance Boundary (Active)

### 11.1 Dev1 Instance
- Primary ownership:
  - `canoe/`
- Current responsibility:
  - CANoe runtime/CAPL 구조 리팩토링
  - ECU surface/runtime merge candidate 검토
  - native CANoe test asset 및 validation harness 안정화
  - `canoe/docs/operations/*` 내부 구현/검증 운영 문서
- Do not do:
  - `driving-situation-alert/` 정본 SoT 직접 수정
  - `scripts/`, `product/sdv_operator/`의 Dev2 제품/도구 흐름 직접 변경

### 11.2 Dev2 Instance
- Primary ownership:
  - `scripts/`
  - `product/sdv_operator/`
- Current responsibility:
  - TUI/CLI/Operator product
  - 검증 실행 오케스트레이션
  - JSON/MD/CI bridge/evidence packaging
- Do not do:
  - `canoe/` runtime/CAPL 로직 직접 리팩토링
  - `driving-situation-alert/` 정본 SoT 직접 rewrite

### 11.3 Docs Instance
- Primary ownership:
  - `driving-situation-alert/`
- Current responsibility:
  - 정본 SoT 문서(`00/01/03/0301/0302/0303/0304/04/05/06/07`)
  - 제출 문서셋/보드/hand-off 동기화
  - reset baseline의 문서 전파
- Do not do:
  - `canoe/` 구현 코드/CAPL 직접 변경
  - `scripts/`, `product/sdv_operator/` 제품 동작 직접 변경

### 11.4 Cross-Team Rule
- Dev1은 SoT 변경이 필요하면 문서팀에 기준안만 전달한다.
- Dev2는 operator/tooling 변경이 필요하면 제품 표면과 실행 산출물만 책임진다.
- 문서팀은 정본 SoT와 제출 문서를 책임지고, 구현 반영은 Dev1/Dev2 기준안에 따라 후행 반영한다.
- 예외:
  - `TMP_HANDOFF.md`
  - 팀 보드/queue 성격의 임시 coordination 문서
  - 리드 지시가 있는 cross-team reset 문서
### 11.5 OEM System Framing Rule (Added)
- 이 프로젝트는 “한 시나리오 PoC”가 아니라 “OEM 차량 시스템 축약 모델”로 정의한다.
- 따라서 문서/코드 판단 우선순위는 아래를 따른다:
  1. 차량 전체 구조 타당성(도메인/경계/Owner)
  2. 통신 규칙 일관성(ID/주기/Timeout/소유권)
  3. 검증 가능성(UT/IT/ST 및 하네스 증빙)
  4. 개별 시나리오 표현
- 단일 시나리오 편의를 위해 전체 구조를 왜곡하는 변경은 금지한다.
