> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# Naming & Abbreviation Reference (Project Internal)

## 1) 문서 목적
- 본 문서는 `01~07` 공식 산출물에 넣지 않는 **참조용 명명표**이다.
- 목적: 약어/노드명을 빠르게 해석하고, 리뷰 시 용어 혼선을 줄이는 것.
- 적용 범위: `driving-situation-alert` 프로젝트 전용 + 업계 표준 용어 참고.

## 2) 프로젝트 핵심 약어/노드 명명표
| 이름 | 약어/풀네임 | 의미(프로젝트 기준) | 비고 |
|---|---|---|---|
| `WARN_ARB_MGR` | Warning Arbitration Manager | 다중 경고 동시 발생 시 우선순위 중재 관리자 | `ARB = Arbiter(중재자)` |
| `ADAS_WARN_CTRL` | ADAS Warning Controller | 주행 문맥/위험 조건을 경고 레벨로 판정 | 경고 기준 판단 노드 |
| `NAV_CONTEXT_MGR` | Navigation Context Manager | 구간/제한속도/유도 문맥을 생성/관리 | 내비 문맥 제공 |
| `EMS_POLICE_TX` | Emergency Message Service Police Transmitter | 경찰 긴급 이벤트 송신 노드 | `TX = 송신` |
| `EMS_AMB_TX` | Emergency Message Service Ambulance Transmitter | 구급 긴급 이벤트 송신 노드 | `AMB = Ambulance` |
| `EMS_ALERT_RX` | Emergency Alert Receiver | 긴급 이벤트 수신/정규화/해제 처리 | `RX = 수신` |
| `BCM_AMBIENT_CTRL` | Body Control Module Ambient Controller | 엠비언트(패턴/점등) 제어 | `BCM` 계열 출력 |
| `CLU_HMI_CTRL` | Cluster HMI Controller | 클러스터 경고 UI/HMI 출력 제어 | `CLU = Cluster` |
| `SIL_TEST_CTRL` | SIL Test Controller | CANoe SIL 환경 테스트 자극/검증 제어 | 테스트 전용 |
| `BODY_GW` | Body Gateway | Body 도메인 게이트웨이 | `GW = Gateway` |
| `CHASSIS_GW` | Chassis Gateway | Chassis 도메인 게이트웨이 |  |
| `INFOTAINMENT_GW` | Infotainment Gateway | Infotainment 도메인 게이트웨이 |  |
| `ETH_SWITCH` | Ethernet Switch | 도메인 간 Ethernet 스위칭 | 백본 스위치 |
| `ETH_CORE` | Ethernet Core | Ethernet 코어 구간/백본 | 내부 설계 식별자 |

### 2-1) CANoe CAPL 노드명 ↔ 문서 노드명 매핑
| CANoe 노드 파일명 | 문서/아키텍처 명칭 | 역할 |
|---|---|---|
| `Police_Node.can` | `EMS_POLICE_TX` | 경찰 긴급 이벤트 송신 |
| `Ambulance_Node.can` | `EMS_AMB_TX` | 구급 긴급 이벤트 송신 |
| `Civ_Node.can` | `WARN_ARB_MGR` | 다중 경고 중재 및 출력 분기 |
| `Context_Manager.can` | `NAV_CONTEXT_MGR` | 주행 문맥 생성/갱신 |
| `Ambient_ECU.can` | `BCM_AMBIENT_CTRL` | 앰비언트 출력 제어 |
| `Cluster_ECU.can` | `CLU_HMI_CTRL` | 클러스터 경고/HMI 표시 |
| `Test_Node.can` | `SIL_TEST_CTRL` | SIL 테스트 제어/검증 |

