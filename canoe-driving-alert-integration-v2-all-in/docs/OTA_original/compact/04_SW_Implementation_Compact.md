# SW 구현서 (Compact Version)

> 이 문서는 `Project_Result_Sample.xlsx` 형식(04_System implementation)에 맞추어 현업 실무진 및 아키텍처 전문가 보고용으로 극히 간략화된 버전입니다.

| 구분 | 개발 언어 | 모듈명 | 상태 | 주요 구현 알고리즘 핵심 요약 |
|------|-----------|--------|------|------------------------------|
| CAPL | CAPL | WDM 로직 구현 | 완료 | 동역학 신호 수집 및 우선순위에 따른 Level 1~3 산출 / 2초 타이머 소거 자동화 |
| CAPL | CAPL | 구간 인식 제어 | 완료 | 일반/스쿨/고속/IC 구간 별 임계값 가변화 및 패턴 로직(RED점멸, 컬러파동) 구현 |
| CAPL | CAPL | UDS 통신 엔진 | 완료 | DoIP 기반의 0x10, 0x27, 0x34, 0x36 연속 세션 흐름도 및 다운로드 에러(Fail-safe) 핸들링 |
| Python| Python | Smart Claim | 완료 | COM API를 활용, Level 3 사고 감지 시 시뮬레이션 환경 내 EDR 변수를 Flask 웹서버로 전송하는 모의 텔레매틱스 파이프라인 |
| Python| Python | Flask 대시보드 | 완료 | JSON 페이로드 수신 후 `[접수번호 001] 속도 85km/h 완료` 등 사내 브라우저 기반 HTML 모니터링 데모 제공 |
