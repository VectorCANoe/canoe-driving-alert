<div align="center">

# canoe-driving-alert

### 현대모비스 부트캠프와 Vector Korea와 함께 진행한 CAN Communication Project

CANoe SIL 기반 주행 경고 시스템을 설계하고, 검증하고, 리뷰하기 위한 공개 엔지니어링 저장소입니다.

![CANoe SIL](https://img.shields.io/badge/CANoe-SIL-0A5C36?style=flat-square)
![Transport](https://img.shields.io/badge/CAN%20%2B%20Ethernet-Communication-004A7C?style=flat-square)
![Traceability](https://img.shields.io/badge/V--Cycle-Traceability-6B4EFF?style=flat-square)
![C CAPL](https://img.shields.io/badge/C%20%2F%20CAPL-Runtime-5A3E85?style=flat-square)
![Python](https://img.shields.io/badge/Python-Tooling-3776AB?style=flat-square)

[English](README.md) | [한국어](README.ko.md)

</div>

<p align="center">
  <strong>Hyundai Mobis Bootcamp</strong> · <strong>Vector Korea</strong>
</p>

<p align="center">
  <a href="#overview"><strong>Overview</strong></a> ·
  <a href="#highlights"><strong>Highlights</strong></a> ·
  <a href="#system-overview"><strong>System Overview</strong></a> ·
  <a href="#quick-start"><strong>Quick Start</strong></a> ·
  <a href="#repository-map"><strong>Repository Map</strong></a>
</p>

<details>
<summary><strong>프로젝트 배경</strong></summary>

이 프로젝트는 현대모비스 부트캠프와 Vector Korea 협업 맥락에서 진행되었습니다.
저장소는 통신 설계, CANoe 런타임 자산, 추적 가능한 워크프로덕트, 검증 툴링을 하나의 공개 엔지니어링 표면으로 연결하도록 구성되어 있습니다.

</details>

<details>
<summary><strong>주요 레퍼런스</strong></summary>

- Vector CANoe 문서와 샘플 구성
- Automotive SPICE PAM 3.1
- ISO 26262
- AUTOSAR Classic Platform SWC Modeling Guide
- 워크프로덕트 구조와 리뷰 형식을 정리할 때 참고한 project-result review sample

</details>

---

## Overview

대부분의 CAN 통신 프로젝트 저장소는 런타임 자산, 코드, 테스트 산출 중 한 층만 보여줍니다.

이 저장소는 아래 전체 엔지니어링 흐름을 한 번에 보여주는 것을 목표로 합니다.

- 통신 설계
- CANoe 런타임 구현
- V-cycle 워크프로덕트
- 검증 실행과 리뷰 툴링

## Highlights

- CANoe SIL 기반 CAN + Ethernet 통신 모델링
- 요구사항부터 검증까지 이어지는 추적성
- 리뷰 워크플로우를 위한 product surface 포함
- gate, quality, release 지원을 위한 공용 자동화 스크립트

## System Overview

```mermaid
flowchart LR
    A[Requirements] --> B[Functional Definition]
    B --> C[Network Flow]
    C --> D[Communication Specification]
    D --> E[System Variables]
    E --> F[CANoe Runtime and CAPL]
    F --> G[UT / IT / ST]
    G --> H[Evidence and Review]
```

## System flow

```text
Requirements
  -> Functional Definition
  -> Network Flow
  -> Communication Specification
  -> System Variables
  -> CANoe Runtime and CAPL
  -> Unit / Integration / System Verification
```

## Quick start

```powershell
python scripts/run.py
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

## Repository map

| 경로 | 설명 |
| --- | --- |
| [`canoe/`](canoe/) | CANoe 런타임 프로젝트, 설정, CAPL 소스, 계약 문서, 검증 문서 |
| [`driving-alert-workproducts/`](driving-alert-workproducts/) | 정본 워크프로덕트와 추적 가능한 엔지니어링 문서 |
| [`product/`](product/) | 운영자 관점의 product surface와 리뷰 자산 |
| [`scripts/`](scripts/) | 공용 실행기, gate, quality tooling, release helper |

## Start here

- [`canoe/README.md`](canoe/README.md)
- [`product/sdv_operator/README.md`](product/sdv_operator/README.md)
- [`product/sdv_operator/docs-src/index.md`](product/sdv_operator/docs-src/index.md)

## Contributing

기여 방법은 [`CONTRIBUTING.md`](CONTRIBUTING.md) 를 참고하면 됩니다.

## Core architecture and ECU maps

아키텍처가 왜 이렇게 나뉘었는지, ECU별 역할과 런타임 소유권이 어떻게 정리되어 있는지, 검증 체계가 어떤 기준으로 묶여 있는지 보려면 아래 문서부터 읽는 것이 가장 빠릅니다.

- [Surface Map](canoe/docs/architecture/11_SURFACE_RUNTIME_VERIFICATION_MAP.md)
- [ECU Ownership](canoe/docs/contracts/11_RUNTIME_MESSAGE_OWNERSHIP_MATRIX.md)
- [Multibus Policy](canoe/docs/contracts/12_RUNTIME_MULTIBUS_VISIBILITY_POLICY.md)
- [Ethernet Contract](canoe/docs/contracts/13_ETH_INTERFACE_CONTRACT.md)
- [Panel and SysVar Binding](canoe/docs/contracts/17_PANEL_SYSVAR_BINDING_CONTRACT.md)
- [Verification Evidence](canoe/docs/verification/23_VERIFICATION_EVIDENCE_LOG_STANDARD.md)
