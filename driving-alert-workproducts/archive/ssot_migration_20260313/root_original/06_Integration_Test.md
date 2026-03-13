# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 (Software Integration and Integration Test)
**ASPICE Reference**: SWE.5 (Software Integration and Integration Test)
**Version**: 4.22
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 중단 (SWE.5) | `06_Integration_Test.md` | `05_Unit_Test.md` | `07_System_Test.md` |

---

## 작성 원칙

- 본 문서는 모듈 간 인터페이스/흐름(Flow, Comm) 연동 검증을 수행한다.
- 상단 표는 샘플 형식(`테스트 ID/요구사항 ID/테스트 목적/예상 결과/...`)을 유지한다.
- 상세 추적은 하단 IT-Flow/Comm 연계 표로 분리하며 Req-VC-IT 추적을 유지한다.
- 범위는 CANoe SIL, CAN+Ethernet으로 고정한다.
- 임시 주석(실행 제약): 현재 CANoe.CAN 라이선스 환경에서는 SIL 실행 시 Ethernet 구간을 CAN 대체 백본으로 검증하며, Ethernet 라이선스 확보 후 동일 IT 케이스로 재검증한다.
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 수행결과를 기입한다.
- 대조군/우수성 비교 실험은 본 문서 범위 밖으로 두며, 요구사항 충족 Pass/Fail 증빙을 우선한다.
- IT는 인터페이스/흐름 중심의 핵심 체인만 유지한다(Lean IT).
- 세부 경계값/미세 분기는 원칙적으로 UT(05)와 ST(07)에서 검증하고, 인터페이스 리스크가 큰 항목은 IT 보강 케이스로 선별 검증한다.
- IT 증적(로그/캡처/리포트)은 `canoe/logging/evidence/IT/` 경로 규칙으로 관리한다.
- IT 증적 포맷/채점 규칙은 `canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md`를 따른다.
- 검증 배치 실행/리포트 생성은 `scripts/run.py verify batch`를 사용하고, 출력 포맷은 기본 `json,md`(옵션 `--report-formats csv`)를 적용한다.
- V2 확장 요구(`Req_120~Req_121, Req_123, Req_125~Req_129`)는 구현 활성 상태로 IT 항목을 관리하며, SIL 시나리오 15~19와 연계해 검증한다.
- ADAS 객체 인지 확장(`Req_130~Req_139`)은 Pre-Activation(설계 선반영) IT 항목(`IT_ADAS_OBJ_001`)으로 관리한다.
- 차량 경보 편의 확장(`Req_140~Req_147`)은 Pre-Activation(설계 선반영) IT 항목(`IT_BASE_ALERT_EXT_001`)으로 관리한다.
- 경고 강건성·인지성 확장(`Req_148~Req_155`)은 Pre-Activation(설계 선반영) IT 항목(`IT_BASE_ROBUST_EXT_001`)으로 관리한다.

---

## 05-06 동기화 기준 (OEM100 Surface ECU)

### 동기화 원칙

- 06은 Surface ECU 개별 IT를 강제하지 않고, 인터페이스 리스크 기준의 도메인/기능 묶음 IT로 커버한다.
- Surface 수량 변경 시 IT 케이스 수를 동일 비율로 늘리지 않고, `요구 기능/인터페이스 변경`이 있을 때만 IT를 증설한다.
- Placeholder Surface ECU는 실행 IT 대상이 아니라 `미구현(계획)` 상태로 유지하고, 컴파일/정합 확인 대상으로만 관리한다.
- Surface ECU 최신 수량/상태는 `00e_ECU_Naming_Standard.md`를 기준으로 참조한다.

### DEV2 테스트 설계 전달 규칙

| 항목 | 규칙 |
|---|---|
| 테스트 오케스트레이션 단위 | `Req/VC`와 `Flow/Comm` 기반 묶음 IT를 기준으로 배치 실행 |
| Surface 확장 대응 | 신규 Active Surface가 기존 Flow/Comm에 편입되면 기존 IT에 흡수, 신규 인터페이스가 생기면 IT 신설 |
| Placeholder 대응 | 실행 실패 처리 대상이 아니라 `Not Implemented` 분류로 리포트 분리 |
| 증적 기준 | `json/md` 산출물에서 IT ID, Req/VC, Pass/Fail, 미구현 상태를 분리 기록 |

### OEM100 Surface 상세-IT 매핑 (실제 본문 운영)

