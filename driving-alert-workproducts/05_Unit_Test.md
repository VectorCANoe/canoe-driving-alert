# 단위 테스트 (Unit Test)

**Document ID**: PROJ-05-UT
**ISO 26262 Reference**: Part 6, Cl.9 (Software Unit Verification)
**ASPICE Reference**: SWE.4 (Software Unit Verification)
**Version**: 2.25
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 하단 (SWE.4) | `05_Unit_Test.md` | `04_SW_Implementation.md` | `06_Integration_Test.md` |

---

> 경고: `canoe/src/capl` 구현이 추가 개발 또는 업데이트되면, 해당 변경과 직접 연결된 UT 상태, oracle, evidence, executable TEST 자산도 같은 기준선에서 즉시 동기화해야 한다. CAPL과 테스트 문서/자산 중 하나라도 불일치하면 검증 기준은 유효하지 않다.

## 단위 테스트 표 (공식 표준 양식)

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| 제어기 | 제어 | UT_001 - CGW (`CHS_GW`) | 차량 기본 입력과 차체 상태 정보를 수신하여 100ms 주기로 경계 경로에 전달 | Ready |  |  |
|  |  | UT_002 - CGW (`INFOTAINMENT_GW`) | 구간, 방향, 거리(m), 제한속도(km/h) 정보를 수신하여 100ms 주기로 표시 경로에 전달 | Ready |  |  |
|  |  | UT_003 - ADAS (`ADAS_WARN_CTRL`) | 주행 상태와 제한속도(km/h)를 반영하여 150ms 이내 기본 경고 상태를 판단 | Ready |  |  |
|  |  | UT_004 - V2X (`EMS_ALERT`, V2 확장) | 긴급차량 접근 정보를 수신하고 1000ms 기준 유지, 해제, 타임아웃을 관리 | Ready |  |  |
|  |  | UT_005 - ADAS (`WARN_ARB_MGR`, V2 확장) | 긴급차량 방향과 접근 시간을 반영하여 위험도와 감속 보조를 판단 | Ready |  |  |
|  |  | UT_006 - ADAS (`ADAS_WARN_CTRL`, ADAS 객체 확장) | 주변 객체와 센서 상태를 반영하여 위험 경고를 판단 | Ready |  |  |
|  |  | UT_007 - CLU (`CLU_HMI_CTRL`, 차량 경보 편의 확장) | 운전자 상태와 차량 맥락을 반영하여 경고 표시와 안내를 보정 | Ready |  |  |
|  |  | UT_008 - CGW (`DOMAIN_BOUNDARY_MGR`, 경고 강건성·인지성 확장) | 입력 신선도와 서비스 상태를 반영하여 경고 강등과 경계 상태를 유지 | Ready |  |  |
|  |  | UT_009 - IVI (`NAV_CTX_MGR`) | 구간, 방향, 거리, 제한속도 정보를 받아 주행 맥락을 계산 | Ready |  |  |
|  |  | UT_010 - V2X (`EMS_ALERT`) | 경찰, 구급 긴급 이벤트의 송신, 수신, 해제, 1000ms 타임아웃 동작을 검증 | Ready |  |  |
|  |  | UT_011 - ADAS (`WARN_ARB_MGR`) | 긴급 경고와 일반 경고가 겹칠 때 우선순위를 결정 | Ready |  |  |
|  |  | UT_012 - BCM (`BODY_GW`) | 경고 결과를 50ms 주기로 앰비언트 출력 경로에 전달 | Ready |  |  |
|  |  | UT_013 - IVI (`IVI_GW`) | 경고 결과를 50ms 주기로 클러스터 표시 경로에 전달 | Ready |  |  |
|  |  | UT_014 - BCM (`AMBIENT_CTRL`) | 경고 상태에 맞는 앰비언트 색상과 패턴을 50ms 주기로 출력 | Ready |  |  |
|  |  | UT_015 - CLU (`CLU_HMI_CTRL`) | 경고 문구와 방향 표시를 50ms 주기로 출력 | Ready |  |  |
|  |  | UT_016 - CGW (`CHS_GW`, 제동 확장) | 전동 주차와 제동 보조 상태를 수신하여 경고 판단 경로에 전달 | Ready |  |  |
|  |  | UT_017 - CGW (`CHS_GW`, 차체 제어 확장) | 차체안정과 승차 제어 상태를 수신하여 경고 판단 경로에 전달 | Ready |  |  |
|  |  | UT_018 - BCM (`BODY_GW`, 출입 개폐 확장) | 출입문과 테일게이트 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | UT_019 - BCM (`BODY_GW`, 탑승자 보호 확장) | 에어백과 탑승자 감지 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | UT_020 - BCM (`BODY_GW`, 실내 편의 확장) | 조명, 공조, 시트, 선루프 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | UT_021 - IVI (`IVI_GW`, 표시·안내 확장) | HUD, 음향, 텔레매틱스 상태를 수신하여 화면과 안내 기능에 반영 | Ready |  |  |
|  |  | UT_022 - IVI (`IVI_GW`, 서비스 접근 확장) | 디지털 키와 차량 서비스 상태를 수신하여 사용자 안내에 반영 | Ready |  |  |
|  |  | UT_023 - ADAS (`ADAS_WARN_CTRL`, 주행 보조 확장) | 주행 보조 상태를 수신하여 위험 판단에 반영 | Ready |  |  |
|  |  | UT_024 - ADAS (`ADAS_WARN_CTRL`, 주차·인지 확장) | 주차 보조와 주변 인지 상태를 수신하여 위험 판단에 반영 | Ready |  |  |
|  |  | UT_025 - CGW (경고 전달 경계 관리, 백본 서비스 확장) | 백본 및 경고 서비스 상태 정보를 수신하여 전달 경계 상태와 fail-safe 동작에 반영 | Ready |  |  |
|  |  | UT_026 - CGW (`DOMAIN_ROUTER`, 구동 확장) | 모터와 인버터 상태를 수신하여 차량 구동 상태에 반영 | Ready |  |  |
|  |  | UT_027 - CGW (`DOMAIN_ROUTER`, 전력·충전 확장) | 전력 변환과 충전 상태를 수신하여 차량 구동 상태에 반영 | Ready |  |  |
| 가상 노드 (Simulator) | 입력 | UT_028 - Vehicle/Steering Input | 차량 속도(km/h), 주행 상태, 조향 각도 입력 정보를 생성 |  |  |  |
|  |  | UT_029 - Nav Context Input | 구간, 방향, 거리(m), 제한속도(km/h) 입력 정보를 생성 |  |  |  |
|  |  | UT_030 - Emergency Input | 경찰, 구급 긴급 접근 정보와 도착예정시간(s) 입력을 생성 |  |  |  |
|  |  | UT_031 - EPB Input | 전동 주차 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_032 - EHB Input | 제동 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_033 - VSM Input | 차체안정 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_034 - ECS Input | 차고 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_035 - CDC Input | 감쇠 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_036 - DOOR_FL Input | 좌전 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_037 - DOOR_FR Input | 우전 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_038 - DOOR_RL Input | 좌후 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_039 - DOOR_RR Input | 우후 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_040 - TGM Input | 테일게이트 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_041 - ACU Input | 에어백 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_042 - ODS Input | 탑승자 감지 상태를 입력 |  |  |  |
|  |  | UT_043 - AFLS Input | 전조등 방향 제어 상태를 입력 |  |  |  |
|  |  | UT_044 - AHLS Input | 전조등 높이 제어 상태를 입력 |  |  |  |
|  |  | UT_045 - DATC Input | 공조 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_046 - SEAT_DRV Input | 운전석 시트 편의 상태를 입력 |  |  |  |
|  |  | UT_047 - SEAT_PASS Input | 동승석 시트 편의 상태를 입력 |  |  |  |
|  |  | UT_048 - SRF Input | 선루프 ECU 상태를 입력 |  |  |  |
|  |  | UT_049 - HUD Input | 전면 표시 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_050 - AMP Input | 음향 출력 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_051 - TMU Input | 텔레매틱스 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_052 - SCC Input | 주행 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_053 - PGS Input | 주차 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_054 - PUS Input | 주차 초음파 센서 상태를 입력 |  |  |  |
|  |  | UT_055 - AVM Input | 주변 영상 ECU 상태를 입력 |  |  |  |
|  |  | UT_056 - FCAM Input | 전방 카메라 센서 상태를 입력 |  |  |  |
|  |  | UT_057 - FRADAR Input | 전방 레이더 센서 상태를 입력 |  |  |  |
|  |  | UT_058 - SRR_FL Input | 좌전 측후방 레이더 상태를 입력 |  |  |  |
|  |  | UT_059 - SRR_FR Input | 우전 측후방 레이더 상태를 입력 |  |  |  |
|  |  | UT_060 - SRR_RL Input | 좌후 측후방 레이더 상태를 입력 |  |  |  |
|  |  | UT_061 - SRR_RR Input | 우후 측후방 레이더 상태를 입력 |  |  |  |
|  |  | UT_062 - IBOX Input | 차량 서비스 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_063 - SGW Input | 보안 게이트웨이 상태를 입력 | Ready |  |  |
|  |  | UT_064 - DCM Input | 진단 제어 상태를 입력 | Ready |  |  |
|  |  | UT_065 - ETHB Input | 백본 서비스 상태를 입력 |  |  |  |
|  |  | UT_066 - OBC Input | 충전 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_067 - DCDC Input | 전력 변환 ECU 상태를 입력 |  |  |  |
|  |  | UT_068 - MCU Input | 모터 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | UT_069 - INVERTER Input | 인버터 상태를 입력 |  |  |  |
|  | 출력 | UT_070 - BCM (앰비언트 경고 출력) | 경고 상태에 따라 앰비언트 모드, 색상, 패턴을 출력 | Ready |  |  |
|  |  | UT_071 - IVI (클러스터/HMI 출력) | 경고 문구, 거리/방향, 팝업, 테마, 오디오 포커스 정보를 생성하여 표시 채널에 전달 | Ready |  |  |
|  |  | UT_072 - CLU (클러스터 표시 처리) | 경고 문구와 팝업, 테마 정보를 수신하여 클러스터 표시에 반영 | Ready |  |  |
|  |  | UT_073 - HUD (전면 표시 처리) | 경고 문구와 팝업, 경로, 테마 정보를 수신하여 전면 표시에 반영 | Ready |  |  |
|  |  | UT_074 - AMP (오디오 안내 처리) | 오디오 포커스와 음성안내, TTS 상태를 수신하여 오디오 안내에 반영 | Ready |  |  |
|  |  | UT_075 - ADAS (자동 감속 보조 요청 출력) | 위험도와 fail-safe 상태에 따라 자동 감속 보조 요청을 출력 | Ready |  |  |
|  |  | UT_076 - V2X (경찰 긴급 알림 송신) | 경찰 긴급 알림을 외부 송신 프레임으로 전송 | Ready |  |  |
|  |  | UT_077 - V2X (구급 긴급 알림 송신) | 구급 긴급 알림을 외부 송신 프레임으로 전송 | Ready |  |  |

---
