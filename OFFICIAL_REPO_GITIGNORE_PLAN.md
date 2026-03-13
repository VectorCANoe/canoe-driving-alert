# Official Repo Gitignore Plan

이 문서는 `공식 자료 공개` 전 정리를 위한 기준입니다.

## Official Repo Scope

공식 레포 기준으로 유지할 최상위 경로는 아래 4개입니다.

- `canoe/`
- `driving-alert-workproducts/`
- `product/`
- `scripts/`

공식 레포 전환 시 위 4개를 제외한 나머지 최상위 폴더는 모두 제외 대상으로 관리합니다.

## Official Public Surface Tree

아래 트리는 `공식 공개 surface`만 남겼을 때의 목표 구조입니다.

```text
/
  canoe/
    AGENTS.md
    FILE_INDEX.md
    README.md
    cfg/
    databases/
    docs/
    project/
    src/
    tests/
    tools/

  driving-alert-workproducts/
    README.md
    00_Project_Overview.md
    01_Requirements.md
    02_Concept_design.md
    03_Function_definition.md
    0301_SysFuncAnalysis.md
    0302_NWflowDef.md
    0303_Communication_Specification.md
    0304_System_Variables.md
    04_SW_Implementation.md
    05_Unit_Test.md
    06_Integration_Test.md
    07_System_Test.md
    governance/
    excel/

  product/
    sdv_operator/
      README.md
      manifest.json
      mkdocs.yml
      config/
      docs/
      docs-src/

  scripts/
    run.py
    tui_app.py
    cliops/
    gates/
    quality/
    release/
    report/
```

## Hard Exclusion Rule

아래 성격의 자료는 공식 공개 surface에 포함하지 않습니다.

- `archive`
- `tmp`
- `local reference`
- `internal notes`

이 규칙은 디렉터리 이름이 다르더라도 동일하게 적용합니다.

예:

- archived snapshots
- migrated root backups
- handoff notes
- mentoring notes
- reports
- change-order history
- local reference vault
- imported OSS/tutorial/standard/sample banks
- execution-only support material

## Top-Level Exclusion Inventory (Full, Pending)

아래는 현재 루트 기준 `4개 공식 폴더 외` 전체 목록입니다.
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
- `ops/`
- `reference/`

세부 제외 원칙:

- `archive/` = archived snapshots, migrated root backups, old tmp payloads
- `ops/` = handoff, mentoring, reports, change-orders, submission support, internal execution notes
- `reference/` = local reference bank, imported OSS/tutorial/standard/sample material
- `tmp` 성격 자료 = 공개 surface에서 제외
- `internal notes` 성격 자료 = 공개 surface에서 제외

공개 목표 트리:

```text
driving-alert-workproducts/
  README.md
  00_Project_Overview.md
  01_Requirements.md
  02_Concept_design.md
  03_Function_definition.md
  0301_SysFuncAnalysis.md
  0302_NWflowDef.md
  0303_Communication_Specification.md
  0304_System_Variables.md
  04_SW_Implementation.md
  05_Unit_Test.md
  06_Integration_Test.md
  07_System_Test.md
  governance/
  excel/
  ───────────────────────
  제외:
    archive/
    ops/
    reference/
```

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

### `scripts/`

유지:

- `run.py`
- `tui_app.py`
- `cliops/`
- `gates/`
- `quality/`
- `release/`
- `report/`

공식 공개 제외(ignorable candidates):

- 생성물 성격의 임시 출력물
- 로컬 전용 실행 로그
- 캐시 및 가상환경

## Proposed .gitignore Entries

아래는 적용 후보입니다. 아직 자동 적용하지 않습니다.

```gitignore
# official repo prep

# root-level (keep only canoe/, driving-alert-workproducts/, product/, scripts/)
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
__pycache__/

canoe/legacy/
canoe/tmp/
canoe/logging/
canoe/reference/
canoe/.claude/
canoe/AGENT/

driving-alert-workproducts/archive/
driving-alert-workproducts/ops/
driving-alert-workproducts/reference/

product/sdv_operator/site/
# product/sdv_operator/examples/
```

## Apply Sequence (Safe)

1. 이 문서 기준으로 최종 제외 범위를 확정한다.
2. `.gitignore`에 경로 규칙을 반영한다.
3. 이미 추적 중인 파일은 `git rm --cached`로 인덱스에서만 제거한다.
4. 최종 공개 브랜치에서 `canoe/`, `driving-alert-workproducts/`, `product/`, `scripts/`만 검수한다.

## Publish Enforcement Checklist

공개 브랜치 반영 전 아래를 반드시 확인합니다.

1. 루트에는 `canoe/`, `driving-alert-workproducts/`, `product/`, `scripts/`와 승인된 루트 문서만 남겼는가
2. `driving-alert-workproducts/` 안에 아래 경로가 staging 대상에서 빠졌는가
   - `archive/`
   - `ops/`
   - `reference/`
3. `archive/tmp/local reference/internal notes` 성격 자료가 다른 이름으로 남아 있지 않은가
4. 이미 추적 중인 제외 대상은 `git rm --cached`로 인덱스에서 제거했는가
5. 반영 시 `git add .` 대신 허용 경로만 path-based add 했는가
