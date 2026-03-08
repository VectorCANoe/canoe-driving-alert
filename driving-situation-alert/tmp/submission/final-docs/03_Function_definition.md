# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 4.31
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

## 작성 원칙

- 본 문서는 요구사항을 실제 시스템 기능 단위로 분해해 설명한다.
- 기능의 입력, 처리, 출력이 한눈에 보이도록 표 구조를 유지한다.
- 심사자가 기능 범위와 책임 노드를 빠르게 파악할 수 있게 간결하게 작성한다.
- 정책 문서는 별도 문서로 관리하고 본문은 기능 설명에 집중한다.

---

## 기능 정의 표 (공식 표준 양식)

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|---|---|---|---|---|
| 입력 | 구간 정보 | 구간 상태 입력(일반/스쿨존/고속/유도) | Panel/Indicator로 값 입력 | Req_007 |
| 입력 | 유도 방향 | 유도 구간 방향 입력(좌/우) | Panel/Indicator로 값 입력 | Req_014 |
| 입력 | 구간 거리 | 구간 거리 입력 | TrackBar로 값 조절 | Req_013 |
| 입력 | 제한 속도 | 현재 구간 제한속도 입력 | CAN 또는 Panel 입력 | Req_007,Req_010 |
| 입력 | 차량 속도 | 차량 속도 입력 | CAN 또는 Panel 입력 | Req_001,Req_010 |
| 입력 | 조향 입력 | 조향 입력 여부 입력 | CAN 또는 Panel 입력 | Req_011,Req_012 |
| 입력 | 경찰 긴급 활성 | 경찰 긴급 활성 상태 입력 | Switch/Indicator ON/OFF | Req_017 |
| 입력 | 경찰 ETA | 경찰 도달예상시간 입력 | TrackBar로 값 조절 | Req_030 |
| 입력 | 경찰 방향 | 경찰 접근 방향 입력 | Switch/Indicator로 방향 선택 | Req_020 |
| 입력 | 구급 긴급 활성 | 구급 긴급 활성 상태 입력 | Switch/Indicator ON/OFF | Req_017 |
| 입력 | 구급 ETA | 구급 도달예상시간 입력 | TrackBar로 값 조절 | Req_030 |
| 입력 | 구급 방향 | 구급 접근 방향 입력 | Switch/Indicator로 방향 선택 | Req_020 |
| 입력 | 시나리오 선택 | 테스트 시나리오 선택 입력 | 테스트 패널 선택 | Req_041 |
| 출력 | 앰비언트 제어 | 구간/긴급 상태에 따른 앰비언트 출력 | ETH 백본 -> BODY_GW -> CAN 출력 | Req_008~Req_009,Req_013~Req_016,Req_033,Req_034,Req_035,Req_037 |
| 출력 | 클러스터 경고 | 경고 문구 및 상태 출력 | ETH 백본 -> IVI_GW -> CAN 출력 | Req_005,Req_019~Req_021,Req_026,Req_040 |
| 출력 | 경찰 알림 송신 | 경찰 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 |
| 출력 | 구급 알림 송신 | 구급 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 |
| 출력 | 판정 결과 | 시나리오 판정 결과 출력 | 로그/패널 출력 | Req_043 |
| ECU 동작 | 구간 컨텍스트 관리 | 구간/제한속도 입력을 바탕으로 컨텍스트 갱신 | 상태 업데이트 | Req_007,Req_010 |
| ECU 동작 | 경고 조건 판정 | 속도/조향/제한속도 기반 경고 조건 판정 | 경고 트리거 생성 | Req_001~Req_004,Req_006,Req_010~Req_012 |
| ECU 동작 | 경찰 알림 송신 제어 | 경찰 알림 송신 주기 관리 | 송신 상태 관리 | Req_017 |
| ECU 동작 | 구급 알림 송신 제어 | 구급 알림 송신 주기 관리 | 송신 상태 관리 | Req_017 |
| ECU 동작 | 긴급 알림 수신 처리 | 긴급 알림 수신/해제 처리 | 타임아웃 처리 | Req_023,Req_024 |
| ECU 동작 | 경보 우선순위 판정 | 긴급/구간 충돌 시 우선순위 결정 | 중재 결과 산출 | Req_022,Req_025~Req_032 |
| ECU 동작 | 앰비언트 제어 | 경고 패턴/색상 적용 | 패턴 결정 | Req_008,Req_009,Req_013~Req_016,Req_033,Req_034,Req_035,Req_037 |
| ECU 동작 | 클러스터 표시 | 경고 문구/유형 표시 | 문구 결정 | Req_005,Req_019~Req_021,Req_026,Req_040 |
| ECU 동작 | 테스트 실행/판정 | 테스트 시나리오 실행 및 판정 | Pass/Fail 기록 | Req_041~Req_043 |
| ECU 동작 | 엔진 기본 제어 | 시동 입력 기반 엔진 상태 반영 | Vehicle Baseline | Req_101 |
| ECU 동작 | 변속 기본 제어 | 기어 입력(P/R/N/D) 상태 반영 | Vehicle Baseline | Req_102 |
| ECU 동작 | 가속 기본 제어 | 가속 입력 상태 반영 | Vehicle Baseline | Req_103 |
| ECU 동작 | 제동 기본 제어 | 브레이크 입력 상태 반영 | Vehicle Baseline | Req_104 |
| ECU 동작 | 조향 기본 제어 | 조향 입력 상태 반영 | Vehicle Baseline | Req_105 |
| ECU 동작 | 비상등 기본 제어 | 비상등 On/Off 상태 반영 | Vehicle Baseline | Req_106 |
| ECU 동작 | 창문 기본 제어 | 창문 개폐 상태 반영 | Vehicle Baseline | Req_107 |
| ECU 동작 | 클러스터 기본 표시 | 속도/기어/경고 기본 표시 반영 | Vehicle Baseline | Req_109 |
| ECU 동작 | 도메인 게이트웨이 전달 | 도메인 경계 기반 메시지 전달 | Vehicle Baseline | Req_110 |
| ECU 동작 | 도메인 경계 유지 | 도메인 통신 경계/정책 유지 | Vehicle Baseline | Req_111 |
| ECU 동작 | 차량 기본 기능 SIL 검증 | 기본 기능 시나리오 실행/판정 | Vehicle Baseline | Req_112 |
| ECU 동작 | 공조 상태 반영 | HVAC 상태/제어 신호 반영 | Vehicle Baseline | Req_113 |
| ECU 동작 | 시트 상태 반영 | 시트 상태/제어 신호 반영 | Vehicle Baseline | Req_113 |
| ECU 동작 | 미러 상태 반영 | 미러 상태 신호 반영 | Vehicle Baseline | Req_113 |
| ECU 동작 | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태 반영 | Vehicle Baseline | Req_116 |
| ECU 동작 | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태 반영 | Vehicle Baseline | Req_116 |
| ECU 동작 | 보안 상태 반영 | 이모빌라이저/경보 상태 반영 | Vehicle Baseline | Req_118 |
| ECU 동작 | 오디오 상태 반영 | Audio Focus/Voice/TTS 상태 반영 | Vehicle Baseline | Req_119 |
| ECU 동작 | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 위험도 산정 | V2 확장(Implemented) | Req_120 |
| ECU 동작 | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | V2 확장(Implemented) | Req_121 |
| ECU 동작 | 감속 보조 시 긴급경고 최우선 유지 | 감속 보조 활성 시 긴급 경고가 비긴급 경고보다 우선 유지 | V2 확장(Implemented) | Req_125 |
| ECU 동작 | 감속 보조 시 경고 채널 동기화 | 감속 보조 활성 시 Ambient/Cluster 출력 동기화 유지 | V2 확장(Implemented) | Req_126 |
| ECU 동작 | 운전자 개입 우선 해제 | 제동/조향 회피 입력 시 감속 보조 요청 즉시 해제 | V2 확장(Implemented) | Req_123 |
| ECU 동작 | 도메인 단절 시 자동감속 금지 | 도메인 경로 단절 시 자동 감속 보조 요청 생성 금지 | V2 확장(Implemented) | Req_127 |
| ECU 동작 | 도메인 단절 시 최소 경고 유지 | 도메인 경로 단절 시 최소 경고 채널 유지 | V2 확장(Implemented) | Req_128 |
| ECU 동작 | 도메인 단절 시 안전 강등 전환 | 도메인 경로 단절 시 failSafeMode 전환 | V2 확장(Implemented) | Req_129 |
| ECU 동작 | 객체 목록 수용/위험 객체 선정 | 주변 객체 목록 수신 후 대표 위험 객체를 선정 | ADAS 객체 인지 확장(Planned) | Req_130,Req_131 |
| ECU 동작 | TTC/상대속도 기반 위험 단계화 | TTC/상대속도/거리 기반으로 위험 단계를 산정하고 보수 유지시간을 적용 | ADAS 객체 인지 확장(Planned) | Req_132,Req_133,Req_136 |
| ECU 동작 | 교차로/합류 위험 경고 판정 | 교차로 측방 접근 및 합류/끼어들기 위험 경고를 생성하고 기존 경고와 정합 판정 | ADAS 객체 인지 확장(Planned) | Req_134,Req_135,Req_139 |
| ECU 동작 | 신뢰도 기반 강등 및 이벤트 기록 | 객체 신뢰도 저하 시 자동감속 보조 차단/강등 및 이벤트 로깅 | ADAS 객체 인지 확장(Planned) | Req_137,Req_138 |
| ECU 동작 | 방향지시등/안전벨트 기반 경보 맥락 반영 | 방향지시등/안전벨트 상태를 경보 맥락 및 강조 정책에 반영 | 차량 경보 편의 확장(Planned) | Req_140,Req_142 |
| ECU 동작 | 주행모드 기반 경보 민감도 반영 | 주행 모드에 따라 경보 민감도 프로파일을 보정 | 차량 경보 편의 확장(Planned) | Req_141 |
| ECU 동작 | 접근거리 표시/이벤트 이력 관리 | 긴급차량 접근 거리 표시와 경보 이벤트 기록·이력 조회를 제공 | 차량 경보 편의 확장(Planned) | Req_143,Req_144,Req_145 |
| ECU 동작 | 표시 방식/음량 설정 반영 | 경보 표시 방식/음량 설정을 HMI 출력 정책에 반영 | 차량 경보 편의 확장(Planned) | Req_146,Req_147 |
| ECU 동작 | 경고 입력 유효성/신선도 보호 | 경고 판정 입력의 유효성/신선도를 검사하고 stale·저신뢰 입력에 보수 정책을 적용 | 경고 강건성·인지성 확장(Planned) | Req_148,Req_149 |
| ECU 동작 | 경고 안정화/채널 가용성·대체·인지성/동기 관리 | 상태전이 안정화, 출력 채널 가용성 판정, 대체 출력 유지, 오디오 경합/팝업 과밀 제어, 채널 동기 일관성 관리 | 경고 강건성·인지성 확장(Planned) | Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 |

