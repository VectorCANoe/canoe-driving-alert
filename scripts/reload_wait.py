"""
Wait for CANoe UI to be free, then reload configuration from disk.
Run this after closing any dialogs in CANoe.
"""
import win32com.client
import sys
import time

CFG_PATH = r"C:\Users\이준영\CANoe-IVI-OTA\canoe\cfg\CAN_500kBaud_1ch.cfg"

print("Connecting to CANoe...")
app = win32com.client.Dispatch("CANoe.Application")

# Poll until UI is free (max 30 seconds)
print("Waiting for CANoe UI to be free (close any dialogs)...")
for attempt in range(30):
    try:
        app.Open(CFG_PATH)
        print(f"  Open OK on attempt {attempt+1}")
        break
    except Exception as e:
        if "busy" in str(e).lower() or "17161" in str(e):
            print(f"  [{attempt+1}/30] UI busy, waiting 1s...")
            time.sleep(1)
        else:
            print(f"  Open failed with unexpected error: {e}")
            sys.exit(1)
else:
    print("  Timeout: UI still busy after 30s. Please manually reopen cfg in CANoe.")
    sys.exit(1)

# Wait for config to load
time.sleep(3)

# Verify nodes
cfg = app.Configuration
nds = cfg.SimulationSetup.Nodes
print(f"\nNode count after reload: {nds.Count}")
for i in range(1, nds.Count + 1):
    node = nds.Item(i)
    print(f"  [{i}] Name={node.Name!r}  Active={node.Active}")

print("\nDone. Now compile CAPL and start measurement.")
