# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.1
**Date**: 2026-02-25
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템

---

## 기능 정의 원칙

- 본 문서는 요구사항(01)의 What을 노드 기능(How)으로 분해한다.
- Panel은 테스트 자극/관측 인터페이스이며 기능 주체 ECU로 보지 않는다.
- 기능 ID는 `Func_001~Func_043`로 요구사항 ID와 1:1 대응한다.
- DBC 단계에서 OEM 네이밍으로 변경 가능하며, 기능 ID/추적 ID는 유지한다.

---

## 기능-요구사항 1:1 매핑

| Func ID | Req ID | 기능명 | 담당 노드 | 기능 설명 |
|---|---|---|---|---|
| Func_001 | Req_001 | 주행시 경고엔진 활성 | ADAS_WARN_CTRL | 주행 상태에서 경고 판단 엔진 활성화 |
| Func_002 | Req_002 | 비주행 경고 억제 | ADAS_WARN_CTRL | 정차/비주행 상태에서 경고 출력 억제 |
| Func_003 | Req_003 | 경고 시작 트리거 | ADAS_WARN_CTRL | 경고 조건 성립 시 출력층 활성 시작 |
| Func_004 | Req_004 | 경고 종료 트리거 | ADAS_WARN_CTRL | 해제 조건 성립 시 출력층 종료 |
| Func_005 | Req_005 | 경고 원인 전달 | CLU_HMI_CTRL | 경고 원인 텍스트 표시 |
| Func_006 | Req_006 | 반복 경고 디바운스 | ADAS_WARN_CTRL | 동일 경고 재출력 간격 제어 |
| Func_007 | Req_007 | 구간값 변경 반영 | NAV_CONTEXT_MGR | gRoadZone 변경 시 구간 상태 갱신 |
| Func_008 | Req_008 | 일반구간 정책 적용 | BCM_AMBIENT_CTRL | 일반 구간 기본 패턴 적용 |
| Func_009 | Req_009 | 스쿨존 강화 경고 | BCM_AMBIENT_CTRL | 스쿨존 전용 강화 패턴 적용 |
| Func_010 | Req_010 | 스쿨존 과속 경고 | ADAS_WARN_CTRL | 스쿨존 속도 초과 이벤트 판정 |
| Func_011 | Req_011 | 고속 장시간 무조향 감지 | ADAS_WARN_CTRL | 고속 구간 무조향 타이머 경고 |
| Func_012 | Req_012 | 무조향 경고 해제 | ADAS_WARN_CTRL | 조향 입력 복귀 시 경고 해제 |
| Func_013 | Req_013 | 유도구간 진입 전환 | BCM_AMBIENT_CTRL | 유도구간 진입 시 방향안내 모드 전환 |
| Func_014 | Req_014 | 좌우 방향 구분 표시 | BCM_AMBIENT_CTRL | gNavDirection 기준 좌/우 패턴 분기 |
| Func_015 | Req_015 | 구간 전환 완화 | BCM_AMBIENT_CTRL | 전환 중 점멸 튐 현상 완화 |
| Func_016 | Req_016 | 구간경고 종료 복귀 | BCM_AMBIENT_CTRL | 조건 해제 시 기본 구간 패턴 복귀 |
| Func_017 | Req_017 | 경찰 접근 경고 송신 | EMS_POLICE_TX | 경찰 긴급 ACTIVE 알림 송신 |
| Func_018 | Req_018 | 구급 접근 경고 송신 | EMS_AMB_TX | 구급 긴급 ACTIVE 알림 송신 |
| Func_019 | Req_019 | 긴급차량 종류 표시 | CLU_HMI_CTRL | 경찰/구급 타입 구분 표시 |
| Func_020 | Req_020 | 긴급차량 방향 표시 | CLU_HMI_CTRL | 접근 방향 정보 표시 |
| Func_021 | Req_021 | 양보 유도 메시지 | CLU_HMI_CTRL | 양보 요청 고정 메시지 표시 |
| Func_022 | Req_022 | 긴급경고 우선 출력 | WARN_ARB_MGR | 일반 안내보다 긴급경고 우선 적용 |
| Func_023 | Req_023 | 종료 신호 처리 | EMS_ALERT_RX | CLEAR 수신 시 긴급경고 종료 |
| Func_024 | Req_024 | 타임아웃 보호해제 | EMS_ALERT_RX | 1000ms 무갱신 시 안전 해제 |
| Func_025 | Req_025 | 다중긴급 단일선택 | WARN_ARB_MGR | 동시 긴급 신호 중 1개 선택 |
| Func_026 | Req_026 | 중복 팝업 억제 | CLU_HMI_CTRL | 동일 긴급 이벤트 중복 팝업 억제 |
| Func_027 | Req_027 | 충돌중재 개시 | WARN_ARB_MGR | 구간/긴급 동시 발생 시 중재 시작 |
| Func_028 | Req_028 | 긴급>구간 우선 적용 | WARN_ARB_MGR | 긴급 시 구간 패턴 오버라이드 |
| Func_029 | Req_029 | 구급>경찰 우선 적용 | WARN_ARB_MGR | EmergencyType 우선순위 적용 |
| Func_030 | Req_030 | ETA 우선 적용 | WARN_ARB_MGR | 동급 알림이면 ETA 최소값 선택 |
| Func_031 | Req_031 | SourceID 동률판정 | WARN_ARB_MGR | ETA 동률 시 SourceID 오름차순 |
| Func_032 | Req_032 | 중재결과 결정론 보장 | WARN_ARB_MGR | 동일 입력이면 동일 결과 출력 |
| Func_033 | Req_033 | 종료후 이전상태 복원 | BCM_AMBIENT_CTRL | 긴급 종료 후 직전 구간 상태 복원 |
| Func_034 | Req_034 | 전환 깜빡임 완화 | BCM_AMBIENT_CTRL | 중재 전환 시 패턴 안정화 |
| Func_035 | Req_035 | 긴급 색상 정책 | BCM_AMBIENT_CTRL | 긴급 색상 팔레트 고정 적용 |
| Func_036 | Req_036 | 긴급 패턴 정책 | BCM_AMBIENT_CTRL | 긴급 점등 패턴 고정 적용 |
| Func_037 | Req_037 | 스쿨존 패턴 정책 | BCM_AMBIENT_CTRL | 스쿨존 패턴 고정 적용 |
| Func_038 | Req_038 | 고속도로 패턴 정책 | BCM_AMBIENT_CTRL | 고속 경고 패턴 고정 적용 |
| Func_039 | Req_039 | 유도선 패턴 정책 | BCM_AMBIENT_CTRL | 좌/우 유도 패턴 고정 적용 |
| Func_040 | Req_040 | 문구 길이 제한 | CLU_HMI_CTRL | 경고 문구 길이/형식 고정 |
| Func_041 | Req_041 | SIL 시나리오 실행 | SIL_TEST_CTRL | CANoe SIL에서 시나리오 실행 제어 |
| Func_042 | Req_042 | CAN+ETH 동시 검증 | SIL_TEST_CTRL | CAN/Ethernet 동시 조건 검증 |
| Func_043 | Req_043 | 판정 결과 산출 | SIL_TEST_CTRL | 시나리오 Pass/Fail 판정 출력 |

