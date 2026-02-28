# DBC Split Report

## 1) Scope and Boundary
- Source baseline: `canoe/network/dbc/emergency_system.dbc`
- References used (read-only):
  - `docs/meeting-notes/MET_30_2026.02.28.txt`
  - `driving-situation-alert/00~07` (no modification)
- Repository boundary applied:
  - `driving-situation-alert` is read-only per `canoe/AGENTS.md`
  - Report is written to `canoe/tmp/dbc_split_report.md`

## 2) Output Files (Domain Split)
- `canoe/network/dbc/emergency_system_chassis.dbc`
- `canoe/network/dbc/emergency_system_powertrain.dbc`
- `canoe/network/dbc/emergency_system_body.dbc`
- `canoe/network/dbc/emergency_system_infotainment.dbc`
- `canoe/network/dbc/chassis_can.dbc`
- `canoe/network/dbc/powertrain_can.dbc`
- `canoe/network/dbc/body_can.dbc`
- `canoe/network/dbc/infotainment_can.dbc`
- `canoe/network/dbc/test_can.dbc`

## 3) Frame Allocation Result (Expanded)
| Domain DBC | Frame IDs | Message Count | Note |
|---|---|---:|---|
| chassis | `0x100`, `0x101`, `0x102`, `0x103`, `0x104`, `0x105`, `0x106`, `0x107`, `0x108`, `0x109`, `0x230`, `0x231`, `0x232` | 13 | 湲곗〈 ?낅젰/寃곌낵 + ?좎냽???붾젅?댄듃/釉뚮젅?댄겕/?좏겕/?ъ뒪 + 湲닿툒紐⑤땲??|
| body | `0x210`, `0x211`, `0x212`, `0x213`, `0x214`, `0x215`, `0x216`, `0x217`, `0x218`, `0x219` | 10 | 湲곗〈 ?곕퉬?명듃/鍮꾩긽??李쎈Ц/?댁쟾?먯긽??+ ?꾩뼱/?⑦봽/??댄띁/?쒗듃踰⑦듃/罹먮퉰/?ъ뒪 |
| infotainment | `0x110`, `0x220`, `0x221`, `0x222`, `0x223`, `0x224`, `0x225`, `0x226`, `0x227`, `0x228` | 10 | 湲곗〈 NAV/Cluster + 誘몃뵒??肄쒖긽??寃쎈줈/?뚮쭏/?앹뾽/?ъ뒪 |
| powertrain | `0x300`, `0x301`, `0x302`, `0x303`, `0x304`, `0x305`, `0x306`, `0x307`, `0x308`, `0x309`, `0x30A` | 11 | ?쒕룞/湲곗뼱/?쇱슦??+ RPM/???곕즺/?ㅻ줈?/紐⑤뱶/由щ컠/?щ（利??ъ뒪 |

## 4) Powertrain Domain Status
- `emergency_system_powertrain.dbc`??scaffold ?곹깭瑜?醫낅즺?섍퀬 ?ㅼ젣 CAN ?꾨젅??3媛쒕? 諛섏쁺??
- 諛섏쁺 ?꾨젅?? `0x300~0x30A` 珥?11媛쒕줈 ?뺤옣.
- Req ?곌껐 ?섎룄: `Req_101`, `Req_102`, `Req_110`.

## 7) MET_30 ?뺥빀 泥댄겕 (DBC 愿??
- ?꾨찓??遺꾨━: ?꾨즺 (`chassis/body/infotainment/powertrain` 媛쒕퀎 DBC)
- ?꾨씫 ECU ?먭?(湲곗? ?명듃): ?꾨씫 ?놁쓬
- 硫붿떆吏 蹂쇰ⅷ: split ?⑷퀎 `44` (硫섑넗 沅뚭퀬 理쒖냼 `40` 異⑹”)
- 0303 ?뺤젙 Comm 諛섏쁺: `Comm_101~Comm_106` ?듭떖 ID(`0x300~0x304`)瑜?canonical `*_can.dbc` ?명듃??諛섏쁺

## 8) 0303 canonical ?뚯씪紐??뺥빀
- 臾몄꽌 ?뺤젙 ?뚯씪紐?`chassis_can.dbc`, `powertrain_can.dbc`, `body_can.dbc`, `infotainment_can.dbc`, `test_can.dbc`)???좉퇋 ?앹꽦.
- `project_profile.xml`??`<Databases>`????canonical ?뚯씪紐?湲곗??쇰줈 遺遺??섏젙 ?꾨즺.
- ?ㅽ뻾 湲곗? `CAN_500kBaud_1ch_split.cfg`??CANoe 吏곷젹???щ㎎ ?뱀꽦???섎룞(UI/API) 諛섏쁺 沅뚯옣.

## 5) Consistency Notes
- Ethernet contract remains out of DBC scope (meeting guidance reflected).
- Existing baseline file `emergency_system.dbc` is kept unchanged for compatibility.
- No files under `driving-situation-alert` were modified.

## 6) 2026-02-28 Pull 諛섏쁺 ?섎룞 ?뺥빀
- Pull 諛섏쁺 而ㅻ컠 踰붿쐞: `89ef104 -> 280aa5e`
- 蹂寃?臾몄꽌:
  - `driving-situation-alert/01_Requirements.md` (Req_101~Req_112 異붽?)
  - `driving-situation-alert/03_Function_definition.md`
  - `driving-situation-alert/0301_SysFuncAnalysis.md`
  - `driving-situation-alert/tmp/Domain_DBC_Split_Execution.md`
- ?섎룞 諛섏쁺 ?댁슜(?꾨찓??DBC ?몃뱶 ?뺥빀):
  - chassis: `ACCEL_CTRL`, `BRAKE_CTRL`, `STEERING_CTRL`, `VEHICLE_BASE_TEST_CTRL` 異붽?
  - body: `HAZARD_CTRL`, `WINDOW_CTRL`, `DRIVER_STATE_CTRL` 異붽?
  - infotainment: `NAV_CONTEXT_MGR`, `CLUSTER_BASE_CTRL` 異붽?
  - powertrain: `ENGINE_CTRL`, `TRANSMISSION_CTRL`, `DOMAIN_GW_ROUTER` 異붽?
- ?듯빀 DBC(`emergency_system.dbc`)???숈씪?섍쾶 Vehicle Baseline ?몃뱶 ?몃깽?좊━瑜?`BU_`/`CM_ BU_`??諛섏쁺
- ?꾩냽 ?뺥빀 二쇱쓽:
  - ?대쾲 ?뺤옣 ?꾨젅??0x102/0x103/0x211~0x213/0x221~0x222/0x300~0x302/0x231)? `0302/0303/0304` 臾몄꽌???ㅼ쓬 媛쒖젙?먯꽌 ?숈씪 ID/DLC/bit濡??숆린???꾩슂.

