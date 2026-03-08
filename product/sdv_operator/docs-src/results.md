# 결과 해석

## 결과 화면이 보여줘야 하는 것

1. PASS / WARN / FAIL
2. 왜 그렇게 판정됐는지 한 줄 이유
3. 다음 액션
4. 증빙 경로
5. COM 상태

## 기본 판단 축

### PASS
- 핵심 명령이 정상 종료
- 필요한 산출물이 생성됨
- 준비 상태가 허용 범위 안에 있음

### WARN
- 실행은 됐지만 사람이 봐야 할 조건이 있음
- 예:
  - measurement stopped
  - ack timeout
  - readiness partial

### FAIL
- 실행 자체가 실패
- 예:
  - CANoe COM attach 실패
  - gate 실패
  - 필수 산출물 생성 실패

## 병목 해석

우리는 다음 소스에서 병목을 읽는다.

- stdout/stderr 로그
- `run_readiness.json`
- `dev2_batch_report.json`
- doctor report

즉, 수동 판단이 아니라 구조화된 산출물과 로그를 같이 사용한다.

## 증빙 원칙

- Markdown/JSON이 정본
- CSV는 선택 출력
- TUI는 그 결과를 읽어 보여주는 review surface