| 그룹 | Surface ECU(실명) | IT 커버 방식 | 주요 IT ID |
|---|---|---|---|
| A1 Infrastructure/Integration | `CGW`, `ETH_BACKBONE`, `DCM`, `IBOX`, `SGW` | 경계/서비스 가용성 중심 IT | `IT_OEM_SURFACE_001`, `IT_BACKBONE_STATE_001` |
| A2 Powertrain | `EMS`, `TCU`, `VCU`, `_4WD`, `BAT_BMS`, `FPCM`, `LVR`, `ISG`, `EOP`, `EWP` | 동력/상태 전달 IT | `IT_BASE_PT_001`, `IT_BASE_EXT_PT_002`, `IT_BASE_001` |
| A3 Chassis/Safety | `ESC`, `MDPS`, `ABS`, `EPB`, `TPMS`, `SAS`, `ECS`, `ACU`, `ODS`, `VSM`, `EHB`, `CDC` | 제동/조향/차체상태 IT | `IT_BASE_CH_001`, `IT_BASE_001` |
| A4 Body/Comfort | `BCM`, `DATC`, `SMK`, `AFLS`, `AHLS`, `WIPER_MODULE`, `SUNROOF_MODULE`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `TAILGATE_MODULE`, `SEAT_DRV`, `SEAT_PASS`, `MIRROR_MODULE`, `BODY_SECURITY_MODULE` | 바디/편의 제어 IT | `IT_BASE_BODY_001`, `IT_BASE_EXT_BODY_001`, `IT_BASE_EXT_BODY_002`, `IT_BASE_001` |
| A5 IVI/HMI/Connectivity | `IVI`, `CLU`, `HUD`, `TMU`, `AMP`, `PGS`, `NAV_MODULE`, `VOICE_ASSIST`, `RSE`, `DIGITAL_KEY` | HMI/표시/음향 IT | `IT_OUT_001`, `IT_BASE_IVI_001`, `IT_BASE_EXT_IVI_001` |
| A6 ADAS/V2X/Parking | `ADAS`, `V2X`, `SCC`, `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PARK_ULTRASONIC`, `DMS`, `OMS` | 핵심 경보/중재/객체위험 IT | `IT_CORE_001`, `IT_EMS_001`, `IT_ARB_001`, `IT_V2_RISK_001`, `IT_ADAS_OBJ_001` |
| C Premium Option | `OBC`, `DCDC`, `MCU`, `INVERTER`, `CHARGE_PORT_CTRL`, `AIR_SUSPENSION`, `RWS`, `NIGHT_VISION`, `AEB_DOMAIN`, `HIGHWAY_PILOT`, `PARK_MASTER`, `TRAILER_CTRL`, `HEADLAMP_LEVELING`, `AUTO_DOOR_CTRL`, `POWER_TAILGATE_CTRL`, `MASSAGE_SEAT_CTRL`, `REAR_CLIMATE_MODULE`, `CABIN_SENSING`, `BIOMETRIC_AUTH`, `CARPAY_CTRL`, `PHONE_AS_KEY`, `OTA_MASTER`, `EDR`, `ROAD_PREVIEW_CAMERA`, `LIDAR`, `REAR_RADAR_MASTER`, `SURROUND_PARK_MASTER` | 기존 IT 체인 흡수, 미구현 1개 계획 상태 | `IT_BASE_EXT_PT_002`, `IT_BASE_EXT_CH_002`, `IT_BASE_EXT_BODY_002`, `IT_BASE_EXT_IVI_002`, `IT_ADAS_EXT_STATE_001`, `IT_BACKBONE_STATE_001`, `IT_BASE_ALERT_EXT_001`, `IT_BASE_ROBUST_EXT_001` |

---

## 통합 테스트 표 (공식 표준 양식)

