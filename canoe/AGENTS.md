# AGENTS.md (scope: `canoe/`)

## MCP CANoe 운영 규칙 (필수)

자동화 충돌(`User interface is busy`) 방지를 위해, CANoe 제어는 아래 순서를 강제한다.

1. 병렬 호출 금지
- CANoe MCP 관련 호출은 반드시 순차 1개씩 실행한다.
- `multi_tool_use.parallel`로 CANoe MCP 도구를 동시에 호출하지 않는다.

2. 측정 시작 표준 시퀀스 고정
- 항상 아래 순서만 사용한다.
- `open_configuration -> wait(2~3s) -> compile_capl_nodes -> wait(2~3s) -> start_measurement`

3. busy 발생 시 즉시 중단 + 재시도 루틴
- `busy` 또는 `User interface is busy` 발생 시 즉시 추가 호출 중단.
- 쿨다운 `2~3s` 후 `get_connection_status` 1회 확인.
- 측정 중이면 `stop_measurement` 1회 실행.
- `open_configuration` 1회 재시도.
- 재시도 최대 2회. 실패 시 무한 반복 금지, 즉시 상태 보고.

4. 검증 실행 원칙
- FZ 실측은 `FZ_001 -> FZ_007` 순차 실행.
- 각 케이스는 `입력 설정 -> 대기 -> 관측 -> 판정` 단일 트랜잭션으로 종료 후 다음 케이스 진행.
- 케이스 도중 구성 재오픈/재컴파일 금지(복구 루틴에서만 허용).

5. 범위 제한
- 구현 변경은 `canoe/` 폴더만 허용.
- `driving-situation-alert/00~07` 문서는 참고용이며 자동 수정 금지.

## Repository Boundary (Non-Negotiable)
- DO NOT modify any file under `C:\Users\이준영\CANoe-IVI-OTA\driving-situation-alert`.
- That folder is source-of-truth documentation and is read-only for implementation tasks.
- Only `C:\Users\이준영\CANoe-IVI-OTA\canoe` can be changed during development.
