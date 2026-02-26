# CAPL 코딩 가이드라인 (CANoe 19 기준)

> **이 문서는 AI(Claude)가 .can 파일을 작성할 때 반드시 먼저 읽는 가이드입니다.**
> 프로젝트에서 직접 디버깅한 실전 경험 + Vector 공식 동작 기준을 통합했습니다.

---

## 1. 인코딩 규칙 (가장 중요 — 컴파일 실패의 주원인)

### 핵심 원칙

> **write() 문자열 리터럴 안에는 순수 ASCII(0x00~0x7F)만 사용한다.**

### 이유

CAPL 컴파일러(CANoe 19)는 `.can` 파일을 **Windows-1252 (CP1252)** 로 읽는다.
파일이 UTF-8로 저장되어 있어도 컴파일러는 그대로 Windows-1252로 해석한다.

UTF-8 멀티바이트 문자의 바이트 시퀀스 중 일부가 Windows-1252에서 `"` 로 해석되면
**문자열이 중간에 강제 종료**되고 `corresponding " missed` 컴파일 에러가 발생한다.

| Win-1252 바이트 | 해석 값 | 의미 |
|----------------|---------|------|
| `0x93` | `"` | 좌측 큰따옴표 = 문자열 종료! |
| `0x94` | `"` | 우측 큰따옴표 = 문자열 종료! |

### 위험 문자 목록

| 문자 | 유니코드 | UTF-8 바이트 | 위험 바이트 | 증상 |
|------|---------|------------|-----------|------|
| `—` (em dash) | U+2014 | E2 80 **94** | 0x94 | `corresponding " missed` |
| `─` (box drawing) | U+2500 | E2 **94** 80 | 0x94 | 동일 |
| `드` (한글) | U+B4DC | EB **93** 9C | 0x93 | 동일 |
| `🔧` (emoji) | U+1F527 | F0 9F **94** A7 | 0x94 | 동일 |
| `📦` (emoji) | U+1F4E6 | F0 9F **93** A6 | 0x93 | 동일 |
| 기타 이모지 | 다수 | F0 9F 9x xx | 0x93/0x94 포함 가능 | 동일 |

> **중요**: 한글은 일부 글자만 위험하지만, 어느 글자가 위험한지 예측하기 어렵다.
> 따라서 **write() 안에 한글을 절대 사용하지 않는다.**

### 안전한 특수문자 (write() 안 사용 가능)

| 문자 | 유니코드 | UTF-8 | 판정 |
|------|---------|-------|------|
| `⚠` (경고) | U+26A0 | E2 9A A0 | 0x93/0x94 없음 — 안전 |
| `★` (별) | U+2605 | E2 98 85 | 안전 |
| `▶` (삼각) | U+25B6 | E2 96 B6 | 안전 |
| `═` (box 이중선) | U+2550 | E2 95 90 | 안전 |

> **권고**: 안전 여부를 확인하려면 UTF-8 바이트에 0x93 또는 0x94가 포함되는지 확인한다.
> 번거로우므로 **write() 는 항상 ASCII only**가 실질적 최선이다.

### 올바른 패턴

```c
/* 한글 설명은 주석으로 */
on start
{
  /* 노드 시작 초기화 */
  write("[MyNode] start -- init OK");      /* OK: ASCII only */
  write("[MyNode] zone change: %d -> %d", prevZone, gZone);  /* OK */
}
```

### 잘못된 패턴 (컴파일 에러)

```c
on start
{
  write("[MyNode] 노드 시작 — 초기화 완료");  /* 에러: '드'=0x93, '—'=0x94 */
  write("[MyNode] Zone %d → Zone %d", a, b); /* 에러: '→'의 바이트가 문제될 수 있음 */
  write("[MyNode] 🔧 완료");                  /* 에러: 이모지에 0x94 포함 */
}
```

### 특수기호 ASCII 대체표

| 원본 | 대체 | 원본 | 대체 |
|------|------|------|------|
| `—` (em dash) | `--` | `→` | `->` |
| `←` | `<-` | `↔` | `<->` |
| `⚠` 경고 | `[!]` | `✅` 완료 | `[OK]` |
| `❌` 에러 | `[ERR]` | `★` 중요 | `**` |
| `▶` 실행 | `>` | `─────` | `-----` |

---

## 2. 데이터 타입

### CAPL 기본 타입

