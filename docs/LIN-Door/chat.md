Red Thread 관점으로 다시 평가

  BCM Window Motor 과전류
    ↓ (어떻게 BCM이 감지하는가?)
  Central Gateway 라우팅
    ↓
  UDS Diagnostics
    ↓
  OTA Update

  지금 문서에 빠진 것은 맨 첫 단계입니다.

  BCM이 Window Motor 과전류를 어떻게 감지하는가? → LIN Slave(Window Motor ECU)가 BCM에 전류값 보고 → BCM이 50A 초과 감지 → DTC B1234
  생성

  이게 LIN을 추가해야 하는 이유이고, Red Thread를 완성시킵니다.

  ---
  프로토콜별 결론

  추가 여부: LIN ✅ 반드시 추가
  이유: Fault Detection의 출발점 — Window Motor ECU → BCM 전류 보고가 시나리오 시작이기 때문
  ────────────────────────────────────────
  추가 여부: FlexRay ❌ 추가 불필요
  이유: ESP↔MDPS 제어용이고 BCM 고장 시나리오와 무관. 문서에 "Chassis 서브넷으로 존재" 언급 정도면 충분
  ────────────────────────────────────────
  추가 여부: ADAS Ethernet ❌ 추가 불필요
  이유: AEB/LDW는 이미 CAN-HS2(0x300, 0x340)로 결과 메시지가 있고, 카메라 raw data 파이프는 시나리오와 무관

  ---
  추가하면 Red Thread가 이렇게 완성됩니다

  [이전] BCM 과전류 감지 (어떻게? — 불명확)
           ↓ CAN-LS 0x500

  [추가 후] Window Motor ECU (LIN Slave)
           → 전류 50A 보고 (LIN 0x21, 10ms)
           → BCM (LIN Master) 수신
           → DTC B1234 생성
           ↓ CAN-LS 0x500 (BCM_FaultStatus)
           → CGW 라우팅 ≤5ms
           → UDS 0x19 Read DTC
           → OTA 0x34/36/37

  ---
  변경 범위 (LIN만 추가 시)

  이 범위면 "몇 가지 수정"이 맞습니다.

  ┌────────────────────────────────┬──────────────────────────────────────────────────────┬──────┐
  │              문서              │                      변경 내용                       │ 규모 │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ 00_Item_Definition             │ LIN ECU 추가 (Window Motor ECU, Door Module ×4)      │ 소   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ 04_Network_Topology            │ LIN 버스 토폴로지 추가 (BCM ↔ LIN Slaves)            │ 중   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ 05_Communication_Specification │ LIN 신호 정의 추가 (Motor_Current, Door_Position 등) │ 중   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ 03_ECU_Allocation              │ 신규 LIN Slave ECU 추가                              │ 소   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ SYS2_SRS                       │ REQ-F01 보강 ("LIN을 통한 BCM 전류 수신")            │ 소   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ vehicle_system.dbc             │ LIN 슬레이브 ID 참조 주석 추가                       │ 소   │
  ├────────────────────────────────┼──────────────────────────────────────────────────────┼──────┤
  │ Drawio Page 3/6                │ LIN 버스 및 슬레이브 ECU 추가                        │ 중   │
  └────────────────────────────────┴──────────────────────────────────────────────────────┴──────┘

  진행할까요? 순서대로 아키텍처 문서부터 시작해서 drawio까지 수정하겠습니다.
