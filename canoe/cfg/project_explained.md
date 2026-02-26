# project.sysvars — 시스템 변수 상세 설명

> **주의**: 이 파일은 참조용입니다. CANoe에 로드하는 실제 파일은 `project.sysvars`를 사용하세요.
> `project.sysvars`에는 XML 주석이 없어야 CANoe가 정상 로드합니다.

---

## 파일 구조 개요

```
project.sysvars
  └── SystemVariables (version="4")
        ├── Namespace: Navigation    ← 구간 인식 입력 (Panel 제어)
        ├── Namespace: V2V           ← 긴급차량 V2V 시뮬레이션
        ├── Namespace: Arbiter       ← Alert Arbiter 중재 결과 (CAPL 기록)
        └── Namespace: Ambient       ← 앰비언트 ECU 현재 출력 (Panel 표시)
```

---

## Namespace: Navigation

**역할**: Panel 버튼/슬라이더에서 구간·속도·조향 정보를 주입. Context_Manager CAPL 노드가 읽어서 Vehicle_Context CAN 메시지로 브로드캐스트함.

| 변수명 | 타입 | 기본값 | 범위 | 설명 |
|--------|------|--------|------|------|
| `gRoadZone` | int | 0 | 0~3 | 현재 도로 구간 (아래 표 참조) |
| `gNavDirection` | int | 0 | 0~1 | IC 진출 방향 (gRoadZone=3일 때만 유효) |
| `gZoneDistance` | int | 0 | 0~999 m | 다음 구간 경계까지 남은 거리 |
| `gVehicleSpeed` | float | 60.0 | 0.0~300.0 km/h | 시뮬레이션 차속 |
| `gSteeringInput` | int | 1 | 0~1 | 조향 입력 여부 |

### gRoadZone 값 의미

| 값 | 구간 | 제한속도 | 앰비언트 동작 |
|----|------|---------|-------------|
| 0 | 일반도로 | 80 km/h | 기본 아이들 (딤 화이트) |
| 1 | 스쿨존 | 30 km/h | 앰비언트 AMBER 강조, 과속 시 RED 점멸 |
| 2 | 고속도로 | 110 km/h | 조향 없음 10초 → ORANGE 파동 경고 |
| 3 | IC/휴게소 근접 | — | 좌/우 방향 흐름 애니메이션 |

### gNavDirection 값 의미

| 값 | 의미 |
|----|------|
| 0 | 좌측 진출 → 앰비언트 우→좌 흐름 |
| 1 | 우측 진출 → 앰비언트 좌→우 흐름 |

### gSteeringInput 값 의미

| 값 | 의미 |
|----|------|
| 0 | 조향 없음 (핸즈오프) — 고속도로에서 10초 후 경고 |
| 1 | 조향 활성 (정상) |

---

## Namespace: V2V

**역할**: Ethernet UDP 브로드캐스트를 sysvar로 시뮬레이션. 실제 배포 시에는 Police_Node/Ambulance_Node가 UdpSocket으로 실제 전송하지만, CANoe SIL에서는 이 sysvar로 동일 인터페이스 구현.

| 변수명 | 타입 | 기본값 | 범위 | 설명 |
|--------|------|--------|------|------|
| `Police_Active` | int | 0 | 0~1 | 경찰차 긴급 상태 (0=비활성, 1=긴급출동) |
| `Police_Direction` | int | 0 | 0~3 | 경찰차 접근 방향 |
| `Police_ETA` | int | 999 | 0~999 s | 경찰차 도착 예상 시간 (999=불명) |
| `Ambulance_Active` | int | 0 | 0~1 | 구급차 긴급 상태 (0=비활성, 1=긴급출동) |
| `Ambulance_Direction` | int | 0 | 0~3 | 구급차 접근 방향 |
| `Ambulance_ETA` | int | 999 | 0~999 s | 구급차 도착 예상 시간 (999=불명) |

### Direction 값 의미 (Police/Ambulance 공통)

| 값 | 의미 |
|----|------|
| 0 | Front — 전방에서 접근 |
| 1 | Left — 좌측에서 접근 |
| 2 | Right — 우측에서 접근 |
| 3 | Rear — 후방에서 접근 |

### 실제 Ethernet 메시지 구조 (참조)

```
EmergencyVehicleMsg (브로드캐스트, Port 5000):
  byte[0]  VehicleType   1=POLICE, 2=AMBULANCE
  byte[1]  Status        0=CLEAR,  1=ACTIVE
  byte[2]  Direction     0=Front, 1=Left, 2=Right, 3=Rear
  byte[3]  ETA_seconds   (0~254, 255=unknown)
```

---

## Namespace: Arbiter

**역할**: Civ_Node의 `runArbiter()` 함수가 기록하는 중재 결과. Panel에서 읽어 상태 표시.

