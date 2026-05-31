# claude-container

`--dangerously-skip-permissions` を安全に使うための Docker コンテナ上の Claude Code 実行環境。

## 構成

```
claude-container/
├── Dockerfile              # Claude Code + 各種 CLI ツールのイメージ定義
├── setup-competitive.sh    # 競技プログラミング環境のインストールスクリプト
├── build.sh                # イメージビルドスクリプト
└── claude-c                # どこからでも呼び出せる起動スクリプト
```

ローカルのシンボリックリンク：

| リンク元 | リンク先 |
|----------|----------|
| `~/claude-container` | このディレクトリ |
| `~/.local/bin/claude-c` | `claude-c` スクリプト |

## 含まれるツール

**常時**
- **Claude Code** (`@anthropic-ai/claude-code`)
- **GitHub CLI** (`gh`)
- `git`, `tmux`, `curl`, `wget`, `jq`, `ripgrep`, `fzf`, `vim`

**`--competitive` ビルド時のみ**
- `g++`、`python3`、`uv`
- **Rust** (`cargo`, `rustc`)

## セットアップ

### 1. シンボリックリンクを作成

```bash
REPO_DIR=/path/to/claude-container   # このリポジトリをクローンしたパスに変更

ln -s "$REPO_DIR" ~/claude-container
ln -s "$REPO_DIR/claude-c" ~/.local/bin/claude-c
```

`~/.local/bin` が PATH に含まれていることを確認してください。

```bash
# ~/.zshrc または ~/.bashrc に追加
export PATH="$HOME/.local/bin:$PATH"
```

### 2. イメージをビルド

```bash
# 通常ビルド
~/claude-container/build.sh

# 競技プログラミング環境込みでビルド（g++, Python, uv, Rust を追加）
~/claude-container/build.sh --competitive
```

## 使い方

任意のディレクトリで `claude-c` を実行するだけです。

```bash
claude-c
```

`--dangerously-skip-permissions` が自動で付与されます。追加の引数も渡せます。

```bash
claude-c --model claude-opus-4-7
```

## マウント構成

起動時に以下がコンテナへマウントされます。

| ホスト | コンテナ内 | 備考 |
|--------|-----------|------|
| `~/.claude` | `/home/ubuntu/.claude` | Claude Code の設定・キャッシュ |
| `~/.claude.json` | `/home/ubuntu/.claude.json` | Claude Code の設定ファイル |
| `~/Documents` | `/home/ubuntu/Documents` | 作業ディレクトリ群 |
| `~/.gitconfig` | `/home/ubuntu/.gitconfig` | 読み取り専用 |
| `~/.config/gh` | `/home/ubuntu/.config/gh` | gh 認証情報 |
| `~/.ssh` | `/home/ubuntu/.ssh` | 読み取り専用 |
| カレントディレクトリ | ※自動判定 | 下記参照 |

### カレントディレクトリの自動判定

- `~/Documents` 以下にいる場合 → コンテナ内の対応パスに自動 `cd`（追加マウント不要）
- それ以外の場合 → `/workspace` にマウントして起動

```bash
# 例: ~/Documents/repo/foo にいる場合
# → コンテナ内の /home/ubuntu/Documents/repo/foo で起動

# 例: ~/Desktop/bar にいる場合
# → /workspace にマウントして起動
```

## コンテナ内にいるか確認する

`/.dockerenv` ファイルの有無で判断できます。

```bash
ls /.dockerenv 2>/dev/null && echo "コンテナ内" || echo "ホスト"
```

## イメージの更新

Claude Code のバージョンを上げたい場合はイメージを再ビルドします。

```bash
~/claude-container/build.sh
```
