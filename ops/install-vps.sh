#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="/opt/openclaw/data/workspace/daily-signal"
EXCHANGE_DIR="/var/lib/daily-signal-exchange"
SERVICE_USER="ubuntu"

[[ "$EUID" -eq 0 ]] || { echo "Run this installer as root (sudo)." >&2; exit 1; }

for command in git docker flock runuser; do
  command -v "$command" >/dev/null || { echo "Required command not found: $command" >&2; exit 1; }
done
id "$SERVICE_USER" >/dev/null 2>&1 || { echo "Service user not found: $SERVICE_USER" >&2; exit 1; }
[[ -d "$REPO_DIR/.git" ]] || { echo "Blog Git repository not found: $REPO_DIR" >&2; exit 1; }
[[ -x "$REPO_DIR/.venv/bin/python" && -x "$REPO_DIR/.venv/bin/pip" ]] || {
  echo "Create ${REPO_DIR}/.venv as ${SERVICE_USER} before installation." >&2
  exit 1
}
[[ "$(git -C "$REPO_DIR" branch --show-current)" == "main" ]] || {
  echo "Blog repository must be on main." >&2
  exit 1
}
[[ -z "$(git -C "$REPO_DIR" status --porcelain --untracked-files=no)" ]] || {
  echo "Blog repository has tracked local changes." >&2
  exit 1
}
git -C "$REPO_DIR" remote get-url origin >/dev/null
docker compose version >/dev/null
[[ -f /etc/systemd/system/daily-signal-collector@.service ]] || {
  echo "Install daily-signal-collector before the blog units." >&2
  exit 1
}
[[ -d "${EXCHANGE_DIR}/candidates" && -d "${EXCHANGE_DIR}/feedback" ]] || {
  echo "Collector exchange directories are not installed." >&2
  exit 1
}
runuser -u "$SERVICE_USER" -- test -w "${EXCHANGE_DIR}/feedback" || {
  echo "Feedback exchange is not writable by ${SERVICE_USER}." >&2
  exit 1
}

runuser -u "$SERVICE_USER" -- "${REPO_DIR}/.venv/bin/pip" install -r "${REPO_DIR}/requirements.txt"

for unit in \
  daily-signal-emma.service daily-signal-emma.timer \
  daily-signal-emma-deep-dive.service daily-signal-emma-deep-dive.timer \
  daily-signal-emma-market.service daily-signal-emma-market.timer; do
  install -m 0644 "${REPO_DIR}/ops/${unit}" "/etc/systemd/system/${unit}"
done

systemctl daemon-reload

echo "Daily Signal publisher units installed but timers were not started."
echo "After a successful collector smoke test, enable them with:"
echo "  systemctl enable --now daily-signal-emma.timer daily-signal-emma-deep-dive.timer daily-signal-emma-market.timer"
