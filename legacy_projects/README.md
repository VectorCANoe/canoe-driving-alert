# Legacy Projects Archive

이 폴더는 현재 제품 스코프 밖의 과거 주제/샘플을 보관하는 아카이브입니다.

## 목적
- 주제별 레거시 자산을 루트에서 분리 보관
- 현재 개발 SoT 경로(`driving-situation-alert`, `canoe`)와 물리적으로 구분
- 필요 시 참고용 조회만 허용

## 구성
- `legacy_projects/reference/`
  - `samples/`
  - `legacy/`
- `legacy_projects/docs/`
  - `v2x_original/`
  - `v2x/`
  - `V-Model/`
  - `OTA_original/`
  - `LIN-Door/`
  - `architecture/`

## 운영 규칙
- 기본 상태는 **폐기안/참고용**이다.
- 현재 개발 체인(Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST)에 직접 연결하지 않는다.
- 재사용이 필요하면 change-order 문서에 목적/범위/소유자/롤백을 먼저 기록한다.
