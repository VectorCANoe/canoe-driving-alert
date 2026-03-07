# RTE Name Mapping 표준

**Document ID**: PROJ-00G-RTE-NAMING  
**Version**: 1.1  
**Date**: 2026-03-05  
**Status**: Released (SoT Fixed)  
**Scope**: `04 -> Code(CAPL/C) -> 05/06/07`

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

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

