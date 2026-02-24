# 컨셉 디자인 (Concept Design)

> SDV 기반 차량 경험(Experience) 플랫폼 — 시스템 개요 / 네트워크 / 시나리오 흐름

---

## 1. What — 시스템 구성도

```
┌─────────────────────────────────────────────────────────────┐
│                    입력층 (Foundation)                        │
│  A: Vehicle_ECU ── 속도/가속도/제동 (스칼라)                  │
│  B: MDPS_ECU ───── 조향 입력/급차선변경 (벡터)               │
│     LDW_ECU ────── 차선이탈 감지                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ CAN-LS (125kbps) → CGW → CAN-HS
┌─────────────────────▼───────────────────────────────────────┐
│                    판단층 WDM_ECU (Rule-Based)                │
│  A 단독 OR B 단독  → Level 1 (Cluster 황색 + Sound)          │
│  A AND B           → Level 2 (Cluster 적색 + Sound + Ambient)│
│  gCrashEvent = 1   → Level 3 (긴급 — 운전자 능동 해제 필요)  │
└────────────┬────────────────────────────────────────────────┘
             │ CAN-HS (500kbps)
┌────────────▼────────────────────────────────────────────────┐
│  출력층                                                       │
│  Cluster_ECU ─ 경고등 (황색/적색)                            │
│  Ambient_ECU ─ 앰비언트 라이트 (패턴/색상)                   │
│  Sound_ECU ── 경고음 (1~3단계)                               │
│  IVI_ECU ──── 경고 표시 / OTA 구독 팝업                      │
└─────────────────────────────────────────────────────────────┘
    │ 해제                    │ 특화층 D
    │                         │
┌───▼───────────────┐  ┌──────▼──────────────────────────────┐
│  해제층            │  │  특화층 D                           │
│  라엘: 응시 복귀   │  │  준영: gRoadZone 구간 인식           │
│  현준: 핸들 입력   │  │    스쿨존 / 고속도로 / IC출구 안내  │
└───────────────────┘  │                                     │
                       │  성현: OTA 구독 서비스 (SOTA)        │
                       │    Drive Coach / Seasonal Theme     │
                       │    ETH_OTA_Param (UDP, 8 bytes)     │
                       └─────────────────────────────────────┘
```

---

## 2. 주요 도메인 및 역할

| 도메인 | ECU / 노드 | 역할 |
|--------|-----------|------|
| 입력 A | Vehicle_ECU | 차속·가속도·제동을 CAN-LS 0x100으로 100ms 주기 WDM_ECU에 보고 |
| 입력 B | MDPS_ECU | 조향 입력·급차선변경을 CAN-LS 0x110으로 WDM_ECU에 보고 |
| 입력 B | LDW_ECU | 차선이탈을 CAN-LS 0x120으로 WDM_ECU에 보고 |
| Gateway | CGW | CAN-LS(입력층) → CAN-HS(WDM_ECU) 신호 라우팅 |
| 판단층 | WDM_ECU | Rule-Based 위험 판단 → gWarningLevel 0~3 설정 → 출력 ECU 제어 |
| 출력 | Cluster_ECU | 황색/적색 경고등 활성화 |
| 출력 | Ambient_ECU | 앰비언트 라이트 패턴 제어 (구간별/경고 단계별) |
| 출력 | Sound_ECU | 단계별 경고음 출력 |
| 출력 | IVI_ECU | 경고 표시 / OTA 구독 팝업 / 적용 완료 알림 |
| OTA | OTA_Server | ETH_OTA_Param(UDP Port 6000) 전송 — SOTA 파라미터 패킷 |
| OTA | OTA_ECU | ETH_OTA_Param 수신 → CRC8 검증 → sysvar 업데이트 → CAN_OTA_Applied 전송 |

---

## 3. How — 네트워크 토폴로지

```
[CAN-LS 125kbps] ──────────────────────── CGW ──────────
  Vehicle_ECU  (0x100 — 차속/가속)                        │
  MDPS_ECU     (0x110 — 조향/급차선변경)                   │ CAN-HS
  LDW_ECU      (0x120 — 차선이탈)                          │ 500kbps
                                                        WDM_ECU
                                                           │
[CAN-HS 500kbps] ─────────────────────────────────────────
  WDM_ECU      (0x200 — WDM_Warning)
  Cluster_ECU  (0x210 — Cluster_Warning)
  Ambient_ECU  (0x220 — Ambient_Control)
  Sound_ECU    (0x230 — Sound_Control)
  IVI_ECU      (0x240 — IVI_Status)
  OTA_ECU      (0x600 — CAN_OTA_Applied)

[Ethernet UDP]
  OTA_Server ─ Port 6000 ─ OTA_ECU  (ETH_OTA_Param, 8 bytes)
```

---

## 4. Scenario — E2E 시나리오 흐름

### Base 시나리오 (경고 시스템)

```
정상 주행 → 위험 감지 (A 또는 B 입력)
  → WDM_ECU: gWarningLevel 설정 (1/2/3)
  → Cluster/Sound/Ambient/IVI: 단계별 경고 출력
  → 해제: Level 1/2 자동 소거 | Level 3 운전자 능동 해제
```

### Test Suite 1 — 준영 (구간 인식)

```
Panel 버튼으로 gRoadZone 설정
  → 스쿨존(1): 과속 시 Ambient RED 점멸
  → 고속도로(2): 핸들 미입력 10초 → Ambient ORANGE 파동 + 진동
  → IC출구(3): gNavDirection에 따라 좌/우 방향 안내 흐름 애니메이션
```

### Test Suite 2 — 성현 (SOTA OTA 구독)

```
[Drive Coach]
P 기어 정차 → IVI [Drive Coach 설치] 버튼
  → OTA_Server: ETH_OTA_Param 전송 (PackageID=0x01, 8 bytes)
  → OTA_ECU: CRC8 검증 통과 → sysvar 업데이트
  → CAN_OTA_Applied(0x600) → WDM_ECU 파라미터 즉시 활성화
  → IVI: "Drive Coach 적용 완료"

[Seasonal Theme]
P 기어 정차 → IVI 알림 → 운전자 동의
  → OTA_Server: ETH_OTA_Param 전송 (PackageID=0x02, ThemeID=1~4)
  → OTA_ECU: 검증 통과 → sysvar 업데이트
  → Ambient 테마 색상 + IVI 배경 즉시 변경

[Fail-Safe]
CRC8 불일치 → 파라미터 미적용 → 이전 설정 유지
P 기어 이탈 → OTA 세션 즉시 중단
```

---

## 5. 검증 환경

| 항목 | 내용 |
|------|------|
| Tool | Vector CANoe 17+ (SIL — Software In the Loop) |
| Language | CAPL (Communication Access Programming Language) |
| Network | Virtual CAN-LS / CAN-HS / Virtual Ethernet (Local Loopback) |
| Panel | gRoadZone 버튼(4개) / 속도·가속도 TrackBar / OTA 구독 버튼 / 상태 Indicator |
