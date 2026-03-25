# Ethernet Backbone Interface Specification 안내본

원문:
- [../../contracts/ethernet-backbone.md](../../contracts/ethernet-backbone.md)

상태:
- 이 문서는 canonical 원문이 이미 한국어 중심으로 작성되어 있습니다.
- 따라서 본 안내본은 별도 번역 복제본이 아니라 `한글팩 구조 안에서 canonical 문서로 연결하기 위한 진입점`입니다.

## 이 문서에서 확인할 것

- active Ethernet backbone contract의 단일 원본
- UDP multicast `239.0.2.1:5000` 기준
- `0x510/0x511/0x512`, `0xE100`, `0xE200`, `0xE210~0xE216`, `0x1C2`의 signal contract
- validation result sysvar seam
- `0302 -> 0303 -> 0304 -> 04 -> 05/06/07` 업데이트 순서

## 바로 가기

- canonical 문서 열기: [../../contracts/ethernet-backbone.md](../../contracts/ethernet-backbone.md)
- 관련 interface 문서: [../../contracts/ethernet-interface.md](../../contracts/ethernet-interface.md)
- 관련 matrix 문서: [./communication-matrix.md](./communication-matrix.md)
