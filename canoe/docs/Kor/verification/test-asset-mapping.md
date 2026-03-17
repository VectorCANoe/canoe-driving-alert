# Test Asset Mapping

원문:
- [../../verification/test-asset-mapping.md](../../verification/test-asset-mapping.md)

동기화 기준:
- `5d83ee7f`
- native asset 이름, oracle seam 이름, evidence artifact 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 CANoe SIL test construction의 현재 개발 기준선입니다.
> native CANoe test asset, oracle seam, evidence collection이 최종 고정되기 전까지 일부 내용은 변경될 수 있습니다.

## 1. 목적

이 문서는 아래 reviewer-facing test ID와:

- `driving-alert-workproducts/05_Unit_Test.md`
- `driving-alert-workproducts/06_Integration_Test.md`
- `driving-alert-workproducts/07_System_Test.md`

다음 실행 자산 사이의 공식 매핑을 정의합니다.

- native CANoe test asset 후보
- primary oracle source
- primary evidence source
- 현재 diagnostic 필요 여부

즉, 공식 `05/06/07` 표와 executable CANoe SIL test surface를 연결하는 implementation-side verification bridge입니다.

## 2. 매핑 규칙

1. `05`는 제품 기준선의 controller, input, output verification으로 매핑합니다.
2. `06`은 runtime boundary를 넘는 integrated function verification으로 매핑합니다.
3. `07`은 end-user 및 whole-vehicle scenario verification으로 매핑합니다.
4. `Diagnostic Needed?`는 `Yes`와 `No`만 사용합니다.
5. `Yes`는 명시적인 diagnostic 또는 security state visibility가 없으면 verdict 근거가 약해지는 row에만 사용합니다.
6. native asset 후보, oracle type, evidence type이 완전히 동일한 simulator preset row만 반복 row로 묶을 수 있습니다.

추가 해석 원칙:

- asset ID, scenario ID, oracle seam, evidence artifact 이름은 canonical technical string으로 유지합니다.
- 대형 표 안에서는 reviewer가 바로 판단해야 하는 의미를 우선 설명하고, raw implementation detail은 줄입니다.
- 표 셀 안에 영어 technical phrase가 남아 있더라도 그것은 식별자 보존을 위한 것이며, 해석 기준은 한국어 section과 note를 우선 봅니다.

## 3. Unit Test 매핑

### 3.1 공통 oracle 표현 읽기

대형 표 안에서 반복되는 oracle 표현은 아래처럼 해석합니다.

| 표기 | 한국어 해석 |
|---|---|
| `selected warning state` | 최종 선택 경고 상태 |
| `zone context state` | 구역 판단 상태 |
| `clear and restore state` | 해제 및 복원 상태 |
| `final selected warning state` | 최종 선택 경고 결과 |
| `fail-safe state` | fail-safe 진입 또는 유지 상태 |
| `minimum-channel state` | 최소 채널 유지 상태 |
| `display-policy reflection state` | 표시 정책 반영 상태 |
| `audio focus, ducking, and volume policy state` | 오디오 focus, ducking, volume 정책 상태 |
| `output-channel availability and fallback state` | 출력 채널 가용성과 fallback 상태 |
| `duplicate-popup suppression state` | 중복 팝업 억제 상태 |
| `channel-restore consistency state` | 채널 복원 일관성 상태 |
| `end-to-end scenario verdict` | 종단 간 시나리오 판정 |
| `end-to-end fail-safe scenario verdict` | 종단 간 fail-safe 시나리오 판정 |

### 3.2 공통 evidence 표현 읽기

evidence column은 artifact 이름을 유지하되, 조합 의미는 아래처럼 읽습니다.

| 표기 | 한국어 해석 |
|---|---|
| `native report + trace + sysvar snapshot` | native report, trace, sysvar snapshot을 함께 보는 기본 조합 |
| `native report + sysvar snapshot + panel capture` | runtime report와 sysvar, panel capture를 함께 보는 조합 |
| `panel capture + screenshot + native report` | panel 기준의 visible output evidence 조합 |
| `cluster capture + screenshot + native report` | cluster/HUD 기준 visual evidence 조합 |
| `write window + trace + sysvar snapshot` | diagnostic 또는 fail-safe 확인용 심화 evidence 조합 |
| `Ethernet trace + write window + verification_log.csv` | 외부 TX/주기 확인용 transport evidence 조합 |
| `panel capture + trace + verification_log.csv` | system-level 동작과 trace chronology를 함께 보는 조합 |

