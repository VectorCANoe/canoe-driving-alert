# Diagnostic Description

원문:
- [../../contracts/diagnostic-description.md](../../contracts/diagnostic-description.md)

동기화 기준:
- `5d83ee7f`
- `Diag::*` namespace, request/response field 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 CANoe SIL baseline에서 현재 사용 중인 diagnostic model을 설명합니다.
> runtime, diagnostic, verification 구현이 계속 고정되는 단계이므로 일부 내용은 바뀔 수 있습니다.

## 목적

이 문서는 현재 CANoe SIL baseline이 어떤 diagnostic model을 사용하고 있는지 설명합니다.

## 범위

다음 내용을 포함합니다.

- diagnostic request와 response를 어떻게 관찰하는지
- runtime, panel, tool에 어떤 diagnostic summary seam을 노출하는지
- evidence 친화적인 diagnostic field를 어떻게 유지하는지
- 향후 어떤 방향으로 확장할 수 있는지

## 현재 diagnostic model

현재 active baseline은 완전한 standalone diagnostic stack 설명보다는, observation과 evidence에 중심을 둔 lightweight diagnostic surface를 사용합니다.

현재 model은 다음 네 축으로 구성됩니다.

- 시스템에 어떤 request가 들어왔는지 기록하는 request-side capture
- runtime이 어떤 response를 반환했는지 기록하는 response-side capture
- verdict와 evidence workflow를 위해 정리된 summary field
- 반복 검증과 debug 지원을 위한 counter와 timestamp

## Diagnostic layer

| Layer | 역할 | 주요 출력 |
| --- | --- | --- |
| Request observation | service intent와 request metadata를 기록 | request identifier, service type, bus/context |
| Response observation | status, payload summary, timing result를 기록 | response code, response summary, timing field |
| Runtime summary | panel, tool, verification에서 diagnostic state를 읽을 수 있게 노출 | `Diag::*` SysVars |
| Evidence support | screenshot, log, verification record를 뒷받침 | summary field, counter, timestamp |

## 현재 source chain

- `contracts/diagnostic-sysvar-contract.md`
- `verification/execution-guide.md`
- `verification/evidence-policy.md`

## 설계 규칙

- diagnostic observation은 명시적이고 읽기 쉬워야 합니다
- panel-facing variable에 raw transport payload detail을 그대로 얹지 않습니다
- implementation detail이 바뀌어도 evidence-friendly summary field는 안정적으로 유지합니다
- active baseline에 실제로 필요할 때만 protocol-specific depth를 추가합니다

## 개발 메모

이 문서는 frozen final protocol specification이 아니라, 현재 development description입니다.

프로젝트가 native diagnostic coverage를 더 확장하면 transport detail과 ownership depth도 함께 확장될 수 있습니다.