| 테스트 ID | 요구사항 ID | VC ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | 차량 속도, 조향, 구간 정보가 함께 들어올 때 기본 경고 판단 통합 검증 | 입력 변화 후 `150ms` 이내 기본 경고와 구간 정보가 정상 반영되고 통신 누락이 없다 |  |  |  |
| IT_EMS_001 | Req_017,Req_023 | VC_017,VC_023 | 경찰, 구급 긴급 알림 송수신 통합 검증 | 긴급 알림 송수신이 일치하고 송신 주기 `100ms`가 유지되며 `150ms` 이내 경고 판단에 반영된다 |  |  |  |
| IT_ARB_001 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | 긴급 경고와 구간 경고가 동시에 발생할 때 우선순위 통합 검증 | 긴급 경고가 구간 경고보다 우선하고, 구급이 경찰보다 우선하며, 도착예정시간과 발신원 기준으로 단일 경고가 일관되게 결정된다 |  |  |  |
| IT_OUT_001 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_037,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | 경고 판단 결과가 앰비언트와 클러스터에 올바르게 전달되는지 통합 검증 | 문구, 색상, 패턴, 복귀 동작이 일치하고 출력 주기 `50ms`가 유지된다 |  |  |  |
| IT_TIMEOUT_001 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | 긴급 알림 미수신 시 안전 해제와 복귀 통합 검증 | `1000ms` 동안 갱신이 없으면 경고가 안전하게 해제되고 `150ms` 이내 기본 상태로 복귀하며 중복 토글이 없다 |  |  |  |
| IT_V2_RISK_001 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | 긴급차량 근접 위험도 기반 감속 보조 요청과 경고 출력 통합 검증 | 위험도 임계값 초과 시 `150ms` 이내 감속 보조 요청이 생성되고, 활성 상태에서 앰비언트와 클러스터 출력 차이는 `50ms` 이내이며, 운전자 개입 시 `150ms` 이내 해제된다 (SIL Scenario 15/16/17/19) | Ready |  |  |
| IT_V2_FAILSAFE_001 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | 도메인 경로 단절 시 강등 동작 통합 검증 | 단절 감지 후 `150ms` 이내 강등 상태로 전환되고 자동 감속 보조는 발생하지 않으며 최소 경고 채널은 유지된다 (SIL Scenario 18) | Ready |  |  |
| IT_ADAS_OBJ_001 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | 객체 목록, 상대속도, 교차로, 합류 위험 반영 통합 검증 | 객체 입력은 `100ms` 이내 반영되고 위험 경고는 `150ms` 이내 발생하며 신뢰도 저하 시 강등과 이벤트 기록이 누락 없이 수행된다 | Planned |  |  |
| IT_BASE_ALERT_EXT_001 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | 방향지시등, 주행모드, 안전벨트, 접근거리, 표시 설정, 음량 설정 반영 통합 검증 | 입력 보정은 `150ms` 이내 반영되고 접근거리 표시는 `200ms` 이내 갱신되며 이벤트 기록 누락이 없고 표시·음량 설정은 `150ms` 이내 반영된다 | Planned |  |  |
| IT_BASE_ROBUST_EXT_001 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | 입력 지연 감지, 상태 전이 안정화, 채널 전환, 오디오 경합 대응 통합 검증 | 입력 지연 감지는 `100ms`, 상태 전이 안정화는 `150ms`, 채널 전환과 오디오 경합 대응은 `150ms` 기준을 충족한다 | Planned |  |  |
| IT_BASE_001 | Req_101~Req_107,Req_109,Req_113~Req_119,Req_167,Req_168 | VC_101~VC_107,VC_109,VC_113~VC_119,VC_167,VC_168 | 시동, 기어, 가감속, 조향, 비상등, 창문, 표시, 주요 확장 상태 통합 검증 | 기본 차량 기능과 주요 확장 기능이 함께 동작해도 기본 상태와 표시가 일관되게 유지된다 |  |  |  |
| IT_BASE_PT_001 | Req_101,Req_102 | VC_101,VC_102 | 엔진, 변속, 동력 상태 통합 검증 | 엔진, 변속, 동력 상태가 `100ms` 주기로 일관되게 반영된다 |  |  |  |
| IT_BASE_CH_001 | Req_103,Req_104,Req_105 | VC_103,VC_104,VC_105 | 가감속, 조향, 제동, 차체 상태 통합 검증 | 입력과 차체 상태 정보가 `100ms` 기준으로 일관되게 반영된다 |  |  |  |
| IT_BASE_BODY_001 | Req_106,Req_107 | VC_106,VC_107 | 비상등, 창문, 차체 편의 상태 통합 검증 | 차체 제어 상태가 일관되게 유지된다 |  |  |  |
| IT_BASE_IVI_001 | Req_109 | VC_109 | 기본 표시, UI 연동 통합 검증 | 표시 상태와 연계 이벤트가 50/100ms 규칙을 만족한다 |  |  |  |
| IT_BASE_EXT_BODY_001 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | 공조, 시트, 미러, 도어, 와이퍼, 보안 상태 통합 검증 | 관련 상태와 제어 정보가 `100ms` 주기로 연계되고 `150ms` 이내 정책에 반영된다 |  |  |  |
| IT_BASE_EXT_IVI_001 | Req_119 | VC_119 | 오디오, 음성 안내, TTS 상태 통합 검증 | 오디오와 음성 상태가 50/100ms 규칙을 만족하고 `150ms` 이내 HMI 정책에 반영된다 |  |  |  |
| IT_OEM_SURFACE_001 | Req_151,Req_152 | VC_151,VC_152 | 주요 Active Surface ECU의 출력 채널 가용성과 대체 출력 통합 검증 | 경계와 상태 이상이 누락 없이 전달되고 대체 출력 전환 규칙이 `150ms` 내 충족된다 | Planned |  |  |
| IT_OEM_PREMIUM_001 | Req_113,Req_116,Req_118,Req_119,Req_140,Req_141,Req_142,Req_146,Req_147,Req_153,Req_154,Req_155 | VC_113,VC_116,VC_118,VC_119,VC_140,VC_141,VC_142,VC_146,VC_147,VC_153,VC_154,VC_155 | Premium Option ECU 편입 영향 통합 검증(`NIGHT_VISION` 제외) | Premium Option ECU가 편입되어도 기존 검증 항목이 유지되고 `NIGHT_VISION`은 Not Implemented로 분리 기록된다 | Planned |  |  |
| IT_BASE_EXT_CH_002 | Req_156,Req_157 | VC_156,VC_157 | EPB, EHB, VSM, ECS, CDC 상태 통합 검증 | 제동과 차체 제어 상태가 `100ms` 주기로 반영되고 `150ms` 이내 경고 맥락에 반영된다 | Ready |  |  |
| IT_BASE_EXT_BODY_002 | Req_158,Req_159,Req_160 | VC_158,VC_159,VC_160 | 도어, 테일게이트, 에어백, 탑승자 감지, 공조, 시트, 선루프 상태 통합 검증 | 관련 상태가 `100ms` 주기로 반영되고 `150ms` 이내 정책에 반영된다 | Ready |  |  |
| IT_BASE_EXT_IVI_002 | Req_161,Req_162 | VC_161,VC_162 | HUD, AMP, TMU, 디지털 접근 서비스 상태 통합 검증 | 관련 서비스 상태가 `100ms` 주기로 반영되고 `150ms` 이내 표시와 안내 정책에 반영된다 | Ready |  |  |
| IT_ADAS_EXT_STATE_001 | Req_163,Req_164,Req_165 | VC_163,VC_164,VC_165 | SCC, 주차 보조, 주변 센서 상태 통합 검증 | 관련 상태가 `100ms` 주기로 반영되고 `150ms` 이내 위험, 가용성, 강등 정책에 반영된다 | Ready |  |  |
| IT_BACKBONE_STATE_001 | Req_166 | VC_166 | IBOX, SGW, DCM 등 도메인 서비스 가용성 상태 통합 검증 | 관련 서비스 상태가 `100ms` 주기로 반영되고 경계 가용성과 강등 상태가 즉시 반영된다 | Ready |  |  |
| IT_BASE_EXT_PT_002 | Req_167,Req_168 | VC_167,VC_168 | OBC, DCDC, MCU, INVERTER 상태 통합 검증 | 전력, 충전, 구동 상태가 `100ms` 주기로 반영되고 `150ms` 이내 구동 준비와 서비스 경고 맥락에 반영된다 | Ready |  |  |

