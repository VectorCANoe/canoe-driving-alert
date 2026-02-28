# 감사 준비 체크리스트 (Audit Readiness Checklist)

**Document ID**: PROJ-00A-ARC  
**Version**: 1.0  
**Date**: 2026-02-28  
**Status**: Draft  
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 목적
- 감사/멘토 점검 시 문서 체인이 끊기지 않는지 사전 확인한다.
- 핵심 확인 항목만 단일 문서로 요약한다.

## A. 추적성 커버리지 (01 -> 07)

| 항목 | 기준 | 현재 상태 | 판정 |
|---|---|---|---|
| Req 커버리지(05) | Req_001~Req_043 모두 참조 | 43/43 | OK |
| Req 커버리지(06) | Req_001~Req_043 모두 참조 | 43/43 | OK |
| Req 커버리지(07) | Req_001~Req_043 모두 참조 | 43/43 | OK |
| VC 커버리지(07) | VC_001~VC_043 모두 참조 | 43/43 | OK |
| 체인 무결성 | Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST | 문서상 연결 확인 | OK |

## B. 문서 버전/날짜 정합

| 문서 | Version | Date | 비고 |
|---|---|---|---|
| `00_VModel_Mapping.md` | 4.3 | 2026-02-28 | V-model 매핑 |
| `00b_Project_Scope.md` | 2.3 | 2026-02-28 | 범위/제외 |
| `01_Requirements.md` | 5.8 | 2026-02-28 | Req+VC 기준 |
| `02_Concept_design.md` | 2.4 | 2026-02-28 | 컨셉/네트워크 그림 중심 |
| `03_Function_definition.md` | 4.7 | 2026-02-28 | 기능 정의 |
| `0301_SysFuncAnalysis.md` | 3.8 | 2026-02-28 | 노드 기능 분석 |
| `0302_NWflowDef.md` | 3.0 | 2026-02-28 | 네트워크 흐름 |
| `0303_Communication_Specification.md` | 2.9 | 2026-02-28 | 통신 명세 |
| `0304_System_Variables.md` | 2.5 | 2026-02-28 | 변수/추적 |
| `04_SW_Implementation.md` | 2.6 | 2026-02-28 | 구현 연결 |
| `05_Unit_Test.md` | 2.4 | 2026-02-28 | UT |
| `06_Integration_Test.md` | 4.4 | 2026-02-28 | IT |
| `07_System_Test.md` | 5.3 | 2026-02-28 | ST |

## C. 범위 경계(고정)

| 구분 | 정책 | 판정 |
|---|---|---|
| 검증 환경 | CANoe SIL only | OK |
| 통신 범위 | CAN + Ethernet(UDP) only | OK |
| 제외 항목 | OTA/UDS/DoIP | OK |
| 문서 분리 | 01=What, 03+=How, 05~07=Verification | OK |

## D. 최종 제출 전 체크

| 체크 항목 | 담당 | 상태 |
|---|---|---|
| 07 상단 Pass/Fail, 담당자, 일자 기입 | Test Lead | TODO |
| 02 최종 이미지 파일명/버전 고정 | Architecture Lead | TODO |
| 실행 로그/Trace 증적 파일명 규칙 확정 | Validation Lead | TODO |

---

## 메모
- 상단 공식 표는 간결하게 유지하고, 추적성/수치/경계값은 하단 상세표에서 관리한다.
- UT 개수와 Func 개수의 단순 비교는 기준이 아니다. 핵심 기준은 Req/VC 커버리지와 체인 무결성이다.
