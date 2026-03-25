# CANoe 문서 한글팩

이 폴더는 `canoe/docs/` 원문 문서를 따라가는 한국어 안내본 묶음입니다.

원칙:
- 기준 원문은 계속 `../` 아래 문서입니다.
- 한글 문서는 Git에서 빠르게 읽고 구조를 파악하기 위한 운영용 안내본입니다.
- technical identifier, ECU 이름, message name, test asset ID, SysVar name은 원문과 동일하게 유지합니다.
- 원문이 이미 한국어 중심으로 작성된 문서는 중복 번역 대신 원문으로 직접 연결합니다.

`Kor/` 전체는 한글 문서 묶음이고, 이 README 안의 "실제 제공 핵심 문서" 목록이 제출/검토에 바로 쓰는 선별 세트입니다.

## 우선 읽을 문서

### 완전 한국어판

1. [communication-matrix.md](./contracts/communication-matrix.md)
2. [layer-separation-policy.md](./contracts/layer-separation-policy.md)
3. [diagnostic-description.md](./contracts/diagnostic-description.md)
4. [diagnostic-matrix.md](./contracts/diagnostic-matrix.md)
5. [diagnostic-sysvar-contract.md](./contracts/diagnostic-sysvar-contract.md)
6. [test-asset-mapping.md](./verification/test-asset-mapping.md)
7. [execution-guide.md](./verification/execution-guide.md)
8. [VECTOR_ALIGNED_CLOSEOUT_STANDARD.md](./verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md)
9. [evidence-policy.md](./verification/evidence-policy.md)
10. [diagnostic-coverage.md](./verification/diagnostic-coverage.md)
11. [diagnostic-seam-design.md](./verification/diagnostic-seam-design.md)
12. [native-test-asset-naming.md](./verification/native-test-asset-naming.md)
13. [test-suite-composition.md](./verification/test-suite-composition.md)

### 안내본 / 진입점

1. [ethernet-backbone.md](./contracts/ethernet-backbone.md)
2. [acceptance-criteria.md](./verification/acceptance-criteria.md)
3. [oracle.md](./verification/oracle.md)
4. [ecu-classification.md](./architecture/ecu-classification.md)
5. [surface-runtime-verification-map.md](./architecture/surface-runtime-verification-map.md)
6. [gui-operations.md](./operations/gui-operations.md)
7. [run-procedure.md](./operations/run-procedure.md)

## 카테고리

- `contracts/`
  - 소유권, 메시지 경계, backbone contract, interface 관련 안내본
- `verification/`
  - test mapping, 실행 절차, closeout 기준, 증빙 정책 안내본

## 실제 제공 핵심 문서

### 핵심 계약 문서

1. [communication-matrix.md](./contracts/communication-matrix.md)
2. [layer-separation-policy.md](./contracts/layer-separation-policy.md)
3. [owner-route.md](./contracts/owner-route.md)
4. [multibus-policy.md](./contracts/multibus-policy.md)
5. [ethernet-interface.md](./contracts/ethernet-interface.md)
6. [panel-sysvar-contract.md](./contracts/panel-sysvar-contract.md)
7. [diagnostic-matrix.md](./contracts/diagnostic-matrix.md)
8. [diagnostic-sysvar-contract.md](./contracts/diagnostic-sysvar-contract.md)

### 핵심 검증 문서

1. [test-asset-mapping.md](./verification/test-asset-mapping.md)
2. [execution-guide.md](./verification/execution-guide.md)
3. [oracle.md](./verification/oracle.md)
4. [acceptance-criteria.md](./verification/acceptance-criteria.md)
5. [VECTOR_ALIGNED_CLOSEOUT_STANDARD.md](./verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md)
6. [evidence-policy.md](./verification/evidence-policy.md)
7. [diagnostic-coverage.md](./verification/diagnostic-coverage.md)

### 핵심 native asset guide

1. [test_units README.ko.md](../../tests/modules/test_units/README.ko.md)
2. [test_suites README.ko.md](../../tests/modules/test_suites/README.ko.md)

## 원문 인덱스

- 원문 루트: [../README.md](../README.md)

## 현재 포함 문서

### Contracts

- [communication-matrix.md](./contracts/communication-matrix.md)
- [layer-separation-policy.md](./contracts/layer-separation-policy.md)
- [ethernet-backbone.md](./contracts/ethernet-backbone.md)
- [owner-route.md](./contracts/owner-route.md)
- [multibus-policy.md](./contracts/multibus-policy.md)
- [ethernet-interface.md](./contracts/ethernet-interface.md)
- [panel-sysvar-contract.md](./contracts/panel-sysvar-contract.md)
- [diagnostic-matrix.md](./contracts/diagnostic-matrix.md)
- [diagnostic-sysvar-contract.md](./contracts/diagnostic-sysvar-contract.md)
- [diagnostic-description.md](./contracts/diagnostic-description.md)

### Architecture

- [ecu-classification.md](./architecture/ecu-classification.md)
- [surface-runtime-verification-map.md](./architecture/surface-runtime-verification-map.md)
- [skeleton.md](./architecture/skeleton.md)

### Operations

- [gui-operations.md](./operations/gui-operations.md)
- [sync-rule.md](./operations/sync-rule.md)
- [run-procedure.md](./operations/run-procedure.md)

### Verification

- [test-asset-mapping.md](./verification/test-asset-mapping.md)
- [execution-guide.md](./verification/execution-guide.md)
- [VECTOR_ALIGNED_CLOSEOUT_STANDARD.md](./verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md)
- [evidence-policy.md](./verification/evidence-policy.md)
- [oracle.md](./verification/oracle.md)
- [acceptance-criteria.md](./verification/acceptance-criteria.md)
- [diagnostic-coverage.md](./verification/diagnostic-coverage.md)
- [diagnostic-seam-design.md](./verification/diagnostic-seam-design.md)
- [native-test-asset-naming.md](./verification/native-test-asset-naming.md)
- [test-suite-composition.md](./verification/test-suite-composition.md)

## 동기화 규칙

- 원문 변경 후 의미가 바뀌면 한글 안내본도 함께 갱신합니다.
- 표 수치, pack count, active suite 구성, official closeout tier는 원문 기준으로만 해석합니다.
- 한글 안내본과 원문이 다르면 원문이 우선입니다.
