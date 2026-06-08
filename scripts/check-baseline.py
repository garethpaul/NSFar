#!/usr/bin/env python3
"""Static baseline checks for the sparse NSFar archive."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-nsfar-artifact-baseline.md"
REQUIRED = [
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "docs/readme-overview.svg",
    PLAN,
    "gitfiti",
    "scripts/check-baseline.py",
]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def main():
    failures = []
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"required file missing: {path}")

    lines = read("gitfiti").splitlines()
    if len(lines) != 2889:
        failures.append("gitfiti artifact must stay at 2889 lines")
    invalid = [line for line in lines if not line.isdigit() or not 0 <= int(line) <= 17]
    if invalid:
        failures.append("gitfiti artifact must contain only integer rows from 0 through 17")
    if not {"0", "17"}.issubset(set(lines)):
        failures.append("gitfiti artifact must preserve the observed 0 through 17 range")

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in ["make check", "gitfiti", "numeric artifact", "2,889"]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "make check" not in plan:
        failures.append("plan must record completed status and verification")

    gitignore = read(".gitignore")
    for expected in [".env", "*.log", "tmp/"]:
        if expected not in gitignore:
            failures.append(f".gitignore must include {expected}")

    try:
        ET.parse(ROOT / "docs/readme-overview.svg")
    except ET.ParseError as error:
        failures.append(f"docs/readme-overview.svg must parse as XML: {error}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("NSFar archive baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
