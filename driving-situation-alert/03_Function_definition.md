# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 4.37
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 작성 원칙

- 본 문서는 요구사항(01)의 What을 노드 기능(How)으로 분해한다.
- 상단 표는 표준 양식 구조만 유지하고, 상세 추적 정보는 하단 표에 분리한다.
- Panel은 테스트 자극/관측 인터페이스이며 기능 주체 ECU로 보지 않는다.
- `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`는 Validation Harness(검증 전용)로만 취급하며, 제품 ECU 인벤토리와 분리해 표기한다.
- 통합 기본요구사항 구간은 기능 ID `Func_001~Func_043`을 기준으로 요구사항 ID(`Req_001~Req_043`)와 누락 없는 추적 커버리지(N:M 허용)를 유지한다.
- 차량 기본 기능 확장 요구(`Req_101~Req_107`, `Req_109~Req_119`)는 `Func_101~Func_107`, `Func_109~Func_119`로 별도 관리한다.
- V2 확장 요구(`Req_120~Req_121`, `Req_123`, `Req_125~Req_129`)는 `Func_120~Func_121`, `Func_123`, `Func_125~Func_129`로 별도 관리하며, 본 문서에서는 구현 활성 상태로 유지한다.
- ADAS 객체 인지 확장 요구(`Req_130~Req_139`)는 `Func_130~Func_139`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 차량 경보 편의 확장 요구(`Req_140~Req_147`)는 `Func_140~Func_147`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 경고 강건성·인지성 확장 요구(`Req_148~Req_155`)는 `Func_148~Func_155`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 제출 전 현대/기아 및 OEM 기준 명칭으로 일괄 대체하되, 기능 ID/추적 ID는 유지한다.
- ID 규칙 SoT는 `00f_CAN_ID_Allocation_Standard.md`를 따르며, 적용 참조는 `0303_Communication_Specification.md`를 사용한다.
- ECU 명칭은 Canonical(`UPPER_SNAKE_CASE`)만 사용하며, 명명 규칙은 `00e`를 단일 SoT로 하고 본 문서는 ECU 적용 참조 문서로 유지한다.
- RTE 생성명 규칙은 `00g_RTE_Name_Mapping_Standard.md`를 SoT로 하고, 본 문서가 아닌 `04`에서 적용한다.
- OEM100 Surface ECU 전체 전수(100개)와 구현 상태(`활성/미구현`)는 `00e` 6.4를 단일 기준으로 사용한다.
- 본 문서는 활성(상세 정의) Surface ECU만 `Func` 상세를 부여하고, 미구현(Placeholder) Surface ECU는 이름/상태만 유지한다.
- 네트워크 구현은 옵션1 아키텍처를 고정 적용한다: `ETH_SW + CHS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `WARN_ARB_MGR`의 기능은 경보 우선순위 판정이며, CAN 비트 레벨 arbitration과 구분해 해석한다.
- EMS는 문서 상위 계층에서 단일 논리 단말 `EMS_ALERT`로 정의하고, 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`)은 하단 매핑표에서만 분리 관리한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- 본 사이클의 기능-요구 추적 범위는 `Req_001~043`, `Req_101~107`, `Req_109~121`, `Req_123`, `Req_125~129`를 활성 범위로 유지하고, `Req_130~Req_155`는 확장 요구(Pre-Activation) 범위로 관리한다.

---

