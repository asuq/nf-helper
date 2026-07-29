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

## MPCDF Viper-CPU

The `viper-cpu` profile runs ordinary processes with Slurm and routes processes
labelled `needs_internet` to the login node. It is intentionally restricted to
launches from `viper05i`; the local executor admits at most two one-CPU tasks.
Slurm queue size is unlimited from Nextflow's perspective, leaving Viper's
scheduler limits authoritative.

Before launching, load the pinned Apptainer module and choose shared `/ptmp`
locations for both the container cache and Nextflow work directory:

```bash
module load apptainer/1.4.3
export NXF_APPTAINER_CACHEDIR=/ptmp/<project-or-user>/apptainer-cache

nextflow run <pipeline> \
  -profile viper-cpu \
  -w /ptmp/<project-or-user>/work
```

The profile does not use `/tmp`, generic `$TMPDIR`, `/r`, or the `datatransfer`
partition. `/ptmp` is not backed up, and inactive files are subject to the
MPCDF retention policy. Global scratch staging is disabled. Processes that
explicitly opt into `process_local_scratch` use Slurm's job-specific
`$JOB_TMPDIR` and copy declared outputs back to the shared work directory.
