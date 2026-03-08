# Scripts Guide

`scripts/`는 구현 위치입니다.

하지만 사용자는 이 폴더 전체를 알 필요가 없습니다.

## Start Here

하나의 진입점만 사용하십시오.

```powershell
python scripts/run.py
```

제품 설명과 상세 문서는 여기서 봅니다.

1. `product/sdv_operator/README.md`
2. `product/sdv_operator/docs-src/quickstart.md`
3. `product/sdv_operator/docs-src/commands.md`
4. `product/sdv_operator/docs-src/maintenance.md`

## Daily Surface

일반 사용자는 아래 네 개만 기억하면 됩니다.

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id <n>
python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>
python scripts/run.py doctor
```

## Interpretation

- `run.py` = 단일 공개 런처
- `tui_app.py` = 검토 콘솔
- `cliops/*`, `quality/*`, `gates/*` = 내부 구현 계층
- hidden alias는 호환성 유지용이며 일반 운영 표면이 아닙니다.
