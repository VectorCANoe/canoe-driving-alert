# 시스템 동작 분석 / 네트워크 흐름 / 변수 사양서

> 특수목적 차량 V2V 통신 검증 플랫폼 — 0301~0304 통합 문서

---

## 0301. 시스템 기능 분석 (SysFuncAnalysis)

| 대분류 | 중분류 | 기능 요약 |
|--------|--------|-----------|
| **경찰 V2V** | 긴급 브로드캐스트 | 경찰차 긴급 상태 전환 → Ethernet 1:N 동시 전송 → 전 차량 HMI 즉시 강제 경고 |
| **군집 대응** | 위협 단계 동기화 | 선두차 위협 레벨 입력 → Ethernet 동기 명령 → 후행차 전체 동시 동일 동작 수행 |
| **OTA 임무 전환** | 펌웨어 배포 + 검증 | 서버 → Ethernet 블록 전송 → CRC 검증 → 재시작 → 차량 역할 전환 (물류 → 긴급) |
| **Fail-Safe** | 오류 복구 | CRC 불일치 시 이전 상태 자동 복구. 차량 기능 중단 없이 안전 유지 |

---

## 0302. 네트워크 흐름 정의 (NWflowDef)

| 송신 노드 | 수신 노드 | 신호 / 메시지명 | 전송 조건 (Trigger) |
|-----------|-----------|-----------------|----------------------|
| Police_Node | Civ_Node A/B/C | `ETH_Emergency` (gEmergency, 차량 ID, 방향) | 경찰차 긴급 버튼 클릭 시 (Event) |
| Police_Node | Civ_Node A/B/C | `ETH_Emergency_Clear` | 경찰차 해제 버튼 클릭 시 (Event) |
| Civ_Node A/B/C | Cluster / Ambient | `CAN_HMI_Warning` | ETH_Emergency 수신 즉시 (CAN Event) |
| Lead_Node | Follow_Node 1/2/3 | `ETH_ThreatCmd` (gThreatLevel 1/2/3) | 선두차 위협 단계 설정 시 (Event) |
| Lead_Node | Follow_Node 1/2/3 | `ETH_ThreatClear` | 선두차 위협 해제 시 (Event) |
| Follow_Node | Lighting / Brake | `CAN_ThreatAct` | ETH_ThreatCmd 수신 즉시 (CAN Event) |
| Server_Node | Logistics_Node | `ETH_OTA_Start` + `ETH_FW_Block[n]` | 재난 코드 입력 후 OTA 시작 버튼 (Event) |
| Logistics_Node | 내부 CAN | `CAN_EmergencyMode` | CRC 검증 통과 + 재시작 후 (Event) |

---

## 0303. 통신 스펙 (Communication Specification)

| 노드 | 메시지 | 버스 | ID / 포트 | Cycle | DLC |
|------|--------|------|-----------|-------|-----|
| Police_Node | `ETH_Emergency` | Ethernet | UDP Port 5000 | Event | 가변 |
| Lead_Node | `ETH_ThreatCmd` | Ethernet | UDP Port 5001 | Event | 가변 |
| Server_Node | `ETH_FW_Block` | Ethernet | UDP Port 5002 | Event | 512 bytes/block |
| Civ_Node | `CAN_HMI_Warning` | CAN-HS | 0x300 | Event | 8 |
| Follow_Node | `CAN_ThreatAct` | CAN-HS | 0x400 | Event | 8 |
| Logistics_Node | `CAN_EmergencyMode` | CAN-HS | 0x500 | Event | 8 |

---

## 0304. 시스템 변수 명세서 (System Variables)

| Namespace | Variable | Type | 설명 |
|-----------|----------|------|------|
| `Emergency` | `gEmergency` | Integer | 경찰차 긴급 상태 (0: 정상 / 1: 긴급 출동) |
| `Military` | `gThreatLevel` | Integer | 위협 단계 (0: 정상 / 1: 경계 / 2: 회피 / 3: 스텔스) |
| `OTA` | `gOTA_Progress` | Float | 펌웨어 전송 진행률 (0~100%) |
| `OTA` | `gOTA_CRC_OK` | Integer | CRC 검증 결과 (0: 실패 / 1: 통과) |
| `Vehicle` | `gEmergencyMode` | Integer | 물류차 긴급차량 모드 전환 상태 (0: 물류 / 1: 긴급) |
