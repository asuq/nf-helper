"""Contract tests for reusable Nextflow site profiles."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = ROOT / "conf" / "sites"


class SiteProfileContractTestCase(unittest.TestCase):
    """Protect the public site profile surface."""

    def read_profile(self, name: str) -> str:
        """Return one site profile as text."""
        return (SITES / f"{name}.config").read_text(encoding="ascii")

    def test_oist_profile_exposes_slurm_and_container_defaults(self) -> None:
        """Keep the OIST profile reusable across projects."""
        text = self.read_profile("oist")

        self.assertIn("profiles {", text)
        self.assertIn("oist {", text)
        self.assertIn("executor = 'slurm'", text)
        self.assertIn("queue = params.slurm_queue ?: params.queue_standard", text)
        self.assertIn("clusterOptions = {", text)
        self.assertIn("params.slurm_cluster_options instanceof Boolean", text)
        self.assertIn('params.slurm_qos ? "--qos=${params.slurm_qos}" : null', text)
        self.assertIn("params.slurm_cluster_options ?: null", text)
        self.assertIn("singularity {", text)
        self.assertIn("enabled = true", text)
        self.assertIn("apptainer {", text)
        self.assertIn("cacheDir = params.apptainer_cache_dir", text)
        self.assertIn("docker {", text)
        self.assertIn("enabled = false", text)
        self.assertNotIn("withName:", text)

    def test_gwdg_profile_keeps_rich_site_behaviour(self) -> None:
        """Keep the reusable GWDG SCC settings from the source profile."""
        text = self.read_profile("gwdg")

        self.assertIn("profiles {", text)
        self.assertIn("gwdg {", text)
        self.assertIn("gwdg_default_container_cache_dir", text)
        self.assertIn("gwdg_proxy_url = 'http://www-cache.gwdg.de:3128'", text)
        self.assertIn("clusterOptions = {", text)
        self.assertIn("'-C ssd'", text)
        self.assertIn("scratch = '$LOCAL_TMPDIR'", text)
        self.assertIn("stageOutMode = 'copy'", text)
        self.assertIn("withLabel: needs_internet", text)
        self.assertIn("-C \"ssd&inet\"", text)
        self.assertIn("APPTAINERENV_http_proxy", text)
        self.assertIn("params.gwdg_proxy_url", text)
        self.assertIn("withLabel: gpu", text)
        self.assertIn("--gpus=${params.gpu_type}:${params.gpus ?: 1}", text)
        self.assertIn("params.gpu_container_options ?: '--nv'", text)
        self.assertIn("ociAutoPull = false", text)
        self.assertIn("docker {", text)
        self.assertIn("enabled = false", text)
        self.assertNotIn("slurm_cluster_options", text)
        self.assertNotIn("slurm_qos", text)
        self.assertNotIn("--qos", text)
        self.assertNotIn("DOWNLOAD_SRA_METADATA", text)
        self.assertNotIn("RESOLVE_SRR_METADATA", text)
        self.assertNotIn("DOWNLOAD_SRR", text)

    def test_marmic_profile_keeps_site_runtime_settings(self) -> None:
        """Keep Marmic scheduler and runtime defaults project-neutral."""
        text = self.read_profile("marmic")

        self.assertIn("profiles {", text)
        self.assertIn("marmic {", text)
        self.assertIn("executor = 'slurm'", text)
        self.assertIn("clusterOptions = '--export=ALL'", text)
        self.assertIn('scratch = "/scratch/${System.getenv(\'USER\')}"', text)
        self.assertIn("stageOutMode = 'copy'", text)
        self.assertIn("executor_queue_size = 30", text)
        self.assertIn("submitRateLimit = params.executor_submit_rate_limit ?: '10/1s'", text)
        self.assertIn("apptainer {", text)
        self.assertIn("enabled = true", text)
        self.assertIn("conda {", text)
        self.assertIn("enabled = false", text)
        self.assertNotIn("withLabel: assembly", text)
        self.assertNotIn("trace {", text)

    def test_viper_cpu_profile_enforces_site_and_login_node_contracts(self) -> None:
        """Keep Viper compute, local-download, and storage policies explicit."""
        text = self.read_profile("viper-cpu")

        self.assertIn("profiles {", text)
        self.assertIn("'viper-cpu' {", text)
        self.assertIn("executor = 'slurm'", text)
        self.assertIn("clusterOptions = '--export=ALL'", text)
        self.assertIn("max_memory = 2250000.MB", text)
        self.assertIn("max_cpus = 128", text)
        self.assertIn("max_time = 24.h", text)
        self.assertIn("viper_slurm_queue_size = 250", text)
        self.assertIn("queueSize = params.viper_slurm_queue_size as int", text)
        self.assertNotIn("queueSize = 0", text)
        self.assertIn("pollInterval = '30 sec'", text)
        self.assertIn("queueStatInterval = '30 sec'", text)
        self.assertIn("exitReadTimeout = '1 min'", text)
        self.assertIn("submitRateLimit = '5/1s'", text)
        self.assertIn("perCpuMemAllocation = false", text)
        self.assertIn("$local {", text)
        self.assertIn("cpus = 2", text)
        self.assertIn("memory = 32.GB", text)
        self.assertIn("withLabel: needs_internet", text)
        self.assertIn("executor = 'local'", text)
        self.assertIn("memory = 16.GB", text)
        self.assertIn("withLabel: process_local_scratch", text)
        self.assertIn("scratch = '$JOB_TMPDIR'", text)
        self.assertIn("scratch = false", text)
        self.assertIn("stageOutMode = 'copy'", text)
        self.assertLess(text.index("viper05"), text.index("process {"))
        self.assertIn("viperLaunchHost.tokenize('.')[0]", text)
        self.assertIn("viperLaunchHostShort != 'viper05'", text)
        self.assertIn("viperLaunchHostShort != 'viper05i'", text)
        self.assertNotIn("startsWith('viper05i')", text)
        self.assertIn("viper05", text)
        self.assertIn("viper05i", text)
        self.assertIn("NXF_APPTAINER_CACHEDIR", text)
        self.assertIn("viperCacheDir.toString().startsWith('/ptmp/')", text)
        self.assertNotIn("def launchHost", text)
        self.assertIn("viper_apptainer_module = 'apptainer/1.4.3'", text)
        self.assertIn("enabled = true", text)
        self.assertIn("ociAutoPull = false", text)
        self.assertIn("cleanup = false", text)
        self.assertNotIn("workDir =", text)
        self.assertNotIn("datatransfer", text)
        self.assertNotIn("withLabel: gpu", text)
        self.assertNotIn("slurm_account", text)
        self.assertNotIn("slurm_qos", text)
        self.assertNotIn("--qos", text)
        self.assertNotIn("queue =", text)


if __name__ == "__main__":
    unittest.main()
