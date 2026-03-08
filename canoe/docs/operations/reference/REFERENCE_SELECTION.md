# Reference Selection (Execution Baseline)

## 1) Purpose

Freeze which external/local references are allowed as implementation baseline.
This avoids rework from importing large OSS projects wholesale.

## 2) Primary (Adopt)

1. Vector CANoe sample baseline (logic/render separation)
- `reference/vector_samples_19_4_10/ADAS/ADASSystem/ApplicationModels/DashboardControl.can`
- `reference/vector_samples_19_4_10/ADAS/ADASSystem/Panels/Dashboard.xvp`
- `canoe/reference/vector_code_sample/Car.xvp`

2. Unity renderer adapter baseline (project-owned)
- `canoe/reference/unity_bridge_samples/README.md`
- `canoe/docs/operations/unity/UNITY_RENDERER_BRIDGE_QUICKSTART.md`
- `canoe/docs/operations/unity/UNITY_SCENE_BLUEPRINT.md`

3. Curated skin baseline (already filtered)
- `canoe/reference/oss_panels/_exports/unity_skin_pack_v1/manifest.md`
- `canoe/reference/oss_panels/_exports/unity_skin_pack_v1/manifest.json`

## 3) Secondary (Reference Only, Partial Reuse)

- `canoe/reference/oss_panels/coupled_sim_unity_ref_u63_trial`
- `canoe/reference/oss_panels/genivi_vehicle_sim_ref`
- `canoe/reference/oss_panels/headunit_desktop_ref`
- `canoe/reference/oss_panels/qdashboard_ref`

Rule:
- Do not import whole projects as a runtime dependency.
- Reuse only selected assets/scripts with source trace.

## 4) Exclusion Rule

- `canoe/reference/oss_panels/*` full-project migration is out of scope.
- Keep project architecture unchanged:
  - CAPL = decision/arbitration
  - IVI/Panel/Unity = renderer adapter only

## 5) CLI/Verification Link

This reference baseline supports current CLI-first plan:
- `scripts/run.py verify ...` for evidence automation
- `scripts/run.py verify insight ...` for run-level KPI/insight report
- CANoe panel/Unity remains manual or semi-automatic visualization evidence.
