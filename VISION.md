## NSFar Vision

NSFar is a minimal legacy repository with a small checked-in data artifact and
no active application surface documented in the README.

The repository is useful as an archive of the original experiment. Its next
useful state is not more code by default, but enough context for a future reader
to understand why the artifact exists, how it was produced, and whether it
should be kept.

The goal is to preserve the repository without inventing behavior that is not
present in the codebase.

The current focus is:

Priority:

- Keep the existing artifact intact
- Document provenance before making functional changes
- Avoid adding generated churn without explaining the source
- Preserve the security-reporting path

Next priorities:

- Add a short README describing the repository purpose
- Identify whether the numeric artifact is source data or generated output
- Add reproduction notes if the artifact can be regenerated
- Archive or remove obsolete files only with clear rationale

Contribution rules:

- One PR = one focused documentation, cleanup, or provenance change.
- Do not rewrite the artifact without a reproducible source.
- Explain any generated data updates.
- Keep security and ownership metadata current.

## Security And Responsible Use

Sparse repositories are easy to misinterpret. Do not treat the contents as an
installable tool until a maintainer has documented the intended behavior and
supported use.

## What We Will Not Merge For Now

- Claims about runtime behavior that the repository does not implement
- Large generated replacements without provenance
- Hidden automation or telemetry
- Unscoped rewrites before the project purpose is documented
