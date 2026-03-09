# Placeholder Surface ECU Bank

This tree contains shallow CAPL nodes used to keep the OEM surface breadth visible.

Rules:

- These files are not deep runtime implementations.
- These files expose only surface ECU names.
- These files must stay compile-safe with empty start handlers.
- Promotion to real runtime should move logic into the target surface ECU, not create internal names at the top level.

Current bank:

- `87` placeholder nodes
- mirrored `1:1` into `canoe/cfg/channel_assign/**`
