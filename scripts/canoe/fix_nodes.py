"""
Delete all broken nodes and re-add them correctly with CAPL files.
Uses late-binding COM to avoid gen_py cache issues.
"""
import win32com.client
import sys
import os
import time

NODES_DIR = r"C:\Users\이준영\canoe-driving-alert\canoe\nodes"

# Order matters: Context_Manager first, then consumers
CAPL_FILES = [
    ("Context_Manager", "Context_Manager.can"),
    ("Police_Node",     "Police_Node.can"),
    ("Ambulance_Node",  "Ambulance_Node.can"),
    ("Civ_Node",        "Civ_Node.can"),
    ("Ambient_ECU",     "Ambient_ECU.can"),
    ("Cluster_ECU",     "Cluster_ECU.can"),
]

try:
    # Use late-binding (EnsureDispatch may trigger gen_py rebuild)
    app = win32com.client.DispatchEx("CANoe.Application")
    cfg = app.Configuration
    nds = cfg.SimulationSetup.Nodes

    print(f"Current node count: {nds.Count}")

    # Step 1: Remove all existing nodes (iterate in reverse)
    print("\nRemoving existing nodes...")
    for i in range(nds.Count, 0, -1):
        node = nds.Item(i)
        name = node.Name
        try:
            nds.Remove(node)
            print(f"  Removed: {name}")
        except Exception as e:
            try:
                node.Active = False
                print(f"  Deactivated (Remove failed): {name} — {e}")
            except:
                print(f"  Could not remove: {name} — {e}")

    time.sleep(0.5)
    print(f"Nodes after removal: {nds.Count}")

    # Step 2: Add nodes with CAPL files via AddWithTitle
    print("\nAdding CAPL nodes...")
    for node_name, can_filename in CAPL_FILES:
        capl_path = os.path.join(NODES_DIR, can_filename)
        if not os.path.exists(capl_path):
            print(f"  WARN: File not found: {capl_path}")
            continue
        try:
            # AddWithTitle expects the CAPL file path
            node = nds.AddWithTitle(capl_path)
            node.Name = node_name
            actual_path = node.Path
            actual_fullname = node.FullName
            print(f"  Added: {node.Name}  Path={actual_path!r}  FullName={actual_fullname!r}")
        except Exception as e:
            print(f"  AddWithTitle({can_filename}) ERROR: {e}")
            # Try plain Add
            try:
                node = nds.Add(node_name)
                print(f"  Add({node_name}) fallback OK")
            except Exception as e2:
                print(f"  Add fallback ERROR: {e2}")

    time.sleep(0.5)
    print(f"\nFinal node count: {nds.Count}")

    # Step 3: List final state
    for i in range(1, nds.Count + 1):
        node = nds.Item(i)
        print(f"  [{i}] {node.Name}  Active={node.Active}  FullName={node.FullName!r}")

    # Step 4: Save
    print("\nAttempting save...")
    for attempt in range(5):
        try:
            cfg.Save()
            print("  Save OK")
            break
        except Exception as e:
            print(f"  Save attempt {attempt+1} failed: {e}")
            time.sleep(1)
    else:
        print("  All save attempts failed")

except Exception as e:
    print(f"FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
