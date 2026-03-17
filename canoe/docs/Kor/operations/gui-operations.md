# GUI Operations 한글판

원문:
- [../../operations/gui-operations.md](../../operations/gui-operations.md)

## 목적

이 문서는 어떤 CANoe 작업이 반드시 GUI-first로 남아야 하는지 정의합니다.

## GUI-first 범위

아래는 CANoe GUI로 처리해야 합니다.

- `canoe/cfg/*.cfg`의 open / save / save-as
- `*.cfg.ini`, `*.stcfg`의 생성 또는 업데이트
- channel mapping, hardware assignment, IL registration, network setup
- active configuration 안에서 visible node placement와 multibus visibility 복원

## 직접 수정 허용 예외

직접 텍스트 수정이 허용되는 항목:
- `canoe/project/panel/*.xvp`
- `canoe/project/sysvars/project.sysvars`
- developer-facing Markdown documentation

## 복구 규칙

config integrity가 의심되면:
1. CANoe GUI로 reload
2. CANoe GUI로 save
3. 그 다음 안정화된 결과를 text document에 기록

## 작업 규칙

- GUI가 관리하는 config file을 직접 patch하지 않습니다.
- recovery task가 명시적으로 주어진 경우만 예외입니다.
- 더 자세한 local checklist는 [../../cfg/GUI_ONLY_OPERATIONS.md](../../cfg/GUI_ONLY_OPERATIONS.md)를 봅니다.
