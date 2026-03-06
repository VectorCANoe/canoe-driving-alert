# 개발팀 임시 전달서: TTC/객체인식 ADAS 요구사항 증설 제안 (Pre-CR)

- 작성일: 2026-03-06
- 작성주체: CANoe 개발팀
- 전달대상: 문서작성팀
- 적용범위: CANoe SIL, CAN + Ethernet

## 1) 한 줄 결론

- 현재 제품 체인은 `구역/긴급차 기반 경고` 중심으로 구현되어 있으며, 교차로/합류 ADAS 확장을 위해서는 `객체 인식 입력 + 객체별 TTC 위험도` 요구 블록을 신규로 정의하는 것이 필요합니다.
- 이전 `Driver/gaze` 계열은 제품 스코프 정합 관점에서 활성 경로에서 제거하는 판단이 맞았고, 향후 ADAS 확장은 `졸음 추정`이 아닌 `객체 기반 충돌위험` 축으로 진행하는 것이 타당합니다.

## 2) 현재 구현 기준에서 확인한 갭

1. [ADAS_WARN_CTRL.can](/C:/Users/이준영/CANoe-IVI-OTA/canoe/src/capl/logic/ADAS_WARN_CTRL.can): 위험도 계산이 `긴급차 type/ETA/방향/자차속도` 중심이며 객체 리스트 기반이 아님.
2. [WARN_ARB_MGR.can](/C:/Users/이준영/CANoe-IVI-OTA/canoe/src/capl/logic/WARN_ARB_MGR.can): 중재 로직은 존재하나 객체별 우선순위(다중 객체 충돌경합) 입력이 없음.
3. [VAL_SCENARIO_CTRL.can](/C:/Users/이준영/CANoe-IVI-OTA/canoe/src/capl/input/VAL_SCENARIO_CTRL.can): 시나리오 1~19는 구역/긴급차/Fail-safe 중심이며 교차로 횡단·합류 객체 상호작용 케이스가 부족함.
4. [ETH_INTERFACE_CONTRACT.md](/C:/Users/이준영/CANoe-IVI-OTA/canoe/docs/operations/ETH_INTERFACE_CONTRACT.md): 현재 E100/E200/E210/E211/E212 중심이며 객체 트랙 인터페이스가 없음.

## 3) 외부 근거 요약 (핵심만)

1. Euro NCAP AEB C2C v4.3.1(2024)은 후방추돌 외에 `CCFtap(턴-가로지름)`, `CCCscp(직진 교차)` 시나리오를 포함합니다.
2. Euro NCAP Crash Avoidance Frontal Collisions v1.1(2025, 2026 적용)은 TTC/FCW/AEB 시간 정의와 복잡도(robustness layer) 기반 평가를 명시합니다.
3. 미국 `49 CFR 571.127`은 2029-09-01 이후 경량차 AEB/FCW 요구를 규정하고, 정지차/저속 선행차/감속 선행차 시나리오와 TTC 기반 시험 세팅을 명시합니다.
4. FHWA SSAM 보고서는 교차로 안전평가에서 TTC/PET(충돌확률 지표)와 심각도 지표를 함께 봐야 함을 보여줍니다.
5. TTC 확장 연구(TTCmo)는 교차/합류처럼 방향성이 큰 상황에서 yaw(방향) 반영 TTC의 유효성을 제시합니다.
6. RSS(형식 안전모델), 교차로 SMPC 연구는 다중 객체/불확실성 상황에서 안전 한계(규칙) + 예측 기반 제어가 필요함을 뒷받침합니다.
7. CenterFusion/BEVFusion/nuScenes/Waymo 계열은 객체 인식 입력(카메라/레이더/라이다 융합)과 평가 데이터 축을 실무적으로 제공합니다.

## 4) 문서팀 요청: 요구사항 증설 초안 (제안 ID)

아래는 문서팀이 `01/03/0301/0302/0303/0304/04/05/06/07` 체인으로 확장하기 위한 초안입니다.

