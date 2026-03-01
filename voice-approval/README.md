# voice-approval

Claude Code のプロンプトを音声で承認するスクリプト集。

「ok」「okay」「approve」などと発話するだけで Enter キーを送信できる。

---

## シナリオ別の選択

| 使い方 | 使うファイル |
|---|---|
| 手元の Mac で Claude Code を使う | `voice_approval.py` |
| iPad / 別 PC から SSH で接続して使う | `ssh_server.py` + `web_client.html` |

---

## シナリオ 1 — ローカル使用 (`voice_approval.py`)

手元の Mac に Claude Code と音声認識スクリプトを同時に起動する構成。

### セットアップ

```bash
bash setup.sh
```

内部で以下を実行:
- `brew install portaudio` (pyaudio ビルドに必要)
- `python3 -m venv .venv` (仮想環境の作成)
- `pip install -r requirements.txt`

### 使い方

```bash
python voice_approval.py
```

1. マイクのキャリブレーションが完了すると「準備完了」と表示される
2. **Claude Code のターミナルをフォーカスした状態**で承認ワードを発話
3. Enter キーが自動送信される

> **注意**: `pynput` は現在フォーカスされているウィンドウにキーを送る。
> Claude Code のターミナルがフォーカスされていないと別のウィンドウに Enter が送られる。

---

## シナリオ 2 — SSH 経由 / iPad 対応 (`ssh_server.py`)

iPad や別 PC から SSH でリモートサーバーに接続して Claude Code を使う場合の構成。

### アーキテクチャ

```
[iPad / 別 PC のブラウザ]
        |
        | HTTP POST /approve
        v
[リモートサーバー: ssh_server.py :8765]
        |
        | tmux send-keys -t <session> Enter
        v
[Claude Code が動く tmux セッション]
```

ブラウザの [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) で音声認識し、承認ワードを検出したらサーバーの `/approve` エンドポイントに POST する。
サーバーは `tmux send-keys` で指定セッションに Enter を送信する。

> Web Speech API は **Safari (iOS 14.5 以降)** と Chrome で動作する。

### セットアップ (リモートサーバー側)

```bash
# tmux のインストール (未インストールの場合)
# Ubuntu/Debian: sudo apt install tmux
# macOS:         brew install tmux

pip install flask
```

### 使い方

**リモートサーバー側:**

```bash
# 1. tmux セッションで Claude Code を起動
tmux new -s claude
# (tmux セッション内で claude コマンドを実行)

# 2. 別ターミナルでサーバーを起動
TMUX_SESSION=claude python ssh_server.py
```

**iPad / 別 PC 側:**

同一ネットワークの場合:
```
http://<サーバーのIPアドレス>:8765
```

SSH トンネル経由の場合 (別 PC から):
```bash
ssh -L 8765:localhost:8765 user@server
# その後ブラウザで http://localhost:8765 にアクセス
```

ブラウザで開いたら:
1. `tmux セッション名` 入力欄に `claude` (セッション名) を入力
2. **「音声認識を開始」** ボタンをタップ
3. マイクの使用を許可
4. 承認ワードを発話 → Enter が送信される

### iPhone ショートカットで「Hey Siri」承認

ブラウザの Web Speech API は iOS でバックグラウンド動作しないため、
ターミナルアプリを見ながら使うには **iOS ショートカット + Siri** が最も確実。

#### 仕組み

```
「Hey Siri、承認」
    ↓
iOS ショートカット: POST /approve
    ↓
ssh_server.py → tmux send-keys Enter
```

#### ショートカットの作成手順

1. **「ショートカット」アプリ** を開き、右上の **+** をタップ
2. **「アクションを追加」** → 検索欄に `URL` と入力 → **「URLの内容を取得」** を選択
3. 以下の通り設定する:

   | 項目 | 値 |
   |---|---|
   | URL | `http://<サーバーのIP>:8765/approve` |
   | 方法 | POST |
   | リクエストの本文 | JSON |

   JSON の本文に以下のキーと値を追加:

   | キー | 値 |
   |---|---|
   | `text` | `approve` |
   | `session` | `claude` (tmux のセッション名) |

4. 画面上部のショートカット名を **「承認」** などに変更して保存

#### Siri からの呼び出し

Siri を起動し、ショートカット名をそのまま呼びかければ実行できる。

```
「Hey Siri、承認」
```

参考: [Siri でショートカットを実行する — Apple サポート](https://support.apple.com/ja-jp/guide/shortcuts/apd07c25bb38/8.0/ios/18.0)

> **サーバー IP の確認**: サーバー側で `ifconfig | grep "inet "` を実行する。

---

### ポート変更

```bash
PORT=9000 TMUX_SESSION=claude python ssh_server.py
```

### セキュリティ注意

`ssh_server.py` は認証なしで Listen する。
外部公開サーバーで使う場合は SSH トンネルを使い、`0.0.0.0` ではなく `127.0.0.1` に変更するか、ファイアウォールでポートを制限すること。

---

## ファイル構成

```
voice-approval/
├── README.md
├── requirements.txt       # SpeechRecognition, pynput, pyaudio, flask
├── setup.sh               # macOS 向けセットアップ (ローカル用)
├── voice_approval.py      # シナリオ 1: ローカル使用
├── ssh_server.py          # シナリオ 2: SSH 経由・サーバー側
└── web_client.html        # シナリオ 2: ブラウザ音声 UI
```
