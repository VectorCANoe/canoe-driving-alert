"""CANoe node property diagnostic script"""
import win32com.client
import sys

try:
    app = win32com.client.Dispatch("CANoe.Application")
    cfg = app.Configuration
    nds = cfg.SimulationSetup.Nodes

    print(f"Node count: {nds.Count}")
    for i in range(1, nds.Count + 1):
        node = nds.Item(i)
        print(f"\n--- Node {i}: {node.Name} ---")
        print(f"  Active: {node.Active}")
        try:
            print(f"  Path: {node.Path}")
        except Exception as e:
            print(f"  Path ERROR: {e}")
        try:
            print(f"  FullName: {node.FullName}")
        except Exception as e:
            print(f"  FullName ERROR: {e}")

        # List all available attributes
        attrs = [x for x in dir(node) if not x.startswith('_')]
        print(f"  Attrs: {attrs}")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
