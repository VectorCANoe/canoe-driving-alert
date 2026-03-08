# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 4.1  
**Date**: 2026-03-09  
**Status**: Draft (Policy SoT, Under Refactor)  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

## 1. 목적

- 현재 운영 중인 11-bit 정책(`3/3/5`)을 유지하면서, 확장 대비용 29-bit 정책을 명확히 고정한다.
- 도메인 분리(블록/대역) 체계를 유지하고, 비트필드 해석 규칙을 함께 제공한다.
- 문서/DBC/CAPL/테스트가 동일한 ID 거버넌스를 사용하도록 기준을 단순화한다.

---

## 2. 근거 요약

- MET40: ID 규칙은 팀이 정의 가능하며, 우선순위/도메인/시퀀스 근거를 문서화해야 한다.
- MET41: 11-bit만 고정하기보다 29-bit 확장 논리를 갖추는 편이 방어에 유리하다.
- ISO 11898 관점: CAN 중재는 Identifier 값 기준이며, 비트 분할 방식 자체는 프로젝트 정책이다.
- 업계 관행: 블록/대역 운영 + 비트필드 해석을 병행하는 하이브리드 방식이 일반적이다.

---

## 3. 정책 결정 (고정)

### 3.1 Primary / Compatibility

- Primary Policy: CAN Extended 29-bit
- Compatibility Policy: CAN Standard 11-bit (현 SIL 실행 호환)

### 3.2 Primary 스키마 (29-bit, 3분할)

- `[28:26]` Tier (3bit): 버스 중재 우선순위 대역
- `[25:21]` Block (5bit): 도메인/경계 블록
- `[20:0]` Slot (21bit): 메시지 슬롯

계산식:

`EXT_ID = (Tier << 26) | (Block << 21) | Slot`

핵심 의미:

- `Tier`가 최상위 블록/대역 규칙
- `Block`이 도메인 경계 규칙
- `Slot`이 상세 메시지 확장 영역

---

## 4. Tier/Block 사전

### 4.1 Tier 사전

| Tier | 의미 | 설명 |
|---|---|---|
| 0 | Safety-Critical Control | 즉시 제어/안전 핵심 루프 |
| 1 | Warning & Risk Core | 경보 판정/위험 상태 전파 |
| 2 | HMI/Driver Output | 클러스터/앰비언트/알림 출력 |
| 3 | Baseline Vehicle State | 기본 차량 상태/입력/주행 정보 |
| 4 | Validation/Diag | 검증/진단/시험 프레임 |
| 5~7 | Reserved | 향후 확장 |

### 4.2 Block 사전

| Block | Domain |
|---|---|
| 0x01 | CHASSIS |
| 0x02 | BODY |
| 0x03 | INFOTAINMENT |
| 0x04 | POWERTRAIN |
| 0x05 | ADAS |
| 0x06 | BACKBONE/GATEWAY |
| 0x07 | VALIDATION |
| 0x1F | RESERVED |

---

## 5. Slot 규칙 (21bit)

### 5.1 기본 규칙

- 범위: `0x000000 ~ 0x1FFFFF`
- 동일 `(Tier, Block, Slot)` 조합 중복 금지
- `0x1FF000 ~ 0x1FFFFF`는 Reserved

### 5.2 권고 프로파일 (선택)

- 단순 운영이 필요하면 Slot 내부를 아래처럼 쓸 수 있다.
  - `ClassPage = Slot[20:16]` (5bit)
  - `Seq = Slot[15:0]` (16bit)
- 이 권고 프로파일은 기존 `3/5/5/16` 운영 습관을 보존하기 위한 선택 사항이며, 상위 정책은 여전히 `3/5/21`이다.

권고 ClassPage 예시:

| ClassPage | 의미 |
|---|---|
| 0x00 | GW/Boundary |
| 0x01 | Vehicle State |
| 0x02 | Driver Input |
| 0x03 | Dynamics Control |
| 0x04 | Warning Core |
| 0x05 | HMI Cluster |
| 0x06 | Body Actuation |
| 0x07 | Powertrain Control |
| 0x08 | Fail-safe |
| 0x09 | Validation/Diag |
| 0x0A | ADAS Object |

---

## 6. 11-bit 호환 정책

- 현행 11-bit 실행 ID 대역은 컷오버 전까지 유지 가능
- 신규/변경 요구의 정책 승인 ID는 29-bit를 기준으로만 발급
- 11-bit 값은 `Compatibility Mapping`으로만 유지
- `0x000~0x0FF` 신규 할당 금지

---

## 7. 중재/해석 경계

- CAN 중재 우선순위: Identifier 값 기준
- 서비스 우선순위(경보 판정/강등/복구): 애플리케이션 로직 기준
- 두 개념을 문서에서 혼용하지 않는다.

---

## 8. Comm 기준 Target EXT_ID 샘플 (1차)

| Comm ID | 용도 | Target EXT_ID |
|---|---|---|
| Comm_001 | 차량 상태 입력 | `0x0C200001` |
| Comm_003 | 내비 컨텍스트 입력 | `0x0C600003` |
| Comm_006 | 경고 선택 egress | `0x04A00006` |
| Comm_008 | 클러스터 출력 | `0x08600008` |
| Comm_009 | 검증 결과 프레임 | `0x10E00009` |
| Comm_120 | 근접 위험 상태 | `0x04A00078` |
| Comm_124 | 경계/Fail-safe | `0x04C0007C` |
| Comm_130 | 객체 위험 입력 | `0x04A00082` |
| Comm_133 | 객체 안전/강등 | `0x04A00085` |

- 위 샘플은 정책 검증용이다.
- Comm 전수 매핑은 0303 동기화 시점에 확정한다.

---

## 9. 전환 절차 (R0~R4)

1. R0 정책 동결: 00f v4.1 승인
2. R1 계약 동결: 0303 Comm별 Target EXT_ID 전수 매핑
3. R2 구현 반영: DBC/CAPL/채널할당/게이트 스크립트
4. R3 검증 반영: 05/06/07 증빙 동기화
5. R4 컷오버: 11-bit 호환 계층 축소/종료 결정

---

## 10. SoT 우선순위

- 정책 SoT: `00f_CAN_ID_Allocation_Standard.md`
- 통신 계약 SoT: `0303_Communication_Specification.md`
- 실행 SoT: `canoe/databases/*.dbc`, `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- 변경 실행 보드: `tmp/change-orders/TEAM_SYNC_BOARD.md`

---

## 11. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.1 | 2026-03-09 | Primary 정책을 29-bit 3분할(`3/5/21`)로 단순화. 기존 `3/5/5/16`은 Slot 권고 프로파일(선택)로 하향. Tier/Block/Slot 하이브리드 규칙 및 Comm 샘플 EXT_ID 재정의. |
| 4.0 | 2026-03-09 | 29-bit Extended 중심 정책 초안 도입(`3/5/5/16`). |
| 3.7 | 2026-03-07 | 11-bit 유지/29-bit 전환 기준 추가. |
| 3.6 | 2026-03-07 | 베이스라인 정합 보강 및 E213~E216 운영 규칙 명확화. |
