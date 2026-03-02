# Unity Asset Pipeline (PNG/SVG)

## Policy
- Keep design master in `SVG`.
- Use `PNG` for runtime in CANoe/Unity.
- Do not add new `BMP` for new skin work.

## Why
- `SVG`: scalable, easy design iteration.
- `PNG`: stable runtime import, alpha transparency, predictable rendering.

## Build skin pack from OSS references
```bash
python canoe/scripts/build_unity_skin_pack.py --clean
```

Generated output:
- `canoe/reference/oss_panels/_exports/unity_skin_pack_v1/`
  - `manifest.json`
  - `manifest.md`
  - `external/...`
  - `cabin/...`

## Unity import
1. Copy generated `unity_skin_pack_v1` folder into Unity project:
   - `Assets/Resources/Skins/unity_skin_pack_v1/`
2. Ensure texture import settings:
   - Type: `Sprite (2D and UI)` for icon/marker/cluster images
   - Type: `Default` for material textures (road/background)
3. Add `SdvSkinRuntimeLoader` and click `Apply Skin`.

### Automated sync option
```bash
python canoe/scripts/sync_unity_integration.py --auto-detect --clean-skin-dir
```
This command copies:
- `canoe/reference/unity_bridge_samples/*.cs` -> `Assets/Scripts/SdvBridge/`
- `canoe/reference/oss_panels/_exports/unity_skin_pack_v1/*` -> `Assets/Resources/Skins/unity_skin_pack_v1/`

## External/Cabin usage model
- External:
  - Background/road as PNG texture.
  - Vehicle/warning markers as PNG sprite.
  - Optional vector icons kept as SVG references for re-export.
- Cabin:
  - Cluster background/needle/car icons as PNG sprite.
  - Ambient layers as PNG strips + runtime color modulation.

## Traceability note
- Visual assets are renderer-side only.
- Logic remains in CAPL nodes and `UiRender::*` derived outputs.
