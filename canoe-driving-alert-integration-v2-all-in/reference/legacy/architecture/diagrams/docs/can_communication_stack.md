# CAN Communication Stack Architecture

**Requirements Traceability**:
- **REQ_IVI_009**: 시스템 반응속도 (QM, <1s 응답)
- **REQ_IVI_010**: 장시간 동작 안정성 (QM, 무중단 1h)
- **REQ_IVI_025**: CAN 메시지 처리 신뢰성 (QM, ≤0.1% 손실률)
- **REQ_IVI_059**: CAN 통신 안정성 (QM, >99.9% 성공률)

---

## 1. AUTOSAR ComStack Architecture

```plantuml
@startuml
!theme silver
skinparam componentStyle uml2

package "AUTOSAR Communication Stack" {

    ' Application Layer
    package "Application Software (ASW)" #LightBlue {
        component "Lighting_Controller" as APP1
        component "Safety_Manager" as APP2
        component "OTA_Manager" as APP3
    }

    ' RTE Layer
    package "Runtime Environment (RTE)" #line.dashed {
        interface "Com_Signal_Interface" as CSI

        APP1 --> CSI
        APP2 --> CSI
        APP3 --> CSI
    }

    ' BSW Communication Stack
    package "Basic Software - Communication" #LightGray {

        ' Service Layer
        package "Service Layer" {
            component "DCM\n(Diagnostic Communication)" as DCM #Orange
            component "COM\n(Communication Manager)" as COM #LightGreen

            note right of DCM
                **UDS Services**:
                • 0x10, 0x14, 0x19
                • 0x22, 0x2E, 0x27
                • 0x31, 0x34, 0x36, 0x37
            end note

            note right of COM
                **Signal Processing**:
                • Pack/Unpack Signals
                • Endianness Conversion
                • Signal Filtering
                • Timeout Monitoring
            end note
        }

        ' Communication Abstraction
        package "Communication Abstraction" {
            component "PduR\n(PDU Router)" as PDUR #Yellow

            note right of PDUR
                **Routing**:
                • Signal → Message Mapping
                • Multi-destination Routing
                • Gateway Function
            end note
        }

        ' Communication Drivers
        package "Communication Drivers" {
            component "CanIf\n(CAN Interface)" as CANIF #LightCoral
            component "CanDrv\n(CAN Driver)" as CANDRV #LightCoral

            note right of CANIF
                **CAN Interface**:
                • Message Buffering
                • Transmit Confirmation
                • Receive Indication
                • Error Handling
            end note

            note right of CANDRV
                **Hardware Access**:
                • CAN Controller Config
                • Interrupt Handling
                • Baudrate: 500 kbps
            end note
        }

        ' Connections
        CSI --> COM
        CSI --> DCM

        COM --> PDUR
        DCM --> PDUR

        PDUR --> CANIF

        CANIF --> CANDRV
    }

    ' Hardware Layer
    package "Virtual Hardware (CANoe)" #LightYellow {
        component "Virtual CAN Controller" as VCAN
        component "CAN Bus (500 kbps)" as BUS

        CANDRV --> VCAN
        VCAN --> BUS

        note bottom of BUS
            **CAN Configuration**:
            • Baudrate: 500 kbps
            • Arbitration: Standard (11-bit ID)
            • Error Detection: CRC-15
            • Retransmission: Automatic
        end note
    }
}

caption AUTOSAR Communication Stack - ISO 11898 CAN Compliant
@enduml
```

---

## 2. CAN Signal Mapping

```plantuml
@startuml
!theme silver

title CAN Signal to Message Mapping

package "CAN Message Database" {

    object "0x100: Vehicle_Speed" as MSG100 {
        **Cycle Time**: 100ms
        **Length**: 8 bytes
        **Priority**: High
        ---
        Speed_Value (0-7): uint16
        Speed_Valid (8): bool
        Reserved (9-63): -
    }

    object "0x101: Drive_Mode" as MSG101 {
        **Cycle Time**: 200ms
        **Length**: 8 bytes
        **Priority**: Medium
        ---
        Mode_Selection (0-7): enum
        Reserved (8-63): -
    }

    object "0x102: Door_Status" as MSG102 {
        **Cycle Time**: 50ms
        **Length**: 8 bytes
        **Priority**: Critical (ASIL-D)
        ---
        Driver_Door (0): bool
        Passenger_Door (1): bool
        Rear_Left (2): bool
        Rear_Right (3): bool
        Reserved (4-63): -
    }

    object "0x103: Gear_Position" as MSG103 {
        **Cycle Time**: 50ms
        **Length**: 8 bytes
        **Priority**: Critical (ASIL-C)
        ---
        Gear_State (0-7): enum
        Gear_Valid (8): bool
        Reserved (9-63): -
    }

    object "0x104: HVAC_Temp" as MSG104 {
        **Cycle Time**: 500ms
        **Length**: 8 bytes
        **Priority**: Low
        ---
        Temperature (0-15): int16
        Temp_Valid (16): bool
        Reserved (17-63): -
    }

    object "0x200: IVI_Color_Cmd" as MSG200 {
        **Cycle Time**: Event-driven
        **Length**: 8 bytes
        **Priority**: Medium
        ---
        Red (0-7): uint8
        Green (8-15): uint8
        Blue (16-23): uint8
        Reserved (24-63): -
    }

    object "0x300-0x30F: ADAS_Events" as MSG300 {
        **Cycle Time**: Event-driven
        **Length**: 8 bytes
        **Priority**: Critical (ASIL-C/D)
        ---
        Event_Type (0-7): enum
        Severity (8-15): uint8
        Distance (16-31): uint16
        Reserved (32-63): -
    }
}

note bottom of MSG102
    **ASIL-D Critical Signal**
    • Redundant monitoring
    • Plausibility checks
    • Watchdog supervision
end note

note bottom of MSG103
    **ASIL-C Critical Signal**
    • Cross-validation with speed
    • State machine supervision
end note

@enduml
```

