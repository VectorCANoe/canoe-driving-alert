# B-PLAN POC (After A Complete)

## A안 현황 요약 (현재 기준)
- 상태: A안 핵심 체인(입력→판단→중재→출력) 동작/시연 가능
- 실행 기준: `canoe/cfg/CAN_500kBaud_1ch.cfg`
- 확인 완료:
  - 주행/비주행, 스쿨존 경고, 긴급 경고, 기본 우선순위, 1000ms 워치독
  - CANoe SIL 환경에서 컴파일/측정 정상
- 현재 묶음 보류(한 번에 설계/검증):
  - `Req_030/031`, `Req_033`, `Req_043`
  - 시나리오 `3/4/5` 전환 시 우선순위/주입값 정합
- 우선 개발 진행 항목:
  - `Req_011/012`, `Req_013/014`, `Req_019/020/021`, `Req_006/026`

## 1) 목적
A안(CANoe 단독 데모)을 먼저 완성한 뒤, B안(도로 3D 렌더링 연동)을 단계적으로 붙인다.

## 2) 왜 B안을 구현하는가
A안만으로도 기능 시연은 가능하지만, 아래 요구를 충족하려면 B안이 필요하다.
- 대외 시연에서 "도로 상황"을 직관적으로 보여야 함
- 네비 진입(스쿨존/고속/유도선)과 긴급차 접근을 시각적으로 설득력 있게 전달
- 기능 데모를 홍보/리뷰 영상으로 재사용 가능해야 함

즉, B안은 기능 검증 목적이 아니라 "스토리텔링/전달력 강화" 목적이다.

## 3) 툴 선택
선택: `CARLA + Python Bridge + CANoe`

선정 근거:
- Python 기반 자동화/AI 생태계가 가장 풍부
- 도로/교통 시나리오 생성이 용이
- 기존 CANoe UDP 구조와 브리지 연결이 단순

## 4) 아키텍처
- CARLA: 도로/차량/환경 렌더링 + 이벤트 생성
- Bridge(Python): CARLA 이벤트 -> CANoe 변수 계약으로 변환
- CANoe: 기존 CAPL 경고 로직 처리 + Ambient/Cluster 결과 생성

데이터 방향:
- CARLA -> Bridge -> CANoe 입력
  - `Chassis::vehicleSpeed`
  - `Infotainment::roadZone`, `Infotainment::navDirection`, `Infotainment::zoneDistance`
  - `V2X::alertState`, `V2X::emergencyType`, `V2X::emergencyDirection`, `V2X::eta`
- CANoe 출력(관측)
  - `Body::*`, `Cluster::warningTextCode`
  - Trace(`0x210`, `0x220`, `E100`, `E200`)

## 5) 단계별 계획
### Phase B0 (사전조건)
- A안 100% 재현 가능
- FZ_001~FZ_007 캡처 증적 확보

### Phase B1 (PoC)
- CARLA 1개 맵에서 기본 주행 + 구간 이벤트 3종 구현
- CANoe 입력 변수 브리지 연결
- CANoe 출력과 CARLA 화면 동시 녹화 성공

### Phase B2 (시나리오 확장)
- 긴급차 시나리오(경찰/구급) + 우선순위 장면 구현
- 타임아웃/복귀 시나리오까지 포함

### Phase B3 (영상 패키징)
- 60~90초 데모 영상 템플릿 고정
- 자막/오버레이(현재 경고 타입/레벨) 반영

## 6) 리스크와 대응
- 리스크: B안 일정 지연
- 대응: A안 완성본을 기본 납품선으로 유지
- 규칙: B안 실패 시에도 A안 데모로 납기 대응 가능해야 함

## 7) 구현 범위 규칙
- `00~07` 문서는 수정하지 않음(참조)
- 구현/스크립트/운영문서는 `canoe/` 기준으로 추가
