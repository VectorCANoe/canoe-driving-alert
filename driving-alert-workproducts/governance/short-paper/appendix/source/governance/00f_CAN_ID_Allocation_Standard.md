# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID
**Version**: 4.7
**Date**: 2026-03-09
**Status**: Draft (Submission Summary)
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05 -> 06 -> 07`

---

> 제출용 정리본: 현재 실행 기준인 11-bit CAN ID 규칙과 Ethernet/UDP 식별자 규칙을 분리해 정리한 문서입니다.

## 1. 현재 운영 구조

- 현재 개발 코드와 실행 환경은 CAN/CAN-stub 버스를 `11-bit CAN ID`로 통합 운영한다.
- 승용차 기준 대역폭, 지연, 운영 단순성을 고려해 현재 단계에서는 11-bit 체계를 유지한다.
- CAN 활성 운영 범위는 `0x100 ~ 0x2FF`이며, 현재 사용 범위는 `0x100 ~ 0x2AA`다.
- `0x000 ~ 0x0FF` 구간은 신규 할당하지 않는다.
- 진단 및 확장 기능을 위한 `29-bit` 구조는 별도 확장 설계로 검토 중이며, 현재 실행 기준에는 적용하지 않는다.

## 1-1. Ethernet 사전 정의 (나중에 이더넷 실 전환)

- CAN ID 제거 가능.
- 대신 아래를 필수 관리:
- 현재 `0x510`, `0x511`, `0x512`, `0x206`, `0xE100` 값은 CAN ID가 아니라 Ethernet/UDP 식별자로 관리한다.
- Protocol (UDP/TCP/SOME-IP/DoIP)
- Service/Event/Method ID (SOME-IP면)
- Src/Dst IP:Port
- PDU/Message Name
- Cycle/Timeout
- Gateway mapping (필요 시 CAN↔ETH 변환 규칙)

## 2. 목적

본 문서는 CAN 메시지의 ID 배정 원칙과 현재 운영 대역을 정리한다.
문서, DBC, 구현, 시험은 동일한 ID 기준을 사용한다.

## 3. 배정 원칙

- `우선순위`: 차량 거동과 직접 연결되는 제어/상태 메시지를 우선 배정한다.
- `도메인`: Chassis, Powertrain, Body, IVI, ADAS, Backbone 등 owner 도메인 기준으로 나눈다.
- `연속성`: 같은 도메인 메시지는 같은 대역 안에서 연번으로 관리한다.
- `확장성`: 신규 메시지를 위해 각 도메인별 예약 구간을 남겨 둔다.
- `동기화`: ID 변경 시 `0302`, `0303`, `0304`, `DBC`, `04`, `05~07`을 함께 갱신한다.

## 4. CAN Active ID 대역 (11-bit)

- `0x100 ~ 0x13F`: 차량 기본 상태, 조향, 제동, 동력 기본 루프, 대표 영역은 Chassis + Powertrain + 일부 Backbone
- `0x1C0 ~ 0x20F`: 긴급 알림, 위험 판단, 주행 보조 상태, 대표 영역은 ADAS + V2X
- `0x260 ~ 0x27F`: 출입, 조명, 공조, 실내 편의 상태, 대표 영역은 Body
- `0x280 ~ 0x29F`: 내비 문맥, 클러스터 표시, HMI 상태, 대표 영역은 IVI + CLU

## 4-1. Ethernet/UDP 식별자 운영 값

> 아래 값은 CAN ID가 아니라 Ethernet/UDP 식별자다.

- `0x510 ~ 0x512`: 차량 상태, 조향, 구간 문맥 전달용 UDP 식별자
- `0x206`: 최종 경고 결과 배포용 UDP 식별자, `Event + 50ms`
- `0xE100`: 긴급 알림 송수신용 UDP 식별자, `100ms`

## 5. 예약 구간 (식별자 정책)

- `0x500 ~ 0x50F`: Ethernet 경계 확장 예약, Ethernet/UDP 식별자
- `0x513 ~ 0x53F`: Backbone/CGW 확장 예약, Ethernet/UDP 식별자
- `0x700 ~ 0x7FF`: Validation/Diagnostic 확장 예약, CAN 11-bit

## 6. 배정 절차

1. 메시지의 Owner ECU와 도메인을 정한다.
2. CAN 메시지는 `0x100 ~ 0x2FF` 활성 대역에서 선택하고, Ethernet 메시지는 프로토콜 식별자 정책으로 관리한다.
3. 같은 도메인 안에서 중복 없이 다음 ID를 배정한다.
4. `0303`, `DBC`, 시험 문서까지 같은 ID로 맞춘다.

## 7. 운영 메모

- 제출 문서 기준에서는 현재 실행 중인 11-bit ID 체계를 사용한다.
- 29-bit 확장 정책은 진단 및 향후 확장 검토 항목으로 live SoT에서 별도로 관리한다.
- 신규 메시지는 기존 활성 대역과 예약 구간 충돌 여부를 먼저 확인한다.
