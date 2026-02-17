# System Requirements Specification (시스템 요구사항 명세서)

**Document ID**: PART4-01-SRS
**ISO 26262 Reference**: Part 4, Clause 6
**ASPICE Reference**: SYS.2
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---


---

## 🔴 핵심 검증 시나리오 — Master E2E Scenario (Red Thread)

> 본 프로젝트의 모든 문서는 아래 시나리오를 중심 실(Red Thread)로 연결됩니다.
> ASPICE SYS.2는 "시나리오 기반 요구사항 도출"을 명시합니다.

```
[Phase 1] Fault Injection (고장 주입)
  BCM (Body Domain, CAN-LS)
    └─ Window Motor Overcurrent 감지 (50A > 정상 5A)
    └─ DTC B1234 저장 (ISO 14229 DTC Format)
    └─ BCM_FaultStatus CAN 메시지 전송 (CAN-LS, 0x500)

[Phase 2] Gateway Routing & Cluster Warning (중앙 게이트웨이 라우팅)
  Central Gateway (CGW)
    └─ CAN-LS 수신 (BCM_FaultStatus 0x500)
    └─ CAN-HS2 라우팅 → vECU (0x500 → CAN-HS2 broadcast)
    └─ Ethernet/DoIP 경로 제공 → OTA 서버 연결 (ISO 13400)
  vECU (CAN-HS2)
    └─ Cluster 경고등 활성화 (Warning Priority: P0)
    └─ DTC 이력 내부 기록

[Phase 3] UDS Diagnostics (진단 통신)
  CANoe Tester (CAPL 기반 진단 노드)
    └─ UDS 0x10 0x03 (Extended Diagnostic Session) → BCM
    └─ UDS 0x19 0x02 (Read DTC by Status Mask) → DTC B1234 수집
    └─ TCP/IP → 가상 OTA 서버 전송 (DTC 데이터 패킷)

[Phase 4] OTA Update (무선 업데이트)
  OTA Server (CANoe 가상 노드, Ethernet)
    └─ SW 버전 분석 → 업데이트 결정
    └─ UDS 0x10 0x02 (Programming Session) → BCM
    └─ UDS 0x34 (Request Download, 64KB)
    └─ UDS 0x36 × N (Transfer Data, 4KB/block)
    └─ UDS 0x37 (Transfer Exit)
    └─ BCM 재시작 → DTC 소거 → 정상 복귀 검증
```

**적용 표준**: ISO 14229-1 UDS, ISO 13400-2 DoIP, ISO 26262-4 (Safety), ASPICE PAM 3.1

---

---

## 1. 요구사항 개요

**총 요구사항**: 59개 (REQ-001~055 기존 + REQ-056~059 시나리오 보강)

| Category | Count | ASIL Distribution |
|----------|-------|-------------------|
| 기능 요구사항 (Functional) | 36 | D: 2, C: 4, B: 23, A: 1 |
| **시나리오 요구사항 (Scenario/E2E)** | **4** | **B: 2, A: 1, QM: 1** |
| 안전 요구사항 (Safety) | 11 | - |
| 비기능 요구사항 (Non-Functional) | 11 | - |

---

## 2. 요구사항 목록


### REQ-001: 스포츠모드 속도연동 엠비언트조명

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: IVI에서 스포츠 모드를 선택할 경우 차량 속도 CAN 신호를 실시간으로 수신하여 0~50km/h는 녹색 50~100km/h는 파란색 100km/h 이상은 빨간색으로 자동 변경하며 색상 변경은 500ms 이내에 반영되어야 한다
...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-002: 후진 안전경고 UI 및 시트조명

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-C
- **Description**: 변속 상태가 D에서 R로 변경되면 시스템은 즉시 이를 감지하여 IVI 화면에 안전 경고 UI를 표시하고 시트조명을 자동 점등하며 최소 3초 이상 유지해야 하고 조명 제어 실패 시 음성 경고를 추가로 출력해야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Safety (안전)

---


