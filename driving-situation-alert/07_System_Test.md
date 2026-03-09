# 시스템 테스트 (System Test)

**Document ID**: PROJ-07-ST
**ISO 26262 Reference**: Part 4, Cl.10 (System Integration and System Qualification Test)
**ASPICE Reference**: SYS.5 (System Qualification Test)
**Version**: 5.22
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 상단 (SYS.5) | `07_System_Test.md` | `06_Integration_Test.md`, `01_Requirements.md` | 릴리즈/검수 |

---

## 작성 원칙

- 본 문서는 운전자 관점 E2E 시나리오로 요구사항 충족을 검증한다.
- 상단 표는 샘플 형식(`Scene ID/설명/Pass/담당자/일자`)을 유지한다.
- ST는 사용자/운전자 시나리오 중심으로 유지하고, 미세 경계값 판정은 UT/IT 근거를 참조한다.
- ST는 블랙박스 관점(입력 이벤트 -> 사용자 관찰 결과)으로 작성하며, 내부 구현 세부는 05/06 참조로 분리한다.
- 상세 추적은 하단 ST 추적표에서 `Req/VC/Func/Flow/Comm/Var/IT`로 연결한다.
- 검증 환경은 CANoe SIL, CAN+Ethernet으로 고정한다.
- 임시 주석(실행 제약): 현재 CANoe.CAN 라이선스 환경에서는 SIL 실행 시 Ethernet 구간을 CAN 대체 백본으로 검증하며, Ethernet 라이선스 확보 후 동일 ST 케이스로 재검증한다.
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 Pass/Fail를 기입한다.
- 대조군/우수성 비교 실험은 본 문서 범위 밖으로 두며, 요구사항 충족 Pass/Fail 증빙을 우선한다.
- `ST_SIL_001`, `ST_SIL_002`, `ST_RESULT_001`, `ST_BASE_DIAG_001`은 Validation Harness 기반 검증 시나리오(검증 전용)다.
- ST 증적(로그/캡처/리포트)은 `canoe/logging/evidence/ST/` 경로 규칙으로 관리한다.
- ST 증적 포맷/채점 규칙은 `canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md`를 따른다.
- 검증 배치 실행/리포트 생성은 `scripts/run.py verify batch`를 사용하고, 출력 포맷은 기본 `json,md`(옵션 `--report-formats csv`)를 적용한다.
- V2 확장 요구(`Req_120~Req_121, Req_123, Req_125~Req_129`)는 구현 활성 상태로 ST 항목을 분리 관리하며, SIL 시나리오 15~19와 연계해 검증한다.
- ADAS 객체 인지 확장(`Req_130~Req_139`)은 Pre-Activation(설계 선반영) ST 항목(`ST_ADAS_OBJ_001`)으로 분리 관리한다.
- 차량 경보 편의 확장(`Req_140~Req_147`)은 Pre-Activation(설계 선반영) ST 항목(`ST_BASE_ALERT_EXT_001`)으로 분리 관리한다.
- 경고 강건성·인지성 확장(`Req_148~Req_155`)은 Pre-Activation(설계 선반영) ST 항목(`ST_BASE_ROBUST_EXT_001`)으로 분리 관리한다.
- Panel 검증은 `차량 화면 -> 제어 패널 -> 상태 모니터` 순서로 수행하고, 시스템 동작 확인은 차량 화면 기준으로 판정한다.

---

## 시나리오 확장 원칙 (OEM100 Surface ECU)

### 핵심 원칙

- Surface ECU가 증가해도 ST의 핵심 사용자 시나리오 축(`구간`, `긴급`, `중재`, `기본차량`, `확장`)은 유지한다.
- ST는 ECU 개수 기반이 아니라 사용자 관찰 결과 기반으로 설계한다.
- 신규 Active Surface가 기존 시나리오 경로에 편입되면 기존 ST에 흡수하고, 사용자 관찰 결과가 달라질 때만 ST를 추가한다.
- Placeholder Surface는 ST 실행 대상이 아니라 `Planned` 상태로 유지한다.

### ST 운영 매핑 (요약)

| 분류 | ST 반영 방식 | 대표 ST |
|---|---|---|
| Active Surface ECU | 기존 E2E 시나리오에 흡수하여 검증 | `ST_SPEED_001`, `ST_EMS_001`, `ST_POLICY_001`, `ST_BASE_001` |
| Validation Harness | 검증 전용 시나리오로 분리 검증 | `ST_SIL_001`, `ST_SIL_002`, `ST_RESULT_001`, `ST_BASE_DIAG_001` |
| Placeholder Surface ECU | 구현 완료 전까지 Planned 유지 | `ST_ADAS_OBJ_001`, `ST_BASE_ALERT_EXT_001`, `ST_BASE_ROBUST_EXT_001` |

