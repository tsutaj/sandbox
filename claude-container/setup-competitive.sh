#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-root}"

if [ "$MODE" = "root" ]; then
  apt-get update && apt-get install -y g++ python3 python3-pip && rm -rf /var/lib/apt/lists/*
  pip3 install --break-system-packages uv

elif [ "$MODE" = "user" ]; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
fi
