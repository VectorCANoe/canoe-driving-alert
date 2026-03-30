# Vehicle ECU Architecture and Interaction Reference

## 목적

본 문서는 CANoe SIL 기준 차량 ECU 구조와 ECU 간 상호작용을 제3자 관점에서 빠르게 이해하기 위한 공식 architecture reference 패키지를 설명한다.

이 reference는 다음 질문에 답하도록 구성된다.

- 전체 ECU 표면은 어떻게 묶여 있는가
- 어떤 행동 흐름이 여러 ECU를 가로지르는가
- 특정 ECU는 어떤 역할과 계약으로 동작하는가
- exact message, owner seam, linked sysvar는 어디에서 확인하는가

## 공식 기준 자산

- `canoe/docs/architecture/master_book/ECU_METADATA_BOOK_2026-03-28.pdf`
- `canoe/docs/architecture/master_book/README.md`
- `canoe/docs/architecture/master_book/ECU_GROUP_NETWORK_VIEW_2026-03-28.md`
- `canoe/docs/architecture/master_book/ACTION_FLOW_INDEX_2026-03-28.md`
- `canoe/docs/architecture/master_book/ECU_ACTION_FLOW_MATRIX_2026-03-28.md`
- `canoe/docs/architecture/master_book/ECU_CARD_INDEX_2026-03-28.md`
- `canoe/docs/architecture/master_book/SIGNAL_FLOW_INDEX_2026-03-28.md`

## 읽는 순서

1. `Visual Opening`
   - 전체 101 ECU surface를 먼저 본다.
2. `Group Snapshot`
   - 어떤 ECU가 같은 vehicle story 안에서 함께 움직이는지 본다.
3. `Action-Flow Pack`
   - 행동 기준 canonical flow를 먼저 이해한다.
4. `ECU Catalog`
   - 각 ECU의 역할과 실제 contract를 본다.
5. `Signal Flow Index`
   - exact runtime name과 per-signal route가 필요할 때만 내려간다.

## ECU 카드 해석

- `P1 Overview`
  - 구조 요약
  - inbound / outbound 방향
  - representative signal path
  - domain footprint
- `P2 Reference`
  - exact Rx / Tx inventory
  - owner seam
  - linked sysvar
  - lead test asset
  - full linked ECU bank
- `P3 / P4`
  - dense ECU에서만 추가되는 overflow inventory page

## 인덱스 사용 규칙

- `Action Flow Index`
  - canonical behavior chapter를 찾을 때 사용한다.
- `ECU to Flow Matrix`
  - 한 ECU를 primary/supporting flow로 연결할 때 사용한다.
- `ECU Card Index`
  - 특정 ECU의 `p1/p2/p3/p4` 페이지를 바로 찾을 때 사용한다.
- `Signal Flow Index`
  - exact signal name, route, appendix drill-down이 필요할 때만 사용한다.

## Appendix 사용 원칙

- 본 architecture reference는 supplementary appendix를 보강하는 공식 읽기 레이어다.
- 논문 본문이나 발표 자료에서는 핵심 그림과 핵심 ECU만 선별해 사용한다.
- 상세한 exact contract와 per-signal route는 appendix나 별도 reference PDF에서 확인한다.
