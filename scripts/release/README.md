# Release Scripts

? ??? `SDV Operator` ?? ???? ??? ????? ????.

## Fixed Artifact Paths

??? ??? ??? ?????.

- one-folder exe: `dist/sdv_cli/sdv/`
- one-file exe: `dist/sdv_cli/sdv.exe`
- portable folder: `dist/portable/sdv_portable/`
- portable zip: `dist/portable/sdv_portable.zip`
- PyInstaller work: `build/pyinstaller/`
- PyInstaller spec: `build/spec/`

? ??? `scripts/release/layout.py`? ???? ?????.

## Build sdv exe

??? ????:

- `python -m pip install pyinstaller`
- `python scripts/run.py package build-exe --mode onefolder --clean`
- `python scripts/run.py package build-exe --mode onefile --clean`

?? ??:

- `python scripts/release/build_sdv_exe.py --mode onefolder --clean`
- `python scripts/release/build_sdv_exe.py --mode onefile --clean`

## Build portable bundle

- `python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe`
- `python scripts/release/build_portable_bundle.py --mode onefolder --clean --rebuild-exe`
