from __future__ import annotations

import json
import re
import textwrap
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


DATE_STAMP = "2026-03-28"
REPO_ROOT = Path(__file__).resolve().parents[5]

SRC_CAPL_ROOT = REPO_ROOT / "canoe" / "src" / "capl"
CHANNEL_ASSIGN_ROOT = REPO_ROOT / "canoe" / "cfg" / "channel_assign"
DBC_ROOT = REPO_ROOT / "canoe" / "databases"
OWNERSHIP_MATRIX = REPO_ROOT / "canoe" / "tmp" / "runtime_message_ownership_matrix.md"
TEST_UNIT_ROOT = REPO_ROOT / "canoe" / "tests" / "modules" / "test_units"

INTERNAL_ARCH_ROOT = REPO_ROOT / "canoe" / "AGENT" / "canoe" / "docs" / "architecture"
ARCH_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ARCH_ROOT / "data"
FLOW_ROOT = ARCH_ROOT / "flows"
SVG_ROOT = ARCH_ROOT / "svg"
CARD_ROOT = SVG_ROOT / "ecu_cards"
FLOW_SVG_ROOT = SVG_ROOT / "flows"
PROTOTYPE_ROOT = INTERNAL_ARCH_ROOT / "svg" / "card_prototypes"

METADATA_JSON = DATA_ROOT / f"ECU_METADATA_DATASET_{DATE_STAMP}.json"
ACTION_FLOW_JSON = DATA_ROOT / f"ACTION_FLOW_DATASET_{DATE_STAMP}.json"
FUNCTION_STATEMENTS_JSON = DATA_ROOT / "ECU_FUNCTION_STATEMENTS.json"
RISK_NOTES_JSON = DATA_ROOT / "ECU_RISK_NOTES.json"
MASTER_BOOK = ARCH_ROOT / f"ECU_METADATA_BOOK_{DATE_STAMP}.md"
CARD_INDEX = ARCH_ROOT / f"ECU_CARD_INDEX_{DATE_STAMP}.md"
ACTION_FLOW_INDEX = ARCH_ROOT / f"ACTION_FLOW_INDEX_{DATE_STAMP}.md"
ECU_FLOW_MATRIX = ARCH_ROOT / f"ECU_ACTION_FLOW_MATRIX_{DATE_STAMP}.md"
GROUP06_SVG = SVG_ROOT / f"GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_{DATE_STAMP}.svg"
ECU_DOMAIN_LOOKUP: dict[str, str] = {}

MESSAGE_RE = re.compile(r"^BO_\s+(\d+)\s+(\w+):\s+(\d+)\s+(\w+)")
SIGNAL_RE = re.compile(r'^SG_\s+(\w+).*?"[^"]*"\s+(.+)$')
TABLE_ROW_RE = re.compile(r"^\|")


@dataclass
class MessageContract:
    name: str
    source: str
    sender: str
    receivers: set[str] = field(default_factory=set)


@dataclass
class EcuMeta:
    ecu: str
    domain: str
    group: str
    source_capl: str
    mirror_capl: str
    role_hint: str
    owner_seam: list[str]
    published_contracts: list[str]
    consumed_contracts: list[str]
    linked_ecus: list[str]
    upstream_ecus: list[str]
    downstream_ecus: list[str]
    inbound_edges: list[str]
    outbound_edges: list[str]
    inbound_dbc_sources: list[str]
    outbound_dbc_sources: list[str]
    sysvar_hints: list[str]
    test_assets: list[str]
    dbc_sources: list[str]
    doc_sources: list[str]
    current_gap_risk: str
    runtime_note: str


@dataclass
class ActionFlow:
    flow_id: str
    slug: str
    title: str
    category: str
    summary: str
    participants: list[str]
    steps: list[tuple[str, str, str]]
    key_contracts: list[str]
    key_files: list[str]
    user_outcome: str


CURATED_HINTS: dict[str, dict[str, object]] = {
    "VCU": {
        "role_hint": "Powertrain controller",
        "owner_seam": ["Chassis::vehicleSpeed", "Chassis::driveState", "Chassis::throttlePosition"],
        "sysvar_hints": ["@Chassis::vehicleSpeed", "@Chassis::driveState", "@Chassis::throttlePosition"],
        "current_gap_risk": "Manual speed target and pedal dynamics can still fight if stale assist hints are reasserted.",
        "runtime_note": "Primary dynamics producer for speed, drive state, and throttle interpretation.",
    },
    "ESC": {
        "role_hint": "Chassis brake controller",
        "owner_seam": ["Chassis::brakePressure", "Chassis::brakeLamp", "Chassis::absActive"],
        "sysvar_hints": ["@Chassis::brakePressure", "@Chassis::brakeLamp", "@Chassis::absActive"],
        "current_gap_risk": "assistPressureFloor remains the strongest current dynamics risk during AEB overlay.",
        "runtime_note": "Consumes vehicle and AEB state, then publishes brake and stability state to downstream readers.",
    },
    "MDPS": {
        "role_hint": "Chassis steering controller",
        "owner_seam": ["Chassis::steeringAngle", "Display::steeringFrame"],
        "sysvar_hints": ["@Chassis::steeringAngle", "@Display::steeringFrame"],
        "current_gap_risk": "Steering path is largely coherent after bar, wheel, and readback unification.",
        "runtime_note": "Steering state must stay aligned across manual command, owner readback, and display frame.",
    },
    "CGW": {
        "role_hint": "Central gateway and gatekeeper",
        "owner_seam": ["CoreState::selectedAlertGateReason"],
        "sysvar_hints": ["@CoreState::selectedAlertGateReason"],
        "current_gap_risk": "Downstream display behavior depends heavily on gate reason consistency.",
        "runtime_note": "Bridges domain outputs toward IVI, CLU, BCM, and AMP while enforcing gate logic.",
    },
    "ADAS": {
        "role_hint": "Alert arbitration and decel assist domain controller",
        "owner_seam": ["Core::selectedAlertType", "Core::selectedAlertLevel"],
        "sysvar_hints": ["@Core::selectedAlertType", "@Core::selectedAlertLevel"],
        "current_gap_risk": "Must be read together with AEB, not as a standalone risk producer.",
        "runtime_note": "Consumes route, chassis, and emergency context, then emits selected alert and assist intent.",
    },
    "SCC": {
        "role_hint": "Longitudinal assist support controller",
        "owner_seam": ["Powertrain::cruiseSetSpeed"],
        "sysvar_hints": ["@Powertrain::cruiseSetSpeed"],
        "current_gap_risk": "Support-state coupling matters more than standalone bus ownership.",
        "runtime_note": "SCC support behavior feeds ADAS and VCU rather than directly owning output HMI.",
    },
    "V2X": {
        "role_hint": "Emergency ingress and V2X alert controller",
        "owner_seam": ["V2X::v2xFrame", "V2X::AmbFrame", "V2X::MyCarFrame"],
        "sysvar_hints": ["@V2X::v2xFrame", "@V2X::AmbFrame", "@V2X::MyCarFrame"],
        "current_gap_risk": "External ingress is stable; arbitration and output priority happen later.",
        "runtime_note": "Owns emergency ingress context before ADAS and CGW perform prioritization.",
    },
    "AEB": {
        "role_hint": "AEB domain controller",
        "owner_seam": ["AEB StopReq / DecelProfile / DomainHealth"],
        "sysvar_hints": ["frmAebDomainStateMsg"],
        "current_gap_risk": "This is the most likely producer of stepped brake feel across ESC, EHB, and VSM.",
        "runtime_note": "One AEB profile change can appear as multiple simultaneous chassis ECU reactions.",
    },
    "EHB": {
        "role_hint": "Brake assist leaf ECU",
        "owner_seam": ["local brake assist state"],
        "sysvar_hints": ["local brake assist state"],
        "current_gap_risk": "Shares the same decel profile thresholds as ESC/VSM and can amplify perceived brake stutter.",
        "runtime_note": "Coupled consumer of AEB state rather than an independent decision origin.",
    },
    "VSM": {
        "role_hint": "Vehicle stability intervention leaf ECU",
        "owner_seam": ["local intervention state"],
        "sysvar_hints": ["local intervention state"],
        "current_gap_risk": "Contributes to perceived intervention step changes under the same AEB profile shifts.",
        "runtime_note": "Consumes ESC and AEB domain state to produce local stability intervention behavior.",
    },
    "IVI": {
        "role_hint": "HMI and display gateway",
        "owner_seam": ["Cluster::warningTextCode", "UiRender::*"],
        "sysvar_hints": ["@Cluster::warningTextCode", "@UiRender::renderVolumLevel"],
        "current_gap_risk": "Display path is structurally sound; most issues originate upstream.",
        "runtime_note": "Routes gated alert state into visible display, map, and audio focus paths.",
    },
    "BCM": {
        "role_hint": "Body and ambient owner",
        "owner_seam": ["Body::ambientMode", "Body::frontWiperAnimFrame", "Body::blinkLeft", "Body::blinkRight"],
        "sysvar_hints": ["@Body::ambientMode", "@Body::frontWiperAnimFrame", "@Body::blinkLeft", "@Body::blinkRight"],
        "current_gap_risk": "Ambient and comfort breadth are wider than the current input-console surface.",
        "runtime_note": "Owns comfort and ambient outputs while bridging body leaf ECU state back to HMI.",
    },
    "CLU": {
        "role_hint": "Cluster owner",
        "owner_seam": ["Cluster::warningTextCode", "Display::steeringFrame"],
        "sysvar_hints": ["@Cluster::warningTextCode", "@Display::steeringFrame"],
        "current_gap_risk": "Output ownership is clean; visible issues are usually upstream.",
        "runtime_note": "Consumes selected alert state and vehicle state to build cluster-facing output.",
    },
    "AMP": {
        "role_hint": "Audio output owner",
        "owner_seam": ["UiRender::renderVolumLevel", "CoreState::baseVolume"],
        "sysvar_hints": ["@UiRender::renderVolumLevel", "@CoreState::baseVolume"],
        "current_gap_risk": "Audio rendering is stable; alert priority path matters more than bus mapping.",
        "runtime_note": "Receives gated audio intent from IVI/BCM and renders the final alert volume.",
    },
    "TEST_SCN": {
        "role_hint": "Validation and scenario harness",
        "owner_seam": ["Test::scenarioCommand", "Test::scenarioActiveId", "Test::scenarioResult"],
        "sysvar_hints": ["@Test::scenarioCommand", "@Test::scenarioActiveId", "@Test::scenarioResult"],
        "current_gap_risk": "Must stay scenario-focused and not silently become a normal feature owner.",
        "runtime_note": "Scenario entry point for validation presets, stop/manual logic, and scenario verdict readback.",
    },
    "TEST_BAS": {
        "role_hint": "Validation baseline harness",
        "owner_seam": ["validation summary seams", "Input_Console router entry"],
        "sysvar_hints": ["validation summary seams"],
        "current_gap_risk": "Should remain validation-focused and not drift back into scenario ownership.",
        "runtime_note": "Receives internal input router helpers and publishes baseline validation summaries.",
    },
}


def load_curated_text_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    curated: dict[str, str] = {}
    for ecu, text in data.items():
        if not isinstance(ecu, str) or not isinstance(text, str):
            continue
        normalized = " ".join(text.split()).strip()
        if normalized:
            curated[ecu] = normalized.rstrip(".")
    return curated


CURATED_FUNCTION_STATEMENTS = load_curated_text_map(FUNCTION_STATEMENTS_JSON)
CURATED_RISK_NOTES = load_curated_text_map(RISK_NOTES_JSON)

GROUP_LABELS: dict[str, str] = {
    "GROUP_01_BASE_VEHICLE_DYNAMICS": "Group 01 Base Vehicle Dynamics",
    "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "Group 02 ADAS AEB Brake Assist",
    "GROUP_03_DISPLAY_WARNING_AUDIO": "Group 03 Display Warning Audio",
    "GROUP_04_BODY_COMFORT_AMBIENT": "Group 04 Body Comfort Ambient",
    "GROUP_05_VALIDATION_SCENARIO": "Group 05 Validation Scenario",
    "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "Group 06 Backbone Gateway Diagnostics",
}

GROUP_STORIES: dict[str, str] = {
    "GROUP_01_BASE_VEHICLE_DYNAMICS": "The base vehicle dynamics group consolidates steering, braking, propulsion, and chassis health into one controllable runtime lane.",
    "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "The ADAS group collects perception, collision risk, parking assist, and intervention logic into one behavior-decision layer.",
    "GROUP_03_DISPLAY_WARNING_AUDIO": "The display and alert group turns selected warning state into visible, audible, and service-facing user output.",
    "GROUP_04_BODY_COMFORT_AMBIENT": "The body and comfort group amplifies warning context through lighting, entry, ambient, climate, and comfort-domain state.",
    "GROUP_05_VALIDATION_SCENARIO": "The validation group isolates scenario injection and verdict readback so test orchestration stays separate from normal feature ownership.",
    "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "The backbone and diagnostics group routes runtime state, service traffic, and external interfaces without becoming a hidden feature owner.",
}

CATEGORY_ORDER = [
    "Dynamics",
    "ADAS",
    "Display and Alert",
    "Body and Comfort",
    "Validation",
    "Backbone",
]

CATEGORY_STORIES: dict[str, str] = {
    "Dynamics": "These flows explain how driver input, vehicle state, brake intervention, and propulsion feedback stay aligned on the runtime surface.",
    "ADAS": "These flows show how sensing, fusion, and assist logic become one coherent intervention and warning chain.",
    "Display and Alert": "These flows turn selected alert state into cluster, HUD, audio, navigation, and service-facing user output.",
    "Body and Comfort": "These flows describe how body, comfort, and ambient actuators amplify or support the selected runtime state.",
    "Validation": "These flows keep scenario control and verdict readback inside a dedicated validation lane.",
    "Backbone": "These flows describe how gateway, diagnostics, and Ethernet-facing services route state across domains.",
}

PAGE_BREAK = '<div style="page-break-before: always;"></div>'

PROTOTYPE_CARD_ECUS = {"AFLS", "AEB", "VCU", "CGW", "TEST_SCN"}