| ID | 후보 native asset | 주요 oracle | 주요 evidence | 진단 필요 여부 |
|---|---|---|---|---|
| `UT_001` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW` | vehicle-state 전달 seam | native report + trace + `verification_log.csv` | `No` |
| `UT_002` | `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` | navigation 맥락 전달 seam | native report + trace + `verification_log.csv` | `No` |
| `UT_003` | `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | 선택 경고 상태 | native report + sysvar snapshot + panel capture | `No` |
| `UT_004` | `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` | emergency 상태 및 timeout clear | native report + trace + sysvar snapshot | `No` |
| `UT_005` | `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST` | arbitration 결과 및 decel-assist 상태 | native report + sysvar snapshot + panel capture | `No` |
| `UT_006` | `TC_CANOE_UT_EXT_006_OBJECT_RISK` | object-risk 상태 및 downgrade 상태 | native report + trace + event log | `No` |
| `UT_007` | `TC_CANOE_UT_EXT_007_CLU_CONTEXT_ADJUST` | 렌더링된 경고 맥락 | native report + cluster capture + sysvar snapshot | `No` |
| `UT_008` | `TC_CANOE_UT_EXT_008_DOMAIN_BOUNDARY_FAILSAFE` | fail-safe 진입 상태 및 boundary-health 상태 | native report + sysvar snapshot + trace + write window | `No` |
| `UT_009` | `TC_CANOE_UT_CORE_009_NAV_CTX_MGR` | 구역 맥락 상태 | native report + sysvar snapshot | `No` |
| `UT_010` | `TC_CANOE_UT_CORE_010_EMS_ALERT_TXRX` | emergency tx/rx 상태 및 timeout 상태 | native report + CAN/Ethernet trace + write window | `No` |
| `UT_011` | `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | 최종 선택 경고 상태 | native report + sysvar snapshot + panel capture | `No` |
| `UT_012` | `TC_CANOE_UT_CORE_012_BODY_GW_ROUTE` | ambient route 상태 | native report + trace + ambient capture | `No` |
| `UT_013` | `TC_CANOE_UT_CORE_013_IVI_GW_ROUTE` | cluster route 상태 | native report + trace + cluster capture | `No` |
| `UT_014` | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` | ambient 색상 및 패턴 상태 | native report + panel capture + screenshot | `No` |
| `UT_015` | `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` | 경고 text 및 direction 상태 | native report + cluster capture + screenshot | `No` |
| `UT_016` | `TC_CANOE_UT_EXT_016_CHS_BRAKE_EXT` | brake 관련 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_017` | `TC_CANOE_UT_EXT_017_CHS_DYNAMICS_EXT` | chassis 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_018` | `TC_CANOE_UT_EXT_018_BODY_ENTRY_EXIT` | door/tailgate 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_019` | `TC_CANOE_UT_EXT_019_BODY_OCCUPANT_PROTECTION` | occupant-protection 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_020` | `TC_CANOE_UT_EXT_020_BODY_COMFORT` | comfort 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_021` | `TC_CANOE_UT_EXT_021_IVI_DISPLAY_SERVICE` | 표시/서비스 맥락 상태 | native report + sysvar snapshot + panel capture | `No` |
| `UT_022` | `TC_CANOE_UT_EXT_022_IVI_SERVICE_ACCESS` | service-access 맥락 상태 | native report + sysvar snapshot + trace | `No` |
| `UT_023` | `TC_CANOE_UT_EXT_023_ADAS_DRIVE_ASSIST` | drive-assist 맥락 상태 | native report + sysvar snapshot + trace | `No` |
| `UT_024` | `TC_CANOE_UT_EXT_024_ADAS_PARKING_PERCEPTION` | parking/perception 맥락 상태 | native report + sysvar snapshot + trace | `No` |
| `UT_025` | `TC_CANOE_UT_EXT_025_WARNING_DELIVERY_BOUNDARY` | delivery-health 및 fail-safe 상태 | native report + trace + write window + sysvar snapshot | `No` |
| `UT_026` | `TC_CANOE_UT_EXT_026_DOMAIN_ROUTER_PROPULSION` | propulsion 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_027` | `TC_CANOE_UT_EXT_027_DOMAIN_ROUTER_POWER_CHARGE` | power/charge 맥락 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_028` | `TC_CANOE_UT_INP_028_VEHICLE_STEERING` | drive-state / speed / steering 정규화 | native report + trace + sysvar snapshot | `Yes` |
| `UT_029` | `TC_CANOE_UT_INP_029_NAV_CONTEXT` | nav 맥락의 alert-level trigger 및 안정 경로 | native report + trace + sysvar snapshot | `Yes` |
| `UT_030` | `TC_CANOE_UT_INP_030_EMERGENCY_INPUT` | emergency type / ETA 관측 패턴 | native report + trace + sysvar snapshot | `Yes` |
| `UT_031` | `TC_CANOE_UT_INP_031_EPB_INPUT` | park brake decel 입력 정규화 | native report + trace + sysvar snapshot | `Yes` |
| `UT_032` | `TC_CANOE_UT_INP_032_EHB_INPUT` | hydraulic brake decel 입력 정규화 | native report + trace + sysvar snapshot | `Yes` |
| `UT_033` | `TC_CANOE_UT_INP_033_VSM_INPUT` | VSM 안정 상태 및 spurious alert 없음 | native report + trace + sysvar snapshot | `Yes` |
| `UT_034` | `TC_CANOE_UT_INP_034_ECS_INPUT` | air suspension ride-height mode | native report + trace + sysvar snapshot | `Yes` |
| `UT_035` | `TC_CANOE_UT_INP_035_CDC_INPUT` | damper mode and valve current | native report + trace + sysvar snapshot | `Yes` |
| `UT_036` | `TC_CANOE_UT_INP_036_DOOR_FL_INPUT` | front-left door auto unlock / approach score | native report + trace + sysvar snapshot | `Yes` |
| `UT_037` | `TC_CANOE_UT_INP_037_DOOR_FR_INPUT` | front-right door auto unlock / approach score | native report + trace + sysvar snapshot | `Yes` |
| `UT_038` | `TC_CANOE_UT_INP_038_DOOR_RL_INPUT` | rear-left door auto unlock / approach score | native report + trace + sysvar snapshot | `Yes` |
| `UT_039` | `TC_CANOE_UT_INP_039_DOOR_RR_INPUT` | rear-right door auto unlock / approach score | native report + trace + sysvar snapshot | `Yes` |
| `UT_040` | `TC_CANOE_UT_INP_040_TGM_INPUT` | tailgate assist mode and actuator command | native report + trace + sysvar snapshot | `Yes` |
| `UT_041` | `TC_CANOE_UT_INP_041_ACU_INPUT` | airbag deployment armed + pretension request | native report + trace + sysvar snapshot | `Yes` |
| `UT_042` | `TC_CANOE_UT_INP_042_ODS_INPUT` | occupant detection / weight class / child seat | native report + trace + sysvar snapshot | `Yes` |
| `UT_043` | `TC_CANOE_UT_INP_043_AFLS_INPUT` | adaptive front-light mode + headlamp angle | native report + trace + sysvar snapshot | `Yes` |
| `UT_044` | `TC_CANOE_UT_INP_044_AHLS_INPUT` | auto high-beam assist + active flag | native report + trace + sysvar snapshot | `Yes` |
| `UT_045` | `TC_CANOE_UT_INP_045_DATC_INPUT` | cabin temp / blower / AC / vent mode | native report + trace + sysvar snapshot | `Yes` |
| `UT_046` | `TC_CANOE_UT_INP_046_SEAT_DRV_INPUT` | driver seat position + heat level | native report + trace + sysvar snapshot | `Yes` |
| `UT_047` | `TC_CANOE_UT_INP_047_SEAT_PASS_INPUT` | passenger seat position + heat level | native report + trace + sysvar snapshot | `Yes` |
| `UT_048` | `TC_CANOE_UT_INP_048_SRF_INPUT` | sunroof position state | native report + trace + sysvar snapshot | `Yes` |
| `UT_049` | `TC_CANOE_UT_INP_049_HUD_INPUT` | HUD mode + warning code | native report + trace + sysvar snapshot | `Yes` |
| `UT_050` | `TC_CANOE_UT_INP_050_AMP_INPUT` | audio mute / ducking / volume level | native report + trace + sysvar snapshot | `Yes` |
| `UT_051` | `TC_CANOE_UT_INP_051_TMU_INPUT` | telematics link state / service mode / remote climate | native report + trace + sysvar snapshot | `Yes` |
| `UT_052` | `TC_CANOE_UT_INP_052_SCC_INPUT` | SCC proximity decel — decel-assist observer | native report + trace + sysvar snapshot | `Yes` |
| `UT_053` | `TC_CANOE_UT_INP_053_PGS_INPUT` | parking guidance 활성 / 기동 준비 | native report + trace + sysvar snapshot | `Yes` |
| `UT_054` | `TC_CANOE_UT_INP_054_PUS_INPUT` | parking ultrasonic sensor proximity class | native report + trace + sysvar snapshot | `Yes` |
| `UT_055` | `TC_CANOE_UT_INP_055_AVM_INPUT` | surround-view mode and active flag | native report + trace + sysvar snapshot | `Yes` |
| `UT_056` | `TC_CANOE_UT_INP_056_FCAM_INPUT` | forward camera health and lane preview | native report + trace + sysvar snapshot | `Yes` |
| `UT_057` | `TC_CANOE_UT_INP_057_FRADAR_INPUT` | forward radar object range and risk class | native report + trace + sysvar snapshot | `Yes` |
| `UT_058` | `TC_CANOE_UT_INP_058_SRR_FL_INPUT` | left-front SRR — intersection conflict flag | native report + trace + sysvar snapshot | `Yes` |
| `UT_059` | `TC_CANOE_UT_INP_059_SRR_FR_INPUT` | right-front SRR — merge cut-in flag | native report + trace + sysvar snapshot | `Yes` |
| `UT_060` | `TC_CANOE_UT_INP_060_SRR_RL_INPUT` | rear-left SRR blind-spot state | native report + trace + sysvar snapshot | `Yes` |
| `UT_061` | `TC_CANOE_UT_INP_061_SRR_RR_INPUT` | rear-right SRR blind-spot state | native report + trace + sysvar snapshot | `Yes` |
| `UT_062` | `TC_CANOE_UT_INP_062_IBOX_INPUT` | digital key / vehicle service 상태 | native report + trace + sysvar snapshot | `Yes` |
| `UT_063` | `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE` | security-state injection | write window + trace + sysvar snapshot | `Yes` |
| `UT_064` | `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE` | diagnostic-state injection | write window + trace + sysvar snapshot | `Yes` |
| `UT_065` | `TC_CANOE_UT_INP_065_ETHB_INPUT` | backbone failure 및 fail-safe 관측 | native report + trace + sysvar snapshot | `Yes` |
| `UT_066` | `TC_CANOE_UT_INP_066_OBC_INPUT` | OBC charge power and AC plug state | native report + trace + sysvar snapshot | `Yes` |
| `UT_067` | `TC_CANOE_UT_INP_067_DCDC_INPUT` | DCDC LV output voltage and current | native report + trace + sysvar snapshot | `Yes` |
| `UT_068` | `TC_CANOE_UT_INP_068_MCU_INPUT` | motor torque command and speed rpm | native report + trace + sysvar snapshot | `Yes` |
| `UT_069` | `TC_CANOE_UT_INP_069_INVERTER_INPUT` | inverter state and DC link voltage | native report + trace + sysvar snapshot | `Yes` |
| `UT_070` | `TC_CANOE_UT_OUT_070_BCM_AMBIENT` | ambient output 렌더링 상태 | panel capture + screenshot + native report | `No` |
| `UT_071` | `TC_CANOE_UT_OUT_071_IVI_HMI` | HMI output 상태 | panel capture + screenshot + native report | `No` |
| `UT_072` | `TC_CANOE_UT_OUT_072_CLU_DISPLAY` | cluster display 렌더링 상태 | cluster capture + screenshot + native report | `No` |
| `UT_073` | `TC_CANOE_UT_OUT_073_HUD_DISPLAY` | HUD 렌더링 상태 | HUD capture + screenshot + native report | `No` |
| `UT_074` | `TC_CANOE_UT_OUT_074_AMP_AUDIO` | audio-guide 상태 | write window + audio state capture + native report | `No` |
| `UT_075` | `TC_CANOE_UT_OUT_075_DECEL_ASSIST_REQ` | decel-assist request 상태 | native report + trace + sysvar snapshot | `No` |
| `UT_076` | `TC_CANOE_UT_OUT_076_POLICE_TX` | external tx frame 관찰 | Ethernet trace + write window + `verification_log.csv` | `No` |
| `UT_077` | `TC_CANOE_UT_OUT_077_AMBULANCE_TX` | external tx frame 관찰 | Ethernet trace + write window + `verification_log.csv` | `No` |

## 4. Integration Test 매핑

| ID | 후보 native asset | 주요 oracle | 주요 evidence | 진단 필요 여부 |
|---|---|---|---|---|
| `IT_001` | `TC_CANOE_IT_CORE_001_BASE_ACTIVATION` | 경고 활성/비활성 상태 | native report + sysvar snapshot + panel capture | `No` |
| `IT_002` | `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` | 구역 경고 결과 상태 | native report + trace + panel capture | `No` |
| `IT_003` | `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` | 고속도로 경고 발생 및 해제 상태 | native report + sysvar snapshot + panel capture | `No` |
| `IT_004` | `TC_CANOE_IT_V2_004_POLICE_RX` | 경찰차 경고 결과 상태 | native report + trace + panel capture | `No` |
| `IT_005` | `TC_CANOE_IT_V2_005_AMBULANCE_RX` | 구급차 경고 결과 상태 | native report + trace + panel capture | `No` |
| `IT_006` | `TC_CANOE_IT_V2_006_ARBITRATION` | 최종 선택 경고 상태 | native report + sysvar snapshot + panel capture | `No` |
| `IT_007` | `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | ambient 색상/패턴 결과 | panel capture + screenshot + `verification_log.csv` | `No` |
| `IT_008` | `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` | cluster 텍스트/방향 결과 | cluster capture + screenshot + `verification_log.csv` | `No` |
| `IT_009` | `TC_CANOE_IT_V2_009_TIMEOUT_CLEAR` | 해제 및 복원 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_010` | `TC_CANOE_IT_V2_010_DECEL_ASSIST` | decel-assist request 및 동기 상태 | native report + trace + sysvar snapshot + panel capture | `No` |
| `IT_011` | `TC_CANOE_IT_V2_011_FAILSAFE_MIN_WARNING` | fail-safe 및 최소 채널 상태 | native report + write window + sysvar snapshot + trace | `No` |
| `IT_012` | `TC_CANOE_IT_EXT_012_OBJECT_RISK_EVENTLOG` | object-risk 및 event-log 상태 | native report + trace + event log | `No` |
| `IT_013` | `TC_CANOE_IT_013_SEATBELT_CONTEXT` | 안전벨트 강조 상태 | native report + panel capture + sysvar snapshot | `No` |
| `IT_014` | `TC_CANOE_IT_014_DISPLAY_POLICY` | 표시 정책 반영 상태 | native report + panel capture + sysvar snapshot | `No` |
| `IT_015` | `TC_CANOE_IT_015_TURN_LAMP_CONTEXT` | turn-lamp 맥락에 따른 경고 유형 조정 | native report + panel capture + sysvar snapshot | `No` |
| `IT_016` | `TC_CANOE_IT_016_DRIVE_MODE_SENSITIVITY` | 주행 모드 민감도 상태 | native report + panel capture + sysvar snapshot | `No` |
| `IT_017` | `TC_CANOE_IT_017_AUDIO_VOLUME_POLICY` | 오디오 focus, ducking, volume 정책 상태 | native report + panel capture + sysvar snapshot | `No` |
| `IT_018` | `TC_CANOE_IT_EXT_018_EMERGENCY_PLUS_TTC` | 경고/decel 결합 결과 상태 | native report + trace + panel capture | `No` |
| `IT_019` | `TC_CANOE_IT_019_POWERTRAIN_PARKED_BASELINE` | 주차 기준선 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_020` | `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE` | 주행 기준선 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_021` | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE` | 조향 입력 기준선 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_022` | `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE` | 제동 입력 기준선 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_023` | `TC_CANOE_IT_023_CHASSIS_ACCEL_BASELINE` | 가속 기반 drive-mode 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_024` | `TC_CANOE_IT_BASE_024_BODY_STATE` | hazard 반영 기준선 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_025` | `TC_CANOE_IT_EXT_025_WINDOW_STATE` | window 상태 반영 | native report + door-state trace + sysvar snapshot | `No` |
| `IT_026` | `TC_CANOE_IT_BASE_026_BASIC_DISPLAY_UI` | 기본 표시 통합 상태 | panel capture + screenshot + native report | `No` |
| `IT_027` | `TC_CANOE_IT_BASE_027_COMFORT_CONTEXT` | comfort 맥락의 정책 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_028` | `TC_CANOE_IT_EXT_028_BODY_CONTROL_LOCK` | door lock/open 반영 상태 | native report + door-state trace + sysvar snapshot | `No` |
| `IT_029` | `TC_CANOE_IT_EXT_029_WIPER_RAIN_BASELINE` | wiper/rain 기준선 반영 상태 | native report + body-output trace + sysvar snapshot | `No` |
| `IT_030` | `TC_CANOE_IT_BASE_030_BODY_SECURITY_CONTEXT` | security-state service-boundary 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_031` | `TC_CANOE_IT_031_AUDIO_GUIDE_RUNTIME` | 오디오 및 voice-guide 통합 상태 | panel capture + write window + native report | `No` |
| `IT_032` | `TC_CANOE_IT_032_OUTPUT_FALLBACK` | 출력 채널 가용성 및 fallback 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_033` | `TC_CANOE_IT_033_DUPLICATE_POPUP_SUPPRESSION` | 중복 팝업 억제 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_034` | `TC_CANOE_IT_034_CHANNEL_RESTORE` | 채널 복원 일관성 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_035` | `TC_CANOE_IT_EXT_035_DISTANCE_HISTORY` | 거리 및 이력 조회 결과 | panel capture + native report + `verification_log.csv` | `No` |
| `IT_036` | `TC_CANOE_IT_EXT_036_CHASSIS_EXT_CONTEXT` | EPB/EHB/VSM/ECS/CDC 통합 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_037` | `TC_CANOE_IT_EXT_037_OCCUPANT_COMFORT_CONTEXT` | occupant/comfort 통합 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_038` | `TC_CANOE_IT_EXT_038_DISPLAY_SERVICE_CONTEXT` | 표시/서비스 통합 상태 | panel capture + trace + native report | `No` |
| `IT_039` | `TC_CANOE_IT_EXT_039_ADAS_PERCEPTION_CONTEXT` | ADAS/perception 통합 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_040` | `TC_CANOE_IT_EXT_040_SERVICE_SECURITY_DIAG` | service/security/diagnostic 통합 상태 | native report + trace + write window + sysvar snapshot | `Yes` |
| `IT_041` | `TC_CANOE_IT_EXT_041_CHARGE_POWER_CONTEXT` | power/charge 통합 상태 | native report + trace + sysvar snapshot | `No` |
| `IT_042` | `TC_CANOE_IT_EXT_042_DISPLAY_CHANNELS` | 채널 간 visual 일관성 | panel capture + screenshot + `verification_log.csv` | `No` |
| `IT_043` | `TC_CANOE_IT_EXT_043_AUDIO_GUIDE_CHANNEL` | audio-guide 일관성 | write window + audio state capture + `verification_log.csv` | `No` |
| `IT_044` | `TC_CANOE_IT_ETH_044_POLICE_TX` | 경찰 외부 TX 관찰 | Ethernet trace + write window + `verification_log.csv` | `No` |
| `IT_045` | `TC_CANOE_IT_ETH_045_AMBULANCE_TX` | 구급차 외부 TX 관찰 | Ethernet trace + write window + `verification_log.csv` | `No` |

