# Safe Make Root

## Problem

Whitespace-splitting Make functions and caller-controlled `MAKEFILE_LIST`
values could redirect verification away from the provenance-sensitive artifact.

## Change

- Resolve the raw Makefile path with POSIX-compatible system tooling.
- Reject non-file origins for GNU Make's automatic `MAKEFILE_LIST` value.
- Add non-mutating regressions for spaces, a literal apostrophe, and injection.

## Validation

- Run artifact integrity, manifest, hostile mutation, and root-policy checks.
- Confirm pinned Ubuntu CI and CodeQL pass at the exact pull-request head.
