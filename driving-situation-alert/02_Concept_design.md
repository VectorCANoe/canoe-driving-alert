# 컨셉 디자인 (Concept Design)

**Document ID**: PROJ-02-CD
**Version**: 2.2
**Date**: 2026-02-26
**Status**: Released
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

---

## 1. 시스템 컨셉

본 시스템은 단일 경고 제어 베이스를 유지한 채, 주행상황 입력에 따라 경고 시나리오만 전환하는 구조로 설계한다.

- 베이스 공통 기능: 경고 표시, 우선순위 중재, 경고 해제 후 복귀
- 시나리오 전환 조건:
  - 구간 인식 이벤트 수신 시 구간 경고 시나리오 활성
  - 긴급차량 이벤트 수신 시 긴급 경고 시나리오 활성

```text
[Input Gateway Layer]
  CHASSIS_GW / INFOTAINMENT_GW (CAN -> Ethernet 정규화)

[Navigation Context Layer]
  gRoadZone / gNavDirection / gZoneDistance -> NAV_CONTEXT_MGR

[V2V Emergency Layer]
  EMS_POLICE_TX / EMS_AMB_TX
        -> ETH_EmergencyAlert (UDP Broadcast)

[Arbitration Layer]
  WARN_ARB_MGR Engine
    rule-1 Emergency > Context
    rule-2 Ambulance > Police
    rule-3 Same Type: ETA asc -> SourceID asc

[HMI Actuation Layer]
  ETH_SWITCH -> BODY_GW/IVI_GW -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL
```

---

## 2. 주요 동작

1. 구간 컨텍스트 활성: 스쿨존/고속도로 유도선 기반 Ambient 패턴 적용
2. 긴급차량 알림 수신: 경찰차 또는 구급차 접근 알림 즉시 적용
3. 중재: 다중 이벤트 충돌 시 우선순위 규칙으로 단일 패턴 결정
4. 복귀: 긴급 해제 후 마지막 구간 컨텍스트로 복귀

---

## 3. 네트워크

- Ethernet UDP: V2V 긴급 알림 전파
- CAN-HS: 수신 차량 내부 HMI 제어 (Ambient/Cluster)
- Domain Gateway 고정: `CHASSIS_GW`, `INFOTAINMENT_GW`, `BODY_GW`, `IVI_GW`

## 3.1 아키텍처 대안 검토 결론

| 대안 | 특징 | 판단 |
|---|---|---|
| Option 1 (채택) | ETH_SWITCH + Domain GW + Domain CAN + 중앙 경고코어 | 현재 스코프(CANoe SIL, 문서 추적성, 05~07 검증)에서 최적 |
| Option 1A (조건부) | Option 1 + 이중 ETH 백본/이중화 GW | HIL/실차 이전 장애 허용성 강화 단계에서 도입 검토 |
| Option 2 | 도메인 CAN 직접 연계 중심 | 확장성과 중재 가시성 저하로 미채택 |
| Option 3 | 단일 CAN 백본 | 도메인 분리 약화/병목 위험으로 미채택 |

- 결론: 본 프로젝트는 Option 1을 기준 아키텍처로 고정하고, Option 1A는 차기 고도화 단계 후보로 유지한다.

## 4. 검증 전제 (CANoe SIL Only)

- 구현/검증은 CANoe 내부에서만 수행한다. (Hardware-in-the-loop 미사용)
- 모든 ECU는 CAPL 기반 가상 노드로 구성한다.
- 입력은 Panel/System Variable 주입 방식만 사용한다.
- 네트워크는 CAN + Ethernet(UDP) 2계층만 사용한다.

## 5. 제외 범위

- 군집 위협 대응
- 물류차 OTA 임무전환
- OTA 구독 패키지 및 UDS 절차
- 위험운전 레벨 기반 경고 시스템

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.0 | 2026-02-25 | 주행상황 연동 실시간 경고 시스템 기준으로 컨셉 재정의 |
| 2.1 | 2026-02-26 | 아키텍처 대안(Option 1/1A/2/3) 비교 및 채택 결론 추가 |
| 2.2 | 2026-02-26 | 컨셉 블록도/네트워크 섹션에 도메인 GW 실명(`CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW`) 반영 |
