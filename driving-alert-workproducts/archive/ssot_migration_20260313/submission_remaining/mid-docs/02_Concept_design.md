# 컨셉 디자인 (Concept Design)

**Document ID**: PROJ-02-CD
**Version**: 2.7
**Date**: 2026-03-06
**Status**: Draft (Figure Finalized)
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 문서 목적

본 문서는 00~07 문서 체인 중 **시각 설계 증거(Architecture Visualization)**를 담당한다.
그림 반영이 완료된 기준본으로, 본문은 최소 설명만 유지하고 핵심 설계 근거는 그림/캡션으로 관리한다.

---

![alt text](tmp/assets/current/02_concept.png)
![alt text](tmp/assets/current/02_networkflow.png)

## 2. 기준 아키텍처 (고정)

- 채택안: **Option 1**
- 구조: `ETH_SW + Domain Gateway + Domain CAN + 중앙 경고코어`
- 범위: CANoe SIL, CAN + Ethernet(UDP)
- 핵심 규칙:
  - `Emergency > Zone`
  - `Ambulance > Police`
  - 동률 시 `ETA 오름차순 -> SourceID 오름차순`
  - Timeout Clear: `1000ms`

---

## 3. 그림 구성 (확정)

| 문서 그림 번호 | 그림명 | 핵심 내용 | 연계 문서 |
|---|---|---|---|
| 02-01 | 전체 아키텍처 블록도 | VAL_SCENARIO_CTRL -> GW -> ETH_SW -> 중앙 경고코어 -> 출력 도메인 | 03, 0301, 0302 |
| 02-02 | 도메인/버스 분리도 | Chassis CAN / Infotainment CAN / Ethernet UDP 경계 | 0302, 0303 |
| 02-03 | 시나리오 체인도 | 스쿨존 과속 / 고속도로 무조향 / 긴급 접근-해제 | 0301, 05, 06, 07 |
| 02-04 | 중재/상태 전이도 | 경고 충돌 중재, 우선순위, 해제/복귀 | 0301, 04 |
| 02-05 | 추적성 연결도 | Req -> Func -> Flow -> Comm -> Var 경로 가시화 | 01, 0301~0304 |

---

## 4. 그림 캡션 초안 (삽입용)

### Figure 02-01. Option 1 시스템 아키텍처
- 입력: `VAL_SCENARIO_CTRL`
- 게이트웨이: `CHS_GW`, `INFOTAINMENT_GW`
- 중앙 코어: `ADAS_WARN_CTRL`, `NAV_CTX_MGR`, `EMS_ALERT`, `WARN_ARB_MGR`
- 출력: `BODY_GW -> AMBIENT_CTRL`, `IVI_GW -> CLU_HMI_CTRL`

### Figure 02-02. 도메인 네트워크 분리
- Chassis CAN: 차량 상태/조향 입력
- Infotainment CAN: 내비 문맥(roadZone/navDirection/zoneDistance/speedLimit)/클러스터 경고
- Ethernet UDP: 긴급 알림(E100), 중재 결과(E200)

### Figure 02-03. 핵심 시나리오 체인
- 스쿨존 과속
- 고속도로 무조향
- 경찰/구급 긴급 접근 + 1000ms 타임아웃 해제

### Figure 02-04. 경고 중재 상태도
- Normal -> Zone Warning -> Emergency Warning
- 충돌 시 중재 규칙 적용
- Clear/Timeout 시 이전 문맥 복귀

### Figure 02-05. 추적성 브리지
- 요구-기능-네트워크-통신-변수의 연결 구조를 단계별로 시각화
- 05/06/07 테스트 시나리오와의 역방향 추적 관계 표시

---
