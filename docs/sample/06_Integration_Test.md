# 통합 테스트 (Integration Test)

> **V-Model 위치**: 우측 중단 — 소프트웨어 통합 테스트 단계 (SWE.5)
> **대응 문서**: `03_Function_definition.md` + `0301_SysFuncAnalysis.md` (SYS.3 설계 검증)
> **ISO 26262**: Part 6, Clause 10 — 소프트웨어 통합 테스트 / Part 4, Clause 9 — 시스템 통합 테스트
> **ASPICE**: SWE.5 (BP1: 통합 테스트 명세, BP2: 통합 테스트 수행, BP3: 결과 평가)
> **상위 연결**: `05_Unit_Test.md`(단위 테스트) → 본 문서 → `07_System_Test.md`(시스템 테스트)
> **추적성**: 각 테스트 ID는 `01_Requirements.md`의 Req. ID와 1:1 또는 N:1로 연결
> **검증 환경**: CANoe SIL — 복수 CAPL 노드 연동 시나리오 실행

---

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|----------|-----------|-----------|---------|--------------|--------|------|
| In_Test_01 | Req_001, Req_002 | Fault Injection 시 DTC B1234 생성 확인 | 과전류 신호 주입 후 DTC B1234 생성 및 BCM_FaultStatus(0x500) 전송 | | | |
| In_Test_02 | Req_002, Req_003 | DTC 생성 후 Cluster 경고등 활성화 확인 | DTC 발생 50ms 이내 Cluster RED 경고등 점등 | | | |
| In_Test_03 | Req_005, Req_006 | Gateway CAN-LS → CAN-HS 라우팅 확인 | BCM_FaultStatus(0x500) 5ms 이내 CAN-HS로 라우팅 | | | |
| In_Test_04 | Req_007 | DoIP Routing Activation 처리 확인 | OTA Server의 DoIP 0xE001 요청에 Gateway 응답 및 경로 활성화 | | | |
| In_Test_05 | Req_008 | UDS 세션 전환 확인 | Default → Extended → Programming 세션 순차 전환 및 PositiveResponse 수신 | | | |
| In_Test_06 | Req_009 | UDS 0x19 DTC 조회 확인 | Extended Session에서 0x19 0x02 요청 시 DTC B1234 포함 응답 | | | |
| In_Test_07 | Req_010, Req_003 | UDS 0x14 DTC 클리어 후 경고등 소등 확인 | 0x14 요청 후 DTC 클리어 및 Cluster 경고등 소등 | | | |
| In_Test_08 | Req_011, Req_012 | OTA Programming Session 진입 및 펌웨어 전송 확인 | 0x10 0x02 진입 → 0x34 요청 → 0x36 블록 전송 순서 정상 동작 | | | |
| In_Test_09 | Req_013 | OTA 전송 완료 및 CRC 검증 확인 | 0x37 전송 후 CRC-32 일치 시 PositiveResponse 및 BCM 재시작 | | | |
| In_Test_10 | Req_014 | OTA 실패 시 Rollback 확인 | CRC 불일치 주입 시 자동 Rollback 및 이전 펌웨어 유지 | | | |
| In_Test_11 | Req_015 | Bus Off 시 OTA 세션 안전 중단 확인 | OTA 진행 중 Bus Off 주입 시 세션 중단 및 DTC 저장 | | | |
| In_Test_12 | Req_004 | 연속 Fault Injection 10회 반복 확인 | 10회 연속 주입 시 매회 DTC B1234 생성 | | | |
