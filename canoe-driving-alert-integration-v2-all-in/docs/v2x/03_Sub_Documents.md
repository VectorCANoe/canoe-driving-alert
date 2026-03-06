# 시스템 동작 분석 / 네트워크 흐름 / 통신 스펙 / 변수 사양서

> 특수목적 차량 V2V 통신 검증 플랫폼 — 0301~0304 통합 문서

---

## 0301. 시스템 기능 분석 (SysFuncAnalysis)

| 노드 | 기능 상세 | 비고 |
|------|----------|------|
| **Ethernet V2V Layer** | | |
| Police_Node | 긴급 버튼 입력 → gEmergency 플래그 설정 → ETH_Emergency 브로드캐스트. 해제 시 gEmergency = 0 재전송 | 시나리오 1 송신 |
| Civ_Node (A/B/C) | ETH_Emergency 수신 → CAN_HMI_Warning(0x300) 발송 → Cluster/Ambient 경보 활성화. gEmergency = 0 수신 시 경보 해제 | 시나리오 1 수신 |
| Lead_Node | 위협 단계(1/2/3) 입력 → gThreatLevel 설정 → ETH_ThreatCmd 브로드캐스트. 해제 시 gThreatLevel = 0 재전송 | 시나리오 2 송신 |
| Follow_Node (1/2/3) | ETH_ThreatCmd 수신 → ThreatLevel 분기 → CAN_ThreatAct(0x400) 발송 → 경계등/비상제동/전소등 즉시 실행 | 시나리오 2 수신 |
| Server_Node | 재난 코드 입력 → ETH_OTA_Start 전송 → ETH_FW_Block 512byte 단위 순차 전송 | 시나리오 3 송신 |
| Logistics_Node | ETH_FW_Block 수신 조립 → CRC-32 검증 → 통과: gEmergencyMode=1 + CAN_EmergencyMode(0x500) 발송 + 재시작 / 실패: 이전 상태 복구 | 시나리오 3 수신 |
| **CAN Internal Layer** | | |
| Cluster_ECU | CAN_HMI_Warning(0x300) 수신 → "긴급 차량 접근 중, 우측 양보" 팝업 표시 | Civ_Node 내부 |
| Ambient_ECU | CAN_HMI_Warning(0x300) 수신 → 주황 점멸 / CAN_EmergencyMode(0x500) 수신 → 적청 교차 | 각 차량 내부 |
| Lighting_ECU | CAN_ThreatAct(0x400) ThreatLevel=1 → 경계등 점멸 / ThreatLevel=3 → 전 조명 소등 | Follow_Node 내부 |
| Brake_ECU | CAN_ThreatAct(0x400) ThreatLevel=2 → 비상 제동 시뮬레이션 | Follow_Node 내부 |
| Siren_ECU | CAN_EmergencyMode(0x500) EmergencyMode=1 → 사이렌 ON | Logistics_Node 내부 |

---

## 0302. 네트워크 흐름 정의 (NWflowDef)

### Ethernet V2V 통신 (차량 간)

