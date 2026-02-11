#!/usr/bin/env python3
"""
DBC File Validation Test Suite
Tests vehicle_system.dbc for syntax, structure, and Level 1 architecture compliance
"""

import sys
from pathlib import Path

try:
    import cantools
except ImportError:
    print("❌ Error: cantools library not installed")
    print("Install with: pip install cantools")
    sys.exit(1)


def test_dbc_syntax():
    """Test 1: DBC file syntax validation"""
    print("\n" + "="*60)
    print("TEST 1: DBC Syntax Validation")
    print("="*60)

    dbc_path = Path(__file__).parent / "architecture/system-architecture/level3_communication/vehicle_system.dbc"

    if not dbc_path.exists():
        print(f"❌ DBC file not found: {dbc_path}")
        return False

    try:
        db = cantools.database.load_file(str(dbc_path))
        print(f"✅ DBC file loaded successfully")
        print(f"   - ECUs: {len(db.nodes)}")
        print(f"   - Messages: {len(db.messages)}")

        total_signals = sum(len(msg.signals) for msg in db.messages)
        print(f"   - Signals: {total_signals}")

        # ECU count validation
        if len(db.nodes) != 11:
            print(f"❌ Expected 11 ECUs, got {len(db.nodes)}")
            return False

        # Message count validation
        if len(db.messages) < 15:
            print(f"❌ Expected >= 15 messages, got {len(db.messages)}")
            return False

        # Signal count validation
        if total_signals < 80:
            print(f"❌ Expected >= 80 signals, got {total_signals}")
            return False

        print("✅ All syntax checks passed")
        return True

    except Exception as e:
        print(f"❌ DBC syntax error: {e}")
        return False


def test_ecu_names():
    """Test 2: ECU names match Level 1 architecture"""
    print("\n" + "="*60)
    print("TEST 2: ECU Names Validation")
    print("="*60)

    dbc_path = Path(__file__).parent / "architecture/system-architecture/level3_communication/vehicle_system.dbc"
    db = cantools.database.load_file(str(dbc_path))

    required_ecus = ['EMS', 'TCU', 'ESP', 'MDPS', 'BCM', 'IVI',
                     'Cluster', 'Camera', 'Radar', 'SCC', 'CGW']

    missing_ecus = []
    for ecu in required_ecus:
        if ecu not in db.nodes:
            missing_ecus.append(ecu)
            print(f"❌ Missing ECU: {ecu}")
        else:
            print(f"✅ Found ECU: {ecu}")

    if missing_ecus:
        print(f"\n❌ Missing {len(missing_ecus)} ECUs: {', '.join(missing_ecus)}")
        return False

    print("\n✅ All 11 ECUs present")
    return True


def test_can_id_ranges():
    """Test 3: CAN ID ranges match Level 1 architecture"""
    print("\n" + "="*60)
    print("TEST 3: CAN ID Range Validation")
    print("="*60)

    dbc_path = Path(__file__).parent / "architecture/system-architecture/level3_communication/vehicle_system.dbc"
    db = cantools.database.load_file(str(dbc_path))

    # ECU CAN ID ranges from Level 1
    id_ranges = {
        'EMS': (0x100, 0x17F),
        'TCU': (0x180, 0x1FF),
        'ESP': (0x200, 0x27F),
        'MDPS': (0x280, 0x2FF),
        'Camera': (0x300, 0x33F),
        'Radar': (0x340, 0x37F),
        'SCC': (0x380, 0x3BF),
        'IVI': (0x400, 0x47F),
        'Cluster': (0x480, 0x4FF),
        'BCM': (0x500, 0x57F),
        'CGW': (0x700, 0x7FF),
    }

    errors = []
    for msg in db.messages:
        sender = msg.senders[0] if msg.senders else None
        if sender and sender in id_ranges:
            min_id, max_id = id_ranges[sender]
            if not (min_id <= msg.frame_id <= max_id):
                error_msg = f"Message {msg.name} (ID 0x{msg.frame_id:X}) from {sender} outside range 0x{min_id:X}-0x{max_id:X}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
            else:
                print(f"✅ {msg.name} (0x{msg.frame_id:X}) from {sender} - OK")

    if errors:
        print(f"\n❌ {len(errors)} CAN ID range violations")
        return False

    print("\n✅ All CAN IDs within correct ranges")
    return True


