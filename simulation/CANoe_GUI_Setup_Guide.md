# CANoe GUI Configuration Setup Guide

**Project**: CANoe-IVI-OTA
**Date**: 2026-02-12
**Issue**: `.cfg` files must be created through CANoe GUI

---

## ⚠️ Important Discovery

**Vector CANoe `.cfg` files are binary format and CANNOT be created as text files.**

You must create the configuration through the CANoe GUI.

---

## 🚀 Step-by-Step Configuration Setup (GUI Method)

### Step 1: Create New Configuration

1. **Launch CANoe 19.4**
   - Open Vector CANoe from Start Menu or Desktop

2. **Create New Configuration**
   ```
   File → New Configuration...
   Or press: Ctrl+N
   ```

3. **Save Configuration**
   ```
   File → Save Configuration As...
   Location: C:\Users\이준영\CANoe-IVI-OTA\simulation\configurations\
   Name: IVI_OTA_Project.cfg
   ```

---

### Step 2: Add CAN Database

1. **Open Database Configuration**
   ```
   Configuration → Databases...
   ```

2. **Add DBC File**
   ```
   Click "Add Database..."
   Navigate to: simulation/databases/vehicle_system.dbc
   Select and click "Open"
   ```

3. **Verify Database**
   ```
   ✅ Check that vehicle_system.dbc appears in the list
   ✅ Verify 20 messages are listed
   ✅ Verify 13 ECUs (BU_) are listed
   ```

---

### Step 3: Configure Networks

1. **Open Network Configuration**
   ```
   Configuration → Network Hardware...
   Or press: Ctrl+H
   ```

