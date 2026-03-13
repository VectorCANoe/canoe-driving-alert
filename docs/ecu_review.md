# ECU CAPL 코드 점검 체크리스트

각 ECU별 핵심 로직 및 통신 상태를 점검하기 위한 체크리스트입니다.

## 1. 핵심 시나리오 로직 (Control Layer)
| ECU | 파일 경로 | 점검 항목 | 상태 | 비고 |
| :--- | :--- | :--- | :---: | :--- |
| **ADAS** | `canoe/cfg/channel_assign/ADAS/ADAS.can` | 위험도 판정 및 경보 선택 로직 | [ ] | |
| **V2X** | `canoe/cfg/channel_assign/ETH_Backbone/V2X.can` | 긴급차량 브로드캐스트 수신/처리 | ✅ | frmEmergencyBroadcastMsg, frmEmergencyMonitorMsg 두 개의 메세지를 내보내는 코드가 있지만, 현재는 아무 메세지도 내보내거나 받고 있지 않음 |
| **SCC** | `canoe/cfg/channel_assign/ADAS/SCC.can` | 스마트 크루즈 컨트롤 연동 및 감속 요청 | ✅ | |

## 2. 출력층 (Output Layer)
| ECU | 파일 경로 | 점검 항목 | 상태 | 비고 |
| :--- | :--- | :--- | :---: | :--- |
| **BCM** | `canoe/cfg/channel_assign/Body/BCM.can` | 바디 제어 및 비상등/경고음 출력 | ✅ | |
| **CLU** | `canoe/cfg/channel_assign/Infotainment/CLU.can` | 클러스터 경고 문구 및 아이콘 표시 | [ ] | |
| **IVI** | `canoe/cfg/channel_assign/Infotainment/IVI.can` | 인포테인먼트 화면 및 음성 안내 | [ ] | |

## 3. 제어 (Infrastructure/Integration)
| ECU | 파일 경로 | 점검 항목 | 상태 | 비고 |
| :--- | :--- | :--- | :---: | :--- |
| **CGW** | `canoe/cfg/channel_assign/ETH_Backbone/CGW.can` | 도메인 간 게이트웨이 라우팅 및 Fail-safe | ✅ | 각 도메인과 연결이 되었는지 체크를 하는 코드가 있는데, CAN 메세지를 받는 대신 UDP 패킷을 받는 것이 아키텍처 그림과 일치하는 것 같음(CGW_explain.md문서 참고) |
| **VCU** | `canoe/cfg/channel_assign/Chassis/VCU.can` | 차량 전체 상태 및 동력 정책 제어 | [ ] | |

## 4. 동역학 (Chassis/Safety)
| ECU | 파일 경로 | 점검 항목 | 상태 | 비고 |
| :--- | :--- | :--- | :---: | :--- |
| **ESC** | `canoe/cfg/channel_assign/Chassis/ESC.can` | 제동 상태 및 차체 안정화 제어 | [ ] | |
| **MDPS** | `canoe/cfg/channel_assign/Chassis/MDPS.can` | 조향 상태 및 조향 보조 제어 | [ ] | |

---

### 공통 점검 사항
- [ ] 컴파일 오류 및 경고 발생 여부
- [ ] CAN ID 및 시그널 매핑 (DBC 준수 여부)
- [ ] 시스템 변수(System Variable) 연동 확인
- [ ] 타이머(Timer) 및 주기적 송신 로직 정상 작동 여부
