# SDV Operator

`SDV Operator`는 CANoe SIL 검증을 위한 실행 런처이자 결과 검토 콘솔입니다.

이 제품은 CANoe를 대체하지 않습니다.

- 실행: `gate all`, `scenario run`, `verify quick`
- 검토: `PASS / WARN / FAIL`, COM 상태, 증빙 경로, 병목
- 배포: portable ZIP / exe

## Quick Start

설치:

```powershell
python -m pip install -e .
```

문서 사이트까지 빌드하려면:

```powershell
python -m pip install -e .[docs]
```

실행:

```powershell
python scripts/run.py
```

핵심 운영 흐름:

1. `Gate all`
2. `Scenario run`
3. `Verify quick`
4. `Results / Logs` 확인

## Product Boundary

이 제품이 담당하는 것:

- TUI / CLI 실행 표면
- CANoe COM 기반 검증 실행 진입점
- 증빙 수집 및 결과 검토 표면
- portable ZIP / exe 패키징

이 제품이 담당하지 않는 것:

- CANoe cfg 자체 운영
- CAPL / DBC / SysVar 자체 소유
- CANoe panel 재구현

즉:

- Dev1: `canoe/`
- Dev2: `product/sdv_operator` + verification automation surface

## Documentation

문서 정본:

- `product/sdv_operator/docs-src/`
- `product/sdv_operator/mkdocs.yml`

생성물:

- `product/sdv_operator/site/`

빌드:

```powershell
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## Read Next

1. [`docs-src/index.md`](docs-src/index.md)
2. [`docs-src/quickstart.md`](docs-src/quickstart.md)
3. [`docs-src/commands.md`](docs-src/commands.md)
4. [`docs-src/results.md`](docs-src/results.md)
5. [`docs-src/packaging.md`](docs-src/packaging.md)
6. [`docs-src/maintenance.md`](docs-src/maintenance.md)

## Packaging Rule

ZIP/exe를 만들 때는 저장소 전체가 아니라 `SDV Operator` 제품 범위만 패키징합니다.

상세 범위는 다음을 기준으로 봅니다.

- `product/sdv_operator/manifest.json`
- `product/sdv_operator/docs/PACKAGING_SCOPE.md`
