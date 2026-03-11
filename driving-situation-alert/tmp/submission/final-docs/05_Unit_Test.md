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

## 단위 테스트 표 (공식 표준 양식)

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| 제어기 | 제어 | CGW (`CHS_GW`) | 차량 기본 입력과 차체 상태 정보를 수신하여 100ms 주기로 경계 경로에 전달 |  |  |  |
|  |  | CGW (`INFOTAINMENT_GW`) | 구간, 방향, 거리(m), 제한속도(km/h) 정보를 수신하여 100ms 주기로 표시 경로에 전달 |  |  |  |
|  |  | ADAS (`ADAS_WARN_CTRL`) | 주행 상태와 제한속도(km/h)를 반영하여 150ms 이내 기본 경고 상태를 판단 |  |  |  |
|  |  | V2X (`EMS_ALERT`, V2 확장) | 긴급차량 접근 정보를 수신하고 1000ms 기준 유지, 해제, 타임아웃을 관리 | Ready |  |  |
|  |  | ADAS (`WARN_ARB_MGR`, V2 확장) | 긴급차량 방향과 접근 시간을 반영하여 위험도와 감속 보조를 판단 | Ready |  |  |
|  |  | ADAS (`ADAS_WARN_CTRL`, ADAS 객체 확장, Planned) | 주변 객체와 센서 상태를 반영하여 위험 경고를 판단 | Planned |  |  |
|  |  | CLU (`CLU_HMI_CTRL`, 차량 경보 편의 확장, Planned) | 운전자 상태와 차량 맥락을 반영하여 경고 표시와 안내를 보정 | Planned |  |  |
|  |  | CGW (`DOMAIN_BOUNDARY_MGR`, 경고 강건성·인지성 확장, Planned) | 입력 신선도와 서비스 상태를 반영하여 경고 강등과 경계 상태를 유지 | Planned |  |  |
|  |  | IVI (`NAV_CTX_MGR`) | 구간, 방향, 거리, 제한속도 정보를 받아 주행 맥락을 계산 |  |  |  |
|  |  | V2X (`EMS_ALERT`) | 경찰, 구급 긴급 이벤트의 송신, 수신, 해제, 1000ms 타임아웃 동작을 검증 |  |  |  |
|  |  | ADAS (`WARN_ARB_MGR`) | 긴급 경고와 일반 경고가 겹칠 때 우선순위를 결정 |  |  |  |
|  |  | BCM (`BODY_GW`) | 경고 결과를 50ms 주기로 앰비언트 출력 경로에 전달 |  |  |  |
|  |  | IVI (`IVI_GW`) | 경고 결과를 50ms 주기로 클러스터 표시 경로에 전달 |  |  |  |
|  |  | BCM (`AMBIENT_CTRL`) | 경고 상태에 맞는 앰비언트 색상과 패턴을 50ms 주기로 출력 |  |  |  |
|  |  | CLU (`CLU_HMI_CTRL`) | 경고 문구와 방향 표시를 50ms 주기로 출력 |  |  |  |
|  |  | CGW (`CHS_GW`, 제동 확장) | 전동 주차와 제동 보조 상태를 수신하여 경고 판단 경로에 전달 | Ready |  |  |
|  |  | CGW (`CHS_GW`, 차체 제어 확장) | 차체안정과 승차 제어 상태를 수신하여 경고 판단 경로에 전달 | Ready |  |  |
|  |  | BCM (`BODY_GW`, 출입 개폐 확장) | 출입문과 테일게이트 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | BCM (`BODY_GW`, 탑승자 보호 확장) | 에어백과 탑승자 감지 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | BCM (`BODY_GW`, 실내 편의 확장) | 조명, 공조, 시트, 선루프 상태를 수신하여 차량 상태에 반영 | Ready |  |  |
|  |  | IVI (`IVI_GW`, 표시·안내 확장) | HUD, 음향, 텔레매틱스 상태를 수신하여 화면과 안내 기능에 반영 | Ready |  |  |
|  |  | IVI (`IVI_GW`, 서비스 접근 확장) | 디지털 키와 차량 서비스 상태를 수신하여 사용자 안내에 반영 | Ready |  |  |
|  |  | ADAS (`ADAS_WARN_CTRL`, 주행 보조 확장) | 주행 보조 상태를 수신하여 위험 판단에 반영 | Ready |  |  |
|  |  | ADAS (`ADAS_WARN_CTRL`, 주차·인지 확장) | 주차 보조와 주변 인지 상태를 수신하여 위험 판단에 반영 | Ready |  |  |
|  |  | CGW (경고 전달 경계 관리, 백본 서비스 확장) | 백본 및 경고 서비스 상태 정보를 수신하여 전달 경계 상태와 fail-safe 동작에 반영 | Ready |  |  |
|  |  | CGW (`DOMAIN_ROUTER`, 구동 확장) | 모터와 인버터 상태를 수신하여 차량 구동 상태에 반영 | Ready |  |  |
|  |  | CGW (`DOMAIN_ROUTER`, 전력·충전 확장) | 전력 변환과 충전 상태를 수신하여 차량 구동 상태에 반영 | Ready |  |  |
| 가상 노드 (Simulator) | 입력 | Vehicle/Steering Input | 차량 속도(km/h), 주행 상태, 조향 각도 입력 정보를 생성 |  |  |  |
|  |  | Nav Context Input | 구간, 방향, 거리(m), 제한속도(km/h) 입력 정보를 생성 |  |  |  |
|  |  | Emergency Input | 경찰, 구급 긴급 접근 정보와 도착예정시간(s) 입력을 생성 |  |  |  |
|  |  | EPB Input | 전동 주차 ECU 상태 정보를 입력 |  |  |  |
|  |  | EHB Input | 제동 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | VSM Input | 차체안정 ECU 상태 정보를 입력 |  |  |  |
|  |  | ECS Input | 차고 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | CDC Input | 감쇠 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | DOOR_FL Input | 좌전 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | DOOR_FR Input | 우전 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | DOOR_RL Input | 좌후 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | DOOR_RR Input | 우후 도어 ECU 상태 정보를 입력 |  |  |  |
|  |  | TGM Input | 테일게이트 ECU 상태 정보를 입력 |  |  |  |
|  |  | ACU Input | 에어백 ECU 상태 정보를 입력 |  |  |  |
|  |  | ODS Input | 탑승자 감지 상태를 입력 |  |  |  |
|  |  | AFLS Input | 전조등 방향 제어 상태를 입력 |  |  |  |
|  |  | AHLS Input | 전조등 높이 제어 상태를 입력 |  |  |  |
|  |  | DATC Input | 공조 ECU 상태 정보를 입력 |  |  |  |
|  |  | SEAT_DRV Input | 운전석 시트 편의 상태를 입력 |  |  |  |
|  |  | SEAT_PASS Input | 동승석 시트 편의 상태를 입력 |  |  |  |
|  |  | SRF Input | 선루프 ECU 상태를 입력 |  |  |  |
|  |  | HUD Input | 전면 표시 ECU 상태 정보를 입력 |  |  |  |
|  |  | AMP Input | 음향 출력 ECU 상태 정보를 입력 |  |  |  |
|  |  | TMU Input | 텔레매틱스 ECU 상태 정보를 입력 |  |  |  |
|  |  | SCC Input | 주행 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | PGS Input | 주차 보조 ECU 상태 정보를 입력 |  |  |  |
|  |  | PUS Input | 주차 초음파 센서 상태를 입력 |  |  |  |
|  |  | AVM Input | 주변 영상 ECU 상태를 입력 |  |  |  |
|  |  | FCAM Input | 전방 카메라 센서 상태를 입력 |  |  |  |
|  |  | FRADAR Input | 전방 레이더 센서 상태를 입력 |  |  |  |
|  |  | SRR_FL Input | 좌전 측후방 레이더 상태를 입력 |  |  |  |
|  |  | SRR_FR Input | 우전 측후방 레이더 상태를 입력 |  |  |  |
|  |  | SRR_RL Input | 좌후 측후방 레이더 상태를 입력 |  |  |  |
|  |  | SRR_RR Input | 우후 측후방 레이더 상태를 입력 |  |  |  |
|  |  | IBOX Input | 차량 서비스 ECU 상태 정보를 입력 |  |  |  |
|  |  | SGW Input | 보안 게이트웨이 상태를 입력 |  |  |  |
|  |  | DCM Input | 진단 제어 상태를 입력 |  |  |  |
|  |  | ETHB Input | 백본 서비스 상태를 입력 |  |  |  |
|  |  | OBC Input | 충전 ECU 상태 정보를 입력 |  |  |  |
|  |  | DCDC Input | 전력 변환 ECU 상태 정보를 입력 |  |  |  |
|  |  | MCU Input | 모터 제어 ECU 상태 정보를 입력 |  |  |  |
|  |  | INVERTER Input | 인버터 상태를 입력 |  |  |  |
|  | 출력 | BCM (앰비언트 경고 출력) | 경고 상태에 따라 앰비언트 모드, 색상, 패턴을 출력 | Ready |  |  |
|  |  | IVI (클러스터/HMI 출력) | 경고 문구, 거리/방향, 팝업, 테마, 오디오 포커스 정보를 생성하여 표시 채널에 전달 | Ready |  |  |
|  |  | CLU (클러스터 표시 처리) | 경고 문구와 팝업, 테마 정보를 수신하여 클러스터 표시에 반영 | Ready |  |  |
|  |  | HUD (전면 표시 처리) | 경고 문구와 팝업, 경로, 테마 정보를 수신하여 전면 표시에 반영 | Ready |  |  |
|  |  | AMP (오디오 안내 처리) | 오디오 포커스와 음성안내, TTS 상태를 수신하여 오디오 안내에 반영 | Ready |  |  |
|  |  | ADAS (자동 감속 보조 요청 출력) | 위험도와 fail-safe 상태에 따라 자동 감속 보조 요청을 출력 | Ready |  |  |
|  |  | V2X (경찰 긴급 알림 송신) | 경찰 긴급 알림을 외부 송신 프레임으로 전송 | Ready |  |  |
|  |  | V2X (구급 긴급 알림 송신) | 구급 긴급 알림을 외부 송신 프레임으로 전송 | Ready |  |  |

---
