# 가상노드 Simulator (입출력 기능) — Function Definition

> **V-Model 위치**: 좌측 중단 — 시스템 아키텍처 설계 단계
> **대응 문서**: `06_Integration_Test.md` (SWE.5 통합 테스트로 검증)
> **ISO 26262**: Part 4, Clause 7 — 시스템 설계 (기능 분해 및 ECU 할당)
> **ASPICE**: SYS.3 (BP1: 시스템 아키텍처 설계, BP2: 인터페이스 정의, BP3: 기능 할당)
> **상위 연결**: `01_Requirements.md` → 본 문서 → `0301_SysFuncAnalysis.md`(기능 상세)
> **하위 연결**: 각 ECU 동작 항목은 `05_Unit_Test.md`의 단위 테스트 항목과 1:1 대응

---

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|------|--------|---------|------|------|
| 입력 | Fault Injection 버튼 | BCM 과전류 고장 상태를 수동으로 주입 (0: 정상, 1: 고장) | Switch/Indicator 이용하여 ON/OFF 표현 | In_Test_01, In_Test_12, Scene.3 |
| | OTA 트리거 버튼 | OTA 업데이트 시작 신호 주입 | Switch/Indicator 이용하여 ON/OFF 표현 | In_Test_08, Scene.11 |
| | UDS 서비스 선택 | 0x10/0x14/0x19 서비스 수동 선택 | Switch/Indicator 이용하여 서비스 선택 | In_Test_05, In_Test_06, In_Test_07, Scene.7~9 |
| | Bus Load 조절 | CAN 버스 부하 수준 조절 (0~90%) | TrackBar 사용하여 값 조절 | In_Test_03 |
| 출력 | DTC 상태 | DTC B1234 생성/클리어 상태 표시 | Switch/Indicator 이용하여 ON/OFF 출력 | In_Test_01, In_Test_07, Scene.4, Scene.9 |
| | Cluster 경고등 | 경고등 활성화 여부 및 색상 표시 | Switch/Indicator 이용하여 RED/OFF 출력 | In_Test_02, In_Test_07, Scene.5, Scene.9 |
| | UDS 응답 코드 | PositiveResponse / NegativeResponse 표시 | Switch/Indicator 이용하여 응답 코드 출력 | In_Test_05~09, Scene.7~14 |
| | OTA 진행률 | 펌웨어 전송 블록 진행 상태 표시 | Switch/Indicator 이용하여 진행률 출력 | In_Test_08, In_Test_09, Scene.12~14 |
| | Rollback 상태 | OTA 실패 시 Rollback 완료 여부 표시 | Switch/Indicator 이용하여 ON/OFF 출력 | In_Test_10, Scene.15~17 |
| ECU 동작 | BCM ECU | Window Motor 과전류 감지 → DTC B1234 생성 → BCM_FaultStatus(0x500) 전송 | CAPL 고장 감지 및 DTC 로직 추가 | In_Test_01, In_Test_02, Scene.3~5 |
| | Gateway ECU | CAN-LS(0x500) → CAN-HS 라우팅, DoIP Routing Activation 처리 | CAPL 메시지 복사 및 DoIP 포워딩 로직 추가 | In_Test_03, In_Test_04, Scene.6, Scene.10 |
| | Tester ECU | UDS 0x10/0x19/0x14 서비스 요청 및 응답 처리 | CAPL UDS 세션 및 DTC 조회 로직 추가 | In_Test_05, In_Test_06, In_Test_07, Scene.7~9 |
| | OTA Server ECU | UDS 0x34/0x36/0x37 시퀀스로 펌웨어 전송, CRC-32 검증 | CAPL OTA 전송 및 검증 로직 추가 | In_Test_08, In_Test_09, In_Test_10, Scene.11~17 |
| | Cluster ECU | BCM_FaultStatus 수신 → 경고등 활성화/소등 제어 | CAPL 경고등 제어 로직 추가 | In_Test_02, In_Test_07, Scene.5, Scene.9 |
