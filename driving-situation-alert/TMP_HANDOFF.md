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
  - OEM 전차량 프레이밍을 채택하되, 제품 핵심가치는 `구간 정보 + 긴급차량 접근 기반 실시간 경고`로 고정한다.
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
- Submission rule is fixed:
  - 각 문서의 `공식 표준 양식` 상단 표만 제출 정본으로 간주한다.
  - 하단 `보강표/상세 추적표/참고표`는 내부 작업용 reference이며, 제출 근거를 단독으로 대신할 수 없다.
  - 어떤 입력/처리/출력/시나리오/판정 기준이 하단 표에만 있으면 안 되며, 제출 시점 전에는 상단 공식 표로 끌어올려야 한다.
  - 단, 상단 `공식 표준 양식`의 열/헤더 구조 자체는 임의로 바꾸지 않는다. 상세도가 더 필요하면 기존 컬럼 안에서 문장을 보강한다.
  - 상단 `공식 표준 양식`은 reviewer-facing 요약 표로 유지하며, runtime/module 구현명이나 저수준 기술 나열은 템플릿이 요구하지 않는 한 넣지 않는다.
  - 상단 `공식 표준 양식`의 문체는 `vector_sample`, `Project Result_Sample`의 BP 어투를 따른다. 짧은 평문 문장, 실제 ECU/서비스 기준 표현, "A 정보를 수신하여 B에 반영/전달" 형식을 우선한다.
  - 상단 `공식 표준 양식`은 `Flow/Comm` ID, `체인` 같은 표현, 타 문서 참조에 기대지 않고 그 표만 읽어도 이해 가능해야 한다.
  - ID 범위가 넓더라도 OEM 관점의 의미, 주체, 검증 의도가 달라지면 reviewer-facing 행은 과도하게 합치지 말고 분리한다.
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
- `DCM`
- `IBOX`
- `SGW`
- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `ABS`
- `EPB`
- `TPMS`
- `SAS`
- `VSM`
- `EHB`
- `ECS`
- `CDC`
- `BCM`
- `DATC`
- `SMK`
- `AFLS`
- `WIPER_MODULE`
- `BODY_SECURITY_MODULE`
- `DOOR_FL`
- `DOOR_FR`
- `SEAT_DRV`
- `SEAT_PASS`
- `IVI`
- `CLU`
- `HUD`
- `AMP`
- `VOICE_ASSIST`
- `TMU`
- `SCC`
- `ADAS`
- `V2X`
- `VALIDATION_HARNESS`

### 4.2 Runtime Transition Baseline
- runtime canonical names remain reference baseline until runtime merge decisions are approved
- key examples:
  - `ENG_CTRL -> EMS`
  - `ACCEL_CTRL -> VCU`
  - `BRK_CTRL -> ESC`
  - `STEER_CTRL -> MDPS`
  - `BODY_GW / AMBIENT_CTRL / HAZARD_CTRL / WINDOW_CTRL / DRV_STATE_MGR -> BCM`
  - `IVI_GW / NAV_CTX_MGR -> IVI`
  - `CLU_HMI_CTRL / CLU_BASE_CTRL -> CLU`
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
- Dev1 최신 runtime anchor 승격 반영: `a6fecf1 + 2216335 + f61cb26 + 1fda129`
- visible surface bank: `100` (`99 active + 1 placeholder(NIGHT_VISION)`)
- deep runtime profile: `98 product + VALIDATION_HARNESS(2 runtime nodes)` 기준으로 운영
- `00e_ECU_Naming_Standard.md`: active/placeholder 상태를 최신 승격 기준으로 동기화 완료
- `00f_CAN_ID_Allocation_Standard.md`: placeholder ID 비할당/승격 시 배정 규칙 유지

## 7) Immediate Next Steps
1. Keep `00f` placeholder ID policy as `no allocation until promotion`.
2. `0301/0302/0303` owner 표기에서 surface ECU 우선 원칙 유지(구현 모듈명은 supporting note로 한정).
3. `0304`는 `Var -> Runtime -> Surface` 추적을 유지하고 placeholder 과잉 명세를 금지.
4. `04`는 runtime reality를 유지하고, 승격/미승격 경계를 명시한다.
5. Dev2 게이트 정책(`check_capl_sync.py`)에서 residual placeholder(`NIGHT_VISION`) 처리 규칙만 정리한다.
6. GUI import/compile cycle은 active 99 우선 검증, placeholder 1은 compile-safe 확인만 수행한다.
7. `05/06/07` 상단 공식 표에는 입력 조건, 기대 출력, 대표 시나리오, 판정 기준이 기존 컬럼 안에 직접 들어가야 하며 하단 추적표 의존을 줄인다.
8. `0301` 상단 공식 표는 기존 열 구조(`노드/기능 상세/비고`)를 유지한 채 노드 요약을 넘어서 노드별 기능 명세가 직접 보이도록 보강한다.

