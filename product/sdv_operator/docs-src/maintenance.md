# 유지보수

## 경계

Dev2가 관리하는 것은 `scripts` 전체가 아니라 `SDV Operator` 제품 경계입니다.

제품 경계는 아래를 기준으로 봅니다.

- `product/sdv_operator/`
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/cliops/`
- `scripts/gates/`
- `scripts/quality/`
- `scripts/release/`

## 유지해야 할 표면

### 공개 표면

- 루트 `README.md`
- `product/sdv_operator/README.md`
- generated docs site

### 운영 표면

- `python scripts/run.py`
- `gate all`
- `scenario run`
- `verify quick`
- `doctor`

### 내부 구현면

- `scripts/cliops/*`
- `scripts/gates/*`
- `scripts/quality/*`
- `scripts/release/*`

## 변경 원칙

1. 공개 표면은 더 이상 무겁게 만들지 않습니다.
2. 내부 구현은 모듈화와 계약 중심으로 정리합니다.
3. Verification Console은 운영 콘솔로 유지하고, CANoe 제어 GUI를 재구현하지 않습니다.
4. 구조적 결과 파일(JSON)을 우선하고, Verification Console은 그 결과를 소비합니다.
5. CI 연계는 `dev2_batch_report.junit.xml`을 정본 Jenkins ingress 포맷으로 사용합니다.

## 언어 표면 정책

이 제품은 언어를 아래처럼 분리합니다.

### 한국어로 유지할 것

- 운영 설명
- 도움말
- 실패 원인 설명
- 다음 액션 가이드
- 문서 본문

### 영어로 유지할 것

- 명령명
- 단계명
- 화면 탭/핵심 카드 식별자
- 범주 버튼과 핵심 action label
- 판정값
- JSON 키/산출물 키/CI 식별자

대표 예:

- `Overview / Campaign / Results / Artifacts / Automation`
- `Primary / Runtime / Inspect / Package`
- `gate all / scenario run / verify quick / doctor`
- `PASS / WARN / FAIL`
- `run_id / phase / surface bundle`

원칙:

1. 설명은 한국어로 쉽게 읽혀야 합니다.
2. 식별자는 코드/문서/JSON/CI와 1:1로 맞아야 하므로 영어를 유지합니다.
3. 새 화면/명령/카드 추가 시 이 규칙을 기본으로 따릅니다.
