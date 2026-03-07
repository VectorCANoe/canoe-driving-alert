# 감사 준비 체크리스트 (Audit Readiness Checklist)

**Document ID**: PROJ-00A-ARC  
**Version**: 1.13  
**Date**: 2026-03-07  
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
| Req 커버리지(활성 전환) | 활성 Req 66개 모두 참조 | 66/66 | OK |
| Req 커버리지(Pre-Activation) | 확장 Req(`Req_130~155`) 모두 참조 | 26/26 | OK |
| Req 커버리지(05) | 활성/확장 Req 체인 참조 유지 | 66/66 + 26/26 | OK |
| Req 커버리지(06) | 활성/확장 Req 체인 참조 유지 | 66/66 + 26/26 | OK |
| Req 커버리지(07) | 활성/확장 Req 체인 참조 유지 | 66/66 + 26/26 | OK |
| 체인 무결성 | `Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST` | Active Locked + Pre-Activation Planned 정합 확인 | OK |

## B. 요구사항 분류/안전 프로파일 준비도 (ISO 26262 + ASPICE)

| 항목 | 기준 | 상태 | 판정 |
|---|---|---|---|
| 요구 분류 체계 | Req Type/ Safety Class/ HARA Status 운영 | `00c_Req_Classification_and_Safety_Profile.md` 신설 | OK |
| 안전등급 확정 근거 | QM/ASIL은 HARA 근거 기반으로 확정 | Active는 `00d` 내부 승인 잠금, Pre-Activation은 Provisional 유지 | OK |
| VC 정합 | Req별 VC와 05/06/07 연결 | 01 내 VC 정의 완료, 테스트 증적 일부 미기입 | 보완 필요 |
| ASPICE SYS.2/SYS.3 정합 | 요구(What)와 설계(How) 분리 | 01=What, 03+=How 원칙 유지 | OK |

### B-1. 적용 수준/주장 경계 (Audit Claim Boundary)

| 항목 | 현재 선언 | 판정 |
|---|---|---|
| ISO 26262/ASPICE 인증 주장 | 하지 않음 (SIL 실무형 운영 기준만 적용) | OK |
| Safety Class 확정 상태 | Active 범위 잠금 완료, Pre-Activation(HC-06~08) 진행중 | OK |
| 감사 대응 목표 | 체인 무결성 + 분류/근거 일관성 | OK |

## C. 문서 버전/날짜 정합

| 문서 | Version | Date | 비고 |
|---|---|---|---|
| `00_VModel_Mapping.md` | 4.3 | 2026-02-28 | V-model 매핑 |
| `00b_Project_Scope.md` | 2.8 | 2026-03-05 | 범위/제외 + 분류 운영 기준 |
| `00c_Req_Classification_and_Safety_Profile.md` | 1.7 | 2026-03-07 | ISO26262/ASPICE 분류 기준(Active/Pre-Activation 분리) |
| `00d_HARA_Worksheet.md` | 1.5 | 2026-03-07 | HC-01~HC-08 S/E/C + Safety Goal + 승인 게이트 |
| `00e_ECU_Naming_Standard.md` | 2.7 | 2026-03-05 | ECU Canonical/약어 표준 |
| `00f_CAN_ID_Allocation_Standard.md` | 3.6 | 2026-03-07 | 3/3/5 ID 정책 SoT |
| `00g_RTE_Name_Mapping_Standard.md` | 1.1 | 2026-03-05 | AUTOSAR RTE 네이밍 매핑 |
| `01_Requirements.md` | 5.30 | 2026-03-06 | Req+VC 기준 |
| `03_Function_definition.md` | 4.31 | 2026-03-06 | 기능 정의 |
| `0301_SysFuncAnalysis.md` | 3.27 | 2026-03-06 | 노드 기능 분석 |
| `0302_NWflowDef.md` | 3.24 | 2026-03-07 | 네트워크 흐름 |
| `0303_Communication_Specification.md` | 3.27 | 2026-03-07 | 통신 명세 |
| `0304_System_Variables.md` | 2.24 | 2026-03-06 | 변수/추적 |
| `04_SW_Implementation.md` | 2.22 | 2026-03-06 | 구현 연결 |
| `05_Unit_Test.md` | 2.21 | 2026-03-06 | UT |
| `06_Integration_Test.md` | 4.19 | 2026-03-06 | IT |
| `07_System_Test.md` | 5.19 | 2026-03-06 | ST |

## D. 범위 경계(고정)

| 구분 | 정책 | 판정 |
|---|---|---|
| 검증 환경 | CANoe SIL only | OK |
| 통신 범위 | CAN + Ethernet(UDP) only | OK |
| 통신 원본 분리 | CAN=`*_can.dbc`, ETH=`ETH_INTERFACE_CONTRACT.md` | OK |
| 중재 용어 경계 | WARN_ARB_MGR는 경보 우선순위 판정, CAN bit arbitration과 별개 | OK |
| 제외 항목 | OTA/UDS/DoIP | OK |
| 문서 분리 | 01=What, 03+=How, 05~07=Verification | OK |

