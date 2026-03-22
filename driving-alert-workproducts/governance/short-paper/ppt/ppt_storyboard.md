# PPT 발표 구성안

## 1. 발표 목표

이번 발표의 목적은 특정 계산식 하나를 깊게 설명하는 데 있지 않다.
주행 경고 컨셉을 어떻게 정의했고, 어떤 문서 체계와 ECU 구조를 세웠으며, 이를 어떻게 구현·시험·운영 가능한 기준선으로 만들었는지를 전체 프로세스 관점에서 전달하는 데 목적이 있다.

핵심 메시지는 다음과 같다.

1. 본 프로젝트는 구간 정보, 긴급차량 접근, 객체 위험을 하나의 경고 정책으로 통합하는 컨셉을 정의하였다.
2. 이 컨셉은 문서, CAPL ECU, 시험 자산, 운영 자동화까지 이어지는 하나의 기준선으로 구체화되었다.
3. 그 결과 경고 설계, 구현, 시험, 운영이 분리되지 않고 같은 추적 구조 안에서 설명 가능한 상태가 되었다.

## 2. 권장 발표 길이

- 메인 발표: 12~14장
- 질의 대응용 백업: 4~6장

## 3. 권장 큰 흐름

1. 왜 이 프로젝트를 시작했는가
2. 무엇을 핵심 컨셉으로 정했는가
3. 어떤 문서와 구조로 정리했는가
4. 어떤 ECU/네트워크 구조로 구현했는가
5. 어떤 시험 체계를 만들었는가
6. 운영과 자동화까지 무엇을 구축했는가
7. 무엇을 배웠고, 어디로 확장할 것인가

## 4. 메인 슬라이드 구성

### Slide 1. Title

- 목적: 발표 주제와 범위를 한 장에서 고정
- 핵심 메시지:
  - `주행 상황 실시간 경고 시스템`
  - `구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보`
  - `설계, 구현, 시험, 운영 자동화 경험`
- 권장 시각자료:
  - 대표 패널 또는 시스템 구조 썸네일 1장

### Slide 2. 왜 이 프로젝트를 시작했는가

- 목적: 문제의식 제시
- 핵심 메시지:
  - 차량 경고는 구간 정보, 긴급차량 접근, 객체 위험이 동시에 들어오면 쉽게 충돌한다.
  - 문제는 경고를 많이 만드는 것이 아니라, 여러 입력을 하나의 경고 정책으로 해석하는 구조가 없다는 데 있다.
- 근거 문서:
  - `00_Project_Overview.md`
  - `paper/short_paper_draft.md`
- 권장 시각자료:
  - 스쿨존, 긴급차량, 교차로 위험이 동시에 겹치는 개념도 1장

### Slide 3. 우리가 선택한 핵심 컨셉

- 목적: 발표의 중심 컨셉을 한 장에서 고정
- 핵심 메시지:
  - 스쿨존·고속도로·유도선 구간 경고
  - 긴급차량 접근 경고
  - 교차로·합류구간 충돌위험 경고
  - 위 세 축을 하나의 경고 정책으로 통합하였다.
- 근거 문서:
  - `01_Requirements.md`
  - `03_Function_definition.md`
  - `00_Project_Overview.md`
- 권장 시각자료:
  - 세 입력 축이 하나의 경고 정책으로 수렴하는 컨셉 그림

### Slide 4. 프로젝트 전체 프로세스

- 목적: 논문보다 넓은 범위에서 전체 수행 흐름을 보여줌
- 핵심 메시지:
  - 프로젝트는 단일 기능 구현이 아니라 `요구사항 -> 기능 정의 -> 네트워크/변수 설계 -> 구현 -> 시험 -> 운영 자동화` 흐름으로 진행되었다.
  - 문서와 구현, 시험 자산을 동시에 정리한 것이 핵심 경험이었다.
- 근거 문서:
  - `00_Project_Overview.md`
  - `governance/00d_HARA_Worksheet.md`
  - `governance/00g_Master_Test_Matrix.md`
- 권장 시각자료:
  - `00~07 + governance + product console`이 이어지는 프로세스 맵

### Slide 5. 문서 체계와 추적 구조

