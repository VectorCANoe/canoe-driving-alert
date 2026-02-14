# 02_Concept Design (컨셉 디자인) 가이드

> **작성 기준**: 멘토 요구사항 준수 (수작업 다이어그램)
> **작성일**: 2026-02-13
> **목적**: PPT/Visio로 그릴 때 참고용

---

## 📐 그려야 할 다이어그램

1. **Level 1**: 차량 전체 시스템 아키텍처 (CAN 버스 구조)
2. **Level 2**: 도메인별 구성 (데이터 교환)
3. **Level 3**: 통신 구조 (메시지 흐름)
4. **컴포넌트 구성도**: 서비스 목록 및 구성 요소

---

## 🎨 Level 1: 차량 전체 시스템 아키텍처

### PlantUML 코드

```plantuml
@startuml Level1_Vehicle_System_Architecture
!define RECTANGLE class

skinparam componentStyle rectangle
skinparam backgroundColor #FFFFFF
skinparam component {
  BackgroundColor<<gateway>> #FFD700
  BackgroundColor<<infotainment>> #87CEEB
  BackgroundColor<<body>> #90EE90
  BackgroundColor<<adas>> #FFB6C1
  BackgroundColor<<powertrain>> #FFA07A
  BackgroundColor<<chassis>> #DDA0DD
}

title Level 1: 차량 전체 시스템 아키텍처\n(CAN 버스 구조 - 계층적 표현)

package "Infotainment CAN (500 kbps)" {
  [IVI Control ECU] <<infotainment>>
  [vECU\n(IVI vECU)] <<infotainment>>
  [Cluster ECU] <<infotainment>>
}

[Central Gateway] <<gateway>>

package "Body CAN (500 kbps)" {
  [Lighting Control ECU] <<body>>
  [BDC] <<body>>
  [Door Sensors] <<body>>
}

package "ADAS CAN (500 kbps)" {
  [ADAS Control ECU] <<adas>>
  [LDW Sensor] <<adas>>
  [Rear Obstacle Sensor] <<adas>>
  [AEB Sensor] <<adas>>
}

package "Powertrain CAN (500 kbps)" {
  [Transmission Control ECU] <<powertrain>>
  [Vehicle Speed Sensor] <<powertrain>>
}

package "Chassis CAN (500 kbps)" {
  [HVAC Control ECU] <<chassis>>
  [Wiper Control ECU] <<chassis>>
}

' CAN Bus 연결 (한 줄로)
[IVI Control ECU] -down- [vECU\n(IVI vECU)]
[vECU\n(IVI vECU)] -down- [Cluster ECU]
[Cluster ECU] -down- [Central Gateway]

[Central Gateway] -down- [Lighting Control ECU]
[Lighting Control ECU] -right- [BDC]
[BDC] -right- [Door Sensors]

[Central Gateway] -down- [ADAS Control ECU]
[ADAS Control ECU] -right- [LDW Sensor]
[LDW Sensor] -right- [Rear Obstacle Sensor]
[Rear Obstacle Sensor] -right- [AEB Sensor]

[Central Gateway] -down- [Transmission Control ECU]
[Transmission Control ECU] -right- [Vehicle Speed Sensor]

[Central Gateway] -down- [HVAC Control ECU]
[HVAC Control ECU] -right- [Wiper Control ECU]

note right of [Central Gateway]
  중앙 게이트웨이
  - 모든 도메인 간 메시지 라우팅
  - 메시지 필터링
  - 버스 간 중계
end note

@enduml
```

### 수작업으로 그릴 때 포인트 (PPT/Visio)

1. **CAN 버스를 한 줄로 표현**
   ```
   ECU1 ━━━ ECU2 ━━━ ECU3 ━━━ Gateway
   ```
   ❌ 잘못된 표현 (이더넷 방식):
   ```
   ECU1 ─┐
   ECU2 ─┼─ Gateway
   ECU3 ─┘
   ```

2. **색상 구분**
   - Infotainment: 하늘색
   - Body: 녹색
   - ADAS: 분홍색
   - Powertrain: 주황색
   - Chassis: 보라색
   - Gateway: 금색 (강조)

