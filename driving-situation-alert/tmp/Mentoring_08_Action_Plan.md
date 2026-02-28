# Mentoring 08 Action Plan (Reconfirmed from MET_30)

## 0. 핵심 판단

- 현재 문서는 **서비스 중심으로 너무 슬림**해서 차량 시스템 이해를 보여주기 부족하다.
- 다음 단계의 핵심은 문서 미세정리가 아니라:
  - `차량 기본 기능 확장`
  - `ECU/네트워크 확대`
  - `도메인별 DBC 분리`
  - `그 후 0302/0303/0304 재정렬` 이다.

---

## 1. 멘토 피드백의 실행 해석

1. 요구사항에 차량 기본 시스템이 보여야 한다.  
2. ECU를 늘려서 “차량”이 보이게 만들어야 한다.  
3. DBC는 **네트워크(도메인) 단위**로 분리해야 한다.  
4. Ethernet은 DBC가 아니라 별도 계약 문서로 관리한다.  
5. 테스트 문서는 번호 집착보다 시나리오/기능 커버리지가 중요하다.

---

## 2. 확정 순서 (실행 우선순위)

### Phase 0) Vehicle Baseline 정의 (선행)
- 도메인별 ECU 매트릭스를 먼저 고정한다.
- 권장 최소 구성:
  - Powertrain: Engine, Transmission
  - Chassis: Brake, Steering, Accel
  - Body: BCM, Window, Hazard, CO2/DriverState
  - Infotainment: Cluster, IVI/Navi
  - Core/GW: CHASSIS_GW, INFOTAINMENT_GW, BODY_GW, IVI_GW, ETH_SWITCH

### Phase 1) 01 요구사항 확장 (What)
- 기존 서비스 Req(주행상황 경고)는 유지한다.
- 차량 기본 기능 Req를 별도 그룹으로 추가한다.
- 원칙: “구현 방법”은 넣지 않고, 기능/행동 기준만 작성한다.

### Phase 2) 03/0301 확장 (How)
- 추가된 차량 ECU를 03/0301에 반영한다.
- 기능 책임을 ECU 단위로 분해한다.
- RX/TX로 노드를 쪼개지 않고 ECU 단일 객체로 유지한다.

### Phase 3) DBC 분리 설계/구현
- CAN DBC를 도메인(네트워크) 단위로 분리한다.
- 파일 예시:
  - `chassis_can.dbc`
  - `powertrain_can.dbc`
  - `body_can.dbc`
  - `infotainment_can.dbc`
- Ethernet은 별도 인터페이스 계약으로 유지한다.

### Phase 4) 0302/0303 재작성
- 0302/0303은 실제 DBC + ETH 계약을 원본으로 재정렬한다.
- 각 Flow/Comm에 원본 파일 경로를 명시한다.

### Phase 5) 0304 재정렬
- 확장된 통신/기능 기준으로 변수 체인을 갱신한다.
- 필수 체인: `Req -> Func -> Flow -> Comm -> Var`

### Phase 6) 05~07 정리
- 05(UT): ECU/기능 단위 개발 검증
- 06(IT): 핵심 통합 체인 최소 집합
- 07(ST): 운전자 시나리오 중심 E2E
- 멘토 권고 반영: 필요 시 06은 얇게, 05+07 중심으로 운영 가능

---

## 3. 산출물 기준 (이번 사이클)

- 문서:
  - `01` 차량 기본 기능 추가 반영
  - `03/0301` ECU 확장 반영
  - `0302/0303/0304` DBC 분리 구조 반영
- 통신:
  - CAN SoT = 도메인별 DBC
  - ETH SoT = `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- 테스트:
  - 서비스 체인 + 차량 기본 기능 체인이 모두 ST에서 설명 가능해야 함

---

## 4. 금지/주의

- 문서만 맞추고 구현이 빈약해지는 방향 금지
- 번호 1:1 강박으로 과분해 금지
- 서비스 기능만 남기고 차량 베이스 삭제 금지

---

## 5. Done Definition

- 차량 기본 기능이 요구사항/기능/통신/변수/테스트에서 모두 보인다.
- 도메인별 DBC 분리와 문서 체인이 일치한다.
- 발표 시 “서비스 + 차량 시스템 이해”를 동시에 설명 가능하다.