| Channel | Port | 메시지명 | Byte No. | Function | 필드명 | Police_Node | Civ_Node | Lead_Node | Follow_Node | Server_Node | Logistics_Node |
|---------|------|---------|---------|---------|------|:-----------:|:--------:|:---------:|:-----------:|:-----------:|:--------------:|
| Ethernet | 5000 | ETH_Emergency | 0 | Emergency Flag | EmergencyFlag | Tx | Rx | | | | |
| | | | 1 | Vehicle ID | VehicleID | Tx | Rx | | | | |
| | | | 2 | Direction | Direction | Tx | Rx | | | | |
| | | | 3 | Reserved | Reserved | Tx | | | | | |
| Ethernet | 5001 | ETH_ThreatCmd | 0 | Threat Level | ThreatLevel | | | Tx | Rx | | |
| | | | 1 | Reserved | Reserved | | | Tx | | | |
| Ethernet | 5002 | ETH_OTA_Start | 0 | Command Type | CommandType | | | | | Tx | Rx |
| | | | 1 | Disaster Code | DisasterCode | | | | | Tx | Rx |
| | | | 2 | Total Blocks (H) | TotalBlocks_H | | | | | Tx | Rx |
| | | | 3 | Total Blocks (L) | TotalBlocks_L | | | | | Tx | Rx |
| Ethernet | 5002 | ETH_FW_Block | 0 | Command Type | CommandType | | | | | Tx | Rx |
| | | | 1 | Block Index (H) | BlockIndex_H | | | | | Tx | Rx |
| | | | 2 | Block Index (L) | BlockIndex_L | | | | | Tx | Rx |
| | | | 3 | Reserved | Reserved | | | | | Tx | |
| | | | 4~515 | Firmware Data | FirmwareData | | | | | Tx | Rx |

### CAN 내부 통신 — Civ_Node 내부 CAN

| Channel | ID | 메시지명 | Byte No. | Bit No. | Function | 신호명 | Civ_ETH_Handler | Cluster_ECU | Ambient_ECU |
|---------|-----|---------|---------|--------|---------|------|:--------------:|:-----------:|:-----------:|
| CAN-HS | 0x300 | CAN_HMI_Warning | 0 | 0 | Emergency Alert ON/OFF | EmergencyAlert | Tx | Rx | Rx |

### CAN 내부 통신 — Follow_Node 내부 CAN

| Channel | ID | 메시지명 | Byte No. | Bit No. | Function | 신호명 | Follow_ETH_Handler | Lighting_ECU | Brake_ECU |
|---------|-----|---------|---------|--------|---------|------|:------------------:|:------------:|:---------:|
| CAN-HS | 0x400 | CAN_ThreatAct | 0 | 0~1 | Threat Level Command | ThreatLevel | Tx | Rx | Rx |

### CAN 내부 통신 — Logistics_Node 내부 CAN

| Channel | ID | 메시지명 | Byte No. | Bit No. | Function | 신호명 | Logistics_ETH_Handler | Siren_ECU | Ambient_ECU | Cluster_ECU |
|---------|-----|---------|---------|--------|---------|------|:---------------------:|:---------:|:-----------:|:-----------:|
| CAN-HS | 0x500 | CAN_EmergencyMode | 0 | 0 | Emergency Mode Activate | EmergencyMode | Tx | Rx | Rx | Rx |

---

## 0303. 통신 스펙 (Communication Specification)

### Ethernet 메시지 (V2V — UDP Payload 구조)

