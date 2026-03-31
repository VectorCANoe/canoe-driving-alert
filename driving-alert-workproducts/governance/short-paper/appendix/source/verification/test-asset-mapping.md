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

### 3.1 핵심 oracle 축

별첨에서는 Unit Test oracle을 아래 anchor 중심으로 읽습니다.

- `selected warning state`: 최종 경고 level/type과 text, route 결과
- `zone context state`: school-zone, highway, direction, distance와 같은 문맥 상태
- `clear and restore state`: clear, restore, timeout 복귀 기준
- `fail-safe state`: fail-safe 진입, 유지, 해제 판단
- `display-policy state`: visual-first, popup/theme, cluster-sync 기준
- `audio policy state`: audio focus, ducking, volume policy 기준
- `channel availability/fallback`: 출력 채널 유지와 fallback 기준
- `scenario verdict`: `TEST_SCN` 단위 verdict
- `fail-safe scenario verdict`: boundary/fail-safe가 포함된 verdict

### 3.2 핵심 evidence 축

- `native report + trace + sysvar`: 기본 runtime 동작 확인
- `native report + sysvar + panel`: panel 반영이 중요한 경고/출력 검증
- `panel/cluster capture + screenshot`: reviewer-visible output 검증
- `write window + trace + sysvar`: diagnostic, fail-safe, route-owner 검증
- `Eth trace + write window + verification_log`: external TX와 backbone evidence 검증

### 3.3 UT 그룹 매핑

- `UT_001~UT_015`
  - asset family: `TC_CANOE_UT_CORE_*`
  - focus: zone, emergency, selected-warning, ambient/text route
  - evidence: native report, trace, sysvar, panel
  - diagnostic: `No`
- `UT_016~UT_027`
  - asset family: `TC_CANOE_UT_EXT_*`
  - focus: chassis, body, comfort, service, propulsion context
  - evidence: native report, trace, sysvar
  - diagnostic: `No`
- `UT_028~UT_062`
  - asset family: `TC_CANOE_UT_INP_*`
  - focus: domain input normalization, observer consistency
  - evidence: native report, trace, sysvar
  - diagnostic: `Yes`
- `UT_063~UT_065`
  - asset family: `TC_CANOE_UT_EXT_*`, `TC_CANOE_UT_INP_065_*`
  - focus: security, diagnostic, backbone fail-safe interpretation
  - evidence: write window, trace, sysvar
  - diagnostic: `Yes`
- `UT_070~UT_077`
  - asset family: `TC_CANOE_UT_OUT_*`
  - focus: ambient, HMI, audio render, external TX
  - evidence: panel, cluster capture, Eth trace, native report
  - diagnostic: `No`

### 3.4 직접 diagnostic row

- `UT_063`
  - asset: `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE`
  - minimal evidence: security-state injection, write window, trace, sysvar
- `UT_064`
  - asset: `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE`
  - minimal evidence: diagnostic-state injection, write window, trace, sysvar
- `UT_065`
  - asset: `TC_CANOE_UT_INP_065_ETHB_INPUT`
  - minimal evidence: backbone failure observer, trace, sysvar

## 4. Integration Test 매핑

- `IT_001~IT_009`
  - asset family: `TC_CANOE_IT_CORE_*`, `TC_CANOE_IT_V2_*`
  - focus: activation, school-zone, emergency priority, timeout clear
  - evidence: native report, trace, panel
  - diagnostic: `No`
- `IT_010~IT_018`
  - asset family: `TC_CANOE_IT_*`, `TC_CANOE_IT_EXT_*`
  - focus: decel assist, fail-safe minimum warning, display/audio policy
  - evidence: native report, panel, sysvar
  - diagnostic: `No`
- `IT_019~IT_030`
  - asset family: baseline/body/control integration assets
  - focus: parked/drive baseline, window, wiper, body security context
  - evidence: native report, trace, sysvar
  - diagnostic: `No`
- `IT_031~IT_043`
  - asset family: runtime/output integration assets
  - focus: fallback, duplicate suppression, display/service, audio guide
  - evidence: panel, write window, trace, native report
  - diagnostic: `No`
- `IT_040`, `IT_044`, `IT_045`
  - asset family: diagnostic and external TX assets
  - focus: service/security/diagnostic context, TX continuity
  - evidence: write window, Eth trace, sysvar
  - diagnostic: mixed

## 5. System Test 매핑

- `ST_001~ST_010`
  - asset family: `TC_CANOE_ST_CORE_*`
  - focus: power-on baseline, school/highway transition, guide render
  - evidence: panel, cluster capture, native report
  - diagnostic: `No`
