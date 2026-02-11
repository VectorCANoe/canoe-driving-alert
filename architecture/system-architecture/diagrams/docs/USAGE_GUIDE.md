# PlantUML 설치 및 사용 가이드

## ✅ 설치 완료

**전역 설치 (모든 프로젝트에서 사용 가능)**:
```bash
# 설치 위치
/opt/homebrew/bin/plantuml
/opt/homebrew/bin/dot (Graphviz)

# 버전 확인
plantuml -version
# PlantUML version 1.2026.1
# Graphviz version 14.1.2
```

이제 **어떤 프로젝트에서든** `plantuml` 명령어를 사용할 수 있습니다!

---

## 📦 통합 다이어그램 파일 (권장)

**한 파일에 모든 다이어그램 포함** - Draw.io처럼 페이지 전환:

### 위치
`/architecture/system-architecture/diagrams/puml/`

### 파일 목록
1. **`00_architecture_overview.puml`** (2개 다이어그램)
   - System Context Diagram
   - AUTOSAR Layered Architecture

2. **`01_lighting_control.puml`** (4개 다이어그램)
   - Component Architecture
   - Speed-Linked State Machine
   - Door-Linked Sequence
   - IVI Color Sync Flow

3. **`02_safety_system.puml`** (4개 다이어그램)
   - Safety Component Architecture
   - Reverse Safety State Machine
   - ADAS Integration Sequence
   - Door Hazard Detection

4. **`03_ota_diagnostic.puml`** (4개 다이어그램)
   - UDS 0x14 Clear DTC
   - UDS 0x34 OTA Download
   - OTA Failure Recovery
   - Post-OTA Verification

5. **`04_fault_injection.puml`** (5개 다이어그램)
   - Test Architecture
   - BDC Communication Fault
   - Door Sensor Fault
   - Sensor Signal Fault
   - CANoe Configuration

6. **`05_can_communication.puml`** (6개 다이어그램)
   - AUTOSAR ComStack
   - CAN Signal Mapping
   - Message Transmission
   - Message Reception
   - Performance Metrics
   - Error Handling

---

## 🎨 사용 방법

### 1. VSCode에서 미리보기 (권장)

```bash
# PlantUML 확장 설치
# Extensions → "PlantUML" 검색 → jebbs.plantuml 설치

# .puml 파일 열기
# Alt + D → 미리보기
# 화살표 버튼으로 페이지 전환 (통합 파일의 경우)
```

### 2. CLI로 PNG 생성

```bash
# 단일 파일 렌더링
plantuml -tpng 00_architecture_overview.puml

# 여러 파일 한번에
plantuml -tpng *.puml

# 출력 디렉토리 지정
plantuml -tpng 00_architecture_overview.puml -o ./rendered/

# SVG 생성 (벡터, 무한 확대)
plantuml -tsvg 00_architecture_overview.puml

# PDF 생성
plantuml -tpdf 00_architecture_overview.puml
```

### 3. 다른 프로젝트에서 사용

```bash
# 어디서든 사용 가능 (전역 설치)
cd ~/my-other-project
plantuml -tpng my_diagram.puml
```

---

## 📊 렌더링된 이미지

**위치**: `/architecture/system-architecture/diagrams/rendered/`

**생성된 PNG 파일**:
- `00_architecture_overview.png`, `00_architecture_overview_001.png`, ...
- `01_lighting_control.png`, `01_lighting_control_001.png`, ...
- `02_safety_system.png`, ...
- `03_ota_diagnostic.png`, ...
- `04_fault_injection.png`, ...
- `05_can_communication.png`, ...

**사용처**:
- PowerPoint 프레젠테이션
- Word/PDF 문서
- 기술 리뷰 자료
- ISO 26262 문서화

---

## 🔄 자동화 스크립트

### 모든 다이어그램 재생성

```bash
# 프로젝트 루트에서
cd /Users/juns/code/work/mobis/PBL/architecture/system-architecture

# 통합 .puml 파일 재생성 (마크다운에서 추출)
python3 create_consolidated_puml.py

# 개별 .puml 파일 재생성
python3 extract_plantuml.py

# PNG 이미지 생성
cd diagrams/puml
plantuml -tpng 0*.puml -o ../rendered/
```

### 일괄 렌더링 스크립트

```bash
#!/bin/bash
# render_all.sh

cd /Users/juns/code/work/mobis/PBL/architecture/system-architecture/diagrams/puml

echo "🎨 Rendering all PlantUML diagrams..."

plantuml -tpng 00_*.puml 01_*.puml 02_*.puml 03_*.puml 04_*.puml -o ../rendered/

echo "✅ All diagrams rendered to ../rendered/"
```

---

## 💡 팁

### 고품질 이미지
```bash
# 고해상도 PNG (DPI 300)
plantuml -tpng -DPLANTUML_LIMIT_SIZE=8192 diagram.puml

# SVG (벡터, 무한 확대)
plantuml -tsvg diagram.puml
```

### 테마 변경
```plantuml
@startuml
!theme silver        # 은색 테마
!theme materia       # Material Design
!theme plain         # 심플
!theme bluegray      # 블루그레이
@enduml
```

### 배치 처리
```bash
# 모든 .puml 파일을 PNG와 SVG로 동시 생성
for file in *.puml; do
    plantuml -tpng "$file"
    plantuml -tsvg "$file"
done
```

---

## 📚 참고 자료

- **PlantUML 공식 문서**: https://plantuml.com
- **Graphviz 문서**: https://graphviz.org
- **VSCode 확장**: https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml

---

## ⚠️ 주의사항

1. **원본은 마크다운**: `.puml` 파일은 자동 생성됨. 수정은 마크다운에서!
2. **특수문자 주의**: `<`, `>`, `≤` 등은 PlantUML에서 오류 발생 가능
3. **대용량 다이어그램**: 너무 복잡하면 렌더링 시간 증가

---

**작성일**: 2026-02-08  
**PlantUML 버전**: 1.2026.1  
**Graphviz 버전**: 14.1.2
