# 컨셉 디자인 (Concept Design)

**Document ID**: PROJ-02-CD
**Version**: 2.0
**Date**: 2026-02-25
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
[Navigation Context Layer]
  gRoadZone / gNavDirection / gZoneDistance
        -> Context Manager

[V2V Emergency Layer]
  Police_Node / Ambulance_Node
        -> ETH_EmergencyAlert (UDP Broadcast)

[Arbitration Layer]
  Arbiter Engine
    rule-1 Emergency > Context
    rule-2 Ambulance > Police
    rule-3 Same Type: ETA asc -> SourceID asc

[HMI Actuation Layer]
  Ambient_ECU + Cluster_ECU
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
