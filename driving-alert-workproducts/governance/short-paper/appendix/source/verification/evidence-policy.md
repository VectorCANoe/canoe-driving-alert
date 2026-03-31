# 검증 증빙 로그 표준 (CANoe SIL)

원문:
- [../../verification/evidence-policy.md](../../verification/evidence-policy.md)

동기화 기준:
- `5d83ee7f`
- 원문이 이미 한국어 중심으로 유지되므로 `ko/` mirror는 canonical 내용을 그대로 따라갑니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> runtime, diagnostic, verification 세부사항 가운데 일부는 아직 구현 중이며 변경될 수 있습니다.

관련 운영 표준:
- `canoe/docs/verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`

## 1) 목적
| 항목 | 기준 |
| --- | --- |
| 로그 포맷 | `05/06/07` 증빙 로그 포맷 통일 |
| 검증 축 | `로직 / 통신 / 주기` 분리 |
| 실측 기반 | 실측 없는 PASS 금지 |

## 2) 고정 실행 순서
| 단계 | 내용 |
| --- | --- |
| 1 | 컴파일 + 핵심 경로 확인 |
| 2 | `verification_log.csv` 채우기 |
| 3 | `50/100/150/1000ms` 채점 |
| 4 | 차량/제어/모니터 캡처 |
| 5 | `05/06/07` 판정 반영 |

## 3) 개발완성도 체크 기준 (Step 1)
| 항목 | 기준 |
| --- | --- |
| 컴파일 | 에러 0건 |
| 측정 시작 | 측정 시작 성공 |
| 파생 출력 | scenario 주입 시 아래 파생 출력이 유효값으로 변해야 한다. |

| 출력 그룹 | 확인 값 |
| --- | --- |
| `Core` | `selectedAlertLevel`, `selectedAlertType` |
| `Body` | `ambientMode`, `ambientColor`, `ambientPattern` |
| `Cluster` | `warningTextCode` |
| `UiRender` | `renderMode`, `renderColor`, `renderTextCode` |

## 4) 증빙 폴더 규칙
루트는 `canoe/logging/evidence/`를 사용한다.

| Tier | 경로 | 비고 |
| --- | --- | --- |
| `UT` | `UT/<run_id>/` | 단위시험 run 폴더 |
| `IT` | `IT/<run_id>/` | 통합시험 run 폴더 |
| `ST` | `ST/<run_id>/` | 시스템시험 run 폴더 |
| `FULL` | `FULL/<run_id>/` | 회귀 전용, 공식 closeout seed 없음 |

| 파일/폴더 | 역할 |
| --- | --- |
| `verification_log.csv` | 시험별 판정 로그 |
| `raw_write_window.txt` | Write Window 원본 |
| `capture_index.csv` | 캡처 파일 매핑 |
| `captures/` | 차량/제어/모니터 캡처 |
| `native_reports/` | native report 보관 |
| `native_report_manifest.json` | native report 목록 |
| `supplementary/trace/` | CAN/Ethernet trace 보관 |
| `supplementary/logging/` | logging block 출력 보관 |

### Write Window Drop Root
루트는 `canoe/logging/evidence/incoming/`를 사용한다.

| Tier | 표준 저장 파일 |
| --- | --- |
| `UT` | `UT/raw_write_window.txt` |
| `IT` | `IT/raw_write_window.txt` |
| `ST` | `ST/raw_write_window.txt` |
| `FULL` | `FULL/raw_write_window.txt` |

GUI의 Write Window export 기본 경로는 위 경로로 고정한다. `post-run` 자동화는 위 표준 경로를 우선 수집하고, 기존 `canoe/tmp/write_window/`는 migration fallback으로만 사용한다.

### Trace and Logging Drop Root
루트는 `canoe/logging/evidence/incoming/`를 사용한다.

| 종류 | 표준 supplementary 경로 |
| --- | --- |
| `trace` | `UT~FULL/trace/` |
| `logging` | `UT~FULL/logging/` |

CAN/Ethernet trace export, logging block output, BLF/ASC/MF4/PCAP 계열 산출물은 위 경로에 저장한다. `post-run`은 위 경로를 자동 수집해 run-local `supplementary/trace`, `supplementary/logging`으로 복사한다.

### Write Window 키워드 규칙
| 구분 | 키워드 |
| --- | --- |
| 입력 이벤트 | `[EVIDENCE_IN]` |
| 출력 이벤트 | `[EVIDENCE_OUT]` |
| 시간 계산 | `inputTsMs/outputTsMs -> latency_ms` |

- 입력 형식: `scenario=<id> inputTsMs=<ms>`
- 출력 형식: `scenario=<id> outputTsMs=<ms> result=<0|1> ...`

### Seed Source 규칙
`verification_log.csv` 초기 row는 수동 템플릿 복사가 아니라 `scripts/quality/init_evidence_run.py`로 생성한다.

