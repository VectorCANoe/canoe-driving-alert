# AGENTS.md

## Scope
- This file applies to work under `driving-alert-workproducts/`.
- For general repository rules, also follow the root `AGENTS.md`.
- For paper-writing tasks, this file is the local guardrail source of truth.

## Paper Draft Target
- Primary target:
  - `driving-alert-workproducts/governance/00h_Conference_Paper_Draft.md`
- When editing this paper, do not treat it as a product brochure, marketing copy, or project diary.
- Treat it as a short academic-style conference paper draft written in Korean.

## Paper Positioning
- The paper must be framed as:
  - `현대 차량 시스템 적용을 가정한 주행 경고 신기능 컨셉의 설계·구현·시험 사례`
- Do not frame it as:
  - `차량 전체 시스템을 완전 설계·검증한 연구`
  - `양산 수준 검증을 완료한 결과`
  - `완전한 제품 개발 종료 보고`
- The safe and preferred framing is:
  - `현대 차량 시스템을 벤치마킹한 기본 ECU 구성과 핵심 서비스 경로를 바탕으로, 구간 정보와 긴급차량 접근을 통합하는 경고 컨셉을 CANoe SIL에서 구현하고 시험한 사례`

## Non-Negotiable Facts
- The project benchmarked a Hyundai vehicle-system-style baseline ECU composition and key service paths.
- Official implementation and verification scope is fixed to:
  - `CANoe SIL`
  - `CAN + Ethernet`
- This communication scope limitation must be explained briefly as:
  - `license and verification scope constraint`
- CAPL-based logical ECU implementation and Validation Harness are central implementation elements.
- Traceability must be described as:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- HARA and Master Test Matrix may be referenced as management and traceability artifacts.

## Writing Intent
- The title and abstract must be:
  - easy to read
  - technically credible
  - interesting without exaggeration
  - sufficient to let a reader grasp the whole flow and outcome quickly
- The paper must read as:
  - a sober technical case study
  - not a claim-heavy system-completion paper

## Reference Direction
- Use the following reference direction when the paper tone or structure is ambiguous:
  - Hyundai Motor Group academic presentation style:
    - idea -> technical implementation -> practical value
    - source direction:
      - `https://www.hyundaimotorgroup.com/ko/story/CONT0000000000197008`
      - `https://www.hyundaimotorgroup.com/ko/news/CONT0000000000177931`
  - Domestic engineering paper structure:
    - title / abstract / introduction / body / results / conclusion
    - abstract as one independent paragraph
    - introduction built as background -> observed problem -> objective
    - source direction:
      - `https://knom.or.kr/knom-review/regulations/submission.html`
      - `https://dev.recbt.kr/theme/recbt/html/journal/02.php`

## Preferred Structure
- Keep the paper structure close to the following:
  1. 제목
  2. 국문 초록
  3. 핵심어
  4. 서론
  5. 연구 범위와 목표
  6. 시스템 설계
  7. 구현 및 검증 구성
  8. 결과 및 고찰
  9. 결론 및 제언
- The introduction should follow:
  - `문제 배경`
  - `문제 사례 관찰`
  - `연구 목적`
- The paper narrative should follow:
  - `문제점 관찰 -> 문제 사례 관찰 -> 목표와 아이디어 -> 설계 구조 및 기능 -> 구현/시험 -> 결과 -> 기대효과 및 제언`

## Title Rules
- Keep the title concrete and compact.
- The title should state:
  - what the concept is
  - that it was implemented/tested in CANoe SIL
- Prefer:
  - `... 컨셉`
  - `... 구현 및 시험 사례`
  - `CANoe SIL 기반`
- Avoid stacking too many similar nouns such as:
  - `신기능`, `컨셉`, `기반`, `시스템`
  in one line unless all are necessary.
- Avoid inflated title patterns such as:
  - `차량 시스템의 완전한 설계 및 검증`
  - `양산형 시스템 개발 및 실차 검증`

## Abstract Rules
- The abstract must be one compact paragraph.
- The abstract must quickly answer:
  - why this topic was selected
  - what was implemented
  - what boundary conditions were used
  - what method or structure was used
  - what was actually obtained
- Preferred abstract flow:
  - problem
  - reason for selecting the concept
  - implementation scope
  - method
  - result
- Keep limitations or remaining stabilization items out of the abstract when possible.
- Put detailed limitations and follow-up work in the later `결론 및 제언` section instead.

## Tone Rules
- Tone must be:
  - factual
  - plain
  - reviewer-facing
  - technically grounded
- Prefer short, direct Korean sentences.
- Prefer phrases such as:
  - `정리하였다`
  - `구성하였다`
  - `구현하였다`
  - `시험하였다`
  - `기준선을 마련하였다`
  - `연결하였다`
- Avoid overclaiming phrases such as:
  - `완전하게 검증하였다`
  - `양산 수준으로 확보하였다`
  - `모든 문제를 해결하였다`
  - `실차 수준으로 재현하였다`

## Content Guardrails
- Do not over-focus on the TUI, operator console, or product UI.
- Do not present the paper as a tooling paper.
- The core value is:
  - the warning concept
  - mixed CAN/Ethernet path handling
  - logical ECU structure
  - traceability-backed test organization
- It is acceptable to say:
  - baseline ECU composition and service paths were benchmarked from Hyundai vehicle-system context
- It is not acceptable to say:
  - the entire Hyundai vehicle system was fully reproduced and validated

## Evidence Base
- When writing or revising the paper, preferentially ground claims in:
  - `driving-alert-workproducts/01_Requirements.md`
  - `driving-alert-workproducts/03_Function_definition.md`
  - `driving-alert-workproducts/0301_SysFuncAnalysis.md`
  - `driving-alert-workproducts/0302_NWflowDef.md`
  - `driving-alert-workproducts/0303_Communication_Specification.md`
  - `driving-alert-workproducts/0304_System_Variables.md`
  - `driving-alert-workproducts/04_SW_Implementation.md`
  - `driving-alert-workproducts/05_Unit_Test.md`
  - `driving-alert-workproducts/06_Integration_Test.md`
  - `driving-alert-workproducts/07_System_Test.md`
  - `driving-alert-workproducts/governance/00d_HARA_Worksheet.md`
  - `driving-alert-workproducts/governance/00g_Master_Test_Matrix.md`

## Preferred Current Framing
- Current preferred paper framing:
  - `구간 정보와 긴급차량 접근을 통합한 실시간 주행 경고 컨셉`
- Current preferred title direction:
  - `구간 정보와 긴급차량 접근을 통합한 실시간 주행 경고 컨셉: CANoe SIL 기반 구현 및 시험 사례`
- If a future AI proposes a broader or more promotional framing, reject it and return to this direction.

## Editing Discipline
- Before revising the paper, read:
  - `driving-alert-workproducts/governance/00h_Conference_Paper_Draft.md`
  - this file
- If revising title/abstract:
  - review only title, abstract, keywords, and introduction opening first
  - do not rewrite the whole paper unless explicitly requested
- If adding claims:
  - make sure the same claim can be grounded in local docs
- If unsure:
  - choose the less dramatic wording
  - preserve factual restraint
