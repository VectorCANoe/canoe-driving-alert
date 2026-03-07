# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.27
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 기능을 노드 입력/처리/출력 관점으로 정리한다.
- 제출본은 상단 공식 노드 표를 유지하고, 하단은 대표 매핑만 유지한다.
- 전수 Req-Func 추적은 원문 0301에서 관리한다.
- ECU 명칭은 Canonical만 사용한다.
- Pre-Activation/Legacy 라벨은 원문과 동일하게 유지한다.

---

## 노드별 기능 명세 (공식 표준 양식)

| 노드 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Powertrain |
| ADAS_WARN_CTRL | 차량 주행 상태 기반 경고 조건 판정 및 제어 상태 생성 | 경고 시작/해제 제어 |
| ENG_CTRL | 시동 상태 입력을 엔진 동작 상태로 반영 | 차량 기본 동작 |
| TCM | 기어 입력(P/R/N/D) 상태 유지 및 전달 | 차량 기본 동작 |
|  |  | Chassis |
| ACCEL_CTRL | 가속 페달 입력 상태 처리 | 차량 기본 동작 |
| BRK_CTRL | 브레이크 페달 입력 상태 처리 | 차량 기본 동작 |
| STEER_CTRL | 조향 입력 상태 처리 | 차량 기본 동작 |
| EMS_ALERT | 긴급 알림 송수신 상태 및 해제 상태 관리 | 송신/수신/타임아웃 통합 단말 |
| WARN_ARB_MGR | 긴급 경고와 구간 경고 충돌 시 경보 우선순위 판정 및 감속 보조 요청/해제 수행 | Emergency > Zone, Ambulance > Police |
| VAL_SCENARIO_CTRL | SIL 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드(Validation-only) |
| VAL_BASELINE_CTRL | 차량 기본 기능 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드(Validation-only) |
|  |  | Network Infra |
| ETH_SW | Ethernet 백본 전달 인프라(시스템 관점) | 도메인 간 프레임 전달 경로 |
| CHS_GW | Chassis CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| INFOTAINMENT_GW | Infotainment CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| BODY_GW | 중재 결과 Ethernet 수신 후 Body CAN 출력 메시지 생성(HVAC/Seat/Mirror/Door/Wiper/Security 포함) | ETH->CAN 변환 |
| IVI_GW | 중재 결과 Ethernet 수신 후 Cluster CAN 출력 메시지 생성 | ETH->CAN 변환 |
| DOMAIN_ROUTER | 도메인 간 입력/출력 프레임 전달 경로 관리 | Gateway Routing |
| DOMAIN_BOUNDARY_MGR | 도메인 통신 경계 정책 유지 및 충돌 차단 | Boundary Control |
|  |  | Body |
| AMBIENT_CTRL | 중재 결과 기반 앰비언트 경고 패턴 적용 | 색상/패턴 반영 |
| HAZARD_CTRL | 비상등 On/Off 상태 처리 | 차량 기본 동작 |
| WINDOW_CTRL | 창문/도어/미러 상태 처리 | 차량 기본 동작 |
| DRV_STATE_MGR | 운전자/시트/보안 상태 입력 전달 | 차량 기본 동작 |
|  |  | Infotainment |
| NAV_CTX_MGR | 내비게이션 구간/방향/거리/제한속도 기반 컨텍스트 갱신 | 구간 상태 전환 |
| CLU_HMI_CTRL | 운전자 경고 문구/안내 및 오디오 상태 정보 표시 | 원인/방향/유형/오디오 상태 표시 |
| CLU_BASE_CTRL | 속도/기어/기본 상태 표시 | 차량 기본 동작 |
|  |  | Actual Device |
| Ambient Lights | 실제 앰비언트 장치가 제어 신호를 수신해 점등/패턴 동작 수행 | frmAmbientControlMsg(0x260) 반영 |
| Cluster Display | 실제 클러스터 장치가 경고 문구/상태를 표시 | frmClusterWarningMsg(0x280) 반영 |
| Navigation Panel | 사용자 입력(구간/방향/거리/제한속도) 제공 및 시각화 | Panel UI 입력 소스 |

- 시스템 아키텍처 관점에서 ETH_SW는 백본 전달 인프라로 정의한다.
- 구현 관점의 ETH_SW CAPL 역할(경로 헬스 모니터링)은 `04_SW_Implementation.md`에서 분리 관리한다.

---

## 기능 상세 요약 (제출본)

- 제출본은 상단 노드별 기능 명세를 기준으로 하단 상세/감사 표를 대표행 중심으로 축소한다.
- 전수 Req-Func 매핑은 원문 SoT(`driving-situation-alert/0301_SysFuncAnalysis.md`)를 기준으로 관리한다.

