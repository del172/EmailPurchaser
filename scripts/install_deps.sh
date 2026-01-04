#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip

if ! python -m pip install -r requirements.txt; then
  echo "\nDependency install failed."
  if [[ -n "${HTTPS_PROXY:-}" || -n "${HTTP_PROXY:-}" ]]; then
    echo "Detected proxy settings. Ensure your proxy allows access to https://pypi.org and https://files.pythonhosted.org."
    echo "If you have an internal mirror, set PIP_INDEX_URL and retry, e.g.:"
    echo "  export PIP_INDEX_URL=https://your-mirror/simple"
  else
    echo "No proxy detected. If outbound internet is restricted, configure HTTPS_PROXY/HTTP_PROXY or use an internal PyPI mirror."
  fi
  exit 1
fi
