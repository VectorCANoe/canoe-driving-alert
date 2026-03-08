# 최종 단계 역할 분리 정리 (2026-03-08)

## 목적

- 개발 막바지 기준으로 Dev1, Dev2, 문서팀의 역할을 다시 분리한다.
- 새 기능 확장보다 `실행 증빙`, `외부 자산화`, `최종 제출 구조`에 집중한다.

## 현재 판단

1. Dev1의 current SIL baseline must-do code fix는 사실상 닫혔다.
2. Dev2는 `SDV Operator` 제품 경계를 기준으로 TUI/CLI, 패키징, CI 브리지를 계속 고도화한다.
3. 문서팀은 전체 체인 재작성보다 `04/05/06/07 + final-docs` 마감이 우선이다.

## 팀별 역할

### Dev1
- `canoe/` runtime baseline 유지
- native CANoe Test Unit PoC 실행 지원
- 재현 가능한 runtime defect만 수정
- 현재 자산:
  - `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
  - `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`

### Dev2
- `product/sdv_operator/` 제품 경계 유지
- TUI/CLI 실행 표면 유지
- `JSON + MD` 기본, `CSV` 선택 출력 유지
- Jenkins/CI 연결 가능한 외부 자산화 진행

### 문서팀
- `04_SW_Implementation.md`
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`
- `tmp/submission/final-docs/`

위 경로 중심으로 실행 증빙과 최종 제출본을 닫는다.

## 최종 단계 순서

1. Dev1 native CANoe Test Unit 결과 확보
2. Dev2 외부 증빙 자산화
3. 문서팀이 `04/05/06/07` 및 `final-docs` 반영
4. 멘토 open item `M40-18`, `M41-10` 상태 갱신

## 고정 규칙

- 새 Req/Func/Flow/Comm/Var 확장 금지
- CANoe runtime 자산과 Dev2 product surface를 혼합하지 않음
- 문서팀은 영향 범위 문서만 수정

## 참고 문서

- `canoe/docs/operations/verification/FINAL_PHASE_EXECUTION_FLOW.md`
- `canoe/docs/operations/verification/CANOE_TEST_UNIT_RUNBOOK.md`
- `product/sdv_operator/README.md`
- `product/sdv_operator/docs/PACKAGING_SCOPE.md`
- `driving-situation-alert/tmp/submission/final-docs/00_FINAL_STRUCTURE_LOCK.md`
