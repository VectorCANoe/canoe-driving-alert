# CANoe + Unity Standard (Fixed)

## Standard decision
- Runtime Unity target is fixed to one project:
  - `canoe/reference/oss_panels/coupled_sim_unity_ref`
- Do not run multiple Unity projects in parallel for one CANoe measurement.

## Why this standard
- Reduces ambiguity and sync mismatch risk.
- Keeps evidence collection deterministic.
- Fits rule: logic in CAPL, rendering in adapter only.

## One-command standard pipeline
```bash
python canoe/scripts/unity_standard_pipeline.py --mode all
```

What it does:
1. Build skin pack (`unity_skin_pack_v1`)
2. Sync bridge scripts + skin files into fixed Unity target
3. Verify required files and write standard report:
   - `canoe/docs/operations/unity/UNITY_SYNC_VERIFICATION_STANDARD.md`

## Runtime sequence (production-like)
1. In CANoe: Start Measurement
2. Start bridge:
```bash
python canoe/scripts/unity_renderer_bridge.py --host 127.0.0.1 --port 7400 --period-ms 50
```
3. Open Unity project:
   - `canoe/reference/oss_panels/coupled_sim_unity_ref`
4. Play scene:
   - Start with `ExternalRoadScene`
   - Optionally switch/add `CabinScene`

## Offline sequence (without CANoe)
```bash
python canoe/scripts/unity_renderer_mock_sender.py --host 127.0.0.1 --port 7400 --period-ms 50
```

## Scope guardrails
- Do not move arbitration or timeout logic to Unity.
- Unity uses only derived outputs (`UiRender::*`).
- Keep verification timing points: `50/100/150/1000 ms`.
