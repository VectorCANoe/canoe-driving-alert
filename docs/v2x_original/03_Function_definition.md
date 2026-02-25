# 기능 정의서

> 특수목적 차량 V2V 통신 검증 플랫폼 — 노드별 기능 정의

| 가상노드 | 분류 | 기능명 | 기능 설명 | 비고 | 검증 |
|----------|------|--------|-----------|------|------|
| Police_Node | 송신 | 긴급 출동 트리거 | Panel 버튼 클릭 시 gEmergency = 1 설정 후 Ethernet으로 긴급 메시지(차량 ID + 방향) 브로드캐스트 | 시나리오 1 | Pass |
| Civ_Node A/B/C | 수신 | 긴급 경고 HMI | Ethernet 긴급 메시지 수신 즉시 CAN → Cluster 팝업 + Ambient 주황 점멸 출력 | 시나리오 1 | Pass |
| Civ_Node A/B/C | 해제 | 경고 자동 소거 | 경찰차 해제 메시지 수신 시 Cluster/Ambient 즉시 정상 복귀 | 시나리오 1 | Pass |
| Lead_Node | 송신 | 위협 단계 명령 | Panel에서 gThreatLevel(1/2/3) 설정 후 Ethernet으로 전 후행차에 동시 전송 | 시나리오 2 | Pass |
| Follow_Node 1/2/3 | 수신 | 단계별 즉시 실행 | Level 1 → 경계등 점멸 / Level 2 → 비상 제동 시뮬 / Level 3 → 전 조명 소등 | 시나리오 2 | Pass |
| Follow_Node 1/2/3 | 해제 | 위협 해제 복귀 | 선두차 해제 명령 수신 시 전 조명 즉시 정상 복귀 | 시나리오 2 | Pass |
| Server_Node | 송신 | OTA 명령 발송 | Panel 재난 코드 입력 시 Ethernet으로 물류차에 OTA 시작 명령 + 펌웨어 블록 순차 전송 | 시나리오 3 | Pass |
| Logistics_Node | 수신 | 펌웨어 수신·검증 | 블록 수신 후 CRC 검증 수행. 통과 시 재시작 → 긴급차량 모드 진입 | 시나리오 3 | Pass |
| Logistics_Node | 안전 | OTA Fail-Safe | CRC 불일치 발생 시 이전 상태 자동 복구 + 화면 "복구 완료" 표시 | 시나리오 3 | Pass |
