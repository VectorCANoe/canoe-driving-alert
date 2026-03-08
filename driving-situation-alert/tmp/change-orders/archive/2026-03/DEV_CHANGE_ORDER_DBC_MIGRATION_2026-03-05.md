# 개발팀 전달서 (잔여 항목): 경계 ECU 멀티노드 점검/정합

문서 ID: DEV-CO-DBC-20260305-R3  
작성일: 2026-03-07  
작성 주체: 문서작성팀  
대상: CANoe 개발팀

## 0. 문서 목적

- 본 문서는 완료된 과거 이슈를 제외하고, 현재 남은 **경계 ECU 멀티노드 정합** 항목만 전달한다.
- 핵심 목적은 문서 SoT(`0302/0303/ETH_INTERFACE_CONTRACT`)와 CANoe 런타임 채널 결선 상태를 일치시키는 것이다.

## 1. 현재 고정 구조(변경 금지)

1. 옵션1 아키텍처 고정:
- `도메인 CAN -> GW/Router -> ETH_Backbone -> GW/Router -> 대상 도메인 CAN`
2. 경계 노드 기본 멀티채널(필수):
- `CHS_GW`, `BODY_GW`, `INFOTAINMENT_GW`, `IVI_GW`, `DOMAIN_ROUTER`
3. 단일 도메인 노드는 멀티채널 대상 아님:
- `ADAS_WARN_CTRL`, `WARN_ARB_MGR`, `ENG_CTRL`, `TCM`, `ACCEL_CTRL`, `BRK_CTRL`, `STEER_CTRL`, `AMBIENT_CTRL`, `CLU_HMI_CTRL` 등

## 2. 개발팀 반영 필요 항목 (In Scope)

1. 멀티채널 결선 실측 점검 (GUI 기준)
- 대상 노드:
  - `CHS_GW`: ch1 + ch5
  - `BODY_GW`: ch2 + ch5
  - `INFOTAINMENT_GW`: ch3 + ch5
  - `IVI_GW`: ch3 + ch5
  - `DOMAIN_ROUTER`: ch4 + ch5
- 확인 기준:
  - CANoe Node Properties > Channel Assignments에서 2개 채널 동시 바인딩
  - 런타임 측정 시 양 채널 Rx/Tx 이벤트 확인

2. 추가 멀티노드 후보 확정
- `DOMAIN_BOUNDARY_MGR`:
  - 현재 코드상 `frmChassisHealthMsg / frmBodyHealthMsg / frmInfotainmentHealthMsg` 직접 수신 + `ethFailSafeStateMsg` 송신 구조이므로 멀티채널 운영 여부를 명시 결정한다.
  - 권고: `ch1/ch2/ch3/ch5` 멀티채널 또는 백본 수집 경로로 단일화(둘 중 하나로 구조 고정).
- `VAL_SCENARIO_CTRL`:
  - 현재 다도메인 주입 하네스 역할(`frmVehicleStateCanMsg`, `frmNavContextCanMsg`, `frmIgnitionEngineMsg`, `ethObjectRiskInputMsg`)을 수행하므로 채널 운영 정책을 명시 결정한다.
  - 권고: 하네스 정책에 따라 `ch1/ch3/ch4/ch6(+ch5)` 멀티 또는 현행 단일+브리지 유지 중 택일 후 문서화.

3. 문서/코드 정합 고정
- 결정 결과를 아래에 동기화:
  - `canoe/cfg/channel_assign/README.md` (멀티채널 표)
  - `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md` (Sender/경로 설명)
  - 필요 시 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` 주석
- `0302/0303`의 Flow/Comm 경로 해석과 모순 0건 유지

## 3. 변경 제외 (Out of Scope)

- 기능 로직 변경(TTC/중재/Fail-safe 임계값 변경)
- 신규 요구사항/시나리오 증설
- RTE/ECU 명명 정책 변경

## 4. 수용 기준 (Acceptance)

1. 멀티노드 정합
- 필수 5개 경계 노드의 이중 채널 바인딩 확인 완료
- `DOMAIN_BOUNDARY_MGR`, `VAL_SCENARIO_CTRL` 운영 정책(멀티/단일)이 문서로 명시 완료

2. 실행 동등성
- 핵심 회귀 결과 유지:
  - 무조향 경고
  - 긴급 경고/중재
  - V2 fail-safe

3. 추적성
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 단절 0건

## 5. 개발팀 제출물

1. 변경 파일 목록(README/operations 문서, 필요 시 cfg 스냅샷 포함)
2. 채널 바인딩 확인 캡처(각 멀티노드 1장 이상)
3. `DOMAIN_BOUNDARY_MGR`, `VAL_SCENARIO_CTRL` 운영정책 결정 메모
4. 핵심 회귀 결과 요약 + 기준 커밋 해시

## 6. 전달 메모

- 본 전달은 신규 개발 지시가 아니라 **경계 ECU 결선 정합 마감 지시**다.
- ETH 라이선스 취득 후 실제 Ethernet 전환 시에도 동일 구조(경계 노드 멀티 결선 원칙)를 유지한다.
