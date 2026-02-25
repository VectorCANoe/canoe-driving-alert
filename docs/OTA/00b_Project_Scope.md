# 프로젝트 범위 및 검증 전략 (Project Scope and Verification Strategy)

**Document ID**: PROJ-00b-PS
**Version**: 2.0
**Date**: 2026-02-25
**Status**: Released
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

---

## 1. 프로젝트 범위

### 프로젝트 컨셉

본 프로젝트는 하나의 경고 베이스 엔진 위에서 주행상황에 따라 동작 시나리오가 전환되는 구조를 목표로 한다.

- 시나리오 A: 구간 인식 기반 경고 패턴 동작
- 시나리오 B: 긴급차량 접근 기반 경고 패턴 동작
- 공통 베이스: 경고 표시/중재/복귀 로직

본 프로젝트는 `CANoe SIL` 환경에서 아래 2개 기능만 통합 검증한다.

1. OTA 프로젝트 유산: **내비게이션 활용 구간 인식 컨텍스트**
2. V2V 프로젝트 유산: **경찰/구급차 V2V 긴급차량 알림 + 앰비언트 중재(우선순위/충돌해결)**

### 제외 범위 (명시적 Out of Scope)

- 위험운전 점수 기반 단계 경고(기존 Base B 요구사항)
- Drive Coach / Seasonal Theme / Smart Claim / UDS OTA
- 군집(Lead/Follow) 위협 대응
- 물류차 임무전환 OTA

---

## 2. 통합 핵심 흐름 (Red Thread)

```text
Navigation Context (gRoadZone, gNavDirection, gZoneDistance)
  -> Context Manager (구간 컨텍스트 활성)

EMS_POLICE_TX / EMS_AMB_TX
  -> ETH_EmergencyAlert 브로드캐스트 (차종, 방향, ETA, 긴급레벨)

EMS_ALERT_RX (수신 차량)
  -> Alert WARN_ARB_MGR 실행
  -> 우선순위 규칙에 따라 Ambient/Cluster/HMI 패턴 단일 결정
  -> 해제 조건 충족 시 정상 컨텍스트 복귀
```

---

## 3. 중재 원칙

- 원칙 1: `Emergency Alert`가 `Navigation Context`보다 우선한다.
- 원칙 2: 다중 긴급차량 수신 시 `Ambulance > Police` 우선순위를 적용한다.
- 원칙 3: 동일 우선순위 충돌 시 `ETA(도달예상시간) 짧은 알림`을 우선한다.
- 원칙 4: 긴급 알림 해제 후 마지막 유효 구간 컨텍스트로 자동 복귀한다.

---

## 4. 검증 환경

- Tool: Vector CANoe 17+
- Network: Ethernet UDP (V2V), CAN-HS (차량 내부 HMI 제어)
- 주요 노드: `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX_A/B/C`, `NAV_CONTEXT_MGR`, `BCM_AMBIENT_CTRL`, `CLU_HMI_CTRL`
- Panel 입력: `gRoadZone`, `gNavDirection`, 긴급차량 ON/OFF, ETA, 우선순위 테스트 토글

### 검증 제약 (필수)

- 물리 하드웨어(ECU, 센서, OBU, 외부 게이트웨이)는 사용하지 않는다.
- 모든 노드/신호/이벤트는 CANoe 가상 노드 + System Variable + Panel로만 생성한다.
- 통신 매체는 `CAN`과 `Ethernet(UDP)`만 사용한다.
- 외부 무선 스택(DSRC/C-V2X), 외부 HIL 장비, 실차 연동은 본 범위에서 제외한다.

---

## 개정 이력

- 2.0 (2026-02-25): 범위 재정의. 구간 인식 컨텍스트 + 경찰/구급차 V2V 긴급알림/앰비언트 중재만 유지.