### REQ-003: 승하차 UX 도어연동제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-A
- **Description**: 차량 도어 개방 또는 폐쇄 신호 수신 시 승하차 편의성을 위한 조명 UX가 자동으로 활성화 또는 비활성화되어 사용자 편의성과 가시성을 향상시켜야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-004: IVI 조명색상 동기화

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 사용자가 IVI UI에서 조명 색상을 선택하면 해당 설정값이 CAN 메시지를 통해 vECU로 전달되고 실내 조명 제어 모듈에 정확히 반영되어야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-005: 온도연동 조명제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: HVAC 시스템에서 설정된 실내 온도 정보를 수신하여 미리 정의된 구간별 기준에 따라 조명 색상을 단계적으로 변경하고 사용자에게 직관적인 온도 피드백을 제공해야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-006: 후진중 도어개방 경고제어

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-D
- **Description**: 차량이 후진 상태일 때 도어 개방 신호가 감지되면 즉시 위험 상황으로 판단하여 경고 UI와 경고 조명을 활성화하고 운전자에게 시각적 주의를 제공해야 한다...
- **Verification Method**: HIL (Hardware-in-the-Loop)
- **Related Systems**: Safety (안전)

---


### REQ-007: 경고상태 자동복구기능

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-C
- **Description**: 후진 종료 또는 도어 닫힘 등 위험 조건이 해제되면 시스템은 자동으로 경고 상태를 종료하고 정상 운행 모드로 복귀해야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Safety (안전)

---


### REQ-008: 시스템 반응속도

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 사용자 입력 또는 센서 신호 수신 후 관련 기능이 활성화되기까지 전체 시스템 반응 시간이 1초 이내로 유지되어야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: CAN Communication

---


### REQ-009: 장시간 동작 안정성

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 연속 1시간 이상 시스템을 구동하여도 통신 오류 메모리 누수 또는 기능 오동작이 발생하지 않고 안정적으로 동작해야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: CAN Communication

---


### REQ-010: BCM FaultInjection DTC생성

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: BCM (Body Control Module) ECU 통신 오류 또는 센서 이상 상황을 인위적으로 주입했을 때 해당 오류를 정상적으로 감지하여 표준 DTC 코드로 저장해야 한다...
- **Verification Method**: Fault Injection Test
- **Related Systems**: Diagnostics (진단)

---


### REQ-011: UDS0x14 DTC삭제

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 진단 테스터에서 UDS 0x14 명령을 전송하면 ECU 내부에 저장된 모든 DTC 이력 정보가 정상적으로 삭제되고 재조회 시 출력되지 않아야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Diagnostics (진단)

---


### REQ-012: UDS0x34 OTA다운로드

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: UDS 0x34 서비스를 통해 OTA 패키지를 ECU로 전송하고 전송 완료 후 정상적으로 저장 및 적용되어야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Diagnostics (진단)

---


### REQ-013: OTA업데이트 후 기능검증

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: OTA 업데이트 완료 후 조명 안전 진단 기능이 사전 정의된 요구사항에 따라 정상 동작하는지 자동 테스트로 검증해야 한다...
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: Diagnostics (진단)

---


### REQ-014: OTA실패 자동복구

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-C
- **Description**: 업데이트 중 오류 또는 전원 차단 발생 시 시스템은 이전 정상 버전으로 자동 롤백하여 기능을 복구해야 한다...
- **Verification Method**: HIL (Hardware-in-the-Loop)
- **Related Systems**: Diagnostics (진단)

---


### REQ-015: 후진 기어 진입 시 UX 제어 기능 활성화

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 변속기 상태가 R이고 차량 속도가 5km/h 미만일 경우, 후진 연계 UX 제어 시스템은 활성 상태로 전이되어야 한다....
- **Verification Method**: SIL (Software-in-the-Loop)
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-016: 후진 시 후방 조명 자동 제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 후진 기어 진입 시 후방 조명은 자동으로 ON 되어야 하며, D/N 전환 시 OFF 되어야 한다....
- **Verification Method**: Integration Test, System Test
- **Related Systems**: Lighting Control (조명)

---


### REQ-017: 후진 보조 시트 위치 자동 조정

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 후진 시 운전자 시야 확보를 위해 사전 정의된 시트 위치로 이동해야 한다....
- **Verification Method**: Integration Test, System Test
- **Related Systems**: BDC Logic (바디 제어)

---


