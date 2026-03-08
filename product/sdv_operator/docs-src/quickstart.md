# 빠른 시작

## 1. 설치

저장소 루트에서:

```powershell
python -m pip install -e .
```

문서 사이트까지 빌드하려면:

```powershell
python -m pip install -e .[docs]
```

## 2. 실행

기본 TUI:

```powershell
python scripts/run.py
```

plain shell:

```powershell
python scripts/run.py shell
```

## 3. 일일 핵심 명령

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
python scripts/run.py doctor
```

## 4. 먼저 볼 문서

1. 루트 `README.md`
2. `product/sdv_operator/README.md`
3. [저장소 표면](repo-surfaces.md)
4. [명령 체계](commands.md)

## 5. 운영 규칙

- 일반 사용자는 `scripts/run.py`만 진입점으로 사용
- 숨겨진 alias는 호환성 유지용일 뿐, 운영 표면으로 쓰지 않음
- 생성 산출물은 소스처럼 다루지 않음
