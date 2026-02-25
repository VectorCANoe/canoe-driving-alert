# emergency_system.dbc — 상세 주석 해설

> 실제 사용 파일: `emergency_system.dbc` (주석 없는 순수 DBC)
> 이 파일: 동일 내용을 한국어로 전부 설명한 참조용 문서

---

## DBC 파일 구조 개요

DBC(Database CAN) 파일은 Vector CANoe/CANdb++ 에서 사용하는 CAN 통신 정의 파일이다.
크게 다음 섹션으로 구성된다:

```
VERSION     → 버전 문자열
NS_         → 네임스페이스 (표준 키워드 목록, 항상 동일)
BS_         → 비트타이밍 설정 (보통 비어있음)
BU_         → 네트워크 노드(ECU) 목록
BO_         → CAN 메시지 정의
SG_         → 시그널 정의 (BO_ 안에 포함)
CM_         → 주석(Comment)
BA_DEF_     → 속성 정의 (Attribute Definition)
BA_DEF_DEF_ → 속성 기본값
BA_         → 속성 값 할당
VAL_        → 시그널 값 테이블 (열거형)
```

---

## 1. 헤더 섹션

```
VERSION ""
```
> DBC 파일 버전 문자열. 빈 문자열("")이 표준. 일부 툴에서 버전 식별에 사용.

```
NS_ :
    NS_DESC_  CM_  BA_DEF_  BA_  VAL_  ...
```
> **네임스페이스 섹션**. DBC 표준에 정의된 키워드들을 나열하는 고정 블록.
> 내용 자체를 수정할 일은 없으며, CANdb++가 자동 생성한다.

```
BS_:
```
> **비트타이밍(Bit Timing)** 섹션. 버스 속도를 여기서 정의할 수 있으나,
> 현재 프로젝트는 CANoe Simulation Setup에서 500kbps로 직접 설정하므로 비어 있다.

---

## 2. 노드(BU_) 정의

```
BU_: Context_Manager Police_Node Ambulance_Node Civ_Node Ambient_ECU Cluster_ECU
```

> **BU_ (Bus Unit)** = 이 CAN 버스에 연결된 ECU/노드 목록.
> 여기 선언된 이름들이 이후 BO_/SG_ 에서 송수신 주체로 사용된다.

| 노드명 | 역할 |
|--------|------|
| `Context_Manager` | 주행 구간 인식 ECU. RoadZone + 차속 + 경고레벨을 10ms 주기로 브로드캐스트 |
| `Police_Node` | 경찰차 ECU. 실제로는 sysvar(V2V::Police_*)로 Ethernet 브로드캐스트를 시뮬레이션 |
| `Ambulance_Node` | 구급차 ECU. 동일하게 sysvar(V2V::Ambulance_*)로 시뮬레이션 |
| `Civ_Node` | 일반 수신차 ECU. 중재(Arbiter) 핵심 노드. 우선순위 판정 후 Ambient/Cluster에 명령 송신 |
| `Ambient_ECU` | 앰비언트 라이트 패턴 실행 ECU. Civ_Node 명령을 받아 RGB 타이머 구동 |
| `Cluster_ECU` | 계기판 경고 표시 ECU. Civ_Node 명령을 받아 텍스트 팝업 출력 |

---

## 3. 메시지(BO_) 및 시그널(SG_) 정의

### BO_ 문법

```
BO_ <메시지ID(10진수)> <메시지명>: <DLC(바이트수)> <송신노드>
 SG_ <시그널명> : <시작비트>|<길이>@<바이트순서><부호> (<Factor>,<Offset>) [<Min>|<Max>] "<단위>" <수신노드목록>
```

**바이트 순서 기호:**
- `@1` = Intel 바이트 오더 (Little-Endian) — 낮은 비트가 낮은 주소
- `@0` = Motorola 바이트 오더 (Big-Endian)

