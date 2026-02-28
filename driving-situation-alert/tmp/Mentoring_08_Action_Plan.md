# Mentoring 08 기반 실행 정리 (문서 + 구현)

## 목적
- 문서 완성도는 유지하고, 구현 빈약 문제를 해소한다.
- 번호 1:1 집착보다 **맥락 추적 + 구현 결과**를 우선한다.

## 1) 지금부터 문서에서 할 일

### A. DBC/통신 문서 정리
- `0302/0303`에 맞춰 통신 구조를 **네트워크 단위**로 재정리한다.
- 원칙:
  - CAN: DBC로 관리
  - Ethernet: 인터페이스 명세(표/문서)로 관리
- RX/TX를 ECU 이름으로 분리하지 말고, ECU는 하나로 두고 송수신 행위를 기술한다.

### B. 요구사항/기능 스코프 보강
- 서비스 시나리오(경고)만 남기지 말고 차량 기본 기능을 최소 세트로 포함한다.
- 예: 엔진/브레이크/기어/조향/창문/비상등/클러스터 등.
- 목표: “차량 시스템 이해”가 보이도록 구성.

### C. 테스트 문서 단순화
- 시간 제약 기준으로 `UT + ST` 우선.
- `IT`는 최소 핵심 체인만 유지하거나 필요 시 ST로 통합.
- 기준:
  - UT: ECU/기능 단위 검증
  - ST: 시나리오 단위 검증

### D. 발표자료 정합
- 제목-그림 역할 일치:
  - “전체 시스템 아키텍처” 슬라이드는 오버뷰 그림
  - 네트워크 상세 그림은 “통신 구조”로 분리

## 2) 지금부터 구현에서 할 일

### A. CAPL/노드 확장 (핵심)
- 현재 서비스 로직 외에 차량 기본 기능 ECU를 보강한다.
- 최소 목표: 핵심 ECU 기능 10개 내외가 동작하도록 구성.

### B. DBC 분리/정합
- 네트워크 단위 DBC로 분리(도메인 CAN 기준).
- 각 DBC는 해당 네트워크 노드/메시지에만 집중.
- Ethernet은 DBC에 억지 반영하지 않고 인터페이스 명세로 연결.

### C. 문서-구현 불일치 해소
- `speedLimit` 구현 체인 반영:
  - `SIL_TEST_CTRL`에서 Nav speedLimit 송신
  - `INFOTAINMENT_GW`에서 speedLimit 정규화
  - `ADAS_WARN_CTRL`에서 고정값(30) 대신 speedLimit 비교

### D. 시연 중심 검증
- 패널 기반 시나리오 시연이 가능한 상태를 우선 완성.
- 타임아웃(1000ms), 우선순위(긴급>구간, 구급>경찰, ETA) 동작 로그 확보.

## 3) 우선순위 (실행 순서)
1. DBC 분리 원칙 확정 + 파일 구조 확정  
2. 차량 기본 기능 ECU 보강 구현  
3. speedLimit 체인 구현 반영  
4. UT/ST 최소 세트 갱신  
5. PPT 제목-그림 정합 수정  

## 4) 완료 기준 (Done Definition)
- 문서: 00~07 추적 체인 유지 + 과도한 번호 강박 없이 설명 가능
- 구현: 차량 기본 기능 + 주제 시나리오가 CANoe에서 실제 동작
- 발표: 아키텍처/통신/시나리오를 5분 내 일관되게 설명 가능

---

## 확정안 (상이 항목 정리)
아래 항목을 최신 실행 기준으로 사용한다. 기존 내용과 충돌 시 본 섹션을 우선 적용한다.

# Mentoring 08 Action Plan (Document -> DBC -> Reverse Trace)

## 목표
- 누락 없는 추적성 체인을 유지하면서 개발 속도를 확보한다.
- 기준 흐름을 `01 -> 03 -> DBC -> 0302/0303`로 고정한다.

## 확정 실행 순서
1. `01_Requirements.md`에 차량 기본 기능 요구를 먼저 정의한다. (What)
2. `03_Function_definition.md`에 ECU/기능 배치를 추가한다. (How)
3. 도메인(네트워크) 분할 기준을 확정한다.
4. CAN 통신은 도메인별 DBC를 먼저 작성한다.
5. `0302_NWflowDef.md`, `0303_Communication_Specification.md`는 CAN 영역을 DBC에서 역추출해 작성한다.
6. Ethernet 영역은 DBC가 아닌 별도 인터페이스 명세를 기준으로 작성한다.
7. `0304_System_Variables.md` 및 테스트 문서(05/06/07) 추적 체인을 최종 점검한다.

## 작성 원칙
- `01`은 What만 유지한다.
- `03+`는 How만 유지한다.
- ECU를 RX/TX 역할로 쪼개지 않고 단일 ECU로 정의한다.
- DBC는 CAN 계약만 관리한다.
- Ethernet(E100/E200, 0x510/0x511/0x512)은 인터페이스 명세에서 관리한다.

## 중간 산출물 체크포인트
- C1: `01`에 차량 기본 기능 요구 반영 완료
- C2: `03`에 ECU 확장 및 기능 매핑 완료
- C3: 도메인별 CAN DBC 초안 완료
- C4: `0302/0303` CAN 영역 역추출 반영 완료
- C5: Req -> Func -> Flow -> Comm -> Var 체인 샘플 감사 통과

## Done Definition
- 문서: 01/03/0302/0303/0304의 체인 누락 없음
- 통신: CAN 계약은 DBC와 1:1 일치
- 경계: Ethernet 계약은 별도 명세와 1:1 일치
- 검증: 랜덤 ID 추적 시 체인 단절 없음

## Domain-DBC Policy (Confirmed)
- DBC is NOT one canvas/file for the whole system.
- Create ONE DBC per CAN network(domain).
- Typical split:
  1) Powertrain CAN DBC
  2) Chassis CAN DBC
  3) Body CAN DBC
  4) Infotainment CAN DBC
  5) Additional CAN domains/backbone DBC as needed
- Gateway nodes can appear in multiple DBCs because they connect networks.
- Ethernet contracts are NOT modeled in DBC.
  - Manage Ethernet(E100/E200, 0x510/0x511/0x512) in a separate interface specification.

## Update Rule for 0302/0303
- 0302/0303 CAN sections: reverse-extract from domain DBCs.
- 0302/0303 Ethernet sections: write from Ethernet interface spec.
- Keep traceability source explicit per row:
  - Source=DBC (CAN)
  - Source=ETH_SPEC (Ethernet)

## Review Checklist (Before next mentoring)
- [ ] Domain list fixed (how many CAN networks)
- [ ] One DBC file created per domain
- [ ] Gateway participation mapped per domain DBC
- [ ] Ethernet spec file prepared separately
- [ ] 0302/0303 rows annotated with Source (DBC or ETH_SPEC)