### OEM100 Surface 상세-ST 매핑 (실제 본문 운영)

| 그룹 | Surface ECU(실명) | ST 커버 방식 | 주요 ST ID |
|---|---|---|---|
| A1 Infrastructure/Integration | `CGW`, `ETH_BACKBONE`, `DCM`, `IBOX`, `SGW` | 시스템 경계/인수/진단 시나리오 커버 | `ST_SIL_001`, `ST_SIL_002`, `ST_BASE_DIAG_001`, `ST_OEM_SURFACE_001` |
| A2 Powertrain | `EMS`, `TCU`, `VCU`, `_4WD`, `BAT_BMS`, `FPCM`, `LVR`, `ISG`, `EOP`, `EWP` | 동력계/기어/상태 연계 시나리오 커버 | `ST_BASE_PT_001`, `ST_BASE_EXT_PT_002`, `ST_BASE_001` |
| A3 Chassis/Safety | `ESC`, `MDPS`, `ABS`, `EPB`, `TPMS`, `SAS`, `ECS`, `ACU`, `ODS`, `VSM`, `EHB`, `CDC` | 제동/조향/무조향/안전 연계 시나리오 커버 | `ST_BASE_CH_001`, `ST_STEER_001`, `ST_BASE_001` |
| A4 Body/Comfort | `BCM`, `DATC`, `SMK`, `AFLS`, `AHLS`, `WIPER_MODULE`, `SUNROOF_MODULE`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `TAILGATE_MODULE`, `SEAT_DRV`, `SEAT_PASS`, `MIRROR_MODULE`, `BODY_SECURITY_MODULE` | 바디/편의 상태 시나리오 커버 | `ST_BASE_BODY_001`, `ST_BASE_EXT_BODY_001`, `ST_BASE_EXT_BODY_002`, `ST_BASE_001` |
| A5 IVI/HMI/Connectivity | `IVI`, `CLU`, `HUD`, `TMU`, `AMP`, `PGS`, `NAV_MODULE`, `VOICE_ASSIST`, `RSE`, `DIGITAL_KEY` | 표시/HMI/인지성 시나리오 커버 | `ST_POLICY_001`, `ST_BASE_IVI_001`, `ST_BASE_EXT_IVI_001` |
| A6 ADAS/V2X/Parking | `ADAS`, `V2X`, `SCC`, `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PARK_ULTRASONIC`, `DMS`, `OMS` | 핵심 경보/중재/객체위험 시나리오 커버 | `ST_SPEED_001`, `ST_EMS_001`, `ST_EMS_002`, `ST_V2_RISK_001`, `ST_ADAS_OBJ_001` |
| B Validation Harness | `VALIDATION_HARNESS` | 검증 실행/판정 시나리오 커버 | `ST_SIL_001`, `ST_RESULT_001`, `ST_BASE_DIAG_001` |
| C Premium Option | `OBC`, `DCDC`, `MCU`, `INVERTER`, `CHARGE_PORT_CTRL`, `AIR_SUSPENSION`, `RWS`, `NIGHT_VISION`, `AEB_DOMAIN`, `HIGHWAY_PILOT`, `PARK_MASTER`, `TRAILER_CTRL`, `HEADLAMP_LEVELING`, `AUTO_DOOR_CTRL`, `POWER_TAILGATE_CTRL`, `MASSAGE_SEAT_CTRL`, `REAR_CLIMATE_MODULE`, `CABIN_SENSING`, `BIOMETRIC_AUTH`, `CARPAY_CTRL`, `PHONE_AS_KEY`, `OTA_MASTER`, `EDR`, `ROAD_PREVIEW_CAMERA`, `LIDAR`, `REAR_RADAR_MASTER`, `SURROUND_PARK_MASTER` | 기존 ST 체인 흡수, 미구현 1개 Planned 유지 | `ST_BASE_EXT_PT_002`, `ST_BASE_EXT_CH_002`, `ST_BASE_EXT_BODY_002`, `ST_BASE_EXT_IVI_002`, `ST_ADAS_EXT_STATE_001`, `ST_BACKBONE_STATE_001`, `ST_BASE_ALERT_EXT_001`, `ST_BASE_ROBUST_EXT_001`, `ST_OEM_PREMIUM_001` |

---

## 시스템 테스트 시나리오 (공식 표준 양식)