**부호 기호:**
- `+` = Unsigned (부호 없음)
- `-` = Signed (부호 있음, 2의 보수)

**실제값 변환 공식:**
```
실제값 = (raw값 × Factor) + Offset
raw값  = (실제값 - Offset) / Factor
```

---

### 3-1. Vehicle_Context (0x100 = 256)

```
BO_ 256 Vehicle_Context: 8 Context_Manager
```
> - **ID**: 0x100 (256)
> - **DLC**: 8바이트
> - **송신**: Context_Manager
> - **주기**: 10ms (BA_ GenMsgCycleTime으로 정의)
> - **목적**: 현재 주행 구간 상태와 차량 거동 정보를 전체 노드에 브로드캐스트

#### 시그널 상세

```
SG_ Vehicle_Speed : 0|16@1+ (0.1,0) [0|300] "km/h" Civ_Node,Ambient_ECU,Cluster_ECU
```
> - **위치**: 비트 0번부터 16비트 (바이트 0~1 전체)
> - **Factor=0.1, Offset=0** → raw값 600 = 실제 60.0 km/h
> - **범위**: 0~300 km/h
> - **수신**: Civ_Node, Ambient_ECU, Cluster_ECU
> - 스쿨존 진입 시 30km/h 초과 여부 판단에 사용

```
SG_ RoadZone : 16|4@1+ (1,0) [0|3] "" Civ_Node,Ambient_ECU,Cluster_ECU
```
> - **위치**: 비트 16번부터 4비트 (바이트 2 하위 4비트)
> - **값 범위**: 0~3
> - 0=일반도로(80km/h), 1=스쿨존(30km/h), 2=고속도로(110km/h), 3=IC/휴게소 근접
> - VAL_ 테이블로 CANoe Symbol Explorer에서 텍스트로 표시됨

```
SG_ WarningLevel : 20|4@1+ (1,0) [0|3] "" Civ_Node,Ambient_ECU
```
> - **위치**: 비트 20번부터 4비트 (바이트 2 상위 4비트)
> - 0=경고없음, 1=경고(과속/핸들미입력), 2=위험
> - Civ_Node가 이 값을 읽어 앰비언트 우선순위 중재에 사용

```
SG_ SteeringActive : 24|1@1+ (1,0) [0|1] "" Civ_Node
```
> - **위치**: 비트 24 (바이트 3의 비트 0)
> - 0=핸들 입력 없음(손 뗌), 1=핸들 조작 감지
> - 고속도로(RoadZone=2)에서 0이 10초 지속되면 경고 발령

```
SG_ NavDirection : 25|1@1+ (1,0) [0|1] "" Civ_Node,Ambient_ECU
```
> - **위치**: 비트 25 (바이트 3의 비트 1)
> - 0=좌측 출구, 1=우측 출구
> - RoadZone=3(IC 근접)일 때만 유효. 앰비언트 방향 애니메이션 결정

```
SG_ Reserved : 26|30@1+ (1,0) [0|0] "" Vector__XXX
```
> - **위치**: 비트 26~55 (30비트)
> - 미사용 예약 영역. 수신노드 `Vector__XXX`는 CANoe 내부 더미 노드
> - 향후 기능 추가 시 활용 가능

```
SG_ AliveCounter : 56|4@1+ (1,0) [0|15] "" Civ_Node
```
> - **위치**: 비트 56~59 (바이트 7 하위 4비트)
> - 0~15 순환 카운터. 매 프레임 +1
> - Civ_Node가 이 값이 증가하지 않으면 Context_Manager 통신 단절로 판단

```
SG_ Checksum : 60|4@1+ (1,0) [0|15] "" Civ_Node
```
> - **위치**: 비트 60~63 (바이트 7 상위 4비트)
> - XOR 또는 합산 체크섬. 데이터 무결성 검증용
> - 현재 CAPL에서 간이 구현 (바이트 0~6 XOR 하위 4비트)

