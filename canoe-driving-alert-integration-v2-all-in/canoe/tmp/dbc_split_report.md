# DBC Split Report

## 1) Scope and Boundary
- Source baseline: `canoe/network/dbc/emergency_system.dbc`
- References used (read-only):
  - `docs/meeting-notes/MET_30_2026.02.28.txt`
  - `driving-situation-alert/00~07` (no modification)
- Repository boundary applied:
  - `driving-situation-alert` is read-only per `canoe/AGENTS.md`
  - Report is written to `canoe/tmp/dbc_split_report.md`

## 2) Output Files (Domain Split)
- `canoe/network/dbc/emergency_system_chassis.dbc`
- `canoe/network/dbc/emergency_system_powertrain.dbc`
- `canoe/network/dbc/emergency_system_body.dbc`
- `canoe/network/dbc/emergency_system_infotainment.dbc`

## 3) Frame Allocation Result (Expanded)
| Domain DBC | Frame IDs | Message Count | Note |
|---|---|---:|---|
| chassis | `0x100`, `0x101`, `0x102`, `0x103`, `0x104`, `0x105`, `0x106`, `0x107`, `0x108`, `0x109`, `0x230`, `0x231`, `0x232` | 13 | 기존 입력/결과 + 휠속도/요레이트/브레이크/토크/헬스 + 긴급모니터 |
| body | `0x210`, `0x211`, `0x212`, `0x213`, `0x214`, `0x215`, `0x216`, `0x217`, `0x218`, `0x219` | 10 | 기존 앰비언트/비상등/창문/운전자상태 + 도어/램프/와이퍼/시트벨트/캐빈/헬스 |
| infotainment | `0x110`, `0x220`, `0x221`, `0x222`, `0x223`, `0x224`, `0x225`, `0x226`, `0x227`, `0x228` | 10 | 기존 NAV/Cluster + 미디어/콜상태/경로/테마/팝업/헬스 |
| powertrain | `0x300`, `0x301`, `0x302`, `0x303`, `0x304`, `0x305`, `0x306`, `0x307`, `0x308`, `0x309`, `0x30A` | 11 | 시동/기어/라우팅 + RPM/열/연료/스로틀/모드/리밋/크루즈/헬스 |

## 4) Powertrain Domain Status
- `emergency_system_powertrain.dbc`는 scaffold 상태를 종료하고 실제 CAN 프레임 3개를 반영함.
- 반영 프레임: `0x300~0x30A` 총 11개로 확장.
- Req 연결 의도: `Req_101`, `Req_102`, `Req_110`.

## 7) MET_30 정합 체크 (DBC 관점)
- 도메인 분리: 완료 (`chassis/body/infotainment/powertrain` 개별 DBC)
- 누락 ECU 점검(기준 세트): 누락 없음
- 메시지 볼륨: split 합계 `44` (멘토 권고 최소 `40` 충족)

## 5) Consistency Notes
- Ethernet contract remains out of DBC scope (meeting guidance reflected).
- Existing baseline file `emergency_system.dbc` is kept unchanged for compatibility.
- No files under `driving-situation-alert` were modified.

## 6) 2026-02-28 Pull 반영 수동 정합
- Pull 반영 커밋 범위: `89ef104 -> 280aa5e`
- 변경 문서:
  - `driving-situation-alert/01_Requirements.md` (Req_101~Req_112 추가)
  - `driving-situation-alert/03_Function_definition.md`
  - `driving-situation-alert/0301_SysFuncAnalysis.md`
  - `driving-situation-alert/tmp/Domain_DBC_Split_Execution.md`
- 수동 반영 내용(도메인 DBC 노드 정합):
  - chassis: `ACCEL_CTRL`, `BRAKE_CTRL`, `STEERING_CTRL`, `VEHICLE_BASE_TEST_CTRL` 추가
  - body: `HAZARD_CTRL`, `WINDOW_CTRL`, `DRIVER_STATE_CTRL` 추가
  - infotainment: `NAV_CONTEXT_MGR`, `CLUSTER_BASE_CTRL` 추가
  - powertrain: `ENGINE_CTRL`, `TRANSMISSION_CTRL`, `DOMAIN_GW_ROUTER` 추가
- 통합 DBC(`emergency_system.dbc`)도 동일하게 Vehicle Baseline 노드 인벤토리를 `BU_`/`CM_ BU_`에 반영
- 후속 정합 주의:
  - 이번 확장 프레임(0x102/0x103/0x211~0x213/0x221~0x222/0x300~0x302/0x231)은 `0302/0303/0304` 문서의 다음 개정에서 동일 ID/DLC/bit로 동기화 필요.
