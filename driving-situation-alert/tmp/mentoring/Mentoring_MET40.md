# 03.03 Mentoring 정리 (MET_40_2026.03.03)

기준 회의록: `docs/meeting-notes/MET_40_2026.03.03.txt`  
분석 범위: 멘토/벡터 관계자 발화(`참석자 1`) 중심, 팀 질의응답 문맥 포함

## 0) 판정 규칙

- 상태 기준: `[x]=완료`, `[~]=부분완료(잔여 작업 있음)`, `[ ]=미착수`
- 지시 강도 분류:
  - `Must`: 제출/검증에서 누락 시 리스크가 큰 확정 지시
  - `Should`: 범위 내 권장 지시(시간/가독성/디펜스 품질)

## 1) 벡터 관계자 지시사항 (원문 근거 기반)

| ID | 시간(회의록) | 강도 | 지시사항(요약) | 실행 해석 |
|---|---|---|---|---|
| D01 | 00:00~00:58, 05:56 | Must | 중간보고 제출물은 `PPT + 엑셀 + DBC` 기준 | 중간보고 패키지에서 DBC 제외 금지 |
| D02 | 06:07~06:23 | Must | DBC는 도메인 구분 제출 원칙 유지 | 도메인 DBC 체계(Chassis/Body/Infotainment/Powertrain) 유지 |
| D03 | 16:43~18:10 | Must | `test_can`은 개발 편의 분리 가능, 단 제출/설명 시 오해 없는 명칭 필요 | 제출 설명에서 `공통/검증용` 성격 명시, 테스트 도메인 오해 방지 |
| D04 | 18:30~21:57 | Must | CAN ID 충돌 가능성/예약 ID(UDS 등) 인지하고 설계 근거를 준비 | ID 충돌회피 규칙과 예약영역 회피 근거를 문서화 |
| D05 | 23:09~24:08 | Must | Ethernet은 CAN DBC로 직접 처리하지 않음, 커뮤니케이션 매트릭스 수준으로 관리 | ETH SoT를 계약 문서로 고정, ARXML 심화는 이번 범위 밖 |
| D06 | 47:04~48:25 | Must | 네트워크 도식은 Ethernet 버스선 표현 금지, 스타형 포트 연결로 표현 | `02`/PPT 네트워크 그림에서 버스형 표현 제거 |
| D07 | 30:43~33:00 | Must | Panel 경시 금지, Unity는 보조로만 사용 | Panel이 없는 결과물은 역효과 가능 |
| D08 | 40:28~41:35 | Must | Panel 우선순위는 `차량 화면 -> 제어 패널 -> 상태 모니터` | 1/2는 필수, 3은 시간 허용 시 확장 |
| D09 | 43:15~45:18 | Must | KPI/인사이트 분석보다 V-Model 폐쇄가 핵심 | 설계대로 구현/테스트/확인 증빙 중심으로 정리 |
| D10 | 51:05~51:58 | Must | `Req_041~043`, `Req_112`는 사용자 기능요구가 아닌 검증환경/품질 성격 | 01/00c에서 성격 명확화, 체인 제거가 아니라 분류 정합 |
| D11 | 1:00:37~1:00:54 | Must | Comm 문서에 Period/Event Trigger를 명시 | 0302/0303 핵심 Comm 주기/이벤트 빈칸 금지 |
| D12 | 1:03:08~1:04:28 | Must | `우선순위 중재` 용어는 CAN arbitration과 혼동됨 | 서비스 레벨 용어로 치환(예: 서비스 우선순위) |
| D13 | 1:06:35~1:08:02 | Should | 요구사항 리미트는 없지만 과세분화는 통폐합 훈련 권장 | 지나친 분해 대신 묶음 수준 설계도 병행 |
| D14 | 55:44~57:13 | Should | ADAS 항목이 적어도 도메인 의미를 지키는 편이 디펜스에 유리 | 기능 수가 적어도 구조적 일관성 우선 |

## 2) 실행 체크리스트 (개정)

