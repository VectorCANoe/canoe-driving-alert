# CANoe 프로젝트 구조 — 주행상황 연동 실시간 경고 시스템

## 폴더 구성

```
canoe/
├── cfg/
│   └── project.sysvars       ← System Variables 정의 (XML)
├── databases/
│   └── emergency_system.dbc  ← CAN 메시지/신호 데이터베이스
└── nodes/
    ├── Context_Manager.can   ← 구간 인식: gRoadZone + 속도/조향 경고 평가
    ├── Police_Node.can       ← V2V 경찰차: ETH 브로드캐스트 시뮬
    ├── Ambulance_Node.can    ← V2V 구급차: ETH 브로드캐스트 시뮬
    ├── Civ_Node.can          ← 수신 차량: Alert Arbiter 핵심 로직
    ├── Ambient_ECU.can       ← 앰비언트 패턴 실행 (RGB 타이머/애니메이션)
    └── Cluster_ECU.can       ← 클러스터 경고 문구 표시
```

## CAN 버스 채널 매핑

| 채널 | 프로토콜 | 속도 | 역할 |
|------|----------|------|------|
| CAN 1 (HS) | CAN 2.0B | 500 kbps | 모든 내부 노드 연결 (단일 버스) |
| Ethernet (시뮬) | sysvar | — | V2V 긴급차량 브로드캐스트 (Police/Ambulance → Civ_Node) |

## CAN 메시지 목록

| ID | 이름 | 주기 | 송신 | 수신 |
|----|------|------|------|------|
| 0x100 | Vehicle_Context | 10ms | Context_Manager | Civ_Node, Ambient_ECU, Cluster_ECU |
| 0x220 | Ambient_Control | 이벤트 | Civ_Node | Ambient_ECU |
| 0x221 | Cluster_Warning | 이벤트 | Civ_Node | Cluster_ECU |

## System Variable 목록

| Namespace | 변수 | 제어 | 설명 |
|-----------|------|------|------|
| Navigation | gRoadZone (0~3) | Panel 버튼 | 0=일반 1=스쿨존 2=고속도로 3=IC |
| Navigation | gVehicleSpeed | Panel TrackBar | 차속 (km/h) |
| Navigation | gSteeringInput (0/1) | Panel 버튼 | 0=조향없음 1=조향있음 |
| Navigation | gNavDirection (0/1) | Panel 버튼 | 0=좌측출구 1=우측출구 |
| V2V | Police_Active (0/1) | Panel 버튼 | 경찰차 긴급 출동 (ETH 시뮬) |
| V2V | Police_ETA | Panel TrackBar | 경찰차 도달예상시간(초) |
| V2V | Police_Direction (0~3) | Panel 선택 | 접근 방향 |
| V2V | Ambulance_Active (0/1) | Panel 버튼 | 구급차 긴급 출동 (ETH 시뮬) |
| V2V | Ambulance_ETA | Panel TrackBar | 구급차 도달예상시간(초) |
| V2V | Ambulance_Direction (0~3) | Panel 선택 | 접근 방향 |
| Arbiter | gArbiterMode (0~3) | Civ_Node 기록 | 현재 중재 모드 (Panel 표시용) |
| Arbiter | gAmbientPattern (0~8) | Civ_Node 기록 | 현재 앰비언트 패턴 |
| Ambient | R/G/B_Value | Ambient_ECU 기록 | 현재 RGB값 (Panel LED 인디케이터) |

## Alert Arbiter 우선순위

```
1순위 (최고): Ambulance_Active == 1  → AMBULANCE (RED/WHITE 150ms 교차)
2순위:        Police_Active == 1     → POLICE    (RED/BLUE 150ms 교차)
3순위:        WarningLevel > 0
  Zone 1 과속  → SCHOOLZONE_WARN    (RED 200ms 점멸)
  Zone 2 조향  → HIGHWAY_ALERT      (ORANGE 500ms 파동)
4순위 (최저): 구간 기본 앰비언트
  Zone 0 일반  → NORMAL             (WHITE 60,60,60)
  Zone 1 스쿨존→ SCHOOLZONE_AMBIENT (ORANGE 저조도 파동)
  Zone 3 IC 좌 → IC_LEFT            (초록→분홍→빨강 400ms 순환)
  Zone 3 IC 우 → IC_RIGHT           (동일 패턴)
```

## CANoe 프로젝트 설정 방법 (Windows)

1. CANoe 17 실행 → **File > New Configuration**
2. **Network** 탭 → CAN Channel 1 추가 (500kbps)
3. **Database** 탭 → `databases/emergency_system.dbc` 로드
4. **System Variables** → `cfg/project.sysvars` 로드
5. **Nodes** 탭 → `nodes/` 폴더의 .can 파일 6개 추가
   - 각 노드를 CAN Channel 1에 연결
6. **Panel Editor** → 버튼/TrackBar/LED 인디케이터 구성
   - Navigation 버튼 4개 (일반/스쿨존/고속도로/IC)
   - V2V 버튼 4개 (경찰 출동/해제, 구급 출동/해제)
   - ETA TrackBar 2개, 방향 선택 2개
   - Ambient RGB LED 인디케이터 (R/G/B_Value sysvar 연결)
7. **Start** (F9) → Trace 창에서 CAN 메시지 확인

## Ethernet (V2V) 시뮬레이션 구조

```
[Panel 버튼] → sysvar V2V::Police_Active = 1
                    ↓
            Police_Node.can (on sysvar)
              → keepAlive 500ms 로그 출력 (ETH 브로드캐스트 시뮬)
                    ↓
            Civ_Node.can (on sysvar V2V::Police_Active)
              → runArbiter() 즉시 실행
              → Ambient_Control CAN 송신 (0x220)
              → Cluster_Warning CAN 송신 (0x221)
                    ↓
            Ambient_ECU.can → RED/BLUE 점멸 시작
            Cluster_ECU.can → "경찰차 긴급 접근" 출력
```

실제 Ethernet 배포 시 `UdpSocket::SendTo(socket, "255.255.255.255", 5000, data, 4)` 로 대체.
인터페이스(sysvar 이름, CAN 메시지 ID) 변경 없음.