---

## DBC 리네이밍 가이드 (Old -> New)

> 목적: 현재 논리 노드명을 유지한 채, DBC 생성 단계에서 현업형 ECU 명칭으로 치환하기 위한 기준표

| Old (현재 문서) | New (DBC 권장) | 비고 |
|---|---|---|
| WDM_ECU | ADAS_WARN_CTRL | 경고 판단/중재 통합 제어 노드 |
| Context_Manager | NAV_CONTEXT_MGR | 네비 구간/방향 컨텍스트 처리 |
| Arbiter | WARN_ARB_MGR | 우선순위/충돌해결 전담 |
| Police_Node | EMS_POLICE_TX | 긴급 알림 송신 노드(경찰) |
| Ambulance_Node | EMS_AMB_TX | 긴급 알림 송신 노드(구급) |
| Civ_Node | EMS_ALERT_RX | 긴급 알림 수신/해제 처리 노드 |
| Ambient_ECU | BCM_AMBIENT_CTRL | 앰비언트 제어 노드 |
| Cluster_ECU | CLU_HMI_CTRL | 클러스터 경고 표시 노드 |
| Test_Controller | SIL_TEST_CTRL | CANoe SIL 테스트 제어 노드 |

신규 기능(팀 정의) 명명 원칙:
- `도메인_기능_역할` 형식 사용
- 약어는 대문자 + 밑줄(`_`) 사용
- 메시지/신호명은 SAE/Vector 스타일(`Msg_Signal`)로 일관 유지

리네이밍 동시 반영 범위:
1. `0302_NWflowDef.md` 송신/수신 노드명
2. `0303_Communication_Specification.md` 메시지 송수신 주체 설명
3. `0304_System_Variables.md` Description/연결 노드 표기
4. `04_SW_Implementation.md` CAPL 노드 파일/핸들러 이름
5. `05/06/07` 테스트 절차의 노드 참조명
6. DBC 노드명/메시지 송신자 정보

규칙:
- 이름은 바꿔도 `Req_###`, `Func_###`, `Flow_###`, `Comm_###`, `Var_###` 식별자는 바꾸지 않는다.
- 리네이밍은 기능 변경이 아니라 식별자 치환 작업으로 관리한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.0 | 2026-02-25 | Req_001~Req_043 기준으로 Func_001~Func_043 1:1 매핑 전면 재작성 |
| 3.1 | 2026-02-25 | 노드명 일괄 치환(현업형 DBC 네이밍) 및 DBC 리네이밍 가이드 하단 이동 |
