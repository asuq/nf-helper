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
        self.assertIn("oist_slurm_cluster_options", text)
        self.assertIn("clusterOptions = { params.oist_slurm_cluster_options() }", text)
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
        self.assertIn("gwdg_cluster_options = { needsInternet, extraOptions ->", text)
        self.assertIn("gwdg_gpu_cluster_options", text)
        self.assertIn("gwdg_before_script", text)
        self.assertIn("withLabel: needs_internet", text)
        self.assertIn('export APPTAINERENV_http_proxy=\\"${proxyUrl}\\"', text)
        self.assertIn("withLabel: gpu", text)
        self.assertIn("ociAutoPull = true", text)
        self.assertIn("docker {", text)
        self.assertIn("enabled = false", text)
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
        self.assertIn("executor_queue_size = 30", text)
        self.assertIn("submitRateLimit = params.executor_submit_rate_limit ?: '10/1s'", text)
        self.assertIn("apptainer {", text)
        self.assertIn("enabled = true", text)
        self.assertIn("conda {", text)
        self.assertIn("enabled = false", text)
        self.assertNotIn("withLabel: assembly", text)
        self.assertNotIn("trace {", text)


if __name__ == "__main__":
    unittest.main()
