## OEM Placeholder Wave 1 (2026-03-09)

This wave materializes the OEM breadth target as compile-safe CAPL surface nodes.

Current visible target:

- deep runtime anchors: `13`
- validation anchors: `2`
- shallow surface placeholders: `87`
- total visible CAPL nodes: `100`

Execution rule:

- deep runtime anchors keep current ownership and logic
- shallow placeholders expose OEM surface names only
- no internal module names are surfaced in this wave
- later promotion replaces placeholder bodies with real runtime logic

### Domain Distribution

| Domain | Deep anchors | Placeholder nodes | Total visible nodes |
| --- | --- | --- | --- |
| `ETH_Backbone` | `3` | `5` | `8` |
| `Powertrain` | `2` | `12` | `14` |
| `Chassis` | `4` | `12` | `16` |
| `Body` | `1` | `22` | `23` |
| `Infotainment` | `2` | `11` | `13` |
| `ADAS` | `1` | `25` | `26` |

### Placeholder Policy

- A placeholder node must compile without extra DBC dependencies.
- A placeholder node must not emit traffic by default.
- A placeholder node exists to keep the OEM vehicle surface breadth visible.
- Promotion order should follow domain waves, not random ECU-by-ECU edits.

### First Promotion Candidates

1. `SCC`
2. `TMU`
3. `SECURITY_GATEWAY`
4. `ETH_BACKBONE`
5. `HVAC`
6. `HUD`
7. `ABS`
8. `TPMS`

### Source Locations

- source placeholders: `canoe/src/capl/placeholders/**`
- GUI import placeholders: `canoe/cfg/channel_assign/**`
