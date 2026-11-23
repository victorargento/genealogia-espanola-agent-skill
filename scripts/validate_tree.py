#!/usr/bin/env python3
"""Compatibility entry point for the canonical skill tool."""
import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    tool = Path(__file__).resolve().parents[1] / "skills" / "investigacion-genealogica-es" / "scripts" / "genealogy_tool.py"
    sys.argv = [str(tool), "validate", *sys.argv[1:]]
    runpy.run_path(str(tool), run_name="__main__")