## 기능 정의 표 (공식 표준 양식)

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|---|---|---|---|---|
| 입력 | 구간 정보 | 구간 상태 입력(일반/스쿨존/고속/유도) | 패널에서 값을 입력한다. | 구간 전환 시 경고 기준 반영 확인 |
| 입력 | 유도 방향 | 유도 구간 방향 입력(좌/우) | 패널에서 값을 입력한다. | 좌우 방향 표시 반영 확인 |
| 입력 | 구간 거리 | 구간 거리 입력 | 패널에서 값을 조절한다. | 거리 변화 반영 확인 |
| 입력 | 제한 속도 | 현재 구간 제한속도 입력 | 차량 입력 또는 패널 입력을 사용한다. | 제한속도 변경 반영 확인 |
| 입력 | 차량 속도 | 차량 속도 입력 | 차량 입력 또는 패널 입력을 사용한다. | 속도 변화에 따른 경고 반영 확인 |
| 입력 | 조향 입력 | 조향 입력 여부 입력 | 차량 입력 또는 패널 입력을 사용한다. | 조향 입력에 따른 경고 해제 확인 |
| 입력 | 경찰 긴급 활성 | 경찰 긴급 활성 상태 입력 | 패널에서 켜고 끈다. | 경찰 긴급 경고 발생과 해제 확인 |
| 입력 | 경찰 ETA | 경찰 도달예상시간 입력 | 패널에서 값을 조절한다. | 경찰 ETA 우선순위 반영 확인 |
| 입력 | 경찰 방향 | 경찰 접근 방향 입력 | 패널에서 방향을 선택한다. | 경찰 접근 방향 표시 확인 |
| 입력 | 구급 긴급 활성 | 구급 긴급 활성 상태 입력 | 패널에서 켜고 끈다. | 구급 긴급 경고 발생과 해제 확인 |
| 입력 | 구급 ETA | 구급 도달예상시간 입력 | 패널에서 값을 조절한다. | 구급 ETA 우선순위 반영 확인 |
| 입력 | 구급 방향 | 구급 접근 방향 입력 | 패널에서 방향을 선택한다. | 구급 접근 방향 표시 확인 |
| 출력 | 앰비언트 제어 | 구간/긴급 상태에 따른 앰비언트 출력 | 경고 판단 결과를 차체 출력으로 전달한다. | 앰비언트 출력이 상황에 맞게 동작하는지 확인 |
| 출력 | 클러스터 경고 | 경고 문구 및 상태 출력 | 경고 판단 결과를 클러스터 표시로 전달한다. | 경고 문구와 방향 표시 확인 |
| 출력 | 경찰 알림 송신 | 경찰 긴급 알림 송신 | 긴급 알림을 외부로 송신한다. | 경찰 긴급 알림 송신 확인 |
| 출력 | 구급 알림 송신 | 구급 긴급 알림 송신 | 긴급 알림을 외부로 송신한다. | 구급 긴급 알림 송신 확인 |
| ECU 동작 | 구간 컨텍스트 관리 | 구간/제한속도 입력을 바탕으로 컨텍스트 갱신 | 입력 변화에 따라 상태를 갱신한다. | 구간 정보 갱신 확인 |
| ECU 동작 | 경고 조건 판정 | 속도/조향/제한속도 기반 경고 조건 판정 | 경고 발생 조건을 계산한다. | 과속 및 무조향 경고 판단 확인 |
| ECU 동작 | 경찰 알림 송신 제어 | 경찰 알림 송신 주기 관리 | 송신 주기와 상태를 관리한다. | 경찰 긴급 알림 주기 유지 확인 |
| ECU 동작 | 구급 알림 송신 제어 | 구급 알림 송신 주기 관리 | 송신 주기와 상태를 관리한다. | 구급 긴급 알림 주기 유지 확인 |
| ECU 동작 | 긴급 알림 수신 처리 | 긴급 알림 수신/해제 처리 | 수신 상태와 해제 동작을 관리한다. | 수신, 해제, 타임아웃 동작 확인 |
| ECU 동작 | 경보 우선순위 판정 | 긴급/구간 충돌 시 우선순위 결정 | 우선순위를 반영한 경고 결과를 정한다. | 우선순위와 ETA 규칙 확인 |
| ECU 동작 | 앰비언트 제어 | 경고 패턴/색상 적용 | 앰비언트 색상과 패턴을 정한다. | 앰비언트 출력이 상황에 맞게 동작하는지 확인 |
| ECU 동작 | 클러스터 표시 | 경고 문구/유형 표시 | 문구와 방향 표시를 정한다. | 클러스터 표시 동작 확인 |
| ECU 동작 | 엔진 기본 제어 | 시동 입력 기반 엔진 상태 반영 | 차량 기본 기능 | 시동 상태 반영 확인 |
| ECU 동작 | 변속 기본 제어 | 기어 입력(P/R/N/D) 상태 반영 | 차량 기본 기능 | 기어 상태 반영 확인 |
| ECU 동작 | 가속 기본 제어 | 가속 입력 상태 반영 | 차량 기본 기능 | 가속 상태 반영 확인 |
| ECU 동작 | 제동 기본 제어 | 브레이크 입력 상태 반영 | 차량 기본 기능 | 제동 상태 반영 확인 |
| ECU 동작 | 조향 기본 제어 | 조향 입력 상태 반영 | 차량 기본 기능 | 조향 상태 반영 확인 |
| ECU 동작 | 비상등 기본 제어 | 비상등 On/Off 상태 반영 | 차량 기본 기능 | 비상등 상태 반영 확인 |
| ECU 동작 | 창문 기본 제어 | 창문 개폐 상태 반영 | 차량 기본 기능 | 창문 상태 반영 확인 |
| ECU 동작 | 클러스터 기본 표시 | 속도/기어/경고 기본 표시 반영 | 차량 기본 기능 | 기본 표시 반영 확인 |
| ECU 동작 | 도메인 게이트웨이 전달 | 도메인 경계 기반 메시지 전달 | 차량 기본 기능 | 도메인 간 전달 동작 확인 |
| ECU 동작 | 도메인 경계 유지 | 도메인 통신 경계/정책 유지 | 차량 기본 기능 | 도메인 경계 상태 유지 확인 |
| ECU 동작 | 공조 상태 반영 | DATC 상태/제어 신호 반영 | 차량 기본 기능 | 공조 상태 반영 확인 |
| ECU 동작 | 시트 상태 반영 | 시트 상태/제어 신호 반영 | 차량 기본 기능 | 시트 상태 반영 확인 |
| ECU 동작 | 미러 상태 반영 | 미러 상태 신호 반영 | 차량 기본 기능 | 미러 상태 반영 확인 |
| ECU 동작 | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태 반영 | 차량 기본 기능 | 도어 제어 상태 반영 확인 |
| ECU 동작 | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태 반영 | 차량 기본 기능 | 와이퍼와 우적 상태 반영 확인 |
| ECU 동작 | 보안 상태 반영 | 이모빌라이저/경보 상태 반영 | 차량 기본 기능 | 보안 상태 반영 확인 |
| ECU 동작 | 오디오 상태 반영 | 오디오, 음성안내, TTS 상태 반영 | 차량 기본 기능 | 오디오 상태 반영 확인 |
| ECU 동작 | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 위험도 산정 | 긴급차량 확장 기능 | 긴급차량 위험도 판단 확인 |
| ECU 동작 | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | 긴급차량 확장 기능 | 감속 보조 요청 발생 확인 |
| ECU 동작 | 감속 보조 시 긴급경고 최우선 유지 | 감속 보조 활성 시 긴급 경고가 비긴급 경고보다 우선 유지 | 긴급차량 확장 기능 | 긴급 경고 우선 유지 확인 |
| ECU 동작 | 감속 보조 시 경고 채널 동기화 | 감속 보조 활성 시 앰비언트와 클러스터 출력 동기화 유지 | 긴급차량 확장 기능 | 경고 표시 동기화 확인 |
| ECU 동작 | 운전자 개입 우선 해제 | 제동/조향 회피 입력 시 감속 보조 요청 즉시 해제 | 긴급차량 확장 기능 | 운전자 개입 시 해제 동작 확인 |
| ECU 동작 | 도메인 단절 시 자동감속 금지 | 도메인 경로 단절 시 자동 감속 보조 요청 생성 금지 | 긴급차량 확장 기능 | 도메인 단절 시 자동 감속 금지 확인 |
| ECU 동작 | 도메인 단절 시 최소 경고 유지 | 도메인 경로 단절 시 최소 경고 채널 유지 | 긴급차량 확장 기능 | 도메인 단절 시 최소 경고 유지 확인 |
| ECU 동작 | 도메인 단절 시 안전 강등 전환 | 도메인 경로 단절 시 안전 강등 상태 전환 | 긴급차량 확장 기능 | 도메인 단절 시 안전 강등 전환 확인 |
| ECU 동작 | 객체 목록 수용/위험 객체 선정 | 주변 객체 목록 수신 후 대표 위험 객체를 선정 | 객체 인지 확장 기능(계획) | 대표 위험 객체 선정 확인 |
| ECU 동작 | TTC/상대속도 기반 위험 단계화 | TTC/상대속도/거리 기반으로 위험 단계를 산정하고 보수 유지시간을 적용 | 객체 인지 확장 기능(계획) | 객체 위험 단계화 확인 |
| ECU 동작 | 교차로/합류 위험 경고 판정 | 교차로 측방 접근 및 합류/끼어들기 위험 경고를 생성하고 기존 경고와 정합 판정 | 객체 인지 확장 기능(계획) | 교차로와 합류 위험 경고 확인 |
| ECU 동작 | 신뢰도 기반 강등 및 이벤트 기록 | 객체 신뢰도 저하 시 자동감속 보조 차단/강등 및 이벤트 로깅 | 객체 인지 확장 기능(계획) | 신뢰도 저하 강등과 기록 확인 |
| ECU 동작 | 방향지시등/안전벨트 기반 경보 맥락 반영 | 방향지시등/안전벨트 상태를 경보 맥락 및 강조 정책에 반영 | 경보 편의 기능(계획) | 방향지시등과 안전벨트 반영 확인 |
| ECU 동작 | 주행모드 기반 경보 민감도 반영 | 주행 모드에 따라 경보 민감도 프로파일을 보정 | 경보 편의 기능(계획) | 주행모드 민감도 반영 확인 |
| ECU 동작 | 접근거리 표시/이벤트 이력 관리 | 긴급차량 접근 거리 표시와 경보 이벤트 기록·이력 조회를 제공 | 경보 편의 기능(계획) | 접근거리 표시와 이력 조회 확인 |
| ECU 동작 | 표시 방식/음량 설정 반영 | 경보 표시 방식/음량 설정을 HMI 출력 정책에 반영 | 경보 편의 기능(계획) | 표시 방식과 음량 설정 반영 확인 |
| ECU 동작 | 경고 입력 유효성 및 갱신 상태 보호 | 경고 판정 입력의 유효성과 갱신 상태를 검사하고 저신뢰 입력에 보수 정책을 적용 | 경고 안정화 기능(계획) | 입력 유효성과 갱신 상태 보호 확인 |
| ECU 동작 | 경고 안정화 및 채널 전환 관리 | 경고 전환을 안정화하고 출력 채널 상태에 따라 표시와 음향 동작을 정리한다 | 경고 안정화 기능(계획) | 경고 안정화와 채널 전환 확인 |
| ECU 동작 | 전동 주차/제동 보조 상태 반영 | 전동 주차 및 제동 보조 상태를 제동 관련 경고 맥락에 반영 | 확장 ECU 상태 연계 | 제동 관련 상태 반영 확인 |
| ECU 동작 | 차체자세/조향 안정화 상태 반영 | 차체자세/현가/후륜조향 상태를 주행 안정성 경고 맥락에 반영 | 확장 ECU 상태 연계 | 주행 안정 상태 반영 확인 |
| ECU 동작 | 출입 개폐 상태 반영 | 도어 및 테일게이트 개폐/제어 상태를 출입 개방 관련 경고 맥락에 반영 | 확장 ECU 상태 연계 | 출입 개폐 상태 반영 확인 |
| ECU 동작 | 탑승자 보호 상태 반영 | 탑승자 감지 및 보호 상태를 탑승자 보호 경고 맥락에 반영 | 확장 ECU 상태 연계 | 탑승자 보호 상태 반영 확인 |
| ECU 동작 | 실내 편의/조명 상태 반영 | 실내 편의 및 조명 상태를 차체 편의 경고 및 표시 맥락에 반영 | 확장 ECU 상태 연계 | 실내 편의와 조명 상태 반영 확인 |
| ECU 동작 | 표시/음향 서비스 상태 반영 | 표시 및 음향 서비스 상태를 경고 표시/HMI 상태 판단에 반영 | 확장 ECU 상태 연계 | 표시와 음향 서비스 상태 반영 확인 |
| ECU 동작 | 디지털 접근/차량 서비스 상태 반영 | 디지털 접근 및 차량 서비스 상태를 사용자 안내 및 서비스 경고 맥락에 반영 | 확장 ECU 상태 연계 | 디지털 접근과 차량 서비스 상태 반영 확인 |
| ECU 동작 | 주행 보조 제어 상태 반영 | 주행 보조 제어 상태를 위험 경고 및 기능 가용성 판단에 반영 | 확장 ECU 상태 연계 | 주행 보조 상태 반영 확인 |
| ECU 동작 | 주차/저속 주변인지 상태 반영 | 주차 보조 및 저속 주변인지 상태를 주차 관련 경고와 기능 가용성 판단에 반영 | 확장 ECU 상태 연계 | 주차와 저속 주변 인지 상태 반영 확인 |
| ECU 동작 | 인지 센서 상태 반영 | 인지 센서 상태를 위험 판단 신뢰도 및 경고 강등 판단에 반영 | 확장 ECU 상태 연계 | 인지 센서 상태 반영 확인 |
| ECU 동작 | 도메인 서비스 가용성 상태 반영 | 백본 및 도메인 서비스 가용성 상태를 경계 통신 가용성과 서비스 강등 정책에 반영 | 확장 ECU 상태 연계 | 도메인 서비스 가용성 반영 확인 |
| ECU 동작 | 구동/전력변환 상태 반영 | 구동 및 전력변환 상태를 동력 전달 가용성과 에너지 기반 경고 맥락에 반영 | 확장 ECU 상태 연계 | 구동과 전력변환 상태 반영 확인 |
| ECU 동작 | 변속/열관리/충전 인터페이스 상태 반영 | 변속, 열관리 및 충전 인터페이스 상태를 구동 준비 상태와 서비스 경고 맥락에 반영 | 확장 ECU 상태 연계 | 변속, 열관리, 충전 상태 반영 확인 |
---

