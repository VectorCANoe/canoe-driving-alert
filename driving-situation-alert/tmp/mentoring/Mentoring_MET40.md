> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

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
| D15 | 01:00~06:30 | Must | 중간보고 엑셀은 첫 탭에 프로젝트 개요를 두고 팀 간 비교 가능한 포맷을 유지 | 엑셀 1번 탭 개요 추가 + 제출본 탭/컬럼 구조 정합 점검 |
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
| D12 | 1:03:08~1:04:28 | Must | 기존 우선순위 용어는 CAN arbitration과 혼동됨 | 경보 용어로 치환(예: 경보 우선순위 판정) |
| D13 | 1:06:35~1:08:02 | Should | 요구사항 리미트는 없지만 과세분화는 통폐합 훈련 권장 | 지나친 분해 대신 묶음 수준 설계도 병행 |
| D14 | 55:44~57:13 | Should | ADAS 항목이 적어도 도메인 의미를 지키는 편이 디펜스에 유리 | 기능 수가 적어도 구조적 일관성 우선 |
| D16 | 1:05:41~1:08:02 | Should | 난이도 상승보다 기능 축 추가가 우선, 상태 전송 위주 인상을 줄이고 구현 범위를 확장 | 신규 기능을 추가하되 요구사항은 통폐합 단위로 재구성(정답 고집보다 설계 판단 훈련) |

## 2) 실행 체크리스트 (개정)

