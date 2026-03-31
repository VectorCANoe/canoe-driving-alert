# Official Repo Main/Develop Operating Plan

이 문서는 `develop` 브랜치에서만 유지하는 작업용 운영 기준이다.
`main` 은 공식 공개 표면만 유지하며, 이 문서는 `main` 에서 추적하지 않는다.

## 1. Branch Roles

- `develop`: 내부 작업 브랜치
- `main`: 공식 공개 브랜치

`develop` 에서는 아래를 모두 유지할 수 있다.

- handoff / ops / mentoring / change-orders
- archive / reference / tmp 성격 자산
- agent/operator 지시 문서
- 로컬 evidence / log / generated output

`main` 은 항상 리뷰 가능한 공식 표면만 유지한다.

## 2. Official Main Surface

`main` 에서 유지하는 최상위 축은 아래 4개다.

- `canoe/`
- `driving-alert-workproducts/`
- `product/`
- `scripts/`

루트 공개 문서는 아래만 유지한다.

- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `pyproject.toml`
- `sdv_cli.py`
- `.gitignore`
- `.gitattributes`
- `.editorconfig`

## 3. Main Exclusions

### Root internal/operator docs

- `AGENTS.md`
- `CLAUDE.md`
- `OFFICIAL_REPO_GITIGNORE_PLAN.md`

### Root local/build/generated surfaces

- `.claude/`
- `.codex-tmp/`
- `.githooks/`
- `.github/`
- `.pytest_cache/`
- `.venv/`
- `artifacts/`
- `build/`
- `canoe_sdv_cli.egg-info/`
- `dist/`
- `docs/`
- `legacy_projects/`
- `reference/`
- `__pycache__/`

### `canoe/`

공식 유지:

- `cfg/`
- `databases/`
- `docs/`
- `project/`
- `src/`
- `tests/`
- `tools/`
- `README.md`
- `FILE_INDEX.md`

공식 제외:

- `AGENTS.md`
- `AGENT/`
- `.claude/`
- `legacy/`
- `logging/`
- `reference/`
- `tmp/`

주의:

- `canoe/src/capl/ecu/WIP.can`
- `canoe/cfg/channel_assign/Body/WIP.can`

위 두 파일의 `WIP` 는 `Wiper` ECU 약어이므로 제외 대상이 아니다.

### `driving-alert-workproducts/`

공식 유지:

- 루트 SSoT 문서
- `excel/`
- 필요 시 공개용 governance 성격 문서

공식 제외:

- `archive/`
- `ops/`
- `reference/`

### `product/`

공식 유지:

- `sdv_operator/config/`
- `sdv_operator/docs-src/`
- `sdv_operator/docs/`
- `sdv_operator/manifest.json`
- `sdv_operator/mkdocs.yml`
- `sdv_operator/README.md`
- product 내부로 이동한 실행 스크립트

공식 제외:

- `sdv_operator/site/`
- `sdv_operator/examples/`

### `scripts/`

공식 유지:

- 공용 실행/게이트/품질/릴리즈 스크립트

공식 제외:

- `scripts/canoe/`
- `scripts/docs/`
- `scripts/report/`
- `scripts/__pycache__/`

## 4. Fixed Working Rules

- 평상시 작업은 `develop` 에서만 한다.
- `main` 에서는 `git add .` 를 사용하지 않는다.
- `main` 반영은 경로 지정 add 만 사용한다.
- `main` 제외 자산은 `git rm --cached` 로 인덱스에서만 제거한다.
- `.gitignore` 제외 자산은 Git diff 대신 로컬 파일시스템에서 직접 확인한다.

## 5. Promotion Rule: develop -> main

1. `develop` 에서 작업한다.
2. 공개할 경로만 선택한다.
3. `main` 에서는 아래처럼 경로 지정 반영만 한다.

```powershell
git add canoe driving-alert-workproducts product scripts README.md CHANGELOG.md CONTRIBUTING.md pyproject.toml sdv_cli.py
```

4. 내부 운영 파일이 다시 추적되지 않았는지 확인한다.
5. `main` 은 항상 공식 공개 표면만 남긴다.

## 6. Current Operating Decision

- 우리는 앞으로 `develop` 만 작업 브랜치로 사용한다.
- `main` 은 항상 클린한 공식 레포 상태로 유지한다.
