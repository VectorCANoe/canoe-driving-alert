# PlantUML 미리보기 문제 해결 가이드

## ❌ "No valid diagram found here!" 오류

### 원인
VSCode PlantUML 확장은 **커서가 `@startuml`과 `@enduml` 사이**에 있을 때만 다이어그램을 표시합니다.

### 해결 방법

1. **커서 위치 확인**
   - `.puml` 파일을 열고 커서를 `@startuml` 아래 아무 곳에나 위치시키세요
   - 예: 10번 라인쯤

2. **미리보기 실행**
   - `Alt + D` (Mac: `Option + D`)
   - 또는 `Cmd + Shift + P` → "PlantUML: Preview Current Diagram" 입력

3. **통합 파일의 경우**
   - 파일에 여러 다이어그램이 있으면 미리보기 창에서 **화살표 버튼**으로 전환
   - 각 `@startuml` ~ `@enduml` 블록이 하나의 페이지

---

## 🔧 Graphviz 관련

### Graphviz는 백그라운드 엔진입니다
- **매번 실행할 필요 없음**: PlantUML이 자동으로 호출
- **설치 확인**:
  ```bash
  dot -V
  # dot - graphviz version 14.1.2
  ```

### VSCode가 Graphviz를 못 찾는 경우

1. **VSCode 재시작** (가장 중요!)
   - Graphviz 설치 후 반드시 VSCode 완전 종료 후 재시작

2. **설정 확인**
   - `Cmd + ,` → "plantuml" 검색
   - `Plantuml: Render` = "Local" 확인
   - 필요시 `Plantuml: Dot Home` = `/opt/homebrew/bin/dot` 설정

3. **수동 경로 설정** (VSCode settings.json)
   ```json
   {
     "plantuml.render": "Local",
     "plantuml.server": "",
     "plantuml.commandArgs": [],
     "plantuml.jarPath": ""
   }
   ```

---

## 📁 파일 구조 정리 완료

### 현재 상태
```
diagrams/puml/
├── 00_architecture_overview.puml    (2개 다이어그램)
├── 01_lighting_control.puml          (4개)
├── 02_safety_system.puml             (4개)
├── 03_ota_diagnostic.puml            (4개)
├── 04_fault_injection.puml           (5개)
├── 05_can_communication.puml         (6개)
├── archive/                          (개별 파일 25개 백업)
├── README.md
└── USAGE_GUIDE.md
```

### 백업 위치
- **아카이브**: `diagrams/puml/archive/`
- 개별 파일 25개 모두 안전하게 보관됨
- 필요시 언제든 복원 가능

---

## 🎨 디자인 변경 방법

### 테마 변경 (한 줄로 전체 스타일 변경)

파일 상단의 `!theme` 라인만 수정:

```plantuml
@startuml
!theme silver        ← 이 부분만 변경
skinparam componentStyle rectangle
...
```

### 추천 테마

```plantuml
' 1. 전문가/프레젠테이션용 (현재)
!theme silver

' 2. 모던/부드러운 스타일
!theme materia

' 3. 다크 모드
!theme black-knight

' 4. 블루 계열
!theme bluegray

' 5. 심플/미니멀
!theme plain
```

### 세부 커스터마이징

```plantuml
@startuml
!theme silver

' 색상 변경
skinparam componentBackgroundColor #LightSkyBlue
skinparam componentBorderColor #Navy

' 폰트 변경
skinparam defaultFontName Arial
skinparam defaultFontSize 12

' 화살표 스타일
skinparam ArrowThickness 2
skinparam ArrowColor #333333
@enduml
```

---

## ✅ 체크리스트

- [x] Graphviz 설치 확인 (`dot -V`)
- [x] PlantUML 설치 확인 (`plantuml -version`)
- [x] VSCode PlantUML 확장 설치
- [x] VSCode 재시작
- [x] 커서를 `@startuml` 블록 안에 위치
- [x] `Alt + D`로 미리보기 실행
- [x] 개별 파일 아카이브로 백업
- [x] 통합 파일 6개로 정리 완료

---

**작성일**: 2026-02-10  
**마지막 업데이트**: 파일 구조 정리 및 미리보기 오류 수정
