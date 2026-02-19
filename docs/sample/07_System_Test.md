# 시스템 테스트 (System Test)

> **V-Model 위치**: 우측 상단 — 시스템 적격성 테스트 단계 (SYS.5)
> **대응 문서**: `01_Requirements.md` (SYS.2 요구사항 전체 검증)
> **ISO 26262**: Part 4, Clause 10 — 시스템 적격성 테스트
> **ASPICE**: SYS.5 (BP1: 시스템 테스트 명세, BP2: 시스템 테스트 수행, BP3: 결과 평가)
> **상위 연결**: `06_Integration_Test.md`(통합 테스트) → 본 문서 → 릴리즈/검수
> **HARA 연관**: Scene.15(CRC 불일치 Rollback), Scene.16(Bus Off 중단)은 HARA SG-01, SG-08 안전목표 달성 여부를 최종 검증
> **검증 환경**: CANoe SIL — 전체 E2E 시나리오 (Fault → Gateway → UDS → OTA) 순차 실행

---

| Scene. ID | 설명 | Pass/Fail | 담당자 | 일자 |
|-----------|------|----------|--------|------|
| Scene. 1 | CANoe 프로젝트 실행 후 모든 ECU 노드(BCM, Gateway, Tester, OTA Server, Cluster) 초기화 확인 | | | |
| Scene. 2 | 초기 상태에서 DTC 없음, 경고등 소등, 세션 Default 상태 확인 | | | |
| Scene. 3 | Fault Injection 버튼 ON → BCM_FaultStatus(0x500) 전송 확인 | | | |
| Scene. 4 | BCM_FaultStatus 전송 후 DTC B1234 생성 및 저장 확인 | | | |
| Scene. 5 | DTC 생성 후 50ms 이내 Cluster RED 경고등 활성화 확인 | | | |
| Scene. 6 | Gateway가 CAN-LS(0x500)를 CAN-HS로 5ms 이내 라우팅하는 모습 확인 | | | |
| Scene. 7 | Tester가 UDS 0x10 0x03으로 Extended Session 전환 및 PositiveResponse(0x50 0x03) 수신 확인 | | | |
| Scene. 8 | Extended Session에서 UDS 0x19 0x02 요청 → DTC B1234 포함 응답 확인 | | | |
| Scene. 9 | UDS 0x14 0xFF 0xFF 0xFF 요청 → DTC 클리어 및 Cluster 경고등 소등 확인 | | | |
| Scene. 10 | DoIP Routing Activation(0xE001) → Gateway 경로 활성화 확인 | | | |
| Scene. 11 | UDS 0x10 0x02 Programming Session 진입 → PositiveResponse(0x50 0x02) 확인 | | | |
| Scene. 12 | UDS 0x34 다운로드 요청 → maxBlockLength 포함 응답(0x74) 확인 | | | |
| Scene. 13 | UDS 0x36으로 4KB 블록 순차 전송 → 각 블록 PositiveResponse(0x76) 확인 | | | |
| Scene. 14 | UDS 0x37 전송 완료 → CRC-32 검증 통과 → PositiveResponse(0x77) 및 BCM 재시작 확인 | | | |
| Scene. 15 | OTA 중 CRC 불일치 주입 → NegativeResponse(0x7F 0x37 0x70) 및 Rollback 확인 | | | |
| Scene. 16 | OTA 중 Bus Off 주입 → 세션 안전 중단 및 DTC 저장 확인 | | | |
| Scene. 17 | Rollback 완료 후 이전 펌웨어 버전으로 BCM 정상 동작 확인 | | | |
| Scene. 18 | Fault Injection 재실행 → 전체 시나리오(Fault→Gateway→UDS→OTA) 2회 연속 정상 동작 확인 | | | |