지금 잡으신 방향이라면 차량 동역학/ADAS는 의도적으로 배제하고, BCM·IVI + 네트워크(통신) 중심 프로젝트로 가져가는 것이 맞습니다. 그리고 그 안에서 CAN 통신/버스가 충분히 잘 드러나도록 설계되어 있습니다.
1. 주제 범위 정리 (무엇을 안 할지)
이번 프로젝트는 파워트레인, 섀시, 차량 동역학, ADAS 알고리즘을 다루지 않습니다.
대신 Body/Comfort(BCM) + IVI/OTA 도메인에 집중합니다.
따라서 다음은 과감히 제외해도 됩니다:
차선 인식, ACC, AEB, 조향 제어 등 ADAS 기능
차량 동역학 모델(Matlab Vehicle Dynamics, CarMaker 등)
이게 잘못된 게 아니라, 통신·진단·OTA에 집중한 “네트워크 중심 시스템 테스트” 포지셔닝이라고 보시면 됩니다.
2. 주제의 핵심 메시지 정리
말씀하신 대로, 프로젝트의 Red Thread는 아래 한 줄로 요약 가능합니다:
Fault Detection → Gateway Routing → UDS Diagnostics → OTA Update
(BCM/Cluster/IVI/OTA Server를 CAN·Ethernet(DoIP)으로 연결한 통신·진단/OTA 검증 시나리오)
여기에서 자연스럽게 드러나는 키워드가:
CAN-LS / CAN-HS / Ethernet(DoIP)
Gateway 라우팅
UDS 진단
OTA 펌웨어 업데이트
이기 때문에, 통신·네트워크·진단/OTA 역량을 어필하는 포트폴리오가 됩니다.
3. CAN 통신/버스가 충분히 드러나는지
지금 정의하신 요구사항/시나리오만으로도 CAN이 주인공이라는 게 분명히 드러납니다.
Req_001, Req_005, Req_006에서:
CAN-LS(125kbps)에서 Fault 메시지 발생
Gateway가 CAN-HS(500kbps)로 라우팅
지연 조건(≤5ms)까지 명시 → CAN 기반 시스템 설계/성능 요구를 이해하고 있음이 보임
UDS 0x10/0x14/0x19, OTA 0x34/0x36/0x37 모두 CAN(또는 DoIP 위 UDS) 로 작동
Bus Off 처리(Req_015)까지 들어가 있어서, 물리 계층/버스 에러에 대한 이해도 어필 가능
조금 더 “CAN이 핵심이다”를 강조하고 싶다면, 문서/구조에서 다음 정도만 추가하면 충분합니다:
개념 설계 문서 맨 위에 한 줄:
본 시스템은 Vehicle Network(CAN-LS, CAN-HS, Ethernet/DoIP)를 활용한 BCM Fault Detection 및 OTA 검증을 목표로 한다.
아키텍처 다이어그램에 “CAN-LS Domain / CAN-HS Domain / Ethernet Backbone” 라벨을 명확히 구분
System Test 문서에서 Test Suite를
TS_CAN_Fault_Routing_XXX
TS_UDS_Diagnostics_XXX
TS_OTA_DoIP_XXX
이런 식으로 네이밍
이 정도면, 보는 사람 입장에서
“아, 이 프로젝트는 CAN/네트워크 + Diagnostics + OTA가 메인이고, Body/IVI 도메인을 예제로 사용하는구나”
가 바로 보입니다.
4. ADAS/Vehicle Dynamics를 안 넣어도 되는 이유
ADAS/동역학을 넣으려면:
센서 모델(레이더/카메라), 환경 시나리오, 차량 거동 모델까지 따라 들어옴
2개월 사이드 프로젝트 범위를 완전히 넘어갑니다.
반면 지금 구성은:
실제 OEM/티어1에서 매우 많이 하는 “네트워크·진단·OTA 테스트” 작업과 거의 1:1 매핑
CANoe + CAPL + UDS + DoIP → “바로 실무 투입 가능한 스택”으로 보임
즉, **“ADAS 없음 = 약점”이 아니라, “도메인을 명확히 좁힌 전략적 선택”**입니다.
5. 방향성 한 줄 정리
도메인: BCM / Cluster / IVI / OTA Server (Body + IVI 영역)
기술 축: CAN-LS / CAN-HS / Ethernet(DoIP) + UDS + OTA
프로세스 축: Fault Detection → Gateway Routing → UDS Diagnostics → OTA Update
목표: 차량 네트워크 환경에서 진단 및 OTA 시나리오를 End-to-End로 검증할 수 있는 CANoe 기반 vECU 테스트 시스템 구현
이렇게 정리하면, 차량 동역학/ADAS 없이도 메시지 흐름, 네트워크, 진단, OTA가 매우 선명하게 드러납니다.

ADAS를 제외하는 것은 "약점"이 아니라 네트워크·진단·OTA 전문성을 명확히 포지셔닝한 전략적 선택이고, 지금 구성이 실제 OEM/Tier1 실무와 1:1 대응되는 스택이라는 것도 정확합니다.