| Scene. ID | 설명 | Pass / Fail | 담당자 | 일자 |
|---|---|---|---|---|
| ST_SPEED_001 | 구간 제한속도 대비 속도 상승/감속 조건에서 경고 활성/해제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_ZONE_001 | 일반/스쿨존/고속 구간 전환 시 구간별 경고 정책이 즉시 반영되는지 확인한다. |  |  |  |
| ST_GUIDE_001 | 유도 구간에서 좌/우 방향 정보가 시각적으로 구분되어 표시되는지 확인한다. |  |  |  |
| ST_GUIDE_002 | 유도 구간 진입/전환/종료 시 경고가 깨지지 않고 기본 상태로 복귀되는지 확인한다. |  |  |  |
| ST_STEER_001 | 고속 구간 무조향 경고 발생 및 조향 복귀 시 해제 동작을 확인한다. |  |  |  |
| ST_EMS_001 | 경찰 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_EMS_002 | 구급 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_001 | 경찰 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_002 | 구급 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_ARB_ETA_001 | 동일 등급 경찰 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_ARB_ETA_002 | 동일 등급 구급 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_TIMEOUT_001 | 긴급 알림 1000ms 무갱신 시 안전 해제 및 복귀 동작을 확인한다. |  |  |  |
| ST_POLICY_001 | 긴급/구간 패턴·색상·문구 정책과 중복 팝업 억제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_SIL_001 | 물리 하드웨어 없이 CANoe SIL에서 핵심 시나리오 수행이 가능한지 확인한다. |  |  |  |
| ST_SIL_002 | CAN+Ethernet(또는 CAN 대체 백본) 동시 통신 조건에서 E2E 경고 체인이 유지되는지 확인한다. |  |  |  |
| ST_RESULT_001 | 시나리오별 합격/불합격 결과가 일관되게 기록·추적되는지 확인한다. |  |  |  |
| ST_BASE_PT_001 | 시동/기어/동력계 상태가 Powertrain 시나리오에서 안정적으로 연동되는지 확인한다. |  |  |  |
| ST_BASE_CH_001 | 가감속/조향/제동 입력이 Chassis 시나리오에서 안전 규칙대로 반영되는지 확인한다. |  |  |  |
| ST_BASE_BODY_001 | 비상등/창문 등 Body 시나리오가 의도한 동작으로 유지되는지 확인한다. |  |  |  |
| ST_BASE_IVI_001 | 클러스터 기본표시/안내/UI 상태가 Infotainment 시나리오에서 일관되게 유지되는지 확인한다. |  |  |  |
| ST_BASE_EXT_BODY_001 | DATC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 Body 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 Infotainment 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_DIAG_001 | 테스트/진단 요청-응답 및 결과 기록이 시나리오 종료까지 추적 가능하게 유지되는지 확인한다. |  |  |  |
| ST_V2_RISK_001 | 긴급차량 근접 위험도 기반 감속 보조 요청과 경고 출력 동기화가 일관되게 동작하는지 확인한다. (SIL Scenario 15/16/17/19) | Ready |  |  |
| ST_V2_FAILSAFE_001 | 도메인 경로 단절 시 자동 감속 보조 금지와 최소 경고 채널 유지 강등이 동작하는지 확인한다. (SIL Scenario 18) | Ready |  |  |
| ST_ADAS_OBJ_001 | 객체 목록 기반 TTC/교차로/합류 위험 경고와 신뢰도 저하 강등/이벤트 기록이 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ALERT_EXT_001 | 방향지시등/주행모드/안전벨트 입력 기반 경보 보정, 접근거리 표시, 이벤트 기록·조회, 표시/음량 설정 반영이 E2E로 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ROBUST_EXT_001 | 입력 유효성/신선도 보호, 상태전이 안정화, 채널 가용성·대체 출력, 오디오 경합/팝업 과밀/채널 동기 복원 정책이 E2E로 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_EXT_CH_002 | 전동 주차/제동 보조 및 차체안정 상태가 시스템 시나리오에서 경고 맥락으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_BODY_002 | 출입 개폐/탑승자 보호/실내 편의 상태가 시스템 시나리오에서 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_IVI_002 | 표시/음향/디지털 접근 서비스 상태가 시스템 시나리오에서 표시/HMI/안내 정책에 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_ADAS_EXT_STATE_001 | 주행 보조/주차 인지/센서 가용성 상태가 시스템 시나리오에서 위험/가용성 판단으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BACKBONE_STATE_001 | 백본 및 도메인 서비스 가용성 상태가 시스템 시나리오에서 경계 가용성/강등 정책으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_PT_002 | 구동/전력변환 및 변속·열관리·충전 인터페이스 상태가 시스템 시나리오에서 구동 준비/서비스 경고 맥락으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_001 | 차량 기본 기능(시동/기어/가감속/조향/비상등/창문/기본표시/도메인경계 + Body/IVI/Powertrain 확장 상태)이 시스템 수준에서 일관되게 동작하는지 확인한다. |  |  |  |
| ST_OEM_SURFACE_001 | OEM100 Active Surface ECU 그룹(A1~A6, B)에서 경계/소유권/헬스 상태가 시스템 시나리오에서 일관되게 유지되는지 확인한다. | Planned |  |  |
| ST_OEM_PREMIUM_001 | Premium Option 그룹(C) 활성 ECU가 기존 경고/표시/강건성 시나리오에 편입될 때 사용자 관찰 결과가 기존 요구를 위반하지 않는지 확인한다. (`NIGHT_VISION` 제외) | Planned |  |  |