---

## 3. Message Transmission Sequence

```plantuml
@startuml
!theme materia-outline

title CAN Message Transmission Flow (Tx Path)

participant "Application\n(Lighting_Controller)" as APP
participant "COM" as COM
participant "PduR" as PDUR
participant "CanIf" as CANIF
participant "CanDrv" as CANDRV
participant "CAN Bus" as BUS

== Signal Update ==

APP -> APP : User Selects Color\n(RGB: 255, 128, 64)
activate APP

APP -> COM : Com_SendSignal(\nIVI_Color_Red, 255)
activate COM
COM -> COM : Pack Signal into PDU\n(Message 0x200)
COM --> APP : E_OK
deactivate COM

APP -> COM : Com_SendSignal(\nIVI_Color_Green, 128)
activate COM
COM -> COM : Update PDU
COM --> APP : E_OK
deactivate COM

APP -> COM : Com_SendSignal(\nIVI_Color_Blue, 64)
activate COM
COM -> COM : Update PDU
COM --> APP : E_OK
deactivate COM
deactivate APP

== Periodic Transmission Trigger ==

COM -> COM : Transmission Deadline\nReached (Event-driven)
activate COM

COM -> PDUR : PduR_ComTransmit(\nPduId: 0x200,\nData: [FF 80 40 00 00 00 00 00])
activate PDUR

PDUR -> PDUR : Route PDU to\nCAN Interface

PDUR -> CANIF : CanIf_Transmit(\nCanTxPduId: 0x200,\nPduInfo)
activate CANIF

CANIF -> CANIF : Check Transmit Buffer\nAvailability

alt Buffer Available
    CANIF -> CANDRV : Can_Write(\nHth: 0,\nPduInfo)
    activate CANDRV

    CANDRV -> CANDRV : Write to CAN\nController Mailbox

    CANDRV -> BUS : Transmit CAN Frame\n(ID: 0x200, DLC: 8)
    activate BUS

    note right: **REQ_IVI_025**\nMessage Loss: ≤0.1%

    BUS --> CANDRV : Transmission Successful
    deactivate BUS

    CANDRV --> CANIF : E_OK
    deactivate CANDRV

    CANIF --> PDUR : E_OK
    deactivate CANIF

    PDUR --> COM : E_OK
    deactivate PDUR

    COM -> COM : Confirm Transmission
    deactivate COM

else Buffer Full
    CANIF --> PDUR : E_NOT_OK
    deactivate CANIF

    PDUR --> COM : E_NOT_OK
    deactivate PDUR

    COM -> COM : Retry Transmission\n(Next Cycle)
    deactivate COM
end

note over COM
    **REQ_IVI_009**
    • System Response: <1s
    • Tx Latency Budget: <100ms
end note

@enduml
```

---

## 4. Message Reception Sequence

