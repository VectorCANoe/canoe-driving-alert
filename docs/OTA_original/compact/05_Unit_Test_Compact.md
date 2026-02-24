# 단위 테스트 (Compact Version)

> 이 문서는 `Project_Result_Sample.xlsx` 형식(05_Unit Test)에 맞추어 현업 실무진 및 아키텍처 전문가 보고용으로 극히 간략화된 버전입니다.

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|----|----|--------|-----------|-----------|--------|------|
| 제어기 | 제어 | WDM_ECU | [Level 3] 충돌 감지(gCrashEvent=1) 버튼 클릭 시, 0x200 캔 메시지의 WDM 위험등급 신호가 3으로 변경 | Pass | 준영 | 26.02.24 |
| 제어기 | 모니터 | WDM_ECU | [과속 판단] 스쿨존(gRoadZone=1) 시 30km/h 초과 시 과속 경고 플래그 생성 확인 | Pass | 준영 | 26.02.24 |
| 출력기 | 앰비언트 | Ambient_ECU | 위험 3단계 등급 수신 시 즉각적인 200ms RED 점멸 패턴 정상 출력 확인 | Pass | 준영 | 26.02.24 |
| 가상노드 | 통신 | OTA_Server | P 기어 주차 조건에서 IVI 동의 시, 0x10, 0x27, 0x34 연쇄 UDS 세션 정상 수립 확인 | Pass | 성현 | 26.02.24 |
| 외부 | 모니터 | Smart_Claim | Python COM API 호출 시 Flask 로컬 서버로 JSON 모의사고 데이터 200 OK 전송 확인 | Pass | 성현 | 26.02.24 |
| 출력기 | 인프라 | IVI_ECU | OTA 다운로드 중 o_OTA_Progress 변수에 맞추어 UI 프로그레스바 증가 확인 | Pass | 성현 | 26.02.24 |
