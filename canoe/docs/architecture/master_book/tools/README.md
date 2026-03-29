# Master Book Tools

These tracked scripts regenerate the official `master_book` asset pack in place.

## Files

- `build_master_book_asset_pack.py`
  - builds the ECU metadata dataset, grouped SVG figures, action-flow figures, and 101 ECU cards
- `render_master_book_pdf.py`
  - converts the generated markdown master book into HTML and PDF

## Standard Order

1. `python tools/build_master_book_asset_pack.py`
2. `python tools/render_master_book_pdf.py`

## Output Root

All generated outputs land in `canoe/docs/architecture/master_book/**`.

Archived prototype studies now live under `canoe/docs/architecture/master_book/prototypes/card_prototypes/`.
They are preserved for layout reference only and are not used by the standard build/render flow.
