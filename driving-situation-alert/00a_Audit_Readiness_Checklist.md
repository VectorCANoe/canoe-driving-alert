# 감사 준비 체크리스트 (Audit Readiness Checklist)

**Document ID**: PROJ-00A-ARC  
**Version**: 1.5  
**Date**: 2026-03-02  
**Status**: Draft  
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 목적
- 감사/멘토 점검 시 문서 체인과 안전/프로세스 근거가 끊기지 않는지 사전 확인한다.
- ISO 26262/ASPICE 관점의 최소 필수 항목만 단일 문서로 요약한다.

## A. 추적성 커버리지 (01 -> 07)

| 항목 | 기준 | 현재 상태 | 판정 |
|---|---|---|---|
| Req 커버리지(03/0301/0302/0303/0304) | 활성 Req(`Req_001~043`, `Req_101~119`) 모두 참조 | 62/62 | OK |
| Func 커버리지(0301/0302/0303/0304) | 활성 Func(`Func_001~043`, `Func_101~119`) 모두 참조 | 62/62 | OK |
| Req 커버리지(05) | 활성 Req 62개 모두 참조 | 55/62 | 보완 필요 |
| Req 커버리지(06) | 활성 Req 62개 모두 참조 | 40/62 | 보완 필요 |
| Req 커버리지(07) | 활성 Req 62개 모두 참조 | 55/62 | 보완 필요 |
| 체인 무결성 | `Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST` | 01~04 체인 정합 확인 | OK |

## B. 요구사항 분류/안전 프로파일 준비도 (ISO 26262 + ASPICE)

| 항목 | 기준 | 상태 | 판정 |
|---|---|---|---|
| 요구 분류 체계 | Req Type/ Safety Class/ HARA Status 운영 | `00c_Req_Classification_and_Safety_Profile.md` 신설 | OK |
| 안전등급 확정 근거 | QM/ASIL은 HARA 근거 기반으로 확정 | 현재 `Provisional` 단계, 확정 HARA 미완료 | 보완 필요 |
| VC 정합 | Req별 VC와 05/06/07 연결 | 01 내 VC 정의 완료, 테스트 증적 일부 미기입 | 보완 필요 |
| ASPICE SYS.2/SYS.3 정합 | 요구(What)와 설계(How) 분리 | 01=What, 03+=How 원칙 유지 | OK |

## C. 문서 버전/날짜 정합

| 문서 | Version | Date | 비고 |
|---|---|---|---|
| `00_VModel_Mapping.md` | 4.3 | 2026-02-28 | V-model 매핑 |
| `00b_Project_Scope.md` | 2.5 | 2026-03-02 | 범위/제외 + 분류 운영 기준 |
| `00c_Req_Classification_and_Safety_Profile.md` | 1.0 | 2026-03-02 | ISO26262/ASPICE 분류 기준 |
| `01_Requirements.md` | 5.14 | 2026-03-02 | Req+VC 기준 |
| `03_Function_definition.md` | 4.14 | 2026-03-02 | 기능 정의 |
| `0301_SysFuncAnalysis.md` | 3.14 | 2026-03-02 | 노드 기능 분석 |
| `0302_NWflowDef.md` | 3.9 | 2026-03-02 | 네트워크 흐름 |
| `0303_Communication_Specification.md` | 3.9 | 2026-03-02 | 통신 명세 |
| `0304_System_Variables.md` | 2.11 | 2026-03-02 | 변수/추적 |
| `04_SW_Implementation.md` | 2.8 | 2026-02-28 | 구현 연결 |
| `05_Unit_Test.md` | 2.7 | 2026-02-28 | UT |
| `06_Integration_Test.md` | 4.8 | 2026-02-28 | IT |
| `07_System_Test.md` | 5.8 | 2026-02-28 | ST |

## D. 범위 경계(고정)

| 구분 | 정책 | 판정 |
|---|---|---|
| 검증 환경 | CANoe SIL only | OK |
| 통신 범위 | CAN + Ethernet(UDP) only | OK |
| 통신 원본 분리 | CAN=`*_can.dbc`, ETH=`ETH_INTERFACE_CONTRACT.md` | OK |
| 중재 용어 경계 | WARN_ARB_MGR는 서비스(QoS) 중재, CAN bit arbitration과 별개 | OK |
| 제외 항목 | OTA/UDS/DoIP | OK |
| 문서 분리 | 01=What, 03+=How, 05~07=Verification | OK |

## E. 제출 전 잔여 항목

| 체크 항목 | 담당 | 상태 |
|---|---|---|
| 05/07의 `Req_113~118` 누락 체인 보강 | Test Lead | TODO |
| 06의 Lean IT 범위와 활성 Req 커버리지 정책 확정(필수/권장 분리) | QA Lead | TODO |
| Req Safety Class 확정(QM/ASIL) 및 HARA 근거 문서화 | Safety Lead | TODO |
| 05/06/07 상단 Pass/Fail, 담당자, 일자 기입 | Validation Lead | TODO |

---

## 메모
- 상단 공식 표는 간결하게 유지하고, 안전/분류/근거는 하단 보강표와 00c에서 관리한다.
- `UT 개수` 자체는 합격 기준이 아니며, 핵심 기준은 Req/VC 커버리지와 체인 무결성이다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.5 | 2026-03-02 | ISO26262/ASPICE 관점 보강: 00c 연계 항목 추가, 활성 Req 62개 기준 추적성/테스트 커버리지 재점검, 제출 전 잔여 항목 재정의. |
| 1.4 | 2026-03-01 | D 섹션 잔여 TODO 3건 종료(07 상단 기록 규칙, 02 이미지 네이밍 고정, 로그/Trace 파일명 규칙 고정). |
| 1.0 | 2026-02-28 | 초기 작성 |
