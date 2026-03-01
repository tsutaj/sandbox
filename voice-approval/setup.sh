#!/bin/bash
set -e

echo "=== voice_approval セットアップ ==="

# portaudio (pyaudio のビルドに必要)
if ! brew list portaudio &>/dev/null; then
    echo "portaudio をインストール中..."
    brew install portaudio
else
    echo "portaudio は既にインストール済みです"
fi

# venv のセットアップ
SCRIPT_DIR="$(dirname "$0")"
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "venv を作成中 (.venv)..."
    python3 -m venv "$SCRIPT_DIR/.venv"
else
    echo "venv は既に存在します (.venv)"
fi

# venv を有効化
# shellcheck disable=SC1091
source "$SCRIPT_DIR/.venv/bin/activate"

# Python 依存関係
echo "Python パッケージをインストール中..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "セットアップ完了。以下で起動できます:"
echo "  source .venv/bin/activate"
echo "  python voice_approval.py                          # ローカル使用の場合"
echo "  TMUX_SESSION=claude python ssh_server.py          # 別クライアントで使用する場合"
