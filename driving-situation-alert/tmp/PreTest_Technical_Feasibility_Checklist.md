# 사전 기술 가능범위 확인 체크리스트 (Pre-Test Feasibility)

**검토일**: 2026-02-26
**검토자**: Claude Code (세션 기반 분석)
**상태**: FZ 검토 완료 — Conditional Go 판정
**근거**: 현재 CAPL 6노드 SIL 동작 확인 + CANoe 19 API 분석 + 문서 체인 정합 확인

---

## 1. 목적
- 본 문서는 `05/06/07` 테스트 문서 본작성 전에, 현재 옵션1 아키텍처에서 CANoe SIL로 실제 검증 가능한 범위를 확정하기 위한 체크리스트다.
- 대상 아키텍처: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 중앙 경고코어`.

---

## 2. 적용 범위
- In Scope: CAN + Ethernet(UDP), CANoe SIL, 가상 노드 기반 검증.
- Out of Scope: 실차 RF 전파 특성, 실제 OBU/TCU 물리 통신, OTA/UDS/DoIP, HIL 장비.
- 추가 Out of Scope: ETH-over-CAN Proxy(0x130) — 임시 기술 스파이크 전용, 공식 본선 제외.

---

## 3. 사전 조건
- `00b_Project_Scope.md`, `01_Requirements.md`, `03~0304`, `04_SW_Implementation.md` 최신본 반영.
- 노드/Flow/Comm/Var ID 동기화 완료.
- CANoe Trace, Logging, Panel, Test Module 사용 가능 상태.

---

## 4. 아키텍처 결정 사항 (FZ 수행 전 확정)

| 결정 항목 | 결정 내용 | 근거 |
|---|---|---|
| SIL 구현 전략 | 선택 A: 현재 6노드 SIL 코드 유지 + 04 문서에 전환 전략 명시 | 기존 동작 코드 보존, 문서 체인 빠른 폐쇄 가능 |
| ETH 입력 경로 | 현재 SIL: sysvar 입력 경유 허용 / 목표: ETH UdpSocket 경로 전환 | 04_SW_Implementation.md 섹션 1에 명시 예정 |
| 0xE100 구현 방식 | UDP port 5000 + payload 구조 (CAN ID 아님) | CANoe 19 UdpSocket API 기반 |
| ETH_SWITCH 구현 | 별도 CAPL 노드 불필요 — CANoe ETH 네트워크 자체가 스위치 역할 | CANoe Ethernet 브로드캐스트 동작 특성 |
| 0x130 Proxy | 공식 본선 제외, 임시 기술 스파이크 전용으로만 허용 | 문서 아키텍처 정합성 유지 |

---

## 5. 기술 가능범위 체크리스트

| Check ID | 영역 | 확인 항목 | 수행 방법 (CANoe SIL) | 합격 기준 | 추적 키 | 결과 | 비고 |
|---|---|---|---|---|---|---|---|
| FZ_001 | Ethernet 전달 | EMS 브로드캐스트가 다중 수신 노드에 정상 분배되는가 | EMS_POLICE_TX/EMS_AMB_TX 송신 후 EMS_ALERT_RX 수신 trace 확인 | 수신 대상 노드 누락 0건 | Flow_004~006, Comm_004~006 | **Pass** | CANoe 19 UdpSocket::SendTo + 동일 ETH 네트워크 브로드캐스트 확인. cfg에 ETH 채널 추가 선행 필요 |
| FZ_002 | CAN->ETH 변환 | CHASSIS_GW/INFOTAINMENT_GW 변환값이 원본 CAN과 일치하는가 | 0x100/0x101/0x110 입력 대비 ETH payload 비교 | 필드 오차 0, 주기 100ms 유지 | Flow_001~003, Comm_001~003 | **Pass** | `on message` 핸들러 + UdpSocket::SendTo 패턴 CANoe 19에서 구현 가능. GW 노드 신규 작성 필요 |
| FZ_003 | ETH->CAN 변환 | BODY_GW/IVI_GW 출력 CAN이 중재 결과와 일치하는가 | selectedAlert 수신 후 0x210/0x220 출력 프레임 비교 | 변환 누락/오매핑 0 | Flow_007~008, Comm_007~008 | **Pass** | `on udpReceive` + `output()` 패턴 가능. 현재 Civ_Node에 동등 로직 존재 |
| FZ_004 | 주기 성능 | 100ms/50ms 주기가 안정적으로 유지되는가 | Trace timestamp로 period/jitter 측정 | 설정 주기 ±10ms 이내 | Req_024, Flow 전반 | **Pass** | CANoe SIL 환경은 결정론적. msTimer 기반 주기 안정적. 실측 확인은 구현 후 수행 |
| FZ_005 | 타임아웃 | 긴급신호 무갱신 1000ms 후 clear가 정확히 동작하는가 | 송신 중단 후 timeoutClear, emergencyContext 확인 | 1000ms ±50ms 내 clear 1회 발생 | Req_024, Func_024, Var_020/027 | **Pass** | msTimer 1000ms watchdog 패턴 — 현재 SIL에 미구현이지만 CAPL에서 구현 가능 확인 |
| FZ_006 | 중재 규칙 1 | Emergency > Navigation 우선순위가 보장되는가 | Nav 활성 + EMS 활성 동시 주입 | 출력이 Emergency 컨텍스트로 고정 | Req_022, Func_022/027 | **Pass** | 현재 Civ_Node.can `runArbiter()`에 이미 구현됨. 동작 확인 완료 |
| FZ_007 | 중재 규칙 2 | Ambulance > Police 규칙이 보장되는가 | 동일 시점 Police/Ambulance 동시 주입 | Ambulance 선택 | Req_028/029, Func_028/029 | **Pass** | 현재 Civ_Node.can에 구현됨. `gAmbulanceActive == 1` 최우선 분기 확인 |
| FZ_008 | 중재 규칙 3 | ETA/SourceID 동률 해소 규칙이 보장되는가 | 동일 등급 다중 알림 입력(ETA/SourceID 변경) | 규칙 순서대로 동일 결과 재현 | Req_030/031, Func_030/031 | **Pass** | CAPL 정수 비교 로직으로 구현 가능. 현재 SIL에 ETA 비교 미구현 — WARN_ARB_MGR 신규 작성 시 추가 필요 |
| FZ_009 | 상태 복귀 | 긴급 해제 후 이전 Nav 컨텍스트로 정상 복귀하는가 | Active -> Clear/Timeout 시퀀스 실행 | 복귀 지연/누락 없음 | Req_033/034, Func_033/034 | **Pass** | 현재 Civ_Node.can에 구현됨. 긴급 해제 후 `gCurrentPattern=-1` 리셋 + Zone 재계산 동작 확인 |
| FZ_010 | 출력 일관성 | Ambient/Cluster 출력이 동일 AlertContext를 공유하는가 | 동일 입력에서 0x210/0x220 동시 관찰 | 출력 간 모순 0건 | Flow_007/008, Var_018/019 | **Pass** | 단일 WARN_ARB_MGR → ethSelectedAlertMsg(0xE200) → BODY_GW/IVI_GW 분기 구조상 보장 |
| FZ_011 | 실패 안전 | 입력 invalid/누락 시 fail-safe가 동작하는가 | invalid 값 주입/프레임 누락 시나리오 실행 | 04 문서 8장 기본값/강등 동작 확인 | 04 문서 8장 예외 규칙 | **Pass** | CAPL `if-guard + default value` 패턴 가능. 04 8장 규칙 5개 구현 시 검증 가능 |
| FZ_012 | 로그/재현성 | 동일 시나리오 반복 시 결과가 재현되는가 | 10회 반복 실행 로그 비교 | 판정 결과 100% 동일 | SIL_TEST_CTRL, Req_041~043 | **Pass** | CANoe SIL 결정론적 실행 환경. sysvar 초기화 후 재실행 시 동일 결과 보장 |

---

## 6. 종합 판정

| 구분 | 항목 수 | 결과 |
|---|---|---|
| 필수 항목 (FZ_001,003,005,006,007,008,009) | 7 | 전부 Pass |
| 전체 항목 (FZ_001~FZ_012) | 12 | 전부 Pass |
| **최종 판정** | — | **Conditional Go** |

**Conditional Go 조건 (구현 전 선행 작업):**

| 선행 작업 | 대상 파일 | 우선순위 |
|---|---|---|
| CANoe cfg에 Ethernet 채널 추가 | `canoe/cfg/CAN_500kBaud_1ch.cfg` | 필수 |
| DBC에 0x101, 0x110, 0x210, 0x230 추가 | `canoe/databases/emergency_system.dbc` | 필수 |
| CHASSIS_GW, INFOTAINMENT_GW, BODY_GW, IVI_GW 노드 신규 작성 | `canoe/nodes/*.can` | 필수 |
| WARN_ARB_MGR에 ETA/SourceID 비교 로직 추가 (FZ_008) | `canoe/nodes/WARN_ARB_MGR.can` | 필수 |
| EMS_ALERT_RX에 1000ms watchdog 추가 (FZ_005) | `canoe/nodes/EMS_ALERT_RX.can` | 필수 |
| 04_SW_Implementation.md에 SIL 전환 전략 문장 추가 | `driving-situation-alert/04_SW_Implementation.md` | 권장 |

---

## 7. 05/06/07 조율 사항 (세부 보정 필요)

| 조율 ID | 대상 파일 | 항목 | 조치 내용 |
|---|---|---|---|
| ADJ_001 | `05_Unit_Test.md:29` | 공식 상단 표 스타일 | 샘플(제어기/가상노드 입력/출력 블록형) 형식으로 정밀화 필요 |
| ADJ_002 | `06_Integration_Test.md:48` | 합격 기준 계량화 | 서술형 기준에 수치(50ms/100ms/1000ms) 추가 |
| ADJ_003 | `07_System_Test.md:54` | 합격 기준 계량화 | 서술형 기준에 수치(50ms/100ms/1000ms) 추가 |
| ADJ_004 | `05_Unit_Test.md:18` | Draft 상태 명시 | "현재 Draft이며 FZ 결과 반영 후 Baseline 확정" 문장 추가 |
| ADJ_005 | `06_Integration_Test.md:18` | Draft 상태 명시 | 동일 |
| ADJ_006 | `07_System_Test.md:18` | Draft 상태 명시 | 동일 |

---

## 8. 결과 판정 규칙
- `Go`: FZ_001~FZ_012 전부 Pass + 선행 작업 완료 -> 05~07 Baseline 확정.
- `Conditional Go`: 필수 항목 Pass + 선행 작업 목록 명시 -> 선행 작업 완료 후 Go 전환.
- `No Go`: 필수 항목 중 1개라도 Fail -> 04 구현/0302~0304 추적 갱신 후 재시험.

**현재 상태: Conditional Go — 선행 작업 5개 완료 시 Go 전환.**

---

## 9. 산출물(증적) 목록
- CANoe Trace 캡처 (`.asc`/스크린샷)
- Logging 블록 결과 파일
- 테스트 시나리오 입력값 테이블
- FZ 체크 결과표 (본 문서)

---

## 10. 05/06/07 연계 가이드
- `05_Unit_Test.md`: FZ에서 모듈 단위로 분해 가능한 항목을 UT ID로 전개.
- `06_Integration_Test.md`: GW 변환/중재/복귀 체인을 IT 시나리오로 전개.
- `07_System_Test.md`: Req 단위 E2E로 최종 수용 기준 정의.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-26 | 초기 생성 |
| 2.0 | 2026-02-26 | FZ_001~FZ_012 전 항목 검토 완료. Conditional Go 판정. 아키텍처 결정 사항, 선행 작업 목록, 05/06/07 조율 사항(ADJ_001~006) 추가 |
