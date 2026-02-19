# 요구사항 명세서 (System Requirements Specification)

> **V-Model 위치**: 좌측 상단 — 시스템 요구사항 정의 단계
> **대응 문서**: `07_System_Test.md` (SYS.5 시스템 테스트로 검증)
> **ISO 26262**: Part 4, Clause 6 — 시스템 요구사항 명세
> **ASPICE**: SYS.2 (BP1: 요구사항 도출, BP2: 요구사항 분석, BP4: 추적성 확보)
> **HARA 연관**: Req_001~003(DTC/경고등)은 HARA에서 식별된 위험 H-01(Window Motor 과전류)에서 도출. Req_014(Rollback), Req_015(Bus Off 중단)은 안전목표 SG-01에 대응.
> **상위 연결**: Concept Design → 본 문서 → `03_Function_definition.md`(기능 분해)

---

| Req. ID | 요약 | 설명 | 비고 (Rationale) | 중요도/긴급도 | 추적성 (Traceability) |
|---------|------|------|------------------|--------------|-----------------------|
| Req_001 | BCM 고장 메시지 수신 | BCM은 Window Motor 과전류(50A 초과) 발생 시 `BCM_FaultStatus` 메시지(0x500, CAN-LS)를 10ms 주기로 전송한다. | **근거**: 정상 구동 3A, Stall 시 30-50A (Motor Spec) | 상/상 | HARA-H01 → Scene.3 |
| Req_002 | DTC 생성 및 저장 | 과전류 조건 감지 시 DTC B1234를 생성하고 내부 메모리에 저장한다. | ISO 14229-1, **DTC Status Byte: 0x47 (Test Failed+Confirmed)** | 상/상 | HARA-H01 → Scene.4 |
| Req_003 | Cluster 경고등 활성화 | DTC 발생 후 Cluster 경고등(RED)이 50ms 이내에 활성화된다. DTC 클리어 전까지 유지된다. | 운전자 인지 시간 고려 (HARA SG-01) | 상/상 | SG-01 → Scene.5 |
| Req_004 | Fault Injection 지원 | CANoe CAPL을 통해 BCM_FaultStatus 신호를 소프트웨어적으로 주입할 수 있다. | **검증**: CAPL onSysVar 이벤트 활용 | 상/중 | Scene.3 |
| Req_005 | CAN-LS → CAN-HS 라우팅 | Central Gateway는 CAN-LS(125kbps)에서 수신한 BCM_FaultStatus(0x500)를 CAN-HS(500kbps)로 라우팅한다. | Bandwidth 차이 고려 (버퍼링 필요) | 상/상 | Scene.6 |
| Req_006 | 라우팅 지연 기준 | Gateway의 CAN-LS → CAN-HS 메시지 전달 지연은 최대 5ms 이내여야 한다. | Real-time 요구사항 | 상/중 | Scene.6 |
| Req_007 | DoIP 경로 제공 | Gateway는 OTA Server와 BCM 사이의 DoIP(ISO 13400-2) 통신 경로를 제공한다. | ISO 13400-2 표준 준수 | 상/상 | Scene.10 |
| Req_008 | UDS 세션 제어 | 시스템은 UDS 0x10 서비스를 지원한다. 세션 유형: Default(0x01), Extended(0x03), Programming(0x02). | ISO 14229-1 UDS 표준 | 상/상 | Scene.7 |
| Req_009 | DTC 읽기 | 시스템은 UDS 0x19 서비스로 DTC B1234 정보를 읽을 수 있다. | 정비 편의성 (Serviceability) | 상/상 | Scene.8 |
| Req_010 | DTC 클리어 | 시스템은 UDS 0x14 서비스로 DTC를 클리어할 수 있다. 클리어 후 Cluster 경고등이 소등된다. | **보안**: DTC 클리어 보안성 (UDS 0x27 Security Access 필수) | 상/중 | Scene.9 |
| Req_011 | OTA 프로그래밍 세션 진입 | OTA Server는 UDS 0x10 0x02로 BCM Programming Session을 요청할 수 있다. | **순서**: UDS 0x27 Security Access → 0x10 0x02 순서 고정 | 상/상 | Scene.11 |
| Req_012 | 펌웨어 다운로드 요청 | OTA Server는 UDS 0x34로 펌웨어 다운로드를 요청하고, 0x36으로 4KB 블록 단위로 전송한다. | 대용량 전송 효율성 고려 | 상/상 | Scene.12~13 |
| Req_013 | 전송 완료 및 CRC 검증 | 전송 완료 후 UDS 0x37을 전송하고, CRC-32 검증 통과 시 BCM을 재시작한다. | 데이터 무결성 보장 (Integrity) | 상/상 | Scene.14 |
| Req_014 | OTA 실패 시 Rollback | OTA 중 전원 차단, 통신 단절, CRC 오류 발생 시 이전 펌웨어로 자동 복구한다. | **구현**: Dual Bank 또는 Checksum 기반 복구 권장 | 상/상 | SG-08 → Scene.15, 17 |
| Req_015 | Bus Off 시 안전 중단 | CAN Bus Off 감지 시 진행 중인 UDS/OTA 세션을 안전하게 중단하고 DTC를 저장한다. | **참조**: ISO 11898-1 Bus Off 복구 표준 | 상/중 | SG-08 → Scene.16 |
