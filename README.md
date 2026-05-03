# nf-helper

Reusable Nextflow site profiles and small operational helpers shared across
local workflow projects.

## Layout

- `conf/sites/`: standalone site profiles for Nextflow.
- `helpers/`: reusable operational shell helpers.
- `tests/`: lightweight contract and smoke tests.
- `docs/provenance.tsv`: source and rationale for migrated reusable files.

Project-specific pipeline scripts, workflow modules, containers, generated
outputs, caches, and local run artefacts are intentionally out of scope.
