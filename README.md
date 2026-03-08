# canoe-driving-alert

CANoe SIL 기반 주행상황 경고 시스템과 검증 자동화 워크스페이스입니다.

이 저장소는 공개용 단일 제품 저장소라기보다 다음이 함께 있는 협업 저장소입니다.

- CANoe 런타임 프로젝트
- V-model 문서/추적성 산출물
- SDV Operator 검증 자동화 제품

그래서 내부 작업 자료는 유지하되, 외부에서 보는 시작점은 최소화합니다.

## Start Here

### Product Surface
- [SDV Operator](product/sdv_operator/README.md)
- [Operator Docs Source](product/sdv_operator/docs-src/index.md)

### Core Commands
```powershell
python scripts/run.py
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

### Repository Layers
- `product/sdv_operator/`: Dev2 public-facing verification product surface
- `canoe/`: Dev1 CANoe runtime project (`cfg`, `CAPL`, `DBC`, `SysVar`, panel)
- `driving-situation-alert/`: V-model 문서와 추적성 정본

## Scope

현재 범위는 다음에 집중합니다.

- navigation-context warnings
- emergency vehicle alerts (police / ambulance)
- warning arbitration and timeout clear behavior
- CANoe SIL 기반 UT / IT / ST 증빙 수집
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 추적성 유지

## Public Docs Policy

- Markdown이 정본입니다.
- HTML은 generated site입니다.
- 내부 handoff / mentoring / tmp / team board는 제품 표면이 아닙니다.

문서 사이트를 빌드하려면:

```powershell
python -m pip install -e .[docs]
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## Internal Working Docs

<details>
<summary>Open internal working entrypoints</summary>

읽기 시작점:

1. `AGENTS.md`
2. `driving-situation-alert/TMP_HANDOFF.md`
3. `docs/DEVELOPMENT_ENTRYPOINTS.md`
4. `canoe/FILE_INDEX.md`
5. `scripts/README.md`

주요 내부 작업면:

- `driving-situation-alert/tmp/`
- `canoe/tmp/`
- `docs/README.md`
- `docs/meeting-notes/`
- `reference/README.md`
- `.claude/README.md`

</details>

## External References

- [Vector CANoe](https://www.vector.com/int/en/products/products-a-z/software/canoe/)
- [CAN in Automation](https://www.can-cia.org/)
- [Hyundai Mobis](https://www.mobis.co.kr/)
- [Vector Korea](https://www.vector.com/kr/ko/)
