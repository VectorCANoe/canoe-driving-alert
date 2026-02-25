# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**Version**: 2.0
**Date**: 2026-02-25

| 노드 | 분류 | 기능명 | 기능설명 |
|------|------|--------|---------|
| Panel | 입력 | 구간 컨텍스트 입력 | gRoadZone / gNavDirection / gZoneDistance 설정 |
| Panel | 입력 | 경찰 알림 송신 | Police AlertActive/ETA/Direction 입력 |
| Panel | 입력 | 구급차 알림 송신 | Ambulance AlertActive/ETA/Direction 입력 |
| Context_Manager | ECU 동작 | 컨텍스트 계산 | 구간 정보 기반 기본 Ambient 패턴 계산 |
| Police_Node | ECU 동작 | 긴급 알림 송신 | ETH_EmergencyAlert(EmergencyType=Police) 브로드캐스트 |
| Ambulance_Node | ECU 동작 | 긴급 알림 송신 | ETH_EmergencyAlert(EmergencyType=Ambulance) 브로드캐스트 |
| Civ_Node | ECU 동작 | 알림 수신/중재 | 다중 긴급 알림 수신 후 우선순위/충돌해결 수행 |
| Arbiter | ECU 동작 | 우선순위 결정 | Emergency > Context, Ambulance > Police, ETA/SourceID tie-break |
| Ambient_ECU | ECU 동작 | 최종 패턴 출력 | Arbiter 선택 결과를 시각 패턴으로 반영 |
| Cluster_ECU | ECU 동작 | 텍스트 경고 출력 | "긴급차량 접근" 메시지 및 타입/방향 표시 |
| Panel | 출력 | 중재 결과 표시 | SelectedSource, ActiveMode, ReasonCode Indicator |
