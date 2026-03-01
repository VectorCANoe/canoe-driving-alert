# SIL Pass/Fail Criteria (Req_043)

> CANoe SIL 환경에서 시나리오별 합격/불합격 판정 기준.
> SIL_TEST_CTRL.can의 `evaluateScenarioResult()` 함수와 1:1 대응한다.

---

## 시나리오 판정 기준표

| ID | 시나리오명 | 관련 Req | 판정 조건 | 커버 흐름 |
|----|-----------|---------|---------|---------|
| **S01** | 정상 아이들 | Req_001/002 | `selectedAlertLevel==0 AND warningTextCode==0` | driveState=3, 경고 없음 |
| **S02** | 스쿨존 과속 | Req_009/010/037 | `level==3 AND type==3 AND ambientColor==3 AND ambientPattern==5` | roadZone=1, speed=45, limit=30 |
| **S03** | 고속도로 조향미입력 | Req_011/012/038 | `level==2 AND type==4 AND ambientColor==4 AND ambientPattern==4` | roadZone=2, steerInput=0, 10s 경과 |
| **S04** | 경찰차 긴급 | Req_017/022/035/036 | `level==6 AND type==1 AND code==101 AND guard>0 AND ambientColor==6 AND ambientPattern==6` | V2X police active |
| **S05** | 구급차 긴급 | Req_018/022/035/036 | `level==7 AND type==2 AND code==202 AND guard>0 AND ambientColor==7 AND ambientPattern==7` | V2X ambulance active |
| **S06** | 타임아웃 해제 | Req_024 | `timeoutClear==1 AND level==0 AND code==0` | 1000ms 무갱신 후 watchdog 해제 |
| **S07** | 유도구간 좌측 | Req_013/014/039 | `level==2 AND type==5 AND ambientColor==5 AND ambientPattern==2 AND code==31` | roadZone=3, navDir=1 |
| **S08** | 유도구간 우측 | Req_013/014/039 | `level==2 AND type==6 AND ambientColor==5 AND ambientPattern==3 AND code==32` | roadZone=3, navDir=2 |
| **S09** | ETA 우선순위 | Req_030 | `V2X::eta==10 AND V2X::sourceId==99 AND level==6` | 경쟁 police: ETA20→ETA10 takeover |
| **S10** | SourceID 동률 처리 | Req_031 | `V2X::sourceId==5 AND V2X::eta==10 AND level==6` | 동ETA 경쟁: sourceId20→sourceId5 |
| **S11** | 전환 완화 | Req_034 | `level==6 AND type==1 AND snapshotDelta<=3` | 내비 guide→police, arb 변화 ≤3회 |
| **S12** | 경고 반복 억제 | Req_006/026 | `level==3 AND type==3 AND duplicatePopupGuard>0` | 스쿨존 경고 해제 후 재발생, 가드 재활성 |
| **S13** | 구간 전환 안정성 | Req_015 | `level==3 AND type==3 AND snapshotDelta<=3` | school→highway→school, arb 변화 ≤3회 |
| **S14** | 도메인 경계 무결성 | Req_110/111/112 | `domainBoundaryStatus==1 AND routingPolicy==1 AND level==0` | D gear 정상 주행, 3도메인 alive |

---

## 판정 흐름

```
Test::testScenario = N  →  applyScenarioPreset(N)
                        →  scheduleScenarioEvaluation(N)  [tScenarioEval]
                        →  (Phase2: tScenarioPhase2, Phase3: tScenarioPhase3)
                        →  evaluateScenarioResult()
                        →  Test::scenarioResult = 1(PASS) / 0(FAIL)
                        →  frmTestResultMsg.ScenarioResult 출력
                        →  frmBaseTestResultMsg.BaseScenarioResult 출력
```

---

## 자동 데모 실행 (scenarioId=100)

`Test::testScenario = 100` 설정 시 S01→S08 순환 자동 실행 (각 4초 간격).

- 고속도로 시나리오(S03)는 10초 대기 포함 → 전체 데모 약 50초 소요
- Write 창에서 각 단계 결과 확인 가능

---

## sysvar 판정 체계

| sysvar | 역할 | 판정에 사용 |
|--------|------|----------|
| `@Test::scenarioResult` | 현재 시나리오 결과 (0/1) | S01~S14 전체 |
| `@Core::selectedAlertLevel` | 중재 결과 alertLevel (0~7) | 전체 |
| `@Core::selectedAlertType` | 중재 결과 alertType (0~7) | 전체 |
| `@Cluster::warningTextCode` | IVI 표시 코드 | S04~S08 |
| `@Body::ambientColor` | 앰비언트 색상 (0~7) | S02~S05, S07/S08 |
| `@Body::ambientPattern` | 앰비언트 패턴 (0~7) | S02~S05, S07/S08 |
| `@CoreState::duplicatePopupGuard` | 팝업 가드 잔여 ms | S04/S05/S12 |
| `@CoreState::arbitrationSnapshotId` | 중재 상태 변경 카운터 | S11/S13 |
| `@CoreState::domainBoundaryStatus` | 도메인 경계 건강도 (0/1) | S14 |
| `@CoreState::routingPolicy` | GW 라우팅 정책 (0/1/2) | S14 |
| `@V2X::eta` | 활성 긴급신호 ETA | S09/S10 |
| `@V2X::sourceId` | 활성 긴급신호 SourceID | S09/S10 |

---

## 앰비언트 색상/패턴 표준 (Req_035~039)

| alertType | 의미 | ambientColor | ambientPattern |
|-----------|------|-------------|----------------|
| ≥6 (Emergency) | 경찰 | 6 (RED/BLUE) | 6 (emergency flash) |
| ≥6 (Ambulance) | 구급 | 7 (RED/WHITE) | 7 (emergency flash) |
| 3 | 스쿨존 | 3 (RED) | 5 (fast flash) |
| 4 | 고속도로 | 4 (ORANGE) | 4 (pulse) |
| 5 | 유도 좌 | 5 (CYAN) | 2 (flow-left) |
| 6 | 유도 우 | 5 (CYAN) | 3 (flow-right) |
| 1 | 일반 | 1 (GREEN) | 1 (solid) |
| 0 | 없음 | 0 | 0 |

---

## 판정 체계 버전 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v1.0 | 2026-03-01 | S01~S14 판정 기준 최초 정의 |
