# 개발팀 반영 점검 결과 (ADAS/ECU)

점검일: 2026-03-05  
기준 브랜치: `main` (`origin/main` pull 완료)  
대상 커밋: `d13159c`, `95939cb`, `efedc3f`

## 1) 총평

- ADAS 도메인 분리(`adas_can.dbc`)와 Validation 프레임 통합(`0x230/0x231 -> chassis_can.dbc`)은 반영되었다.
- 문서 SoT(`01~07`, `03xx`, `00e`)는 Canonical 기준으로 정렬되었고 Chassis 약어는 `ACCEL_CTRL`/`STEER_CTRL`로 확정되었다.
- 남은 검증 포인트는 `canoe` 활성 cfg/CAPL/운영문서의 Canonical 정합성 최종 확인이다.

## 2) 지시 항목별 판정

| 항목 | 판정 | 근거 |
|---|---|---|
| ADAS 도메인 DBC 신설 | PASS | `canoe/databases/adas_can.dbc` 생성 (`0x11F`, `0x313`) |
| ADAS 소유 프레임 분리 | PASS | `0x11F/0x313`가 `adas_can.dbc`로 이동, `eth_backbone_can_stub.dbc`에서 `0x11F` 제거 |
| Validation 프레임 Chassis 통합 (`0x230/0x231`) | PASS | `chassis_can.dbc` 기준으로 문서/DBC 정합 반영 |
| 활성 경로 `test_can` 참조 제거 | PASS | 최신 cfg에서 `test_can.dbc` 참조 제거 (`efedc3f`) |
| Validation ECU 명칭 `VAL_*` 일원화 | PARTIAL | 문서 체인은 PASS, `canoe` 활성 cfg/CAPL 경로 추가 확인 필요 |
| Chassis 약어 전환 (`ACCEL_CTRL`, `STEER_CTRL`) | PASS (문서) | `01~07`, `03xx`, `00e`에 반영 완료 (`ACCL_CTRL`, `STRG_CTRL` 제거) |
| DBC ID 충돌 0건 | PASS | 활성 DBC 스캔 결과 collision 0 |

## 3) 지금 확인할 내용 (개발팀)

1. 활성 cfg에 `test_can` 참조가 남아있는지 최종 확인
- [CAN_v2_topology_wip.cfg](/Users/juns/code/work/mobis/PBL/canoe/cfg/CAN_v2_topology_wip.cfg:10008)

2. 활성 운영 문서의 runtime split 표기가 최신 구조와 일치하는지 확인
- [project_explained.md](/Users/juns/code/work/mobis/PBL/canoe/docs/architecture/project_explained.md:7)

3. Canonical 명칭 적용 범위를 active path로 고정할지(legacy 분리 유지) 정책 확정
- [README.md](/Users/juns/code/work/mobis/PBL/canoe/README.md:47)
- [CAN_MESSAGE_OWNERSHIP_MATRIX.md](/Users/juns/code/work/mobis/PBL/canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md:15)

4. 문서 체인 정합성 재확인 (완료 상태 유지)
- [04_SW_Implementation.md](/Users/juns/code/work/mobis/PBL/driving-situation-alert/04_SW_Implementation.md:24)

## 4) 권고 (명칭/약어 적용 원칙)

- 신규 ECU만 별도 명칭을 쓰지 말고, 전체 ECU에 동일한 Canonical 규칙을 적용한다.
- AUTOSAR 정합은 별도 `shortName` 매핑 컬럼으로 유지한다.
- 공식명은 `00e_ECU_Naming_Standard.md`의 Canonical을 단일 SoT로 사용한다.