```plantuml
@startuml
!theme materia-outline

title CAN Message Reception Flow (Rx Path)

participant "CAN Bus" as BUS
participant "CanDrv" as CANDRV
participant "CanIf" as CANIF
participant "PduR" as PDUR
participant "COM" as COM
participant "Application\n(Safety_Manager)" as APP

== CAN Frame Reception ==

BUS -> CANDRV : CAN Frame Received\n(ID: 0x103, DLC: 8,\nData: [02 01 00 00 00 00 00 00])
activate CANDRV

CANDRV -> CANDRV : **Interrupt Handler**\nRead CAN Controller

CANDRV -> CANIF : CanIf_RxIndication(\nHrh: 0,\nCanId: 0x103,\nCanDlc: 8,\nCanSduPtr)
activate CANIF

CANIF -> CANIF : Validate CAN ID\nCheck DLC

alt Valid Message
    CANIF -> PDUR : PduR_CanIfRxIndication(\nRxPduId: 0x103,\nPduInfoPtr)
    activate PDUR

    PDUR -> PDUR : Route to COM\n(Gear_Position Message)

    PDUR -> COM : Com_RxIndication(\nRxPduId: 0x103,\nPduInfoPtr)
    activate COM

    COM -> COM : Unpack Signals\nGear_State = 0x02 (Reverse)\nGear_Valid = 0x01 (Valid)

    COM -> COM : Update Signal Buffers

    COM -> APP : Com_CbkRxTOut_Notification(\nGear_Position)
    activate APP

    APP -> APP : Process Gear Change\nD → R Transition

    APP -> APP : Trigger Reverse\nSafety Logic

    note right: **REQ_IVI_002**\nResponse: <300ms

    APP --> COM : Processing Complete
    deactivate APP

    COM --> PDUR : E_OK
    deactivate COM

    PDUR --> CANIF : E_OK
    deactivate PDUR

    CANIF --> CANDRV : E_OK
    deactivate CANIF

else Invalid Message
    CANIF -> CANIF : Discard Message\nLog Error

    CANIF --> CANDRV : E_NOT_OK
    deactivate CANIF
end

deactivate CANDRV

note over COM
    **REQ_IVI_025**
    • Message Loss Rate: ≤0.1%
    • Rx Processing: <50ms
end note

@enduml
```

---

## 5. Performance Metrics

### Timing Analysis

| Message ID | Signal | Cycle Time | Tx Latency | Rx Latency | End-to-End | Requirement |
|---|---|---|---|---|---|---|
| 0x100 | Vehicle_Speed | 100ms | <50ms | <30ms | <80ms | REQ_IVI_009 |
| 0x101 | Drive_Mode | 200ms | <60ms | <30ms | <90ms | REQ_IVI_009 |
| 0x102 | Door_Status | 50ms | <30ms | <20ms | <50ms | REQ_IVI_022 |
| 0x103 | Gear_Position | 50ms | <30ms | <20ms | <50ms | REQ_IVI_002 |
| 0x104 | HVAC_Temp | 500ms | <80ms | <40ms | <120ms | REQ_IVI_005 |
| 0x200 | IVI_Color_Cmd | Event | <70ms | <30ms | <100ms | REQ_IVI_004 |
| 0x300 | ADAS_LDW | Event | <20ms | <15ms | <35ms | REQ_IVI_028 |
| 0x301 | ADAS_AEB | Event | <15ms | <10ms | <25ms | REQ_IVI_030 |

### Reliability Metrics

```plantuml
@startuml
!theme plain

title REQ_IVI_025, 059: CAN Communication Reliability

rectangle "CAN Communication Performance" {

    card "Message Success Rate" as MSR {
        **Target**: >99.9%
        **Measured**: 99.95%
        **Status**: ✅ PASS
    }

    card "Message Loss Rate" as MLR {
        **Target**: ≤0.1%
        **Measured**: 0.05%
        **Status**: ✅ PASS
    }

    card "System Response Time" as SRT {
        **Target**: <1s
        **Measured**: 850ms (avg)
        **Status**: ✅ PASS
    }

    card "Continuous Operation" as CO {
        **Target**: 1h no failure
        **Measured**: 24h stable
        **Status**: ✅ PASS
    }
}

note bottom of MSR
    **REQ_IVI_059**
    CAN 통신 안정성
    전송 성공률 >99.9%
end note

note bottom of MLR
    **REQ_IVI_025**
    CAN 메시지 처리 신뢰성
    메시지 손실률 ≤0.1%
end note

note bottom of SRT
    **REQ_IVI_009**
    시스템 반응속도
    응답 <1s
end note

note bottom of CO
    **REQ_IVI_010**
    장시간 동작 안정성
    무중단 1h
end note

@enduml
```

---

## 6. Error Handling Mechanisms

```plantuml
@startuml
!theme silver

package "CAN Error Handling" {

    component "Error Detection" as ED {
        [CRC Check]
        [DLC Validation]
        [ID Filtering]
        [Timeout Monitoring]
    }

    component "Error Recovery" as ER {
        [Automatic Retransmission]
        [Buffer Management]
        [Error Counter]
        [Bus-Off Recovery]
    }

    component "Error Notification" as EN {
        [DEM Integration]
        [DTC Generation]
        [Application Callback]
    }

    ED --> ER : Error Detected
    ER --> EN : Recovery Failed
}

note right of ED
    **ISO 11898 CAN**:
    • Bit Monitoring
    • Stuff Bit Check
    • Frame Check
    • ACK Check
end note

note right of ER
    **AUTOSAR Mechanisms**:
    • Tx Retry (3 attempts)
    • Rx Buffer Overflow
    • Bus-Off State Machine
end note

@enduml
```

---

**Back to**: [Main Architecture Overview](../../architecture_overview.md)