## 기능 정의 상세 표 (추적성/노드/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_001 | Req_001 | ADAS_WARN_CTRL | 주행 시 경고 시스템 활성 | 주행 상태에서 경고 시스템 활성화 | 입력: vehicleSpeedNorm, driveStateNorm / 출력: warningState |
| Func_002 | Req_002 | ADAS_WARN_CTRL | 비주행 경고 억제 | 정차/비주행 상태에서 경고 출력 억제 | 입력: driveStateNorm / 출력: warningState |
| Func_003 | Req_003 | ADAS_WARN_CTRL | 경고 시작 트리거 | 경고 조건 성립 시 시스템 출력 시작 | 입력: baseZoneContext, warningState / 출력: warningState |
| Func_004 | Req_004 | ADAS_WARN_CTRL | 경고 종료 트리거 | 해제 조건 성립 시 시스템 출력 종료 | 입력: warningState / 출력: warningState |
| Func_005 | Req_005 | CLU_HMI_CTRL | 경고 원인 전달 | 경고 원인 텍스트 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_006 | Req_006 | ADAS_WARN_CTRL | 반복 경고 디바운스 | 동일 조건 경고의 재출력 간격을 관리해 중복 표시를 억제 | 입력: warningState / 출력: warningState |
| Func_007 | Req_007 | NAV_CTX_MGR | 구간값 변경 반영 | roadZone/speedLimit 변경 시 구간 상태 갱신 | 입력: roadZone, navDirection, zoneDistance, speedLimit / 출력: baseZoneContext, speedLimitNorm |
| Func_008 | Req_008 | AMBIENT_CTRL | 일반구간 정책 적용 | 일반 구간 기본 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_009 | Req_009 | AMBIENT_CTRL | 스쿨존 강화 경고 | 스쿨존 전용 강화 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_010 | Req_010 | ADAS_WARN_CTRL | 스쿨존 과속 경고 | 스쿨존 속도 초과 이벤트 판정 | 입력: vehicleSpeedNorm, speedLimitNorm, baseZoneContext / 출력: warningState |
| Func_011 | Req_011 | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 | 고속 구간 무조향 타이머 경고 | 입력: steeringInputNorm, baseZoneContext / 출력: warningState |
| Func_012 | Req_012 | ADAS_WARN_CTRL | 무조향 경고 해제 | 고속도로 무조향 의심 경고 활성 상태에서 조향 입력 검출 시 경고 해제 | 입력: steeringInputNorm / 출력: warningState |
| Func_013 | Req_013 | AMBIENT_CTRL | 유도구간 진입 전환 | 유도구간 진입 시 방향안내 모드 전환 | 입력: selectedAlertType, navDirection / 출력: ambientMode |
| Func_014 | Req_014 | AMBIENT_CTRL | 좌우 방향 구분 표시 | navDirection 기준 좌/우 패턴 분기 | 입력: navDirection / 출력: ambientPattern |
| Func_015 | Req_015 | AMBIENT_CTRL | 구간 전환 완화 | 전환 중 점멸 튐 현상 완화 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_016 | Req_016 | AMBIENT_CTRL | 구간경고 종료 복귀 | 조건 해제 시 기본 구간 패턴 복귀 | 입력: timeoutClear / 출력: ambientMode |
| Func_017 | Req_017 | EMS_ALERT | 경찰 접근 경고 송신 | 경찰 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_018 | Req_017 | EMS_ALERT | 구급 접근 경고 송신 | 구급 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_019 | Req_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 | 경찰/구급 타입 구분 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_020 | Req_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 | 접근 방향 정보 표시 | 입력: emergencyDirection / 출력: warningTextCode |
| Func_021 | Req_021 | CLU_HMI_CTRL | 양보 유도 메시지 | 양보 요청 고정 메시지 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_022 | Req_022 | WARN_ARB_MGR | 긴급경고 우선 출력 | 비긴급 경고(구간/안내형)보다 긴급 경고 우선 적용 | 입력: emergencyContext, warningState, baseZoneContext / 출력: selectedAlertLevel, selectedAlertType |
| Func_023 | Req_023 | EMS_ALERT | 종료 신호 처리 | CLEAR 수신 시 긴급경고 종료 | 입력: alertState, emergencyType / 출력: emergencyContext |
| Func_024 | Req_024 | EMS_ALERT | 타임아웃 보호해제 | 긴급 신호가 1000ms 이상 미갱신되면 안전 해제 | 입력: lastEmergencyRxMs / 출력: timeoutClear |
| Func_025 | Req_025 | WARN_ARB_MGR | 다중긴급 단일선택 | 동시 긴급 신호 중 1개만 선택해 표시 | 입력: emergencyContext / 출력: selectedAlertType |
| Func_026 | Req_026 | CLU_HMI_CTRL | 중복 팝업 억제 | 동일 긴급 이벤트 중복 팝업 억제 | 입력: selectedAlertType, duplicatePopupGuard / 출력: warningTextCode |
| Func_027 | Req_027 | WARN_ARB_MGR | 충돌중재 적용 | 구간 경고/긴급 경고 동시 유효 시 중재 규칙 적용 | 입력: emergencyContext, warningState / 출력: selectedAlertLevel |
| Func_028 | Req_028 | WARN_ARB_MGR | 긴급>구간 우선 적용 | 긴급 시 구간 패턴 오버라이드 | 입력: emergencyContext / 출력: selectedAlertLevel |
| Func_029 | Req_029 | WARN_ARB_MGR | 구급>경찰 우선 적용 | emergencyType 우선순위 적용 | 입력: emergencyType / 출력: selectedAlertType |
| Func_030 | Req_030 | WARN_ARB_MGR | ETA 우선 적용 | 동급 알림이면 ETA 최소값 선택 | 입력: eta / 출력: selectedAlertType |
| Func_031 | Req_031 | WARN_ARB_MGR | SourceID 동률판정 | ETA 동률 시 sourceId 오름차순 | 입력: sourceId / 출력: selectedAlertType |
| Func_032 | Req_032 | WARN_ARB_MGR | 중재결과 결정론 보장 | 동일 입력이면 동일 결과 출력 | 입력: arbitrationSnapshotId / 출력: selectedAlertLevel, selectedAlertType |
| Func_033 | Req_033 | AMBIENT_CTRL | 종료후 이전상태 복원 | 긴급 종료 후 직전 구간 상태 복원 | 입력: timeoutClear, baseZoneContext / 출력: ambientMode |
| Func_034 | Req_034 | AMBIENT_CTRL | 전환 깜빡임 완화 | 구간 경고에서 긴급 경고 전환 시 표시 안정화(점멸/소실 방지) 제어 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_035 | Req_035 | AMBIENT_CTRL | 긴급 색상 정책 | 긴급 색상 팔레트 고정 적용 | 입력: selectedAlertType / 출력: ambientColor |
| Func_036 | Req_035 | AMBIENT_CTRL | 긴급 패턴 정책 | 긴급 점등 패턴 고정 적용 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_037 | Req_037 | AMBIENT_CTRL | 스쿨존 패턴 정책 | 스쿨존 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_038 | Req_037 | AMBIENT_CTRL | 고속도로 패턴 정책 | 고속 경고 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_039 | Req_037 | AMBIENT_CTRL | 유도선 패턴 정책 | 좌/우 유도 패턴 고정 적용 | 입력: navDirection, baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_040 | Req_040 | CLU_HMI_CTRL | 문구 길이 제한 | 경고 문구 길이/형식 고정 | 입력: warningTextCode / 출력: warningTextCode |
| Func_041 | Req_041 | VAL_SCENARIO_CTRL | SIL 시나리오 실행(Validation-only) | CANoe SIL에서 시나리오 실행 제어 | 입력: testScenario / 출력: scenarioResult |
| Func_042 | Req_042 | VAL_SCENARIO_CTRL | CAN+ETH 동시 검증(Validation-only) | CAN/Ethernet 동시 조건 검증 | 입력: testScenario / 출력: scenarioResult |
| Func_043 | Req_043 | VAL_SCENARIO_CTRL | 판정 결과 산출(Validation-only) | 시나리오 Pass/Fail 판정 출력 | 입력: scenarioResult / 출력: scenarioResult |

