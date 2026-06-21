#!/usr/bin/env python3
"""Static baseline checks for the sparse NSFar archive."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAKEFILE = """override SHELL := /bin/sh
override .SHELLFLAGS := -c
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must not be set)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell MAKEFILE_LIST_RAW='$(subst ','"'"',$(MAKEFILE_LIST))' python3 -c "import os; raw = os.environ['MAKEFILE_LIST_RAW']; candidates = [raw] + [raw[index + 1:] for index, char in enumerate(raw) if char == ' ']; path = next((candidate for candidate in candidates if (candidate == 'Makefile' or candidate.endswith('/Makefile')) and os.path.isfile(os.path.abspath(candidate))), None); assert path is not None, 'trusted Makefile path not found'; print(os.path.dirname(os.path.abspath(path)))")

.PHONY: build check lint static-check test verify

override PYTHON := python3
build check lint static-check test verify: override ROOT := $(ROOT)
build check lint static-check test verify: override PYTHON := $(PYTHON)

check: verify

verify: static-check test

lint build: static-check

test:
\tPYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/test-check-baseline.py"

static-check:
\tPYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/check-baseline.py"
"""
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
SCHEMA_CLOSURE_PLAN = "docs/plans/2026-06-12-manifest-schema-closure.md"
CHECKOUT_CREDENTIAL_PLAN = "docs/plans/2026-06-12-checkout-credential-boundary.md"
PROVENANCE_PLAN = "docs/plans/2026-06-13-artifact-construction-provenance.md"
LOCATION_INDEPENDENT_MAKE_PLAN = "docs/plans/2026-06-13-location-independent-make.md"
MALFORMED_ARTIFACT_PLAN = "docs/plans/2026-06-14-malformed-artifact-diagnostics.md"
MALFORMED_MANIFEST_PLAN = "docs/plans/2026-06-14-malformed-manifest-diagnostics.md"
MISSING_REQUIRED_FILE_PLAN = "docs/plans/2026-06-15-missing-required-file-diagnostics.md"
GIT_PROBE_PLAN = "docs/plans/2026-06-15-git-probe-diagnostics.md"
UNREADABLE_ARTIFACT_PLAN = "docs/plans/2026-06-15-unreadable-artifact-diagnostics.md"
MANIFEST_VALUE_TYPE_PLAN = "docs/plans/2026-06-16-manifest-value-type-closure.md"
MANIFEST_DUPLICATE_KEY_PLAN = "docs/plans/2026-06-17-manifest-duplicate-key-rejection.md"
MANIFEST = "docs/artifact-manifest.json"
EXPECTED_SHA256 = "89d4697d0d5d78624761159d4371a135124f4c10169e65018eb3b825afbb66d4"
REQUIRED = [
    ".github/CODEOWNERS",
    ".github/workflows/check.yml",
    ".gitattributes",
    ".gitignore",
    "CHANGES.md",
    "AGENTS.md",
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
    SCHEMA_CLOSURE_PLAN,
    CHECKOUT_CREDENTIAL_PLAN,
    PROVENANCE_PLAN,
    LOCATION_INDEPENDENT_MAKE_PLAN,
    MALFORMED_ARTIFACT_PLAN,
    MALFORMED_MANIFEST_PLAN,
    MISSING_REQUIRED_FILE_PLAN,
    GIT_PROBE_PLAN,
    UNREADABLE_ARTIFACT_PLAN,
    MANIFEST_VALUE_TYPE_PLAN,
    MANIFEST_DUPLICATE_KEY_PLAN,
    "docs/artifact-provenance.md",
    "gitfiti",
    "scripts/check-baseline.py",
    "scripts/test-check-baseline.py",
]


def read(relative_path):
    try:
        return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def read_artifact_bytes(path):
    try:
        return path.read_bytes(), None
    except OSError as error:
        return b"", f"protected artifact could not be read: {error}"


def parse_artifact_values(lines):
    values = []
    invalid = []
    for line in lines:
        if not line.isdigit():
            invalid.append(line)
            continue
        value = int(line)
        if not 0 <= value <= 17:
            invalid.append(line)
            continue
        values.append(value)
    return (None, invalid) if invalid else (values, [])


def reject_duplicate_object_pairs(pairs):
    parsed = {}
    for key, value in pairs:
        if key in parsed:
            raise ValueError(f"duplicate object key: {key}")
        parsed[key] = value
    return parsed


def exceeds_json_nesting_limit(text, maximum_depth=100):
    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > maximum_depth:
                return True
        elif character in "]}":
            depth -= 1
    return False


def parse_manifest(text):
    if exceeds_json_nesting_limit(text):
        return None, "maximum JSON nesting depth exceeded"
    try:
        manifest = json.loads(text, object_pairs_hook=reject_duplicate_object_pairs)
    except RecursionError:
        return None, "maximum JSON nesting depth exceeded"
    except (TypeError, ValueError) as error:
        return None, str(error)
    if not isinstance(manifest, dict):
        return None, "top-level JSON value must be an object"
    return manifest, None


def same_json_value(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            same_json_value(actual[key], value) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            same_json_value(actual_value, expected_value)
            for actual_value, expected_value in zip(actual, expected)
        )
    return actual == expected


def read_indexed_mode(relative_path):
    try:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", relative_path],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except UnicodeError:
        return "", "git index probe returned undecodable output"
    except OSError as error:
        return "", f"git index probe could not start: {error}"
    if result.returncode != 0:
        return "", f"git index probe exited with status {result.returncode}"
    match = re.fullmatch(
        r"(?P<mode>[0-7]{6}) [0-9a-fA-F]{40,64} 0\t[^\r\n]+\n?",
        result.stdout,
    )
    if not match:
        return "", "git index probe returned malformed output"
    return match.group("mode"), None


def read_workflow_files():
    workflow_directory = ROOT / ".github/workflows"
    try:
        files = sorted(
            path.relative_to(ROOT).as_posix()
            for path in workflow_directory.iterdir()
            if path.is_file()
        )
    except OSError as error:
        return [], f"workflow inventory could not be read: {error}"
    return files, None


def checkout_workflow_failures(workflow):
    failures = []
    lines = workflow.splitlines()
    checkout_pattern = re.compile(r"^(?P<indent>\s*)-\s+uses:\s+actions/checkout@(?P<ref>\S+)\s*$")
    checkout_steps = []
    for index, line in enumerate(lines):
        match = checkout_pattern.fullmatch(line)
        if match:
            checkout_steps.append((index, len(match.group("indent")), match.group("ref")))

    expected_ref = "df4cb1c069e1874edd31b4311f1884172cec0e10"
    if len(checkout_steps) != 1 or checkout_steps[0][2] != expected_ref:
        return ["Check workflow must keep one pinned credential-free checkout step"]

    start, step_indent, _ = checkout_steps[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and len(line) - len(line.lstrip()) <= step_indent:
            end = index
            break
    step_lines = lines[start + 1:end]
    expected_with = " " * (step_indent + 2) + "with:"
    expected_credentials = (
        " " * (step_indent + 4) + "persist-credentials: false"
    )
    if step_lines.count(expected_with) != 1:
        failures.append("checkout step must contain exactly one with mapping")
        return failures
    if step_lines != [expected_with, expected_credentials]:
        failures.append(
            "checkout step must contain only the credential-free with mapping"
        )
    return failures


def build_value_manifest(values, failures):
    if not values:
        return {}

    value_counts = {}
    for value in values:
        key = str(value)
        value_counts[key] = value_counts.get(key, 0) + 1
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
    return {
        "valueCountTotal": len(values),
        "firstValue": values[0],
        "lastValue": values[-1],
        "minValue": min(values),
        "maxValue": max(values),
        "sequencePattern": "zero-based ascending runs",
        "runCount": len(run_lengths),
        "minRunLength": min(run_lengths),
        "maxRunLength": max(run_lengths),
        "runLengthCounts": run_length_counts,
        "distinctValues": sorted(set(values)),
        "valueCounts": value_counts,
    }


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def main():
    failures = []
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"required file missing: {path}")

    artifact_path = ROOT / "gitfiti"
    artifact_bytes = b""
    artifact_read_error = None
    if artifact_path.is_file():
        artifact_bytes, artifact_read_error = read_artifact_bytes(artifact_path)
    if artifact_read_error:
        failures.append(f"gitfiti artifact read failed: {artifact_read_error}")
    if hashlib.sha256(artifact_bytes).hexdigest() != EXPECTED_SHA256:
        failures.append("gitfiti artifact checksum changed without a baseline update")
    indexed_mode, index_probe_error = read_indexed_mode("gitfiti")
    if index_probe_error:
        failures.append(f"gitfiti artifact index mode probe failed: {index_probe_error}")
    if indexed_mode != "100644":
        failures.append("gitfiti artifact must stay a non-executable 100644 file")
    if b"\r" in artifact_bytes:
        failures.append("gitfiti artifact must use LF line endings")
    if not artifact_bytes.endswith(b"\n"):
        failures.append("gitfiti artifact must preserve its terminal newline")

    lines = artifact_bytes.decode("ascii", errors="replace").splitlines()
    if len(lines) != 2889:
        failures.append("gitfiti artifact must stay at 2889 lines")
    values, invalid = parse_artifact_values(lines)
    if invalid:
        failures.append("gitfiti artifact must contain only integer rows from 0 through 17")
    if values is not None and not {0, 17}.issubset(set(values)):
        failures.append("gitfiti artifact must preserve the observed 0 through 17 range")

    malformed_values, malformed_rows = parse_artifact_values(
        ["0", "not-an-integer", "18"]
    )
    if malformed_values is not None or malformed_rows != ["not-an-integer", "18"]:
        failures.append("artifact value parser must reject malformed rows without partial values")
    sample_values, sample_invalid = parse_artifact_values(["0", "1", "17"])
    if sample_values != [0, 1, 17] or sample_invalid:
        failures.append("artifact value parser must preserve valid rows")
    invalid_manifest = build_value_manifest(None, [])
    empty_manifest = build_value_manifest([], [])
    if invalid_manifest != {} or empty_manifest != {}:
        failures.append("artifact manifest derivation must ignore invalid or empty value sets")
    malformed_manifest, malformed_manifest_error = parse_manifest("{")
    if malformed_manifest is not None or not malformed_manifest_error:
        failures.append("manifest parser must reject malformed JSON without raising")
    non_object_manifest, non_object_manifest_error = parse_manifest("[]")
    if non_object_manifest is not None or non_object_manifest_error != "top-level JSON value must be an object":
        failures.append("manifest parser must reject non-object JSON values")
    sample_manifest, sample_manifest_error = parse_manifest('{"schemaVersion": 1}')
    if sample_manifest != {"schemaVersion": 1} or sample_manifest_error is not None:
        failures.append("manifest parser must preserve valid JSON objects")
    duplicate_manifest, duplicate_manifest_error = parse_manifest(
        '{"schemaVersion": 0, "schemaVersion": 1}'
    )
    if duplicate_manifest is not None or duplicate_manifest_error != "duplicate object key: schemaVersion":
        failures.append("manifest parser must reject duplicate top-level object keys")
    nested_duplicate_manifest, nested_duplicate_manifest_error = parse_manifest(
        '{"valueCounts": {"0": 1, "0": 318}}'
    )
    if nested_duplicate_manifest is not None or nested_duplicate_manifest_error != "duplicate object key: 0":
        failures.append("manifest parser must reject duplicate nested object keys")
    if (same_json_value(True, 1) or same_json_value(1.0, 1) or
            same_json_value([1, True], [1, 1]) or
            same_json_value({"count": 1.0}, {"count": 1}) or
            not same_json_value({"counts": [1, 2]}, {"counts": [1, 2]})):
        failures.append("manifest value comparison must preserve exact recursive JSON types")
    checker_source = read("scripts/check-baseline.py")
    for required_missing_file_contract in [
        'except OSError:\n        return ""',
        "if artifact_path.is_" + "file():",
        "except (ET.ParseError, OSError) as error:",
    ]:
        if required_missing_file_contract not in checker_source:
            failures.append(
                "checker must preserve controlled missing-file contract: "
                + required_missing_file_contract
            )
    for required_git_probe_contract in [
        "def read_" + "indexed_mode(relative_path):",
        'except OSError as error:\n        return "", f"git index probe could not '
        + 'start: {error}"',
        "if result.returncode != " + "0:",
        'indexed_mode, index_probe_error = read_' + 'indexed_mode("gitfiti")',
    ]:
        if required_git_probe_contract not in checker_source:
            failures.append(
                "checker must preserve controlled git-probe contract: "
                + required_git_probe_contract
            )
    for required_artifact_read_contract in [
        "def read_" + "artifact_bytes(path):",
        'except OSError as error:\n        return b"", f"protected artifact could not '
        + 'be read: {error}"',
        "artifact_bytes, artifact_read_error = read_"
        + "artifact_bytes(artifact_path)",
        'failures.append(f"gitfiti artifact read failed: '
        + '{artifact_read_error}")',
    ]:
        if required_artifact_read_contract not in checker_source:
            failures.append(
                "checker must preserve controlled artifact-read contract: "
                + required_artifact_read_contract
            )
    for required_manifest_contract in [
        "parse_" + 'manifest("{")',
        "parse_" + 'manifest("[]")',
        "object_pairs_hook=" + "reject_duplicate_object_pairs",
        'raise ValueError(f"duplicate object key: {key}")',
        'duplicate_manifest_error != "duplicate object key: schemaVersion"',
        'nested_duplicate_manifest_error != "duplicate object key: 0"',
        "isinstance(manifest, " + "dict)",
        "manifest, manifest_error = " + "parse_manifest(read(MANIFEST))",
        "manifest = " + "{}",
    ]:
        if required_manifest_contract not in checker_source:
            failures.append(
                "checker must preserve safe manifest parsing contract: "
                + required_manifest_contract
            )
    for required_type_contract in [
        "if type(actual) is not " + "type(expected):",
        "same_json_" + "value(actual[key], value)",
        "same_json_" + "value(actual_value, expected_value)",
        'if not same_json_' + 'value(manifest.get("schemaVersion"), 1):',
        "if not same_json_" + "value(manifest.get(key), expected):",
    ]:
        if required_type_contract not in checker_source:
            failures.append(
                "checker must preserve exact manifest value type contract: "
                + required_type_contract
            )
    manifest, manifest_error = parse_manifest(read(MANIFEST))
    if manifest_error:
        failures.append(f"artifact manifest must contain a valid JSON object: {manifest_error}")
        manifest = {}
    if not same_json_value(manifest.get("schemaVersion"), 1):
        failures.append("artifact manifest schemaVersion must be 1")

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
    }
    expected_manifest_keys = {
        "schemaVersion", "path", "encoding", "format", "fileMode",
        "lineEnding", "trailingNewline", "sha256", "bytes", "lineCount",
        "valueCountTotal", "firstValue", "lastValue", "minValue", "maxValue",
        "sequencePattern", "runCount", "minRunLength", "maxRunLength",
        "runLengthCounts", "distinctValues", "valueCounts",
    }
    expected_manifest.update(build_value_manifest(values, failures))
    missing_manifest_keys = sorted(expected_manifest_keys - manifest.keys())
    unexpected_manifest_keys = sorted(manifest.keys() - expected_manifest_keys)
    if missing_manifest_keys:
        failures.append(
            "artifact manifest is missing schema keys: "
            + ", ".join(missing_manifest_keys)
        )
    if unexpected_manifest_keys:
        failures.append(
            "artifact manifest has unexpected schema keys: "
            + ", ".join(unexpected_manifest_keys)
        )
    for key, expected in expected_manifest.items():
        if not same_json_value(manifest.get(key), expected):
            failures.append(f"artifact manifest {key} must match gitfiti")

    readme = read("README.md")
    docs = "\n".join([readme, read("SECURITY.md"), read("VISION.md")])
    location_independent_make_plan = read(LOCATION_INDEPENDENT_MAKE_PLAN)
    if "make -f /path/to/NSFar/Makefile check" not in readme:
        failures.append("README must document location-independent Makefile invocation")
    if not all(
        evidence in location_independent_make_plan.lower()
        for evidence in [
            "status: completed",
            "root and external-directory",
            "six isolated hostile mutations",
        ]
    ):
        failures.append(
            "location-independent Make plan must record completed root, external, and mutation verification"
        )
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
        "exact key set",
        "docs/artifact-provenance.md",
        "construction history is not a reproduction recipe",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    provenance = " ".join(read("docs/artifact-provenance.md").split())
    for phrase in [
        "Construction status: partially established",
        "exactly 2,889 commits",
        "Each commit added one line to the file and deleted none",
        "425882d4734218b7fc5b5f672611d671b22c93b7",
        "5b41cbeb9e52af1e0ac449b779b8ff06c212f4f1",
        "2013-12-08T12:00:00-08:00",
        "2014-11-29T12:00:00-08:00",
        "does not establish the generator, source instructions, or intended rendered pattern",
        "Author and committer dates are repository metadata",
        "schema version 1 manifest is intentionally unchanged",
        "A shallow hosted checkout cannot reproduce the history counts",
    ]:
        if phrase not in provenance:
            failures.append(f"artifact provenance must include {phrase}")
    if "[`docs/artifact-provenance.md`](docs/artifact-provenance.md)" not in read("README.md"):
        failures.append("README must link the artifact provenance note")

    makefile = read("Makefile")
    if makefile != EXPECTED_MAKEFILE:
        failures.append(
            "Makefile must exactly preserve rooted dependency-free aliases and the Python override"
        )

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
    make_gate_plan = read(MAKE_GATE_PLAN)
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
    if "status: completed" not in hosted_plan or "make check" not in hosted_plan:
        failures.append("hosted artifact validation plan must record completed status and verification")
    sequence_shape_plan = read(SEQUENCE_SHAPE_PLAN)
    if "status: completed" not in sequence_shape_plan or "runLengthCounts" not in sequence_shape_plan:
        failures.append("sequence shape plan must record completed status and verification")
    schema_closure_plan = read(SCHEMA_CLOSURE_PLAN)
    if "status: completed" not in schema_closure_plan or "unexpected manifest key" not in schema_closure_plan:
        failures.append("manifest schema closure plan must record completed status and verification")
    checkout_credential_plan = read(CHECKOUT_CREDENTIAL_PLAN)
    if (
        "status: completed" not in checkout_credential_plan
        or "persist-credentials: false" not in checkout_credential_plan
        or "hostile mutations rejected" not in checkout_credential_plan
    ):
        failures.append("checkout credential plan must record completed status and verification")
    provenance_plan = read(PROVENANCE_PLAN)
    provenance_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", provenance_plan)
    provenance_work = markdown_section(provenance_plan, "Work Completed")
    provenance_verification = markdown_section(provenance_plan, "Verification Completed")
    if provenance_status != ["completed"] or not provenance_work:
        failures.append("artifact provenance plan must record completed status and work")
    if not provenance_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", provenance_verification
    ):
        failures.append("artifact provenance plan must record completed verification")
    for evidence in [
        "2,889 commits",
        "2,889 additions and zero deletions",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "hostile mutations rejected",
        "git diff --check",
    ]:
        if evidence not in provenance_verification:
            failures.append(f"artifact provenance verification must record {evidence}")
    malformed_plan = read(MALFORMED_ARTIFACT_PLAN)
    malformed_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", malformed_plan)
    malformed_work = markdown_section(malformed_plan, "Work Completed")
    malformed_verification = markdown_section(malformed_plan, "Verification Completed")
    if (malformed_status != ["completed"] or not malformed_work or
            not malformed_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                malformed_verification,
            )):
        failures.append("malformed artifact diagnostics plan must record completed work and verification")
    for evidence in [
        "controlled nonzero result without a traceback",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "hostile mutations",
        "git diff --check",
    ]:
        if evidence not in malformed_verification:
            failures.append(f"malformed artifact verification must record {evidence}")
    malformed_manifest_plan = read(MALFORMED_MANIFEST_PLAN)
    malformed_manifest_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", malformed_manifest_plan
    )
    malformed_manifest_work = markdown_section(
        malformed_manifest_plan, "Work Completed"
    )
    malformed_manifest_verification = markdown_section(
        malformed_manifest_plan, "Verification Completed"
    )
    if (malformed_manifest_status != ["completed"] or
            not malformed_manifest_work or
            not malformed_manifest_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                malformed_manifest_verification,
            )):
        failures.append("malformed manifest diagnostics plan must record completed work and verification")
    for evidence in [
        "controlled nonzero result without a traceback",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "hostile mutations",
        "git diff --check",
    ]:
        if evidence not in malformed_manifest_verification:
            failures.append(f"malformed manifest verification must record {evidence}")
    missing_file_plan = read(MISSING_REQUIRED_FILE_PLAN)
    missing_file_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", missing_file_plan)
    missing_file_verification = markdown_section(
        missing_file_plan, "Verification Completed"
    )
    if (missing_file_status != ["completed"] or not missing_file_verification or
            re.search(r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b", missing_file_verification)):
        failures.append("missing required file plan must record completed verification")
    for evidence in [
        "missing artifact, manifest, README, and SVG",
        "status 1 without a traceback",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "Six isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in missing_file_verification:
            failures.append(f"missing required file verification must record {evidence}")
    git_probe_plan = read(GIT_PROBE_PLAN)
    git_probe_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", git_probe_plan)
    git_probe_work = markdown_section(git_probe_plan, "Work Completed")
    git_probe_verification = markdown_section(git_probe_plan, "Verification Completed")
    if (git_probe_status != ["completed"] or not git_probe_work or
            not git_probe_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                git_probe_verification,
            )):
        failures.append("git probe diagnostics plan must record completed work and verification")
    for evidence in [
        "status 1 with a named git-probe diagnostic and without a traceback",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "Six isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in git_probe_verification:
            failures.append(f"git probe verification must record {evidence}")
    unreadable_artifact_plan = read(UNREADABLE_ARTIFACT_PLAN)
    unreadable_artifact_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", unreadable_artifact_plan
    )
    unreadable_artifact_work = markdown_section(
        unreadable_artifact_plan, "Work Completed"
    )
    unreadable_artifact_verification = markdown_section(
        unreadable_artifact_plan, "Verification Completed"
    )
    unreadable_artifact_verification_normalized = " ".join(
        unreadable_artifact_verification.split()
    )
    if (unreadable_artifact_status != ["completed"] or not unreadable_artifact_work or
            not unreadable_artifact_verification or re.search(
                r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
                unreadable_artifact_verification,
            )):
        failures.append("unreadable artifact diagnostics plan must record completed work and verification")
    for evidence in [
        "status 1 with a named artifact-read diagnostic and without a traceback",
        "independent checksum and row findings",
        "python3 -m py_compile scripts/check-baseline.py",
        "make lint",
        "make test",
        "make build",
        "make check",
        "external working directory",
        "Six isolated hostile mutations",
        "git diff --check",
    ]:
        if evidence not in unreadable_artifact_verification_normalized:
            failures.append(f"unreadable artifact verification must record {evidence}")
    manifest_type_plan = read(MANIFEST_VALUE_TYPE_PLAN)
    manifest_type_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", manifest_type_plan)
    manifest_type_verification = markdown_section(
        manifest_type_plan, "Verification Completed"
    )
    if (manifest_type_status != ["completed"] or not manifest_type_verification or
            "All four Make gates passed" not in manifest_type_verification or
            "Ten isolated hostile mutations were rejected" not in manifest_type_verification or
            "external directory" not in manifest_type_verification or
            re.search(r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b", manifest_type_verification)):
        failures.append("manifest value type closure plan must record completed verification")
    duplicate_key_plan = read(MANIFEST_DUPLICATE_KEY_PLAN)
    duplicate_key_verification = markdown_section(
        duplicate_key_plan, "Verification Completed"
    )
    if not (
        "status: completed" in duplicate_key_plan.lower()
        and "All four Make gates passed" in duplicate_key_verification
        and "Seven isolated hostile mutations were rejected" in duplicate_key_verification
        and "external directory" in duplicate_key_verification
        and "duplicate" in duplicate_key_verification.lower()
        and not re.search(
            r"(?i)\b(?:pending|todo|tbd|not run|to be recorded)\b",
            duplicate_key_verification,
        )
    ):
        failures.append("manifest duplicate-key rejection plan must record completed verification")
    workflow_files, workflow_inventory_error = read_workflow_files()
    if workflow_inventory_error:
        failures.append(workflow_inventory_error)
    if workflow_files != [".github/workflows/check.yml"]:
        failures.append("workflow inventory must contain only .github/workflows/check.yml")
    failures.extend(checkout_workflow_failures(workflow))
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        'python-version: "3.12"',
        "run: make check",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")

    docs = " ".join(
        "\n".join(
            read(path) for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]
        ).split()
    )
    for phrase in [
        "checkout credentials are not persisted",
        "credential-free checkout",
        "malformed artifact rows fail cleanly without traceback output",
        "malformed artifact manifests fail cleanly without traceback output",
        "missing required files fail cleanly without traceback output",
        "Git index probe failures fail cleanly without traceback output",
        "Unreadable protected artifacts fail cleanly without traceback output",
    ]:
        if phrase not in docs:
            failures.append(f"repository guidance must mention {phrase}")
    guidance_documents = [
        " ".join(read(path).lower().split())
        for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]
    ]
    if not all(
        "malformed artifact manifests fail cleanly without traceback output"
        in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document controlled malformed manifest diagnostics"
        )
    if not all(
        "missing required files fail cleanly without traceback output"
        in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document controlled missing-file diagnostics"
        )
    if not all(
        "git index probe failures fail cleanly without traceback output"
        in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document controlled git-probe diagnostics"
        )
    if not all(
        "unreadable protected artifacts fail cleanly without traceback output"
        in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document controlled artifact-read diagnostics"
        )
    if not all(
        "manifest value type closure" in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document manifest value type closure"
        )
    if not all(
        "manifest duplicate-key rejection" in document
        for document in guidance_documents
    ):
        failures.append(
            "all repository guidance must document manifest duplicate-key rejection"
        )

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
    except (ET.ParseError, OSError) as error:
        failures.append(f"docs/readme-overview.svg must parse as XML: {error}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("NSFar archive baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
