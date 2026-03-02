# HARA 워크시트 (Hazard Analysis and Risk Assessment)

**Document ID**: PROJ-00D-HARA  
**ISO 26262 Reference**: Part 3 (Concept Phase, Hazard Analysis and Risk Assessment)  
**ASPICE Reference**: SYS.2 (요구 근거), SUP.10 (추적성)  
**Version**: 1.1  
**Date**: 2026-03-02  
**Status**: Draft  
**Project Title**: 주행 상황 실시간 경고 시스템  
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 목적 및 범위
- 본 문서는 00c의 HARA 후보(`HC-01~HC-05`)에 대해 S/E/C 평가값, Safety Goal, 검증 연결을 명시한다.
- 본 평가는 SIL 프로젝트 기준의 **초안(working baseline)**이며, 실차/양산 확정 ASIL 평가는 별도 안전심의에서 확정한다.

## 2. S/E/C 평가 기준(요약)

| 항목 | 레벨 | 의미(요약) |
|---|---|---|
| Severity (S) | S0~S3 | 부상/사망 위험의 심각도 |
| Exposure (E) | E0~E4 | 운전 중 해당 상황 노출 빈도 |
| Controllability (C) | C0~C3 | 운전자가 위험 상황을 통제 가능한 정도 |

운영 규칙:
- 본 문서의 `ASIL Candidate`는 설계 우선순위 결정을 위한 임시값이다.
- ASIL 확정은 HARA 리뷰 회의에서 근거(시나리오, 운행조건, 제어가능성)를 첨부해 잠근다.

## 3. HARA 상세 워크시트 (HC-01~HC-05)

| HARA ID | 관련 Req | Hazardous Event (요약) | Operational Situation | S | E | C | ASIL Candidate | Safety Goal ID | Safety Goal (안전 목표) | FTTI/Timing 가정 |
|---|---|---|---|---|---|---|---|---|---|---|
| HC-01 | Req_010 | 스쿨존 과속 경고 누락/지연으로 운전자 감속 타이밍 상실 | 도심 스쿨존(고빈도), 제한속도 초과 진입 | S2 | E4 | C2 | B (Provisional) | SG-01 | 스쿨존에서 `vehicleSpeed > speedLimit` 성립 시 경고가 지연 없이 표시되어야 한다. | 150ms 이내 경고 반영 |
| HC-02 | Req_011, Req_012 | 고속 구간 무조향 경고 미발생/해제 실패로 주의저하 상태 지속 | 고속도로 장시간 주행, 조향 입력 부재/복귀 | S3 | E3 | C3 | C (Provisional) | SG-02 | 무조향 경고는 조건 성립 시 발생하고, 조향 복귀 시 즉시 해제되어야 한다. | 150ms 이내 발생/해제 |
| HC-03 | Req_022, Req_027~Req_031 | 중재 규칙 오류로 긴급경고 미우선/오선택 표시 | 긴급차량 경고와 구간경고 동시 발생, 다중 긴급 충돌 | S3 | E3 | C2 | C (Provisional) | SG-03 | 중재는 Emergency>Zone, Ambulance>Police, ETA, SourceID 순으로 결정론적으로 동작해야 한다. | 150ms 이내 중재 결정 |
| HC-04 | Req_024, Req_033, Req_034 | 타임아웃/복귀/전환 불안정으로 경고 반복 깜빡임 및 운전자 혼란 | 긴급 신호 무갱신, 긴급->구간 전환 구간 | S2 | E4 | C2 | B (Provisional) | SG-04 | `1000ms` 무갱신 시 안전 해제 후 안정 복귀하고 반복 점멸 없이 전환되어야 한다. | 1000ms timeout + 150ms 복귀 |
| HC-05 | Req_110, Req_111 | 도메인 경계/게이트웨이 전달 오류로 경고 체인 단절 | 도메인 CAN/ETH 경계 라우팅, Gateway 부하/오류 상황 | S3 | E3 | C2 | C (Provisional) | SG-05 | 도메인 경계 정책을 유지하며 입력/출력 라우팅 체인이 단절되지 않아야 한다. | 주기 100ms/50ms 연속성 유지 |

## 4. Safety Goal -> 검증 링크

| Safety Goal ID | 관련 VC | UT 링크 | IT 링크 | ST 링크 | 증적 경로(기록 위치) |
|---|---|---|---|---|---|
| SG-01 | VC_010 | UT_ADAS_001, UT_NAV_001 | IT_CORE_001 | ST_SPEED_001 | `canoe/logs/system/ST_SPEED_001/*` |
| SG-02 | VC_011, VC_012 | UT_ADAS_001 | IT_CORE_001 | ST_STEER_001 | `canoe/logs/system/ST_STEER_001/*` |
| SG-03 | VC_022, VC_027~VC_032 | UT_ARB_001 | IT_ARB_001 | ST_EMS_001, ST_EMS_002, ST_ARB_ETA_001, ST_ARB_ETA_002, ST_POLICY_001 | `canoe/logs/system/ST_ARB_ETA_*/`, `canoe/logs/system/ST_EMS_*/` |
| SG-04 | VC_024, VC_033, VC_034 | UT_EMS_RX_001, UT_BCM_001, UT_BND_024_A/B/C | IT_TIMEOUT_001 | ST_TIMEOUT_001, ST_GUIDE_002 | `canoe/logs/system/ST_TIMEOUT_001/*` |
| SG-05 | VC_110, VC_111 | UT_BASE_GW_001 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001 | ST_BASE_001, ST_BASE_PT_001, ST_BASE_CH_001, ST_BASE_BODY_001, ST_BASE_IVI_001 | `canoe/logs/system/ST_BASE_*/` |

## 5. 현재 판단과 남은 작업

| 항목 | 현재 상태 | 다음 조치 |
|---|---|---|
| HARA 후보 5건 S/E/C 입력 | 완료 (초안) | 안전 리뷰에서 근거 문장 보강 |
| ASIL Candidate 정의 | 완료 (Provisional) | HARA 회의 후 확정/조정 |
| Safety Goal 정의 | 완료 (SG-01~SG-05) | 04 구현 정책과 양방향 링크 검증 |
| 검증 링크(VC/UT/IT/ST) | 완료 | 실제 Pass/Fail 증적 파일 경로 채우기 |

## 6. HARA 승인 게이트 (01~07 착수 전)

| 항목 | 담당 | 기준 | 상태 | 승인일 |
|---|---|---|---|---|
| S/E/C 값 검토 | Safety Lead | HC-01~HC-05의 S/E/C 근거 문장 확인 | TODO |  |
| ASIL Candidate 검토 | Safety Lead | ASIL Candidate(B/C) 타당성 확인 | TODO |  |
| Safety Goal 잠금 | System Lead | SG-01~SG-05 문구/범위 확정 | TODO |  |
| 검증 링크 검토 | Validation Lead | SG별 VC/UT/IT/ST 링크 유효성 확인 | TODO |  |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.1 | 2026-03-02 | 01~07 착수 전 HARA 승인 게이트(담당/기준/상태/승인일) 표 추가. |
| 1.0 | 2026-03-02 | 신규 작성: HC-01~HC-05 S/E/C, ASIL Candidate, Safety Goal, VC/UT/IT/ST 검증 링크 정의. |
