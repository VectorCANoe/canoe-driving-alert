# 저장소 표면

이 저장소는 하나의 제품 폴더만 있는 구조가 아닙니다.
대신 다음 세 표면을 분리해서 운영합니다.

## 1. SDV Operator 표면

- 위치: `product/sdv_operator/`
- 대상: 검증 실행자, 패키징, TUI/CLI 사용자
- 역할:
  - 실행 진입점
  - 결과 검토
  - 패키징 경계

## 2. CANoe Runtime 표면

- 위치: `canoe/`
- 대상: CANoe runtime 유지 담당자
- 역할:
  - cfg
  - CAPL
  - DBC
  - SysVar / panel
  - native CANoe tests

## 3. Canonical Docs 표면

- 위치: `driving-situation-alert/`
- 대상: 요구사항/설계/검증 문서 작성자
- 역할:
  - `00~07` 정본 문서
  - 제출본 편집
  - traceability 유지

## 내부 작업면

다음 경로는 저장소에 남아 있지만 public first-read surface는 아닙니다.

- `driving-situation-alert/tmp/`
- `docs/`
- `reference/`
- `canoe/tmp/`

이 경로들은 추적성, 제출 편집, 내부 판단 근거 때문에 유지됩니다.

## 권장 진입 순서

1. 루트 `README.md`
2. `product/sdv_operator/README.md`
3. `canoe/README.md`
4. `driving-situation-alert/README.md`
