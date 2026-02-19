# 01_Requirements Traceability Matrix (요구사항 추적성 매트릭스)

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | IVI vECU 프로젝트 요구사항 추적성 매트릭스 |
| **작성 기준** | ISO 26262 Part 8, ASPICE SYS.2/SYS.3 |
| **작성일** | 2026-02-14 |
| **버전** | 1.0 |
| **총 요구사항** | 56개 |
| **적용 표준** | ISO 26262-6, ASPICE 3.1 (SYS.2 BP6, SYS.3 BP6) |

---

## 목적 및 범위

본 문서는 **ISO 26262 Part 8 (Supporting Processes)** 및 **ASPICE SYS.2/SYS.3** 프로세스 요구사항에 따라:

1. **시스템 요구사항 (System Requirements)** 을 **시스템 아키텍처 (System Architecture)** 로 할당 (Allocation)
2. **양방향 추적성 (Bidirectional Traceability)** 확보
3. **일관성 (Consistency)** 검증
4. **안전 목표 (Safety Goals)** 와 **ASIL 등급** 매핑

---

## 도메인 아키텍처 (Domain Architecture)

### 현대기아 생태계 기반 도메인 분류

본 프로젝트는 **현대기아 CAN DBC 레퍼런스**를 기반으로 5개 도메인으로 구성됩니다.

| Domain ID | Domain Name | 설명 | CAN Network | ASIL |
|-----------|-------------|------|-------------|------|
| **DOM_01** | Infotainment Domain | 운전자 인터페이스, 엔터테인먼트 | CAN 500 kbps | QM / ASIL-A |
| **DOM_02** | Body Domain | 차체 제어, 조명, HVAC | CAN 500 kbps | ASIL-B |
| **DOM_03** | ADAS Domain | 첨단 운전자 보조 시스템 | CAN 500 kbps | ASIL-D |
| **DOM_04** | Powertrain Domain | 엔진, 변속기 제어 | CAN 500 kbps | ASIL-C |
| **DOM_05** | Chassis Domain | 조향, 제동, 차량 안정성 | CAN 500 kbps | ASIL-D |

---

## ECU 할당 (ECU Allocation)

### DOM_01: Infotainment Domain

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_IVI_01** | IVI Control ECU | 인포테인먼트 제어, HMI | vehicle_system.dbc | CAN | QM |
| **ECU_IVI_02** | vECU (IVI vECU) | **가상 ECU, 조명/경고/ADAS UI 통합 제어** | **본 프로젝트 신규** | CAN | ASIL-B |
| **ECU_IVI_03** | Cluster ECU | 계기판 표시 | hyundai_kia_generic.dbc (CLU) | CAN | ASIL-A |
| **ECU_IVI_04** | HUD ECU | Head-Up Display | hyundai_kia_generic.dbc (HUD) | CAN | QM |

### DOM_02: Body Domain

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_BODY_01** | BCM (Body Control Module) | 차체 통합 제어 | vehicle_system.dbc (BCM) | CAN | ASIL-B |
| **ECU_BODY_02** | Lighting Control ECU | Ambient 조명 제어 | **본 프로젝트 신규 (BCM 분리)** | CAN | ASIL-A |
| **ECU_BODY_03** | HVAC Control ECU | 공조 제어 | vehicle_system.dbc (HVAC) | CAN | QM |
| **ECU_BODY_04** | BDC (Body Domain Controller) | 도어, 시트 센서 통합 | hyundai_kia_generic.dbc (BCM 통합) | CAN | ASIL-A |
| **ECU_BODY_05** | Door Sensors | 도어 개폐 감지 | vehicle_system.dbc (BCM_DoorStatus) | CAN | ASIL-A |
| **ECU_BODY_06** | Seat Control ECU | 시트 위치 제어 | vehicle_system.dbc (BCM_SeatStatus) | CAN | QM |

### DOM_03: ADAS Domain

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_ADAS_01** | ADAS Control ECU | ADAS 통합 제어 | **본 프로젝트 신규** | CAN | ASIL-D |
| **ECU_ADAS_02** | Front Camera (LDW) | 차선 이탈 경고 | vehicle_system.dbc (Camera) | CAN | ASIL-D |
| **ECU_ADAS_03** | Rear Camera (RVC) | 후방 카메라, 장애물 감지 | vehicle_system.dbc (Rear_Camera) | CAN | ASIL-C |
| **ECU_ADAS_04** | Radar (BSD) | 후측방 감지 | vehicle_system.dbc (Radar) | CAN | ASIL-D |
| **ECU_ADAS_05** | SCC (Smart Cruise Control) | 적응형 순항 제어, AEB | vehicle_system.dbc (SCC) | CAN | ASIL-D |
| **ECU_ADAS_06** | AVM ECU | Around View Monitor | hyundai_kia_generic.dbc (AVM) | CAN | ASIL-B |