### 2-2) 주요 메시지/신호 네이밍
| 이름 | 의미 | 분류 |
|---|---|---|
| `Vehicle_Context` | 주행 문맥(구간/속도/경고 레벨) 전달 | CAN 메시지 |
| `Ambient_Control` | 앰비언트 패턴/활성 상태 출력 | CAN 메시지 |
| `Cluster_Warning` | 계기판 경고 정보 출력 | CAN 메시지 |
| `ETH_EmergencyAlert` | 긴급차량 이벤트(종류/상태/방향/ETA) 전달 | Ethernet(UDP) 메시지 |
| `ethSelectedAlertMsg` | 중재 완료된 단일 경고 컨텍스트 전달 | Ethernet(UDP) 메시지 |

## 3) 중재(Arbitration) 용어 해석
- `ARB = Arbiter (중재자)`
- `WARN_ARB_MGR = Warning Arbitration Manager`
- 현재 `canoe/nodes/Civ_Node.can` 기준 우선순위:
1. `Ambulance`
2. `Police`
3. `Zone Warning`
4. `Base Zone Ambient`

## 4) 접미어/접두어 네이밍 규칙 (프로젝트 공통)
| 토큰 | 의미 | 사용 규칙 |
|---|---|---|
| `CTRL` | Controller | 제어 책임이 있는 노드/모듈에 사용 |
| `MGR` | Manager | 상태/정책/오케스트레이션 관리 주체에 사용 |
| `ARB` | Arbiter | 충돌/우선순위 결정 로직 포함 시 사용 |
| `TX` | Transmit | 송신 전담 역할 |
| `RX` | Receive | 수신/수집/정규화 전담 역할 |
| `GW` | Gateway | 도메인 간 메시지 중계/변환 역할 |
| `HMI` | Human Machine Interface | 사용자 시각/조작 인터페이스 처리 |

## 5) 현대기아/모빌리티 실무 용어 (참고)
- 주의: 아래는 업계 일반 관용어이며, 최종 명명은 사내 표준 우선.

| 용어 | 일반 의미 | 프로젝트 적용 메모 |
|---|---|---|
| `HMG` | Hyundai Motor Group | 대외 표현/보고서에서 그룹 지칭 |
| `IVI` | In-Vehicle Infotainment | `Infotainment` 도메인과 매핑 |
| `Cluster` | 계기판 ECU/UI 영역 | `CLU_HMI_CTRL`와 연관 |
| `BCM` | Body Control Module | 바디 액추에이터/램프 제어 |
| `Gateway/CGW` | 도메인 간 라우팅 ECU | `*_GW` 네이밍과 동일 철학 |
| `ADAS` | 운전자 보조 시스템 영역 | 경고 판단/중재 상위 문맥 |
| `Domain Controller(DCU)` | 도메인 단위 통합 제어기 | 현재 SIL에서는 CAPL 노드로 모델링 |

### 5-1) 프로젝트 ECU ↔ OEM 스타일 매핑 (권장 운영안)

- 원칙(BP): `03/0301`의 프로젝트 표준 노드명은 유지하고, OEM 스타일은 매핑표로 관리한다.
- 이유: 추적성 ID 체인(Req/Func/Flow/Comm/Var/Test) 안정성을 유지하면서, 대외 설명 시 OEM 용어 호환이 가능하다.

