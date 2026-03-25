# test_units 한글 가이드

원문:
- [README.md](./README.md)

동기화 기준:
- `5d83ee7f`
- native asset 폴더 이름, testcase ID, scenario 번호는 canonical technical identifier로 유지합니다.

## 목적

이 문서는 현재 SIL cycle에서 사용하는 native CANoe Test Unit 자산 구조와 운영 규칙을 한국어로 설명합니다.

## 현재 구조

- 공용 harness 세트
  - `TEST_SCN`
  - `TEST_BAS`
  - `common/ValidationHarnessTestCommon.cin`
- active baseline 자산은 `TC_CANOE_UT_*`, `TC_CANOE_IT_*`, `TC_CANOE_ST_*` 계열로 구성합니다.
- active level suite는 sibling path인 `../test_suites/`에서 관리합니다.
- retire 대상 draft skeleton은 `retire/` 아래로 분리합니다.

## Ownership split

- Dev2
  - testcase portfolio
  - oracle / timing / evidence blueprint
  - skeleton `.can/.vtestunit.yaml/.vtesttree.yaml`
- Dev1
  - common harness
  - concrete signal/message/assert hookup
  - CANoe GUI 등록
  - native `.vtestreport`

## 실행 상태 해석

- anchor asset은 실제 실행 가능한 자산으로 봅니다.
- diagnostic-linked skeleton asset은 아직 공식 PASS target이 아닐 수 있습니다.
- skeleton asset은 concrete stimulus/oracle wiring이 완료되기 전까지 `oracle-hook` 수준에서 멈출 수 있습니다.

## 파일 형식

- `*.can`
  - CAPL `export testcase` 구현 또는 draft skeleton
- `*.vtestunit.yaml`
  - CANoe Test Unit descriptor
- `*.vtesttree.yaml`
  - test tree / fixture mapping

## GUI 등록 규칙

1. active CANoe configuration을 GUI에서 엽니다.
2. `*.can`을 직접 넣지 말고 `*.vtestunit.yaml` descriptor를 등록합니다.
3. bulk import는 `assign/UT_ACTIVE_BASELINE`, `assign/IT_ACTIVE_BASELINE`, `assign/ST_ACTIVE_BASELINE`, `assign/FULL_ACTIVE_BASELINE`를 사용합니다.
4. wrapper filename은 GUI import ordering을 위해 ID-first 규칙을 유지합니다.
5. `test_suites/TS_*/*.vtestunit.yaml`은 repository suite manifest이며, GUI direct import 파일이 아닙니다.
6. active suite에는 executable asset만 활성화합니다.
7. `.cfg` 저장은 GUI에서만 수행합니다.

## Evidence

- native CANoe test report (`.vtestreport`)
- 실행 screenshot
- measurement log / run-id binding
- 필요 시 Dev2 TUI/CLI에서 후처리 packaging

## 현재 읽을 때 주의할 점

- wave별 asset 상태와 direct-output / gateway / diagnostic 확장 상태는 원문 README가 더 상세합니다.
- 한국어 가이드는 현재 구조, ownership split, GUI 등록 규칙, evidence 규칙을 빠르게 읽기 위한 mirror입니다.
- exact asset list와 최신 scenario binding은 항상 원문 README를 우선합니다.