| Seed SoT | 용도 |
| --- | --- |
| `05_Unit_Test.md` | 단위시험 seed |
| `06_Integration_Test.md` | 통합시험 seed |
| `07_System_Test.md` | 시스템시험 seed |
| `test-asset-mapping.md` | 자산-시험 매핑 |
| `<asset>.can` | native asset 근거 |

`expected`는 공식 `05/06/07` 표에서 추출하고, `scenario_id`는 native CAPL의 `launchScenarioAndWait(...)` 호출에서 시드한다. `rule_type` / `rule_ms`는 공식 표 문장 기준으로 정리하며, 애매한 row는 `note`에 manual confirmation을 남긴다. `FULL`은 regression tier이므로 `prepare` seed 대상이 아니며 `collect/post-run`으로 native report와 raw log만 저장한다.

## 5) verification_log.csv 필수 컬럼
| 컬럼 | 의미 |
| --- | --- |
| `tier` | `UT|IT|ST` |
| `test_id` | 시험 ID |
| `native_asset` | native test asset |
| `scenario_id` | 시나리오 ID |
| `input_ts_ms` | 입력 시각 |
| `output_ts_ms` | 출력 시각 |
| `latency_ms` | 지연 시간, 비어 있어도 채점기가 계산 |
| `rule_type` | `LE|GE|BETWEEN|EQ` |
| `rule_ms` | 예) `150`, `1000`, `1000:1300` |
| `expected` | 기대 결과 |
| `observed` | 관찰 결과 |
| `logic_verdict` | `PASS|FAIL` |
| `comm_verdict` | `PASS|FAIL` |
| `verdict` | 수동 입력값(선택), 최종 판정은 `computed_verdict` 기준 |
| `owner` | 실행 담당자 |
| `run_date` | `YYYY-MM-DD` |
| `evidence_log_path` | 로그 경로 |
| `evidence_capture_path` | 캡처 경로 |
| `note` | 메모 |

### 관찰 문자열(observed) 표준
`observed`는 현재 `[EVIDENCE_OUT]`의 핵심 필드를 key/value 문자열로 저장한다.

| 구분 | 필드 |
| --- | --- |
| 기본 포함 | `level`, `type`, `code`, `timeout`, `risk` 등 |
| 선택 포함 | `release`, `objValid`, `objClass`, `objTtc` 등 |

## 6) 판정 규칙
### 6.1 주기(Period)
| 규칙 | 의미 |
| --- | --- |
| `LE` | `latency_ms <= rule_ms` |
| `GE` | `latency_ms >= rule_ms` |
| `BETWEEN` | `min <= latency_ms <= max` |
| `EQ` | `latency_ms == rule_ms` |

### 6.2 로직(Logic)
- 로직 기대값(`expected`)과 실제 상태(`observed`)를 비교해 `logic_verdict`를 기록합니다.

### 6.3 통신(Comm)
- 기대 경로의 파생 출력 반영 여부를 `comm_verdict`로 기록합니다.
- 예: `Core -> Body -> UiRender`, `Core -> Cluster -> UiRender`

### 6.4 최종 판정
| 조건 | 기준 |
| --- | --- |
| 주기 | 주기 판정 PASS |
| 로직 | `logic_verdict=PASS` |
| 통신 | `comm_verdict=PASS` |
| 증빙 필드 | `owner`, `run_date`, `evidence_*`가 비어 있지 않을 것 |

위 조건을 모두 만족하면 `computed_verdict = PASS`이며, 하나라도 위반하면 FAIL이다.

## 7) 표준 시간 기준
| 기준 | 의미 |
| --- | --- |
| `50ms` | 출력 주기 |
| `100ms` | 입력/통신 주기 |
| `150ms` | 즉시 반영 상한(`100ms + 50ms`) |
| `1000ms` | timeout clear 기준 |

## 8) 캡처 규칙
| 파일명 | 용도 |
| --- | --- |
| `{test_id}_01_vehicle.png` | 차량 화면 |
| `{test_id}_02_control.png` | 제어 패널 |
| `{test_id}_03_monitor.png` | 상태 모니터 |

`capture_index.csv`에는 파일 경로와 설명을 반드시 매핑한다.

## 9) 실행 명령 예시
```powershell
python scripts/run.py verify prepare --run-id 20260306_1930
python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner <OWNER>
```

## 10) 05/06/07 반영 규칙
| 항목 | 기준 |
| --- | --- |
| 문서 판정 입력 | `computed_verdict` 기준 입력 |
| 증빙 경로 연결 | 테스트 ID와 1:1 연결 |
| 문서-채점 불일치 | 값이 다르면 FAIL |
| trace/log 필수 | trace/log 없으면 closeout 불가 |

## 11) 승인 규칙
| 항목 | 기준 |
| --- | --- |
| 자동화 범위 | candidate verdict까지만 생성 |
| 공식 반영 | reviewer approval 필요 |
| 실패 처리 | `fail_disposition_template.md` 사용 |
