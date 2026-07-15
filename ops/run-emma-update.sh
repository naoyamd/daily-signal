#!/usr/bin/env bash
set -Eeuo pipefail

EDITION="${1:-digest}"
REPO_DIR="${DAILY_SIGNAL_REPO_DIR:-/opt/openclaw/data/workspace/daily-signal}"
OPENCLAW_DIR="${OPENCLAW_DIR:-/opt/openclaw/source}"
PYTHON="${DAILY_SIGNAL_PYTHON:-${REPO_DIR}/.venv/bin/python}"
CONTAINER_REPO="/home/node/.openclaw/workspace/daily-signal"
MODEL="${DAILY_SIGNAL_MODEL:-openai/gpt-5.6-luna}"
THINKING="${DAILY_SIGNAL_THINKING:-xhigh}"
DISCORD_USER_ID="${DAILY_SIGNAL_DISCORD_USER_ID:-}"
LOCK_FILE="${DAILY_SIGNAL_LOCK_FILE:-/tmp/daily-signal-emma.lock}"

case "$EDITION" in
  digest)
    WORK_DIR="${REPO_DIR}/.daily-signal"
    CONTAINER_PROMPT="${CONTAINER_REPO}/ops/emma-cron-prompt.md"
    STATE_PATH="data/seen.json"
    ARTICLE_PATH="content/daily/$(TZ=Asia/Tokyo date +%F)-daily-signal.md"
    EDITION_LABEL="AI Digest"
    ;;
  deep-dive)
    WORK_DIR="${REPO_DIR}/.daily-signal/deep-dive"
    CONTAINER_PROMPT="${CONTAINER_REPO}/ops/emma-deep-dive-prompt.md"
    STATE_PATH="data/seen-deep-dive.json"
    ARTICLE_PATH="content/daily/$(TZ=Asia/Tokyo date +%F)-tech-deep-dive.md"
    EDITION_LABEL="Tech Deep-Dive"
    ;;
  market)
    WORK_DIR="${REPO_DIR}/.daily-signal/market"
    CONTAINER_PROMPT="${CONTAINER_REPO}/ops/emma-market-prompt.md"
    STATE_PATH="data/seen-market.json"
    ARTICLE_PATH="content/daily/stock-report-$(TZ=Asia/Tokyo date +%F).md"
    EDITION_LABEL="夕方の株式レポート"
    ;;
  *)
    echo "Unsupported edition: $EDITION" >&2
    exit 2
    ;;
esac

mkdir -p "$WORK_DIR"
exec 9>"$LOCK_FILE"
flock 9

notify() {
  local message="$1"
  [[ -n "$DISCORD_USER_ID" ]] || return 0
  docker compose -f "$OPENCLAW_DIR/docker-compose.yml" run -T --rm openclaw-cli \
    message send --channel discord --target "user:${DISCORD_USER_ID}" --message "$message" \
    >/dev/null 2>&1 || true
}

fail() {
  local line="$1"
  notify "⚠️ Daily Signal ${EDITION_LABEL}の更新が失敗しました（line ${line}）。VPSのjournalを確認してください。"
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
today="$(TZ=Asia/Tokyo date +%F)"
if [[ -f "$ARTICLE_PATH" ]]; then
  echo "${EDITION_LABEL} for ${today} already exists; nothing to do."
  notify "☕ Daily Signal: ${today}の${EDITION_LABEL}は公開済みのため、重複更新を見送りました。"
  exit 0
fi

set +e
if [[ "$EDITION" == "digest" ]]; then
  "$PYTHON" -m scripts.emma_pipeline prepare --output "$WORK_DIR/candidates.json"
else
  "$PYTHON" -m scripts.emma_legacy_editions prepare \
    --edition "$EDITION" \
    --state "$STATE_PATH" \
    --output "$WORK_DIR/candidates.json"
fi
prepare_status=$?
set -e
if [[ $prepare_status -eq 3 ]]; then
  echo "No new candidates found."
  notify "☕ Daily Signal ${EDITION_LABEL}: 新しい候補がなかったため、更新を見送りました。"
  exit 0
elif [[ $prepare_status -ne 0 ]]; then
  exit "$prepare_status"
fi

rm -f "$WORK_DIR/draft.json" "$WORK_DIR/publish-result.json" "$WORK_DIR/agent-result.json"

docker compose -f "$OPENCLAW_DIR/docker-compose.yml" run -T --rm openclaw-cli agent \
  --session-id "daily-signal-${EDITION}-${today}" \
  --model "$MODEL" \
  --thinking "$THINKING" \
  --message-file "$CONTAINER_PROMPT" \
  --json \
  --timeout 1800 \
  >"$WORK_DIR/agent-result.json"

if [[ ! -f "$WORK_DIR/draft.json" ]]; then
  echo "The editorial agent skipped ${EDITION_LABEL}; no draft was produced."
  notify "☕ Daily Signal ${EDITION_LABEL}: 公開条件を満たさなかったため、更新を見送りました。"
  exit 0
fi

if [[ "$EDITION" == "digest" ]]; then
  "$PYTHON" -m scripts.emma_pipeline publish \
    --bundle "$WORK_DIR/candidates.json" \
    --draft "$WORK_DIR/draft.json" \
    --result "$WORK_DIR/publish-result.json"
else
  "$PYTHON" -m scripts.emma_legacy_editions publish \
    --edition "$EDITION" \
    --bundle "$WORK_DIR/candidates.json" \
    --draft "$WORK_DIR/draft.json" \
    --state "$STATE_PATH" \
    --result "$WORK_DIR/publish-result.json"
fi

article="$($PYTHON -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["article"])' "$WORK_DIR/publish-result.json")"
title="$($PYTHON -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["title"])' "$WORK_DIR/publish-result.json")"

unexpected="$(git status --porcelain | cut -c4- | grep -Fvx -e "$article" -e "$STATE_PATH" || true)"
if [[ -n "$unexpected" ]]; then
  echo "The editorial agent changed files outside the publication allowlist:" >&2
  echo "$unexpected" >&2
  exit 1
fi

"$PYTHON" -m unittest discover -s tests
git add -- "$article" "$STATE_PATH"
git diff --cached --check
git config user.name "Daily Signal Editorial Bot"
git config user.email "daily-signal[bot]@users.noreply.github.com"
git commit -m "content: publish ${EDITION_LABEL} ${today}"
git push origin HEAD:main

notify "📝 Daily Signal ${EDITION_LABEL}を更新しました: ${title}"
echo "Published ${article}: ${title}"