### DOM_04: Powertrain Domain

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_PT_01** | EMS (Engine Management System) | 엔진 제어 | vehicle_system.dbc (EMS) | CAN | ASIL-C |
| **ECU_PT_02** | TCU (Transmission Control Unit) | 변속기 제어 | vehicle_system.dbc (TCU) | CAN | ASIL-C |
| **ECU_PT_03** | Vehicle Speed Sensor | 차량 속도 센서 | vehicle_system.dbc (EMS_EngineStatus) | CAN | ASIL-B |

### DOM_05: Chassis Domain

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_CH_01** | ESP/ESC (Electronic Stability Program) | 차량 안정성 제어 | vehicle_system.dbc (ESP) | CAN | ASIL-D |
| **ECU_CH_02** | MDPS (Motor Driven Power Steering) | 전동 조향 | vehicle_system.dbc (MDPS) | CAN | ASIL-D |
| **ECU_CH_03** | ABS (Anti-lock Braking System) | 제동 제어 | hyundai_kia_generic.dbc (ABS) | CAN | ASIL-D |
| **ECU_CH_04** | EPB (Electric Parking Brake) | 전자식 주차 브레이크 | hyundai_kia_generic.dbc (EPB) | CAN | ASIL-C |

### Gateway

| ECU ID | ECU Name | 기능 | DBC 출처 | 통신 | ASIL |
|--------|----------|------|----------|------|------|
| **ECU_GW_01** | Central Gateway (CGW) | 도메인 간 메시지 라우팅 | vehicle_system.dbc (CGW) | CAN | ASIL-B |

---

## 요구사항 할당 매트릭스 (Requirements Allocation Matrix)

### ISO 26262 & ASPICE 추적성 기준

- **SYS.2 BP6**: 시스템 요구사항과 시스템 요소(ECU) 간 추적성
- **SYS.3 BP6**: 시스템 아키텍처(Domain/ECU)와 시스템 요구사항 간 추적성
- **Bidirectional**: 요구사항 → ECU, ECU → 요구사항 양방향 추적

---

## Domain(ECU(Requirements)) 상세 매핑

### 1. DOM_01: Infotainment Domain

#### ECU_IVI_02 (vECU - IVI vECU) ⭐ **핵심 ECU**

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_001 | 스포츠모드 속도연동 엠비언트조명 | ASIL-B | HIL, SIL | Vehicle Speed 입력 필요 |
| Req_004 | IVI 조명색상 동기화 | ASIL-A | Integration Test | IVI → vECU CAN 통신 |
| Req_008 | 시스템 반응속도 (1초 이내) | ASIL-B | Performance Test | 타이밍 요구사항 |
| Req_009 | 장시간 동작 안정성 | ASIL-B | Reliability Test | 1시간 연속 구동 |
| Req_010 | BDC FaultInjection DTC생성 | ASIL-B | Fault Injection | UDS 0x19 ReadDTC |
| Req_011 | UDS0x14 DTC삭제 | ASIL-B | Diagnostic Test | UDS 0x14 ClearDTC |
| Req_012 | UDS0x34 OTA다운로드 | ASIL-B | OTA Test | UDS 0x34 RequestDownload |
| Req_013 | OTA업데이트 후 기능검증 | ASIL-B | Regression Test | 자동 테스트 스위트 |
| Req_014 | OTA실패 자동복구 | ASIL-C | Fail-Safe Test | Rollback 검증 |
| Req_038 | IVI 모드 선택 시 조명 테마 자동 적용 | ASIL-A | Integration Test | 스포츠/에코/컴포트 모드 |
| Req_039 | 운전자 프로필 기반 조명 개인화 | ASIL-A | User Acceptance Test | 최대 3개 프로필 |
| Req_040 | 주행 컨텍스트 기반 조명 씬 제어 | ASIL-B | Scenario Test | 야간/도심/주차 씬 |
| Req_041 | 사용자 정의 조명 시나리오 편집 & 저장 | QM | Functional Test | OTA 배포 가능 |
| Req_042 | 이벤트 시뮬레이션 & 재생 모드 (CANoe 연계) | QM | MIL, SIL | CANoe 시뮬레이션 |
| Req_043 | 정비 모드용 IVI 자진단 수행 화면 | ASIL-A | Service Test | Pass/Fail 판정 |
| Req_044 | 조명 테마 & 시나리오 OTA 업데이트 관리 | ASIL-B | OTA Test | UDS 파라미터 갱신 |
| Req_045 | 조명 테마 A/B 테스트 기능 | QM | User Test | 사용 패턴 로깅 |
| Req_046 | 사용자 피드백 연동 진단 로그 태깅 | QM | Logging Test | CAN 로그 태깅 |
| Req_047 | OTA 전후 기능 변경 이력 뷰어 | QM | Version Test | 변경점 표시 |

