# OpenDBC Reference Files

이 폴더는 **OpenDBC 레퍼런스 파일**을 보관합니다.

## 📁 파일 목록

### 1. hyundai_kia_base.dbc (메인 레퍼런스) ⭐
- **크기**: 1676 lines, 93KB
- **ECU**: 47개
- **메시지**: 146개
- **신호**: 1325개
- **Value Tables**: 15개
- **출처**: [commaai/opendbc](https://github.com/commaai/opendbc)
- **용도**: 프로젝트 베이스 DBC (실차 검증 데이터)

### 2. hyundai_2015_ccan.dbc
- **크기**: 1416 lines, 82KB
- **ECU**: 47개
- **메시지**: 113개
- **신호**: 1154개
- **출처**: OpenDBC (2015년 C-CAN 네트워크)

### 3. hyundai_2015_mcan.dbc
- **크기**: 1564 lines, 78KB
- **ECU**: 24개
- **메시지**: 171개
- **신호**: 1184개
- **출처**: OpenDBC (2015년 M-CAN 네트워크)

### 4. hyundai_i30_2014.dbc
- **크기**: 549 lines, 23KB
- **ECU**: 2개
- **메시지**: 32개
- **신호**: 0개
- **출처**: OpenDBC (2014년 i30 모델)

### 5. hyundai_santafe_2007.dbc
- **크기**: 118 lines, 4KB
- **ECU**: 7개
- **메시지**: 13개
- **신호**: 49개
- **출처**: OpenDBC (2007년 Santa Fe 모델)

### 6. hyundai_kia_generic.dbc
- **상태**: 빈 파일 (다운로드 실패)
- **참고**: `hyundai_kia_base.dbc`와 동일 (이름만 변경)

---

## 🎯 사용 방법

### 프로젝트 DBC 파일
프로젝트에서 실제로 사용하는 DBC 파일은 **상위 폴더**에 있습니다:
- `../vehicle_system_custom.dbc` (프로젝트 특화 DBC)
- `../vehicle_system.dbc` (기존 커스텀 DBC - 아카이브용)

### 레퍼런스 활용
이 폴더의 파일들은 **참고용**입니다:
1. **Best Practice 학습**: Value Tables, Alive Counter, Checksum 패턴
2. **신호 정의 참고**: 물리적 단위, 스케일, 오프셋
3. **ECU 네이밍 참고**: Hyundai/Kia 표준 ECU 이름

---

## 📊 비교 분석

자세한 비교 분석은 다음 문서를 참고하세요:
- `opendbc_comparison_report.md` (5개 파일 상세 비교)
- `opendbc_integration_plan.md` (통합 전략)

---

**업데이트**: 2026-02-11
**목적**: OpenDBC 레퍼런스 파일 보관 및 프로젝트 DBC와 구분
