# Runtime Skeleton

원문:
- [../../architecture/skeleton.md](../../architecture/skeleton.md)

동기화 기준:
- `5d83ee7f`
- asset path, folder 이름, harness identifier는 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 active CANoe baseline의 planned runtime skeleton을 설명합니다.
> runtime, diagnostic, verification 구현이 계속 고정되는 단계이므로 일부 세부사항은 바뀔 수 있습니다.

## 목적

이 문서는 active CANoe baseline이 어떤 runtime skeleton을 목표 구조로 삼고 있는지 설명합니다.

## 범위

다음 항목을 포함합니다.

- input surface
- runtime layer
- transport seam
- test-harness placement
- evidence handoff point

## Target structure

1. Surface layer
- `project/panel/`, `project/sysvars/` 아래의 panel / system-variable input
- SIL execution용 scenario control input

2. Runtime layer
- `src/capl/` 아래 CAPL source of truth
- `cfg/channel_assign/` 아래 GUI import mirror
- input을 정규화하고 alert state를 계산하는 domain logic

3. Contract layer
- active DBC set의 domain CAN contract
- cross-domain delivery와 health signaling을 위한 Ethernet backbone seam
- stable panel seam과 diagnostic observation seam

4. Verification layer
- `TEST_SCN` 기반 scenario orchestration
- `TEST_BAS` 기반 baseline aggregation
- UT/IT 증명을 위한 native CANoe Test Unit asset
- verdict, log, report, screenshot output을 통한 evidence capture

## Runtime block

| Block | 역할 | 주요 자산 |
| --- | --- | --- |
| Input capture | panel, sysvar, domain CAN, Ethernet context를 수집 | `project/panel/`, `project/sysvars/`, CAPL input handler |
| Normalization | raw signal을 stable runtime state로 변환 | `src/capl/logic/`, domain ECU logic |
| Boundary authority | cross-domain ownership, route, timeout, health rule 적용 | `CGW`, boundary-state logic, route contract |
| Alert decision | selected alert, clear, fail-safe outcome 계산 | core alert logic, arbitration logic |
| Output publish | CAN, Ethernet, panel-readable status를 publish | domain ECU publisher, Ethernet helper, SysVar mirror |
| Verification harness | scenario 구동, verdict 집계, evidence seam 준비 | `TEST_SCN`, `TEST_BAS`, native Test Unit asset |

## 설계 규칙

- business semantics와 transport를 분리합니다
- `src/capl/`를 source of truth로 두고 `cfg/channel_assign/`는 GUI mirror로 유지합니다
- reviewer-facing seam은 stable contract와 SysVar로 읽기 쉽게 유지합니다
- verdict logic을 transport handler 안에 숨기지 말고 harness logic을 명시적으로 유지합니다

## 현재 개발 메모

위 skeleton은 현재 CANoe baseline이 목표로 하는 operating shape입니다.

특정 ECU path나 test harness asset이 아직 구현 중이라면, 이 구조는 final implementation detail의 보장이라기보다 expected integration direction으로 해석해야 합니다.