---

## 통합 테스트 추적 상세 표

| IT ID | 관련 Flow | 관련 Comm | 관련 Func | 관련 Req | 관련 VC | 선행 UT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Flow_001,Flow_002,Flow_003 | Comm_001,Comm_002,Comm_003 | Func_001~Func_012 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | UT_ADAS_001, UT_NAV_001, UT_GW_001 | 입력 `100ms` + 출력 `50ms` 기준 `150ms` 이내 반영 |
| IT_EMS_001 | Flow_004,Flow_005,Flow_006 | Comm_004,Comm_005,Comm_006 | Func_017,Func_018,Func_023 | Req_017,Req_023 | VC_017,VC_023 | UT_EMS_POL_001, UT_EMS_AMB_001, UT_EMS_RX_001 | Active/Clear 송수신 상태 일치, 송신주기 `100ms` 유지 |
| IT_ARB_001 | Flow_006 | Comm_006 | Func_022,Func_025,Func_027~Func_032 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | UT_ARB_001 | 우선순위/동률 규칙 결과가 기대값과 일치 |
| IT_OUT_001 | Flow_007,Flow_008 | Comm_007,Comm_008 | Func_005,Func_008,Func_009,Func_013~Func_016,Func_019~Func_021,Func_026,Func_033~Func_040 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_037,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | UT_BCM_001, UT_CLU_001, UT_OUT_GW_001 | Ambient/Cluster 출력이 정책표와 일치, 출력 주기 `50ms` 유지 |
| IT_TIMEOUT_001 | Flow_006,Flow_007,Flow_008 | Comm_006,Comm_007,Comm_008 | Func_024,Func_033,Func_034 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | UT_EMS_RX_001, UT_BCM_001 | `1000ms` 무갱신 후 timeoutClear=1, `150ms` 이내 복귀 완료 |
| IT_V2_RISK_001 | Flow_120,Flow_121,Flow_122,Flow_123 | Comm_120,Comm_121,Comm_122,Comm_123 | Func_120,Func_121,Func_125,Func_126,Func_123 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | UT_V2_RISK_001, UT_V2_RELEASE_001 | 위험도 기반 보조 요청 생성/경고 동기화/운전자 개입 해제가 수치 기준(`100ms`,`150ms`,`<=50ms`) 충족 (SIL Scenario 15/16/17/19) |
| IT_V2_FAILSAFE_001 | Flow_124 | Comm_124 | Func_127,Func_128,Func_129 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | UT_V2_FAILSAFE_001 | 경로 단절 감지 후 `150ms` 이내 강등 전환, 자동 감속 보조 0건, 최소 경고 채널 유지 (SIL Scenario 18) |
| IT_ADAS_OBJ_001 | Flow_130,Flow_131,Flow_132,Flow_133 | Comm_130,Comm_131,Comm_132,Comm_133 | Func_130,Func_131,Func_132,Func_133,Func_134,Func_135,Func_136,Func_137,Func_138,Func_139 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | UT_ADAS_OBJ_RISK_001, UT_ADAS_OBJ_SAFETY_001 | 객체 기반 위험 경고/강등/이벤트 체인이 수치 기준(`100ms`,`150ms`)과 정책 일관성 기준을 충족(Pre-Activation) |
| IT_BASE_ALERT_EXT_001 | Flow_103,Flow_104,Flow_105,Flow_203,Flow_006,Flow_008 | Comm_103,Comm_104,Comm_105,Comm_203,Comm_006,Comm_008 | Func_140,Func_141,Func_142,Func_143,Func_144,Func_145,Func_146,Func_147 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | UT_BASE_ALERT_EXT_001 | 입력 맥락 보정 `150ms`, 거리 표시 `200ms`, 이벤트 기록 누락 0건, 표시/음량 설정 반영 `150ms` 기준 충족(Pre-Activation) |
| IT_BASE_ROBUST_EXT_001 | Flow_130,Flow_133,Flow_006,Flow_007,Flow_008,Flow_104,Flow_105,Flow_124,Flow_203 | Comm_130,Comm_133,Comm_006,Comm_007,Comm_008,Comm_104,Comm_105,Comm_124,Comm_203 | Func_148,Func_149,Func_150,Func_151,Func_152,Func_153,Func_154,Func_155 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | UT_BASE_ROBUST_EXT_001 | 입력 유효성/신선도 보호, 전이 안정화, 채널 가용성·대체, 오디오 경합·팝업 과밀·채널 동기 복원 체인이 수치 기준(`100ms`,`150ms`)을 충족(Pre-Activation) |
| IT_SIL_001 | Flow_009 | Comm_009 | Func_041,Func_042,Func_043 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | UT_SIL_001 | 시나리오 실행/결과 기록/로그 연동 완료 |
| IT_BASE_001 | Flow_101~Flow_106, Flow_201~Flow_205 | Comm_101~Comm_106, Comm_201~Comm_205 | Func_101~Func_107,Func_109~Func_119,Func_167,Func_168 | Req_101~Req_107,Req_109~Req_119,Req_167,Req_168 | VC_101~VC_107,VC_109~VC_119,VC_167,VC_168 | UT_BASE_001, UT_BASE_PT_001, UT_BASE_EXT_PT_002, UT_BASE_CH_001, UT_BASE_BODY_001, UT_BASE_IVI_001, UT_BASE_EXT_BODY_001, UT_BASE_EXT_IVI_001, UT_BASE_GW_001, UT_BASE_TEST_001 | 차량 기본 기능 입력/상태/표시/도메인 경계/SIL 판정 연동이 일관되게 유지 |
| IT_BASE_PT_001 | Flow_101,Flow_204,Flow_105 | Comm_101,Comm_204,Comm_105 | Func_101,Func_102,Func_110 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | UT_BASE_PT_001, UT_BASE_GW_001 | 엔진/변속/동력 상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_CH_001 | Flow_102,Flow_201,Flow_105 | Comm_102,Comm_201,Comm_105 | Func_103,Func_104,Func_105,Func_110 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | UT_BASE_CH_001, UT_BASE_GW_001 | 가감속/제동/조향/차체상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_BODY_001 | Flow_103,Flow_202,Flow_105 | Comm_103,Comm_202,Comm_105 | Func_106,Func_107,Func_111 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | UT_BASE_BODY_001, UT_BASE_GW_001 | 차체 제어/편의/상태 경로가 일관되게 유지 |
| IT_BASE_IVI_001 | Flow_104,Flow_203,Flow_105 | Comm_104,Comm_203,Comm_105 | Func_109,Func_111 | Req_109,Req_111 | VC_109,VC_111 | UT_BASE_IVI_001, UT_BASE_GW_001 | 기본 표시/UI/연계 이벤트가 50/100ms 기준으로 유지 |
| IT_BASE_EXT_BODY_001 | Flow_202,Flow_105 | Comm_202,Comm_105 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | UT_BASE_EXT_BODY_001, UT_BASE_GW_001 | DATC/Seat/Mirror/Door/Wiper-Rain/Security 확장 상태가 `100ms` 주기로 연계되고 `150ms` 이내 반영 |
| IT_BASE_EXT_IVI_001 | Flow_203,Flow_105 | Comm_203,Comm_105 | Func_119 | Req_119 | VC_119 | UT_BASE_EXT_IVI_001, UT_BASE_GW_001 | Audio Focus/Voice/TTS 상태가 50/100ms 주기 규칙과 `150ms` 반영 기준을 만족 |
| IT_BASE_DIAG_001 | Flow_106,Flow_205 | Comm_106,Comm_205 | Func_112 | Req_112 | VC_112 | UT_BASE_TEST_001 | 진단 요청-응답 및 결과 기록이 Event+100ms 기준으로 유지 |
| IT_OEM_SURFACE_001 | Flow_009,Flow_105,Flow_106,Flow_124,Flow_205 | Comm_009,Comm_105,Comm_106,Comm_124,Comm_205 | Func_041,Func_042,Func_043,Func_110,Func_111,Func_151,Func_152 | Req_041,Req_042,Req_043,Req_110,Req_111,Req_151,Req_152 | VC_041,VC_042,VC_043,VC_110,VC_111,VC_151,VC_152 | UT_BASE_GW_001, UT_BASE_TEST_001, UT_BASE_ROBUST_EXT_001 | OEM100 Active Surface 그룹 경계/헬스/가용성 체인이 누락 없이 유지되고 대체 출력 규칙 위반 0건 |
| IT_OEM_PREMIUM_001 | Flow_202,Flow_203,Flow_103,Flow_104,Flow_105,Flow_008 | Comm_202,Comm_203,Comm_103,Comm_104,Comm_105,Comm_008 | Func_113,Func_116,Func_118,Func_119,Func_140,Func_141,Func_142,Func_146,Func_147,Func_153,Func_154,Func_155 | Req_113,Req_116,Req_118,Req_119,Req_140,Req_141,Req_142,Req_146,Req_147,Req_153,Req_154,Req_155 | VC_113,VC_116,VC_118,VC_119,VC_140,VC_141,VC_142,VC_146,VC_147,VC_153,VC_154,VC_155 | UT_BASE_EXT_BODY_001, UT_BASE_EXT_IVI_001, UT_BASE_ALERT_EXT_001, UT_BASE_ROBUST_EXT_001 | Premium 활성 ECU 편입 후 기존 체인 Pass 유지, 미구현(`NIGHT_VISION`)은 Not Implemented로 분리 관리 |
| IT_BASE_EXT_CH_002 | Flow_206 | Comm_206 | Func_156,Func_157 | Req_156,Req_157 | VC_156,VC_157 | UT_BASE_EXT_CH_002 | 제동/차체안정 상태가 `100ms` 주기로 연계되고 `150ms` 이내 경고 맥락에 반영 |
| IT_BASE_EXT_BODY_002 | Flow_207 | Comm_207 | Func_158,Func_159,Func_160 | Req_158,Req_159,Req_160 | VC_158,VC_159,VC_160 | UT_BASE_EXT_BODY_002 | 출입/탑승자보호/실내편의 상태가 `100ms` 주기로 연계되고 `150ms` 이내 정책 반영 |
| IT_BASE_EXT_IVI_002 | Flow_208 | Comm_208 | Func_161,Func_162 | Req_161,Req_162 | VC_161,VC_162 | UT_BASE_EXT_IVI_002 | 표시/음향/디지털 접근 서비스 상태가 `100ms` 주기로 연계되고 `150ms` 이내 표시/안내 정책 반영 |
| IT_ADAS_EXT_STATE_001 | Flow_209 | Comm_209 | Func_163,Func_164,Func_165 | Req_163,Req_164,Req_165 | VC_163,VC_164,VC_165 | UT_ADAS_EXT_STATE_001 | 주행보조/주차인지/센서가용성 상태가 `100ms` 주기로 연계되고 `150ms` 이내 위험/강등 정책 반영 |
| IT_BACKBONE_STATE_001 | Flow_210 | Comm_210 | Func_166 | Req_166 | VC_166 | UT_BACKBONE_STATE_001 | 백본/도메인 서비스 상태가 `100ms` 주기로 연계되고 경계 가용성/강등 상태가 즉시 반영 |
| IT_BASE_EXT_PT_002 | Flow_204 | Comm_204 | Func_167,Func_168 | Req_167,Req_168 | VC_167,VC_168 | UT_BASE_EXT_PT_002 | 구동/전력변환 및 변속·열관리·충전 인터페이스 상태가 `100ms` 주기로 연계되고 `150ms` 이내 구동 준비/서비스 경고 맥락에 반영 |

