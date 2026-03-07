# 00 마스터 프로젝트 프레임워크 (제출본)

**Document ID**: PROJ-00-MASTER-FRAMEWORK  
**Version**: 1.0  
**Date**: 2026-03-07  
**Status**: Draft (Submission)  

---

> 제출용 축소본: `00_VModel_Mapping` + `00b_Project_Scope`를 중간 제출 관점에서 통합한 문서입니다.

## 작성 원칙

- 본 문서는 00 계열 중 프로젝트 프레임/범위/검증 전략만 통합 요약한다.
- 본문은 평가자가 빠르게 이해할 수 있는 핵심 규칙만 유지한다.
- 상세 운영 메모/세부 근거는 원문 SoT(00, 00b)에서 관리한다.

---

## 1) 프로젝트 목표 및 범위

### 목표

- 주행 상황(구간 + 긴급차량 접근)에 따라 경고를 실시간 판정/표시하는 통합 경보 체인을 구현/검증한다.

### Scope In

- 내비게이션 구간 인식 컨텍스트(roadZone/navDirection/zoneDistance/speedLimit)
- 긴급차량 접근 경보(경찰/구급) 및 경보 우선순위 판정
- 앰비언트/클러스터 출력 동기화
- CANoe SIL 기반 검증(Req-Func-Flow-Comm-Var-Test 체인)

### Scope Out

- OTA/UDS 구독, 군집(Lead/Follow) 위협 대응, 물류 임무전환 OTA
- 위험운전 점수 기반 단계 경고 등 레거시 위험점수 기능
- 실차/외부 HIL/무선 스택 연동

## 2) 통합 아키텍처 및 핵심 흐름

### 고정 아키텍처

- `ETH_SW + CHS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어(ADAS_WARN_CTRL/NAV_CTX_MGR/EMS_ALERT/WARN_ARB_MGR)`

### Red Thread (핵심 경로)

1. Navigation context 입력  
   `INFOTAINMENT_GW -> ETH_SW -> NAV_CTX_MGR -> WARN_ARB_MGR`
2. Vehicle state 입력  
   `CHS_GW -> ETH_SW -> ADAS_WARN_CTRL -> WARN_ARB_MGR`
3. 긴급차량 이벤트  
   `EMS_ALERT(TX/RX) -> ETH_SW -> WARN_ARB_MGR`
4. 최종 출력  
   `WARN_ARB_MGR -> BODY_GW/IVI_GW -> AMBIENT_CTRL/CLU_HMI_CTRL`

## 3) V-Model 적용 규칙

### 정방향

`01 -> 03/0301 -> 0302/0303/0304 -> 04 -> 05/06/07`

### 역방향

`Test 실패 -> Code/Var/Comm/Flow/Func/Req`로 즉시 역추적

### 추적 체인 고정 규칙

- `Req -> Func -> Flow -> Comm -> Var -> Code Ref -> UT -> IT -> ST`
- 임의 ID 샘플 감사 시 체인이 끊기면 불합격

## 4) 검증 환경 및 제약

- Tool: CANoe SIL
- Network: CAN + Ethernet(UDP)
- 실측 전 단계에서는 Pre-Activation 요구를 `Planned/Ready`로 유지
- Ethernet 라이선스 제약 구간은 CAN 대체 백본(stub)로 동일 체인 검증 후, 라이선스 확보 시 동일 케이스 재검증

## 5) 제출 판단 기준

- 01~07 문서에서 핵심 시나리오/추적 체인 일관성 확보
- 문서 분량보다 추적 연결성과 검증 가능성 중심으로 평가 대응
- 00 정책 상세는 `00_MASTER_Governance_Summary.md`에서 통합 참조

---
