# ECU Flow Appendix 한글 가이드

원문:
- [../../architecture/ecu-flow-appendix.md](../../architecture/ecu-flow-appendix.md)

## 목적

이 문서는 active CANoe SIL baseline의 `101`개 ECU를 기준으로 ECU별 네트워크 흐름을 한 표에서 읽기 위한 appendix 안내본입니다.

핵심 질문:
- 어떤 ECU가 어떤 contract를 publish하는가
- 어떤 contract를 consume하는가
- 직접 연결되는 ECU가 누구인가
- 그 ECU에 direct native test anchor가 이미 있는가

## 읽는 법

- `Published contracts`
  - 현재 executable baseline에서 그 ECU가 outbound로 내보내는 active message contract입니다.
- `Consumed contracts`
  - split DBC에서 해당 ECU가 receiver로 나타나는 inbound contract입니다.
- `Linked ECUs`
  - 같은 contract에서 직접 sender/receiver로 연결되는 이웃 ECU입니다.
- `Direct native test anchors`
  - 현재 native asset ID에 ECU명이 직접 들어가는 direct anchor 목록입니다.
  - 간접 커버리지 전체를 의미하지는 않습니다.

## 운영 규칙

- reviewer-facing appendix는 원문을 기준으로 사용합니다.
- 재생성은 아래 명령으로 수행합니다.
  - `python canoe/tools/20_VERIFICATION/20_build_ecu_flow_appendix.py`
- 임시 메모나 작업 가설은 `canoe/docs/**`에 두지 않고 내부 작업 문서에 유지합니다.

## 사용 위치

- CANoe-side reviewer appendix 초안
- ECU별 연계 누락, direct test gap, semantic-only node 식별
- 이후 `driving-alert-workproducts` appendix 및 `tex` 변환의 원천 표
