#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd -P)"

bash -n "$REPO_ROOT/helpers/cleanup_processed_sra_workdirs.sh"
bash -n "$REPO_ROOT/helpers/gwdg_promote_2h_qos.sh"

"$REPO_ROOT/helpers/cleanup_processed_sra_workdirs.sh" --help >/dev/null
"$REPO_ROOT/helpers/gwdg_promote_2h_qos.sh" --help >/dev/null

printf 'helper syntax tests passed\n'
