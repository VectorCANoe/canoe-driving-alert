# Changelog

All notable changes to the CANoe-IVI-OTA project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- CAPL 노드 개발: `BCM_Sim.can`, `CGW_Sim.can`, `Tester_Sim.can`, `OTA_Server_Sim.can`
- CANoe 시뮬레이션 실행 및 검증

## [1.2.0] - 2026-02-18

### Changed
- `Concept_design.drawio` 페이지 구조 재편 (7페이지 체계)
  - `REF_ConceptDesignOverview` — 개요 참조
  - `REF_CANBusPrinciple` — CAN 원리 참조
  - `SYS3_VHA_VehicleArchitecture` — 전체 차량 아키텍처 (92 cells)
  - `SYS3_CBD_SystemFunctionalBlock` — 도메인별 기능 블록 I-C-O (67 cells)
  - `SYS3_FBD_FunctionalBlockDiagram` — 서비스별 기능 블록 I-C-O (47 cells)
  - `SYS3_NET_CANBusTopology` — CAN 버스 토폴로지 (53 cells)
  - `SYS3_SIG_E2EServiceFlow` — E2E 서비스 흐름 (39 cells)
- 페이지 명명 규칙을 V-Model SYS.3 산출물 기준으로 정렬
- `pages` 속성 6→7 수정 (diagram 수와 일치)

## [1.1.0] - 2026-02-13

### Added
- V-Model 문서 체계 46개 완성 (ISO 26262 / ASPICE)
  - 요구사항 SRS: REQ-F/G/D/O/A/N 6-Group 체계 (40개 REQ)
  - HARA v3.0: H-01~H-10 위험, SG-01~SG-09 Safety Goals
  - Safety Validation Report v2.1: SG-05~SG-09 검증 섹션
  - Traceability Matrix, System Qualification Test Plan, Safety Validation Plan
- `Concept_design.drawio` 초기 생성 (6페이지)

### Fixed
- DBC 충돌 해결
  - `BCM_DoorStatus` → **0x501** (1281)로 이동
  - `BCM_FaultStatus` → **0x500** (1280) 신규 정의 (10ms, ASIL-B)
    - Signals: `WindowMotorOvercurrent`, `DTC_Code`, `FaultSeverity`, `AliveCounter`, `Checksum`
  - `vECU_WarningUI` → **0x420** (1056) 신규 정의 (50ms, ASIL-D)
    - Signals: `Warning_Type`, `Warning_Priority`, `Icon_ID`, `Warning_Active`

## [1.0.0] - 2026-02-05

### Added
- Initial project structure with ISO 26262 and ASPICE compliance
- Safety management framework
- Requirements management system
- Architecture documentation structure
- IVI module implementation framework
  - HVAC control structure
  - Window control structure
  - Seat control structure
- UX Lighting modules
  - Ambient lighting control (RGB, zones, scenes)
  - Dashboard lighting control (adaptive brightness)
  - ADAS integration lighting
  - Parking assist lighting
- Diagnostics modules
  - BDC fault injection framework
  - UDS diagnostic services structure
  - OTA update mechanism with vVIRTUALtarget
- Verification and validation framework
- Quality assurance structure
- Configuration management system
- CANoe simulation configurations
- Comprehensive documentation
