# Native E2E Automation Plan

## 목적

이 문서는 `CANoe Test Verification Console`을 현재의 반자동 배치 표면에서
`native CANoe tier 실행 + evidence 자동 수집 + archive materialize`까지 포함하는
end-to-end 검증 실행기로 확장하기 위한 구현 기준을 정의합니다.

현재 baseline은 아래처럼 끊겨 있습니다.

- 제품:
  - `gate all`
  - `doctor`
  - `verify prepare`
  - `verify smoke`
  - `verify status`
  - `verify finalize`
  - `materialize`
- CANoe:
  - native `.vtestreport` 생성
  - Write Window evidence line 생성
  - trace/logging 생성
- 수동 단계:
  - native tier 실행
  - Write Window export 저장
  - trace/logging export 저장
  - `collect/post-run`

목표 baseline은 아래입니다.

1. 제품이 `UT/IT/ST/FULL` native tier 실행을 직접 트리거한다.
2. CAPL evidence line은 Write Window와 raw evidence file에 동시에 기록된다.
3. native report, raw evidence, supplementary trace/logging이 run 단위로 자동 수집된다.
4. `verify batch --phase full` 한 번으로 `execute -> collect -> finalize -> materialize`가 끝난다.

## 현재 문제 정의

현재 구조의 문제는 세 가지입니다.

1. `verify batch`가 native suite 실행을 하지 않는다.
2. `finalize`는 `raw_write_window.txt`가 이미 존재한다고 가정한다.
3. `incoming/<TIER>/`는 canonical drop root이지만 자동 생성 owner가 없다.

즉 현재는 `운영 오케스트레이션 + 정규화`는 있지만,
`native execution + evidence capture` owner가 비어 있는 상태입니다.

## 구현 원칙

1. `CANoe cfg` 직접 패치는 하지 않는다.
2. native `.vtestreport`는 CANoe 원본 증빙으로 계속 유지한다.
3. Write Window parser는 유지하되, GUI export 의존은 제거한다.
4. `run_id / phase / owner / tier`는 제품과 CAPL이 공유하는 고정 실행 계약으로 둔다.
5. `UT/IT/ST`는 official closeout tier, `FULL`은 regression-only wrapper로 유지한다.
6. first pilot은 `ST_ACTIVE_BASELINE`이다.

## Target Flow

```text
verify batch pre/full
  -> doctor / prepare / metadata seed
  -> native tier execute
  -> CAPL dual-write evidence
  -> collect native reports + trace/logging
  -> fill-score
  -> finalize
  -> surface bundle
  -> materialize archive
```

## Wave Plan

### Wave 0 - 계약 고정

목표:
- 제품과 CANoe가 같은 실행 계약을 보도록 고정한다.

제품 변경:
- native e2e 계약 파일 추가
- 문서에서 현재 반자동 경계와 목표 경계를 명시

CANoe 변경:
- 없음

완료 기준:
- `tier / suite / assign / report / incoming path`가 계약 파일로 고정됨
- 다음 wave 구현이 이 계약만 보고 진행 가능

### Wave 1 - Native Execute Pilot

목표:
- 제품이 `ST_ACTIVE_BASELINE` native tier 실행을 직접 트리거한다.

제품 변경:
- `verify batch` 또는 신규 `verify native-run` 경로에서 tier 실행 hook 추가
- 실행 시작/완료/실패 상태를 batch step으로 기록

CANoe 변경:
- 필요 시 CAPL helper function 또는 COM-visible hook 추가
- 단, GUI-only 설정 파일 직접 패치는 금지

완료 기준:
- 제품 표면에서 `ST_ACTIVE_BASELINE` 실행 가능
- `.vtestreport` summary/per-test 생성 확인
- batch report에 native execute step이 남음

### Wave 2 - Evidence Dual-Write

목표:
- `TEST_SCN`/shared harness evidence를 Write Window와 raw file에 동시에 기록한다.

제품 변경:
- run metadata를 CANoe로 주입
- raw evidence file path 규칙을 배치 metadata와 연결

CANoe 변경:
- 공통 include 또는 harness helper에서 evidence writer 추가
- `EVIDENCE_IN/OUT`를 dual-write로 확장
- `run_id / tier / owner / evidenceAutoWrite` 계약 수용

완료 기준:
- GUI export 없이 `canoe/logging/evidence/incoming/<TIER>/raw_write_window.txt`가 자동 생성됨
- 기존 parser가 그대로 `fill-score` 가능

현 시점 구현 상태:

- 제품은 native execute 직전에 `incoming/<TIER>/raw_write_window.txt`를 비우고
  evidence drop 디렉토리를 보장한다.
- CANoe harness는 `Test::nativeExecTierCode`, `Test::evidenceAutoWrite`를 보고
  `TEST_SCN`의 `[EVIDENCE_IN]`, `[EVIDENCE_OUT]`를 Write Window와 raw file에 동시 기록한다.
- 이 구현은 차량 비즈니스 로직이 아니라 SIL verification harness 책임으로
  `TEST_SCN.can`에 한정해 넣는다.

### Wave 3 - Collect/Post-Run Inline

목표:
- `verify batch`가 내부에서 `collect -> fill-score -> finalize`까지 이어서 처리한다.

제품 변경:
- post/full phase에 `collect/post-run` 내장
- `finalize` 호출 전에 tier evidence readiness 확인

CANoe 변경:
- trace/logging 경로가 제품 수집 규칙과 맞게 고정돼 있어야 함

완료 기준:
- 사용자가 `incoming` 폴더를 수동으로 만질 필요가 없음
- `verify batch --phase post/full`이 수집 포함 경로로 닫힘

