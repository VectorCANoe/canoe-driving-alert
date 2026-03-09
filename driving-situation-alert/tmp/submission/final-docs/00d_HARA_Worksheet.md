# HARA 워크시트 (Hazard Analysis and Risk Assessment)

**Document ID**: PROJ-00D-HARA
**ISO 26262 Reference**: Part 3 (Concept Phase, Hazard Analysis and Risk Assessment)
**ASPICE Reference**: SYS.2, SUP.10
**Version**: 1.5
**Date**: 2026-03-07
**Status**: Draft (Submission Summary)
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 제출용 정리본: 원본 SoT에서 HARA 핵심 표와 검증 연결만 유지한 문서입니다.

## 1. 목적 및 범위

본 문서는 프로젝트 주요 위험 상황에 대한 S/E/C 평가, ASIL 후보, Safety Goal, 검증 연결을 정리한다.
본 평가는 SIL 프로젝트 기준의 내부 승인 baseline이다.

## 2. S/E/C 평가 기준(요약)

| 항목 | 레벨 | 의미 |
|---|---|---|
| Severity (S) | S0~S3 | 부상 및 사고 위험의 심각도 |
| Exposure (E) | E0~E4 | 해당 상황에 노출될 가능성 |
| Controllability (C) | C0~C3 | 운전자가 상황을 제어할 수 있는 정도 |

## 3. HARA 상세 워크시트

| HARA ID | 관련 Req | Hazardous Event (요약) | Operational Situation | S | E | C | ASIL Candidate | Safety Goal ID | Safety Goal (안전 목표) | FTTI/Timing 가정 |
|---|---|---|---|---|---|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락 또는 지연으로 감속 시점을 놓침 | 도심 스쿨존, 제한속도 초과 진입 | S2 | E4 | C2 | B (Locked) | SG-01 | 스쿨존에서 제한속도 초과 시 경고가 지연 없이 표시되어야 한다. | 150ms 이내 경고 반영 |
| HC-02 | Req_011, Req_012 | 고속 구간 무조향 의심 경고가 발생하지 않거나 해제되지 않음 | 고속도로 장시간 주행, 조향 입력 부재 또는 복귀 | S3 | E3 | C3 | C (Locked) | SG-02 | 무조향 의심 경고는 조건 성립 시 발생하고, 조향 복귀 시 즉시 해제되어야 한다. | 150ms 이내 발생/해제 |
| HC-03 | Req_022, Req_027~Req_031 | 긴급 경고와 구간 경고가 충돌할 때 우선순위가 잘못 적용됨 | 긴급차량 경고와 구간 경고 동시 발생 | S3 | E3 | C2 | C (Locked) | SG-03 | 중재는 Emergency 우선, Ambulance 우선, ETA, SourceID 순으로 결정되어야 한다. | 150ms 이내 중재 결정 |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃 또는 복귀 전환이 불안정해 경고가 반복 표시됨 | 긴급 신호 무갱신, 긴급 경고에서 구간 경고로 전환되는 상황 | S2 | E4 | C2 | B (Locked) | SG-04 | `1000ms` 무갱신 시 경고를 안전하게 해제하고 정상 상태로 복귀해야 한다. | `1000ms` timeout + `150ms` 복귀 |
| HC-05 | Req_110, Req_111, Req_125~Req_129 | 도메인 경계 또는 게이트웨이 전달 오류로 경고가 끊기거나 강등 동작이 실패함 | 도메인 CAN/ETH 경계 라우팅, 게이트웨이 부하 또는 오류 상황 | S3 | E3 | C2 | C (Locked) | SG-05 | 도메인 경계 전달이 유지되어야 하며, 단절 시 강등 동작이 즉시 적용되어야 한다. | 주기 `100ms/50ms` 연속성 + `150ms` 강등 전환 |
| HC-06 | Req_130~Req_139 | 객체 인지 또는 위험 판단 실패로 위험 경고가 누락되거나 지연됨 | 교차로, 합류, 전방 접근 등 객체 다중 입력 상황 | S3 | E3 | C2 | C (Provisional) | SG-06 | 객체 기반 위험 경고는 TTC, 상대속도, 상대거리, 경로 간섭 조건을 기준으로 정해진 시간 내 발생, 강등, 해제되어야 한다. | 입력 반영 `100ms` + 경고/강등 `150ms` |
| HC-07 | Req_148~Req_152 | 입력 stale 또는 채널 장애 시 경고 연속성과 강등 출력이 유지되지 않음 | 입력 신뢰도 저하, 경로 단절, 출력 채널 일부 장애 | S3 | E3 | C2 | C (Provisional) | SG-07 | 저신뢰 입력은 안전 규칙에 따라 차단 또는 강등되고, 채널 장애 시 대체 경고 채널이 유지되어야 한다. | stale `1000ms` + 전환 `150ms` |
| HC-08 | Req_153~Req_155 | 오디오 경합, 팝업 과밀, 채널 비동기로 경고 인지가 어려워짐 | 다중 HMI 부하, 경고 동시다발 상황 | S2 | E3 | C2 | B (Provisional) | SG-08 | 다중 경고 상황에서도 우선 경고의 인지성과 채널 동기 일관성이 유지되어야 한다. | 인지성/동기 복원 `150ms` |

## 4. Safety Goal -> 검증 링크

| Safety Goal ID | 관련 VC | UT 링크 | IT 링크 | ST 링크 |
|---|---|---|---|---|
| SG-01 | VC_010 | UT_ADAS_001, UT_NAV_001 | IT_CORE_001 | ST_SPEED_001 |
| SG-02 | VC_011, VC_012 | UT_ADAS_001 | IT_CORE_001 | ST_STEER_001 |
| SG-03 | VC_022, VC_027~VC_032 | UT_ARB_001 | IT_ARB_001 | ST_EMS_001, ST_EMS_002, ST_ARB_ETA_001, ST_ARB_ETA_002, ST_POLICY_001 |
| SG-04 | VC_024, VC_033, VC_034 | UT_EMS_RX_001, UT_BCM_001, UT_BND_024_A/B/C | IT_TIMEOUT_001 | ST_TIMEOUT_001, ST_GUIDE_002 |
| SG-05 | VC_110, VC_111, VC_125~VC_129 | UT_BASE_GW_001, UT_V2_FAILSAFE_001 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_V2_FAILSAFE_001 | ST_BASE_001, ST_BASE_PT_001, ST_BASE_CH_001, ST_BASE_BODY_001, ST_BASE_IVI_001, ST_V2_FAILSAFE_001 |
| SG-06 | VC_130~VC_139 | UT_ADAS_OBJ_RISK_001, UT_ADAS_OBJ_SAFETY_001 | IT_ADAS_OBJ_001 | ST_ADAS_OBJ_001 |
| SG-07 | VC_148~VC_152 | UT_BASE_ROBUST_EXT_001 | IT_BASE_ROBUST_EXT_001 | ST_BASE_ROBUST_EXT_001 |
| SG-08 | VC_153~VC_155 | UT_BASE_ALERT_EXT_001, UT_BASE_ROBUST_EXT_001 | IT_BASE_ALERT_EXT_001, IT_BASE_ROBUST_EXT_001 | ST_BASE_ALERT_EXT_001, ST_BASE_ROBUST_EXT_001 |
