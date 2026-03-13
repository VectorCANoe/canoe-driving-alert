# PlantUML Diagrams

이 디렉토리에는 IVI vECU 아키텍처의 모든 PlantUML 다이어그램이 포함되어 있습니다.

## 📦 통합 파일 (권장)

**한 파일에 모든 다이어그램 포함** - Draw.io처럼 페이지 전환으로 탐색 가능:

- **`00_architecture_overview.puml`** (2 diagrams)
  - System Context Diagram
  - AUTOSAR Layered Architecture

- **`01_lighting_control.puml`** (4 diagrams)
  - Component Architecture
  - Speed-Linked State Machine
  - Door-Linked Sequence
  - IVI Color Sync Flow

- **`02_safety_system.puml`** (4 diagrams)
  - Safety Component Architecture
  - Reverse Safety State Machine
  - ADAS Integration Sequence
  - Door Hazard Detection

- **`03_ota_diagnostic.puml`** (4 diagrams)
  - UDS 0x14 Clear DTC
  - UDS 0x34 OTA Download
  - OTA Failure Recovery
  - Post-OTA Verification

- **`04_fault_injection.puml`** (5 diagrams)
  - Test Architecture
  - BDC Communication Fault
  - Door Sensor Fault
  - Sensor Signal Fault
  - CANoe Configuration

- **`05_can_communication.puml`** (6 diagrams)
  - AUTOSAR ComStack
  - CAN Signal Mapping
  - Message Transmission
  - Message Reception
  - Performance Metrics
  - Error Handling

## 📄 개별 파일

각 다이어그램이 별도 파일로도 제공됩니다:
- `architecture_overview_01.puml`, `architecture_overview_02.puml`
- `lighting_control_architecture_01~04.puml`
- `safety_system_architecture_01~04.puml`
- `ota_diagnostic_sequence_01~04.puml`
- `fault_injection_workflow_01~05.puml`
- `can_communication_stack_01~06.puml`

## 🎨 사용 방법

### VSCode에서 렌더링

1. **PlantUML 확장 설치**: `jebbs.plantuml`

2. **통합 파일 열기** (권장):
   ```
   00_architecture_overview.puml
   ```

3. **미리보기**:
   - `Alt + D` 또는 `Ctrl + Shift + P` → "PlantUML: Preview Current Diagram"

4. **페이지 전환**:
   - 미리보기 창에서 **화살표 버튼** 또는 **페이지 번호** 클릭
   - Draw.io처럼 여러 다이어그램을 하나의 파일에서 탐색 가능

5. **이미지 내보내기**:
   - `Ctrl + Shift + P` → "PlantUML: Export Current Diagram"
   - PNG, SVG, PDF 등 지원

## 🔄 다이어그램 재생성

마크다운 파일 업데이트 후:

```bash
# 통합 파일 재생성
python3 ../create_consolidated_puml.py

# 개별 파일 재생성
python3 ../extract_plantuml.py
```

## 💡 팁

- **통합 파일 사용 권장**: 한 파일에서 모든 다이어그램 탐색 가능
- **개별 파일**: 특정 다이어그램만 빠르게 열고 싶을 때 사용
- **원본은 마크다운**: `.puml` 파일은 렌더링 전용, 수정은 마크다운에서
