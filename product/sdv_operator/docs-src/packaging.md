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

이 경로는 release layout contract로 고정되어 있습니다.

## 운영 원칙

- public surface는 `product/sdv_operator` 기준으로 묶습니다.
- 구현 전체를 제품으로 보지 않습니다.
- 패키징은 manifest 기준 범위만 포함합니다.
- 배포 전에는 `validate-contract -> build-exe -> bundle-portable` 순서로 진행합니다.
