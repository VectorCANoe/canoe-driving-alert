# Legacy Asset Archive (v1)

이 폴더는 v1 호환/과거 디버깅용 자산만 보관합니다.

- `legacy/cfg/v1_cfg/*`: 과거 CANoe CFG 프로필
- `legacy/dbc/v1_legacy/*`: 과거 DBC/보조 DBC
- `legacy/nodes/*`: v1 계열 노드 정의(.can)

원칙:
- V2 일상 개발/검증에는 사용하지 않음
- 재활성화가 필요할 때만 Read-only로 참조
- 실사용은 GUI에서 검증 가능한 최신 v2 자산만 사용