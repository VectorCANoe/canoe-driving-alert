# CLI Productization BP (Research + Foundation Plan)

## 1) Purpose

This document defines a practical, industry-aligned baseline for turning current script assets into a maintainable CLI product and CI/CD pipeline.

Scope:

- current repository script topology (`scripts/`, `canoe/scripts/`)
- command surface standardization
- packaging/release path
- CI/CD integration strategy

Out of scope:

- GUI implementation details
- RAG service implementation details

## 2) Research Summary (Primary Sources)

### 2.1 Python CLI packaging baseline

- PyPA recommends packaging with `pyproject.toml` and modern build backends.
- CLI tools should expose commands via entry points (`[project.scripts]` / `console_scripts`).
- `src` layout is explicitly used in PyPA command-line tool guide.

Implication for this repo:

- move from ad-hoc `python path/to/script.py` calls to installable CLI command(s)
- keep code import-safe and package-friendly

### 2.2 Entry points and command groups

- Entry points are an interoperability spec, not tied to a single build tool.
- `console_scripts` generates executable command wrappers during installation.
- Entry point groups should avoid collisions and use clear namespaces for plugins.

Implication:

- we can keep one top-level CLI and later add plugin-style command groups (e.g. `verify`, `gate`, `unity`)

### 2.3 CLI framework selection

- Python stdlib `argparse` supports structured subcommands and remains stable.
- Click/Typer are valid advanced layers for nested commands/help/completion.

Implication:

- short term: keep `argparse`-based `scripts/run.py` (already present)
- mid term: decide whether to keep `argparse` or migrate to Typer (only if UX gain is clear)

### 2.4 Distribution (exe)

- PyInstaller one-folder is easier to debug; one-file is simpler for users but slower to startup.
- Nuitka can build standalone/onefile binaries, but requires compiler/toolchain constraints.

Implication:

- first production packaging should be PyInstaller one-folder for stability
- then add one-file distribution channel if startup/time and AV behavior are acceptable
- consider Nuitka only when performance/hardening justifies toolchain cost

### 2.5 CI/CD best practices

- Reusable workflows reduce duplication and improve maintainability.
- Artifacts should be used to pass evidence outputs between jobs.
- PyPA publishing guide recommends Trusted Publishing with OIDC (`id-token: write`) for PyPI.

Implication:

- keep current gates, then refactor into reusable workflows
- persist verification reports/artifacts consistently
- if package publishing is needed, use trusted publishing path

## 3) Current Repository Topology (Fact)

- `scripts/`: quality gates, verification pipeline, CANoe maintenance, doc/report helpers
- `canoe/scripts/`: unity bridge, panel tooling, navigation simulator, cfg fix helpers
- CI currently calls:
  - `python scripts/run.py gate doc-sync`
  - `python scripts/run.py gate cfg-hygiene`
  - `python scripts/run.py gate capl-sync`

See inventory and maintenance boundary:

- `product/sdv_operator/docs-src/maintenance.md`

## 4) Target Architecture

### 4.1 Product layers

1. Command Surface
- single public entrypoint (`sdv` or `python scripts/run.py`)

2. Application Services
- `verify` (prepare/smoke/fill/score/insight)
- `gate` (doc/cfg/capl sync)
- `unity` (bridge/mock/sync/check)
- `ops` (CANoe maintenance helpers)

3. Adapters
- CANoe COM adapter
- filesystem/report adapters

### 4.2 Command policy

- Basic users: `verify`, `gate` only
- Advanced users: `unity`, `ops`
- Experimental/unsafe scripts (`cfg` patch style): exclude from official command help

### 4.3 Output contract

Each command should standardize:

- exit code (`0` pass, `2` validation fail, `>=10` runtime/system error)
- machine-readable output (`--json` planned)
- deterministic report paths

## 5) Foundation Work (Before CLI/GUI Build)

### Phase F0: Inventory Freeze

