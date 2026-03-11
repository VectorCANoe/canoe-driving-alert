# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.24
**Date**: 2026-03-11
**Status**: Draft (Submission Summary)
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 하단 (SWE.3) | `04_SW_Implementation.md` | `0304_System_Variables.md` | `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

## 1. 문서 목적

본 문서는 현재 CANoe SIL 구현이 도메인 단위로 어떻게 구성되어 있는지 간략히 정리한다.
세부 CAPL 함수나 내부 보조 모듈 설명보다, 각 도메인이 어떤 역할을 담당하고 어떤 ECU군으로 구현되었는지를 우선 설명한다.

## 2. 구현 단위 명세 (공식 표준 양식)

| 구현 모듈 | 기능 상세 | 비고 |
|---|---|---|
| Backbone / Gateway | `CGW`, `ETHB`, `SGW`, `DCM`, `IBOX`를 중심으로 도메인 경계 통신, 진단 경계, 백본 서비스 기능을 수행한다. | 중앙 경계 및 서비스 계층 |
| Powertrain Domain | `EMS`, `TCU`, `VCU`와 전동화·동력 계열 ECU가 동력 상태와 차량 기초 상태를 생성하고, 필요한 상태를 다른 도메인에 전달한다. | 동력 및 차량 상태 계층 |
| Chassis Domain | `ESC`, `MDPS`와 제동·조향·차체 안정화 ECU가 주행 제어 상태를 생성하고 위험 판단 입력을 제공한다. | 주행 동역학 계층 |
| Body Domain | `BCM`, `DATC`, `SMK`, `AFLS`와 바디·편의 ECU가 실내/차체 상태를 생성하고 앰비언트 출력 및 차체 상태 연동 기능을 담당한다. | 차체 및 편의 계층 |
| IVI / HMI Domain | `IVI`, `CLU`, `TMU`와 표시·안내 ECU가 경고 문구, 기본 표시, 안내 정보를 운전자 인터페이스에 반영한다. | 표시 및 안내 계층 |
| ADAS / V2X Domain | `ADAS`, `SCC`, `V2X`와 센서·주행보조 ECU가 객체 위험, 주행 위험, 긴급차량 접근 정보를 바탕으로 경고 판단 입력을 생성한다. | 위험 판단 입력 계층 |
| Validation Harness | `TEST_SCN`, `TEST_BAS`가 검증 시나리오 실행과 결과 집계를 담당하며 제품 ECU와 분리된 검증 계층으로 동작한다. | 검증 전용 계층 |

## 3. 도메인 구현 해석 포인트

| 구분 | 설명 |
|---|---|
| 중앙 구조 | 도메인 간 통신은 Backbone / Gateway 계층을 통해 연결되며, 제품 ECU와 검증 ECU를 분리해 구성한다. |
| 제품 ECU 구조 | 주요 제품 기능은 Powertrain, Chassis, Body, IVI/HMI, ADAS/V2X 도메인으로 나누어 구현한다. |
| 표시 구조 | 최종 경고는 Cluster와 Ambient 중심으로 반영되며, IVI/HMI 및 Body 도메인이 출력 역할을 맡는다. |
| 확장 구조 | Leaf ECU는 도메인 내부 상태 생성 역할을 맡고, Domain Controller/Anchor ECU가 주요 상태를 대표한다. |
| 검증 구조 | TEST_SCN과 TEST_BAS는 제품 기능 구현과 분리된 검증 전용 단위로 유지한다. |

## 4. 도메인 그림 구성 원칙

- 최종 제출본에서는 각 도메인별 대표 화면 또는 구조 그림을 1장씩 배치한다.
- 그림은 내부 CAPL 함수나 helper 명칭이 아니라 도메인 역할과 ECU 구성을 보여주는 수준으로 유지한다.
- Backbone / Gateway, Powertrain, Chassis, Body, IVI / HMI, ADAS / V2X, Validation Harness 순서로 배치한다.
- 각 그림 하단에는 해당 도메인이 생성하는 상태와 전달 대상만 짧게 기술한다.
