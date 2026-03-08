# SDV Operator

`SDV Operator`는 CANoe SIL 검증 자동화를 위한 Dev2 제품 표면입니다.

이 경로는 CANoe 자체를 대체하지 않습니다. CANoe는 실행기이고, `SDV Operator`는
검증 실행, 결과 수집, 증빙 산출, 운영 콘솔을 제공합니다.

## 제공 범위

- 실행: `gate all`, `scenario run`, `verify quick`, `doctor`
- 검토: TUI 기반 결과/로그/COM 상태 확인
- 산출: readiness, batch report, portable ZIP / exe

## 빠른 시작

```powershell
python -m pip install -e .
python scripts/run.py
```

문서 사이트 빌드:

```powershell
python -m pip install -e .[docs]
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## 운영 경계

이 제품이 담당하는 것:

- CLI / TUI 실행 표면
- CANoe COM 기반 검증 자동화
- 결과/증빙 요약과 패키징

이 제품이 담당하지 않는 것:

- CANoe cfg 직접 편집
- CAPL / DBC / SysVar 원본 설계
- CANoe 패널 재구현

즉, Dev1은 `canoe/`, Dev2는 `product/sdv_operator`와 검증 자동화 표면을 담당합니다.

## 읽기 순서

1. [`docs-src/index.md`](docs-src/index.md)
2. [`docs-src/quickstart.md`](docs-src/quickstart.md)
3. [`docs-src/commands.md`](docs-src/commands.md)
4. [`docs-src/results.md`](docs-src/results.md)
5. [`docs-src/packaging.md`](docs-src/packaging.md)
6. [`docs-src/repo-surfaces.md`](docs-src/repo-surfaces.md)
7. [`docs-src/maintenance.md`](docs-src/maintenance.md)

## 패키징 계약

ZIP / exe 산출물 범위는 아래 두 파일을 기준으로 고정합니다.

- `product/sdv_operator/manifest.json`
- `product/sdv_operator/docs/PACKAGING_SCOPE.md`
