# V2 Risk/Fail-safe Reference Notes

Purpose: evidence-backed implementation notes for `Req_120~Req_124` and their
`Func -> Flow -> Comm -> Var -> Code -> Test` chain.

## 1) Peer-reviewed papers (risk timing / TTC)

1. Hayward, J.C. (1972), *Near-miss determination through use of a scale of danger*.
- TTC is a core conflict indicator used by later warning/braking studies.
- Link: https://nap.nationalacademies.org/read/22850/chapter/11

2. van der Horst, A.R.A. (1990), *A time-based analysis of road user behavior in normal and critical encounters*.
- Time-based conflict framing and TTC banding background for ADAS warning timing.

3. Kiefer et al. (2005), *Developing an inverse time-to-collision crash alert timing approach*.
- Driver warning timing should be speed-coupled, not fixed-time only.
- DOI: https://doi.org/10.1016/j.aap.2004.09.003
- PubMed: https://pubmed.ncbi.nlm.nih.gov/15667816/

4. Shalev-Shwartz et al. (2017), *On a Formal Model of Safe and Scalable Self-driving Cars* (RSS model).
- Formal safety-distance model useful as upper-level guardrail for arbitration/failsafe logic.
- arXiv: https://arxiv.org/abs/1708.06374

## 2) Public protocol / engineering references

1. Euro NCAP Safety Assist + AEB Car-to-Car protocols.
- Confirms broad-speed and scenario-based collision-avoidance evaluation.
- Safety Assist index: https://www.euroncap.com/en/for-engineers/protocols/safety-assist/
- AEB C2C overview: https://www.euroncap.com/en/car-safety/the-ratings-explained/safety-assist/aeb-car-to-car/

2. NHTSA Crash Avoidance Test Reference Guide (Volume IV, 2024).
- Uses explicit `TTCFCW` and `TTCAEB` measurement items for FCW/AEB timing evidence.
- PDF: https://www.nhtsa.gov/sites/nhtsa.gov/files/2025-05/crash-avoidance-test-reference-guide-volume-4-2024.pdf

## 3) Open-source implementation references

1. openpilot safety concept.
- Driver override and actuator limits are treated as first-class safety constraints.
- https://docs.comma.ai/concepts/safety/

2. Autoware Emergency Handler + AEB docs.
- Watchdog/heartbeat based emergency activation and clear path are explicitly modeled.
- Emergency Handler: https://autowarefoundation.gitlab.io/autoware.auto/AutowareAuto/emergency_handler.html
- AEB module: https://autowarefoundation.github.io/autoware_universe/main/control/autoware_autonomous_emergency_braking/
- Obstacle velocity limiter (`min_ttc` concept): https://autowarefoundation.github.io/autoware_universe/pr-10077/planning/motion_velocity_planner/autoware_motion_velocity_obstacle_velocity_limiter_module/

3. CARLA ScenarioRunner (for scenario-based verification style).
- OpenSCENARIO-driven validation + watchdog/timeout hardening references.
- Repo: https://github.com/carla-simulator/scenario_runner
- Changelog: https://scenario-runner.readthedocs.io/en/latest/CHANGELOG/

## 4) Applied decisions in current CANoe V2 implementation

The following are implementation decisions mapped to code and test artifacts.

1. `Req_120` (risk score + publish contract)
- Code: `ADAS_WARN_CTRL.can`
- Decision: `10 ms` internal cycle, risk publish every change or max `100 ms` heartbeat.
- Risk model: `TTCScore` is piecewise inverse-time style (`eta <=2s` highest, 20s -> 0), then
  speed coupling and direction/type bias are fused (`speed`, `driveState`, `emergencyDirection`,
  `emergencyContext`) before final clamp to 0~100.
- Rationale: preserves responsiveness while bounding bus load, and aligns with
  speed-sensitive inverse-time collision urgency patterns from TTC literature.

2. `Req_121` (decel assist request)
- Code: `WARN_ARB_MGR.can`
- Decision: hysteresis (`on >= 70`, `off <= 55`) for `decelAssistReq`.
- Rationale: reduces threshold chatter and oscillation.

3. `Req_122` (driver override release)
- Code: `WARN_ARB_MGR.can`
- Decision: release on `brakePedal >= 15` or `steeringInput == 1`.
- Rationale: aligned with openpilot-style immediate manual takeover principle.

4. `Req_124` (failsafe mode)
- Code: `DOMAIN_BOUNDARY_MGR.can`
- Decision: health check every `100 ms`, 3-domain freshness window `300 ms`,
  `failSafeMode=1` (degraded), `failSafeMode=2` (forced test injection).
- Rationale: watchdog-like degraded/failsafe separation with deterministic forcing path.

Inference note:
- Exact thresholds (`70/55`, `15`, `300 ms`) are project calibration values.
- Literature/protocols justify the safety pattern and measurement method, not these exact numbers.

## 5) Validation hooks (link to 05/06/07 + SIL scenarios)

1. Risk/decel consistency: Scenario `15`, `16`, `19`
2. Driver release behavior: Scenario `17`
3. Failsafe activation and recoverability: Scenario `18`

PASS criteria are defined in:
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`

## 6) Local OSS sources already cloned in this repo

Path: `canoe/reference/oss/`

- `cantools`, `canmatrix`, `python-can`: signal encode/decode verification patterns
- `sil-kit`, `sil-kit-docs`, `vsomeip`: SIL and Ethernet communication reference structure
- `can-utils`, `can-isotp`, `python-udsoncan`, `iso14229`: transport/diagnostic path checks

These are supporting engineering references for communication robustness and tooling, while
the risk/failsafe behavior calibration is driven by sections 1~5 above.
