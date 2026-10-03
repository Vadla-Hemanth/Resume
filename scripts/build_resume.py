#!/usr/bin/env python3
"""Build or check the resume and its original-filename download copy."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "design" / "build_resume.py"
PDF = ROOT / "website" / "assets" / "Vadla-Hemanth-Resume.pdf"
COMPATIBILITY_PDF = ROOT / "VADLA HEMANTH RESUME.pdf"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate all outputs without overwriting files.",
    )
    args = parser.parse_args()
    command = [sys.executable, "-B", str(BUILDER)]
    if args.check:
        command.append("--check")
    result = subprocess.run(command, check=False)
    if result.returncode:
        return result.returncode

    if args.check:
        if not COMPATIBILITY_PDF.is_file() or COMPATIBILITY_PDF.read_bytes() != PDF.read_bytes():
            print(
                f"Missing or out-of-date compatibility PDF: {COMPATIBILITY_PDF}",
                file=sys.stderr,
            )
            return 1
    else:
        shutil.copyfile(PDF, COMPATIBILITY_PDF)
    print("Original-filename PDF matches the canonical PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