3. **계층 구조**
   - 상단: Infotainment CAN
   - 중앙: Central Gateway (가장 중요)
   - 하단: 각 도메인 CAN (Body, ADAS, Powertrain, Chassis)

---

## 🎨 Level 2: 도메인별 구성 (데이터 교환)

### PlantUML 코드

```plantuml
@startuml Level2_Domain_Architecture
!theme plain

title Level 2: 도메인별 구성\n(도메인 간 데이터 교환만 표현 - 통신 방법 제외)

package "Infotainment Domain" {
  component "vECU\n(IVI vECU)" as vECU
  component "Cluster ECU" as Cluster
  component "IVI Control ECU" as IVI
}

package "Body Domain" {
  component "Lighting\nControl ECU" as Lighting
  component "BDC" as BDC
}

package "ADAS Domain" {
  component "ADAS\nControl ECU" as ADAS
}

package "Powertrain Domain" {
  component "Transmission\nControl ECU" as Trans
  component "Vehicle Speed\nSensor" as Speed
}

package "Chassis Domain" {
  component "HVAC\nControl ECU" as HVAC
  component "Wiper\nControl ECU" as Wiper
}

' 데이터 교환 (통신 방법은 명시하지 않음)
vECU --> Lighting : "조명 색상·밝기\n제어 데이터"
vECU --> Cluster : "경고 UI\n표시 데이터"
vECU --> BDC : "시트 위치\n제어 데이터"

ADAS --> vECU : "LDW/AEB 이벤트\n데이터"
Trans --> vECU : "기어 상태\n데이터"
Speed --> vECU : "차량 속도\n데이터"
HVAC --> vECU : "실내 온도\n데이터"
BDC --> vECU : "도어 개방 상태\n데이터"

IVI --> vECU : "사용자 입력\n(모드, 색상 등)"
vECU --> Cluster : "ADAS 상태 아이콘"

note bottom of vECU
  vECU는 모든 도메인의
  데이터를 수신하여
  조명·경고·UI 제어
end note

@enduml
```

### 수작업으로 그릴 때 포인트

1. **"데이터"만 표현 (통신 방법 X)**
   - ✅ "조명 색상·밝기 제어 데이터"
   - ❌ "CAN High Speed로 조명 제어 메시지 전송"

2. **화살표 방향**
   - 데이터 흐름 방향으로만 표시
   - 양방향은 피하고, 명확한 단방향으로

3. **vECU 중심 구조**
   - vECU가 중앙에 위치
   - 모든 도메인에서 데이터 수신
   - 필요한 제어 데이터 송신

---

## 🎨 Level 3: 통신 구조 (메시지 흐름)

### PlantUML 시퀀스 다이어그램

```plantuml
@startuml Level3_Communication_Flow
!theme plain

title Level 3: 통신 구조 - 시나리오: 후진 안전경고 (Req_002)\n(메시지 흐름 시퀀스)

actor "운전자" as Driver
participant "IVI Control ECU" as IVI
participant "Transmission\nControl ECU" as Trans
participant "Central\nGateway" as GW
participant "vECU\n(IVI vECU)" as vECU
participant "Cluster ECU" as Cluster
participant "Lighting\nControl ECU" as Light

== 기어 변경 (D → R) ==

Driver -> Trans : 기어 R 선택
activate Trans
Trans -> GW : frmTrans_GearStatus\n(0x400)\nGearStatus=1 (R)
activate GW
GW -> vECU : frmTrans_GearStatus\n(라우팅)
deactivate GW
activate vECU

== vECU 후진 감지 및 제어 ==

vECU -> vECU : 기어 D→R 변경 감지\n후진 안전경고 활성화
vECU -> Cluster : frmWarning_UI\n(0x700)\nWarningType=1 (후진 경고)
activate Cluster
Cluster -> Driver : 클러스터에\n경고 UI 표시
deactivate Cluster

vECU -> Light : frmLighting_SeatCtrl\n(0x201)\nSeatLightOn=1 (ON)
activate Light
Light -> Driver : 시트조명 점등
deactivate Light

note right of vECU
  응답시간 < 300ms
  시트조명 최소 3초 유지
end note

deactivate vECU
deactivate Trans

@enduml
```

