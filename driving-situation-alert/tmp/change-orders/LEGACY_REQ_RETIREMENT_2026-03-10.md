# Legacy Req Retirement Archive

- Date: 2026-03-10
- Status: Archived reference only
- Live SoT: `01_Requirements.md`, `03_Function_definition.md`, `0301~0304`, `04`, `05`, `06`, `07`
- Rule: legacy Req는 live 문서에서 제거하고, 본 문서에만 매핑 이력을 보관한다.

## Retired Legacy Mapping

| Legacy Req ID | Legacy Summary | Active Req ID | Active VC ID | Notes |
|---|---|---|---|---|
| Req_018 | 긴급차량 접근 경고(구급 분리) | Req_017 | VC_017 | 구급 분리 요구는 긴급차량 접근 통합 요구에 흡수 |
| Req_036 | 긴급 패턴 분리 | Req_035 | VC_035 | 긴급 시각표현 표준화 요구에 흡수 |
| Req_038 | 고속도로 패턴 단독 규정 | Req_037 | VC_037 | 구간별 고정 패턴 표준 요구에 흡수 |
| Req_039 | 유도선 패턴 단독 규정 | Req_037 | VC_037 | 구간별 고정 패턴 표준 요구에 흡수 |
| Req_108 | 운전자 상태 단일 레벨 전달 | Req_113, Req_116, Req_118 | VC_113, VC_116, VC_118 | Body 확장 상태 통합 요구로 재구성 |
| Req_114 | 시트 상태 단독 반영 | Req_113 | VC_113 | 실내편의 상태 반영 요구에 흡수 |
| Req_115 | 미러 상태 단독 반영 | Req_113 | VC_113 | 실내편의 상태 반영 요구에 흡수 |
| Req_117 | 와이퍼/우적 단독 반영 | Req_116 | VC_116 | 차체 제어/연동 상태 반영 요구에 흡수 |
| Req_122 | 감속 보조-경고 동기화(복합) | Req_125, Req_126 | VC_125, VC_126 | 긴급 최우선 유지와 경고 채널 동기화로 분할 |
| Req_124 | 도메인 경로 단절 강등(복합) | Req_127, Req_128, Req_129 | VC_127, VC_128, VC_129 | 자동감속 금지, 최소 경고 유지, 안전 강등으로 분할 |

## Removed From Live Docs

| Document | Removed Scope |
|---|---|
| `01_Requirements.md` | legacy Req 행, legacy VC 행, Part 8 legacy section, legacy guide bullets, legacy transition mapping section |
| `03_Function_definition.md` | legacy note, legacy mapping section |
| `0301_SysFuncAnalysis.md` | legacy mapping section |
| `0302_NWflowDef.md` | legacy mapping section |
| `0303_Communication_Specification.md` | legacy mapping section |
| `0304_System_Variables.md` | legacy mapping section |
| `04_SW_Implementation.md` | legacy implementation note |
| `05_Unit_Test.md` | legacy mapping section |
| `06_Integration_Test.md` | legacy mapping section |
| `07_System_Test.md` | legacy mapping section |

## Retention Rule

- revision history는 감사 흔적으로 유지한다.
- 본 archive는 제출본이 아니라 내부 보관용이다.
- live 문서는 legacy 없이 active Req 기준으로만 읽히도록 유지한다.
