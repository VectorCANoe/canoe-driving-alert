# HARA 워크시트 (Hazard Analysis and Risk Assessment)

**Document ID**: PROJ-00D-HARA  
**ISO 26262 Reference**: Part 3 (Concept Phase, Hazard Analysis and Risk Assessment)  
**ASPICE Reference**: SYS.2 (요구 근거), SUP.10 (추적성)  
**Version**: 1.5  
**Date**: 2026-03-07  
**Status**: Draft (Active Baseline Approved + Pre-Activation In Progress)  
**Project Title**: 주행 상황 실시간 경고 시스템  
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 목적 및 범위
- 본 문서는 00c의 HARA 후보(`HC-01~HC-08`)에 대해 S/E/C 평가값, Safety Goal, 검증 연결을 명시한다.
- 본 평가는 SIL 프로젝트 기준의 **내부 승인 baseline**이며, 실차/양산 확정 ASIL 평가는 별도 안전심의에서 확정한다.

## 2. S/E/C 평가 기준(요약)

| 항목 | 레벨 | 의미(요약) |
|---|---|---|
| Severity (S) | S0~S3 | 부상/사망 위험의 심각도 |
| Exposure (E) | E0~E4 | 운전 중 해당 상황 노출 빈도 |
| Controllability (C) | C0~C3 | 운전자가 위험 상황을 통제 가능한 정도 |

운영 규칙:
- 본 문서의 `ASIL Candidate`는 설계 우선순위 결정을 위한 임시값이다.
- ASIL 확정은 HARA 리뷰 회의에서 근거(시나리오, 운행조건, 제어가능성)를 첨부해 잠근다.

## 3. HARA 상세 워크시트 (HC-01~HC-08)

| HARA ID | 관련 Req | Hazardous Event (요약) | Operational Situation | S | E | C | ASIL Candidate | Safety Goal ID | Safety Goal (안전 목표) | FTTI/Timing 가정 |
|---|---|---|---|---|---|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연으로 운전자 감속 타이밍 상실 | 도심 스쿨존(고빈도), 제한속도 초과 진입 | S2 | E4 | C2 | B (Locked) | SG-01 | 스쿨존에서 `vehicleSpeed > speedLimit` 성립 시 경고가 지연 없이 표시되어야 한다. | 150ms 이내 경고 반영 |
| HC-02 | Req_011, Req_012 | 고속 구간 무조향 의심 경고 미발생/해제 실패로 주의저하 의심 상태 관리 실패 | 고속도로 장시간 주행, 조향 입력 부재/복귀 | S3 | E3 | C3 | C (Locked) | SG-02 | 무조향 의심 경고는 조건 성립 시 발생하고, 조향 복귀 시 즉시 해제되어야 한다. | 150ms 이내 발생/해제 |
| HC-03 | Req_022, Req_027~Req_031 | 중재 규칙 오류로 긴급경고 미우선/오선택 표시 | 긴급차량 경고와 구간경고 동시 발생, 다중 긴급 충돌 | S3 | E3 | C2 | C (Locked) | SG-03 | 중재는 Emergency>Zone, Ambulance>Police, ETA, SourceID 순으로 결정론적으로 동작해야 한다. | 150ms 이내 중재 결정 |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃/복귀/전환 불안정으로 경고 반복 깜빡임 및 운전자 혼란 | 긴급 신호 무갱신, 긴급->구간 전환 구간 | S2 | E4 | C2 | B (Locked) | SG-04 | `1000ms` 무갱신 시 안전 해제 후 안정 복귀하고 반복 점멸 없이 전환되어야 한다. | 1000ms timeout + 150ms 복귀 |
| HC-05 | Req_110, Req_111, Req_125~Req_129 | 도메인 경계/게이트웨이 전달 오류로 경고 체인 단절 또는 강등 정책 미동작 | 도메인 CAN/ETH 경계 라우팅, Gateway 부하/오류 상황 | S3 | E3 | C2 | C (Locked) | SG-05 | 도메인 경계 정책을 유지하며 입력/출력 라우팅 체인이 단절되지 않아야 하고, 단절 시 fail-safe 강등이 즉시 적용되어야 한다. | 주기 100ms/50ms 연속성 + 150ms 강등 전환 |
| HC-06 | Req_130~Req_139 | 객체 인지/위험판정 실패로 위험 객체 경고가 누락되거나 지연됨 | 교차로/합류/전방 접근 상황, 객체 다중 입력 환경 | S3 | E3 | C2 | C (Provisional, Pre-Activation) | SG-06 | 객체 기반 위험 경고는 TTC/상대속도/상대거리/경로 간섭 조건을 기준으로 정해진 시간 내 발생/강등/해제되어야 한다. | 입력 반영 100ms + 경고/강등 150ms |
| HC-07 | Req_148~Req_152 | 입력 stale/채널 장애 시 경고 연속성 및 fail-safe 출력 상실 | 입력 신뢰도 저하, 경로 단절, 출력 채널 일부 장애 | S3 | E3 | C2 | C (Provisional, Pre-Activation) | SG-07 | 저신뢰/미갱신 입력은 안전 규칙에 따라 차단/강등되고, 채널 장애 시 대체 경고 채널이 연속 유지되어야 한다. | stale 1000ms + 전환 150ms |
| HC-08 | Req_153~Req_155 | 오디오 경합/팝업 과밀/채널 비동기로 경고 인지 실패 | 다중 HMI 부하, 경고 동시다발 상황 | S2 | E3 | C2 | B (Provisional, Pre-Activation) | SG-08 | 오디오 경합/표시 과밀 상황에서도 우선 경고 인지성과 채널 동기 일관성이 유지되어야 한다. | 인지성/동기 복원 150ms |

