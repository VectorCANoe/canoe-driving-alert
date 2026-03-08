# Team Sync Board (Dev1 / Dev2 / Docs)

## 목적
- 개발 1팀, 개발 2팀, 문서팀이 동일 변경사항을 같은 형식으로 확인/갱신하는 공용 전달 보드.
- 구두 전달/채팅 전달로 인한 누락을 줄이고, `문서-코드-증빙` 동기화를 빠르게 확인한다.

## 운영 원칙
1. 한 변경사항 = 보드 1행.
2. 상태 변경 시 `증빙`(파일/커밋/리포트) 함께 갱신.
3. 문서팀은 `driving-situation-alert` 체인(01~07) 기준으로만 반영 상태를 판단.
4. 개발팀은 구현 완료 후 `Ready for Docs`로 전환하고, 문서팀 반영 완료 시 `Done`으로 닫는다.

## 상태 코드
- `Proposed`: 제안됨
- `In Progress`: 작업 중
- `Ready for Docs`: 코드/설계 반영 완료, 문서 반영 대기
- `Docs Updated`: 문서 반영 완료
- `Done`: 코드+문서+증빙 폐쇄
- `Blocked`: 외부 의존(라이선스/환경)으로 보류

## 팀별 역할 분리 (고정)

| 구분 | 개발 1팀 (구현) | 개발 2팀 (검증+CLI) | 문서팀 |
|---|---|---|---|
| 주책임 | CAPL/DBC/멀티버스/GW 구조 고정 | 테스트 실행체계, 자동화, 리포트 수집 | 00~07 문서 정합/제출본 |
| 핵심 산출물 | 코드/DBC/CFG 안정화 | Pass/Fail 리포트, CLI 명령 체계 | Req~Test 추적성, 멘토 피드백 반영 |

## 병렬 가능 작업 (즉시)

### 개발 1팀
- `timeNow()` 경고 정리(overflow-safe 시간 계산 패턴 반영)
- GW/멀티버스 정책 최종 고정(일반 노드 단일 버스, GW 다중 버스)
- DBC 도메인 소유권/중복 ID 최종 점검

### 개발 2팀
- gate + test 일괄 실행 CLI 완성
- UT/IT/ST 자동 실행 및 결과 수집 포맷 고정(JSON/MD)
- 오프라인 실행 패키지/명령어 정리

### 문서팀
- `Req_151` 문구 명확화(“경로 상태” 모호 표현 제거)
- `Req_017`, `Req_139/VC_139` 문장 정밀화
- `00f`에 11-bit 유지 + 29-bit 전환 조건 디펜스 문구 추가
- 제출 양식(멘토 양식) 정렬

## 선행-후행 작업 (의존)

1. 선행: 개발 1팀 인터페이스 동결
2. 후행 병렬: 개발 2팀 검증 자동화 최종 실행 + 문서팀 `0302/0303/0304/04` 동기화
3. 선행: 개발 2팀 Pass/Fail 증빙 확정
4. 후행: 문서팀 `05/06/07` 최종 폐쇄 및 제출본 반영

## 인터페이스 동결 항목 (개발1 선행)
- SysVar 이름/범위/단위
- CAN/ETH 메시지명 및 ID 소유권
- CAPL 노드 역할(일반 노드 vs GW vs 테스트 노드)

## 팀 운영 규칙
- 구현 변경은 개발 1팀 머지 후 검증 리런(개발 2팀)
- 문서팀은 `동결된 인터페이스` 기준으로만 반영
- 문서 확장보다 증빙 폐쇄 우선(Pass/Fail 중심)

## 공용 변경 보드