---

---

## 핵심 보강 케이스 (선별 수용)

| IT 보강 ID | 기준 IT | Req/VC | 목적 | 입력/조건 | 합격 기준 | 선행 UT |
|---|---|---|---|---|---|---|
| IT_BND_024_A | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 미만 확인 | 마지막 긴급 수신 후 `999ms` | `timeoutClear=0` 유지 | UT_BND_024_A |
| IT_BND_024_B | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 확인 | 마지막 긴급 수신 후 `1000ms` | `timeoutClear=1` 단회 전환 | UT_BND_024_B |
| IT_BND_024_C | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 초과 확인 | 마지막 긴급 수신 후 `>1000ms` | 해제 상태 유지, 중복 토글 없음 | UT_BND_024_C |
| IT_ARB_030_031_A | IT_ARB_001 | Req_030,Req_031 / VC_030,VC_031 | ETA/SourceID 동률 규칙 확인 | 동급 긴급 2건(ETA 동률 포함) | ETA 우선, 동률 시 sourceId 오름차순 선택 | UT_ARB_001 |
| IT_HMI_020_A | IT_OUT_001 | Req_020 / VC_020 | 방향 표시 분기 확인 | emergencyDirection = LEFT/RIGHT/NONE | 방향 코드가 규칙표와 일치 | UT_CLU_001 |

