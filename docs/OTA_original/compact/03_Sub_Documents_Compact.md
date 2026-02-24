# 시스템 동작 분석 / 네트워크 흐름 / 변수 사양서 (Compact Version)

> 이 문서는 `Project_Result_Sample.xlsx` 형식(0301 ~ 0304)에 맞추어 현업 실무진 및 아키텍처 전문가 보고용으로 극히 간략화된 버전입니다. 개별 문서를 하나로 통합 요약했습니다.

## 0301. 시스템 기능 분석 (SysFuncAnalysis)
| 대분류 | 중분류 | 기능 요약 |
|--------|--------|-----------|
| **모니터링** | 동역학 분석 | 속도/가속/브레이크/조향 입력 상시 추적 및 Level 1~3 위험도 스코어링 |
| **구간 인식** | 환경 매핑 | 일반도로/스쿨존/고속도로/IC출구 진입에 따른 시각적 앰비언트 동기화 |
| **HMI 제어** | 경고 피드백 | 앰비언트(파동/점멸), 클러스터 뷰, 경고음 발생 통합 제어 |
| **FoD OTA** | UDS 세션 | P기어 상태 시 Drive Coach / 시즌 테마 등의 컨텐츠 패키지 원격 다운로드 |
| **텔레매틱스**| 외부 연동 | 충돌(Level 3) 감지 시 Python-Flask 서버 연동하여 실시간 모의 사고 접수 |

## 0302. 네트워크 흐름 정의 (NWflowDef)
| 송신 노드 | 수신 노드 | 신호/메시지명 | 전송 조건 (Trigger) |
|-----------|-----------|---------------|----------------------|
| Vehicle_ECU | WDM_ECU | `gVehicleSpeed`, `gAccelValue` | 100ms Base 주기 전송 |
| WDM_ECU | Ambient/Sound | `WDM_Warning` (Level 1~3) | 위험 감지 / 해제 시 Event 전송 |
| OTA_Server | IVI_ECU / CGW | `UDS Request (0x10, 0x27, 0x34)` | 사용자의 패키지(테마 등) 다운로드 동의 시 |
| Python (로컬)| Flask (서버) | `HTTP POST /claim` | `gCrashEvent = 1` CAN 데이터 수신 시 |

## 0303. 통신 스펙 (Communication Specification)
| Node | Message | ID | Length | Cycle | DLC | Type |
|--------|---------|------|--------|-------|-----|------|
| Vehicle | `Vehicle_Data` | 0x100 | 8 | 100ms | 8 | CAN |
| WDM | `WDM_Warning` | 0x200 | 8 | Event | 8 | CAN |
| OTA | `UDS_Diag` | 0x7E0 | 8 | Event | 8 | CAN (DoIP 적용) |

## 0304. 시스템 변수 명세서 (System Variables)
| Namespace | Variable | Type | Description |
|-----------|----------|------|-------------|
| `VehicleBase` | `gVehicleSpeed` | Integer | 차량 현재 속도 (0~200 km/h) |
| `Warning` | `gWarningLevel` | Integer | 현재 시스템 위험 통합 단계 (0:안전 ~ 3:사고) |
| `Environment` | `gRoadZone` | Integer | 구간 인식 매핑 (0:일반, 1:스쿨존, 2:고속, 3:IC) |
| `OTA` | `o_OTA_Progress` | Float | 현재 실행중인 UDS 다운로드 퍼센테이지 |
| `CrashEvent` | `gCrashEvent` | Integer | 사고 감지 플래그 (1:사고 이벤트 발생) |
