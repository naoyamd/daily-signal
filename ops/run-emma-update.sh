#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="${DAILY_SIGNAL_REPO_DIR:-/opt/openclaw/data/workspace/daily-signal}"
OPENCLAW_DIR="${OPENCLAW_DIR:-/opt/openclaw/source}"
PYTHON="${DAILY_SIGNAL_PYTHON:-${REPO_DIR}/.venv/bin/python}"
WORK_DIR="${REPO_DIR}/.daily-signal"
CONTAINER_REPO="/home/node/.openclaw/workspace/daily-signal"
MODEL="${DAILY_SIGNAL_MODEL:-openai/gpt-5.6-luna}"
DISCORD_USER_ID="${DAILY_SIGNAL_DISCORD_USER_ID:-}"
LOCK_FILE="${DAILY_SIGNAL_LOCK_FILE:-/tmp/daily-signal-emma.lock}"

mkdir -p "$WORK_DIR"
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "Daily Signal update is already running."; exit 0; }

notify() {
  local message="$1"
  [[ -n "$DISCORD_USER_ID" ]] || return 0
  docker compose -f "$OPENCLAW_DIR/docker-compose.yml" run -T --rm openclaw-cli \
    message send --channel discord --target "user:${DISCORD_USER_ID}" --message "$message" \
    >/dev/null 2>&1 || true
}

fail() {
  local line="$1"
  notify "⚠️ Daily SignalのEmma更新が失敗しました（line ${line}）。VPSのjournalを確認してください。"
}
trap 'fail "$LINENO"' ERR

cd "$REPO_DIR"
[[ -x "$PYTHON" ]] || { echo "Python environment not found: $PYTHON" >&2; exit 1; }
[[ "$(git branch --show-current)" == "main" ]] || { echo "Repository must be on main." >&2; exit 1; }
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || {
  echo "Refusing to run with tracked local changes." >&2
  exit 1
}

git pull --ff-only origin main

set +e
"$PYTHON" -m scripts.emma_pipeline prepare --output "$WORK_DIR/candidates.json"
prepare_status=$?
set -e
if [[ $prepare_status -eq 3 ]]; then
  echo "No new candidates found."
  notify "☕ Daily Signal: 本日は新しい候補がなかったため、更新を見送りました。"
  exit 0
elif [[ $prepare_status -ne 0 ]]; then
  exit "$prepare_status"
fi

rm -f "$WORK_DIR/draft.json" "$WORK_DIR/publish-result.json" "$WORK_DIR/agent-result.json"
today="$(TZ=Asia/Tokyo date +%F)"

docker compose -f "$OPENCLAW_DIR/docker-compose.yml" run -T --rm openclaw-cli agent \
  --session-id "daily-signal-${today}" \
  --model "$MODEL" \
  --thinking high \
  --message-file "$CONTAINER_REPO/ops/emma-cron-prompt.md" \
  --json \
  --timeout 1800 \
  >"$WORK_DIR/agent-result.json"

"$PYTHON" -m scripts.emma_pipeline publish \
  --bundle "$WORK_DIR/candidates.json" \
  --draft "$WORK_DIR/draft.json" \
  --result "$WORK_DIR/publish-result.json"

article="$($PYTHON -c 'import json; print(json.load(open(".daily-signal/publish-result.json", encoding="utf-8"))["article"])')"
title="$($PYTHON -c 'import json; print(json.load(open(".daily-signal/publish-result.json", encoding="utf-8"))["title"])')"

unexpected="$(git status --porcelain | cut -c4- | grep -Ev "^(${article}|data/seen.json)$" || true)"
if [[ -n "$unexpected" ]]; then
  echo "Emma changed files outside the publication allowlist:" >&2
  echo "$unexpected" >&2
  exit 1
fi

"$PYTHON" -m unittest discover -s tests
git add -- "$article" data/seen.json
git diff --cached --check
git config user.name "Emma Sensei"
git config user.email "emma-sensei[bot]@users.noreply.github.com"
git commit -m "content: Emma publishes daily brief ${today}"
git push origin HEAD:main

notify "📝 Daily Signalを更新しました: ${title}"
echo "Published ${article}: ${title}"