| ID | 항목 | 완료기준 | 상태 | 증빙 문서/파일 |
|---|---|---|---|---|
| M40-01 | 중간보고 제출물 정합 | 중간보고 제출본을 `PPT + 엑셀 + DBC`로 버전/날짜 고정 | [~] | `driving-situation-alert/TMP_MID_AUDIT_MAIN.md` (제출 hash/날짜 고정 잔여) |
| M40-02 | 도메인 DBC 분리/명명 정리 | 도메인 DBC 구조 유지 + `test_can` 제출 해석 문구 고정 | [~] | `canoe/databases/*.dbc`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-03 | Ethernet SoT 분리 | CAN DBC와 ETH 계약 원본을 분리 명시 | [x] | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`, `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-04 | test_can 해석 정리 | `test_can`을 공통/검증용으로 정의하고 오해 방지 설명 확보 | [~] | `driving-situation-alert/0303_Communication_Specification.md` (명칭 최종 확정/발표 문구 고정 잔여) |
| M40-05 | 네트워크 도식 수정 | Ethernet 버스선 제거 + 스타형 연결 그림 반영 | [~] | `driving-situation-alert/02_Concept_design.md`, `driving-situation-alert/tmp/assets/current/02_networkflow.png` |
| M40-06 | Panel 우선순위 반영 | `차량 화면(1) / 제어패널(2) / 상태모니터(3)` 기준을 설계/테스트에 반영 | [~] | `driving-situation-alert/04_SW_Implementation.md`, `driving-situation-alert/07_System_Test.md` (캡처 증빙 링크 잔여) |
| M40-07 | KPI 과분석 배제 | 분석 지표 중심 대신 `설계대로 동작 검증` 중심으로 정리 | [x] | `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md` |
| M40-08 | Req 성격 분리 반영 | `Req_041~043`, `Req_112`를 검증환경/품질 성격으로 명시 | [x] | `driving-situation-alert/01_Requirements.md`, `driving-situation-alert/00c_Req_Classification_and_Safety_Profile.md` |
| M40-09 | 주기/이벤트 명시 | 0302/0303 핵심 Comm에 Period/Event 표기 누락 없음 | [x] | `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-10 | 용어 혼동 제거 | 서비스 우선순위와 CAN arbitration 용어 분리 | [x] | `driving-situation-alert/03_Function_definition.md`, `driving-situation-alert/0301_SysFuncAnalysis.md`, `driving-situation-alert/04_SW_Implementation.md` |
| M40-11 | 요구사항 통폐합 품질 | 과세분화 구간 통폐합 근거와 개정 이력 유지 | [~] | `driving-situation-alert/01_Requirements.md` 개정이력 |
| M40-12 | CAN ID 설계 근거 | ID 배정 룰(도메인/충돌회피/확장성/예약영역) 문서화 | [x] | `driving-situation-alert/0303_Communication_Specification.md` |
| M40-13 | Ethernet DBC 경계 명시 | “Ethernet에는 CAN DBC 직접 적용하지 않음” 문구 고정 | [x] | `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-14 | DBC ID 충돌/예약영역 대응 | UDS 예약영역/ID 충돌 대응 원칙과 디펜스 문구 준비 | [~] | `driving-situation-alert/0303_Communication_Specification.md`, 발표 Q&A 메모(추가 필요) |

## 3) 즉시 실행 To-do (이번 사이클)

1. `02_Concept_design.md`와 발표용 그림에서 Ethernet 버스형 표현을 완전히 제거하고 스타형만 남긴다.
2. `0303`의 `test_can` 관련 문구를 “공통/검증용 DBC(제출 설명용 명칭 포함)”로 최종 고정한다.
3. Panel 증빙(차량 화면/제어패널/상태모니터)을 `07` 기준으로 링크/캡처까지 채운다.
4. `01` 요구사항 통폐합 후보를 1회 더 정리하고 개정 이력 근거를 남긴다.
5. 중간보고 제출본에 대해 `PPT + 엑셀 + DBC` 버전/hash/date를 `TMP_MID_AUDIT_MAIN.md`에 잠근다.

## 4) 비고

- 이 문서는 회의록 분석 기반 내부 실행 메모다.
- 회의록 원문 발화(시간대)는 `1)` 표를 기준으로 추적한다.
- 현재 잔여 핵심 항목은 `M40-01`, `M40-02`, `M40-04`, `M40-05`, `M40-06`, `M40-11`, `M40-14`다.
