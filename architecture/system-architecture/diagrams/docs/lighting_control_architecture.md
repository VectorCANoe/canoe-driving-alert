# Lighting Control Architecture

**Requirements Traceability**:
- **REQ_IVI_001**: 스포츠모드 속도연동 엠비언트조명 (ASIL-B, <500ms)
- **REQ_IVI_003**: 승하차 UX 도어연동제어 (ASIL-A, <400ms)
- **REQ_IVI_004**: IVI 조명색상 동기화 (QM, >99%)
- **REQ_IVI_005**: 온도연동 조명제어 (QM, <5% 오차)
- **REQ_IVI_017**: 후진 시 후방 조명 자동 제어 (ASIL-B, ≤150ms)
- **REQ_IVI_042**: IVI 모드 선택 시 조명 테마 자동 적용 (QM, <100ms)

---

## 1. Component Architecture (PlantUML)

```plantuml
@startuml
!theme silver
skinparam componentStyle uml2

package "Lighting Control Subsystem" {

    ' Application Layer Components
    package "Application Software (ASW)" #LightBlue {
        component "Ambient_Light_Controller" as ALC #LightBlue {
            portin "Speed_Signal_In" as ALC_SPEED
            portin "Mode_Signal_In" as ALC_MODE
            portin "Temp_Signal_In" as ALC_TEMP
            portout "RGB_Command_Out" as ALC_RGB

            note right of ALC
                **REQ_IVI_001**
                Sport Mode Speed-linked
                • 0~50km/h: Green
                • 50~100km/h: Blue
                • 100km/h+: Red
                • Response: <500ms
                • ASIL-B
            end note
        }

        component "Dashboard_Lighting_Controller" as DLC #LightGreen {
            portin "Door_Status_In" as DLC_DOOR
            portin "Gear_Position_In" as DLC_GEAR
            portout "Dashboard_LED_Out" as DLC_LED

            note right of DLC
                **REQ_IVI_003, 017**
                Door-linked UX
                • Door Open: Auto ON
                • Reverse Gear: Rear Light ON
                • Response: <400ms (Door)
                • Response: ≤150ms (Reverse)
                • ASIL-A / ASIL-B
            end note
        }

        component "IVI_Sync_Manager" as ISM #Orange {
            portin "IVI_Color_Cmd_In" as ISM_CMD
            portout "vECU_Color_Out" as ISM_OUT

            note right of ISM
                **REQ_IVI_004**
                IVI Color Sync
                • Sync Rate: >99%
                • CAN Message Relay
                • QM (Non-Critical)
            end note
        }

        component "Theme_Manager" as TM #LightYellow {
            portin "Mode_Selection_In" as TM_MODE
            portout "Theme_Package_Out" as TM_PKG

            note right of TM
                **REQ_IVI_042**
                Theme Auto-Apply
                • Sport/Eco/Comfort
                • Response: <100ms
                • QM
            end note
        }
    }

    ' RTE Layer
    package "Runtime Environment (RTE)" #line.dashed {
        interface "CAN_Signal_Port" as CSP
        interface "PWM_Control_Port" as PWM

        ALC_RGB --> CSP
        DLC_LED --> PWM
        ISM_OUT --> CSP
        TM_PKG --> CSP

        CSP --> ALC_SPEED
        CSP --> ALC_MODE
        CSP --> ALC_TEMP
        CSP --> DLC_DOOR
        CSP --> DLC_GEAR
        CSP --> ISM_CMD
        CSP --> TM_MODE
    }

    ' BSW Layer
    package "Basic Software (BSW)" #LightGray {
        component "COM Stack" as COM
        component "IoHwAb\n(I/O Hardware Abstraction)" as IOHW

        CSP --> COM
        PWM --> IOHW
    }

    ' Virtual Hardware
    package "Virtual Hardware (CANoe)" #LightYellow {
        component "CAN Bus (500kbps)" as CAN
        component "PWM Output Simulation" as PWM_SIM

        COM --> CAN
        IOHW --> PWM_SIM

        note bottom of CAN
            **CAN Signals**:
            • Vehicle_Speed (0x100)
            • Drive_Mode (0x101)
            • Door_Status (0x102)
            • Gear_Position (0x103)
            • HVAC_Temp (0x104)
            • IVI_Color_Cmd (0x200)
        end note
    }
}

caption Lighting Control Architecture - AUTOSAR ASW Components
@enduml
```

---

## 2. Speed-Linked Ambient Lighting State Machine

```plantuml
@startuml
!theme materia-outline

title REQ_IVI_001: Sport Mode Speed-Linked Ambient Lighting

[*] --> Idle

state "Idle" as Idle {
    Idle : Sport Mode = OFF
    Idle : Color = Default
}

state "Sport Mode Active" as Sport {
    state "Speed_0_50" as S1 {
        S1 : Speed: 0~50 km/h
        S1 : Color: GREEN
        S1 : Transition: <500ms
    }

    state "Speed_50_100" as S2 {
        S2 : Speed: 50~100 km/h
        S2 : Color: BLUE
        S2 : Transition: <500ms
    }

    state "Speed_100_Plus" as S3 {
        S3 : Speed: 100+ km/h
        S3 : Color: RED
        S3 : Transition: <500ms
    }

    [*] --> S1
    S1 --> S2 : Speed >= 50
    S2 --> S3 : Speed >= 100
    S3 --> S2 : Speed < 100
    S2 --> S1 : Speed < 50
}

Idle --> Sport : Sport Mode ON
Sport --> Idle : Sport Mode OFF

note right of Sport
    **ASIL-B Requirement**
    • Color transition must complete
      within 500ms of speed change
    • CAN signal update rate: 100ms
    • RGB command latency budget: 400ms
end note

@enduml
```

