# 요구사항 명세서 (System Requirements Specification)

**Document ID**: SAMPLE-01-SRS
**ISO 26262 Reference**: Part 4, Cl.6 — 시스템 요구사항 명세
**ASPICE Reference**: SYS.2 (BP1: 요구사항 도출, BP2: 요구사항 분석, BP4: 추적성 확보)
**Version**: 1.4
**Date**: 2026-02-19
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 상단 — SYS.2 시스템 요구사항 | `07_System_Test.md` (SYS.5) | Concept Design | `03_Function_definition.md` |

---

| Req. ID | 요약 | 설명 | 비고 (Rationale) | ASIL | 추적성 (Traceability) |
|---------|------|------|-----------------|------|----------------------|
| Req_001 | BCM 고장 메시지 전송 | BCM은 LIN Slave(WindowMotorECU)로부터 수신한 Motor_Current가 50A를 초과할 경우 `BCM_FaultStatus` 메시지(0x500, CAN-LS)를 10ms 주기로 전송한다. | **근거**: 정상 구동 3A, Stall 시 30-50A (Motor Spec). LIN(ISO 17987) 기반 실제 차량 구조 반영. | ASIL-B | HARA-H01 → Req_016 → Scene.3 |
| Req_002 | DTC 생성 및 저장 | 과전류 조건 감지 시 DTC B1234를 생성하고 내부 메모리에 저장한다. | ISO 14229-1, **DTC Status Byte: 0x47 (Test Failed+Confirmed)** | ASIL-B | HARA-H01 → Scene.4 |
| Req_003 | Cluster 경고등 활성화 | DTC 발생 후 Cluster 경고등(RED)이 50ms 이내에 활성화된다. DTC 클리어 전까지 유지된다. | 운전자 인지 시간 고려 (HARA SG-01) | ASIL-B | SG-01 → Scene.5 |
| Req_004 | Fault Injection 지원 | CANoe CAPL을 통해 BCM_FaultStatus 신호를 소프트웨어적으로 주입할 수 있다. | **검증**: CAPL onSysVar 이벤트 활용 | QM | Scene.3 |
| Req_005 | CAN-LS → CAN-HS 라우팅 | Central Gateway는 CAN-LS(125kbps)에서 수신한 BCM_FaultStatus(0x500)를 CAN-HS(500kbps)로 라우팅한다. | Bandwidth 차이 고려 (버퍼링 필요) | ASIL-A | Scene.6 |
| Req_006 | 라우팅 지연 기준 | Gateway의 CAN-LS → CAN-HS 메시지 전달 지연은 최대 5ms 이내여야 한다. | Real-time 요구사항 | ASIL-A | Scene.6 |
| Req_007 | DoIP 경로 제공 | Gateway는 OTA Server와 BCM 사이의 DoIP(ISO 13400-2) 통신 경로를 제공한다. | ISO 13400-2 표준 준수 | QM | Scene.10 |
| Req_008 | UDS 세션 제어 | 시스템은 UDS 0x10 서비스를 지원한다. 세션 유형: Default(0x01), Extended(0x03), Programming(0x02). | ISO 14229-1 UDS 표준 | QM | Scene.7 |
| Req_009 | DTC 읽기 | 시스템은 UDS 0x19 서비스로 DTC B1234 정보를 읽을 수 있다. | 정비 편의성 (Serviceability) | QM | Scene.8 |
| Req_010 | DTC 클리어 | 시스템은 UDS 0x14 서비스로 DTC를 클리어할 수 있다. 클리어 후 Cluster 경고등이 소등된다. | **보안**: DTC 클리어 보안성 (UDS 0x27 Security Access 필수) | QM | Scene.9 |
| Req_011 | OTA 프로그래밍 세션 진입 | OTA Server는 UDS 0x10 0x02로 BCM Programming Session을 요청할 수 있다. | **순서**: UDS 0x27 Security Access → 0x10 0x02 순서 고정 | QM | Scene.11 |
| Req_012 | 펌웨어 다운로드 요청 | OTA Server는 UDS 0x34로 펌웨어 다운로드를 요청하고, 0x36으로 4KB 블록 단위로 전송한다. | 대용량 전송 효율성 고려 | QM | Scene.12~13 |
| Req_013 | 전송 완료 및 CRC 검증 | 전송 완료 후 UDS 0x37을 전송하고, CRC-32 검증 통과 시 BCM을 재시작한다. | 데이터 무결성 보장 (Integrity) | QM | Scene.14 |
| Req_014 | OTA 실패 시 Rollback | OTA 중 전원 차단, 통신 단절, CRC 오류 발생 시 이전 펌웨어로 자동 복구한다. | **구현**: Dual Bank 또는 Checksum 기반 복구 권장 | ASIL-B | SG-02 → Scene.15, 17 |
| Req_015 | Bus Off 시 안전 중단 | CAN Bus Off 감지 시 진행 중인 UDS/OTA 세션을 안전하게 중단하고 DTC를 저장한다. | **참조**: ISO 11898-1 Bus Off 복구 표준 | ASIL-B | SG-02 → Scene.16 |
| Req_016 | LIN Motor Current 수신 | BCM(LIN Master)은 WindowMotorECU(LIN Slave, ID: 0x21)로부터 Motor_Current 값을 10ms 주기로 수신한다. Motor_Current > 50A 조건이 감지되면 BCM은 DTC B1234를 생성한다. | **근거**: 실차 Body 도메인 구조 — Window Motor ECU가 LIN Slave로 전류값 직접 보고. LIN 2.2A (ISO 17987), 19.2 kbps. | ASIL-B | HARA-H01 → Req_001 → Scene.3 |
| Req_017 | LIN Door Module 상태 수신 | BCM(LIN Master)은 DoorModule FL/FR/RL/RR(LIN Slave, ID: 0x22~0x25)로부터 Door_Position 및 Lock_Status를 50ms 주기로 수신하고 BCM 내부 상태를 갱신한다. | **근거**: 도어 개폐 제어는 실차에서 LIN Bus를 통해 BCM이 관리하는 표준 구조. | QM | Scene.2b |
| Req_018 | LIN 통신 이상 감지 및 DTC 생성 | BCM(LIN Master)은 WindowMotorECU(LIN Slave, ID: 0x21) LIN 프레임이 50ms 이상 수신되지 않을 경우 통신 이상으로 판단하고 DTC U0100을 생성하여 내부 메모리에 저장한다. | **근거**: LIN 통신 단절 시 BCM이 Motor 전류 상태를 알 수 없어 안전 상태 전환 불가(HARA H-01). ISO 17987 LIN 통신 이상 감지 기준. DTC U0100: Lost Communication with LIN Bus (OBD-II 표준). | ASIL-B | HARA-H01, SG-01 → In_Test_15, Scene.2c |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-19 | 초기 생성 |
| 1.1 | 2026-02-19 | Req_018 추가 — LIN 통신 이상 감지 및 DTC U0100 생성 요구사항 (HARA H-01 완화 수단) |
| 1.2 | 2026-02-19 | ASIL 열 추가 — `중요도/긴급도` 대체. ISO 26262 기능 안전 등급 명시 (ASIL-B/A/QM) |
| 1.3 | 2026-02-19 | HARA 정합성 — SG-08→SG-02 변경 (H-09→H-03 재번호, sample 독립 프로젝트 일련번호 정렬) |
| 1.4 | 2026-02-19 | Req_018 추적성 완결 — Scene.2c 추가 (시스템 테스트 레벨 V&V 확보) |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-19 |
| Lead Engineer | — | — | 2026-02-19 |
