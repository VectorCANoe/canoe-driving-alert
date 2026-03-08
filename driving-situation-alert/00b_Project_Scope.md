# 프로젝트 범위 및 검증 전략 (Project Scope and Verification Strategy)

**Document ID**: PROJ-00b-PS
**Version**: 2.10
**Date**: 2026-03-09
**Status**: Released
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 1. 프로젝트 범위

### 프로젝트 컨셉

본 프로젝트는 단일 데모 시나리오가 아니라, 완성차 시스템의 핵심 통신/판정/출력 체인을 SIL 환경에서 축약 구현하는 것을 목표로 한다.

- 차량 베이스: 시동/기어/가감속/조향/비상등/창문/클러스터 기본 기능
- 상태 입력 체인: 차량/내비/외부(V2X) 입력을 도메인 경계에서 정규화
- 판정 체인: 위험/경보 우선순위 판정과 fail-safe 전환
- 출력 체인: 클러스터/앰비언트/HMI 동기 출력 및 복귀
- 운영 원칙: 단일 시나리오 최적화보다 차량 전체 시스템 타당성을 우선
- Validation Harness(`VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`)는 SIL 검증 전용 계층이며 양산 기능/사용자 기능 범위에 포함하지 않는다.
- 역할 고정: `VAL_SCENARIO_CTRL`는 E2E 주입/관찰용 멀티버스 예외 노드, `VAL_BASELINE_CTRL`는 Chassis 단일버스 기반 결과 집계 노드로 운영한다.

본 프로젝트는 `CANoe SIL` 환경에서 아래 5개 기능군을 통합 검증한다.

1. Vehicle Baseline: **기본 차량 기능(시동/기어/입력/표시)**
2. Core Scenario: **내비게이션 구간 인식 컨텍스트 + 긴급차량 경고/중재**
3. V2 Extension: **근접 위험 산정 + 감속 보조 요청 + Fail-safe 강등 (`Req_120~121`, `Req_123`, `Req_125~129`)**
4. ADAS Extension (Pre-Activation): **객체 기반 위험 인지/경고 (`Req_130~139`)**
5. Alert UX/Robustness Extension (Pre-Activation): **경보 편의/강건성 확장 (`Req_140~155`)**

### 제외 범위 (명시적 Out of Scope)

- 위험운전 점수 기반 단계 경고(기존 Base B 요구사항)
- Drive Coach / Seasonal Theme / Smart Claim / UDS OTA
- 군집(Lead/Follow) 위협 대응
- 물류차 임무전환 OTA

---

## 2. 통합 핵심 흐름 (Red Thread)

```text
Navigation Context (gRoadZone, gNavDirection, gZoneDistance, gSpeedLimit)
  -> INFOTAINMENT_GW (CAN->ETH 정규화)
  -> ETH_SW
  -> NAV_CTX_MGR (구간 컨텍스트 활성)
  -> WARN_ARB_MGR

Vehicle State (gVehicleSpeed, gDriveState, SteeringInput)
  -> CHS_GW (CAN->ETH 정규화)
  -> ETH_SW
  -> ADAS_WARN_CTRL
  -> WARN_ARB_MGR

EMS_ALERT (internal: EMS_POLICE_TX / EMS_AMB_TX, `AMB`=Ambulance)
  -> ETH_SW (ETH_EmergencyAlert 브로드캐스트)
  -> EMS_ALERT (internal: EMS_ALERT_RX, 수신 차량)
  -> WARN_ARB_MGR

SelectedAlertContext
  -> ETH_SW
  -> BODY_GW -> AMBIENT_CTRL (Body CAN 출력, 0x210)
  -> IVI_GW -> CLU_HMI_CTRL (Infotainment CAN 출력, 0x220)

WARN_ARB_MGR
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

- Tool: Vector CANoe 19 SP4
- Network: Ethernet UDP 백본 + Domain CAN-HS
- Domain CAN 역할 분리: Body CAN(앰비언트, 0x210), Infotainment CAN(클러스터, 0x220)
- 아키텍처 고정: `ETH_SW + CHS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어(ADAS_WARN_CTRL/NAV_CTX_MGR/EMS_ALERT/WARN_ARB_MGR)`
- 주요 노드: `VAL_SCENARIO_CTRL`, `CHS_GW`, `INFOTAINMENT_GW`, `ETH_SW`, `ADAS_WARN_CTRL`, `NAV_CTX_MGR`, `EMS_ALERT`, `WARN_ARB_MGR`, `BODY_GW`, `IVI_GW`, `AMBIENT_CTRL`, `CLU_HMI_CTRL`
- EMS 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`)은 03/0301/0302/0303/0304 하단 보강표에서 분리 관리하며, `Ambient`는 항상 `AMBIENT` 풀토큰을 사용한다.
- Panel 입력: `gRoadZone`, `gNavDirection`, `gZoneDistance`, `gSpeedLimit`, 긴급차량 ON/OFF, ETA, 우선순위 테스트 토글