### REQ-018: 후진 상태 안내 UX 메시지 제공

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 후진 상태 진입 시 클러스터에 후진 안내 메시지가 표시되어야 한다....
- **Verification Method**: Integration Test, System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-019: 후진 경고음 제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 후진 상태에서 일정 조건(저속, 장애물 이벤트 등) 발생 시 경고음을 출력해야 한다....
- **Verification Method**: Integration Test
- **Related Systems**: Safety (안전)

---


### REQ-020: 속도 증가 시 UX 자동 해제

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 차량 속도가 10km/h 이상일 경우 후진 UX 기능은 비활성화되어야 한다....
- **Verification Method**: Integration Test, System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-021: 도어 오픈 시 후진 UX 제한

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 운전자 도어가 열려 있는 상태에서는 후진 UX 기능이 제한되어야 한다....
- **Verification Method**: Fault Injection Test
- **Related Systems**: Safety (안전)

---


### REQ-022: UX 제어 응답 시간

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 모든 UX 제어 기능은 입력 이벤트 발생 후 정의된 시간 내에 반응해야 한다....
- **Verification Method**: Integration Test, System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-023: 오류 발생 시 안전 상태 전이

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 센서 오류 또는 CAN 통신 오류 발생 시 UX 기능은 안전 상태로 전이되어야 한다....
- **Verification Method**: Fault Injection Test
- **Related Systems**: Safety (안전)

---


### REQ-024: CAN 메시지 처리 신뢰성

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: CAN 메시지 손실률은 허용 기준 이하로 유지되어야 한다....
- **Verification Method**: Integration Test
- **Related Systems**: CAN Communication

---


### REQ-025: UX 기능 확장 고려 설계

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Low (P3) - Phase 3
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 추가 UX 기능(카메라, HUD 등)을 고려한 구조로 설계되어야 한다....
- **Verification Method**: Peer Review/Static Analysis
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-026: 요구사항–테스트 추적성 확보

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 모든 요구사항은 테스트 케이스와 양방향 추적 가능해야 한다....
- **Verification Method**: Peer Review/Static Analysis
- **Related Systems**: Diagnostics (진단)

---


### REQ-027: 차선 이탈 발생 시 ADAS 연계 시각적 경고 UI 제공

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-C
- **Description**: 차량 주행 중 차선 이탈 경고(LDW) 이벤트가 발생하면,
vECU는 ADAS 센서 데이터를 CAN 통신을 통해 수신하여
대시보드 및 앰비언트 조명을 이용한 시각적 경고를 즉시 제공해야 한다.

해당 경고는 차선 이탈 상태가 해제될 때까지 유지되어야 하며,
CANoe 기반 vECU 시뮬레이션 환경에서 동일한 동작 시나리오가 반복 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: ADAS/자율주행

---


### REQ-028: 후진 시 ADAS 연계 앰비언트 조명 기반 시각적 경고 제공

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 차량이 후진 기어 상태로 진입하고,
후방 ADAS 센서에서 장애물이 감지되면
vECU는 CAN 통신을 통해 해당 정보를 수신하여
실내 앰비언트 조명을 점멸 방식으로 제어함으로써
운전자에게 시각적 경고를 제공해야 한다.

장애물 위험 상태가 해제되면 조명은 정상 상태로 복귀해야 하며,
본 동작은 CANoe 기반 vECU 시뮬레이션 환경에서
반복 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: ADAS/자율주행

---


### REQ-029: 긴급 제동 발생 시 ADAS 연계 대시보드 시각적 경고 제공

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-D
- **Description**: 차량 주행 중 ADAS 시스템에서 긴급 제동(AEB) 이벤트가 발생하면,
vECU는 해당 이벤트 정보를 수신하여
대시보드 영역에 고위험 시각적 경고 UI를 즉시 표시해야 한다.

경고 UI는 긴급 제동 상태가 종료될 때까지 유지되며,
CANoe 기반 vECU 시뮬레이션 환경에서
동일한 긴급 제동 시나리오가 반복 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: ADAS/자율주행

---


### REQ-030: 승하차 시 ADAS 연계 운전자 인지 UI 제공

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 차량 정차 상태에서 운전자가 하차를 위해 도어를 개방할 경우,
vECU는 ADAS 센서 데이터를 기반으로
차량 후측방 또는 주변 이동 객체(차량, 자전거 등)의 접근 여부를 확인해야 한다.

