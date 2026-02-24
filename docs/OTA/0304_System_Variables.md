# 시스템 변수 정의 (System Variables)

> SDV 기반 차량 경험(Experience) 플랫폼 — CANoe sysvar 전체 목록

---

| ID | Namespace | Name | Data Type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|--------------|-------------|
| 1 | Vehicle | vehicleSpeed | double | 0 | 200 | 60 | 차량 속도 (km/h). Panel TrackBar로 조절. gRoadZone별 기준과 비교. |
| 2 | Vehicle | accelValue | double | -10 | 10 | 0 | 가속도 (m/s²). > 3.5 시 A그룹 플래그. |
| 3 | Vehicle | brakeValue | double | 0 | 10 | 0 | 제동 감속도 (m/s²). > 4.0 시 A그룹 플래그. |
| 4 | Vehicle | overspeedFlag | uint32 | 0 | 1 | 0 | 과속 플래그. gRoadZone 기준 초과 시 1. |
| 5 | Vehicle | gGearP | uint32 | 0 | 1 | 0 | P 기어 상태. 0:비P / 1:P. OTA 적용 전제조건. Panel Button으로 설정. |
| 6 | Driver | gazeActive | uint32 | 0 | 1 | 1 | 운전자 응시 여부. 0→1 전환 시 Level 3 경고 해제 트리거. (라엘) |
| 7 | MDPS | steeringInput | uint32 | 0 | 1 | 0 | 조향 핸들 입력. 1 감지 시 Level 3 경고 해제 트리거. (현준) |
| 8 | LDW | laneDeparture | uint32 | 0 | 1 | 0 | 차선이탈 감지. 0:정상 / 1:이탈. B그룹 입력. |
| 9 | LDW | laneChangeAlert | uint32 | 0 | 1 | 0 | 급차선변경 감지. 조향각속도 > 50°/s 시 자동 설정. B그룹 입력. |
| 10 | WDM | warningLevel | uint32 | 0 | 3 | 0 | 현재 경고 단계. 0:없음/1:Level1/2:Level2/3:Level3. WDM_ECU 핵심 출력. |
| 11 | WDM | warningType | uint32 | 0 | 7 | 0 | 경고 원인 비트마스크. bit0:A그룹 / bit1:B그룹. |
| 12 | WDM | roadZone | uint32 | 0 | 3 | 0 | 도로 구간. 0:일반(80km/h)/1:스쿨존(30km/h)/2:고속도로(110km/h)/3:IC출구. Panel 버튼 4개. (준영) |
| 13 | WDM | steerTimer | uint32 | 0 | 600 | 0 | 고속도로 핸들 미입력 타이머 (초). 10초 초과 시 진동 경고. (준영) |
| 14 | WDM | navDirection | uint32 | 0 | 1 | 0 | IC출구 진출 방향. 0:좌 / 1:우. Ambient 방향 안내 연동. (준영) |
| 15 | WDM | crashEvent | uint32 | 0 | 1 | 0 | 충돌 이벤트 시뮬레이션. 1 = Level 3 강제 발령. Panel Button. |
| 16 | Ambient | ambientMode | uint32 | 0 | 4 | 0 | 앰비언트 동작 모드. 0:OFF/1:경고RED/2:ORANGE파동/3:방향안내/4:IC흐름. |
| 17 | Ambient | ambientColor | uint32 | 0 | 4 | 0 | 앰비언트 색상. 0:OFF/1:RED/2:ORANGE/3:BLUE/4:WHITE. |
| 18 | Ambient | ambientPattern | uint32 | 0 | 3 | 0 | 점등 패턴. 0:고정/1:점멸/2:파동/3:흐름. |
| 19 | OTA | packageID | uint32 | 0 | 2 | 0 | 현재 적용된 패키지. 0:없음/1:DriveCoach/2:SeasonalTheme. |
| 20 | OTA | subscriptionLevel | uint32 | 0 | 2 | 0 | 구독 상태. 0:기본/1:DriveCoach/2:SeasonalTheme. |
| 21 | OTA | noviceMode | uint32 | 0 | 1 | 0 | 초보 운전 모드. 0:비활성/1:활성. Drive Coach 적용 시 1. |
| 22 | OTA | speedLimit | uint32 | 0 | 200 | 200 | 최고 속도 제한 (km/h). 200=제한없음. Drive Coach 적용 시 100. |
| 23 | OTA | torqueLimit | uint32 | 0 | 100 | 100 | 최대 토크 제한 (%). 100=제한없음. Drive Coach 적용 시 70. |
| 24 | OTA | ldwSensitivity | uint32 | 0 | 1 | 0 | LDW 경고 민감도. 0:기본/1:강화. Drive Coach 적용 시 1. |
| 25 | OTA | themeID | uint32 | 0 | 4 | 0 | 시즌 테마. 0:없음/1:봄/2:여름/3:가을/4:겨울. Seasonal Theme 적용 시 설정. |
| 26 | OTA | applySuccess | uint32 | 0 | 1 | 0 | 파라미터 적용 성공 여부. CRC8 검증 결과. 0:실패/1:성공. |
| 27 | OTA | otaInProgress | uint32 | 0 | 1 | 0 | OTA 세션 진행 중 여부. 1이면 P 기어 이탈 감시 활성화. |