**총 18개 요구사항** | ASIL-C: 1개, ASIL-B: 9개, ASIL-A: 4개, QM: 4개

#### ECU_IVI_03 (Cluster ECU)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_002 | 후진 안전경고 UI 표시 | ASIL-C | HIL, Integration | vECU → Cluster 경고 UI |
| Req_006 | 후진중 도어개방 경고 UI 표시 | ASIL-C | HIL, Fault Injection | 위험 상황 경고 |
| Req_018 | 후진 상태 안내 UX 메시지 제공 | ASIL-A | Integration Test | 후진 진입 메시지 |
| Req_027 | 차선 이탈 시 대시보드 시각적 경고 UI | ASIL-D | ADAS HIL | LDW 이벤트 연동 |
| Req_029 | 긴급 제동 시 대시보드 시각적 경고 | ASIL-D | ADAS HIL | AEB 이벤트 연동 |
| Req_031 | ADAS 기능 활성 상태 안내 UI | ASIL-A | Integration Test | 아이콘/텍스트 표시 |
| Req_036 | 주행 종료 후 ADAS 위험 상황 요약 UI | QM | User Test | 이벤트 요약 정보 |

**총 7개 요구사항** | ASIL-D: 2개, ASIL-C: 2개, ASIL-A: 2개, QM: 1개

---

### 2. DOM_02: Body Domain

#### ECU_BODY_02 (Lighting Control ECU)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_001 | 스포츠모드 속도연동 엠비언트조명 | ASIL-B | HIL | vECU → Lighting 제어 |
| Req_003 | 승하차 UX 도어연동제어 | ASIL-A | Integration Test | 도어 신호 연동 |
| Req_005 | 온도연동 조명제어 | ASIL-A | Integration Test | HVAC 온도 신호 |
| Req_016 | 후진 시 후방 조명 자동 제어 | ASIL-B | HIL | R 기어 → 조명 ON |
| Req_028 | 후진 시 ADAS 연계 앰비언트 조명 경고 | ASIL-C | ADAS HIL | 점멸 제어 |
| Req_048 | 야간 승하차 안전 조명 시스템 | ASIL-B | Night Test | 바닥/발판 조명 |
| Req_049 | 주차장 위치 찾기 지원 조명 모드 | QM | User Test | 찾기 모드 활성화 |
| Req_053 | 조명 제어 안전 모니터링 | ASIL-B | Fail-Safe Test | Fail-Safe 50% 밝기 |

**총 8개 요구사항** | ASIL-C: 1개, ASIL-B: 4개, ASIL-A: 2개, QM: 1개

#### ECU_BODY_01 (BCM - Body Control Module)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_003 | 승하차 UX 도어연동제어 | ASIL-A | Integration Test | 도어 개폐 신호 전송 |
| Req_006 | 후진중 도어개방 경고제어 | ASIL-C | Fault Injection | 도어 센서 감지 |
| Req_021 | 도어 오픈 시 후진 UX 제한 | ASIL-B | Safety Test | 안전 기능 제한 |
| Req_030 | 승하차 시 ADAS 연계 운전자 인지 UI | ASIL-B | ADAS Integration | 후측방 객체 감지 |
| Req_051 | 어린이 보호 모드 통합 UX | ASIL-B | Safety Test | 뒷좌석 탑승 감지 |

**총 5개 요구사항** | ASIL-C: 1개, ASIL-B: 3개, ASIL-A: 1개

#### ECU_BODY_06 (Seat Control ECU)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_002 | 후진 시 시트조명 자동 점등 | ASIL-C | Integration Test | 최소 3초 유지 |
| Req_017 | 후진 보조 시트 위치 자동 조정 | ASIL-A | Integration Test | 시야 확보 위치 |

**총 2개 요구사항** | ASIL-C: 1개, ASIL-A: 1개

#### ECU_BODY_03 (HVAC Control ECU)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_005 | 온도연동 조명제어 | ASIL-A | Integration Test | 실내 온도 정보 전송 |
| Req_050 | 기상 조건 인지 UX 대시보드 | QM | User Test | 와이퍼/레인센서 연동 |

**총 2개 요구사항** | ASIL-A: 1개, QM: 1개

