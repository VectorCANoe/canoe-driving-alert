# V-Model 문서 매핑표 (V-Model Document Mapping)

**Document ID**: PROJ-00-VMM
**Version**: 4.3
**Date**: 2026-02-28
**Status**: Released
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 2. 현재 프로젝트 범위

- 포함: 내비게이션 구간 인식 컨텍스트(roadZone/navDirection/zoneDistance/speedLimit) + 경찰/구급차 V2V 긴급알림 + 앰비언트 중재
- 환경: CANoe SIL only (하드웨어 미사용)
- 네트워크: CAN + Ethernet(UDP) only
- 도메인 CAN 분리: Ambient=`Body CAN(0x210)`, Cluster=`Infotainment CAN(0x220)`
- 아키텍처 고정: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어`
- 제외: 군집 위협 대응, 물류 OTA 임무전환, UDS OTA 구독, 위험운전 레벨 경고

---

## 5. 1:1 추적성 규칙 (멘토링 핵심)

아래 체인을 각 항목마다 반드시 연결한다.

`Req ID -> Func ID -> Flow ID -> Comm ID -> Var ID -> Code Ref -> UT -> IT -> ST`

### 필수 규칙

1. 01의 각 Req ID는 최소 1개의 Func ID와 연결되어야 한다.
2. 03/0301의 각 Func ID는 최소 1개의 0302 Flow ID와 연결되어야 한다.
3. 0302의 각 Flow ID는 최소 1개의 0303 Comm ID(메시지/신호)와 연결되어야 한다.
4. 0303/0304의 신호/변수는 04 코드 참조 지점이 있어야 한다.
5. 05/06/07 테스트 케이스는 반드시 상위 ID를 역추적 가능해야 한다.

### 랜덤 샘플 감사 규칙

- 아무 ID 하나를 임의 선택했을 때 위 체인이 끊기지 않아야 한다.
- 중간 하나라도 비어 있으면 문서 불합격으로 간주한다.

---

## 7. V-Model 양방향 사용법

### 정방향 (고객 요구 -> 구현)

1. 01에서 요구사항 확정
2. 03/0301로 노드 기능 정의
3. 0302/0303/0304로 인터페이스 구체화
4. 04에서 구현

### 역방향 (테스트/개발 관점 -> 요구 검증)

1. 05는 03/0303 기준으로 단위 검증 항목 작성
2. 06은 0302 기준으로 연동 검증 항목 작성
3. 07은 01 기준으로 E2E 검증 항목 작성
4. 실패 시 반대방향으로 원인 문서까지 즉시 역추적

---