## 4. Safety Goal -> 검증 링크

| Safety Goal ID | 관련 VC | UT 링크 | IT 링크 | ST 링크 | 증적 경로(기록 위치) |
|---|---|---|---|---|---|
| SG-01 | VC_010 | UT_ADAS_001, UT_NAV_001 | IT_CORE_001 | ST_SPEED_001 | `canoe/logs/system/ST_SPEED_001/*` |
| SG-02 | VC_011, VC_012 | UT_ADAS_001 | IT_CORE_001 | ST_STEER_001 | `canoe/logs/system/ST_STEER_001/*` |
| SG-03 | VC_022, VC_027~VC_032 | UT_ARB_001 | IT_ARB_001 | ST_EMS_001, ST_EMS_002, ST_ARB_ETA_001, ST_ARB_ETA_002, ST_POLICY_001 | `canoe/logs/system/ST_ARB_ETA_*/`, `canoe/logs/system/ST_EMS_*/` |
| SG-04 | VC_024, VC_033, VC_034 | UT_EMS_RX_001, UT_BCM_001, UT_BND_024_A/B/C | IT_TIMEOUT_001 | ST_TIMEOUT_001, ST_GUIDE_002 | `canoe/logs/system/ST_TIMEOUT_001/*` |
| SG-05 | VC_110, VC_111, VC_125~VC_129 | UT_BASE_GW_001, UT_V2_FAILSAFE_001 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_V2_FAILSAFE_001 | ST_BASE_001, ST_BASE_PT_001, ST_BASE_CH_001, ST_BASE_BODY_001, ST_BASE_IVI_001, ST_V2_FAILSAFE_001 | `canoe/logs/system/ST_BASE_*/`, `canoe/logs/system/ST_V2_FAILSAFE_001/*` |
| SG-06 | VC_130~VC_139 | UT_ADAS_OBJ_RISK_001, UT_ADAS_OBJ_SAFETY_001 | IT_ADAS_OBJ_001 | ST_ADAS_OBJ_001 | `canoe/logs/system/ST_ADAS_OBJ_001/*` |
| SG-07 | VC_148~VC_152 | UT_BASE_ROBUST_EXT_001 | IT_BASE_ROBUST_EXT_001 | ST_BASE_ROBUST_EXT_001 | `canoe/logs/system/ST_BASE_ROBUST_EXT_001/*` |
| SG-08 | VC_153~VC_155 | UT_BASE_ALERT_EXT_001, UT_BASE_ROBUST_EXT_001 | IT_BASE_ALERT_EXT_001, IT_BASE_ROBUST_EXT_001 | ST_BASE_ALERT_EXT_001, ST_BASE_ROBUST_EXT_001 | `canoe/logs/system/ST_BASE_ALERT_EXT_001/*`, `canoe/logs/system/ST_BASE_ROBUST_EXT_001/*` |

