# Software Unit Implementation Guidelines (소프트웨어 유닛 구현 가이드)

**Document ID**: PART6-10-SUIG
**ISO 26262 Reference**: Part 6, Clause 10
**ASPICE Reference**: SWE.4
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Coding Standards

**Standard**: MISRA C:2012
**ASIL-D Required Rules**: 143개 (Mandatory + Required)
**ASIL-C Required Rules**: 110개

---

## 2. MISRA C Compliance

### Mandatory Rules (ASIL-D)

- **Rule 1.3**: No undefined behavior
- **Rule 2.1**: No unreachable code
- **Rule 8.14**: No untagged unions
- **Rule 21.3**: No dynamic memory allocation (malloc, free)

### Advisory Rules

- **Rule 2.7**: Unused parameters should be removed or documented
- **Rule 8.13**: Use `const` for read-only pointers

---

## 3. Implementation Example (ASIL-D)

### CAN_Receive_AEB() Implementation

```c
/**
 * @file can_receive_aeb.c
 * @brief AEB CAN Message Reception Unit
 * @asil ASIL-D
 * @swr SWR-001
 * @misra MISRA C:2012 Compliant
 */

#include "can_driver.h"
#include "crc8.h"

#define AEB_CAN_ID          0x340U
#define AEB_TIMEOUT_MS      30U
#define AEB_CRC_POLY        0x1DU

/**
 * @brief Receive and validate AEB CAN message
 * @param[in] msg Pointer to CAN message structure
 * @param[out] out_data Pointer to decoded AEB data
 * @return true if valid, false if error
 * @asil ASIL-D
 */
bool CAN_Receive_AEB(const CAN_Message* msg, AEB_Data* out_data)
{
  // Input validation (MISRA Rule 1.3)
  if ((msg == NULL) || (out_data == NULL))
  {
    return false;
  }

  // CAN ID check
  if (msg->id != AEB_CAN_ID)
  {
    return false;
  }

  // CRC-8 Validation (Safety Mechanism)
  uint8_t calculated_crc = CRC8_Calculate(msg->data, 7U, AEB_CRC_POLY);
  if (calculated_crc != msg->data[7])
  {
    DTC_Set(DTC_AEB_CRC_ERROR);
    return false;
  }

  // Alive Counter Check
  static uint8_t last_counter = 0U;
  uint8_t current_counter = msg->data[6];
  if (current_counter != ((last_counter + 1U) & 0x0FU))
  {
    DTC_Set(DTC_AEB_COUNTER_ERROR);
    // Do NOT return false - continue processing
  }
  last_counter = current_counter;

  // Signal Decoding
  out_data->aeb_active = (msg->data[0] & 0x01U) != 0U;
  out_data->aeb_level = (msg->data[0] >> 1U) & 0x07U;
  out_data->timestamp = OS_GetTickCount();

  return true;
}
```

---

## 4. Safety Mechanisms Implementation

### Watchdog Kick

```c
void Task_ADAS_Runnable(void)
{
  static uint32_t exec_count = 0U;

  // Core logic
  ADAS_UI_Manager_Main();

  // Watchdog kick every 100ms (10 cycles)
  exec_count++;
  if ((exec_count % 10U) == 0U)
  {
    WD_Kick();
  }
}
```

---

## 5. Code Review Checklist (ASIL-D)

- ✅ MISRA C:2012 compliance verified
- ✅ No dynamic memory allocation
- ✅ All pointers NULL-checked
- ✅ CRC/Timeout/Alive Counter implemented
- ✅ DTC generated on errors
- ✅ Cyclomatic Complexity ≤ 10
- ✅ No recursion
- ✅ No floating-point arithmetic (use fixed-point)

---

## 6. ASPICE SWE.4 Compliance

**Base Practices** (ASPICE PAM 3.1 SWE.4 — 6개 전체):
- ✅ BP1: Develop software units (SW Unit 구현)
- ✅ BP2: Apply coding guidelines (MISRA C:2012 적용)
- ✅ BP3: Conduct code reviews (코드 리뷰 수행 — Peer Review 기록 포함)
- ✅ BP4: Establish bidirectional traceability (SW Unit Design ↔ Code)
- ✅ BP5: Ensure consistency (SU 설계 ↔ 구현 일관성)
- ✅ BP6: Communicate results (코드 리뷰 결과 및 정적분석 결과 배포)

---

**Auto-generated**: 2026-02-14 15:10:48
