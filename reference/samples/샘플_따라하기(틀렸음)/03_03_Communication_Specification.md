# 0303_Communication Specification (통신 명세)

## IVI vECU 프로젝트 통신 명세

> **작성 기준**: 멘토 샘플 형식 준수 (DBC 파일의 "사람이 읽을 수 있는" 버전)
> **작성일**: 2026-02-13

---

## 주요 메시지 상세 명세

### 📋 frmIVI_ModeSelect (0x100)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x100 |
| **DLC** | 2 bytes |
| **Cycle Time** | 100 ms |
| **Sender** | IVI Control ECU |
| **Receivers** | vECU (IVI vECU) |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **ModeSelected** | 0~1 | 2 bits | 0: 에코<br>1: 컴포트<br>2: 스포츠<br>3: Reserved | IVI 화면에서 선택한 주행 모드 | vECU는 이 값을 기반으로 조명 테마 패키지 적용 (Req_038) |
| **ProfileSelected** | 2~3 | 2 bits | 1: 프로필1<br>2: 프로필2<br>3: 프로필3 | 운전자 프로필 선택 | vECU는 이 값을 기반으로 저장된 조명 선호 설정 로드 (Req_039) |

---

### 📋 frmIVI_LightColorSet (0x101)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x101 |
| **DLC** | 4 bytes |
| **Cycle Time** | 200 ms |
| **Sender** | IVI Control ECU |
| **Receivers** | vECU (IVI vECU) |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **ColorR** | 0~7 | 8 bits | 0~255 | 조명 색상 Red 값 | IVI 화면에서 사용자가 선택한 RGB 색상 중 R 값 |
| **ColorG** | 8~15 | 8 bits | 0~255 | 조명 색상 Green 값 | IVI 화면에서 사용자가 선택한 RGB 색상 중 G 값 |
| **ColorB** | 16~23 | 8 bits | 0~255 | 조명 색상 Blue 값 | IVI 화면에서 사용자가 선택한 RGB 색상 중 B 값 |
| **Brightness** | 24~31 | 8 bits | 0~100 | 조명 밝기 (%) | IVI 화면에서 사용자가 선택한 밝기 (Req_004) |

---

### 📋 frmLighting_AmbientCtrl (0x200)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x200 |
| **DLC** | 5 bytes |
| **Cycle Time** | 50 ms (조명 제어는 빠른 응답 필요) |
| **Sender** | vECU (IVI vECU) |
| **Receivers** | Lighting Control ECU |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **AmbientR** | 0~7 | 8 bits | 0~255 | 앰비언트 조명 Red 값 | Lighting Control ECU는 이 값을 기반으로 실제 LED PWM 신호 생성 |
| **AmbientG** | 8~15 | 8 bits | 0~255 | 앰비언트 조명 Green 값 | Lighting Control ECU는 이 값을 기반으로 실제 LED PWM 신호 생성 |
| **AmbientB** | 16~23 | 8 bits | 0~255 | 앰비언트 조명 Blue 값 | Lighting Control ECU는 이 값을 기반으로 실제 LED PWM 신호 생성 |
| **AmbientBrightness** | 24~31 | 8 bits | 0~100 | 앰비언트 조명 밝기 (%) | Lighting Control ECU는 이 값을 기반으로 전체 밝기 조정 |
| **BlinkMode** | 32~33 | 2 bits | 0: 정상<br>1: 느린 점멸 (1Hz)<br>2: 빠른 점멸 (3Hz)<br>3: Reserved | 점멸 모드 | ADAS 경고 시 점멸 패턴 적용 (Req_027, Req_028) |

---

### 📋 frmBDC_DoorStatus (0x210)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x210 |
| **DLC** | 1 byte |
| **Cycle Time** | 100 ms |
| **Sender** | BDC (Body Domain Controller) |
| **Receivers** | vECU (IVI vECU), Gateway |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **DoorStatus** | 0~7 | 8 bits (비트맵) | Bit 0: 운전석 도어<br>Bit 1: 조수석 도어<br>Bit 2: 후석 좌 도어<br>Bit 3: 후석 우 도어<br>(0: 닫힘, 1: 열림) | 각 도어의 개방/폐쇄 상태 | vECU는 도어 개방 시 승하차 UX 활성화 (Req_003), 후진 중 도어 개방 시 경고 (Req_006) |