## 5. System Test 매핑

| ID | 후보 native asset | 주요 oracle | 주요 evidence | 진단 필요 여부 |
|---|---|---|---|---|
| `ST_001` | `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE` | 무경고 기준선 상태 | panel capture + screenshot + native report | `No` |
| `ST_002` | `TC_CANOE_ST_CORE_002_NORMAL_DRIVE` | 정상 주행 상태 | panel capture + screenshot + native report | `No` |
| `ST_003` | `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION` | 기본 경고 활성 결과 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_004` | `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR` | 정상 복귀 상태 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_005` | `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE` | school-zone 경고 전이 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_006` | `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE` | school-zone 복구 상태 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_007` | `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION` | 고속도로 정책 전이 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_008` | `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY` | 경고 발생 및 해제 결과 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_009` | `TC_CANOE_ST_CORE_009_GUIDE_LEFT` | 좌측 안내 표시 결과 | cluster capture + screenshot + native report | `No` |
| `ST_010` | `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR` | 우측 안내 표시 결과 | cluster capture + screenshot + native report | `No` |
| `ST_011` | `TC_CANOE_ST_V2_011_POLICE_OVERRIDE` | 경찰 우선 결과 | panel capture + trace + native report | `No` |
| `ST_012` | `TC_CANOE_ST_V2_012_AMBULANCE_OVERRIDE` | 구급차 우선 결과 | panel capture + trace + native report | `No` |
| `ST_013` | `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` | 경찰 방향 표시 | cluster/HUD capture + native report | `No` |
| `ST_014` | `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` | 구급차 방향 표시 | cluster/HUD capture + native report | `No` |
| `ST_015` | `TC_CANOE_ST_V2_015_AMBULANCE_PRIORITY` | 최종 선택 경고 상태 | panel capture + trace + native report | `No` |
| `ST_016` | `TC_CANOE_ST_V2_016_POLICE_TIEBREAK` | ETA 및 SourceID 중재 결과 | native report + sysvar snapshot + trace | `No` |
| `ST_017` | `TC_CANOE_ST_V2_017_AMBULANCE_TIEBREAK` | ETA 및 SourceID 중재 결과 | native report + sysvar snapshot + trace | `No` |
| `ST_018` | `TC_CANOE_ST_018_POLICE_TX_PERIOD` | 경찰 TX 주기 관찰 | Ethernet trace + `verification_log.csv` + write window | `No` |
| `ST_019` | `TC_CANOE_ST_019_AMBULANCE_TX_PERIOD` | 구급차 TX 주기 관찰 | Ethernet trace + `verification_log.csv` + write window | `No` |
| `ST_020` | `TC_CANOE_ST_V2_020_TIMEOUT_CLEAR` | timeout 해제 및 복귀 상태 | native report + trace + sysvar snapshot | `No` |
| `ST_021` | `TC_CANOE_ST_CORE_021_EMERGENCY_CLEAR_RESTORE` | 이전 경고 복원 상태 | panel capture + trace + native report | `No` |
| `ST_022` | `TC_CANOE_ST_EXT_022_INTERSECTION_DECEL` | 경고/decel 결합 결과 | panel capture + trace + sysvar snapshot | `No` |
| `ST_023` | `TC_CANOE_ST_EXT_023_MERGE_DECEL` | 경고/decel 결합 결과 | panel capture + trace + sysvar snapshot | `No` |
| `ST_024` | `TC_CANOE_ST_EXT_024_DRIVER_INTERVENTION_CLEAR` | 운전자 개입 해제 결과 | panel capture + trace + native report | `No` |
| `ST_025` | `TC_CANOE_ST_EXT_025_FAILSAFE_ENTRY` | fail-safe 진입 및 최소 채널 상태 | native report + write window + trace + sysvar snapshot | `No` |
| `ST_026` | `TC_CANOE_ST_EXT_026_FAILSAFE_RECOVERY` | fail-safe 복구 상태 | native report + trace + sysvar snapshot | `No` |
| `ST_027` | `TC_CANOE_ST_EXT_027_FRONTAL_OBJECT_RISK` | object-warning 표시 결과 | panel capture + event log + trace | `No` |
| `ST_028` | `TC_CANOE_ST_EXT_028_LATERAL_OBJECT_RISK` | object-warning 표시 결과 | panel capture + event log + trace | `No` |
| `ST_029` | `TC_CANOE_ST_EXT_029_CUTIN_OBJECT_RISK` | object-warning 표시 결과 | panel capture + event log + trace | `No` |
| `ST_030` | `TC_CANOE_ST_030_SEATBELT_CONTEXT_ADJUST` | 안전벨트/운전자 맥락 조정 경고 | panel capture + screenshot + native report | `No` |
| `ST_031` | `TC_CANOE_ST_031_DISTANCE_DISPLAY_CONSISTENCY` | 긴급 거리 표시 일관성 | panel capture + screenshot + native report | `No` |
| `ST_032` | `TC_CANOE_ST_EXT_032_USER_SETTING_CHANGE` | 출력 정책 갱신 상태 | panel capture + screenshot + native report | `No` |
| `ST_033` | `TC_CANOE_ST_EXT_033_HISTORY_QUERY` | 이력 조회 결과 | panel capture + screenshot + native report | `No` |
| `ST_034` | `TC_CANOE_ST_034_DUPLICATE_POPUP_GUARD` | 중복 팝업 guard 안정성 결과 | native report + trace + `verification_log.csv` | `No` |
| `ST_035` | `TC_CANOE_ST_035_TIMEOUT_CLEAR_RESTORE` | timeout-clear 복원 안정성 결과 | native report + trace + `verification_log.csv` | `No` |
| `ST_036` | `TC_CANOE_ST_036_FAILSAFE_RECOVERY_STABILITY` | fail-safe 복구 안정성 결과 | native report + trace + `verification_log.csv` | `No` |
| `ST_037` | `TC_CANOE_ST_037_AUDIO_CHANNEL_STABILITY` | 오디오 채널 안정성 결과 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_038` | `TC_CANOE_ST_038_VISUAL_CHANNEL_STABILITY` | 시각 채널 안정성 결과 | panel capture + trace + `verification_log.csv` | `No` |
| `ST_039` | `TC_CANOE_ST_EXT_039_CHASSIS_CONTEXT` | 제동/안정성 맥락 결과 | native report + trace + sysvar snapshot | `No` |
| `ST_040` | `TC_CANOE_ST_EXT_040_OCCUPANT_COMFORT_CONTEXT` | body/occupant/comfort 맥락 결과 | native report + trace + sysvar snapshot | `No` |
| `ST_041` | `TC_CANOE_ST_EXT_041_DISPLAY_SERVICE_CONTEXT` | 표시/서비스 맥락 결과 | panel capture + trace + native report | `No` |
| `ST_042` | `TC_CANOE_ST_EXT_042_ADAS_PERCEPTION_CONTEXT` | ADAS/perception 맥락 결과 | native report + trace + sysvar snapshot | `No` |
| `ST_043` | `TC_CANOE_ST_EXT_043_SERVICE_SECURITY_DIAG_CONTEXT` | service/security/diagnostic 맥락 결과 | native report + trace + write window + sysvar snapshot | `Yes` |
| `ST_044` | `TC_CANOE_ST_EXT_044_CHARGE_POWER_CONTEXT` | power/charge 맥락 결과 | native report + trace + sysvar snapshot | `No` |
| `ST_045` | `TC_CANOE_ST_EXT_045_TRIP_SEQUENCE` | 종단 간 시나리오 판정 | native report + panel capture + trace + `verification_log.csv` | `No` |
| `ST_046` | `TC_CANOE_ST_EXT_046_FAILSAFE_RECOVERY` | 종단 간 fail-safe 시나리오 판정 | native report + panel capture + trace + `verification_log.csv` | `No` |

## 6. 현재 구현 우선순위

native asset 구축 우선순위는 다음과 같습니다.

1. `UT_003`, `UT_009`, `UT_011`, `UT_014`, `UT_015`
2. `IT_001` to `IT_008`
3. `ST_001` to `ST_021`
4. diagnostic-linked 항목:
   - `UT_063`
   - `UT_064`
   - `IT_040`
   - `ST_043`

## 7. 다른 verification 문서와의 관계

이 문서는 다음 문서와 함께 읽습니다.

- `oracle.md`
- `execution-guide.md`
- `acceptance-criteria.md`
- `evidence-policy.md`
- `diagnostic-coverage.md`

## 최신 diagnostic 실행 기준선 (2026-03-15)

| 공식 범위 | Native Asset | TEST_SCN Scenario | 주요 producer 연결 | 현재 gate |
| --- | --- | --- | --- | --- |
| UT_063 | `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE` | `203` | `SGW.can -> Diag::SecurityState, Diag::RouteOwner` | 실행 가능한 unit contract 고정 |
| UT_064 | `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE` | `204` | `DCM.can -> Diag::ServiceState, Diag::ResponseKind, Diag::ReasonCode, Diag::LastRequestSid, Diag::LastResponseCode, Diag::LastResponseOk` | 실행 가능한 unit contract 고정 |
| IT_040 | `TC_CANOE_IT_EXT_040_SERVICE_SECURITY_DIAG` | `205` | `SGW + DCM 통합 diagnostic seam` | producer 연결 고정, runtime evidence 대기 |
| ST_043 | `TC_CANOE_ST_EXT_043_SERVICE_SECURITY_DIAG_CONTEXT` | `202` | `SGW + DCM 통합 diagnostic seam with scenario phase tracking` | producer 연결 고정, runtime evidence 대기 |

## Wave 2 direct-ownership UT 기준선

| 공식 범위 | Native Asset | 예약 TEST_SCN Scenario | 현재 상태 |
| --- | --- | --- | --- |
| UT_003 | `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | `206` | 실행 가능한 scenario contract 고정 |
| UT_011 | `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | `207` | 실행 가능한 scenario contract 고정 |
| UT_014 | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` | `208` | 실행 가능한 scenario contract 고정 |
| UT_015 | `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` | `209` | 실행 가능한 scenario contract 고정 |
| UT_076 | `TC_CANOE_UT_OUT_076_POLICE_TX` | `4` | external-TX unit contract 생성, 최종 frame-period closure는 trace gate 대기 |
| UT_077 | `TC_CANOE_UT_OUT_077_AMBULANCE_TX` | `5` | external-TX unit contract 생성, 최종 frame-period closure는 trace gate 대기 |