2. **Add CAN Channels**

   **CAN Channel 1** (CAN-HS #1):
   ```
   Type: CAN
   Baudrate: 500 kbit/s
   Name: CAN1 (Powertrain/Chassis/Safety)
   Channel: 1
   ```

   **CAN Channel 2** (CAN-HS #2):
   ```
   Type: CAN
   Baudrate: 500 kbit/s
   Name: CAN2 (ADAS/Infotainment)
   Channel: 2
   ```

   **CAN Channel 3** (CAN-LS):
   ```
   Type: CAN
   Baudrate: 125 kbit/s
   Name: CAN3 (Body Control)
   Channel: 3
   ```

---

### Step 4: Add CAPL Nodes

1. **Open Simulation Setup**
   ```
   Configuration → Simulation Setup...
   ```

2. **Add Network Nodes**

   For each network, right-click and select "Insert Network Node..."

   **On CAN1 (Channel 1)**:
   - Add node: EMS → Browse to `nodes/EMS.can`
   - Add node: TCU → Browse to `nodes/TCU.can`
   - Add node: ESP → Browse to `nodes/ESP.can`
   - Add node: MDPS → Browse to `nodes/MDPS.can`
   - Add node: CGW → Browse to `nodes/CGW.can` ⭐

   **On CAN2 (Channel 2)**:
   - Add node: IVI → Browse to `nodes/IVI.can` ⭐
   - Add node: Cluster → Browse to `nodes/Cluster.can`
   - Add node: Camera → Browse to `nodes/Camera.can`
   - Add node: Rear_Camera → Browse to `nodes/Rear_Camera.can`
   - Add node: Radar → Browse to `nodes/Radar.can`
   - Add node: SCC → Browse to `nodes/SCC.can`

   **On CAN3 (Channel 3)**:
   - Add node: BCM → Browse to `nodes/BCM.can` ⭐
   - Add node: HVAC → Browse to `nodes/HVAC.can`

3. **Configure CGW for Multi-Network**
   ```
   Right-click CGW node → Properties
   Networks tab → Check: CAN1, CAN2, CAN3
   Apply
   ```

---

### Step 5: Assign Database Messages to Nodes

1. **Open Databases Window**
   ```
   View → Databases
   Or press: Alt+2
   ```

2. **Assign Messages**

   Expand `vehicle_system.dbc` → Messages

   **For each message**:
   - Right-click message → Properties
   - "Transmitter" tab
   - Select corresponding ECU node

   Example:
   ```
   IVI_AmbientLight (0x400) → IVI node
   BCM_LightControl (0x510) → BCM node
   EMS_EngineStatus (0x100) → EMS node
   CGW_Status (0x700) → CGW node
   ```

---

### Step 6: Configure Environment Variables

1. **Open System Variables**
   ```
   Environment → System Variables...
   ```

2. **Add Variables** (as defined in our nodes)
   ```
   IVI_Theme_Selected: int, Init=0
   IVI_Brightness: int, Init=50
   IVI_RGB_R: int, Init=255
   IVI_RGB_G: int, Init=255
   IVI_RGB_B: int, Init=255
   Vehicle_Speed: float, Init=0.0
   Engine_RPM: int, Init=0
   Gear_Position: int, Init=0
   ADAS_LDW_Active: int, Init=0
   ADAS_AEB_Active: int, Init=0
   UDS_Active: int, Init=0
   OTA_Active: int, Init=0
   ```

---

### Step 7: Compile and Test

1. **Compile All CAPL Nodes**
   ```
   Build → Compile All CAPL Nodes
   Or press: F9
   ```

2. **Check Compilation Output**
   ```
   View → Write Window
   Should see: "Compilation completed successfully" for each node
   ```

3. **Start Measurement**
   ```
   Measurement → Start
   Or press: F9
   ```

4. **Open Trace Window**
   ```
   View → Trace
   Or press: Ctrl+Alt+T
   ```

5. **Verify Messages**
   ```
   ✅ IVI_AmbientLight (0x400) transmitting every 100ms
   ✅ BCM_LightControl (0x510) transmitting every 100ms
   ✅ EMS_EngineStatus (0x100) transmitting every 10ms
   ✅ CGW_Status (0x700) transmitting every 1000ms
   ```

---

## 🎨 Testing Ambient Lighting

### Test 1: Theme Switching

1. **Activate IVI Write Window**
   ```
   Click on "IVI" in Simulation Setup
   View → Write Window for this node
   ```

2. **Press Keys**:
   ```
   Press '1' → SPORT theme (Red-Orange)
   → Trace window shows: Ambient_Light_R=255, G=50, B=0

   Press '2' → COMFORT theme (Soft Blue)
   → Trace window shows: Ambient_Light_R=100, G=150, B=255

   Press '3' → ECO theme (Green)
   → Trace window shows: Ambient_Light_R=50, G=255, B=100
   ```

3. **Verify BCM Feedback**
   ```
   In Trace window, check BCM_LightControl message:
   → Ambient_R_Actual should match requested R value (±5)
   → Ambient_G_Actual should match requested G value (±5)
   → Ambient_B_Actual should match requested B value (±5)
   ```

### Test 2: Brightness Control

```
Press '+' → Brightness increases by 10%
Press '-' → Brightness decreases by 10%

Check IVI_AmbientLight.Brightness signal in Trace
```

### Test 3: Custom RGB

```
Press 'r' → Pure Red (255, 0, 0)
Press 'g' → Pure Green (0, 255, 0)
Press 'b' → Pure Blue (0, 0, 255)
Press 'w' → White (255, 255, 255)
```

### Test 4: ADAS Event Coordination

1. **Activate Camera Write Window**

2. **Trigger Events**:
   ```
   Press 'L' → Lane Departure Warning
   → IVI lighting changes to YELLOW (255, 200, 0)

   Press 'B' → Emergency Braking
   → IVI lighting changes to RED (255, 0, 0) at 100% brightness

   Press 'K' → Clear warnings
   → IVI returns to normal theme
   ```

### Test 5: Speed-Linked Dynamic Lighting

1. **Activate EMS Write Window**

2. **Activate IVI Write Window** and press '4' (DYNAMIC theme)

3. **In EMS Window**:
   ```
   Press 'I' → Idle (0 km/h)
   → Check IVI brightness = 30%

   Press 'C' → Cruise (80 km/h)
   → Check IVI brightness increases (≈77%)

   Press 'A' → Accelerate (60 km/h)
   → Check IVI brightness = 80%
   ```

---

## 🔀 Testing Gateway Routing

### Test 1: CAN1 → CAN2 Routing

1. **In EMS node**: Press 'C' (Cruise 80 km/h)
   ```
   ✅ EMS_EngineStatus transmitted on CAN1
   ✅ CGW routes to CAN2
   ✅ Cluster receives and displays speed
   ```

2. **Verify in Trace**:
   ```
   Filter: "EMS_EngineStatus"
   Check: Message appears on both CAN1 and CAN2
   ```

### Test 2: CAN2 → CAN3 Routing

1. **In IVI node**: Press '1' (SPORT theme)
   ```
   ✅ IVI_AmbientLight transmitted on CAN2
   ✅ CGW routes to CAN3
   ✅ BCM receives RGB commands
   ```

2. **Verify in Trace**:
   ```
   Filter: "IVI_AmbientLight"
   Check: Message appears on both CAN2 and CAN3
   ```

### Test 3: CAN3 → CAN2 Routing

1. **BCM automatically sends feedback**
   ```
   ✅ BCM_LightControl transmitted on CAN3
   ✅ CGW routes to CAN2
   ✅ IVI and Cluster receive feedback
   ```

2. **Verify in Trace**:
   ```
   Filter: "BCM_LightControl"
   Check: Message appears on both CAN3 and CAN2
   ```

### Test 4: Gateway Statistics

1. **Activate CGW Write Window**

2. **Press 'S'** → Print statistics
   ```
   Output in Write window:
   - Messages routed: XXX
   - Network load: CAN1/CAN2/CAN3 (%)
   - Status: OK/WARNING/ERROR
   ```

3. **Test Routing Control**:
   ```
   Press 'R' → Disable routing
   → Messages no longer cross networks

   Press 'R' → Re-enable routing
   → Routing resumes
   ```

---

## 📊 Monitoring Bus Load

1. **Open Bus Statistics**
   ```
   View → Bus Statistics
   ```

2. **Check Load Values**:
   ```
   CAN1 (HS #1): Should be ~15% (Target: <30%)
   CAN2 (HS #2): Should be ~12% (Target: <30%)
   CAN3 (LS):    Should be ~5%  (Target: <50%)
   ```

3. **If Load Too High**:
   - Increase message cycle times
   - Reduce number of active messages
   - Optimize message content

---

## 🧪 Advanced Testing with MCP Server

Once configuration is running in CANoe GUI, you can use MCP server for automation:

```python
# Example: Automated theme testing
for theme in range(11):
    set_system_variable(f"IVI::Theme", theme)
    sleep(2)
    rgb = get_signal_value("CAN2", "IVI_AmbientLight", "Ambient_Light_R")
    print(f"Theme {theme}: R={rgb}")
```

---

## 📝 Troubleshooting

### Issue: Nodes don't compile
**Solution**:
- Check CAPL syntax in Write window
- Verify file paths are correct
- Ensure database is loaded

### Issue: Messages not transmitted
**Solution**:
- Check node is active (green icon in Simulation Setup)
- Verify message is assigned to node
- Check timers are started (`setTimer()` in `on start`)

### Issue: Gateway doesn't route
**Solution**:
- Verify CGW is on all 3 networks
- Check routing enable flags
- Press 'S' in CGW to see statistics

### Issue: RGB feedback doesn't match
**Solution**:
- BCM has smooth transition (20% per cycle)
- Wait 0.5 seconds for RGB to stabilize
- Check tolerance (±5 is acceptable)

---

## 🎯 Success Criteria Checklist

After setup, verify:

- [ ] All 13 CAPL nodes compile without errors
- [ ] Measurement starts successfully (green play button)
- [ ] Messages appear in Trace window
- [ ] IVI theme switching works (keyboard 1-4,0)
- [ ] BCM provides RGB feedback
- [ ] Gateway routes messages between networks
- [ ] Bus load remains under 30% (HS) and 50% (LS)
- [ ] ADAS events trigger lighting changes
- [ ] Environment variables update correctly

---

## 🚀 Next Steps After Setup

1. **Create Test Sequences**
   - Automate theme testing
   - Test ADAS event scenarios
   - Validate gateway routing

2. **Add Control Panels**
   - RGB color picker GUI
   - Theme selection buttons
   - Brightness slider

3. **Implement UDS Diagnostics**
   - Diagnostic services (0x22, 0x2E, etc.)
   - DTC management
   - OTA update process

4. **Documentation & Demo**
   - Record demo video
   - Create user manual
   - Prepare final presentation

---

**Created**: 2026-02-12
**Status**: ✅ CAPL Nodes Ready - GUI Setup Required