위험 객체가 감지된 경우,
센터페시아 UI를 통해 시각적 경고 메시지를 표시하여
운전자에게 하차 위험 상황을 인지시켜야 한다.

본 기능은 CANoe 기반 vECU 시뮬레이션 환경에서
반복 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: ADAS/자율주행

---


### REQ-031: ADAS 기능 활성 상태 안내 UI 표시

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Low (P3) - Phase 3
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 차량 주행 중 ADAS 기능이 활성화 또는 비활성화될 경우,
vECU는 해당 ADAS 상태 정보를 수신하여
센터페시아 UI 영역에 현재 ADAS 동작 상태를 아이콘 또는 텍스트 형태로 표시해야 한다.

본 UI는 운전자에게 시스템 상태를 인지시키기 위한 정보 제공 목적이며,
주행 제어 또는 안전 기능에 직접적인 영향을 주지 않는다.
해당 동작은 CANoe 기반 vECU 시뮬레이션 환경에서 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-032: ADAS 연계 UI 시각적 경고 반응 일관성 확보

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: ADAS 이벤트(후진 위험 감지, 차선 이탈, 긴급 제동 등)가 발생할 경우,
vECU는 시각적 경고 UI를 일정하고 일관된 반응 시간 내에 표시해야 한다.

동일한 ADAS 이벤트에 대해 UI 표시 지연 시간의 편차는 최소화되어야 하며,
CANoe 기반 vECU 시뮬레이션 환경에서 반복 수행 시에도
유사한 반응 특성을 유지해야 한다.

본 요구사항은 시스템 성능 및 사용자 인지 품질 향상을 목적으로 한다....
- **Verification Method**: SIL (Software-in-the-Loop), System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-033: ADAS 연계 시각적 경고 UI의 색상 및 표시 방식 일관성 유지

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Low (P3) - Phase 3
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: ADAS 이벤트(후진 위험, 차선 이탈, 긴급 제동 등)가 발생할 경우,
vECU는 시각적 경고 UI를 사전에 정의된 색상, 점멸 주기, 표시 영역 규칙에 따라
일관된 방식으로 출력해야 한다.

동일한 ADAS 이벤트에 대해
시각적 경고의 색상 또는 표시 위치가 임의로 변경되어서는 안 되며,
CANoe 기반 vECU 시뮬레이션 환경에서 반복 실행 시에도
동일한 UI 표현 결과를 유지해야 한다.

본 요구사항은 운전자 혼란 방지 및 인지 품질 향상을 목적으로 한다.
...
- **Verification Method**: SIL (Software-in-the-Loop), System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-034: ADAS 경고 UI 출력 실패 시 대체 시각적 안내 제공

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: ASIL-B
- **Description**: ADAS 이벤트(차선 이탈, 후진 위험, 긴급 제동 등)가 발생했으나
주요 시각적 경고 UI(대시보드 또는 센터페시아)가
출력되지 않거나 비정상 상태로 판단될 경우,
vECU는 사전에 정의된 대체 시각적 수단을 통해
운전자에게 위험 상황을 인지시켜야 한다.

대체 시각적 안내는
간소화된 경고 아이콘 또는 기본 색상 점등 형태로 제공되며,
본 동작은 CANoe 기반 vECU 시뮬레이션 환경에서
재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: Safety (안전)

---


### REQ-035: ADAS 고위험 상황 발생 시 비핵심 UI 자동 제한 기능

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: ASIL-B
- **Description**: 차량 주행 중 ADAS 시스템에서 고위험 이벤트
(차선 이탈, 긴급 제동, 후진 장애물 근접 등)가 발생하면,
vECU는 운전자의 주의 분산을 최소화하기 위해
비핵심 UI 요소(미디어 정보, 설정 팝업, 알림 메시지 등)를
일시적으로 제한해야 한다.
ADAS 고위험 상태가 해제되면,
제한되었던 UI는 자동으로 정상 상태로 복귀해야 하며,
본 동작은 CANoe 기반 vECU 시뮬레이션 환경에서
반복 재현 가능해야 한다....
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-036: 주행 종료 후 ADAS 위험 상황 요약 UI 제공

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Low (P3) - Phase 3
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 차량 주행이 종료되고 시동이 OFF 되면,
vECU는 해당 주행 중 발생한 ADAS 이벤트
(차선 이탈 경고, 후진 장애물 경고, 긴급 제동 등)를
요약 정보 형태로 센터페시아 UI에 표시해야 한다.

