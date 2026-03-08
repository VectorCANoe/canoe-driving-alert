# 패키징

## 목적

Dev2 제품 표면은 나중에 portable ZIP 또는 Windows executable로 전달할 수 있어야 합니다.

## 기본 명령

### Packaging contract check

```powershell
python scripts/run.py package validate-contract
```

manifest와 release layout 상수가 drift 없이 맞는지 먼저 확인합니다.

### Portable bundle

```powershell
python scripts/run.py package bundle-portable --mode onefolder
```

### Windows executable

```powershell
python scripts/run.py package build-exe --mode onefolder
```

## 고정 산출물 경로

- `dist/sdv_cli/sdv/`
- `dist/sdv_cli/sdv.exe`
- `dist/portable/sdv_portable/`
- `dist/portable/sdv_portable.zip`
- `build/pyinstaller/`
- `build/spec/`
- `artifacts/verification_runs/<run_id>/<phase>/`

이 경로는 release layout contract로 고정되어 있습니다.

최종 검증 아카이브는 아래 4축으로 봅니다.

- `reports/`
  - doctor / readiness / batch / junit / surface summary
- `surface/`
  - `BCM`, `IVI`, `CLUSTER`, `ADAS`, `V2X`, `CGW` ... 기준 reviewer bundle
- `native_reports/`
  - Dev1 native CANoe `.vtestreport` 원본
- `evidence/`
  - `UT / IT / ST` raw evidence/log copy
- `manifests/`
  - `artifact_manifest.*`
  - `execution_manifest.*`

## 운영 원칙

- public surface는 `product/sdv_operator` 기준으로 묶습니다.
- 구현 전체를 제품으로 보지 않습니다.
- 패키징은 manifest 기준 범위만 포함합니다.
- reviewer-facing 검증 결과는 `surface_evidence_bundle.*`와 `surface/<bundle_key>/*`까지 포함합니다.
- reviewer-facing 식별자는 `Surface ECU / Req / TestCase / Scenario`입니다.
- execution 식별자는 `run_id / phase / owner / run_date`입니다.
- staging 결과는 `canoe/tmp/reports/verification`에 남겨두되, 배포/보관/CI 아카이브는 `artifacts/verification_runs`만 기준으로 봅니다.
- 배포 전에는 `validate-contract -> build-exe -> bundle-portable` 순서로 진행합니다.