| ID | 항목 | 완료기준 | 상태 | 증빙 문서/파일 |
|---|---|---|---|---|
| M40-01 | 중간보고 제출물 정합 | 중간보고 제출본을 `PPT + 엑셀 + DBC`로 버전/날짜 고정 | [x] | `driving-situation-alert/TMP_MID_AUDIT_MAIN.md`, `driving-situation-alert/tmp/reports/M40_EVIDENCE_INDEX.md` |
| M40-15 | 중간보고 엑셀 포맷 정합 | 엑셀 첫 탭에 프로젝트 개요 추가 + 팀 간 비교 가능한 탭/컬럼 구조 유지 | [x] | `driving-situation-alert/TMP_MID_AUDIT_MAIN.md`, `driving-situation-alert/tmp/reports/M40_EVIDENCE_INDEX.md` |
| M40-02 | 도메인 DBC 분리/명명 정리 | 도메인 DBC 구조 유지 + `test_can` 제출 해석 문구 고정 | [x] | `canoe/databases/*.dbc`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-03 | Ethernet SoT 분리 | CAN DBC와 ETH 계약 원본을 분리 명시 | [x] | `canoe/docs/operations/10_ETHERNET_BACKBONE_INTERFACE_SPEC.md`, `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-04 | test_can 해석 정리 | `test_can`을 공통/검증용으로 정의하고 오해 방지 설명 확보 | [x] | `driving-situation-alert/0303_Communication_Specification.md` |
| M40-05 | 네트워크 도식 수정 | Ethernet 버스선 제거 + 스타형 연결 그림 반영 | [x] | `driving-situation-alert/02_Concept_design.md`, `driving-situation-alert/tmp/assets/current/02_networkflow.png`, `driving-situation-alert/tmp/reports/M40_EVIDENCE_INDEX.md` |
| M40-06 | Panel 우선순위 반영 | `차량 화면(1) / 제어패널(2) / 상태모니터(3)` 기준을 설계/테스트에 반영 | [x] | `driving-situation-alert/04_SW_Implementation.md`, `driving-situation-alert/07_System_Test.md`, `driving-situation-alert/tmp/reports/M40_EVIDENCE_INDEX.md` |
| M40-07 | KPI 과분석 배제 | 분석 지표 중심 대신 `설계대로 동작 검증` 중심으로 정리 | [x] | `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md` |
| M40-08 | Req 성격 분리 반영 | `Req_041~043`, `Req_112`를 검증환경/품질 성격으로 명시 | [x] | `driving-situation-alert/01_Requirements.md`, `driving-situation-alert/00c_Req_Classification_and_Safety_Profile.md` |
| M40-09 | 주기/이벤트 명시 | 0302/0303 핵심 Comm에 Period/Event 표기 누락 없음 | [x] | `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-10 | 용어 혼동 제거 | 경보 우선순위 판정과 CAN arbitration 용어 분리 | [x] | `driving-situation-alert/03_Function_definition.md`, `driving-situation-alert/0301_SysFuncAnalysis.md`, `driving-situation-alert/04_SW_Implementation.md` |
| M40-11 | 요구사항 통폐합 품질 | 과세분화 구간 통폐합 근거와 개정 이력 유지 | [x] | `driving-situation-alert/01_Requirements.md` 개정이력 |
| M40-12 | CAN ID 설계 근거 | ID 배정 룰(도메인/충돌회피/확장성/예약영역) 문서화 | [x] | `driving-situation-alert/0303_Communication_Specification.md` |
| M40-13 | Ethernet DBC 경계 명시 | “Ethernet에는 CAN DBC 직접 적용하지 않음” 문구 고정 | [x] | `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md` |
| M40-14 | DBC ID 충돌/예약영역 대응 | UDS 예약영역/ID 충돌 대응 원칙과 디펜스 문구 준비 | [x] | `driving-situation-alert/0303_Communication_Specification.md`, 본 문서 `4) ID 디펜스 Q&A 메모` |
| M40-16 | 기능 다양화 증설(상태전송 편중 해소) | 신규 기능축을 체인에 추가해 `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 폐쇄를 확보 | [x] | `driving-situation-alert/01_Requirements.md`, `driving-situation-alert/03_Function_definition.md`, `driving-situation-alert/0301_SysFuncAnalysis.md`, `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md`, `driving-situation-alert/0304_System_Variables.md`, `driving-situation-alert/04_SW_Implementation.md`, `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md`, `driving-situation-alert/tmp/reports/Doc_Code_Sync_Report.md` |
| M40-17 | 요구사항 통폐합 리밸런싱 | 신규/기존 Req를 통합 단위 기준으로 재정렬하고 변경 매핑(Old->New)을 유지 | [x] | `driving-situation-alert/01_Requirements.md`(C-1~C-4), `driving-situation-alert/03_Function_definition.md`(Legacy 전환 매핑), `driving-situation-alert/0301_SysFuncAnalysis.md`(Legacy Req 상속), `driving-situation-alert/0302_NWflowDef.md`(Legacy Req 상속), `driving-situation-alert/0303_Communication_Specification.md`(Legacy Req 상속), `driving-situation-alert/0304_System_Variables.md`(Legacy Req 상속), `driving-situation-alert/tmp/reports/Doc_Code_Sync_Report.md` |
| M40-18 | Pre-Activation 실행 증빙 폐쇄 | `Req_130~Req_155` 활성 전환 항목에 대해 실제 구현/실행 결과(`Pass/Fail`, owner/date, log/capture)를 05/06/07에 채워 G4 재개 기준을 충족 | [~] | `driving-situation-alert/04_SW_Implementation.md`, `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md`, `canoe/src/*`, `canoe/logging/evidence/ST/*`, `driving-situation-alert/tmp/reports/M40_EVIDENCE_INDEX.md` |

## 3) 즉시 실행 To-do (다음 사이클)

1. `M40-18` 잔여: `Req_130~Req_155` Pre-Activation 항목에 대해 실측 로그/캡처를 수집한다.
2. 수집 완료 후 `05/06/07`의 `Pass/Fail`, 담당자, 일자를 실제 실행 결과로 갱신한다.
3. 증빙 반영 후 `driving-situation-alert/tmp/reports/Doc_Code_Sync_Report.md` 재실행으로 체인 정합을 재확인한다.
4. 제출 직전 `TMP_MID_AUDIT_MAIN.md`의 lock anchor를 최종 제출 커밋으로 1회 재동기화한다.
5. `canoe/logging/evidence/ST/` 경로 실측 캡처/로그와 `M40_EVIDENCE_INDEX.md` 링크를 동일 커밋으로 갱신한다.

## 4) ID 디펜스 Q&A 메모 (발표용)

- 질문: `test_can`을 왜 별도 도메인으로 제출하지 않았나?
  - 답변: Validation 공통 프레임(`0x2A5`, `0x2A6`)은 `chassis_can.dbc`에 통합 관리해 도메인 오해와 중복 관리 리스크를 줄였다.
- 질문: UDS/예약영역과 충돌 리스크는 어떻게 대응했나?
  - 답변: 신규 ID는 기존 DBC ID와 중복 금지, 진단/검증 예약 구간과 충돌 금지 원칙으로 배정했고(0303 규칙표), 배정 정책 SoT는 00f를 기준으로 유지했다.
- 질문: Ethernet도 DBC로 관리하나?
  - 답변: Ethernet은 CAN DBC 직접 적용 대상이 아니며, `10_ETHERNET_BACKBONE_INTERFACE_SPEC.md` 기반의 계약/매트릭스 수준으로 관리한다.

## 5) 비고

- 이 문서는 회의록 분석 기반 내부 실행 메모다.
- 회의록 원문 발화(시간대)는 `1)` 표를 기준으로 추적한다.
- 현재 Must 항목은 문서 기준 완료 상태다.
- 핵심 잔여는 실행증빙 실측 데이터 반영(`M40-18`)이며, 현재 문서/추적 정의는 완료([~]) 상태다.
---
# 회의록 (2026.03.03)

**일시:** 2026년 3월 3일 (화) 22:18 ~ 23:47 (약 89분)

**참석자:** 멘토, 팀원들 (택천, 성현, 라엘, 현준, 준영)

**장소:** 온라인 (음성 및 화면 공유)

---

## 1. 중간 보고서 제출 안내

### 1.1. 제출 항목

- **중간 보고서:**
    - **PPT (결과 보고서 양식):** 발표 자료로, 전체적인 프로젝트 설명과 시나리오, 시연에 초점.
    - **엑셀 파일:** 프로젝트 요구사항, 기능 정의, 네트워크 설계 등이 상세히 기록된 통합 문서.
        - 첫 번째 탭에 프로젝트 개요(컨셉 디자인)를 추가할 것.
        - 탭 구조는 변경/통합 가능.
    - **DBC 파일:** 도메인별로 분리하여 제출 (여러 개 파일을 폴더에 담아 제출).
- **최종 보고서 (향후):**
    - PPT + 한글 보고서 + 엑셀 + 구현 결과물 (CANoe 프로젝트 등).
    - 한글 보고서는 PPT보다 상세한 기술 문서 및 개인별 포트폴리오 역할.

### 1.2. 평가 기준

- 중간 보고서는 **계획 대비 진행 상황**만 확인 (정답/오답 평가 아님).
- 엑셀 파일은 모든 팀이 동일한 포맷으로 제출하여 비교 평가의 기준으로 활용.

---

## 2. 기술 검토 및 질의 응답

### 2.1. DBC 파일 및 네트워크 구성

- **테스트 캔(Test CAN) DB 논의:**
    - 팀원이 진단 및 공통 기능을 위해 별도의 Test CAN DB를 만들었으나, 멘토는 **공통 DB는 각 도메인 DB에 통합**할 것을 권고.
    - 이유: 여러 네트워크에 동일한 ID가 존재할 경우 충돌 가능성.
    - 해결 방안: UDS(Unified Diagnostic Services) 프로토콜처럼 ID는 동일하게 사용하고, 데이터 내부 플래그로 구분하는 방식 사용.
    - 제출 시에는 DB를 하나로 합쳐서 깔끔하게 정리할 것.
- **Ethernet 관련:**
    - Ethernet 라이선스가 아직 발급되지 않음 → 멘토가 빠른 발급 약속.
    - Ethernet 구현 시 CAN DB를 사용할 수 없고, 애플리케이션 프로토콜(예: SOME/IP, MQTT 등)을 정의해야 함.
    - 현재는 CAN으로 대체하여 개발 중이며, 향후 Ethernet으로 전환 시 IP 및 토폴로지 변경 필요.
- **ID 할당 규칙 (네이밍 컨벤션):**
    - 팀원 질문: ID 할당 시 업계 표준 규칙이 있는가?
    - 멘토 답변: 회사마다 자체 규칙을 정함. 예를 들어 ID의 앞 비트는 우선순위, 중간 비트는 도메인, 뒤는 시퀀스 등으로 나누어 확장성과 유지보수를 고려.
    - 우리 프로젝트에서도 이러한 규칙을 정하고 문서화하면 좋음.

### 2.2. 아키텍처 및 도메인 설계

- **ADAS 도메인 신설 여부:**
    - 팀원이 TTC(Time to Collision) 등 ADAS 기능을 추가하려 함.
    - 멘토: 기능 수가 적더라도 **ADAS 도메인을 별도로 구성**하는 것이 일반적인 설계에 부합.
    - 면접관의 의심을 피하기 위해 표준 아키텍처를 따르는 것이 안전.
- **우선순위 중재 로직 용어:**
    - 팀원이 사용한 "우선순위 중재"는 CAN의 Arbitration과 혼동 가능 → "서비스 우선순위" 등으로 변경 권고.

### 2.3. 패널(Panel) 구현 및 시각화

- **현재 상황:**
    - 팀에서 클러스터, 앰비언트 라이트, 3D 차량 뷰 등 다양한 패널을 고민 중.
    - 유니티를 활용한 외부 렌더링도 검토.
- **멘토 조언:**
    - 패널의 목적은 **상황 인지와 제어**를 쉽게 하기 위함.
    - 우선순위:
        1. **차량 화면** (클러스터, 내비게이션 등) – 필수
        2. **제어 패널** (시나리오 동작, 메시지 송신 등) – 필수
        3. **상태 모니터링** (로그, 이벤트 표시) – 있으면 좋음
    - 유니티 사용은 시간 대비 효과가 낮을 수 있음. CANoe 패널의 기본 기능만으로도 충분하며, 지나친 시각화는 오히려 역효과.
    - 복잡한 외부 툴보다 **CANoe 패널로 최대한 구현**하고, 부족한 부분은 간단한 이미지나 수치로 대체.

### 2.4. 요구사항 명세서 관련

- **테스트 관련 요구사항 (예: 041, 042, 043, 112번):**
    - 팀원: 이런 항목은 실제 고객 요구사항이 아닌데, 문서에 포함해도 되는가?
    - 멘토: 이는 **품질 요구사항** 또는 **검증 환경 요구사항**으로, 시스템 요구사항과 별도로 관리 가능.
    - 최종 문서에서는 통폐합하거나 제외해도 무방.
- **요구사항 개수 제한:**
    - 팀원: 요구사항이 너무 많아지면 추적성이 어려움. 적정 개수는?
    - 멘토: 정해진 제한은 없음. 다만, 너무 세분화하면 관리가 힘드므로 **통합 수준**을 조정하되, 필요하면 더 추가해도 됨.
    - 중요한 것은 **설계 의도**가 드러나는 것.

### 2.5. 기타 기술 질문

- **CANoe에서 Ethernet 사용 시 DB 구성:**
    - Ethernet은 CAN과 달리 ARXML 등의 파일이 필요하지만, 간단한 구현은 소켓 통신으로 가능.
    - 팀에서 Ethernet을 CAN으로 대체한 것은 임시 방편이며, 라이선스 발급 후 전환 예정.
- **주기/이벤트 전송:**
    - 네트워크 설계에 **메시지 전송 주기(Cyclic) 및 이벤트 조건**을 명시할 것.
    - 이는 실제 차량 네트워크 부하와 실시간성에 중요한 요소.

---

## 3. 결정 사항

| 항목 | 내용 |
| --- | --- |
| **중간 보고서 제출** | PPT, 엑셀, DBC 파일 (도메인별 분리) 제출. 엑셀 첫 탭에 프로젝트 개요 추가. |
| **DBC 파일 통합** | Test CAN DB는 각 도메인 DB에 통합. ID 충돌 방지를 위해 UDS 방식 참고. |
| **ADAS 도메인** | 기능 수가 적더라도 별도 도메인으로 구성 (표준 아키텍처 준수). |
| **패널 개발** | CANoe 패널 우선. 유니티 등 외부 툴은 시간 허락 시 보조적으로 활용. |
| **우선순위 용어** | '서비스 우선순위' 등으로 변경하여 CAN Arbitration과 혼동 방지. |
| **ID 할당 규칙** | 팀 내 컨벤션을 정하고 문서화 (예: 비트 필드별 의미 부여). |

---

## 4. 향후 일정 및 액션 아이템

### 4.1. 다음 멘토링

- **일시:** 2026년 3월 7일 (토) 22:00 ~ (2~3시간 예상)
- **내용:** 중간 보고서 초안 검토, 구현 진행 상황 확인, 추가 질의 응답.

### 4.2. 당장의 할 일

- **엑셀 문서:** 요구사항, 기능, 네트워크 설계 보완 (특히 메시지 주기/이벤트 추가).
- **DBC 파일:** 도메인별로 정리하고, 공통 DB는 각 도메인에 통합.
- **패널:** 1순위(클러스터)와 2순위(제어 패널) 우선 구현.
- **PPT:** 멘토 피드백 반영하여 수정 (예: 11페이지의 삐져나온 선 제거, Ethernet을 스타 토폴로지로 표현).
- **ADAS 기능 추가:** TTC 기반 긴급 상황 감지 등 최소 1~2개 기능 추가 검토 (도메인 신설).

### 4.3. 멘토 요청 사항

- Ethernet 라이선스 발급 진행 중.
- 다음 주 화요일(3/10)은 별도 멘토링 없음.

---

## 5. 특이사항

- 팀원들의 적극적인 질의와 준비로 멘토의 만족도가 높았음.
- 팀 내에서 카톡 등을 통해 지속적인 논의가 이루어지고 있어 멘토링 시간을 효율적으로 활용함.

---

**작성자:** 회의록 정리

**날짜:** 2026. 3. 3.
