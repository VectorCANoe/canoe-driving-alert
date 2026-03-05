> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# OTA/V2V 통합 임시 구현 계획 (TMP)

- 문서 목적: 멘토 피드백 기반 누락 항목 점검 및 순차 반영
- 상태: 임시 문서 (작업 완료 후 삭제)
- 생성일: 2026-02-25
- 삭제 조건: 01~07 문서 정합성 검토 완료 + 랜덤 추적성 샘플 통과

---

## 1) 멘토 피드백 핵심 체크리스트

- [ ] 1:1 추적성 완성: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT -> IT -> ST`
- [ ] 랜덤 포인트 추적 검증 3건 통과 (중간 끊김 0건)
- [ ] 요구사항(What)과 기능명세(How) 완전 분리
- [ ] 03xx 문서 역할별 내용 분리 (0301/0302/0303/0304)
- [ ] V-Model 양방향 사용 흔적 반영 (정방향+역방향)

근거 회의록:
- `docs/mentoring/Mentoring_07_feedback.md:921`
- `docs/mentoring/Mentoring_07_feedback.md:924`
- `docs/mentoring/Mentoring_07_feedback.md:1007`
- `docs/mentoring/Mentoring_07_feedback.md:1008`

---

## 2) 현재 누락/충돌 항목 (즉시 수정 대상)

- [ ] 구 범위 잔존 제거: Req_B/Req_O, Drive Coach, Smart Claim, Seasonal, UDS/DoIP
- [ ] Panel을 노드로 기술한 항목 정리 (Panel=입력/관찰 인터페이스)
- [ ] 03~07 문서를 새 범위로 재기준화
  - 범위: 내비 컨텍스트 + 경찰/구급차 V2V + 앰비언트 중재
  - 제약: CANoe SIL only, CAN+Ethernet only
- [ ] compact 문서 세트 정리 (사용 시 동일 기준 반영, 미사용 시 제외 표기)

참조 위치(현재 충돌 확인):
- `docs/OTA/0301_SysFuncAnalysis.md:23`
- `docs/OTA/0302_NWflowDef.md:49`
- `docs/OTA/0303_Communication_Specification.md:49`
- `docs/OTA/0304_System_Variables.md:46`
- `docs/OTA/06_Integration_Test.md:49`
- `docs/OTA/07_System_Test.md:56`

---

## 3) 문서별 실행 계획 (Implementation Steps)

### Step A. 요구/설계 정합화
- [ ] `01_Requirements.md` 상세화 (Req_Cxx/Req_Exx/Req_Axx 고정)
- [ ] `02_Concept_design.md`와 용어 동기화 (ID/노드명/신호명)
- [ ] `03_Function_definition.md`에서 노드별 기능만 유지 (Panel 노드화 금지)

### Step B. 03 하위문서 재작성
- [ ] `0301_SysFuncAnalysis.md`: 노드 내부 입력/처리/출력 분해
- [ ] `0302_NWflowDef.md`: Tx/Rx/조건/주기/해제 조건 명시
- [ ] `0303_Communication_Specification.md`: ID/DLC/bit/range/의미 정리
- [ ] `0304_System_Variables.md`: 위 3개 확정 후 최종 반영

### Step C. 구현/테스트 추적성 체인 완성
- [ ] `04_SW_Implementation.md` 코드 참조 ID 연결
- [ ] `05_Unit_Test.md` (Func/Comm 기준)
- [ ] `06_Integration_Test.md` (Flow 기준)
- [ ] `07_System_Test.md` (Req 기준)

### Step D. 랜덤 감사
- [ ] 랜덤 ID #1 추적
- [ ] 랜덤 ID #2 추적
- [ ] 랜덤 ID #3 추적
- [ ] 누락 시 해당 문서 즉시 보정

---

## 4) 완료 정의 (Definition of Done)

- [ ] 문서 간 ID 명명 규칙 통일 (C/E/A + Func/Flow/Comm/Var/Test)
- [ ] 01~07 전 문서에서 구 범위 키워드 0건
- [ ] 랜덤 추적 3건 성공
- [ ] 멘토 피드백 4대 항목 모두 체크 완료

---

## 5) 삭제 메모

- 이 문서는 임시 관리용이다.
- 완료 후 아래 파일 삭제:
  - `docs/tmp/OTA_V2V_Implementation_Plan_TMP.md`