| ID | 주제 | 요청팀 | 담당팀 | 상태 | 코드/구현 증빙 | 문서 반영 대상 | 문서 상태 | 비고 |
|---|---|---|---|---|---|---|---|---|
| TSB-001 | 역할 분리 타당성 점검(멀티버스/GW/테스터) | Dev1 | Dev1 + Docs | Docs Updated | `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`, `scripts/gates/multibus_cfg_dbc_gate.py` PASS | `tmp/mentoring/Mentoring_MET41.md`, `0302/0303` | 반영완료 | Dev1 구조 고정 완료: 일반 노드 단일버스, GW 다중버스, 테스터 예외 운영 |
| TSB-002 | Req_151 문구 명확화 (`도메인 헬스/경로 상태`) | Docs | Docs | Docs Updated | `01_Requirements.md` (`Req_151`,`VC_151`) | `01_Requirements.md` + VC 문구 | 반영완료 | 도메인 경계 통신 상태(주기/타임아웃/유효플래그) 기준으로 수정 |
| TSB-003 | Req_017/Req_139 표현 정밀화 | Docs | Docs | Docs Updated | `01_Requirements.md` (`Req_017`,`Req_139`,`VC_139`) | `01_Requirements.md` | 반영완료 | `일반차` 표현 정리 + 우선순위 규칙 문장 명확화 |
| TSB-004 | CANoe 공식 Test PoC 1~2건 + Dev2 외부화 브리지 정합 | Dev1 | Dev1 + Dev2 + Docs | In Progress | `canoe/docs/operations/verification/CANOE_TEST_POC_SCOPE_2026-03-08.md`, native CANoe test source/report, Dev2 TUI/CLI package flow | `04`, `05`, `06`, `07`, `TMP_HANDOFF.md`, `tmp/mentoring/Mentoring_MET41.md` | 진행중 | Dev1은 native CANoe test 자산 작성, Dev2는 외부 orchestration/evidence/CI 브리지 유지 |
| TSB-005 | M40-18 실행 증빙 폐쇄 | Dev1 + Dev2 | Dev1 + Dev2 + Docs | In Progress | 로그/캡처/리포트 | `05/06/07`, `TMP_HANDOFF.md` | 진행중 | G4 재개 조건 |
| TSB-008 | Dev2 검증 일괄 CLI + 저장포맷 옵션(기본 JSON/MD, CSV 선택) | Dev2 | Dev2 | Docs Updated | `scripts/run.py` (`verify batch`, `shell /verify batch`), `scripts/README.md`, `canoe/tmp/onboarding/VERIFY_EXECUTION_RUNBOOK.md` | `05/06/07` 실행 증빙 작성 가이드에 연결 | 반영완료 | pre/post/full 배치 + `--report-formats` (`json,md` 기본 / `csv` 옵션) |
| TSB-006 | CAPL `timeNow()` overflow-safe 정리 | Dev1 | Dev1 | Docs Updated | `src/capl/*`, `cfg/channel_assign/*`의 `timeNowInt64()` 전환 + `check_capl_sync` PASS | 필요 시 `0304`, `04` 구현 노트 | 반영완료 | 컴파일 경고 `08-0041` 사전 제거 목적 |
| TSB-007 | ETH Backbone DBC 누락 3건 보완 | Dev1 | Dev1 | Docs Updated | `canoe/databases/eth_backbone_can_stub.dbc` + `multibus-dbc` PASS | `0303`, `00f`(소유권/ID 운영 근거) | 반영완료 | `ethVehicleStateMsg`, `ethSteeringMsg`, `ethNavContextMsg` 추가 |
| TSB-009 | 인터페이스/멀티버스/CLI 운영 해석 정렬 | Docs | Docs + Dev2 | Docs Updated | `scripts/run.py`, `scripts/README.md`, `scripts/gates/multibus_cfg_dbc_gate.py` | `tmp/change-orders/TEAM_SYNC_BOARD.md` | 반영완료 | 인터페이스는 메시지 계약 단위로 해석, 도메인 테스트 분리 + E2E 예외 멀티버스 정책 명확화 |
| TSB-011 | ECU 명명/약어 정책 재확인 (멘토 D11 + `_TX/_RX` 해석) | Dev1 | Dev1 + Docs | Ready for Docs | `docs/meeting-notes/MET_41_2026.03.07.txt`, `driving-situation-alert/00e_ECU_Naming_Standard.md`, `reference/standards/AUTOSAR_CP_TR_SWCModelingGuide.pdf` 교차검증 | `00e`, `0302`, `0303` | 대기 | 결론: 3글자 강제 아님, 짧은 약어 권장. 상위 체인 문서는 논리명 우선(`EMS_ALERT`), 구현/하위 매핑표만 내부 모듈명(`EMS_*_TX/RX`) 허용 |

## 업데이트 템플릿