## Wave 2 oracle 기준선

- `UT_003 / 206`: 정상 CGW 경계 준비 상태, 정상 routing policy, fail-safe 해제를 확인합니다.
- `UT_011 / 207`: 의도한 ADAS warning-selection 맥락, 정상 경고 경로, fail-safe 해제를 확인합니다.
- `UT_014 / 208`: 정상 body gateway health 아래의 BCM ambient 정책을 확인합니다.
- `UT_015 / 209`: fail-safe 우선 덮어쓰기 없이 의도한 IVI 문구/출력 매핑을 확인합니다.
- `UT_076 / 4`: TX 기준 oracle과 trace-gated frame 증적을 기준으로 police emergency 전송 활성화를 확인합니다.
- `UT_077 / 5`: TX 기준 oracle과 trace-gated frame 증적을 기준으로 ambulance emergency 전송 활성화를 확인합니다.

## Wave 2 현재 진행 업데이트

- `UT_003 / 206`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `domainBoundaryStatus=1`, `routingPolicy=1`, `selectedAlertLevel=0`, `failSafeMode=0`를 확인합니다.
- `UT_011 / 207`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `selectedAlertLevel=3`, `selectedAlertType=3`, `warningPathStatus=0`, `failSafeMode=0`를 확인합니다.
- `UT_014 / 208`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `selectedAlertLevel=3`, `selectedAlertType=3`, `ambientColor=3`, `ambientPattern=5`, `failSafeMode=0`를 기준으로 school-zone ambient 정책을 확인합니다.
- `UT_015 / 209`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `selectedAlertLevel=6`, `selectedAlertType=1`, `warningTextCode=101`, `failSafeMode=0`를 기준으로 police-emergency text 매핑을 확인합니다.

