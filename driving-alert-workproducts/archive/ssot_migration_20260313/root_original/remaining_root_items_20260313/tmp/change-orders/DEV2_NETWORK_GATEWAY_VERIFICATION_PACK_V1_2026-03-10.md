# Dev2 Network/Gateway Verification Pack V1

- Date: 2026-03-10
- Owner: Dev2
- Status: `Design Baseline`
- Purpose:
  - define a separate OEM-style network/gateway verification pack
  - keep it distinct from the 6-asset functional warning portfolio

## 1. Decision

- Keep `Native Functional Portfolio 6` unchanged.
- Create a separate `Network/Gateway Verification Pack`.
- Recommended pack structure for the current cycle:
  - `4` core assets
  - `1` diagnostic routing draft asset

## 2. Why Separate It

The 6 functional assets prove product value:

- school-zone warning
- emergency ETA priority
- timeout clear
- fail-safe downgrade
- decel/warning sync
- ADAS object-risk path

Network/gateway tests prove infrastructure quality:

- CAN bus priority behavior
- route forwarding integrity
- timeout/stale handling at path level
- load/period/jitter stability

These should not be mixed into one reviewer-facing set.

## 3. Why `4` Is the Right Count Now

For the current reset stage, `4` core assets are enough to cover the representative infrastructure axes:

1. CAN bus arbitration / ID priority
2. gateway route forwarding integrity
3. stale/timeout path behavior
4. bus/load timing stability

Diagnostic routing is important, but it is still moving with Dev1/runtime ownership work.
Therefore:

- keep the mandatory pack at `4`
- allow `1` diagnostic routing draft slot in parallel

## 4. Recommended Pack

| Asset ID | Level | Category | Primary Intent | Current Recommendation |
|---|---|---|---|---|
| `TC_CANOE_NET_001_CAN_BUS_ARBITRATION_PRIORITY` | IT | CAN protocol | lower CAN ID wins under contention | Include now |
| `TC_CANOE_NET_002_GW_ROUTE_FORWARDING_INTEGRITY` | IT | Gateway | ETH/CAN-stub to domain path forwards expected payload without illegal mutation | Include now |
| `TC_CANOE_NET_003_TIMEOUT_STALE_CHAIN_CLEAR` | IT | Robustness | path stale/timeout leads to safe clear / no illegal residue | Include now |
| `TC_CANOE_NET_004_LOAD_PERIOD_JITTER_STABILITY` | IT | Timing/load | key messages keep expected period/jitter under burst/load condition | Include now |
| `TC_CANOE_NET_005_DIAG_ROUTE_INTEGRITY` | IT | Diagnostic gateway | diagnostic request/response routing stays owner-safe and traceable | Draft include |

## 5. Out of Scope for V1

Do not force these into mandatory V1 gate yet:

- security/authentication channel verification
- physical hardware transceiver behavior

Reason:

- diagnostic routing is allowed as `draft`, but not yet mandatory for V1 gate close
- security/hardware scope is not stable in current SIL baseline

## 6. Detailed Design

### 6.1 `TC_CANOE_NET_001_CAN_BUS_ARBITRATION_PRIORITY`

- Level: `IT`
- Primary intent:
  - verify actual `CAN bus arbitration` behavior under message contention
- Scope:
  - network/protocol only
  - not a warning priority decision test
- Stimulus:
  1. schedule simultaneous transmit opportunity for at least two CAN frames
  2. configure one lower-ID frame and one higher-ID frame
  3. observe bus winner and loser retry behavior
- Oracle:
  - lower numeric CAN ID wins arbitration
  - higher numeric CAN ID is delayed/retried without corruption
  - no illegal frame mutation
- Timing / evidence:
  - trace capture with arbitration order proof
  - optional bus statistics snapshot

### 6.2 `TC_CANOE_NET_002_GW_ROUTE_FORWARDING_INTEGRITY`

- Level: `IT`
- Primary intent:
  - verify gateway forwarding across backbone/domain boundary
- Scope:
  - ETH backbone / CAN-stub / domain CAN path
- Stimulus:
  1. inject known payload from source side
  2. trigger route through gateway path
  3. observe target-side message or sysvar reflection
- Oracle:
  - expected payload fields are forwarded
  - no illegal owner swap
  - no forbidden field mutation
  - route health remains valid in nominal case
- Timing / evidence:
  - source frame timestamp
  - target frame timestamp
  - forwarding latency summary

### 6.3 `TC_CANOE_NET_003_TIMEOUT_STALE_CHAIN_CLEAR`

- Level: `IT`
- Primary intent:
  - verify stale/timeout at transport/path level leads to safe clear behavior
- Scope:
  - path health, stale detection, clear action
- Stimulus:
  1. establish nominal path
  2. stop or pause upstream updates
  3. wait through timeout window
  4. observe downstream clear/downgrade
- Oracle:
  - stale or timeout is detected at configured threshold
  - clear/downgrade happens once
  - no oscillation or duplicate flip-flop
- Timing / evidence:
  - timeout threshold proof
  - clear transition proof
  - relevant path-health variables

### 6.4 `TC_CANOE_NET_004_LOAD_PERIOD_JITTER_STABILITY`

- Level: `IT`
- Primary intent:
  - verify key network channels remain within expected period/jitter bounds under load
- Scope:
  - representative key frames only
  - not full stress/performance certification
- Stimulus:
  1. apply burst or repeated transmit load
  2. keep target key frames active
  3. capture actual periods
- Oracle:
  - representative key frames stay within configured period tolerance
  - no unexpected starvation on required channels
  - no uncontrolled jitter growth beyond allowed threshold
- Timing / evidence:
  - trace-derived period/jitter summary
  - bus statistics / message timing table

### 6.5 `TC_CANOE_NET_005_DIAG_ROUTE_INTEGRITY` (Draft)

- Level: `IT`
- Status: `Draft / Pre-Gate`
- Primary intent:
  - verify diagnostic request/response routing is preserved across the intended path
- Scope:
  - diagnostic transport ownership
  - request/response direction
  - owner-safe routing
- Stimulus:
  1. inject representative diagnostic request on source side
  2. trigger routing across the intended gateway path
  3. observe routed request and matching response on target side
- Oracle:
  - request reaches intended target route
  - response returns through intended route
  - no illegal payload mutation
  - no wrong-surface ownership leakage
  - timeout/failure path is reported correctly when route is unavailable
- Timing / evidence:
  - request timestamp
  - response timestamp
  - route path summary
  - diagnostic trace capture

## 7. OEM-Oriented Recommendation

For this project, use:

1. `Functional Portfolio 6`
2. `Network/Gateway Verification Pack 4`
3. `Diagnostic Routing Draft 1`

This is balanced:

- functional value is clearly visible
- network/protocol quality is explicitly covered
- diagnostic routing can start early without forcing unstable criteria into the mandatory gate
- native asset count stays controlled

## 8. Future Extension Rule

After Dev1 finalizes diagnostic surface and route ownership, promote:

- `TC_CANOE_NET_005_DIAG_ROUTE_INTEGRITY`

from `draft` to `mandatory network pack` status.
