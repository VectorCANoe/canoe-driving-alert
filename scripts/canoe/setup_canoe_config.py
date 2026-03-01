"""
setup_canoe_config.py
CANoe Simulation Setup 자동 구성 스크립트

실행 전 확인:
  - CANoe가 실행 중이어야 함
  - 측정(Measurement)이 중지된 상태여야 함

실행:
  python scripts/canoe/setup_canoe_config.py
"""

import win32com.client
import time
import os
import sys

# ── 경로 설정 ──────────────────────────────────────────
BASE    = r"C:\Users\이준영\canoe-driving-alert\canoe"
CFG     = os.path.join(BASE, r"cfg\CAN_500kBaud_1ch_split.cfg")
DBC     = os.path.join(BASE, r"databases\chassis_can.dbc")
SYSVARS = os.path.join(BASE, r"project\sysvars\project.sysvars")
NODES_DIR = os.path.join(BASE, "nodes")

NODES = [
    "Context_Manager",
    "Police_Node",
    "Ambulance_Node",
    "Civ_Node",
    "Ambient_ECU",
    "Cluster_ECU",
]

def wait(sec, msg=""):
    if msg:
        print(f"  ⏳ {msg}")
    time.sleep(sec)

def main():
    # ── 1. CANoe 연결 ──────────────────────────────────
    print("▶ CANoe 연결 중...")
    try:
        app = win32com.client.Dispatch("CANoe.Application")
        print(f"  ✅ CANoe {app.Version} 연결됨")
    except Exception as e:
        print(f"  ❌ CANoe 연결 실패: {e}")
        print("     → CANoe가 실행 중인지 확인하세요")
        sys.exit(1)

    # ── 2. 측정 중지 확인 ──────────────────────────────
    meas = app.Measurement
    if meas.Running:
        print("▶ 측정 중지 중...")
        meas.Stop()
        wait(2, "측정 중지 대기")

    # ── 3. CFG 열기 ────────────────────────────────────
    print(f"▶ 설정 파일 열기: {CFG}")
    try:
        app.Open(CFG, 0, 0)
        wait(3, "설정 로드 대기")
        print("  ✅ 설정 파일 로드됨")
    except Exception as e:
        print(f"  ❌ 설정 파일 열기 실패: {e}")
        sys.exit(1)

    cfg = app.Configuration
    sim = cfg.SimulationSetup

    # ── 4. 기존 노드/DB 정리 ───────────────────────────
    print("▶ 기존 구성 초기화...")
    try:
        busses = sim.Busses
        bus_count = busses.Count
        print(f"  버스 수: {bus_count}")
        for i in range(1, bus_count + 1):
            bus = busses.Item(i)
            print(f"  버스[{i}]: {bus.Name}")
    except Exception as e:
        print(f"  ⚠ 버스 정보 조회 실패: {e}")

    # ── 5. DBC 추가 ────────────────────────────────────
    print(f"▶ DBC 추가: {DBC}")
    try:
        # py_canoe 방식
        from py_canoe import CANoe as PyCANoe
        py = PyCANoe()
        py.application.com_object = app  # 기존 인스턴스 재사용

        result = py.add_database(DBC, 1, "CAN")
        print(f"  ✅ DBC 추가 완료: {result}")
    except Exception as e:
        print(f"  ⚠ py_canoe 방식 실패, COM 직접 시도: {e}")
        try:
            busses = sim.Busses
            for i in range(1, busses.Count + 1):
                bus = busses.Item(i)
                if "CAN" in bus.Name.upper():
                    db_setup = bus.Databases
                    db_setup.Add(DBC)
                    print(f"  ✅ DBC 추가 완료 (COM 직접)")
                    break
        except Exception as e2:
            print(f"  ❌ DBC 추가 실패: {e2}")

    wait(1)

    # ── 6. 노드 추가 ────────────────────────────────────
    print("▶ 노드 추가 중...")
    try:
        busses = sim.Busses
        target_bus = None
        for i in range(1, busses.Count + 1):
            bus = busses.Item(i)
            if "CAN" in bus.Name.upper():
                target_bus = bus
                break

        if target_bus is None:
            print("  ❌ CAN 버스를 찾을 수 없음")
        else:
            nodes_obj = target_bus.Nodes
            for node_name in NODES:
                capl_path = os.path.join(NODES_DIR, f"{node_name}.can")
                try:
                    # 기존 노드 중복 체크
                    exists = False
                    for j in range(1, nodes_obj.Count + 1):
                        if nodes_obj.Item(j).Name == node_name:
                            exists = True
                            print(f"  ⚠ 이미 존재: {node_name} (스킵)")
                            break

                    if not exists:
                        node = nodes_obj.Add()
                        node.Name = node_name
                        # CAPL 파일 연결
                        node.Modules.Add(capl_path)
                        print(f"  ✅ 노드 추가: {node_name}")
                except Exception as e:
                    print(f"  ❌ 노드 추가 실패 ({node_name}): {e}")

    except Exception as e:
        print(f"  ❌ 노드 추가 실패: {e}")

    wait(1)

    # ── 7. System Variables 로드 ────────────────────────
    print(f"▶ System Variables 로드: {SYSVARS}")
    try:
        env = cfg.SystemVariables
        env.Load(SYSVARS)
        print("  ✅ System Variables 로드 완료")
    except Exception as e:
        print(f"  ⚠ SystemVariables.Load 실패, 다른 방법 시도: {e}")
        try:
            app.Configuration.SystemVariables.Add(SYSVARS)
            print("  ✅ System Variables 추가 완료 (Add 방식)")
        except Exception as e2:
            print(f"  ❌ System Variables 로드 실패: {e2}")
            print("     → 수동: Environment → System Variables → Load 메뉴 사용")

    wait(1)

    # ── 8. 저장 ─────────────────────────────────────────
    print(f"▶ 설정 저장: {CFG}")
    try:
        cfg.SaveAs(CFG, True)
        print("  ✅ 저장 완료")
    except Exception as e:
        try:
            cfg.Save()
            print("  ✅ 저장 완료 (Save)")
        except Exception as e2:
            print(f"  ❌ 저장 실패: {e2}")

    # ── 9. 결과 확인 ────────────────────────────────────
    print("\n▶ 구성 결과 확인...")
    try:
        busses = sim.Busses
        for i in range(1, busses.Count + 1):
            bus = busses.Item(i)
            print(f"  버스: {bus.Name}")
            dbs = bus.Databases
            for j in range(1, dbs.Count + 1):
                print(f"    DB[{j}]: {dbs.Item(j).FullName}")
            nds = bus.Nodes
            for j in range(1, nds.Count + 1):
                print(f"    Node[{j}]: {nds.Item(j).Name}")
    except Exception as e:
        print(f"  ⚠ 결과 확인 실패: {e}")

    print("\n✅ 설정 완료!")
    print("   → CANoe에서 측정 시작(F9) 후 MCP 검증 가능")


if __name__ == "__main__":
    main()