---

### 📋 frmTrans_GearStatus (0x400)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x400 |
| **DLC** | 1 byte |
| **Cycle Time** | 50 ms |
| **Sender** | Transmission Control ECU |
| **Receivers** | vECU (IVI vECU), Gateway, Cluster ECU |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **GearStatus** | 0~1 | 2 bits | 0: P (Parking)<br>1: R (Reverse)<br>2: N (Neutral)<br>3: D (Drive) | 현재 변속 상태 | vECU는 R 진입 시 후진 UX 활성화 (Req_015), 후진 안전경고 (Req_002) |

---

### 📋 frmVehicle_Speed (0x401)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x401 |
| **DLC** | 1 byte |
| **Cycle Time** | 50 ms |
| **Sender** | Vehicle Speed Sensor |
| **Receivers** | vECU (IVI vECU), Gateway, Cluster ECU |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **VehicleSpeed** | 0~7 | 8 bits | 0~255 km/h | 현재 차량 속도 | vECU는 속도 기반으로 조명 색상 변경 (Req_001), 속도 10km/h 이상 시 후진 UX 해제 (Req_020) |

---

### 📋 frmADAS_LDW_Event (0x300)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x300 |
| **DLC** | 1 byte |
| **Cycle Time** | 50 ms |
| **Sender** | ADAS Control ECU |
| **Receivers** | vECU (IVI vECU), Gateway |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **LDW_Event** | 0 | 1 bit | 0: 정상 주행<br>1: 차선 이탈 감지 | 차선 이탈 경고 이벤트 | vECU는 이벤트 수신 시 대시보드 경고 UI 표시 및 조명 점멸 (Req_027) |
| **LDW_Direction** | 1~2 | 2 bits | 0: 좌측 이탈<br>1: 우측 이탈<br>2: Reserved | 이탈 방향 | 좌우 방향에 따라 조명 점멸 패턴 변경 가능 |

---

### 📋 frmADAS_AEB_Event (0x302)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x302 |
| **DLC** | 1 byte |
| **Cycle Time** | 20 ms (긴급 제동은 매우 빠른 응답 필요) |
| **Sender** | ADAS Control ECU |
| **Receivers** | vECU (IVI vECU), Gateway |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **AEB_Event** | 0 | 1 bit | 0: 정상 주행<br>1: 긴급 제동 발생 | 긴급 제동 이벤트 | vECU는 이벤트 수신 시 대시보드 고위험 경고 UI 즉시 표시 (Req_029), 응답시간 < 50ms |
| **AEB_Level** | 1~2 | 2 bits | 0: 낮음<br>1: 중간<br>2: 높음<br>3: 매우 높음 | 위험 수준 | 위험 수준에 따라 경고 UI 색상 및 밝기 조정 |

---

### 📋 frmWarning_UI (0x700)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x700 |
| **DLC** | 2 bytes |
| **Cycle Time** | Event-based (이벤트 발생 시) |
| **Sender** | vECU (IVI vECU) |
| **Receivers** | Cluster ECU |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **WarningType** | 0~3 | 4 bits | 0: 없음<br>1: 후진 경고<br>2: LDW 경고<br>3: AEB 경고<br>4: 도어 개방 경고<br>5: 휴식 권장<br>6~15: Reserved | 경고 유형 | Cluster ECU는 경고 유형에 따라 적절한 UI 표시 |
| **WarningLevel** | 4~5 | 2 bits | 0: 정보<br>1: 주의<br>2: 경고<br>3: 위험 | 경고 수준 | 수준에 따라 색상 변경 (정보: 파란색, 주의: 노란색, 경고: 주황색, 위험: 빨간색) |
| **DisplayDuration** | 8~15 | 8 bits | 0~255 (×0.1초) | 표시 지속 시간 (0: 영구 표시) | Cluster ECU는 이 시간 동안 경고 UI 유지 |

---

### 📋 frmDiag_Request (0x7DF) - UDS 요청

| 속성 | 값 |
|------|---|
| **Message ID** | 0x7DF (Physical Addressing) |
| **DLC** | 8 bytes |
| **Cycle Time** | Event-based |
| **Sender** | Diagnostic Tester |
| **Receivers** | Diagnostic Service ECU |

#### UDS 서비스 상세