- complete and lock product maintenance/inventory baseline in `product/sdv_operator/docs-src/maintenance.md`
- classify every script into A/B/C/D

Done status:

- initial classification complete

### Phase F1: Command Contract Freeze

- define official verbs and options
- map old direct script calls to command aliases

Minimum commands:

- `verify-prepare`
- `verify-smoke`
- `verify-fill-score`
- `verify-insight`
- `gate-doc-sync`
- `gate-cfg-hygiene`
- `gate-capl-sync`

Done status:

- canonical command contract defined in `scripts/run.py`
- legacy aliases kept for migration safety

### Phase F2: CI Alignment

- route workflow calls through single entrypoint
- upload standardized artifacts for verification outputs

Done status:

- `doc-code-sync-gate.yml` now calls `python scripts/run.py gate doc-sync`
- `cfg-hygiene-gate.yml` now calls `python scripts/run.py gate cfg-hygiene`

### Phase F3: Packaging Baseline

- introduce package metadata (`pyproject.toml`)
- define `console_scripts` entry point (e.g. `sdv`)
- keep `scripts/run.py` as compatibility path during migration

Done status:

- `pyproject.toml` added
- `sdv` console entrypoint added (`sdv_cli:main`)
- `scripts/run.py` remains canonical implementation during migration

### Phase F4: Binary Distribution

- channel A: PyInstaller one-folder (debug/stable baseline)
- channel B: PyInstaller one-file (operator convenience)
- optional channel C: Nuitka (compiler-dependent path)

Done status:

- build script added: `scripts/release/build_sdv_exe.py`
- command surface integrated: `python scripts/run.py package build-exe --mode onefolder|onefile`
- manual build workflow added: `.github/workflows/sdv-cli-build.yml`

### Phase F5: GUI Readiness Gate

GUI work can start after:

- command contract fixed
- CLI execution deterministic
- verification artifacts and exit codes stable
- CI gate integration complete

Done status:

- readiness gate implemented: `python scripts/run.py gate cli-readiness`
- machine-readable contract output added: `python scripts/run.py contract --json`

## 6) Documentation Set to Maintain

- `scripts/README.md` (daily command quick-start)
- `product/sdv_operator/docs-src/maintenance.md` (asset governance)
- `canoe/docs/operations/CLI_PRODUCTIZATION_BP.md` (this document)
- `canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md` (verification evidence standard)

## 7) Risks and Mitigations

1. Risk: dual roots (`scripts`, `canoe/scripts`) stay confusing
- Mitigation: single command surface + inventory governance

2. Risk: CI and local commands diverge
- Mitigation: CI calls same command entrypoint as local usage

3. Risk: one-file exe startup/AV friction
- Mitigation: keep one-folder baseline and validate before one-file rollout

4. Risk: unsafe cfg patch scripts used in production flow
- Mitigation: classify as experimental and hide from default CLI

## 8) Immediate Next Step (Actionable)

1. Freeze command contract in `scripts/run.py`.
2. Update CI workflows to use `scripts/run.py` commands.
3. Add `pyproject.toml` + `console_scripts` without breaking existing paths.
4. Build first packaging target (PyInstaller one-folder).

## 9) Source Links

- PyPA packaging tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- PyPA CLI packaging guide: https://packaging.python.org/en/latest/guides/creating-command-line-tools/
- PyPA entry points spec: https://packaging.python.org/en/latest/specifications/entry-points/
- Setuptools entry points: https://setuptools.pypa.io/en/latest/userguide/entry_point.html
- Python argparse docs: https://docs.python.org/3/library/argparse.html
- pytest good practices: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- PyInstaller operating mode: https://pyinstaller.org/en/stable/operating-mode.html
- Nuitka user manual: https://nuitka.net/user-documentation/user-manual.html
- GitHub reusable workflows: https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations
- GitHub artifacts: https://docs.github.com/en/actions/tutorials/store-and-share-data
- PyPA publishing with GitHub Actions: https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