| 제안 Req ID | 요구사항 초안 (What) | 검증 포인트 (요약) |
|---|---|---|
| Req_125 | 시스템은 객체 인식 입력(위치/속도/방향/신뢰도)을 주기적으로 수신해야 한다. | 수신주기/누락율/타임아웃 검증 |
| Req_126 | 시스템은 객체별 추적 ID와 유효성(신뢰도 임계) 관리를 수행해야 한다. | ID 유지율, ghost 제거율 |
| Req_127 | 시스템은 종방향 선행 객체에 대해 TTC를 계산해야 한다. | TTC 계산 오차 허용치 |
| Req_128 | 시스템은 교차/합류 상황에서 방향성을 반영한 TTC 확장 지표를 계산해야 한다. | 횡단/합류 시나리오 검증 |
| Req_129 | 시스템은 다중 객체 중 위험 우선 객체를 결정해야 한다. | 우선순위 규칙 일관성 |
| Req_130 | 시스템은 객체 위험도를 0~100 범위로 정규화하여 출력해야 한다. | 위험도 경계/단조성 |
| Req_131 | 시스템은 위험 임계 도달 시 FCW를 발생시켜야 한다. | TFCW, 오경보율 |
| Req_132 | 시스템은 임계 초과 시 감속보조 요청을 발생시키되 Fail-safe 정책을 따라야 한다. | decelReq/failSafe 연동 |
| Req_133 | 시스템은 운전자 개입(조향/제동) 시 감속보조를 해제해야 한다. | 개입 해제 응답시간 |
| Req_134 | 시스템은 센서 입력 단절/노후화 시 안전 강등 모드로 전이해야 한다. | 타임아웃/강등 전이 |
| Req_135 | 시스템은 핵심 판단(입력, TTC, 선택객체, 경고결정)을 추적 로그로 남겨야 한다. | 로그 완전성/재현성 |
| Req_136 | 시스템은 교차로/합류/후방추돌 시나리오 세트에서 성능 기준을 만족해야 한다. | UT/IT/ST PASS 기준 |

## 5) 인터페이스/아키텍처 제안 (개발팀안)

1. 노드 구조는 1차로 기존 체인 유지: `ADAS_WARN_CTRL -> WARN_ARB_MGR -> BODY/IVI`.
2. 신규 입력은 Ethernet 계약에 객체 리스트 채널로 추가하고, CAN ID/소유권은 SoT(`00f`, Annex A) 절차로 할당.
3. 1차 구현은 SIL에서 `VAL_SCENARIO_CTRL` 객체 주입 하네스로 시작, 2차에서 실제 Perception ECU 계약 연동.

## 6) 시나리오 증설 요청 (개발팀 제안)

| 제안 시나리오 | 요약 |
|---|---|
| S20 | 교차로 직진-직진 충돌 경합(CCCscp 계열) |
| S21 | 좌/우회전 중 맞은편 차와 Turn-Across-Path 경합(CCFtap 계열) |
| S22 | 합류구간 후측방 빠른 접근차량과 gap 미확보 |
| S23 | 본선 합류 중 전방 감속차 + 후방 접근차 동시 경합 |
| S24 | 전방 저속/정지차 + cut-in 복합 |
| S25 | 센서 노이즈/객체 소실/오검출 강건성(robustness layer) |

## 7) 문서팀에 요청하는 업데이트 경로

1. `01_Requirements.md`: Req_125+ 블록 신설 (What only)
2. `03/0301`: 기능 분해(객체수신/TTC/위험선정/경고결정)
3. `0302/0303`: 교차로/합류 흐름 및 Ethernet 객체 계약
4. `0304`: 객체/위험도/중재 변수 정의
5. `04`: CAPL 모듈 책임 및 경계
6. `05/06/07`: 시나리오별 PASS 기준/증적 항목

## 8) 개발팀 선행 착수안 (문서 병행 가능)

1. SIL 객체 주입 하네스와 TTC 계산기 골격 구현
2. 다중 객체 우선순위/임계 로직 구현
3. 시나리오 20~25 템플릿 작성 및 기본 회귀 파이프라인 연결

## 9) 참고 자료 (Primary Sources)

1. Euro NCAP AEB C2C v4.3.1 (2024): https://www.euroncap.com/media/80155/euro-ncap-aeb-c2c-test-protocol-v431.pdf
2. Euro NCAP Crash Avoidance Frontal Collisions v1.1 (2025, 2026 적용): https://www.euroncap.com/media/91710/euro-ncap-protocol-crash-avoidance-frontal-collisions-v11.pdf
3. 49 CFR §571.127 (AEB systems for light vehicles): https://www.law.cornell.edu/cfr/text/49/571.127
4. FHWA SSAM Final Report: https://www.fhwa.dot.gov/publications/research/safety/08051/08051.pdf
5. RSS (Formal Safety Model): https://arxiv.org/abs/1708.06374
6. Intersection SMPC (multi-modal prediction): https://arxiv.org/abs/2109.09792
7. TTC with motion orientation (TTCmo): https://www.sciencedirect.com/science/article/abs/pii/S0001457523002191
8. CenterFusion (radar-camera fusion): https://arxiv.org/abs/2011.04841
9. BEVFusion (multi-sensor BEV fusion): https://arxiv.org/abs/2205.13542
10. nuScenes dataset: https://arxiv.org/abs/1903.11027
11. Waymo Open Dataset paper: https://openaccess.thecvf.com/content_CVPR_2020/papers/Sun_Scalability_in_Perception_for_Autonomous_Driving_Waymo_Open_Dataset_CVPR_2020_paper.pdf

---

### 메모
- 위 요구사항 ID/수치/임계값은 개발팀 제안 초안이며, 문서팀 SoT 반영 시 CR 절차와 안전/검증 기준에 맞춰 확정이 필요합니다.
