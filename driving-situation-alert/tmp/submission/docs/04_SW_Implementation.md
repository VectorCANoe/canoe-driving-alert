# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.22
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 하단 (SWE.3) | `04_SW_Implementation.md` | `0304_System_Variables.md` | `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 구현 구조/모듈/인터페이스를 요약한다.
- 제출본은 상단 공식 모듈 표를 유지하고, 하단은 대표 추적만 유지한다.
- 전수 Func-Code-UT/IT/ST 매핑은 원문 04에서 관리한다.
- 05/06/07 문서와 추적 키 일관성을 유지한다.
- Pre-Activation 라벨은 원문과 동일하게 유지한다.

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
| CHS_GW | Chassis CAN 입력 정규화 및 ETH 송신 | Flow_001,002 |
| INFOTAINMENT_GW | Infotainment CAN 입력(구간/방향/거리/제한속도) 정규화 및 ETH 송신 | Flow_003 |
| ETH_SW | ETH 경로 헬스 모니터링(메시지 age 기반 path health 판정) | Flow_001~008 |
| BODY_GW | 중재 결과 ETH 수신 후 Ambient CAN 송신 | Flow_007 |
| IVI_GW | 중재 결과 ETH 수신 후 Cluster CAN 송신 | Flow_008 |
|  |  | Output |
| AMBIENT_CTRL | 경고 레벨/타입 기반 앰비언트 패턴/색상 출력 | Func_008,009,013~016,033~039 |
| CLU_HMI_CTRL | 경고 문구/방향/유형 표시 및 중복 억제 | Func_005,019~021,026,040,143,145~147,153~155 |
|  |  | SIL Verification |
| VAL_SCENARIO_CTRL | 시나리오 실행, CAN+ETH 동시 검증, 결과 기록 | Func_041~043 |

- 상단 공식표는 감사 일관성을 위해 `EMS_ALERT` 논리 단말 기준으로 표기한다.
- 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`) 분해는 본문 상세 추적표(3장, 4장)에서 관리한다.
- 프레임 포워딩은 Ethernet 스위칭 인프라(실차 스위치 또는 SIL 네트워크 스택)가 담당하고, `ETH_SW` CAPL은 경로 상태 모니터링/진단 로직을 담당한다.

---

## 구현 추적 요약 (제출본)

- 제출본은 상단 구현 모듈 명세를 기준으로 하단 상세 추적표를 대표행 중심으로 축소한다.
- 전수 `Func -> Code -> UT/IT/ST` 매핑은 원문 SoT(`driving-situation-alert/04_SW_Implementation.md`)를 기준으로 관리한다.

| 구분 | Func 범위 | 핵심 구현 모듈 | 주요 입출력 | 테스트 연결 |
|---|---|---|---|---|
| Core 경고 판정 | Func_001~Func_012 | ADAS_WARN_CTRL | vehicleSpeedNorm, steeringInputNorm -> warningState | UT_ADAS_001 / IT_CORE_001 |
| 긴급 수신/우선 판정 | Func_017~Func_032 | EMS_ALERT, WARN_ARB_MGR | emergencyType, eta -> selectedAlertLevel/Type | UT_EMS_RX_001 / IT_ARB_001 |
| 표시 출력 | Func_033~Func_040 | AMBIENT_CTRL, CLU_HMI_CTRL | selectedAlertType -> ambientPattern/warningTextCode | UT_BCM_001 / IT_OUT_001 |
| Baseline 확장 | Func_101~Func_119 | ENG_CTRL, TCM, HAZARD_CTRL, WINDOW_CTRL, CLU_BASE_CTRL | 차량 기본 입력/상태 -> 기본 표시/제어 | UT_BASE_EXT_001 / IT_BASE_EXT_001 |
| V2 확장(활성) | Func_120,121,123,125~129 | ADAS_WARN_CTRL, WARN_ARB_MGR, DOMAIN_BOUNDARY_MGR | proximityRiskLevel, failSafeMode -> decelAssistReq/경고 유지 | UT_V2_001 / IT_V2_001 / ST_V2_001 |
| ADAS 객체 인지(계획) | Func_130~Func_139 | ADAS_WARN_CTRL, WARN_ARB_MGR | objectTrackValid, objectTtcMin -> objectRiskClass/경고 출력 | UT_ADAS_OBJ_RISK_001(Planned) |
| 경보 편의(계획) | Func_140~Func_147 | WARN_ARB_MGR, CLU_HMI_CTRL | TurnLampState, VolumeLevel -> 경보 정책/표시 반영 | UT_BASE_ALERT_EXT_001(Planned) |
| 강건성·인지성(계획) | Func_148~Func_155 | ADAS_WARN_CTRL, DOMAIN_BOUNDARY_MGR, CLU_HMI_CTRL | objectConfidence, failSafeMode -> 대체 출력/동기 복원 | UT_BASE_ROBUST_EXT_001(Planned) |

## 인터페이스 요약 (SWE.3 BP2 축소본)

| 인터페이스 | 입력 | 출력 | 타이밍 | 예외 |
|---|---|---|---|---|
| CAN Ingestion | 도메인 CAN 프레임 | 정규화 Core 변수 | 100ms | invalid 값 필터링 |
| ETH Core Link | ETH 논리 계약(E100/E200/E213~E216) | 중재/상태 변수 | 50~100ms + Event | CANoe.CAN 환경은 stub 대체 |
| Output Dispatch | selectedAlertLevel/Type | Ambient/Cluster CAN 출력 | 50ms | timeoutClear/failSafeMode 반영 |
| Validation Harness | testScenario/sysvar 입력 | scenarioResult/log | Event | 양산 경로와 분리 |

---
