## NSFar Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

NSFar is a minimal legacy repository with a small checked-in data artifact and
no active application surface documented in the README.

The repository is useful as an archive of the original experiment. Its next
useful state is not more code by default, but enough context for a future reader
to understand why the artifact exists, how it was produced, and whether it
should be kept.

The goal is to preserve the repository without inventing behavior that is not
present in the codebase.

Current baseline: `make lint`, `make test`, `make build`, and `make check`
verify that `gitfiti` remains a 2,889-line numeric artifact with values from 0
through 17 and SHA-256
`89d4697d0d5d78624761159d4371a135124f4c10169e65018eb3b825afbb66d4`.
The artifact manifest in `docs/artifact-manifest.json` records the same
preservation metadata in machine-readable form with schema version 1, LF line
ending metadata, terminal newline state, file mode, distinct values, and
boundary values. The manifest also records a value count total so the histogram
can be checked against the artifact line count, plus sequence shape and a
run-length histogram for its zero-based ascending runs.
The schema version 1 validator also requires the manifest's exact key set so
undocumented metadata cannot accumulate silently.
Manifest value type closure keeps every scalar and nested JSON type aligned
with the schema version 1 evidence.

The current focus is:

Priority:

- Keep the existing artifact intact
- Document provenance before making functional changes
- Avoid adding generated churn without explaining the source
- Preserve the security-reporting path
- Keep artifact-shape verification available through `make check`
- Keep the artifact manifest synchronized with the preserved file
- Keep the artifact manifest schema version explicit
- Keep the manifest schema's exact key set enforced
- Keep artifact line ending metadata explicit
- Keep artifact file mode metadata explicit
- Keep repository line-ending attributes aligned with byte-sensitive artifacts
- Keep artifact distinct values explicit in the manifest
- Keep artifact boundary values explicit in the manifest
- Keep the manifest value count total explicit
- Keep the artifact sequence shape and run-length histogram explicit
- Keep `make lint`, `make test`, `make build`, and `make check` on the
  SDK-free static baseline
- Keep artifact integrity validation pinned and read-only in hosted Linux CI
- Keep hosted source retrieval credential-free after checkout
- Keep established construction-history evidence separate from unresolved
  generator and intended-pattern claims
- Keep malformed artifact rows failing cleanly without traceback output
- Ensure malformed artifact manifests fail cleanly without traceback output
- Ensure missing required files fail cleanly without traceback output
- Ensure Git index probe failures fail cleanly without traceback output
- Ensure unreadable protected artifacts fail cleanly without traceback output

Next priorities:

- Add a short README describing the repository purpose
- Identify the missing generator or source instructions, if independently
  verifiable evidence becomes available
- Add reproduction notes if the artifact can be regenerated
- Extend the artifact manifest with provenance once the source is identified
- Archive or remove obsolete files only with clear rationale

Contribution rules:

- One PR = one focused documentation, cleanup, or provenance change.
- Do not rewrite the artifact without a reproducible source.
- Explain any generated data updates.
- Keep security and ownership metadata current.
- Preserve the artifact file mode unless provenance justifies a change.
- Preserve `.gitattributes` LF rules for archive artifacts.
- Preserve the manifest value count total when changing archive metadata.
- Preserve sequence-shape metadata when changing archive metadata.
- Preserve manifest value type closure when changing archive metadata.
- Preserve manifest duplicate-key rejection when changing archive metadata.
- Run `make lint`, `make test`, `make build`, and `make check` before changing
  archive metadata.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Sparse repositories are easy to misinterpret. Do not treat the contents as an
installable tool until a maintainer has documented the intended behavior and
supported use.

## What We Will Not Merge (For Now)

- Claims about runtime behavior that the repository does not implement
- Large generated replacements without provenance
- Hidden automation or telemetry
- Unscoped rewrites before the project purpose is documented

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