| Service ID | Service Name | Description | Usage |
|-----------|--------------|-------------|-------|
| **0x14** | ClearDiagnosticInformation | 저장된 모든 DTC 삭제 | 정비 후 DTC 초기화 (Req_011) |
| **0x19** | ReadDTCInformation | DTC 정보 조회 | 진단 테스터에서 저장된 DTC 확인 |
| **0x22** | ReadDataByIdentifier | 데이터 식별자로 데이터 읽기 | OTA 버전 정보, 시스템 상태 조회 |
| **0x2E** | WriteDataByIdentifier | 데이터 식별자로 데이터 쓰기 | 조명 테마 파라미터 설정 |
| **0x34** | RequestDownload | OTA 다운로드 요청 | OTA 패키지 수신 시작 (Req_012) |
| **0x36** | TransferData | 데이터 전송 | OTA 패키지 데이터 블록 전송 |
| **0x37** | RequestTransferExit | 전송 종료 요청 | OTA 다운로드 완료 |

---

### 📋 frmOTA_Progress (0x601)

| 속성 | 값 |
|------|---|
| **Message ID** | 0x601 |
| **DLC** | 2 bytes |
| **Cycle Time** | 100 ms (OTA 진행 중) |
| **Sender** | Diagnostic Service ECU |
| **Receivers** | vECU (IVI vECU), Cluster ECU |

#### 신호 상세

| Signal | Bit Position | Length | Data Range | Description | Usage |
|--------|-------------|--------|------------|-------------|-------|
| **OTAProgress** | 0~7 | 8 bits | 0~100 (%) | OTA 진행률 | Cluster ECU는 진행률을 프로그레스바로 표시 |
| **OTAStatus** | 8~9 | 2 bits | 0: 대기<br>1: 진행중<br>2: 성공<br>3: 실패 | OTA 상태 | vECU는 상태에 따라 적절한 UI 표시 및 롤백 처리 (Req_014) |

---

## 통신 특성 요구사항

### 메시지 우선순위

| 우선순위 | Message ID Range | Message Type | 비고 |
|---------|------------------|--------------|------|
| **최우선 (긴급)** | 0x300~0x3FF | ADAS 이벤트 (LDW, AEB, 후방 장애물) | ASIL-D/C 수준, 응답시간 < 50ms |
| **높음 (안전)** | 0x700~0x7FF | 경고 UI/사운드, Fail-Safe | ASIL-B/C 수준, 응답시간 < 100ms |
| **중간 (제어)** | 0x200~0x2FF, 0x400~0x4FF | 조명 제어, 차량 정보 | 응답시간 < 150ms |
| **낮음 (정보)** | 0x100~0x1FF, 0x500~0x5FF | IVI 입력, HVAC, 와이퍼 | 응답시간 < 300ms |
| **진단** | 0x7DF, 0x7E8, 0x600~0x6FF | UDS, DTC, OTA | Event-based |

### 통신 품질 요구사항

| 항목 | 요구사항 | 관련 요구사항 |
|------|----------|--------------|
| **CAN 메시지 전송 성공률** | 99.9% 이상 | Req_054 |
| **CAN 통신 지연** | 10ms 미만 | Req_054 |
| **CAN 메시지 손실률** | 0.1% 이하 | Req_024 |
| **시스템 반응 시간** | 1초 이내 (사용자 입력 → 기능 활성화) | Req_008 |
| **ADAS 연계 경고 응답시간** | 50~120ms (이벤트별 상이) | Req_027, Req_028, Req_029 |

---

## DBC 파일 생성 가이드

본 통신 명세를 기반으로 DBC 파일을 생성할 때 다음 사항을 고려:

1. **메시지 ID 할당**: 위 표의 ID 값 사용
2. **신호 정의**: Bit Position, Length, Data Range 정확히 반영
3. **송신 주기**: Cycle Time 정확히 반영
4. **송수신 노드**: Tx/Rx ECU 정확히 반영
5. **신호 값 정의**: Value Table로 Enum 값 정의 (예: GearStatus 0=P, 1=R, 2=N, 3=D)
6. **물리값 변환**: Factor, Offset 정의 (예: DisplayDuration은 Factor=0.1, Offset=0)

---

**다음 단계**: 0304_System Variables (시스템 변수) 작성