## Wave 2 진행 업데이트 (208/209)

- `UT_014 / 208`: 실행 가능한 scenario contract를 고정했고 현재 ambient-policy 기준선에 정렬했습니다.
- `UT_015 / 209`: 실행 가능한 scenario contract를 고정했고 현재 IVI text-mapping 기준선에 정렬했습니다.
- dedicated external-TX unit row는 `UT_076 / 4`, `UT_077 / 5`로 별도 추적합니다.
- `UT_006`: 실행 가능한 object-risk unit contract를 추가했습니다. 현재 oracle은 scenario `20`, `21`, `22`, `24`를 통해 정면/교차로/merge risk와 confidence-degrade 동작을 확인합니다.
- `UT_007`: 실행 가능한 CLU context-adjust unit contract를 추가했습니다. 현재 oracle은 scenario `214`, `215`, `222`를 통해 seat-belt 강조, display-policy 반영, 거리 맥락 표시를 확인합니다.
- `UT_008`: 실행 가능한 boundary/fail-safe unit contract를 추가했습니다. 현재 oracle은 scenario `18`, `203`, `204`를 통해 fail-safe 유지와 SGW/DCM service seam 해석을 확인합니다.
- `UT_010`: 실행 가능한 emergency lifecycle unit contract를 추가했습니다. 현재 oracle은 scenario `4`, `5`에서 police/ambulance 활성화를 확인하고, scenario `6`에서 timeout-clear를 확인합니다.
- `UT_070`: 실행 가능한 BCM output unit contract를 추가했습니다. 현재 oracle은 scenario `208`, `4`를 통해 school-zone 및 emergency ambient 출력을 확인합니다.
- `UT_071`: 실행 가능한 IVI HMI output unit contract를 추가했습니다. 현재 oracle은 scenario `215`, `220`, `222`를 통해 문구/방향, 팝업/테마, 거리 맥락을 확인합니다.
- `UT_072`: 실행 가능한 CLU display unit contract를 추가했습니다. 현재 oracle은 scenario `30`, `33`, `220`을 통해 police/ambulance 방향 표시와 팝업/테마 동기화를 확인합니다.
- `UT_073`: 실행 가능한 HUD/front-display unit contract를 추가했습니다. 현재 oracle은 scenario `30`, `220`을 통해 전면 표시 공용 방향 정보와 팝업/테마 seam을 확인합니다.
- `UT_074`: 실행 가능한 AMP audio unit contract를 추가했습니다. 현재 oracle은 scenario `215`를 통해 audio focus, ducking, volume policy를 확인합니다.
- `UT_075`: 실행 가능한 decel-assist output unit contract를 추가했습니다. 현재 oracle은 scenario `16`, `18`을 통해 활성 request와 fail-safe 차단을 확인합니다.

