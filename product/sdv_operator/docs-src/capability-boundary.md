# Capability Boundary

이 문서는 `CANoe TEST`, `Jenkins`, `CANoe Test Verification Console`의 역할 경계를 한 표면에서 다시 확인하기 위한 문서입니다.

## 핵심 원칙

- `CANoe TEST`는 native test asset과 native execution을 담당합니다.
- `Jenkins`는 scheduling, retry, timeout, archive를 담당합니다.
- `CANoe Test Verification Console`은 campaign metadata, evidence normalization, reviewer-facing surface ECU 결과 묶음을 담당합니다.

## 우리가 만들지 않는 것

- CANoe Test authoring tool 재구현
- Jenkins scheduler 재구현
- CANoe Panel 대체 GUI

## 우리가 반드시 담당하는 것

- `gate all`, `doctor`, `scenario run`, `verify batch` 같은 운영 흐름
- `surface_evidence_bundle.*`
- `execution_manifest.*`
- `native report + batch report + source contract`를 한 run 흐름으로 따라가는 review surface

## 제품 섹션 기준

- `Home`
  - 현재 상태와 다음 조치
- `Run`
  - scenario / phase / execution metadata
- `Results`
  - verdict / evidence / surface ECU summary
- `Artifacts`
  - staging / archive / source / build
- `Automation`
  - Jenkins / execution profiles / active suite pack
- `Logs`
  - raw stdout/stderr review

## 관련 원본

- `product/sdv_operator/config/capability_boundary_matrix.json`
- `product/sdv_operator/docs-src/role-boundary.md`
- `product/sdv_operator/docs-src/campaign-profiles.md`
- `product/sdv_operator/docs-src/ci-bridge.md`
