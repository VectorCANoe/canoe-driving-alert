# SDV Operator

`SDV Operator`는 CANoe SIL 검증을 위한 실행 런처이자 결과 검토 콘솔입니다.

이 문서 세트는 제품 표면만 다룹니다. 내부 handoff, mentoring, submission workspace는 여기서 직접 설명하지 않습니다.

## What It Does

- `gate all` 실행
- `scenario run` 주입
- `verify quick` 기반 증빙/준비 상태 확인
- `PASS / WARN / FAIL`, COM 상태, 증빙 경로, 병목 검토
- portable ZIP / exe 패키징

## What It Does Not Do

- CANoe panel 대체
- CAPL / DBC / SysVar 자체 소유
- CANoe cfg 운영 대체

## Core Flow

1. `python scripts/run.py`
2. `Gate all`
3. `Scenario run`
4. `Verify quick`
5. `Results / Logs` 확인

## Read Next

- [빠른 시작](quickstart.md)
- [명령 참고](commands.md)
- [결과 해석](results.md)
- [패키징](packaging.md)
- [유지보수](maintenance.md)

## Documentation Policy

- Markdown이 정본입니다.
- HTML은 generated site입니다.
- 사용자 표면은 단순하게 유지합니다.
- 내부 구현과 작업 문서는 제품 표면에서 직접 노출하지 않습니다.
