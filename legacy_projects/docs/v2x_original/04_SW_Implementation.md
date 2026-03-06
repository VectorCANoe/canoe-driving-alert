# SW 구현서

> 특수목적 차량 V2V 통신 검증 플랫폼 — CANoe CAPL 기반 구현

| 구분 | 언어 | 모듈명 | 상태 | 주요 구현 알고리즘 핵심 요약 |
|------|------|--------|------|------------------------------|
| CAPL | CAPL | Police_Node | 완료 | Panel 버튼 → gEmergency 플래그 설정 → UDP 브로드캐스트 전송. 해제 버튼 → Clear 메시지 전송 |
| CAPL | CAPL | Civ_Node (A/B/C) | 완료 | Ethernet 수신 핸들러 → 긴급 메시지 파싱 → CAN HMI 명령 즉시 발송 (Cluster 팝업 + Ambient 주황 점멸) |
| CAPL | CAPL | Lead_Node | 완료 | Panel 위협 단계 입력 → gThreatLevel 설정 → Ethernet 동기 브로드캐스트. 전달 지연 ≤ 50ms 보장 |
| CAPL | CAPL | Follow_Node (1/2/3) | 완료 | ETH 명령 수신 → Level 분기(1: 경계등 / 2: 비상 제동 시뮬 / 3: 전 조명 소등) 즉시 CAN 출력 |
| CAPL | CAPL | Server_Node | 완료 | 재난 코드 입력 → OTA 시작 명령 → 512byte 블록 단위 Ethernet 순차 전송 → 전송 완료 신호 |
| CAPL | CAPL | Logistics_Node | 완료 | 블록 수신 조립 → CRC-32 검증 → 통과 시 gEmergencyMode = 1 + ECU 재시작 시뮬 / 실패 시 이전 상태 복구 + "복구 완료" 표시 |
