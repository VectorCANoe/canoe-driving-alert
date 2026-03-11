# 시스템 테스트 (System Test)

**Document ID**: PROJ-07-ST
**ISO 26262 Reference**: Part 4, Cl.10 (System Integration and System Qualification Test)
**ASPICE Reference**: SYS.5 (System Qualification Test)
**Version**: 5.22
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 상단 (SYS.5) | `07_System_Test.md` | `06_Integration_Test.md`, `01_Requirements.md` | 릴리즈/검수 |

---

## 시스템 테스트 시나리오 (공식 표준 양식)

| Scene. ID | 설명 | Pass / Fail | 담당자 | 일자 |
|---|---|---|---|---|
| ST_SPEED_001 | 구간 제한속도 대비 속도 상승/감속 조건에서 경고 활성/해제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_ZONE_001 | 일반/스쿨존/고속 구간 전환 시 구간별 경고 정책이 즉시 반영되는지 확인한다. |  |  |  |
| ST_GUIDE_001 | 유도 구간에서 좌/우 방향 정보가 시각적으로 구분되어 표시되는지 확인한다. |  |  |  |
| ST_GUIDE_002 | 유도 구간 진입/전환/종료 시 경고가 깨지지 않고 기본 상태로 복귀되는지 확인한다. |  |  |  |
| ST_STEER_001 | 고속 구간 무조향 경고 발생 및 조향 복귀 시 해제 동작을 확인한다. |  |  |  |
| ST_EMS_001 | 경찰 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_EMS_002 | 구급 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_001 | 경찰 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_002 | 구급 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_ARB_ETA_001 | 동일 등급 경찰 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_ARB_ETA_002 | 동일 등급 구급 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_TIMEOUT_001 | 긴급 알림 1000ms 무갱신 시 안전 해제 및 복귀 동작을 확인한다. |  |  |  |
| ST_POLICY_001 | 긴급/구간 패턴·색상·문구 정책과 중복 팝업 억제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_BASE_PT_001 | 시동/기어/동력계 상태가 Powertrain 시나리오에서 안정적으로 연동되는지 확인한다. |  |  |  |
| ST_BASE_CH_001 | 가감속/조향/제동 입력이 Chassis 시나리오에서 안전 규칙대로 반영되는지 확인한다. |  |  |  |
| ST_BASE_BODY_001 | 비상등/창문 등 Body 시나리오가 의도한 동작으로 유지되는지 확인한다. |  |  |  |
| ST_BASE_IVI_001 | 클러스터 기본표시/안내/UI 상태가 Infotainment 시나리오에서 일관되게 유지되는지 확인한다. |  |  |  |
| ST_BASE_EXT_BODY_001 | 공조, 시트, 미러, 도어, 와이퍼, 보안 상태가 Body 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_EXT_IVI_001 | 오디오, 음성 안내, TTS 상태가 Infotainment 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_V2_RISK_001 | 긴급차량 근접 위험도 기반 감속 보조 요청과 경고 출력 동기화가 일관되게 동작하는지 확인한다. (SIL Scenario 15/16/17/19) | Ready |  |  |
| ST_V2_FAILSAFE_001 | 경고 전달 이상 시 자동 감속 보조 차단, 최소 경고 채널 유지, fail-safe 전환이 동작하는지 확인한다. (SIL Scenario 18) | Ready |  |  |
| ST_ADAS_OBJ_001 | 객체 목록, 교차로, 합류 위험이 들어올 때 위험 경고와 강등, 이벤트 기록이 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ALERT_EXT_001 | 방향지시등, 주행모드, 안전벨트, 접근거리 표시, 표시 설정, 음량 설정이 함께 반영될 때 경고 안내가 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ROBUST_EXT_001 | 입력 지연, 상태 전이, 채널 전환, 오디오 경합이 발생해도 경고 안내가 안정적으로 유지되는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_EXT_CH_002 | EPB, EHB, VSM, ECS, CDC 상태가 시스템 시나리오에서 경고 맥락으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_BODY_002 | 도어, 테일게이트, 에어백, 탑승자 감지, 공조, 시트, 선루프 상태가 시스템 시나리오에서 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_IVI_002 | HUD, AMP, TMU, 디지털 접근 서비스 상태가 시스템 시나리오에서 표시와 안내 정책에 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_ADAS_EXT_STATE_001 | SCC, 주차 보조, 주변 센서 상태가 시스템 시나리오에서 위험과 가용성 판단으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BACKBONE_STATE_001 | IBOX, SGW, DCM 등 경고 서비스 가용성 상태가 시스템 시나리오에서 전달 가용성과 강등 정책으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_EXT_PT_002 | OBC, DCDC, MCU, INVERTER 상태가 시스템 시나리오에서 구동 준비와 서비스 경고 맥락으로 일관되게 반영되는지 확인한다. | Ready |  |  |
| ST_BASE_001 | 차량 기본 기능과 주요 확장 상태가 시스템 수준에서 일관되게 동작하는지 확인한다. |  |  |  |
| ST_OEM_SURFACE_001 | 주요 Active Surface ECU의 경계, 소유권, 헬스 상태가 시스템 시나리오에서 일관되게 유지되는지 확인한다. | Planned |  |  |
| ST_OEM_PREMIUM_001 | Premium Option ECU가 기존 경고, 표시, 강건성 시나리오에 편입될 때 사용자 관찰 결과가 기존 요구를 위반하지 않는지 확인한다. (`NIGHT_VISION` 제외) | Planned |  |  |

---
