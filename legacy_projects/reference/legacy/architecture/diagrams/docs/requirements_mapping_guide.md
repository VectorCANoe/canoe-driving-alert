# 요구사항 명세서 활용 가이드

## 📋 요약

**결론**: 기존 요구사항 명세서(REQ_IVI_vECU_Requirements.xlsx)는 **그대로 사용 가능**합니다.

새로운 차량 시스템 아키텍처는 기존 요구사항의 **상위 컨텍스트**를 제공하며, IVI vECU 요구사항은 **Level 4 (ECU 내부 상세 설계)**에서 그대로 적용됩니다.

---

## 🎯 아키텍처 레벨별 요구사항 매핑

### Level 1: 차량 전체 시스템
**목적**: 차량 시스템 이해 및 통신 필요성 파악

**요구사항 적용**: ❌ 직접 적용 안 됨 (상위 컨텍스트 제공)

**설명**:
- Level 1은 차량 전체 ECU 구성을 보여줌
- IVI는 11개 ECU 중 하나로 표현됨
- 다른 ECU(EMS, ESP, Camera 등)와의 **통신 관계** 정의

**예시**:
```
IVI가 속도를 표시하려면?
→ Engine ECU(0x101: Vehicle Speed) 신호 수신 필요
→ Level 1에서 이 통신 경로를 정의
```

---

### Level 2: 도메인별 상세
**목적**: 각 도메인 내 ECU 역할 및 협업 구조

**요구사항 적용**: ⚠️ 간접 적용 (도메인 간 인터페이스)

**설명**:
- Infotainment Domain 내 IVI, Cluster, ADAS ECU 관계
- IVI가 ADAS 경고를 표시하려면 Camera ECU와 통신 필요

**예시**:
```
REQ_IVI_028: 차선 이탈 경고 표시 (<80ms)
→ Camera ECU가 LDW 이벤트 송신 (0x300)
→ IVI가 수신 후 UI 표시
→ Level 2에서 이 도메인 내 협업 정의
```

---

### Level 3: CAN 통신 구조
**목적**: ECU 간 메시지 흐름 및 CAN 데이터베이스

**요구사항 적용**: ✅ 부분 적용 (CAN 신호 정의)

**설명**:
- IVI 송수신 CAN 메시지 정의
- 기존 요구사항의 CAN 신호 ID를 전체 차량 CAN 매트릭스에 통합

**기존 요구사항 활용**:
| 요구사항 | CAN 신호 | Level 3 적용 |
|---------|---------|-------------|
| REQ_IVI_001 | 0x100-0x104 (차량 신호 수신) | ✅ CAN DB에 포함 |
| REQ_IVI_004 | 0x210 (IVI 색상 명령 송신) | ✅ CAN DB에 포함 |
| REQ_IVI_028-031 | 0x300-0x305 (ADAS 이벤트 수신) | ✅ CAN DB에 포함 |

---

### Level 4: IVI ECU 내부 상세
**목적**: IVI vECU 소프트웨어 아키텍처 (AUTOSAR)

**요구사항 적용**: ✅ **전체 적용** (기존 요구사항 그대로 사용)

**설명**:
- 기존 56개 요구사항 **모두 Level 4에서 적용**
- IVI 내부 컴포넌트 설계 (Ambient_Light_Controller, ADAS_Safety_Coordinator 등)
- 기존 다이어그램 재활용 가능

**기존 작업물 활용**:
| 기존 다이어그램 | Level 4 활용 |
|---------------|-------------|
| `adas_integration_architecture.puml` | ✅ IVI 내부 ADAS 통합 |
| `ivi_ui_architecture.puml` | ✅ IVI 내부 UI 구조 |
| `lighting_control_architecture.puml` | ✅ IVI 내부 라이팅 제어 |
| `safety_system_architecture.puml` | ✅ IVI 내부 안전 기능 |

---

## 📊 요구사항 분류별 레벨 매핑

### 기능 요구사항 (28개)

#### 조명 제어 (REQ_IVI_001-005, 017, 042)
- **Level 1**: IVI → BCM 통신 경로 정의
- **Level 3**: CAN 신호 0x210 (Ambient_Light_RGB) 정의
- **Level 4**: `Ambient_Light_Controller` 컴포넌트 상세 설계 ✅

#### ADAS 연계 (REQ_IVI_028-038)
- **Level 1**: Camera ECU → IVI 통신 경로 정의
- **Level 3**: CAN 신호 0x300-0x305 (LDW, AEB, BSD) 정의
- **Level 4**: `ADAS_Safety_Coordinator` 컴포넌트 상세 설계 ✅

#### IVI UI 기능 (REQ_IVI_042-050)
- **Level 1**: IVI ECU 존재 표시
- **Level 3**: IVI 내부 통신 (해당 없음)
- **Level 4**: `Theme_Manager`, `Profile_Manager` 등 UI 컴포넌트 설계 ✅

---

### 안전 요구사항 (11개)

#### 후진 안전 (REQ_IVI_002, 007, 008)
- **Level 1**: TCU (기어 위치) → IVI 통신 정의
- **Level 3**: CAN 신호 0x180 (Gear Position) 정의
- **Level 4**: `Reverse_Safety_Manager` 컴포넌트 설계 ✅

#### ADAS 안전 (REQ_IVI_028-031)
- **Level 1**: Camera/Radar ECU → IVI 통신 정의
- **Level 3**: ADAS CAN 신호 정의
- **Level 4**: ADAS 핸들러 (LDW, AEB, BSD) 설계 ✅

