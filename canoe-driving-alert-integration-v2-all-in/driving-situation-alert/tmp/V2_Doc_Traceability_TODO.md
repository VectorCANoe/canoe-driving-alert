# V2 문서 개정 TODO (Req-Func-Comm 정합 강화)

## 목적
- 현재 DBC/CAPL 확장분(기본 차량 기능 + 확장 CAN 신호)을 01/03 문서 수준까지 끌어올려
  `Req -> Func -> Flow -> Comm -> Var -> UT/IT/ST` 추적 밀도를 동등하게 맞춘다.

## 작업 원칙
- 01은 What, 03+는 How 유지
- 공식 상단표 구조는 유지, 상세는 하단 추적표로 분리
- 기존 Req/Func ID는 보존, 신규는 확장 ID로 추가
- CANoe SIL + CAN/Ethernet 검증 범위만 다룸

## Phase 1 (Critical)
- [ ] 01 세분 요구 추가 (차량 기본 기능군)
  - 파일: `driving-situation-alert/01_Requirements.md`
  - 대상: HVAC, Seat, Mirror, Door Control, Wiper/Rain Auto, Immobilizer/Alarm, Audio Focus/TTS
  - 제안 ID: `Req_113~Req_132`
  - 산출: 각 Req에 VC 추가(`VC_113~VC_132`), Part 0 설명 갱신

- [ ] 03 세분 기능 추가 (기능군별 독립 Func)
  - 파일: `driving-situation-alert/03_Function_definition.md`
  - 제안 ID: `Func_113~Func_132`
  - 예: `HVAC_CTRL`, `SEAT_CTRL`, `MIRROR_CTRL`, `DOOR_CTRL`, `WIPER_RAIN_CTRL`, `SECURITY_STATE_CTRL`, `AUDIO_STATE_CTRL`
  - 산출: Req 1:1 연결 + 입력/출력 변수 명시

## Phase 2 (High)
- [ ] 0301 정합화
  - 파일: `driving-situation-alert/0301_SysFuncAnalysis.md`
  - 내용: 신규 Func/노드 역할/책임/도메인 배치 반영

- [ ] 0302/0303 매핑 밀도 보강
  - 파일: `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md`
  - 내용: 이미 존재하는 확장 메시지(HVAC/Seat/Diag/Audio 등)를 신규 Req/Func와 명시적 연결

- [ ] 0304 변수 추적표 동기화
  - 파일: `driving-situation-alert/0304_System_Variables.md`
  - 내용: 신규 Func/Req 기준으로 Var 추적표(Internal/Comm/Flow/Func/Req) 보강

## Phase 3 (Validation)
- [ ] 05/06/07 테스트 커버리지 확장
  - 파일: `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md`
  - 내용: 신규 Req/Func 별 최소 1개 이상 UT/IT/ST 연결
  - 기준: 정상 + 경계 + fail-safe(해당 시) 케이스 분리

## 의사결정 보류 항목
- [ ] Sound 경고 출력 체인(AMP/SOUND ECU) 도입 여부
  - 현재: Audio Focus/TTS 상태는 존재, 독립 경고음 출력 체인은 미도입
  - 선택지:
    - A. V2 포함: `Req/Func/Comm/Var/UT-IT-ST` 전체 신규 추가
    - B. V2 제외: `Out of Scope` 명시 후 V3 백로그

## 완료 조건 (Merge Gate)
- [ ] 신규 Req/Func가 0302/0303/0304 및 05/06/07에 누락 없이 연결
- [ ] 랜덤 Req 샘플 10건 추적 시 체인 단절 0건
- [ ] 상단 공식 표 형식 훼손 0건
- [ ] 문서 인코딩 UTF-8 유지, 품질 게이트 통과
