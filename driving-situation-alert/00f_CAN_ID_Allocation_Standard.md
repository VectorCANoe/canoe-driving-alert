# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 4.5  
**Date**: 2026-03-09  
**Status**: Draft (Policy SoT, Under Refactor)  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

## 1. 목적

- 본 문서는 특정 시나리오가 아니라 **완성차 전체 시스템 관점**에서 CAN ID 배정 규칙을 정의한다.
- 도메인/게이트웨이 구조를 유지하면서, 중장기 확장을 위해 29-bit 정책을 기본으로 사용한다.
- 문서/DBC/CAPL/테스트가 동일한 ID 거버넌스를 따르도록 단일 기준을 제공한다.

---

## 2. 설계 철학 (OEM 관점)

핵심 원칙 3가지:

1. **중재 우선순위 분리**: 버스 중재 우선순위(Tier)와 기능 의미를 혼동하지 않는다.
2. **소유권 고정**: 메시지 Block은 경로가 아니라 Owner ECU 도메인으로 고정한다.
3. **확장 우선**: Slot 공간을 크게 확보해 재할당 비용을 줄인다.

이 구조의 의미:

- `Tier`: 얼마나 지연에 민감한가
- `Block`: 어느 도메인이 책임지는가
- `Slot`: 해당 도메인 내에서 어떤 메시지인가

---

## 3. 정책 결정 (고정)

### 3.1 Primary / Compatibility

- Primary Policy: CAN Extended 29-bit
- Compatibility Policy: CAN Standard 11-bit (현 SIL 실행 호환)

### 3.2 Primary 스키마 (29-bit, 3분할)

- `[28:26]` Tier (3bit)
- `[25:21]` Block (5bit)
- `[20:0]` Slot (21bit)

계산식:

`EXT_ID = (Tier << 26) | (Block << 21) | Slot`

---

## 4. Tier 규칙 (OEM Latency Class)

| Tier | OEM Class | 통신 지연 목표(권고) | 적용 기준 (간단 판단) |
|---|---|---|---|
| 0 | Motion Control | 5~10 ms | 제동/조향/동력 등 차량 거동을 즉시 바꾸는 제어 명령 |
| 1 | Safety State | 10~20 ms | 제어/안전 판단에 직접 쓰이는 입력 상태(속도/조향/객체/구간) |
| 2 | Coordination & Fail-safe | 20~50 ms | 도메인 간 조정, 경보 판정 결과, 강등/복구 트리거 |
| 3 | Driver Info & Comfort | 50~100 ms | 클러스터/앰비언트/음향/편의 출력 |
| 4 | Validation & Diagnostic | Event/On-demand | 검증 하네스, 진단, 시험/정비 전용 트래픽 |
| 5~7 | Reserved | N/A | 향후 확장 |

Tier 판정 규칙:

- Tier 숫자가 작을수록 CAN arbitration 우선순위가 높다.
- Tier는 기능명 기준이 아니라 **지연 허용도(latency class)** 기준으로 배정한다.
- 동일 기능이라도 지연 목표가 다르면 Tier를 분리할 수 있다.
- 서비스 우선순위(예: 경보 우선순위 판정)는 애플리케이션 로직으로 별도 처리한다.

---

## 5. Block 규칙 (도메인 소유권)

| Block | Domain | Owner 예시 |
|---|---|---|
| 0x01 | CHASSIS | CHS_GW, BRK_CTRL, STEER_CTRL |
| 0x02 | BODY | BODY_GW, AMBIENT_CTRL, HAZARD_CTRL |
| 0x03 | INFOTAINMENT/CLUSTER | IVI_GW, NAV_CTX_MGR, CLU_* |
| 0x04 | POWERTRAIN | ENG_CTRL, TCM |
| 0x05 | ADAS | ADAS_WARN_CTRL, WARN_ARB_MGR |
| 0x06 | BACKBONE/GATEWAY | DOMAIN_BOUNDARY_MGR, ETH_SW, DOMAIN_ROUTER |
| 0x07 | VALIDATION/DIAG | VAL_SCENARIO_CTRL, VAL_BASELINE_CTRL |
| 0x08 | V2X/EXTERNAL | EMS_* (V2X ingress/egress), 외부 연계 |
| 0x09 | HVAC/ENERGY (Reserved Active) | HVAC/열관리/에너지 확장용 |
| 0x1F | RESERVED | 사용 금지 |

