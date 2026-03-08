# 빠른 시작

## 1. 기본 실행

```powershell
python scripts/run.py
```

기본 실행은 Textual TUI를 엽니다.  
터미널 호환성 문제로 TUI를 쓰기 어렵다면 plain shell로 전환합니다.

```powershell
python scripts/run.py shell
```

## 2. 핵심 3단계

### Gate

```powershell
python scripts/run.py gate all
```

### Scenario

```powershell
python scripts/run.py scenario run --id 4
```

### Verify

```powershell
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

## 3. 점검 명령

```powershell
python scripts/run.py doctor
```

이 명령은 다음을 빠르게 확인합니다.

- CANoe COM attach 가능 여부
- measurement running 여부
- 핵심 sysvar 접근 가능 여부

## 4. TUI 기본 흐름

1. Home에서 핵심 작업 선택
2. Execute에서 필요한 값 입력
3. Run now 실행
4. Logs에서 실시간 출력 확인
5. Results에서 verdict, COM 상태, 증빙 경로 확인
