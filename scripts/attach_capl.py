"""
Attach CAPL source files to simulation nodes in CANoe.
Each node's Path property must point to its .can file.
"""
import win32com.client
import time
import sys
import os

NODES_DIR = r"c:\Users\이준영\canoe-ivi-ota\canoe\nodes"

NODE_MAP = {
    "Context_Manager": os.path.join(NODES_DIR, "Context_Manager.can"),
    "Police_Node":     os.path.join(NODES_DIR, "Police_Node.can"),
    "Ambulance_Node":  os.path.join(NODES_DIR, "Ambulance_Node.can"),
    "Civ_Node":        os.path.join(NODES_DIR, "Civ_Node.can"),
    "Ambient_ECU":     os.path.join(NODES_DIR, "Ambient_ECU.can"),
    "Cluster_ECU":     os.path.join(NODES_DIR, "Cluster_ECU.can"),
}

try:
    app = win32com.client.Dispatch("CANoe.Application")
    cfg = app.Configuration
    nds = cfg.SimulationSetup.Nodes

    print(f"Node count: {nds.Count}")

    for i in range(1, nds.Count + 1):
        node = nds.Item(i)
        name = node.Name
        if name in NODE_MAP:
            capl_path = NODE_MAP[name]
            if not os.path.exists(capl_path):
                print(f"  WARN: File not found: {capl_path}")
                continue
            try:
                old_path = node.Path
                node.Path = capl_path
                new_path = node.Path
                print(f"  [{name}] Path: {old_path!r} -> {new_path!r}")
            except Exception as e:
                print(f"  [{name}] Path set ERROR: {e}")
        else:
            print(f"  [{node.Name}] Not in NODE_MAP, skipped")

    # Save configuration
    print("\nSaving configuration...")
    try:
        cfg.SaveAs(r"c:\Users\이준영\canoe-ivi-ota\canoe\cfg")
        print("  SaveAs OK")
    except Exception as e:
        print(f"  SaveAs error: {e}")
        try:
            cfg.Save()
            print("  Save OK")
        except Exception as e2:
            print(f"  Save error: {e2}")

    print("\nDone.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