Block 판정 규칙:

- Block은 메시지 생성 주체(Owner ECU) 도메인으로 지정한다.
- GW를 경유해도 Block은 Owner 기준을 유지한다.
- Block 번호 크고 작음은 우선순위 의미가 없다.

---

## 6. Slot 규칙 (21bit 확장 영역)

- 범위: `0x000000 ~ 0x1FFFFF`
- 동일 `(Tier, Block, Slot)` 조합 중복 금지
- 같은 `Tier+Block` 조합 내에서는 Slot 1-up 증가를 기본으로 사용
- `0x1FF000 ~ 0x1FFFFF`는 예약(운영/실험 직접 사용 금지)

선택 프로파일(운영 편의):

- 필요 시 `Slot[20:16]`을 ClassPage, `Slot[15:0]`을 Sequence로 사용 가능
- 단, 이는 운영 편의 옵션이며 상위 정책은 `3/5/21`로 고정

---

## 7. 배정 절차 (실무)

1. Tier 결정: 지연 허용도 기준 분류
2. Block 결정: Owner ECU 도메인 지정
3. Slot 할당: 동일 Tier+Block 내 연번 배정
4. 충돌 점검: 기존 DBC/예약 구간 중복 확인
5. 동기화: `0303 -> DBC/CAPL -> 05/06/07` 같은 사이클로 반영

---

## 8. 11-bit 호환 정책

- 현재 SIL 실행 ID는 컷오버 전까지 유지 가능
- 신규/변경 메시지의 정책 승인 기준은 29-bit를 우선 적용
- 11-bit 값은 Compatibility Mapping 용도로만 관리
- `0x000~0x0FF` 신규 할당 금지

---

## 9. 샘플 (정책 이해용)

| 항목 | Tier | Block | Slot | EXT_ID |
|---|---:|---:|---:|---|
| Vehicle State Input | 1 | 0x01 | 0x000001 | `0x04200001` |
| Navigation Context Input | 1 | 0x03 | 0x000003 | `0x04600003` |
| Alert Decision Output | 2 | 0x05 | 0x000006 | `0x08A00006` |
| Cluster Warning Output | 3 | 0x03 | 0x000008 | `0x0C600008` |
| Validation Result | 4 | 0x07 | 0x000009 | `0x10E00009` |

---

## 10. SoT 우선순위

- 정책 SoT: `00f_CAN_ID_Allocation_Standard.md`
- 통신 계약 SoT: `0303_Communication_Specification.md`
- 실행 SoT: `canoe/databases/*.dbc`, `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- 운영 보드: `tmp/change-orders/TEAM_SYNC_BOARD.md`

---

## 11. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.5 | 2026-03-09 | Tier를 OEM latency class 기준(Motion Control/Safety State/Coordination/Driver Info/Validation)으로 재정의하고 권고 지연 목표를 추가해 배정 기준을 명확화. |
| 4.4 | 2026-03-09 | OEM 시스템 관점으로 전면 재구성: Tier/Block/Slot 철학을 단순화하고, Tier를 입력->판정/조정->출력 흐름으로 재정의. Block에 V2X/HVAC 확장 도메인 추가. |
| 4.3 | 2026-03-09 | Tier 순서를 데이터 경로(입력 -> 판정/Fail-safe -> HMI) 기준으로 재정렬. 샘플 Target EXT_ID 재계산. |
| 4.2 | 2026-03-09 | Tier/Block 빠른 판단 기준, Owner 기반 Block 선택 원칙, 3단계 배정 절차, 체크리스트 추가. |
| 4.1 | 2026-03-09 | Primary를 29-bit `3/5/21`로 단순화. |
