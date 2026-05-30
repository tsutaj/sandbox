#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
docker build -t claude-code-container .
echo "Build complete: claude-code-container"