### 수작업으로 그릴 때 포인트

1. **시퀀스 다이어그램 형식**
   - 상단: 참여자(ECU)
   - 세로선: 시간 흐름
   - 화살표: 메시지 전송

2. **메시지 표현**
   ```
   송신자 → 수신자 : 메시지명 (ID)
                      신호명=값
   ```

3. **시나리오별 작성**
   - 시나리오 1: 후진 안전경고
   - 시나리오 2: 속도 기반 조명 변경
   - 시나리오 3: ADAS 연계 경고
   - 등등...

---

## 🎨 컴포넌트 구성도 (서비스 목록 및 구성 요소)

### PlantUML 컴포넌트 다이어그램

```plantuml
@startuml Component_Structure
!theme plain

title 컴포넌트 구성도\n(서비스 목록 및 구성 요소)

package "vECU (IVI vECU) 내부 구조" {

  component "조명 제어 서비스" as LightSvc {
    portin "속도 정보" as SpeedIn
    portin "온도 정보" as TempIn
    portin "IVI 명령" as IVIIn
    portout "조명 제어 명령" as LightOut
  }

  component "ADAS 연계 경고 서비스" as ADASSvc {
    portin "LDW 이벤트" as LDWIn
    portin "AEB 이벤트" as AEBIn
    portin "후방 장애물" as ObstacleIn
    portout "경고 UI 명령" as WarnOut
    portout "경고 조명 명령" as WarnLightOut
  }

  component "진단/OTA 서비스" as DiagSvc {
    portin "UDS 요청" as UDSIn
    portout "UDS 응답" as UDSOut
    portout "DTC 정보" as DTCOut
    portout "OTA 진행률" as OTAOut
  }

  component "Fail-Safe 관리 서비스" as FailSafeSvc {
    portin "오류 감지" as FaultIn
    portout "Fail-Safe 상태" as FailSafeOut
    portout "기본 조명 명령" as DefaultLightOut
  }

  database "프로필 저장소" as ProfileDB
  database "조명 테마 저장소" as ThemeDB
  database "DTC 저장소" as DTCDB

  LightSvc --> ThemeDB : 읽기/쓰기
  LightSvc --> ProfileDB : 읽기/쓰기
  DiagSvc --> DTCDB : 읽기/쓰기

  note right of LightSvc
    - 속도 기반 조명 제어
    - 온도 기반 조명 제어
    - 프로필 관리
    - 조명 테마 적용
  end note

  note right of ADASSvc
    - LDW 경고 UI
    - AEB 경고 UI
    - 후방 장애물 경고
    - 우선순위 관리
  end note

  note right of DiagSvc
    - UDS 서비스 처리
    - DTC 생성/삭제
    - OTA 다운로드
    - 자동 롤백
  end note
}

@enduml
```

### 수작업으로 그릴 때 포인트

1. **서비스별 그룹화**
   - 큰 박스 안에 관련 서비스 배치
   - 조명 제어, ADAS 연계, 진단/OTA, Fail-Safe 등

2. **입출력 표시**
   - 왼쪽: 입력 포트
   - 오른쪽: 출력 포트

3. **데이터 저장소**
   - 원통형(DB 모양)으로 표현
   - 프로필, 조명 테마, DTC 저장소

---

## 📋 네트워크 구성 요약표

### 표 형식 (Excel/PPT 표)

| CAN 버스 | 속도 | 연결된 ECU | 주요 메시지 |
|---------|------|-----------|----------|
| **Infotainment CAN** | 500 kbps | IVI Control ECU<br>vECU (IVI vECU)<br>Cluster ECU | frmIVI_ModeSelect (0x100)<br>frmIVI_LightColorSet (0x101)<br>frmWarning_UI (0x700) |
| **Body CAN** | 500 kbps | Lighting Control ECU<br>BDC<br>Door Sensors | frmLighting_AmbientCtrl (0x200)<br>frmBDC_DoorStatus (0x210) |
| **ADAS CAN** | 500 kbps | ADAS Control ECU<br>LDW Sensor<br>AEB Sensor | frmADAS_LDW_Event (0x300)<br>frmADAS_AEB_Event (0x302) |
| **Powertrain CAN** | 500 kbps | Transmission Control ECU<br>Vehicle Speed Sensor | frmTrans_GearStatus (0x400)<br>frmVehicle_Speed (0x401) |
| **Chassis CAN** | 500 kbps | HVAC Control ECU<br>Wiper Control ECU | frmHVAC_Temp (0x500)<br>frmWiper_Status (0x501) |

