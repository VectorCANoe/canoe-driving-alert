> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# Architecture Optimization Review (SIL Scope)

## 1. 목적
- 현재 채택 아키텍처(Option 1)가 프로젝트 요구사항과 검증 범위에 최적인지 점검한다.
- 대안 아키텍처를 비교하고, 적용 시점(지금/차기)을 명확히 정의한다.

## 2. 평가 기준
| 기준 ID | 평가 항목 | 기준 설명 |
|---|---|---|
| AC_01 | 요구사항 충족성 | `Req_001~Req_043`를 누락 없이 구현/검증 가능한가 |
| AC_02 | 추적성 유지성 | `Req->Func->Flow->Comm->Var->Code->UT/IT/ST` 체인 유지 용이성 |
| AC_03 | SIL 구현 난이도 | CANoe SIL에서 구현/디버깅/재현이 가능한 수준인가 |
| AC_04 | 확장성 | HIL/실차 이전에 확장 가능한 구조인가 |
| AC_05 | 장애 허용성 | 단일 노드/링크 오류 시 영향 격리가 가능한가 |

## 3. 대안 비교
| 옵션 | 구성 | AC_01 | AC_02 | AC_03 | AC_04 | AC_05 | 판정 |
|---|---|---|---|---|---|---|---|
| Option 1 (현재) | ETH_SWITCH + Domain GW + Domain CAN + 중앙 경고코어 | 높음 | 높음 | 중간 | 높음 | 중간 | 채택 유지 |
| Option 1A (고도화) | Option 1 + 이중 ETH 백본 + 이중화 GW | 높음 | 높음 | 낮음 | 매우 높음 | 높음 | 차기 후보 |
| Option 1B (SOA 강화) | Option 1 + 서비스 인터페이스 레이어(SOME/IP 계열) | 높음 | 중간 | 낮음 | 높음 | 중간 | 현 단계 과설계 |
| Option 2 | 도메인 CAN 직접 연계 중심 | 중간 | 중간 | 높음 | 낮음 | 낮음 | 미채택 |
| Option 3 | 중앙 단일 CAN 백본 | 중간 | 낮음 | 높음 | 낮음 | 낮음 | 미채택 |

## 4. 결론
- 현재 프로젝트 범위(CANoe SIL, CAN+Ethernet, 문서 추적성 기준)에서는 **Option 1이 최적안**이다.
- Option 1A는 장애 허용성 측면에서 우수하지만, 현재 단계에서는 구현 복잡도 대비 실익이 낮다.
- Option 1B는 서비스 계층 설계 비용이 커서 본 프로젝트 기간/범위에서는 비권장이다.

## 5. 권장 적용 순서
1. `00~07` 문서 체인을 Option 1 기준으로 고정 유지한다.
2. CANoe 구현에서 sysvar 경로를 단계적으로 ETH `UdpSocket` 경로로 치환한다.
3. 차기 단계(HIL/실차 이전)에서만 Option 1A 이중화 항목을 추가 검토한다.

## 6. 추적 링크
- 요구사항: `driving-situation-alert/01_Requirements.md`
- 기능/흐름/통신/변수: `driving-situation-alert/03_Function_definition.md`, `driving-situation-alert/0301_SysFuncAnalysis.md`, `driving-situation-alert/0302_NWflowDef.md`, `driving-situation-alert/0303_Communication_Specification.md`, `driving-situation-alert/0304_System_Variables.md`
- 구현: `driving-situation-alert/04_SW_Implementation.md`
- 검증: `driving-situation-alert/05_Unit_Test.md`, `driving-situation-alert/06_Integration_Test.md`, `driving-situation-alert/07_System_Test.md`
