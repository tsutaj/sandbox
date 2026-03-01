#!/usr/bin/env python3
"""
ssh_server.py — SSH 経由利用向け音声承認サーバー

リモートサーバーで起動し、iPad/PC のブラウザから音声承認を受け付ける。
承認ワードを受信したら tmux send-keys で指定セッションに Enter を送信する。

使い方:
    tmux new -s claude          # Claude Code を tmux セッションで起動
    TMUX_SESSION=claude python ssh_server.py

ブラウザから http://<サーバーIP>:8765 にアクセス。
"""

import os
import subprocess
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

APPROVE_WORDS = {
    "ok", "okay", "approve"
}

DENY_WORDS = {
    "deny", "reject"
}

DEFAULT_SESSION = os.environ.get("TMUX_SESSION", "")


def is_approval(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(word in text_lower for word in APPROVE_WORDS)


def is_denial(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(word in text_lower for word in DENY_WORDS)


def send_enter(session: str) -> None:
    if not session:
        raise ValueError("tmux セッション名が指定されていません")
    subprocess.run(
        ["tmux", "send-keys", "-t", session, "Enter"],
        check=True,
        capture_output=True,
    )


def send_escape(session: str) -> None:
    if not session:
        raise ValueError("tmux セッション名が指定されていません")
    subprocess.run(
        ["tmux", "send-keys", "-t", session, "Escape"],
        check=True,
        capture_output=True,
    )


@app.route("/")
def index():
    return send_file("web_client.html")


@app.route("/approve", methods=["POST"])
def approve():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    session = data.get("session", DEFAULT_SESSION).strip()

    if not text:
        return jsonify({"status": "error", "message": "テキストが空です"}), 400

    if not is_approval(text):
        return jsonify({"status": "ignored", "text": text})

    if not session:
        return jsonify({
            "status": "error",
            "message": "tmux セッション名を指定してください (画面の入力欄 or TMUX_SESSION 環境変数)",
        }), 400

    try:
        send_enter(session)
        return jsonify({"status": "approved", "text": text, "session": session})
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": f"tmux send-keys 失敗: {e.stderr.decode().strip()}",
        }), 500


@app.route("/deny", methods=["POST"])
def deny():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    session = data.get("session", DEFAULT_SESSION).strip()

    if not text:
        return jsonify({"status": "error", "message": "テキストが空です"}), 400

    if not is_denial(text):
        return jsonify({"status": "ignored", "text": text})

    if not session:
        return jsonify({
            "status": "error",
            "message": "tmux セッション名を指定してください (画面の入力欄 or TMUX_SESSION 環境変数)",
        }), 400

    try:
        send_escape(session)
        return jsonify({"status": "denied", "text": text, "session": session})
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": f"tmux send-keys 失敗: {e.stderr.decode().strip()}",
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    print(f"サーバー起動中 → http://0.0.0.0:{port}")
    if DEFAULT_SESSION:
        print(f"対象 tmux セッション: {DEFAULT_SESSION}")
    else:
        print("警告: TMUX_SESSION が未設定です。ブラウザ画面で入力してください。")
    app.run(host="0.0.0.0", port=port, debug=False)
