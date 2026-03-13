# VSCode PlantUML 최신 버전 사용 설정

## 🎯 목표
VSCode PlantUML 확장이 Homebrew로 설치한 **최신 PlantUML CLI (1.2026.1)**를 사용하도록 설정

## ⚙️ 설정 방법

### 1. VSCode 설정 열기
- `Cmd + ,` 또는 `Code > Settings > Settings`

### 2. PlantUML 설정 검색
- 검색창에 `plantuml` 입력

### 3. 다음 설정 변경

#### A. Render 방식 (중요!)
```
Plantuml: Render = "Local"
```
- 기본값은 "PlantUMLServer"일 수 있음
- **반드시 "Local"로 변경**

#### B. PlantUML 실행 경로
```
Plantuml: Command Path = "/opt/homebrew/bin/plantuml"
```
- 또는 비워두면 시스템 PATH에서 자동 검색

#### C. Java 경로 (선택사항)
```
Plantuml: Java = ""
```
- 비워두면 시스템 기본 Java 사용
- PlantUML이 이미 Java를 포함하므로 보통 불필요

### 4. settings.json 직접 편집 (권장)

`Cmd + Shift + P` → "Preferences: Open User Settings (JSON)"

```json
{
  "plantuml.render": "Local",
  "plantuml.commandArgs": [],
  "plantuml.jarPath": "",
  "plantuml.server": "",
  "plantuml.urlFormat": "png"
}
```

## 🔄 적용 방법

1. **VSCode 재시작** (중요!)
2. `.puml` 파일 열기
3. `Alt + D` (Mac: `Option + D`)로 미리보기

## ✅ 확인 방법

미리보기 창 하단에 버전 정보 표시:
```
PlantUML version 1.2026.1
```

이전에 `1.2021.00`이 표시되었다면 성공!

## 🎨 테마 활성화

설정 완료 후 모든 `.puml` 파일에서 테마 주석 제거:

```plantuml
@startuml
!theme silver  ' 이제 정상 작동!
skinparam componentStyle rectangle
```

## 🔧 자동 업데이트 스크립트

테마 주석 제거 (6개 파일 일괄 처리):

```bash
cd /Users/juns/code/work/mobis/PBL/architecture/system-architecture/diagrams/puml

# 주석 제거
sed -i '' "s/^' !theme silver.*$/!theme silver/g" 0*.puml

echo "✅ 테마 활성화 완료!"
```

## 📋 체크리스트

- [ ] VSCode 설정에서 `Plantuml: Render = "Local"` 설정
- [ ] VSCode 완전 재시작
- [ ] `.puml` 파일 열어서 미리보기 테스트
- [ ] 버전 확인 (1.2026.1 표시되는지)
- [ ] 테마 주석 제거 스크립트 실행
- [ ] 모든 다이어그램 미리보기 정상 작동 확인

---

**작성일**: 2026-02-10  
**목적**: VSCode에서 최신 PlantUML 사용하여 `!theme` 등 최신 기능 활용
