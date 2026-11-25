from __future__ import annotations

import json
import locale
import os
from pathlib import Path
from typing import Any


SETTINGS_VERSION = 1


def default_language() -> str:
    language = (locale.getlocale()[0] or "").lower()
    return "zh-CN" if language.startswith("zh") else "en"


def default_settings() -> dict[str, Any]:
    return {
        "version": SETTINGS_VERSION,
        "language": default_language(),
        "theme": "dark",
        "time_format": "24h",
        "always_on_top": True,
        "window": {"x": None, "y": None},
    }


def settings_path() -> Path:
    base = Path(os.environ.get("APPDATA", Path.home()))
    return base / "DesktopClock" / "settings.json"


def normalize_settings(raw: Any) -> dict[str, Any]:
    result = default_settings()
    if not isinstance(raw, dict):
        return result

    if raw.get("language") in {"zh-CN", "en"}:
        result["language"] = raw["language"]
    if raw.get("theme") in {"dark", "light"}:
        result["theme"] = raw["theme"]
    if raw.get("time_format") in {"12h", "24h"}:
        result["time_format"] = raw["time_format"]
    if isinstance(raw.get("always_on_top"), bool):
        result["always_on_top"] = raw["always_on_top"]

    window = raw.get("window")
    if isinstance(window, dict):
        for axis in ("x", "y"):
            value = window.get(axis)
            if value is None or (isinstance(value, int) and not isinstance(value, bool)):
                result["window"][axis] = value
    return result


def load_settings(path: Path | None = None) -> dict[str, Any]:
    target = path or settings_path()
    try:
        return normalize_settings(json.loads(target.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError):
        return default_settings()


def save_settings(settings: dict[str, Any], path: Path | None = None) -> None:
    target = path or settings_path()
    normalized = normalize_settings(settings)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(target)


def ensure_visible_position(
    x: int,
    y: int,
    width: int,
    height: int,
    desktop: tuple[int, int, int, int] | list[tuple[int, int, int, int]],
    visible_margin: int = 80,
) -> tuple[int, int]:
    """Keep at least part of the clock inside the virtual desktop bounds."""
    if isinstance(desktop, list):
        if not desktop:
            raise ValueError("At least one monitor is required")
        for left, top, mw, mh in desktop:
            overlap_x = min(x + width, left + mw) - max(x, left)
            overlap_y = min(y + height, top + mh) - max(y, top)
            if overlap_x >= min(visible_margin, width) and overlap_y >= min(visible_margin, height):
                return x, y
        candidates = [
            (min(max(x, left), left + max(0, mw - width)),
             min(max(y, top), top + max(0, mh - height)))
            for left, top, mw, mh in desktop
        ]
        return min(candidates, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
    left, top, desktop_width, desktop_height = desktop
    right = left + desktop_width
    bottom = top + desktop_height
    min_x = left - width + visible_margin
    max_x = right - visible_margin
    min_y = top
    max_y = bottom - visible_margin
    return min(max(x, min_x), max_x), min(max(y, min_y), max_y)

