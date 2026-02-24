# 기능 정의서

> 특수목적 차량 V2V 통신 검증 플랫폼

| 가상노드 Simulator (입출력 기능) | 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|----------------------------------|------|--------|----------|------|------|
| | 입력 | 긴급 출동 버튼 | 경찰차 Panel — 긴급 출동 ON/OFF 버튼 | Switch/Indicator 이용 | ok |
| | | 위협 단계 버튼 | 선두차 Panel — Level 0~3 설정 버튼 | Switch/Indicator 이용 | ok |
| | | OTA 시작 버튼 | 서버 Panel — 재난 코드 입력 및 OTA 시작 버튼 | Switch/Indicator 이용 | ok |
| | 출력 | Ethernet 긴급 메시지 | Police_Node → 전 차량 긴급 상태 브로드캐스트 출력 | Ethernet Tx 표시 | ok |
| | | Ethernet 위협 명령 | Lead_Node → Follow_Node 전체 위협 단계 브로드캐스트 출력 | Ethernet Tx 표시 | ok |
| | | Ethernet OTA 전송 | Server_Node → Logistics_Node 펌웨어 블록 전송 출력 | Ethernet Tx 표시 | ok |
| | | 진행률 표시 | OTA 전송 진행률 0%→100% Indicator 출력 | TrackBar/Indicator | ok |
| | | 긴급 모드 전환 표시 | 물류차 재시작 후 "긴급차량 모드" 계기판 표시 | Switch/Indicator 이용 | ok |
| | ECU 동작 | Police_Node ECU | 긴급 버튼 → gEmergency 설정 → ETH_Emergency 브로드캐스트 전송 | CAPL Ethernet Tx 로직 | ok |
| | | Civ_Node ECU | ETH_Emergency 수신 → CAN_HMI_Warning 발송 → Cluster/Ambient 경보 활성화 | CAPL Ethernet Rx + CAN Tx | ok |
| | | Lead_Node ECU | 위협 단계 버튼 → gThreatLevel 설정 → ETH_ThreatCmd 브로드캐스트 전송 | CAPL Ethernet Tx 로직 | ok |
| | | Follow_Node ECU | ETH_ThreatCmd 수신 → Level 분기 → CAN_ThreatAct 발송 → 경계등/제동/소등 실행 | CAPL Ethernet Rx + CAN Tx | ok |
| | | Server_Node ECU | 재난 코드 입력 → ETH_OTA_Start 전송 → ETH_FW_Block 512byte 순차 전송 | CAPL Ethernet Tx 로직 | ok |
| | | Logistics_Node ECU | ETH_FW_Block 수신 조립 → CRC-32 검증 → 통과 시 gEmergencyMode = 1 + ECU 재시작 / 실패 시 이전 상태 복구 | CAPL Ethernet Rx + CAN Tx | ok |
| | | Cluster_ECU | CAN_HMI_Warning 수신 → 계기판 팝업 표시 / CAN_EmergencyMode 수신 → 긴급차량 모드 UI 표시 | CAPL CAN Rx 로직 | ok |
| | | Ambient_ECU | CAN_HMI_Warning 수신 → 주황 점멸 / CAN_EmergencyMode 수신 → 적청 교차 | CAPL CAN Rx 로직 | ok |
| | | Siren_ECU | CAN_EmergencyMode 수신 → 사이렌 ON | CAPL CAN Rx 로직 | ok |
| | | Lighting_ECU | CAN_ThreatAct 수신 → Level 1: 경계등 점멸 / Level 3: 전 조명 소등 | CAPL CAN Rx 로직 | ok |
| | | Brake_ECU | CAN_ThreatAct 수신 → Level 2: 비상 제동 시뮬레이션 | CAPL CAN Rx 로직 | ok |