## External TX unit 완료 업데이트

- `UT_076 / 4`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `V2X::alertState=1`, `V2X::emergencyType=1`, `V2X::eta=12`, `V2X::sourceId=11`, `selectedAlertLevel=6`, `warningTextCode=101`을 기준으로 police emergency 전송 활성화를 확인합니다.
- `UT_077 / 5`: 실행 가능한 scenario contract를 추가했습니다. 현재 oracle은 `V2X::alertState=1`, `V2X::emergencyType=2`, `V2X::eta=8`, `V2X::sourceId=22`, `selectedAlertLevel=7`, `warningTextCode=202`를 기준으로 ambulance emergency 전송 활성화를 확인합니다.
- 이전에 `UT_076/077`을 차지하던 retired 맥락/표시 초안은 `retire/` 아래로 이동했습니다.

## Wave 3 system-test 기준선

| 공식 범위 | Native Asset | TEST_SCN Scenario | 현재 계약 |
| --- | --- | --- | --- |
| ST_001 | `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE` | `1` | 전원 인가 초기화가 fail-safe 잔여 상태 없이 no-warning 준비 상태로 들어가는지 확인 |
| ST_002 | `TC_CANOE_ST_CORE_002_NORMAL_DRIVE` | `14` | 정상 주행 기준선에서 routing이 정상이고 no-warning 상태가 안정적인지 확인 |
| ST_003 | `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION` | `1 -> 26` | general-road single-risk 활성화가 fail-safe drift 없이 basic warning 상태를 올리는지 확인 |
| ST_004 | `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR` | `26 -> 1` | 조건 제거 후 basic warning이 no-warning 기준선으로 정상 복귀하는지 확인 |
| ST_005 | `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE` | `1 -> 2` | 정상 주행에서 school-zone 과속으로 전이될 때 school-zone warning 정책으로 전환되는지 확인 |
| ST_006 | `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE` | `2 -> 1` | 정상 주행 기준선으로 돌아갈 때 school-zone warning이 정상 해제되는지 확인 |
| ST_007 | `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION` | `14 -> 244` | 정상 주행에서 highway 맥락으로 전이될 때 false warning 없이 highway policy에 안정화되는지 확인 |
| ST_008 | `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY` | `244 -> 3 -> 244` | 지속적인 steering inactivity 뒤 highway no-steer warning이 발생하고 steering recovery 후 해제되는지 확인 |
| ST_009 | `TC_CANOE_ST_CORE_009_GUIDE_LEFT` | `7` | 좌측 안내 warning이 표시 출력 전반에서 일관되게 렌더링되는지 확인 |
| ST_010 | `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR` | `8 -> 1` | guide-right warning이 올바르게 렌더링되고 완료 후 no-warning 기준선으로 복귀하는지 확인 |
| ST_011 | `TC_CANOE_ST_V2_011_POLICE_OVERRIDE` | `11` | police emergency가 활성 general-warning 맥락을 모호함 없이 우선 덮어쓰는지 확인 |
| ST_012 | `TC_CANOE_ST_V2_012_AMBULANCE_OVERRIDE` | `223` | ambulance emergency가 활성 general-warning 맥락을 모호함 없이 우선 덮어쓰는지 확인 |
| ST_013 | `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` | `30` | `warningTextCode=102`, `renderDirection=2` 조건의 police-right emergency 표시를 확인 |
| ST_014 | `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` | `33` | `warningTextCode=201`, `renderDirection=1` 조건의 ambulance-left emergency 표시를 확인 |
| ST_015 | `TC_CANOE_ST_V2_015_AMBULANCE_PRIORITY` | `212` | police와 ambulance dispatch가 동시에 들어올 때 ambulance warning이 선택 유지되는지 확인 |
| ST_016 | `TC_CANOE_ST_V2_016_POLICE_TIEBREAK` | `10` | 동순위 police warning이 ETA 동률 후 SourceID 기준으로 일관되게 결정되는지 확인 |
| ST_017 | `TC_CANOE_ST_V2_017_AMBULANCE_TIEBREAK` | `224` | 동순위 ambulance warning이 ETA 동률 후 SourceID 기준으로 일관되게 결정되는지 확인 |
| ST_018 | `TC_CANOE_ST_018_POLICE_TX_PERIOD` | `4` | police external transport 맥락이 trace-gated `100ms` 주기 closure로 자극되는지 확인 |
| ST_019 | `TC_CANOE_ST_019_AMBULANCE_TX_PERIOD` | `5` | ambulance external transport 맥락이 trace-gated `100ms` 주기 closure로 자극되는지 확인 |
| ST_020 | `TC_CANOE_ST_V2_020_TIMEOUT_CLEAR` | `35` | timeout-clear가 emergency 맥락을 제거하고 시스템을 안전한 복원 상태로 돌리는지 확인 |
| ST_021 | `TC_CANOE_ST_CORE_021_EMERGENCY_CLEAR_RESTORE` | `35` | emergency clear 후 zone-warning 복원이 이어지는지 확인 |
| ST_027 | `TC_CANOE_ST_EXT_027_FRONTAL_OBJECT_RISK` | `20` | forward TTC conflict 조건에서 frontal object-risk warning과 event-log 일관성을 확인 |
| ST_028 | `TC_CANOE_ST_EXT_028_LATERAL_OBJECT_RISK` | `21` | intersection conflict 조건에서 lateral object-risk warning과 event-log 일관성을 확인 |
| ST_029 | `TC_CANOE_ST_EXT_029_CUTIN_OBJECT_RISK` | `22` | merge conflict 조건에서 cut-in object-risk warning과 event-log 일관성을 확인 |
| ST_030 | `TC_CANOE_ST_030_SEATBELT_CONTEXT_ADJUST` | `214` | 의도하지 않은 fail-safe 또는 alert-class drift 없이 seat-belt/driver 맥락이 warning 맥락을 조정하는지 확인 |
| ST_031 | `TC_CANOE_ST_031_DISTANCE_DISPLAY_CONSISTENCY` | `222` | emergency 거리 표시가 warning text 및 police-right 렌더링 맥락과 일관되는지 확인 |
| ST_032 | `TC_CANOE_ST_EXT_032_USER_SETTING_CHANGE` | `215` | 사용자 표시/볼륨 정책 변경이 system-level warning 안내에 일관되게 반영되는지 확인 |
| ST_033 | `TC_CANOE_ST_EXT_033_HISTORY_QUERY` | `222 + historyQuery(0)` | emergency warning 이후 거리 표시와 latest-history query response가 일관되는지 확인 |
| ST_034 | `TC_CANOE_ST_034_DUPLICATE_POPUP_GUARD` | `12` | 안정된 warning 안내를 유지하면서 rapid re-trigger oscillation을 억제하는지 확인 |
| ST_035 | `TC_CANOE_ST_035_TIMEOUT_CLEAR_RESTORE` | `35` | timeout-clear 경로가 fail-safe 잔여 상태 없이 이전 valid warning 맥락을 복원하는지 확인 |
| ST_036 | `TC_CANOE_ST_036_FAILSAFE_RECOVERY_STABILITY` | `201` | fail-safe recovery 후 warning 경로가 residual oscillation 없이 normal로 복귀하는지 확인 |
| ST_037 | `TC_CANOE_ST_037_AUDIO_CHANNEL_STABILITY` | `215` | 활성 emergency 안내 동안 audio focus, ducking, volume handling이 안정적인지 확인 |
| ST_038 | `TC_CANOE_ST_038_VISUAL_CHANNEL_STABILITY` | `220` | 시각 우선 warning mode에서 popup priority와 cluster synchronization이 fail-safe drift 없이 안정적인지 확인 |
| ST_045 | `TC_CANOE_ST_EXT_045_TRIP_SEQUENCE` | `200` | 전체 주행 시퀀스 후 no-warning 안정 상태로 복귀하는지 확인 |
| ST_046 | `TC_CANOE_ST_EXT_046_FAILSAFE_RECOVERY` | `201` | fail-safe recovery 후 `failSafeMode`가 `0`으로 복귀하는지 확인 |