- `ST_011~ST_021`
  - asset family: `TC_CANOE_ST_V2_*`, `TC_CANOE_ST_CORE_*`
  - focus: emergency override, tie-break, TX period, timeout restore
  - evidence: trace, report, panel
  - diagnostic: `No`
- `ST_022~ST_029`
  - asset family: `TC_CANOE_ST_EXT_*`
  - focus: decel coupling, fail-safe entry/recovery, object-risk scenario
  - evidence: trace, sysvar, panel
  - diagnostic: `No`
- `ST_030~ST_038`
  - asset family: HMI and system robustness assets
  - focus: seatbelt context, distance/history, popup/audio/visual stability
  - evidence: panel, screenshot, native report
  - diagnostic: `No`
- `ST_039~ST_046`
  - asset family: context and trip-sequence assets
  - focus: chassis, body, service, charge context, fail-safe round-trip
  - evidence: native report, trace, sysvar
  - diagnostic: `ST_043` only

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

- `UT_063`
  - native asset: `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE`
  - scenario: `203`
  - producer: `SGW.can -> Diag::SecurityState, Diag::RouteOwner`
  - gate: 실행 가능한 unit contract 고정
- `UT_064`
  - native asset: `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE`
  - scenario: `204`
  - producer: `DCM.can -> Diag::ServiceState, Diag::ResponseKind, Diag::ReasonCode, Diag::LastRequestSid, Diag::LastResponseCode, Diag::LastResponseOk`
  - gate: 실행 가능한 unit contract 고정
- `IT_040`
  - native asset: `TC_CANOE_IT_EXT_040_SERVICE_SECURITY_DIAG`
  - scenario: `205`
  - producer: `SGW + DCM` 통합 diagnostic seam
  - gate: producer 연결 고정, runtime evidence 대기
- `ST_043`
  - native asset: `TC_CANOE_ST_EXT_043_SERVICE_SECURITY_DIAG_CONTEXT`
  - scenario: `202`
  - producer: `SGW + DCM` 통합 diagnostic seam with scenario phase tracking
  - gate: producer 연결 고정, runtime evidence 대기

## Wave 2 direct-ownership UT 기준선

- `UT_003`
  - native asset: `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS`
  - scenario: `206`
  - status: 실행 가능한 scenario contract 고정
- `UT_011`
  - native asset: `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`
  - scenario: `207`
  - status: 실행 가능한 scenario contract 고정
- `UT_014`
  - native asset: `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY`
  - scenario: `208`
  - status: 실행 가능한 scenario contract 고정
- `UT_015`
  - native asset: `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING`
  - scenario: `209`
  - status: 실행 가능한 scenario contract 고정
- `UT_076`
  - native asset: `TC_CANOE_UT_OUT_076_POLICE_TX`
  - scenario: `4`
  - status: external-TX unit contract 생성, 최종 frame-period closure는 trace gate 대기
- `UT_077`
  - native asset: `TC_CANOE_UT_OUT_077_AMBULANCE_TX`
  - scenario: `5`
  - status: external-TX unit contract 생성, 최종 frame-period closure는 trace gate 대기

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

### 1. Baseline and transition

- `ST_001` `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE`, scenario `1`: no-warning 준비 상태 진입 확인
- `ST_002` `TC_CANOE_ST_CORE_002_NORMAL_DRIVE`, scenario `14`: 정상 주행 기준선 안정화 확인
- `ST_003` `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION`, scenario `1 -> 26`: basic warning 활성화 확인
- `ST_004` `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR`, scenario `26 -> 1`: no-warning 기준선 복귀 확인
- `ST_005` `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE`, scenario `1 -> 2`: school-zone 전환 확인
- `ST_006` `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE`, scenario `2 -> 1`: school-zone 해제 확인
- `ST_007` `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION`, scenario `14 -> 244`: highway policy 안정화 확인
- `ST_008` `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY`, scenario `244 -> 3 -> 244`: no-steer 경고 발생과 recovery 해제 확인
- `ST_009` `TC_CANOE_ST_CORE_009_GUIDE_LEFT`, scenario `7`: 좌측 안내 렌더링 확인
- `ST_010` `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR`, scenario `8 -> 1`: guide-right 렌더링과 clear 확인

### 2. Emergency precedence and TX

