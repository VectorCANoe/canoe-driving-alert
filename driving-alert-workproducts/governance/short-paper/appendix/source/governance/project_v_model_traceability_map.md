# 프로젝트 V-모델 및 추적 구조

## 1. 목적

본 문서는 주행 상황 실시간 경고 시스템 프로젝트의 개발 문서와 검증 문서가 실제 V-모델 구조 안에서 어떻게 대응되는지를 reviewer-facing 형식으로 정리한 별첨이다.

본 프로젝트는 CANoe SIL 기반 구현형 프로젝트로, ASPICE 전체 산출물을 모두 독립 문서로 분리하지는 않았다. 대신 `01 -> 03 -> 0301 -> 0302 -> 0303 -> 0304 -> 04 -> 05 -> 06 -> 07` 문서 체인을 실행 가능한 기준선으로 유지하고, `00d_HARA_Worksheet`와 `00g_Master_Test_Matrix`를 통해 안전성 및 추적성을 고정하였다.

## 2. 프로젝트 V-모델 해석

- 좌측 개발 축은 요구사항, 시스템 설계, 통신/변수 계약, CAPL 구현 순으로 구성하였다.
- 우측 검증 축은 단위시험, 통합시험, 시스템시험 순으로 구성하였다.
- `00d_HARA_Worksheet`는 안전 사건과 검증 우선순위의 기준점으로 사용하였다.
- `00g_Master_Test_Matrix`는 요구사항, 기능, 시험 자산을 연결하는 프로젝트 Test Matrix로 사용하였다.

## 3. V-모델 매핑 표

- 안전 / 추적성 기준
  - standard: `SYS.2`, `SUP.10` / Part 3, Part 8
  - project docs: `00d_HARA_Worksheet`, `00g_Master_Test_Matrix`
  - verification link: `05`, `06`, `07` 전 계층
- 시스템 요구사항
  - standard: `SYS.2` / Part 4, Cl.6
  - project docs: `01_Requirements`
  - verification link: `07_System_Test`
- 시스템 설계
  - standard: `SYS.3` / Part 4, Cl.7
  - project docs: `03`, `0301`, `0302`
  - verification link: `06`, `07`
- 통신 / 변수 계약
  - standard: `SWE.2`, `SWE.3` / Part 6, Cl.7~8
  - project docs: `0303`, `0304`
  - verification link: `05`, `06`
- 구현 기준선
  - standard: `SWE.3` / Part 6, Cl.9
  - project docs: `04_SW_Implementation`
  - verification link: `05`, `06`
- 단위 검증
  - standard: `SWE.4` / Part 6, Cl.9
  - project docs: `05_Unit_Test`
  - verification link: `0303`, `0304`, `04`
- 통합 검증
  - standard: `SWE.5` / Part 6, Cl.10
  - project docs: `06_Integration_Test`
  - verification link: `03`, `0301`, `0302`, `0303`, `0304`
- 시스템 검증
  - standard: `SYS.5` / Part 4, Cl.10
  - project docs: `07_System_Test`
  - verification link: `01_Requirements`, `00d_HARA_Worksheet`

표 1의 각 행은 아래 의미를 갖는다.

- `00d_HARA_Worksheet`는 위험 사건과 안전 우선순위의 기준점이다.
- `00g_Master_Test_Matrix`는 요구사항, 기능, 시험 자산을 연결하는 프로젝트 Test Matrix이다.
- `03`, `0301`, `0302`는 ECU 역할, 기능 분해, 네트워크 흐름을 담당하는 시스템 설계 축이다.
- `0303`, `0304`는 실행 가능한 통신/변수 계약을 정의하는 인터페이스 축이다.
- `04_SW_Implementation`은 CAPL, panel, sysvar를 포함한 구현 기준선이다.

## 4. 프로젝트 추적성 체인

본 프로젝트의 추적성 체인은 아래 순서로 고정하였다.

`Req -> Func -> Flow -> Comm -> Var -> Code -> Unit Test -> Integration Test -> System Test`

이 체인은 다음 의미를 갖는다.

- `Req`: 시스템 요구사항 기준선
- `Func / Flow`: 기능 책임과 ECU 간 흐름
- `Comm / Var`: 통신 및 상태 관측 계약
- `Code`: CAPL 구현 기준선
- `Unit / Integration / System Test`: 검증 계층별 판정 기준

## 5. 작성 기준

- 본 매핑은 현재 active baseline 문서를 기준으로 정리하였다.
- 별도 `SWE.1` 독립 문서는 두지 않고, 기능 정의와 통신/변수 계약 문서가 소프트웨어 요구/설계 역할을 분담하도록 구성하였다.
- 따라서 본 프로젝트의 V-모델은 이론적 완전 분리형이 아니라, CANoe SIL 구현 프로젝트에 맞춘 실행형 추적 구조로 해석한다.
