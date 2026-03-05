# Domain DBC Split Execution (Post-Mentoring 08)

## 1. 목적

- 단일 CAN DBC(`emergency_system.dbc`)를 도메인 네트워크 단위로 분리한다.
- 멘토 피드백(네트워크별 DBC, 차량 기본 기능 확장)을 실제 구현 단계로 연결한다.

---

## 2. 분리 대상 DBC (초안)

| 파일명(계획) | 도메인 | 주요 노드 | 포함 메시지(초안) |
|---|---|---|---|
| `chassis_can.dbc` | Chassis | SIL_TEST_CTRL, CHASSIS_GW, ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL | 0x100, 0x101, (추가) 페달/조향 보강 메시지 |
| `powertrain_can.dbc` | Powertrain | ENGINE_CTRL, TRANSMISSION_CTRL, (필요 시 POWERTRAIN_GW) | (추가) 시동/기어/엔진 상태 메시지 |
| `body_can.dbc` | Body | BODY_GW, BCM_AMBIENT_CTRL, HAZARD_CTRL, WINDOW_CTRL, DRIVER_STATE_CTRL | 0x210, (추가) 창문/비상등/운전자 상태 메시지 |
| `infotainment_can.dbc` | Infotainment | INFOTAINMENT_GW, IVI_GW, NAV_CONTEXT_MGR, CLU_HMI_CTRL, CLUSTER_BASE_CTRL | 0x110, 0x220, (추가) 클러스터 기본 상태 메시지 |
| `test_can.dbc` (선택) | SIL/Test | SIL_TEST_CTRL | 0x230 (결과 보고) |

---

## 3. Ethernet 분리 원칙 (고정)

- Ethernet 계약은 DBC로 만들지 않는다.
- 원본 문서:
  - `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- 대상 ID:
  - 0x510, 0x511, 0x512, 0xE100, 0xE200

---

## 4. 실행 순서

1. 도메인별 노드/메시지 할당표 확정  
2. DBC 파일 분리 생성(기존 메시지 이관 + 차량 기본 기능 메시지 추가)  
3. CANoe cfg에서 각 네트워크와 DBC 연결  
4. 0302/0303 SoT 경로를 단일 DBC -> 도메인 DBC 세트로 변경  
5. 0304 Var-Comm-Flow를 분리 DBC 기준으로 재매핑  
6. 05/06/07 검증 케이스에서 변경된 메시지 경로 반영

---

## 5. 완료 기준

- 도메인별 DBC 파일이 실제로 존재한다.
- 각 DBC의 Tx/Rx 노드가 도메인 경계와 일치한다.
- 0302/0303/0304 문서가 분리 DBC 구조와 일치한다.
- SIL 시나리오(ST)에서 기본 차량 기능 + 서비스 기능이 모두 동작한다.
