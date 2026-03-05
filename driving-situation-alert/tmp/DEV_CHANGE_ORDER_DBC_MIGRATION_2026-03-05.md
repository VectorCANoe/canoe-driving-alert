# 개발팀 변경지시서: Validation DBC 통합 이관

문서 ID: DEV-CO-DBC-20260305  
작성일: 2026-03-05  
작성 주체: 문서작성팀  
대상: CANoe 개발팀

## 1. 목적

- `test_can.dbc` 기반 Validation 프레임 운용을 도메인 DBC 구조로 통합해 명명 혼선을 제거한다.
- 검증 하네스 성격은 유지하되, 제출/설명 시 교과서적 도메인 구조로 정렬한다.

## 2. 배경

- 현재 `frmTestResultMsg(0x230)`, `frmBaseTestResultMsg(0x231)`는 `test_can.dbc`에 존재한다.
- 해당 구조는 실행상 유효하나, 명칭 오해 가능성이 높아 개발/감사 설명 일관성 개선이 필요하다.
- 본 변경은 기능 추가가 아니라 DBC 구조/명명 정리다.

## 3. 변경 범위 (In Scope)

1. DBC 구조 변경
- `canoe/databases/test_can.dbc`의 Validation 프레임(`0x230`, `0x231`)을 도메인 DBC로 이관한다.
- 기본 권장 대상: `canoe/databases/chassis_can.dbc`
- 결과적으로 활성 DBC 집합에서 `test_can.dbc` 의존을 제거한다.

2. 노드(ECU) 명칭 정리
- 기존 Validation 전용 노드명:
  - `SIL_TEST_CTRL`
  - `VEHICLE_BASE_TEST_CTRL`
- 신규 명칭(권장):
  - `VAL_SCENARIO_CTRL`
  - `VAL_BASELINE_CTRL`
- CAPL, DBC, 문서, 매트릭스에서 동일 명칭으로 일괄 정합한다.

3. 참조 정리
- CANoe 설정(`cfg`)의 `test_can.dbc` 참조 제거 및 이관 DBC 참조 반영
- CAPL 송수신 메시지 타입/노드명 참조 일괄 반영
- 운영 문서의 DBC Ownership/SoT 표기 정합

## 4. 변경 제외 (Out of Scope)

- 경고 로직/우선순위 정책/ETA 규칙 등 기능 동작 변경
- Ethernet 계약 체계 변경
- 시나리오 정의 자체(케이스 추가/삭제)

## 5. 구현 지시 상세

1. 메시지 이관
- `frmTestResultMsg` (`0x230`, DLC=1)
- `frmBaseTestResultMsg` (`0x231`, DLC=8)
- 기존 Signal 정의/bit layout/값 범위/VAL table 불변 유지

2. CAPL 연계 유지
- 시나리오 결과 출력 경로 유지
- 베이스 시나리오 집계 출력 경로 유지
- 송신 Trigger(Event) 및 로그 포맷 의미 변경 금지

3. 설정/운영 파일 정합
- DBC ownership 문서의 소유 DBC명 업데이트
- `test_can.dbc` 참조 남아있는 경로 0건 보장

## 6. 수용 기준 (Acceptance Criteria)

1. 동작 동일성
- 기존 SIL 시나리오 실행 결과(Pass/Fail)가 변경 전과 동일
- `0x230`, `0x231` 출력 타이밍/값 의미 동일

2. 정합성
- 활성 경로 기준 `test_can.dbc` 참조 0건
- DBC/CFG/CAPL/문서 간 노드명 불일치 0건

3. 추적성
- Req/Func/Flow/Comm/Var/Test 체인에서 Validation 항목 참조 끊김 0건

## 7. 개발팀 산출물 요청

1. 변경 파일 목록(최종 경로)
2. 이관 전/후 메시지 정의 비교표 (`0x230`, `0x231`)
3. 시나리오 회귀 결과 요약(핵심 케이스)
4. 잔여 리스크 및 롤백 방법

## 8. 전달 메모

- 본 지시는 "Validation-only 경로를 제거"하는 지시가 아니다.
- 본 지시는 "Validation 프레임을 도메인 DBC 체계로 통합 정리"하는 지시다.
