# RTE Name Mapping 표준

**Document ID**: PROJ-00G-RTE-NAMING  
**Version**: 1.1  
**Date**: 2026-03-05  
**Status**: Released (SoT Fixed)  
**Scope**: `04 -> Code(CAPL/C) -> 05/06/07`

---

## 1. 목적

- AUTOSAR shortName에서 RTE 생성 함수명으로 이어지는 규칙을 단일 SoT로 고정한다.
- ECU 명명 정책(`00e`)과 RTE 생성명 정책을 분리해 변경 경계를 명확히 한다.
- 구현/리뷰 단계에서 RTE 함수명 길이/중복/가독성 리스크를 사전 차단한다.

---

## 2. 기준 레퍼런스

| 구분 | 기준 | 반영 포인트 |
|---|---|---|
| 국제/산업 | AUTOSAR CP SWC Modeling Guide (R24-11, 6.3.1/6.3.3) | shortName 제약, RTE 생성명 연결 규칙 |
| 국제/산업 | `SWS_Rte_1153`, `SWS_Rte_3837` | 모델 요소-함수명 매핑 규칙 |
| 내부 SoT | `00e_ECU_Naming_Standard.md` | Canonical/shortName 정합 |
| 구현 참조 | `04_SW_Implementation.md` | 구현 단계 적용/승인 경로 |

---

## 3. 3계층 이름체계

| 계층 | 목적 | 규칙 | 예시 |
|---|---|---|---|
| Project Canonical | 문서/DBC/CAPL/리뷰 기준명 | `UPPER_SNAKE_CASE` | `WARN_ARB_MGR` |
| AUTOSAR shortName | SW-C/Port/Runnable 모델링명 | `UpperCamelCase` | `WarnArbMgr` |
| RTE Generated | 코드 생성 API명 | `Rte_*` 연결 규칙 | `Rte_IRead_WarnArbMgr_InAlert_AlertState` |

---

## 4. RTE Name Mapping 규칙

- AUTOSAR CP SWC Modeling Guide 6.3.3 기준으로, 모델 shortName은 RTE C 함수명으로 연결된다.
- 적용 근거: `SWS_Rte_1153`, `SWS_Rte_3837`.
- 생성명 패턴(대표):
  - `Rte_IRead_<Runnable>_<Port>_<DataElement>`
  - `Rte_IRead_<Component>_<Runnable>_<Port>_<DataElement>`
- 원문 예시 토큰: `Wshr`, `WshrFrnt`, `Monr`, `OutdT`, `Val`.
- 원문 예시 생성명:
  - `Rte_IRead_Monr_OutdT_Val`
  - `Rte_IRead_Wshr_Monr_OutdT_Val`

### 4.1 Length Restriction 연계 (6.3.1)

- RTE 생성명은 모델 요소명 연결 길이에 비례해 급격히 길어질 수 있다.
- AUTOSAR 원문 예시: 단일 모델명이 최대 128일 경우 `Rte_IWrite_<Runnable>_<Port>_<Data>` 형식은 이론상 최대 397자까지 증가 가능하다.
- 프로젝트 품질 규칙(가독성/리뷰성):
  - `Rte_IRead/IWrite_<Runnable>_<Port>_<DataElement>`: 권장 `<= 64`
  - `Rte_IRead/IWrite_<Component>_<Runnable>_<Port>_<DataElement>`: 권장 `<= 80`
  - 권장값 초과 시 shortName 재설계(토큰 길이 축소, 중복 어근 제거)를 우선 적용한다.

### 4.2 프로젝트 적용 제약

- Canonical ECU명(`UPPER_SNAKE_CASE`)은 `00e` 기준을 따른다.
- shortName 토큰 권장 길이:
  - SW-C/Prototype: `<= 16`
  - Runnable: `<= 12`
  - Port/DataElement: `<= 12`
- 토큰은 의미 기반 약어만 허용하고, 임의 축약/모음제거형은 금지한다.
- 대소문자만 다른 shortName 금지(사람/도구 혼동 방지).

### 4.3 Canonical -> shortName 변환 규칙

- Canonical 토큰(`_`)을 기준으로 단어 경계를 유지한다.
- shortName은 각 토큰의 의미를 유지한 `UpperCamelCase`로 변환한다.
- 역할 토큰(`CTRL`, `MGR`, `GW`, `TX`, `RX`, `DEV`)은 축약 해제 없이 그대로 보존한다.
- 예시:
  - `NAV_CTX_MGR` -> `NavCtxMgr`
  - `VAL_SCENARIO_CTRL` -> `ValScenarioCtrl`
  - `DOMAIN_ROUTER` -> `DomainRouter`

---

## 5. 설계/리뷰 체크포인트

- ECU/인터페이스 신규/변경 시 Canonical + shortName을 동시에 등록한다.
- RTE 함수명 샘플 2개 이상을 산출해 과도한 길이/중복을 사전 점검한다.
- 포트/데이터명 변경 시 기존 생성 함수명과의 역추적 가능성을 유지한다.
- 승인 경로: `00e`(명명 기준 확인) -> `04`(RTE/구현 반영) 순으로 적용한다.

---

## 6. 운영 경계

- RTE 명명 규칙의 명시적 관리 문서는 `00g`로 고정한다.
- 참조 문서는 `04`로 한정한다.
- `01/03/0301/0302/0303/0304/05/06/07`은 RTE 규칙 본문을 중복 정의하지 않는다.

---

## 7. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.1 | 2026-03-05 | `00e` Canonical 약어 동기화: 예시 매핑을 `NAV_CTX_MGR`, `DOMAIN_ROUTER` 기준으로 갱신. |
| 1.0 | 2026-03-05 | `00e`에서 RTE Name Mapping 규칙을 분리해 `00g` 표준 문서 신설. |
