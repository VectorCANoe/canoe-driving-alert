# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 2.0  
**Date**: 2026-03-05  
**Status**: Released (SoT Fixed)  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

## 1. 목적

- CAN ID 배정/예약/충돌검사 규칙의 단일 SoT를 정의한다.
- 문서 스펙(0302/0303/0304)과 DBC 구현의 동기화를 보장한다.
- ID 정책의 운영 경계를 고정해 변경 시 감사 추적성을 보장한다.

---

## 2. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | ISO 11898 series, ISO 15765-2(ISO-TP), SAE J1939-21, AUTOSAR CP(COM/CanIf/CanTp/PduR) | CAN ID 구조/중재/전송계층/스택 정합 원칙 |
| 공개 구현 | Linux kernel CAN/ISO-TP/J1939 docs | 구현 검증/툴링 관점 참조 |
| 내부 SoT | `canoe/databases/*.dbc` | 실제 ID/Owner 최종 기준 |
| 내부 문서 | `0302`, `0303`, `0304`, `04` | Flow/Comm/Var/구현 연동 |
| 레퍼런스 카탈로그 | `reference/catalogs/ID_REFERENCE_CATALOG.md` | RAG ingestion 순서/출처 관리 |
| 멘토링 | MET40 | test_can 의존 제거, 도메인 기반 운영 고정 |

---

## 3. 운영 경계 (SoT Governance)

- ID 정책 SoT는 `00f`로 고정하고, 참조 문서는 `0303`(ID 적용), `04`(구현 반영)로 한정한다.
- `01/03/0301/0302/0304/05/06/07`은 정책 본문을 중복 정의하지 않고 적용 결과만 유지한다.
- 최종 판정 우선순위:
  1. `canoe/databases/*.dbc`
  2. `00f_CAN_ID_Allocation_Standard.md`
  3. `0303_Communication_Specification.md`

---

## 4. ID 체계 정책

### 4.1 식별자 타입

- 본 프로젝트 CAN 메시지 ID는 **11-bit(Standard ID)**를 기본으로 사용한다.
- 29-bit(Extended ID)는 현재 범위 외이며, 도입 시 별도 변경승인(00f/0303/DBC 동시 개정)이 필요하다.

### 4.2 우선순위 원칙

- CAN arbitration 특성상 **숫자가 작은 ID가 높은 우선순위**를 갖는다.
- 긴급/안전 관련 메시지는 낮은 값 영역에 우선 배정한다.
- 동일 기능군 내부에서는 주기/지연요구를 고려해 ID를 정렬한다.

### 4.3 논리 ID와 Stub ID 분리

- Ethernet 논리 ID(`0xE100`, `0xE200`, `0xE210~0xE212`)와 CAN Stub ID(`0x064`, `0x232`, `0x313~0x315`)를 분리 관리한다.
- 문서 설명은 논리 ID 우선, CANoe SIL 실행은 Stub ID를 병기한다.

---

## 5. ID 블록 정책 (11-bit CAN)

| 블록 | 용도 | 상태 |
|---|---|---|
| `0x060~0x07F` | ETH-backbone CAN stub/bridge | 사용중 (`0x064`) |
| `0x100~0x12F` | Chassis + 입력/상태 + Validation ingress | 사용중 |
| `0x210~0x21F` | Body core | 사용중 |
| `0x220~0x22F` | Infotainment core/cluster | 사용중 |
| `0x230~0x23F` | Validation result frames | 사용중 (`0x230`, `0x231`, `0x232`) |
| `0x240~0x24F` | Body extended | 사용중 |
| `0x260~0x26F` | Infotainment extended | 사용중 |
| `0x300~0x31F` | Powertrain + V2 stub | 사용중 |
| `0x330~0x34F` | ADAS reserved/new domain | 예약 |
| `0x350~0x37F` | Future extension reserve | 예약 |

---

## 6. 할당 원칙

- 신규 CAN ID는 해당 도메인 블록 내부에서만 할당한다.
- 블록 여유 부족 시 예약 블록 전개 승인 후 할당한다.
- `Validation frame(0x230/0x231)`은 Chassis 통합 경로를 유지한다.
- `test_can`은 활성 SoT가 아니며, 운영 경로는 도메인 DBC 기준으로 관리한다.
- 동일 변경에서 `ID -> Comm -> Var -> Code -> Test` 연쇄 동기화를 필수로 한다.

---

## 7. 변경 절차 (필수 게이트)

1. `0302/0303/0304` 동시 수정  
2. DBC(`canoe/databases/*.dbc`) 반영  
3. CAPL 송수신 노드/메시지 정합  
4. `05/06/07` 검증 케이스 참조 갱신  
5. ID 중복/범위 점검 결과 첨부  
6. 변경 이력(00f/0303/04) 동시 갱신

---

## 8. 충돌 검사 규칙

- 기준: 활성 DBC 전체에서 Message ID 중복 0건.
- 기준: ID가 허용 블록 범위 밖으로 벗어나지 않을 것.
- 점검 방법: `BO_` ID 전수 스캔 결과를 change-order 또는 commit note에 첨부한다.

권장 점검 명령:

```bash
awk '/^BO_ /{print $2}' canoe/databases/*.dbc | sort -n | uniq -d
```

```bash
awk '/^BO_ /{print $2}' canoe/databases/*.dbc | sort -n | awk 'BEGIN{m=999999;M=0}{if($1<m)m=$1;if($1>M)M=$1}END{print m,M}'
```

---

## 9. 문서 적용 규칙

- 명명/약어 정책은 `00e_ECU_Naming_Standard.md`를 따른다.
- ID 정책은 본 문서를 기준으로 한다.
- `0302/0303/0304`와 DBC가 불일치하면 DBC SoT를 우선 확인 후 문서를 동기화한다.

---

## 10. 기준 베이스라인 점검 결과 (2026-03-05)

- 대상: `canoe/databases/*.dbc`
- 총 메시지 수: `98`
- 사용 ID 범위: `0x064(100) ~ 0x315(789)`
- 중복 ID: `0건`
- 블록 분포:
  - `0x060~0x07F`: 1
  - `0x100~0x12F`: 25
  - `0x210~0x21F`: 10
  - `0x220~0x22F`: 9
  - `0x230~0x23F`: 3
  - `0x240~0x24F`: 14
  - `0x260~0x26F`: 14
  - `0x300~0x31F`: 22
  - `0x330~0x34F`: 0 (reserved)
  - `0x350~0x37F`: 0 (reserved)
  - 기타: 0

---

## 11. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.0 | 2026-03-05 | SoT 확정본 고정: `Released (SoT Fixed)` 전환, 11-bit/29-bit 정책·우선순위 원칙·운영 경계·변경 게이트를 체계화하고 레퍼런스 카탈로그(`reference/catalogs/ID_REFERENCE_CATALOG.md`)를 연결. |
| 1.2 | 2026-03-05 | ID 레퍼런스 운영 카탈로그 연동 항목 추가. |
| 1.1 | 2026-03-05 | ID 레퍼런스를 규격 단위(ISO 11898/ISO-TP/J1939/AUTOSAR CP)로 구체화하고, 기준 베이스라인 점검 결과(중복/분포)를 추가. |
| 1.0 | 2026-03-05 | 통합 문서에서 CAN ID 배정 표준을 00f로 분리 |
