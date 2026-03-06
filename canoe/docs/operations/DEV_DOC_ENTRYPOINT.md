# 개발팀 문서 진입 인덱스 (화이트리스트)

## 목적
- 문서팀 폴더 구조를 변경하지 않고 개발 실행 안정성을 유지한다.
- `driving-situation-alert/tmp` 탐색 노이즈를 줄인다.
- 개발팀 문서 탐색 시작점을 이 파일 하나로 고정한다.

## 운영 원칙
- 개발팀은 `driving-situation-alert` 하위 파일 이동/개편을 수행하지 않는다.
- 명시된 화이트리스트 외 경로는 작업 필요 시에만 읽는다.

## 1차 SoT (읽기 순서)
1. `driving-situation-alert/TMP_HANDOFF.md`
2. `driving-situation-alert/01_Requirements.md`
3. `driving-situation-alert/03_Function_definition.md`
4. `driving-situation-alert/0301_SysFuncAnalysis.md`
5. `driving-situation-alert/0302_NWflowDef.md`
6. `driving-situation-alert/0303_Communication_Specification.md`
7. `driving-situation-alert/0304_System_Variables.md`
8. `driving-situation-alert/04_SW_Implementation.md`
9. `driving-situation-alert/05_Unit_Test.md`
10. `driving-situation-alert/06_Integration_Test.md`
11. `driving-situation-alert/07_System_Test.md`

## 2차 범위 (필요 시만)
- 변경지시서 전용:
  - `driving-situation-alert/tmp/change-orders/`
- 멘토링 체크리스트:
  - `driving-situation-alert/tmp/mentoring/Mentoring_MET40.md`

## 기본 탐색 제외 경로 (기본 미탐색)
- `driving-situation-alert/tmp/reference-*`
- `driving-situation-alert/tmp/archive/`
- `driving-situation-alert/tmp/onboarding/`
- `driving-situation-alert/tmp/vector_sample/`
- SoT/변경지시서에서 직접 참조하지 않는 대용량 asset/raw 폴더

## 개발 실행 체크리스트
1. `TMP_HANDOFF.md`의 freshness 상태(`FRESH`/`STALE`)를 먼저 확인한다.
2. `FRESH`면 handoff-first 방식으로 실행한다.
3. `STALE`이면 canonical 체인으로 실행한다.
   - `01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`
4. 구현 변경 시 추적 체인을 반드시 유지한다.
   - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
5. 팀 운영 방식이 바뀌면 `canoe/docs/operations` 인덱스를 즉시 갱신한다.

## 소유권
- 문서팀 소유:
  - `driving-situation-alert` 구조 및 본문 내용
- 개발팀 소유:
  - `canoe/docs/operations`의 진입 인덱스 및 운영 가이드