**바이트 레이아웃 요약 (Vehicle_Context 8바이트):**

```
Byte 0: Vehicle_Speed [7:0]
Byte 1: Vehicle_Speed [15:8]
Byte 2: RoadZone[3:0] | WarningLevel[7:4]
Byte 3: SteeringActive[0] | NavDirection[1] | Reserved[7:2]
Byte 4: Reserved
Byte 5: Reserved
Byte 6: Reserved
Byte 7: AliveCounter[3:0] | Checksum[7:4]
```

---

### 3-2. Ambient_Control (0x220 = 544)

```
BO_ 544 Ambient_Control: 4 Civ_Node
```
> - **ID**: 0x220 (544)
> - **DLC**: 4바이트
> - **송신**: Civ_Node (Alert Arbiter 결과)
> - **주기**: 이벤트 기반 (우선순위 변경 시만 송신)
> - **목적**: 앰비언트 ECU에게 표시할 패턴과 모드를 명령

```
SG_ AmbientPattern : 0|4@1+ (1,0) [0|8] "" Ambient_ECU
```
> - 어떤 패턴을 표시할지 ID로 지정
> - 0=대기, 1=정상, 2=스쿨존앰비언트, 3=스쿨존경고, 4=고속도로경고,
>   5=IC좌측유도, 6=IC우측유도, 7=경찰패턴, 8=구급차패턴

```
SG_ AmbientActive : 4|1@1+ (1,0) [0|1] "" Ambient_ECU
```
> - 0=앰비언트 꺼짐, 1=앰비언트 켜짐
> - 경고 해제 시 0으로 설정해 앰비언트를 즉시 소등

```
SG_ AnimStep : 8|4@1+ (1,0) [0|7] "" Ambient_ECU
```
> - IC 방향 유도 애니메이션의 현재 단계 (0~7)
> - Civ_Node가 타이머로 0→7 순환. Ambient_ECU는 이 값을 보고 LED 이동 위치 결정

```
SG_ ArbiterMode : 12|4@1+ (1,0) [0|3] "" Ambient_ECU
```
> - 현재 활성 중재 레이어를 Ambient_ECU에 알림
> - 0=기본, 1=구간경고, 2=경찰, 3=구급차
> - Ambient_ECU는 이 값으로 색상 팔레트 선택

```
SG_ AliveCounter : 28|4@1+ (1,0) [0|15] "" Ambient_ECU
```
> - Civ_Node→Ambient_ECU 통신 활성 확인용 순환 카운터

---

### 3-3. Cluster_Warning (0x221 = 545)

```
BO_ 545 Cluster_Warning: 4 Civ_Node
```
> - **ID**: 0x221 (545)
> - **DLC**: 4바이트
> - **송신**: Civ_Node
> - **주기**: 이벤트 기반
> - **목적**: 계기판에 경고 팝업 텍스트와 긴급차량 정보 표시

```
SG_ WarningType : 0|4@1+ (1,0) [0|8] "" Cluster_ECU
```
> - 표시할 경고 종류
> - 0=없음, 1=스쿨존, 2=고속도로, 3=IC안내, 4=경찰차접근, 5=구급차접근

```
SG_ WarningActive : 4|1@1+ (1,0) [0|1] "" Cluster_ECU
```
> - 0=경고 팝업 숨김, 1=경고 팝업 표시

```
SG_ EmergencyVehicle : 8|2@1+ (1,0) [0|2] "" Cluster_ECU
```
> - 긴급차량 종류. 0=없음, 1=경찰차, 2=구급차
> - Cluster_ECU는 이 값에 따라 "경찰차 접근" 또는 "구급차 접근" 팝업 선택

```
SG_ Direction : 10|2@1+ (1,0) [0|3] "" Cluster_ECU
```
> - 긴급차량 접근 방향 (0=전방, 1=좌, 2=우, 3=후방)
> - 현재 시뮬레이션에서는 고정값 사용. 확장 시 Radar/Camera 연동 가능

