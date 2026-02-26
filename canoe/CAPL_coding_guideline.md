# CAPL Coding Guideline (CANoe SIL)

이 문서는 `canoe/` 작업 시 AI/개발자가 동일하게 따라야 하는 코딩 기준입니다.
현재 Option1 아키텍처(FZ_00~07) 기준으로 정리합니다.

## 0) 우선 적용 규칙 (프로젝트 고정)
- 작업 범위: `canoe/` 폴더만 수정
- 통신 범위: CAN + Ethernet(UDP)만 사용
- ETH 포트: **5000 고정**
- ETH 프레임: **실제 UdpSocket 사용**, sysvar 경유 금지
  - 대상: `0x510`, `0x511`, `0x512`, `E100`, `E200`
- `BODY_GW`, `IVI_GW`: **udpReceive(5000) -> CAN 송신** (sysvar 브리지 금지)

## 1) 메시지 페이로드 규격 (고정)
- `E100` DLC=4
  - `b0 = (type | (dir << 2))`
  - `b1 = eta`
  - `b2 = sourceId`
  - `b3 = alertState`
- `E200` DLC=2
  - `b0 = (alertLevel | (alertType << 3))`
  - `b1 = timeoutClear`

## 2) sysvar 사용 원칙
- 허용: Panel I/O, 내부 상태 저장, 디버그/모니터링
- 금지: ETH 전송/수신 데이터 경유 채널로 사용
- CAN<->sysvar 게이트웨이 노드에서만 브리지 사용

## 3) CAPL 문법/스타일 규칙
- `variables {}`: 전역 선언만
- 이벤트 핸들러 내부 지역변수는 선언/대입 분리
- 배열 초기화는 `on start`에서 수행
- 타이머 재주기는 `on timer` 마지막에 `setTimer()` 호출
- 네이밍: 노드 역할이 드러나도록 `*_GW`, `*_CTRL`, `*_MGR`, `*_RX`, `*_TX`

## 4) 인코딩/로그 규칙 (필수)
- 파일 인코딩: UTF-8
- `write()` 문자열: **ASCII only** 권장
  - 금지: 이모지, 스마트쿼트, 특수 대시(—), 박스문자
- 로그 프리픽스 통일: `[NodeName]`

예시:
```c
write("[EMS_ALERT_RX] rx E100 type=%d dir=%d eta=%d", type, dir, eta);
write("[WARN_ARB_MGR] selected level=%d type=%d", level, alertType);
```

## 5) UdpSocket 사용 패턴
- 시작 시 소켓 생성/바인딩 실패 처리
- 전송 시 payload 길이(DLC)와 바이트 packing 명시
- 수신 시 길이 검증 후 파싱
- watchdog(1000ms) 타임아웃 처리 로직 분리

## 6) 구현 체크리스트
- [ ] UDP 포트 5000 하드코딩 반영
- [ ] E100/E200 packing 규격 일치
- [ ] ETH 경로에서 sysvar 경유 없음
- [ ] BODY_GW/IVI_GW가 udpReceive 기반
- [ ] watchdog 1000ms 동작
- [ ] WARN_ARB_MGR 우선순위(Ambulance > Police > Zone > Idle)
- [ ] FZ_001~007 시나리오 재현 가능

## 7) 검증 기준
- MCP `get_bus_nodes_info`에서 13개 노드 확인
- CAPL 컴파일 에러 0건
- FZ_001~007 모두 pass

---
최종 업데이트: 2026-02-26