def build_action_flows() -> dict[str, ActionFlow]:
    flows = [
        ActionFlow(
            flow_id="FLOW_01",
            slug="STEERING_CONTROL_READBACK",
            title="Steering Control Readback",
            category="Dynamics",
            summary="Manual steering input is normalized, published as steering state, and rendered back into the donor wheel image path.",
            participants=["Input_Console", "ESC", "MDPS", "CGW", "ADAS", "CLU"],
            steps=[
                ("Input_Console", "Capture steering request", "Driver wheel or bar writes Cmd::steeringAngleCmd."),
                ("ESC", "Normalize manual angle", "Bridge command into legacy steering angle and manual readback seams."),
                ("MDPS", "Publish steering state", "Produce steering state, torque, and EPS state on the chassis lane."),
                ("CGW / ADAS", "Consume steering freshness", "Gateway and ADAS merge steering freshness and steeringInputNorm."),
                ("CLU", "Render wheel feedback", "Display::steeringFrame keeps the donor wheel image aligned with input."),
            ],
            key_contracts=["Cmd::steeringAngleCmd", "Chassis::steeringAngle", "frmSteeringStateCanMsg", "frmSteeringTorqueMsg", "Display::steeringFrame"],
            key_files=["ESC.can", "MDPS.can", "CGW.can", "ADAS.can", "CLU.can"],
            user_outcome="Steering bar, steering angle readback, and wheel image move together without drift.",
        ),
        ActionFlow(
            flow_id="FLOW_02",
            slug="BRAKE_STABILITY_RESPONSE",
            title="Brake Stability Response",
            category="Dynamics",
            summary="Brake request, AEB pressure intent, and stability outputs are synchronized across chassis brake owners and downstream readers.",
            participants=["AEB / ADAS", "ESC", "ABS / EHB / VSM", "VCU", "CGW / CLU"],
            steps=[
                ("AEB / ADAS", "Raise brake assist intent", "Decel profile and stop request are emitted for chassis actuation."),
                ("ESC", "Arbitrate brake pressure", "Brake controller merges manual state, assist pressure, and stability state."),
                ("ABS / EHB / VSM", "Reflect local intervention", "Leaf brake and stability ECUs consume the same intervention window."),
                ("VCU", "Consume vehicle state", "Powertrain side reacts to brake and wheel speed state transitions."),
                ("CGW / CLU", "Expose brake state", "Gateway and display surfaces publish brake, stability, and health readback."),
            ],
            key_contracts=["frmAebDomainStateMsg", "frmBrakeStatusMsg", "frmBrakeTempMsg", "frmWheelSpeedMsg", "Chassis::brakePressure"],
            key_files=["AEB.can", "ADAS.can", "ESC.can", "EHB.can", "VSM.can"],
            user_outcome="Brake intervention feels coordinated and the driver sees consistent brake and stability state feedback.",
        ),
        ActionFlow(
            flow_id="FLOW_03",
            slug="PROPULSION_ENERGY_STATUS",
            title="Propulsion Energy Status",
            category="Dynamics",
            summary="Powertrain and energy ECUs consolidate drive, torque, battery, and charging state into the central propulsion state lane.",
            participants=["BAT_BMS / EMS", "VCU", "TCU / TRM", "CGW / ADAS", "CLU / IVI"],
            steps=[
                ("BAT_BMS / EMS", "Publish energy inputs", "Battery, engine, and power limits are produced into the propulsion lane."),
                ("VCU", "Fuse drive state", "Vehicle controller merges speed, drive, throttle, and energy conditions."),
                ("TCU / TRM", "Propagate support state", "Transmission and thermal support readers react to the central propulsion state."),
                ("CGW / ADAS", "Expose runtime state", "Gateway and ADAS consume propulsion status for visibility and control adaptation."),
                ("CLU / IVI", "Render vehicle status", "Display surfaces show mode, vehicle state, and support context."),
            ],
            key_contracts=["frmBatBmsStateMsg", "frmVehicleStateCanMsg", "frmPowertrainGatewayMsg", "Chassis::vehicleSpeed", "Chassis::driveState"],
            key_files=["VCU.can", "EMS.can", "BAT_BMS.can", "TCU.can", "CGW.can"],
            user_outcome="Vehicle mode, energy state, and propulsion readiness appear as one coherent status surface.",
        ),
        ActionFlow(
            flow_id="FLOW_04",
            slug="CRUISE_SPEED_SUPPORT",
            title="Cruise Speed Support",
            category="Dynamics",
            summary="Cruise and longitudinal support state moves from support controllers into vehicle speed management and driver-facing outputs.",
            participants=["SCC", "VCU", "ADAS", "CGW", "CLU / IVI"],
            steps=[
                ("SCC", "Publish cruise intent", "Cruise set speed and support status are produced for vehicle control."),
                ("VCU", "Merge longitudinal state", "Vehicle controller fuses cruise state with propulsion and pedal context."),
                ("ADAS", "Adapt support behavior", "Longitudinal assist uses cruise state for warning and decel strategy."),
                ("CGW", "Route cruise visibility", "Gateway exposes cruise freshness and selected support state."),
                ("CLU / IVI", "Render speed support", "Cluster and IVI show speed support and drive-assist context."),
            ],
            key_contracts=["Powertrain::cruiseSetSpeed", "frmCruiseStateMsg", "frmVehicleStateCanMsg", "selected support state"],
            key_files=["SCC.can", "VCU.can", "ADAS.can", "CGW.can", "CLU.can"],
            user_outcome="Cruise support state is readable, timely, and aligned between control and HMI.",
        ),
        ActionFlow(
            flow_id="FLOW_05",
            slug="CHASSIS_SENSOR_HEALTH",
            title="Chassis Sensor Health",
            category="Dynamics",
            summary="Wheel, angle, suspension, and chassis leaf signals are collected so downstream control and visibility stay health-aware.",
            participants=["SAS / TPMS / RWS", "ESC / MDPS", "VCU / ADAS", "CGW", "CLU"],
            steps=[
                ("SAS / TPMS / RWS", "Produce chassis leaf state", "Leaf chassis sensors publish angle, tire, and rear steer status."),
                ("ESC / MDPS", "Normalize control inputs", "Primary chassis controllers merge raw leaf state into central control state."),
                ("VCU / ADAS", "Consume for behavior", "Vehicle and ADAS logic use chassis state for stability and warning decisions."),
                ("CGW", "Merge health visibility", "Gateway tracks freshness and health across the chassis domain."),
                ("CLU", "Display chassis readiness", "Driver-visible status follows the normalized health and state lane."),
            ],
            key_contracts=["frmSteeringAngleMsg", "frmWheelSpeedMsg", "frmTirePressureMsg", "frmSuspensionStateMsg"],
            key_files=["SAS.can", "TPMS.can", "RWS.can", "ESC.can", "MDPS.can"],
            user_outcome="Chassis sensing and readiness stay visible and synchronized across control and display surfaces.",
        ),
        ActionFlow(
            flow_id="FLOW_06",
            slug="OBJECT_RISK_FUSION",
            title="Object Risk Fusion",
            category="ADAS",
            summary="Radar, camera, lidar, and perception nodes are fused into one object-risk lane for ADAS warning and assist decisions.",
            participants=["FCAM / FRADAR / LDR", "SRR_* / OMS", "ADAS", "CGW", "CLU / IVI"],
            steps=[
                ("FCAM / FRADAR / LDR", "Publish scene primitives", "Front sensing ECUs emit object, lane, and range context."),
                ("SRR_* / OMS", "Add side and occupant context", "Side radar and occupant perception enrich the risk picture."),
                ("ADAS", "Fuse object risk", "ADAS turns multi-sensor state into warning, release, and assist candidates."),
                ("CGW", "Route selected risk state", "Gateway distributes the fused ADAS state toward HMI surfaces."),
                ("CLU / IVI", "Expose warning context", "Display surfaces show the selected risk interpretation."),
            ],
            key_contracts=["frmObjectRiskMsg", "frmLaneStateMsg", "frmAdasDomainStateMsg", "selected alert level"],
            key_files=["FCAM.can", "FRADAR.can", "LDR.can", "ADAS.can", "CGW.can"],
            user_outcome="Object-risk interpretation is unified before any warning or assist output is shown to the driver.",
        ),
        ActionFlow(
            flow_id="FLOW_07",
            slug="AEB_DECEL_INTERVENTION",
            title="AEB Decel Intervention",
            category="ADAS",
            summary="AEB stop intent, decel profile, and downstream chassis response are connected as one intervention chain.",
            participants=["FCA", "AEB", "ESC / EHB / VSM", "VCU / SCC", "CGW / CLU"],
            steps=[
                ("FCA", "Trigger collision intent", "Forward collision logic raises the emergency intervention need."),
                ("AEB", "Build intervention profile", "AEB creates stop request, decel profile, and domain health state."),
                ("ESC / EHB / VSM", "Execute braking response", "Chassis intervention readers apply the shared decel profile."),
                ("VCU / SCC", "Adapt longitudinal control", "Vehicle and cruise controllers react to the intervention state."),
                ("CGW / CLU", "Expose intervention outcome", "Display and gateway surfaces reflect the active emergency braking state."),
            ],
            key_contracts=["frmFcaStateMsg", "frmAebDomainStateMsg", "ethDecelAssistReqMsg", "frmBrakeStatusMsg"],
            key_files=["FCA.can", "AEB.can", "ESC.can", "EHB.can", "VCU.can"],
            user_outcome="AEB behavior reads as one intervention story instead of separate ECU reactions.",
        ),
        ActionFlow(
            flow_id="FLOW_08",
            slug="LANE_SURROUND_KEEPING",
            title="Lane and Surround Keeping",
            category="ADAS",
            summary="Lane keeping, blind-spot, and surround sensing work together to support steering and warning decisions.",
            participants=["LDWS_LKAS / LCA / BCW", "SRR_*", "ADAS", "MDPS", "CLU / HUD"],
            steps=[
                ("LDWS_LKAS / LCA / BCW", "Publish lane and surround state", "Lane departure and blind-spot surfaces raise steering-side warnings."),
                ("SRR_*", "Reinforce side context", "Short-range radar confirms adjacent-lane occupancy and movement."),
                ("ADAS", "Select steering-side alert", "ADAS chooses whether steering-related warning or release logic should fire."),
                ("MDPS", "Consume steering-side state", "Steering controller reads the lane/surround state where needed."),
                ("CLU / HUD", "Render lane-side warning", "Cluster and HUD show the selected lane or surround cue."),
            ],
            key_contracts=["frmLaneStateMsg", "frmBlindSpotStateMsg", "frmSteeringStateCanMsg", "warning text code"],
            key_files=["LDWS_LKAS.can", "LCA.can", "BCW.can", "ADAS.can", "MDPS.can"],
            user_outcome="Lane and surround warnings appear as one steering-side assistance behavior.",
        ),
        ActionFlow(
            flow_id="FLOW_09",
            slug="PARKING_SURROUND_ASSIST",
            title="Parking and Surround Assist",
            category="ADAS",
            summary="Parking cameras, ultrasonic sensing, and parking controllers feed one parking-assist behavior chain.",
            participants=["AVM / PUS", "RPC / RRM / PKM", "RSPA / SPAS / SPM", "ADAS", "IVI / CLU"],
            steps=[
                ("AVM / PUS", "Publish parking perception", "Camera and ultrasonic surfaces emit parking scene context."),
                ("RPC / RRM / PKM", "Propagate maneuver state", "Parking controllers and key modules provide maneuver readiness and state."),
                ("RSPA / SPAS / SPM", "Select parking support behavior", "Parking-assist runtimes determine the active surround-assist action."),
                ("ADAS", "Arbitrate with driving state", "ADAS balances parking support against the wider warning context."),
                ("IVI / CLU", "Render maneuver guidance", "Display surfaces show parking or surround-assist status."),
            ],
            key_contracts=["frmParkingStateMsg", "frmUltrasonicStateMsg", "frmCameraStateMsg", "maneuver status"],
            key_files=["AVM.can", "PUS.can", "RPC.can", "RSPA.can", "IVI.can"],
            user_outcome="Parking guidance and surround assistance feel like one guided maneuver story.",
        ),
        ActionFlow(
            flow_id="FLOW_10",
            slug="DRIVER_MONITOR_OCCUPANT",
            title="Driver Monitor and Occupant Risk",
            category="ADAS",
            summary="Driver state and occupant perception are fed into the warning lane before output arbitration happens.",
            participants=["DMS / OMS", "ADAS", "CGW", "CLU / IVI", "AMP"],
            steps=[
                ("DMS / OMS", "Publish human-state context", "Driver and occupant monitoring raise attention and occupancy context."),
                ("ADAS", "Merge human-state risk", "ADAS combines human-state signals with the active warning picture."),
                ("CGW", "Route selected human-state cue", "Gateway exposes the chosen occupant-related warning state."),
                ("CLU / IVI", "Render warning cue", "Visual surfaces show the driver or occupant-related warning meaning."),
                ("AMP", "Render audio cue", "Audio alert follows the selected human-state warning severity."),
            ],
            key_contracts=["frmDriverStateMsg", "frmOccupantStateMsg", "selected alert type", "base volume"],
            key_files=["DMS.can", "OMS.can", "ADAS.can", "CGW.can", "AMP.can"],
            user_outcome="Driver-state and occupant warnings are visible, audible, and consistent with the active context.",
        ),
        ActionFlow(
            flow_id="FLOW_11",
            slug="NAV_ZONE_CONTEXT_INGRESS",
            title="Navigation Zone Context Ingress",
            category="Display and Alert",
            summary="Map and telematics context enters the runtime and becomes zone-aware alert context for downstream selection and HMI.",
            participants=["NAV / TMU", "IVI", "CGW", "ADAS", "CLU / AMP"],
            steps=[
                ("NAV / TMU", "Publish route and zone context", "Navigation and telematics layers raise school-zone, highway, and route context."),
                ("IVI", "Normalize HMI context", "IVI converts map context into one runtime-visible navigation state lane."),
                ("CGW", "Expose context to domain readers", "Gateway forwards the selected navigation context to downstream domains."),
                ("ADAS", "Blend zone context into alerts", "ADAS uses zone context for warning prioritization and speed adjustment."),
                ("CLU / AMP", "Render zone-aware warning", "Cluster and audio surfaces express the selected zone-aware alert."),
            ],
            key_contracts=["frmNavContextCanMsg", "frmNavModuleStateMsg", "frmRoadZoneStateMsg", "selected alert type"],
            key_files=["NAV.can", "TMU.can", "IVI.can", "CGW.can", "ADAS.can"],
            user_outcome="Zone-aware warning behavior is traceable from map context ingress to the final driver cue.",
        ),
        ActionFlow(
            flow_id="FLOW_12",
            slug="V2X_EMERGENCY_INGRESS",
            title="V2X Emergency Ingress",
            category="Display and Alert",
            summary="Emergency-vehicle ingress arrives through the V2X lane and is routed into the warning decision chain.",
            participants=["V2X", "CGW / ETHB", "ADAS", "IVI / CLU", "AMP / HUD"],
            steps=[
                ("V2X", "Receive emergency context", "Emergency vehicle and ETA information enters through the V2X runtime owner."),
                ("CGW / ETHB", "Route backbone visibility", "Backbone and gateway surfaces expose the ingress state to other domains."),
                ("ADAS", "Prioritize emergency warning", "ADAS compares emergency ingress against the current alert picture."),
                ("IVI / CLU", "Render visual alert", "Display surfaces present the prioritized emergency-warning context."),
                ("AMP / HUD", "Emit final urgency cue", "Audio and HUD outputs reinforce the selected emergency alert."),
            ],
            key_contracts=["V2X::v2xFrame", "ETH_EmergencyAlert", "selected alert level", "warning text code"],
            key_files=["V2X.can", "CGW.can", "ADAS.can", "IVI.can", "HUD.can"],
            user_outcome="Emergency-vehicle alerts have a clear ingress point and an explainable output path.",
        ),
        ActionFlow(
            flow_id="FLOW_13",
            slug="ALERT_ARBITRATION_GATE",
            title="Alert Arbitration and Gate",
            category="Display and Alert",
            summary="Multiple warning candidates are reduced into one selected alert with explicit gateway and display semantics.",
            participants=["ADAS", "CGW", "IVI", "CLU", "AMP"],
            steps=[
                ("ADAS", "Select alert candidate", "ADAS reduces zone, risk, and emergency inputs into selected alert type and level."),
                ("CGW", "Apply gate reason", "Gateway stores why the alert was allowed, blocked, or downgraded."),
                ("IVI", "Prepare HMI payload", "IVI converts the selected alert into display and audio-ready forms."),
                ("CLU", "Render cluster meaning", "Cluster uses the selected alert to show the final warning text and icon state."),
                ("AMP", "Render sound priority", "Audio lane follows the same selected alert and base-volume priority."),
            ],
            key_contracts=["Core::selectedAlertType", "Core::selectedAlertLevel", "CoreState::selectedAlertGateReason", "Cluster::warningTextCode"],
            key_files=["ADAS.can", "CGW.can", "IVI.can", "CLU.can", "AMP.can"],
            user_outcome="Only one alert meaning survives to the user-facing surfaces, and the gate reason remains explainable.",
        ),
        ActionFlow(
            flow_id="FLOW_14",
            slug="CLUSTER_HUD_AUDIO_OUTPUT",
            title="Cluster, HUD, and Audio Output",
            category="Display and Alert",
            summary="Selected warning state is rendered into cluster, HUD, and audio output without diverging message semantics.",
            participants=["CGW / IVI", "CLU", "HUD", "AMP", "User"],
            steps=[
                ("CGW / IVI", "Prepare output payload", "Selected alert and supporting context are packaged for visible and audible output."),
                ("CLU", "Render cluster text and icon", "Cluster output turns the alert into the donor-facing warning surface."),
                ("HUD", "Mirror critical cue", "HUD surfaces present only the critical condensed cue."),
                ("AMP", "Render sound level", "Audio lane emits the final alert volume and sound intent."),
                ("User", "Consume synchronized cue", "Driver sees and hears one coherent alert story."),
            ],
            key_contracts=["Cluster::warningTextCode", "Display::steeringFrame", "UiRender::renderVolumLevel", "base volume"],
            key_files=["IVI.can", "CLU.can", "HUD.can", "AMP.can", "CGW.can"],
            user_outcome="Visual and audio warning channels stay aligned instead of competing with each other.",
        ),
        ActionFlow(
            flow_id="FLOW_15",
            slug="SERVICE_ACCESS_HMI",
            title="Service and Access HMI",
            category="Display and Alert",
            summary="Digital-key, payment, OTA, and related service surfaces are orchestrated through one HMI-facing service chain.",
            participants=["DKEY / PAK / CPAY / OTA", "IVI / TMU", "IBOX / CGW", "CLU / RSE / VCS", "User"],
            steps=[
                ("DKEY / PAK / CPAY / OTA", "Raise service surface", "Service-facing runtimes publish access, payment, or update state."),
                ("IVI / TMU", "Normalize service state", "HMI and telematics layers convert service state into one readable lane."),
                ("IBOX / CGW", "Bridge backbone/service context", "Backbone services route the service state to the correct consumer surfaces."),
                ("CLU / RSE / VCS", "Render service-facing UI", "Display surfaces expose the current service or access state."),
                ("User", "Read or act on service state", "The user sees a consistent service and access surface."),
            ],
            key_contracts=["service state", "key presence", "payment context", "OTA readiness"],
            key_files=["DKEY.can", "PAK.can", "CPAY.can", "OTA.can", "IVI.can"],
            user_outcome="Service-facing screens read like one digital-access ecosystem, not isolated widgets.",
        ),
        ActionFlow(
            flow_id="FLOW_16",
            slug="BODY_AMBIENT_WARNING",
            title="Body Ambient Warning Output",
            category="Body and Comfort",
            summary="Body lighting, ambient, wiper, and exterior cues amplify the selected warning state in the comfort domain.",
            participants=["CGW / BCM", "AFLS / AHLS / HLM", "WIP / MIR / SRF", "IVI / CLU", "User"],
            steps=[
                ("CGW / BCM", "Route body-facing alert intent", "Gateway and BCM expose selected warning meaning into the body domain."),
                ("AFLS / AHLS / HLM", "Apply lighting response", "Lighting controllers react to the selected body-facing alert cue."),
                ("WIP / MIR / SRF", "Propagate exterior comfort state", "Exterior comfort ECUs keep the body context visible and synchronized."),
                ("IVI / CLU", "Mirror ambient warning status", "Display surfaces show the same ambient or body warning meaning."),
                ("User", "See ambient reinforcement", "Driver perceives a reinforced warning through body and lighting behavior."),
            ],
            key_contracts=["Body::ambientMode", "Body::blinkLeft", "Body::blinkRight", "frontWiperAnimFrame"],
            key_files=["BCM.can", "AFLS.can", "AHLS.can", "WIP.can", "CLU.can"],
            user_outcome="Ambient and body warning outputs reinforce the selected alert instead of acting independently.",
        ),
        ActionFlow(
            flow_id="FLOW_17",
            slug="ACCESS_SECURITY_ENTRY",
            title="Access, Security, and Entry",
            category="Body and Comfort",
            summary="Key, access, security, and door controllers are connected into one vehicle-entry behavior chain.",
            participants=["DKEY / PAK / PGS", "SMK / BSEC / CSM", "DOOR_*", "BCM", "IVI / User"],
            steps=[
                ("DKEY / PAK / PGS", "Raise access request", "Digital key and passive-entry surfaces publish vehicle-access context."),
                ("SMK / BSEC / CSM", "Validate access state", "Security owners determine whether the entry request is valid."),
                ("DOOR_*", "Apply door action", "Door controllers react to the accepted entry or lock state."),
                ("BCM", "Consolidate body status", "BCM reflects the resulting access and door state across body surfaces."),
                ("IVI / User", "Render entry result", "The user sees one coherent entry and lock result."),
            ],
            key_contracts=["key presence", "door lock state", "entry authorization", "body security state"],
            key_files=["DKEY.can", "PAK.can", "SMK.can", "BSEC.can", "BCM.can"],
            user_outcome="Entry, lock, and security behavior can be read as one access story from request to result.",
        ),
        ActionFlow(
            flow_id="FLOW_18",
            slug="COMFORT_CLIMATE_SEAT",
            title="Comfort, Climate, and Seat",
            category="Body and Comfort",
            summary="Climate and seat controllers are orchestrated as one comfort-domain runtime surface with body and HMI visibility.",
            participants=["DATC / RATC", "SEAT_DRV / SEAT_PASS", "BCM", "IVI / CLU", "User"],
            steps=[
                ("DATC / RATC", "Publish climate state", "Climate controllers expose cabin and rear climate context."),
                ("SEAT_DRV / SEAT_PASS", "Publish seat state", "Seat ECUs provide local comfort and seat status."),
                ("BCM", "Consolidate comfort visibility", "BCM bridges comfort-domain state into shared body visibility."),
                ("IVI / CLU", "Render comfort status", "Display surfaces expose climate and seat state to the user."),
                ("User", "Read comfort readiness", "The user can interpret comfort and climate state from one surface."),
            ],
            key_contracts=["climate state", "seat state", "comfort visibility", "body comfort mode"],
            key_files=["DATC.can", "RATC.can", "SEAT_DRV.can", "SEAT_PASS.can", "BCM.can"],
            user_outcome="Comfort-domain status is discoverable without hunting across separate climate and seat surfaces.",
        ),
        ActionFlow(
            flow_id="FLOW_19",
            slug="VALIDATION_SCENARIO_CONTROL",
            title="Validation Scenario Control",
            category="Validation",
            summary="Scenario command, injected state, and verdict readback are kept inside a dedicated validation control story.",
            participants=["TEST_SCN", "feature owners", "CGW / IVI / CLU", "TEST_BAS", "Engineer"],
            steps=[
                ("TEST_SCN", "Inject scenario command", "Scenario harness writes the exogenous test-world input seams."),
                ("feature owners", "Consume injected state", "Owner ECUs react to the scenario as if it were live runtime input."),
                ("CGW / IVI / CLU", "Expose runtime reaction", "Gateway and HMI surfaces show the resulting runtime behavior."),
                ("TEST_BAS", "Collect verdict summary", "Baseline harness reads back summarized validation state."),
                ("Engineer", "Interpret scenario result", "Scenario result and readback stay explicitly separated from product ownership."),
            ],
            key_contracts=["Test::scenarioCommand", "Test::scenarioActiveId", "Test::scenarioResult", "validation summary seams"],
            key_files=["TEST_SCN.can", "TEST_BAS.can", "CGW.can", "IVI.can", "CLU.can"],
            user_outcome="Validation control remains an explicit harness story instead of leaking into product ownership.",
        ),
        ActionFlow(
            flow_id="FLOW_20",
            slug="BACKBONE_DIAGNOSTIC_SERVICE",
            title="Backbone, Diagnostic, and Service Routing",
            category="Backbone",
            summary="Gateway, backbone, diagnostics, and service-facing surfaces route runtime state without becoming hidden feature owners.",
            participants=["ETHB / IBOX", "CGW / SGW", "DCM / EXT_DIAG / EDR", "IVI / service surfaces", "Engineer / tool"],
            steps=[
                ("ETHB / IBOX", "Bridge backbone state", "Backbone owners surface transport-level service and routing state."),
                ("CGW / SGW", "Route feature visibility", "Gateway lanes expose cross-domain runtime state to the right consumers."),
                ("DCM / EXT_DIAG / EDR", "Handle diagnostic path", "Diagnostic and recorder surfaces maintain the service and evidence chain."),
                ("IVI / service surfaces", "Render service result", "User-facing service surfaces show the routed service outcome."),
                ("Engineer / tool", "Read diagnostic evidence", "Service and diagnostic paths remain explainable from request to readback."),
            ],
            key_contracts=["diagnostic request", "diagnostic response", "gateway state", "service routing state"],
            key_files=["ETHB.can", "IBOX.can", "CGW.can", "DCM.can", "EXT_DIAG.can"],
            user_outcome="Backbone and diagnostic behavior is readable as one routing story instead of scattered support nodes.",
        ),
    ]
    return {flow.flow_id: flow for flow in flows}


