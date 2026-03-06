"""
Reload CANoe configuration from disk to restore CAPL-attached nodes.
The disk cfg has correct CAPL references; in-memory state is broken from previous session.
"""
import win32com.client
import sys
import time

CFG_PATH = r"C:\Users\이준영\canoe-driving-alert\canoe\cfg\CAN_500kBaud_1ch_split.cfg"

try:
    app = win32com.client.Dispatch("CANoe.Application")

    # Stop measurement if running
    try:
        meas = app.Measurement
        if meas.Running:
            meas.Stop()
            time.sleep(1)
            print("Measurement stopped")
    except Exception as e:
        print(f"Stop measurement: {e}")

    # Reopen configuration from disk (discards in-memory changes)
    print(f"Opening configuration: {CFG_PATH}")
    try:
        app.Open(CFG_PATH)
        time.sleep(2)
        print("  Open OK")
    except Exception as e:
        print(f"  Open error: {e}")
        # Try via Configuration
        try:
            cfg = app.Configuration
            cfg.Open(CFG_PATH)
            time.sleep(2)
            print("  cfg.Open OK")
        except Exception as e2:
            print(f"  cfg.Open error: {e2}")

    # Verify nodes
    cfg = app.Configuration
    nds = cfg.SimulationSetup.Nodes
    print(f"\nNode count after reload: {nds.Count}")
    for i in range(1, nds.Count + 1):
        node = nds.Item(i)
        print(f"  [{i}] Name={node.Name!r}  FullName={node.FullName!r}  Active={node.Active}")

except Exception as e:
    print(f"FATAL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
