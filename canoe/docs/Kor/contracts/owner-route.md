# Owner / Bus / Timeout / Route Contract

원문:
- [../../contracts/owner-route.md](../../contracts/owner-route.md)

동기화 기준:
- `5d83ee7f`
- seam 이름, owner, bus 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> runtime, diagnostic, verification 세부사항 가운데 일부는 아직 구현 중이며 변경될 수 있습니다.

## 목적

이 문서는 주요 runtime seam마다 누가 owner인지, 어떤 bus가 적용되는지, 그리고 timeout authority와 route authority가 누구인지 정의합니다.

## 계약 차원

| 차원 | 의미 |
| --- | --- |
| Owner | 해당 seam의 business meaning을 소유하는 runtime authority |
| Bus | active baseline에서 사용하는 primary transport 또는 observation seam |
| Timeout authority | stale-state, clear, fail-safe 동작을 결정하는 runtime authority |
| Route authority | cross-domain delivery와 forwarding을 제어하는 runtime authority |

## 규칙

- 하나의 logical seam은 하나의 explicit owner를 가져야 합니다
- cross-domain forwarding이 개입되면 owner와 route authority는 달라질 수 있습니다
- timeout 및 clear 동작은 transport만으로 추정하지 말고 명시적으로 정의해야 합니다
- foreign-domain CAN visibility는 `contracts/multibus-policy.md`를 따릅니다
- 상세 frame-level ownership은 `contracts/communication-matrix.md`에서 관리합니다

## 현재 seam 표

| Seam | Owner | Primary bus | Timeout authority | Route authority | 비고 |
| --- | --- | --- | --- | --- | --- |
| Navigation context | `IVI` | Infotainment CAN | `IVI` | `CGW` when cross-domain delivery is required | road zone, direction, distance, speed-limit context |
| Emergency context | `V2X` | Ethernet backbone | `CGW` boundary authority | `CGW` | emergency source, direction, ETA, active/clear context |
| Arbitration result | core alert runtime | local runtime + published output seam | core alert runtime | `CGW` for cross-domain forwarding | selected alert level/type and clear behavior |
| Boundary health | `CGW` | Ethernet backbone | `CGW` | `CGW` | fail-safe and cross-domain health summary |
| Scenario result | `TEST_SCN` | test harness seam | `TEST_SCN` | none | per-scenario verdict and trace anchor |
| Baseline result | `TEST_BAS` | SysVar-only seam | `TEST_BAS` | none | aggregate baseline verdict and health summary |

## 사용 규칙

seam-level authority 판단은 이 문서를 기준으로 합니다.
frame-level ownership을 확인할 때는 `contracts/communication-matrix.md`를 사용합니다.

## 개발 메모

위 seam 표는 active baseline의 현재 계획 계약입니다.
개발 중 seam의 transport 또는 ownership이 바뀌면, 그 변경을 공식으로 취급하기 전에 먼저 이 문서를 갱신해야 합니다.