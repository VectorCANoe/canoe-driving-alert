# 개발팀 임시 전달서: ADAS 객체기반 확장 실행안 (Req_130+ Pre-Activation)

- 작성일: 2026-03-06
- 작성주체: CANoe 개발팀
- 전달대상: 문서작성팀
- 적용범위: CANoe SIL, CAN + Ethernet
- 기준 상태: `Req_120~121,123,125~129` 활성 유지 + `Req_130~139` 증설 준비

## 1) 결론

- ADAS 요구사항 증설 타이밍은 지금이 맞습니다.
- 단, 기존 활성 V2 블록(`Req_120~129`)을 건드리지 않고 `Req_130+`를 별도 블록으로 확장해야 합니다.
- 구현 범위는 `객체 입력 계약/판단/중재/검증`까지로 제한하고, 카메라 인지 알고리즘(Perception 자체 개발)은 범위에서 제외합니다.

## 2) 교차검증 결과 (내부 + 외부)

1. 내부 SoT 기준
- 문서 체인은 `Req_130~139`를 Pre-Activation으로 이미 분리했고, `Comm_130~133`, `Flow_130~133`, `Var_330~339` 추적 골격까지 선반영됨.
- 활성 승격 조건은 `ETH_INTERFACE_CONTRACT.md v1.2`에 `E213~E216` 계약 반영 완료임.

2. 코드 기준 갭
- `ADAS`는 현재 긴급차 ETA/방향/자차속도 중심 위험도 모델이며 객체 리스트/TTC 다중객체 선정 로직이 없음.
- `ADAS`는 긴급/구역 중재는 있으나 객체 경합 우선순위 입력이 없음.
- `VAL_SCENARIO_CTRL`는 시나리오 1~19 중심이며 교차로/합류 객체 상호작용 세트가 부족함.

3. 외부 기준 교차검증
- Euro NCAP AEB 평가 축은 후방추돌뿐 아니라 교차/횡단 계열(CCFtap, CCFscp)을 포함.
- 미국 NHTSA AEB 최종 규칙(FMVSS No.127)은 정지/저속/감속 선행차 조건과 FCW/AEB 성능 요구를 명시(적용 시작: 2029-09-01).
- SOTIF(ISO 21448)와 시나리오 기반 평가(ISO 34502) 관점에서도 객체 입력 신뢰도/강건성/재현성 로그가 필수.

## 3) 확정 스코프 경계

1. In Scope
- `Req_130~139` 객체기반 ADAS 확장
- 교차로/합류 위험 판단 보강
- 객체 입력 단절/신뢰도 저하 시 강등 정책
- 재현성 로그 체계

2. Out of Scope
- Driver/gaze/졸음추정 제품기능 부활
- 카메라/레이더 Perception 알고리즘 자체 개발
- 기존 `Req_120~129` 로직의 의미 변경

## 4) 요구사항 블록 권장안 (130+)

| Req ID | 권장 핵심 문구 (요약) | 구현 모듈(초안) |
|---|---|---|
| Req_130 | 객체 입력 계약(위치/상대속도/방향/신뢰도/타임스탬프) 수신 | ADAS |
| Req_131 | 객체 유효성(age/timeout/confidence) 관리 | ADAS |
| Req_132 | 종방향 TTC 산정 | ADAS |
| Req_133 | 교차/합류 확장 TTC(상대 진행방향 반영) | ADAS |
| Req_134 | 다중 객체 위험 우선 대상 선정 | ADAS |
| Req_135 | 위험도 정규화(0~100) + 히스테리시스 | ADAS |
| Req_136 | FCW 트리거/해제 규칙 | ADAS |
| Req_137 | 감속보조 요청 연동(기존 Req_121/123 정합) | ADAS |
| Req_138 | 객체 입력 단절/저신뢰 시 강등 정책 | CGW |
| Req_139 | 입력-판단-결정 로그/재현성 | EMS_ALERT + VAL_SCENARIO_CTRL |

## 5) 인터페이스 게이트 (필수 선행)

1. Ethernet 계약 v1.2 승격
- `E213`: `ethObjectRiskInputMsg`
- `E214`: `ethObjectRiskStateMsg`
- `E215`: `ethObjectScenarioAlertMsg`
- `E216`: `ethObjectSafetyStateMsg`

2. 동기화 원칙
- 계약 갱신 시 `0302 -> 0303 -> 0304 -> 04 -> 05/06/07` 동시 커밋
- 코드 선반영은 가능하되, 활성 SoT 승격 전에는 `Pre-Activation/Pending` 표기 유지

## 6) 개발 실행 PLAN (단계형)

1. Phase A: 스코프 정합 마감
- 활성 경로에서 DriverState/gaze 잔여 제거 완료
- 핵심 회귀(무조향/긴급/V2 Fail-safe) 동등성 확인

2. Phase B: 계약/변수 기반 확장
- `ETH_INTERFACE_CONTRACT.md` v1.2 초안 반영(E213~E216)
- `project.sysvars`에 Var_330~339 대응 변수 추가
- CAPL 입력 하네스(VAL_SCENARIO_CTRL)로 객체 입력 주입 경로 확보

3. Phase C: 판단/중재 로직 구현
- ADAS: 객체 유효성 + TTC + 위험도 계산
- ADAS: 다중객체 우선선정 + 기존 긴급/구역 우선정책 정합
- CGW: 저신뢰/단절 강등, decelAssistReq 차단 연동

4. Phase D: 검증/증적
- 시나리오 S20~S25(교차로/합류/복합/강건성) 추가
- UT/IT/ST PASS 기준 및 로그 재현성(입력-TTC-선정객체-결정) 확보

## 7) 문서팀 동시 반영 요청

1. `01`: Req_130~139 문구 고정(120~129 비변경 명시)
2. `03/0301`: Func_130~139 책임/경계 확정
3. `0302/0303`: Comm_130~133 및 E213~E216 계약 활성조건 명시
4. `0304`: Var_330~339 타입/범위/주기/소유자 확정
5. `04/05/06/07`: 구현/시험 케이스와 증적 항목 동시 업데이트

## 8) 리스크와 제어

1. 번호 충돌 리스크
- 제어: `Req_130+` 고정, 기존 `Req_125~129` 재사용 금지

2. 범위 팽창 리스크
- 제어: Perception 알고리즘 개발 제외, 계약/판단/검증 체인에 한정

3. 체인 불일치 리스크
- 제어: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 1:1 체크리스트 운영

## 9) 참고 기준 (Primary)

1. Euro NCAP Assessment Protocol - AEB Car-to-Car, v10.4.1 (CCFtap/CCFscp 포함):
https://www.euroncap.com/media/85711/euro-ncap-assessment-protocol-aeb-c2c-v1041.pdf
2. NHTSA Final Rule (FMVSS No.127, AEB/PAEB):
https://www.nhtsa.gov/press-releases/nhtsa-fmvss-127-automatic-emergency-braking-rule
3. ISO 21448:2022 (SOTIF):
https://www.iso.org/standard/77490.html
4. ISO 34502:2022 (Scenario-based safety evaluation):
https://www.iso.org/standard/78951.html
5. RSS (Formal model):
https://arxiv.org/abs/1708.06374

---

### 메모
- 본 문서는 구현 착수용 개발 관점 정리다.
- 최종 수치/임계값/승인 상태는 문서팀 SoT와 CR 절차로 확정한다.