---

### 진단/OTA 요구사항 (9개)

#### UDS 진단 (REQ_IVI_011, 012, 047)
- **Level 1**: Diagnostic Tester → Gateway → IVI 경로 정의
- **Level 3**: 진단 CAN ID 0x7DF (요청), 0x7E8 (응답) 정의
- **Level 4**: `Diagnostic Stack` (DCM, DEM) 설계 ✅

#### OTA 업데이트 (REQ_IVI_013-015)
- **Level 1**: OTA Server → Gateway → IVI 경로 정의
- **Level 3**: Telematics 통신 (4G/5G) 정의
- **Level 4**: `OTA_Update_Agent` 컴포넌트 설계 ✅

---

### 비기능 요구사항 (8개)

#### 성능 (REQ_IVI_039-041)
- **Level 1**: 네트워크 대역폭 정의 (CAN-HS: 500 kbps)
- **Level 3**: 메시지 주기 정의 (10ms, 50ms, 100ms)
- **Level 4**: 타이밍 분석 및 성능 모니터링 ✅

#### 추적성 (REQ_IVI_048)
- **Level 1-4**: 모든 레벨에서 요구사항 ID 명시 ✅

---

## ✅ 기존 요구사항 활용 전략

### 1. 요구사항 명세서는 그대로 유지
- **변경 불필요**: 56개 요구사항 모두 유효
- **추가 컨텍스트**: Level 1-3 아키텍처가 상위 컨텍스트 제공

### 2. 레벨별 요구사항 참조 방식

**Level 1 다이어그램**:
```plantuml
component "IVI Head Unit" as ECU_IVI {
    note bottom
        **Requirements Coverage**:
        • REQ_IVI_001-005: Lighting
        • REQ_IVI_042-050: UI Features
        • REQ_IVI_028-038: ADAS Display
    end note
}
```

**Level 4 다이어그램** (기존 방식 유지):
```plantuml
component "Ambient_Light_Controller" as ALC {
    note right
        **REQ_IVI_001**
        Sport Mode Speed-linked
        • Response: <500ms
        • ASIL-B
    end note
}
```

### 3. 기존 다이어그램 재활용

| 기존 파일 | 새로운 위치 | 변경 사항 |
|---------|-----------|----------|
| `adas_integration_architecture.puml` | Level 4 | ✅ 그대로 사용 |
| `ivi_ui_architecture.puml` | Level 4 | ✅ 그대로 사용 |
| `lighting_control_architecture.puml` | Level 4 | ✅ 그대로 사용 |
| `safety_system_architecture.puml` | Level 4 | ✅ 그대로 사용 |
| `ota_diagnostic_sequence.puml` | Level 4 | ✅ 그대로 사용 |

---

## 🎯 멘토링 대비 답변 준비

### Q: "기존 요구사항은 어떻게 되나요?"

**A**:
> "기존 56개 요구사항은 모두 유효하며, Level 4 (IVI ECU 내부 설계)에서 그대로 적용됩니다.
>
> 새로운 Level 1-3 아키텍처는 **왜 IVI가 다른 ECU와 통신해야 하는지**를 설명하는 상위 컨텍스트입니다.
>
> 예를 들어, REQ_IVI_001 (속도 연동 조명)을 구현하려면:
> - Level 1: Engine ECU → IVI 통신 경로 확인
> - Level 3: CAN 신호 0x101 (Vehicle Speed) 정의
> - Level 4: Ambient_Light_Controller 컴포넌트 설계 (기존 요구사항 적용)"

### Q: "기존 작업물은 버려야 하나요?"

**A**:
> "아닙니다! 기존 작업물은 **Level 4 상세 설계**로 그대로 활용됩니다.
>
> 우리가 추가한 것은:
> - Level 1: 차량 전체 시스템 (11개 ECU)
> - Level 2: 도메인별 상세 (4개 도메인)
> - Level 3: CAN 통신 구조
>
> 기존 ADAS 통합, IVI UI, 조명 제어 다이어그램은 Level 4에서 재활용합니다."

---

## 📝 결론

### ✅ 기존 요구사항 명세서 활용 방안

1. **그대로 유지**: 56개 요구사항 모두 유효
2. **Level 4 적용**: IVI ECU 내부 설계에 전체 적용
3. **Level 1-3 추가**: 차량 시스템 컨텍스트 제공
4. **기존 다이어그램 재활용**: Level 4에서 활용

### 📊 레벨별 요구사항 적용률

| 레벨 | 요구사항 적용 | 설명 |
|------|-------------|------|
| Level 1 | 간접 (컨텍스트) | 차량 전체 시스템, 통신 필요성 |
| Level 2 | 부분 (도메인 인터페이스) | 도메인 간 협업 구조 |
| Level 3 | 부분 (CAN 신호) | 메시지 흐름 및 신호 정의 |
| Level 4 | **100% 전체 적용** | IVI ECU 내부 상세 설계 |

### 🎯 핵심 메시지

> **기존 요구사항은 버리지 않습니다!**
>
> 새로운 아키텍처는 "IVI가 왜 존재하는가?"와 "왜 통신이 필요한가?"를 설명하는 **상위 컨텍스트**입니다.
>
> IVI 내부 설계는 기존 요구사항을 **그대로 사용**합니다.

---

**작성일**: 2026-02-11
**참고**: Level 1 차량 시스템 아키텍처 (`01_vehicle_system_architecture.puml`)
