# VSCode PlantUML 버전 호환성 문제 해결

## 🔴 문제 상황

**증상**: VSCode에서 "Syntax Error?" 발생, PNG는 정상 생성됨

**원인**: VSCode PlantUML 확장이 **구버전(1.2021.00)** 사용
- `!theme` 명령어는 **PlantUML 1.2021.7 이상** 필요
- CLI는 최신 버전(1.2026.1) 사용 → PNG 생성 정상

## ✅ 해결 방법

### 임시 해결 (완료)
모든 `.puml` 파일에서 `!theme` 주석 처리:
```plantuml
@startuml
' !theme silver  ' Commented out for VSCode compatibility
skinparam componentStyle rectangle
```

### 영구 해결 (권장)

VSCode 설정에서 최신 PlantUML JAR 사용:

1. **최신 PlantUML JAR 다운로드**
   ```bash
   cd ~/Downloads
   curl -O https://github.com/plantuml/plantuml/releases/download/v1.2026.1/plantuml-1.2026.1.jar
   ```

2. **VSCode 설정** (`Cmd + ,`)
   - `plantuml.jar` 검색
   - `Plantuml: Jar Path` 설정:
     ```
     /Users/juns/Downloads/plantuml-1.2026.1.jar
     ```

3. **VSCode 재시작**

4. **테마 활성화**
   - 모든 `.puml` 파일에서 주석 제거:
     ```plantuml
     !theme silver  ' 이제 정상 작동
     ```

## 🎨 테마 사용 가능 여부

| 환경 | 버전 | `!theme` 지원 | 상태 |
|------|------|--------------|------|
| CLI (`plantuml`) | 1.2026.1 | ✅ | PNG 생성 정상 |
| VSCode 확장 (기본) | 1.2021.00 | ❌ | 주석 처리 필요 |
| VSCode 확장 (JAR 설정 후) | 1.2026.1 | ✅ | 모든 기능 사용 가능 |

## 📝 현재 상태

- ✅ 모든 통합 `.puml` 파일에서 `!theme` 주석 처리 완료
- ✅ VSCode 미리보기 정상 작동
- ✅ CLI PNG 생성 정상 (테마 없이도 깔끔한 출력)

---

**작성일**: 2026-02-10  
**해결**: VSCode 구버전 PlantUML 호환성 문제