## Wave 2 완료 업데이트 (UT_004/UT_005)

- `UT_004`: `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN`은 scenario `9`를 사용하며 `V2X.can`의 ETA/source 우선순위 처리를 검증합니다.
- `UT_005`: `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST`는 scenario `16`를 사용하며 `ADAS.can`의 proximity-risk 및 decel-assist 활성화를 검증합니다.
- 위 추가분까지 포함하면 현재 direct-ownership `05` core 기준선 (`UT_003`, `UT_004`, `UT_005`, `UT_011`, `UT_014`, `UT_015`, `UT_063`, `UT_064`, `UT_076`, `UT_077`)은 실행 가능한 asset contract를 확보한 상태입니다.

## Wave 5 gateway 및 extension UT 기준선

- `UT_001`: `TC_CANOE_UT_CORE_001_CGW_CHS_GW`는 scenario `216`, `217`, `218`, `219`를 사용해 drive, speed, steering, brake 맥락에 대한 정규화된 chassis-state 전달을 검증합니다.
- `UT_002`: `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW`는 scenario `2`, `7`, `8`을 사용해 infotainment gateway 경로를 통한 zone, direction, distance, speed-limit 전달을 검증합니다.
- `UT_009`: `TC_CANOE_UT_CORE_009_NAV_CTX_MGR`는 scenario `2`, `3`, `7`, `8`을 사용해 zone 맥락 분류와 navigation 맥락 안정화를 검증합니다.
- `UT_012`: `TC_CANOE_UT_CORE_012_BODY_GW_ROUTE`는 scenario `208`, `4`를 사용해 최종 warning result가 body 출력 경로로 ambient-route 전달되는지 검증합니다.
- `UT_013`: `TC_CANOE_UT_CORE_013_IVI_GW_ROUTE`는 scenario `209`, `30`, `33`을 사용해 최종 warning result가 IVI/cluster 출력 경로로 cluster-route 전달되는지 검증합니다.
- `UT_016`: `TC_CANOE_UT_EXT_016_CHS_BRAKE_EXT`는 scenario `216`, `219`를 사용해 brake 및 parked-state 맥락 전파를 검증합니다.
- `UT_017`: `TC_CANOE_UT_EXT_017_CHS_DYNAMICS_EXT`는 scenario `225`를 사용해 suspension/chassis-dynamics 맥락 전파를 검증합니다.
- `UT_018`: `TC_CANOE_UT_EXT_018_BODY_ENTRY_EXIT`는 scenario `226`, `227`을 사용해 door 및 tailgate 진입/이탈 맥락 전파를 검증합니다.
- `UT_019`: `TC_CANOE_UT_EXT_019_BODY_OCCUPANT_PROTECTION`는 scenario `228`을 사용해 occupant-detection 및 occupant-protection 맥락 전파를 검증합니다.

## Wave 6 service, assist, router UT 기준선

- `UT_020`: `TC_CANOE_UT_EXT_020_BODY_COMFORT`는 scenario `229`, `230`을 사용해 HVAC remote-climate 동작, AFLS/AHLS comfort-lighting 전파, static seat/sunroof comfort 출력을 함께 검증합니다.
- `UT_021`: `TC_CANOE_UT_EXT_021_IVI_DISPLAY_SERVICE`는 scenario `229`, `30`, `215`를 사용해 TMU service 전달, HUD 표시 렌더링, AMP audio-policy 전파를 검증합니다.
- `UT_022`: `TC_CANOE_UT_EXT_022_IVI_SERVICE_ACCESS`는 scenario `229`를 사용해 TMU service 상태와 digital-key service-access 전파를 검증합니다.
- `UT_023`: `TC_CANOE_UT_EXT_023_ADAS_DRIVE_ASSIST`는 scenario `233`을 사용해 FCAM state 기반의 `LDWS_LKAS`, `RPC` drive-assist / road-preview 전파를 검증합니다.
- `UT_024`: `TC_CANOE_UT_EXT_024_ADAS_PARKING_PERCEPTION`는 scenario `234`를 사용해 AVM / ultrasonic / SPAS / RSPA state 기반의 `PKM`, `SPM` parking-perception 전파를 검증합니다.
- `UT_025`: `TC_CANOE_UT_EXT_025_WARNING_DELIVERY_BOUNDARY`는 scenario `18`, `203`, `204`를 사용해 fail-safe 진입과 SGW/DCM delivery-boundary, response-state 전파를 함께 검증합니다.
- `UT_026`: `TC_CANOE_UT_EXT_026_DOMAIN_ROUTER_PROPULSION`는 scenario `232`를 사용해 `EOP`, `MCU`, `INVERTER`를 통한 propulsion 맥락 전파를 검증합니다.
- `UT_027`: `TC_CANOE_UT_EXT_027_DOMAIN_ROUTER_POWER_CHARGE`는 scenario `231`를 사용해 `OBC`, `DCDC`를 통한 charging 맥락 전파를 검증합니다.

## Wave 4 integration 기준선