- 목적: OEM/학술 발표에서 설득력이 생기는 근거 체계 제시
- 핵심 메시지:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> 단위시험/통합시험/시스템시험`
  - HARA, Test Oracle, Test Matrix를 통해 ISO 26262 추적성과 V-cycle 검증 구조를 유지하였다.
- 근거 문서:
  - `governance/00d_HARA_Worksheet.md`
  - `governance/00g_Master_Test_Matrix.md`
  - `05_Unit_Test.md`
  - `06_Integration_Test.md`
  - `07_System_Test.md`
- 권장 시각자료:
  - 추적성 체인 도식
  - HARA-시험 연결 표 일부 캡처

### Slide 6. 시스템 아키텍처

- 목적: 어떤 ECU 구조 위에서 컨셉을 구현했는지 설명
- 핵심 메시지:
  - 입력 수집 계층, 판단 계층, 출력 계층, 검증 계층을 분리하였다.
  - `V2X`, `ADAS`, `CGW`, `IVI`, `CLU`, `HUD`, `BCM`, `AMP`, `VALIDATION_HARNESS`가 핵심 축이다.
- 근거 문서:
  - `04_SW_Implementation.md`
  - `03_Function_definition.md`
- 권장 시각자료:
  - ECU 블록도
  - 패널/출력 채널 관계 요약도

### Slide 7. 네트워크 흐름

- 목적: CAN과 Ethernet을 어떻게 역할 분리했는지 설명
- 핵심 메시지:
  - CAN은 차량 상태와 구간 맥락 수집에 사용하였다.
  - Ethernet은 긴급 이벤트 전달과 경고 연계 경로로 사용하였다.
  - 운영 경로와 검증 관측 경로를 함께 설계하였다.
- 근거 문서:
  - `0302_NWflowDef.md`
  - `0303_Communication_Specification.md`
  - `canoe/docs/contracts/communication-matrix.md`
- 권장 시각자료:
  - CAN/Ethernet 혼합 흐름도

### Slide 8. V2X 핵심 로직

- 목적: 외부 이벤트 정규화 로직 설명
- 핵심 메시지:
  - V2X는 긴급차량 유형, ETA, SourceID를 기준으로 활성 이벤트를 정규화한다.
  - timeout clear로 이벤트 유효 상태를 관리한다.
- 근거 문서:
  - `paper/short_paper_draft.md`
  - `0304_System_Variables.md`
  - `canoe/src/capl/logic/V2X.can`
- 권장 시각자료:
  - V2X 상태도
  - 수식 또는 의사결정 규칙 1개

### Slide 9. ADAS 핵심 로직

- 목적: 위험도 산정과 경고 중재 설명
- 핵심 메시지:
  - ADAS는 긴급 접근 정보와 TTC 기반 객체 위험을 결합해 최종 경고와 감속 보조 요청을 결정한다.
  - on/off 안정화, timeout clear, fail-safe로 경고 전환과 복귀 일관성을 유지한다.
- 근거 문서:
  - `paper/short_paper_draft.md`
  - `0304_System_Variables.md`
  - `canoe/src/capl/logic/ADAS.can`
- 권장 시각자료:
  - ADAS 블록도
  - `R_emg`, `TTC`, `R_obj` 식 요약

### Slide 10. 구현 경험

- 목적: 실제로 무엇을 구현했는지 보여줌
- 핵심 메시지:
  - CAPL 기반 논리 ECU와 검증 하네스를 통해 경고 컨셉을 실행 가능한 구조로 옮겼다.
  - 패널, Diagnostic Console, Validation Harness를 통해 출력과 관측을 동시에 확인할 수 있게 했다.
- 근거 문서:
  - `04_SW_Implementation.md`
  - `paper/short_paper_draft.md`
- 권장 시각자료:
  - 대표 CANoe 패널 캡처
  - Diagnostic Console 캡처

### Slide 11. 시험 체계 경험

- 목적: 무엇을 어떻게 검증 대상으로 묶었는지 보여줌
- 핵심 메시지:
  - 단위시험은 규칙 확인, 통합시험은 경고 중재, 시스템시험은 연속 시나리오와 복귀 안정성을 다룬다.
  - 구간 경고, 긴급차량 우선순위 판단, timeout clear, 교차로·합류구간 위험을 핵심 시나리오로 고정하였다.
- 근거 문서:
  - `05_Unit_Test.md`
  - `06_Integration_Test.md`
  - `07_System_Test.md`
  - `governance/00g_Master_Test_Matrix.md`
- 권장 시각자료:
  - 대표 시험 시나리오 표
  - CANoe Test Unit 실행 화면

### Slide 12. 운영 자동화 경험

- 목적: 제품 스코프와 운영 경험을 별도 가치로 보여줌
- 핵심 메시지:
  - 경고 컨셉과 시험 자산을 운영 가능한 콘솔 구조로 연결하였다.
  - 결과 확인, 문서 closeout, appendix bundle, 엑셀 산출까지 운영 워크스페이스를 구축하였다.
- 근거 문서:
  - `product/sdv_operator/`
  - `governance/short-paper/appendix/`
  - `excel/submission_final_all_in_one.xlsx`
- 권장 시각자료:
  - TUI 홈/결과/아티팩트 화면
  - appendix bundle 또는 엑셀 산출 캡처

### Slide 13. 현재까지 도출된 결과

- 목적: 성능 과장 없이 현재 성과를 정리
- 핵심 메시지:
  - 경고 컨셉, 시험 기준, 운영 체계가 하나의 기준선으로 연결되었다.
  - V2X 선택 정확도, 교차로·합류 통합 경고 성공률, 복귀 안정성 준수율의 세 지표로 결과를 해석할 수 있는 구조를 확보하였다.
- 근거 문서:
  - `paper/short_paper_draft.md`
  - `paper/short_paper_manuscript.tex`
- 권장 시각자료:
  - 정량 지표 placeholder 표
  - 대표 실행 화면

### Slide 14. 우리가 실제로 배운 점

- 목적: 발표의 경험 가치 정리
- 핵심 메시지:
  - 핵심은 기능 추가가 아니라, 여러 입력을 하나의 경고 정책으로 정리하는 구조였다.
  - 설계, 구현, 시험, 운영 자동화는 따로가 아니라 같은 추적 구조 안에서 관리되어야 했다.
  - CAN과 Ethernet 혼합 경로에서는 기능 경로와 관측 경로를 함께 설계해야 했다.
- 권장 시각자료:
  - Lessons learned 3-box 요약

### Slide 15. 결론 및 다음 단계

- 목적: 발표 마무리
- 핵심 메시지:
  - 본 프로젝트는 주행 경고 컨셉을 문서, 구현, 시험, 운영 기준선으로 연결한 사례이다.
  - 다음 단계는 시험 기준 안정화, 정량 결과 확정, 협력인지·SPaT/MAP·군집 이벤트 공유 같은 확장형 V2X 주제로 이어진다.
- 권장 시각자료:
  - 로드맵 1장

## 5. 백업 슬라이드 권장안

### Backup A. HARA와 Test Matrix 연결

- 목적: 질의 대응
- 내용:
  - HARA 항목이 어떻게 시험 시나리오로 내려오는지

### Backup B. 대표 패널 설명

- 목적: 패널 질문 대응
- 내용:
  - Ambient / Cluster / Navigation / Diagnostic Console

### Backup C. 대표 CAPL 로직

- 목적: 구현 질문 대응
- 내용:
  - V2X 선택 규칙
  - ADAS TTC 및 위험도 식

### Backup D. Appendix Bundle 구성

- 목적: 문서 관리 질문 대응
- 내용:
  - supplementary appendix bundle
  - core contract set

## 6. 시각자료 우선순위

1. 시스템 아키텍처 블록도
2. CAN/Ethernet 흐름도
3. V2X 상태도
4. ADAS 블록도
5. CANoe 실행 화면
6. 패널 또는 Diagnostic Console
7. TUI 운영 콘솔
8. Appendix/Excel 산출물

## 7. 발표 톤 원칙

- 소논문보다 넓은 범위를 다루되, 기술 홍보문처럼 과장하지 않는다.
- 슬라이드는 `우리가 무엇을 경험했고 무엇을 구축했는가`를 먼저 전달한다.
- 긴 문단보다 짧은 메시지와 큰 그림을 우선한다.
- 계산식은 핵심 한두 개만 두고, 나머지는 백업 슬라이드로 보낸다.

## 참고

  - MIT Mechanical Engineering Communication Lab: 한 슬라이드는 한 메시지만 가져야 하고, 텍스트보다
    시각 자료가 우선이며, 제목 자체가 메시지를 말해야 함.
    https://mitcommlab.mit.edu/meche/commkit/technical-presentation/
  - MIT PowerPoint tips: 1–2 slides/min, 1–3 points/slide, 키워드 중심, 텍스트 최소화.

  https://ocw.mit.edu/courses/21w-035-science-writing-and-new-media-communicating-science-to-the-public-fall-2016/68f91d169741f8b142aec4ab278718dd_MIT21W_035F16_PowerPointTips.pdf
  - CIRS oral presentation guideline: 문제, 목표, 방법, 결과, 결론을 명확히 하고, 텍스트보다 figure를
    우선.
    https://cirs.cinec.edu/index.php/oral-and-poster-guidelines/
  - USC Viterbi oral presentation guideline: 산업/사회적 의미를 분명히 넣는 것이 좋음.
    https://bme.usc.edu/grodins-25/students/grodins-students-oral-presentation-guide/