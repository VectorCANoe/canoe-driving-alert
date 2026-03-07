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
| TSB-001 | 역할 분리 타당성 점검(멀티버스/GW/테스터) | Dev1 | Dev1 + Docs | In Progress | `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md` | `tmp/mentoring/Mentoring_MET41.md`, 필요 시 `0302/0303` | 진행중 | 멘토 권고: 가능/권고 분리 기록 |
| TSB-002 | Req_151 문구 명확화 (`도메인 헬스/경로 상태`) | Docs | Docs | Docs Updated | `01_Requirements.md` (`Req_151`,`VC_151`) | `01_Requirements.md` + VC 문구 | 반영완료 | 도메인 경계 통신 상태(주기/타임아웃/유효플래그) 기준으로 수정 |
| TSB-003 | Req_017/Req_139 표현 정밀화 | Docs | Docs | Docs Updated | `01_Requirements.md` (`Req_017`,`Req_139`,`VC_139`) | `01_Requirements.md` | 반영완료 | `일반차` 표현 정리 + 우선순위 규칙 문장 명확화 |
| TSB-004 | CANoe 공식 Test Unit PoC 1건 | Dev2 | Dev2 | Proposed | Test Unit 실행 캡처/리포트 | `tmp/mentoring/Mentoring_MET41.md` 체크 갱신 | 대기 | CAPL 하네스는 유지 |
| TSB-005 | M40-18 실행 증빙 폐쇄 | Dev1 + Dev2 | Dev1 + Dev2 + Docs | In Progress | 로그/캡처/리포트 | `05/06/07`, `TMP_HANDOFF.md` | 진행중 | G4 재개 조건 |
| TSB-008 | Dev2 검증 일괄 CLI + 저장포맷 옵션(기본 JSON/MD, CSV 선택) | Dev2 | Dev2 | Ready for Docs | `scripts/run.py` (`verify batch`, `shell /verify batch`), `scripts/README.md`, `canoe/tmp/onboarding/VERIFY_EXECUTION_RUNBOOK.md` | `05/06/07` 실행 증빙 작성 가이드에 연결 | 미반영 | pre/post/full 배치 + `--report-formats` (`json,md` 기본 / `csv` 옵션) |
| TSB-006 | CAPL `timeNow()` overflow-safe 정리 | Dev1 | Dev1 | Ready for Docs | `src/capl/*`, `cfg/channel_assign/*`의 `timeNowInt64()` 전환 + `check_capl_sync` PASS | 필요 시 `0304`, `04` 구현 노트 | 미반영 | 컴파일 경고 `08-0041` 사전 제거 목적 |
| TSB-007 | ETH Backbone DBC 누락 3건 보완 | Dev1 | Dev1 | Ready for Docs | `canoe/databases/eth_backbone_can_stub.dbc` + `multibus-dbc` PASS | `0303`, `00f`(소유권/ID 운영 근거) | 미반영 | `ethVehicleStateMsg`, `ethSteeringMsg`, `ethNavContextMsg` 추가 |

## 업데이트 템플릿

| ID | 날짜 | 변경 요약 | 변경 파일 | 상태 전환 | 담당 | 증빙 링크/커밋 |
|---|---|---|---|---|---|---|
| TSB-XXX | YYYY-MM-DD |  |  | Proposed -> In Progress -> Ready for Docs -> Docs Updated -> Done |  |  |

## 합의 메모
- 본 보드는 전달용 단일 창구다.
- 상세 설계/정책 SoT는 기존 정식 문서(00~07, 운영 계약서)를 따른다.
