# 단위 테스트

> 특수목적 차량 V2V 통신 검증 플랫폼 — 노드별 단위 테스트

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|------|------|--------|-----------|-----------|--------|------|
| Police_Node | 송신 | 긴급 브로드캐스트 | Panel "긴급 출동" 버튼 클릭 시 gEmergency = 1 설정 + ETH_Emergency 메시지 전송 확인 | Pass | 팀 | 26.02.24 |
| Civ_Node A | 수신 | 긴급 HMI 경고 | ETH_Emergency 수신 즉시 CAN → Cluster 팝업 "긴급 차량 접근 중" + Ambient 주황 점멸 출력 확인 | Pass | 팀 | 26.02.24 |
| Civ_Node A | 해제 | 경고 자동 소거 | ETH_Emergency_Clear 수신 시 Cluster/Ambient 즉시 정상 복귀 확인 | Pass | 팀 | 26.02.24 |
| Lead_Node | 송신 | 위협 명령 전송 | Panel Level 1/2/3 설정 시 ETH_ThreatCmd 50ms 이내 전송 확인 | Pass | 팀 | 26.02.24 |
| Follow_Node 1 | 수신 Level 1 | 경계등 점멸 | ETH_ThreatCmd(Level=1) 수신 즉시 CAN → 경계등 점멸 출력 확인 | Pass | 팀 | 26.02.24 |
| Follow_Node 1 | 수신 Level 2 | 비상 제동 시뮬 | ETH_ThreatCmd(Level=2) 수신 즉시 CAN → 비상 제동 시뮬레이션 출력 확인 | Pass | 팀 | 26.02.24 |
| Follow_Node 1 | 수신 Level 3 | 전 조명 소등 | ETH_ThreatCmd(Level=3) 수신 즉시 CAN → 전 조명 소등 확인 | Pass | 팀 | 26.02.24 |
| Server_Node | 송신 | OTA 블록 전송 | 재난 코드 입력 후 512byte 블록 순차 전송 및 진행률 표시 확인 | Pass | 팀 | 26.02.24 |
| Logistics_Node | 검증 | CRC 통과 | 정상 펌웨어 수신 후 CRC-32 검증 통과 → gEmergencyMode = 1 전환 확인 | Pass | 팀 | 26.02.24 |
| Logistics_Node | 안전 | CRC 실패 복구 | 의도적 데이터 변조 주입 시 CRC 불일치 감지 → 이전 상태 자동 복구 + "복구 완료" 표시 확인 | Pass | 팀 | 26.02.24 |
