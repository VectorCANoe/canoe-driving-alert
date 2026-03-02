# OSS PANEL REFERENCE INDEX

## Local Root
- `canoe/reference/oss_panels`

## Clone Policy
- Folder is ignored by Git: `canoe/reference/oss_panels/`
- Purpose: visual/HMI reference benchmarking only
- Note: open-source CANoe `*.xvp` panels are still not available in this set

## Current Repositories
- `ICSim_panel_ref` <- `https://github.com/zombieCraig/ICSim.git`
- `openroadsim_ref` <- `https://github.com/karthagokul/openroadsim.git`
- `qt_hmi_display_ui_ref` <- `https://github.com/cppqtdev/Qt-HMI-Display-UI.git`
- `can2cluster_ref` <- `https://github.com/thomastech/CAN2Cluster.git`
- `openxc_vehicle_simulator_ref` <- `https://github.com/openxc/openxc-vehicle-simulator.git`
- `des_instrument_cluster_ref` <- `https://github.com/SEA-ME/DES_Instrument-Cluster.git`
- `dashboardsample_ref` <- `https://github.com/opernitt/dashboardsample.git`
- `modern_car_dashboard_ref` <- `https://github.com/cppqtdev/Modern-Car-Dashboard.git`
- `rpi_digital_cluster_ref` <- `https://github.com/pratikfarkase94/Touch-Screen-based-fully-Digital-Instrument-cluster-Using-Raspberry-Pi-3-CPP-QT-QML.git`
- `car_cluster_hmi_ref` <- `https://github.com/afondiel/car-cluster-hmi.git`
- `qml_flight_instruments_ref` <- `https://github.com/berkbavas/QmlFlightInstruments.git`
- `headunit_desktop_ref` <- `https://github.com/viktorgino/headunit-desktop.git`
- `genivi_vehicle_sim_ref` <- `https://github.com/GENIVI/genivi-vehicle-simulator.git`
- `out_gauge_cluster_ref` <- `https://github.com/fuelsoft/out-gauge-cluster.git`
- `qdashboard_ref` <- `https://github.com/IndeemaSoftware/QDashBoard.git`
- `car_hmi_dashboard_ui_ref` <- `https://github.com/cppqtdev/Car-HMI-Dashboard-UI.git`
- `car_speedometer_ref` <- `https://github.com/cppqtdev/Car-Speedometer.git`
- `coupled_sim_unity_ref` <- `https://github.com/bazilinskyy/coupled-sim.git`
- `unity_speedometer_ref` <- `https://github.com/TheDeveloper10/Unity-Speedometer.git`
- `js_vehicle_physics_ref` <- `https://github.com/Jermesa-Studio/JS_Vehicle_Physics_Controller.git`

## Quick Facts
- `*.xvp` count in `oss_panels`: `0`
- Image assets (`png/bmp/jpg/svg/gif`) in `oss_panels`: `2314`

## Recommended Priority
- High-fidelity macro scene reference:
  - `headunit_desktop_ref` (largest QML/UI set)
  - `genivi_vehicle_sim_ref` (vehicle/world simulator assets)
  - `qdashboard_ref` (balanced dashboard architecture)
- Unity-ready external renderer reference:
  - `coupled_sim_unity_ref` (Unity project, scenes + scripts)
  - `js_vehicle_physics_ref` (Unity vehicle stack, large script set)
  - `unity_speedometer_ref` (small gauge-focused sample)
- Clean core cluster/gauge reference:
  - `car_speedometer_ref`
  - `car_hmi_dashboard_ui_ref`
  - `modern_car_dashboard_ref`

## Usage Guidance
- Reuse only visual patterns/animation ideas, not external arbitration logic.
- Keep project rule: logic in CAPL nodes, render in panel (`UiRender::*` derived outputs).
- Convert selected references into project-owned bitmap/QML-like design assets before XVP binding.