ACTION_FLOWS = build_action_flows()
ACTION_FLOW_ORDER = list(ACTION_FLOWS)


def action_flow_filename(flow: ActionFlow) -> str:
    return f"{flow.flow_id}_{flow.slug}_{DATE_STAMP}.svg"


def add_flow_id(target: list[str], *flow_ids: str) -> None:
    for flow_id in flow_ids:
        if flow_id in ACTION_FLOWS and flow_id not in target:
            target.append(flow_id)


def related_action_flow_ids(meta: EcuMeta) -> list[str]:
    ecu = meta.ecu
    domain = meta.domain
    group = meta.group
    flow_ids: list[str] = []

    if group == "GROUP_01_BASE_VEHICLE_DYNAMICS":
        if ecu in {"ESC", "MDPS", "SAS", "RWS", "ADAS", "CGW", "CLU", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_01")
        if ecu in {"AEB", "ABS", "ESC", "EPB", "EHB", "VSM", "VCU", "ADAS", "FCA", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_02")
        if domain == "Powertrain" or ecu in {"VCU", "TCU", "TRM", "CGW", "IVI", "CLU", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_03")
        if ecu in {"SCC", "VCU", "ADAS", "EMS", "TCU", "CGW", "CLU", "IVI", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_04")
        if domain == "Chassis":
            add_flow_id(flow_ids, "FLOW_05")

    if group == "GROUP_02_ADAS_AEB_BRAKE_ASSIST":
        add_flow_id(flow_ids, "FLOW_06")
        if ecu in {"FCA", "AEB", "ESC", "EHB", "VSM", "VCU", "SCC", "ADAS", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_07")
        if ecu in {"LDWS_LKAS", "LCA", "BCW", "SRR_FL", "SRR_FR", "SRR_RL", "SRR_RR", "ADAS", "MDPS", "CLU", "HUD"}:
            add_flow_id(flow_ids, "FLOW_08")
        if ecu in {"AVM", "PUS", "RPC", "RRM", "PKM", "RSPA", "SPAS", "SPM", "ADAS", "IVI", "CLU", "BCM", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_09")
        if ecu in {"DMS", "OMS", "ADAS", "CGW", "CLU", "IVI", "AMP", "TEST_SCN"}:
            add_flow_id(flow_ids, "FLOW_10")

    if group == "GROUP_03_DISPLAY_WARNING_AUDIO":
        if ecu in {"NAV", "TMU", "IVI", "CGW", "ADAS", "CLU", "AMP", "HUD", "VCS", "RSE"}:
            add_flow_id(flow_ids, "FLOW_11")
        if ecu in {"IVI", "CGW", "ADAS", "CLU", "AMP", "HUD", "TMU", "VCS"}:
            add_flow_id(flow_ids, "FLOW_13", "FLOW_14")
        if ecu in {"DKEY", "PAK", "CPAY", "OTA", "PGS", "NAV", "IVI", "TMU", "VCS", "RSE"}:
            add_flow_id(flow_ids, "FLOW_15")

    if group == "GROUP_04_BODY_COMFORT_AMBIENT":
        if ecu in {"BCM", "AFLS", "AHLS", "HLM", "WIP", "SRF", "MIR", "ADM", "BIO", "TGM", "PTG", "MSC", "CGW", "IVI", "CLU"}:
            add_flow_id(flow_ids, "FLOW_16")
        if ecu in {"SMK", "BSEC", "CSM", "DOOR_FL", "DOOR_FR", "DOOR_RL", "DOOR_RR", "BCM", "IVI"}:
            add_flow_id(flow_ids, "FLOW_17")
        if ecu in {"DATC", "RATC", "SEAT_DRV", "SEAT_PASS", "BCM", "IVI", "CLU", "TMU"}:
            add_flow_id(flow_ids, "FLOW_18")

    if group == "GROUP_05_VALIDATION_SCENARIO":
        add_flow_id(flow_ids, "FLOW_19", "FLOW_20")

    if group == "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS":
        add_flow_id(flow_ids, "FLOW_20")
        if ecu in {"V2X", "CGW", "ETHB", "IVI", "ADAS", "CLU", "AMP", "HUD"}:
            add_flow_id(flow_ids, "FLOW_12")
        if ecu in {"CGW", "V2X"}:
            add_flow_id(flow_ids, "FLOW_13")

    if ecu in {"CGW", "ADAS", "CLU"}:
        add_flow_id(flow_ids, "FLOW_01")
    if ecu in {"AEB", "ADAS", "FCA", "ESC", "EHB", "VSM", "VCU", "CGW", "CLU"}:
        add_flow_id(flow_ids, "FLOW_02", "FLOW_07")
    if ecu in {"SCC", "VCU", "ADAS", "CGW", "CLU", "IVI"}:
        add_flow_id(flow_ids, "FLOW_04")
    if ecu in {"CGW", "ADAS", "IVI", "CLU", "AMP"}:
        add_flow_id(flow_ids, "FLOW_11", "FLOW_13")
    if ecu in {"V2X", "CGW", "ETHB", "ADAS", "IVI", "CLU", "AMP", "HUD"}:
        add_flow_id(flow_ids, "FLOW_12")
    if ecu in {"DKEY", "PAK", "PGS", "SMK", "BSEC", "CSM", "DOOR_FL", "DOOR_FR", "DOOR_RL", "DOOR_RR", "BCM", "IVI"}:
        add_flow_id(flow_ids, "FLOW_17")
    if ecu in {"BCM", "CGW", "IVI", "CLU"}:
        add_flow_id(flow_ids, "FLOW_16")

    if ecu in {"CGW", "IVI", "CLU", "AMP"}:
        add_flow_id(flow_ids, "FLOW_14")

    if not flow_ids:
        fallback = {
            "GROUP_01_BASE_VEHICLE_DYNAMICS": "FLOW_03" if domain == "Powertrain" else "FLOW_05",
            "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "FLOW_06",
            "GROUP_03_DISPLAY_WARNING_AUDIO": "FLOW_14",
            "GROUP_04_BODY_COMFORT_AMBIENT": "FLOW_16",
            "GROUP_05_VALIDATION_SCENARIO": "FLOW_19",
            "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "FLOW_20",
        }
        add_flow_id(flow_ids, fallback[group])

    return flow_ids[:4]


def short_list(items: Iterable[str], limit: int) -> list[str]:
    cleaned = [item for item in items if item]
    return cleaned[:limit]


def wrap_lines(text: str, width: int) -> list[str]:
    if not text:
        return ["-"]
    lines: list[str] = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(
            paragraph,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        if wrapped:
            lines.extend(wrapped)
        else:
            lines.append("")
    return lines or ["-"]


def domain_group(domain: str, ecu: str) -> str:
    if ecu in {"TEST_BAS", "TEST_SCN"}:
        return "GROUP_05_VALIDATION_SCENARIO"
    if domain in {"Powertrain", "Chassis"}:
        return "GROUP_01_BASE_VEHICLE_DYNAMICS"
    if domain == "ADAS":
        return "GROUP_02_ADAS_AEB_BRAKE_ASSIST"
    if domain == "Infotainment":
        return "GROUP_03_DISPLAY_WARNING_AUDIO"
    if domain == "Body":
        return "GROUP_04_BODY_COMFORT_AMBIENT"
    return "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS"


def domain_role_hint(domain: str, ecu: str) -> str:
    mapping = {
        "Powertrain": "Powertrain runtime ECU",
        "Chassis": "Chassis runtime ECU",
        "ADAS": "ADAS / sensing runtime ECU",
        "Infotainment": "Display / infotainment runtime ECU",
        "Body": "Body / comfort runtime ECU",
        "ETH_Backbone": "Gateway / backbone / diagnostic runtime ECU",
    }
    if ecu.startswith("DOOR_"):
        return "Door body leaf ECU"
    if ecu.startswith("SEAT_"):
        return "Seat comfort leaf ECU"
    if ecu.startswith("SRR_"):
        return "Radar sensing leaf ECU"
    return mapping.get(domain, "Runtime ECU")


def load_inventory() -> dict[str, list[str]]:
    domains: dict[str, list[str]] = defaultdict(list)
    for path in sorted(CHANNEL_ASSIGN_ROOT.rglob("*.can")):
        if "common" in path.parts:
            continue
        domains[path.parent.name].append(path.stem)
    return {domain: sorted(set(ecus)) for domain, ecus in sorted(domains.items())}


def parse_dbc_contracts() -> dict[str, MessageContract]:
    contracts: dict[str, MessageContract] = {}
    for dbc_path in sorted(DBC_ROOT.glob("*.dbc")):
        current: MessageContract | None = None
        for raw_line in dbc_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line:
                continue

            message_match = MESSAGE_RE.match(line)
            if message_match:
                _, name, _, sender = message_match.groups()
                current = MessageContract(name=name, source=dbc_path.name, sender=sender)
                contracts[name] = current
                continue

            if current is None:
                continue

            signal_match = SIGNAL_RE.match(line)
            if not signal_match:
                continue

            receiver_blob = signal_match.group(2)
            for receiver in receiver_blob.split(","):
                receiver = receiver.strip()
                if receiver and receiver != "Vector__XXX":
                    current.receivers.add(receiver)
    return contracts


def parse_runtime_matrix(contracts: dict[str, MessageContract]) -> None:
    if not OWNERSHIP_MATRIX.exists():
        return
    for line in OWNERSHIP_MATRIX.read_text(encoding="utf-8").splitlines():
        if not TABLE_ROW_RE.match(line) or "---" in line:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        if parts[0] in {"Message", "ID (hex)"}:
            continue
        message, _, _, sender, source = parts[:5]
        if message not in contracts:
            contracts[message] = MessageContract(name=message, source=source, sender=sender)


def collect_test_assets() -> list[str]:
    assets: list[str] = []
    for path in sorted(TEST_UNIT_ROOT.iterdir()):
        if not path.is_dir():
            continue
        if path.name in {"assign", "common", "retire"}:
            continue
        if path.name.startswith("TC_CANOE_"):
            assets.append(path.name)
    return assets


def asset_matches_ecu(asset: str, ecu: str) -> bool:
    pattern = re.compile(rf"(^|_){re.escape(ecu)}($|_)")
    return bool(pattern.search(asset))


def build_metadata() -> list[EcuMeta]:
    domains = load_inventory()
    contracts = parse_dbc_contracts()
    parse_runtime_matrix(contracts)
    assets = collect_test_assets()

    published_by_ecu: dict[str, list[str]] = defaultdict(list)
    consumed_by_ecu: dict[str, list[str]] = defaultdict(list)
    linked_by_ecu: dict[str, set[str]] = defaultdict(set)
    upstream_by_ecu: dict[str, set[str]] = defaultdict(set)
    downstream_by_ecu: dict[str, set[str]] = defaultdict(set)
    dbc_by_ecu: dict[str, set[str]] = defaultdict(set)
    inbound_edges_by_ecu: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    outbound_edges_by_ecu: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    inbound_dbc_by_ecu: dict[str, set[str]] = defaultdict(set)
    outbound_dbc_by_ecu: dict[str, set[str]] = defaultdict(set)

    for contract in contracts.values():
        published_by_ecu[contract.sender].append(contract.name)
        dbc_by_ecu[contract.sender].add(contract.source)
        for receiver in sorted(contract.receivers):
            consumed_by_ecu[receiver].append(contract.name)
            dbc_by_ecu[receiver].add(contract.source)
            inbound_edges_by_ecu[receiver][contract.sender].append(contract.name)
            outbound_edges_by_ecu[contract.sender][receiver].append(contract.name)
            inbound_dbc_by_ecu[receiver].add(contract.source)
            outbound_dbc_by_ecu[contract.sender].add(contract.source)
            if receiver != contract.sender:
                linked_by_ecu[contract.sender].add(receiver)
                linked_by_ecu[receiver].add(contract.sender)
                upstream_by_ecu[receiver].add(contract.sender)
                downstream_by_ecu[contract.sender].add(receiver)

    metadata: list[EcuMeta] = []
    for domain in sorted(domains):
        for ecu in domains[domain]:
            hints = CURATED_HINTS.get(ecu, {})
            group = domain_group(domain, ecu)
            source_capl = f"canoe/src/capl/ecu/{ecu}.can" if (SRC_CAPL_ROOT / "ecu" / f"{ecu}.can").exists() else "-"
            mirror_capl = f"canoe/cfg/channel_assign/{domain}/{ecu}.can" if (CHANNEL_ASSIGN_ROOT / domain / f"{ecu}.can").exists() else "-"
            test_assets = sorted(asset for asset in assets if asset_matches_ecu(asset, ecu))

            metadata.append(
                EcuMeta(
                    ecu=ecu,
                    domain=domain,
                    group=group,
                    source_capl=source_capl,
                    mirror_capl=mirror_capl,
                    role_hint=str(hints.get("role_hint", domain_role_hint(domain, ecu))),
                    owner_seam=list(hints.get("owner_seam", [])),
                    published_contracts=sorted(set(published_by_ecu.get(ecu, []))),
                    consumed_contracts=sorted(set(consumed_by_ecu.get(ecu, []))),
                    linked_ecus=sorted(linked_by_ecu.get(ecu, set())),
                    upstream_ecus=sorted(upstream_by_ecu.get(ecu, set())),
                    downstream_ecus=sorted(downstream_by_ecu.get(ecu, set())),
                    inbound_edges=[
                        f"{sender} :: {', '.join(sorted(set(messages))[:6])}"
                        for sender, messages in sorted(inbound_edges_by_ecu.get(ecu, {}).items())
                    ],
                    outbound_edges=[
                        f"{receiver} :: {', '.join(sorted(set(messages))[:6])}"
                        for receiver, messages in sorted(outbound_edges_by_ecu.get(ecu, {}).items())
                    ],
                    inbound_dbc_sources=sorted(inbound_dbc_by_ecu.get(ecu, set())),
                    outbound_dbc_sources=sorted(outbound_dbc_by_ecu.get(ecu, set())),
                    sysvar_hints=list(hints.get("sysvar_hints", [])),
                    test_assets=test_assets,
                    dbc_sources=sorted(dbc_by_ecu.get(ecu, set())),
                    doc_sources=list(
                        hints.get(
                            "doc_sources",
                            ["0301", "0302", "0303", "0304", "04_SW_Implementation", "ecu-flow-appendix"],
                        )
                    ),
                    current_gap_risk=str(
                        hints.get(
                            "current_gap_risk",
                            "No ECU-specific risk note is curated yet. Use the group overview and official appendix for deeper interpretation.",
                        )
                    ),
                    runtime_note=str(
                        hints.get(
                            "runtime_note",
                            "Use this generated card as the first runtime reading layer, then drop into group view, appendix, and CAPL source.",
                        )
                    ),
                )
            )

    return sorted(metadata, key=lambda item: (item.group, item.domain, item.ecu))


def render_multiline_text(x: int, y: int, lines: list[str], css_class: str, line_height: int = 24) -> str:
    parts = []
    for idx, line in enumerate(lines):
        parts.append(f'<text x="{x}" y="{y + idx * line_height}" class="{css_class}">{escape(line)}</text>')
    return "\n".join(parts)


def clean_items(items: Iterable[str]) -> list[str]:
    return [item.strip() for item in items if item and item.strip() and item.strip() != "-"]


def block_height(lines: list[str], line_height: int, padding: int = 0) -> int:
    return len(lines) * line_height + padding


def render_bullets(items: Iterable[str], width: int = 52) -> list[str]:
    cleaned = clean_items(items)
    if not cleaned:
        return ["-"]
    result: list[str] = []
    for item in cleaned:
        wrapped = wrap_lines(item, width)
        for idx, line in enumerate(wrapped):
            result.append(f"{'- ' if idx == 0 else '  '}{line}")
    return result


def normalize_lines(lines: Iterable[str]) -> list[str]:
    result = list(lines)
    if any(line.strip() for line in result):
        return result
    return ["-"]


def render_section_card(
    x: int,
    y: int,
    width: int,
    title: str,
    lines: Iterable[str],
    *,
    fill: str = "#ffffff",
    css_class: str = "text",
    line_height: int = 22,
) -> tuple[str, int]:
    content_lines = normalize_lines(lines)
    height = max(132, 92 + block_height(content_lines, line_height) + 18)
    return (
        "\n".join(
            [
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="{fill}"/>',
                f'<text x="{x + 22}" y="{y + 36}" class="label">{escape(title)}</text>',
                render_multiline_text(x + 22, y + 70, content_lines, css_class, line_height),
            ]
        ),
        height,
    )


def render_chip_grid_card(
    x: int,
    y: int,
    width: int,
    title: str,
    items: Iterable[str],
    *,
    fill: str = "#ffffff",
    chip_fill: str = "#ffffff",
    chip_stroke: str = "#cbd5e1",
    lead_lines: Iterable[str] | None = None,
) -> tuple[str, int]:
    cleaned = clean_items(items)
    if not cleaned:
        cleaned = ["-"]
    note_lines = normalize_lines(lead_lines or [])
    inner_width = width - 44
    gap = 10
    cols = 4 if width >= 700 else 3
    chip_width = max(120, (inner_width - gap * (cols - 1)) // cols)
    chip_height = 34
    start_y = y + 70 + block_height(note_lines, 20) + 12
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="{fill}"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">{escape(title)}</text>',
        render_multiline_text(x + 22, y + 64, note_lines, "small", 20),
    ]
    for idx, item in enumerate(cleaned):
        row = idx // cols
        col = idx % cols
        chip_x = x + 22 + col * (chip_width + gap)
        chip_y = start_y + row * (chip_height + gap)
        parts.append(
            f'<rect x="{chip_x}" y="{chip_y}" width="{chip_width}" height="{chip_height}" rx="14" ry="14" fill="{chip_fill}" stroke="{chip_stroke}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{chip_x + chip_width / 2:.1f}" y="{chip_y + 22}" text-anchor="middle" class="small">{escape(item)}</text>'
        )
    rows = max(1, (len(cleaned) + cols - 1) // cols)
    height = max(156, start_y - y + rows * (chip_height + gap) + 14)
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), height


def render_dual_list_card(
    x: int,
    y: int,
    width: int,
    title: str,
    left_title: str,
    left_lines: Iterable[str],
    right_title: str,
    right_lines: Iterable[str],
    *,
    fill: str = "#ffffff",
) -> tuple[str, int]:
    left_block = normalize_lines(left_lines)
    right_block = normalize_lines(right_lines)
    inner_width = width - 44
    gap = 24
    col_width = (inner_width - gap) // 2
    top_y = y + 70
    left_height = 34 + block_height(left_block, 18)
    right_height = 34 + block_height(right_block, 18)
    height = max(156, 96 + max(left_height, right_height))
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="{fill}"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">{escape(title)}</text>',
        f'<text x="{x + 22}" y="{top_y}" class="small">{escape(left_title)}</text>',
        render_multiline_text(x + 22, top_y + 28, left_block, "small", 18),
        f'<text x="{x + 22 + col_width + gap}" y="{top_y}" class="small">{escape(right_title)}</text>',
        render_multiline_text(x + 22 + col_width + gap, top_y + 28, right_block, "small", 18),
        f'<line x1="{x + 22 + col_width + gap // 2}" y1="{y + 56}" x2="{x + 22 + col_width + gap // 2}" y2="{y + height - 18}" stroke="#cbd5e1" stroke-width="1.2"/>',
    ]
    return "\n".join(parts), height


def primary_action_flow_ids(meta: EcuMeta) -> list[str]:
    flow_ids = related_action_flow_ids(meta)
    return flow_ids[:2]


def action_flow_members(metadata: list[EcuMeta]) -> dict[str, list[str]]:
    members: dict[str, list[str]] = {flow_id: [] for flow_id in ACTION_FLOW_ORDER}
    for item in metadata:
        for flow_id in related_action_flow_ids(item):
            members.setdefault(flow_id, []).append(item.ecu)
    for flow_id in members:
        members[flow_id] = sorted(set(members[flow_id]))
    return members


def render_action_flow_svg(flow: ActionFlow, members: list[str]) -> str:
    participant_width = 220
    participant_gap = 20
    participant_cols = 4
    participant_rows = max(1, (len(flow.participants) + participant_cols - 1) // participant_cols)
    participant_band_height = 150 + participant_rows * 84

    step_width = 280
    step_gap = 24
    steps_per_row = 3
    step_rows = max(1, (len(flow.steps) + steps_per_row - 1) // steps_per_row)
    step_band_height = 116 + step_rows * 178

    member_lines = render_bullets(members, width=42)
    contract_lines = render_bullets(flow.key_contracts, width=46)
    file_lines = render_bullets(flow.key_files, width=42)
    outcome_lines = wrap_lines(flow.user_outcome, 48)
    footer_height = max(
        320,
        96 + max(block_height(member_lines, 20), block_height(contract_lines, 20), block_height(file_lines + [""] + outcome_lines, 20)),
    )

    total_height = 130 + participant_band_height + step_band_height + footer_height + 120
    participant_y = 120
    step_y = participant_y + participant_band_height + 24
    footer_y = step_y + step_band_height + 24
    accent = group_fill({
        "Dynamics": "GROUP_01_BASE_VEHICLE_DYNAMICS",
        "ADAS": "GROUP_02_ADAS_AEB_BRAKE_ASSIST",
        "Display and Alert": "GROUP_03_DISPLAY_WARNING_AUDIO",
        "Body and Comfort": "GROUP_04_BODY_COMFORT_AMBIENT",
        "Validation": "GROUP_05_VALIDATION_SCENARIO",
        "Backbone": "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS",
    }[flow.category])

    participant_parts: list[str] = []
    for idx, participant in enumerate(flow.participants):
        row = idx // participant_cols
        col = idx % participant_cols
        x = 52 + col * (participant_width + participant_gap)
        y = participant_y + 94 + row * 84
        participant_parts.append(f'<rect x="{x}" y="{y}" width="{participant_width}" height="54" rx="16" ry="16" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>')
        participant_parts.append(f'<text x="{x + 18}" y="{y + 32}" class="node">{escape(participant)}</text>')

    step_parts: list[str] = []
    for idx, step in enumerate(flow.steps):
        row = idx // steps_per_row
        col = idx % steps_per_row
        x = 52 + col * (step_width + step_gap)
        y = step_y + 64 + row * 178
        actor, title, detail = step
        detail_lines = wrap_lines(detail, 32)
        step_parts.append(f'<rect x="{x}" y="{y}" width="{step_width}" height="128" rx="18" ry="18" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>')
        step_parts.append(f'<text x="{x + 20}" y="{y + 28}" class="small">{escape(actor)}</text>')
        step_parts.append(f'<text x="{x + 20}" y="{y + 56}" class="label">{escape(title)}</text>')
        step_parts.append(render_multiline_text(x + 20, y + 84, detail_lines, "text", 20))
        if col < steps_per_row - 1 and idx + 1 < len(flow.steps) and (idx + 1) // steps_per_row == row:
            arrow_y = y + 64
            step_parts.append(f'<line x1="{x + step_width}" y1="{arrow_y}" x2="{x + step_width + step_gap}" y2="{arrow_y}" class="lane"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #f8fafc; }}
    .title {{ font: 700 30px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 14px 'Segoe UI', sans-serif; fill: #475569; }}
    .node {{ font: 700 16px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 20; ry: 20; stroke: #475569; stroke-width: 2; }}
    .lane {{ stroke: #64748b; stroke-width: 3; fill: none; marker-end: url(#arrow); }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">{escape(flow.flow_id)} - {escape(flow.title)}</text>
  <text x="34" y="72" class="sub">{escape(flow.category)} | generated canonical action-flow companion for the internal ECU master book</text>

  <rect x="30" y="100" width="1540" height="{participant_band_height}" class="box" fill="{accent}"/>
  <text x="52" y="136" class="label">Flow overview</text>
  <text x="52" y="166" class="text">{escape(flow.summary)}</text>
  <text x="52" y="202" class="small">Participants</text>
  {"".join(participant_parts)}

  <rect x="30" y="{step_y}" width="1540" height="{step_band_height}" class="box" fill="#ffffff"/>
  <text x="52" y="{step_y + 36}" class="label">Action sequence</text>
  {"".join(step_parts)}

  <rect x="30" y="{footer_y}" width="500" height="{footer_height}" class="box" fill="#eff6ff"/>
  <text x="52" y="{footer_y + 36}" class="label">Related ECU bank</text>
  {render_multiline_text(52, footer_y + 66, member_lines, "text", 20)}

  <rect x="550" y="{footer_y}" width="500" height="{footer_height}" class="box" fill="#ffffff"/>
  <text x="572" y="{footer_y + 36}" class="label">Key contracts</text>
  {render_multiline_text(572, footer_y + 66, contract_lines, "text", 20)}

  <rect x="1070" y="{footer_y}" width="500" height="{footer_height}" class="box" fill="#fff7ed"/>
  <text x="1092" y="{footer_y + 36}" class="label">Files and user outcome</text>
  {render_multiline_text(1092, footer_y + 66, file_lines + [""] + outcome_lines, "text", 20)}
</svg>
"""


def render_action_flow_index(flow_members: dict[str, list[str]]) -> str:
    lines = [
        f"# Action Flow Index ({DATE_STAMP})",
        "",
        "This is the canonical action-flow pack for the internal ECU master book.",
        "Each flow is behavior-first and can be reused by multiple ECU sections in the book.",
        "",
    ]
    by_category: dict[str, list[ActionFlow]] = defaultdict(list)
    for flow_id in ACTION_FLOW_ORDER:
        by_category[ACTION_FLOWS[flow_id].category].append(ACTION_FLOWS[flow_id])
    for category in sorted(by_category):
        lines.extend([f"## {category}", ""])
        for flow in by_category[category]:
            members = flow_members.get(flow.flow_id, [])
            lines.extend(
                [
                    f"### `{flow.flow_id}` {flow.title}",
                    "",
                    f"- SVG: `svg/flows/{action_flow_filename(flow)}`",
                    f"- Related ECU count: `{len(members)}`",
                    f"- Related ECU bank: `{', '.join(members) if members else '-'}`",
                    f"- Summary: {flow.summary}",
                    "",
                ]
            )
    return "\n".join(lines) + "\n"


def render_ecu_flow_matrix(metadata: list[EcuMeta]) -> str:
    lines = [
        f"# ECU Action Flow Matrix ({DATE_STAMP})",
        "",
        "| ECU | Domain | Group | Primary action flow | Supporting action flows |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in metadata:
        related = related_action_flow_ids(item)
        primary = related[0] if related else "-"
        supporting = "<br>".join(related[1:]) if len(related) > 1 else "-"
        lines.append(
            f"| `{item.ecu}` | `{item.domain}` | `{GROUP_LABELS[item.group]}` | `{primary}` | {supporting} |"
        )
    return "\n".join(lines) + "\n"


def card_filename(ecu: str) -> str:
    return f"ECU_CARD_{ecu}_{DATE_STAMP}.svg"


def card_page_filename(ecu: str, page: int) -> str:
    return f"ECU_CARD_{ecu}_{DATE_STAMP}_P{page}.svg"


def prototype_card_filename(ecu: str, version: str = "layout_v2") -> str:
    return f"ECU_CARD_{ecu}_{DATE_STAMP}_{version}.svg"


def group_fill(group: str) -> str:
    palette = {
        "GROUP_01_BASE_VEHICLE_DYNAMICS": "#dbeafe",
        "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "#fee2e2",
        "GROUP_03_DISPLAY_WARNING_AUDIO": "#ede9fe",
        "GROUP_04_BODY_COMFORT_AMBIENT": "#dcfce7",
        "GROUP_05_VALIDATION_SCENARIO": "#fef3c7",
        "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "#fce7f3",
    }
    return palette.get(group, "#e5e7eb")


def summarize_edges(edges: Iterable[str], limit: int | None = None) -> list[str]:
    cleaned = clean_items(edges)
    if limit is None or len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit]


def split_edge(edge: str) -> tuple[str, str]:
    if "::" in edge:
        ecu, payload = edge.split("::", 1)
        return ecu.strip(), payload.strip()
    return edge.strip(), "-"


def render_edge_column(x: int, y: int, width: int, title: str, edges: Iterable[str], fill: str) -> tuple[str, int]:
    rendered_edges = summarize_edges(edges, limit=None)
    column_gap = 12
    inner_width = width - 28
    column_width = (inner_width - column_gap) // 2
    column_y = [y + 58, y + 58]
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" rx="18" ry="18" class="box" fill="{fill}"/>',
        f'<text x="{x + 24}" y="{y + 36}" class="label">{escape(title)}</text>',
    ]
    if not rendered_edges:
        rendered_edges = ["- :: no direct DBC edge extracted"]
    for edge in rendered_edges:
        ecu, payload = split_edge(edge)
        payload_lines = wrap_lines(payload, width=18)
        card_height = 48 + len(payload_lines) * 18
        col = 0 if column_y[0] <= column_y[1] else 1
        card_x = x + 14 + col * (column_width + column_gap)
        card_y = column_y[col]
        parts.append(
            f'<rect x="{card_x}" y="{card_y}" width="{column_width}" height="{card_height}" rx="16" ry="16" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>'
        )
        parts.append(f'<text x="{card_x + 16}" y="{card_y + 26}" class="node">{escape(ecu)}</text>')
        parts.append(render_multiline_text(card_x + 16, card_y + 48, payload_lines, "small", 18))
        column_y[col] += card_height + 12

    total_height = max(220, max(column_y) - y + 6)
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{total_height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), total_height


def render_edge_grid_section(x: int, y: int, width: int, title: str, edges: Iterable[str], fill: str) -> tuple[str, int]:
    rendered_edges = summarize_edges(edges, limit=None)
    if not rendered_edges:
        rendered_edges = ["- :: no direct DBC edge extracted"]
    inner_width = width - 28
    cols = 3 if width >= 700 else 2
    gap = 12
    card_width = (inner_width - gap * (cols - 1)) // cols
    cursor_y = [y + 58 for _ in range(cols)]
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="{fill}"/>',
        f'<text x="{x + 24}" y="{y + 36}" class="label">{escape(title)}</text>',
    ]
    for edge in rendered_edges:
        ecu, payload = split_edge(edge)
        payload_lines = wrap_lines(payload, width=18)
        card_height = 48 + len(payload_lines) * 18
        col = min(range(cols), key=lambda idx: cursor_y[idx])
        card_x = x + 14 + col * (card_width + gap)
        card_y = cursor_y[col]
        parts.append(
            f'<rect x="{card_x}" y="{card_y}" width="{card_width}" height="{card_height}" rx="16" ry="16" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.4"/>'
        )
        parts.append(f'<text x="{card_x + 16}" y="{card_y + 26}" class="node">{escape(ecu)}</text>')
        parts.append(render_multiline_text(card_x + 16, card_y + 48, payload_lines, "small", 18))
        cursor_y[col] += card_height + 12
    total_height = max(220, max(cursor_y) - y + 6)
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{total_height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), total_height


def render_metric_tile(
    x: int,
    y: int,
    width: int,
    title: str,
    value: str,
    *,
    fill: str = "#ffffff",
) -> str:
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="82" rx="18" ry="18" fill="{fill}" stroke="#cbd5e1" stroke-width="1.2"/>',
            f'<text x="{x + 18}" y="{y + 28}" class="small">{escape(title)}</text>',
            f'<text x="{x + 18}" y="{y + 58}" class="node">{escape(value)}</text>',
        ]
    )


def render_metadata_note_tile(
    x: int,
    y: int,
    width: int,
    title: str,
    lines: Iterable[str],
    *,
    fill: str = "#ffffff",
    height: int | None = None,
) -> str:
    content_lines = normalize_lines(lines)
    tile_height = height or max(102, 48 + block_height(content_lines, 18) + 16)
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="{tile_height}" rx="18" ry="18" fill="{fill}" stroke="#cbd5e1" stroke-width="1.2"/>',
            f'<text x="{x + 18}" y="{y + 28}" class="small">{escape(title)}</text>',
            render_multiline_text(x + 18, y + 54, content_lines, "small", 18),
        ]
    )


def render_overview_metadata_strip(
    x: int,
    y: int,
    width: int,
    *,
    meta: EcuMeta,
) -> tuple[str, int]:
    published = clean_items(meta.published_contracts)
    consumed = clean_items(meta.consumed_contracts)
    key_test = clean_items(meta.test_assets)
    tiles = [
        (
            "Key seam",
            wrap_lines(clean_items(meta.owner_seam)[0] if clean_items(meta.owner_seam) else "-", 28)[:3],
            "#ffffff",
        ),
        (
            "Runtime contract",
            [
                f"Publish: {compact_label(published[0], 28)}" if published else "Publish: -",
                f"Consume: {compact_label(consumed[0], 28)}" if consumed else "Consume: -",
            ],
            "#ffffff",
        ),
        (
            "Verification",
            wrap_lines(key_test[0] if key_test else "No direct test asset", 28)[:3],
            "#ffffff",
        ),
        (
            "Risk focus",
            wrap_lines(ecu_risk_focus(meta), 28)[:3],
            "#fff7ed",
        ),
    ]
    inner_x = x + 22
    inner_w = width - 44
    gap = 14
    tile_width = (inner_w - gap * 3) // 4
    tile_y = y + 54
    tile_height = max(104, max(48 + block_height(lines, 18) + 16 for _, lines, _ in tiles))
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{tile_height + 76}" class="box" fill="#ffffff"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">ECU metadata</text>',
    ]
    for idx, (title, lines, fill) in enumerate(tiles):
        tile_x = inner_x + idx * (tile_width + gap)
        parts.append(
            render_metadata_note_tile(
                tile_x,
                tile_y,
                tile_width,
                title,
                lines,
                fill=fill,
                height=tile_height,
            )
        )
    return "\n".join(parts), tile_height + 76


def unique_edge_ecus(edges: Iterable[str]) -> list[str]:
    seen: list[str] = []
    for edge in summarize_edges(edges, limit=None):
        ecu, _ = split_edge(edge)
        if ecu not in seen:
            seen.append(ecu)
    return seen


def external_edge_ecus(edges: Iterable[str], self_ecu: str) -> list[str]:
    return [ecu for ecu in unique_edge_ecus(edges) if ecu != self_ecu]


def domain_label(domain: str) -> str:
    return {
        "ETH_Backbone": "Backbone",
        "Infotainment": "Display",
    }.get(domain, domain)


def clustered_actor_labels(items: Iterable[str], limit: int = 6) -> list[str]:
    counter: Counter[str] = Counter()
    for ecu in clean_items(items):
        domain = ECU_DOMAIN_LOOKUP.get(ecu, "Unknown")
        counter[domain_label(domain)] += 1
    if not counter:
        return ["-"]
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    labels = [f"{name} · {count}" for name, count in ranked]
    if len(labels) <= limit:
        return labels
    overflow = len(labels) - limit
    return labels[:limit] + [f"+{overflow} more"]


def preview_items(
    items: list[str],
    limit: int = 6,
    noun: str = "actors",
    *,
    show_overflow_note: bool = True,
) -> tuple[list[str], str | None]:
    if len(items) <= limit:
        return items, None
    return items[:limit], f"+{len(items) - limit} more" if show_overflow_note else None


def preview_bullet_lines(
    items: Iterable[str],
    width: int,
    limit: int = 3,
    noun: str = "items",
    *,
    show_overflow_note: bool = True,
) -> list[str]:
    cleaned = clean_items(items)
    if not cleaned:
        return ["-"]
    preview, overflow_note = preview_items(cleaned, limit=limit, noun=noun, show_overflow_note=show_overflow_note)
    lines = render_bullets(preview, width=width)
    if overflow_note:
        lines.extend(["", overflow_note])
    return lines


def preview_chip_items(items: Iterable[str], limit: int = 4, transform=None) -> list[str]:
    cleaned = clean_items(items)
    if transform is not None:
        cleaned = [transform(item) for item in cleaned]
    cleaned = [item for item in cleaned if item and item.strip()]
    if not cleaned:
        return ["-"]
    if len(cleaned) <= limit:
        return cleaned
    overflow = len(cleaned) - limit
    return cleaned[:limit] + [f"+{overflow} more"]


def compact_label(text: str, max_len: int = 26) -> str:
    cleaned = " ".join(text.replace("\\", "/").split())
    if len(cleaned) <= max_len:
        return cleaned
    return f"{cleaned[: max_len - 1]}…"


def short_path_label(path: str) -> str:
    normalized = path.replace("\\", "/")
    return compact_label(Path(normalized).name or normalized, max_len=24)


def function_statement(meta: EcuMeta) -> str:
    curated = CURATED_FUNCTION_STATEMENTS.get(meta.ecu, "").strip()
    if curated:
        return curated.rstrip(".")
    note = " ".join(meta.runtime_note.split()).strip().rstrip(".")
    if note and not note.startswith("Use this generated"):
        return note
    return f"Curation required for {meta.ecu}"


def ecu_risk_focus(meta: EcuMeta) -> str:
    curated = CURATED_RISK_NOTES.get(meta.ecu, "").strip()
    if curated:
        return curated.rstrip(".")
    return meta.current_gap_risk


def statement_headline(statement: str) -> str:
    normalized = " ".join(statement.split()).strip().rstrip(".")
    for token in (" so ", " to ", " for "):
        if token in normalized:
            head = normalized.split(token, 1)[0].strip()
            if head:
                return head
    return normalized


def render_card_layout_v2(meta: EcuMeta) -> str:
    margin = 30
    gutter = 20
    column = 110

    def grid_x(col_idx: int) -> int:
        return margin + col_idx * (column + gutter)

    def grid_w(span: int) -> int:
        return span * column + (span - 1) * gutter

    title = f"ECU Design Study - {meta.ecu}"
    group_label = GROUP_LABELS[meta.group]
    group_color = group_fill(meta.group)
    flow_ids = related_action_flow_ids(meta)
    primary_flow = ACTION_FLOWS[flow_ids[0]] if flow_ids else None
    supporting_flows = [ACTION_FLOWS[flow_id] for flow_id in flow_ids[1:]]
    role = wrap_lines(meta.role_hint, 34)
    primary_flow_lines = wrap_lines(
        f"{primary_flow.flow_id} {primary_flow.title}" if primary_flow else "-",
        38,
    )
    owner_preview = wrap_lines(meta.owner_seam[0] if meta.owner_seam else "-", 34)
    signal_src, _, signal_dst, _ = representative_signal_path(meta)
    signal_route = (
        f"{signal_src} -> {meta.ecu} -> {signal_dst}"
        if signal_src and signal_dst
        else f"{signal_src} -> {meta.ecu}"
        if signal_src
        else f"{meta.ecu} -> {signal_dst}"
        if signal_dst
        else "No representative signal route extracted"
    )
    signal_route_lines = wrap_lines(signal_route, 40)

    hero_y = 100
    hero_left_x = grid_x(0)
    hero_left_w = grid_w(7)
    hero_right_x = grid_x(7)
    hero_right_w = grid_w(5)
    hero_left_lines = (
        [f"{group_label} | {meta.domain}"]
        + [""]
        + role
        + [""]
        + ["Primary action flow"]
        + primary_flow_lines
        + [""]
        + ["Signal route"]
        + signal_route_lines
    )
    hero_height = max(240, 88 + block_height(hero_left_lines, 20))
    tile_gap = 12
    tile_width = (hero_right_w - tile_gap) // 2
    tile_x1 = hero_right_x
    tile_x2 = hero_right_x + tile_width + tile_gap
    tile_y1 = hero_y + 34
    tile_y2 = tile_y1 + 94
    tile_y3 = tile_y2 + 94
    hero_parts = [
        f'<rect x="{margin}" y="{hero_y}" width="{grid_w(12)}" height="{hero_height}" class="box" fill="{group_color}"/>',
        f'<text x="{hero_left_x + 22}" y="{hero_y + 34}" class="small">ECU at a glance</text>',
        f'<text x="{hero_left_x + 22}" y="{hero_y + 72}" class="title">{escape(meta.ecu)}</text>',
        render_multiline_text(hero_left_x + 22, hero_y + 104, hero_left_lines, "text", 20),
        render_metric_tile(tile_x1, tile_y1, tile_width, "Published", str(len(meta.published_contracts)), fill="#ffffff"),
        render_metric_tile(tile_x2, tile_y1, tile_width, "Consumed", str(len(meta.consumed_contracts)), fill="#ffffff"),
        render_metric_tile(tile_x1, tile_y2, tile_width, "Linked ECU", str(len(meta.linked_ecus)), fill="#ffffff"),
        render_metric_tile(tile_x2, tile_y2, tile_width, "Native Tests", str(len(meta.test_assets)), fill="#ffffff"),
        render_metric_tile(tile_x1, tile_y3, tile_width, "Upstream", str(len(meta.upstream_ecus)), fill="#ffffff"),
        render_metric_tile(tile_x2, tile_y3, tile_width, "Downstream", str(len(meta.downstream_ecus)), fill="#ffffff"),
    ]
    hero_svg = "\n".join(hero_parts)

    flow_y = hero_y + hero_height + 24
    inbound_svg, inbound_height = render_edge_grid_section(grid_x(0), flow_y, grid_w(6), "Inbound Flow", meta.inbound_edges, "#e0f2fe")
    outbound_svg, outbound_height = render_edge_grid_section(grid_x(6), flow_y, grid_w(6), "Outbound Flow", meta.outbound_edges, "#dbeafe")

    published_contracts = render_bullets(meta.published_contracts, width=30)
    consumed_contracts = render_bullets(meta.consumed_contracts, width=30)
    row2_y = flow_y + max(inbound_height, outbound_height) + 24
    linked_lead = [
        f"Primary flow: {primary_flow.flow_id if primary_flow else '-'}",
        f"Support flow count: {len(supporting_flows)}",
    ]
    linked_svg, linked_height = render_chip_grid_card(
        grid_x(0),
        row2_y,
        grid_w(5),
        "Linked ECU bank",
        meta.linked_ecus,
        fill="#eff6ff",
        chip_fill="#ffffff",
        chip_stroke="#bfdbfe",
        lead_lines=linked_lead,
    )
    contract_svg, contract_height = render_dual_list_card(
        grid_x(5),
        row2_y,
        grid_w(7),
        "Contract inventory",
        f"Published ({len(meta.published_contracts)})",
        published_contracts,
        f"Consumed ({len(meta.consumed_contracts)})",
        consumed_contracts,
        fill="#ffffff",
    )

    metadata_block = (
        [f"Layer / Group: {meta.domain} / {group_label}"]
        + [""]
        + ["Owner seam"]
        + render_bullets(meta.owner_seam, width=36)
        + [""]
        + ["Sysvar hints"]
        + render_bullets(meta.sysvar_hints, width=36)
    )
    evidence_block = (
        ["Direct native tests"]
        + render_bullets(meta.test_assets, width=42)
        + [""]
        + ["Files"]
        + render_bullets([meta.source_capl, meta.mirror_capl], width=42)
        + [""]
        + ["Doc source"]
        + render_bullets(meta.doc_sources, width=40)
    )
    row3_y = row2_y + max(linked_height, contract_height) + 24
    metadata_svg, metadata_height = render_section_card(grid_x(0), row3_y, grid_w(6), "Metadata anchors", metadata_block, fill="#f8fafc")
    evidence_svg, evidence_height = render_section_card(grid_x(6), row3_y, grid_w(6), "Evidence and reading anchors", evidence_block, fill="#ffffff")

    note_lines = (
        [f"Primary flow: {primary_flow.flow_id} {primary_flow.title}" if primary_flow else "Primary flow: -"]
        + [f"Supporting flow: {flow.flow_id} {flow.title}" for flow in supporting_flows]
        + [""]
        + wrap_lines(ecu_risk_focus(meta), 110)
        + [""]
        + wrap_lines(meta.runtime_note, 110)
        + [""]
        + ["Owner seam preview"]
        + owner_preview
    )
    row4_y = row3_y + max(metadata_height, evidence_height) + 24
    notes_svg, notes_height = render_section_card(grid_x(0), row4_y, grid_w(12), "Review notes and action map", note_lines, fill="#fff7ed")

    total_height = row4_y + notes_height + 50

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{group_color}"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
  </defs>
  <style>
    .bg {{ fill: #f7f7f5; }}
    .title {{ font: 700 32px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 13px 'Segoe UI', sans-serif; fill: #475569; }}
    .node {{ font: 700 18px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 22; ry: 22; stroke: #334155; stroke-width: 1.6; }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">{escape(title)}</text>
  <text x="34" y="72" class="sub">12-column internal card exploration | consulting-style SVG prototype</text>
  {hero_svg.replace(f'fill="{group_color}"', 'fill="url(#heroGradient)"', 1)}
  {inbound_svg}
  {outbound_svg}
  {linked_svg}
  {contract_svg}
  {metadata_svg}
  {evidence_svg}
  {notes_svg}
</svg>
"""


def render_story_stage_card(
    x: int,
    y: int,
    width: int,
    title: str,
    actors: list[str],
    note: str,
    fill: str,
) -> tuple[str, int]:
    preview, overflow_note = preview_items(actors, limit=4, noun="actors", show_overflow_note=False)
    lead_lines = [note]
    if overflow_note:
        lead_lines.append(overflow_note)
    card_svg, height = render_chip_grid_card(
        x,
        y,
        width,
        title,
        preview if preview else ["-"],
        fill=fill,
        chip_fill="#ffffff",
        chip_stroke="#cbd5e1",
        lead_lines=lead_lines,
    )
    return card_svg, height


def render_processing_stage_card(
    x: int,
    y: int,
    width: int,
    meta: EcuMeta,
    role_lines: list[str],
    owner_preview: list[str],
    primary_flow_lines: list[str],
    fill: str,
) -> tuple[str, int]:
    consumes_lines = preview_bullet_lines(meta.consumed_contracts, width=44, limit=3, noun="contracts", show_overflow_note=False)
    publishes_lines = preview_bullet_lines(meta.published_contracts, width=44, limit=3, noun="contracts", show_overflow_note=False)
    process_lines = normalize_lines(role_lines + [""] + ["Owner seam"] + owner_preview + [""] + ["Primary flow"] + primary_flow_lines)

    inner_x = x + 22
    inner_w = width - 44
    panel_gap = 12
    panels: list[tuple[str, list[str], str]] = [
        (f"Consumes / reads ({len(clean_items(meta.consumed_contracts))})", consumes_lines, "#ffffff"),
        ("Processes / decides", process_lines, "#f8fafc"),
        (f"Publishes / routes ({len(clean_items(meta.published_contracts))})", publishes_lines, "#ffffff"),
    ]
    cursor_y = y + 94
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="{fill}"/>',
        f'<text x="{x + 22}" y="{y + 34}" class="small">ECU processing stage</text>',
        f'<text x="{x + width / 2:.1f}" y="{y + 72}" text-anchor="middle" class="title">{escape(meta.ecu)}</text>',
    ]
    for panel_title, panel_lines, panel_fill in panels:
        height = max(88, 54 + block_height(panel_lines, 18) + 16)
        parts.extend(
            [
                f'<rect x="{inner_x}" y="{cursor_y}" width="{inner_w}" height="{height}" rx="18" ry="18" fill="{panel_fill}" stroke="#bbf7d0" stroke-width="1.2"/>',
                f'<text x="{inner_x + 18}" y="{cursor_y + 28}" class="small">{escape(panel_title)}</text>',
                render_multiline_text(inner_x + 18, cursor_y + 54, panel_lines, "small", 18),
            ]
        )
        cursor_y += height + panel_gap
    total_height = cursor_y - y + 10
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{total_height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), total_height


def render_quick_snapshot_card(
    x: int,
    y: int,
    width: int,
    *,
    primary_flow: ActionFlow | None,
    supporting_flows: list[ActionFlow],
    owner_seams: list[str],
    test_assets: list[str],
    source_files: list[str],
    doc_sources: list[str],
    sysvar_hints: list[str],
) -> tuple[str, int]:
    inner_x = x + 22
    inner_w = width - 44
    tile_gap = 12
    tile_width = (inner_w - tile_gap) // 2
    tile_height = 82
    tile_y1 = y + 62
    tile_y2 = tile_y1 + tile_height + 12
    support_count = len(supporting_flows)
    key_seam = compact_label(clean_items(owner_seams)[0], 54) if clean_items(owner_seams) else "-"
    key_test = compact_label(clean_items(test_assets)[0], 54) if clean_items(test_assets) else "No direct test asset"
    source_pack = f"{len([item for item in clean_items(source_files) if item != '-'])} CAPL / {len(clean_items(doc_sources))} docs"
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="#ffffff"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">Reference snapshot</text>',
        render_metric_tile(inner_x, tile_y1, tile_width, "Flows", str(1 + len(supporting_flows) if primary_flow else len(supporting_flows)), fill="#f8fafc"),
        render_metric_tile(inner_x + tile_width + tile_gap, tile_y1, tile_width, "Owner seams", str(len(clean_items(owner_seams))), fill="#f8fafc"),
        render_metric_tile(inner_x, tile_y2, tile_width, "Sysvars", str(len(clean_items(sysvar_hints))), fill="#f8fafc"),
        render_metric_tile(inner_x + tile_width + tile_gap, tile_y2, tile_width, "Tests", str(len(clean_items(test_assets))), fill="#f8fafc"),
    ]

    snapshot_rows = [
        ("Primary flow", primary_flow.flow_id if primary_flow else "-"),
        ("Support pack", f"{support_count} supporting flows"),
        ("Key seam", key_seam),
        ("Verification", key_test),
        ("Source pack", source_pack),
    ]
    cursor_y = tile_y2 + tile_height + 22
    chip_height = 34
    for section_title, value in snapshot_rows:
        parts.append(f'<text x="{inner_x}" y="{cursor_y}" class="small">{escape(section_title)}</text>')
        cursor_y += 14
        parts.extend(
            [
                f'<rect x="{inner_x}" y="{cursor_y}" width="{inner_w}" height="{chip_height}" rx="14" ry="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>',
                f'<text x="{inner_x + 14}" y="{cursor_y + 22}" class="small">{escape(value)}</text>',
            ]
        )
        cursor_y += chip_height + 14
    height = max(248, cursor_y - y + 8)
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="#ffffff"/>'
    return "\n".join(parts), height


def render_action_rail_card(
    x: int,
    y: int,
    width: int,
    *,
    meta: EcuMeta,
    primary_flow: ActionFlow | None,
) -> tuple[str, int]:
    inbound_actors = external_edge_ecus(meta.inbound_edges, meta.ecu)
    outbound_actors = external_edge_ecus(meta.outbound_edges, meta.ecu)
    reads = preview_chip_items(inbound_actors, limit=4, transform=lambda item: compact_label(item, 18))
    writes = preview_chip_items(outbound_actors, limit=4, transform=lambda item: compact_label(item, 18))
    owner = preview_chip_items(meta.owner_seam, limit=2, transform=lambda item: compact_label(item, 24))
    headline = compact_label(statement_headline(function_statement(meta)), 28)

    inner_x = x + 22
    inner_w = width - 44
    card_gap = 22
    card_w = (inner_w - card_gap * 2) // 3
    card_y = y + 66
    card_h = 188
    card_xs = [inner_x, inner_x + card_w + card_gap, inner_x + (card_w + card_gap) * 2]

    cards = [
        (
            "Inbound",
            f"{len(inbound_actors)} upstream actor / {len(clean_items(meta.consumed_contracts))} reads",
            reads,
            "#e0f2fe",
            "#bfdbfe",
        ),
        (
            "ECU Core",
            compact_label(primary_flow.flow_id if primary_flow else "No primary flow", 28),
            [headline] + owner,
            "#dcfce7",
            "#86efac",
        ),
        (
            "Outbound",
            f"{len(outbound_actors)} downstream actor / {len(clean_items(meta.published_contracts))} writes",
            writes,
            "#dbeafe",
            "#93c5fd",
        ),
    ]

    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="#ffffff"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">Action rail</text>',
    ]
    for idx, (title, subtitle, items, fill, stroke) in enumerate(cards):
        cx = card_xs[idx]
        parts.extend(
            [
                f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="20" ry="20" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>',
                f'<text x="{cx + 18}" y="{card_y + 30}" class="small">{escape(title)}</text>',
                f'<text x="{cx + 18}" y="{card_y + 56}" class="text">{escape(subtitle)}</text>',
            ]
        )
        chip_gap = 10
        chip_w = (card_w - 36 - chip_gap) // 2
        chip_y = card_y + 84
        normalized = items if items else ["-"]
        for item_idx, item in enumerate(normalized[:4]):
            row = item_idx // 2
            col = item_idx % 2
            chip_x = cx + 18 + col * (chip_w + chip_gap)
            chip_row_y = chip_y + row * 44
            parts.extend(
                [
                    f'<rect x="{chip_x}" y="{chip_row_y}" width="{chip_w}" height="34" rx="14" ry="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>',
                    f'<text x="{chip_x + chip_w / 2:.1f}" y="{chip_row_y + 22}" text-anchor="middle" class="small">{escape(item)}</text>',
                ]
            )
    arrow_y = card_y + card_h / 2
    parts.extend(
        [
            f'<line x1="{card_xs[0] + card_w}" y1="{arrow_y}" x2="{card_xs[1]}" y2="{arrow_y}" class="lane"/>',
            f'<line x1="{card_xs[1] + card_w}" y1="{arrow_y}" x2="{card_xs[2]}" y2="{arrow_y}" class="lane"/>',
        ]
    )
    height = card_y + card_h - y + 22
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="#ffffff"/>'
    return "\n".join(parts), height


def render_network_footprint_card(
    x: int,
    y: int,
    width: int,
    *,
    meta: EcuMeta,
    title: str = "Network footprint",
    fill: str = "#eff6ff",
) -> tuple[str, int]:
    upstream = clean_items(meta.upstream_ecus)
    downstream = clean_items(meta.downstream_ecus)
    peers = sorted(set(clean_items(meta.linked_ecus)) - set(upstream) - set(downstream))
    groups = [
        ("Upstream", upstream, "#e0f2fe", "#bfdbfe"),
        ("Peer / linked", peers, "#f8fafc", "#cbd5e1"),
        ("Downstream", downstream, "#dbeafe", "#93c5fd"),
    ]

    inner_x = x + 22
    inner_w = width - 44
    group_gap = 18
    group_w = (inner_w - group_gap * 2) // 3
    group_y = y + 66
    chip_gap = 10
    chip_h = 34
    chip_cols = 2
    chip_w = (group_w - 36 - chip_gap) // chip_cols

    group_heights: list[int] = []
    for _, items, _, _ in groups:
        visible = clustered_actor_labels(items, limit=4)
        rows = max(1, (len(visible) + chip_cols - 1) // chip_cols)
        group_heights.append(92 + rows * chip_h + max(0, rows - 1) * chip_gap)
    group_h = max(154, max(group_heights))

    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="{fill}"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">{escape(title)}</text>',
    ]
    group_xs = [inner_x, inner_x + group_w + group_gap, inner_x + (group_w + group_gap) * 2]
    for idx, (group_title, items, group_fill, stroke) in enumerate(groups):
        gx = group_xs[idx]
        visible = clustered_actor_labels(items, limit=4)
        parts.extend(
            [
                f'<rect x="{gx}" y="{group_y}" width="{group_w}" height="{group_h}" rx="20" ry="20" fill="{group_fill}" stroke="{stroke}" stroke-width="1.4"/>',
                f'<text x="{gx + 18}" y="{group_y + 28}" class="small">{escape(group_title)}</text>',
                f'<text x="{gx + 18}" y="{group_y + 56}" class="node">{len(items)}</text>',
                f'<text x="{gx + 88}" y="{group_y + 56}" class="small">Domain clusters</text>',
            ]
        )
        chip_start_y = group_y + 74
        for item_idx, item in enumerate(visible):
            row = item_idx // chip_cols
            col = item_idx % chip_cols
            chip_x = gx + 18 + col * (chip_w + chip_gap)
            chip_y = chip_start_y + row * (chip_h + chip_gap)
            parts.extend(
                [
                    f'<rect x="{chip_x}" y="{chip_y}" width="{chip_w}" height="{chip_h}" rx="14" ry="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.1"/>',
                    f'<text x="{chip_x + chip_w / 2:.1f}" y="{chip_y + 22}" text-anchor="middle" class="small">{escape(item)}</text>',
                ]
            )

    arrow_y = group_y + group_h / 2
    parts.extend(
        [
            f'<line x1="{group_xs[0] + group_w}" y1="{arrow_y}" x2="{group_xs[1]}" y2="{arrow_y}" class="lane"/>',
            f'<line x1="{group_xs[1] + group_w}" y1="{arrow_y}" x2="{group_xs[2]}" y2="{arrow_y}" class="lane"/>',
        ]
    )
    height = group_y + group_h - y + 22
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), height


def render_statement_card(x: int, y: int, width: int, statement: str) -> tuple[str, int]:
    lines = wrap_lines(statement, 44)
    height = max(132, 88 + block_height(lines, 28))
    return (
        "\n".join(
            [
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="#fff7ed"/>',
                f'<text x="{x + 22}" y="{y + 34}" class="small">What this ECU does</text>',
                render_multiline_text(x + 22, y + 78, lines, "statement", 28),
            ]
        ),
        height,
    )


def render_mini_function_diagram(
    x: int,
    y: int,
    width: int,
    *,
    ecu: str,
    statement: str,
    inbound_actors: list[str],
    outbound_actors: list[str],
) -> tuple[str, int]:
    height = 180
    inner_x = x + 22
    card_gap = 18
    card_width = (width - 44 - card_gap * 2) // 3
    box_y = y + 66
    headline = statement_headline(statement)
    titles = ["Input", "ECU", "Output"]
    values = [
        f"{len(inbound_actors)} inbound",
        ecu,
        f"{len(outbound_actors)} outbound",
    ]
    captions = [
        compact_label(", ".join(inbound_actors[:2]) if inbound_actors else "-", 22),
        compact_label(headline, 22),
        compact_label(", ".join(outbound_actors[:2]) if outbound_actors else "-", 22),
    ]
    fills = ["#e0f2fe", "#dcfce7", "#dbeafe"]
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="box" fill="#ffffff"/>',
        f'<text x="{x + 22}" y="{y + 34}" class="small">Interaction sketch</text>',
    ]
    xs = [inner_x, inner_x + card_width + card_gap, inner_x + (card_width + card_gap) * 2]
    for idx, box_x in enumerate(xs):
        parts.extend(
            [
                f'<rect x="{box_x}" y="{box_y}" width="{card_width}" height="88" rx="18" ry="18" fill="{fills[idx]}" stroke="#cbd5e1" stroke-width="1.2"/>',
                f'<text x="{box_x + 18}" y="{box_y + 26}" class="small">{titles[idx]}</text>',
                f'<text x="{box_x + 18}" y="{box_y + 52}" class="node">{escape(values[idx])}</text>',
                f'<text x="{box_x + 18}" y="{box_y + 74}" class="small">{escape(captions[idx])}</text>',
            ]
        )
    parts.extend(
        [
            f'<line x1="{xs[0] + card_width}" y1="{box_y + 44}" x2="{xs[1]}" y2="{box_y + 44}" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>',
            f'<line x1="{xs[1] + card_width}" y1="{box_y + 44}" x2="{xs[2]}" y2="{box_y + 44}" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>',
        ]
    )
    return "\n".join(parts), height


def render_card_detail_page(meta: EcuMeta, page_number: int = 2) -> str:
    margin = 30
    gutter = 20
    column = 110

    def grid_x(col_idx: int) -> int:
        return margin + col_idx * (column + gutter)

    def grid_w(span: int) -> int:
        return span * column + (span - 1) * gutter

    group_label = GROUP_LABELS[meta.group]
    group_color = group_fill(meta.group)
    flow_ids = related_action_flow_ids(meta)
    primary_flow = ACTION_FLOWS[flow_ids[0]] if flow_ids else None
    supporting_flows = [ACTION_FLOWS[flow_id] for flow_id in flow_ids[1:]]
    primary_flow_id = primary_flow.flow_id if primary_flow else "-"
    statement = function_statement(meta)
    inbound_actors = external_edge_ecus(meta.inbound_edges, meta.ecu)
    outbound_actors = external_edge_ecus(meta.outbound_edges, meta.ecu)

    header_y = 100
    header_h = 142
    header_parts = [
        f'<rect x="{margin}" y="{header_y}" width="{grid_w(12)}" height="{header_h}" class="box" fill="url(#heroGradient)"/>',
        f'<text x="{margin + 22}" y="{header_y + 34}" class="small">Reference bank | page {page_number}</text>',
        f'<text x="{margin + 22}" y="{header_y + 72}" class="title">{escape(meta.ecu)}</text>',
        f'<text x="{margin + 22}" y="{header_y + 102}" class="text">{escape(group_label)} | {escape(meta.domain)}</text>',
        f'<text x="{margin + 22}" y="{header_y + 126}" class="text">Primary flow: {escape(primary_flow_id)}</text>',
    ]

    content_y = header_y + header_h + 24
    peer_count = len(sorted(set(clean_items(meta.linked_ecus)) - set(clean_items(meta.upstream_ecus)) - set(clean_items(meta.downstream_ecus))))
    linked_svg, linked_height = render_chip_grid_card(
        margin,
        content_y,
        grid_w(12),
        "Linked ECU bank",
        meta.linked_ecus,
        fill="#eff6ff",
        chip_fill="#ffffff",
        chip_stroke="#bfdbfe",
        lead_lines=[
            f"Linked ECU visible: {len(clean_items(meta.linked_ecus))}",
            f"Upstream {len(clean_items(meta.upstream_ecus))} | Downstream {len(clean_items(meta.downstream_ecus))} | Peer {peer_count}",
        ],
    )

    second_row_y = content_y + linked_height + 18
    statement_svg, statement_height = render_statement_card(
        grid_x(0),
        second_row_y,
        grid_w(4),
        statement,
    )
    snapshot_svg, snapshot_height = render_quick_snapshot_card(
        grid_x(4),
        second_row_y,
        grid_w(4),
        primary_flow=primary_flow,
        supporting_flows=supporting_flows,
        owner_seams=meta.owner_seam,
        test_assets=meta.test_assets,
        source_files=[meta.source_capl, meta.mirror_capl],
        doc_sources=meta.doc_sources,
        sysvar_hints=meta.sysvar_hints,
    )
    diagram_svg, diagram_height = render_mini_function_diagram(
        grid_x(8),
        second_row_y,
        grid_w(4),
        ecu=meta.ecu,
        statement=statement,
        inbound_actors=inbound_actors,
        outbound_actors=outbound_actors,
    )
    total_height = second_row_y + max(statement_height, snapshot_height, diagram_height) + 50
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{group_color}"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #f7f7f5; }}
    .title {{ font: 700 32px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 13px 'Segoe UI', sans-serif; fill: #475569; }}
    .statement {{ font: 700 26px 'Segoe UI', sans-serif; fill: #111827; }}
    .node {{ font: 700 18px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 22; ry: 22; stroke: #334155; stroke-width: 1.6; }}
    .lane {{ stroke: #64748b; stroke-width: 3; fill: none; marker-end: url(#arrow); }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">ECU Reference Card - {escape(meta.ecu)}</text>
  <text x="34" y="72" class="sub">page {page_number} | grouped reference bank with balanced network layout</text>
  {' '.join(header_parts)}
  {linked_svg}
  {snapshot_svg}
  {statement_svg}
  {diagram_svg}
</svg>
"""


def render_card_layout_v3(meta: EcuMeta) -> str:
    margin = 30
    gutter = 20
    column = 110

    def grid_x(col_idx: int) -> int:
        return margin + col_idx * (column + gutter)

    def grid_w(span: int) -> int:
        return span * column + (span - 1) * gutter

    title = f"ECU Story Card - {meta.ecu}"
    group_label = GROUP_LABELS[meta.group]
    group_color = group_fill(meta.group)
    flow_ids = related_action_flow_ids(meta)
    primary_flow = ACTION_FLOWS[flow_ids[0]] if flow_ids else None
    statement = function_statement(meta)
    role_lines = wrap_lines(statement_headline(statement), 42)
    inbound_actors = external_edge_ecus(meta.inbound_edges, meta.ecu)
    outbound_actors = external_edge_ecus(meta.outbound_edges, meta.ecu)
    primary_flow_label = f"{primary_flow.flow_id} {primary_flow.title}" if primary_flow else "-"

    hero_y = 100
    hero_left_x = grid_x(0)
    hero_right_x = grid_x(7)
    hero_right_w = grid_w(5)
    hero_tile_gap = 12
    hero_tile_width = (hero_right_w - hero_tile_gap) // 2
    hero_lines = (
        [f"{group_label} | {meta.domain}"]
        + [""]
        + role_lines
        + [""]
        + ["Primary action flow"]
        + wrap_lines(primary_flow_label, 42)
    )
    hero_height = max(184, 88 + block_height(hero_lines, 20))
    tile_x1 = hero_right_x
    tile_x2 = hero_right_x + hero_tile_width + hero_tile_gap
    tile_y1 = hero_y + 34
    tile_y2 = tile_y1 + 94
    hero_svg = "\n".join(
        [
            f'<rect x="{margin}" y="{hero_y}" width="{grid_w(12)}" height="{hero_height}" class="box" fill="url(#heroGradient)"/>',
            f'<text x="{hero_left_x + 22}" y="{hero_y + 34}" class="small">Story overview</text>',
            f'<text x="{hero_left_x + 22}" y="{hero_y + 72}" class="title">{escape(meta.ecu)}</text>',
            render_multiline_text(hero_left_x + 22, hero_y + 104, hero_lines, "text", 20),
            render_metric_tile(tile_x1, tile_y1, hero_tile_width, "Inbound actors", str(len(inbound_actors)), fill="#ffffff"),
            render_metric_tile(tile_x2, tile_y1, hero_tile_width, "Outbound actors", str(len(outbound_actors)), fill="#ffffff"),
            render_metric_tile(tile_x1, tile_y2, hero_tile_width, "Linked ECU", str(len(meta.linked_ecus)), fill="#ffffff"),
            render_metric_tile(tile_x2, tile_y2, hero_tile_width, "Native Tests", str(len(meta.test_assets)), fill="#ffffff"),
        ]
    )

    metadata_y = hero_y + hero_height + 24
    metadata_svg, metadata_height = render_overview_metadata_strip(
        margin,
        metadata_y,
        grid_w(12),
        meta=meta,
    )

    rail_y = metadata_y + metadata_height + 24
    action_svg, action_h = render_action_rail_card(
        margin,
        rail_y,
        grid_w(12),
        meta=meta,
        primary_flow=primary_flow,
    )

    flow_y = rail_y + action_h + 24
    rep_svg, rep_height = render_representative_signal_flow(margin, flow_y, grid_w(12), meta)

    footprint_y = flow_y + rep_height + 24
    footprint_svg, footprint_h = render_network_footprint_card(
        margin,
        footprint_y,
        grid_w(12),
        meta=meta,
        title="Network footprint",
        fill="#eff6ff",
    )

    total_height = footprint_y + footprint_h + 50
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{group_color}"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #f7f7f5; }}
    .title {{ font: 700 32px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 13px 'Segoe UI', sans-serif; fill: #475569; }}
    .node {{ font: 700 18px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 22; ry: 22; stroke: #334155; stroke-width: 1.6; }}
    .lane {{ stroke: #64748b; stroke-width: 3; fill: none; marker-end: url(#arrow); }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">ECU Overview Card - {escape(meta.ecu)}</text>
  <text x="34" y="72" class="sub">page 1 | hierarchy-first overview with action rail and network footprint</text>
  {hero_svg}
  {metadata_svg}
  {action_svg}
  {rep_svg}
  {footprint_svg}
</svg>
"""


def representative_signal_path(meta: EcuMeta) -> tuple[str | None, str | None, str | None, str | None]:
    inbound_candidates = summarize_edges(meta.inbound_edges, limit=None)
    outbound_candidates = summarize_edges(meta.outbound_edges, limit=None)
    inbound = next((edge for edge in inbound_candidates if split_edge(edge)[0] != meta.ecu), inbound_candidates[0] if inbound_candidates else None)
    outbound = next((edge for edge in outbound_candidates if split_edge(edge)[0] != meta.ecu), outbound_candidates[0] if outbound_candidates else None)
    src_ecu = None
    src_msg = None
    dst_ecu = None
    dst_msg = None
    if inbound:
        src_ecu, src_msg = split_edge(inbound)
    if outbound:
        dst_ecu, dst_msg = split_edge(outbound)
    return src_ecu, src_msg, dst_ecu, dst_msg


def render_representative_signal_flow(x: int, y: int, width: int, meta: EcuMeta) -> tuple[str, int]:
    src_ecu, src_msg, dst_ecu, dst_msg = representative_signal_path(meta)
    if not src_ecu and not dst_ecu:
        no_path_height = 118
        return (
            "\n".join(
                [
                    f'<rect x="{x}" y="{y}" width="{width}" height="{no_path_height}" class="box" fill="#eff6ff"/>',
                    f'<text x="{x + 22}" y="{y + 36}" class="label">Representative signal flow</text>',
                    f'<text x="{x + 22}" y="{y + 72}" class="text">No representative DBC signal path extracted for this ECU.</text>',
                ]
            ),
            no_path_height,
        )

    panel_height = 206
    left_x = x + 28
    center_x = x + width // 2 - 110
    right_x = x + width - 248
    box_y = y + 70
    msg_y = y + 132
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{panel_height}" class="box" fill="#eff6ff"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">Representative signal flow</text>',
    ]

    if src_ecu:
        parts.append(f'<rect x="{left_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>')
        parts.append(f'<text x="{left_x + 18}" y="{box_y + 34}" class="node">{escape(src_ecu)}</text>')

    parts.append(f'<rect x="{center_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>')
    parts.append(f'<text x="{center_x + 110}" y="{box_y + 34}" text-anchor="middle" class="node">{escape(meta.ecu)}</text>')

    if dst_ecu:
        parts.append(f'<rect x="{right_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#ffffff" stroke="#86efac" stroke-width="1.5"/>')
        parts.append(f'<text x="{right_x + 18}" y="{box_y + 34}" class="node">{escape(dst_ecu)}</text>')

    if src_ecu:
        parts.append(f'<line x1="{left_x + 220}" y1="{box_y + 29}" x2="{center_x}" y2="{box_y + 29}" class="lane"/>')
        rx_lines = wrap_lines(f"Rx {src_msg or '-'}", 28)
        parts.append(render_multiline_text(left_x + 236, msg_y, rx_lines, "small", 18))

    if dst_ecu:
        parts.append(f'<line x1="{center_x + 220}" y1="{box_y + 29}" x2="{right_x}" y2="{box_y + 29}" class="lane"/>')
        tx_lines = wrap_lines(f"Tx {dst_msg or '-'}", 28)
        parts.append(render_multiline_text(center_x + 236, msg_y, tx_lines, "small", 18))

    lane_note = []
    if src_ecu and dst_ecu:
        lane_note = [f"{src_ecu} -> {meta.ecu} -> {dst_ecu}"]
    elif src_ecu:
        lane_note = [f"{src_ecu} -> {meta.ecu}"]
    elif dst_ecu:
        lane_note = [f"{meta.ecu} -> {dst_ecu}"]
    if lane_note:
        parts.append(render_multiline_text(x + 22, y + 182, lane_note, "text", 20))

    return "\n".join(parts), panel_height


def render_card(meta: EcuMeta) -> str:
    title = f"ECU Network Flow - {meta.ecu}"
    group_label = GROUP_LABELS[meta.group]
    group_color = group_fill(meta.group)
    flow_ids = related_action_flow_ids(meta)
    primary_flow = ACTION_FLOWS[flow_ids[0]] if flow_ids else None
    supporting_flows = [ACTION_FLOWS[flow_id] for flow_id in flow_ids[1:]]

    role = wrap_lines(meta.role_hint, 28)
    seams = render_bullets(meta.owner_seam, width=34)
    files = render_bullets([meta.source_capl, meta.mirror_capl], width=42)
    sysvars = render_bullets(meta.sysvar_hints, width=34)
    tests = render_bullets(meta.test_assets, width=42)
    doc_sources = render_bullets(meta.doc_sources, width=36)
    linked = render_bullets(meta.linked_ecus, width=30)
    inbound_dbc = render_bullets(meta.inbound_dbc_sources or meta.dbc_sources, width=22)
    outbound_dbc = render_bullets(meta.outbound_dbc_sources or meta.dbc_sources, width=22)
    published_contracts = render_bullets(meta.published_contracts, width=28)
    consumed_contracts = render_bullets(meta.consumed_contracts, width=28)
    gap_lines = wrap_lines(ecu_risk_focus(meta), 42)
    runtime_lines = wrap_lines(meta.runtime_note, 42)
    flow_lines = normalize_lines(
        [
            f"Primary flow: {primary_flow.flow_id} {primary_flow.title}" if primary_flow else "Primary flow: -",
            *([f"Supporting flow: {flow.flow_id} {flow.title}" for flow in supporting_flows] or ["Supporting flow: -"]),
        ]
    )
    stat_lines = wrap_lines(
        f"Published {len(meta.published_contracts)} | Consumed {len(meta.consumed_contracts)} | Linked {len(meta.linked_ecus)} | Tests {len(meta.test_assets)}",
        40,
    )
    primary_flow_lines = wrap_lines(
        f"{primary_flow.flow_id} {primary_flow.title}" if primary_flow else "-",
        34,
    )
    owner_preview = wrap_lines(meta.owner_seam[0] if meta.owner_seam else "-", 30)
    signal_src, signal_src_msg, signal_dst, signal_dst_msg = representative_signal_path(meta)
    signal_route = (
        f"{signal_src} -> {meta.ecu} -> {signal_dst}"
        if signal_src and signal_dst
        else f"{signal_src} -> {meta.ecu}"
        if signal_src
        else f"{meta.ecu} -> {signal_dst}"
        if signal_dst
        else "No representative signal route extracted"
    )
    signal_route_lines = wrap_lines(signal_route, 34)

    placement_y = 100
    placement_height = max(126, 100 + block_height(role, 22))

    flow_band_y = placement_y + placement_height + 24
    flow_band_height = max(140, 98 + max(block_height(inbound_dbc, 20), block_height(outbound_dbc, 20)))

    edge_y = flow_band_y + flow_band_height + 24
    left_svg, left_height = render_edge_column(40, edge_y, 450, "Inbound Flow", meta.inbound_edges, "#e0f2fe")
    right_svg, right_height = render_edge_column(1110, edge_y, 450, "Outbound Flow", meta.outbound_edges, "#dbeafe")

    center_x = 530
    center_width = 500
    center_y = edge_y + 58
    center_role_y = center_y + 82
    center_stat_label_y = center_role_y + block_height(role, 22) + 18
    center_stat_y = center_stat_label_y + 24
    center_flow_label_y = center_stat_y + block_height(stat_lines, 18) + 24
    center_flow_y = center_flow_label_y + 24
    center_seam_label_y = center_flow_y + block_height(primary_flow_lines, 18) + 24
    center_seam_y = center_seam_label_y + 24
    center_route_label_y = center_seam_y + block_height(owner_preview, 18) + 24
    center_route_y = center_route_label_y + 24
    center_height = max(320, center_route_y - center_y + block_height(signal_route_lines, 18) + 40)
    edge_area_height = max(left_height, right_height, center_height + 80)
    edge_panel_height = edge_area_height + 80

    path_y = edge_y + edge_panel_height + 24
    path_svg, path_height = render_representative_signal_flow(30, path_y, 1540, meta)

    row1_y = path_y + path_height + 20
    metadata_block = (
        [f"Layer / Group: {meta.domain} / {group_label}"]
        + [""]
        + ["Owner seam"]
        + seams
        + [""]
        + ["Sysvar hints"]
        + sysvars
    )
    evidence_block = ["Direct native tests"] + tests + [""] + ["Doc source"] + doc_sources + [""] + ["Files"] + files
    metadata_svg, metadata_height = render_section_card(30, row1_y, 740, "Metadata anchors", metadata_block, fill="#f8fafc")
    evidence_svg, evidence_height = render_section_card(800, row1_y, 770, "Evidence and reading anchors", evidence_block, fill="#ffffff")

    row2_y = row1_y + max(metadata_height, evidence_height) + 20
    interaction_lead = [
        f"Linked ECU count: {len(meta.linked_ecus)}",
        f"Upstream ECU count: {len(meta.upstream_ecus)} | Downstream ECU count: {len(meta.downstream_ecus)}",
    ]
    interaction_svg, interaction_height = render_chip_grid_card(
        30,
        row2_y,
        740,
        "Linked ECU bank",
        meta.linked_ecus,
        fill="#eff6ff",
        chip_fill="#ffffff",
        chip_stroke="#bfdbfe",
        lead_lines=interaction_lead,
    )
    contract_svg, contract_height = render_dual_list_card(
        800,
        row2_y,
        770,
        "Contract inventory",
        f"Published ({len(meta.published_contracts)})",
        published_contracts,
        f"Consumed ({len(meta.consumed_contracts)})",
        consumed_contracts,
        fill="#ffffff",
    )

    row3_y = row2_y + max(interaction_height, contract_height) + 20
    note_block = flow_lines + [""] + gap_lines + [""] + runtime_lines
    note_svg, note_height = render_section_card(30, row3_y, 1540, "Review notes and action map", note_block, fill="#fff7ed")
    total_height = row3_y + note_height + 50

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #f8fafc; }}
    .title {{ font: 700 30px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 14px 'Segoe UI', sans-serif; fill: #475569; }}
    .node {{ font: 700 18px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 20; ry: 20; stroke: #475569; stroke-width: 2; }}
    .lane {{ stroke: #64748b; stroke-width: 3; fill: none; marker-end: url(#arrow); }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">{escape(title)}</text>
  <text x="34" y="72" class="sub">{escape(group_label)} | Domain {escape(meta.domain)} | generated internal OEM-style network flow card</text>

  <rect x="30" y="{placement_y}" width="1540" height="{placement_height}" class="box" fill="{group_color}"/>
  <text x="52" y="{placement_y + 36}" class="label">ECU placement</text>
  <text x="52" y="{placement_y + 68}" class="text">Group: {escape(group_label)}</text>
  <text x="450" y="{placement_y + 68}" class="text">Domain: {escape(meta.domain)}</text>
  {render_multiline_text(52, placement_y + 98, role, "text", 22)}

  <rect x="30" y="{flow_band_y}" width="1540" height="{flow_band_height}" class="box" fill="#ffffff"/>
  <text x="52" y="{flow_band_y + 36}" class="label">Network surface</text>
  <rect x="52" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="74" y="{flow_band_y + 82}" class="small">Inbound DBC / bus surface</text>
  {render_multiline_text(74, flow_band_y + 108, inbound_dbc, "text", 20)}
  <rect x="585" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#ecfeff" stroke="#67e8f9" stroke-width="1.5"/>
  <text x="607" y="{flow_band_y + 82}" class="small">Current ECU lane</text>
  <text x="607" y="{flow_band_y + 110}" class="node">{escape(meta.ecu)}</text>
  <text x="607" y="{flow_band_y + 138}" class="small">{escape(meta.domain)} / {escape(group_label)}</text>
  <rect x="1118" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="1140" y="{flow_band_y + 82}" class="small">Outbound DBC / bus surface</text>
  {render_multiline_text(1140, flow_band_y + 108, outbound_dbc, "text", 20)}

  <rect x="30" y="{edge_y}" width="1540" height="{edge_panel_height}" class="box" fill="#ffffff"/>
  <text x="52" y="{edge_y + 36}" class="label">Runtime network flow</text>
  {left_svg}

  <rect x="{center_x}" y="{center_y}" width="{center_width}" height="{center_height}" class="box" fill="#dcfce7"/>
  <text x="{center_x + center_width / 2:.1f}" y="{center_y + 42}" text-anchor="middle" class="node">{escape(meta.ecu)}</text>
  {render_multiline_text(center_x + 26, center_role_y, role, "text", 22)}
  <text x="{center_x + 26}" y="{center_stat_label_y}" class="small">Interaction summary</text>
  {render_multiline_text(center_x + 26, center_stat_y, stat_lines, "small", 18)}
  <text x="{center_x + 26}" y="{center_flow_label_y}" class="small">Primary action flow</text>
  {render_multiline_text(center_x + 26, center_flow_y, primary_flow_lines, "small", 18)}
  <text x="{center_x + 26}" y="{center_seam_label_y}" class="small">Owner seam</text>
  {render_multiline_text(center_x + 26, center_seam_y, owner_preview, "small", 18)}
  <text x="{center_x + 26}" y="{center_route_label_y}" class="small">Signal route</text>
  {render_multiline_text(center_x + 26, center_route_y, signal_route_lines, "small", 18)}

  {right_svg}

  <line x1="490" y1="{center_y + center_height // 2}" x2="{center_x}" y2="{center_y + center_height // 2}" class="lane"/>
  <line x1="{center_x + center_width}" y1="{center_y + center_height // 2}" x2="1110" y2="{center_y + center_height // 2}" class="lane"/>
  <text x="500" y="{center_y + center_height // 2 - 18}" class="small">consume / normalize</text>
  <text x="{center_x + center_width + 10}" y="{center_y + center_height // 2 - 18}" class="small">publish / route</text>

  {path_svg}

  {metadata_svg}
  {evidence_svg}
  {interaction_svg}
  {contract_svg}
  {note_svg}
</svg>
"""


def write_card_set(metadata: list[EcuMeta]) -> None:
    global ECU_DOMAIN_LOOKUP
    ECU_DOMAIN_LOOKUP = {item.ecu: item.domain for item in metadata}
    CARD_ROOT.mkdir(parents=True, exist_ok=True)
    for meta in metadata:
        card_svg = render_card_layout_v3(meta)
        detail_svg = render_card_detail_page(meta, page_number=2)
        (CARD_ROOT / card_filename(meta.ecu)).write_text(card_svg, encoding="utf-8")
        (CARD_ROOT / card_page_filename(meta.ecu, 2)).write_text(detail_svg, encoding="utf-8")


def write_prototype_card_set(metadata: list[EcuMeta]) -> None:
    PROTOTYPE_ROOT.mkdir(parents=True, exist_ok=True)
    for meta in metadata:
        if meta.ecu not in PROTOTYPE_CARD_ECUS:
            continue
        prototype_v2 = render_card_layout_v2(meta)
        prototype_v3 = render_card_layout_v3(meta)
        (PROTOTYPE_ROOT / prototype_card_filename(meta.ecu, "layout_v2")).write_text(prototype_v2, encoding="utf-8")
        (PROTOTYPE_ROOT / prototype_card_filename(meta.ecu, "layout_v3")).write_text(prototype_v3, encoding="utf-8")


def render_summary_table(counter: Counter[str], label: str) -> list[str]:
    lines = [f"| {label} | Count |", "| --- | ---: |"]
    for key, count in sorted(counter.items()):
        lines.append(f"| `{key}` | `{count}` |")
    return lines


def group_svg_filename(group: str) -> str:
    return f"{group}_{DATE_STAMP}.svg"


def ordered_unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = str(item).strip()
        if not normalized or normalized == "-" or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def compact_bank(items: Iterable[str], limit: int = 8, joiner: str = ", ") -> str:
    values = ordered_unique(items)
    if not values:
        return "-"
    head = values[:limit]
    rendered = joiner.join(head)
    if len(values) > limit:
        rendered = f"{rendered}{joiner}+{len(values) - limit} more"
    return rendered


def compact_table_bank(items: Iterable[str], limit: int = 6) -> str:
    return compact_bank(items, limit=limit, joiner="<br>")


def render_master_book(metadata: list[EcuMeta]) -> str:
    total = len(metadata)
    group_counts = Counter(item.group for item in metadata)
    domain_counts = Counter(item.domain for item in metadata)
    flow_members = action_flow_members(metadata)
    direct_tests = sum(1 for item in metadata if item.test_assets)
    no_test = [item.ecu for item in metadata if not item.test_assets]
    no_published = [item.ecu for item in metadata if not item.published_contracts]
    no_consumed = [item.ecu for item in metadata if not item.consumed_contracts]
    action_flow_count = len(ACTION_FLOW_ORDER)
    group_members: dict[str, list[EcuMeta]] = defaultdict(list)
    category_group = {
        "Dynamics": "GROUP_01_BASE_VEHICLE_DYNAMICS",
        "ADAS": "GROUP_02_ADAS_AEB_BRAKE_ASSIST",
        "Display and Alert": "GROUP_03_DISPLAY_WARNING_AUDIO",
        "Body and Comfort": "GROUP_04_BODY_COMFORT_AMBIENT",
        "Validation": "GROUP_05_VALIDATION_SCENARIO",
        "Backbone": "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS",
    }
    flows_by_category: dict[str, list[ActionFlow]] = defaultdict(list)
    for item in metadata:
        group_members[item.group].append(item)
    for flow_id in ACTION_FLOW_ORDER:
        flow = ACTION_FLOWS[flow_id]
        flows_by_category[flow.category].append(flow)

    lines: list[str] = [
        f"# CANoe Runtime ECU Master Book ({DATE_STAMP})",
        "",
        "CANoe architecture master book for the active SIL baseline.",
        "This book is the orchestration layer that ties overview SVG, action-flow pack, and 101 ECU cards into one reading sequence.",
        "",
        "## Table Of Contents",
        "",
        "1. Book Intent",
        "2. Reading Guide",
        "3. Visual Opening",
        "4. System Narrative",
        "5. Coverage Summary",
        "6. Group Snapshot",
        "7. Action-Flow Pack",
        "8. ECU Catalog",
        "9. Evidence Watchlist",
        "",
        "## Book Intent",
        "",
        "Use this document as the official CANoe-side master asset for PDF generation, consulting-style briefings, and later appendix extraction.",
        "The structure is behavior-first: system overview and action flows come before the per-ECU catalog.",
        "Each ECU page is an explanatory card, not just an inventory row.",
        "",
        "## Reading Guide",
        "",
        "1. Start with the overview SVG to understand the full 101-ECU surface.",
        "2. Move into the grouped architecture view to see domain-level bundling.",
        "3. Read the canonical action flows to understand behavior chains.",
        "4. Drop into per-ECU cards only after the behavior context is clear.",
        "5. Use the evidence watchlist at the end to spot test and contract gaps.",
        "",
        "### Core Reading Path",
        "",
        f"1. [Overview SVG](svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_{DATE_STAMP}.svg)",
        f"2. [Group View](ECU_GROUP_NETWORK_VIEW_{DATE_STAMP}.md)",
        f"3. [Action Flow Index](ACTION_FLOW_INDEX_{DATE_STAMP}.md)",
        f"4. [ECU to Flow Matrix](ECU_ACTION_FLOW_MATRIX_{DATE_STAMP}.md)",
        f"5. [ECU Card Index](ECU_CARD_INDEX_{DATE_STAMP}.md)",
        "",
        PAGE_BREAK,
        "",
        "## Visual Opening",
        "",
        "Start with the full 101-ECU overview before zooming into grouped figures, action flows, and per-ECU cards.",
        "",
        f"![](svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_{DATE_STAMP}.svg)",
        "",
        "## System Narrative",
        "",
        f"- Runtime surface inventory: `{total}` ECU",
        f"- Canonical behavior pack: `{action_flow_count}` action flows",
        "- Meaningful behavior is not organized as 101 independent flows.",
        "- One action flow crosses multiple ECU, and one ECU participates in multiple action flows.",
        "- This book therefore uses three layers: overview architecture, action-flow atlas, and per-ECU catalog.",
        "",
        "### Book Parts",
        "",
        "- Part I. Architecture narrative: overview map, grouped view, and action-flow pack.",
        "- Part II. ECU catalog: 101 ECU cards with story page and reference page.",
        "- Part III. Evidence watchlist: test anchor, contract, and consumption gaps that need later closure.",
        "",
        "## Source Priority",
        "",
        "1. `canoe/src/capl/**/*.can`",
        "2. `canoe/cfg/channel_assign/**/*.can`",
        "3. `canoe/databases/*.dbc`",
        "4. `canoe/tmp/runtime_message_ownership_matrix.md`",
        "5. `canoe/tests/modules/test_units/**`",
        "6. `driving-alert-workproducts/0301~0304`, `04_SW_Implementation`",
        "",
        PAGE_BREAK,
        "",
        "## Coverage Summary",
        "",
        f"- ECU inventory count: `{total}`",
        f"- Canonical action-flow count: `{action_flow_count}`",
        f"- ECUs with direct matching native tests: `{direct_tests}`",
        f"- ECUs without direct matching native tests: `{len(no_test)}`",
        f"- ECUs without published contract rows in current DBC/runtime supplement: `{len(no_published)}`",
        f"- ECUs without consumed contract rows in current DBC/runtime supplement: `{len(no_consumed)}`",
        "",
        "### By Group",
        "",
        *render_summary_table(group_counts, "Group"),
        "",
        "### By Domain",
        "",
        *render_summary_table(domain_counts, "Domain"),
        "",
        PAGE_BREAK,
        "",
        "## Group Snapshot",
        "",
    ]
    for group in sorted(group_members):
        members = group_members[group]
        group_direct_tests = sum(1 for item in members if item.test_assets)
        dominant_domains = Counter(item.domain for item in members)
        lead_flows = [
            f"{flow.flow_id} {flow.title}"
            for flow in ACTION_FLOWS.values()
            if category_group.get(flow.category) == group
        ]
        lines.extend(
            [
                f"### {GROUP_LABELS[group]}",
                "",
                GROUP_STORIES[group],
                "",
                f"- ECU count: `{len(members)}`",
                f"- Direct native test anchor count: `{group_direct_tests}`",
                f"- Domains: `{', '.join(f'{domain} {count}' for domain, count in sorted(dominant_domains.items()))}`",
                f"- Lead action flows: `{compact_bank(lead_flows, limit=4)}`",
                "",
                f"![](svg/{group_svg_filename(group)})",
                "",
            ]
        )

    lines.extend(
        [
            PAGE_BREAK,
            "",
            "## Action-Flow Pack",
            "",
            "The canonical action-flow pack is the behavior atlas for this project.",
            "Use it to understand why multiple ECU cards point back to the same flow family.",
            "",
            f"- [Action Flow Index](ACTION_FLOW_INDEX_{DATE_STAMP}.md)",
            f"- [ECU to Flow Matrix](ECU_ACTION_FLOW_MATRIX_{DATE_STAMP}.md)",
            "- Flow figures are embedded below so the PDF reads like one orchestrated narrative.",
            "",
        ]
    )
    for category in CATEGORY_ORDER:
        flows = flows_by_category.get(category, [])
        if not flows:
            continue
        lines.extend(
            [
                f"### {category}",
                "",
                CATEGORY_STORIES[category],
                "",
            ]
        )
        for flow in flows:
            members = flow_members.get(flow.flow_id, [])
            lines.extend(
                [
                    f"#### `{flow.flow_id}` {flow.title}",
                    "",
                    flow.summary,
                    "",
                    f"- User outcome: {flow.user_outcome}",
                    f"- Participant bank: `{compact_bank(flow.participants, limit=6)}`",
                    f"- Related ECU bank: `{compact_bank(members, limit=10)}`",
                    f"- Key contracts: `{compact_bank(flow.key_contracts, limit=6)}`",
                    "",
                    f"![](svg/flows/{action_flow_filename(flow)})",
                    "",
                ]
            )

    lines.extend(
        [
            PAGE_BREAK,
            "",
            "## ECU Catalog",
            "",
            "The catalog below is grouped by architecture group so the book reads as one system story instead of a flat asset list.",
            "Each ECU section keeps one human-readable sentence, one concise metadata table, and the two SVG pages.",
            "",
        ]
    )

    current_group = None
    for item in metadata:
        if item.group != current_group:
            current_group = item.group
            group_items = group_members[item.group]
            group_direct_tests = sum(1 for candidate in group_items if candidate.test_assets)
            dominant_domains = Counter(candidate.domain for candidate in group_items)
            lines.extend(
                [
                    PAGE_BREAK,
                    "",
                    f"## {GROUP_LABELS[item.group]}",
                    "",
                    GROUP_STORIES[item.group],
                    "",
                    f"- Group size: `{len(group_items)}` ECU",
                    f"- Native test anchor count: `{group_direct_tests}`",
                    f"- Domain spread: `{', '.join(f'{domain} {count}' for domain, count in sorted(dominant_domains.items()))}`",
                    "",
                    f"![](svg/{group_svg_filename(item.group)})",
                    "",
                ]
            )
        related_flows = related_action_flow_ids(item)
        statement = function_statement(item)
        lines.extend(
            [
                f"### `{item.ecu}`",
                "",
                statement,
                "",
                f"![](svg/ecu_cards/{card_filename(item.ecu)})",
                "",
                f"![](svg/ecu_cards/{card_page_filename(item.ecu, 2)})",
                "",
            ]
        )

    lines.extend(
        [
            PAGE_BREAK,
            "",
            "## Evidence Watchlist",
            "",
            f"- No direct native test anchor yet: `{compact_bank(no_test, limit=18)}`",
            f"- No published contract rows: `{compact_bank(no_published, limit=12)}`",
            f"- No consumed contract rows: `{compact_bank(no_consumed, limit=12)}`",
            f"- Canonical action-flow count: `{action_flow_count}`",
            "",
        ]
    )

    return "\n".join(lines) + "\n"


def render_card_index(metadata: list[EcuMeta]) -> str:
    lines = [
        f"# ECU Card Index ({DATE_STAMP})",
        "",
        "This is the generated index for all per-ECU OEM-style network flow SVG cards.",
        "",
    ]
    by_group: dict[str, list[EcuMeta]] = defaultdict(list)
    for item in metadata:
        by_group[item.group].append(item)
    for group in sorted(by_group):
        lines.extend([f"## {GROUP_LABELS[group]}", ""])
        for item in by_group[group]:
            lines.append(
                f"- [{item.ecu} p1](svg/ecu_cards/{card_filename(item.ecu)}) | [p2](svg/ecu_cards/{card_page_filename(item.ecu, 2)})"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def render_group06_svg(metadata: list[EcuMeta]) -> str:
    members = [item.ecu for item in metadata if item.group == "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS"]
    primary_nodes = ", ".join(members)
    columns = 4
    ecu_boxes: list[str] = []
    for idx, ecu in enumerate(members):
        row = idx // columns
        col = idx % columns
        x = 60 + col * 300
        y = 390 + row * 52
        ecu_boxes.append(f'<rect x="{x}" y="{y}" width="250" height="36" rx="12" ry="12" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>')
        ecu_boxes.append(f'<text x="{x + 14}" y="{y + 24}" class="node">{escape(ecu)}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="980" viewBox="0 0 1320 980">
  <style>
    .title {{ font: 700 28px 'Segoe UI', sans-serif; fill: #111827; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .node {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 14px 'Segoe UI', sans-serif; fill: #475569; }}
    .box {{ rx: 18; ry: 18; stroke: #475569; stroke-width: 2; }}
  </style>
  <text x="34" y="42" class="title">Group 06 - Backbone / Gateway / Diagnostics</text>
  <text x="34" y="70" class="small">Runtime backbone, gateway, diagnostics, and service-facing nodes that do not fit the display/body/dynamics groups.</text>

  <rect x="30" y="110" width="1260" height="130" class="box" fill="#fce7f3"/>
  <text x="52" y="146" class="label">Primary nodes</text>
  <text x="52" y="176" class="node">{escape(primary_nodes)}</text>
  <text x="52" y="204" class="small">Validation nodes stay in Group 05. This group focuses on backbone routing, diagnostics, and service surfaces.</text>

  <rect x="30" y="270" width="1260" height="90" class="box" fill="#ede9fe"/>
  <text x="52" y="306" class="label">Main path</text>
  <text x="52" y="336" class="node">domain state / service requests -> CGW / ETHB / DCM / SGW / IBOX -> routed gateway, diagnostic, and external service surfaces</text>

  <rect x="30" y="380" width="1260" height="520" class="box" fill="#ffffff"/>
  <text x="52" y="416" class="label">ECU roster</text>
  {"".join(ecu_boxes)}

  <rect x="30" y="920" width="1260" height="40" class="box" fill="#f8fafc"/>
  <text x="52" y="946" class="small">Use the per-ECU card index for individual runtime details.</text>
</svg>
"""


def ensure_dirs() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    FLOW_ROOT.mkdir(parents=True, exist_ok=True)
    CARD_ROOT.mkdir(parents=True, exist_ok=True)
    FLOW_SVG_ROOT.mkdir(parents=True, exist_ok=True)
    PROTOTYPE_ROOT.mkdir(parents=True, exist_ok=True)


def write_outputs(metadata: list[EcuMeta]) -> None:
    ensure_dirs()
    flow_members = action_flow_members(metadata)
    METADATA_JSON.write_text(json.dumps([asdict(item) for item in metadata], ensure_ascii=False, indent=2), encoding="utf-8")
    ACTION_FLOW_JSON.write_text(
        json.dumps(
            [
                {
                    **asdict(flow),
                    "related_ecus": flow_members.get(flow.flow_id, []),
                }
                for flow in ACTION_FLOWS.values()
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    MASTER_BOOK.write_text(render_master_book(metadata), encoding="utf-8")
    CARD_INDEX.write_text(render_card_index(metadata), encoding="utf-8")
    ACTION_FLOW_INDEX.write_text(render_action_flow_index(flow_members), encoding="utf-8")
    ECU_FLOW_MATRIX.write_text(render_ecu_flow_matrix(metadata), encoding="utf-8")
    GROUP06_SVG.write_text(render_group06_svg(metadata), encoding="utf-8")
    for flow_id in ACTION_FLOW_ORDER:
        flow = ACTION_FLOWS[flow_id]
        (FLOW_SVG_ROOT / action_flow_filename(flow)).write_text(
            render_action_flow_svg(flow, flow_members.get(flow_id, [])),
            encoding="utf-8",
        )
    write_card_set(metadata)
    write_prototype_card_set(metadata)


def main() -> None:
    metadata = build_metadata()
    write_outputs(metadata)
    print(f"[internal-ecu-pack] dataset: {METADATA_JSON}")
    print(f"[internal-ecu-pack] action-flow-dataset: {ACTION_FLOW_JSON}")
    print(f"[internal-ecu-pack] book: {MASTER_BOOK}")
    print(f"[internal-ecu-pack] index: {CARD_INDEX}")
    print(f"[internal-ecu-pack] action-flow-index: {ACTION_FLOW_INDEX}")
    print(f"[internal-ecu-pack] ecu-flow-matrix: {ECU_FLOW_MATRIX}")
    print(f"[internal-ecu-pack] group06: {GROUP06_SVG}")
    print(f"[internal-ecu-pack] action-flow-count: {len(ACTION_FLOW_ORDER)}")
    print(f"[internal-ecu-pack] card_count: {len(metadata)}")
    print(f"[internal-ecu-pack] prototype-cards: {PROTOTYPE_ROOT}")


if __name__ == "__main__":
    main()
