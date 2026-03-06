# 개발팀 전달서 (잔여 항목): 제품 스코프 정합 정리

문서 ID: DEV-CO-DBC-20260305-R2  
작성일: 2026-03-06  
작성 주체: 문서작성팀  
대상: CANoe 개발팀

## 0. 문서 목적

- 본 문서는 기존 DBC/명명 정리 작업의 **완료 항목을 제외**하고, 현재 남아 있는 개발팀 반영 필요사항만 전달한다.
- 핵심 목적은 제품 체인(무조향 경고)과 비제품 하네스 항목(과거 DriverState/gaze 흔적)의 경계를 런타임 아티팩트까지 일치시키는 것이다.

## 1. 현재 문서팀 결정(고정)

- 제품 기능 체인: `고속도로 무조향 기반 주의저하 의심 경고` (`Req_011/012/038`)
- 비제품 하네스: `Test/*`, `V2X/*`, `UiRender/*`만 허용
- 제품 기능처럼 보이는 `DriverState/gaze` 계열 표현은 문서체인(00c/00d/01/03/04/0304)에서 제거 완료

## 2. 개발팀 잔여 반영 항목 (In Scope)

1. 활성 런타임 경로에서 DriverState/gaze 잔여 제거
- 대상(활성 경로):
  - `canoe/src/capl/ecu/DRV_STATE_MGR.can`
  - `canoe/src/capl/output/BODY_GW.can`
  - `canoe/cfg/channel_assign/Body/DRV_STATE_MGR.can`
  - `canoe/cfg/channel_assign/Body/BODY_GW.can`
  - `canoe/project/sysvars/project.sysvars`
  - `canoe/databases/body_can.dbc` 내 `frmDriverStateMsg` 계열
  - `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md` 관련 행

2. 통신/DB 정합
- `frmDriverStateMsg`를 활성 제품 경로에서 제거하거나, 불가피 시 별도 하네스 전용으로 분리(제품 Req 체인 미연계 명시).
- 문서 SoT 기준(01/03/0302/0303/0304/04)과 DBC/CAPL 간 불일치 0건 보장.

3. cfg/생성물 동기화
- GUI-first 원칙으로 cfg 재저장 후 관련 생성물(`*.cfg.ini`, `*.stcfg`) 포함 정합 점검.

## 3. 변경 제외 (Out of Scope)

- 무조향 경고 로직 자체 변경
- TTC/위험도/Fail-safe 임계값 변경
- 신규 기능 추가(후진/주차 신규 시나리오 포함)

## 4. 수용 기준 (Acceptance)

1. 스코프 정합
- 활성 경로에서 `DriverState/gaze` 제품 기능 해석 요소 0건
- 제품 기능 설명이 `무조향 경고` 체인과 1:1 일치

2. 실행 동등성
- 기존 핵심 시나리오 결과 유지:
  - 무조향 경고 발생/해제
  - 긴급 경고/중재
  - V2 위험도/Fail-safe

3. 추적성
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 단절 0건

## 5. 개발팀 제출물

1. 변경 파일 목록(DBC/CAPL/sysvars/cfg)
2. 잔여 문자열 스캔 결과:
- `DriverState`
- `gaze`
- `frmDriverStateMsg`
3. 핵심 회귀 결과 요약(무조향/긴급/V2)
4. 최종 기준 커밋 해시

## 6. 전달 메모

- 본 전달은 기능 추가 지시가 아니라 **제품 스코프 정합 마감 지시**다.
- 필요 시 하네스 보조 코드는 별도 브랜치/별도 네임스페이스로만 유지하고, 메인 제품 경로와 혼합하지 않는다.
