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


if __name__ == "__main__":
    unittest.main()
