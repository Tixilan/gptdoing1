import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from desktop_clock.settings import (
    ensure_visible_position,
    load_settings,
    normalize_settings,
    save_settings,
)


class SettingsTests(unittest.TestCase):
    def test_gap_between_monitors_is_not_visible(self):
        monitors = [(0, 0, 1920, 1080), (1920, 1080, 1920, 1080)]
        self.assertEqual(ensure_visible_position(2200, 100, 360, 160, monitors), (1560, 100))

    def test_negative_monitor_position_is_preserved(self):
        monitors = [(0, 0, 1920, 1080), (-1920, 0, 1920, 1080)]
        self.assertEqual(ensure_visible_position(-1200, 200, 360, 160, monitors), (-1200, 200))

    def test_disconnected_monitor_returns_to_screen(self):
        self.assertEqual(ensure_visible_position(2500, 200, 360, 160, [(0, 0, 1920, 1080)]), (1560, 200))

    @patch("desktop_clock.settings.default_language", return_value="en")
    def test_invalid_values_use_defaults(self, _language) -> None:
        value = normalize_settings({
            "language": "xx",
            "theme": "neon",
            "time_format": "clock",
            "always_on_top": "yes",
            "window": {"x": True, "y": "10"},
        })
        self.assertEqual(value["language"], "en")
        self.assertEqual(value["theme"], "dark")
        self.assertEqual(value["time_format"], "24h")
        self.assertTrue(value["always_on_top"])
        self.assertEqual(value["window"], {"x": None, "y": None})

    def test_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            expected = {
                "version": 1,
                "language": "zh-CN",
                "theme": "light",
                "time_format": "12h",
                "always_on_top": False,
                "window": {"x": -120, "y": 80},
            }
            save_settings(expected, path)
            self.assertEqual(load_settings(path), expected)

    def test_broken_json_uses_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("{broken", encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result["version"], 1)
            self.assertIn(result["language"], {"zh-CN", "en"})

    def test_unknown_fields_are_not_saved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings({"theme": "dark", "secret": "discard-me"}, path)
            self.assertNotIn("secret", json.loads(path.read_text(encoding="utf-8")))

    def test_position_is_kept_partly_visible(self) -> None:
        desktop = (-1920, 0, 3840, 1080)
        self.assertEqual(ensure_visible_position(5000, 2000, 360, 160, desktop), (1840, 1000))
        self.assertEqual(ensure_visible_position(-5000, -50, 360, 160, desktop), (-2200, 0))


if __name__ == "__main__":
    unittest.main()

