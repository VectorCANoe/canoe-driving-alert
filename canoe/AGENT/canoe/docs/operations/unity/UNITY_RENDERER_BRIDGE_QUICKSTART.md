# Unity Renderer Bridge Quickstart

## Goal
- Keep CAPL as source of decision logic.
- Send derived renderer outputs (`UiRender::*`) to Unity over UDP.

## 1) Run Python bridge
```bash
python canoe/scripts/unity_renderer_bridge.py --host 127.0.0.1 --port 7400 --period-ms 50
```

### Optional: run without CANoe (mock stream)
```bash
python canoe/scripts/unity_renderer_mock_sender.py --host 127.0.0.1 --port 7400 --period-ms 50
```

### One-command sync into detected Unity projects
```bash
python canoe/scripts/sync_unity_integration.py --auto-detect --clean-skin-dir
```

### Standard fixed-target pipeline (recommended)
```bash
python canoe/scripts/unity_standard_pipeline.py --mode all
```
See:
- `canoe/docs/operations/CANOE_UNITY_STANDARD.md`

## 2) Unity side
- Copy script:
  - `canoe/reference/unity_bridge_samples/UdpUiRenderReceiver.cs`
  - `canoe/reference/unity_bridge_samples/UiRenderVisualMap.cs`
  - `canoe/reference/unity_bridge_samples/ExternalRoadViewController.cs`
  - `canoe/reference/unity_bridge_samples/CabinPanoramaViewController.cs`
  - `canoe/reference/unity_bridge_samples/SdvSceneAutoBinder.cs`
  - `canoe/reference/unity_bridge_samples/UiRenderStatusOverlay.cs`
  - `canoe/reference/unity_bridge_samples/QuickPrototypeSceneBuilder.cs`
  - `canoe/reference/unity_bridge_samples/SdvSkinRuntimeLoader.cs`
- Attach `UdpUiRenderReceiver` to a Unity scene object.
- Set `listenPort` to `7400` (or match bridge `--port`).

## 2a) Scene split (recommended)
- Scene A: `ExternalRoadScene`
  - `UdpUiRenderReceiver` + `ExternalRoadViewController`
  - Bind lane/flow materials, vehicle marker transform, emergency light renderers
- Scene B: `CabinScene`
  - `UdpUiRenderReceiver` + `CabinPanoramaViewController`
  - Bind ambient zone renderers, phase indicators, direction arrows
- Optional helper object in each scene:
  - `SdvSceneAutoBinder` (auto-assign by object names)
  - `UiRenderStatusOverlay` (debug HUD)
  - `QuickPrototypeSceneBuilder` (generate placeholder objects quickly)
  - `SdvSkinRuntimeLoader` (apply PNG-based skin from Resources)

## 2b) Recommended object names
- External scene:
  - `RoadLane`, `FlowStrip`, `VehicleMarker`, `EmergencyLightLeft`, `EmergencyLightRight`
- Cabin scene:
  - `AmbientZone_Driver`, `AmbientZone_Passenger`, `AmbientZone_Rear`
  - `FlowPhase_0` ... `FlowPhase_7`
  - `DirectionArrow_Left`, `DirectionArrow_Right`, `DirectionArrow_Rear`

## 2c) Apply reference skin pack
1. Build pack in this repo:
```bash
python canoe/scripts/build_unity_skin_pack.py --clean
```
2. Copy generated folder:
   - from: `canoe/reference/oss_panels/_exports/unity_skin_pack_v1`
   - to: `Assets/Resources/Skins/unity_skin_pack_v1` (Unity project)
3. Add `SdvSkinRuntimeLoader` and click `Apply Skin`.

## 3) Packet schema
```json
{
  "schema": "sdv.ui_render.v1",
  "seq": 123,
  "tsMs": 1730000000000,
  "uiRender": {
    "renderMode": 0,
    "renderColor": 0,
    "renderPattern": 0,
    "renderTextCode": 0,
    "renderDirection": 0,
    "roadZoneColorCode": 0,
    "roadFlowDirection": 0,
    "vehicleObjectPos": 0,
    "emsBlinkPhase": 0,
    "ambientPulsePhase": 0,
    "icFlowPhase": 0,
    "activeAlertType": 0
  }
}
```

## 4) Timing policy
- Recommended bridge period: `50ms` for smooth visuals.
- Keep verification points aligned with project thresholds:
  - `50 / 100 / 150 / 1000 ms`

## 5) Rule reminders
- Do not move arbitration/timeout logic into Unity.
- Unity is renderer-only adapter.
- Any new renderer-facing variable must be traceable in `0304`.

## 6) Asset pipeline
- See:
  - `canoe/docs/operations/unity/UNITY_ASSET_PIPELINE.md`
