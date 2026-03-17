# Sync Rule 한글판

원문:
- [../../operations/sync-rule.md](../../operations/sync-rule.md)

## 목적

이 문서는 `src/capl`과 `cfg/channel_assign` 사이의 고정 sync rule을 정의합니다.

## Source of Truth

- `canoe/src/capl/**`가 source of truth입니다.
- `canoe/cfg/channel_assign/**`는 GUI import mirror입니다.

## 필수 규칙

`src/capl/`에서 CAPL node를 바꿨다면, 그 active change를 `cfg/channel_assign/`에도 mirror해야 완료로 봅니다.

## 완료 조건

CAPL 변경은 아래가 모두 참일 때만 완료입니다.

1. `src/capl/` source update 완료
2. `cfg/channel_assign/` mirror update 완료
3. CAPL compile clean
4. behavior에 영향을 주면 runtime result는 별도 review

## 하지 말아야 할 해석

- `cfg/channel_assign/`를 독립 source tree로 취급하지 않습니다.
- compile success만으로 runtime success를 추정하지 않습니다.
- source/mirror drift를 덮기 위해 DBC visibility나 transport setting을 우회 수정하지 않습니다.
