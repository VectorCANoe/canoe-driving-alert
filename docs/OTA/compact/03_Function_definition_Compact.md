# 기능 정의서 (Compact Version)

> 이 문서는 `Project_Result_Sample.xlsx` 형식(03_Function definition)에 맞추어 현업 실무진 및 아키텍처 전문가 보고용으로 극히 간략화된 버전입니다.

| 가상노드 Simulator | 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|--------------------|------|--------|----------|------|------|
| WDM_ECU | 제어 | 위험 상황 판단 | 입력된 차량 동역학/구간 데이터를 바탕으로 위험 단계(1~3)를 판단하고 경고 플래그 생성 | 핵심 로직 | Pass |
| WDM_ECU | 제어 | 구간 임계값 변경 | 앰비언트 구간(일반/스쿨/고속/IC)에 맞춰 과속 판단 기준 속도를 동적 변경 | 준영 | Pass |
| Vehicle_ECU | 입력 | 차량 동역학 주입 | 가속도, 브레이크값, 속도 등을 Panel 값을 통해 100ms 주기로 CAN 전송 | 인프라 | Pass |
| LDW / MDPS_ECU | 입력 | 조향/차선 제어 | 차선 이탈 신호, 핸들 조향 여부 100ms 파악 후 WDM 전달 | 인프라 | Pass |
| Sound_ECU | 출력 | Auditory 경고 | 위험 단계 정보(Level 1~3) 수신 시 등급에 맞는 경고음 발생 | 인프라 | Pass |
| Cluster_ECU | 출력 | Visual 계기판 알림 | 위험 단계 발생 시 대시보드 경고등 및 HUD 텍스트 점등 | 인프라 | Pass |
| Ambient_ECU | 출력 | Visual 앰비언트 | 주행 구간 진입 시 및 충돌 경고 시 애니메이션 조명 효과(RED 점멸 등) 출력 | 준영 | Pass |
| IVI_ECU | 출력/입력| HMI 스토어 UI | 테마/Drive Coach 패키지 다운로드 사용자 동의 수집 및 OTA 진행률 표시 | 성현 | Pass |
| OTA_Server | 인프라 | UDS 세션 제어 | Drive Coach / 시즌 테마 다운로드 패키지를 UDS 프로토콜로 IVI에 전송 | 성현 | Pass |
| Python (COM API) | 외부 | Smart Claim | Level 3 발생 시 CANoe 내부 EDR 데이터를 외부 보험용 Flask 서버로 POST 전송 | 성현 | Pass |