---

## 3. Door-Linked Lighting Sequence

```plantuml
@startuml
!theme materia-outline

title REQ_IVI_003, 017: Door-Linked UX & Reverse Lighting

actor "Driver" as Driver
participant "CAN Bus" as CAN
participant "Dashboard_Lighting_Controller" as DLC
participant "LED_Actuator" as LED

== Door Open Scenario (REQ_IVI_003) ==

Driver -> CAN : Door Open Signal (0x102)
activate CAN
CAN -> DLC : Door_Status = OPEN
activate DLC
note right: Response Time Budget: <400ms

DLC -> DLC : Validate Signal
DLC -> LED : Turn ON Dashboard Light
activate LED
LED --> DLC : ACK
deactivate LED

DLC --> CAN : Status Confirmation
deactivate DLC
deactivate CAN

note over DLC
    **ASIL-A Requirement**
    • Detection: >99%
    • Response: <400ms
    • Auto OFF when door closed
end note

== Reverse Gear Scenario (REQ_IVI_017) ==

Driver -> CAN : Gear Position = R (0x103)
activate CAN
CAN -> DLC : Gear_Position = REVERSE
activate DLC
note right: Response Time Budget: ≤150ms

DLC -> DLC : Validate Reverse State
DLC -> LED : Turn ON Rear Light
activate LED
LED --> DLC : ACK
deactivate LED

DLC --> CAN : Status Confirmation
deactivate DLC

... Reverse Operation ...

Driver -> CAN : Gear Position = D/N
CAN -> DLC : Gear_Position = DRIVE/NEUTRAL
activate DLC
DLC -> LED : Turn OFF Rear Light
activate LED
LED --> DLC : ACK
deactivate LED
deactivate DLC
deactivate CAN

note over DLC
    **ASIL-B Requirement**
    • Lighting ON delay: ≤150ms
    • Auto OFF on D/N transition
    • Integration Test Required
end note

@enduml
```

---

## 4. IVI Color Synchronization Flow

```plantuml
@startuml
!theme silver

title REQ_IVI_004: IVI Color Synchronization (>99%)

participant "IVI HMI" as IVI
participant "CAN Bus" as CAN
participant "IVI_Sync_Manager" as ISM
participant "Lighting_Module" as LM

IVI -> IVI : User Selects Color\n(RGB: 255, 128, 64)
activate IVI

IVI -> CAN : IVI_Color_Cmd (0x200)\n[R=255, G=128, B=64]
activate CAN

CAN -> ISM : Receive Color Command
activate ISM

ISM -> ISM : Parse RGB Values
ISM -> ISM : Validate Range (0-255)

alt Valid Color Command
    ISM -> LM : Apply RGB to Interior Lighting
    activate LM
    LM -> LM : Set LED PWM Duty Cycle
    LM --> ISM : Color Applied Successfully
    deactivate LM

    ISM -> CAN : Sync Confirmation (0x201)
    CAN -> IVI : Display "Color Applied"
    deactivate ISM
    deactivate CAN
    deactivate IVI

else Invalid Color Command
    ISM -> CAN : Error Response (0x7F)
    CAN -> IVI : Display "Color Sync Failed"
    deactivate ISM
    deactivate CAN
    deactivate IVI
end

note over ISM
    **QM Requirement**
    • Synchronization Rate: >99%
    • CAN Message Reliability
    • No Safety Impact
end note

@enduml
```

---

## 5. Performance Metrics Summary

| Requirement ID | Function | Performance Metric | ASIL | Status |
|---|---|---|---|---|
| REQ_IVI_001 | Sport Mode Speed-Linked | Color Transition <500ms | ASIL-B | ✅ Implemented |
| REQ_IVI_003 | Door-Linked UX | Response <400ms | ASIL-A | ✅ Implemented |
| REQ_IVI_004 | IVI Color Sync | Sync Rate >99% | QM | ✅ Implemented |
| REQ_IVI_005 | Temperature-Linked | Error <5% | QM | 🔄 Phase 2 |
| REQ_IVI_017 | Reverse Rear Light | Delay ≤150ms | ASIL-B | ✅ Implemented |
| REQ_IVI_042 | Theme Auto-Apply | Response <100ms | QM | ✅ Implemented |

---

## 6. Safety Considerations

### ASIL-B Components
- **Ambient_Light_Controller**: Sport mode speed-linked logic
- **Dashboard_Lighting_Controller** (Reverse): Rear lighting control

### ASIL-A Components
- **Dashboard_Lighting_Controller** (Door): Door-linked UX

### QM (Non-Critical) Components
- **IVI_Sync_Manager**: Color synchronization
- **Theme_Manager**: Mode-based theme application

---

**Back to**: [Main Architecture Overview](../../architecture_overview.md)
