"""
setup_canoe_config.py
CANoe Simulation Setup 자동 구성 스크립트

실행 전 확인:
  - CANoe가 실행 중이어야 함
  - 측정(Measurement)이 중지된 상태여야 함

실행:
  python scripts/setup_canoe_config.py
"""

import win32com.client
import time
import os
import sys

# ── 경로 설정 ──────────────────────────────────────────
BASE    = r"C:\Users\이준영\CANoe-IVI-OTA\canoe"
CFG     = os.path.join(BASE, r"cfg\CAN_500kBaud_1ch.cfg")
DBC     = os.path.join(BASE, r"databases\emergency_system.dbc")
SYSVARS = os.path.join(BASE, r"cfg\project.sysvars")
NODES_DIR = os.path.join(BASE, "nodes")

OPTION1_NODES = [
    "SIL_TEST_CTRL",
    "CHASSIS_GW",
    "INFOTAINMENT_GW",
    "ADAS_WARN_CTRL",
    "NAV_CONTEXT_MGR",
    "EMS_POLICE_TX",
    "EMS_AMB_TX",
    "EMS_ALERT_RX",
    "WARN_ARB_MGR",
    "BODY_GW",
    "IVI_GW",
    "BCM_AMBIENT_CTRL",
    "CLU_HMI_CTRL",
]

LEGACY_NODES = [
    "Context_Manager",
    "Police_Node",
    "Ambulance_Node",
    "Civ_Node",
    "Ambient_ECU",
    "Cluster_ECU",
    "Test_Node",
]

def wait(sec, msg=""):
    if msg:
        print(f"  [WAIT] {msg}")
    time.sleep(sec)

def main():
    # ── 1. CANoe 연결 ──────────────────────────────────
    print("[STEP] Connect to CANoe...")
    try:
        app = win32com.client.Dispatch("CANoe.Application")
        print(f"  [OK] CANoe {app.Version} connected")
    except Exception as e:
        print(f"  [ERR] CANoe connection failed: {e}")
        print("     → CANoe가 실행 중인지 확인하세요")
        sys.exit(1)

    # ── 2. 측정 중지 확인 ──────────────────────────────
    meas = app.Measurement
    if meas.Running:
        print("[STEP] Stop measurement...")
        meas.Stop()
        wait(2, "측정 중지 대기")

    # ── 3. CFG 열기 ────────────────────────────────────
    print(f"[STEP] Open configuration: {CFG}")
    try:
        app.Open(CFG, 0, 0)
        wait(3, "설정 로드 대기")
        print("  [OK] Configuration loaded")
    except Exception as e:
        print(f"  [ERR] Failed to open config: {e}")
        sys.exit(1)

    cfg = app.Configuration
    sim = cfg.SimulationSetup

    # ── 4. 기존 노드/DB 정리 ───────────────────────────
    print("[STEP] Inspect current setup...")
    try:
        buses = sim.Buses
        bus_count = buses.Count
        print(f"  버스 수: {bus_count}")
        for i in range(1, bus_count + 1):
            bus = buses.Item(i)
            print(f"  버스[{i}]: {bus.Name}")
    except Exception as e:
        print(f"  [WARN] Failed to read bus info: {e}")

    # ── 5. DBC 추가 ────────────────────────────────────
    print(f"[STEP] Add DBC: {DBC}")
    try:
        buses = sim.Buses
        for i in range(1, buses.Count + 1):
            bus = buses.Item(i)
            if "CAN" in bus.Name.upper():
                db_setup = bus.Databases
                db_setup.Add(DBC)
                print("  [OK] DBC added")
                break
    except Exception as e2:
        print(f"  [ERR] DBC add failed: {e2}")

    wait(1)

    # ── 6. 노드 교체 (Legacy 제거 후 Option1 추가) ─────────────────────────
    print("[STEP] Replace nodes (Legacy -> Option1)...")
    try:
        buses = sim.Buses
        target_bus = None
        for i in range(1, buses.Count + 1):
            bus = buses.Item(i)
            if "CAN" in bus.Name.upper():
                target_bus = bus
                break

        if target_bus is None:
            print("  [ERR] CAN bus not found")
        else:
            nodes_obj = target_bus.Nodes

            # 6-1) Legacy 노드 제거
            remove_targets = set(LEGACY_NODES)
            to_remove = []
            for j in range(1, nodes_obj.Count + 1):
                try:
                    existing_name = nodes_obj.Item(j).Name
                    if existing_name in remove_targets:
                        to_remove.append(existing_name)
                except Exception:
                    pass

            for node_name in to_remove:
                try:
                    for idx in range(1, nodes_obj.Count + 1):
                        if nodes_obj.Item(idx).Name == node_name:
                            nodes_obj.Remove(idx)
                            print(f"  - legacy removed: {node_name}")
                            break
                except Exception as e:
                    print(f"  ! legacy remove failed ({node_name}): {e}")

            # 6-2) Option1 노드 추가
            for node_name in OPTION1_NODES:
                capl_path = os.path.join(NODES_DIR, f"{node_name}.can")
                try:
                    # 기존 노드 중복 체크
                    exists = False
                    for j in range(1, nodes_obj.Count + 1):
                        if nodes_obj.Item(j).Name == node_name:
                            exists = True
                            print(f"  [WARN] already exists: {node_name} (skip)")
                            break

                    if not exists:
                        node = nodes_obj.Add(capl_path)
                        try:
                            node.Name = node_name
                        except Exception:
                            pass
                        print(f"  + option1 added: {node_name}")
                except Exception as e:
                    print(f"  [ERR] node add failed ({node_name}): {e}")

    except Exception as e:
        print(f"  [ERR] node replace failed: {e}")

    wait(1)

    # ── 7. System Variables 로드 ────────────────────────
    print(f"[STEP] Load System Variables: {SYSVARS}")
    print("  [INFO] Skip COM load (CANoe COM API mismatch).")
    print("  [INFO] Load manually in CANoe: Environment -> System Variables -> Load")

    wait(1)

    # ── 8. 저장 ─────────────────────────────────────────
    print(f"[STEP] Save configuration: {CFG}")
    try:
        cfg.SaveAs(CFG, True)
        print("  [OK] Saved")
    except Exception as e:
        try:
            cfg.Save()
            print("  [OK] Saved (Save)")
        except Exception as e2:
            print(f"  [ERR] Save failed: {e2}")

    # ── 9. 결과 확인 ────────────────────────────────────
    print("\n[STEP] Verify final setup...")
    try:
        buses = sim.Buses
        for i in range(1, buses.Count + 1):
            bus = buses.Item(i)
            print(f"  버스: {bus.Name}")
            dbs = bus.Databases
            for j in range(1, dbs.Count + 1):
                print(f"    DB[{j}]: {dbs.Item(j).FullName}")
            nds = bus.Nodes
            for j in range(1, nds.Count + 1):
                print(f"    Node[{j}]: {nds.Item(j).Name}")
    except Exception as e:
        print(f"  [WARN] Final verification failed: {e}")

    print("\n[OK] Setup complete")
    print("   -> Start measurement (F9) and run MCP validation")


if __name__ == "__main__":
    main()
