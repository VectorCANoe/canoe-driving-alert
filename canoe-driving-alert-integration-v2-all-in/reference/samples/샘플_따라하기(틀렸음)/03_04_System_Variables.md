# 0304_System Variables (시스템 변수)

## IVI vECU 프로젝트 시스템 변수 정의

> **작성 기준**: 멘토 샘플 형식 준수
> **작성일**: 2026-02-13

---

## CANoe 시스템 변수 목록

| ID | Namespace | Name | Data Type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|---------------|-------------|
| 1 | IVI | IgnStart | uint32 | 0 | 1 | 0 | 시동 여부 판단 (0: OFF, 1: ON) |
| 2 | IVI | ProfileSelected | uint32 | 1 | 3 | 1 | 선택된 프로필 (1/2/3) |
| 3 | IVI | ModeSelected | uint32 | 0 | 2 | 1 | 선택된 모드 (0: 에코, 1: 컴포트, 2: 스포츠) |
| 4 | Lighting | AmbientColorR | uint8 | 0 | 255 | 255 | 앰비언트 조명 색상 R (0~255) |
| 5 | Lighting | AmbientColorG | uint8 | 0 | 255 | 255 | 앰비언트 조명 색상 G (0~255) |
| 6 | Lighting | AmbientColorB | uint8 | 0 | 255 | 255 | 앰비언트 조명 색상 B (0~255) |
| 7 | Lighting | AmbientBrightness | uint8 | 0 | 100 | 50 | 앰비언트 조명 밝기 (0~100%) |
| 8 | Lighting | SeatLightOn | uint8 | 0 | 1 | 0 | 시트조명 ON/OFF (0: OFF, 1: ON) |
| 9 | Lighting | RearLightOn | uint8 | 0 | 1 | 0 | 후방 조명 ON/OFF (0: OFF, 1: ON) |
| 10 | Lighting | FootLightOn | uint8 | 0 | 1 | 0 | 바닥·발판 조명 ON/OFF (0: OFF, 1: ON) |
| 11 | Lighting | BlinkMode | uint8 | 0 | 2 | 0 | 점멸 모드 (0: 정상, 1: 느림, 2: 빠름) |
| 12 | Vehicle | VehicleSpeed | uint8 | 0 | 255 | 0 | 차량 속도 (0~255 km/h) |
| 13 | Vehicle | GearStatus | uint8 | 0 | 3 | 0 | 기어 상태 (0: P, 1: R, 2: N, 3: D) |
| 14 | Vehicle | DoorStatus | uint8 | 0 | 255 | 0 | 도어 개방 상태 (비트맵: 0x01=운전석, 0x02=조수석, 0x04=후석좌, 0x08=후석우) |
| 15 | HVAC | InteriorTemp | int8 | -20 | 40 | 22 | 실내 온도 (-20~40°C) |
| 16 | Weather | WiperStatus | uint8 | 0 | 3 | 0 | 와이퍼 상태 (0: OFF, 1~3: 속도) |
| 17 | Weather | ExteriorBrightness | uint8 | 0 | 100 | 50 | 외부 밝기 (0: 어두움 ~ 100: 밝음) |
| 18 | ADAS | LDW_Event | uint8 | 0 | 1 | 0 | 차선 이탈 경고 (0: 정상, 1: 이탈) |
| 19 | ADAS | LDW_Direction | uint8 | 0 | 1 | 0 | 이탈 방향 (0: 좌측, 1: 우측) |
| 20 | ADAS | RearObstacleDistance | uint8 | 0 | 255 | 255 | 후방 장애물 거리 (0~255 cm) |
| 21 | ADAS | AEB_Event | uint8 | 0 | 1 | 0 | 긴급 제동 이벤트 (0: 정상, 1: 긴급 제동) |
| 22 | ADAS | AEB_Level | uint8 | 0 | 3 | 0 | 위험 수준 (0: 낮음, 1: 중간, 2: 높음, 3: 매우 높음) |
| 23 | ADAS | SideObjectDetected | uint8 | 0 | 1 | 0 | 후측방 객체 감지 (0: 없음, 1: 있음) |
| 24 | ADAS | StatusIcon | uint8 | 0 | 15 | 0 | ADAS 기능 활성 상태 아이콘 (비트맵) |
| 25 | Safety | WarningUIActive | uint8 | 0 | 1 | 0 | 경고 UI 활성 여부 (0: OFF, 1: ON) |
| 26 | Safety | WarningType | uint8 | 0 | 15 | 0 | 경고 유형 (0: 없음, 1: 후진, 2: LDW, 3: AEB, ...) |
| 27 | Safety | WarningLevel | uint8 | 0 | 3 | 0 | 경고 수준 (0: 정보, 1: 주의, 2: 경고, 3: 위험) |
| 28 | Safety | WarningSoundActive | uint8 | 0 | 1 | 0 | 경고음 활성 여부 (0: OFF, 1: ON) |
| 29 | Safety | FailSafeMode | uint8 | 0 | 1 | 0 | Fail-Safe 모드 (0: 정상, 1: Fail-Safe) |
| 30 | Diagnostic | DTCCount | uint16 | 0 | 65535 | 0 | 저장된 DTC 개수 |
| 31 | Diagnostic | DiagModeActive | uint8 | 0 | 1 | 0 | 진단 모드 활성 (0: 비활성, 1: 활성) |
| 32 | Diagnostic | DiagResult | uint8 | 0 | 1 | 0 | 진단 결과 (0: Fail, 1: Pass) |
| 33 | OTA | OTAProgress | uint8 | 0 | 100 | 0 | OTA 진행률 (0~100%) |
| 34 | OTA | OTAStatus | uint8 | 0 | 3 | 0 | OTA 상태 (0: 대기, 1: 진행중, 2: 성공, 3: 실패) |
| 35 | BDC | SeatOccupancy | uint8 | 0 | 15 | 0 | 좌석 점유 상태 (비트맵) |
| 36 | BDC | SeatPosition | uint8 | 0 | 1 | 0 | 시트 위치 (0: 정상, 1: 후진용) |
| 37 | UserFeedback | ComplaintType | uint8 | 0 | 15 | 0 | 불만 유형 (0: 없음, 1: 불편, 2: 너무 밝음, 3: 늦음, ...) |
| 38 | UserFeedback | FeedbackTimestamp | uint32 | 0 | 4294967295 | 0 | 피드백 시간 (Unix Timestamp) |

---

## Namespace별 분류

### IVI Namespace
- 시동, 프로필, 모드 선택 관련 변수

### Lighting Namespace
- 조명 색상, 밝기, 점멸 모드 등

### Vehicle Namespace
- 차량 속도, 기어 상태, 도어 상태 등

### HVAC/Weather Namespace
- 온도, 와이퍼, 외부 밝기 등

### ADAS Namespace
- ADAS 이벤트 및 센서 데이터

### Safety Namespace
- 경고 UI, 경고음, Fail-Safe 모드

### Diagnostic/OTA Namespace
- 진단, DTC, OTA 관련

---

**다음 단계**: 05_Unit Test, 06_Integration Test, 07_System Test 작성
