# Location-Independent NSFar Verification

status: completed

## Context

The dependency-free Make aliases invoke `scripts/check-baseline.py` relative to
the caller's working directory. An absolute Makefile invocation from elsewhere
can therefore fail or inspect the wrong tree instead of this checkout.

## Objectives

- Resolve every Make alias from the checkout containing the loaded Makefile.
- Preserve the existing target graph and `PYTHON` override.
- Enforce the exact rooted recipe, operator guidance, completed status, and
  verification evidence in the active checker.
- Prove root and external-directory behavior with mutation-sensitive checks.

## Implementation Units

### Make Contract

Files: `Makefile` and `scripts/check-baseline.py`.

Derive one absolute root from the loaded Makefile and invoke the checker by
absolute path. Require the complete small Makefile so aliases, the Python
override, and path resolution cannot drift independently.

### Documentation And Evidence

Files: `README.md`, `CHANGES.md`, and this plan.

Document absolute Makefile invocation and record bounded local and hostile
mutation verification after it completes.

## Boundaries

- Do not change the 2,889-line artifact, its schema version 1 manifest,
  workflows, or repository history.
- Do not infer or recreate the unknown generator, source instructions, or
  intended rendered pattern.
- Preserve the existing stacked PR chain and exact-head evidence.

## Work Completed

- Rooted every dependency-free Make alias at the checkout containing the loaded
  Makefile while preserving the target graph and `PYTHON` override.
- Added exact Makefile, README invocation, completed status, and verification
  evidence contracts to `scripts/check-baseline.py`.
- Documented absolute Makefile invocation without changing the artifact,
  manifest, workflow, or history.

## Verification Completed

- Root and external-directory `lint`, `test`, `build`, `verify`, and `check`
  gates passed through the checkout's absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Six isolated hostile mutations covering root derivation, checker resolution,
  alias delegation, the Python override, completed plan evidence, and README
  invocation guidance were rejected by the intended contracts.
- Artifact and manifest hashes, tracked file mode, line endings, intended paths,
  secret patterns, conflict markers, generated artifacts, workflows, history,
  and credential boundaries remained unchanged or passed their audits.
