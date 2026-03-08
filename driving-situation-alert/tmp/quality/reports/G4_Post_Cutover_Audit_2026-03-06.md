# G4 Post-Cutover Audit (2026-03-06)

## Scope
- Branch: `main`
- Cutover policy: `tmp/change-orders/archive/2026-03/DEV_CHANGE_ORDER_CAN_ID_335_FULL_RENUMBERING_2026-03-05.md`
- Active configuration: `canoe/cfg/CAN_v2_topology_wip.cfg`
- Active DBC set:
  - `canoe/databases/adas_can.dbc`
  - `canoe/databases/body_can.dbc`
  - `canoe/databases/chassis_can.dbc`
  - `canoe/databases/infotainment_can.dbc`
  - `canoe/databases/powertrain_can.dbc`
  - `canoe/databases/eth_backbone_can_stub.dbc`

## Audit Results
1. ID schema integrity
- Message count: `98`
- Range: `0x100 ~ 0x2AA`
- Duplicate CAN ID: `0`
- IDs below 0x100 in active DBC: `0`

2. Traceability/sync gates
- `python scripts/quality/check_capl_sync.py`: `PASS`
  - `src=26 cfg=26 common=26 only_src=0 only_cfg=0 content_diff=0`
- `python scripts/quality/doc_code_sync_gate.py`: `PASS`
- `python scripts/quality/cfg_hygiene_gate.py`: `PASS`

3. Runtime evidence (COM)
- CANoe version: `19.4.10`
- Configuration load: `PASS`
- CAPL compile: `PASS` (`CompileResult.Result = 0`)
- Measurement start/stop: `PASS`
- Core sysvar sampling: `PASS`
  - `Core::failSafeMode`
  - `Core::decelAssistReq`
  - `Core::proximityRiskLevel`
  - `CoreState::domainPathStatus`
  - `Test::forceFailSafe`

## Residual Notes
- `test_can` 문자열은 운영 활성 경로가 아니라 문서의 이관 이력/변경지시 맥락에만 존재함.
- GUI-first 원칙에 따라 `*.cfg/*.cfg.ini/*.stcfg`는 GUI에서만 최종 저장/수정한다.

## Decision
- **G4 status: HOLD (Deferred)**
- Hold reason: 전체 개발 범위가 아직 종료되지 않아 Post-Cutover 최종 감사를 지금 시점에 닫지 않는다.
- Reopen criteria:
  1. 잔여 개발 범위가 `main`에 반영 완료될 것
  2. `check_capl_sync.py`, `doc_code_sync_gate.py`, `cfg_hygiene_gate.py` 재실행 PASS
  3. 런타임(COM) 증적을 최신 구성으로 재채집하고 PM/QA 최종 리뷰 완료
- 현재 기준으로 3/3/5 Cutover 이후 운영 기준(main)은 유지 가능하며, G4는 조건 충족 시 재개한다.
