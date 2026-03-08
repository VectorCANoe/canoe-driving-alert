> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# V2 All-in 문서 동기화 메모 (2026-03-04)

## 1) 현재 상태
- 기준 브랜치: `integration/v2-all-in`
- 작업 브랜치: `work/all-in-main-doc-sync-20260304`
- 문서 동기화는 **통째 복사 금지**, **라인 단위 선별 반영** 원칙 유지

## 2) 이번 선별 반영 완료 항목
- `0302_NWflowDef.md`
- `0303_Communication_Specification.md`
- `0304_System_Variables.md`
- `04_SW_Implementation.md`
- `0301_SysFuncAnalysis.md` (BaseScenarioResult 명칭 정합)
- `03_Function_definition.md` (BaseScenarioResult 명칭 정합)

## 3) 핵심 정합 포인트
- CAN SoT: 도메인 DBC + `eth_backbone_can_stub.dbc`
- Ethernet 논리 SoT: `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- CANoe.CAN 제약으로 대체 운반되는 Stub ID 명시 유지:
  - `0x064`, `0x11F`, `0x232`, `0x313`, `0x314`, `0x315`

## 4) 감사 관점 확인 결과
- `0302/0303` 문서 내 CAN ID 중 DBC 비존재 항목은 아래 8개이며, 의도된 Ethernet 논리/Stub 구간임
  - `0x510`, `0x511`, `0x512`, `0xE100`, `0xE200`, `0xE210`, `0xE211`, `0xE212`
- 위 8개는 `ETH_INTERFACE_CONTRACT.md`에 정의되어 있어 SoT 단절 없음

## 5) 다음 액션
1. 개발팀 DBC 최종본 고정 시점에 `0302/0303`의 ID/DLC/Signal 최종 1회 재대조
2. all-in으로 반영 시, 아래 커밋만 선별 반영
   - `24e9dfe`
   - `db577b8`
   - `ec8dac6`
3. 반영 후 `scripts/quality/doc_code_sync_gate.py` PASS 확인
