# Unity Bridge Sample Scripts

## Script list
- `UdpUiRenderReceiver.cs`
  - Receives UDP JSON packet and publishes `PacketUpdated` event.
- `UiRenderVisualMap.cs`
  - Shared visual color/blink mapping utility.
- `ExternalRoadViewController.cs`
  - Applies packet to external road scene objects.
- `CabinPanoramaViewController.cs`
  - Applies packet to cabin panorama scene objects.
- `SdvSceneAutoBinder.cs`
  - Auto-assigns object references by naming convention.
- `UiRenderStatusOverlay.cs`
  - On-screen debug HUD for received values.
- `QuickPrototypeSceneBuilder.cs`
  - Builds named placeholder objects for instant External/Cabin demo.
- `SdvSkinRuntimeLoader.cs`
  - Loads PNG sprite/texture assets from `Resources/Skins/unity_skin_pack_v1`.

## Runtime dependency
- Python sender:
  - `canoe/scripts/unity_renderer_bridge.py` (live CANoe)
  - `canoe/scripts/unity_renderer_mock_sender.py` (mock)

## Related docs
- `canoe/docs/operations/unity/UNITY_RENDERER_BRIDGE_QUICKSTART.md`
- `canoe/docs/operations/unity/UNITY_SCENE_BLUEPRINT.md`
