# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 — 소프트웨어 아키텍처 설계 (데이터 인터페이스 정의)
**ASPICE Reference**: SWE.2 (BP3: 소프트웨어 인터페이스 정의, SWE.3 BP1: 상세 설계)
**Version**: 1.0
**Date**: 2026-02-23
**Status**: Released

| V-Model 위치 | 대응 문서 | 상위 연결 | 하위 연결 |
|-------------|---------|---------|---------|
| 좌측 하단 — SWE.2 시스템 변수 | `05_Unit_Test.md` (SWE.4) | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

**CANoe 연관**: 본 문서의 변수는 CANoe System Variables(`project.sysvars`)로 직접 구현되며 CAPL에서 `sysvar::Namespace::Name` 형식으로 참조.

---

| ID | Namespace | Name | Data Type | Min | Max | Initial Value | Description |
|----|-----------|------|-----------|-----|-----|--------------|-------------|
| 1 | Vehicle | vehicleSpeed | double | 0 | 200 | 60 | 차량 속도 (km/h). Panel TrackBar로 조절. gRoadZone별 임계값과 비교. |
| 2 | Vehicle | accelValue | double | -10 | 10 | 0 | 가속도 (m/s²). 양수: 가속, 음수: 제동. >3.5 시 급가속 이벤트. |
| 3 | Vehicle | brakeValue | double | 0 | 10 | 0 | 제동 감속도 (m/s²). >4.0 시 급제동 이벤트. |
| 4 | Vehicle | overspeedFlag | uint32 | 0 | 1 | 0 | 과속 플래그. gRoadZone 기준 초과 시 자동 설정. |
| 5 | Driver | gazeActive | uint32 | 0 | 1 | 1 | 운전자 응시 여부. 0: 전방 미응시, 1: 전방 응시. 0→1 전환 시 경고 해제 트리거. (라엘) |
| 6 | MDPS | steeringInput | uint32 | 0 | 1 | 0 | 조향 핸들 입력 여부. 0: 미입력, 1: 입력. 1 감지 시 경고 해제 트리거. (현준) |
| 7 | LDW | laneDeparture | uint32 | 0 | 1 | 0 | 차선이탈 감지 여부. 0: 정상, 1: 이탈. B그룹 입력. |
| 8 | LDW | laneChangeAlert | uint32 | 0 | 1 | 0 | 급차선변경 감지 여부. 0: 정상, 1: 감지. 조향각속도 >50°/s 시 자동 설정. |
| 9 | WDM | warningLevel | uint32 | 0 | 3 | 0 | 현재 경고 단계. 0:없음 / 1:1단계 / 2:2단계 / 3:3단계. WDM_ECU 핵심 출력. |
| 10 | WDM | warningType | uint32 | 0 | 7 | 0 | 경고 원인 비트마스크. bit0:A그룹 / bit1:B그룹 / bit2:OTA조건. |
| 11 | WDM | roadZone | uint32 | 0 | 3 | 0 | 도로 구간. 0:일반도로(80km/h) / 1:스쿨존(30km/h) / 2:고속도로(110km/h) / 3:IC출구. Panel 버튼 4개로 설정. (준영) |
| 12 | WDM | accelCount | uint32 | 0 | 10 | 0 | 급가속 누적 카운트 (10분 타이머 기반). ≥3 시 OTA 조건 충족. (택천) |
| 13 | WDM | accelTimerActive | uint32 | 0 | 1 | 0 | 급가속 10분 타이머 활성화 여부. |
| 14 | WDM | steerTimer | uint32 | 0 | 600 | 0 | 고속도로 핸들 미입력 타이머 (초). 10초 초과 시 진동 경고. (준영) |
| 15 | Ambient | ambientMode | uint32 | 0 | 5 | 0 | 앰비언트 동작 모드. 0:OFF / 1:경고RED / 2:ORANGE파동 / 3:방향안내 / 4:IC흐름 / 5:사용자정의. |
| 16 | Ambient | ambientColor | uint32 | 0 | 7 | 0 | 앰비언트 색상 코드. 0:OFF / 1:RED / 2:ORANGE / 3:BLUE / 4:WHITE. |
| 17 | Ambient | ambientPattern | uint32 | 0 | 3 | 0 | 점등 패턴. 0:고정 / 1:점멸 / 2:파동 / 3:흐름. |
| 18 | OTA | subscriptionLevel | uint32 | 0 | 2 | 0 | 현재 OTA 구독 레벨. 0:기본 / 1:Level1(무료, 토크0.85) / 2:Level2(유료, 토크0.75). |
| 19 | OTA | otaInProgress | uint32 | 0 | 1 | 0 | OTA 업데이트 진행 중 여부. |
| 20 | OTA | blockSequenceCounter | uint32 | 0 | 255 | 0 | 전송 블록 순서 카운터 (0x36 SubFunction). |
| 21 | OTA | crcMatch | uint32 | 0 | 1 | 0 | CRC-32 검증 일치 여부. 0: 불일치, 1: 일치. |
| 22 | OTA | rollbackTriggered | uint32 | 0 | 1 | 0 | Rollback 실행 여부. |
| 23 | OTA | otaProgress | uint32 | 0 | 100 | 0 | OTA 전송 진행률 (%). IVI_ECU 표시용. |
| 24 | Rain | rainMode | uint32 | 0 | 1 | 0 | 빗길 모드. 0: 맑음, 1: 빗길. 빗길 시 경고 임계값 하향 적용. |
| 25 | Door | doorLockActive | uint32 | 0 | 1 | 0 | 3단계 도어 잠금 활성화 여부. 3초 후 자동 해제. (현준2) |
| 26 | CGW | busOffDetected | uint32 | 0 | 1 | 0 | CAN Bus Off 감지 여부. 1 감지 시 OTA 세션 안전 중단 트리거. |
| 27 | UDS | currentSession | uint32 | 1 | 3 | 1 | 현재 UDS 세션. 1: Default, 2: Programming, 3: Extended. |
| 28 | UDS | lastServiceID | uint32 | 0 | 255 | 0 | 마지막 UDS 서비스 ID. |
| 29 | UDS | lastResponseCode | uint32 | 0 | 255 | 0 | 마지막 UDS 응답 코드. |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-23 | 초기 생성 |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| Project Manager | — | — | 2026-02-23 |
| Lead Engineer | — | — | 2026-02-23 |
