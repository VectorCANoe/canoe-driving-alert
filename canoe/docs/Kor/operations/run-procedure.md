# Run Procedure 한글판

원문:
- [../../operations/run-procedure.md](../../operations/run-procedure.md)

## 목적

이 문서는 현재 active CANoe baseline에 대해 `import -> compile -> run -> evidence` 절차를 정의합니다.

## 표준 절차

1. active configuration을 CANoe GUI에서 연다.
2. 필요한 node visibility와 database assignment를 복원한다.
3. panel과 SysVar surface가 로드되었는지 확인한다.
4. active CAPL 변경을 `src/capl/`에서 `cfg/channel_assign/`로 sync한다.
5. CAPL node를 compile한다.
6. measurement 또는 native Test Unit execution을 시작한다.
7. verdict, report, supporting evidence를 수집한다.
8. run이 official이면 reviewer-facing verification record까지 업데이트한다.

## 기대 출력

- compile result
- runtime verdict 또는 Test Unit verdict
- native Test Unit 사용 시 report path
- evidence policy가 요구하면 screenshot 또는 write-window capture

## 작업 규칙

- compile success와 runtime success는 별도 gate로 취급합니다.
- runtime delivery가 불확실하면 configuration만 보고 맞다고 추정하지 않고 `pending`으로 보고합니다.
- GUI-first operation은 [../../operations/gui-operations.md](../../operations/gui-operations.md)를 우선 따릅니다.
