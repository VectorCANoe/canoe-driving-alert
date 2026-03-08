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

- `run.py` = 단일 런처 표면
- `tui_app.py` = 운영 콘솔 화면
- `cliops/*`, `quality/*`, `gates/*` = 내부 구현 계층
- 호환용 alias는 유지하지만, 일일 사용자는 canonical 명령만 사용합니다