| ID | 날짜 | 변경 요약 | 변경 파일 | 상태 전환 | 담당 | 증빙 링크/커밋 |
|---|---|---|---|---|---|---|
| TSB-001 | 2026-03-08 | 역할 분리 운영정책을 Dev1 기준으로 확정하고 문서 반영 대기 전환 | `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`, `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` | In Progress -> Ready for Docs | Dev1 | `79c0b98`, `137a69e` |
| TSB-001 | 2026-03-08 | 멀티버스 운영 원칙(일반 노드 단일버스/GW 경유/테스터 예외)을 SoT 문서와 MET41에 반영 | `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md`, `driving-situation-alert/tmp/mentoring/Mentoring_MET41.md` | Ready for Docs -> Docs Updated | Docs | `48b351e` |
| TSB-006 | 2026-03-08 | CAPL 시간 계산 overflow-safe 구현 기준(`timeNowInt64`)을 SI 문서에 반영 | `driving-situation-alert/04_SW_Implementation.md` | Ready for Docs -> Docs Updated | Docs | (this commit) |
| TSB-007 | 2026-03-08 | ETH Backbone 보강 프레임 3건의 소유권/운반 해석 근거를 통신·ID 정책 문서에 반영 | `driving-situation-alert/0303_Communication_Specification.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` | Ready for Docs -> Docs Updated | Docs | (this commit) |
| TSB-008 | 2026-03-08 | Dev2 검증 배치 실행/리포트 포맷 정책을 05/06/07 작성 원칙에 연결 | `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md` | Ready for Docs -> Docs Updated | Docs | (this commit) |
| TSB-009 | 2026-03-08 | 인터페이스/멀티버스/CLI 운영 해석을 공통 언어로 정리하고 예외 범위를 명시 | `driving-situation-alert/tmp/change-orders/TEAM_SYNC_BOARD.md` | Ready for Docs -> Docs Updated | Docs | (this commit) |
| TSB-011 | 2026-03-08 | 멘토 D11 원문과 AUTOSAR/00e 기준을 교차검증해 ECU 명명 운영 결론을 확정 | `docs/meeting-notes/MET_41_2026.03.07.txt`, `driving-situation-alert/00e_ECU_Naming_Standard.md`, `reference/standards/AUTOSAR_CP_TR_SWCModelingGuide.pdf` | Proposed -> Ready for Docs | Dev1 | working note |
| TSB-004 | 2026-03-08 | 공식 CANoe Test PoC 범위를 대표 2건으로 고정하고 Dev1/Dev2/Docs 역할을 분리 | `canoe/docs/operations/verification/CANOE_TEST_POC_SCOPE_2026-03-08.md`, `driving-situation-alert/tmp/change-orders/DEV1_CANOE_TEST_DOC_IMPACT_2026-03-08.md` | Proposed -> In Progress | Dev1 | planning note |
| TSB-004 | 2026-03-08 | Dev1이 CANoe native Test Unit source/yaml 2건과 실행 runbook 초안을 작성 | `canoe/tests/modules/test_units/TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED/*`, `canoe/tests/modules/test_units/TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY/*`, `canoe/docs/operations/verification/CANOE_TEST_UNIT_RUNBOOK.md` | In Progress -> In Progress | Dev1 | source scaffolded |
| TSB-XXX | YYYY-MM-DD |  |  | Proposed -> In Progress -> Ready for Docs -> Docs Updated -> Done |  |  |

## 합의 메모
- 본 보드는 전달용 단일 창구다.
- 상세 설계/정책 SoT는 기존 정식 문서(00~07, 운영 계약서)를 따른다.

## 문서팀 전달사항 (2026-03-08)
- TSB-001 문서 반영 요청은 반영 완료되었으며, 정책 문구는 `0302/0303`에 고정했다.
1. 일반 노드는 단일 버스 상주를 기본으로 한다.
2. 게이트웨이 노드는 다중 버스 상주를 허용한다.
3. 테스터 노드는 예외적으로 멀티버스 구성이 가능하나, 기본 권고는 버스별 분리다.
4. ECU 명명은 `3글자 강제`가 아니라 `짧고 눈에 잘 띄는 약어 권장`으로 해석한다.
5. `_TX/_RX` 접미사는 구현/하위 매핑표에서는 허용하되, 상위 체인 문서 본문/표면 표기에서는 논리명(`EMS_ALERT`) 우선으로 정리한다.
6. `00e`는 Canonical(`UPPER_SNAKE_CASE`)과 AUTOSAR shortName(`UpperCamelCase`)를 분리 유지하고, shortName 제약(영문, 1..128, namespace unique, underscore 금지)은 유지한다.

## ECU 명명 정책 메모 (2026-03-08)
- 멘토 D11 원문: `가급적이면 영어 세 자`, `너무 길게 쓰지 말고`, `상관은 없는데 세자가 눈에 잘 띈다`.
- 해석: 하드 룰이 아니라 가독성 중심 `Should` 권고다.
- AUTOSAR 근거: shortName은 영문 기반, 1..128자, namespace unique이며 underscore를 쓰지 않는다. `3글자` 요구는 없다.
- 현재 SoT(`00e`)는 유지 가능하다. Canonical은 약어형 `UPPER_SNAKE_CASE`, AUTOSAR 모델명은 별도 shortName으로 분리한다.
- 문서 후속 요청:
  1. `0302_NWflowDef.md` 상단 노드 열/주석에서 `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`의 전면 노출을 줄이고 `EMS_ALERT` 논리명 우선으로 정리
  2. `0303_Communication_Specification.md` Comm 설명의 `EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx)` 표현을 논리 단말 중심으로 축약
  3. `00e_ECU_Naming_Standard.md`는 현행 유지. 다만 `상위 체인 문서=논리명`, `04/보강표/코드=내부 모듈명 허용` 경계를 한 줄 더 명시하면 좋음

## 확장 설계 의사결정안 v1 (Dev1/Dev2/Docs 공통)