| 타입 | 크기 | 범위 | 용도 |
|------|------|------|------|
| `int` | 4 byte | -2,147,483,648 ~ 2,147,483,647 | 일반 정수 |
| `long` | 4 byte | `int`와 동일 | 큰 정수 |
| `float` | 4 byte | 단정밀도 부동소수 | 부동소수 (비권장) |
| `double` | 8 byte | 배정밀도 부동소수 | **부동소수 권장** |
| `byte` | 1 byte | 0 ~ 255 | 비트 조작, CAN 바이트 |
| `word` | 2 byte | 0 ~ 65535 | 16bit 값 |
| `dword` | 4 byte | 0 ~ 4,294,967,295 | 32bit 값, 타임스탬프 |
| `char` | 1 byte | — | 문자 |

> `uint32`, `int32` 등 C 스타일 타입은 CAPL에서 사용 불가. (sysvars XML에서는 사용함 — 혼동 주의)

### 타입 변환

```c
/* 명시적 캐스트 사용 */
int rawVal  = (int)(gSpeed * 10.0);    /* double -> int */
double val  = (double)rawInt * 0.1;    /* int -> double */
byte  bVal  = (byte)(intVal & 0xFF);   /* int -> byte */
```

---

## 3. 변수 선언 규칙

### variables {} 블록 (글로벌)

```c
variables
{
  /* 타이머 */
  msTimer tMyTimer;

  /* 상수 — 스칼라만 가능, const 배열은 CAPL 버전에 따라 미지원 */
  const int    MAX_SPEED = 110;
  const double THRESHOLD = 50.0;

  /* 일반 변수 — 상수로 초기화 가능 */
  int    gMyInt    = 0;
  double gMyDouble = 60.0;
  int    gMyArray[6];   /* 배열: 선언만, on start에서 초기화 */
}
```

### 로컬 변수 (이벤트 핸들러/함수 내부)

```c
/* WRONG: 비상수 표현식으로 초기화 불가 */
on message MyMsg
{
  int prevZone = gZone;        /* 컴파일 에러: Must be constant expression */
  double speed = gSpeed * 0.1; /* 컴파일 에러 */
}

/* CORRECT: 선언과 대입 분리 */
on message MyMsg
{
  int    prevZone;
  double speed;
  prevZone = gZone;
  speed    = this.Vehicle_Speed * 0.1;
}
```

### 배열 초기화

```c
/* WRONG: 배열 inline 초기화 미지원 */
variables
{
  int gBright[6] = {40, 120, 200, 255, 200, 120};  /* 컴파일 에러 */
}

/* CORRECT: on start에서 초기화 */
variables
{
  int gBright[6];
}
on start
{
  gBright[0] = 40;
  gBright[1] = 120;
  gBright[2] = 200;
  gBright[3] = 255;
  gBright[4] = 200;
  gBright[5] = 120;
}
```

### const 배열

```c
/* CAPL에서 const 배열이 필요한 경우 → switch-case로 대체 */
/* WRONG (일부 버전에서 미지원):
   const int COLOR_R[3] = {0, 255, 255}; */

/* CORRECT: switch-case */
void getColor(int step, int* r, int* g, int* b)
{
  switch (step)
  {
    case 0: *r =   0; *g = 200; *b =   0; break;  /* GREEN */
    case 1: *r = 255; *g = 100; *b = 150; break;  /* PINK */
    case 2: *r = 255; *g =   0; *b =   0; break;  /* RED */
    default: *r = 60; *g =  60; *b =  60; break;
  }
}
```

---

## 4. System Variables (sysvar) 접근

```c
/* 읽기 */
int zone = @Navigation::gRoadZone;

/* 쓰기 */
@Arbiter::gWarningLevel = 1;

/* 변경 이벤트 핸들러 */
on sysvar Navigation::gRoadZone
{
  int newVal;
  newVal = @Navigation::gRoadZone;
  /* 처리 로직 */
}
```

---

## 5. CAN 메시지 송신

```c
void sendMyMsg(int pattern, int mode)
{
  message Ambient_Control txMsg;  /* DBC에 정의된 메시지명 */

  txMsg.AmbientPattern = pattern;
  txMsg.AmbientActive  = 1;
  txMsg.AliveCounter   = gAliveCounter;

  output(txMsg);
  gAliveCounter = (gAliveCounter + 1) & 0x0F;
}
```

---

## 6. 타이머 패턴

```c
variables
{
  msTimer tMyTimer;
}

on start
{
  setTimer(tMyTimer, 10);   /* 10ms 후 첫 발화 */
}

on timer tMyTimer
{
  /* 처리 */
  setTimer(tMyTimer, 10);   /* 재시작: 마지막에 호출 */
}

/* 조건부 취소 */
on sysvar Navigation::gSteeringInput
{
  if (@Navigation::gSteeringInput == 1)
    cancelTimer(tHighwaySteer);
  else
    setTimer(tHighwaySteer, 10000);
}
```

