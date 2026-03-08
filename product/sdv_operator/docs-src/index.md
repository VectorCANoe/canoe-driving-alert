# SDV Operator

`SDV Operator`는 CANoe SIL 검증을 위한 실행 런처이자 결과 검토 콘솔입니다.

이 문서 세트는 제품 표면만 다룹니다.
내부 handoff, mentoring, submission workspace는 여기서 직접 설명하지 않습니다.

## 제품 역할

- 검증 실행 진입점 제공
- COM 상태와 검증 결과를 빠르게 읽게 함
- 증빙 경로와 병목을 한 화면에서 확인하게 함
- portable ZIP / exe 패키징 표면 제공

## 제품이 하지 않는 일

- CANoe panel 대체
- CAPL / DBC / SysVar 자체 소유
- CANoe cfg 운영 대체

## 기본 운영 흐름

1. `python scripts/run.py`
2. `Gate all`
3. `Scenario run`
4. `Verify quick`
5. `Results / Logs` 확인

## 권장 읽기 순서

1. [빠른 시작](quickstart.md)
2. [저장소 표면](repo-surfaces.md)
3. [명령 체계](commands.md)
4. [결과 해석](results.md)
5. [패키징 범위](packaging.md)
6. [유지보수 경계](maintenance.md)

## 문서 정책

- Markdown이 정본입니다.
- HTML은 생성된 문서 표면입니다.
- 내부 구현과 운영 문서는 제품 표면에서 직접 노출하지 않습니다.