### Wave 4 - Multi-Tier Expansion

목표:
- ST pilot을 `UT`, `IT`, `FULL`로 확장한다.

제품 변경:
- campaign/profile에서 tier별 native execute 매핑 확대
- `batch report`, `surface bundle`, `execution manifest`에 execute step 반영

CANoe 변경:
- tier별 evidence path 안정화
- per-tier supplementary trace/logging 수집 규칙 검증

완료 기준:
- `UT/IT/ST/FULL` 모두 제품 표면에서 일관된 실행 가능
- Jenkins가 `verify batch` 결과만으로 archive 수집 가능

## 구현 경계

### 제품 책임

- 실행 metadata seed
- native tier execution orchestration
- collect/fill/finalize/materialize chaining
- batch/surface/archive/report generation

### CANoe 책임

- native `.vtestreport` 생성
- CAPL evidence line 생성
- trace/logging 산출
- runtime observable state 제공

### 공통 계약

- tier id
- suite id
- assign folder
- summary report path
- per-test report root
- incoming raw evidence path
- supplementary trace/logging path
- run metadata fields

## 제안 Control Contract

### 제품 -> CANoe

제품은 최소 아래 실행 metadata를 내려야 합니다.

- `run_id`
- `phase`
- `owner`
- `tier`
- `profile_id`
- `pack_id`
- `surface_scope`
- `evidence_auto_write`

### CANoe -> 제품

CANoe는 최소 아래 실행 상태를 올려야 합니다.

- `native execution accepted`
- `native execution running`
- `native execution finished`
- `native execution verdict`
- `native report path ready`
- `raw evidence file ready`

## 제안 Interface Shape

현재 후보는 두 가지입니다.

1. COM native execution bridge
   - 장점: 제품이 실행 제어를 직접 소유
   - 단점: CANoe TEST object model binding을 추가로 검증해야 함

2. CAPL helper + sysvar handshake
   - 장점: 현재 `scenario run` 구조와 유사해 구현 일관성이 높음
   - 단점: native test UI와 직접 연결되지 않으면 중간 래퍼가 더 필요

현재 권장안은 `Wave 1`에서 ST pilot만 좁게 COM native execution bridge로 검증하고,
불안정하면 `CAPL helper + sysvar handshake` 보조 경로를 붙이는 방식입니다.

현 시점 확인 결과:

- `CANoe.Application.Configuration.TestConfigurations` COM 컬렉션에서
  `UT_ACTIVE_BASELINE`, `IT_ACTIVE_BASELINE`, `ST_ACTIVE_BASELINE`가 직접 조회됩니다.
- 즉 `Wave 1`은 별도 GUI macro 없이 COM native execution bridge로 시작할 수 있습니다.
- `FULL`은 현재 native `TestConfiguration`으로 노출되지 않으므로 후속 wave에서 별도 래핑이 필요합니다.

## 권장 우선순위

1. `Wave 0`
2. `Wave 1` with `ST_ACTIVE_BASELINE`
3. `Wave 2`
4. `Wave 3`
5. `Wave 4`

## 완료 기준

최종적으로 아래가 되면 end-to-end 자동화가 닫힌 것으로 봅니다.

1. 사용자가 제품에서 `verify batch --phase full`만 실행한다.
2. 제품이 native tier를 실행한다.
3. raw evidence와 native report와 supplementary trace/logging이 자동 수집된다.
4. `verification_log_scored.csv`, `surface bundle`, `execution manifest`, `archive`가 자동 생성된다.
5. 사용자는 CANoe GUI에서 수동 export를 하지 않는다.

## 공식 Report Tooling 경로

native `.vtestreport` 후처리는 Vector 공식 tooling을 우선 사용한다.

- CLI
  - `ReportViewerCli.exe`
  - 용도: `XML`, `XUnit`, 선택적 `PDF` export
- .NET API
  - `Vector.ReportViewer.DataApi`
  - `Vector.ReportViewer.DataApi.DiVa`
  - 용도: immutable native report 구조 조회
- 공식 help
  - `ctrvusage.htm`
  - `ctrvdataapi.htm`
  - `VectorCANoeTestReportViewerDataAPI.htm`

제품 staging 출력은 아래에 고정한다.

- `canoe/tmp/reports/verification/official_report_tooling.json`
- `canoe/tmp/reports/verification/official_report_manifest.json`
- `canoe/tmp/reports/verification/official_report_manifest.md`
- `canoe/tmp/reports/verification/official_reports/<TIER>/...`

운영 원칙은 다음과 같다.

1. native 실행 직후 제품이 공식 CLI export를 수행한다.
2. 이어서 공식 Data API snapshot을 JSON으로 생성한다.
3. 제품은 XML/XUnit/Data API 결과를 병합해 fail triage에 사용한다.
4. staging 산출물은 archive materialize에 함께 포함한다.

### 공식 도구 우선순위

| 구분 | 컴포넌트 | 제품 사용 여부 | 역할 |
|---|---|---|---|
| Mandatory | `ReportViewerCli.exe` | 필수 | official `XML/XUnit/PDF` export |
| Mandatory | `Vector.ReportViewer.DataApi` | 필수 | official native report parse |
| Recommended | `CANoe Test Report Viewer` | 권장 | 사람이 `.vtestreport`를 직접 여는 fallback |
| Optional | `ReportViewerSelector.exe` | 선택 | viewer launch helper |

운영 규칙은 고정한다.

1. 제품 자동화는 반드시 `CLI + Data API` 조합을 사용한다.
2. GUI Viewer는 운영자 검토 fallback으로 유지한다.
3. Selector는 설치돼 있으면 기록하되, primary pipeline 의존성으로 두지 않는다.
