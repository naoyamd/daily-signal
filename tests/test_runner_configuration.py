import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ops" / "run-emma-update.sh"


class RunnerConfigurationTests(unittest.TestCase):
    def test_discord_channel_takes_priority_with_user_fallback(self):
        runner = RUNNER.read_text(encoding="utf-8")

        self.assertIn('DISCORD_CHANNEL_ID="${DAILY_SIGNAL_DISCORD_CHANNEL_ID:-}"', runner)
        self.assertLess(runner.index('if [[ -n "$DISCORD_CHANNEL_ID" ]]'), runner.index('elif [[ -n "$DISCORD_USER_ID" ]]'))
        self.assertIn('target="channel:${DISCORD_CHANNEL_ID}"', runner)
        self.assertIn('target="user:${DISCORD_USER_ID}"', runner)
        self.assertIn('message send --channel discord --target "$target"', runner)

    def test_success_notification_includes_public_article_url(self):
        runner = RUNNER.read_text(encoding="utf-8")

        self.assertIn(
            'PUBLIC_BASE_URL="${DAILY_SIGNAL_PUBLIC_BASE_URL:-https://blog.nightly.dedyn.io}"',
            runner,
        )
        self.assertIn('[[ "$article_path" == content/*.md ]]', runner)
        self.assertIn('[[ "$PUBLIC_BASE_URL" == https://* ]]', runner)
        self.assertIn('relative="${article_path#content/}"', runner)
        self.assertIn('relative="${relative%.md}"', runner)
        self.assertIn('article_url="$(public_article_url "$article")"', runner)
        self.assertIn('${title} — ${article_url}', runner)

        function_start = runner.index("public_article_url() {")
        function_end = runner.index("\n}\n", function_start) + 3
        function = runner[function_start:function_end]
        script = "\n".join([
            "set -Eeuo pipefail",
            'PUBLIC_BASE_URL="https://blog.nightly.dedyn.io/"',
            function,
            'public_article_url "content/daily/2026-07-18-daily-signal.md"',
            'public_article_url "content/daily/stock-report-2026-07-18.md"',
        ])
        result = subprocess.run(
            ["bash"], input=script, capture_output=True, text=True, check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "https://blog.nightly.dedyn.io/daily/2026-07-18-daily-signal/",
                "https://blog.nightly.dedyn.io/daily/stock-report-2026-07-18/",
            ],
        )


if __name__ == "__main__":
    unittest.main()
