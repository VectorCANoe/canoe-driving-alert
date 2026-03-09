# Verification Staging

이 폴더는 Dev2 검증 실행의 **staging output** 전용입니다.

- 예:
  - `doctor_report.*`
  - `run_readiness.*`
  - `dev2_batch_report.*`
  - `surface_evidence_bundle.*`
  - `surface/<bundle_key>/*`

운영 원칙:

1. 이 경로의 파일은 실행 결과이며 **정본 소스가 아닙니다**.
2. Git 추적 대상이 아니며, 실행할 때마다 다시 생성됩니다.
3. reviewer/Jenkins 기준 최종 보관 경로는 아래입니다.
   - `artifacts/verification_runs/<run_id>/<phase>/...`
4. 정리 명령:
   - `python scripts/run.py package clean --scope staging --yes`