---

## OEM100 Surface ECU 적용 상태 (03 기준)
| 구분 | 내용 |
|---|---|
| 기준 SoT | `00e_ECU_Naming_Standard.md` 6.4 (100 ECU 전수표) |
| 전체 Surface ECU | 100 |
| 활성(상세 정의) | 99 |
| 미구현(Placeholder) | 1 |

### OEM100 전수표 (100개)

| Surface ECU | Group | Domain Bucket | Surface Type | 구현 상태 | Runtime Binding | 문서 반영 정책 |
|---|---|---|---|---|---|---|
| `CGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `CGW` | 추적체인 반영 대상 |
| `ETHB` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `ETHB(Health/Freshness monitor)` | 추적체인 반영 대상 |
| `DCM` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `DCM` | 추적체인 반영 대상 |
| `IBOX` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `IBOX` | 추적체인 반영 대상 |
| `SGW` | A1 | Infrastructure/Integration | INFRA_SERVICE | 활성(상세 정의) | `SGW` | 추적체인 반영 대상 |
| `EMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EMS` | 추적체인 반영 대상 |
| `TCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `TCU` | 추적체인 반영 대상 |
| `VCU` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `VCU` | 추적체인 반영 대상 |
| `_4WD` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `_4WD` | 추적체인 반영 대상 |
| `BAT_BMS` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `BAT_BMS` | 추적체인 반영 대상 |
| `FPCM` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `FPCM` | 추적체인 반영 대상 |
| `LVR` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `LVR` | 추적체인 반영 대상 |
| `ISG` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `ISG` | 추적체인 반영 대상 |
| `EOP` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EOP` | 추적체인 반영 대상 |
| `EWP` | A2 | Powertrain | PHYSICAL/DOMAIN | 활성(상세 정의) | `EWP` | 추적체인 반영 대상 |
| `ESC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ESC` | 추적체인 반영 대상 |
| `MDPS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `MDPS` | 추적체인 반영 대상 |
| `ABS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ABS` | 추적체인 반영 대상 |
| `EPB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `EPB` | 추적체인 반영 대상 |
| `TPMS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `TPMS` | 추적체인 반영 대상 |
| `SAS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `SAS` | 추적체인 반영 대상 |
| `ECS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ECS` | 추적체인 반영 대상 |
| `ACU` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ACU` | 추적체인 반영 대상 |
| `ODS` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `ODS` | 추적체인 반영 대상 |
| `VSM` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `VSM` | 추적체인 반영 대상 |
| `EHB` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `EHB` | 추적체인 반영 대상 |
| `CDC` | A3 | Chassis/Safety | PHYSICAL/DOMAIN | 활성(상세 정의) | `CDC` | 추적체인 반영 대상 |
| `BCM` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `BCM` | 추적체인 반영 대상 |
| `DATC` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DATC` | 추적체인 반영 대상 |
| `SMK` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SMK` | 추적체인 반영 대상 |
| `AFLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `AFLS` | 추적체인 반영 대상 |
| `AHLS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `AHLS` | 추적체인 반영 대상 |
| `WIP` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `WIPER_MODULE` | 추적체인 반영 대상 |
| `SRF` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SUNROOF_MODULE` | 추적체인 반영 대상 |
| `DOOR_FL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_FL` | 추적체인 반영 대상 |
| `DOOR_FR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_FR` | 추적체인 반영 대상 |
| `DOOR_RL` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_RL` | 추적체인 반영 대상 |
| `DOOR_RR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `DOOR_RR` | 추적체인 반영 대상 |
| `TGM` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `TAILGATE_MODULE` | 추적체인 반영 대상 |
| `SEAT_DRV` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SEAT_DRV` | 추적체인 반영 대상 |
| `SEAT_PASS` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `SEAT_PASS` | 추적체인 반영 대상 |
| `MIR` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `MIRROR_MODULE` | 추적체인 반영 대상 |
| `BSEC` | A4 | Body/Comfort | PHYSICAL/DOMAIN | 활성(상세 정의) | `BODY_SECURITY_MODULE` | 추적체인 반영 대상 |
| `IVI` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `IVI` | 추적체인 반영 대상 |
| `CLU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `CLU` | 추적체인 반영 대상 |
| `HUD` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `HUD` | 추적체인 반영 대상 |
| `TMU` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `TMU` | 추적체인 반영 대상 |
| `AMP` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `AMP` | 추적체인 반영 대상 |
| `PGS` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `PGS` | 추적체인 반영 대상 |
| `NAV` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `NAV_MODULE` | 추적체인 반영 대상 |
| `VCS` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `VOICE_ASSIST` | 추적체인 반영 대상 |
| `RSE` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `RSE` | 추적체인 반영 대상 |
| `DKEY` | A5 | IVI/HMI/Connectivity | PHYSICAL/DOMAIN | 활성(상세 정의) | `DIGITAL_KEY` | 추적체인 반영 대상 |
| `ADAS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `ADAS` | 추적체인 반영 대상 |
| `V2X` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `V2X` | 추적체인 반영 대상 |
| `SCC` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `SCC` | 추적체인 반영 대상 |
| `LDWS_LKAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `LDWS_LKAS` | 추적체인 반영 대상 |
| `FCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `FCA` | 추적체인 반영 대상 |
| `BCW` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `BCW` | 추적체인 반영 대상 |
| `LCA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `LCA` | 추적체인 반영 대상 |
| `SPAS` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `SPAS` | 추적체인 반영 대상 |
| `RSPA` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `RSPA` | 추적체인 반영 대상 |
| `AVM` | A6 | ADAS/V2X/Parking | FUNCTION_SURFACE | 활성(상세 정의) | `AVM` | 추적체인 반영 대상 |
| `FCAM` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `FCAM` | 추적체인 반영 대상 |
| `FRADAR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `FRADAR` | 추적체인 반영 대상 |
| `SRR_FL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_FL` | 추적체인 반영 대상 |
| `SRR_FR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_FR` | 추적체인 반영 대상 |
| `SRR_RL` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_RL` | 추적체인 반영 대상 |
| `SRR_RR` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `SRR_RR` | 추적체인 반영 대상 |
| `PUS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `PARK_ULTRASONIC` | 추적체인 반영 대상 |
| `DMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `DMS` | 추적체인 반영 대상 |
| `OMS` | A6 | ADAS/V2X/Parking | PHYSICAL/DOMAIN | 활성(상세 정의) | `OMS` | 추적체인 반영 대상 |
| `VALIDATION_HARNESS` | B | Validation | VALIDATION | 활성(상세 정의) | `VAL_SCENARIO_CTRL + VAL_BASELINE_CTRL` | 추적체인 반영 대상 |
| `OBC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `OBC` | 추적체인 반영 대상 |
| `DCDC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `DCDC` | 추적체인 반영 대상 |
| `MCU` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `MCU` | 추적체인 반영 대상 |
| `INVERTER` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `INVERTER` | 추적체인 반영 대상 |
| `CPC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `CHARGE_PORT_CTRL` | 추적체인 반영 대상 |
| `ASM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `AIR_SUSPENSION` | 추적체인 반영 대상 |
| `RWS` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `RWS` | 추적체인 반영 대상 |
| `NIGHT_VISION` | C | Premium Option | PHYSICAL/DOMAIN | 미구현(Placeholder) | - | 승격 전 참조만, 추적체인 미부여 |
| `AEB` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `AEB_DOMAIN` | 추적체인 반영 대상 |
| `HWP` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `HIGHWAY_PILOT` | 추적체인 반영 대상 |
| `PKM` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `PARK_MASTER` | 추적체인 반영 대상 |
| `TRM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `TRAILER_CTRL` | 추적체인 반영 대상 |
| `HLM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `HEADLAMP_LEVELING` | 추적체인 반영 대상 |
| `ADM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `AUTO_DOOR_CTRL` | 추적체인 반영 대상 |
| `PTG` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `POWER_TAILGATE_CTRL` | 추적체인 반영 대상 |
| `MSC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `MASSAGE_SEAT_CTRL` | 추적체인 반영 대상 |
| `RATC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `REAR_CLIMATE_MODULE` | 추적체인 반영 대상 |
| `CSM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `CABIN_SENSING` | 추적체인 반영 대상 |
| `BIO` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `BIOMETRIC_AUTH` | 추적체인 반영 대상 |
| `CPAY` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `CARPAY_CTRL` | 추적체인 반영 대상 |
| `PAK` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `PHONE_AS_KEY` | 추적체인 반영 대상 |
| `OTA` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `OTA_MASTER` | 추적체인 반영 대상 |
| `EDR` | C | Premium Option | INFRA_SERVICE | 활성(상세 정의) | `EDR` | 추적체인 반영 대상 |
| `RPC` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `ROAD_PREVIEW_CAMERA` | 추적체인 반영 대상 |
| `LDR` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `LIDAR` | 추적체인 반영 대상 |
| `RRM` | C | Premium Option | PHYSICAL/DOMAIN | 활성(상세 정의) | `REAR_RADAR_MASTER` | 추적체인 반영 대상 |
| `SPM` | C | Premium Option | FUNCTION_SURFACE | 활성(상세 정의) | `SURROUND_PARK_MASTER` | 추적체인 반영 대상 |


- Placeholder ECU는 승격 전까지 상세 추적(Req/Func/Flow/Comm/Var/Test)을 강제하지 않는다.
- Placeholder ECU 승격 시 `03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07` 순서로 동일 커밋 편입한다.
---

## 차량 기본 기능 확장 상세 표 (Phase-1)

| Func ID | Req ID | 실제 노드명(Surface ECU / runtime alias) | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_101 | Req_101 | EMS / ENG_CTRL | 시동 상태 반영 | 시동 On/Off 입력을 차량 기본 동작 상태로 반영 | 입력: IgnitionState / 출력: EngineState |
| Func_102 | Req_102 | TCU / TCU | 기어 상태 반영 | P/R/N/D 기어 입력을 상태값으로 유지/전달 | 입력: GearInput / 출력: GearState |
| Func_103 | Req_103 | VCU / ACCEL_CTRL | 가속 입력 반영 | 가속 페달 입력을 종방향 제어 입력으로 전달 | 입력: AccelPedal / 출력: AccelRequest |
| Func_104 | Req_104 | ESC / BRK_CTRL | 제동 입력 반영 | 브레이크 페달 입력을 감속 제어 입력으로 전달 | 입력: BrakePedal / 출력: BrakePressure |
| Func_105 | Req_105 | MDPS / STEER_CTRL | 조향 입력 반영 | 조향 입력을 차량 상태/주의 판단 입력으로 전달 | 입력: steeringInput / 출력: SteeringState |
| Func_106 | Req_106 | BCM / HAZARD_CTRL | 비상등 기본 제어 | 비상등 On/Off 입력을 상태 출력으로 반영 | 입력: HazardSwitch / 출력: HazardState |
| Func_107 | Req_107 | BCM / WINDOW_CTRL | 창문 기본 제어 | 창문 개폐 입력을 창문 상태로 반영 | 입력: WindowCommand / 출력: WindowState |
| Func_109 | Req_109 | CLU / CLU_BASE_CTRL | 클러스터 기본 표시 | 속도/기어/경고 기본 상태를 클러스터에 표시 | 입력: ClusterSpeed, ClusterGear, warningTextCode / 출력: ClusterStatus |
| Func_110 | Req_110 | CGW / DOMAIN_ROUTER | 도메인 게이트웨이 전달 | 도메인 간 입력/출력 메시지 라우팅 수행 | 입력: RoutingPolicy / 출력: BodyGatewayRoute |
| Func_111 | Req_111 | CGW / DOMAIN_BOUNDARY_MGR | 도메인 경계 유지 | 도메인별 통신 경계/역할 분리를 유지 | 입력: RoutingPolicy / 출력: BoundaryStatus |
| Func_112 | Req_112 | VALIDATION_HARNESS / VAL_BASELINE_CTRL | 차량 기본 기능 SIL 검증(Validation-only) | 기본 차량 기능 시나리오 실행 및 판정 | 입력: BaseScenarioId / 출력: BaseScenarioResult |
| Func_113 | Req_113 | BCM / BODY_GW | 공조 상태 반영 | 공조 상태/제어 프레임(DATC) 수신 정보를 도메인 정책에 반영 | 입력: CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode / 출력: CabinTemp |
| Func_114 | Req_113 | BCM / DRV_STATE_MGR | 시트 상태 반영 | 시트 상태/제어 프레임 수신 정보를 상태 관리에 반영 | 입력: DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel / 출력: DriverStateInfo |
| Func_115 | Req_113 | BCM / WINDOW_CTRL | 미러 상태 반영 | 미러 상태 프레임(폴딩/열선/조정) 정보를 차량 상태에 반영 | 입력: MirrorFoldState, MirrorHeatState, MirrorAdjAxis / 출력: WindowState |
| Func_116 | Req_116 | BCM / WINDOW_CTRL | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태를 수신/반영/전달 | 입력: DoorUnlockCmd, DoorLockState, DoorOpenWarn / 출력: DoorStateMask |
| Func_117 | Req_116 | BCM / AMBIENT_CTRL | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태를 연동 정책에 반영 | 입력: FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq / 출력: WiperInterval |
| Func_118 | Req_118 | BCM / DRV_STATE_MGR | 보안 상태 반영 | 이모빌라이저/경보 상태를 보안 상태로 반영 | 입력: ImmoState, AlarmArmed, AlarmTrigger, AlarmZone / 출력: DriverStateInfo |
| Func_119 | Req_119 | CLU / CLU_HMI_CTRL | 오디오 상태 반영 | 오디오 포커스/음성비서/TTS 상태를 HMI 정책에 반영 | 입력: AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId / 출력: warningTextCode |


## V2 확장 기능 상세 표 (Implemented, Phase-2)

| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_120 | Req_120 | ADAS_WARN_CTRL | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 근접 위험도 산정 | 입력: emergencyDirection, eta, vehicleSpeedNorm / 출력: proximityRiskLevel |
| Func_121 | Req_121 | WARN_ARB_MGR | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | 입력: proximityRiskLevel, failSafeMode, driveStateNorm / 출력: decelAssistReq |
| Func_125 | Req_125 | WARN_ARB_MGR | 감속 보조 시 긴급경고 최우선 유지 | 감속 보조 요청 활성 시 긴급 경고 최우선 유지 | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertType, selectedAlertLevel |
| Func_126 | Req_126 | WARN_ARB_MGR | 감속 보조 시 경고 채널 동기화 | 감속 보조 요청 활성 시 Ambient/Cluster 출력 동기화 | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertType, selectedAlertLevel |
| Func_123 | Req_123 | WARN_ARB_MGR | 운전자 개입 우선 해제 | 운전자 제동/조향 회피 입력 검출 시 감속 보조 요청 해제 | 입력: steeringInputNorm, brakePedalNorm / 출력: decelAssistReq |
| Func_127 | Req_127 | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 자동감속 금지 | 도메인 경로 단절 감지 시 자동 감속 보조 요청 생성 금지 | 입력: domainPathStatus, e2eHealthState / 출력: decelAssistReq |
| Func_128 | Req_128 | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 최소 경고 유지 | 도메인 경로 단절 감지 시 최소 경고 채널 유지 | 입력: domainPathStatus, e2eHealthState / 출력: selectedAlertType, selectedAlertLevel |
| Func_129 | Req_129 | DOMAIN_BOUNDARY_MGR | 도메인 단절 시 안전 강등 전환 | 도메인 경로 단절 감지 시 failSafeMode 전환 | 입력: domainPathStatus, e2eHealthState / 출력: failSafeMode |

---

## ADAS 객체 인지 확장 기능 상세 표 (Planned, Phase-3)

| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_130 | Req_130 | ADAS_WARN_CTRL | 객체 목록 수용 | 주변 객체 목록을 수신해 위험 판단 입력으로 정규화 | 입력: objectTrackValid, objectRange, objectRelSpeed, objectConfidence / 출력: objectTrackValid, objectRange, objectRelSpeed |
| Func_131 | Req_131 | ADAS_WARN_CTRL | 대표 위험 객체 선정 | 자차 경로 기준 대표 위험 객체 선정 | 입력: objectTrackValid, objectRange, objectRelSpeed / 출력: objectRiskClass, objectTtcMin |
| Func_132 | Req_132 | ADAS_WARN_CTRL | TTC 기반 전방 충돌 경고 | TTC 임계 이하 객체에 대해 전방 충돌 경고 트리거 | 입력: objectTtcMin, objectRiskClass / 출력: objectRiskClass, selectedAlertLevel |
| Func_133 | Req_133 | ADAS_WARN_CTRL | 상대속도/거리 기반 단계화 | 상대속도/거리 변화 기반 경고 단계 상하향 | 입력: objectRelSpeed, objectRange, objectRiskClass / 출력: objectRiskClass, selectedAlertLevel |
| Func_134 | Req_134 | WARN_ARB_MGR | 교차로 측방 위험 경고 | 교차로 진입 맥락에서 측방 접근 객체 경고 생성 | 입력: intersectionConflictFlag, objectRiskClass / 출력: selectedAlertType, selectedAlertLevel |
| Func_135 | Req_135 | WARN_ARB_MGR | 합류/끼어들기 위험 경고 | 합류/끼어들기 급간섭 객체 경고 생성 | 입력: mergeCutInFlag, objectRiskClass / 출력: selectedAlertType, selectedAlertLevel |
| Func_136 | Req_136 | ADAS_WARN_CTRL | 추적 손실 보수 유지 | 추적 손실 시 경고 유지시간 적용 후 해제 | 입력: objectTrackValid, objectAlertHoldMs / 출력: objectRiskClass, selectedAlertLevel |
| Func_137 | Req_137 | DOMAIN_BOUNDARY_MGR | 신뢰도 저하 강등 | 객체 신뢰도 저하 시 자동감속 보조 차단 및 경고 강등 | 입력: objectConfidence, decelAssistReq / 출력: decelAssistReq, failSafeMode, selectedAlertLevel |
| Func_138 | Req_138 | EMS_ALERT | 객체 경고 이벤트 기록 | 객체 기반 경보 발생/해제/강등 이벤트 기록 | 입력: objectRiskClass, selectedAlertType, selectedAlertLevel / 출력: objectEventCode |
| Func_139 | Req_139 | WARN_ARB_MGR | 객체 경고 우선순위 정합 | 객체 경고와 기존 구간/긴급 경고의 최종 우선순위 일관성 보장 | 입력: objectRiskClass, emergencyContext, baseZoneContext / 출력: selectedAlertType, selectedAlertLevel |

---

## 차량 경보 편의 확장 기능 상세 표 (Planned, Phase-3B)

| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_140 | Req_140 | WARN_ARB_MGR | 방향지시등 기반 경보 맥락 보정 | 방향지시등 상태를 활용해 경보 방향/문구 맥락 보정 | 입력: TurnLampState, selectedAlertType / 출력: selectedAlertType, warningTextCode |
| Func_141 | Req_141 | WARN_ARB_MGR | 주행모드 기반 경보 민감도 프로파일 | DriveMode/Eco/Sport 상태에 따른 경보 민감도 보정 | 입력: DriveMode, EcoMode, SportMode, selectedAlertLevel / 출력: selectedAlertLevel |
| Func_142 | Req_142 | WARN_ARB_MGR | 안전벨트 상태 기반 경보 강조 | 안전벨트 상태/경고레벨 기반 경보 강조 적용 | 입력: DriverSeatBelt, PassengerSeatBelt, SeatBeltWarnLvl, selectedAlertLevel / 출력: selectedAlertLevel, selectedAlertType |
| Func_143 | Req_143 | CLU_HMI_CTRL | 긴급차량 접근 거리 표시 | ETA와 자차 속도 기반 접근 거리 등급/문구 표시 | 입력: eta, vehicleSpeedNorm, selectedAlertType / 출력: warningTextCode |
| Func_144 | Req_144 | EMS_ALERT | 경보 이벤트 공통 기록 | 긴급/구간/객체 경보 이벤트를 공통 포맷으로 기록 | 입력: selectedAlertType, selectedAlertLevel, warningTextCode / 출력: arbitrationSnapshotId |
| Func_145 | Req_145 | CLU_HMI_CTRL | 경보 이벤트 이력 조회 | 최근 경보 이벤트 이력을 HMI에서 조회/표시 | 입력: arbitrationSnapshotId, ClusterNotifType, ClusterNotifPrio / 출력: warningTextCode |
| Func_146 | Req_146 | CLU_HMI_CTRL | 경보 표시 방식 설정 반영 | 테마/팝업 설정을 경보 표시 정책에 반영 | 입력: ThemeMode, PopupType, PopupPriority, PopupActive / 출력: warningTextCode, ClusterNotifPrio |
| Func_147 | Req_147 | CLU_HMI_CTRL | 경보 음량 설정 반영 | 음량/오디오 포커스 상태를 반영해 경보 음량 정책 적용 | 입력: VolumeLevel, AudioFocusOwner / 출력: warningTextCode, ClusterNotifPrio |
| Func_148 | Req_148 | ADAS_WARN_CTRL | 경고 입력 유효성 필터링 | 객체/상태 입력의 유효성·신뢰도 기준을 점검해 판정 입력을 필터링 | 입력: objectTrackValid, objectConfidence, objectRiskClass / 출력: objectRiskClass, selectedAlertLevel |
| Func_149 | Req_149 | WARN_ARB_MGR | 경고 입력 신선도 보호 | 핵심 입력 무갱신 상태(stale)를 감지해 보수 경고 정책으로 전환 | 입력: lastEmergencyRxMs, timeoutClear, warningState / 출력: warningState, selectedAlertLevel |
| Func_150 | Req_150 | WARN_ARB_MGR | 경고 상태 전이 안정화 | 동일 원인 경고 상태의 반복 진동을 억제하도록 전이 안정화 처리 | 입력: warningState, selectedAlertLevel, duplicatePopupGuard / 출력: selectedAlertLevel, selectedAlertType |
| Func_151 | Req_151 | DOMAIN_BOUNDARY_MGR | 출력 채널 가용성 판정 | 도메인 경계 통신 상태(헬스/타임아웃/유효 플래그) 기반 출력 채널 가용성 판정 | 입력: domainPathStatus, e2eHealthState, BoundaryStatus / 출력: domainPathStatus, failSafeMode |
| Func_152 | Req_152 | WARN_ARB_MGR | 출력 채널 장애 대체 정책 | 주 출력 채널 장애 시 대체 채널 기반 경고 지속 정책 적용 | 입력: failSafeMode, selectedAlertType, selectedAlertLevel / 출력: selectedAlertType, selectedAlertLevel, warningTextCode |
| Func_153 | Req_153 | CLU_HMI_CTRL | 오디오 경합 인지성 보호 | 오디오/음성 경합 상태를 반영해 경고 인지성 보호 정책 적용 | 입력: AudioFocusOwner, AudioDuckLevel, TtsState / 출력: warningTextCode, ClusterNotifPrio |
| Func_154 | Req_154 | CLU_HMI_CTRL | 팝업 과밀 억제 및 우선 표시 | 복수 경고 동시 상황에서 비긴급 팝업 과밀을 억제하고 우선 경고를 선표시 | 입력: PopupType, PopupPriority, PopupActive, duplicatePopupGuard / 출력: warningTextCode, ClusterNotifPrio |
| Func_155 | Req_155 | CLU_HMI_CTRL | 경고 채널 동기 일관성 관리 | 앰비언트/클러스터 경고 맥락 불일치 감시 및 동기 복원 | 입력: ClusterSyncState, ClusterSyncSeq, selectedAlertType, selectedAlertLevel / 출력: warningTextCode, ClusterNotifPrio |
| Func_156 | Req_156 | CHS_GW | 전동 주차/제동 보조 상태 통합 | 전동 주차 및 제동 보조 상태를 통합해 제동 관련 경고 맥락에 반영 | 입력: EpbState, EhbState / 출력: brakeAssistExtState, selectedAlertLevel |
| Func_157 | Req_157 | CHS_GW | 차체자세/조향 안정화 상태 통합 | 차체자세 제어, 현가, 후륜조향 상태를 통합해 주행 안정성 경고 맥락에 반영 | 입력: VsmState, EcsState, CdcState, AirSuspensionState, RwsState / 출력: chassisStabilityExtState, selectedAlertLevel |
| Func_158 | Req_158 | BODY_GW | 출입 개폐 상태 통합 | 도어 및 테일게이트 개폐/제어 상태를 통합해 출입 개방 관련 경고 맥락에 반영 | 입력: DoorModuleStateMask, TailgateState, AutoDoorCtrlState, PowerTailgateCtrlState / 출력: closureAccessState |
| Func_159 | Req_159 | BODY_GW | 탑승자 보호 상태 통합 | 탑승자 감지 및 보호 상태를 통합해 탑승자 보호 경고 맥락에 반영 | 입력: CabinSensingState, AcuState, OdsState, BiometricAuthState / 출력: occupantProtectionState |
| Func_160 | Req_160 | BODY_GW | 실내 편의/조명 상태 통합 | 실내 편의 및 조명 상태를 통합해 차체 편의 경고 및 표시 맥락에 반영 | 입력: AflsState, AhlsAssistState, RearClimateState, SunroofState, HeadlampLevelState, MassageSeatState / 출력: comfortLightingState |
| Func_161 | Req_161 | IVI_GW | 표시/음향 서비스 상태 통합 | 표시 및 음향 서비스 상태를 통합해 경고 표시/HMI 상태 판단에 반영 | 입력: HudState, AmpState, RseState, NavModuleState, PgsState / 출력: displayAudioServiceState, navigationTelematicsState |
| Func_162 | Req_162 | IVI_GW | 디지털 접근/차량 서비스 상태 통합 | 디지털 접근 및 차량 서비스 상태를 통합해 사용자 안내 및 서비스 경고 맥락에 반영 | 입력: TmuServiceState, OtaMasterState, DigitalKeyState, PhoneAsKeyState, CarpayCtrlState / 출력: digitalAccessServiceState |
| Func_163 | Req_163 | ADAS_WARN_CTRL | 주행 보조 제어 상태 통합 | 주행 보조 제어 상태를 통합해 위험 경고 및 기능 가용성 판단에 반영 | 입력: LaneKeepState, FcaState, BlindSpotState, AebDomainState, HighwayPilotState / 출력: drivingAssistStateExt, selectedAlertLevel |
| Func_164 | Req_164 | ADAS_WARN_CTRL | 주차/저속 주변인지 상태 통합 | 주차 보조 및 저속 주변인지 상태를 통합해 주차 관련 경고와 기능 가용성 판단에 반영 | 입력: ParkingAssistState, TrailerCtrlState / 출력: parkingSurroundState, selectedAlertLevel |
| Func_165 | Req_165 | ADAS_WARN_CTRL | 인지 센서 상태 통합 | 인지 센서 상태를 통합해 위험 판단 신뢰도 및 경고 강등 판단에 반영 | 입력: CameraRadarState, OccupantMonitorState, LidarState / 출력: sensorAvailabilityState, failSafeMode |
| Func_166 | Req_166 | DOMAIN_BOUNDARY_MGR | 도메인 서비스 가용성 상태 통합 | 백본 및 도메인 서비스 가용성 상태를 통합해 경계 통신 가용성과 서비스 강등 정책에 반영 | 입력: IboxState, SecurityState, DiagState, EdrState, BackboneState / 출력: backboneServiceState, domainPathStatus, failSafeMode |
| Func_167 | Req_167 | DOMAIN_ROUTER | 구동/전력변환 상태 통합 | 구동 및 전력변환 상태를 통합해 동력 전달 가용성과 에너지 기반 경고 맥락에 반영 | 입력: ObcChargeState, DcDcSupplyState, MotorDriveState, InverterDriveState, TorqueSplitState, BatteryEnergyState / 출력: PowertrainElectrifiedState |
| Func_168 | Req_168 | DOMAIN_ROUTER | 변속/열관리/충전 인터페이스 상태 통합 | 변속, 열관리 및 충전 인터페이스 상태를 통합해 구동 준비 상태와 서비스 경고 맥락에 반영 | 입력: FuelPumpState, ShiftLeverExtState, IdleStopState, ThermalPumpState, ChargePortState / 출력: PowertrainAuxiliaryState |

---

## 경고 표시 정책표 (Req_008, Req_035, Req_037 기준)

| selectedAlertType | 의미 | ambientMode | ambientColor | ambientPattern | 정책 요약 |
|---|---|---:|---:|---:|---|
| 0 | Off | 0 | 0 | 0 | 경고 없음 |
| 1 | Police | 2 | 1/5 교차 | 2 | Red/Blue 교차 점멸 |
| 2 | Ambulance | 2 | 1/6 교차 | 2 | Red/White 교차 점멸 |
| 3 | School Zone | 2 | 1 | 3 | Red 빠른 점멸 |
| 4 | Highway (무조향 의심) | 2 | 2 | 1 | Orange 계열 정책 |
| 5 | Guide Left | 1 | 4 | 1 | Green 계열 좌측 유도 |
| 6 | Guide Right | 1 | 4 | 2 | Green 계열 우측 유도 |

### 코드값 사전
- `ambientColor`: `0=off, 1=red, 2=orange, 3=amber, 4=green, 5=blue, 6=white`
- `ambientPattern`: `0=off, 1=steady, 2=slow-flash, 3=fast-flash`
- `ambientMode`: `0=off, 1=steady, 2=flash/wave`

### Cluster 표시 코드 정책
- `timeoutClear == 0` 이고 `selectedAlertLevel > 0`일 때:
  - `warningTextCode = (selectedAlertType * 10) + selectedAlertLevel`
- 그 외(`timeoutClear == 1` 또는 `selectedAlertLevel == 0`)는 `warningTextCode = 0`

### 정합 기준
- 본 표와 CAPL 구현(`AMBIENT_CTRL`, `CLU_HMI_CTRL`)이 불일치하면 CAPL 구현을 우선 기준으로 보고, 본 문서를 동일 커밋에서 갱신한다.

---

---

## 상세 설명 및 추가 사항

- 상단 표는 공식 표준 양식의 열 구성(분류/기능명/기능설명/비고/검증)을 유지한다.
- 하단 표는 `Func/Req/노드/입출력` 기준으로 추적성을 보강한다.
- 추적 체인: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`.
- 옵션1 네트워크 전달 경로 고정: `입력 CAN -> 도메인 GW 정규화 -> ETHB -> 중앙 경고코어 -> 도메인 GW -> 출력 CAN`.
- `Func_101~Func_107`, `Func_109~Func_119`는 차량 기본 기능 확장 체인으로, 0302/0303/0304의 Flow/Comm/Var와 최신 도메인 DBC 기준으로 동기화되어야 한다.
- `Func_120~Func_121`, `Func_123`, `Func_125~Func_129`는 V2 확장 활성 체인으로 관리하며, 코드/DBC/05/06/07 변경을 동일 커밋 단위로 동기화한다.
- `Func_130~Func_139`는 ADAS 객체 인지 확장 Pre-Activation 체인으로 관리하며, 구현 착수 시 0302/0303/0304/04/05/06/07을 동일 커밋 단위로 동기화한다.
- `Func_140~Func_147`는 차량 경보 편의 확장 Pre-Activation 체인으로 관리하며, 구현 착수 시 0302/0303/0304/04/05/06/07을 동일 커밋 단위로 동기화한다.
- `Func_148~Func_155`는 경고 강건성·인지성 확장 Pre-Activation 체인으로 관리하며, 구현 착수 시 0302/0303/0304/04/05/06/07을 동일 커밋 단위로 동기화한다.

