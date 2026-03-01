# claude-notification

Claude Code の承認待ちや応答完了を [Pushover](https://pushover.net/) 経由で iPhone に通知する仕組みです。

## 概要・仕組み

Claude Code のフック機能を使い、以下の2つのタイミングで iPhone にプッシュ通知を送ります。

| タイミング | フックイベント | スクリプト | 通知音 |
|---|---|---|---|
| ツール実行の承認待ち | `PermissionRequest` | `notify-pushover.sh` | siren（高優先度） |
| 応答完了 | `Stop` | `notify-stop.sh` | magic（通常優先度） |

```
【承認待ち】
Claude Code がツール実行を要求
  → PermissionRequest イベント発火
  → hooks/notify-pushover.sh が呼ばれる（tool_name・command が JSON で渡される）
  → Pushover API にリクエスト
  → iPhone に「承認待ち: Bash / ls /tmp」のような通知が届く

【応答完了】
Claude Code が応答を完了
  → Stop イベント発火
  → hooks/notify-stop.sh が呼ばれる
  → Pushover API にリクエスト
  → iPhone に「タスクが完了しました」の通知が届く
```

## 前提条件

- [Pushover](https://pushover.net/) のアカウント（有料・買い切り $5）
- iPhone に Pushover アプリをインストール済み
- Pushover の **User Key** と **App Token** を取得済み
  - User Key: Pushover ダッシュボードのトップページに表示
  - App Token: 「Your Applications」でアプリを新規作成して取得

## セットアップ手順

### 1. リポジトリをクローン（または配置）

```bash
git clone <this-repo> ~/claude-notification
```

### 2. .env ファイルを作成

```bash
cd ~/claude-notification
cp .env.example .env
```

`.env` を編集して実際のキーを設定します。

```
PUSHOVER_USER_KEY=実際のユーザーキー
PUSHOVER_APP_TOKEN=実際のアプリトークン
```

### 3. スクリプトに実行権限を付与

```bash
chmod 755 hooks/notify-pushover.sh hooks/notify-stop.sh
```

### 4. ~/.claude/settings.json を編集

`settings-snippet.json` の内容を参考に、`~/.claude/settings.json` の `hooks` セクションを追加・編集します。

`/path/to/claude-notification` はクローンした実際のパスに置き換えてください。

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/yourname/claude-notification/hooks/notify-pushover.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/yourname/claude-notification/hooks/notify-stop.sh"
          }
        ]
      }
    ]
  }
}
```

## 動作確認

承認待ち通知のテスト（`PermissionRequest` フック）：

```bash
echo '{"hook_event_name":"PermissionRequest","tool_name":"Bash","tool_input":{"command":"ls /tmp"}}' | bash hooks/notify-pushover.sh
```

完了通知のテスト（`Stop` フック）：

```bash
bash hooks/notify-stop.sh
```

それぞれ iPhone に通知が届けば設定完了です。

Claude Code を起動してツール実行の承認を求められたタイミング、および応答が完了したタイミングで通知が届くことを確認してください。

## カスタマイズ

### 承認待ち通知（notify-pushover.sh）

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `priority` | `1`（高優先度） | `-2`〜`2` で設定。`2` は確認応答必須。[詳細](https://pushover.net/api#priority) |
| `sound` | `siren` | 通知音の種類。[利用可能な音一覧](https://pushover.net/api#sounds) |

### 完了通知（notify-stop.sh）

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `priority` | `0`（通常） | 完了通知なので低めに設定 |
| `sound` | `magic` | 承認待ちとは別の音で区別 |
