# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 1.0  
**Date**: 2026-03-05  
**Status**: Draft  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

## 1. 목적

- CAN ID 배정/예약/충돌검사 규칙의 단일 SoT를 정의한다.
- 문서 스펙(0302/0303/0304)과 DBC 구현의 동기화를 보장한다.

---

## 2. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | Linux CAN/J1939/ISO-TP docs | CAN ID 구조/확장성 원칙 |
| 내부 SoT | `canoe/databases/*.dbc` | 실 ID/Owner 기준 |
| 내부 문서 | `0302`, `0303`, `0304` | Flow/Comm/Var 연동 |
| 멘토링 | MET40 | test_can 해석, 도메인 분리, ID 룰 명확화 |

---

## 3. ID 블록 정책 (11-bit CAN)

| 블록 | 용도 | 상태 |
|---|---|---|
| `0x060~0x07F` | ETH-backbone CAN stub/bridge | 사용중 (`0x064`) |
| `0x100~0x12F` | Chassis + 입력/상태 + Validation ingress | 사용중 |
| `0x210~0x21F` | Body core | 사용중 |
| `0x220~0x22F` | Infotainment core/cluster | 사용중 |
| `0x230~0x23F` | Validation result frames | 사용중 (`0x230`,`0x231`,`0x232`) |
| `0x240~0x24F` | Body extended | 사용중 |
| `0x260~0x26F` | Infotainment extended | 사용중 |
| `0x300~0x31F` | Powertrain | 사용중 |
| `0x330~0x34F` | ADAS reserved/new domain | 예약 |
| `0x350~0x37F` | Future extension reserve | 예약 |

---

## 4. 할당 원칙

- 신규 CAN ID는 해당 도메인 블록 내부에서만 할당한다.
- 블록 여유 부족 시, 확장안 승인 후 할당한다.
- `Validation frame(0x230/0x231)`은 Chassis 통합 경로 유지.
- Ethernet 논리 ID(`0xE100/0xE200/...`)와 CAN stub ID(`0x064/0x232/0x313~`)를 혼동하지 않는다.
- `test_can`은 활성 SoT가 아니며, 운영 경로는 도메인 DBC 기준으로 관리한다.

---

## 5. 변경 절차 (필수)

1. `0302/0303/0304` 동시 수정  
2. DBC(`canoe/databases/*.dbc`) 반영  
3. CAPL 송수신 노드/메시지 정합  
4. `05/06/07` 검증 케이스 참조 갱신  
5. 충돌 검사 기록 첨부

---

## 6. 충돌 검사 규칙

- 기준: 활성 DBC 전체에서 Message ID 중복 0건.
- 점검 방법: `BO_` ID 전수 스캔으로 중복 여부를 산출하고 change-order에 결과 첨부.

---

## 7. 문서 적용 규칙

- 명명/약어 정책은 `00e_ECU_Naming_Standard.md`를 따른다.
- ID 정책은 본 문서를 기준으로 한다.
- `0302`/`0303`/`0304`와 DBC가 불일치하면 DBC SoT를 우선 확인 후 문서를 동기화한다.

---

## 8. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-03-05 | 통합 문서에서 CAN ID 배정 표준을 00f로 분리 |
