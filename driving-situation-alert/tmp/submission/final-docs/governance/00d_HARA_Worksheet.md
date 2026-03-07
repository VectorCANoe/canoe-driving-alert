# HARA 워크시트 (Hazard Analysis and Risk Assessment)

**Document ID**: PROJ-00D-HARA  
**ISO 26262 Reference**: Part 3 (Concept Phase, Hazard Analysis and Risk Assessment)  
**ASPICE Reference**: SYS.2 (요구 근거), SUP.10 (추적성)  
**Version**: 1.4  
**Date**: 2026-03-04  
**Status**: Draft (Internal Baseline Approved)  
**Project Title**: 주행 상황 실시간 경고 시스템  
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 3. HARA 상세 워크시트 (HC-01~HC-05)

| HARA ID | 관련 Req | Hazardous Event (요약) | Operational Situation | S | E | C | ASIL Candidate | Safety Goal ID | Safety Goal (안전 목표) | FTTI/Timing 가정 |
|---|---|---|---|---|---|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연으로 운전자 감속 타이밍 상실 | 도심 스쿨존(고빈도), 제한속도 초과 진입 | S2 | E4 | C2 | B (Locked) | SG-01 | 스쿨존에서 `vehicleSpeed > speedLimit` 성립 시 경고가 지연 없이 표시되어야 한다. | 150ms 이내 경고 반영 |
| HC-02 | Req_011, Req_012 | 고속 구간 무조향 의심 경고 미발생/해제 실패로 주의저하 의심 상태 관리 실패 | 고속도로 장시간 주행, 조향 입력 부재/복귀 | S3 | E3 | C3 | C (Locked) | SG-02 | 무조향 의심 경고는 조건 성립 시 발생하고, 조향 복귀 시 즉시 해제되어야 한다. | 150ms 이내 발생/해제 |
| HC-03 | Req_022, Req_027~Req_031 | 중재 규칙 오류로 긴급경고 미우선/오선택 표시 | 긴급차량 경고와 구간경고 동시 발생, 다중 긴급 충돌 | S3 | E3 | C2 | C (Locked) | SG-03 | 중재는 Emergency>Zone, Ambulance>Police, ETA, SourceID 순으로 결정론적으로 동작해야 한다. | 150ms 이내 중재 결정 |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃/복귀/전환 불안정으로 경고 반복 깜빡임 및 운전자 혼란 | 긴급 신호 무갱신, 긴급->구간 전환 구간 | S2 | E4 | C2 | B (Locked) | SG-04 | `1000ms` 무갱신 시 안전 해제 후 안정 복귀하고 반복 점멸 없이 전환되어야 한다. | 1000ms timeout + 150ms 복귀 |
| HC-05 | Req_110, Req_111, Req_124 | 도메인 경계/게이트웨이 전달 오류로 경고 체인 단절 또는 강등 정책 미동작 | 도메인 CAN/ETH 경계 라우팅, Gateway 부하/오류 상황 | S3 | E3 | C2 | C (Locked) | SG-05 | 도메인 경계 정책을 유지하며 입력/출력 라우팅 체인이 단절되지 않아야 하고, 단절 시 fail-safe 강등이 즉시 적용되어야 한다. | 주기 100ms/50ms 연속성 + 150ms 강등 전환 |

## 4. Safety Goal -> 검증 링크

| Safety Goal ID | 관련 VC | UT 링크 | IT 링크 | ST 링크 | 증적 경로(기록 위치) |
|---|---|---|---|---|---|
| SG-01 | VC_010 | UT_ADAS_001, UT_NAV_001 | IT_CORE_001 | ST_SPEED_001 | `canoe/logs/system/ST_SPEED_001/*` |
| SG-02 | VC_011, VC_012 | UT_ADAS_001 | IT_CORE_001 | ST_STEER_001 | `canoe/logs/system/ST_STEER_001/*` |
| SG-03 | VC_022, VC_027~VC_032 | UT_ARB_001 | IT_ARB_001 | ST_EMS_001, ST_EMS_002, ST_ARB_ETA_001, ST_ARB_ETA_002, ST_POLICY_001 | `canoe/logs/system/ST_ARB_ETA_*/`, `canoe/logs/system/ST_EMS_*/` |
| SG-04 | VC_024, VC_033, VC_034 | UT_EMS_RX_001, UT_BCM_001, UT_BND_024_A/B/C | IT_TIMEOUT_001 | ST_TIMEOUT_001, ST_GUIDE_002 | `canoe/logs/system/ST_TIMEOUT_001/*` |
| SG-05 | VC_110, VC_111, VC_124 | UT_BASE_GW_001, UT_V2_FAILSAFE_001 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_V2_FAILSAFE_001 | ST_BASE_001, ST_BASE_PT_001, ST_BASE_CH_001, ST_BASE_BODY_001, ST_BASE_IVI_001, ST_V2_FAILSAFE_001 | `canoe/logs/system/ST_BASE_*/`, `canoe/logs/system/ST_V2_FAILSAFE_001/*` |

