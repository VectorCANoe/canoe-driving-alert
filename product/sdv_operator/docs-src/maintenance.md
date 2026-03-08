# 유지보수 경계

## Dev1과 Dev2 경계

### Dev1
- `canoe/`
- cfg
- panel
- sysvars
- DBC
- CAPL
- CANoe runtime behavior

### Dev2
- SDV Operator 제품 표면
- CLI/TUI
- gate 실행
- verification/evidence 실행 진입점
- packaging

## 현재 제품 경계

참조 문서:

- `product/sdv_operator/README.md`
- `product/sdv_operator/manifest.json`
- `scripts/MAINTENANCE_MAP.md`

## 리팩터링 원칙

지금은 물리 이동보다 논리 경계가 우선이다.

1. 제품 경계 먼저 고정
2. 호환 경로 유지
3. 실제 제품 소유 코드만 점진적으로 승격
4. helper/legacy는 필요할 때만 이동

## 복잡도 규칙

질문이 길어지면 구조가 잘못된 것이다.
운영자가 기억해야 할 것은 아래면 충분해야 한다.

- `python scripts/run.py`
- `gate all`
- `scenario run`
- `verify quick`
- `doctor`
