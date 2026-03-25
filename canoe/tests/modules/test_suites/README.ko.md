# Test Suites 한글 가이드

원문:
- [README.md](./README.md)

동기화 기준:
- `5d83ee7f`
- suite 이름과 asset count는 canonical 원문 기준으로 해석합니다.

## Active suite 정책

- level suite는 현재 non-retired `TC_CANOE_UT_*`, `TC_CANOE_IT_*`, `TC_CANOE_ST_*` 자산으로 구성합니다.
- `retire/` 자산은 suite에서 제외합니다.
- suite composition은 historical umbrella ID가 아니라 active executable asset을 기준으로 합니다.

## 현재 제공 suite

- `TS_CANOE_UT_ACTIVE_BASELINE`
- `TS_CANOE_IT_ACTIVE_BASELINE`
- `TS_CANOE_ST_ACTIVE_BASELINE`
- `TS_CANOE_FULL_ACTIVE_BASELINE`

## 해석 규칙

- `UT`, `IT`, `ST`는 공식 closeout tier입니다.
- `FULL`은 active baseline wrapper이지만 closeout official tier는 아닙니다.
- 최신 count와 wrapper 구성은 원문 README를 우선합니다.
