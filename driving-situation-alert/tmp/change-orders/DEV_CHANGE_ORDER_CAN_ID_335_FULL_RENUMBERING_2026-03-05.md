# 개발팀 변경지시서: CAN ID 3/3/5 전면 재할당

문서 ID: DEV-CO-CANID-335-20260305  
작성일: 2026-03-05  
작성 주체: 문서작성팀  
대상: CANoe 개발팀

## 0. 실행 우선순위 (필수 고정)

본 변경은 아래 순서를 반드시 지킨다.

1. 도메인/게이트웨이 구조 유지(Ownership/경계 불변)
2. 메시지 우선순위 기반 ID 정책 확정(Tier/Group)
3. 매핑 매트릭스 + 승인 게이트 기반 변경 통제(G1~G4)
4. 위 1~3이 확정된 뒤 `3/3/5` 전면 재할당 실행

즉, `3/3/5`는 단독 목표가 아니라 상위 3개 원칙을 구현하는 수단이다.

## 1. 목적

- 현행 도메인 블록 대역형 ID 정책을 종료하고, 11-bit `3/3/5` 인코딩으로 전면 전환한다.
- 문서/DBC/CAPL/테스트의 ID 체계를 단일 규칙으로 정렬한다.

## 2. 고정 정책

- 인코딩:
  - `[10:8]` Tier(3bit)
  - `[7:5]` Group(3bit)
  - `[4:0]` Index(5bit)
- 계산식:
  - `ID = (Tier << 8) | (Group << 5) | Index`
- 전환 방식:
  - Full Renumbering only
  - 기존 ID와 신 ID 공존 금지

## 2.1 배정 의사결정 우선순위 (Normative)

- ID 배정 의사결정은 아래 우선순위를 따른다.
  1. Owner/도메인 경계
  2. 안전/검증 경로(Fail-safe/Validation 영향)
  3. Tier/Group/Index 인코딩 규칙
- `Group`은 단독 최상위 기준이 아니며, 1/2번 조건을 만족한 뒤 분류/정렬 축으로 적용한다.

## 2.2 버스중재 vs 기능중재 경계 (Normative)

- 버스중재(CAN 컨트롤러/프로토콜 레벨):
  - 전송 우선순위는 CAN Identifier 값으로만 결정한다.
  - payload 신호/비트필드는 버스중재 순서에 영향을 주지 않는다.
  - 본 변경의 버스 우선순위 해석은 `Tier -> Group -> Index` 순서를 따른다.
- 기능중재(소프트웨어 로직 레벨):
  - 경고/감속보조/Fail-safe 판단은 payload 신호, 타이머, 상태 로직으로 처리한다.
  - 기능중재는 기능 상태/출력을 바꿀 수 있으나 버스중재 순서를 재정의해서는 안 된다.
- 일관성 규칙:
  - 안전 핵심 경로는 기능 긴급도와 버스 우선순위 배정을 동시에 만족해야 한다.
  - 불일치 시 Annex A 및 게이트 심사(G1~G4)에서 ID 매핑을 수정한다.

## 3. 현재 기준(전환 전)

- 활성 DBC: `adas/body/chassis/eth_stub/infotainment/powertrain`
- 메시지 수: `98`
- ID 범위(신규 3/3/5 배치 결과): `0x100 ~ 0x2AA`
- Old baseline 참고 범위(전환 전): `0x064 ~ 0x315`
- 중복: 0건

## 4. 필수 수행 항목

1. Annex A 파일(`driving-situation-alert/tmp/ID_335_AnnexA_Mapping_98_Template.csv`)에 `Old -> New` 98건 작성/확정  
2. 활성 DBC 6종 `BO_` ID 전량 교체  
3. CAPL/panel/sysvar/log raw ID 상수 전수 교체  
4. 문서 체인 동시 반영:
   - `0302`, `0303`, `0304`, `04`, `05`, `06`, `07`
5. 회귀 검증:
   - ID 중복 0건
   - Old ID 잔존 참조 0건
   - SIL 시나리오 결과 동등
6. 승인 게이트 준수:
   - G1 Mapping Freeze
   - G2 Implementation Freeze
   - G3 Cutover Approval
   - G4 Post-Cutover Audit

## 5. 수용 기준 (Acceptance)

1. 정책 정합성
- 모든 활성 ID가 `3/3/5` 해석 가능
- Tier/Group/Index 규칙 위반 0건
- Tier 우선순위 역전 0건(핵심 제어 프레임의 저우선 Tier 배치 금지)

2. 기능 동등성
- 기존 시나리오 Pass/Fail 결과 동등
- 타이밍/중재/해제 동작 동등

3. 추적성
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 단절 0건

## 6. 개발팀 제출물

1. 98건 전량 매핑표(Old/New/Tier/Group/Index/근거)
2. DBC 변경 diff 및 충돌 검사 결과
3. CAPL/panel/sysvar/log 변경 파일 목록
4. 회귀 결과 요약(핵심 시나리오, 실패/리스크 포함)
5. Gate 승인 증빙(G1~G4) 및 승인자/승인일

## 7. Cutover/Rollback 규칙

0. 롤백 기준점(개발팀 확정)
- 백업 브랜치: `backup/rollback-20260305-160559`
- 원격 브랜치: `origin/backup/rollback-20260305-160559`
- 기준 커밋: `71d4402`

1. Cutover 전
- Annex A 98건 `Approved` 완료
- 충돌 검사 0건, 핵심 시나리오 PASS

2. Rollback 조건
- 충돌 발생
- Tier 우선순위 역전
- 핵심 시나리오 Fail

3. Rollback 방식
- Cutover 직전 Git tag 기준 즉시 복귀
- DBC/CAPL/문서를 동일 커밋 단위로 원복

## 8. 비고

- 본 지시는 기능 추가가 아니라 ID 스키마 전면 재정렬이다.
- `canoe/cfg` 변경은 GUI-first 운영 원칙에 따라 개발팀에서 수행한다.
