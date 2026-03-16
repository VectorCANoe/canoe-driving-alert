# Retired umbrella rows for Master Test Matrix

이 문서는 active 기준선에서 분리된 umbrella row 이력을 보관한다.
active 추적과 실행 기준은 [00g_Master_Test_Matrix.md](C:/Users/이준영/CANoe-IVI-OTA/driving-alert-workproducts/governance/00g_Master_Test_Matrix.md)를 따른다.

| Req ID | Safety Goal | Summary | Test Level | Retired ID | Stimulus | Oracle | Timing | Evidence | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `Req_067, Req_068, Req_069, Req_073, Req_074` | `-` | 운전자 상태와 경고 설정이 출력 정책에 반영되어야 한다 | `IT` | `RET_IT_013` | 방향지시등, 주행모드, 안전벨트, 표시/음량 설정 입력 | 운전자 상태/설정 umbrella row는 exact executable rows로 분해되어 관리된다 | `<=150ms` | `evidence/RET_IT_013/*` | `Validation` | `Retired` |
| `Req_037, Req_038` | `-` | 시동 및 기어 상태는 경고 판단 경로에 일관되게 반영되어야 한다 | `IT` | `RET_IT_015` | 시동 ON/OFF, 기어 상태 변화 입력 | 시동/기어 umbrella row는 exact executable rows로 분해되어 관리된다 | `100ms` | `evidence/RET_IT_015/*` | `Validation` | `Retired` |
| `Req_039, Req_040, Req_041` | `HC-02` | 가속, 제동, 조향 입력은 주행 판단 경로에 정확히 반영되어야 한다 | `IT` | `RET_IT_016` | 가속, 제동, 조향 입력 변화 | 가속/제동/조향 umbrella row는 exact executable rows로 분해되어 관리된다 | `100ms` | `evidence/RET_IT_016/*` | `Validation` | `Retired` |
| `Req_042, Req_043` | `-` | 비상등과 창문 상태는 경고 맥락에 일관되게 반영되어야 한다 | `IT` | `RET_IT_017` | 비상등, 창문 상태 변화 입력 | 비상등/창문 umbrella row는 exact executable rows로 분해되어 관리된다 | `100ms` | `evidence/RET_IT_017/*` | `Validation` | `Retired` |
| `Req_045, Req_046, Req_047` | `-` | 실내 제어와 보안 상태는 경고 정책에 일관되게 반영되어야 한다 | `IT` | `RET_IT_019` | 공조, 시트, 미러, 도어, 와이퍼, 보안 상태 입력 | 공조/도어·와이퍼 baseline/보안 umbrella row는 exact executable rows로 분해되어 관리된다 | `100ms/150ms` | `evidence/RET_IT_019/*` | `Validation` | `Retired` |
| `Req_078, Req_079, Req_081, Req_082` | `HC-07, HC-08` | 채널 장애와 팝업 과밀 상황에서도 우선 경고 인지성과 채널 동기가 유지되어야 한다 | `IT` | `RET_IT_021` | 출력 채널 장애, 팝업 과밀, 대체 출력 조건 입력 | 출력 가용성/과밀/동기 umbrella row는 exact executable rows로 분해되어 관리된다 | `<=150ms` | `evidence/RET_IT_021/*` | `Validation` | `Retired` |
| `Req_096, Req_097` | `-` | 경찰 또는 구급 긴급 이벤트 발생 시 Ethernet 경로의 외부 송신 메시지가 정의된 `100ms` 주기로 연속 관찰되어야 한다 | `ST` | `RET_ST_018` | 경찰/구급 긴급 이벤트 발생 및 유지 입력 | 외부 송신 메시지가 `100ms` 주기로 연속 관찰되고 clear 시점까지 컨텍스트가 일관 유지 | `100ms` | `evidence/RET_ST_018/*` | `Validation` | `Retired` |
| `Req_067, Req_068, Req_069, Req_070, Req_073` | `-` | 운전자 상태와 접근거리 정보가 시스템 레벨 경고 안내에 기대대로 반영되어야 한다 | `ST` | `RET_ST_029` | 방향지시등, 주행모드, 안전벨트, 접근거리 표시 조건 입력 | 사용자 기대와 일치하는 안내 보정 | `<=150ms` | `evidence/RET_ST_029/*` | `Validation` | `Retired` |
| `Req_075, Req_076, Req_077, Req_080` | `HC-08` | 입력 지연과 상태 전이 상황에서도 경고 안내는 안정적으로 유지되어야 한다 | `ST` | `RET_ST_032` | 입력 지연, stale, 상태 전이 조건 입력 | 경고 안내가 안정적으로 유지되고 반복 진동이 억제 | `<=150ms` | `evidence/RET_ST_032/*` | `Validation` | `Retired` |
| `Req_078, Req_079, Req_080, Req_081, Req_082` | `HC-07, HC-08` | 경고 인지성과 채널 동기가 다중 부하 상황에서도 유지되어야 한다 | `ST` | `RET_ST_033` | 채널 전환, 오디오 경합, 팝업 과밀 입력 | 안정적 출력, 우선 경고 인지성 유지, 채널 동기 유지 | `<=150ms` | `evidence/RET_ST_033/*` | `Validation` | `Retired` |