| 공식 범위 | Native Asset | TEST_SCN Scenario | 현재 계약 |
| --- | --- | --- | --- |
| IT_002 | `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` | `2` | nav/chassis 입력에서 ambient 출력까지 이어지는 school-zone 경고 경로를 검증 |
| IT_003 | `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` | `3` | chassis 입력에서 ambient 출력까지 이어지는 highway no-steer 경로를 검증 |
| IT_001 | `TC_CANOE_IT_CORE_001_BASE_ACTIVATION` | `1 -> 2 -> 12` | idle no-warning 기준선, 활성화, duplicate-guard 안정성을 하나의 통합 흐름으로 검증 |
| IT_004 | `TC_CANOE_IT_V2_004_POLICE_RX` | `4` | police emergency 수신 경로가 최종 warning 상태로 반영되는지 검증 |
| IT_005 | `TC_CANOE_IT_V2_005_AMBULANCE_RX` | `5` | ambulance emergency 수신 경로가 최종 warning 상태로 반영되는지 검증 |
| IT_006 | `TC_CANOE_IT_V2_006_ARBITRATION` | `9 -> 10 -> 11 -> 212` | ETA 우선순위, SourceID tiebreak, emergency-over-nav takeover, ambulance-over-police dispatch priority를 포함한 arbitration 기준선을 검증 |
| IT_007 | `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | `4` | emergency ambient 출력 경로를 검증 |
| IT_008 | `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` | `30` | cluster 방향 출력 경로를 검증 |
| IT_009 | `TC_CANOE_IT_V2_009_TIMEOUT_CLEAR` | `35` | emergency clear 후 이전 valid 맥락으로 안전하게 복원되는지 검증 |
| IT_010 | `TC_CANOE_IT_V2_010_DECEL_ASSIST` | `19` | emergency proximity 상황에서 decel-assist request와 warning synchronization을 검증 |
| IT_011 | `TC_CANOE_IT_V2_011_FAILSAFE_MIN_WARNING` | `18` | fail-safe downgrade 시 minimum warning 유지와 decel 차단을 검증 |
| IT_012 | `TC_CANOE_IT_EXT_012_OBJECT_RISK_EVENTLOG` | `20 -> 21 -> 22 -> 24 -> 25` | object-risk escalation, validity filtering, confidence downgrade, event-log 연속성을 검증 |
| RET_IT_013 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `214 -> 215 -> 236 -> 239` | driver-context umbrella row는 retired 처리하고 exact executable row로 대체 |
| IT_013 | `TC_CANOE_IT_013_SEATBELT_CONTEXT` | `214` | 의도하지 않은 alert-class drift 없이 seat-belt 맥락이 warning 강조를 높이는지 검증 |
| IT_014 | `TC_CANOE_IT_014_DISPLAY_POLICY` | `215` | display-policy 설정이 output code와 렌더링된 방향 상태에 반영되는지 검증 |
| IT_015 | `TC_CANOE_IT_015_TURN_LAMP_CONTEXT` | `239` | fail-safe 또는 level drift 없이 right turn-lamp context가 school-zone warning 유형을 조정하는지 검증 |
| IT_016 | `TC_CANOE_IT_016_DRIVE_MODE_SENSITIVITY` | `236` | alert 유형을 유지한 채 sport-mode context가 school-zone warning 민감도를 올리는지 검증 |
| IT_017 | `TC_CANOE_IT_017_AUDIO_VOLUME_POLICY` | `215` | alert-volume 설정이 audio focus, ducking, volume policy state에 반영되는지 검증 |
| IT_018 | `TC_CANOE_IT_EXT_018_EMERGENCY_PLUS_TTC` | `213` | 동시 TTC intersection conflict 상황에서 emergency priority 유지와 decel-assist request를 검증 |
| RET_IT_015 | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | `216 -> 217` | powertrain umbrella row는 retired 처리하고 exact parked/drive executable row로 대체 |
| IT_019 | `TC_CANOE_IT_019_POWERTRAIN_PARKED_BASELINE` | `216` | parked 기준선에서 drive-state와 speed-state가 stable no-warning integration 기준선을 유지하는지 검증 |
| IT_020 | `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE` | `217` | drive 기준선이 의도하지 않은 warning activation 없이 drive-state와 speed-state를 전달하는지 검증 |
| RET_IT_016 | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | `218 -> 219 -> 237` | chassis umbrella row는 retired 처리하고 exact steering/braking/acceleration executable row로 대체 |
| IT_021 | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE` | `218` | steering-input 전파 기준선에서 steering과 speed state가 warning judgment에 맞게 정렬되는지 검증 |
| IT_022 | `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE` | `219` | braking-input 전파 기준선에서 brake와 speed state가 warning judgment에 맞게 정렬되는지 검증 |
| IT_023 | `TC_CANOE_IT_023_CHASSIS_ACCEL_BASELINE` | `237` | high-acceleration 기준선이 driveMode와 sport-state를 stable chassis integration result로 이끄는지 검증 |
| RET_IT_017 | `TC_CANOE_IT_BASE_024_BODY_STATE` | `211 -> 216` | body umbrella row는 retired 처리하고 exact hazard/window executable row로 대체 |
| IT_024 | `TC_CANOE_IT_BASE_024_BODY_STATE` | `211` | hazard 반영 기준선에서 turn-lamp state와 alert level이 drift 없이 정렬되는지 검증 |
| IT_025 | `TC_CANOE_IT_EXT_025_WINDOW_STATE` | `226` | 진입 맥락에서 좌/우 door window position이 door/window 출력 반영과 일관되는지 검증 |
| IT_026 | `TC_CANOE_IT_BASE_026_BASIC_DISPLAY_UI` | `220` | visual-first display mode에서 popup, theme, cluster-sync state가 school-zone warning에 맞게 일관되는지 검증 |
| RET_IT_019 | `TC_CANOE_IT_BASE_027_COMFORT_CONTEXT / TC_CANOE_IT_BASE_030_BODY_SECURITY_CONTEXT` | `229 / 203` | comfort/security umbrella row는 retired 처리하고 exact executable row로 대체 |
| IT_027 | `TC_CANOE_IT_BASE_027_COMFORT_CONTEXT` | `229` | remote-climate, HVAC, rear-climate, digital-access 출력이 하나의 comfort context로 일관되게 유지되는지 검증 |
| IT_028 | `TC_CANOE_IT_EXT_028_BODY_CONTROL_LOCK` | `226` | 좌/우 body control 출력 경로 전반에서 door lock/open 반영이 일관되는지 검증 |
| IT_029 | `TC_CANOE_IT_EXT_029_WIPER_RAIN_BASELINE` | `229` | parked comfort context에서 wiper와 rain-light 기준선이 비활성 상태로 일관되게 유지되는지 검증 |
| IT_030 | `TC_CANOE_IT_BASE_030_BODY_SECURITY_CONTEXT` | `203` | service downgrade state와 충돌 없이 security-state boundary가 유지되는지 검증 |
| IT_031 | `TC_CANOE_IT_031_AUDIO_GUIDE_RUNTIME` | `215` | emergency warning 상황에서 audio focus, ducking, 명시적 warning-volume policy를 검증 |
| RET_IT_021 | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | `18 -> 12 -> 35` | output-availability umbrella row는 retired 처리하고 exact executable row로 대체 |
| IT_032 | `TC_CANOE_IT_032_OUTPUT_FALLBACK` | `18` | fail-safe entry 상황에서도 minimum warning channel이 유지되는지 검증 |
| IT_033 | `TC_CANOE_IT_033_DUPLICATE_POPUP_SUPPRESSION` | `12` | 중복 팝업 억제가 과도한 non-emergency popup 반복 변동을 막는지 검증 |
| IT_034 | `TC_CANOE_IT_034_CHANNEL_RESTORE` | `35` | clear 또는 mismatch recovery 뒤 channel 상태가 일관된 warning 맥락으로 복원되는지 검증 |
| IT_035 | `TC_CANOE_IT_EXT_035_DISTANCE_HISTORY` | `222 + historyQuery(0)` | emergency 거리 표시와 latest-history response가 일관되는지 검증 |
