# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.23
**Date**: 2026-03-07
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 하단 (SWE.3) | `04_SW_Implementation.md` | `0304_System_Variables.md` | `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

## 작성 원칙

- 본 문서는 구현 구조/모듈/인터페이스를 요약한다.
- 구현 아키텍처와 모듈 책임을 한눈에 파악할 수 있게 작성한다.
- 모듈 간 인터페이스 경계와 데이터 전달 방향을 명확히 유지한다.
- 테스트 문서(05~07)에서 재현 가능한 수준의 구현 정보를 제공한다.

---

## 1. 구현 아키텍처 요약

```text
Input CAN
  -> CHS_GW / INFOTAINMENT_GW (CAN->ETH 정규화)
  -> ETH_SW
  -> 중앙 경고코어 (ADAS_WARN_CTRL, NAV_CTX_MGR, EMS_ALERT, WARN_ARB_MGR)
  -> ETH_SW
  -> BODY_GW / IVI_GW (ETH->CAN 변환)
  -> AMBIENT_CTRL / CLU_HMI_CTRL

Emergency Source (logical terminal)
  -> EMS_ALERT (internal: EMS_POLICE_TX / EMS_AMB_TX)
  -> ETH_SW
  -> EMS_ALERT (internal: EMS_ALERT_RX)
```

## 2. 구현 모듈 명세 (공식 표준 양식)

| 구현 모듈 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Core |
| ADAS_WARN_CTRL | 차량 상태 입력 기반 경고 조건 판정 및 경고 시작/종료 제어 | Func_001~004,006,010~012,130,131,136,148 |
| NAV_CTX_MGR | 구간/방향/거리 입력을 컨텍스트로 변환 | Func_007 |
| EMS_ALERT | 긴급알림 송신(Tx) 및 수신/해제/타임아웃(Rx) 통합 관리 | Func_017,018,023,024,144 |
| WARN_ARB_MGR | 긴급/구간 충돌 중재 및 최종 경고 컨텍스트 생성 | Func_022,025,027~032,140~142,149,150,152 |
|  |  | Gateway/Network |
| CHS_GW | Chassis CAN 입력 정규화 및 ETH 송신 | 차량 상태 입력 경로 |
| INFOTAINMENT_GW | Infotainment CAN 입력(구간/방향/거리/제한속도) 정규화 및 ETH 송신 | 구간 컨텍스트 입력 경로 |
| ETH_SW | ETH 경로 헬스 모니터링(메시지 age 기반 path health 판정) | 도메인 경계 경로 상태 관리 |
| BODY_GW | 중재 결과 ETH 수신 후 Ambient CAN 송신 | 출력 분배 경로 |
| IVI_GW | 중재 결과 ETH 수신 후 Cluster CAN 송신 | 출력 분배 경로 |
|  |  | Output |
| AMBIENT_CTRL | 경고 레벨/타입 기반 앰비언트 패턴/색상 출력 | Func_008,009,013~016,033~039 |
| CLU_HMI_CTRL | 경고 문구/방향/유형 표시 및 중복 억제 | Func_005,019~021,026,040,143,145~147,153~155 |
|  |  | SIL Verification |
| VAL_SCENARIO_CTRL | 시나리오 실행, CAN+ETH 동시 검증, 결과 기록 | Func_041~043 |

- 상단 공식표는 감사 일관성을 위해 `EMS_ALERT` 논리 단말 기준으로 표기한다.
- EMS 송신/수신 기능은 논리 단말(`EMS_ALERT`) 기준으로 설명하며, 구현 상세는 코드 저장소 기준으로 관리한다.
- 프레임 포워딩은 Ethernet 스위칭 인프라(실차 스위치 또는 SIL 네트워크 스택)가 담당하고, `ETH_SW` CAPL은 도메인 경계 통신 상태 모니터링/진단 로직을 담당한다.

---
