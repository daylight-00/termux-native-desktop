# 0035 — Obsidian Semantic Classifier AWK Portability Fix

## Status

The first execution of:

```text
classify-control-capabilities.sh
```

failed while generating `semantic-review.tsv`.

Observed diagnostic:

```text
awk: cmd. line:3:         NR > 1 && (
awk: cmd. line:3:                    ^ unexpected newline or end of string
```

## Cause

The review filter used a multiline AWK boolean expression with a newline immediately after an opening parenthesis:

```awk
NR > 1 && (
    condition_a ||
    condition_b ||
    condition_c
) { print }
```

The AWK implementation active on the device rejected that line continuation form.

The semantic classification loop and semantic count generation occur before this review-filter stage, so the failure does not imply that `semantic-objects.tsv` or `semantic-counts.tsv` were necessarily absent or invalid. The script is rerunnable and rewrites all derived outputs deterministically from `object-identities.tsv`.

## Correction

The filter is now written as one portable expression:

```awk
NR > 1 && ($1 ~ /REVIEW$/ || $1 == "MISSING_AT_ENRICHMENT" || $1 == "UNCLASSIFIED_PATH_CLASS") { print }
```

No semantic classification rule changed.

## Interpretation

This was a harness portability defect, not an architecture finding and not a control-evidence failure.

The correct recovery is:

```text
sync fixed branch
rerun classifier only
inspect semantic counts and review set
```

No control capture and no identity enrichment rerun is required solely because of this AWK parse failure.
