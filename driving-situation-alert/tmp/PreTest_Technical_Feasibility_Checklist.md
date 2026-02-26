# 사전 기술 가능범위 확인 체크리스트 (Pre-Test Feasibility)

## 1. 목적
- 본 문서는 `05/06/07` 테스트 문서 본작성 전에, 현재 옵션1 아키텍처에서 CANoe SIL로 실제 검증 가능한 범위를 확정하기 위한 체크리스트다.
- 대상 아키텍처: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어`.

## 2. 적용 범위
- In Scope: CAN + Ethernet(UDP), CANoe SIL, 가상 노드 기반 검증.
- Out of Scope: 실차 RF 전파 특성, 실제 OBU/TCU 물리 통신, OTA/UDS/DoIP, HIL 장비.

## 3. 사전 조건
- `00b_Project_Scope.md`, `01_Requirements.md`, `03~0304`, `04_SW_Implementation.md` 최신본 반영.
- 노드/Flow/Comm/Var ID 동기화 완료.
- CANoe Trace, Logging, Panel, Test Module 사용 가능 상태.

## 4. 기술 가능범위 체크리스트

| Check ID | 영역 | 확인 항목 | 수행 방법 (CANoe SIL) | 합격 기준 | 추적 키 | 결과 |
|---|---|---|---|---|---|---|
| FZ_001 | Ethernet 전달 | EMS 브로드캐스트가 다중 수신 노드에 정상 분배되는가 | EMS_POLICE_TX/EMS_AMB_TX 송신 후 EMS_ALERT_RX/관련 노드 수신 trace 확인 | 수신 대상 노드 누락 0건 | Flow_004~006, Comm_004~006 | Pending |
| FZ_002 | CAN->ETH 변환 | CHASSIS_GW/INFOTAINMENT_GW 변환값이 원본 CAN과 일치하는가 | 0x100/0x101/0x110 입력 대비 ETH payload 비교 | 필드 오차 0, 주기 100ms 유지 | Flow_001~003, Comm_001~003 | Pending |
| FZ_003 | ETH->CAN 변환 | BODY_GW/IVI_GW 출력 CAN이 중재 결과와 일치하는가 | selectedAlert 수신 후 0x210/0x220 출력 프레임 비교 | 변환 누락/오매핑 0 | Flow_007~008, Comm_007~008 | Pending |
| FZ_004 | 주기 성능 | 100ms/50ms 주기가 안정적으로 유지되는가 | Trace timestamp로 period/jitter 측정 | 설정 주기 대비 허용오차 내(팀 기준) | Req_024, Flow 전반 | Pending |
| FZ_005 | 타임아웃 | 긴급신호 무갱신 1000ms 후 clear가 정확히 동작하는가 | 송신 중단 후 timeoutClear, emergencyContext 확인 | 1000ms 조건 충족 시 clear 1회 발생 | Req_024, Func_024, Var_020/027 | Pending |
| FZ_006 | 중재 규칙 1 | Emergency > Navigation 우선순위가 보장되는가 | Nav 활성 + EMS 활성 동시 주입 | 출력이 Emergency 컨텍스트로 고정 | Req_022, Func_022/027 | Pending |
| FZ_007 | 중재 규칙 2 | Ambulance > Police 규칙이 보장되는가 | 동일 시점 Police/Ambulance 동시 주입 | Ambulance 선택 | Req_028/029, Func_028/029 | Pending |
| FZ_008 | 중재 규칙 3 | ETA/SourceID 동률 해소 규칙이 보장되는가 | 동일 등급 다중 알림 입력(ETA/SourceID 변경) | 규칙 순서대로 동일 결과 재현 | Req_030/031, Func_030/031 | Pending |
| FZ_009 | 상태 복귀 | 긴급 해제 후 이전 Nav 컨텍스트로 정상 복귀하는가 | Active -> Clear/Timeout 시퀀스 실행 | 복귀 지연/누락 없음 | Req_033/034, Func_033/034 | Pending |
| FZ_010 | 출력 일관성 | Ambient/Cluster 출력이 동일 AlertContext를 공유하는가 | 동일 입력에서 0x210/0x220 동시 관찰 | 출력 간 모순 0건 | Flow_007/008, Var_018/019 | Pending |
| FZ_011 | 실패 안전 | 입력 invalid/누락 시 fail-safe가 동작하는가 | invalid 값 주입/프레임 누락 시나리오 실행 | 정의된 기본값/강등 동작 확인 | 04 문서 8장 예외 규칙 | Pending |
| FZ_012 | 로그/재현성 | 동일 시나리오 반복 시 결과가 재현되는가 | 10회 반복 실행 로그 비교 | 판정 결과 100% 동일 | SIL_TEST_CTRL, Req_041~043 | Pending |

## 5. 결과 판정 규칙
- `Go`: FZ_001~FZ_012 전부 Pass -> `05_Unit_Test.md` 본작성 진행.
- `Conditional Go`: 필수 항목(FZ_001, 003, 005, 006, 007, 008, 009) Pass + 나머지 경미 이슈는 보완계획 첨부.
- `No Go`: 필수 항목 중 1개라도 Fail -> 04 구현/0302~0304 추적 갱신 후 재시험.

## 6. 산출물(증적) 목록
- CANoe Trace 캡처 (`.asc`/스크린샷)
- Logging 블록 결과 파일
- 테스트 시나리오 입력값 테이블
- FZ 체크 결과표 (Pass/Fail, 원인, 조치)

## 7. 05/06/07 연계 가이드
- `05_Unit_Test.md`: FZ에서 모듈 단위로 분해 가능한 항목을 UT ID로 전개.
- `06_Integration_Test.md`: GW 변환/중재/복귀 체인을 IT 시나리오로 전개.
- `07_System_Test.md`: Req 단위 E2E로 최종 수용 기준 정의.