## 8) Do Not Do
- Do not change file encoding away from UTF-8.
- Do not place implementation details in 01.
- Do not write customer-level statements only in 03.
- Do not remove existing template columns.
- Do not patch `canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg` by script unless explicitly requested for recovery.
- Do not rename runtime nodes in GUI before logical ECU grouping and mapping are approved in docs.
- Do not leave 제출 핵심 내용(입력/출력/시나리오/판정 기준)을 하단 보강표에만 두고 상단 공식 표를 빈약하게 유지하지 않는다.

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

### 11.5 Team Commit/Push Isolation Rule
- Dev1은 `canoe/` 소유 변경만 commit/push한다.
- Dev2는 `scripts/`, `product/sdv_operator/` 및 Dev2 운영에 필요한 최소 coordination 문서만 commit/push한다.
- 문서팀은 `driving-situation-alert/` 정본/제출 문서 변경만 commit/push한다.
- 다른 팀 경로가 dirty여도 자기 소유 경로만 `git add`해서 선별 commit/push한다.
- 타 팀 변경을 임시로 로컬에 보관(stash/backup)할 수는 있지만, 묶어서 함께 push하지 않는다.
- cross-team coordination 문서(`TMP_HANDOFF.md`, 팀 보드, 리드 지시 문서)는 목적 범위에 맞는 최소 변경만 허용한다.

### 11.6 OEM System Framing Rule (Added)
- 이 프로젝트는 “한 시나리오 PoC”가 아니라 “OEM 차량 시스템 축약 모델”로 정의한다.
- OEM breadth 확장은 `핵심 가치 시나리오(구간/긴급차량 기반 경고)`를 대체하지 않고, 그 시나리오를 차량 전체 구조 안에 정합되게 배치하기 위한 것이다.
- 따라서 문서/코드 판단 우선순위는 아래를 따른다:
  1. 차량 전체 구조 타당성(도메인/경계/Owner)
  2. 통신 규칙 일관성(ID/주기/Timeout/소유권)
  3. 검증 가능성(UT/IT/ST 및 하네스 증빙)
  4. 개별 시나리오 표현
- 단일 시나리오 편의를 위해 전체 구조를 왜곡하는 변경은 금지한다.

## 12) Documentation Minimalism and Lifecycle (Active)

### 12.1 Why
- 부가 문서를 무제한으로 늘리면 최신 기준이 분산되고, 동일 주제의 중복 설명이 생겨 문서/구현 정합 품질이 오히려 떨어진다.
- 따라서 OSS repo 운영처럼 “핵심 정본 중심 + 수명 짧은 보조 문서” 원칙을 적용한다.

### 12.2 Keep vs Remove Rule
- 항상 유지(삭제 금지):
  - 정본 SoT 체인: `00/01/03/0301/0302/0303/0304/04/05/06/07`
  - 멘토 체크리스트/핸드오프 등 현재 운영 기준 문서
  - 제출본으로 확정된 문서셋
- 제한 생성(필요 시만 생성):
  - 분석 메모, 비교표, 임시 의사결정 노트, 작업 큐 문서
- 사용 종료 후 정리:
  - 임시 문서의 내용이 정본에 반영 완료되면 해당 임시 문서는 삭제 또는 archive로 이동
  - 동일 목적 문서가 2개 이상이면 최신 1개만 유지

### 12.3 Creation Gate (Before adding a new doc)
1. 기존 SoT 문서의 섹션 추가로 해결 가능한가?
2. 새 문서가 없으면 작업/의사결정이 실제로 막히는가?
3. 종료 조건(삭제/흡수 시점)이 명확한가?
- 3개 중 하나라도 `No`면 새 문서 생성 금지, 기존 문서를 부분수정한다.

### 12.4 Quality Guardrail
- 문서 축소 자체는 품질을 떨어뜨리지 않는다.
- 다만 다음은 품질 저하로 간주한다:
  - SoT 증빙이 없는 상태에서 임시 문서만 삭제
  - 추적체인(Req->...->Test)을 끊는 삭제
  - 운영 중 문서를 archive만 하고 정본 반영을 생략
- 원칙: `정본 강화 -> 임시 정리` 순서로만 정리한다.
