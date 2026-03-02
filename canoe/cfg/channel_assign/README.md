# channel_assign — CANoe GUI 채널 일괄 할당 가이드

> **목적**: v2 5-채널 토폴로지 구성 시 노드를 CANoe GUI에서 채널별로 일괄 추가하기 위한 도우미 폴더
> **원본 소스**: `canoe/src/capl/**/*.can` — 이 폴더의 .can 파일은 원본의 복사본
> **주의**: 이 폴더의 .can 파일을 직접 수정하지 말 것 (원본만 수정)

---

## v2 채널 구성

| 채널 | 폴더 | DBC | 역할 |
|------|------|-----|------|
| CAN ch1 — Chassis | `Chassis/` | `chassis_can.dbc` | 섀시 ECU (가속/제동/조향) + GW |
| CAN ch2 — Body | `Body/` | `body_can.dbc` | 바디 ECU (앰비언트/BCM/운전자 상태) + GW |
| CAN ch3 — Infotainment | `Infotainment/` | `infotainment_can.dbc` | IVI/CLU/클러스터 + GW |
| CAN ch4 — Powertrain | `Powertrain/` | `powertrain_can.dbc` | 엔진/변속기 + 도메인 라우터 |
| CAN ch5 — ETH_Backbone | `ETH_Backbone/` | `eth_backbone_can_stub.dbc` | 경고 코어 + EMS + 스위치 (**ETH stub**) |

> **ETH_Backbone**: CANoe.Ethernet 라이선스 취득 시 CAN ch5 → Ethernet 네트워크로 교체.
> 교체 시 `eth_backbone_can_stub.dbc` 삭제, CAPL 코드 변경 없음 (인터페이스 동일 보장).

---

## CANoe GUI 노드 추가 절차

1. `CAN_v2_topology_wip.cfg` 열기
2. 각 채널 네트워크 우클릭 → **Insert CAPL Node**
3. 해당 채널 폴더 전체 선택 → 열기 (일괄 추가)

```
Chassis      채널 → Chassis/       (5개 노드)
Body         채널 → Body/          (7개 노드)
Infotainment 채널 → Infotainment/  (3개 노드)
Powertrain   채널 → Powertrain/    (3개 노드)
ETH_Backbone 채널 → ETH_Backbone/  (8개 노드)
```

4. **F8** 전체 컴파일 확인
5. GW 노드 멀티채널 바인딩 설정 (아래 참조)

---

## GW 노드 멀티채널 바인딩 (필수)

GW 노드는 두 채널에 동시 할당되어야 함.
노드 우클릭 → Properties → Channel Assignments

| 노드 | 채널 1 | 채널 2 |
|------|--------|--------|
| `CHASSIS_GW` | CAN ch1 (Chassis) | CAN ch5 (ETH_Backbone) |
| `BODY_GW` | CAN ch2 (Body) | CAN ch5 (ETH_Backbone) |
| `INFOTAINMENT_GW` | CAN ch3 (Infotainment) | CAN ch5 (ETH_Backbone) |
| `IVI_GW` | CAN ch3 (Infotainment) | CAN ch5 (ETH_Backbone) |
| `DOMAIN_GW_ROUTER` | CAN ch4 (Powertrain) | CAN ch5 (ETH_Backbone) |

---

## 노드 목록

### Chassis/ (CAN ch1)
- `CHASSIS_GW.can` — 섀시 ↔ ETH_Backbone 게이트웨이
- `ACCEL_CTRL.can` — 급가속 감지
- `STEERING_CTRL.can` — 조향 입력 감지
- `BRAKE_CTRL.can` — 급제동 감지
- `VEHICLE_BASE_TEST_CTRL.can` — 차속/기어 기반 테스트 제어

### Body/ (CAN ch2)
- `BODY_GW.can` — 바디 ↔ ETH_Backbone 게이트웨이
- `BCM_AMBIENT_CTRL.can` — 앰비언트 라이트 제어 (핵심 출력)
- `DRIVER_STATE_CTRL.can` — 운전자 상태 감지 (라엘 담당)
- `HAZARD_CTRL.can` — 비상 점멸 제어
- `WINDOW_CTRL.can` — 창문 제어
- `DOMAIN_BOUNDARY_MGR.can` — 도메인 경계 관리
- `SIL_TEST_CTRL.can` — SIL 테스트 오케스트레이터

### Infotainment/ (CAN ch3)
- `INFOTAINMENT_GW.can` — 인포테인먼트 ↔ ETH_Backbone 게이트웨이
- `CLU_HMI_CTRL.can` — HMI 입력 처리
- `CLUSTER_BASE_CTRL.can` — 클러스터 디스플레이

### Powertrain/ (CAN ch4)
- `DOMAIN_GW_ROUTER.can` — 파워트레인 ↔ ETH_Backbone 라우터
- `ENGINE_CTRL.can` — 엔진 ECU
- `TRANSMISSION_CTRL.can` — 변속기 ECU

### ETH_Backbone/ (CAN ch5 — ETH stub)
- `ETH_SWITCH.can` — 백본 스위치 (메시지 라우팅)
- `WARN_ARB_MGR.can` — 경고 우선순위 중재 (핵심)
- `ADAS_WARN_CTRL.can` — ADAS 경고 제어
- `NAV_CONTEXT_MGR.can` — 구간 컨텍스트 관리
- `EMS_ALERT_RX.can` — 긴급차량 수신 처리 (성현 담당)
- `EMS_POLICE_TX.can` — 경찰차 TX 시뮬레이터 (성현 담당)
- `EMS_AMB_TX.can` — 구급차 TX 시뮬레이터 (성현 담당)
- `IVI_GW.can` — IVI/클러스터 ETH 에그레스 GW
