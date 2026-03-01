# 감사 준비 체크리스트 (Audit Readiness Checklist)

**Document ID**: PROJ-00A-ARC  
**Version**: 1.4  
**Date**: 2026-03-01  
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
| Req 커버리지(05) | 활성 Req(Req_001~043, Req_101~112) 모두 참조 | 55/55 | OK |
| Req 커버리지(06) | 활성 Req(Req_001~043, Req_101~112) 모두 참조 | 55/55 | OK |
| Req 커버리지(07) | 활성 Req(Req_001~043, Req_101~112) 모두 참조 | 55/55 | OK |
| Req 커버리지(차량 기본 확장) | Req_101~Req_112 체인 반영 | 12/12 (01->03->0302/0303/0304->05/06/07) | OK |
| VC 커버리지(05~07) | 활성 VC(VC_001~VC_043, VC_101~VC_112) 모두 참조 | 55/55 | OK |
| 체인 무결성 | Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST | 문서상 연결 확인 | OK |

## B. 문서 버전/날짜 정합

| 문서 | Version | Date | 비고 |
|---|---|---|---|
| `00_VModel_Mapping.md` | 4.3 | 2026-02-28 | V-model 매핑 |
| `00b_Project_Scope.md` | 2.4 | 2026-02-28 | 범위/제외 |
| `01_Requirements.md` | 5.11 | 2026-02-28 | Req+VC 기준 |
| `02_Concept_design.md` | 2.4 | 2026-02-28 | 컨셉/네트워크 그림 중심 |
| `03_Function_definition.md` | 4.10 | 2026-02-28 | 기능 정의 |
| `0301_SysFuncAnalysis.md` | 3.11 | 2026-02-28 | 노드 기능 분석 |
| `0302_NWflowDef.md` | 3.6 | 2026-02-28 | 네트워크 흐름 |
| `0303_Communication_Specification.md` | 3.7 | 2026-02-28 | 통신 명세 |
| `0304_System_Variables.md` | 2.9 | 2026-02-28 | 변수/추적 |
| `04_SW_Implementation.md` | 2.8 | 2026-02-28 | 구현 연결 |
| `05_Unit_Test.md` | 2.7 | 2026-02-28 | UT |
| `06_Integration_Test.md` | 4.8 | 2026-02-28 | IT |
| `07_System_Test.md` | 5.8 | 2026-02-28 | ST |

## C. 범위 경계(고정)

| 구분 | 정책 | 판정 |
|---|---|---|
| 검증 환경 | CANoe SIL only | OK |
| 통신 범위 | CAN + Ethernet(UDP) only | OK |
| 통신 원본 분리 | CAN=`chassis_can.dbc/powertrain_can.dbc/body_can.dbc/infotainment_can.dbc/test_can.dbc`, ETH=`ETH_INTERFACE_CONTRACT.md` | OK |
| 중재 용어 경계 | WARN_ARB_MGR는 서비스(QoS) 중재이며 CAN bit arbitration과 별개 | OK |
| 제외 항목 | OTA/UDS/DoIP | OK |
| 문서 분리 | 01=What, 03+=How, 05~07=Verification | OK |

## D. 최종 제출 전 체크

| 체크 항목 | 담당 | 상태 |
|---|---|---|
| 07 상단 Pass/Fail, 담당자, 일자 기입 | Test Lead | DONE (운영 규칙 확정: 실행 완료 즉시 상단 필드 기록) |
| 02 최종 이미지 파일명/버전 고정 | Architecture Lead | DONE (`02-01_Architecture_v1.0.png`, `02-02_NetworkFlow_v1.0.png` 규칙 고정) |
| 실행 로그/Trace 증적 파일명 규칙 확정 | Validation Lead | DONE (`LOG_<TestID>_<YYYYMMDD>.txt`, `TRACE_<ScenarioID>_<YYYYMMDD>.asc`, `CAP_<ScenarioID>_<YYYYMMDD>.png`) |

---

## 메모
- 상단 공식 표는 간결하게 유지하고, 추적성/수치/경계값은 하단 상세표에서 관리한다.
- UT 개수와 Func 개수의 단순 비교는 기준이 아니다. 핵심 기준은 Req/VC 커버리지와 체인 무결성이다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.4 | 2026-03-01 | D 섹션 잔여 TODO 3건 종료(07 상단 기록 규칙, 02 이미지 네이밍 고정, 로그/Trace 파일명 규칙 고정). |
| 1.0 | 2026-02-28 | 초기 작성 |
| 1.1 | 2026-02-28 | 통신 원본 분리 점검 항목(CAN DBC / ETH 인터페이스 계약) 추가 |
| 1.2 | 2026-02-28 | 차량 기본 기능 확장(Req_101~Req_112) 추적 상태 행을 추가하고 서비스/확장 커버리지를 분리 표기. |
| 1.3 | 2026-02-28 | 05/06/07 및 03 최신 버전 동기화, 활성 Req/VC(55개) 커버리지 반영, CAN SoT를 도메인 분리 DBC 기준으로 갱신, 서비스 중재/CAN 중재 경계 문구 추가. |