```
SG_ AliveCounter : 28|4@1+ (1,0) [0|15] "" Cluster_ECU
```
> - Civ_Node→Cluster_ECU 통신 활성 확인용

---

## 4. 주석(CM_) 섹션

```
CM_ BU_ <노드명> "<설명>";
CM_ BO_ <메시지ID> "<설명>";
CM_ SG_ <메시지ID> <시그널명> "<설명>";
```
> CANoe Symbol Explorer, Trace 창, Graphics 창 등에서 툴팁으로 표시된다.
> 실제 통신에는 영향 없음. 디버깅·문서화 목적.

---

## 5. 속성(BA_DEF_ / BA_) 섹션

```
BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;
BA_DEF_DEF_ "GenMsgCycleTime" 0;
```
> - `GenMsgCycleTime`: Vector 표준 속성. 메시지 송신 주기(ms)를 정의
> - 기본값 0 = 이벤트 기반(비주기)
> - CANoe CAPL Generator, Network Statistics 창에서 이 값을 참조

```
BA_ "GenMsgCycleTime" BO_ 256  10;   ← Vehicle_Context: 10ms 주기
BA_ "GenMsgCycleTime" BO_ 544  0;    ← Ambient_Control: 이벤트
BA_ "GenMsgCycleTime" BO_ 545  0;    ← Cluster_Warning: 이벤트
```

---

## 6. 값 테이블(VAL_) 섹션

```
VAL_ <메시지ID> <시그널명> <값> "<텍스트>" ... ;
```
> 시그널의 숫자값에 텍스트 레이블을 붙인다.
> CANoe Trace 창에서 `1` 대신 `"SchoolZone"` 으로 표시되어 디버깅이 쉬워진다.

예시:
```
VAL_ 256 RoadZone
  0 "Normal"
  1 "SchoolZone"
  2 "Highway"
  3 "IC_Guide" ;
```
> RoadZone 시그널이 값 1이면 Trace에 `SchoolZone` 으로 표시

---

## 7. 전체 메시지 ID 요약

| 메시지명 | HEX ID | DEC ID | DLC | 송신 노드 | 주기 |
|---------|--------|--------|-----|---------|------|
| Vehicle_Context | 0x100 | 256 | 8 bytes | Context_Manager | 10ms |
| Ambient_Control | 0x220 | 544 | 4 bytes | Civ_Node | 이벤트 |
| Cluster_Warning | 0x221 | 545 | 4 bytes | Civ_Node | 이벤트 |

---

## 8. 앰비언트 우선순위 중재 테이블 (Civ_Node 로직 참조)

| 우선순위 | 조건 | ArbiterMode | AmbientPattern |
|---------|------|-------------|----------------|
| 1 (최고) | EmergencyVehicle = 2 (구급차) | 3 | 8 (Ambulance) |
| 2 | EmergencyVehicle = 1 (경찰차) | 2 | 7 (Police) |
| 3 | WarningLevel > 0 | 1 | 3 or 4 (경고) |
| 4 (최저) | RoadZone 기본값 | 0 | 1~6 (구간 패턴) |

> 높은 우선순위 조건 해제 시 → 즉시 다음 우선순위로 강등
> 구급차 해제 → 경찰차 있으면 2번, 없으면 경고/구간으로 복귀

---

## 9. DBC 주의사항

1. **블록 주석 불가**: `/* */` 형식은 DBC 파서가 지원하지 않음 → 이 MD 파일로 대체
2. **화살표 문자 불가**: `→` 같은 유니코드 문자는 일부 파서에서 에러 → `->` 사용
3. **BU_ 노드명 일치**: SG_ 수신노드 목록과 BU_ 선언이 반드시 일치해야 함
4. **비트 겹침 금지**: 같은 메시지 내 시그널들의 비트 영역이 겹치면 파싱 에러
