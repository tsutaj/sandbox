#!/bin/bash

# .env ファイルから認証情報を読み込む
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [ -f "$ENV_FILE" ]; then
  # shellcheck source=/dev/null
  source "$ENV_FILE"
fi

if [ -z "$PUSHOVER_USER_KEY" ] || [ -z "$PUSHOVER_APP_TOKEN" ]; then
  echo "Error: PUSHOVER_USER_KEY and PUSHOVER_APP_TOKEN must be set in .env" >&2
  exit 1
fi

curl -s \
  --form-string "token=${PUSHOVER_APP_TOKEN}" \
  --form-string "user=${PUSHOVER_USER_KEY}" \
  --form-string "title=Claude Code" \
  --form-string "message=タスクが完了しました" \
  --form-string "priority=0" \
  --form-string "sound=magic" \
  https://api.pushover.net/1/messages.json > /dev/null 2>&1

exit 0
