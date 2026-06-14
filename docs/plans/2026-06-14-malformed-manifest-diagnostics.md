# Malformed Manifest Diagnostics

status: in_progress

## Context

The checker now reports malformed artifact rows without a traceback, but it
still loads `docs/artifact-manifest.json` through an unguarded `json.loads`.
Malformed JSON can therefore terminate validation before the checker reports
the independent artifact, documentation, workflow, and repository findings.

## Priorities

1. Report malformed manifest JSON as a controlled checker failure.
2. Continue independent fixed artifact and repository checks after the load
   failure.
3. Preserve all valid schema version 1 manifest behavior.
4. Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.

## Implementation Units

### Manifest Loader

File: `scripts/check-baseline.py`

- Parse manifest text through a helper that returns a diagnostic instead of
  raising.
- Require the decoded top-level value to be an object before schema checks.
- Use an empty object after a controlled load failure so fixed checks continue.

### Regression Contract

File: `scripts/check-baseline.py`

- Exercise malformed JSON, a non-object JSON value, and a valid object in
  memory.
- Require completed plan evidence and the safe loader call in the maintained
  checker.

### Documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`

- Document controlled malformed-manifest diagnostics and the unchanged
  protected artifact boundary.

## Verification Planned

- Reproduce malformed manifest JSON in a disposable indexed copy and confirm a
  normal nonzero result without traceback output.
- Run Python compilation and all four Make aliases from the checkout.
- Run the absolute Makefile check from an external directory.
- Reject isolated mutations of loader use, malformed/non-object fixtures,
  documentation, and completed plan evidence.
- Confirm the protected artifact and manifest hashes and modes are unchanged.
- Run diff, generated-artifact, conflict-marker, and changed-line secret audits.

## Boundaries

- Do not modify the protected artifact or schema version 1 manifest.
- Do not infer a generator, source instructions, or rendered pattern.
- Do not weaken existing checksum, mode, line-ending, schema, or provenance
  checks.