| 메시지 | Identifier | Payload (bytes) | Signal | Byte Position | Data 설명 | Data 범위 | Data 사용 |
|--------|-----------|----------------|--------|--------------|---------|---------|---------|
| ETH_Emergency | UDP Port 5000 | 4 | EmergencyFlag | Byte 0 | 긴급 출동 상태 | 0~1 | 0=해제, 1=긴급 출동. Civ_Node 전체로 브로드캐스트 |
| | | | VehicleID | Byte 1 | 송신 차량 식별자 | 0x10 | 경찰차(Police_Node) 고정값 |
| | | | Direction | Byte 2 | 차량 진행 방향 | 0~3 | 0=East / 1=West / 2=North / 3=South |
| | | | Reserved | Byte 3 | 예약 | 0x00 | 미사용 |
| ETH_ThreatCmd | UDP Port 5001 | 2 | ThreatLevel | Byte 0 | 위협 단계 | 0~3 | 0=해제(정상복귀) / 1=경계 / 2=회피기동 / 3=스텔스. Follow_Node 전체로 브로드캐스트 |
| | | | Reserved | Byte 1 | 예약 | 0x00 | 미사용 |
| ETH_OTA_Start | UDP Port 5002 | 4 | CommandType | Byte 0 | 명령 유형 식별자 | 0x01 | OTA 시작 명령 고정값 |
| | | | DisasterCode | Byte 1 | 재난 분류 코드 | 0~255 | 국가 재난 코드 입력값 |
| | | | TotalBlocks_H | Byte 2 | 총 블록 수 상위 바이트 | 0~255 | 전체 전송 블록 수 (Big-Endian 상위) |
| | | | TotalBlocks_L | Byte 3 | 총 블록 수 하위 바이트 | 0~255 | 전체 전송 블록 수 (Big-Endian 하위) |
| ETH_FW_Block | UDP Port 5002 | 516 | CommandType | Byte 0 | 명령 유형 식별자 | 0x02 | 펌웨어 블록 전송 고정값 |
| | | | BlockIndex_H | Byte 1 | 블록 인덱스 상위 바이트 | 0~255 | 현재 블록 번호 (Big-Endian 상위) |
| | | | BlockIndex_L | Byte 2 | 블록 인덱스 하위 바이트 | 0~255 | 현재 블록 번호 (Big-Endian 하위) |
| | | | Reserved | Byte 3 | 예약 | 0x00 | 미사용 |
| | | | FirmwareData | Byte 4~515 | 펌웨어 페이로드 | - | 512 bytes 펌웨어 데이터 블록 |

### CAN 메시지 (차량 내부)

| 메시지 | Identifier | DLC | Signal | Signal Bit Position | Data 설명 | Data 범위 | Data 사용 |
|--------|-----------|-----|--------|--------------------|---------|---------|---------||
| CAN_HMI_Warning | 0x300 | 1 | EmergencyAlert | 0 | 긴급 경보 ON/OFF | 0~1 | 0=경보 해제, 1=경보 활성. Cluster_ECU·Ambient_ECU로 전송 |
| CAN_ThreatAct | 0x400 | 1 | ThreatLevel | 0~1 | 현재 위협 단계 | 0~3 | 0=정상복귀 / 1=경계등 점멸 / 2=비상제동 시뮬 / 3=전 조명 소등. Lighting_ECU·Brake_ECU로 전송 |
| CAN_EmergencyMode | 0x500 | 1 | EmergencyMode | 0 | 긴급차량 모드 전환 | 0~1 | 0=물류 모드, 1=긴급차량 모드 활성. Siren_ECU·Ambient_ECU·Cluster_ECU로 전송 |

---

## 0304. 시스템 변수 명세서 (System Variables)

| ID | Namespace | Name | Data type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|---------------|-------------|
| 1 | Emergency | gEmergency | uint32 | 0 | 1 | 0 | 경찰차 긴급 상태 (0=정상, 1=긴급 출동) |
| 2 | Emergency | gVehicleID | uint32 | 0 | 255 | 16 | 송신 차량 ID (0x10=Police_Node 고정) |
| 3 | Emergency | gDirection | uint32 | 0 | 3 | 0 | 차량 진행 방향 (0=East / 1=West / 2=North / 3=South) |
| 4 | Military | gThreatLevel | uint32 | 0 | 3 | 0 | 위협 단계 (0=정상 / 1=경계 / 2=회피기동 / 3=스텔스) |
| 5 | OTA | gOTA_Progress | Double | 0 | 100 | 0 | 펌웨어 전송 진행률 (%) |
| 6 | OTA | gOTA_CRC_OK | uint32 | 0 | 1 | 0 | CRC-32 검증 결과 (0=실패, 1=통과) |
| 7 | OTA | gTotalBlocks | uint32 | 0 | 65535 | 0 | 전체 전송 블록 수 |
| 8 | OTA | gCurrentBlock | uint32 | 0 | 65535 | 0 | 현재 수신 블록 인덱스 |
| 9 | Vehicle | gEmergencyMode | uint32 | 0 | 1 | 0 | 물류차 긴급차량 모드 전환 상태 (0=물류, 1=긴급) |