| 프로젝트 노드명 | OEM 스타일 기능군/용어 | 비고 |
|---|---|---|
| ADAS_WARN_CTRL | ADAS Domain Logic | FCA/LDW/LKA/SCC와 같은 기능군의 상위 경고 판단 레이어 |
| NAV_CONTEXT_MGR | IVI/Navi Context | IVI 또는 Navigation ECU 문맥 처리 레이어 |
| WARN_ARB_MGR | ADAS/VCU Arbitration | 다중 ADAS/경고 이벤트 우선순위 중재 |
| CLU_HMI_CTRL | Cluster HMI ECU | OEM의 Cluster ECU/HU 경고 표시 경로와 대응 |
| BCM_AMBIENT_CTRL | BCM (Body Control Module) | 바디 램프/앰비언트 출력 제어 |
| EMS_ALERT_RX | EMS/V2X Alert Handler | 긴급차량 메시지 수신·해제·타임아웃 처리 |
| EMS_POLICE_TX, EMS_AMB_TX | V2X Tx (Emergency Source) | 경찰/구급 이벤트 송신 역할 분리 |
| CHASSIS_GW | Chassis Gateway/CGW | Chassis CAN 경계 게이트웨이 |
| INFOTAINMENT_GW | Infotainment Gateway/CGW | IVI CAN 경계 게이트웨이 |
| BODY_GW | Body Gateway/CGW | Body CAN 경계 게이트웨이 |
| IVI_GW | IVI Gateway/CGW | Cluster/IVI 출력 경계 게이트웨이 |
| ENGINE_CTRL | EMS/ECM(개념 대응) | 엔진 상태 반영 기능(프로젝트 모델) |
| TRANSMISSION_CTRL | TCU(개념 대응) | 기어 상태 반영 기능(프로젝트 모델) |
| ACCEL_CTRL / BRAKE_CTRL / STEERING_CTRL | Chassis ECU 기능군 | EPS/ESC/Brake ECU 기능군에 대응되는 입력 처리 모델 |

### 5-2) 제출 전 최종 치환 계획(고정)

- 본 문서는 현재 프로젝트 표준 노드명을 기준으로 유지한다.
- 제출 직전에는 현대/기아 및 OEM 실차 문서(DBC/사내 용어집) 기준으로 명칭을 최종 점검한다.
- 점검 완료 후 `03/0301/0302/0303/0304/04/05/06/07`의 표시명을 OEM 표기로 일괄 대체한다.
- 단, 추적성 ID(`Req/Func/Flow/Comm/Var/Test`)와 ID 번호 체계는 변경하지 않는다.

## 6) ISO 26262 용어 (참고)
| 용어 | 풀네임 | 핵심 의미 |
|---|---|---|
| `HARA` | Hazard Analysis and Risk Assessment | 위험원 식별 및 리스크 평가 |
| `ASIL` | Automotive Safety Integrity Level | 안전 무결성 등급 (A~D) |
| `SG` | Safety Goal | 상위 안전 목표 |
| `FSR` | Functional Safety Requirement | 기능안전 요구사항 |
| `TSR` | Technical Safety Requirement | 기술안전 요구사항 |
| `SEooC` | Safety Element out of Context | 맥락 독립 안전 요소 개발 접근 |

## 7) ASPICE 용어 (참고)
| 용어 | 의미 | 문서/추적 관점 |
|---|---|---|
| `SYS.1` | System Requirements Analysis | 시스템 요구 정의/정합 |
| `SYS.2` | System Architectural Design | 시스템 아키텍처 설계 |
| `SYS.3` | System Integration and Integration Test | 시스템 통합/통합 시험 |
| `SYS.4` | System Qualification Test | 시스템 자격 시험 |
| `SWE.1` | Software Requirements Analysis | SW 요구 정의 |
| `SWE.2` | Software Architectural Design | SW 아키텍처 설계 |
| `SWE.3` | Software Detailed Design and Unit Construction | 상세 설계/구현 |
| `SWE.4` | Software Unit Verification | 단위 검증 |
| `SWE.5` | Software Integration and Integration Test | SW 통합/통합 시험 |
| `SWE.6` | Software Qualification Test | SW 자격 시험 |

## 8) 문서 적용 원칙 (01~07 비침투)
- `01~07` 본문에는 표준 양식 중심으로 작성하고, 약어 과다 확장은 지양한다.
- 약어 해석이 필요한 경우 본 문서를 참조 링크로만 연결한다.
- 공식 문서에서는 추적성 ID(`Req/Func/Flow/Comm/Var/Test`)를 우선하고, 약어 해설은 본 참조 문서에서 관리한다.

## 9) 변경 이력
| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| `1.0` | `2026-02-26` | 프로젝트 전용 네이밍/약어/표준 용어 참조표 초안 작성 |
| `1.1` | `2026-02-28` | 프로젝트 노드명 유지 + OEM 스타일 매핑표(5-1) 추가 |