## EMS 논리 단말-내부 모듈 매핑

| 논리 단말(문서 표준) | 내부 구현 모듈(코드/통신) | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 알림 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 알림 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 알림 수신/해제/타임아웃 처리 |

## 차량 ECU 인벤토리 (03 기준 요약)

| 구분 | 내용 |
|---|---|
| Surface 인벤토리 | OEM100 전체 100개 (`00e` 6.4) |
| 상세 정의 대상 | 활성 99개 Surface ECU |
| Placeholder 정책 | 미구현 1개(`NIGHT_VISION`)는 이름/상태만 유지, 승격 전 상세 추적 미부여 |
| Runtime 모듈 표기 | `Func` 상세표에서 supporting trace로만 유지 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.38 | 2026-03-09 | 03~0304 정합 점검 반영: `ETHB` runtime 표기를 `ETHB(Health/Freshness monitor)`로 통일하고, Phase-1 기능표의 owner 표기를 `Surface ECU / runtime alias` 형식으로 정리해 reviewer 해석 혼선을 제거. |
| 4.37 | 2026-03-09 | Dev1 최종 승격(`1fda129`) 동기화: OEM100 상태를 `99 활성/1 미구현(NIGHT_VISION)`으로 갱신하고 활성 Surface ECU의 Func owner 표기를 최신 runtime anchor 기준으로 동기화. |
| 4.36 | 2026-03-09 | Dev1 추가 승격(`f61cb26`, rebased from `e4f69a2`) 동기화: `VSM/EHB/ECS/CDC`를 활성(상세 정의)로 전환하고 OEM100 전수표를 `38 활성/62 미구현`으로 갱신. |
| 4.35 | 2026-03-09 | Dev1 추가 승격(`2216335`) 동기화: `DOOR_FL/DOOR_FR/SEAT_DRV/SEAT_PASS`를 활성(상세 정의)로 전환하고 OEM100 전수표를 `34 활성/66 미구현`으로 갱신. |
| 4.34 | 2026-03-09 | Dev1 최신 승격(`a6fecf1`) 동기화: OEM100 전수표 상태를 30 활성/70 미구현으로 갱신하고 `03` 문서의 OEM100 섹션을 최신화. |
| 4.33 | 2026-03-09 | OEM100 선행 문서화 반영: `00e` 6.4를 100 ECU 단일 기준으로 연결하고, 03 문서에 활성 16/미구현 84 운영 규칙과 100 ECU 전수표(각 ECU 상태 명시)를 반영. |
| 4.32 | 2026-03-07 | Req_151 정합 보강: `Func_151` 설명을 `도메인 경계 통신 상태(헬스/타임아웃/유효 플래그)` 기준으로 명확화해 01 요구 문구와 동기화. |
| 4.31 | 2026-03-06 | Legacy 누락군 보강: `Req_018/036/038/039/114/115/117/122/124` 상속 관계를 `Legacy 전환 매핑` 섹션으로 명시해 통폐합 이후 추적 경로를 고정. |
| 4.30 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `Func_148~Func_155` 상세표와 상단 기능요약을 추가하고 `Req_148~Req_155` 추적 범위를 문서 원칙에 반영. |
| 4.29 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `Func_140~Func_147` 상세표와 상단 기능요약을 추가하고 `Req_140~Req_147` 추적 범위를 문서 원칙에 반영. |
| 4.28 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `Func_130~Func_139` 상세표와 상단 기능요약을 추가하고 `Req_130~Req_139` 추적 범위를 문서 원칙에 반영. |
| 4.27 | 2026-03-06 | 용어 정리: `Func_012` 설명을 `고속도로 무조향 의심 경고` 기준으로 통일해 비제품 기능 기반 해석 여지를 제거. |
| 4.26 | 2026-03-06 | 미사용 체인 정리: `Req_108/Func_108` 항목을 Vehicle Baseline 활성 범위에서 제거하고 범위 문구를 `108 제외` 기준으로 동기화. |
| 4.25 | 2026-03-06 | `Func_108` 설명의 특정 상태 예시 표현을 제거하고 운전자 상태 레벨 코드 전달으로 일반화. |
| 4.24 | 2026-03-05 | ECU 명칭 관리 경계를 정리해 03 문서를 ECU 적용 참조로 유지하고, 명명 규칙 SoT를 `00e`로 고정. |
| 4.23 | 2026-03-05 | Validation Harness 노드 명칭을 `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`로 정리해 Req_041~043, Req_112 추적 표기 일관성을 강화. |
| 4.22 | 2026-03-03 | 중간감사 대응 보강: 추적 체인을 `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`로 통일하고, Vehicle Baseline `Req_101~Req_112` 검증 ID를 도메인 단위(`ST_BASE_PT/CH/BODY/IVI`, `IT_BASE_GW`, `ST_BASE_DIAG`)로 세분화. |
| 4.21 | 2026-03-03 | `Func_121/Func_123` 소유 노드를 `WARN_ARB_MGR`로 정정하고 V2 확장(`Func_120~124`) 상태를 Implemented로 전환. Chassis 인벤토리에서 미구현 `DECEL_ASSIST_CTRL` 제거. |
| 4.20 | 2026-03-02 | 감사 정합 보강: 통합구간 1:1 문구 명확화, 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구 추가, V2 확장 행 검증 컬럼을 ST/Flow/Comm ID 기준으로 구체화. |
| 4.19 | 2026-03-02 | V2 확장 제어 책임 분리: `Func_121/Func_123` 실제 노드를 `DECEL_ASSIST_CTRL`로 조정하고 Chassis ECU 인벤토리에 반영. |
| 4.18 | 2026-03-02 | V2 확장 요구 반영: `Func_120~Func_121, Func_123, Func_125~Func_129`(근접위험/감속보조/동기화/운전자개입해제/도메인단절강등) 추가, 작성 원칙의 활성/Pre-Activation 범위 분리, 상단 공식표 확장 항목 반영. |
| 4.17 | 2026-03-02 | 03-하위문서 최종 동기화 준비 반영: `Func_101~Func_119` 설명을 병렬 반영 문구에서 최신 DBC 동기화 운영 문구로 정리. |
| 4.16 | 2026-03-02 | Vehicle Baseline 상단 `검증` 참조 ID 정합화: `Req_113~Req_118`는 `IT_BASE_EXT_BODY_001`, `Req_119`는 `IT_BASE_EXT_IVI_001`로 연결 보정. |
| 4.15 | 2026-03-02 | 본 사이클 추적 범위 고정(`Req_001~043`,`Req_101~119`) 원칙을 작성 원칙에 명시. |
| 4.14 | 2026-03-02 | 0304 변수 계약명 정합화: `Func_101~Func_119` 입력/출력명을 0304 표준 Name 기준으로 보정(`AcCompressorReq`, `DoorUnlockCmd`, `ImmoState`, `TtsLangId` 등)하고 Domain/Test 변수명 불일치(`domainInputFrames`, `baseTestScenario`)를 제거. |
| 4.13 | 2026-03-02 | V2 추적 밀도 보강 1차: 차량 기본 기능 확장 `Func_113~Func_119`(DATC/Seat/Mirror/Door/Wiper-Rain/Security/Audio) 추가 및 `Req_113~Req_119` 1:1 매핑 반영. |
| 4.12 | 2026-03-01 | 표현 명확화 반영: Func_001/003/004/006/012/022/024/025/027/034 문구를 고객 관점 요구(Req_012/022/024/025/027/034)와 정합되도록 보정. |
| 4.2 | 2026-02-25 | 상단 공식 표준 양식 단순화, 하단 상세 추적 표 분리 |
| 4.3 | 2026-02-25 | 옵션1 아키텍처 기준 반영. 출력 경로를 ETH 백본+도메인 GW 구조로 정합화하고 Func_013~016 입출력 정의를 실제 전달체계 기준으로 보정 |
| 4.4 | 2026-02-25 | 상단 공식표 `검증` 열의 TBD 제거. Req/Flow/Comm/Test ID를 행별로 명시해 감사 추적성을 강화 |
| 4.5 | 2026-02-28 | 기능 정의 상세 표의 입출력 변수를 0304 표준 변수명으로 정규화하고 비정의 변수(WarningCond/LastAlertId 등) 제거 |
| 4.6 | 2026-02-28 | Func_014 설명에서 비정의 객체명(`selectedAlertContext`)을 제거하고 0304 표준 변수(`navDirection`) 기준으로 정합화 |
| 4.7 | 2026-02-28 | 스쿨존 과속 정합 강화를 위해 `speedLimit/speedLimitNorm` 입력을 Func_007/Func_010과 상단 입력 표에 반영. |
| 4.8 | 2026-02-28 | 차량 기본 기능 확장 대응으로 `Func_101~Func_112`(시동/기어/페달/창문/비상등/도메인경계 등) 상세 표를 추가. |
| 4.9 | 2026-02-28 | 상단 공식표에 Vehicle Baseline ECU 동작 행을 추가하고, 03 기준 차량 ECU 인벤토리 요약 표를 신설. |
| 4.10 | 2026-02-28 | 06/07 Lean IT 체계와 정합화: 상단 `검증`의 구 IT ID를 `IT_OUT_001`, `IT_EMS_001`로 갱신하고 경보 우선순위 판정/CAN 중재 경계 문구를 작성 원칙에 추가. |
| 4.11 | 2026-03-01 | 멘토 피드백 반영: EMS를 상위 문서에서 단일 논리 단말(`EMS_ALERT`)로 통합 표기하고, 내부 TX/RX 모듈 분리는 하단 매핑표로 분리. |