요약 UI에는 이벤트 발생 횟수 및 주요 발생 유형이 포함되며,
운전자가 주행 중 경험한 위험 상황을
사후에 인지하고 개선할 수 있도록 지원한다.

본 기능은 주행 중 차량 제어 또는 안전 동작에는 개입하지 않으며,
CANoe 기반 vECU 시뮬레이션 환경에서
이벤트 로그 기반으로 재현 가능해야 한다.
...
- **Verification Method**: SIL (Software-in-the-Loop), System Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-037: 다중 ADAS 이벤트 발생 시 우선순위 기반 시각적 안내 제공

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: ASIL-B
- **Description**: 차량 주행 중 두 개 이상의 ADAS 이벤트
(예: 차선 이탈 경고, 전방 충돌 경고, 후방 장애물 감지)가
동시에 발생하거나 짧은 시간 간격으로 연속 발생할 경우,
vECU는 사전에 정의된 위험도 기준에 따라
이벤트의 우선순위를 판단해야 한다.

가장 위험도가 높은 ADAS 이벤트는
대시보드 또는 센터페시아 UI의 주요 영역에 우선 표시되어야 하며,
우선순위가 낮은 이벤트는 보조 표시 또는 요약 형태로 제공되어
운전자의 인지 혼란을 방지해야 한다.

본 기능은 CANoe 기반 vECU 시뮬레이션 환경에서
다중 이벤트 시나리오를 통...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **Related Systems**: ADAS/자율주행

---


### REQ-038: IVI 모드 선택 시 조명 테마 자동 적용

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 사용자가 IVI 화면에서 스포츠/에코/컴포트 모드 선택 시, 해당 테마의 조명 색상·밝기·효과 패키지 일괄 적용 (응답시간 <100ms)...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: Lighting Control (조명)

---


