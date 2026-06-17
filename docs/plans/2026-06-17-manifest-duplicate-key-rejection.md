# Manifest Duplicate-Key Rejection

Status: planned

## Problem

Python's default JSON parser silently keeps the last value when an object repeats
a key. An ambiguous archive manifest can therefore contain duplicate top-level
or nested keys while still appearing to satisfy the exact key and value checks.

## Requirements

- Reject duplicate JSON object keys before any schema or artifact comparison.
- Apply the duplicate-key rule recursively to top-level and nested objects.
- Return a controlled manifest diagnostic that names the duplicate key without
  exposing a traceback.
- Preserve malformed JSON handling, exact JSON value types, schema closure,
  artifact checksums, file modes, line endings, sequence shape, and Git probes.
- Add mutation-sensitive portable contracts and synchronized guidance.

## Implementation Units

### U1: Duplicate-aware manifest parsing

Files:

- `scripts/check-baseline.py`

Parse JSON objects through an ordered-pair hook that raises a controlled error
when a key appears more than once. Keep the existing top-level object guard and
error-return contract.

Test scenarios:

- The current manifest parses and validates unchanged.
- A duplicated top-level key is rejected even when its final value is correct.
- A duplicated nested `valueCounts` or `runLengthCounts` key is rejected.
- Malformed JSON and non-object top-level values retain controlled diagnostics.

### U2: Integrity guidance and evidence

Files:

- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-17-manifest-duplicate-key-rejection.md`

Document that exact manifest integrity includes recursive duplicate-key
rejection and record the actual completed verification.

## Validation

- Run checker compilation and all Make aliases from the checkout, plus the
  absolute Makefile check from an external directory.
- Run focused duplicate-key probes and isolated hostile mutations for parser,
  nested-object, guidance, and completed-plan requirements.
- Audit the exact diff, generated artifacts, secret signatures, conflict
  markers, binaries, large files, modes, and whitespace before committing.

## Risks

- This intentionally rejects JSON that permissive parsers may accept; duplicate
  keys are ambiguous and are not part of the protected manifest contract.
- Integrity remains repository-local and does not establish external provenance.
- This change is stacked on PR #11, which must remain open and merge first.
