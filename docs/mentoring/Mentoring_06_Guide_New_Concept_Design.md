> [!NOTE]
> **[GUIDE DOCUMENT]**
> 이 문서는 우리 프로젝트의 요구사항(`REQ_IVI_vECU`)을 **멘토의 샘플 형식에 맞추면 어떻게 되는지 보여주는 예시 가이드**입니다.
> 아키텍처를 그리기 위한 **참조 가이드**로 활용하세요.

# 가이드: [REQ_IVI_vECU] 기반 컨셉 디자인 및 아키텍처 재설계

제공해주신 `REQ_IVI_vECU_Requirements.xlsx`의 요구사항을 분석하여, 멘토가 원하는 **V-Model 및 CAN Bus 아키텍처**로 변환하는 방법을 안내합니다.

---

## 1. 기존 다이어그램에 대한 답변

> **Q: 우리가 작성한 다이어그램들은 무엇인가요? 폐기해야 하나요?**

**A: 폐기하지 마시고 '논리(Logical) 아키텍처'로 분류해 두세요.**

기존에 그리신 'Star Topology(중앙 집중형)'나 '이더넷 기반' 그림은, 차량의 **논리적인 연결 관계**(누가 누구와 통신하는지)를 표현한 것입니다. 이는 틀린 그림이 아니라 **관점이 다른 그림**입니다.
다만, 멘토가 요구하는 것은 **물리(Physical) 아키텍처**와 **실제 제어 흐름**이므로, 이번 과제 제출용으로는 **새로 그리는 것**이 맞습니다. 기존 그림은 "추후 이더넷 도입 시 참조 모델"로 남겨두시면 됩니다.

---

## 2. 요구사항 분석 및 도메인 할당

엑셀의 요구사항들을 분석하여 4가지 핵심 도메인으로 분류했습니다. 이 표를 먼저 작성하세요.

### 2.1 Domain & ECU 정의 (Concept Design)

| 도메인 | ECU 이름 | 주요 역할 및 기능 (Function Definition) | 근거(Req ID) |
| :--- | :--- | :--- | :--- |
| **ADAS** | **ADAS Unit** | - 전방 레이더/카메라 센서 데이터 처리<br>- 앞차 거리 유지(SCC) 및 차선 유지(LKA) 판단<br>- 하이빔 자동 제어(HBA) 판단 | Req_01~05 |
| **Chassis** | **Brake/Steer Unit** | - ADAS의 감속 요청을 받아 실제 **제동(Brake)** 압력 제어<br>- LKA 조향 요청을 받아 **핸들(Steering)** 제어 | Req_02, 06 |
| **Body** | **Body Control Unit** | - **창문(Window)** 개폐 제어 (음성/버튼)<br>- **시트(Seat)** 위치 제어 (IMS)<br>- **헤드램프** On/Off/HighBeam 제어 | Req_07~15 |
| **IVI** | **IVI Unit (Head Unit)** | - 운전자에게 ADAS 상태(SCC On/Off, 경고) **표시**<br>- 공조/시트 상태 **모니터링 및 터치 제어**<br>- 음성 인식 명령 수신 | Req_16~20 |

---

## 3. 아키텍처 (Architecture) 그리기 가이드

멘토가 원하는 **CAN Bus Topology**로 그리는 방법입니다. 종이나 PPT에 이 구조를 따라 그리세요.

### Level 1: Vehicle System Architecture

**핵심**: 가운데 **두 줄의 굵은 선(CAN Bus)**을 그리고, 각 ECU를 **빨랫줄에 걸린 옷**처럼 매다세요.

```mermaid
graph TD
    %% Bus Backbone
    BUS[[=== CAN BUS (High Speed) ===]]

    %% Nodes connected to Bus
    ADAS[ADAS ECU] --- BUS
    CHASSIS[Chassis/Brake ECU] --- BUS
    BODY[Body Control ECU] --- BUS
    IVI[IVI / Cluster ECU] --- BUS

    %% Physical Sensors/Actuators (Connected to ECUs, NOT Bus)
    Radar((Radar)) --- ADAS
    Camera((Camera)) --- ADAS
    Motor((Brake Actuator)) --- CHASSIS
    Lamp((Headlamp)) --- BODY
    Display((Display Panel)) --- IVI
```

**(그리는 팁)**
1.  가운데 **긴 직사각형(CAN Bus)**을 하나 그립니다.
2.  그 주변에 `ADAS ECU`, `Chassis ECU`, `Body ECU`, `IVI ECU` 네모 상자를 배치합니다.
3.  각 ECU 상자에서 선을 하나씩 빼서 **CAN Bus**에 연결합니다. (점 대 점 연결 X)
4.  각 ECU 상자 밖에는 실제 부품(센서, 모터, 램프)을 연결하여 그림을 풍성하게 만듭니다.

---

## 4. 네트워크 데이터 흐름 (Network Flow)

아키텍처 위에 흐르는 데이터를 정의합니다. (샘플 파일의 `0302` 시트 대응)

| 보내는 놈 (Source) | 받는 놈 (Destination) | 데이터 내용 (Content) |
| :--- | :--- | :--- |
| **ADAS ECU** | Chassis ECU | "감속해라" (Target Deceleration) |
| **ADAS ECU** | Body ECU | "하이빔 켜라" (High Beam Cmd) |
| **ADAS ECU** | IVI ECU | "SCC 켜졌다" (SCC Status) |
| **Body ECU** | IVI ECU | "창문 열렸다" (Window Status) |
| **IVI ECU** | Body ECU | "창문 열어라" (Window Control Cmd) |

> **작성 팁**: 이 표를 먼저 손으로 작성해보고, 이걸 그대로 화살표로 아키텍처 그림 위에 덧그리면 **Level 2/3 다이어그램**이 됩니다.

---

## 5. 요약

1.  **기존 그림**: 버리지 말고 보관 (Logical View).
2.  **새 그림**:
    *   **ADAS / Body / Chassis / IVI** 4개 덩어리로 나눈다.
    *   가운데 **CAN Bus**를 긋고 다 연결한다.
    *   **ADAS**는 명령하고, **Chassis/Body**는 움직이고, **IVI**는 보여준다.
    *   이 흐름대로 화살표를 그린다.
