# Artifact Provenance

Construction status: partially established

## Established Evidence

The local Git history shows that `gitfiti` was accumulated across exactly
2,889 commits. Each commit added one line to the file and deleted none, which
matches the preserved artifact's 2,889 lines.

- First artifact commit: `425882d4734218b7fc5b5f672611d671b22c93b7`
  added the file with the single value `0`.
- Last artifact commit: `5b41cbeb9e52af1e0ac449b779b8ff06c212f4f1`
  added the final value `8` at line 2,889.
- All 2,889 artifact commits use the subject `gitfiti` and the author identity
  `Gareth Paul Jones <gareth@garethpaul.com>`.
- Their author and committer date range is
  `2013-12-08T12:00:00-08:00` through `2014-11-29T12:00:00-08:00`.
- The artifact history is linear: it contains one root commit and no merges.

These facts establish how the checked-in file was constructed in this
repository. Author and committer dates are repository metadata; they do not by
themselves establish when an external generator was run or when a design was
created.

## Unresolved Provenance

The repository does not establish the generator, source instructions, or
intended rendered pattern behind the numeric sequence. It also does not contain
an independent source file from which `gitfiti` can be regenerated and
verified. Do not infer those details from the repository name, commit dates, or
numeric shape.

The schema version 1 manifest is intentionally unchanged because its current
fields describe artifact integrity, not externally verified provenance. Add a
new manifest provenance field only with a deliberate schema revision and a
citable source.

## Reproducing The History Audit

Run these commands from a full local clone. A shallow hosted checkout cannot
reproduce the history counts.

```bash
git rev-list --count HEAD -- gitfiti
git log --format= --numstat -- gitfiti
git log --format='%s' -- gitfiti | sort | uniq -c
git log --format='%an <%ae>' -- gitfiti | sort | uniq -c
git log --format='%aI' -- gitfiti | sort
git log --format='%cI' -- gitfiti | sort
git rev-list --count --merges HEAD -- gitfiti
git rev-list --count --max-parents=0 HEAD -- gitfiti
```

For the numstat output, 2,889 rows each report one addition and zero deletions,
for totals of 2,889 additions and zero deletions.

## Preservation Boundary

- Do not rewrite `gitfiti` from a guessed generator or visual interpretation.
- Do not treat construction history as proof of authorship or intended use.
- Preserve the artifact checksum and schema version 1 manifest until stronger,
  independently verifiable provenance is available.