---

## 7. 파일 구조 표준

```c
/*
 * NodeName.can — 노드 역할 요약 (한 줄)
 *
 * 역할: (한글 가능 — 주석이므로)
 *   - ...
 *
 * 채널: ...
 * DBC: ...
 * V-Model: SWE.3
 * Req 추적: Req_XXX
 */

includes
{
}

variables
{
  /* 타이머 */

  /* 상수 */

  /* 상태 변수 */
}

/*============================================================
 * 초기화
 *============================================================*/
on start
{
  write("[NodeName] start -- brief english description");
  /* 초기화 로직 */
}

/*============================================================
 * 이벤트 핸들러들
 *============================================================*/
on message MessageName { ... }
on sysvar Namespace::VarName { ... }
on timer tMyTimer { ... }

/*============================================================
 * 헬퍼 함수들
 *============================================================*/
void myFunction(int param) { ... }
```

---

## 8. write() 함수 사용법

```c
/* 기본 출력 */
write("[Node] message text");

/* printf 스타일 포맷 */
write("[Node] int=%d  float=%.1f  hex=0x%02X", intVal, floatVal, hexVal);

/* 권장 접두사 패턴 */
write("[NodeName] start -- ...");       /* 초기화 */
write("[NodeName] event: ...");         /* 이벤트 수신 */
write("[NodeName] [!] warning: ...");   /* 경고 */
write("[NodeName] [ERR] ...");          /* 에러 */
write("[NodeName] [OK] ...");           /* 정상 완료 */
write("[NodeName] pattern: %d -> %d", oldP, newP);  /* 상태 전환 */
```

---

## 9. 조건부 삼항 연산자

```c
/* CAPL은 C 스타일 삼항 연산자 지원 */
gCurrentWarning = (active == 1) ? warnType : WARN_NONE;
txMsg.AmbientActive = (pattern != 0) ? 1 : 0;
```

---

## 10. LIN 프레임 수신 (참고)

```c
on linFrame 0x21
{
  word rawCurrent;
  rawCurrent = (this.byte(1) & 0x03) << 8 | this.byte(0);
  gMotorCurrent = rawCurrent * 0.1;
}
```

---

## 11. 이벤트 핸들러 종류

```c
on start           { }   /* 측정 시작 */
on stopMeasurement { }   /* 측정 종료 */
on message MsgName { }   /* CAN 메시지 수신 */
on timer tName     { }   /* 타이머 만료 */
on sysvar NS::Var  { }   /* System Variable 변경 */
on linFrame 0xNN   { }   /* LIN 프레임 수신 */
on key 'A'         { }   /* 키보드 입력 (테스트용) */
on errorFrame      { }   /* CAN 에러 프레임 */
on busOff          { }   /* Bus Off */
```

---

## 12. 체크섬 / AliveCounter 패턴

```c
/* AliveCounter: 0~15 순환, CAN 메시지마다 증가 */
txMsg.AliveCounter = gAliveCounter;
txMsg.Checksum     = (gAliveCounter ^ gZone ^ gWarningLvl) & 0x0F;
output(txMsg);
gAliveCounter = (gAliveCounter + 1) & 0x0F;
```

---

## 13. 레퍼런스 파일 주의사항

> **docs/LIN-Door/canoe/nodes/*.can** 및 **reference/legacy/capl_nodes/*.can** 파일들은
> write() 문자열 안에 한글, `—`, `⚠`, 이모지 등을 포함하고 있어 **그대로 컴파일하면 에러 발생**.
> 구조·로직 참조용으로만 사용하고, write() 문자열은 이 가이드라인에 따라 새로 작성한다.

---

## 14. 빠른 체크리스트

새 `.can` 파일 작성 전 확인:

- [ ] `write()` 문자열에 한글 없음
- [ ] `write()` 문자열에 `—`, `→`, `─`, 이모지 없음 (ASCII only)
- [ ] 로컬 변수 선언 시 비상수 초기화 없음 (선언/대입 분리)
- [ ] 배열 초기화는 `on start {}` 에서
- [ ] `const` 배열 대신 `switch-case` 사용
- [ ] `variables {}` 에 타이머, 상수, 상태변수 순으로 선언
- [ ] `on timer` 핸들러 끝에 `setTimer()` 재호출
- [ ] `output()` 전에 모든 메시지 필드 설정
- [ ] AliveCounter `(cnt + 1) & 0x0F` 패턴 사용

---

*최종 업데이트: 2026-02-26 — 실전 디버깅(노드 컴파일 에러 2회) 기반 작성*