### 검증 제약 (필수)

- 물리 하드웨어(ECU, 센서, OBU, 외부 게이트웨이)는 사용하지 않는다.
- 모든 노드/신호/이벤트는 CANoe 가상 노드 + System Variable + Panel로만 생성한다.
- 통신 매체는 `CAN`과 `Ethernet(UDP)`만 사용한다.
- 외부 무선 스택(DSRC/C-V2X), 외부 HIL 장비, 실차 연동은 본 범위에서 제외한다.
- 검증/설계 판단은 개별 시연 장면보다 전체 시스템 연속성(입력->판정->출력->복귀)을 기준으로 한다.

---

## 5. 요구 분류/안전 프로파일 운영 기준

- 본 프로젝트의 요구사항 분류는 `Functional`, `Non-Functional`, `Interface`, `Verification-Acceptance`로 운영한다.
- `Req_041~Req_043`은 제품 기능 추가 요구가 아니라 고객 요구 검증을 위한 인수 조건으로 관리한다.
- 안전등급(QM/ASIL)은 HARA 근거 기반으로 확정하며, 현재 사이클은 `00d` 내부 승인 기준으로 QM/ASIL Candidate를 잠금 관리한다.
- 분류/안전 프로파일의 단일 기준 문서는 `00c_Req_Classification_and_Safety_Profile.md`를 사용한다.
- HARA 후보별 S/E/C 평가와 Safety Goal-검증 링크 근거는 `00d_HARA_Worksheet.md`를 기준으로 관리한다.

---

## 개정 이력

- 2.10 (2026-03-09): 프로젝트 컨셉 설명을 시나리오 중심 표현에서 OEM 시스템 체인(입력/판정/출력/복귀) 중심으로 부분 개편하고, 운영 원칙에 `단일 시나리오 최적화 금지`를 명시.
- 2.9 (2026-03-07): 00e Canonical 정합 반영으로 Scope/Red Thread/검증환경의 노드 표기를 `CHS_GW/ETH_SW/NAV_CTX_MGR/AMBIENT_CTRL` 기준으로 통일하고, 확장 기능군(`Req_120~129`, `Req_130~155`)을 현재 범위에 반영.
- 2.8 (2026-03-05): Validation Harness 노드 명칭을 `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`로 정리하고 범위 표기의 검증 전용 성격을 명확화.
- 2.7 (2026-03-04): HARA 내부 승인 기준 반영으로 안전등급 운영 문구를 `Provisional` 단계에서 `QM/ASIL Candidate 잠금` 단계로 갱신.
- 2.6 (2026-03-02): 요구 분류/안전 프로파일 운영 기준 섹션에 HARA 워크시트(`00d_HARA_Worksheet.md`) 연계 규칙을 추가.
- 2.5 (2026-03-02): 상위 범위 문서 표기를 `EMS_ALERT` 논리 단말 기준으로 통일하고 내부 TX/RX 모듈은 03계열 하단 보강표 분리 원칙으로 정리. 요구 분류/안전 프로파일 운영 기준(Req Type, Req_041~043 성격, HARA 전 Provisional 정책, 00c 참조)을 추가.
- 2.4 (2026-02-28): 멘토링 피드백 반영으로 Vehicle Baseline 기능군(시동/기어/입력/표시)을 프로젝트 범위에 추가.
- 2.3 (2026-02-28): Navigation Context 입력에 `gSpeedLimit`을 추가해 Req_010 과속 판정 기준(`vehicleSpeed > speedLimit`)과 0302/0303/0304 체인을 정합화.
- 2.2 (2026-02-26): SelectedAlertContext 출력 경로의 도메인 CAN 역할(Body 0x210 / Infotainment 0x220)을 명시해 0302/0303/04와 정합화.
- 2.1 (2026-02-25): 옵션1 아키텍처(ETH_SWITCH + 도메인 GW + 도메인 CAN) 기준으로 Red Thread와 검증 노드 구성 업데이트.
- 2.0 (2026-02-25): 범위 재정의. 구간 인식 컨텍스트 + 경찰/구급차 V2V 긴급알림/앰비언트 중재만 유지.