- `ST_011` `TC_CANOE_ST_V2_011_POLICE_OVERRIDE`, scenario `11`: police priority override 확인
- `ST_012` `TC_CANOE_ST_V2_012_AMBULANCE_OVERRIDE`, scenario `223`: ambulance priority override 확인
- `ST_013` `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT`, scenario `30`: police-right 방향 표시 확인
- `ST_014` `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT`, scenario `33`: ambulance-left 방향 표시 확인
- `ST_015` `TC_CANOE_ST_V2_015_AMBULANCE_PRIORITY`, scenario `212`: ambulance dispatch priority 유지 확인
- `ST_016` `TC_CANOE_ST_V2_016_POLICE_TIEBREAK`, scenario `10`: police tie-break 확인
- `ST_017` `TC_CANOE_ST_V2_017_AMBULANCE_TIEBREAK`, scenario `224`: ambulance tie-break 확인
- `ST_018` `TC_CANOE_ST_018_POLICE_TX_PERIOD`, scenario `4`: police TX period closure 확인
- `ST_019` `TC_CANOE_ST_019_AMBULANCE_TX_PERIOD`, scenario `5`: ambulance TX period closure 확인
- `ST_020` `TC_CANOE_ST_V2_020_TIMEOUT_CLEAR`, scenario `35`: timeout-clear 복원 확인
- `ST_021` `TC_CANOE_ST_CORE_021_EMERGENCY_CLEAR_RESTORE`, scenario `35`: zone-warning restore 확인

### 3. Object risk and fail-safe

- `ST_027` `TC_CANOE_ST_EXT_027_FRONTAL_OBJECT_RISK`, scenario `20`: frontal object-risk 경고와 event-log 일관성 확인
- `ST_028` `TC_CANOE_ST_EXT_028_LATERAL_OBJECT_RISK`, scenario `21`: lateral object-risk 경고와 event-log 일관성 확인
- `ST_029` `TC_CANOE_ST_EXT_029_CUTIN_OBJECT_RISK`, scenario `22`: cut-in object-risk 경고와 event-log 일관성 확인
- `ST_035` `TC_CANOE_ST_035_TIMEOUT_CLEAR_RESTORE`, scenario `35`: 이전 valid warning 복원 확인
- `ST_036` `TC_CANOE_ST_036_FAILSAFE_RECOVERY_STABILITY`, scenario `201`: residual oscillation 없는 recovery 확인
- `ST_046` `TC_CANOE_ST_EXT_046_FAILSAFE_RECOVERY`, scenario `201`: `failSafeMode=0` 복귀 확인

### 4. HMI stability and context

- `ST_030` `TC_CANOE_ST_030_SEATBELT_CONTEXT_ADJUST`, scenario `214`: seat-belt 강조와 alert drift 부재 확인
- `ST_031` `TC_CANOE_ST_031_DISTANCE_DISPLAY_CONSISTENCY`, scenario `222`: 거리 표시와 text/render 맥락 일치 확인
- `ST_032` `TC_CANOE_ST_EXT_032_USER_SETTING_CHANGE`, scenario `215`: user policy 반영 확인
- `ST_033` `TC_CANOE_ST_EXT_033_HISTORY_QUERY`, scenario `222 + historyQuery(0)`: history response 일관성 확인
- `ST_034` `TC_CANOE_ST_034_DUPLICATE_POPUP_GUARD`, scenario `12`: duplicate popup suppression 확인
- `ST_037` `TC_CANOE_ST_037_AUDIO_CHANNEL_STABILITY`, scenario `215`: audio focus, ducking, volume 안정성 확인
- `ST_038` `TC_CANOE_ST_038_VISUAL_CHANNEL_STABILITY`, scenario `220`: popup priority와 cluster sync 안정성 확인
- `ST_045` `TC_CANOE_ST_EXT_045_TRIP_SEQUENCE`, scenario `200`: 전체 시퀀스 후 no-warning 복귀 확인

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

### 1. Core and emergency integration

- `IT_001` `TC_CANOE_IT_CORE_001_BASE_ACTIVATION`, scenario `1 -> 2 -> 12`: idle baseline, activation, duplicate-guard 안정성 검증
- `IT_002` `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH`, scenario `2`: school-zone 경고 경로 검증
- `IT_003` `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH`, scenario `3`: highway no-steer 경로 검증
- `IT_004` `TC_CANOE_IT_V2_004_POLICE_RX`, scenario `4`: police emergency 수신 경로 검증
- `IT_005` `TC_CANOE_IT_V2_005_AMBULANCE_RX`, scenario `5`: ambulance emergency 수신 경로 검증
- `IT_006` `TC_CANOE_IT_V2_006_ARBITRATION`, scenario `9 -> 10 -> 11 -> 212`: arbitration 기준선 검증
- `IT_007` `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT`, scenario `4`: emergency ambient 출력 검증
- `IT_008` `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT`, scenario `30`: cluster 방향 출력 검증
- `IT_009` `TC_CANOE_IT_V2_009_TIMEOUT_CLEAR`, scenario `35`: emergency clear 후 안전 복원 검증
- `IT_010` `TC_CANOE_IT_V2_010_DECEL_ASSIST`, scenario `19`: decel-assist와 warning synchronization 검증
- `IT_011` `TC_CANOE_IT_V2_011_FAILSAFE_MIN_WARNING`, scenario `18`: minimum warning 유지와 decel 차단 검증
- `IT_012` `TC_CANOE_IT_EXT_012_OBJECT_RISK_EVENTLOG`, scenario `20 -> 21 -> 22 -> 24 -> 25`: object-risk escalation과 event-log 연속성 검증
- `IT_018` `TC_CANOE_IT_EXT_018_EMERGENCY_PLUS_TTC`, scenario `213`: emergency priority와 TTC decel-assist 동시 검증

