# Unity Scene Blueprint (External + Cabin)

## Purpose
- Provide fixed scene structure for fast integration with `UiRender::*` stream.
- Keep renderer side presentation-only.

## Scene A: `ExternalRoadScene`
- Required components:
  - `UdpUiRenderReceiver`
  - `ExternalRoadViewController`
  - `SdvSceneAutoBinder` (optional but recommended)
  - `UiRenderStatusOverlay` (optional)
  - `QuickPrototypeSceneBuilder` (optional for placeholder generation)
  - `SdvSkinRuntimeLoader` (optional for PNG skin application)
- Required object names:
  - `RoadLane`
  - `FlowStrip`
  - `VehicleMarker`
  - `EmergencyLightLeft`
  - `EmergencyLightRight`

## Scene B: `CabinScene`
- Required components:
  - `UdpUiRenderReceiver`
  - `CabinPanoramaViewController`
  - `SdvSceneAutoBinder` (optional but recommended)
  - `UiRenderStatusOverlay` (optional)
  - `QuickPrototypeSceneBuilder` (optional for placeholder generation)
  - `SdvSkinRuntimeLoader` (optional for PNG skin application)
- Required object names:
  - `AmbientZone_Driver`
  - `AmbientZone_Passenger`
  - `AmbientZone_Rear`
  - `FlowPhase_0` ... `FlowPhase_7`
  - `DirectionArrow_Left`
  - `DirectionArrow_Right`
  - `DirectionArrow_Rear`

## UiRender Mapping
- `roadZoneColorCode` -> lane color in external scene
- `roadFlowDirection` + `icFlowPhase` -> flow strip offset
- `vehicleObjectPos` -> vehicle marker X interpolation
- `activeAlertType` + `emsBlinkPhase` -> emergency light alternation
- `renderColor` + `ambientPulsePhase` -> cabin ambient zone color
- `renderDirection` -> direction arrow visibility

## Validation Checklist
- Start Unity scene and run:
  - `python canoe/scripts/unity_renderer_mock_sender.py --port 7400 --period-ms 50`
- Optional skin step:
  - Build: `python canoe/scripts/build_unity_skin_pack.py --clean`
  - Copy to Unity: `Assets/Resources/Skins/unity_skin_pack_v1`
- Confirm:
  - Vehicle marker moves continuously (0..100 loop)
  - Lane color changes by zone code
  - Emergency lights alternate by alert type/phase
  - Cabin ambient zones pulse with `ambientPulsePhase`
  - Flow indicators rotate by `icFlowPhase`

## Architecture Rule
- CAPL nodes remain source of warning/arbitration decisions.
- Unity scene applies only visual mapping from derived outputs.
