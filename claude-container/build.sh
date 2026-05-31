#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

COMPETITIVE=false
for arg in "$@"; do
  [[ "$arg" == "--competitive" ]] && COMPETITIVE=true
done

docker build --build-arg INSTALL_COMPETITIVE=$COMPETITIVE -t claude-code-container .
echo "Build complete: claude-code-container (competitive=$COMPETITIVE)"
