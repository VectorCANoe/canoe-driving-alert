# V2 진단 자산 매트릭스 (Rebuild 기준)

## Scope
- 대상: `canoe/cfg/channel_assign` + `canoe/src/capl`
- 제외: `v1_legacy` 하위
- 목표: 기존 진단 자산을 기준으로 삭제/재정의 판단을 완결하고, 충돌 없는 v2 재빌드 기반을 만들기

## Skalaton / Oracle 분류

| 분류 | 상태 | 항목 | 판단 근거 |
|---|---|---|---|
| Skalaton | KEEP | v2 전용 로직 자산(현재 수정 파일 68개) | 진단 키워드 제거 후 통신/로직 동작 코드만 유지 |
| Oracle | REMOVE | `diag`/`Diag`/`DIAG_*`/`mirrorDiag*`/`Diag::`/`getBasicDiagRespCode` 관련 패턴 | 현재 v2 범위에서 **0개 매칭** |

## 스캔 결과 요약
- `rg` 진단 패턴 스캔 결과(v2 .can/.cin 기준): `0`개
- 체크 패턴: `diag`, `Diag`, `DIAG`, `mirrorDiag`, `mirrorDiagResponse`, `Diag::`, `DIAG_TARGET`, `DIAG_BUS`, `getBasicDiagRespCode`
- 수치상으로는 삭제할 진단 자산이 남아있지 않음

## 적용 규칙(Next Pass)
1. v2 `.can`은 기존 파일 재활용은 허용하되, 진단/체크포인트 함수 호출은 금지
2. `CAPL_COMMON.cin`에는 진단 유틸/래핑 코드 미배치
3. 진단 재도입이 필요하면 v2 별도 모듈로 신규 분리