### 2. Driver and HMI policy integration

- `RET_IT_013` `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT`, scenario `214 -> 215 -> 236 -> 239`: retired umbrella row
- `IT_013` `TC_CANOE_IT_013_SEATBELT_CONTEXT`, scenario `214`: seat-belt 강조 검증
- `IT_014` `TC_CANOE_IT_014_DISPLAY_POLICY`, scenario `215`: display-policy 출력 반영 검증
- `IT_015` `TC_CANOE_IT_015_TURN_LAMP_CONTEXT`, scenario `239`: turn-lamp 맥락 조정 검증
- `IT_016` `TC_CANOE_IT_016_DRIVE_MODE_SENSITIVITY`, scenario `236`: sport-mode 민감도 조정 검증
- `IT_017` `TC_CANOE_IT_017_AUDIO_VOLUME_POLICY`, scenario `215`: audio volume policy 반영 검증
- `IT_031` `TC_CANOE_IT_031_AUDIO_GUIDE_RUNTIME`, scenario `215`: emergency audio runtime 검증
- `RET_IT_021` `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY`, scenario `18 -> 12 -> 35`: retired umbrella row
- `IT_032` `TC_CANOE_IT_032_OUTPUT_FALLBACK`, scenario `18`: minimum warning channel 유지 검증
- `IT_033` `TC_CANOE_IT_033_DUPLICATE_POPUP_SUPPRESSION`, scenario `12`: duplicate popup suppression 검증
- `IT_034` `TC_CANOE_IT_034_CHANNEL_RESTORE`, scenario `35`: channel restore 검증
- `IT_035` `TC_CANOE_IT_EXT_035_DISTANCE_HISTORY`, scenario `222 + historyQuery(0)`: distance/history response 일관성 검증

### 3. Vehicle baseline and body integration

- `RET_IT_015` `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE`, scenario `216 -> 217`: retired umbrella row
- `IT_019` `TC_CANOE_IT_019_POWERTRAIN_PARKED_BASELINE`, scenario `216`: parked baseline 검증
- `IT_020` `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE`, scenario `217`: drive baseline 검증
- `RET_IT_016` `TC_CANOE_IT_BASE_002_CHASSIS_STATE`, scenario `218 -> 219 -> 237`: retired umbrella row
- `IT_021` `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE`, scenario `218`: steering baseline 검증
- `IT_022` `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE`, scenario `219`: brake baseline 검증
- `IT_023` `TC_CANOE_IT_023_CHASSIS_ACCEL_BASELINE`, scenario `237`: high-acceleration baseline 검증
- `RET_IT_017` `TC_CANOE_IT_BASE_024_BODY_STATE`, scenario `211 -> 216`: retired umbrella row
- `IT_024` `TC_CANOE_IT_BASE_024_BODY_STATE`, scenario `211`: hazard 반영 기준선 검증
- `IT_025` `TC_CANOE_IT_EXT_025_WINDOW_STATE`, scenario `226`: door/window 출력 일관성 검증
- `IT_026` `TC_CANOE_IT_BASE_026_BASIC_DISPLAY_UI`, scenario `220`: visual-first display mode 검증
- `RET_IT_019` `TC_CANOE_IT_BASE_027_COMFORT_CONTEXT / TC_CANOE_IT_BASE_030_BODY_SECURITY_CONTEXT`, scenario `229 / 203`: retired umbrella row
- `IT_027` `TC_CANOE_IT_BASE_027_COMFORT_CONTEXT`, scenario `229`: comfort context 출력 일관성 검증
- `IT_028` `TC_CANOE_IT_EXT_028_BODY_CONTROL_LOCK`, scenario `226`: body control lock/open 일관성 검증
- `IT_029` `TC_CANOE_IT_EXT_029_WIPER_RAIN_BASELINE`, scenario `229`: parked comfort baseline 검증
- `IT_030` `TC_CANOE_IT_BASE_030_BODY_SECURITY_CONTEXT`, scenario `203`: security-state boundary 유지 검증
