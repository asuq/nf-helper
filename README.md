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

Run the dependency-locked test suite with `pixi run test`.

## MPCDF Viper-CPU

The `viper-cpu` profile runs ordinary processes with Slurm and routes processes
labelled `needs_internet` to the login node. It is intentionally restricted to
launches from `viper05i`; its runtime short hostname may be reported as
`viper05`. The local executor admits at most two one-CPU tasks. Nextflow keeps
at most 250 Slurm tasks outstanding by default, leaving headroom below Viper's
default 300-job per-user submission limit; lower this with
`--viper_slurm_queue_size` when other launches or manual jobs share the same
limit. Nextflow refreshes the batched Slurm status query every 30 seconds and
waits at most one minute for the task exit file after a job leaves the queue, so
killed and out-of-memory jobs are reported promptly.

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

## MPCDF Raven

The `raven` profile follows the same storage, internet, and Slurm-controller
policy as `viper-cpu`, while also supporting Raven's NVIDIA A100 nodes. Ordinary
CPU tasks are capped at 72 physical cores; pipelines may explicitly opt a
process into Raven hyperthreading up to `params.raven_max_cpus_ht` (144 logical
CPUs). Processes labelled `gpu` request one A100 by default, expose 18 CPU cores,
and run with Apptainer `--nv`. Valid `--gpus` values are 1, 2, and 4. Use
`--raven_gpu_constraint gpu-bw` or `no-gpu-bw` only when the interconnect class
matters.

Launch from an explicit `raven01i` through `raven04i` host, not a legacy DNS
alias. Internet-labelled work runs in the bounded two-task local executor because
Raven batch jobs cannot access the internet:

```bash
module load apptainer/1.4.3
export NXF_APPTAINER_CACHEDIR=/ptmp/<project-or-user>/apptainer-cache

nextflow run <pipeline> \
  -profile raven \
  -w /ptmp/<project-or-user>/work
```

The profile requires the Apptainer cache and work data to live on shared
`/ptmp`. It leaves partition selection to Raven's Slurm job-submit filter and
keeps at most 250 Slurm tasks outstanding, below Raven's default 300-job submit
limit.
