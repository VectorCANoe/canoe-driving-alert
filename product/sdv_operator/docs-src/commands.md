# 명령 체계

## 핵심 4개

### Gate all

```powershell
python scripts/run.py gate all
```

용도:
- 사전 정합 점검
- 문서/코드/구성 드리프트 탐지

### Scenario run

```powershell
python scripts/run.py scenario run --id 4
```

용도:
- CANoe COM으로 시나리오 주입
- 수동 패널 없이 검증 경로 트리거

### Verify quick

```powershell
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

용도:
- 준비/상태/기본 검증 경로를 한 번에 수행

### Doctor

```powershell
python scripts/run.py doctor
```

용도:
- CANoe COM 연결
- measurement 상태
- 기본 sysvar 가시성

## 보조 명령

상세 명령은 아래 문서를 기준으로 본다.

- `scripts/COMMAND_REFERENCE.md`

## 원칙

- 운영 문서는 canonical 명령만 사용
- hidden alias는 기존 습관 보호용
- 사용자에게는 최소 표면만 보여줌
