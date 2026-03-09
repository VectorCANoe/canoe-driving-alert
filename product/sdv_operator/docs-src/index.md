# CANoe Test Verification Console

`CANoe Test Verification Console`은 CANoe SIL 검증을 위한 Dev2 운영 콘솔입니다.

역할은 세 가지로 고정합니다.

1. 실행
   - `gate all`
   - `scenario run`
   - `verify quick`
2. 결과 확인
   - Verification Console 결과 카드
   - 하단 Log 패널
   - 증빙 경로
   - artifact open / artifact list
3. 패키징
   - portable ZIP
   - Windows executable
4. CI bridge
   - JUnit XML
   - Jenkins archive contract
   - sample pipeline: `product/sdv_operator/examples/Jenkinsfile.verify`
5. 역할 경계 / capability boundary / campaign profile
   - CANoe TEST / Jenkins / Console 역할 분리
   - capability boundary source contract
   - campaign profile source contract

## One-Line Flow

```powershell
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
python scripts/run.py verify batch --run-id 20260308_0900 --campaign-id CMP_20260310 --owner DEV2 --phase pre --surface-scope ALL --repeat-count 1 --duration-minutes 0 --interval-seconds 0 --report-formats json,md,junit
```

## 표면 원칙

- 내부 실행 계층은 Verification Console 화면과 Shell fallback으로 나뉘지만, 사용자 표면은 하나의 CANoe Test Verification Console으로 봅니다.
- CANoe Panel은 별도 제품 조작 UI로 유지합니다.
- CANoe Test Verification Console은 CANoe를 대체하지 않고, 검증 운영/리뷰 표면만 제공합니다.
- 표면 언어 정책은 `한국어 설명 + 영어 식별자`를 기본으로 합니다.

## 문서 순서

1. Quickstart
2. Commands
3. Results
4. Role Boundary
5. Capability Boundary
6. Campaign Profiles
7. CI Bridge
8. Packaging
9. Maintenance
10. Repo Surfaces