## E. 제출 전 잔여 항목

| 체크 항목 | 담당 | 상태 |
|---|---|---|
| 05/06/07 확장 요구(`Req_130~155`) 커버리지 유지 점검 | Test Lead | DONE (26/26) |
| 활성 전환 Req 커버리지 정책 잠금 | QA Lead | DONE (66/66) |
| HARA 후보(HC-01~HC-05) S/E/C 평가 및 ASIL Candidate 승인 | Safety Lead | DONE (내부 Baseline 승인) |
| HARA 후보(HC-06~HC-08) S/E/C 확정 및 잠금 | Safety Lead | TODO (Pre-Activation 종료 시) |
| Req Safety Class 확정(QM/ASIL) 및 HARA 근거 문서화 | Safety Lead | PARTIAL (Active 완료, Pre-Activation 진행중) |
| 05/06/07 상단 Pass/Fail, 담당자, 일자 기입 | Validation Lead | TODO |

## F. 01~07 착수 전 고정값 (이번 사이클)

| 항목 | 고정 내용 | 상태 |
|---|---|---|
| HARA 승인 게이트 | `00d_HARA_Worksheet.md` 6절 기준으로 Active(승인), Pre-Activation(진행중) 분리 운영 | DONE |
| 검증 증적 경로 규칙 | UT/IT/ST 증적 경로를 `canoe/logging/evidence/{UT\\|IT\\|ST}/...`로 고정 | Locked |
| 활성 Req 범위 고정 | 이번 사이클 활성 범위는 66개(`Req_001~043`, `Req_101~107`, `Req_109~113`, `Req_116`, `Req_118~121`, `Req_123`, `Req_125~129`)로 잠금 | Locked |
| 확장 Req 범위 고정 | Pre-Activation 범위는 `Req_130~155`(26개)로 운영 | Locked |

---

## 메모
- 상단 공식 표는 간결하게 유지하고, 안전/분류/근거는 하단 보강표와 00c에서 관리한다.
- `UT 개수` 자체는 합격 기준이 아니며, 핵심 기준은 Req/VC 커버리지와 체인 무결성이다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.13 | 2026-03-07 | 감사 기준 최신화: 활성 전환 Req(66) + Pre-Activation Req(26) 이중 커버리지 표기로 개편, 문서 버전 매트릭스를 00~07 최신 버전으로 동기화, HARA 상태를 Active 잠금/Pre-Activation 진행중으로 분리. |
| 1.12 | 2026-03-04 | Lean IT 범위(활성 Req 67개) 고정, HARA/ASIL 내부 승인 완료 상태 반영, 문서 버전 매트릭스 최신화(0302/0303/0304/04 포함). |
| 1.11 | 2026-03-02 | ISO26262/ASPICE 우선 정합 반영: 00c(1.3), 0304(2.12), 04(2.10) 버전 매트릭스 동기화. |
| 1.10 | 2026-03-02 | 05/06/07 `Req_113~Req_119` 보강 반영: 테스트 Req 커버리지 수치를 `62/62`로 갱신하고 확장 요구 커버리지 점검 항목을 DONE 처리. 문서 버전 매트릭스(03/05/06/07) 최신화. |
| 1.9 | 2026-03-02 | 01/03/05/06/07 버전 업데이트(활성 Req 범위 잠금 및 UT/IT/ST 증적 경로 규칙 반영) 정합화. |
| 1.8 | 2026-03-02 | 01~07 착수 전 고정값(F섹션) 추가: HARA 승인 게이트/증적 경로 규칙/활성 Req 범위 잠금 명시. |
| 1.7 | 2026-03-02 | 00d HARA 워크시트(v1.0) 연계 반영, 00c 버전 정합(1.2), HARA TODO를 \"작성\"에서 \"리뷰/승인\" 단계로 갱신. |
| 1.6 | 2026-03-02 | 적용 수준/주장 경계(B-1) 추가, 00c v1.1 정합 반영, HARA 후보 S/E/C 평가 TODO 명시. |
| 1.5 | 2026-03-02 | ISO26262/ASPICE 관점 보강: 00c 연계 항목 추가, 활성 Req 62개 기준 추적성/테스트 커버리지 재점검, 제출 전 잔여 항목 재정의. |
| 1.4 | 2026-03-01 | D 섹션 잔여 TODO 3건 종료(07 상단 기록 규칙, 02 이미지 네이밍 고정, 로그/Trace 파일명 규칙 고정). |
| 1.0 | 2026-02-28 | 초기 작성 |
