import unittest
from datetime import datetime

from desktop_clock.i18n import format_date, format_time, text


class I18nTests(unittest.TestCase):
    def setUp(self) -> None:
        self.value = datetime(2026, 11, 25, 13, 5, 9)

    def test_24_hour_time(self) -> None:
        self.assertEqual(format_time(self.value, "24h"), "13:05:09")

    def test_12_hour_time(self) -> None:
        self.assertEqual(format_time(self.value, "12h"), "1:05:09 PM")

    def test_chinese_date(self) -> None:
        self.assertEqual(format_date(self.value, "zh-CN"), "2026年11月25日  星期三")

    def test_english_date(self) -> None:
        self.assertEqual(format_date(self.value, "en"), "Wednesday, November 25, 2026")

    def test_unknown_language_falls_back_to_english(self) -> None:
        self.assertEqual(text("unknown", "exit"), "Exit")


if __name__ == "__main__":
    unittest.main()

