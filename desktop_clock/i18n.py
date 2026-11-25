from __future__ import annotations

from datetime import datetime


STRINGS = {
    "zh-CN": {
        "app_name": "桌面时钟",
        "time_format": "时间格式",
        "format_24h": "24 小时制",
        "format_12h": "12 小时制",
        "theme": "主题",
        "dark": "深色",
        "light": "浅色",
        "language": "语言",
        "chinese": "中文",
        "english": "English",
        "always_on_top": "窗口置顶",
        "reset_position": "恢复默认位置",
        "exit": "退出",
    },
    "en": {
        "app_name": "Desktop Clock",
        "time_format": "Time format",
        "format_24h": "24-hour",
        "format_12h": "12-hour",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "language": "Language",
        "chinese": "中文",
        "english": "English",
        "always_on_top": "Always on top",
        "reset_position": "Reset position",
        "exit": "Exit",
    },
}

ZH_WEEKDAYS = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
EN_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
EN_MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def text(language: str, key: str) -> str:
    return STRINGS.get(language, STRINGS["en"]).get(key, key)


def format_time(value: datetime, time_format: str) -> str:
    if time_format == "12h":
        hour = value.strftime("%I").lstrip("0") or "12"
        return f"{hour}:{value:%M:%S} {value:%p}"
    return value.strftime("%H:%M:%S")


def format_date(value: datetime, language: str) -> str:
    if language == "zh-CN":
        return f"{value.year}年{value.month:02d}月{value.day:02d}日  {ZH_WEEKDAYS[value.weekday()]}"
    return f"{EN_WEEKDAYS[value.weekday()]}, {EN_MONTHS[value.month - 1]} {value.day}, {value.year}"

