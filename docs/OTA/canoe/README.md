# CANoe 프로젝트 구조

## 폴더 구성

```
canoe/
├── cfg/
│   ├── project.cfg          ← CANoe 프로젝트 파일 (메인)
│   └── project.sysvars      ← System Variables 정의
├── databases/
│   └── project.dbc          ← CAN 메시지/신호 데이터베이스
├── nodes/
│   ├── Vehicle_ECU.can      ← 입력 A: 차속/가속도/제동 (택천)
│   ├── MDPS_ECU.can         ← 입력 B: 조향/급차선변경 (현준)
│   ├── LDW_ECU.can          ← 입력 B: 차선이탈 (현준)
│   ├── WDM_ECU.can          ← 판단층: Rule-Based 경고 결정 (공동/준영)
│   ├── CGW.can              ← Gateway: CAN-LS→HS 라우팅, DoIP
│   ├── Cluster_ECU.can      ← 출력: 경고등 (1단계황색/2단계적색)
│   ├── Ambient_ECU.can      ← 출력: 앰비언트 패턴 (준영)
│   ├── Sound_ECU.can        ← 출력: 단계별 경고음
│   ├── IVI_ECU.can          ← 출력: OTA 팝업 (성현)
│   ├── Door_ECU.can         ← 출력: 도어잠금/미러LED (현준2)
│   └── OTA_Server.can       ← OTA: UDS 세션 관리 (성현)
└── test_modules/
    ├── TC_A_SpeedInput/      ← 과속/급가속/급제동 테스트
    ├── TC_B_DirectionInput/  ← 차선이탈/급차선변경 테스트
    ├── TC_W_Warning/         ← 1/2/3단계 경고 및 해제 테스트
    ├── TC_Z_ZoneAmbient/     ← gRoadZone 구간별 앰비언트 테스트
    ├── TC_O_OTA/             ← OTA UDS 세션 / Rollback / Bus Off 테스트
    └── TC_E2E_Master_Scenario/ ← 전체 E2E 시나리오 (Scene.1~17)
```

## CAN 버스 채널 매핑

| 채널 | 프로토콜 | 속도 | 연결 ECU |
|------|----------|------|----------|
| CAN 1 (LS) | CAN 2.0B | 125 kbps | Vehicle_ECU / MDPS_ECU / LDW_ECU → CGW |
| CAN 2 (HS) | CAN 2.0B | 500 kbps | CGW → WDM_ECU / Cluster / Ambient / Sound / IVI / Door |
| Ethernet | DoIP | 100 Mbps | OTA_Server ↔ CGW ↔ WDM_ECU |

## 참조

- 통신 명세: `../0303_Communication_Specification.md`
- System Variables: `../0304_System_Variables.md`
- SW 구현: `../04_SW_Implementation.md`
- Sample CAPL 패턴 참조: `../../sample/canoe/nodes/BCM.can`, `CGW.can`
