# 빠른 시작

## 1. 기본 실행

```powershell
python scripts/run.py
```

기본 실행은 Verification Console 화면을 엽니다.  
터미널 호환성 문제로 화면형 콘솔을 쓰기 어렵다면 plain shell로 전환합니다.

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
python scripts/run.py verify batch --run-id 20260310_0900 --campaign-id CMP_20260310 --owner DEV2 --phase pre --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0 --report-formats json,md,junit
```

현재 권장 verification pack 축:

- `ts_canoe_ut_active_baseline`
- `ts_canoe_it_active_baseline`
- `ts_canoe_st_active_baseline`
- `ts_canoe_full_active_baseline`

즉 제품은 현재 executable CANoe suite 기준으로 UT/IT/ST/FULL을 분리해서 운영합니다.

## 3. 점검 명령

```powershell
python scripts/run.py doctor
```

이 명령은 다음을 빠르게 확인합니다.

- CANoe COM attach 가능 여부
- measurement running 여부
- 핵심 sysvar 접근 가능 여부

## 4. Verification Console 기본 흐름

1. Home에서 핵심 작업 선택
2. Run 화면에서 범주 버튼과 Task list를 통해 작업 선택
3. Quick form에 필요한 값 입력
4. Run now 실행
5. Logs에서 실시간 출력 확인
6. Results에서 최근 판정과 연결 산출물을 먼저 확인
7. Automation에서 운영 profile과 active suite pack을 선택
8. Artifacts에서 `staging / archive / source / build` 네 영역을 구분해 확인하고 필요하면 `surface archive`까지 바로 연다
9. closeout 직전에는 `verify finalize` 또는 `run insight / doc binding bundle / doc fill template`를 확인한다

## 5. Campaign 메타데이터

Verification Console은 단순 실행기보다 한 단계 위의 운영 계층입니다.  
그래서 batch/precheck에는 아래 메타데이터를 함께 남깁니다.

- `run_id`
  - 이번 한 번의 실행 묶음 식별자
- `campaign_id`
  - nightly/repeat/CI 묶음 식별자
- `surface_scope`
  - reviewer-facing으로 집중해서 볼 surface ECU 범위
- `repeat_count / duration_minutes / interval_seconds`
  - 반복 실행 의도와 운영 profile 기록

즉 OEM/CI 관점에서는:

- `Req / TestCase / Surface ECU / Scenario` = stable trace key
- `run_id / campaign_id / phase` = execution key

관련 원본:

- `artifact open --target campaign-profiles`
- `artifact open --target unit-test-doc`
- `artifact open --target integration-test-doc`
- `artifact open --target system-test-doc`
- `artifact open --target test-asset-mapping`
- `artifact open --target active-test-units-guide`
- `artifact open --target active-test-suites-guide`
- `artifact open --target execution-guide`
- `artifact open --target run-insight`
- `artifact open --target doc-binding-bundle`
- `artifact open --target doc-fill-template`
- `artifact open --target verification-pack-matrix`
- `artifact open --target role-boundary-doc`
- `artifact open --target capability-matrix-doc`
- `artifact list --scope build`
- `artifact open --target surface-dir --latest`