## 5. 현재 판단과 남은 작업

| 항목 | 현재 상태 | 다음 조치 |
|---|---|---|
| HARA 후보 8건 S/E/C 입력 | HC-01~HC-05 완료, HC-06~HC-08 진행중 | HC-06~HC-08 내부 잠금(근거 문장 + 회의록 근거) |
| ASIL Candidate 정의 | HC-01~HC-05 Locked, HC-06~HC-08 Provisional | Pre-Activation 종료 시 최종 잠금/조정 |
| Safety Goal 정의 | SG-01~SG-05 Locked, SG-06~SG-08 Pre-Activation | 04 구현 정책과 양방향 링크 검증 |
| 검증 링크(VC/UT/IT/ST) | Active 체인 완료, Pre-Activation 체인 계획 반영 | 실제 Pass/Fail 증적 파일 경로 채우기 |

## 6. HARA 승인 게이트 (01~07 착수 전)

| 항목 | 담당 | 기준 | 상태 | 승인일 |
|---|---|---|---|---|
| S/E/C 값 검토 | Safety Lead | HC-01~HC-05 근거 문장 승인 + HC-06~HC-08 초안 검토 | Partial Approved (Active Locked) | 2026-03-07 |
| ASIL Candidate 검토 | Safety Lead | Active(B/C) 잠금 + Pre-Activation Provisional 등급 타당성 검토 | Partial Approved (Active Locked) | 2026-03-07 |
| Safety Goal 잠금 | System Lead | SG-01~SG-05 확정 + SG-06~SG-08 초안 확정 | Partial Approved (Active Locked) | 2026-03-07 |
| 검증 링크 검토 | Validation Lead | Active 링크 승인 + Pre-Activation 링크(Planned) 유효성 확인 | Partial Approved (Active Locked) | 2026-03-07 |

내부 승인 경계:
- 본 게이트의 `Approved`는 프로젝트 내부 기준선 잠금을 의미한다.
- ISO 26262 인증/법규 인증의 최종 승인 효력은 포함하지 않는다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.5 | 2026-03-07 | HARA 범위 확장 반영: `HC-06~HC-08`/`SG-06~SG-08` 추가, `Req_125~129` 반영으로 HC-05 범위를 갱신. Active(내부 잠금)와 Pre-Activation(진행중) 게이트를 분리 표기. |
| 1.4 | 2026-03-06 | 용어 정리: HC-02/SG-02 문구를 `고속 무조향 기반 주의저하 의심 경고` 기준으로 통일하고 비제품 기능 오해 여지를 제거. |
| 1.3 | 2026-03-04 | HARA 승인 게이트 4개 항목을 내부 Baseline 승인 상태로 전환하고 승인일을 기록. 상태 문구를 `초안`에서 `내부 승인 baseline`으로 갱신. |
| 1.2 | 2026-03-02 | 중간감사 운영 반영: HARA 승인 게이트 상태를 `TODO`에서 `Planned(중간감사 후 확정/증적 잠금)`으로 갱신. |
| 1.1 | 2026-03-02 | 01~07 착수 전 HARA 승인 게이트(담당/기준/상태/승인일) 표 추가. |
| 1.0 | 2026-03-02 | 신규 작성: HC-01~HC-05 S/E/C, ASIL Candidate, Safety Goal, VC/UT/IT/ST 검증 링크 정의. |