---

## 07 연계 체크포인트

- `IT_*`의 E2E 결과는 `07_System_Test.md`의 `ST_*` 수용 판단 근거로 사용한다.
- `IT_CORE_001`, `IT_EMS_001`, `IT_ARB_001`, `IT_OUT_001`, `IT_TIMEOUT_001`, `IT_SIL_001`, `IT_BASE_001`, `IT_BASE_PT_001`, `IT_BASE_EXT_PT_002`, `IT_BASE_CH_001`, `IT_BASE_BODY_001`, `IT_BASE_IVI_001`, `IT_BASE_DIAG_001`, `IT_BASE_ALERT_EXT_001`, `IT_BASE_ROBUST_EXT_001`, `IT_BASE_EXT_CH_002`, `IT_BASE_EXT_BODY_002`, `IT_BASE_EXT_IVI_002`, `IT_ADAS_EXT_STATE_001`, `IT_BACKBONE_STATE_001`는 03/04 문서의 검증 참조 ID와 일치해야 한다.
- `IT_OEM_SURFACE_001`, `IT_OEM_PREMIUM_001`은 OEM100 확장 ST(`ST_OEM_SURFACE_001`, `ST_OEM_PREMIUM_001`)의 선행 근거로 유지한다.
- `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001`은 `Req_120~Req_121, Req_123, Req_125~Req_129` 활성 체인의 ST 연계 근거로 유지한다.
- `IT_ADAS_OBJ_001`은 `Req_130~Req_139` Pre-Activation 체인의 ST 연계 근거(`ST_ADAS_OBJ_001`)로 유지한다.
- `IT_BASE_ALERT_EXT_001`은 `Req_140~Req_147` Pre-Activation 체인의 ST 연계 근거(`ST_BASE_ALERT_EXT_001`)로 유지한다.
- `IT_BASE_ROBUST_EXT_001`은 `Req_148~Req_155` Pre-Activation 체인의 ST 연계 근거(`ST_BASE_ROBUST_EXT_001`)로 유지한다.
- `IT_BASE_EXT_CH_002`, `IT_BASE_EXT_BODY_002`, `IT_BASE_EXT_IVI_002`, `IT_ADAS_EXT_STATE_001`, `IT_BACKBONE_STATE_001`, `IT_BASE_EXT_PT_002`은 `Req_156~Req_168` 구현 체인의 ST 연계 근거로 유지한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.22 | 2026-03-09 | OEM100 확장 실케이스 반영: `IT_OEM_SURFACE_001`, `IT_OEM_PREMIUM_001`를 상단/상세 표와 07 연계 체크포인트에 추가. |
| 4.21 | 2026-03-09 | 본문 실내용 보강: `OEM100 Surface 상세-IT 매핑` 표를 추가해 그룹별 실제 ECU 목록과 IT 커버 경로를 명시. |
| 4.20 | 2026-03-09 | OEM100 통합 검증 원칙 보강: `05-06 동기화 기준` 섹션을 추가해 Surface 확장 시 IT 증설 조건, Placeholder 처리, DEV2 테스트 설계 전달 규칙을 명시. |
| 4.19 | 2026-03-06 | Legacy 누락군 보강: `Req_018/036/038/039/108/114/115/117/122/124` 상속 관계를 `Legacy Req 상속 매핑` 섹션으로 추가해 Lean IT advisory 누락을 해소. |
| 4.18 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `IT_BASE_ROBUST_EXT_001` 추가, `Req_148~Req_155`/`Flow·Comm_130·133·006·007·008·104·105·124·203` 추적 및 07 연계 체크포인트를 동기화. |
| 4.17 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `IT_BASE_ALERT_EXT_001` 추가, `Req_140~Req_147`/`Flow·Comm_103·104·105·203·006·008` 추적 및 07 연계 체크포인트를 동기화. |
| 4.16 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `IT_ADAS_OBJ_001`을 추가하고 `Req_130~Req_139`/`Flow_130~133`/`Comm_130~133` 추적 및 07 연계 체크포인트를 동기화. |
| 4.15 | 2026-03-06 | 미사용 체인 정리: `Req/VC/Func_108`을 `IT_BASE_001/IT_BASE_BODY_001`에서 제거하고 Baseline 범위를 `108 제외`로 동기화. |
| 4.14 | 2026-03-03 | V2 IT를 구현 활성 상태로 전환하고 `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001` 수행 상태를 Ready로 갱신. |
| 4.13 | 2026-03-02 | V2 확장(Pre-Activation) IT 반영: `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001` 추가 및 `Req_120~Req_121, Req_123, Req_125~Req_129` 추적 연계/체크포인트 보강. |
| 4.12 | 2026-03-02 | 작성 원칙에 CANoe.CAN 실행 제약 임시 주석을 추가하고, 경계값 검증 규칙을 `UT/ST 원칙 + IT 선별 보강`으로 명확화. `IT_SIL_001` 기대결과에 대체 백본 조건을 병기. |
| 4.11 | 2026-03-02 | 중간감사 추적성 보강: IT 상단/상세 표의 Req 범위 표기를 일부 구간(`~`)에서 개별 Req 나열로 확장해 `Req_002/003/004/006/007/011/014/015/028/029/035~039`의 명시 추적을 강화. |
| 4.10 | 2026-03-02 | 차량 기본 기능 확장 추적 보강: `Req/VC/Func_113~119`를 `IT_BASE_001` 범위에 반영하고 `IT_BASE_EXT_BODY_001`, `IT_BASE_EXT_IVI_001`를 상단/하단 표에 추가. |
| 4.9 | 2026-03-02 | 증적 경로 규칙 고정: IT 실행 증적 저장 경로를 `canoe/logging/evidence/IT/`로 명시. |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-23 | 구버전 요구 ID 구조 반영 |
| 3.0 | 2026-02-24 | 구버전 TS 시나리오 확장 |
| 4.0 | 2026-02-26 | 옵션1 아키텍처 기준 전면 재작성. OTA/UDS/DoIP 제거, IT ID 체계 및 Flow/Comm 중심 통합 검증 구조 반영 |
| 4.1 | 2026-02-26 | 합격 기준에 50ms/100ms/150ms/1000ms 수치 기준을 반영하고, FZ 사전 점검 결과 반영 전 Draft 경계 문구 추가 |
| 4.2 | 2026-02-26 | VC 추적 강화를 위해 상단/상세 표에 VC ID 컬럼을 추가하고 Req-VC-IT 연결을 명시 |
| 4.3 | 2026-02-28 | 팀 제안 중 현업 BP에 부합하는 핵심만 선별 반영: 타임아웃 경계값(999/1000/>1000), ETA/SourceID 우선순위, 방향 분기 보강 케이스 추가 |
| 4.4 | 2026-02-28 | Flow_003(Comm_003)에 `speedLimit` 연계를 추가하여 Req_010(스쿨존 과속) 통합 검증 경로를 보강. |
| 4.5 | 2026-02-28 | 차량 기본 기능 통합 검증을 위해 `IT_BASE_001`(Req/VC/Func 101~112, Flow/Comm 101~106 및 201~205)을 추가. |
| 4.6 | 2026-02-28 | 멘토링 피드백 반영: IT를 핵심 통합 체인 중심(Lean IT)으로 재구성하고 세부 경계값은 UT/ST로 분리. |
| 4.7 | 2026-02-28 | Lean IT 재구성 후 잔여 참조 ID 정리(`IT_HMI_020_A`, 07 연계 체크포인트) 및 03/04 검증 링크 문구를 최신 체계로 동기화. |
| 4.8 | 2026-02-28 | 확장된 통신/기본차량 범위 반영: 도메인별 통합 검증(`IT_BASE_PT/CH/BODY/IVI/DIAG`)을 상단/하단 표에 추가. |
