# canoe-driving-alert

CANoe SIL 기반 주행상황 경고 시스템과 검증 자동화 저장소입니다.

이 저장소는 단일 제품 저장소가 아니라 아래 세 층을 함께 포함합니다.

- `canoe/`: CANoe 런타임 프로젝트
- `driving-alert-workproducts/`: V-model 문서와 추적성 정본
- `product/sdv_operator/`: Dev2 검증 실행/리뷰 표면

## Start Here

### Product Surface
- [CANoe Test Verification Console](product/sdv_operator/README.md)
- [Operator Docs](product/sdv_operator/docs-src/index.md)

### Core Commands
```powershell
python scripts/run.py
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

## Scope

- navigation-context warnings
- emergency vehicle alerts (police / ambulance)
- warning arbitration and timeout clear behavior
- CANoe SIL 기반 UT / IT / ST 증빙 수집
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 추적성 유지

## Docs Policy

- Markdown이 정본입니다.
- HTML은 generated site입니다.
- 내부 handoff, mentoring, tmp, team board는 제품 표면에 직접 노출하지 않습니다.

## Official Repo Prep

공식 공개 기준 최상위 범위:

- `canoe/`
- `driving-alert-workproducts/`
- `product/`

공개 전 `gitignore` 제외 후보(legacy/tmp/archive/generated)와 적용 순서는 아래 문서 기준으로 관리합니다.

- [OFFICIAL_REPO_GITIGNORE_PLAN.md](OFFICIAL_REPO_GITIGNORE_PLAN.md)

문서 사이트 빌드:

```powershell
python -m pip install -e .[docs]
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## Internal Working Docs

<details>
<summary>Open internal working entrypoints</summary>

읽기 시작점:

1. `AGENTS.md`
2. `driving-alert-workproducts/ops/handoff/TMP_HANDOFF.md`
3. `docs/DEVELOPMENT_ENTRYPOINTS.md`
4. `canoe/FILE_INDEX.md`

주요 내부 작업면:

- `driving-alert-workproducts/ops/`
- `canoe/tmp/`
- `docs/`
- `reference/`
- `legacy_projects/`

</details>
