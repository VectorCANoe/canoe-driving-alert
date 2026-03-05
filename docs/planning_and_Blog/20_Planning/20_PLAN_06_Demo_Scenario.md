# 20_PLAN_06_Demo_Scenario.md - 앰비언트 라이팅 시점 제어 시나리오

**날짜**: 2026년 2월 13일 (멘토링 데모용)
**주제**: IVI(Infotainment) ↔ BCM(Body) 양방향 통신 및 Gateway 라우팅 검증

---

## 🚀 데모 목표
1. **차량 분산 시스템 실증**: IVI, CGW, BCM 3개 ECU의 협업 시각화
2. **네트워크 통합 검증**: CAN-HS #2와 CAN-LS 간의 데이터 중계 확인
3. **피드백 루프 확인**: 제어 명령(0x400) 전송 후 실제 상태(0x520) 피드백 수신 과정 증명

---

## 🛠️ 준비 사항 (CANoe 가상 환경)
- **Node 1 (IVI)**: `IVI_AmbientLight (0x400)` 전송 노드
- **Node 2 (CGW)**: 두 네트워크 간 데이터 라우팅 노드
- **Node 3 (BCM)**: `BCM_LightControl (0x520)` 피드백 전송 노드
- **Panel**: IVI 제어 패널 (테마 버튼), BCM 모니터링 패널 (RGB 표시기)

---

## 📝 시나리오 단계 (7 steps)

### Step 1: 사용자 입력 (IVI Node)
- **액션**: 사용자가 IVI Panel에서 **"SPORT"** 버튼 클릭
- **발생 상황**: IVI 내부에서 `Theme_Package = 0` (SPORT) 모드로 상태 천이
- **코드 (CAPL)**:
  ```c
  on control_panel "SPORT_Button" {
    msg_400.Theme_Package = 0; // SPORT
    msg_400.Ambient_Light_R = 255;
    msg_400.Ambient_Light_G = 0;
    msg_400.Ambient_Light_B = 0;
    output(msg_400);
  }
  ```

### Step 2: 메시지 전송 (CAN-HS #2)
- **메시지**: `IVI_AmbientLight (0x400)`
- **데이터**: `FF 00 00 50 00 ...` (Red=255, Brightness=80%)
- **Trace 창 확인**: CAN-HS #2 채널에 0x400 메시지 발생 확인 (주기 100ms)

### Step 3: Gateway 라우팅 (CGW Node)
- **액션**: CGW 노드가 HS2에서 0x400 수신 후 LS로 복사
- **검증 포인트**:
  - CRC 검증 통과 여부
  - `Rule R011` 적용 확인
- **Trace 창 확인**: CAN-LS 채널에 동일한 ID(0x400) 또는 매핑된 노드 수신 확인

### Step 4: BCM 수신 및 LED 제어 (BCM Node)
- **액션**: BCM이 LS에서 0x400 수신하여 가상 LED 구동
- **BCM Panel**: LED 표시등이 **빨간색(Red)**으로 점등됨을 확인
- **Fail-safe 체크**: 만약 AliveCounter가 멈추면 BCM은 '마지막 값 유지' 모드로 이동

### Step 5: BCM 피드백 생성 (CAN-LS)
- **메시지**: `BCM_LightControl (0x520)`
- **데이터**: `01 FF 00 00 ...` (Ambient_Light_Active=1, Actual_R=255)
- **목적**: IVI에 "실제로 빨간색 조명이 켜졌다"는 사실을 알림

### Step 6: Gateway 역방향 라우팅 (CGW Node)
- **액션**: CGW 노드가 LS에서 0x520 수신 후 HS2로 복사
- **검증 포인트**: `Rule R021` 적용 확인
- **Trace 창 확인**: CAN-HS #2 채널에 0x520 메시지 발생

### Step 7: IVI 상태 업데이트 (IVI Node)
- **액션**: IVI Panel에 "Status: ACTIVE" 텍스트 및 현재 조명 색상 리포트 표시
- **성공 메시지**: "Ambient Light: SPORT (Red, 80%) ✓ Active"

---

## 📈 검증 매트릭스 (성공 판정 기준)

| 검증 항목 | 기대 결과 | 확인 도구 |
|-----------|-----------|-----------|
| **메시지 주기** | 0x400: 100ms / 0x520: 100ms 유지 | CANoe Statistics |
| **라우팅 지연** | HS2 ↔ LS 간 지연 시간 5ms 미만 | Graphics Window |
| **데이터 일관성** | IVI 명령값(RGB) == BCM 피드백값(Actual RGB) | Trace Window (Diff) |
| **에러 처리** | CRC 에러 발생 시 BCM 패널에 Error 표시 | Fault Injection Panel |

---

## 💡 멘토 소구 포인트 (Selling Point)
- "데이터가 단순 전달되는 것이 아니라, **Gateway의 보안 및 무결성 검증(CRC)**을 거치는 과정을 시연하겠습니다."
- "사용자 눈에는 버튼 클릭 즉시 불이 켜지는 것 같지만, 실제로는 **네트워크 간 라우팅과 피드백 루프**가 15ms 이내에 완료되는 시스템입니다."

---

**최종 업데이트**: 2026-02-11
**관련 문서**: `50_REP_07_Phase_Walkthrough.md`, `80_TASK_01_Project_Tracking.md`