- 상단 공식표의 `검증` 열은 요구사항 식별자 기준으로 유지한다.

---

## 기능군 요약

| 기능군 | 상태 | 설명 |
|---|---|---|
| 통합 기본 기능 | Active | 주행/구간/긴급 입력을 경보로 판정하고 Amb/Cluster로 출력 |
| 검증 하네스 기능 | Active | SIL 시나리오 실행, 판정, 결과 기록 |
| 차량 기본 기능 확장 | Active | 기본 차량 상태(시동/기어/가감속/조향/차체/표시) 연동 |
| V2 확장 | Implemented | 위험도 기반 감속 보조 및 fail-safe 정책 |
| ADAS 객체 인지 확장 | Planned | 객체 목록 기반 TTC/교차로/합류 위험 경고 |
| 차량 경보 편의 확장 | Planned | 표시/음량 설정, 접근거리 표시, 이벤트 이력 |
| 경고 강건성/인지성 확장 | Planned | 입력 유효성, 채널 대체, 경고 인지성 보호 |

## 경고 표시 정책표 요약 (Req_008, Req_035, Req_037)

| selectedAlertType | 의미 | ambientMode | ambientColor | ambientPattern |
|---|---|---:|---:|---:|
| 0 | Off | 0 | 0 | 0 |
| 1 | Police | 2 | 1/5 교차 | 2 |
| 2 | Ambulance | 2 | 1/6 교차 | 2 |
| 3 | School Zone | 2 | 1 | 3 |
| 4 | Highway (무조향 의심) | 2 | 2 | 1 |
| 5 | Guide Left | 1 | 4 | 1 |
| 6 | Guide Right | 1 | 4 | 2 |

- `warningTextCode` 정책: `timeoutClear == 0` 이고 `selectedAlertLevel > 0`이면 `selectedAlertType*10 + selectedAlertLevel`, 그 외는 `0`.
- 상세 코드 사전(`ambientColor`, `ambientPattern`, `ambientMode`)은 통신/변수 문서와 동일 규칙으로 유지한다.

---
