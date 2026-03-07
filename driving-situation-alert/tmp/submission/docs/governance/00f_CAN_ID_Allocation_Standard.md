# CAN ID 배정 표준

**Document ID**: PROJ-00F-CAN-ID  
**Version**: 3.7  
**Date**: 2026-03-07  
**Status**: Draft (Policy SoT)  
**Scope**: `0302 -> 0303 -> 0304 -> DBC -> 04 -> 05/06/07`

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 2. 핵심 원칙 (고정)

- 본 프로젝트는 `도메인 분리 구조`와 `3/3/5 ID 인코딩`을 **병행**한다.
- 정의:
  - 도메인 분리 = 네트워크/소유 경계(어느 DBC가 어떤 메시지를 소유하는가)
  - 3/3/5 = 11-bit CAN ID 번호체계(어떤 비트 의미로 ID를 배정하는가)
- 즉, 도메인 DBC 파일 분할은 유지하고, `BO_ ID`만 3/3/5 정책으로 재배정한다.

---

## 5. 3/3/5 사전

### 5.1 Tier 사전 (`[10:8]`)

| Tier | ID 대역 | 의미 | 우선순위 |
|---|---|---|---|
| 1 | `0x100~0x1FF` | 실시간 제어/핵심 상태 루프 | High |
| 2 | `0x200~0x2FF` | 출력/표시/Body/Validation 결과 | Medium |
| 3 | `0x300~0x3FF` | 파워트레인 확장/V2 Stub/진단 확장 | Low |
| 0,4~7 | 예약 | 미래 확장 | Reserved |

### 5.2 Group 사전 (`[7:5]`)

| Group | 의미 | 대표 ECU/기능 |
|---|---|---|
| 0 | Gateway/Boundary/Manager | `CHS_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` |
| 1 | Driver command + baseline state loop | `ACCEL_CTRL`, `BRK_CTRL`, `STEER_CTRL`, `ENG_CTRL`, `TCM`의 입력/요청/상태 핵심 프레임 |
| 2 | Chassis dynamics + actuator feedback | EPS/ABS/ESC/TCS/휠속/요레이트/조향각 등 동역학/제어반환 프레임 |
| 3 | Body comfort/control | `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` |
| 4 | IVI/Cluster/HMI context | `NAV_CTX_MGR`, `CLU_HMI_CTRL`, `CLU_BASE_CTRL` |
| 5 | Validation harness/result | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` |
| 6 | Emergency/V2 assist | `EMS_*`, `WARN_ARB_MGR` |
| 7 | Diag/Reserve | 진단/예약 |

- 해석 규칙: 메시지 이름에 `Diag`가 포함되어도 Group 7 강제 배정 사유가 되지 않는다.
- Group 결정은 `Owner/도메인 경계 -> 안전/검증 경로 -> Group 사전` 순서로 수행한다.

### 5.3 Index 사전 (`[4:0]`)

- 범위: `0~31`
- 규칙:
  - 동일 Tier/Group 내 Index 중복 금지
  - `31`은 기본 예약(예외는 변경승인 필요)

### 5.4 예외 규칙 (Legacy Stub/Transition)

- Tier `0`은 신규 할당 금지다.
- 전환 전 베이스라인의 저대역 ID(`0x064` 포함)는 `Old ID`로만 인정하며 Cutover 대상에 포함한다.
- 전환 완료 후 `0x000~0x0FF` 활성 운영 ID는 0건이어야 한다.
- 논리 Ethernet ID(`0xE1xx/0xE2xx`)는 CAN 11-bit 3/3/5 대상이 아니다.
- `E213~E216`(`Comm_130~Comm_133`)은 Pre-Activation Ethernet 논리 ID이며, `ETH_INTERFACE_CONTRACT.md v1.2` 반영 전에는 활성 계약으로 취급하지 않는다.

### 5.5 11-bit 유지/29-bit 전환 기준 (운영 디펜스)

- 현재 정책:
  - 본 프로젝트는 CAN ID를 11-bit 3/3/5 체계로 운영한다.
  - 29-bit(Extended)는 현재 단계에서 필수 전환 항목이 아니다.
- 11-bit 유지 조건:
  - Tier/Group 내 Index 충돌 없이 신규 배정이 가능하다.
  - 도메인 분리/우선순위 정책 설명이 11-bit 체계에서 충분히 가능하다.
- 29-bit 전환 트리거(권고):
  - 특정 Tier/Group 슬롯 점유율이 높아 신규 배정 여유가 부족할 때
  - 11-bit 공간에서 진단/확장 기능 충돌을 해소하기 어려울 때
  - 외부 인터페이스 요구로 Extended ID가 필요해질 때
- 전환 원칙:
  - 정책(00f) -> 매핑표(Annex A) -> DBC/코드 -> 테스트 문서 순으로 단계 적용한다.
  - 전환 전까지는 11-bit 운영을 유지하고, 29-bit는 확장 대응 옵션으로 관리한다.

---

## 7. 현행 베이스라인 (전환 전 스냅샷)

- 현행 구조: 도메인 블록 대역형
- 메시지 수: `98`
- ID 범위(신규 3/3/5 배치 결과): `0x100 ~ 0x2AA`
- Old baseline 참고 범위(전환 전): `0x064 ~ 0x315`
- 중복: `0건`
- 대표 블록:
  - `0x100~0x2A6` Chassis
  - `0x260~0x277` Body
  - `0x280~0x2A7` Infotainment
  - `0x109~0x2AA` Powertrain
  - `0x111~0x1C4` ADAS + ETH Stub

---