---

## 시스템 테스트 추적 상세 표

| ST ID | Req ID | VC ID | 관련 Func | 관련 Flow/Comm | 관련 Var | 선행 IT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| ST_SPEED_001 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010 | Func_001,Func_002,Func_003,Func_004,Func_006,Func_010 | Flow_001,Flow_003 / Comm_001,Comm_003 | Var_012,Var_013,Var_016,Var_031 | IT_CORE_001 | 입력 변동 후 `150ms` 이내 경고 활성/해제 상태가 요구와 일치(`vehicleSpeed > speedLimit`) |
| ST_ZONE_001 | Req_007,Req_008,Req_009 | VC_007,VC_008,VC_009 | Func_007,Func_008,Func_009 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_015,Var_021 | IT_CORE_001, IT_OUT_001 | 구간 전환 후 `150ms` 이내 정책 반영, 출력 주기 `50ms` 유지 |
| ST_GUIDE_001 | Req_014,Req_037 | VC_014,VC_037 | Func_014,Func_039 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_005,Var_023 | IT_CORE_001, IT_OUT_001 | 좌/우 방향 구분 패턴이 명확히 출력 |
| ST_GUIDE_002 | Req_013,Req_015,Req_016,Req_037 | VC_013,VC_015,VC_016,VC_037 | Func_013,Func_015,Func_016,Func_037,Func_038 | Flow_007 / Comm_007 | Var_021,Var_022,Var_023 | IT_OUT_001, IT_TIMEOUT_001 | 진입/전환/종료 시 깜빡임 없이 복귀 |
| ST_STEER_001 | Req_011,Req_012 | VC_011,VC_012 | Func_011,Func_012 | Flow_002 / Comm_002 | Var_014,Var_016 | IT_CORE_001 | 무조향 경고 발생/해제가 각각 `150ms` 이내 반영 |
| ST_EMS_001 | Req_017,Req_019,Req_020,Req_021,Req_022 | VC_017,VC_019,VC_020,VC_021,VC_022 | Func_017,Func_019,Func_020,Func_021,Func_022 | Flow_004,Flow_006,Flow_008 / Comm_004,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 경찰 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_EMS_002 | Req_017,Req_019,Req_020,Req_021,Req_022 | VC_017,VC_019,VC_020,VC_021,VC_022 | Func_018,Func_019,Func_020,Func_021,Func_022 | Flow_005,Flow_006,Flow_008 / Comm_005,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 구급 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_HMI_DIR_001 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 경찰 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_HMI_DIR_002 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 구급 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_ARB_ETA_001 | Req_030,Req_031 | VC_030,VC_031 | Func_030,Func_031 | Flow_006 / Comm_006 | Var_009,Var_010,Var_019 | IT_ARB_001 | 경찰 알림 충돌 시 ETA 우선, 동률 시 SourceID 우선 적용 |
| ST_ARB_ETA_002 | Req_029,Req_030,Req_031 | VC_029,VC_030,VC_031 | Func_029,Func_030,Func_031 | Flow_006 / Comm_006 | Var_007,Var_009,Var_010,Var_019 | IT_ARB_001 | 구급/경찰 충돌 시 구급 우선 후 ETA/SourceID 규칙 적용 |
| ST_TIMEOUT_001 | Req_023,Req_024,Req_033,Req_034 | VC_023,VC_024,VC_033,VC_034 | Func_023,Func_024,Func_033,Func_034 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_017,Var_020,Var_021,Var_024 | IT_TIMEOUT_001 | `1000ms` 무갱신 해제 후 `150ms` 이내 복귀/완화 동작 정상 |
| ST_POLICY_001 | Req_005,Req_025,Req_026,Req_027,Req_028,Req_032,Req_035,Req_040 | VC_005,VC_025,VC_026,VC_027,VC_028,VC_032,VC_035,VC_040 | Func_005,Func_025,Func_026,Func_027,Func_028,Func_032,Func_035,Func_036,Func_040 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_018,Var_019,Var_022,Var_023,Var_024,Var_028,Var_029 | IT_ARB_001, IT_OUT_001 | 중재/표시 정책과 결정론이 요구 기준을 충족 |
| ST_SIL_001 | Req_041 | VC_041 | Func_041 | Flow_009 / Comm_009 | Var_025 | IT_SIL_001 | CANoe SIL 단독 환경에서 시나리오 실행 가능 |
| ST_SIL_002 | Req_042 | VC_042 | Func_042 | Flow_001~Flow_009 / Comm_001~Comm_009 | Var_001~Var_031 | IT_SIL_001 | CAN+Ethernet(또는 CAN 대체 백본) 동시 조건에서 통신/기능 체인 유지 |
| ST_RESULT_001 | Req_043 | VC_043 | Func_043 | Flow_009 / Comm_009 | Var_026 | IT_SIL_001 | 결과 판정 로그와 요약 상태가 일치 |
| ST_BASE_PT_001 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | Func_101,Func_102,Func_110 | Flow_101,Flow_204,Flow_105 / Comm_101,Comm_204,Comm_105 | Var_175~Var_182,Var_298~Var_304,Var_309~Var_314 | IT_BASE_PT_001 | 시동/기어 전환 후 동력계 상태가 `150ms` 이내 반영되고 도메인 경계 연동이 유지 |
| ST_BASE_CH_001 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Func_103,Func_104,Func_105,Func_110 | Flow_102,Flow_201,Flow_105 / Comm_102,Comm_201,Comm_105 | Var_101~Var_120,Var_204~Var_237 | IT_BASE_CH_001 | 가감속/조향/제동 입력 이벤트가 안전 규칙대로 반영되고 상태 연동이 유지 |
| ST_BASE_BODY_001 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | Func_106,Func_107,Func_111 | Flow_103,Flow_202,Flow_105 / Comm_103,Comm_202,Comm_105 | Var_121~Var_146,Var_238~Var_267 | IT_BASE_BODY_001 | 비상등/창문 시나리오에서 출력과 상태가 기대값으로 유지 |
| ST_BASE_IVI_001 | Req_109,Req_111 | VC_109,VC_111 | Func_109,Func_111 | Flow_104,Flow_203,Flow_105 / Comm_104,Comm_203,Comm_105 | Var_147~Var_171,Var_268~Var_297 | IT_BASE_IVI_001 | 표시/UI 이벤트가 누락 없이 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_EXT_BODY_001 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Flow_202,Flow_105 / Comm_202,Comm_105 | Var_238~Var_267 | IT_BASE_EXT_BODY_001 | DATC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 `150ms` 이내 반영되고 범위/매핑 규칙을 만족 |
| ST_BASE_EXT_IVI_001 | Req_119 | VC_119 | Func_119 | Flow_203,Flow_105 / Comm_203,Comm_105 | Var_268~Var_271,Var_289~Var_290 | IT_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 `150ms` 이내 HMI 정책으로 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_DIAG_001 | Req_112 | VC_112 | Func_112 | Flow_106,Flow_205 / Comm_106,Comm_205 | Var_172~Var_174 | IT_BASE_DIAG_001 | 진단 요청-응답 및 결과 로그가 시나리오 단위로 추적 가능하게 기록 |
| ST_V2_RISK_001 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | Func_120,Func_121,Func_125,Func_126,Func_123 | Flow_120,Flow_121,Flow_122,Flow_123 / Comm_120,Comm_121,Comm_122,Comm_123 | Var_320,Var_321,Var_322,Var_323,Var_324,Var_325 | IT_V2_RISK_001 | 위험도 산정 주기 `100ms`, 감속 보조 요청 생성/해제 `150ms` 이내, Ambient/Cluster 동기 오프셋 `<=50ms` (SIL Scenario 15/16/17/19) |
| ST_V2_FAILSAFE_001 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | Func_127,Func_128,Func_129 | Flow_124 / Comm_124 | Var_326,Var_327,Var_328,Var_329 | IT_V2_FAILSAFE_001 | 단절 감지 후 `150ms` 이내 failSafeMode 전환, 자동 감속 보조 0건, 최소 경고 채널 유지 (SIL Scenario 18) |
| ST_ADAS_OBJ_001 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | Func_130,Func_131,Func_132,Func_133,Func_134,Func_135,Func_136,Func_137,Func_138,Func_139 | Flow_130,Flow_131,Flow_132,Flow_133 / Comm_130,Comm_131,Comm_132,Comm_133 | Var_330,Var_331,Var_332,Var_333,Var_334,Var_335,Var_336,Var_337,Var_338,Var_339 | IT_ADAS_OBJ_001 | 객체 입력 반영 `100ms`, 경고/강등 반영 `150ms`, 이벤트 기록 누락 0건 및 우선순위 결정론 유지(Pre-Activation) |
| ST_BASE_ALERT_EXT_001 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | Func_140,Func_141,Func_142,Func_143,Func_144,Func_145,Func_146,Func_147 | Flow_103,Flow_104,Flow_105,Flow_203,Flow_006,Flow_008 / Comm_103,Comm_104,Comm_105,Comm_203,Comm_006,Comm_008 | Var_009,Var_012,Var_024,Var_029,Var_133,Var_138,Var_139,Var_141,Var_155,Var_164,Var_166,Var_167,Var_168,Var_191,Var_192,Var_193,Var_268,Var_281,Var_282 | IT_BASE_ALERT_EXT_001 | 맥락 보정/거리 표시/이력 조회/설정 반영 체인이 E2E에서 수치 기준(`150ms`,`200ms`)과 기록 기준(누락 0건)을 충족(Pre-Activation) |
| ST_BASE_ROBUST_EXT_001 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | Func_148,Func_149,Func_150,Func_151,Func_152,Func_153,Func_154,Func_155 | Flow_130,Flow_133,Flow_006,Flow_007,Flow_008,Flow_104,Flow_105,Flow_124,Flow_203 / Comm_130,Comm_133,Comm_006,Comm_007,Comm_008,Comm_104,Comm_105,Comm_124,Comm_203 | Var_330,Var_333,Var_334,Var_016,Var_020,Var_021,Var_024,Var_027,Var_028,Var_166,Var_167,Var_168,Var_180,Var_268,Var_269,Var_289,Var_296,Var_297,Var_326,Var_327,Var_328,Var_282 | IT_BASE_ROBUST_EXT_001 | 입력 유효성 필터링 `100ms`, stale/전이 안정화 `150ms`, 채널 가용성·대체 출력 `150ms`, 오디오 경합·팝업 과밀·채널 동기 복원 `150ms` 기준 충족(Pre-Activation) |
| ST_BASE_EXT_CH_002 | Req_156,Req_157 | VC_156,VC_157 | Func_156,Func_157 | Flow_206 / Comm_206 | Var_340,Var_341,Var_342,Var_343 | IT_BASE_EXT_CH_002 | 제동/차체안정 상태가 `150ms` 이내 경고 맥락에 반영되고 상태 누락 0건 |
| ST_BASE_EXT_BODY_002 | Req_158,Req_159,Req_160 | VC_158,VC_159,VC_160 | Func_158,Func_159,Func_160 | Flow_207 / Comm_207 | Var_344,Var_345,Var_346,Var_367 | IT_BASE_EXT_BODY_002 | 출입/탑승자보호/실내편의 상태가 `150ms` 이내 정책 반영되고 상태 누락 0건 |
| ST_BASE_EXT_IVI_002 | Req_161,Req_162 | VC_161,VC_162 | Func_161,Func_162 | Flow_208 / Comm_208 | Var_347,Var_348,Var_349 | IT_BASE_EXT_IVI_002 | 표시/음향/디지털 접근 서비스 상태가 `150ms` 이내 표시/안내 정책 반영 |
| ST_ADAS_EXT_STATE_001 | Req_163,Req_164,Req_165 | VC_163,VC_164,VC_165 | Func_163,Func_164,Func_165 | Flow_209 / Comm_209 | Var_350,Var_351,Var_352 | IT_ADAS_EXT_STATE_001 | 주행보조/주차인지/센서가용성 상태 수신 `100ms`, 위험/강등 정책 반영 `150ms` 기준 충족 |
| ST_BACKBONE_STATE_001 | Req_166 | VC_166 | Func_166 | Flow_210 / Comm_210 | Var_353,Var_326,Var_328 | IT_BACKBONE_STATE_001 | 백본/도메인 서비스 상태가 `100ms` 이내 경계 가용성/강등 정책에 반영 |
| ST_BASE_EXT_PT_002 | Req_167,Req_168 | VC_167,VC_168 | Func_167,Func_168 | Flow_204 / Comm_204 | Var_354~Var_366 | IT_BASE_EXT_PT_002 | 구동/전력변환 및 변속·열관리·충전 인터페이스 상태가 `150ms` 이내 구동 준비/서비스 경고 맥락에 반영되고 상태 누락 0건 |
| ST_BASE_001 | Req_101~Req_107,Req_109~Req_119,Req_167,Req_168 | VC_101~VC_107,VC_109~VC_119,VC_167,VC_168 | Func_101~Func_107,Func_109~Func_119,Func_167,Func_168 | Flow_101~Flow_106,Flow_201~Flow_205 / Comm_101~Comm_106,Comm_201~Comm_205 | Var_101~Var_314,Var_354~Var_367 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_EXT_PT_002, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_BASE_EXT_BODY_001, IT_BASE_EXT_IVI_001, IT_BASE_DIAG_001 | 차량 기본 기능 E2E 시나리오에서 입력/상태/표시/경계/판정 체인이 일관되게 유지 |
| ST_OEM_SURFACE_001 | Req_041,Req_042,Req_043,Req_110,Req_111,Req_151,Req_152 | VC_041,VC_042,VC_043,VC_110,VC_111,VC_151,VC_152 | Func_041,Func_042,Func_043,Func_110,Func_111,Func_151,Func_152 | Flow_009,Flow_105,Flow_106,Flow_124,Flow_205 / Comm_009,Comm_105,Comm_106,Comm_124,Comm_205 | Var_025,Var_026,Var_118~Var_120,Var_169~Var_171,Var_172~Var_174,Var_180,Var_326~Var_328 | IT_OEM_SURFACE_001, IT_SIL_001 | Active Surface 그룹 경계/헬스/가용성 판정이 누락 없이 유지되고 대체 출력 규칙 위반 0건 |
| ST_OEM_PREMIUM_001 | Req_113,Req_116,Req_118,Req_119,Req_140,Req_141,Req_142,Req_146,Req_147,Req_153,Req_154,Req_155 | VC_113,VC_116,VC_118,VC_119,VC_140,VC_141,VC_142,VC_146,VC_147,VC_153,VC_154,VC_155 | Func_113,Func_116,Func_118,Func_119,Func_140,Func_141,Func_142,Func_146,Func_147,Func_153,Func_154,Func_155 | Flow_202,Flow_203,Flow_103,Flow_104,Flow_105,Flow_008 / Comm_202,Comm_203,Comm_103,Comm_104,Comm_105,Comm_008 | Var_133,Var_138,Var_139,Var_141,Var_155,Var_164,Var_166,Var_167,Var_168,Var_191,Var_192,Var_193,Var_268,Var_281,Var_282,Var_289,Var_296,Var_297 | IT_OEM_PREMIUM_001, IT_BASE_ALERT_EXT_001 | Premium Active ECU 편입 후에도 경고 인지/설정/강건성 기준 위반 0건, `NIGHT_VISION`은 Planned 상태 유지 |

