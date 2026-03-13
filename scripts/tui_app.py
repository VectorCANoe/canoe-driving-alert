#!/usr/bin/env python3
"""Compatibility launcher for SDV operator Textual UI.

Canonical implementation moved to:
  product/sdv_operator/scripts/tui_app.py
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / "product" / "sdv_operator" / "scripts" / "tui_app.py"
    if not target.exists():
        print(f"[SDV][FAIL] missing target TUI: {target}", file=sys.stderr)
        return 2
    if str(target.parent) not in sys.path:
        sys.path.insert(0, str(target.parent))

    old_argv = sys.argv[:]
    sys.argv = [str(target), *old_argv[1:]]
    try:
        runpy.run_path(str(target), run_name="__main__")
        return 0
    except SystemExit as ex:
        code = ex.code
        if isinstance(code, int):
            return code
        if code is None:
            return 0
        return 1
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    raise SystemExit(main())
