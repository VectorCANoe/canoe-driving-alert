# 개발팀 변경지시서: CAN ID 3/3/5 전면 재할당

문서 ID: DEV-CO-CANID-335-20260305  
작성일: 2026-03-05  
작성 주체: 문서작성팀  
대상: CANoe 개발팀

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

## 3. 현재 기준(전환 전)

- 활성 DBC: `adas/body/chassis/eth_stub/infotainment/powertrain`
- 메시지 수: `98`
- ID 범위: `0x064 ~ 0x315`
- 중복: 0건

## 4. 필수 수행 항목

1. `Old ID -> New ID` 매핑표 98건 작성/확정  
2. 활성 DBC 6종 `BO_` ID 전량 교체  
3. CAPL/panel/sysvar/log raw ID 상수 전수 교체  
4. 문서 체인 동시 반영:
   - `0302`, `0303`, `0304`, `04`, `05`, `06`, `07`
5. 회귀 검증:
   - ID 중복 0건
   - Old ID 잔존 참조 0건
   - SIL 시나리오 결과 동등

## 5. 수용 기준 (Acceptance)

1. 정책 정합성
- 모든 활성 ID가 `3/3/5` 해석 가능
- Tier/Group/Index 규칙 위반 0건

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

## 7. 비고

- 본 지시는 기능 추가가 아니라 ID 스키마 전면 재정렬이다.
- `canoe/cfg` 변경은 GUI-first 운영 원칙에 따라 개발팀에서 수행한다.
