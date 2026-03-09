# OEM Canonical Alias Table (2026-03-09)

This table closes the remaining non-OEM-style visible surface names in `canoe/`.

Rule:
- use direct HKG/OEM abbreviations when they exist
- when no stable OEM abbreviation was found in local references, use a short project canonical alias for visible node names
- full names remain documentation aliases only

| Previous Visible Name | Canonical Short Name | Basis |
|---|---|---|
| `AEB_DOMAIN` | `AEB` | HKG reference uses AEB signal/function naming |
| `AUTO_DOOR_CTRL` | `ADM` | short project alias for auto door module |
| `BODY_SECURITY_MODULE` | `BSEC` | short project alias to avoid collision with BCW/BSM-style names |
| `CARPAY_CTRL` | `CPAY` | short project alias |
| `CHARGE_PORT_CTRL` | `CPC` | short project alias for charge port controller |
| `ETH_BACKBONE` | `ETHB` | short project alias for ethernet backbone service |
| `MASSAGE_SEAT_CTRL` | `MSC` | short project alias |
| `MIRROR_MODULE` | `MIR` | short project alias |
| `NAV_MODULE` | `NAV` | short project alias |
| `OTA_MASTER` | `OTA` | short project alias |
| `PARK_MASTER` | `PKM` | short project alias for park master |
| `PARK_ULTRASONIC` | `PUS` | short project alias for ultrasonic parking controller |
| `POWER_TAILGATE_CTRL` | `PTG` | short project alias |
| `REAR_CLIMATE_MODULE` | `RATC` | rear auto temperature control style alias |
| `REAR_RADAR_MASTER` | `RRM` | short project alias |
| `ROAD_PREVIEW_CAMERA` | `RPC` | short project alias |
| `SUNROOF_MODULE` | `SRF` | short project alias |
| `SURROUND_PARK_MASTER` | `SPM` | short project alias |
| `TAILGATE_MODULE` | `TGM` | short project alias |
| `TRAILER_CTRL` | `TRM` | short project alias |
| `VOICE_ASSIST` | `VCS` | voice control system short alias |
| `WIPER_MODULE` | `WIP` | short project alias |
| `PHONE_AS_KEY` | `PAK` | short project alias |

