# 개발팀 반영 점검 결과 (ADAS/ECU)

점검일: 2026-03-05  
기준 브랜치: `main` (`origin/main` pull 완료)  
대상 커밋: `d13159c`, `95939cb`, `efedc3f`

## 1) 총평

- ADAS 도메인 분리(`adas_can.dbc`)와 문서 SoT 동기화는 반영되었다.
- 최신 커밋(`efedc3f`)에서 `test_can` 활성 참조 제거가 반영되었다.
- 다만 `cfg`/일부 문서에 구 명칭(`SIL_TEST_CTRL`, `VEHICLE_BASE_TEST_CTRL`)이 잔존해 명명 표준 수용은 부분 완료 상태다.

## 2) 지시 항목별 판정

| 항목 | 판정 | 근거 |
|---|---|---|
| ADAS 도메인 DBC 신설 | PASS | `canoe/databases/adas_can.dbc` 생성 (`0x11F`, `0x313`) |
| ADAS 소유 프레임 분리 | PASS | `0x11F/0x313`가 `adas_can.dbc`로 이동, `eth_backbone_can_stub.dbc`에서 `0x11F` 제거 |
| Validation 프레임 Chassis 통합 (`0x230/0x231`) | PASS | `chassis_can.dbc` 기준으로 문서/DBC 정합 반영 |
| 활성 경로 `test_can` 참조 제거 | PASS | 최신 cfg에서 `test_can.dbc` 참조 제거 (`efedc3f`) |
| Validation ECU 명칭 `VAL_*` 일원화 | PARTIAL | 문서는 `VAL_*` 중심이나 파일/CFG에 `SIL_TEST_CTRL`, `VEHICLE_BASE_TEST_CTRL` 잔존 |
| DBC ID 충돌 0건 | PASS | 활성 DBC 스캔 결과 collision 0 |

## 3) 잔여 이슈 (개발팀 수정 필요)

1. 구 명칭 잔존 제거 또는 Alias 정책 확정
- [CAN_v2_topology_wip.cfg](/Users/juns/code/work/mobis/PBL/canoe/cfg/CAN_v2_topology_wip.cfg:7177)
- [CAN_v2_topology_wip.cfg](/Users/juns/code/work/mobis/PBL/canoe/cfg/CAN_v2_topology_wip.cfg:8974)
- [04_SW_Implementation.md](/Users/juns/code/work/mobis/PBL/driving-situation-alert/04_SW_Implementation.md:117)

2. 문서 SoT 미세 불일치 정리
- [04_SW_Implementation.md](/Users/juns/code/work/mobis/PBL/driving-situation-alert/04_SW_Implementation.md:24)  
  `adas_can.dbc` 누락
- [project_explained.md](/Users/juns/code/work/mobis/PBL/canoe/docs/architecture/project_explained.md:7)  
  runtime split에 `test_can` 명시

## 4) 권고 (명칭/약어 적용 원칙)

- 신규 ECU만 별도 명칭을 쓰지 말고, 전체 ECU에 동일한 Canonical 규칙을 적용한다.
- AUTOSAR 정합은 별도 `shortName` 매핑 컬럼으로 유지한다.
- 공식명은 `00e_ECU_Naming_Standard.md`의 Canonical을 단일 SoT로 사용한다.
