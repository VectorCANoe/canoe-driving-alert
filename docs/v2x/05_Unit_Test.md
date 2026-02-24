# 단위 테스트

> 특수목적 차량 V2V 통신 검증 플랫폼 — 노드별 단위 테스트

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail |
|------|------|--------|-----------|-----------|
| Police_Node | 송신 | 긴급 브로드캐스트 | Panel "긴급 출동" 버튼 클릭 시 gEmergency = 1 설정 + ETH_Emergency(EmergencyFlag=1, VehicleID=0x10) 전송 확인 | Pass |
| Police_Node | 송신 | 긴급 해제 | Panel 해제 버튼 클릭 시 gEmergency = 0 설정 + ETH_Emergency(EmergencyFlag=0) 전송 확인 | Pass |
| Civ_Node A | 수신 | 긴급 HMI 경보 | ETH_Emergency(EmergencyFlag=1) 수신 즉시 CAN_HMI_Warning(0x300, EmergencyAlert=1) 발송 → Cluster 팝업 + Ambient 주황 점멸 확인 | Pass |
| Civ_Node A | 수신 | 경보 자동 소거 | ETH_Emergency(EmergencyFlag=0) 수신 시 CAN_HMI_Warning(EmergencyAlert=0) 발송 → Cluster/Ambient 즉시 정상 복귀 확인 | Pass |
| Lead_Node | 송신 | 위협 명령 전송 | Panel Level 1/2/3 설정 시 ETH_ThreatCmd(ThreatLevel=1/2/3) 50ms 이내 전송 확인 | Pass |
| Lead_Node | 송신 | 위협 해제 | Panel 해제 클릭 시 ETH_ThreatCmd(ThreatLevel=0) 전송 확인 | Pass |
| Follow_Node 1 | 수신 Level 1 | 경계등 점멸 | ETH_ThreatCmd(ThreatLevel=1) 수신 즉시 CAN_ThreatAct(0x400, ThreatLevel=1) 발송 → 경계등 점멸 출력 확인 | Pass |
| Follow_Node 1 | 수신 Level 2 | 비상 제동 시뮬 | ETH_ThreatCmd(ThreatLevel=2) 수신 즉시 CAN_ThreatAct(ThreatLevel=2) 발송 → 비상 제동 시뮬레이션 출력 확인 | Pass |
| Follow_Node 1 | 수신 Level 3 | 전 조명 소등 | ETH_ThreatCmd(ThreatLevel=3) 수신 즉시 CAN_ThreatAct(ThreatLevel=3) 발송 → 전 조명 소등 확인 | Pass |
| Server_Node | 송신 | OTA 블록 전송 | 재난 코드 입력 후 ETH_OTA_Start(0x01) 전송 → ETH_FW_Block(0x02) 512byte 블록 순차 전송 및 진행률 표시 확인 | Pass |
| Logistics_Node | 검증 | CRC 통과 | 정상 펌웨어 전체 블록 수신 후 CRC-32 검증 통과 → gEmergencyMode = 1 → CAN_EmergencyMode(0x500, EmergencyMode=1) 전송 확인 | Pass |
| Logistics_Node | 안전 | CRC 실패 복구 | 의도적 데이터 변조 주입 시 CRC-32 불일치 감지 → 이전 상태 자동 복구 + "OTA 실패 — 이전 상태로 복구 완료" 표시 확인 | Pass |