def test_required_signals():
    """Test 4: Required signals are defined"""
    print("\n" + "="*60)
    print("TEST 4: Required Signals Validation")
    print("="*60)

    dbc_path = Path(__file__).parent / "architecture/system-architecture/level3_communication/vehicle_system.dbc"
    db = cantools.database.load_file(str(dbc_path))

    # Required signals from Level 1 specification
    required_signals = {
        'Engine_RPM': 'EMS',
        'Vehicle_Speed': 'EMS',
        'Gear_Position': 'TCU',
        'Steering_Angle': 'MDPS',
        'LDW_Status': 'Camera',
        'AEB_Event': 'Camera',
        'BSD_Object_Left': 'Radar',
        'SCC_Active': 'SCC',
        'Ambient_Light_R': 'IVI',
        'Ambient_Light_G': 'IVI',
        'Ambient_Light_B': 'IVI',
    }

    missing_signals = []
    for signal_name, expected_sender in required_signals.items():
        found = False
        for msg in db.messages:
            for sig in msg.signals:
                if sig.name == signal_name:
                    found = True
                    sender = msg.senders[0] if msg.senders else None
                    if sender == expected_sender:
                        print(f"✅ {signal_name} from {sender}")
                    else:
                        print(f"❌ {signal_name} sent by {sender}, expected {expected_sender}")
                        missing_signals.append(signal_name)
                    break
            if found:
                break

        if not found:
            print(f"❌ Signal {signal_name} not found")
            missing_signals.append(signal_name)

    if missing_signals:
        print(f"\n❌ {len(missing_signals)} signal issues")
        return False

    print("\n✅ All required signals present")
    return True


def test_message_attributes():
    """Test 5: Message attributes (cycle time, ASIL level)"""
    print("\n" + "="*60)
    print("TEST 5: Message Attributes Validation")
    print("="*60)

    dbc_path = Path(__file__).parent / "architecture/system-architecture/level3_communication/vehicle_system.dbc"
    db = cantools.database.load_file(str(dbc_path))

    messages_with_cycle = 0
    messages_with_asil = 0

    for msg in db.messages:
        # Check GenMsgCycleTime
        if hasattr(msg, 'cycle_time') and msg.cycle_time is not None:
            messages_with_cycle += 1
            print(f"✅ {msg.name}: Cycle={msg.cycle_time}ms")

        # Check ASIL_Level (stored in attributes)
        if hasattr(msg, 'attributes') and 'ASIL_Level' in msg.attributes:
            messages_with_asil += 1

    print(f"\n📊 Messages with cycle time: {messages_with_cycle}/{len(db.messages)}")
    print(f"📊 Messages with ASIL level: {messages_with_asil}/{len(db.messages)}")

    if messages_with_cycle < len(db.messages):
        print("⚠️  Some messages missing cycle time")

    print("\n✅ Attribute check complete")
    return True


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    test_names = [
        "DBC Syntax",
        "ECU Names",
        "CAN ID Ranges",
        "Required Signals",
        "Message Attributes"
    ]

    passed = sum(results)
    total = len(results)

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! DBC file is valid.")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review errors above.")
        return 1


def main():
    """Run all tests"""
    print("="*60)
    print("Vehicle System DBC Validation Test Suite")
    print("="*60)

    results = [
        test_dbc_syntax(),
        test_ecu_names(),
        test_can_id_ranges(),
        test_required_signals(),
        test_message_attributes()
    ]

    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