| 변수명 | 타입 | 기본값 | 범위 | 설명 |
|--------|------|--------|------|------|
| `gEmergencyType` | int | 0 | 0~2 | 현재 활성 긴급차량 종류 |
| `gAmbientPattern` | int | 0 | 0~8 | Ambient_ECU에 지시하는 패턴 번호 |
| `gArbiterMode` | int | 0 | 0~3 | 현재 우선순위 계층 |
| `gWarningLevel` | int | 0 | 0~2 | 경고 레벨 (Context_Manager가 설정) |

### gEmergencyType 값 의미

| 값 | 의미 |
|----|------|
| 0 | 없음 (평상시) |
| 1 | 경찰차 긴급출동 |
| 2 | 구급차 긴급출동 |

### gAmbientPattern 값 의미

| 값 | 패턴명 | 색상/동작 |
|----|--------|---------|
| 0 | Idle | 딤 화이트 (R=20, G=20, B=20) |
| 1 | Normal | 소프트 화이트 (R=30, G=30, B=30) |
| 2 | School_Ambient | AMBER 상시 (R=255, G=100, B=0) |
| 3 | School_Warning | RED 빠른 점멸 500ms (R=255, G=0, B=0) |
| 4 | Highway_Alert | ORANGE 파동 (R=255, G=60, B=0) |
| 5 | IC_Left | 우→좌 방향 흐름 애니메이션 |
| 6 | IC_Right | 좌→우 방향 흐름 애니메이션 |
| 7 | Police | RED/BLUE 교차 점멸 (250ms) |
| 8 | Ambulance | RED/WHITE 교차 점멸 (200ms) |

### gArbiterMode 값 의미 (우선순위 계층)

| 값 | 계층 | 조건 |
|----|------|------|
| 0 | Base | 기본 gRoadZone 앰비언트 |
| 1 | ZoneWarning | gWarningLevel > 0 |
| 2 | Police | gEmergencyType = 1 |
| 3 | Ambulance | gEmergencyType = 2 (최고 우선순위) |

### gWarningLevel 값 의미

| 값 | 의미 |
|----|------|
| 0 | 경고 없음 |
| 1 | 속도 초과 또는 고속도로 조향 경고 |
| 2 | 예약 (현재 미사용) |

---

## Namespace: Ambient

**역할**: Ambient_ECU가 현재 출력 중인 RGB 값을 기록. Panel의 RGB 인디케이터가 이 값을 읽어 색상 표시.

| 변수명 | 타입 | 기본값 | 범위 | 설명 |
|--------|------|--------|------|------|
| `R_Value` | int | 20 | 0~255 | 현재 Red 채널 |
| `G_Value` | int | 20 | 0~255 | 현재 Green 채널 |
| `B_Value` | int | 20 | 0~255 | 현재 Blue 채널 |
| `BlinkState` | int | 0 | 0~1 | 현재 점멸 위상 (0/1) |
| `AnimStep` | int | 0 | 0~7 | IC 방향 애니메이션 단계 (0~5) |

---

## 변수 간 의존 관계

```
Panel (버튼/슬라이더)
    │
    ├─► Navigation::gRoadZone ──────► Context_Manager.can
    ├─► Navigation::gVehicleSpeed ──► Context_Manager.can
    ├─► Navigation::gSteeringInput ─► Context_Manager.can
    │       └─ Vehicle_Context CAN(0x100) 10ms 브로드캐스트
    │                   │
    │                   ▼
    ├─► V2V::Police_Active ─────────► Police_Node.can (sysvar 감시)
    ├─► V2V::Ambulance_Active ──────► Ambulance_Node.can (sysvar 감시)
    │       │
    │       ▼
    │   Civ_Node.can (runArbiter)
    │       ├─ 우선순위 결정 → Arbiter::gAmbientPattern 설정
    │       └─ Ambient_Control CAN(0x220) 송신
    │                   │
    │                   ▼
    │           Ambient_ECU.can
    │               └─ 패턴 실행 → Ambient::R/G/B_Value 기록
    │
    └─► Arbiter::gWarningLevel ← Context_Manager.can 설정
```

---

## CANoe에서 sysvars 로드 방법

1. CANoe 메뉴: **Environment → System Variables**
2. 상단 **Load** 버튼 클릭
3. `canoe/cfg/project.sysvars` 선택
4. 4개 네임스페이스(Navigation, V2V, Arbiter, Ambient) 확인
5. **OK** → 측정 시작(F9) 전에 반드시 로드 완료

> 로드 실패 시 체크 포인트:
> - `project.sysvars`에 XML 주석(`<!-- -->`)이 없는지 확인
> - UTF-8 인코딩 확인
> - version="4" 속성 확인 (CANoe 17+)