---

### 3. DOM_03: ADAS Domain

#### ECU_ADAS_02 (Front Camera - LDW)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_027 | 차선 이탈 발생 시 ADAS 연계 시각적 경고 | ASIL-D | ADAS HIL | LDW 이벤트 전송 |
| Req_032 | ADAS 연계 UI 반응 일관성 확보 | ASIL-B | Performance Test | 응답시간 편차 최소화 |
| Req_033 | ADAS 연계 시각적 경고 색상/표시 일관성 | ASIL-A | Integration Test | 색상, 점멸 규칙 |
| Req_037 | 다중 ADAS 이벤트 우선순위 기반 안내 | ASIL-D | Scenario Test | 위험도 우선순위 |

**총 4개 요구사항** | ASIL-D: 2개, ASIL-B: 1개, ASIL-A: 1개

#### ECU_ADAS_03 (Rear Camera - RVC)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_028 | 후진 시 ADAS 연계 앰비언트 조명 경고 | ASIL-C | ADAS HIL | 후방 장애물 감지 |
| Req_030 | 승하차 시 ADAS 연계 운전자 인지 UI | ASIL-B | ADAS Integration | 후측방 객체 접근 |

**총 2개 요구사항** | ASIL-C: 1개, ASIL-B: 1개

#### ECU_ADAS_05 (SCC - AEB)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_029 | 긴급 제동 발생 시 대시보드 시각적 경고 | ASIL-D | ADAS HIL | AEB 이벤트 전송 |
| Req_034 | ADAS 경고 UI 출력 실패 시 대체 안내 | ASIL-B | Fault Injection | 대체 시각적 수단 |
| Req_035 | ADAS 고위험 상황 시 비핵심 UI 제한 | ASIL-B | Safety Test | 주의 분산 최소화 |

**총 3개 요구사항** | ASIL-D: 1개, ASIL-B: 2개

---

### 4. DOM_04: Powertrain Domain

#### ECU_PT_02 (TCU - Transmission Control Unit)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_002 | 후진 안전경고 (D→R 변경 감지) | ASIL-C | HIL | 변속 상태 전송 |
| Req_006 | 후진중 도어개방 경고 (후진 상태 감지) | ASIL-C | HIL | R 기어 상태 |
| Req_015 | 후진 기어 진입 시 UX 제어 활성화 | ASIL-B | Integration Test | R 기어 + 5km/h 미만 |
| Req_016 | 후진 시 후방 조명 자동 제어 | ASIL-B | Integration Test | R → ON, D/N → OFF |
| Req_020 | 속도 증가 시 UX 자동 해제 | ASIL-B | Safety Test | 10km/h 이상 비활성화 |

**총 5개 요구사항** | ASIL-C: 2개, ASIL-B: 3개

#### ECU_PT_03 (Vehicle Speed Sensor)

| Req ID | 요구사항 요약 | ASIL | 검증방법 | 비고 |
|--------|--------------|------|----------|------|
| Req_001 | 스포츠모드 속도연동 엠비언트조명 | ASIL-B | HIL | 속도 신호 전송 |
| Req_015 | 후진 기어 진입 시 UX 제어 (속도 5km/h 미만) | ASIL-B | Integration Test | 저속 조건 확인 |
| Req_020 | 속도 증가 시 UX 자동 해제 (10km/h 이상) | ASIL-B | Safety Test | 속도 임계값 |

**총 3개 요구사항** | ASIL-B: 3개

---

### 5. DOM_05: Chassis Domain

해당 없음 (본 프로젝트에서 Chassis Domain ECU는 요구사항 직접 할당 없음, 간접 참조만)

---

### 6. 공통 요구사항 (Cross-Domain)

#### 시스템 전체 (All ECUs)

| Req ID | 요구사항 요약 | ASIL | 적용 ECU | 검증방법 |
|--------|--------------|------|----------|----------|
| Req_007 | 경고상태 자동복구기능 | ASIL-C | vECU, TCU, BCM | Recovery Test |
| Req_019 | 후진 경고음 제어 | ASIL-B | vECU, IVI | Integration Test |
| Req_022 | UX 제어 응답 시간 | ASIL-B | 모든 ECU | Performance Test |
| Req_023 | 오류 발생 시 안전 상태 전이 | ASIL-C | 모든 ECU | Fail-Safe Test |
| Req_024 | CAN 메시지 처리 신뢰성 (손실률 0.1% 이하) | ASIL-B | CGW, 모든 ECU | Network Test |
| Req_025 | UX 기능 확장 고려 설계 | QM | vECU, IVI | Architecture Review |
| Req_026 | 요구사항–테스트 추적성 확보 | QM | 전체 시스템 | Traceability Audit |
| Req_052 | 장시간 정차·졸음 방지 UX 알림 | QM | IVI, vECU | User Test |
| Req_054 | CAN 통신 안정성 (99.9% 성공률, 10ms 이하 지연) | ASIL-B | CGW, 모든 ECU | Network Test |
| Req_055 | 시스템 가용성 (재시작 3초, 부팅 5초) | ASIL-B | vECU | Boot Test |
| Req_056 | 페일세이프 동작 보장 | ASIL-D | 모든 ECU | Fail-Safe Test |

