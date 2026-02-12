> [!IMPORTANT]
> **[ACTUAL PROJECT OUTPUT]**
> 이 문서는 멘토의 가이드에 따라 재설계된 **우리 팀의 실제 시스템 아키텍처** 초안입니다.
> V-Model의 '시스템 설계' 단계에 해당합니다.

# System Level Design: V-Model Architecture (L1/L2)

This document defines the high-level system architecture, transitioning from the incorrect star topology to the vehicle-standard **CAN Bus Topology**.

## 1. System Overview (Vehicle Level)

The vehicle system is composed of 4 main domains connected via a high-speed CAN Bus backbone.

- **Topology**: Bus Topology (Linear with drops)
- **Communication Protocol**: CAN 2.0B / CAN FD
- **Baud Rate**: 500kbps (High Speed CAN)

```mermaid
graph TD
    %% Bus Backbone
    BUS[[=== CAN BUS (High Speed) ===]]

    %% Domain Controllers (ECUs)
    ADAS[ADAS ECU] --- BUS
    CHASSIS[Chassis ECU] --- BUS
    BODY[Body ECU] --- BUS
    IVI[IVI Head Unit] --- BUS
```

## 2. Domain Specifications (L2)

### 2.1 ADAS Domain (Advanced Driver Assistance System)
- **Primary Function**: Perception and Decision Making
- **Input Sensors**: Front Radar, Front Camera
- **Output Signals**: Target Deceleration, Steering Torque Request
- **Mapped Requirements**: REQ_001 (SCC), REQ_002 (Distance), REQ_003 (LKA)

### 2.2 Chassis Domain
- **Primary Function**: Vehicle Motion Control (Actuation)
- **Components**:
    - **Engine Control Unit (EMS)**: Controls acceleration/torque.
    - **Brake Control Unit (ESC)**: Controls deceleration/braking pressure.
    - **Steering Control Unit (MDPS)**: Controls steering angle/torque.
- **Mapped Requirements**: REQ_001 (Cruise), REQ_003 (Lane Keep Actuation)

### 2.3 Body Domain
- **Primary Function**: Comfort and Visibility
- **Components**:
    - **BCM (Body Control Module)**: Windows, Door Locks, Wipers, Lights.
    - **Lamp Unit**: Headlamps (Low/High Beam).
- **Mapped Requirements**: REQ_004 (HBA), REQ_005 (Window), REQ_006 (Seat), REQ_007 (Door)

### 2.4 IVI Domain (In-Vehicle Infotainment)
- **Primary Function**: Human-Machine Interface (HMI)
- **Components**:
    - **Head Unit**: Center display, Touch interface, Audio navigation.
    - **Cluster**: Driver information display (Speed, RPM, Warnings).
- **Mapped Requirements**: REQ_008 (Status), REQ_009 (Warning), REQ_010 (Media)

## 3. Data Flow (Inter-Domain Communication)

| Flow ID | Source | Destination | Content (Signal) | Trigger |
| :--- | :--- | :--- | :--- | :--- |
| **DF_001** | ADAS | Chassis | Target_Deceleration | SCC Active & Distance < Threshold |
| **DF_002** | ADAS | Chassis | Steering_Torque_Req | LKA Active & Lane Departure Detected |
| **DF_003** | ADAS | IVI | SCC_Status_Disp | SCC On/Off Change |
| **DF_004** | Body | IVI | Door_Open_Warning | Door Switch Signal == Open |
| **DF_005** | IVI | Body | Window_Open_Cmd | Touch Input for Window Open |
| **DF_006** | Chassis (EMS) | IVI | Engine_RPM | Periodic Update (10ms) |
| **DF_007** | Chassis (ESC) | IVI | Vehicle_Speed | Periodic Update (10ms) |

---

## 4. Next Steps (Function Definition)

With the architecture and data flow defined, the next step is to create the detailed **Function Definition** sheet (Excel) to map every `Signal` to a specific logic block within these ECUs.
