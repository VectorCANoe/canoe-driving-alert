# 유지보수 경계

## 소유 경계

### Dev1
- `canoe/`
- cfg
- panel
- sysvars
- DBC
- CAPL
- CANoe runtime behavior

### Dev2
- `SDV Operator` 제품 표면
- CLI / TUI
- gate 실행 표면
- verification / evidence 실행 표면
- packaging

## 제품 경계 정본

제품 경계는 아래 두 파일을 기준으로 봅니다.

- `product/sdv_operator/README.md`
- `product/sdv_operator/manifest.json`

## 코드 계층

### Public operator surface
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/README.md`

### Internal command/runtime layer
- `scripts/cliops/*`

### Verification engines
- `scripts/quality/*`
- `scripts/gates/*`

### Advanced CANoe helpers
- `scripts/canoe/*`
- `canoe/scripts/*`

### Legacy / one-off helpers
- `scripts/docs/*`
- `scripts/report/*`

## 운영 규칙

1. 사용자는 `python scripts/run.py`만 진입점으로 사용합니다.
2. 제품 표면은 `Gate all -> Scenario run -> Verify quick` 흐름을 기준으로 유지합니다.
3. helper / legacy 스크립트는 public surface로 승격하지 않습니다.
4. 생성 산출물은 소스와 분리해서 다룹니다.
5. root README는 제품 소개와 진입점만 보여줍니다.

## 대표 Gate

| Gate | Local Command | Main Script | Primary Scope |
|---|---|---|---|
| CFG Hygiene | `python scripts/run.py gate cfg-hygiene` | `scripts/gates/cfg_hygiene_gate.py` | CANoe text hygiene |
| CAPL Sync | `python scripts/run.py gate capl-sync` | `scripts/gates/check_capl_sync.py` | `src/capl` vs `cfg/channel_assign` sync |
| MultiBus + DBC Policy | `python scripts/run.py gate multibus-dbc` | `scripts/gates/multibus_cfg_dbc_gate.py` | multi-bus cfg + DBC ownership |
| Doc-Code Sync | `python scripts/run.py gate doc-sync` | `scripts/gates/doc_code_sync_gate.py` | traceability + runtime linkage checks |
| CLI Readiness | `python scripts/run.py gate cli-readiness` | `scripts/gates/cli_readiness_gate.py` | CLI contract and help stability |

## 한 줄 기준

질문이 `무엇을 실행하면 되나요?`라면 답은 아래 다섯 개를 넘지 않아야 합니다.

- `python scripts/run.py`
- `gate all`
- `scenario run`
- `verify quick`
- `doctor`
