# Scripts Guide

`scripts/`는 구현 위치입니다. 제품 표면과 사용자 문서는 `product/sdv_operator/`를 기준으로 봅니다.

## Start Here

```powershell
python scripts/run.py
```

제품 문서 진입점:

1. `product/sdv_operator/README.md`
2. `product/sdv_operator/docs-src/quickstart.md`
3. `product/sdv_operator/docs-src/commands.md`

## Daily Surface

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id <n>
python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>
python scripts/run.py doctor
```

## Boundary

- `scripts/run.py` = compatibility launcher (`product/sdv_operator/scripts/run.py`로 위임)
- `scripts/tui_app.py` = compatibility launcher (`product/sdv_operator/scripts/tui_app.py`로 위임)
- `product/sdv_operator/scripts/cliops/*` = 제품 전용 실행 계층
- `scripts/gates/*`, `scripts/quality/*`, `scripts/release/*` = 공용(CANoe/CI) 계층
- 호환용 alias는 유지하지만, 일일 사용자는 canonical 명령만 사용합니다
