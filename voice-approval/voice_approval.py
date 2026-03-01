#!/usr/bin/env python3
"""
voice_approval.py — Claude Code 音声承認スクリプト

別ターミナルで起動しておき、Claude Code のターミナルをフォーカスした状態で
承認ワードを発話すると Enter キーが送信される。
"""

import sys
import speech_recognition as sr
from pynput.keyboard import Key, Controller

APPROVE_WORDS = {
    "ok", "okay", "approve"
}

keyboard = Controller()


def is_approval(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(word in text_lower for word in APPROVE_WORDS)


def send_enter() -> None:
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def main() -> None:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("マイクをキャリブレーション中...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"準備完了。承認ワード ({', '.join(APPROVE_WORDS)}) を発話してください。Ctrl+C で停止。\n")

    while True:
        try:
            with mic as source:
                print("待受中...", end=" ", flush=True)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            text = None
            for lang in ["en-US"]:
                try:
                    text = recognizer.recognize_google(audio, language=lang)
                    break
                except sr.UnknownValueError:
                    continue

            if text is None:
                print("(音声を認識できませんでした)")
                continue

            print(f'認識: "{text}"')

            if is_approval(text):
                print("→ 承認ワード検出 — Enter を送信します\n")
                send_enter()
            else:
                print("→ 承認ワードではありません\n")

        except sr.WaitTimeoutError:
            print("(タイムアウト — 再待受)")
        except KeyboardInterrupt:
            print("\n停止しました。")
            sys.exit(0)


if __name__ == "__main__":
    main()
