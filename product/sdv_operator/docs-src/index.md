# SDV Operator

`SDV Operator`는 CANoe SIL 검증을 위한 Dev2 운영 콘솔입니다.

역할은 세 가지로 고정합니다.

1. 실행
   - `gate all`
   - `scenario run`
   - `verify quick`
2. 결과 확인
   - TUI 결과 카드
   - 로그 화면
   - 증빙 경로
3. 패키징
   - portable ZIP
   - Windows executable

## One-Line Flow

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

## 표면 원칙

- 실행 계층은 CLI입니다.
- 리뷰 계층은 TUI입니다.
- CANoe Panel은 별도 제품 조작 UI로 유지합니다.
- SDV Operator는 CANoe를 대체하지 않고, 검증 운영/리뷰 표면만 제공합니다.

## 문서 순서

1. Quickstart
2. Commands
3. Results
4. Packaging
5. Maintenance
6. Repo Surfaces