### REQ-039: 운전자 프로필 기반 조명 개인화

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 운전자 프로필(계정)에서 선호 조명 색/밝기/알림 강도를 저장 및 관리, 프로필 전환 시 자동 적용 (최대 3개 프로필)...
- **Verification Method**: SIL (Software-in-the-Loop), Unit Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-040: 주행 컨텍스트 기반 조명 씬(Scenes) 제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI에서 주행 상황 씬 선택 (야간 고속도로/도심 정체/주차 대기) 시, 해당 씬의 조명·경고·알림 패턴 자동 활성화...
- **Verification Method**: SIL (Software-in-the-Loop), HIL (Hardware-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-041: 사용자 정의 조명 시나리오 편집 & 저장

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI 화면에서 속도 조건/시간대/주차상태 기반 조명 시나리오를 간단히 편집·저장, 저장된 시나리오는 vECU 파라미터로 내려가 OTA 배포 가능...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-042: 이벤트 시뮬레이션 & 재생 모드 (CANoe 연계)

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI에서 이벤트 시퀀스(후진→도어 오픈→주차) 선택 시 CANoe와 연계해 해당 시나리오를 가상 재생하고 조명/경고 UI 반응을 시각적으로 확인...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-043: 정비 모드용 IVI 자진단 수행 화면

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: 서비스 모드 진입 시 IVI에서 간단한 체크리스트 버튼 제공, 정비사 선택 시 vECU가 내부 자진단 수행 후 결과를 그래픽으로 표시 (Pass/Fail)...
- **Verification Method**: HIL (Hardware-in-the-Loop), Integration Test, Peer Review/Static Analysis
- **Related Systems**: Diagnostics (진단)

---


### REQ-044: 조명 테마 & 시나리오 OTA 업데이트 관리

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: IVI에서 조명 테마/시나리오 정의가 vECU 파라미터로 저장되어 있으며, UDS 0x34/0x36/0x37 서비스를 통해 이 파라미터 집합을 OTA로 갱신 가능 (배포 시간 <45초)...
- **Verification Method**: Integration Test, System Test, Fault Injection Test
- **Related Systems**: OTA Update (업데이트)

---


### REQ-045: 조명 테마 A/B 테스트 기능

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI에서 조명 테마 A/B를 번갈아 적용하고, 사용자가 선호도 선택 시 그 결과와 사용 패턴을 로깅해 다음 SW 배포 시 반영 가능한 데이터로 활용...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-046: 사용자 피드백 연동 진단 로그 태깅

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 사용자가 IVI에서 '이 경고는 불편하다/너무 밝다/늦다'를 신고하면, 그 시점의 vECU 상태·CAN 로그에 태그를 남겨 후속 분석과 SW 개선에 활용...
- **Verification Method**: SIL (Software-in-the-Loop), Unit Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-047: OTA 전후 기능 변경 이력 뷰어 (IVI 관점)

- **Category**: 진단/OTA 요구사항 (Diagnostic/OTA)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI에서 각 조명/경고 기능에 대해 '현재 버전, 이전 버전, 변경점'을 보여주고, 필요 시 이전 버전 행동을 리플레이하는 기능 (OTA가 주제 아니라 IVI에서 보이는 기능 변경 추적이 주제)...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: OTA Update (업데이트)

---


### REQ-048: 야간 승하차 안전 조명 시스템

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 어두운 환경에서 도어 오픈 시 IVI 감지 후 바닥·발판 조명 자동 점등, 후석 승하차 알림, 동승자 방향에 맞춘 조명 강조 (응답시간 <80ms)...
- **Verification Method**: HIL (Hardware-in-the-Loop), Fault Injection Test
- **Related Systems**: Safety (안전)

---


### REQ-049: 주차장 위치 찾기 지원 조명 모드

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 시동 OFF 후 일정 시간 내 복귀 시, IVI에서 조명/경고 패턴을 활용해 차량을 쉽게 찾도록 하는 '찾기 모드' 활성화 (헤드/테일 조명 깜빡임, 사이드 조명 펄스)...
- **Verification Method**: SIL (Software-in-the-Loop), HIL (Hardware-in-the-Loop)
- **Related Systems**: Lighting Control (조명)

---


### REQ-050: 기상 조건 인지 UX 대시보드

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: 와이퍼/레인센서 정보 기반으로 비·눈 감지 시, IVI에서 실내 조명 톤을 따뜻하게 조정하고 외부 조명 상태(전조등/안개등/와이퍼)를 한 화면에 통합 표시...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: Lighting Control (조명)

---


### REQ-051: 어린이 보호 모드 통합 UX

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: ASIL-B
- **Description**: IVI에서 '어린이 보호 모드' 활성화 시, 뒷좌석 탑승 감지 + 도어 락·조명·알림·환기를 통합 관리, 시동 OFF 후 일정 시간 실내 모니터링 (좌석 점유 감지)...
- **Verification Method**: HIL (Hardware-in-the-Loop), Fault Injection Test, Peer Review/Static Analysis
- **Related Systems**: Safety (안전)

---


### REQ-052: 장시간 정차·졸음 방지 UX 알림

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI에서 장시간 정차·저속 주행 시 감지 후, 조명과 사운드를 이용한 졸음 경고 및 환기/휴식 알림 제공 (경고 주기 조정 가능)...
- **Verification Method**: SIL (Software-in-the-Loop), Integration Test
- **Related Systems**: UI/UX (인포테인먼트)

---


### REQ-053: 조명 제어 안전 모니터링

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 조명 제어 명령 2회 이상 연속 실패 시 Fail-Safe 모드 진입 (기본값 50% 밝기)...
- **Verification Method**: HIL (Hardware-in-the-Loop), Integration Test, Peer Review/Static Analysis
- **Related Systems**: Safety (안전)

---


### REQ-054: CAN 통신 안정성

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI vECU CAN 메시지 전송 성공률 99.9% 이상 유지, CAN 통신 지연 <10ms...
- **Verification Method**: Unit Test, Integration Test
- **Related Systems**: CAN Communication

---


### REQ-055: 시스템 가용성

- **Category**: 비기능 요구사항 (Non-Functional)
- **Priority**: Medium (P2) - Phase 2
- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Description**: IVI vECU 재시작 시간 <3초, 부팅 후 CAN 통신 정상화 <5초...
- **Verification Method**: HIL (Hardware-in-the-Loop), System Test
- **Related Systems**: Diagnostics (진단)

---



## 3. ASPICE SYS.2 Work Products

- ✅ System Requirements Specification (본 문서)
- ✅ Traceability to Stakeholder Requirements
- ✅ ASIL Classification
- ✅ Verification Methods Defined

---


---

### REQ-056: UDS Session Control — Diagnostic/Programming Session 전환

- **Category**: 시나리오 요구사항 (Scenario — Diagnostics)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 진단 Tester는 UDS 0x10 서비스를 통해 ECU의 진단 세션을 전환해야 한다.
  Default Session(0x01) → Extended Session(0x03) → Programming Session(0x02) 전환이 가능해야 하며,
  각 세션 전환은 Positive Response(0x50) 또는 Negative Response(0x7F + NRC)로 응답해야 한다.
  세션 타임아웃(P3=5000ms) 초과 시 Default Session으로 자동 복귀해야 한다.
- **Verification Method**: SIL (CANoe CAPL Tester), Unit Test
- **Related Systems**: Diagnostics (진단), Central Gateway
- **Traceability**: FSR-B03, SG-06 → TC-SWQUAL-301

---

### REQ-057: UDS Read DTC Information — DTC 수집 및 전송

- **Category**: 시나리오 요구사항 (Scenario — Diagnostics)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: ASIL-B
- **Description**: 진단 Tester는 UDS 0x19 서비스를 통해 BCM에 저장된 DTC 정보를 수집해야 한다.
  서브함수: 0x02 (Read DTC by Status Mask), 0x06 (Read DTC Extended Data),
  0x09 (Read DTC with Snapshot). 수집된 DTC는 TCP/IP를 통해 가상 OTA 서버로 전송되어야 한다.
  BCM에 DTC B1234 (Window Motor Overcurrent) 주입 시 0x19 0x02 응답에 포함되어야 한다.
- **Verification Method**: SIL (CANoe CAPL Tester), Fault Injection Test
- **Related Systems**: Diagnostics (진단), Central Gateway
- **Traceability**: FSR-B03, SG-06 → TC-SWQUAL-302

---

### REQ-058: Central Gateway OTA Path — DoIP 연결을 통한 OTA 서버 통신

- **Category**: 시나리오 요구사항 (Scenario — Gateway/OTA)
- **Priority**: Critical (P0) - Phase 1
- **ASIL**: QM (Gateway routing은 OTA 품질 관리 범위)
- **Description**: Central Gateway는 CAN-LS (BCM Domain) 메시지를 수신하여
  CAN-HS2 (vECU)로 라우팅하고, 동시에 Ethernet/DoIP (ISO 13400-2)를 통해
  가상 OTA 서버와 연결되는 경로를 제공해야 한다.
  CANoe 환경에서는 CAPL TCP/IP 소켓으로 OTA 서버를 모사(Mocking)한다.
  Gateway 라우팅 지연: CAN-LS → CAN-HS2 ≤ 5ms, CAN → DoIP 변환 ≤ 10ms.
- **Verification Method**: SIL (CANoe 3-Bus Simulation), Integration Test
- **Related Systems**: Central Gateway, OTA Update, CAN Communication
- **Traceability**: FSR-B04, SG-09 → TC-SYS-011

---

### REQ-059: E2E Scenario Regression Coverage — 전 시나리오 자동화 검증

- **Category**: 시나리오 요구사항 (Scenario — E2E)
- **Priority**: High (P1) - Phase 1-2
- **ASIL**: QM
- **Description**: CANoe 환경에서 Fault Injection → Diagnostics → OTA Update의 전체 시나리오를
  단일 자동화 테스트 스크립트로 반복 실행할 수 있어야 한다.
  시나리오 총 소요 시간: < 120초. 회귀 테스트(Regression) 목적으로 반복 실행 가능해야 하며,
  Pass/Fail 결과를 자동으로 로깅해야 한다. (CI/CD 연계 가능)
- **Verification Method**: SIL Automation (CANoe Test Module)
- **Related Systems**: All (E2E)
- **Traceability**: SG-08, QR-01 → TC-SYS-013

---

**Auto-generated from**: /Users/juns/code/work/mobis/PBL/REQ_IVI_vECU_Requirements.xlsx
**Generation Date**: 2026-02-14 14:22:46