| Func ID | Req ID | 노드명 | 핵심 입력 | 핵심 처리 | 핵심 출력 |
|---|---|---|---|---|---|
| Func_001 | Req_001 | ADAS_WARN_CTRL | vehicleSpeed, driveState | 주행 조건 기반 경고 활성 | warningState |
| Func_007 | Req_007 | NAV_CTX_MGR | roadZone, navDirection, zoneDistance, speedLimit | 구간 컨텍스트 갱신 | baseZoneContext |
| Func_017 | Req_017 | EMS_ALERT | emergencyType, emergencyDirection, eta | 긴급 알림 송신 | ETH_EmergencyAlert |
| Func_022 | Req_022 | WARN_ARB_MGR | warningState, emergencyContext | 경보 우선순위 판정 | selectedAlertLevel, selectedAlertType |
| Func_035 | Req_035 | AMBIENT_CTRL | selectedAlertType, selectedAlertLevel | 긴급 시각표현 생성 | ambientMode, ambientColor, ambientPattern |
| Func_109 | Req_109 | CLU_BASE_CTRL | ClusterSpeed, ClusterGear, warningTextCode | 기본 표시 렌더 | ClusterStatus |
| Func_120 | Req_120 | ADAS_WARN_CTRL | emergencyDirection, eta, vehicleSpeed | 근접 위험도 산정 | proximityRiskLevel |
| Func_125 | Req_125 | WARN_ARB_MGR | decelAssistReq, selectedAlertLevel | 긴급 최우선 유지 | selectedAlertLevel |
| Func_130 | Req_130 | ADAS_WARN_CTRL | objectTrackValid, objectRange, objectRelSpeed | 객체 위험 입력 처리 | objectRiskClass |
| Func_140 | Req_140 | WARN_ARB_MGR | TurnLampState, selectedAlertLevel | 방향지시등 연동 정책 | selectedAlertType |
| Func_148 | Req_148 | ADAS_WARN_CTRL | objectTrackValid, objectConfidence | 입력 유효성/신뢰도 필터링 | objectRiskClass, selectedAlertLevel |

## Req-Func 대표 매핑 (N:M 축소본)

| Req ID | Func ID | 실제 노드명 | 기능명 |
|---|---|---|---|
| Req_001 | Func_001 | ADAS_WARN_CTRL | 주행시 경고엔진 활성 |
| Req_003 | Func_003 | ADAS_WARN_CTRL | 경고 시작 트리거 |
| Req_017 | Func_017, Func_018 | EMS_ALERT | 긴급차량 접근 경고 송신 |
| Req_027 | Func_027 | WARN_ARB_MGR | 충돌중재 적용 |
| Req_035 | Func_035, Func_036 | AMBIENT_CTRL | 긴급 색상/패턴 정책 |
| Req_101 | Func_101 | ENG_CTRL | 시동 기본 기능 |
| Req_106 | Func_106 | HAZARD_CTRL | 비상등 기본 제어 |
| Req_109 | Func_109 | CLU_BASE_CTRL | 클러스터 기본 표시 |
| Req_120 | Func_120 | ADAS_WARN_CTRL | 긴급차량 근접 위험 판단 |
| Req_125 | Func_125, Func_126 | WARN_ARB_MGR | 감속 보조 시 경고 동기화 |
| Req_130 | Func_130, Func_131 | ADAS_WARN_CTRL | 객체 위험 입력/판정(Pre-Activation) |
| Req_148 | Func_148 | ADAS_WARN_CTRL | 경고 입력 유효성/신뢰도 보호(Pre-Activation) |

## 대표 체인 샘플 (제출 보강)

| Req ID | Func ID | Flow ID | Comm ID | Var ID(핵심) | Code Ref | Test Link |
|---|---|---|---|---|---|---|
| Req_001 | Func_001 | Flow_001 | Comm_001 | Var_012(vehicleSpeedNorm), Var_013(driveStateNorm) | MOD_01.F001 | UT_ADAS_001 |
| Req_017 | Func_017 | Flow_004 | Comm_004 | Var_007(emergencyType), Var_009(eta) | MOD_03.F017 | UT_EMS_POL_001 |
| Req_022 | Func_022 | Flow_006 | Comm_006 | Var_017(emergencyContext), Var_018(selectedAlertLevel) | MOD_06.F022 | UT_ARB_001 |
| Req_035 | Func_035 | Flow_007 | Comm_007 | Var_019(selectedAlertType), Var_022(ambientColor) | MOD_11.F035 | UT_BCM_001 |
| Req_120 | Func_120 | Flow_120 | Comm_120 | Var_320(proximityRiskLevel) | MOD_01.F120 | UT_V2_RISK_001 |
| Req_130 | Func_130 | Flow_130 | Comm_130 | Var_330(objectTrackValid), Var_331(objectRange) | MOD_01.F130 | UT_ADAS_OBJ_RISK_001 (Planned) |

---
