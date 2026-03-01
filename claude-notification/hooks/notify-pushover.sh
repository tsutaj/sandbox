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

# stdin から JSON を読み込む
INPUT=$(cat)

TITLE=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tool = d.get('tool_name', 'Claude Code')
print(f'承認待ち: {tool}')
" 2>/dev/null || echo "承認待ち: Claude Code")

MESSAGE=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
inp = d.get('tool_input', {})
cmd = inp.get('command') or inp.get('description')
if not cmd:
    cmd = d.get('message', '承認が必要です')
print(cmd[:200])
" 2>/dev/null || echo "承認が必要です")

curl -s \
  --form-string "token=${PUSHOVER_APP_TOKEN}" \
  --form-string "user=${PUSHOVER_USER_KEY}" \
  --form-string "title=${TITLE}" \
  --form-string "message=${MESSAGE}" \
  --form-string "priority=1" \
  --form-string "sound=siren" \
  https://api.pushover.net/1/messages.json > /dev/null 2>&1

exit 0
