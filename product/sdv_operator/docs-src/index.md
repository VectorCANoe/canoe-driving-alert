# SDV Operator

`SDV Operator`는 CANoe를 대체하는 도구가 아닙니다.

역할은 세 가지입니다.

1. 검증 실행 진입점 제공
2. CANoe COM 상태와 검증 결과를 빠르게 읽게 함
3. 증빙 경로와 병목을 한 화면에서 확인하게 함

## 제품 범위

이 제품은 다음을 담당합니다.

- `gate all`
- `scenario run`
- `verify quick`
- TUI/CLI 실행 표면
- 검증 증빙 생성/확인 진입점
- portable ZIP / exe 패키징

이 제품이 하지 않는 일:

- CANoe 패널 재구현
- CAPL/DBC/sysvar 자체 소유
- CANoe cfg 운영 대체

## 기본 사용 흐름

1. `python scripts/run.py`
2. `Gate all`
3. `Scenario run`
4. `Verify quick`
5. `Results / Logs` 확인

## 원칙

- 내부 구현은 복잡해도 됨
- 사용자 표면은 단순해야 함
- 문서 정본은 Markdown
- HTML은 생성물
