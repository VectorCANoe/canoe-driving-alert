# v1 CFG 스냅샷 — CAN_500kBaud_1ch_split.cfg
> 생성일: 2026-03-02
> 목적: v2 채널 분리 작업 시 롤백 기준점

---

## 1. 버스 구성 (현재)

| 항목 | 값 |
|------|-----|
| cfg 파일 | `canoe/cfg/CAN_500kBaud_1ch_split.cfg` |
| 물리 CAN 채널 수 | **1채널** (VDAOBus 블록 1개) |
| 통신 속도 | 500 kBaud |
| 상태 | Option 1 과도기 — 논리 분리 O, 물리 채널 분리 X |

---

## 2. 노드 → DB 매핑 (전체 26개)

| cfg 라인 | 노드명 | 논리 도메인(DBC) | v2 이동 목표 채널 |
|---------|--------|----------------|----------------|
| L5659 | ACCEL_CTRL | chassis_can | CAN ch1 (Chassis) |
| L5763 | CLUSTER_BASE_CTRL | infotainment_can | CAN ch3 (Infotainment) |
| L5867 | DOMAIN_GW_ROUTER | powertrain_can | 멀티채널 GW |
| L5971 | ENGINE_CTRL | powertrain_can | CAN ch4 (Powertrain) |
| L6075 | STEERING_CTRL | chassis_can | CAN ch1 (Chassis) |
| L6179 | VEHICLE_BASE_TEST_CTRL | chassis_can | CAN ch1 (Chassis) |
| L6284 | EMS_AMB_TX | chassis_can | ETH ch (Emergency) |
| L6388 | CHASSIS_GW | chassis_can | 멀티채널 GW |
| L6493 | SIL_TEST_CTRL | body_can | CAN ch2 (Body) |
| L6601 | EMS_ALERT_RX | chassis_can | ETH ch (Emergency) |
| L6705 | WARN_ARB_MGR | body_can | CAN ch2 (Body) |
| L6809 | BCM_AMBIENT_CTRL | body_can | CAN ch2 (Body) |
| L6913 | CLU_HMI_CTRL | infotainment_can | CAN ch3 (Infotainment) |
| L7018 | BRAKE_CTRL | chassis_can | CAN ch1 (Chassis) |
| L7122 | DOMAIN_BOUNDARY_MGR | body_can | 멀티채널 GW |
| L7228 | DRIVER_STATE_CTRL | body_can | CAN ch2 (Body) |
| L7332 | HAZARD_CTRL | body_can | CAN ch2 (Body) |
| L7436 | TRANSMISSION_CTRL | powertrain_can | CAN ch4 (Powertrain) |
| L7540 | WINDOW_CTRL | body_can | CAN ch2 (Body) |
| L7644 | EMS_POLICE_TX | chassis_can | ETH ch (Emergency) |
| L7748 | INFOTAINMENT_GW | infotainment_can | 멀티채널 GW |
| L7852 | ADAS_WARN_CTRL | chassis_can | CAN ch1 (Chassis) |
| L7956 | NAV_CONTEXT_MGR | infotainment_can | CAN ch3 (Infotainment) |
| L8060 | ETH_SWITCH | chassis_can | ETH ch (Emergency) |
| L8163 | BODY_GW | body_can | 멀티채널 GW |
| L8267 | IVI_GW | infotainment_can | 멀티채널 GW |

### 도메인별 요약

| 논리 도메인 | 노드 수 | 노드 목록 |
|------------|--------|---------|
| chassis_can | 9 | ACCEL_CTRL, STEERING_CTRL, VEHICLE_BASE_TEST_CTRL, EMS_AMB_TX, CHASSIS_GW, EMS_ALERT_RX, BRAKE_CTRL, EMS_POLICE_TX, ADAS_WARN_CTRL, ETH_SWITCH |
| body_can | 8 | SIL_TEST_CTRL, WARN_ARB_MGR, BCM_AMBIENT_CTRL, DOMAIN_BOUNDARY_MGR, DRIVER_STATE_CTRL, HAZARD_CTRL, WINDOW_CTRL, BODY_GW |
| infotainment_can | 5 | CLUSTER_BASE_CTRL, CLU_HMI_CTRL, INFOTAINMENT_GW, NAV_CONTEXT_MGR, IVI_GW |
| powertrain_can | 3 | DOMAIN_GW_ROUTER, ENGINE_CTRL, TRANSMISSION_CTRL |

---

## 3. 패널 파일 참조

| cfg 라인 | 파일 경로 |
|---------|---------|
| L8696 | `..\project\panel\SDV_Monitor.xvp` |
| L8769 | `..\project\panel\SDV_Control.xvp` |

> ⚠️ v2 작업 시 이 패널들의 Signal/SysVar 바인딩 채널 번호 재확인 필요

---

## 4. Logging / Trace 현황

| 항목 | 현재 설정 |
|------|---------|
| LoggingBlock | VGeneralLoggingBlockSettings — CAN ch1 단일 |
| Trace 필터 | VTraceFilterCfg — 채널 고정값 없음 (전채널 캡처) |
| 로그 파일 | Template 상대경로 `..\..\..\..\..\Public\Documents\Vector\CANoe\...` |

> ⚠️ v2 채널 분리 후 Logging 블록에 채널 4개 + ETH 추가 필요

---

## 5. sysvars 참조

| cfg 라인 | 파일 경로 |
|---------|---------|
| L819, L822 | `..\project\sysvars\project.sysvars` |

---

## 6. v2 마이그레이션 체크리스트 (별도 브랜치)

```
[ ] git checkout -b feature/v2-multi-channel
[ ] CANoe에서 CAN ch2(Body), ch3(Infotainment), ch4(Powertrain), ETH ch 추가
[ ] 위 노드 매핑표 기준으로 각 노드 채널 재배치
[ ] GW 노드(DOMAIN_GW_ROUTER, CHASSIS_GW, BODY_GW, IVI_GW, INFOTAINMENT_GW, DOMAIN_BOUNDARY_MGR)
    → 다중 채널 연결 설정
[ ] DBC → 채널 바인딩 재매핑 (chassis_can→ch1, body_can→ch2, infotainment_can→ch3, powertrain_can→ch4)
[ ] SDV_Monitor.xvp / SDV_Control.xvp 채널 참조 재확인
[ ] Logging 블록 채널 추가
[ ] F8 컴파일 전체 통과 확인
[ ] 0302/0303 메시지 ID·방향 1:1 검증
[ ] main 머지
```

---

## 7. 롤백 방법

```bash
# v2 작업 중 문제 발생 시
git checkout main
# canoe/cfg/CAN_500kBaud_1ch_split.cfg 는 main 기준으로 복구됨
```
