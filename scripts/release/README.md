# Release Scripts

이 폴더는 `SDV Operator` 패키징 산출물을 만드는 내부 빌드 스크립트 모음입니다.

## Fixed Artifact Paths

출력 경로는 아래처럼 고정합니다.

- one-folder exe: `dist/sdv_cli/sdv/`
- one-file exe: `dist/sdv_cli/sdv.exe`
- portable folder: `dist/portable/sdv_portable/`
- portable zip: `dist/portable/sdv_portable.zip`
- PyInstaller work: `build/pyinstaller/`
- PyInstaller spec: `build/spec/`

이 경로는 `scripts/release/layout.py`를 기준으로 공유합니다.

## Build sdv exe

권장 경로:

- `python -m pip install pyinstaller`
- `python scripts/run.py package build-exe --mode onefolder --clean`
- `python scripts/run.py package build-exe --mode onefile --clean`

직접 실행:

- `python scripts/release/build_sdv_exe.py --mode onefolder --clean`
- `python scripts/release/build_sdv_exe.py --mode onefile --clean`

## Build portable bundle

- `python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe`
- `python scripts/release/build_portable_bundle.py --mode onefolder --clean --rebuild-exe`
