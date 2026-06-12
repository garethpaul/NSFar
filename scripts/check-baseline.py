#!/usr/bin/env python3
"""Static baseline checks for the sparse NSFar archive."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-nsfar-artifact-baseline.md"
MANIFEST_PLAN = "docs/plans/2026-06-09-artifact-manifest.md"
SCHEMA_PLAN = "docs/plans/2026-06-09-manifest-schema-version.md"
LINE_ENDING_PLAN = "docs/plans/2026-06-09-artifact-line-endings.md"
FILE_MODE_PLAN = "docs/plans/2026-06-09-artifact-file-mode.md"
GITATTRIBUTES_PLAN = "docs/plans/2026-06-09-artifact-gitattributes.md"
DISTINCT_VALUES_PLAN = "docs/plans/2026-06-09-manifest-distinct-values.md"
MAKE_GATE_PLAN = "docs/plans/2026-06-09-make-gate-aliases.md"
BOUNDARY_VALUES_PLAN = "docs/plans/2026-06-09-manifest-boundary-values.md"
VALUE_COUNT_TOTAL_PLAN = "docs/plans/2026-06-10-manifest-value-count-total.md"
HOSTED_VALIDATION_PLAN = "docs/plans/2026-06-10-hosted-artifact-validation.md"
SEQUENCE_SHAPE_PLAN = "docs/plans/2026-06-10-manifest-sequence-shape.md"
MANIFEST = "docs/artifact-manifest.json"
EXPECTED_SHA256 = "89d4697d0d5d78624761159d4371a135124f4c10169e65018eb3b825afbb66d4"
REQUIRED = [
    ".github/CODEOWNERS",
    ".github/workflows/check.yml",
    ".gitattributes",
    ".gitignore",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    MANIFEST,
    "docs/readme-overview.svg",
    PLAN,
    MANIFEST_PLAN,
    SCHEMA_PLAN,
    LINE_ENDING_PLAN,
    FILE_MODE_PLAN,
    GITATTRIBUTES_PLAN,
    DISTINCT_VALUES_PLAN,
    MAKE_GATE_PLAN,
    BOUNDARY_VALUES_PLAN,
    VALUE_COUNT_TOTAL_PLAN,
    HOSTED_VALIDATION_PLAN,
    SEQUENCE_SHAPE_PLAN,
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

    artifact_path = ROOT / "gitfiti"
    artifact_bytes = artifact_path.read_bytes()
    if hashlib.sha256(artifact_bytes).hexdigest() != EXPECTED_SHA256:
        failures.append("gitfiti artifact checksum changed without a baseline update")
    indexed_artifact = subprocess.run(
        ["git", "ls-files", "--stage", "--", "gitfiti"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    indexed_mode = indexed_artifact.stdout.split(maxsplit=1)[0] if indexed_artifact.stdout else ""
    if indexed_artifact.returncode != 0 or indexed_mode != "100644":
        failures.append("gitfiti artifact must stay a non-executable 100644 file")
    if b"\r" in artifact_bytes:
        failures.append("gitfiti artifact must use LF line endings")
    if not artifact_bytes.endswith(b"\n"):
        failures.append("gitfiti artifact must preserve its terminal newline")

    lines = artifact_bytes.decode("ascii", errors="replace").splitlines()
    if len(lines) != 2889:
        failures.append("gitfiti artifact must stay at 2889 lines")
    invalid = [line for line in lines if not line.isdigit() or not 0 <= int(line) <= 17]
    if invalid:
        failures.append("gitfiti artifact must contain only integer rows from 0 through 17")
    if not {"0", "17"}.issubset(set(lines)):
        failures.append("gitfiti artifact must preserve the observed 0 through 17 range")

    manifest = json.loads(read(MANIFEST))
    if manifest.get("schemaVersion") != 1:
        failures.append("artifact manifest schemaVersion must be 1")

    value_counts = {}
    for line in lines:
        value_counts[line] = value_counts.get(line, 0) + 1
    values = [int(line) for line in lines]
    run_lengths = []
    current_run_length = 0
    previous_value = None
    for value in values:
        if value == 0:
            if current_run_length:
                run_lengths.append(current_run_length)
            current_run_length = 1
        elif previous_value is None or value != previous_value + 1:
            failures.append("gitfiti artifact must contain zero-based ascending runs")
            current_run_length += 1
        else:
            current_run_length += 1
        previous_value = value
    if current_run_length:
        run_lengths.append(current_run_length)
    run_length_counts = {}
    for length in run_lengths:
        key = str(length)
        run_length_counts[key] = run_length_counts.get(key, 0) + 1
    expected_manifest = {
        "path": "gitfiti",
        "encoding": "ascii",
        "format": "newline-delimited integers",
        "fileMode": "100644",
        "lineEnding": "LF",
        "trailingNewline": True,
        "sha256": EXPECTED_SHA256,
        "bytes": len(artifact_bytes),
        "lineCount": len(lines),
        "valueCountTotal": sum(value_counts.values()),
        "firstValue": int(lines[0]),
        "lastValue": int(lines[-1]),
        "minValue": min(int(line) for line in lines),
        "maxValue": max(int(line) for line in lines),
        "sequencePattern": "zero-based ascending runs",
        "runCount": len(run_lengths),
        "minRunLength": min(run_lengths),
        "maxRunLength": max(run_lengths),
        "runLengthCounts": run_length_counts,
        "distinctValues": sorted({int(line) for line in lines}),
        "valueCounts": value_counts,
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            failures.append(f"artifact manifest {key} must match gitfiti")

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in [
        "make lint",
        "make test",
        "make build",
        "make check",
        "gitfiti",
        "numeric artifact",
        "2,889",
        EXPECTED_SHA256,
        "artifact manifest",
        "schema version",
        "file mode",
        "line ending",
        "gitattributes",
        "distinct values",
        "boundary values",
        "value count total",
        "sequence shape",
        "run-length histogram",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    makefile = read("Makefile")
    for phrase in [
        ".PHONY: build check lint static-check test verify",
        "check: verify",
        "verify: static-check",
        "lint test build: static-check",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/check-baseline.py",
    ]:
        if phrase not in makefile:
            failures.append(f"Makefile must include standard gate alias: {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "make check" not in plan:
        failures.append("plan must record completed status and verification")
    manifest_plan = read(MANIFEST_PLAN)
    if "status: completed" not in manifest_plan or "artifact-manifest.json" not in manifest_plan:
        failures.append("manifest plan must record completed status and verification")
    schema_plan = read(SCHEMA_PLAN)
    if "status: completed" not in schema_plan or "schemaVersion" not in schema_plan:
        failures.append("schema plan must record completed status and verification")
    line_ending_plan = read(LINE_ENDING_PLAN)
    if "status: completed" not in line_ending_plan or "lineEnding" not in line_ending_plan:
        failures.append("line ending plan must record completed status and verification")
    file_mode_plan = read(FILE_MODE_PLAN)
    if "status: completed" not in file_mode_plan or "fileMode" not in file_mode_plan:
        failures.append("file mode plan must record completed status and verification")
    gitattributes_plan = read(GITATTRIBUTES_PLAN)
    if "status: completed" not in gitattributes_plan or ".gitattributes" not in gitattributes_plan:
        failures.append("gitattributes plan must record completed status and verification")
    distinct_values_plan = read(DISTINCT_VALUES_PLAN)
    if "status: completed" not in distinct_values_plan or "distinctValues" not in distinct_values_plan:
        failures.append("distinct values plan must record completed status and verification")
    make_gate_plan_path = ROOT / MAKE_GATE_PLAN
    make_gate_plan = make_gate_plan_path.read_text(encoding="utf-8") if make_gate_plan_path.exists() else ""
    if "status: completed" not in make_gate_plan or "make lint" not in make_gate_plan or "make build" not in make_gate_plan:
        failures.append("make gate alias plan must record completed status and verification")
    boundary_values_plan = read(BOUNDARY_VALUES_PLAN)
    if "status: completed" not in boundary_values_plan or "firstValue" not in boundary_values_plan or "lastValue" not in boundary_values_plan:
        failures.append("boundary values plan must record completed status and verification")
    value_count_total_plan = read(VALUE_COUNT_TOTAL_PLAN)
    if "status: completed" not in value_count_total_plan or "valueCountTotal" not in value_count_total_plan:
        failures.append("value count total plan must record completed status and verification")
    hosted_plan = read(HOSTED_VALIDATION_PLAN)
    workflow = read(".github/workflows/check.yml")
    codeowners = read(".github/CODEOWNERS")
    if "status: completed" not in hosted_plan or "make check" not in hosted_plan:
        failures.append("hosted artifact validation plan must record completed status and verification")
    sequence_shape_plan = read(SEQUENCE_SHAPE_PLAN)
    if "status: completed" not in sequence_shape_plan or "runLengthCounts" not in sequence_shape_plan:
        failures.append("sequence shape plan must record completed status and verification")
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "persist-credentials: false",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        'python-version: "3.12"',
        "run: make check",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")
    workflow_files = sorted(str(path.relative_to(ROOT)) for path in (ROOT / ".github/workflows").rglob("*") if path.is_file())
    if workflow_files != [".github/workflows/check.yml"]:
        failures.append("check.yml must be the repository's only hosted workflow")
    if codeowners.strip() != "* @garethpaul":
        failures.append("CODEOWNERS must assign the repository to @garethpaul")

    gitignore = read(".gitignore")
    for expected in [".env", "*.log", "tmp/"]:
        if expected not in gitignore:
            failures.append(f".gitignore must include {expected}")

    gitattributes = read(".gitattributes")
    for expected in [
        "gitfiti text eol=lf",
        "docs/artifact-manifest.json text eol=lf",
    ]:
        if expected not in gitattributes:
            failures.append(f".gitattributes must include {expected}")

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
