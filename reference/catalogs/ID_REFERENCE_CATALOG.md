# ID Reference Catalog (RAG Seed)

**Last Updated**: 2026-03-05  
**Scope**: CAN Identifier policy, AUTOSAR communication stack, traceability evidence for `00f_CAN_ID_Allocation_Standard.md`

---

## 1. Source Tiers

| Tier | Type | Use Rule |
|---|---|---|
| Tier-1 | Official standard/spec (ISO/AUTOSAR/SAE) | 정책/규칙 근거의 1차 출처로 사용 |
| Tier-2 | Official implementation docs (Linux kernel) | 구현/검증 관점의 보조 근거로 사용 |
| Tier-3 | Project SoT (`canoe/databases/*.dbc`, `0302/0303/0304`) | 실제 적용 기준(최종 판단)으로 사용 |
| Tier-4 | OSS/examples/papers | 설계 참고/검증 아이디어로만 사용 |

---

## 2. Collected References

### 2.1 Tier-1: Official Specs

| File | Category | Why It Matters |
|---|---|---|
| `standards/id_comm/autosar_cp_r24-11/AUTOSAR_CP_SWS_COM.pdf` | AUTOSAR CP | COM signal packing/transfer behavior 기준 |
| `standards/id_comm/autosar_cp_r24-11/AUTOSAR_CP_SWS_CANInterface.pdf` | AUTOSAR CP | CanIf Tx/Rx interface and ID handling 기준 |
| `standards/id_comm/autosar_cp_r24-11/AUTOSAR_CP_SWS_CANTransportLayer.pdf` | AUTOSAR CP | CanTp(ISO-TP mapping) 기준 |
| `standards/id_comm/autosar_cp_r24-11/AUTOSAR_CP_SWS_PDURouter.pdf` | AUTOSAR CP | PduR routing/forwarding 기준 |
| `standards/id_comm/iso_sae_snapshots/iso_11898-1_2024.html` | ISO | CAN data-link/general architecture 카탈로그 근거 |
| `standards/id_comm/iso_sae_snapshots/iso_15765-2_2024.html` | ISO | ISO-TP 카탈로그 근거 |
| `standards/id_comm/iso_sae_snapshots/iso_26262-1_2018.html` | ISO 26262 | 용어/프레임워크 카탈로그 근거 |
| `standards/id_comm/iso_sae_snapshots/iso_26262-6_2018.html` | ISO 26262 | SW unit/integration 규율 카탈로그 근거 |
| `standards/id_comm/iso_sae_snapshots/sae_j1939-21_product.html` | SAE | J1939-21 식별자/전송 계층 카탈로그 근거 |

### 2.2 Tier-2: Official Implementation Docs

| File | Category | Why It Matters |
|---|---|---|
| `standards/id_comm/linux_kernel/can.html` | Linux kernel | SocketCAN + CAN frame/ID handling 참조 |
| `standards/id_comm/linux_kernel/iso15765-2.html` | Linux kernel | ISO-TP 소켓/동작 참조 |
| `standards/id_comm/linux_kernel/j1939.html` | Linux kernel | J1939 소켓/주소 체계 참조 |

### 2.3 Tier-3: Project SoT

| Path | Use |
|---|---|
| `canoe/databases/*.dbc` | 실제 메시지 ID/Owner 최종 기준 |
| `driving-situation-alert/0302_NWflowDef.md` | Flow 기준 |
| `driving-situation-alert/0303_Communication_Specification.md` | Comm 기준 |
| `driving-situation-alert/0304_System_Variables.md` | Var 기준 |
| `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` | 프로젝트 ID 정책 SoT |

---

## 3. Gap / TODO (High Value)

| Priority | Item | Status | Note |
|---|---|---|---|
| P1 | ISO 11898-1/15765-2 원문 PDF(라이선스 정식본) | Pending | 사내 라이선스 경로로 확보 필요 |
| P1 | SAE J1939-21 원문 PDF(라이선스 정식본) | Pending | 사내 라이선스 경로로 확보 필요 |
| P2 | AUTOSAR R25-11 동일 문서 세트 비교 | Pending | 현재는 R24-11 기준, 릴리스 업 시 diff 필요 |
| P2 | ID collision 자동 리포트(주기 실행) | Pending | `scripts/quality`에 정기 리포트화 권장 |

---

## 4. RAG Ingestion Order (Recommended)

1. Tier-1 공식 스펙
2. Tier-3 프로젝트 SoT
3. Tier-2 구현 문서
4. Tier-4 OSS/논문

---

## 5. Provenance Rule

- 정책 문구 작성 시 Tier-1 또는 Tier-3 근거를 최소 1개 이상 명시한다.
- Tier-4만으로 정책을 확정하지 않는다.
- `00f` 변경 시, 변경 근거 파일 경로를 change-order 또는 개정 이력에 기록한다.