**총 11개 요구사항** | ASIL-D: 1개, ASIL-C: 2개, ASIL-B: 5개, QM: 3개

---

## 요구사항 통계 요약

### Domain별 요구사항 분포

| Domain | ECU 수 | 요구사항 수 | ASIL-D | ASIL-C | ASIL-B | ASIL-A | QM |
|--------|---------|-------------|--------|--------|--------|--------|-----|
| **Infotainment** | 4 | 25 | 4 | 3 | 9 | 6 | 3 |
| **Body** | 6 | 17 | 0 | 3 | 7 | 5 | 2 |
| **ADAS** | 6 | 9 | 3 | 1 | 4 | 1 | 0 |
| **Powertrain** | 3 | 8 | 0 | 2 | 6 | 0 | 0 |
| **Chassis** | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| **공통** | - | 11 | 1 | 2 | 5 | 0 | 3 |
| **합계** | 23 | 56* | 8 | 11 | 31 | 12 | 8 |

*요구사항 중복 할당으로 인해 총합은 56개보다 많을 수 있음 (양방향 추적성)

### ASIL 분포

| ASIL Level | 요구사항 수 | 비율 | 대표 예시 |
|------------|-------------|------|-----------|
| **ASIL-D** | 8 | 14% | AEB 경고, LDW 경고, 페일세이프 |
| **ASIL-C** | 11 | 20% | 후진 안전경고, OTA 복구, 경고 자동복구 |
| **ASIL-B** | 31 | 55% | 조명 제어, CAN 통신, vECU 핵심 기능 |
| **ASIL-A** | 12 | 21% | 승하차 UX, Cluster UI, 온도 연동 |
| **QM** | 8 | 14% | 사용자 편의, 확장성, A/B 테스트 |

---

## ISO 26262 & ASPICE 준수 사항

### ISO 26262 Part 8 - 추적성 (Traceability)

✅ **8-6 요구사항**: 시스템 요구사항과 시스템 아키텍처 간 양방향 추적성 확보
- 모든 요구사항은 최소 1개 이상의 ECU에 할당됨
- 모든 ECU는 할당된 요구사항 목록 명시

✅ **8-7 일관성 (Consistency)**:
- 동일 요구사항이 여러 ECU에 할당 시 일관성 검증 필요
  - 예: Req_001 (속도연동 조명) → vECU + Lighting ECU + Speed Sensor

✅ **8-9 검증 (Verification)**:
- 모든 요구사항은 검증방법 명시 (HIL, SIL, Integration, Fault Injection)

### ASPICE 3.1 준수

✅ **SYS.2 BP6** (System Requirements Analysis - Traceability):
- Stakeholder 요구사항 → System 요구사항 → ECU 할당 추적

✅ **SYS.3 BP6** (System Architectural Design - Traceability):
- System Architecture (Domain/ECU) → System Requirements 역추적

✅ **SYS.3 BP7** (Consistency):
- 요구사항과 아키텍처 간 일관성 검증
- Domain 간 인터페이스 (CAN 메시지) 일관성 확보

✅ **SYS.4 BP7** (Integration Test Traceability):
- 요구사항 → 통합 테스트 케이스 매핑 (별도 문서 참조)

---

## 다음 단계 산출물

1. **02_Concept_Design**: 입력부/제어부/출력부 구조 정의
2. **03_System_Architecture**: Domain/ECU 계층 구조 시각화
3. **03_01_Function_Definition**: 기능별 상세 정의
4. **03_02_Network_Flow**: CAN 메시지 흐름 정의
5. **03_03_Communication_Specification**: DBC 기반 신호 DB
6. **05~07_Test_Specification**: V-Model 우측 검증 단계

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0 | 2026-02-14 | AI Assistant | 초기 작성 - DBC 기반 ECU 추출 및 요구사항 할당 |

---

**승인**

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| 프로젝트 리더 | | | |
| 안전 관리자 (ISO 26262) | | | |
| 품질 관리자 (ASPICE) | | | |