---

## Legacy Req 상속 매핑 (ST 기준)

| Legacy Req ID | Active Req ID | 상속 ST | 상속 VC | 상속 규칙 |
|---|---|---|---|---|
| Req_018 | Req_017 | ST_EMS_002 | VC_017 | 구급차 분리 요구는 긴급차량 접근 통합 요구(Req_017)의 ST 결과를 상속한다. |
| Req_036 | Req_035 | ST_POLICY_001 | VC_035 | 긴급 패턴 분리 요구는 긴급 시각표현 통합 요구(Req_035)의 ST 결과를 상속한다. |
| Req_038 | Req_037 | ST_GUIDE_002 | VC_037 | 고속도로 패턴 분리 요구는 구간 패턴 통합 요구(Req_037)의 ST 결과를 상속한다. |
| Req_039 | Req_037 | ST_GUIDE_001 | VC_037 | 유도선 패턴 분리 요구는 구간 패턴 통합 요구(Req_037)의 ST 결과를 상속한다. |
| Req_108 | Req_113,Req_116,Req_118 | ST_BASE_EXT_BODY_001 | VC_113,VC_116,VC_118 | 운전자 상태 단일 레벨 요구는 Body 확장 상태 묶음 검증 결과로 상속한다. |
| Req_114 | Req_113 | ST_BASE_EXT_BODY_001 | VC_113 | 시트 상태 단독 요구는 실내편의 통합 요구(Req_113)의 ST 결과를 상속한다. |
| Req_115 | Req_113 | ST_BASE_EXT_BODY_001 | VC_113 | 미러 상태 단독 요구는 실내편의 통합 요구(Req_113)의 ST 결과를 상속한다. |
| Req_117 | Req_116 | ST_BASE_EXT_BODY_001 | VC_116 | 와이퍼/우적 연동 단독 요구는 차체 제어 통합 요구(Req_116)의 ST 결과를 상속한다. |
| Req_122 | Req_125 | ST_V2_RISK_001 | VC_125 | 감속 보조 중 긴급 최우선 단독 요구는 V2 통합 요구(Req_125)의 ST 결과를 상속한다. |
| Req_124 | Req_127,Req_128,Req_129 | ST_V2_FAILSAFE_001 | VC_127,VC_128,VC_129 | 도메인 단절 대응 단일 요구는 금지/최소유지/강등 3분할 요구의 ST 결과를 상속한다. |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 5.22 | 2026-03-09 | OEM100 ST-IT 정합 보강: `ST_OEM_SURFACE_001`, `ST_OEM_PREMIUM_001`의 선행 IT를 `IT_OEM_SURFACE_001`, `IT_OEM_PREMIUM_001` 중심으로 동기화. |
| 5.21 | 2026-03-09 | 본문 실내용 보강: `OEM100 Surface 상세-ST 매핑` 표를 추가하고, `ST_OEM_SURFACE_001`, `ST_OEM_PREMIUM_001` 시나리오 및 추적 상세를 신설. |
| 5.20 | 2026-03-09 | OEM100 시스템 검증 원칙 보강: `시나리오 확장 원칙` 섹션을 추가해 Surface 확장 시 ST 운영 기준(핵심 시나리오 축 유지, Active/Validation/Placeholder 분리)을 명시. |
| 5.19 | 2026-03-06 | Legacy 누락군 보강: `Req_018/036/038/039/108/114/115/117/122/124` 상속 관계를 `Legacy Req 상속 매핑` 섹션으로 추가해 ST 추적 누락을 해소. |
| 5.18 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `ST_BASE_ROBUST_EXT_001` 추가, `Req_148~Req_155`/`Flow·Comm_130·133·006·007·008·104·105·124·203`/`Var_016...334` 추적을 동기화. |
| 5.17 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `ST_BASE_ALERT_EXT_001` 추가, `Req_140~Req_147`/`Flow·Comm_103·104·105·203·006·008`/`Var_133...282` 추적을 동기화. |
| 5.16 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `ST_ADAS_OBJ_001`을 추가하고 `Req_130~Req_139`/`Flow_130~133`/`Comm_130~133`/`Var_330~339` 추적을 동기화. |
| 5.15 | 2026-03-06 | 미사용 체인 정리: `Req/VC/Func_108`을 `ST_BASE_BODY_001/ST_BASE_001`에서 제거하고 Baseline 범위를 `108 제외`로 동기화. |
| 5.14 | 2026-03-04 | 멘토링 체크리스트 반영: ST 작성 원칙에 Panel 검증 우선순위(`차량 화면 -> 제어 패널 -> 상태 모니터`)를 추가. |
| 5.13 | 2026-03-03 | V2 ST를 구현 활성 상태로 전환하고 `ST_V2_RISK_001`, `ST_V2_FAILSAFE_001` 상태를 Ready로 갱신. |
| 5.12 | 2026-03-02 | V2 확장(Pre-Activation) ST 반영: `ST_V2_RISK_001`, `ST_V2_FAILSAFE_001` 추가 및 `Req_120~Req_121, Req_123, Req_125~Req_129` 추적 체인(`IT_V2_RISK_001`, `IT_V2_FAILSAFE_001`) 연결. |
| 5.11 | 2026-03-02 | 작성 원칙에 CANoe.CAN 실행 제약 임시 주석을 추가하고, `ST_SIL_002` 시나리오/합격기준에 CAN 대체 백본 조건을 병기. |
| 5.10 | 2026-03-02 | 차량 기본 기능 확장 추적 보강: `Req/VC/Func_113~119`를 반영한 `ST_BASE_EXT_BODY_001`, `ST_BASE_EXT_IVI_001` 추가 및 `ST_BASE_001` 범위 확장(Req_101~119). |
| 5.9 | 2026-03-02 | 증적 경로 규칙 고정: ST 실행 증적 저장 경로를 `canoe/logging/evidence/ST/`로 명시. |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-23 | 구버전 Scene 구조 반영 |
| 3.0 | 2026-02-23 | 운전자 행동 중심 서술 전환 |
| 4.0 | 2026-02-24 | 구버전 OTA 시나리오 확장 |
| 5.0 | 2026-02-26 | 옵션1 아키텍처/Req_001~043 기준으로 전면 재작성. ST ID 체계 및 IT-Req 추적표 추가 |
| 5.1 | 2026-02-26 | 합격 기준을 150ms/1000ms 및 주기 기준으로 수치화하고, FZ 사전 점검 결과 반영 전 Draft 경계 문구 추가 |
| 5.2 | 2026-02-26 | VC 추적 강화를 위해 ST 상세 표에 VC ID 컬럼을 추가하고 Req-VC-ST 연결을 명시 |
| 5.3 | 2026-02-28 | ST_SPEED_001에 `speedLimit` 기반 과속 조건과 Flow_003/Comm_003/Var_031 연계를 반영. |
| 5.4 | 2026-02-28 | 차량 기본 기능 시스템 검증을 위해 `ST_BASE_001`(Req/VC/Func 101~112, Flow/Comm 101~106 및 201~205)을 추가. |
| 5.5 | 2026-02-28 | 06 문서 Lean IT 재구성 반영: ST 선행 IT 참조를 핵심 통합 체인(`IT_CORE/EMS/ARB/OUT/TIMEOUT/SIL/BASE`)으로 정렬. |
| 5.6 | 2026-02-28 | Lean IT 재구성 후 잔여 참조 ID 정리(`ST_POLICY_001` 선행 IT에서 구 ID 제거) 및 최신 IT 체계 동기화. |
| 5.7 | 2026-02-28 | 차량 기본 기능 확장 반영: `ST_BASE_001` 선행 IT를 도메인별 통합 ID(`IT_BASE_PT/CH/BODY/IVI/DIAG`)까지 연결. |
| 5.8 | 2026-02-28 | 확장된 요구/통신 기준 반영: 도메인별 시스템 시나리오(`ST_BASE_PT/CH/BODY/IVI/DIAG`) 추가 및 ST 작성원칙을 블랙박스(E2E) 중심으로 정렬. |
