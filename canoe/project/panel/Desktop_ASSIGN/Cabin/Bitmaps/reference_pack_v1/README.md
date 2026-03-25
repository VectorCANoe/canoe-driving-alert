# reference_pack_v1

Curated bitmap subset copied from local Vector sample references for panel skin prototyping.

## Source Mapping
- `EXT_VCar_side.bmp` <- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Bitmaps/VCar.bmp`
- `EXT_PoliceLight_Left.bmp` <- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Bitmaps/VCarFlashLightLeft.bmp`
- `EXT_PoliceLight_Right.bmp` <- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Bitmaps/VCarFlashLightRight.bmp`
- `EXT_HeadLight_Left.bmp` <- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Bitmaps/VCarHeadLightLeft.bmp`
- `EXT_HeadLight_Right.bmp` <- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Bitmaps/VCarHeadLightRight.bmp`
- `EXT_VCar_topview.png` <- `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/Bitmap/VCarTopview.png`
- `EXT_Lane_horizontal.png` <- `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/Bitmap/Lines_horizontal.png`
- `EXT_Lane_left.png` <- `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/Bitmap/Lines_left.png`
- `EXT_Lane_right.png` <- `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/Bitmap/Lines_Right.png`
- `EXT_TrafficLight_strip.png` <- `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels/BMP/HU_TrafficLight.png`
- `NAV_Arrow_left.bmp` <- `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels/BMP/Arrow_Left.bmp`
- `NAV_Arrow_right.bmp` <- `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels/BMP/Arrow_Right.bmp`
- `CABIN_FrontWindow_scene.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/FrontWindow.bmp`
- `CABIN_FrontWindow_overlay.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/VCFrontWindow.bmp`
- `CABIN_Window_front_left_strip.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/WinLeft.bmp`
- `CABIN_Window_front_right_strip.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/WinRight.bmp`
- `CABIN_Window_rear_left_strip.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/WinLeftBack.bmp`
- `CABIN_Window_rear_right_strip.bmp` <- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/Bitmaps/Window/WinRightBack.bmp`

## Generated Assets (for macro panel skin v2)
- `EXT_Background.png` (1024x480)
- `CABIN_Background.png` (1024x480)
- `EXT_VehicleMove11.png` (11-state strip, frame 460x70)
- `EXT_FlowBadge3.png` (3-state strip, frame 200x26)
- `EXT_VehicleClass8.png` (8-state strip, frame 220x90)
- `EXT_EmsBlink2.png` (2-state strip, frame 20x20)
- `NAV_Background.png` (734x396)
- `AMB_Background.png` (768x340)

Generation script:
- `canoe/scripts/generate_macro_skin_assets.py`
