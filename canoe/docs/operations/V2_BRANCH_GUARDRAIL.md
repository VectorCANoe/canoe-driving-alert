# v1/v2 Branch Guardrail

## 목적
- 운영 안정성(v1) 유지 상태에서 아키텍처 변경(v2)을 병렬 개발한다.

## 브랜치 규칙
1. `main` 또는 운영 브랜치 = v1 (운영 안정판)
2. `feature/v2-render-adapter-*` = v2 (아키텍처 변경판)
3. v2는 v1 동작을 깨뜨리지 않는 범위로만 머지한다.

## 머지 전 필수 게이트
1. cfg hygiene
```powershell
python scripts/quality/cfg_hygiene_gate.py
```
2. doc-code sync
```powershell
python scripts/quality/doc_code_sync_gate.py
```
3. 시나리오 재실행
- `FZ_001` ~ `FZ_007` 순차 재실행
- 증적: Trace + Panel 캡처 2종

## PASS 기준 고정
- 입력 주기: `100ms`
- 출력 주기: `50ms`
- 즉시 반영: `150ms` 이내
- 타임아웃 해제: `1000ms`

## 문서 연계
- Unit: `driving-situation-alert/05_Unit_Test.md`
- Integration: `driving-situation-alert/06_Integration_Test.md`
- System: `driving-situation-alert/07_System_Test.md`
