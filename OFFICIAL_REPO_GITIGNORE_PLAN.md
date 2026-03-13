# Official Repo Gitignore Plan

이 문서는 `공식 자료 공개` 전 정리를 위한 기준입니다.

## Official Repo Scope

공식 레포 기준으로 유지할 최상위 경로는 아래 3개입니다.

- `canoe/`
- `driving-alert-workproducts/`
- `product/`

공식 레포 전환 시 위 3개를 제외한 나머지 최상위 폴더는 모두 제외 대상으로 관리합니다.

## Top-Level Exclusion Inventory (Full, Pending)

아래는 현재 루트 기준 `3개 공식 폴더 외` 전체 목록입니다.
지금은 문서 기준으로만 고정하고, 실제 `.gitignore` 반영은 나중에 수행합니다.

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
- `scripts/`
- `__pycache__/`

## Keep Policy (By Directory)

### `canoe/`

유지:

- `cfg/`
- `databases/`
- `docs/`
- `project/`
- `src/`
- `tests/`
- `tools/`
- `README.md`
- `AGENTS.md`
- `FILE_INDEX.md`

공식 공개 제외(ignorable candidates):

- `legacy/`
- `tmp/`
- `logging/`
- `reference/`
- `.claude/`
- `AGENT/`

### `driving-alert-workproducts/`

유지:

- `00_Project_Overview.md`
- `01~07`, `0301~0304` SSoT 문서
- `governance/`
- `excel/`

공식 공개 제외(ignorable candidates):

- `archive/`

### `product/`

유지:

- `sdv_operator/config/`
- `sdv_operator/docs-src/`
- `sdv_operator/docs/`
- `sdv_operator/manifest.json`
- `sdv_operator/mkdocs.yml`
- `sdv_operator/README.md`

공식 공개 제외(ignorable candidates):

- `sdv_operator/site/` (generated output)
- `sdv_operator/examples/` (내부 샘플 성격일 때)

## Proposed .gitignore Entries

아래는 적용 후보입니다. 아직 자동 적용하지 않습니다.

```gitignore
# official repo prep

# root-level (keep only canoe/, driving-alert-workproducts/, product/)
.claude/
.codex-tmp/
.githooks/
.github/
.pytest_cache/
.venv/
artifacts/
build/
canoe_sdv_cli.egg-info/
dist/
docs/
legacy_projects/
reference/
scripts/
__pycache__/

canoe/legacy/
canoe/tmp/
canoe/logging/
canoe/reference/
canoe/.claude/
canoe/AGENT/

driving-alert-workproducts/archive/

product/sdv_operator/site/
# product/sdv_operator/examples/
```

## Apply Sequence (Safe)

1. 이 문서 기준으로 최종 제외 범위를 확정한다.
2. `.gitignore`에 경로 규칙을 반영한다.
3. 이미 추적 중인 파일은 `git rm --cached`로 인덱스에서만 제거한다.
4. 최종 공개 브랜치에서 `canoe/`, `driving-alert-workproducts/`, `product/`만 검수한다.
