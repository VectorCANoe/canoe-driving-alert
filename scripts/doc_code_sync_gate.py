#!/usr/bin/env python3
"""
Compatibility wrapper.
Use: python scripts/quality/doc_code_sync_gate.py
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    target = Path(__file__).resolve().parent / "quality" / "doc_code_sync_gate.py"
    module_globals = runpy.run_path(str(target))
    return int(module_globals["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