---

## 🎯 PPT/Visio 작성 가이드

### 슬라이드 구성 (총 5장 권장)

1. **슬라이드 1: 표지**
   - 제목: "IVI vECU 프로젝트 컨셉 디자인"
   - 작성자, 작성일

2. **슬라이드 2: Level 1 - 차량 전체 시스템 아키텍처**
   - CAN 버스 구조 (계층적)
   - Central Gateway 중심
   - 도메인별 색상 구분

3. **슬라이드 3: Level 2 - 도메인별 구성**
   - 도메인 간 데이터 교환
   - vECU 중심 구조
   - 통신 방법 제외

4. **슬라이드 4: Level 3 - 통신 구조**
   - 시퀀스 다이어그램 (2~3개 시나리오)
   - 메시지 흐름 표현

5. **슬라이드 5: 컴포넌트 구성도**
   - vECU 내부 서비스 구조
   - 서비스 목록 및 구성 요소
   - 네트워크 구성 요약표

---

## 💡 Visio/PPT 팁

### Visio 사용 시

1. **도형 라이브러리**:
   - 기본 도형 → 사각형 (ECU)
   - 기본 도형 → 원통 (데이터베이스)
   - 커넥터 → 화살표 (데이터 흐름)

2. **스타일**:
   - 테마: "Office 테마" 또는 "모던"
   - 색상: 파스텔 톤 사용
   - 폰트: Malgun Gothic 또는 나눔고딕

3. **레이아웃**:
   - 자동 정렬 기능 활용
   - 균일한 간격 유지

### PowerPoint 사용 시

1. **도형 삽입**:
   - 삽입 → 도형 → 사각형 (ECU)
   - 삽입 → 도형 → 화살표 (데이터 흐름)

2. **SmartArt 활용**:
   - 계층 구조 → "조직도" 또는 "계층 구조"
   - 관계 → "기본 순환형"

3. **애니메이션** (선택):
   - 메시지 흐름을 순차적으로 보여주기
   - "나타내기" 효과 사용

---

## 🖼️ PlantUML 렌더링 방법

### 온라인에서 바로 보기

1. **PlantUML Online Server**
   - https://www.plantuml.com/plantuml/uml/
   - 위 코드 복사 → 붙여넣기 → 이미지 생성

2. **PlantText**
   - https://www.planttext.com/
   - 실시간 미리보기

3. **VS Code Extension**
   - PlantUML Extension 설치
   - `.puml` 파일 생성 → Alt+D로 미리보기

### 이미지 저장 방법

1. PlantUML 렌더링 후 우클릭 → "이미지 저장"
2. PNG 형식으로 저장
3. PPT/Visio에서 "삽입 → 그림"으로 배경 참고용으로 사용
4. 그 위에 수작업으로 다시 그리기

---

## 📌 멘토 피드백 체크리스트

그리기 전에 확인:

- [ ] CAN 버스 구조를 **한 줄로** 표현했는가? (이더넷 방식 ❌)
- [ ] 계층 구조가 명확한가? (Central Gateway가 중심)
- [ ] 도메인별 **데이터 교환**만 표현했는가? (통신 방법 제외)
- [ ] 메시지 흐름을 **시퀀스 다이어그램**으로 표현했는가?
- [ ] 화살표의 **의미**가 명확한가? (무엇을 전달하는지)
- [ ] **색상 구분**이 되어있는가? (도메인별)
- [ ] **주석/설명**이 충분한가? (Central Gateway 역할, vECU 역할 등)

---

**작성 완료 후**: QA 룸에 업로드 (일요일까지)
