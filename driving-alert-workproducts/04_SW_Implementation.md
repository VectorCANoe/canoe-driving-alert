# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.26
**Date**: 2026-03-17
**Status**: Draft (Submission Summary)
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 하단 (SWE.3) | `04_SW_Implementation.md` | `0304_System_Variables.md` | `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

## 1. 문서 목적

본 문서는 현재 구현된 소프트웨어 구성을 기능 계층 단위로 설명한다.
제출본에서는 내부 함수 단위 상세보다 각 계층의 역할과 ECU 구현 범위를 중심으로 제시한다.

## 2. 구현 단위 명세 (공식 표준 양식)

| 구현 모듈 | 기능 상세 | 비고 |
|---|---|---|
| Gateway / Service Bridge | `CGW`, `ETHB`, `SGW`, `DCM`, `IBOX`가 경고 정보 전달 경계 통신과 서비스 연계 기능을 담당한다. | 중앙 경계 계층 |
| Diagnostic Observation Surface | `EXT_DIAG`가 차량 서비스, 보안, 진단 상태를 외부 진단 관측면으로 제공한다. | 진단 관측 계층 |
| Powertrain Layer | `EMS`, `TCU`, `VCU`와 동력 계열 ECU가 동력 상태와 차량 기초 상태를 생성한다. | 동력 상태 계층 |
| Chassis Layer | `ESC`, `MDPS`와 제동/조향 계열 ECU가 주행 제어 상태를 생성한다. | 주행 제어 계층 |
| Body Layer | `BCM`, `DATC`, `SMK`, `AFLS`와 바디 ECU가 차체/실내 상태와 앰비언트 출력을 담당한다. | 차체/편의 계층 |
| IVI / HMI Layer | `IVI`, `CLU`, `TMU`가 경고 문구, 기본 표시, 안내 정보를 운전자 인터페이스에 반영한다. | 표시/안내 계층 |
| ADAS / V2X Layer | `ADAS`, `SCC`, `V2X`와 센서 계열 ECU가 위험 판단 입력을 생성한다. | 위험 판단 계층 |
| Validation Harness | `TEST_SCN`은 검증 시나리오 실행과 입력 자극을 담당하고 `TEST_BAS`는 관측 결과와 baseline 판정을 집계한다. 실제 경고 의미, freshness 유지, 최종 출력 판단은 기능 ECU가 소유하며 하네스는 이를 대신 생성하지 않는다. | 검증 전용 계층 |

## 3. 설계 규칙

| 규칙 | 내용 |
|---|---|
| 계층 분리 | 제품 ECU 계층과 검증 ECU 계층을 분리하여 운영한다. |
| 전달 경계 | 내부 처리는 CAN 중심으로 유지하고, ECU 간 전달은 경계 게이트웨이 경로를 사용한다. |
| 출력 일관성 | 최종 경고는 클러스터와 앰비언트 채널에 일관되게 반영한다. |
| 추적 연계 | 구현 내용은 `0304` 변수 정의 및 `05~07` 시험 문서와 동일 기준으로 연계한다. |
