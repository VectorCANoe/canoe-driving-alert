# 통합/시스템 테스트

> 특수목적 차량 V2V 통신 검증 플랫폼 — 06 통합 테스트 + 07 시스템 테스트

---

## 06. 통합 테스트 (Integration Test)

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 |
|-----------|-------------|-------------|-----------|------------------|--------|
| In_Test_01 | Req_V01~V03 | 공통 인프라 — 전 노드 연결 및 통신 채널 확인 | Police/Civ/Lead/Follow/Server/Logistics 전 노드 Ethernet 연결 정상, 차량 내부 CAN 채널 응답 확인 | Pass | 팀 |
| In_Test_02 | Req_E01~E03 | 경찰차 긴급 메시지 → 일반차 HMI 연동 | gEmergency = 1 → ETH_Emergency(EmergencyFlag=1) 전송 → Civ_Node A/B/C 동시에 CAN_HMI_Warning → Cluster 팝업 + Ambient 주황 점멸 | Pass | 팀 |
| In_Test_03 | Req_E04 | 긴급 해제 → 전 차량 경고 자동 소거 | gEmergency = 0 → ETH_Emergency(EmergencyFlag=0) 전송 → Civ_Node 3대 경고 즉시 소거 확인 | Pass | 팀 |
| In_Test_04 | Req_M01~M03 | 선두차 위협 단계 → 후행차 전체 동시 실행 | ETH_ThreatCmd(ThreatLevel=1/2/3) → Follow_Node 1/2/3 동시 CAN_ThreatAct → 경계등/비상제동/전소등. 전달 지연 ≤ 50ms | Pass | 팀 |
| In_Test_05 | Req_M04 | 위협 해제 → 후행차 전체 정상 복귀 | ETH_ThreatCmd(ThreatLevel=0) → Follow_Node 1/2/3 전체 조명 및 제동 즉시 정상 복귀 확인 | Pass | 팀 |
| In_Test_06 | Req_P01~P03 | OTA 펌웨어 전송 → 검증 → 임무 전환 E2E | ETH_OTA_Start → ETH_FW_Block 순차 전송 → CRC-32 통과 → gEmergencyMode=1 → CAN_EmergencyMode → 재시작 → 사이렌/앰비언트/계기판 전환 | Pass | 팀 |
| In_Test_07 | Req_P04 | OTA Fail-Safe — CRC 오류 복구 | 전체 블록 수신 후 의도적 데이터 변조(CRC 불일치) 주입 → 이전 물류차 상태 자동 복구 + "OTA 실패 — 이전 상태로 복구 완료" 표시 확인 | Pass | 팀 |

---

## 07. 시스템 테스트 (System Test / E2E 시나리오)

| Scene. ID | 설명 | Pass / Fail |
|-----------|------|-------------|
| Scene. E1 | 경찰차 Panel "긴급 출동" 버튼 클릭 → gEmergency = 1, ETH_Emergency 브로드캐스트 전송 확인 | Pass |
| Scene. E2 | Civ_Node A/B/C 계기판에 동시에 "긴급 차량 접근 중, 우측 양보" 팝업 + Ambient 주황 점멸 확인 | Pass |
| Scene. E3 | "긴급 출동" 버튼 재클릭 → gEmergency = 0, Civ_Node 3대 경고 자동 소거 확인 | Pass |
| Scene. M1 | 선두차 Panel에서 위협 Level 1 명령 전송 → Follow_Node 1/2/3 경계등 동시 점멸 확인 | Pass |
| Scene. M2 | 위협 Level 2 명령 전송 → Follow_Node 1/2/3 비상 제동 시뮬레이션 동시 실행 확인 | Pass |
| Scene. M3 | 위협 Level 3 명령 전송 → Follow_Node 1/2/3 전 조명 즉시 소등(스텔스 모드) 동기화 확인 | Pass |
| Scene. M4 | 선두차 위협 해제(Level 0) 명령 → Follow_Node 전체 정상 상태 복귀 확인 | Pass |
| Scene. P1 | Server Panel 재난 코드 입력 후 OTA 시작 → 물류차 화면 "긴급 업데이트 수신 중" + 진행률 0%→100% 표시 확인 | Pass |
| Scene. P2 | 전체 블록 수신 완료 → CRC-32 검증 통과 → 재시작 → 사이렌 ON + Ambient 적청 교차 + 계기판 "긴급차량 모드" 확인 | Pass |
| Scene. P3 | 전송 완료 후 데이터 변조(CRC 불일치) 주입 → 이전 물류차 상태 자동 복구 + "OTA 실패 — 이전 상태로 복구 완료" 표시 확인 | Pass |