### 목표
- 멘토 피드백과 CANoe 운영 BP를 동시에 만족하는 테스트 하네스 구조로 고정한다.
- 원칙: 일반 노드 단일버스, GW 다중버스, 검증 하네스는 `도메인 분리 + E2E 예외` 2계층.

### 설계 원칙 (결정안)
1. 도메인 하네스(기본): 각 도메인 버스에 단일버스 검증 노드를 배치한다.
2. E2E 하네스(예외): `VAL_SCENARIO_CTRL` 1개만 멀티버스로 유지해 시스템 통합 시나리오를 수행한다.
3. GW 경계 검증: 도메인간 전달 검증은 GW 경유 경로에서만 판정한다(직결 판정 금지).
4. 산출물 표준: Dev2 결과는 `JSON+MD`를 기본으로 하고 `CSV`는 선택 출력으로 유지한다.

### 문서 반영 요청 (Docs)
- `0302_NWflowDef.md`: 하네스 2계층(도메인/통합)과 GW 경유 판정 규칙 명시
- `0303_Communication_Specification.md`: 테스트 메시지 소유권/버스 할당 원칙(도메인 단일, E2E 예외) 명시
- `0304_System_Variables.md`: 도메인 하네스 변수와 E2E 전용 변수 구분 주석 추가
- `05/06/07`: 케이스를 `Domain UT/IT` vs `E2E ST`로 구분해 Pass/Fail 증빙 축 정리

### 적용 판정
- 본 결정안은 구현 강제 전, 문서팀 반영 후 `TSB-001`/`TSB-005` 체인에 따라 단계 적용한다.

### 용어/구조 해석 정렬 (2026-03-08 확정)
- 인터페이스는 도메인 이름 자체가 아니라 노드/도메인 사이의 메시지 계약 단위로 해석한다.
- 메시지 계약 항목은 최소 `Message Name`, `ID`, `DLC`, `주기/이벤트`, `Timeout`, `Owner`를 포함한다.
- 멀티버스 기본 정책은 유지한다: 일반 노드 단일 버스, GW/경계 노드 다중 버스 허용, 테스트 노드는 예외 허용.
- 테스트 구조는 2계층으로 고정한다: 도메인 검증은 버스별 분리 기본, E2E 통합 검증만 `VAL_SCENARIO_CTRL` 멀티버스 예외를 사용한다.
- 하네스 노드 분리 고정: `VAL_SCENARIO_CTRL`는 멀티버스 E2E 오케스트레이션 노드, `VAL_BASELINE_CTRL`는 Chassis 단일버스 baseline 결과 집계 노드다.
- 도메인 간 전달 판정은 GW 경유 경로에서만 수행하며 직결 판정은 금지한다.

### Dev2 CLI 구조 정리 (현재 기준)
1. 단일 엔트리: `python scripts/run.py` (`sdv` 별칭 포함).
2. `verify batch --phase pre`: 게이트 실행 + `verify prepare/smoke/status`.
3. `verify batch --phase post`: `verify finalize` + `verify status`.
4. 리포트 정책: `JSON+MD` 기본, `CSV` 선택 출력.
5. CLI 역할은 검증 오케스트레이션/증빙 수집이며, 네트워크 토폴로지 변경 자체는 범위 밖이다.

## Dev1 Follow-up (2026-03-08)
- TSB-010: Comm_106/Flow_106 baseline result owner 단일화 완료.
- Code decision: `frmTestResultMsg (0x2A5)` owner는 `VAL_SCENARIO_CTRL`, `frmBaseTestResultMsg (0x2A6)` owner는 `VAL_BASELINE_CTRL`로 고정.
- Docs request: `0302_NWflowDef.md`, `0303_Communication_Specification.md`에서 `Comm_106`/`Flow_106` 문구를 `VAL_SCENARIO_CTRL -> frmTestResultMsg(0x2A5) -> VAL_BASELINE_CTRL -> frmBaseTestResultMsg(0x2A6)` 체인으로 수정.
- Evidence: `canoe/src/capl/input/VAL_SCENARIO_CTRL.can`, `canoe/cfg/channel_assign/ETH_Backbone/VAL_SCENARIO_CTRL.can`, `canoe/src/capl/ecu/VAL_BASELINE_CTRL.can`, `python scripts/gates/check_capl_sync.py` PASS.

## Dev1 -> Docs Batch Handoff (2026-03-08)
- handoff file: `driving-situation-alert/tmp/change-orders/DEV1_TO_DOC_BATCH_2026-03-08.md`
- scope: `DSR-001~005`
- current runtime status: current SIL baseline has no additional must-do code fix remaining for Dev1
- accepted backlog: `A-002`, `A-005`
- dependency: `M40-18` closure still waits on Dev2 evidence and docs-team updates in `05/06/07`
