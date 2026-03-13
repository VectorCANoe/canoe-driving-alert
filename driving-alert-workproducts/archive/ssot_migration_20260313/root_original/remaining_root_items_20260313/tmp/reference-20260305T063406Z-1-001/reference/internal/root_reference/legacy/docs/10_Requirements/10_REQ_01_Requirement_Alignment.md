> [!IMPORTANT]
> **[ACTUAL PROJECT OUTPUT]**
> 이 문서는 멘토의 샘플 서식이 아니라, **우리 팀의 실제 요구사항(`REQ_IVI_vECU`)**을 정리한 **실제 프로젝트 산출물**입니다.
> V-Model의 '요구사항 명세' 단계에 해당합니다.

# Requirement Alignment: V-Model Mapping

This document maps our project's requirements (from `REQ_IVI_vECU_Requirements.xlsx`) to the simplified structural format requested by the mentor (based on `Project Result_Sample.xlsx`).

> **Note**: This document serves as the "Requirements Specification" (Level 1 of V-Cycle).

## 1. Functional Requirements (기능 요구사항)

| Rec. ID | Category | Summary | Description | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **REQ_001** | ADAS | **SCC Activation** (스마트 크루즈 컨트롤) | 운전자가 SCC 버튼을 누르면 설정된 속도(예: 80km/h)로 정속 주행을 시작한다. | High |
| **REQ_002** | ADAS | **SCC Distance Control** (차간 거리 유지) | 전방 차량과의 거리가 설정값(예: 50m) 이하로 좁혀지면 자동으로 감속한다. | Critical |
| **REQ_003** | ADAS | **LKA Activation** (차선 유지 보조) | 차량이 차선을 이탈하려 할 때(카메라 감지), 조향을 제어하여 차선 안으로 복귀시킨다. | High |
| **REQ_004** | Body | **HBA Control** (하이빔 보조) | 주변 광량이 낮고 전방에 차량이 없을 때, 자동으로 상향등(High Beam)을 켠다.  | Medium |
| **REQ_005** | Body | **Window Control** (창문 제어) | 운전석/조수석 창문 스위치 조작 시 해당 창문을 개폐한다. (졸음운전 시 자동 개방 포함) | Low |
| **REQ_006** | Body | **Seat Control** (시트 제어) | IMS(메모리 시트) 설정에 따라 시트 포지션을 자동으로 조정한다. | Low |
| **REQ_007** | Body | **Door Lock/Unlock** | 주행 속도가 일정 이상(예: 20km/h) 되면 자동으로 도어를 잠근다. | Medium |
| **REQ_008** | IVI | **Vehicle Status Display** | 속도, RPM, 배터리 전압, ADAS 상태(On/Off)를 실시간으로 화면에 표시한다. | High |
| **REQ_009** | IVI | **Warning Alert** | 졸음운전 감지 또는 전방 충돌 위험 시 경고음과 팝업을 출력한다. | Critical |
| **REQ_010** | IVI | **Media Control** | 블루투스/라디오 미디어 재생, 일시정지, 볼륨 조절 기능을 제공한다. | Low |

## 2. Non-Functional Requirements (비기능 요구사항)

| Rec. ID | Category | Summary | Description | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **NFR_001** | Performance | **Boot Time** | 시동(IG On) 후 IVI 화면이 2초 이내에 켜져야 한다. | High |
| **NFR_002** | Performance | **CAN Latency** | 주요 제어 신호(조향, 제동)의 CAN 통신 지연시간은 10ms 이내여야 한다. | Critical |
| **NFR_003** | Safety | **Fail-Safe** | 센서 고장 시 SCC/LKA 기능을 즉시 해제하고 운전자에게 경고해야 한다. | Critical |

---

## 3. Analysis & Next Steps

This alignment simplifies our detailed engineering requirements into high-level "User Stories" suitable for the System Architecture phase.

**Next Step**: Map each `REQ_ID` to a logical functional block in the **Function Definition** phase.
