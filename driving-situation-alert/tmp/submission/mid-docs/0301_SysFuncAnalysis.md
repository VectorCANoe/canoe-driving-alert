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

## 작성 원칙

- 본 문서는 기능을 노드 입력/처리/출력 관점으로 정리한다.
- 심사자가 기능 책임 분리를 빠르게 확인할 수 있도록 표 구조를 유지한다.
- 세부 운영 메모보다 기능 목적과 출력 결과 설명을 우선한다.

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

## 기능군 요약

| 기능군 | 핵심 노드 | 입력 | 출력 |
|---|---|---|---|
| 주행/구간 경고 판단 | ADAS_WARN_CTRL, NAV_CTX_MGR | 차량 상태, 조향, 구간 컨텍스트 | warningState, baseZoneContext |
| 긴급 알림 처리 | EMS_ALERT | 긴급차량 타입/방향/ETA | emergencyContext, 긴급 알림 프레임 |
| 경보 우선순위 판정 | WARN_ARB_MGR | 구간 경고 + 긴급 경고 | selectedAlertLevel, selectedAlertType |
| 출력 제어 | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | 최종 경보 컨텍스트 | 앰비언트 패턴/클러스터 문구 |
| 기본 차량/검증 | ENG_CTRL, TCM, ACCEL_CTRL, BRK_CTRL, STEER_CTRL, VAL_* | 기본 차량 상태 및 시나리오 입력 | 기본 상태 표시 및 시나리오 판정 |
