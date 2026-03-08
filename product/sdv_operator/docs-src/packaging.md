# 패키징 범위

패키징할 때는 저장소 전체를 묶지 않는다.

## 포함

- `pyproject.toml`
- `sdv_cli.py`
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/cliops/`
- `scripts/gates/`
- `scripts/quality/`
- `scripts/release/`

## 제외

- `canoe/` 런타임 자산
- `scripts/docs/`
- `scripts/report/`
- `scripts/canoe/`
- `canoe/scripts/`
- `reference/`
- `legacy_projects/`
- 생성 산출물

## 이유

패키지 제품은 작고 명확해야 한다.
레포지토리는 클 수 있어도, 배포물은 좁아야 한다.

상세 기준:

- `product/sdv_operator/docs/PACKAGING_SCOPE.md`
- `product/sdv_operator/manifest.json`
